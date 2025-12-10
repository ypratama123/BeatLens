"""
FastAPI application untuk BeatLens
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import time

from models import (
    RecommendationRequest, RecommendationResponse,
    SongResponse, GenresResponse, MoodsResponse, ErrorResponse
)
from db.database import get_database
from services.rule_engine import RuleEngine
from services.knn_recommender import KNNRecommender
from services.spotify_client import SpotifyClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="BeatLens API",
    description="Smart Music Recommender API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",   # Vercel deployments
        "https://beatlens.vercel.app",  # Production domain
        "https://your-custom-domain.com"  # Custom domain if any
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Global instances
db = None
rule_engine = None
knn_recommender = None
spotify_client = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global db, rule_engine, knn_recommender, spotify_client
    
    print("🚀 Starting BeatLens API...")
    
    # Initialize database
    db_url = os.getenv("DATABASE_URL", "beatlens.db")
    db = get_database(db_url)
    db.connect()
    print(f"✓ Database connected: {db_url}")
    
    # Initialize rule engine
    rule_engine = RuleEngine()
    print("✓ Rule engine initialized")
    
    # Initialize KNN recommender
    knn_recommender = KNNRecommender()
    
    # Build encoders from database
    songs = db.get_all_songs()
    if songs:
        knn_recommender.build_encoders(songs)
        print(f"✓ KNN recommender initialized with {len(songs)} songs")
    else:
        print("⚠ Warning: No songs in database. Run init_db.py first!")
    
    # Initialize Spotify client
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    spotify_client = SpotifyClient(spotify_client_id, spotify_client_secret)
    
    if spotify_client.enabled:
        print("✓ Spotify client initialized")
    else:
        print("⚠ Spotify credentials not found. Preview features will be disabled.")
    
    print("✅ BeatLens API ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if db:
        db.close()
    print("👋 BeatLens API shutdown")


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid input", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BeatLens API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db else "disconnected",
        "spotify": "enabled" if spotify_client and spotify_client.enabled else "disabled"
    }


@app.post("/api/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    """
    Get song recommendations based on mood, genre, and tempo
    """
    start_time = time.time()
    
    # Validate mood
    valid_moods = ["sedih", "happy", "galau", "chill", "semangat"]
    if request.mood not in valid_moods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid mood. Must be one of: {', '.join(valid_moods)}"
        )
    
    # Validate tempo if provided
    if request.tempo and request.tempo not in ["slow", "medium", "fast"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tempo. Must be one of: slow, medium, fast"
        )
    
    # Get all songs from database
    all_songs = db.get_all_songs()
    
    if not all_songs:
        return RecommendationResponse(
            recommendations=[],
            metadata={"count": 0, "message": "No songs in database"}
        )
    
    # Step 1: Rule-based filtering
    candidates = rule_engine.filter_by_mood(
        mood=request.mood,
        genre=request.genre,
        tempo=request.tempo,
        songs=all_songs
    )
    
    if not candidates:
        return RecommendationResponse(
            recommendations=[],
            metadata={
                "count": 0,
                "message": "Maaf, belum ada lagu yang cocok. Coba ubah genre atau tempo."
            }
        )
    
    # Step 2: KNN similarity matching
    user_profile = {
        "mood": request.mood,
        "genre": request.genre if request.genre else candidates[0]['genre'],
        "tempo": request.tempo if request.tempo else candidates[0]['tempo']
    }
    
    recommendations = knn_recommender.recommend(
        user_profile=user_profile,
        candidates=candidates,
        k=request.k
    )
    
    # Step 3: Enrich with Spotify data and generate reasons
    enriched_recommendations = []
    for song in recommendations:
        # Generate reason
        reason_parts = []
        if song.get('preliminary_score', 0) > 0.5:
            reason_parts.append("mood match")
        if song['genre'] == user_profile['genre']:
            reason_parts.append("genre match")
        if song['tempo'] == user_profile['tempo']:
            reason_parts.append("tempo match")
        
        similarity_pct = int(song['similarity_score'] * 100)
        reason_parts.append(f"{similarity_pct}% similarity")
        
        reason = " + ".join(reason_parts)
        
        # Get Spotify preview if available
        preview_url = None
        cover_url = None
        
        if spotify_client and spotify_client.enabled and song.get('spotify_id'):
            spotify_data = spotify_client.get_track_preview(song['spotify_id'])
            if spotify_data:
                preview_url = spotify_data.get('preview_url')
                cover_url = spotify_data.get('cover_url')
        
        enriched_recommendations.append({
            "id": song['id'],
            "title": song['title'],
            "artist": song['artist'],
            "genre": song['genre'],
            "mood": song['mood'],
            "tempo": song['tempo'],
            "spotify_id": song.get('spotify_id'),
            "preview_url": preview_url,
            "cover_url": cover_url,
            "similarity_score": song['similarity_score'],
            "reason": reason
        })
    
    processing_time = time.time() - start_time
    
    return RecommendationResponse(
        recommendations=enriched_recommendations,
        metadata={
            "count": len(enriched_recommendations),
            "processing_time": round(processing_time, 3),
            "candidates_filtered": len(candidates)
        }
    )


@app.get("/api/song/{song_id}", response_model=SongResponse)
async def get_song(song_id: int):
    """
    Get detailed information about a specific song
    """
    song = db.get_song_by_id(song_id)
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with ID {song_id} not found"
        )
    
    # Get Spotify preview if available
    preview_url = None
    cover_url = None
    
    if spotify_client and spotify_client.enabled and song.get('spotify_id'):
        spotify_data = spotify_client.get_track_preview(song['spotify_id'])
        if spotify_data:
            preview_url = spotify_data.get('preview_url')
            cover_url = spotify_data.get('cover_url')
    
    return SongResponse(
        id=song['id'],
        title=song['title'],
        artist=song['artist'],
        genre=song['genre'],
        mood=song['mood'],
        tempo=song['tempo'],
        spotify_id=song.get('spotify_id'),
        preview_url=preview_url,
        cover_url=cover_url
    )


@app.get("/api/genres", response_model=GenresResponse)
async def get_genres():
    """
    Get list of available genres
    """
    genres = db.get_genres()
    return GenresResponse(genres=genres)


@app.get("/api/moods", response_model=MoodsResponse)
async def get_moods():
    """
    Get list of supported moods
    """
    moods = ["sedih", "happy", "galau", "chill", "semangat"]
    return MoodsResponse(moods=moods)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

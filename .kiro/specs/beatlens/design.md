# Dokumen Design

## Ringkasan

BeatLens adalah aplikasi web rekomendasi musik yang menggunakan kombinasi rule-based filtering dan algoritma KNN untuk memberikan rekomendasi lagu yang personal. Aplikasi ini dibangun dengan arsitektur client-server, dimana frontend Next.js berkomunikasi dengan backend FastAPI melalui REST API.

## Arsitektur Sistem

### Arsitektur Tingkat Tinggi

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  Next.js        │◄───────►│  FastAPI         │◄───────►│  SQLite         │
│  Frontend       │  HTTP   │  Backend         │         │  Database       │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     │ HTTPS
                                     ▼
                            ┌──────────────────┐
                            │                  │
                            │  Spotify Web API │
                            │                  │
                            └──────────────────┘
```

### Komponen Utama

1. **Frontend (Next.js + React + Tailwind CSS)**
   - Halaman utama dengan form input
   - Halaman hasil rekomendasi
   - Halaman detail lagu
   - Komponen UI reusable

2. **Backend (FastAPI + Python)**
   - REST API endpoints
   - Rule-based engine
   - KNN recommender
   - Spotify client integration
   - Database access layer

3. **Database (SQLite)**
   - Penyimpanan data lagu
   - Schema sederhana untuk MVP

4. **External API (Spotify Web API)**
   - Metadata lagu
   - Preview audio 30 detik
   - Cover album

## Komponen dan Interface

### Frontend Components

#### 1. Pages

**pages/index.jsx**
- Halaman utama aplikasi
- Menampilkan form input dan hasil rekomendasi
- Props: none
- State: mood, genre, tempo, recommendations, loading, error

**pages/song/[id].jsx**
- Halaman detail lagu
- Menampilkan informasi lengkap dan preview player
- Props: id (dari URL parameter)
- State: song, loading, error

#### 2. Components

**components/Header.jsx**
```javascript
Props: none
Renders: Logo BeatLens, navigation menu
```

**components/MoodSelector.jsx**
```javascript
Props: 
  - value: string (selected mood)
  - onChange: function
Renders: Grid of mood buttons with icons
Moods: sedih, happy, galau, chill, semangat
```

**components/GenreSelector.jsx**
```javascript
Props:
  - value: string (selected genre)
  - onChange: function
  - genres: array (list of available genres)
Renders: Dropdown select element
```

**components/TempoSelector.jsx**
```javascript
Props:
  - value: string (selected tempo)
  - onChange: function
Renders: Radio buttons for slow/medium/fast
```

**components/SongCard.jsx**
```javascript
Props:
  - song: object {id, title, artist, spotify_id, reason, cover_url}
  - onPlay: function (optional)
Renders: Card with cover, title, artist, reason, play button
```

**components/AudioPreview.jsx**
```javascript
Props:
  - previewUrl: string
  - title: string
Renders: Audio player with play/pause controls
```

### Backend Services

#### 1. API Routes (routes/)

**routes/recommend.py**
```python
POST /api/recommend
Request Body: {
  "mood": str,
  "genre": str (optional),
  "tempo": str (optional),
  "k": int (default: 5)
}
Response: {
  "recommendations": [
    {
      "id": int,
      "title": str,
      "artist": str,
      "genre": str,
      "mood": str,
      "tempo": str,
      "spotify_id": str,
      "reason": str,
      "similarity_score": float
    }
  ],
  "metadata": {
    "count": int,
    "processing_time": float
  }
}
```

**routes/songs.py**
```python
GET /api/song/:id
Response: {
  "id": int,
  "title": str,
  "artist": str,
  "genre": str,
  "mood": str,
  "tempo": str,
  "spotify_id": str,
  "preview_url": str,
  "cover_url": str
}

GET /api/genres
Response: {
  "genres": [str]
}

GET /api/moods
Response: {
  "moods": [str]
}
```

#### 2. Services Layer

**services/rule_engine.py**

Modul ini bertanggung jawab untuk filtering berbasis aturan.

```python
class RuleEngine:
    MOOD_RULES = {
        "sedih": {
            "preferred_genres": ["indie", "acoustic", "ballad"],
            "preferred_tempo": ["slow", "medium"]
        },
        "happy": {
            "preferred_genres": ["pop", "dance", "indie"],
            "preferred_tempo": ["medium", "fast"]
        },
        "galau": {
            "preferred_genres": ["indie", "pop"],
            "preferred_tempo": ["slow"]
        },
        "chill": {
            "preferred_genres": ["lo-fi", "acoustic", "ambient"],
            "preferred_tempo": ["slow", "medium"]
        },
        "semangat": {
            "preferred_genres": ["rock", "pop punk", "edm"],
            "preferred_tempo": ["fast", "medium"]
        }
    }
    
    def filter_by_mood(self, mood, genre, tempo, songs):
        """
        Filter songs based on mood rules
        
        Args:
            mood: str - user's mood
            genre: str - user's preferred genre (optional)
            tempo: str - user's preferred tempo (optional)
            songs: list - all available songs
            
        Returns:
            list - filtered candidate songs with preliminary scores
        """
        pass
```

**Algoritma Filtering:**
1. Ambil aturan untuk mood yang dipilih
2. Jika user memilih genre spesifik, gunakan itu sebagai prioritas
3. Filter lagu yang match preferred_genres DAN preferred_tempo
4. Jika hasil < 10 lagu, relax filter:
   - Coba hanya genre match
   - Jika masih < 10, coba hanya tempo match
5. Berikan preliminary score berdasarkan:
   - Genre match: +0.3
   - Tempo match: +0.2
   - Mood match: +0.5

**services/knn_recommender.py**

Modul ini mengimplementasikan algoritma KNN untuk similarity matching.

```python
class KNNRecommender:
    def __init__(self):
        self.genre_encoder = {}
        self.mood_encoder = {}
        self.tempo_encoder = {"slow": 0, "medium": 1, "fast": 2}
        
    def encode_features(self, song):
        """
        Convert categorical features to numerical vectors
        
        Args:
            song: dict - song with genre, mood, tempo
            
        Returns:
            numpy.array - feature vector
        """
        pass
        
    def compute_similarity(self, user_vector, song_vector):
        """
        Compute cosine similarity between vectors
        
        Formula: similarity = (A · B) / (||A|| * ||B||)
        
        Args:
            user_vector: numpy.array
            song_vector: numpy.array
            
        Returns:
            float - similarity score (0-1)
        """
        pass
        
    def recommend(self, user_profile, candidates, k=5):
        """
        Find top-k most similar songs
        
        Args:
            user_profile: dict - {mood, genre, tempo}
            candidates: list - filtered songs from rule engine
            k: int - number of recommendations
            
        Returns:
            list - top-k songs with similarity scores
        """
        pass
```

**Representasi Fitur:**
- Genre: One-hot encoding (vector dengan panjang = jumlah genre unik)
- Mood: One-hot encoding (vector dengan panjang = 5)
- Tempo: Ordinal encoding (slow=0, medium=1, fast=2)

**Contoh Feature Vector:**
```
User: mood="sedih", genre="indie", tempo="slow"
Vector: [0,0,1,0,0, 1,0,0,0,0,0,0, 0]
         ^mood^    ^genre^         ^tempo
```

**Algoritma KNN:**
1. Encode user profile menjadi feature vector
2. Encode setiap candidate song menjadi feature vector
3. Hitung cosine similarity antara user vector dan setiap song vector
4. Sort berdasarkan similarity score (descending)
5. Return top-k songs

**services/spotify_client.py**

Modul untuk integrasi dengan Spotify Web API.

```python
class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
        
    def get_access_token(self):
        """
        Get access token using Client Credentials Flow
        
        Returns:
            str - access token
        """
        pass
        
    def get_track_preview(self, spotify_id):
        """
        Get track preview URL and metadata
        
        Args:
            spotify_id: str - Spotify track ID
            
        Returns:
            dict - {preview_url, cover_url, duration}
        """
        pass
        
    def search_track(self, query):
        """
        Search for tracks (optional feature)
        
        Args:
            query: str - search query
            
        Returns:
            list - matching tracks
        """
        pass
```

**Spotify API Integration:**
- Authentication: Client Credentials Flow
- Endpoint: `https://api.spotify.com/v1/tracks/{id}`
- Response fields yang digunakan:
  - `preview_url`: URL audio preview 30 detik
  - `album.images[0].url`: Cover album
  - `name`, `artists`: Metadata

**Error Handling:**
- Jika credentials tidak ada: graceful degradation, tampilkan rekomendasi tanpa preview
- Jika rate limit: cache hasil dan retry dengan exponential backoff
- Jika track tidak memiliki preview: tampilkan pesan "Preview tidak tersedia"

#### 3. Database Layer

**db/database.py**
```python
class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None
        
    def get_all_songs(self):
        """Get all songs from database"""
        pass
        
    def get_song_by_id(self, song_id):
        """Get single song by ID"""
        pass
        
    def get_genres(self):
        """Get list of unique genres"""
        pass
        
    def get_moods(self):
        """Get list of unique moods"""
        pass
```

## Model Data

### Database Schema

**Table: songs**
```sql
CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    genre TEXT NOT NULL,
    mood TEXT NOT NULL,
    tempo TEXT NOT NULL CHECK(tempo IN ('slow', 'medium', 'fast')),
    spotify_id TEXT,
    features TEXT,  -- JSON string untuk future extensions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_genre ON songs(genre);
CREATE INDEX idx_mood ON songs(mood);
CREATE INDEX idx_tempo ON songs(tempo);
```

### Data Models (Python)

**models/song.py**
```python
from pydantic import BaseModel
from typing import Optional

class Song(BaseModel):
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    tempo: str
    spotify_id: Optional[str] = None
    features: Optional[dict] = None
    
class SongWithScore(Song):
    similarity_score: float
    reason: str
    
class RecommendationRequest(BaseModel):
    mood: str
    genre: Optional[str] = None
    tempo: Optional[str] = None
    k: int = 5
    
class RecommendationResponse(BaseModel):
    recommendations: list[SongWithScore]
    metadata: dict
```

### Seed Data Structure

**db/seed_data.json**
```json
[
  {
    "title": "Someone Like You",
    "artist": "Adele",
    "genre": "ballad",
    "mood": "sedih",
    "tempo": "slow",
    "spotify_id": "1zwMYTA5nlNjZxYrvBB2pV"
  },
  {
    "title": "Levitating",
    "artist": "Dua Lipa",
    "genre": "pop",
    "mood": "happy",
    "tempo": "fast",
    "spotify_id": "463CkQjx2Zk1yXoBuierM9"
  }
  // ... 48+ more songs
]
```

**Genre yang akan digunakan:**
- indie
- acoustic
- ballad
- pop
- dance
- lo-fi
- ambient
- rock
- pop punk
- edm

**Mood yang akan digunakan:**
- sedih
- happy
- galau
- chill
- semangat

**Tempo:**
- slow
- medium
- fast

## Error Handling

### Frontend Error Handling

1. **Network Errors**
   - Tampilkan toast notification
   - Retry button
   - Fallback UI

2. **No Results**
   - Tampilkan pesan: "Maaf, belum ada lagu yang cocok. Coba ubah genre atau tempo."
   - Suggestion untuk relax filters

3. **Loading States**
   - Skeleton loaders untuk cards
   - Progress indicator untuk API calls

### Backend Error Handling

1. **Validation Errors (400)**
   ```json
   {
     "error": "Invalid mood value",
     "detail": "Mood must be one of: sedih, happy, galau, chill, semangat"
   }
   ```

2. **Not Found (404)**
   ```json
   {
     "error": "Song not found",
     "detail": "Song with ID 123 does not exist"
   }
   ```

3. **Server Errors (500)**
   ```json
   {
     "error": "Internal server error",
     "detail": "An unexpected error occurred"
   }
   ```

4. **Spotify API Errors**
   - Graceful degradation
   - Log error untuk monitoring
   - Return data tanpa preview

## Strategi Testing

### Unit Tests

**Backend Tests:**

1. **test_rule_engine.py**
   ```python
   def test_mood_sedih_filtering():
       # Test bahwa mood "sedih" memfilter genre yang benar
       
   def test_mood_happy_filtering():
       # Test bahwa mood "happy" memfilter genre yang benar
       
   def test_relax_filter_when_few_results():
       # Test bahwa filter dilonggarkan jika hasil < 10
       
   def test_user_genre_priority():
       # Test bahwa genre user diprioritaskan
   ```

2. **test_knn_recommender.py**
   ```python
   def test_feature_encoding():
       # Test encoding categorical ke numerical
       
   def test_cosine_similarity():
       # Test perhitungan similarity dengan vektor known
       
   def test_top_k_selection():
       # Test bahwa top-k songs dipilih dengan benar
       
   def test_similarity_score_range():
       # Test bahwa score dalam range 0-1
   ```

3. **test_spotify_client.py**
   ```python
   def test_get_access_token():
       # Test mendapatkan access token
       
   def test_get_track_preview():
       # Test mengambil preview URL
       
   def test_graceful_degradation():
       # Test fallback ketika Spotify unavailable
   ```

### Integration Tests

**test_api_integration.py**
```python
def test_recommend_endpoint():
    # Test POST /api/recommend returns valid JSON
    
def test_song_detail_endpoint():
    # Test GET /api/song/:id returns song data
    
def test_genres_endpoint():
    # Test GET /api/genres returns genre list
    
def test_end_to_end_recommendation():
    # Test full flow dari request sampai response
```

### Frontend Tests

**Component Tests (Jest + React Testing Library):**
```javascript
test('MoodSelector renders all moods', () => {
  // Test bahwa semua mood ditampilkan
});

test('SongCard displays song information', () => {
  // Test bahwa card menampilkan info dengan benar
});

test('Recommendation form submits correctly', () => {
  // Test form submission
});
```

## Deployment Strategy

### Frontend Deployment (Vercel)

1. **Build Configuration**
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": ".next",
     "framework": "nextjs"
   }
   ```

2. **Environment Variables**
   - `NEXT_PUBLIC_API_URL`: URL backend API

### Backend Deployment (Railway / Render)

1. **Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Environment Variables**
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
   - `DATABASE_URL`
   - `K` (default: 5)

3. **Database Initialization**
   - Run `python db/init_db.py` sebelum start
   - Atau gunakan startup script

### CORS Configuration

Backend harus mengizinkan requests dari frontend domain:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://beatlens.vercel.app", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance Considerations

1. **Caching**
   - Cache Spotify access token (expires in 1 hour)
   - Cache genre/mood lists (static data)
   - Consider caching popular recommendations

2. **Database Optimization**
   - Index pada genre, mood, tempo columns
   - Limit query results
   - Use connection pooling

3. **Frontend Optimization**
   - Lazy load song detail page
   - Optimize images (Next.js Image component)
   - Debounce form inputs jika ada search

4. **API Rate Limiting**
   - Implement rate limiting untuk prevent abuse
   - Spotify API: handle rate limits gracefully

## Security Considerations

1. **Environment Variables**
   - Jangan commit credentials ke git
   - Use `.env` files (gitignored)
   - Validate all environment variables on startup

2. **Input Validation**
   - Validate mood, genre, tempo values
   - Sanitize user inputs
   - Use Pydantic models untuk validation

3. **API Security**
   - CORS configuration
   - Rate limiting
   - Input sanitization

4. **Spotify Credentials**
   - Use Client Credentials Flow (tidak perlu user OAuth untuk MVP)
   - Store credentials securely
   - Rotate credentials periodically

## Future Enhancements

1. **User Authentication**
   - OAuth Spotify untuk full playback
   - Save playlists ke Spotify account
   - User history dan favorites

2. **Advanced Features**
   - Auto-recommend berdasarkan waktu (pagi/siang/malam)
   - Collaborative filtering
   - User feedback untuk improve recommendations

3. **Analytics**
   - Track recommendation accuracy
   - User behavior analytics
   - A/B testing untuk algorithm improvements

4. **Mobile App**
   - React Native version
   - Offline mode dengan cached recommendations

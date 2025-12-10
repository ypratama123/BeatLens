"""
Pydantic models untuk request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class RecommendationRequest(BaseModel):
    """Request model untuk recommendation endpoint"""
    mood: str = Field(..., description="User's mood (sedih/happy/galau/chill/semangat)")
    genre: Optional[str] = Field(None, description="Preferred genre (optional)")
    tempo: Optional[str] = Field(None, description="Preferred tempo (slow/medium/fast, optional)")
    k: int = Field(5, description="Number of recommendations", ge=1, le=20)


class SongResponse(BaseModel):
    """Response model untuk single song"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    tempo: str
    spotify_id: Optional[str] = None
    preview_url: Optional[str] = None
    cover_url: Optional[str] = None


class SongWithScore(SongResponse):
    """Song dengan similarity score dan reason"""
    similarity_score: float
    reason: str


class RecommendationResponse(BaseModel):
    """Response model untuk recommendations"""
    recommendations: List[SongWithScore]
    metadata: dict


class GenresResponse(BaseModel):
    """Response model untuk genres list"""
    genres: List[str]


class MoodsResponse(BaseModel):
    """Response model untuk moods list"""
    moods: List[str]


class ErrorResponse(BaseModel):
    """Response model untuk errors"""
    error: str
    detail: Optional[str] = None

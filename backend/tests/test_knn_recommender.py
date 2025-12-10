"""
Tests untuk KNN recommender
"""
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.knn_recommender import KNNRecommender


@pytest.fixture
def recommender():
    """Create KNN recommender instance"""
    return KNNRecommender()


@pytest.fixture
def sample_songs():
    """Create sample songs"""
    return [
        {"id": 1, "title": "Song 1", "genre": "indie", "mood": "sedih", "tempo": "slow"},
        {"id": 2, "title": "Song 2", "genre": "pop", "mood": "happy", "tempo": "fast"},
        {"id": 3, "title": "Song 3", "genre": "rock", "mood": "semangat", "tempo": "fast"},
        {"id": 4, "title": "Song 4", "genre": "indie", "mood": "chill", "tempo": "medium"},
        {"id": 5, "title": "Song 5", "genre": "pop", "mood": "galau", "tempo": "slow"},
    ]


def test_build_encoders(recommender, sample_songs):
    """Test building encoders dari dataset"""
    recommender.build_encoders(sample_songs)
    
    # Check genre encoder
    assert len(recommender.genre_encoder) > 0
    assert "indie" in recommender.genre_encoder
    assert "pop" in recommender.genre_encoder
    assert "rock" in recommender.genre_encoder
    
    # Check mood encoder
    assert len(recommender.mood_encoder) > 0
    assert "sedih" in recommender.mood_encoder
    assert "happy" in recommender.mood_encoder
    assert "semangat" in recommender.mood_encoder
    
    # Check lists are sorted
    assert recommender.genre_list == sorted(recommender.genre_list)
    assert recommender.mood_list == sorted(recommender.mood_list)


def test_encode_features(recommender, sample_songs):
    """Test encoding categorical features to numerical"""
    recommender.build_encoders(sample_songs)
    
    # Encode a song
    vector = recommender.encode_features({"genre": "indie", "mood": "sedih", "tempo": "slow"})
    
    # Check vector is numpy array
    assert isinstance(vector, np.ndarray)
    
    # Check vector length
    expected_length = len(recommender.mood_list) + len(recommender.genre_list) + 1
    assert len(vector) == expected_length
    
    # Check values are in valid range
    assert np.all(vector >= 0)
    assert np.all(vector <= 1)


def test_tempo_encoding(recommender, sample_songs):
    """Test tempo ordinal encoding"""
    recommender.build_encoders(sample_songs)
    
    # Test different tempos
    slow_vector = recommender.encode_features("pop", "happy", "slow")
    medium_vector = recommender.encode_features("pop", "happy", "medium")
    fast_vector = recommender.encode_features("pop", "happy", "fast")
    
    # Tempo is last element
    slow_tempo = slow_vector[-1]
    medium_tempo = medium_vector[-1]
    fast_tempo = fast_vector[-1]
    
    # Check ordering: slow < medium < fast
    assert slow_tempo < medium_tempo < fast_tempo


def test_compute_similarity_identical(recommender, sample_songs):
    """Test similarity of identical vectors is 1.0"""
    recommender.build_encoders(sample_songs)
    
    vector = recommender.encode_features("indie", "sedih", "slow")
    similarity = recommender.compute_similarity(vector, vector)
    
    assert abs(similarity - 1.0) < 0.01  # Should be very close to 1.0


def test_compute_similarity_different(recommender, sample_songs):
    """Test similarity of different vectors"""
    recommender.build_encoders(sample_songs)
    
    vector1 = recommender.encode_features("indie", "sedih", "slow")
    vector2 = recommender.encode_features("rock", "semangat", "fast")
    
    similarity = recommender.compute_similarity(vector1, vector2)
    
    # Should be less than 1.0 since vectors are different
    assert 0.0 <= similarity < 1.0


def test_compute_similarity_range(recommender, sample_songs):
    """Test similarity score is in range [0, 1]"""
    recommender.build_encoders(sample_songs)
    
    # Test multiple combinations
    for _ in range(10):
        vector1 = recommender.encode_features("indie", "sedih", "slow")
        vector2 = recommender.encode_features("pop", "happy", "fast")
        
        similarity = recommender.compute_similarity(vector1, vector2)
        
        assert 0.0 <= similarity <= 1.0


def test_recommend_basic(recommender, sample_songs):
    """Test basic recommendation"""
    recommender.build_encoders(sample_songs)
    
    user_profile = {
        "mood": "sedih",
        "genre": "indie",
        "tempo": "slow"
    }
    
    recommendations = recommender.recommend(user_profile, sample_songs, k=3)
    
    # Should return 3 recommendations
    assert len(recommendations) == 3
    
    # Each recommendation should have similarity_score
    for rec in recommendations:
        assert "similarity_score" in rec
        assert 0.0 <= rec["similarity_score"] <= 1.0


def test_recommend_sorted_by_similarity(recommender, sample_songs):
    """Test recommendations are sorted by similarity (descending)"""
    recommender.build_encoders(sample_songs)
    
    user_profile = {
        "mood": "sedih",
        "genre": "indie",
        "tempo": "slow"
    }
    
    recommendations = recommender.recommend(user_profile, sample_songs, k=5)
    
    # Check sorting
    for i in range(len(recommendations) - 1):
        assert recommendations[i]["similarity_score"] >= recommendations[i+1]["similarity_score"]


def test_recommend_top_k(recommender, sample_songs):
    """Test top-k selection"""
    recommender.build_encoders(sample_songs)
    
    user_profile = {
        "mood": "happy",
        "genre": "pop",
        "tempo": "fast"
    }
    
    # Request 2 recommendations
    recommendations = recommender.recommend(user_profile, sample_songs, k=2)
    assert len(recommendations) == 2
    
    # Request 10 recommendations (more than available)
    recommendations = recommender.recommend(user_profile, sample_songs, k=10)
    assert len(recommendations) == len(sample_songs)


def test_recommend_empty_candidates(recommender, sample_songs):
    """Test recommendation dengan empty candidates"""
    recommender.build_encoders(sample_songs)
    
    user_profile = {
        "mood": "happy",
        "genre": "pop",
        "tempo": "fast"
    }
    
    recommendations = recommender.recommend(user_profile, [], k=5)
    
    assert len(recommendations) == 0


def test_recommend_preserves_song_data(recommender, sample_songs):
    """Test bahwa recommendation preserves original song data"""
    recommender.build_encoders(sample_songs)
    
    user_profile = {
        "mood": "sedih",
        "genre": "indie",
        "tempo": "slow"
    }
    
    recommendations = recommender.recommend(user_profile, sample_songs, k=3)
    
    for rec in recommendations:
        # Check original fields are preserved
        assert "id" in rec
        assert "title" in rec
        assert "genre" in rec
        assert "mood" in rec
        assert "tempo" in rec
        
        # Check similarity_score is added
        assert "similarity_score" in rec


def test_similar_songs_higher_score(recommender, sample_songs):
    """Test bahwa lagu yang mirip mendapat score lebih tinggi"""
    recommender.build_encoders(sample_songs)
    
    # User profile: indie, sedih, slow
    user_profile = {
        "mood": "sedih",
        "genre": "indie",
        "tempo": "slow"
    }
    
    # Add candidates with varying similarity
    candidates = [
        {"id": 1, "genre": "indie", "mood": "sedih", "tempo": "slow"},  # Exact match
        {"id": 2, "genre": "indie", "mood": "sedih", "tempo": "medium"},  # Close match
        {"id": 3, "genre": "rock", "mood": "semangat", "tempo": "fast"},  # Very different
    ]
    
    recommendations = recommender.recommend(user_profile, candidates, k=3)
    
    # Exact match should have highest score
    assert recommendations[0]["id"] == 1
    assert recommendations[0]["similarity_score"] > recommendations[1]["similarity_score"]
    assert recommendations[1]["similarity_score"] > recommendations[2]["similarity_score"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

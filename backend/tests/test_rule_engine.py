"""Tests untuk rule engine"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.rule_engine import RuleEngine


@pytest.fixture
def rule_engine():
    return RuleEngine()


@pytest.fixture
def sample_songs():
    return [
        {"id": 1, "title": "Song 1", "artist": "Artist 1", "genre": "indie", "mood": "sedih", "tempo": "slow"},
        {"id": 2, "title": "Song 2", "artist": "Artist 2", "genre": "pop", "mood": "happy", "tempo": "fast"},
        {"id": 3, "title": "Song 3", "artist": "Artist 3", "genre": "rock", "mood": "semangat", "tempo": "fast"},
        {"id": 4, "title": "Song 4", "artist": "Artist 4", "genre": "acoustic", "mood": "chill", "tempo": "slow"},
        {"id": 5, "title": "Song 5", "artist": "Artist 5", "genre": "ballad", "mood": "sedih", "tempo": "slow"},
        {"id": 6, "title": "Song 6", "artist": "Artist 6", "genre": "indie", "mood": "sedih", "tempo": "medium"},
        {"id": 7, "title": "Song 7", "artist": "Artist 7", "genre": "pop", "mood": "galau", "tempo": "slow"},
        {"id": 8, "title": "Song 8", "artist": "Artist 8", "genre": "edm", "mood": "semangat", "tempo": "fast"},
    ]


def test_mood_sedih_filtering(rule_engine, sample_songs):
    """Test filtering untuk mood sedih"""
    candidates = rule_engine.filter_by_mood("sedih", None, None, sample_songs)
    
    assert len(candidates) > 0
    
    # Check bahwa lagu dengan genre indie/acoustic/ballad dan tempo slow/medium diprioritaskan
    for song in candidates:
        assert song['genre'] in ['indie', 'acoustic', 'ballad'] or song['tempo'] in ['slow', 'medium']


def test_mood_happy_filtering(rule_engine, sample_songs):
    """Test filtering untuk mood happy"""
    candidates = rule_engine.filter_by_mood("happy", None, None, sample_songs)
    
    assert len(candidates) > 0
    
    for song in candidates:
        assert song['genre'] in ['pop', 'dance', 'indie'] or song['tempo'] in ['medium', 'fast']


def test_mood_galau_filtering(rule_engine, sample_songs):
    """Test filtering untuk mood galau"""
    candidates = rule_engine.filter_by_mood("galau", None, None, sample_songs)
    
    assert len(candidates) > 0
    
    for song in candidates:
        assert song['genre'] in ['indie', 'pop'] or song['tempo'] == 'slow'


def test_mood_chill_filtering(rule_engine, sample_songs):
    """Test filtering untuk mood chill"""
    candidates = rule_engine.filter_by_mood("chill", None, None, sample_songs)
    
    assert len(candidates) > 0
    
    for song in candidates:
        assert song['genre'] in ['lo-fi', 'acoustic', 'ambient', 'indie'] or song['tempo'] in ['slow', 'medium']


def test_mood_semangat_filtering(rule_engine, sample_songs):
    """Test filtering untuk mood semangat"""
    candidates = rule_engine.filter_by_mood("semangat", None, None, sample_songs)
    
    assert len(candidates) > 0
    
    for song in candidates:
        assert song['genre'] in ['rock', 'pop punk', 'edm'] or song['tempo'] in ['fast', 'medium']


def test_user_genre_priority(rule_engine, sample_songs):
    """Test bahwa genre user diprioritaskan"""
    # User memilih mood sedih tapi genre rock (yang bukan preferred untuk sedih)
    candidates = rule_engine.filter_by_mood("sedih", "rock", None, sample_songs)
    
    # Harus ada hasil dengan genre rock
    rock_songs = [s for s in candidates if s['genre'] == 'rock']
    assert len(rock_songs) > 0


def test_relax_filter_when_few_results(rule_engine):
    """Test bahwa filter dilonggarkan jika hasil < 10"""
    # Create limited dataset
    limited_songs = [
        {"id": 1, "title": "Song 1", "artist": "Artist 1", "genre": "indie", "mood": "sedih", "tempo": "slow"},
        {"id": 2, "title": "Song 2", "artist": "Artist 2", "genre": "pop", "mood": "happy", "tempo": "fast"},
        {"id": 3, "title": "Song 3", "artist": "Artist 3", "genre": "rock", "mood": "sedih", "tempo": "fast"},
    ]
    
    candidates = rule_engine.filter_by_mood("sedih", None, None, limited_songs)
    
    # Harus ada hasil meskipun tidak semua match perfectly
    assert len(candidates) > 0


def test_preliminary_scoring(rule_engine, sample_songs):
    """Test bahwa preliminary score dihitung dengan benar"""
    candidates = rule_engine.filter_by_mood("sedih", None, None, sample_songs)
    
    # Check bahwa semua candidates punya preliminary_score
    for song in candidates:
        assert 'preliminary_score' in song
        assert 0 <= song['preliminary_score'] <= 1.0


def test_invalid_mood(rule_engine, sample_songs):
    """Test error handling untuk mood invalid"""
    with pytest.raises(ValueError):
        rule_engine.filter_by_mood("invalid_mood", None, None, sample_songs)


def test_empty_songs_list(rule_engine):
    """Test handling untuk empty songs list"""
    candidates = rule_engine.filter_by_mood("sedih", None, None, [])
    assert candidates == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Tests untuk database operations
"""
import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db.database import Database
from db.init_db import init_database


@pytest.fixture
def test_db():
    """Create a test database"""
    test_db_path = "test_beatlens.db"
    
    # Initialize test database
    init_database(test_db_path)
    
    # Create database instance
    db = Database(test_db_path)
    
    yield db
    
    # Cleanup
    db.close()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_database_initialization(test_db):
    """Test bahwa database berhasil diinisialisasi dengan data"""
    songs = test_db.get_all_songs()
    assert len(songs) > 0, "Database harus memiliki lagu"
    assert len(songs) >= 30, "Database harus memiliki minimal 30 lagu"


def test_get_all_songs(test_db):
    """Test get_all_songs returns list of songs"""
    songs = test_db.get_all_songs()
    
    assert isinstance(songs, list)
    assert len(songs) > 0
    
    # Check first song structure
    song = songs[0]
    assert 'id' in song
    assert 'title' in song
    assert 'artist' in song
    assert 'genre' in song
    assert 'mood' in song
    assert 'tempo' in song


def test_get_song_by_id(test_db):
    """Test get_song_by_id returns correct song"""
    # Get first song
    songs = test_db.get_all_songs()
    first_song = songs[0]
    
    # Get by ID
    song = test_db.get_song_by_id(first_song['id'])
    
    assert song is not None
    assert song['id'] == first_song['id']
    assert song['title'] == first_song['title']
    assert song['artist'] == first_song['artist']


def test_get_song_by_invalid_id(test_db):
    """Test get_song_by_id returns None for invalid ID"""
    song = test_db.get_song_by_id(99999)
    assert song is None


def test_get_genres(test_db):
    """Test get_genres returns list of unique genres"""
    genres = test_db.get_genres()
    
    assert isinstance(genres, list)
    assert len(genres) > 0
    
    # Check for expected genres
    expected_genres = ['indie', 'acoustic', 'ballad', 'pop', 'dance', 
                      'lo-fi', 'ambient', 'rock', 'pop punk', 'edm', 'classical']
    
    for genre in genres:
        assert genre in expected_genres


def test_get_moods(test_db):
    """Test get_moods returns list of unique moods"""
    moods = test_db.get_moods()
    
    assert isinstance(moods, list)
    assert len(moods) == 5, "Harus ada 5 mood"
    
    # Check for expected moods
    expected_moods = ['sedih', 'happy', 'galau', 'chill', 'semangat']
    
    for mood in moods:
        assert mood in expected_moods


def test_insert_song(test_db):
    """Test insert_song adds new song to database"""
    initial_count = len(test_db.get_all_songs())
    
    # Insert new song
    song_id = test_db.insert_song(
        title="Test Song",
        artist="Test Artist",
        genre="pop",
        mood="happy",
        tempo="fast",
        spotify_id="test123"
    )
    
    assert song_id > 0
    
    # Verify song was added
    new_count = len(test_db.get_all_songs())
    assert new_count == initial_count + 1
    
    # Verify song data
    song = test_db.get_song_by_id(song_id)
    assert song['title'] == "Test Song"
    assert song['artist'] == "Test Artist"
    assert song['genre'] == "pop"
    assert song['mood'] == "happy"
    assert song['tempo'] == "fast"
    assert song['spotify_id'] == "test123"


def test_required_fields(test_db):
    """Test bahwa setiap lagu memiliki field wajib"""
    songs = test_db.get_all_songs()
    
    for song in songs:
        assert song['title'], f"Song {song['id']} harus memiliki title"
        assert song['artist'], f"Song {song['id']} harus memiliki artist"
        assert song['genre'], f"Song {song['id']} harus memiliki genre"
        assert song['mood'], f"Song {song['id']} harus memiliki mood"
        assert song['tempo'], f"Song {song['id']} harus memiliki tempo"
        assert song['tempo'] in ['slow', 'medium', 'fast'], \
            f"Song {song['id']} tempo harus slow/medium/fast"


def test_mood_distribution(test_db):
    """Test bahwa setiap mood memiliki minimal 8 lagu"""
    songs = test_db.get_all_songs()
    
    mood_counts = {}
    for song in songs:
        mood = song['mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    expected_moods = ['sedih', 'happy', 'galau', 'chill', 'semangat']
    
    for mood in expected_moods:
        assert mood in mood_counts, f"Mood {mood} harus ada di database"
        assert mood_counts[mood] >= 8, \
            f"Mood {mood} harus memiliki minimal 8 lagu, found {mood_counts[mood]}"


def test_spotify_id_coverage(test_db):
    """Test bahwa minimal 80% lagu memiliki spotify_id"""
    songs = test_db.get_all_songs()
    
    with_spotify = sum(1 for song in songs if song.get('spotify_id'))
    total = len(songs)
    
    coverage = (with_spotify / total) * 100
    
    assert coverage >= 80, \
        f"Minimal 80% lagu harus memiliki spotify_id, found {coverage:.1f}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

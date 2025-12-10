"""
Database module untuk BeatLens
Mengelola koneksi dan operasi database SQLite
"""
import sqlite3
import json
from typing import List, Optional, Dict


class Database:
    """Class untuk mengelola operasi database"""
    
    def __init__(self, db_url: str = "beatlens.db"):
        """
        Initialize database connection
        
        Args:
            db_url: Path ke database SQLite
        """
        # Remove sqlite:/// prefix jika ada
        if db_url.startswith("sqlite:///"):
            db_url = db_url.replace("sqlite:///", "")
        
        self.db_url = db_url
        self.connection = None
    
    def connect(self):
        """Buat koneksi ke database"""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_url, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Tutup koneksi database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_all_songs(self) -> List[Dict]:
        """
        Get all songs from database
        
        Returns:
            List of song dictionaries
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM songs")
        rows = cursor.fetchall()
        
        songs = []
        for row in rows:
            song = dict(row)
            # Parse features JSON jika ada
            if song.get('features'):
                try:
                    song['features'] = json.loads(song['features'])
                except:
                    song['features'] = None
            songs.append(song)
        
        return songs
    
    def get_song_by_id(self, song_id: int) -> Optional[Dict]:
        """
        Get single song by ID
        
        Args:
            song_id: ID lagu
            
        Returns:
            Song dictionary atau None jika tidak ditemukan
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        row = cursor.fetchone()
        
        if row:
            song = dict(row)
            # Parse features JSON jika ada
            if song.get('features'):
                try:
                    song['features'] = json.loads(song['features'])
                except:
                    song['features'] = None
            return song
        
        return None
    
    def get_genres(self) -> List[str]:
        """
        Get list of unique genres
        
        Returns:
            List of genre strings
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT genre FROM songs ORDER BY genre")
        rows = cursor.fetchall()
        return [row['genre'] for row in rows]
    
    def get_moods(self) -> List[str]:
        """
        Get list of unique moods
        
        Returns:
            List of mood strings
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT mood FROM songs ORDER BY mood")
        rows = cursor.fetchall()
        return [row['mood'] for row in rows]
    
    def insert_song(self, title: str, artist: str, genre: str, mood: str, 
                   tempo: str, spotify_id: Optional[str] = None, 
                   features: Optional[Dict] = None) -> int:
        """
        Insert a new song into database
        
        Args:
            title: Judul lagu
            artist: Nama artis
            genre: Genre lagu
            mood: Mood lagu
            tempo: Tempo lagu (slow/medium/fast)
            spotify_id: Spotify track ID (optional)
            features: Additional features as dict (optional)
            
        Returns:
            ID lagu yang baru diinsert
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        features_json = json.dumps(features) if features else None
        
        cursor.execute("""
            INSERT INTO songs (title, artist, genre, mood, tempo, spotify_id, features)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, artist, genre, mood, tempo, spotify_id, features_json))
        
        conn.commit()
        return cursor.lastrowid


# Singleton instance
_db_instance = None


def get_database(db_url: str = "beatlens.db") -> Database:
    """
    Get database singleton instance
    
    Args:
        db_url: Path ke database SQLite
        
    Returns:
        Database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(db_url)
    return _db_instance

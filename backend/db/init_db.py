"""
Database initialization script
Membuat tabel dan mengisi dengan seed data
"""
import sqlite3
import json
import os
from pathlib import Path


def init_database(db_path: str = "beatlens.db"):
    """
    Initialize database dengan schema dan seed data
    
    Args:
        db_path: Path ke database file
    """
    # Hapus database lama jika ada (untuk development)
    if os.path.exists(db_path):
        print(f"Database {db_path} sudah ada. Menghapus...")
        os.remove(db_path)
    
    # Buat koneksi
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Membuat tabel songs...")
    
    # Buat tabel songs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL,
            mood TEXT NOT NULL,
            tempo TEXT NOT NULL CHECK(tempo IN ('slow', 'medium', 'fast')),
            spotify_id TEXT,
            features TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Buat indexes untuk performa
    print("Membuat indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_genre ON songs(genre)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mood ON songs(mood)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tempo ON songs(tempo)")
    
    conn.commit()
    print("Database schema berhasil dibuat!")
    
    # Load dan insert seed data
    seed_file = Path(__file__).parent / "seed_data.json"
    
    if seed_file.exists():
        print(f"\nMemuat seed data dari {seed_file}...")
        with open(seed_file, 'r', encoding='utf-8') as f:
            seed_data = json.load(f)
        
        print(f"Memasukkan {len(seed_data)} lagu ke database...")
        
        for song in seed_data:
            cursor.execute("""
                INSERT INTO songs (title, artist, genre, mood, tempo, spotify_id, features)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                song['title'],
                song['artist'],
                song['genre'],
                song['mood'],
                song['tempo'],
                song.get('spotify_id'),
                json.dumps(song.get('features')) if song.get('features') else None
            ))
        
        conn.commit()
        print(f"✓ Berhasil memasukkan {len(seed_data)} lagu!")
    else:
        print(f"\n⚠ Warning: Seed data file tidak ditemukan di {seed_file}")
        print("Database dibuat tanpa data awal.")
    
    # Tampilkan statistik
    cursor.execute("SELECT COUNT(*) as count FROM songs")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT genre) as count FROM songs")
    genres = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT mood) as count FROM songs")
    moods = cursor.fetchone()[0]
    
    print(f"\n=== Database Statistics ===")
    print(f"Total lagu: {total}")
    print(f"Total genre: {genres}")
    print(f"Total mood: {moods}")
    
    conn.close()
    print(f"\n✓ Database initialization selesai!")


if __name__ == "__main__":
    # Jalankan dari root directory atau backend directory
    db_path = "beatlens.db"
    
    # Jika dijalankan dari backend directory
    if os.path.basename(os.getcwd()) == "backend":
        db_path = "beatlens.db"
    # Jika dijalankan dari root directory
    elif os.path.exists("backend"):
        db_path = "backend/beatlens.db"
    
    init_database(db_path)

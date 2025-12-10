# BeatLens - Setup Instructions

## Quick Start untuk Demo

### 1. Setup Backend

```bash
# Masuk ke folder backend
cd backend

# Install dependencies Python
pip install -r requirements.txt

# Initialize database dengan seed data
python db/init_db.py

# Jalankan server (tanpa Spotify credentials untuk demo cepat)
python app.py
```

Backend akan berjalan di http://localhost:8000

### 2. Setup Frontend

Buka terminal baru:

```bash
# Masuk ke folder frontend
cd frontend

# Install dependencies Node.js
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan di http://localhost:3000

### 3. Test Aplikasi

1. Buka browser ke http://localhost:3000
2. Pilih mood (contoh: "Happy")
3. Klik "Cari Lagu 🎵"
4. Lihat rekomendasi lagu!

## Setup dengan Spotify (Opsional)

Untuk mendapatkan preview audio 30 detik:

1. Buka https://developer.spotify.com/dashboard
2. Login dan buat aplikasi baru
3. Copy Client ID dan Client Secret
4. Buat file `.env` di folder `backend/`:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
DATABASE_URL=beatlens.db
K=5
```

5. Restart backend server

## Troubleshooting

### Backend tidak bisa start
- Pastikan Python 3.11+ terinstall
- Pastikan semua dependencies terinstall: `pip install -r requirements.txt`
- Pastikan database sudah diinisialisasi: `python db/init_db.py`

### Frontend tidak bisa start
- Pastikan Node.js 18+ terinstall
- Hapus folder `node_modules` dan `.next`, lalu install ulang: `npm install`
- Pastikan backend sudah berjalan di port 8000

### Tidak ada rekomendasi
- Pastikan database sudah diinisialisasi dengan seed data
- Coba pilih mood yang berbeda
- Coba tanpa memilih genre/tempo (biarkan kosong)

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/recommend` - Get recommendations
- `GET /api/song/{id}` - Get song details
- `GET /api/genres` - Get available genres
- `GET /api/moods` - Get supported moods
- `GET /docs` - Interactive API documentation (Swagger UI)

## Testing

### Test Backend
```bash
cd backend
pytest
```

### Test API Manual
```bash
# Test health
curl http://localhost:8000/health

# Test recommendation
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"mood": "happy", "k": 5}'
```

## Demo Features

✅ Mood-based recommendation (5 moods: sedih, happy, galau, chill, semangat)
✅ Genre filtering (10+ genres)
✅ Tempo filtering (slow, medium, fast)
✅ Rule-based engine untuk mood interpretation
✅ KNN algorithm untuk similarity matching
✅ 50 lagu populer dengan 100M+ streams
✅ Beautiful UI dengan Tailwind CSS
✅ Responsive design
✅ Audio preview (jika Spotify credentials dikonfigurasi)

## Next Steps

Setelah demo berhasil, kamu bisa:
1. Tambah lebih banyak lagu ke seed_data.json
2. Setup Spotify credentials untuk preview audio
3. Deploy ke production (Vercel + Railway)
4. Tambah fitur user authentication
5. Tambah fitur save playlist

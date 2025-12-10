# Setup Spotify untuk Preview Audio

## Kenapa Preview Tidak Muncul?

Preview audio 30 detik memerlukan Spotify API credentials. Tanpa credentials, aplikasi tetap bisa memberikan rekomendasi, tapi tidak bisa memutar preview.

## Cara Setup Spotify (5 Menit)

### 1. Buat Spotify Developer Account

1. Buka https://developer.spotify.com/dashboard
2. Login dengan akun Spotify kamu (atau buat akun baru - gratis!)
3. Klik **"Create an App"**

### 2. Isi Form Aplikasi

- **App name:** BeatLens
- **App description:** Smart music recommender
- **Redirect URIs:** (kosongkan saja)
- **Which API/SDKs are you planning to use?** Pilih "Web API"
- Centang agreement dan klik **"Save"**

### 3. Copy Credentials

Setelah app dibuat:
1. Klik app yang baru dibuat
2. Klik **"Settings"** di kanan atas
3. Copy **Client ID**
4. Klik **"View client secret"** dan copy **Client Secret**

### 4. Setup di Backend

Buat file `.env` di folder `backend/`:

```bash
cd backend
```

Buat file `.env` dengan isi:

```env
SPOTIFY_CLIENT_ID=paste_client_id_disini
SPOTIFY_CLIENT_SECRET=paste_client_secret_disini
DATABASE_URL=beatlens.db
K=5
```

**Contoh:**
```env
SPOTIFY_CLIENT_ID=abc123def456ghi789
SPOTIFY_CLIENT_SECRET=xyz987uvw654rst321
DATABASE_URL=beatlens.db
K=5
```

### 5. Restart Backend

```bash
# Stop backend (Ctrl+C)
# Start lagi
python app.py
```

Kamu akan lihat pesan:
```
✓ Spotify client initialized
```

### 6. Test Preview

1. Refresh browser (http://localhost:3000)
2. Pilih mood dan klik "Cari Lagu"
3. Hover di atas cover lagu
4. Klik tombol play ▶️
5. Dengarkan preview 30 detik! 🎵

## Troubleshooting

### "Preview tidak tersedia" muncul terus

**Penyebab:** Tidak semua lagu di Spotify memiliki preview 30 detik.

**Solusi:** 
- Klik tombol "🎵 Spotify" untuk buka lagu di Spotify app
- Atau coba lagu lain yang ada preview-nya

### Backend masih bilang "Spotify credentials not found"

**Cek:**
1. File `.env` ada di folder `backend/` (bukan di root)
2. Tidak ada typo di nama variable (harus `SPOTIFY_CLIENT_ID` dan `SPOTIFY_CLIENT_SECRET`)
3. Tidak ada spasi sebelum/sesudah `=`
4. Backend sudah di-restart setelah buat `.env`

### Preview error saat play

**Penyebab:** Spotify API rate limit atau network issue.

**Solusi:**
- Tunggu beberapa detik dan coba lagi
- Refresh halaman
- Cek koneksi internet

## Fitur Tanpa Spotify

Aplikasi tetap berfungsi 100% tanpa Spotify credentials:
- ✅ Rekomendasi musik berdasarkan mood
- ✅ Filter genre dan tempo
- ✅ Algoritma KNN dan rule-based
- ✅ Tampilan lagu dengan info lengkap
- ❌ Preview audio 30 detik (butuh Spotify)
- ✅ Link ke Spotify (tetap bisa buka di Spotify app)

## Catatan Penting

- Spotify credentials **GRATIS** dan tidak ada limit untuk development
- Credentials hanya untuk backend, tidak perlu di frontend
- Jangan share credentials ke public (sudah ada di `.gitignore`)
- Untuk production, gunakan environment variables di hosting platform

## Alternatif Tanpa Setup

Jika tidak mau setup Spotify:
1. Aplikasi tetap bisa demo dengan sempurna
2. User bisa klik "🎵 Spotify" untuk buka lagu di Spotify app
3. Fokus ke fitur rekomendasi yang sudah bekerja dengan baik

---

**Need help?** Spotify Developer Docs: https://developer.spotify.com/documentation/web-api

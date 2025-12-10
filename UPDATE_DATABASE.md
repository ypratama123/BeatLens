# Update Database dengan Lagu Baru

## Lagu Baru yang Ditambahkan

Saya sudah menambahkan **25+ lagu baru** dari band legendaris:

### 🎸 Queen (5 lagu)
- Don't Stop Me Now (happy)
- We Will Rock You (semangat)
- We Are the Champions (semangat)
- Bohemian Rhapsody (semangat)
- Another One Bites the Dust (semangat)

### 🤘 Avenged Sevenfold (3 lagu)
- Nightmare (semangat)
- Hail to the King (semangat)
- Bat Country (semangat)

### 🎵 Oasis (3 lagu)
- Wonderwall (happy)
- Champagne Supernova (chill)
- Don't Look Back in Anger (chill)

### 🎸 Green Day (3 lagu)
- Basket Case (semangat)
- American Idiot (semangat)
- Boulevard of Broken Dreams (semangat)

### 🎤 Coldplay (2 lagu)
- Fix You (sedih)
- The Scientist (galau)
- Yellow (chill)

### 🇮🇩 Sheila on 7 (3 lagu)
- Sebuah Rasa (chill)
- Kamulah Satu-Satunya (semangat)
- Kita (semangat)

### 🇮🇩 Dewa 19 (4 lagu)
- Kangen (sedih)
- Separuh Nafas (sedih)
- Arjuna Mencari Cinta (semangat)
- Risalah Hati (semangat)

### 🇮🇩 Kerispatih (3 lagu)
- Menghitung Hari 2 (galau)
- Lagu Rindu (galau)
- Bila Rasaku Ini Rasamu (galau)

**Total: 75+ lagu sekarang!**

## Cara Update Database

### Langkah 1: Stop Backend

Tekan `Ctrl+C` di terminal backend untuk stop server.

### Langkah 2: Re-initialize Database

```bash
cd backend
python db/init_db.py
```

Kamu akan lihat:
```
Database beatlens.db sudah ada. Menghapus...
Membuat tabel songs...
Membuat indexes...
Database schema berhasil dibuat!

Memuat seed data dari ...seed_data.json...
Memasukkan 75 lagu ke database...
✓ Berhasil memasukkan 75 lagu!

=== Database Statistics ===
Total lagu: 75
Total genre: 10
Total mood: 5

✓ Database initialization selesai!
```

### Langkah 3: Start Backend Lagi

```bash
python app.py
```

### Langkah 4: Test di Browser

1. Refresh browser (http://localhost:3000)
2. Pilih mood "Semangat"
3. Pilih genre "Rock"
4. Klik "Cari Lagu"
5. Lihat rekomendasi dari Queen, Avenged Sevenfold, Green Day, dll!

## Distribusi Lagu per Mood

- **Sedih:** 13 lagu (Adele, Coldplay, Dewa 19, dll)
- **Happy:** 11 lagu (Queen, Oasis, Pharrell, dll)
- **Galau:** 13 lagu (Kerispatih, Olivia Rodrigo, Coldplay, dll)
- **Chill:** 14 lagu (Oasis, Coldplay, Sheila on 7, dll)
- **Semangat:** 24 lagu (Queen, Avenged Sevenfold, Green Day, Dewa 19, dll)

## Genre yang Tersedia

- rock (banyak lagu baru!)
- pop punk (Green Day, Fall Out Boy)
- pop (Sheila on 7, Kerispatih)
- ballad (Dewa 19, Adele)
- indie (Coldplay, Oasis)
- acoustic
- dance
- edm

## Tips Mencoba

**Untuk Rock Fans:**
- Mood: Semangat
- Genre: Rock
- Hasil: Queen, Avenged Sevenfold, AC/DC, Imagine Dragons

**Untuk Lagu Indonesia:**
- Mood: Galau
- Genre: Pop
- Hasil: Kerispatih, Sheila on 7

**Untuk Chill Vibes:**
- Mood: Chill
- Genre: Rock
- Hasil: Oasis, Coldplay

**Untuk Semangat:**
- Mood: Semangat
- Genre: Pop Punk
- Hasil: Green Day, Fall Out Boy

## Troubleshooting

### Database masih error "file is being used"

Backend masih running. Stop dulu dengan `Ctrl+C`.

### Lagu baru tidak muncul

1. Pastikan database sudah di-reinitialize
2. Restart backend
3. Refresh browser (hard refresh: Ctrl+Shift+R)

### Rekomendasi masih sedikit

Coba tanpa memilih genre (biarkan "Semua Genre") untuk hasil lebih banyak.

---

**Selamat mencoba! Sekarang ada 75+ lagu dari berbagai artis legendaris!** 🎵🎸🤘

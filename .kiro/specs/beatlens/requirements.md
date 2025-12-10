# Dokumen Kebutuhan

## Pendahuluan

BeatLens adalah aplikasi web rekomendasi musik cerdas yang merekomendasikan lagu berdasarkan mood, genre, dan tempo pengguna. Sistem menggabungkan rule-based filtering untuk interpretasi mood dengan algoritma KNN (K-Nearest Neighbors) untuk similarity matching. Aplikasi dibangun dengan Next.js untuk frontend dan FastAPI (Python) untuk backend API service, dengan integrasi Spotify Web API untuk metadata dan preview lagu.

Tujuan utama adalah memberikan rekomendasi musik yang personal dan relevan dengan menganalisis preferensi mood, genre, dan tempo pengguna, kemudian mencocokkannya dengan dataset lagu menggunakan kombinasi rule-based engine dan machine learning sederhana.

## Kebutuhan

### Kebutuhan 1: Input Rekomendasi Musik

**User Story:** Sebagai pengguna, saya ingin memasukkan mood saat ini, genre yang disukai, dan preferensi tempo, sehingga saya dapat menerima rekomendasi musik yang personal sesuai kondisi saya.

#### Kriteria Penerimaan

1. KETIKA pengguna mengakses halaman utama MAKA sistem HARUS menampilkan form dengan pemilih mood, dropdown genre, dan pemilih tempo
2. KETIKA pengguna memilih mood MAKA sistem HARUS menerima nilai: "sedih", "happy", "galau", "chill", "semangat"
3. KETIKA pengguna memilih genre MAKA sistem HARUS menampilkan genre yang tersedia dari database
4. KETIKA pengguna memilih tempo MAKA sistem HARUS menerima nilai: "slow", "medium", "fast", atau mengizinkan opsional
5. KETIKA pengguna mengklik tombol "Recommend" MAKA sistem HARUS mengirim preferensi ke API rekomendasi

### Kebutuhan 2: Filter Mood Berbasis Aturan

**User Story:** Sebagai pengguna, saya ingin sistem memahami pilihan mood saya, sehingga dapat memfilter lagu yang sesuai dengan kondisi emosional saya.

#### Kriteria Penerimaan

1. KETIKA pengguna memilih mood "sedih" MAKA sistem HARUS memilih genre ["indie", "acoustic", "ballad"] dan tempo ["slow", "medium"]
2. KETIKA pengguna memilih mood "happy" MAKA sistem HARUS memilih genre ["pop", "dance", "indie"] dan tempo ["medium", "fast"]
3. KETIKA pengguna memilih mood "galau" MAKA sistem HARUS memilih genre ["indie", "pop"] dan tempo ["slow"]
4. KETIKA pengguna memilih mood "chill" MAKA sistem HARUS memilih genre ["lo-fi", "acoustic", "ambient"] dan tempo ["slow", "medium"]
5. KETIKA pengguna memilih mood "semangat" MAKA sistem HARUS memilih genre ["rock", "pop punk", "edm"] dan tempo ["fast", "medium"]
6. JIKA pengguna secara eksplisit memilih genre MAKA sistem HARUS memprioritaskan genre tersebut di atas preferensi genre berbasis mood
7. JIKA hasil filter mengandung kurang dari 10 lagu MAKA sistem HARUS melonggarkan filter untuk hanya mencocokkan genre atau hanya tempo
8. KETIKA filtering selesai MAKA sistem HARUS mengembalikan daftar lagu kandidat dengan skor awal

### Kebutuhan 3: Pencocokan Kemiripan Berbasis KNN

**User Story:** Sebagai pengguna, saya ingin sistem menemukan lagu yang paling mirip dengan preferensi saya, sehingga saya menerima rekomendasi yang paling relevan.

#### Kriteria Penerimaan

1. KETIKA sistem menerima preferensi pengguna MAKA sistem HARUS mengenkode mood, genre, dan tempo sebagai vektor fitur numerik
2. KETIKA mengenkode genre MAKA sistem HARUS menggunakan one-hot encoding atau categorical indexing
3. KETIKA mengenkode mood MAKA sistem HARUS menggunakan one-hot encoding
4. KETIKA mengenkode tempo MAKA sistem HARUS memetakan "slow"=0, "medium"=1, "fast"=2
5. KETIKA menghitung kemiripan MAKA sistem HARUS menghitung jarak Euclidean atau cosine similarity antara profil pengguna dan lagu kandidat
6. KETIKA merangking kandidat MAKA sistem HARUS mengurutkan berdasarkan skor kemiripan secara ascending (untuk jarak) atau descending (untuk similarity)
7. KETIKA mengembalikan rekomendasi MAKA sistem HARUS mengembalikan top-k lagu dimana k default adalah 5
8. KETIKA parameter k diberikan MAKA sistem HARUS menggunakan nilai yang diberikan untuk jumlah rekomendasi

### Kebutuhan 4: Endpoint API Rekomendasi

**User Story:** Sebagai aplikasi frontend, saya ingin memanggil API rekomendasi, sehingga saya dapat mengambil rekomendasi lagu yang personal untuk pengguna.

#### Kriteria Penerimaan

1. KETIKA request POST dikirim ke /api/recommend MAKA sistem HARUS menerima JSON body dengan field: mood, genre, tempo, dan k opsional
2. KETIKA request valid MAKA sistem HARUS memproses rekomendasi menggunakan rule-based filtering dan KNN
3. KETIKA rekomendasi dihasilkan MAKA sistem HARUS mengembalikan JSON dengan array recommendations berisi id, title, artist, spotify_id, dan reason
4. KETIKA rekomendasi dihasilkan MAKA sistem HARUS menyertakan metadata dengan jumlah hasil
5. JIKA terjadi error MAKA sistem HARUS mengembalikan HTTP status code dan pesan error yang sesuai
6. KETIKA tidak ada lagu yang cocok MAKA sistem HARUS mengembalikan array recommendations kosong dengan pesan yang sesuai

### Kebutuhan 5: Database Lagu dan Data Awal

**User Story:** Sebagai administrator sistem, saya ingin database yang sudah terisi dengan lagu, sehingga mesin rekomendasi memiliki data untuk diproses.

#### Kriteria Penerimaan

1. KETIKA database diinisialisasi MAKA sistem HARUS membuat tabel songs dengan field: id, title, artist, genre, mood, tempo, spotify_id, features
2. KETIKA script seed dijalankan MAKA sistem HARUS mengisi database dengan 30-100 lagu sampel dari seed_data.json
3. KETIKA menyimpan lagu MAKA sistem HARUS memastikan setiap lagu memiliki field wajib: title, artist, genre, mood, tempo
4. KETIKA menyimpan lagu MAKA sistem HARUS mengizinkan spotify_id untuk nullable
5. KETIKA menyimpan lagu MAKA sistem HARUS secara opsional menyimpan features sebagai JSON untuk numeric embeddings
6. KETIKA database di-query MAKA sistem HARUS mendukung filtering berdasarkan genre, mood, dan tempo

### Kebutuhan 6: Tampilan Detail Lagu

**User Story:** Sebagai pengguna, saya ingin melihat informasi detail tentang lagu yang direkomendasikan, sehingga saya dapat mempelajari lebih lanjut sebelum mendengarkan.

#### Kriteria Penerimaan

1. KETIKA pengguna mengklik sebuah lagu MAKA sistem HARUS menavigasi ke halaman /song/[id]
2. KETIKA halaman detail lagu dimuat MAKA sistem HARUS menampilkan judul lagu, artis, genre, mood, dan tempo
3. KETIKA lagu memiliki spotify_id MAKA sistem HARUS menampilkan cover album dari Spotify
4. KETIKA lagu memiliki spotify_id MAKA sistem HARUS menyediakan player preview 30 detik
5. JIKA lagu tidak memiliki spotify_id MAKA sistem HARUS menampilkan informasi yang tersedia tanpa preview dengan baik
6. KETIKA halaman detail dimuat MAKA sistem HARUS memanggil endpoint GET /api/song/:id

### Kebutuhan 7: Integrasi Spotify

**User Story:** Sebagai pengguna, saya ingin preview lagu dari Spotify, sehingga saya dapat mendengarkan sampel sebelum memutuskan apakah saya suka rekomendasi tersebut.

#### Kriteria Penerimaan

1. KETIKA sistem membutuhkan metadata track MAKA sistem HARUS memanggil Spotify Web API dengan client credentials
2. KETIKA spotify_id tersedia MAKA sistem HARUS mengambil URL preview track, cover album, dan metadata
3. KETIKA Spotify API tidak tersedia MAKA sistem HARUS tetap berfungsi dengan baik dan menampilkan rekomendasi tanpa preview
4. KETIKA kredensial Spotify tidak dikonfigurasi MAKA sistem HARUS tetap berfungsi dengan fitur terbatas
5. JIKA rate limit tercapai MAKA sistem HARUS menangani error dengan baik dan menginformasikan pengguna

### Kebutuhan 8: Tampilan Rekomendasi

**User Story:** Sebagai pengguna, saya ingin melihat daftar lagu yang direkomendasikan dengan penjelasan, sehingga saya memahami mengapa setiap lagu direkomendasikan.

#### Kriteria Penerimaan

1. KETIKA rekomendasi diterima MAKA sistem HARUS menampilkan setiap lagu sebagai card dengan cover, judul, dan artis
2. KETIKA menampilkan rekomendasi MAKA sistem HARUS menampilkan alasan untuk setiap rekomendasi (contoh: "mood match + high similarity")
3. KETIKA rekomendasi sedang dimuat MAKA sistem HARUS menampilkan indikator loading
4. KETIKA tidak ada rekomendasi ditemukan MAKA sistem HARUS menampilkan pesan "Maaf, belum ada lagu yang cocok. Coba ubah genre atau tempo."
5. KETIKA card lagu memiliki preview MAKA sistem HARUS menyediakan tombol play untuk preview 30 detik
6. KETIKA pengguna mengklik play MAKA sistem HARUS memutar audio preview

### Kebutuhan 9: Endpoint API Metadata

**User Story:** Sebagai aplikasi frontend, saya ingin mengambil genre dan mood yang tersedia, sehingga saya dapat mengisi dropdown pilihan secara dinamis.

#### Kriteria Penerimaan

1. KETIKA request GET dikirim ke /api/genres MAKA sistem HARUS mengembalikan daftar semua genre yang tersedia dari database
2. KETIKA request GET dikirim ke /api/moods MAKA sistem HARUS mengembalikan daftar mood yang didukung
3. KETIKA request GET dikirim ke /api/song/:id MAKA sistem HARUS mengembalikan informasi detail untuk lagu yang ditentukan
4. JIKA ID lagu tidak ada MAKA sistem HARUS mengembalikan status code 404
5. KETIKA endpoint metadata dipanggil MAKA sistem HARUS mengembalikan response JSON

### Kebutuhan 10: Komponen Frontend

**User Story:** Sebagai developer, saya ingin komponen UI yang dapat digunakan kembali, sehingga interface konsisten dan mudah dipelihara.

#### Kriteria Penerimaan

1. KETIKA mood selector di-render MAKA sistem HARUS menampilkan opsi mood dengan ikon atau indikator visual
2. KETIKA genre selector di-render MAKA sistem HARUS menampilkan dropdown yang diisi dari /api/genres
3. KETIKA tempo selector di-render MAKA sistem HARUS menampilkan radio button atau toggle untuk slow/medium/fast
4. KETIKA song card di-render MAKA sistem HARUS menampilkan gambar cover, judul, artis, alasan, dan tombol preview
5. KETIKA header di-render MAKA sistem HARUS menampilkan logo "BeatLens" dan elemen navigasi

### Kebutuhan 11: Testing dan Validasi

**User Story:** Sebagai developer, saya ingin automated test untuk logika inti, sehingga saya dapat memastikan mesin rekomendasi bekerja dengan benar.

#### Kriteria Penerimaan

1. KETIKA test rule_engine dijalankan MAKA sistem HARUS memverifikasi pemetaan mood-ke-genre-tempo yang benar untuk setiap mood
2. KETIKA test knn_recommender dijalankan MAKA sistem HARUS memverifikasi perhitungan similarity dengan vektor sintetis
3. KETIKA integration test dijalankan MAKA sistem HARUS memverifikasi POST /api/recommend mengembalikan struktur JSON yang diharapkan
4. KETIKA test dijalankan MAKA sistem HARUS memvalidasi bahwa rekomendasi sesuai kriteria yang diharapkan
5. KETIKA semua test berhasil MAKA sistem HARUS mengkonfirmasi fungsionalitas inti bekerja

### Kebutuhan 12: Konfigurasi Environment

**User Story:** Sebagai administrator sistem, saya ingin mengkonfigurasi aplikasi melalui environment variables, sehingga saya dapat men-deploy di berbagai environment.

#### Kriteria Penerimaan

1. KETIKA aplikasi dimulai MAKA sistem HARUS membaca SPOTIFY_CLIENT_ID dari environment variables
2. KETIKA aplikasi dimulai MAKA sistem HARUS membaca SPOTIFY_CLIENT_SECRET dari environment variables
3. KETIKA aplikasi dimulai MAKA sistem HARUS membaca DATABASE_URL dengan nilai default "sqlite:///./beatlens.db"
4. KETIKA aplikasi dimulai MAKA sistem HARUS membaca parameter K dengan nilai default 5
5. JIKA kredensial Spotify tidak ada MAKA sistem HARUS mencatat warning dan melanjutkan tanpa integrasi Spotify

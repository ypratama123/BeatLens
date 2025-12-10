# Implementation Plan

- [x] 1. Setup struktur project dan konfigurasi awal



  - Buat folder structure untuk frontend (Next.js) dan backend (FastAPI)
  - Setup package.json untuk frontend dengan dependencies: next, react, tailwindcss
  - Setup requirements.txt untuk backend dengan dependencies: fastapi, uvicorn, pydantic, sqlite3, requests, numpy
  - Buat file .env.example untuk dokumentasi environment variables
  - Buat .gitignore untuk exclude node_modules, .env, __pycache__, database files
  - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [x] 2. Implementasi database dan seed data


  - [x] 2.1 Buat database schema dan initialization script


    - Tulis db/database.py dengan class Database dan methods: get_all_songs, get_song_by_id, get_genres, get_moods
    - Tulis db/init_db.py untuk create table songs dengan schema yang sudah didefinisikan
    - Tambahkan indexes untuk genre, mood, dan tempo columns


    - _Requirements: 5.1, 5.6_
  - [x] 2.2 Buat seed data dengan 50+ lagu

    - Buat db/seed_data.json dengan minimal 50 lagu yang mencakup semua kombinasi mood, genre, dan tempo


    - Pastikan setiap mood memiliki minimal 8-10 lagu
    - Sertakan spotify_id untuk minimal 80% lagu (gunakan Spotify track IDs yang valid)

    - _Requirements: 5.2, 5.3, 5.4_



  - [ ] 2.3 Implementasi script untuk populate database
    - Update init_db.py untuk membaca seed_data.json dan insert ke database
    - Tambahkan error handling untuk duplicate entries

    - Tulis test untuk verify data integrity setelah seeding
    - _Requirements: 5.2, 5.5_

- [x] 3. Implementasi rule-based engine

  - [x] 3.1 Buat modul rule_engine dengan mood mappings




    - Tulis services/rule_engine.py dengan class RuleEngine
    - Implementasi MOOD_RULES dictionary dengan mappings untuk semua 5 moods
    - Tulis method get_mood_preferences(mood) yang return preferred_genres dan preferred_tempo
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_


  - [x] 3.2 Implementasi filtering logic

    - Tulis method filter_by_mood(mood, genre, tempo, songs) di RuleEngine
    - Implementasi prioritas: user genre > mood preferences

    - Implementasi filter relaxation jika hasil < 10 lagu


    - Tambahkan preliminary scoring (genre match +0.3, tempo match +0.2, mood match +0.5)
    - _Requirements: 2.6, 2.7, 2.8_

  - [x] 3.3 Tulis unit tests untuk rule engine

    - Test mood_sedih_filtering: verify genre dan tempo preferences

    - Test mood_happy_filtering: verify genre dan tempo preferences
    - Test mood_galau_filtering: verify genre dan tempo preferences
    - Test mood_chill_filtering: verify genre dan tempo preferences
    - Test mood_semangat_filtering: verify genre dan tempo preferences

    - Test user_genre_priority: verify user genre overrides mood preferences
    - Test relax_filter_when_few_results: verify filter relaxation logic
    - _Requirements: 11.1_

- [x] 4. Implementasi KNN recommender


  - [x] 4.1 Buat feature encoding system



    - Tulis services/knn_recommender.py dengan class KNNRecommender
    - Implementasi method build_encoders(songs) untuk create genre dan mood encoders dari dataset
    - Implementasi method encode_features(song) untuk convert categorical ke numerical vectors
    - Implementasi tempo encoding: slow=0, medium=1, fast=2
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 4.2 Implementasi similarity calculation



    - Tulis method compute_similarity(user_vector, song_vector) menggunakan cosine similarity
    - Formula: similarity = (A · B) / (||A|| * ||B||)
    - Implementasi normalization untuk vectors
    - _Requirements: 3.5_



  - [x] 4.3 Implementasi recommendation logic

    - Tulis method recommend(user_profile, candidates, k) di KNNRecommender
    - Encode user profile menjadi feature vector
    - Compute similarity untuk semua candidates
    - Sort by similarity score (descending) dan return top-k

    - Tambahkan similarity_score ke setiap song result
    - _Requirements: 3.6, 3.7, 3.8_

  - [ ] 4.4 Tulis unit tests untuk KNN recommender
    - Test feature_encoding: verify categorical to numerical conversion
    - Test cosine_similarity: verify calculation dengan known vectors
    - Test top_k_selection: verify correct songs dipilih
    - Test similarity_score_range: verify scores dalam range 0-1

    - Test edge_case_identical_vectors: verify similarity = 1.0
    - _Requirements: 11.2_



- [ ] 5. Implementasi Spotify client integration
  - [ ] 5.1 Buat Spotify client dengan authentication
    - Tulis services/spotify_client.py dengan class SpotifyClient
    - Implementasi method get_access_token() menggunakan Client Credentials Flow
    - Implementasi token caching dan auto-refresh logic

    - Tambahkan error handling untuk authentication failures
    - _Requirements: 7.1, 7.4_
  - [ ] 5.2 Implementasi track metadata fetching
    - Tulis method get_track_preview(spotify_id) untuk fetch preview_url dan cover_url
    - Parse Spotify API response untuk extract preview_url, album.images[0].url

    - Implementasi graceful degradation jika preview tidak tersedia
    - Tambahkan rate limit handling dengan exponential backoff
    - _Requirements: 7.2, 7.3, 7.5_
  - [ ] 5.3 Tulis unit tests untuk Spotify client
    - Test get_access_token: verify token retrieval
    - Test get_track_preview: verify metadata extraction
    - Test graceful_degradation: verify fallback ketika API unavailable
    - Test rate_limit_handling: verify retry logic
    - Mock Spotify API responses untuk testing
    - _Requirements: 11.3_


- [ ] 6. Implementasi backend API endpoints
  - [x] 6.1 Setup FastAPI application

    - Tulis app.py dengan FastAPI app initialization
    - Setup CORS middleware untuk allow frontend origins
    - Setup error handlers untuk 400, 404, 500 errors
    - Implementasi startup event untuk initialize database dan encoders
    - _Requirements: 4.5_

  - [ ] 6.2 Implementasi POST /api/recommend endpoint
    - Tulis routes/recommend.py dengan endpoint handler
    - Implementasi request validation menggunakan Pydantic model RecommendationRequest
    - Integrate rule_engine.filter_by_mood() untuk get candidates
    - Integrate knn_recommender.recommend() untuk get top-k
    - Generate reason string untuk setiap recommendation
    - Return RecommendationResponse dengan recommendations dan metadata

    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [ ] 6.3 Implementasi GET /api/song/:id endpoint
    - Tulis routes/songs.py dengan endpoint handler
    - Query database untuk get song by ID
    - Jika song memiliki spotify_id, fetch preview_url dan cover_url dari Spotify
    - Return song detail dengan preview dan cover URLs

    - Handle 404 jika song tidak ditemukan
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  - [ ] 6.4 Implementasi metadata endpoints
    - Tulis GET /api/genres endpoint untuk return list of unique genres dari database
    - Tulis GET /api/moods endpoint untuk return list of supported moods

    - Cache results untuk improve performance
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  - [ ] 6.5 Tulis integration tests untuk API
    - Test POST /api/recommend returns valid JSON structure
    - Test GET /api/song/:id returns song data
    - Test GET /api/genres returns genre list
    - Test GET /api/moods returns mood list
    - Test error responses (400, 404, 500)
    - Test end-to-end recommendation flow
    - _Requirements: 11.3_

- [ ] 7. Implementasi frontend components
  - [x] 7.1 Setup Next.js application dengan Tailwind CSS

    - Initialize Next.js project di folder frontend/
    - Setup Tailwind CSS configuration
    - Buat components/ folder structure
    - Setup API client utility untuk call backend endpoints
    - _Requirements: 10.5_

  - [ ] 7.2 Buat Header component
    - Tulis components/Header.jsx dengan logo BeatLens
    - Implementasi navigation menu (Home, About)
    - Style dengan Tailwind CSS

    - _Requirements: 10.5_
  - [ ] 7.3 Buat MoodSelector component
    - Tulis components/MoodSelector.jsx dengan props: value, onChange
    - Render grid of mood buttons dengan icons untuk: sedih, happy, galau, chill, semangat
    - Implementasi active state styling

    - Tambahkan hover effects
    - _Requirements: 1.2, 10.1_
  - [ ] 7.4 Buat GenreSelector component
    - Tulis components/GenreSelector.jsx dengan props: value, onChange, genres
    - Render dropdown select element
    - Fetch genres dari GET /api/genres on mount

    - Tambahkan "Semua Genre" option
    - _Requirements: 1.3, 10.2_
  - [ ] 7.5 Buat TempoSelector component
    - Tulis components/TempoSelector.jsx dengan props: value, onChange
    - Render radio buttons untuk slow, medium, fast

    - Tambahkan "Semua Tempo" option
    - Style dengan Tailwind CSS
    - _Requirements: 1.4, 10.3_
  - [ ] 7.6 Buat SongCard component
    - Tulis components/SongCard.jsx dengan props: song, onPlay
    - Display cover image, title, artist, reason
    - Tambahkan play button untuk preview
    - Implementasi click handler untuk navigate ke detail page
    - Style dengan Tailwind CSS (card layout, hover effects)
    - _Requirements: 8.1, 8.2, 8.5, 10.4_
  - [ ] 7.7 Buat AudioPreview component
    - Tulis components/AudioPreview.jsx dengan props: previewUrl, title
    - Implementasi HTML5 audio player dengan play/pause controls
    - Tambahkan progress bar

    - Handle audio loading states
    - _Requirements: 6.4, 8.6_

- [ ] 8. Implementasi frontend pages
  - [ ] 8.1 Buat halaman utama (index)
    - Tulis pages/index.jsx dengan form dan results section
    - Integrate MoodSelector, GenreSelector, TempoSelector components

    - Implementasi form state management (mood, genre, tempo)
    - Tambahkan "Recommend" button dengan onClick handler
    - _Requirements: 1.1, 1.5_
  - [x] 8.2 Implementasi recommendation flow di halaman utama

    - Implementasi handleRecommend function untuk call POST /api/recommend
    - Tambahkan loading state dengan skeleton loaders
    - Display recommendations menggunakan SongCard components
    - Handle error states dengan toast notifications
    - Display "Maaf, belum ada lagu yang cocok" message jika no results
    - _Requirements: 8.3, 8.4_
  - [ ] 8.3 Buat halaman detail lagu
    - Tulis pages/song/[id].jsx dengan dynamic routing
    - Fetch song detail dari GET /api/song/:id on mount
    - Display large cover, title, artist, genre, mood, tempo
    - Integrate AudioPreview component untuk 30-second preview
    - Handle loading dan error states
    - Tambahkan back button untuk return ke home
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 9. Implementasi error handling dan edge cases
  - [ ] 9.1 Implementasi frontend error handling
    - Tambahkan try-catch blocks untuk semua API calls
    - Implementasi toast notification system untuk errors
    - Tambahkan retry button untuk failed requests
    - Implementasi fallback UI untuk missing data
    - _Requirements: 4.5, 7.3, 7.4, 7.5_
  - [ ] 9.2 Implementasi backend error handling
    - Tambahkan validation error responses (400) dengan detail messages
    - Implementasi 404 responses untuk song not found
    - Tambahkan 500 error handler dengan logging
    - Implementasi graceful degradation untuk Spotify API failures
    - _Requirements: 4.5, 4.6, 9.4_

- [ ] 10. Setup environment configuration
  - [ ] 10.1 Buat environment configuration files
    - Buat .env.example untuk backend dengan: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, DATABASE_URL, K
    - Buat .env.local.example untuk frontend dengan: NEXT_PUBLIC_API_URL
    - Tulis config loader di backend untuk read dan validate env vars
    - Tambahkan default values untuk optional configs
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_
  - [ ] 10.2 Implementasi startup validation
    - Validate required environment variables on backend startup
    - Log warning jika Spotify credentials missing
    - Verify database connection on startup
    - Initialize KNN encoders dengan data dari database
    - _Requirements: 12.5_

- [ ] 11. Buat deployment configuration
  - [ ] 11.1 Buat Dockerfile untuk backend
    - Tulis Dockerfile dengan Python 3.11 base image
    - Copy requirements.txt dan install dependencies
    - Copy application code
    - Setup CMD untuk run uvicorn
    - Expose port 8000
    - _Requirements: Design - Deployment Strategy_
  - [ ] 11.2 Buat deployment configuration untuk frontend
    - Setup vercel.json dengan build configuration
    - Configure environment variables untuk production
    - Setup API URL untuk point ke deployed backend
    - _Requirements: Design - Deployment Strategy_
  - [ ] 11.3 Buat database initialization script
    - Tulis startup.sh script untuk run init_db.py sebelum start server
    - Tambahkan check untuk skip initialization jika database sudah exists
    - _Requirements: 5.2_

- [ ] 12. Buat dokumentasi dan README
  - [ ] 12.1 Tulis README.md lengkap
    - Tambahkan project overview dan features
    - Dokumentasi cara setup local development (frontend dan backend)
    - Dokumentasi environment variables yang diperlukan
    - Dokumentasi cara run database seeding
    - Dokumentasi cara run tests
    - Tambahkan deployment instructions untuk Vercel dan Railway
    - _Requirements: Design - Documentation_
  - [ ] 12.2 Tambahkan code comments dan docstrings
    - Tambahkan docstrings untuk semua functions dan classes di backend
    - Tambahkan JSDoc comments untuk React components
    - Dokumentasi algoritma KNN dan rule-based engine
    - _Requirements: Design - Documentation_

- [ ] 13. Testing dan quality assurance
  - [ ] 13.1 Run semua unit tests dan fix failures
    - Run pytest untuk backend tests
    - Verify semua tests passing
    - Fix any failing tests
    - _Requirements: 11.1, 11.2, 11.3_
  - [ ] 13.2 Run integration tests
    - Test full recommendation flow end-to-end
    - Test dengan berbagai kombinasi mood, genre, tempo
    - Verify recommendations make sense
    - Test error scenarios
    - _Requirements: 11.4, 11.5_
  - [ ] 13.3 Manual testing dan refinement
    - Test UI/UX di browser
    - Test responsive design di mobile
    - Test dengan dan tanpa Spotify credentials
    - Verify loading states dan error messages
    - Test audio preview playback
    - _Requirements: 8.3, 8.4, 8.6_

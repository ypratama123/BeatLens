import { useState, useEffect } from 'react'
import Head from 'next/head'
import MoodSelector from '../components/MoodSelector'
import GenreSelector from '../components/GenreSelector'
import SongCard from '../components/SongCard'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [step, setStep] = useState(1) // 1: Landing, 2: Selection, 3: Results
  const [mood, setMood] = useState('')
  const [genre, setGenre] = useState('')
  const [genres, setGenres] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Fetch genres on mount
  useEffect(() => {
    fetchGenres()
  }, [])

  const fetchGenres = async () => {
    try {
      const response = await fetch(`${API_URL}/api/genres`)
      const data = await response.json()
      setGenres(data.genres)
    } catch (err) {
      console.error('Error fetching genres:', err)
    }
  }

  const handleRecommend = async () => {
    if (!mood) {
      setError('Pilih mood terlebih dahulu!')
      return
    }

    setLoading(true)
    setError(null)
    setStep(3)

    try {
      const response = await fetch(`${API_URL}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mood,
          genre: genre || null,
          k: 10
        })
      })

      const data = await response.json()

      if (response.ok) {
        setRecommendations(data.recommendations)
        if (data.recommendations.length === 0) {
          setError('Maaf, belum ada lagu yang cocok. Coba ubah genre.')
        }
      } else {
        setError(data.detail || 'Terjadi kesalahan')
      }
    } catch (err) {
      setError('Gagal terhubung ke server. Pastikan backend sudah berjalan.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const resetSelection = () => {
    setStep(2)
    setMood('')
    setGenre('')
    setRecommendations([])
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-violet-800 to-indigo-900 relative overflow-hidden">
      <Head>
        <title>BeatLens - Discover Music That Matches Your Vibe</title>
        <meta name="description" content="Smart music recommender based on your mood" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Animated Background Elements */}
      <div className="fixed inset-0 pointer-events-none">
        {/* Gradient Orbs */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500/30 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl animate-float-delay"></div>
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-violet-500/20 rounded-full blur-3xl animate-float-slow"></div>
        
        {/* Floating Music Notes */}
        <div className="absolute top-1/4 left-1/4 text-6xl opacity-10 animate-float-music">🎵</div>
        <div className="absolute top-1/3 right-1/4 text-5xl opacity-10 animate-float-music-delay">🎶</div>
        <div className="absolute bottom-1/4 left-1/3 text-7xl opacity-10 animate-float-music-slow">🎸</div>
        <div className="absolute top-2/3 right-1/3 text-5xl opacity-10 animate-float-music">🎤</div>
        <div className="absolute bottom-1/3 right-1/4 text-6xl opacity-10 animate-float-music-delay">🎧</div>
        
        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
      </div>

      {/* Step 1: Landing Page */}
      {step === 1 && (
        <div className="min-h-screen flex items-center justify-center px-4 py-12">
          <div className="text-center animate-fade-in max-w-5xl mx-auto">
            {/* Logo */}
            <div className="mb-6 animate-bounce-slow">
              <div className="inline-block">
                <div className="text-6xl mb-3">🎵</div>
                <h1 className="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 mb-2">
                  BeatLens
                </h1>
              </div>
            </div>

            {/* Slogan */}
            <p className="text-xl md:text-2xl text-white/90 font-light mb-3 animate-slide-up">
              Discover Music That Matches Your Vibe
            </p>
            <p className="text-base md:text-lg text-purple-200 mb-8 animate-slide-up-delay">
              Rekomendasi musik cerdas berdasarkan mood dan genre favoritmu
            </p>

            {/* Start Button */}
            <button
              onClick={() => setStep(2)}
              className="group relative px-10 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-lg font-bold rounded-full hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-110 shadow-2xl shadow-purple-500/50 animate-pulse-slow"
            >
              <span className="relative z-10">Mulai Sekarang ✨</span>
              <div className="absolute inset-0 rounded-full bg-white/20 blur-xl group-hover:bg-white/30 transition-all"></div>
            </button>

            {/* Features */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-5 animate-slide-up">
                <div className="text-3xl mb-2">🎭</div>
                <h3 className="text-white font-semibold mb-1 text-sm">Mood-Based</h3>
                <p className="text-purple-200 text-xs">Pilih mood sesuai perasaanmu</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-5 animate-slide-up-delay">
                <div className="text-3xl mb-2">🎸</div>
                <h3 className="text-white font-semibold mb-1 text-sm">Multi-Genre</h3>
                <p className="text-purple-200 text-xs">75+ lagu dari berbagai genre</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-5 animate-slide-up-delay-2">
                <div className="text-3xl mb-2">🤖</div>
                <h3 className="text-white font-semibold mb-1 text-sm">AI-Powered</h3>
                <p className="text-purple-200 text-xs">Algoritma KNN untuk akurasi</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Step 2: Selection Page */}
      {step === 2 && (
        <div className="min-h-screen flex items-center justify-center px-4 py-12">
          <div className="w-full max-w-4xl animate-fade-in">
            {/* Header */}
            <div className="text-center mb-12">
              <h2 className="text-5xl font-bold text-white mb-4">
                Ceritakan Mood-mu
              </h2>
              <p className="text-xl text-purple-200">
                Pilih mood dan genre untuk rekomendasi yang sempurna
              </p>
            </div>

            {/* Selection Form */}
            <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 md:p-12 shadow-2xl">
              <div className="space-y-8">
                {/* Mood Selector */}
                <div>
                  <label className="block text-white text-2xl font-bold mb-4">
                    1. Mood Kamu Saat Ini
                  </label>
                  <MoodSelector value={mood} onChange={setMood} />
                </div>

                {/* Genre Selector */}
                <div>
                  <label className="block text-white text-2xl font-bold mb-4">
                    2. Genre Favorit (Opsional)
                  </label>
                  <GenreSelector value={genre} onChange={setGenre} genres={genres} />
                </div>

                {/* Buttons */}
                <div className="flex gap-4 pt-4">
                  <button
                    onClick={() => setStep(1)}
                    className="px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-xl transition-all"
                  >
                    ← Kembali
                  </button>
                  <button
                    onClick={handleRecommend}
                    disabled={!mood}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-4 px-8 rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg shadow-purple-500/50"
                  >
                    Temukan Lagu 🎵
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Step 3: Results Page */}
      {step === 3 && (
        <div className="min-h-screen px-4 py-12">
          <div className="max-w-7xl mx-auto">
            {/* Header */}
            <div className="text-center mb-12 animate-fade-in">
              <h2 className="text-5xl font-bold text-white mb-4">
                {loading ? 'Mencari Lagu Untukmu...' : 'Rekomendasi Untukmu'}
              </h2>
              <p className="text-xl text-purple-200 mb-6">
                {!loading && `Berdasarkan mood: ${mood} ${genre ? `• Genre: ${genre}` : ''}`}
              </p>
              {!loading && (
                <button
                  onClick={resetSelection}
                  className="px-6 py-3 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-xl transition-all"
                >
                  ← Cari Lagi
                </button>
              )}
            </div>

            {/* Loading State */}
            {loading && (
              <div className="text-center py-20">
                <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-white mb-4"></div>
                <p className="text-white text-xl">Menganalisis preferensimu...</p>
              </div>
            )}

            {/* Error Message */}
            {error && !loading && (
              <div className="max-w-2xl mx-auto bg-red-500/20 border-2 border-red-500 text-white px-6 py-4 rounded-xl mb-8 text-center">
                {error}
              </div>
            )}

            {/* Recommendations Grid */}
            {recommendations.length > 0 && !loading && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
                {recommendations.map((song, index) => (
                  <div
                    key={song.id}
                    style={{ animationDelay: `${index * 100}ms` }}
                    className="animate-slide-up"
                  >
                    <SongCard song={song} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes bounce-slow {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
        @keyframes pulse-slow {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.8; }
        }
        @keyframes float {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -30px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        @keyframes float-music {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-30px) rotate(10deg); }
        }
        .animate-fade-in {
          animation: fade-in 0.6s ease-out;
        }
        .animate-slide-up {
          animation: slide-up 0.6s ease-out;
        }
        .animate-slide-up-delay {
          animation: slide-up 0.6s ease-out 0.2s both;
        }
        .animate-slide-up-delay-2 {
          animation: slide-up 0.6s ease-out 0.4s both;
        }
        .animate-bounce-slow {
          animation: bounce-slow 3s ease-in-out infinite;
        }
        .animate-pulse-slow {
          animation: pulse-slow 2s ease-in-out infinite;
        }
        .animate-float {
          animation: float 20s ease-in-out infinite;
        }
        .animate-float-delay {
          animation: float 25s ease-in-out infinite 5s;
        }
        .animate-float-slow {
          animation: float 30s ease-in-out infinite 10s;
        }
        .animate-float-music {
          animation: float-music 8s ease-in-out infinite;
        }
        .animate-float-music-delay {
          animation: float-music 10s ease-in-out infinite 2s;
        }
        .animate-float-music-slow {
          animation: float-music 12s ease-in-out infinite 4s;
        }
        .bg-grid-pattern {
          background-image: 
            linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
          background-size: 50px 50px;
        }
      `}</style>
    </div>
  )
}

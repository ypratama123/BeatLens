// Mood-based gradient colors
const moodGradients = {
  sedih: 'from-blue-600 via-indigo-600 to-purple-700',
  happy: 'from-yellow-400 via-orange-500 to-pink-500',
  galau: 'from-purple-600 via-pink-600 to-rose-600',
  chill: 'from-teal-500 via-cyan-500 to-blue-500',
  semangat: 'from-red-600 via-orange-600 to-yellow-500',
}

// Mood-based icons
const moodIcons = {
  sedih: '😢',
  happy: '😊',
  galau: '💔',
  chill: '😌',
  semangat: '🔥',
}

export default function SongCard({ song }) {
  const openSpotify = () => {
    if (song.spotify_id) {
      window.open(`https://open.spotify.com/track/${song.spotify_id}`, '_blank')
    }
  }

  const gradient = moodGradients[song.mood] || 'from-purple-600 to-pink-600'
  const moodIcon = moodIcons[song.mood] || '🎵'

  return (
    <div className="group bg-white/10 backdrop-blur-lg rounded-2xl overflow-hidden hover:transform hover:scale-105 transition-all duration-300 border border-white/20 hover:border-white/40 hover:shadow-2xl hover:shadow-purple-500/20">
      {/* Cover Image with Gradient Overlay */}
      <div className={`relative h-56 bg-gradient-to-br ${gradient}`}>
        {song.cover_url ? (
          <>
            <img
              src={song.cover_url}
              alt={song.title}
              className="w-full h-full object-cover"
            />
            <div className={`absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent`}></div>
          </>
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center">
            <span className="text-7xl mb-2">{moodIcon}</span>
            <span className="text-white/80 text-sm font-semibold">
              {song.mood.toUpperCase()}
            </span>
          </div>
        )}
        
        {/* Spotify Button Overlay */}
        {song.spotify_id && (
          <button
            onClick={openSpotify}
            className="absolute top-4 right-4 bg-green-500 hover:bg-green-600 text-white p-3 rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-all transform hover:scale-110"
            title="Dengarkan di Spotify"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
          </button>
        )}

        {/* Mood Badge */}
        <div className="absolute bottom-4 left-4">
          <span className="px-3 py-1 bg-black/60 backdrop-blur-sm text-white text-xs font-bold rounded-full border border-white/20">
            {moodIcon} {song.mood.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Song Info */}
      <div className="p-5">
        <h3 className="text-white font-bold text-xl mb-1 truncate group-hover:text-purple-300 transition-colors">
          {song.title}
        </h3>
        <p className="text-gray-300 text-sm mb-3 truncate">
          🎤 {song.artist}
        </p>
        
        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-3">
          <span className="px-3 py-1 bg-purple-500/30 text-purple-200 text-xs rounded-full font-semibold border border-purple-400/30">
            {song.genre}
          </span>
        </div>

        {/* Reason */}
        <div className="text-gray-400 text-xs mb-4 bg-white/5 p-2 rounded-lg">
          <span className="font-semibold text-purple-300">Match:</span> {song.reason}
        </div>

        {/* Spotify Button */}
        {song.spotify_id && (
          <button
            onClick={openSpotify}
            className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-3 px-4 rounded-xl transition-all transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
            Dengarkan di Spotify
          </button>
        )}
      </div>
    </div>
  )
}

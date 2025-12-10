const moods = [
  { value: 'sedih', label: 'Sedih', emoji: '😢', color: 'from-blue-500 to-blue-700' },
  { value: 'happy', label: 'Happy', emoji: '😊', color: 'from-yellow-400 to-orange-500' },
  { value: 'galau', label: 'Galau', emoji: '💔', color: 'from-purple-500 to-pink-600' },
  { value: 'chill', label: 'Chill', emoji: '😌', color: 'from-green-400 to-teal-500' },
  { value: 'semangat', label: 'Semangat', emoji: '🔥', color: 'from-red-500 to-orange-600' },
]

export default function MoodSelector({ value, onChange }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      {moods.map((mood) => (
        <button
          key={mood.value}
          onClick={() => onChange(mood.value)}
          className={`
            relative p-6 rounded-xl transition-all transform hover:scale-105
            ${value === mood.value 
              ? `bg-gradient-to-br ${mood.color} ring-4 ring-white shadow-2xl scale-105` 
              : 'bg-white/10 hover:bg-white/20'
            }
          `}
        >
          <div className="text-center">
            <div className="text-4xl mb-2">{mood.emoji}</div>
            <div className="text-white font-semibold">{mood.label}</div>
          </div>
          {value === mood.value && (
            <div className="absolute top-2 right-2">
              <div className="w-6 h-6 bg-white rounded-full flex items-center justify-center">
                <span className="text-green-600 text-sm">✓</span>
              </div>
            </div>
          )}
        </button>
      ))}
    </div>
  )
}

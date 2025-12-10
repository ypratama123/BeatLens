const tempos = [
  { value: 'slow', label: 'Slow', emoji: '🐢' },
  { value: 'medium', label: 'Medium', emoji: '🚶' },
  { value: 'fast', label: 'Fast', emoji: '🏃' },
]

export default function TempoSelector({ value, onChange }) {
  return (
    <div className="flex gap-4">
      <button
        onClick={() => onChange('')}
        className={`
          flex-1 px-4 py-3 rounded-xl transition-all
          ${!value 
            ? 'bg-white text-gray-900 font-semibold' 
            : 'bg-white/10 text-white hover:bg-white/20'
          }
        `}
      >
        Semua Tempo
      </button>
      {tempos.map((tempo) => (
        <button
          key={tempo.value}
          onClick={() => onChange(tempo.value)}
          className={`
            flex-1 px-4 py-3 rounded-xl transition-all
            ${value === tempo.value 
              ? 'bg-white text-gray-900 font-semibold' 
              : 'bg-white/10 text-white hover:bg-white/20'
            }
          `}
        >
          <span className="mr-2">{tempo.emoji}</span>
          {tempo.label}
        </button>
      ))}
    </div>
  )
}

export default function GenreSelector({ value, onChange, genres }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-4 py-3 rounded-xl bg-white/10 text-white border border-white/20 focus:border-purple-400 focus:ring-2 focus:ring-purple-400 outline-none transition"
    >
      <option value="">Semua Genre</option>
      {genres.map((genre) => (
        <option key={genre} value={genre} className="bg-gray-900">
          {genre.charAt(0).toUpperCase() + genre.slice(1)}
        </option>
      ))}
    </select>
  )
}

export default function Header() {
  return (
    <header className="bg-black/20 backdrop-blur-md border-b border-white/10">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-3xl">🎵</span>
            <h1 className="text-2xl font-bold text-white">BeatLens</h1>
          </div>
          <nav className="hidden md:flex space-x-6">
            <a href="/" className="text-white hover:text-purple-300 transition">
              Home
            </a>
            <a href="#about" className="text-white hover:text-purple-300 transition">
              About
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}

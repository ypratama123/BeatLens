# 🎵 BeatLens - Smart Music Recommender

<div align="center">

![BeatLens Logo](https://img.shields.io/badge/BeatLens-Smart%20Music%20Recommender-blue?style=for-the-badge&logo=music)

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**BeatLens adalah aplikasi rekomendasi musik cerdas yang menggunakan Hybrid AI untuk memberikan rekomendasi lagu berdasarkan mood, genre, dan tempo yang Anda inginkan.**

[🚀 Live Demo](https://beatlens.vercel.app) • [📖 Documentation](https://github.com/ypratama123/BeatLens/wiki) • [🐛 Report Bug](https://github.com/ypratama123/BeatLens/issues)

</div>

## ✨ Fitur Utama

🤖 **Hybrid AI Recommendation** - Kombinasi Rule-based + KNN Machine Learning  
🎭 **5 Mood Categories** - Sedih, Happy, Galau, Chill, Semangat  
🎸 **10+ Genre Support** - Pop, Rock, Indie, Ballad, EDM, dan lainnya  
⚡ **Fast Performance** - Response time < 10ms  
🎧 **Spotify Integration** - Preview musik langsung  
📱 **Responsive Design** - Mobile-friendly interface  
📊 **154+ Songs Database** - Koleksi lagu yang terus bertambah  

## 🏗️ Tech Stack

<table>
<tr>
<td><strong>Backend</strong></td>
<td><strong>Frontend</strong></td>
<td><strong>AI/ML</strong></td>
</tr>
<tr>
<td>

- FastAPI
- SQLite
- Python 3.8+
- Spotify Web API

</td>
<td>

- Next.js 14
- React 18
- Tailwind CSS
- Responsive Design

</td>
<td>

- Rule-based Engine
- K-Nearest Neighbors
- Scikit-learn
- Hybrid Approach

</td>
</tr>
</table>

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+ | Node.js 16+ | npm/yarn
```

### 1️⃣ Clone Repository
```bash
git clone https://github.com/ypratama123/BeatLens.git
cd BeatLens
```

### 2️⃣ Backend Setup
```bash
cd backend
pip install -r requirements.txt
python db/init_db.py
python app.py
```

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4️⃣ Access Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🎯 How It Works

1. **Choose Your Mood** 🎭 - Select from 5 mood categories
2. **Optional Filters** 🎛️ - Pick specific genre or tempo  
3. **AI Processing** 🤖 - Hybrid AI analyzes your preferences
4. **Get Recommendations** 🎵 - Receive 10 personalized songs
5. **Preview & Enjoy** 🎧 - Listen via Spotify integration

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Response Time | < 10ms |
| Database Size | 154+ songs |
| Mood Coverage | 100% (all moods generate 10+ recommendations) |
| Accuracy | 100% mood matching |
| Genres | 10+ categories |

## 🔧 Configuration

### Spotify API Setup (Optional)
```bash
# 1. Create app at https://developer.spotify.com/
# 2. Copy environment file
cp .env.example .env

# 3. Add your credentials
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

## 🧪 Testing

```bash
# Run all tests
cd backend
python -m pytest tests/ -v

# Test API endpoints
python test_api.py

# Test recommendations
python test_all_moods.py
```

## 📚 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/recommend` | Get music recommendations |
| `GET` | `/api/moods` | List available moods |
| `GET` | `/api/genres` | List available genres |
| `GET` | `/api/song/{id}` | Get song details |

### Example Request
```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"mood": "happy", "k": 10}'
```

## 🛣️ Roadmap

- [ ] User authentication & playlists
- [ ] Advanced ML models (Deep Learning)
- [ ] Social features & sharing
- [ ] Mobile app (React Native)
- [ ] Real-time collaborative playlists
- [ ] Integration with more music platforms

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

<div align="center">

**Yusuf Pratama**

[![GitHub](https://img.shields.io/badge/GitHub-ypratama123-black?style=flat-square&logo=github)](https://github.com/ypratama123)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/ypratama123)

</div>

## 🙏 Acknowledgments

- [Spotify Web API](https://developer.spotify.com/) for music integration
- [Scikit-learn](https://scikit-learn.org/) for ML capabilities  
- [FastAPI](https://fastapi.tiangolo.com/) & [Next.js](https://nextjs.org/) communities
- All contributors and testers

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by [Yusuf Pratama](https://github.com/ypratama123)

</div>
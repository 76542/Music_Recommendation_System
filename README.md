# 🎵 Music Recommender System

A personalized **Music Recommender System** built with **Flask**, **Pandas**, and **Scikit-learn**.  
It allows users to **rate songs** and get recommendations using:

- ✅ **Collaborative Filtering** (based on user ratings & preferences)
- ✅ **Content-Based Filtering** (based on song features like energy, valence, danceability, etc.)
- ✅ **Hybrid Approach** (combines both methods for better accuracy)

---

## 🚀 Features

- 🎶 Rate songs (1–5 stars) through a simple UI.
- 🎧 Get personalized music recommendations.
- 🌐 Bollywood + Hollywood dataset (customizable via `data.csv`).
- 🔄 Hybrid recommendation for better accuracy.
- 🖥️ Flask backend with REST APIs (`/api/songs` & `/api/recommend`).

---

## 📂 Project Structure
```bash
music-recommender/
│── app.py # Flask app (backend + API routes)
│── recommender.py # MusicRecommender class (ML logic)
│── data.csv # Music dataset (Bollywood + Hollywood songs)
│── templates/
│ └── index.html # Frontend UI for rating & recommendations
│── static/
│ └── style.css # Custom styles (optional)
│── README.md # Project documentation
```
---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/music-recommender.git
   cd music-recommender

   ```

2. **Create virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows

   pip install -r requirements.txt
   ```
3. **Run the app**

   ```bash
   python app.py
   ```
3. **Open your browser at  http://127.0.0.1:5000/**

---
## 🧪 API Endpoints

GET /api/songs → Returns a list of songs to rate.

POST /api/recommend → Takes user ratings and returns recommendations.


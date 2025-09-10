from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
from recommender import MusicRecommender

app = Flask(__name__)

# Initialize recommender
recommender = MusicRecommender()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/songs')
def get_songs():
    songs = recommender.get_all_songs()

    # Shuffle songs
    random.shuffle(songs)

    # Pick 5 Bollywood + 5 Hollywood/other
    bollywood = [s for s in songs if s.get('artist') in [
        'Arijit Singh', 'Shreya Ghoshal', 'Sonu Nigam', 'Neha Kakkar', 'Atif Aslam'
    ]]
    hollywood = [s for s in songs if s.get('artist') not in [
        'Arijit Singh', 'Shreya Ghoshal', 'Sonu Nigam', 'Neha Kakkar', 'Atif Aslam'
    ]]

    selected = bollywood[:5] + hollywood[:5]

    return jsonify(selected)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_ratings = data.get('ratings', {})
    method = data.get('method', 'collaborative')
    
    recommendations = recommender.recommend(user_ratings, method=method)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

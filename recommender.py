import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

class MusicRecommender:
    def __init__(self):
        self.songs_df = self.load_data()
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load or create sample music data"""
        try:
            return pd.read_csv('data.csv')
        except FileNotFoundError:
            return self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample music dataset"""
        genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical', 'Electronic']
        artists = ['Artist A', 'Artist B', 'Artist C', 'Artist D', 'Artist E']
        
        data = []
        for i in range(50):  # 50 songs
            data.append({
                'song_id': i,
                'title': f'Song {i+1}',
                'artist': np.random.choice(artists),
                'genre': np.random.choice(genres),
                'year': np.random.randint(2000, 2024),
                'duration': np.random.randint(120, 300),
                'popularity': np.random.randint(1, 101),
                'danceability': round(np.random.random(), 2),
                'energy': round(np.random.random(), 2),
                'valence': round(np.random.random(), 2)
            })
        
        df = pd.DataFrame(data)
        df.to_csv('data.csv', index=False)
        print("Sample data created: data.csv")
        return df
    
    def get_all_songs(self):
        """Return all songs as list of dictionaries"""
        return self.songs_df.to_dict('records')
    
    def collaborative_filtering(self, user_ratings, n_recommendations=5):
        """Simple collaborative filtering based on genre and artist preferences"""
        if not user_ratings:
            # Return popular songs if no ratings
            return self.songs_df.nlargest(n_recommendations, 'popularity').to_dict('records')
        
        # Analyze user preferences
        rated_songs = [int(song_id) for song_id in user_ratings.keys()]
        rated_df = self.songs_df[self.songs_df['song_id'].isin(rated_songs)]
        
        # Calculate preferences
        genre_scores = {}
        artist_scores = {}
        
        for song_id, rating in user_ratings.items():
            song = self.songs_df[self.songs_df['song_id'] == int(song_id)].iloc[0]
            genre = song['genre']
            artist = song['artist']
            
            genre_scores[genre] = genre_scores.get(genre, 0) + float(rating)
            artist_scores[artist] = artist_scores.get(artist, 0) + float(rating)
        
        # Score all unrated songs
        unrated_songs = self.songs_df[~self.songs_df['song_id'].isin(rated_songs)].copy()
        unrated_songs['score'] = 0
        
        for idx, song in unrated_songs.iterrows():
            score = 0
            score += genre_scores.get(song['genre'], 0) * 0.6
            score += artist_scores.get(song['artist'], 0) * 0.4
            score += song['popularity'] * 0.01  # Slight popularity boost
            unrated_songs.at[idx, 'score'] = score
        
        # Return top recommendations
        recommendations = unrated_songs.nlargest(n_recommendations, 'score')
        return recommendations.drop('score', axis=1).to_dict('records')
    
    def content_based_filtering(self, user_ratings, n_recommendations=5):
        """Content-based filtering using song features"""
        if not user_ratings:
            return self.songs_df.nlargest(n_recommendations, 'popularity').to_dict('records')
        
        # Get features for liked songs (rating >= 4)
        liked_songs = [int(song_id) for song_id, rating in user_ratings.items() if float(rating) >= 4]
        
        if not liked_songs:
            return self.songs_df.nlargest(n_recommendations, 'popularity').to_dict('records')
        
        liked_df = self.songs_df[self.songs_df['song_id'].isin(liked_songs)]
        
        # Features for similarity calculation
        feature_cols = ['year', 'duration', 'popularity', 'danceability', 'energy', 'valence']
        
        # Normalize features
        all_features = self.scaler.fit_transform(self.songs_df[feature_cols])
        liked_features = self.scaler.transform(liked_df[feature_cols])
        
        # Calculate average profile of liked songs
        user_profile = np.mean(liked_features, axis=0)
        
        # Calculate similarity with all songs
        similarities = cosine_similarity([user_profile], all_features)[0]
        
        # Get unrated songs
        rated_songs = [int(song_id) for song_id in user_ratings.keys()]
        unrated_mask = ~self.songs_df['song_id'].isin(rated_songs)
        
        # Add similarity scores
        recommendations_df = self.songs_df[unrated_mask].copy()
        recommendations_df['similarity'] = similarities[unrated_mask]
        
        # Return top recommendations
        recommendations = recommendations_df.nlargest(n_recommendations, 'similarity')
        return recommendations.drop('similarity', axis=1).to_dict('records')
    
    def recommend(self, user_ratings, method='collaborative', n_recommendations=5):
        """Main recommendation function"""
        if method == 'collaborative':
            return self.collaborative_filtering(user_ratings, n_recommendations)
        elif method == 'content':
            return self.content_based_filtering(user_ratings, n_recommendations)
        else:
            # Hybrid: combine both methods
            collab_recs = self.collaborative_filtering(user_ratings, n_recommendations//2 + 1)
            content_recs = self.content_based_filtering(user_ratings, n_recommendations//2 + 1)
            
            # Combine and remove duplicates
            all_recs = collab_recs + content_recs
            seen_ids = set()
            unique_recs = []
            
            for rec in all_recs:
                if rec['song_id'] not in seen_ids:
                    unique_recs.append(rec)
                    seen_ids.add(rec['song_id'])
                
                if len(unique_recs) >= n_recommendations:
                    break
            
            return unique_recs[:n_recommendations]
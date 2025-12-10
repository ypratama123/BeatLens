"""
KNN Recommender untuk similarity matching
"""
import numpy as np
from typing import List, Dict, Optional


class KNNRecommender:
    """KNN-based recommender menggunakan cosine similarity"""
    
    def __init__(self):
        self.genre_encoder = {}
        self.mood_encoder = {}
        self.tempo_encoder = {"slow": 0, "medium": 1, "fast": 2}
        
    def build_encoders(self, songs: List[Dict]):
        """
        Build encoders dari dataset songs
        
        Args:
            songs: List of all songs
        """
        # Build genre encoder
        unique_genres = sorted(set(song['genre'] for song in songs))
        self.genre_encoder = {genre: idx for idx, genre in enumerate(unique_genres)}
        
        # Build mood encoder
        unique_moods = sorted(set(song['mood'] for song in songs))
        self.mood_encoder = {mood: idx for idx, mood in enumerate(unique_moods)}
    
    def encode_features(self, item: Dict) -> np.ndarray:
        """
        Convert categorical features ke numerical vector
        
        Args:
            item: Song atau user profile dengan genre, mood, tempo
            
        Returns:
            Feature vector sebagai numpy array
        """
        # One-hot encode mood
        mood_vector = np.zeros(len(self.mood_encoder))
        if item['mood'] in self.mood_encoder:
            mood_vector[self.mood_encoder[item['mood']]] = 1
        
        # One-hot encode genre
        genre_vector = np.zeros(len(self.genre_encoder))
        if item['genre'] in self.genre_encoder:
            genre_vector[self.genre_encoder[item['genre']]] = 1
        
        # Ordinal encode tempo
        tempo_value = self.tempo_encoder.get(item['tempo'], 1)  # default to medium
        tempo_vector = np.array([tempo_value / 2.0])  # normalize to 0-1
        
        # Concatenate all features
        feature_vector = np.concatenate([mood_vector, genre_vector, tempo_vector])
        
        return feature_vector
    
    def compute_similarity(self, user_vector: np.ndarray, song_vector: np.ndarray) -> float:
        """
        Compute cosine similarity antara dua vectors
        
        Formula: similarity = (A · B) / (||A|| * ||B||)
        
        Args:
            user_vector: User profile feature vector
            song_vector: Song feature vector
            
        Returns:
            Similarity score (0-1)
        """
        # Compute dot product
        dot_product = np.dot(user_vector, song_vector)
        
        # Compute magnitudes
        user_magnitude = np.linalg.norm(user_vector)
        song_magnitude = np.linalg.norm(song_vector)
        
        # Avoid division by zero
        if user_magnitude == 0 or song_magnitude == 0:
            return 0.0
        
        # Compute cosine similarity
        similarity = dot_product / (user_magnitude * song_magnitude)
        
        # Ensure result is in [0, 1] range
        similarity = max(0.0, min(1.0, similarity))
        
        return float(similarity)
    
    def recommend(self, user_profile: Dict, candidates: List[Dict], k: int = 5) -> List[Dict]:
        """
        Find top-k most similar songs
        
        Args:
            user_profile: Dict dengan mood, genre, tempo
            candidates: Filtered songs dari rule engine
            k: Number of recommendations
            
        Returns:
            Top-k songs dengan similarity scores
        """
        if not candidates:
            return []
        
        # Encode user profile
        user_vector = self.encode_features(user_profile)
        
        # Compute similarity untuk setiap candidate
        scored_songs = []
        for song in candidates:
            song_vector = self.encode_features(song)
            similarity = self.compute_similarity(user_vector, song_vector)
            
            song_with_score = song.copy()
            song_with_score['similarity_score'] = similarity
            scored_songs.append(song_with_score)
        
        # Sort by similarity score (descending)
        scored_songs.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Return top-k
        return scored_songs[:k]

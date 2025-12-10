"""
Rule-based engine untuk filtering lagu berdasarkan mood
"""
from typing import List, Dict, Optional


class RuleEngine:
    """Engine untuk memfilter lagu berdasarkan aturan mood"""
    
    MOOD_RULES = {
        "sedih": {
            "preferred_genres": ["indie", "ballad"],
            "preferred_tempo": ["slow", "medium"]
        },
        "happy": {
            "preferred_genres": ["pop", "rock"],
            "preferred_tempo": ["medium", "fast"]
        },
        "galau": {
            "preferred_genres": ["indie", "pop", "ballad"],
            "preferred_tempo": ["slow"]
        },
        "chill": {
            "preferred_genres": ["lo-fi", "acoustic", "ambient", "indie"],
            "preferred_tempo": ["slow", "medium"]
        },
        "semangat": {
            "preferred_genres": ["rock", "pop punk", "edm"],
            "preferred_tempo": ["fast", "medium"]
        }
    }
    
    def get_mood_preferences(self, mood: str) -> Dict[str, List[str]]:
        """
        Get preferred genres and tempo untuk mood tertentu
        
        Args:
            mood: Mood yang dipilih user
            
        Returns:
            Dictionary dengan preferred_genres dan preferred_tempo
        """
        if mood not in self.MOOD_RULES:
            raise ValueError(f"Invalid mood: {mood}. Must be one of {list(self.MOOD_RULES.keys())}")
        
        return self.MOOD_RULES[mood]
    
    def filter_by_mood(self, mood: str, genre: Optional[str], tempo: Optional[str], 
                      songs: List[Dict]) -> List[Dict]:
        """
        Filter songs berdasarkan mood rules
        
        Args:
            mood: User's mood
            genre: User's preferred genre (optional, overrides mood preferences)
            tempo: User's preferred tempo (optional, overrides mood preferences)
            songs: All available songs
            
        Returns:
            Filtered candidate songs dengan preliminary scores
        """
        if not songs:
            return []
        
        # Get mood preferences
        preferences = self.get_mood_preferences(mood)
        
        # Determine which genres and tempos to filter by
        target_genres = [genre] if genre else preferences["preferred_genres"]
        target_tempos = [tempo] if tempo else preferences["preferred_tempo"]
        
        # First pass: strict filtering (genre AND tempo match)
        candidates = []
        for song in songs:
            score = 0.0
            genre_match = song['genre'] in target_genres
            tempo_match = song['tempo'] in target_tempos
            mood_match = song['mood'] == mood
            
            if genre_match and tempo_match:
                # Calculate preliminary score
                if genre_match:
                    score += 0.3
                if tempo_match:
                    score += 0.2
                if mood_match:
                    score += 0.5
                
                song_with_score = song.copy()
                song_with_score['preliminary_score'] = score
                candidates.append(song_with_score)
        
        # If we have enough candidates, return them
        if len(candidates) >= 10:
            return candidates
        
        # Second pass: relax to genre OR tempo match
        for song in songs:
            # Skip if already in candidates
            if any(c['id'] == song['id'] for c in candidates):
                continue
            
            score = 0.0
            genre_match = song['genre'] in target_genres
            tempo_match = song['tempo'] in target_tempos
            mood_match = song['mood'] == mood
            
            if genre_match or tempo_match:
                if genre_match:
                    score += 0.3
                if tempo_match:
                    score += 0.2
                if mood_match:
                    score += 0.5
                
                song_with_score = song.copy()
                song_with_score['preliminary_score'] = score
                candidates.append(song_with_score)
        
        return candidates

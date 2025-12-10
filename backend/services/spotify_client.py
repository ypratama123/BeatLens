"""
Spotify Web API client untuk metadata dan preview
"""
import requests
import time
from typing import Optional, Dict
from datetime import datetime, timedelta


class SpotifyClient:
    """
    Client untuk Spotify Web API menggunakan Client Credentials Flow
    """
    
    AUTH_URL = "https://accounts.spotify.com/api/token"
    API_BASE_URL = "https://api.spotify.com/v1"
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Initialize Spotify client
        
        Args:
            client_id: Spotify Client ID
            client_secret: Spotify Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
        self.enabled = bool(client_id and client_secret)
    
    def get_access_token(self) -> Optional[str]:
        """
        Get access token using Client Credentials Flow
        Caches token until expiration
        
        Returns:
            Access token string atau None jika credentials tidak ada
        """
        if not self.enabled:
            return None
        
        # Check if we have a valid cached token
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Request new token
        try:
            response = requests.post(
                self.AUTH_URL,
                data={
                    "grant_type": "client_credentials"
                },
                auth=(self.client_id, self.client_secret),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                expires_in = data.get("expires_in", 3600)  # default 1 hour
                
                # Set expiration time (subtract 60 seconds for safety)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                
                return self.access_token
            else:
                print(f"Failed to get Spotify access token: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting Spotify access token: {e}")
            return None
    
    def get_track_preview(self, spotify_id: str) -> Optional[Dict]:
        """
        Get track preview URL and metadata from Spotify
        
        Args:
            spotify_id: Spotify track ID
            
        Returns:
            Dict dengan preview_url, cover_url, duration atau None jika gagal
        """
        if not self.enabled:
            return None
        
        token = self.get_access_token()
        if not token:
            return None
        
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/tracks/{spotify_id}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract preview URL
                preview_url = data.get("preview_url")
                
                # Extract cover image (largest available)
                cover_url = None
                if data.get("album") and data["album"].get("images"):
                    images = data["album"]["images"]
                    if images:
                        cover_url = images[0]["url"]  # First image is usually largest
                
                # Extract duration
                duration_ms = data.get("duration_ms", 0)
                
                return {
                    "preview_url": preview_url,
                    "cover_url": cover_url,
                    "duration_ms": duration_ms
                }
            
            elif response.status_code == 429:
                # Rate limited
                retry_after = int(response.headers.get("Retry-After", 60))
                print(f"Spotify rate limited. Retry after {retry_after} seconds")
                return None
            
            else:
                print(f"Failed to get track from Spotify: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting track from Spotify: {e}")
            return None
    
    def search_track(self, query: str, limit: int = 10) -> Optional[list]:
        """
        Search for tracks on Spotify (optional feature)
        
        Args:
            query: Search query
            limit: Number of results to return
            
        Returns:
            List of track dicts atau None jika gagal
        """
        if not self.enabled:
            return None
        
        token = self.get_access_token()
        if not token:
            return None
        
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/search",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                params={
                    "q": query,
                    "type": "track",
                    "limit": limit
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                tracks = data.get("tracks", {}).get("items", [])
                
                results = []
                for track in tracks:
                    results.append({
                        "id": track["id"],
                        "name": track["name"],
                        "artists": [artist["name"] for artist in track.get("artists", [])],
                        "preview_url": track.get("preview_url"),
                        "cover_url": track["album"]["images"][0]["url"] if track.get("album", {}).get("images") else None
                    })
                
                return results
            else:
                print(f"Failed to search Spotify: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error searching Spotify: {e}")
            return None

import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores the full song catalog for later scoring."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects best matching the user's profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a plain-language string describing why a song was recommended to this user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Reads songs.csv and returns a list of dicts, one per row.
    Numeric fields (id, energy, tempo_bpm, valence, danceability, acousticness)
    are converted from strings to int/float so math operations work later.
    """
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores one song against the user's preferences using a weighted formula:
      genre match = 30%, mood match = 25%, energy proximity = 20%,
      tempo proximity = 10%, valence = 5%, danceability = 5%, acousticness = 5%.
    Categorical features award full points on exact match; numerical features
    use proximity scoring (closer to the user's target = higher score).
    Returns a (score, reasons) tuple where score is 0.0–1.0 and reasons is a
    list of plain-language strings explaining which features contributed.
    """
    score = 0.0
    reasons = []

    # Genre: 30%
    if song.get("genre") == user_prefs.get("genre"):
        score += 0.30
        reasons.append(f"genre matches ({song['genre']})")

    # Mood: 25%
    if song.get("mood") == user_prefs.get("mood"):
        score += 0.25
        reasons.append(f"mood matches ({song['mood']})")

    # Energy proximity: 20%
    target_energy = user_prefs.get("energy", 0.5)
    energy_score = (1 - abs(target_energy - song["energy"])) * 0.20
    score += energy_score
    reasons.append(f"energy proximity {energy_score:.2f} (song={song['energy']}, target={target_energy})")

    # Tempo proximity: 10% (normalize both to 0-1 by dividing by 200)
    target_bpm = user_prefs.get("tempo_bpm", 120)
    tempo_score = (1 - abs((target_bpm / 200) - (song["tempo_bpm"] / 200))) * 0.10
    score += tempo_score
    reasons.append(f"tempo proximity {tempo_score:.2f} (song={song['tempo_bpm']} bpm)")

    # Valence proximity: 5%
    target_valence = user_prefs.get("valence", 0.5)
    valence_score = (1 - abs(target_valence - song["valence"])) * 0.05
    score += valence_score

    # Danceability proximity: 5%
    target_dance = user_prefs.get("danceability", 0.5)
    dance_score = (1 - abs(target_dance - song["danceability"])) * 0.05
    score += dance_score

    # Acousticness proximity: 5%
    acoustic_target = 0.8 if user_prefs.get("likes_acoustic", False) else 0.2
    acoustic_score = (1 - abs(acoustic_target - song["acousticness"])) * 0.05
    score += acoustic_score

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song in the catalog, sorts by score descending, and returns
    the top-k results. Each result is a (song_dict, score, explanation) tuple
    where explanation joins the reasons from score_song into one readable string.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

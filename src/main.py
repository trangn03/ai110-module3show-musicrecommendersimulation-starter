"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


USERS = {
    "Late-night coder": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "tempo_bpm": 80,
        "likes_acoustic": True,
    },
    "Morning run": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 130,
        "likes_acoustic": False,
    },
    "Study session": {
        "genre": "ambient",
        "mood": "focused",
        "energy": 0.3,
        "tempo_bpm": 70,
        "likes_acoustic": True,
    },
    # --- Adversarial / edge-case profiles ---
    "Sad Raver [conflict: high energy + sad mood]": {
        "genre": "EDM",
        "mood": "sad",
        "energy": 0.97,
        "tempo_bpm": 128,
        "likes_acoustic": False,
    },
    "K-Pop Stan [edge: unknown genre]": {
        "genre": "k-pop",
        "mood": "happy",
        "energy": 0.75,
        "tempo_bpm": 125,
        "likes_acoustic": False,
    },
    "Max Everything [edge: all extremes]": {
        "genre": "metal",
        "mood": "angry",
        "energy": 1.0,
        "tempo_bpm": 200,
        "likes_acoustic": False,
    },
    "Perfectly Neutral [edge: all midpoints]": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.5,
        "tempo_bpm": 100,
        "likes_acoustic": True,
    },
    "Unplugged Gymrat [conflict: acoustic + high energy]": {
        "genre": "folk",
        "mood": "peaceful",
        "energy": 0.9,
        "tempo_bpm": 150,
        "likes_acoustic": True,
    },
    "Silence Seeker [edge: zero energy + zero bpm]": {
        "genre": "classical",
        "mood": "melancholic",
        "energy": 0.0,
        "tempo_bpm": 0,
        "likes_acoustic": True,
    },
    "Genre Avoider [edge: near-tie songs]": {
        "genre": "lofi",
        "mood": "focused",
        "energy": 0.40,
        "tempo_bpm": 80,
        "likes_acoustic": True,
    },
}


def print_recommendations(user_name: str, user_prefs: dict, songs: list) -> None:
    """Prints the user profile and their top-5 recommendations."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print(f"  USER: {user_name}")
    print("=" * 50)
    for key, value in user_prefs.items():
        print(f"  {key:<12}: {value}")

    print("\n" + "-" * 50)
    print("  TOP RECOMMENDATIONS")
    print("-" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 1.00")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print("    Why   :")
        for reason in explanation.split(" | "):
            print(f"      - {reason}")
    print("\n" + "=" * 50)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for user_name, user_prefs in USERS.items():
        print_recommendations(user_name, user_prefs, songs)


if __name__ == "__main__":
    main()

# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

---

## How The System Works

Real-world recommenders like Spotify or YouTube learn from massive amounts of behavioral data — what you skip, replay, or add to a playlist — and combine that with audio features and what similar users liked (collaborative filtering). They are powerful but opaque: the system optimizes for engagement, which can create filter bubbles where you only ever hear what you already know. This version takes a simpler, more transparent approach. Instead of learning from behavior, it scores every song directly against a user's stated preferences using a weighted formula: genre and mood account for most of the score because they capture intent most clearly, energy is matched by proximity (closer to the user's target is better, not just higher or lower), and acousticness handles the remaining dimension. Every recommendation comes with a plain-language explanation so the reasoning is always visible. The priority here is interpretability over accuracy — a small system you can fully understand and debug.

**Song features:** Each song carries 10 attributes — `id`, `title`, and `artist` (identity only, not scored), plus `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The scoring formula actively uses `genre`, `mood`, `energy`, and `acousticness`.

**UserProfile fields:** `favorite_genre` (str), `favorite_mood` (str), `target_energy` (float 0–1), `likes_acoustic` (bool).

**Scoring:** Every song receives a score between 0 and 1 from this weighted formula:

| Feature | Weight | Method |
| --- | --- | --- |
| `genre` | 40% | +0.40 if exact match |
| `mood` | 30% | +0.30 if exact match |
| `energy` | 20% | `1 - abs(target_energy - song.energy)` scaled by 0.20 |
| `acousticness` | 10% | proximity to 0.8 (acoustic fan) or 0.2 (non-acoustic) scaled by 0.10 |

Numerical features use proximity scoring — a song is rewarded for being *close* to the user's preference, not for simply having a high or low value.

**Selection:** All songs are scored, sorted descending, and the top `k` (default 5) are returned along with a plain-language explanation of which features matched.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):
  
```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate # Windows
```

1. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


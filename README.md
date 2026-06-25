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

Real-world recommenders like Spotify or YouTube learn from massive amounts of behavioral data — what you skip, replay, or add to a playlist — and combine that with audio features and what similar users liked (collaborative filtering). This version takes a simpler, more transparent approach. Instead of learning from behavior, it scores every song directly against a user's stated preferences using a weighted formula: genre and mood account for most of the score because they capture intent most clearly, energy is matched by proximity (closer to the user's target is better, not just higher or lower), and acousticness handles the remaining dimension. Every recommendation comes with a plain-language explanation so the reasoning is always visible. The priority here is interpretability over accuracy — a small system you can fully understand and debug.

**Song features:** Each song in `data/songs.csv` has 7 scoreable features that the recommender uses:

| Feature | Type | Description |
| --- | --- | --- |
| `genre` | categorical | Musical genre (pop, lofi, rock, ambient, jazz, synthwave, indie pop) |
| `mood` | categorical | Emotional feel (happy, chill, intense, relaxed, focused, moody) |
| `energy` | float 0–1 | Overall intensity of the track |
| `tempo_bpm` | float (60–152) | Beats per minute; normalized to 0–1 before scoring |
| `valence` | float 0–1 | Musical positivity — high = upbeat, low = somber |
| `danceability` | float 0–1 | How suitable the track is for dancing |
| `acousticness` | float 0–1 | How acoustic vs. produced the track sounds |

The remaining fields (`id`, `title`, `artist`) are identity fields and are not used in scoring.

**UserProfile fields:** 
`favorite_genre` (str): the genre that user most wants to hear.
`favorite_mood` (str): the emotional tone that user want to get (ex: happy, sad, chill) 
`target_energy` (float 0–1): music intensity level
`likes_acoustic` (bool): future use to further filter by acoustic character.

**Algorithm Recipe/Scoring:** Every song receives a score between 0 and 1 from this weighted formula:

| Feature | Weight | Rule |
|---|---|---|
| `genre` | **30%** | `+0.30` if `song.genre == user.favorite_genre`, else `0` |
| `mood` | **25%** | `+0.25` if `song.mood == user.favorite_mood`, else `0` |
| `energy` | **20%** | `(1 - abs(user.target_energy - song.energy)) * 0.20` |
| `tempo_bpm` | **10%** | `(1 - abs((user_bpm/200) - (song_bpm/200))) * 0.10` |
| `valence` | **5%** | `(1 - abs(user.target_valence - song.valence)) * 0.05` |
| `danceability` | **5%** | `(1 - abs(user.target_danceability - song.danceability)) * 0.05` |
| `acousticness` | **5%** | `(1 - abs(acoustic_target - song.acousticness)) * 0.05` where `acoustic_target = 0.8` if `likes_acoustic` else `0.2` |

**Total score = sum of all 7 terms** (max possible = 1.0)

Numerical features use proximity scoring — a song is rewarded for being *close* to the user's preference, not for simply having a high or low value.

**Selection:** All songs are scored, sorted descending, and the top `k` (default 5) are returned along with a plain-language explanation of which features matched.

**Why these weights?**

- **Genre (30%) and mood (25%)** dominate because they reflect intent — a user asking for "chill lofi" has a clear categorical preference that should override minor numeric differences.
- **Energy (20%)** uses proximity, not magnitude — a song is not better for being louder, only for being closer to what the user wants.
- **Tempo, valence, danceability, acousticness (5–10% each)** act as tiebreakers between songs that already match genre and mood.

**Example** — user: lofi / chill / energy=0.40

| Song | Genre hit | Mood hit | Energy proximity | Total (approx) |
|---|---|---|---|---|
| Library Rain (lofi, chill, 0.35) | +0.30 | +0.25 | `(1-0.05)*0.20 = 0.19` | ~0.74 |
| Midnight Coding (lofi, chill, 0.42) | +0.30 | +0.25 | `(1-0.02)*0.20 ≈ 0.196` | ~0.75 |
| Focus Flow (lofi, focused, 0.40) | +0.30 | 0 | `1.0 * 0.20 = 0.20` | ~0.55 |

Library Rain and Midnight Coding both score high because they hit **genre + mood** (55% of the total weight combined), and their energy is close to the target.

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
or
```bash
python src/main.py
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
Loaded songs: 20

==================================================
  USER PROFILE
==================================================
  genre       : pop
  mood        : happy
  energy      : 0.8

==================================================
  TOP RECOMMENDATIONS
==================================================

#1  Sunrise City by Neon Echo
    Score : 0.96 / 1.00
    Genre : pop  |  Mood: happy
    Why   :
      - genre matches (pop)
      - mood matches (happy)
      - energy proximity 0.20 (song=0.82, target=0.8)
      - tempo proximity 0.10 (song=118.0 bpm)

#2  Gym Hero by Max Pulse
    Score : 0.68 / 1.00
    Genre : pop  |  Mood: intense
    Why   :
      - genre matches (pop)
      - energy proximity 0.17 (song=0.93, target=0.8)
      - tempo proximity 0.09 (song=132.0 bpm)

#3  Rooftop Lights by Indigo Parade
    Score : 0.65 / 1.00
    Genre : indie pop  |  Mood: happy
    Why   :
      - mood matches (happy)
      - energy proximity 0.19 (song=0.76, target=0.8)
      - tempo proximity 0.10 (song=124.0 bpm)

#4  Night Drive Loop by Neon Echo
    Score : 0.42 / 1.00
    Genre : synthwave  |  Mood: moody
    Why   :
      - energy proximity 0.19 (song=0.75, target=0.8)
      - tempo proximity 0.10 (song=110.0 bpm)

#5  Concrete Jungle by MC Verse
    Score : 0.41 / 1.00
    Genre : hip-hop  |  Mood: energetic
    Why   :
      - energy proximity 0.20 (song=0.8, target=0.8)
      - tempo proximity 0.09 (song=95.0 bpm)

==================================================
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


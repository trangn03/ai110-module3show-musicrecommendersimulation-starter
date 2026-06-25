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
### Standard Profile
```
Loaded songs: 20

==================================================
  USER: Late-night coder
==================================================
  genre       : lofi
  mood        : chill
  energy      : 0.4
  tempo_bpm   : 80
  likes_acoustic: True

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Midnight Coding by LoRoom
    Score : 0.98 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - genre matches (lofi)
      - mood matches (chill)
      - energy proximity 0.20 (song=0.42, target=0.4)
      - tempo proximity 0.10 (song=78.0 bpm)

#2  Library Rain by Paper Lanterns
    Score : 0.97 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - genre matches (lofi)
      - mood matches (chill)
      - energy proximity 0.19 (song=0.35, target=0.4)
      - tempo proximity 0.10 (song=72.0 bpm)

#3  Focus Flow by LoRoom
    Score : 0.74 / 1.00
    Genre : lofi  |  Mood: focused
    Why   :
      - genre matches (lofi)
      - energy proximity 0.20 (song=0.4, target=0.4)
      - tempo proximity 0.10 (song=80.0 bpm)

#4  Spacewalk Thoughts by Orbit Bloom
    Score : 0.65 / 1.00
    Genre : ambient  |  Mood: chill
    Why   :
      - mood matches (chill)
      - energy proximity 0.18 (song=0.28, target=0.4)
      - tempo proximity 0.09 (song=60.0 bpm)

#5  Last Train Home by The Static
    Score : 0.43 / 1.00
    Genre : country  |  Mood: nostalgic
    Why   :
      - energy proximity 0.19 (song=0.45, target=0.4)
      - tempo proximity 0.10 (song=88.0 bpm)

==================================================

==================================================
  USER: Morning run
==================================================
  genre       : pop
  mood        : happy
  energy      : 0.8
  tempo_bpm   : 130
  likes_acoustic: False

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Sunrise City by Neon Echo
    Score : 0.96 / 1.00
    Genre : pop  |  Mood: happy
    Why   :
      - genre matches (pop)
      - mood matches (happy)
      - energy proximity 0.20 (song=0.82, target=0.8)
      - tempo proximity 0.09 (song=118.0 bpm)

#2  Gym Hero by Max Pulse
    Score : 0.68 / 1.00
    Genre : pop  |  Mood: intense
    Why   :
      - genre matches (pop)
      - energy proximity 0.17 (song=0.93, target=0.8)
      - tempo proximity 0.10 (song=132.0 bpm)

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
      - tempo proximity 0.09 (song=110.0 bpm)

#5  Storm Runner by Voltline
    Score : 0.40 / 1.00
    Genre : rock  |  Mood: intense
    Why   :
      - energy proximity 0.18 (song=0.91, target=0.8)
      - tempo proximity 0.09 (song=152.0 bpm)

==================================================

==================================================
  USER: Study session
==================================================
  genre       : ambient
  mood        : focused
  energy      : 0.3
  tempo_bpm   : 70
  likes_acoustic: True

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Spacewalk Thoughts by Orbit Bloom
    Score : 0.72 / 1.00
    Genre : ambient  |  Mood: chill
    Why   :
      - genre matches (ambient)
      - energy proximity 0.20 (song=0.28, target=0.3)
      - tempo proximity 0.10 (song=60.0 bpm)

#2  Focus Flow by LoRoom
    Score : 0.66 / 1.00
    Genre : lofi  |  Mood: focused
    Why   :
      - mood matches (focused)
      - energy proximity 0.18 (song=0.4, target=0.3)
      - tempo proximity 0.10 (song=80.0 bpm)

#3  Mountain Echo by Pine & Wire
    Score : 0.43 / 1.00
    Genre : folk  |  Mood: peaceful
    Why   :
      - energy proximity 0.20 (song=0.3, target=0.3)
      - tempo proximity 0.10 (song=70.0 bpm)

#4  Dusty Road by Blue Ember
    Score : 0.43 / 1.00
    Genre : blues  |  Mood: sad
    Why   :
      - energy proximity 0.19 (song=0.33, target=0.3)
      - tempo proximity 0.10 (song=75.0 bpm)

#5  Library Rain by Paper Lanterns
    Score : 0.43 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - energy proximity 0.19 (song=0.35, target=0.3)
      - tempo proximity 0.10 (song=72.0 bpm)

==================================================
```
### Adversarial & Edge Case User Profiles
```
==================================================
  USER: Sad Raver [conflict: high energy + sad mood]
==================================================
  genre       : EDM
  mood        : sad
  energy      : 0.97
  tempo_bpm   : 128
  likes_acoustic: False

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Neon Pulse by DataWave
    Score : 0.71 / 1.00
    Genre : EDM  |  Mood: euphoric
    Why   :
      - genre matches (EDM)
      - energy proximity 0.20 (song=0.97, target=0.97)
      - tempo proximity 0.10 (song=128.0 bpm)

#2  Dusty Road by Blue Ember
    Score : 0.51 / 1.00
    Genre : blues  |  Mood: sad
    Why   :
      - mood matches (sad)
      - energy proximity 0.07 (song=0.33, target=0.97)
      - tempo proximity 0.07 (song=75.0 bpm)

#3  Storm Runner by Voltline
    Score : 0.41 / 1.00
    Genre : rock  |  Mood: intense
    Why   :
      - energy proximity 0.19 (song=0.91, target=0.97)
      - tempo proximity 0.09 (song=152.0 bpm)

#4  Red Lights by Crimson Drift
    Score : 0.41 / 1.00
    Genre : metal  |  Mood: angry
    Why   :
      - energy proximity 0.20 (song=0.96, target=0.97)
      - tempo proximity 0.08 (song=168.0 bpm)

#5  Depth Charge by Bass Reactor
    Score : 0.41 / 1.00
    Genre : electronic  |  Mood: energetic
    Why   :
      - energy proximity 0.20 (song=0.95, target=0.97)
      - tempo proximity 0.09 (song=140.0 bpm)

==================================================

==================================================
  USER: K-Pop Stan [edge: unknown genre]
==================================================
  genre       : k-pop
  mood        : happy
  energy      : 0.75
  tempo_bpm   : 125
  likes_acoustic: False

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Rooftop Lights by Indigo Parade
    Score : 0.66 / 1.00
    Genre : indie pop  |  Mood: happy
    Why   :
      - mood matches (happy)
      - energy proximity 0.20 (song=0.76, target=0.75)
      - tempo proximity 0.10 (song=124.0 bpm)

#2  Sunrise City by Neon Echo
    Score : 0.65 / 1.00
    Genre : pop  |  Mood: happy
    Why   :
      - mood matches (happy)
      - energy proximity 0.19 (song=0.82, target=0.75)
      - tempo proximity 0.10 (song=118.0 bpm)

#3  Night Drive Loop by Neon Echo
    Score : 0.43 / 1.00
    Genre : synthwave  |  Mood: moody
    Why   :
      - energy proximity 0.20 (song=0.75, target=0.75)
      - tempo proximity 0.09 (song=110.0 bpm)

#4  Concrete Jungle by MC Verse
    Score : 0.39 / 1.00
    Genre : hip-hop  |  Mood: energetic
    Why   :
      - energy proximity 0.19 (song=0.8, target=0.75)
      - tempo proximity 0.09 (song=95.0 bpm)

#5  Storm Runner by Voltline
    Score : 0.39 / 1.00
    Genre : rock  |  Mood: intense
    Why   :
      - energy proximity 0.17 (song=0.91, target=0.75)
      - tempo proximity 0.09 (song=152.0 bpm)

==================================================

==================================================
  USER: Max Everything [edge: all extremes]
==================================================
  genre       : metal
  mood        : angry
  energy      : 1.0
  tempo_bpm   : 200
  likes_acoustic: False

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Red Lights by Crimson Drift
    Score : 0.96 / 1.00
    Genre : metal  |  Mood: angry
    Why   :
      - genre matches (metal)
      - mood matches (angry)
      - energy proximity 0.19 (song=0.96, target=1.0)
      - tempo proximity 0.08 (song=168.0 bpm)

#2  Storm Runner by Voltline
    Score : 0.39 / 1.00
    Genre : rock  |  Mood: intense
    Why   :
      - energy proximity 0.18 (song=0.91, target=1.0)
      - tempo proximity 0.08 (song=152.0 bpm)

#3  Depth Charge by Bass Reactor
    Score : 0.38 / 1.00
    Genre : electronic  |  Mood: energetic
    Why   :
      - energy proximity 0.19 (song=0.95, target=1.0)
      - tempo proximity 0.07 (song=140.0 bpm)

#4  Neon Pulse by DataWave
    Score : 0.37 / 1.00
    Genre : EDM  |  Mood: euphoric
    Why   :
      - energy proximity 0.19 (song=0.97, target=1.0)
      - tempo proximity 0.06 (song=128.0 bpm)

#5  Gym Hero by Max Pulse
    Score : 0.36 / 1.00
    Genre : pop  |  Mood: intense
    Why   :
      - energy proximity 0.19 (song=0.93, target=1.0)
      - tempo proximity 0.07 (song=132.0 bpm)

==================================================

==================================================
  USER: Perfectly Neutral [edge: all midpoints]
==================================================
  genre       : lofi
  mood        : chill
  energy      : 0.5
  tempo_bpm   : 100
  likes_acoustic: True

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Midnight Coding by LoRoom
    Score : 0.96 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - genre matches (lofi)
      - mood matches (chill)
      - energy proximity 0.18 (song=0.42, target=0.5)
      - tempo proximity 0.09 (song=78.0 bpm)

#2  Library Rain by Paper Lanterns
    Score : 0.94 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - genre matches (lofi)
      - mood matches (chill)
      - energy proximity 0.17 (song=0.35, target=0.5)
      - tempo proximity 0.09 (song=72.0 bpm)

#3  Focus Flow by LoRoom
    Score : 0.71 / 1.00
    Genre : lofi  |  Mood: focused
    Why   :
      - genre matches (lofi)
      - energy proximity 0.18 (song=0.4, target=0.5)
      - tempo proximity 0.09 (song=80.0 bpm)

#4  Spacewalk Thoughts by Orbit Bloom
    Score : 0.62 / 1.00
    Genre : ambient  |  Mood: chill
    Why   :
      - mood matches (chill)
      - energy proximity 0.16 (song=0.28, target=0.5)
      - tempo proximity 0.08 (song=60.0 bpm)

#5  Last Train Home by The Static
    Score : 0.43 / 1.00
    Genre : country  |  Mood: nostalgic
    Why   :
      - energy proximity 0.19 (song=0.45, target=0.5)
      - tempo proximity 0.09 (song=88.0 bpm)

==================================================

==================================================
  USER: Unplugged Gymrat [conflict: acoustic + high energy]
==================================================
  genre       : folk
  mood        : peaceful
  energy      : 0.9
  tempo_bpm   : 150
  likes_acoustic: True

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Mountain Echo by Pine & Wire
    Score : 0.82 / 1.00
    Genre : folk  |  Mood: peaceful
    Why   :
      - genre matches (folk)
      - mood matches (peaceful)
      - energy proximity 0.08 (song=0.3, target=0.9)
      - tempo proximity 0.06 (song=70.0 bpm)

#2  Storm Runner by Voltline
    Score : 0.40 / 1.00
    Genre : rock  |  Mood: intense
    Why   :
      - energy proximity 0.20 (song=0.91, target=0.9)
      - tempo proximity 0.10 (song=152.0 bpm)

#3  Red Lights by Crimson Drift
    Score : 0.38 / 1.00
    Genre : metal  |  Mood: angry
    Why   :
      - energy proximity 0.19 (song=0.96, target=0.9)
      - tempo proximity 0.09 (song=168.0 bpm)

#4  Depth Charge by Bass Reactor
    Score : 0.37 / 1.00
    Genre : electronic  |  Mood: energetic
    Why   :
      - energy proximity 0.19 (song=0.95, target=0.9)
      - tempo proximity 0.10 (song=140.0 bpm)

#5  Gym Hero by Max Pulse
    Score : 0.37 / 1.00
    Genre : pop  |  Mood: intense
    Why   :
      - energy proximity 0.19 (song=0.93, target=0.9)
      - tempo proximity 0.09 (song=132.0 bpm)

==================================================

==================================================
  USER: Silence Seeker [edge: zero energy + zero bpm]
==================================================
  genre       : classical
  mood        : melancholic
  energy      : 0.0
  tempo_bpm   : 0
  likes_acoustic: True

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Rainy Window by Ashen Keys
    Score : 0.90 / 1.00
    Genre : classical  |  Mood: melancholic
    Why   :
      - genre matches (classical)
      - mood matches (melancholic)
      - energy proximity 0.16 (song=0.22, target=0.0)
      - tempo proximity 0.07 (song=58.0 bpm)

#2  Spacewalk Thoughts by Orbit Bloom
    Score : 0.35 / 1.00
    Genre : ambient  |  Mood: chill
    Why   :
      - energy proximity 0.14 (song=0.28, target=0.0)
      - tempo proximity 0.07 (song=60.0 bpm)

#3  Mountain Echo by Pine & Wire
    Score : 0.34 / 1.00
    Genre : folk  |  Mood: peaceful
    Why   :
      - energy proximity 0.14 (song=0.3, target=0.0)
      - tempo proximity 0.07 (song=70.0 bpm)

#4  Dusty Road by Blue Ember
    Score : 0.34 / 1.00
    Genre : blues  |  Mood: sad
    Why   :
      - energy proximity 0.13 (song=0.33, target=0.0)
      - tempo proximity 0.06 (song=75.0 bpm)

#5  Library Rain by Paper Lanterns
    Score : 0.33 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - energy proximity 0.13 (song=0.35, target=0.0)
      - tempo proximity 0.06 (song=72.0 bpm)

==================================================

==================================================
  USER: Genre Avoider [edge: near-tie songs]
==================================================
  genre       : lofi
  mood        : focused
  energy      : 0.4
  tempo_bpm   : 80
  likes_acoustic: True

--------------------------------------------------
  TOP RECOMMENDATIONS
--------------------------------------------------

#1  Focus Flow by LoRoom
    Score : 0.99 / 1.00
    Genre : lofi  |  Mood: focused
    Why   :
      - genre matches (lofi)
      - mood matches (focused)
      - energy proximity 0.20 (song=0.4, target=0.4)
      - tempo proximity 0.10 (song=80.0 bpm)

#2  Midnight Coding by LoRoom
    Score : 0.73 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - genre matches (lofi)
      - energy proximity 0.20 (song=0.42, target=0.4)
      - tempo proximity 0.10 (song=78.0 bpm)

#3  Library Rain by Paper Lanterns
    Score : 0.72 / 1.00
    Genre : lofi  |  Mood: chill
    Why   :
      - genre matches (lofi)
      - energy proximity 0.19 (song=0.35, target=0.4)
      - tempo proximity 0.10 (song=72.0 bpm)

#4  Last Train Home by The Static
    Score : 0.43 / 1.00
    Genre : country  |  Mood: nostalgic
    Why   :
      - energy proximity 0.19 (song=0.45, target=0.4)
      - tempo proximity 0.10 (song=88.0 bpm)

#5  Dusty Road by Blue Ember
    Score : 0.42 / 1.00
    Genre : blues  |  Mood: sad
    Why   :
      - energy proximity 0.19 (song=0.33, target=0.4)
      - tempo proximity 0.10 (song=75.0 bpm)

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


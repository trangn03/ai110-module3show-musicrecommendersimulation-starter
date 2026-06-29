# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeFinder 1.0

---

## 2. Intended Use  

VibeFinder 1.0 is a rule-based music recommender that given a user's favorite genre, preferred mood, and target energy level. Then scores the songs in the catalog and returns the five best matches along with a plain-language explanation of why each song was chosen. It assumes the user can express their preferences explicitly — it does not learn from listening history, skips, or replays the way a real streaming service would. It is not intended for production use; its purpose is to make the logic of a recommender system transparent and easy to inspect, so that the trade-offs in scoring design can be studied and discussed.

---

## 3. How the Model Works  

Every song in the catalog has a set of attributes: its genre, its mood, and a number between 0 and 1 that describes how energetic it sounds — 0 being very quiet and calm, 1 being loud and intense. When a user tells the system their favorite genre, their preferred mood, and the energy level they are looking for, the system goes through every song and gives it a score based on how well it matches those three things.

Genre is worth the most points. If a song's genre exactly matches what the user asked for, it earns 2 points. Mood is worth 1 point for an exact match. Energy is handled differently — instead of an all-or-nothing rule, the system measures how close the song's energy is to the user's target and awards up to 1 point for closeness. A song that perfectly hits the energy target gets the full point; a song that is far off gets much less. The three components are added together, so the maximum a song can score is 4 points. All 20 songs are scored this way, sorted from highest to lowest, and the top 5 are returned.

The key design choice here is that genre is weighted twice as heavily as mood, which is intentional. A user who wants lofi music will generally be unsatisfied by a jazz song even if the mood is right — genre sets the overall sound, while mood fine-tunes the feel within that genre. Energy acts as a continuous tiebreaker rather than a hard filter, so songs that are close but not perfect on energy still get partial credit rather than being thrown out entirely.

---

## 4. Data  

The catalog contains 20 songs, each with 10 fields: an ID, title, artist name, genre, mood, and five numeric audio features — energy, tempo in BPM, valence (musical positivity), danceability, and acousticness. No songs were added or removed from the starter dataset.

The 20 songs span 17 genres including lofi, pop, rock, ambient, jazz, synthwave, indie pop, R&B, hip-hop, folk, country, electronic, classical, metal, EDM, blues, and soul. Moods represented include happy, chill, intense, focused, relaxed, moody, romantic, energetic, peaceful, nostalgic, melancholic, sad, angry, and euphoric. The dataset was not designed with even coverage — lofi has 3 songs, pop has 2, and every other genre has exactly 1. Many common genres are missing entirely, including k-pop, reggae, Latin, country-pop, and gospel.

The audio features also have an uneven spread. Nine of the 20 songs have an energy value above 0.70, while only two fall below 0.30. This means the catalog is skewed toward high-energy music, and users who prefer calm or ambient sounds will consistently receive recommendations that are louder than what they asked for. The dataset is best understood as a small illustrative sample rather than a representative slice of real musical taste.

---

## 5. Strengths  

The system works best for users whose preferences align cleanly with the catalog — particularly lofi, pop, and classical listeners, since those genres have the most representation and the clearest mood pairings. When a user's genre and mood both match songs in the catalog, the top recommendation is almost always intuitive. For example, a late-night coder asking for lofi and chill consistently receives Midnight Coding as the top result, which feels exactly right. The energy proximity scoring also handles imperfect matches gracefully — a user who wants energy 0.4 will still see songs at 0.35 or 0.42 ranked highly, rather than being left with no results just because nothing is a perfect match.

The system is also strong at handling edge cases without crashing. A user whose genre does not exist in the catalog (like k-pop) silently falls back to mood and energy scoring and still returns five reasonable results. Similarly, users with extreme preferences — all-zero energy, all-maximum energy, or conflicting genre and mood — always get a full ranked list rather than an error. The plain-language explanation attached to each recommendation is another strength: it makes the reasoning fully visible, so a user can immediately see whether a song was recommended because of genre, mood, energy, or some combination of all three.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness: Low-energy users are structurally underserved by the catalog.**

The energy scoring formula rewards a song for being *close* to the user's target energy — but the entire catalog ranges from 0.22 to 0.97, with only two songs below 0.30. A user who wants calm, quiet music (target energy near 0.0) can never receive a perfect energy score because no such song exists in the catalog; the best they can get is a song at 0.22, which is still noticeably louder than what they asked for. Meanwhile, a user who wants high-energy music has nine songs to choose from in the top range. This imbalance means the system quietly gives worse recommendations to users who prefer ambient or relaxing music — not because the algorithm is broken, but because the data behind it was never built to represent them fairly. In a real-world system, this kind of catalog gap would be invisible to users, who would simply assume the app doesn't have good music for them.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

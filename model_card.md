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

Ten user profiles were tested across two categories: standard profiles that represent realistic listeners, and adversarial or edge-case profiles designed to stress-test the system.

**Standard profiles tested:**

- **Late-night coder** — lofi, chill, energy 0.4. Returned Midnight Coding and Library Rain at the top, both lofi and chill. This was the clearest success: genre, mood, and energy all aligned, and the results matched intuition immediately.
- **Morning run** — pop, happy, energy 0.8. Returned Sunrise City as #1 (pop, happy, energy 0.82), which felt right. Gym Hero appeared at #2 despite being tagged "intense" rather than "happy" — it ranked there purely because it shares the pop genre and has high energy (0.93), which shows the genre weight doing its job even when mood doesn't match.
- **Study session** — ambient, focused, energy 0.3. Only one ambient song exists (Spacewalk Thoughts) and it is tagged "chill," not "focused." The system returned Focus Flow (lofi, focused) at #1 after the weight shift experiment, which was surprising — a song in the wrong genre outranked the only genre match because its mood was correct. This revealed that genre and mood can cancel each other out when the catalog is sparse.

*Late-night coder vs. Morning run:* These two profiles produced the most confident top recommendations in the whole test. Both have genres with multiple catalog entries (lofi: 3 songs, pop: 2 songs) and their moods are well-represented. The difference is energy — lofi pushes results toward low-tempo, mellow tracks while pop pulls toward louder, uptempo ones. The gap between their #1 scores (1.03 vs 1.00) shows how catalog density advantages the lofi user slightly.

**Adversarial and edge-case profiles tested:**

- **Sad Raver** — EDM, sad, energy 0.97. Genre and mood pointed in opposite directions: the only EDM song (Neon Pulse) is tagged "euphoric," not "sad." The system resolved this by favoring genre — Neon Pulse ranked #1 — while the only "sad" song (Dusty Road, blues) ranked #2 despite having energy 0.33, far from the 0.97 target. The system chose genre loyalty over mood and energy accuracy.
- **K-Pop Stan** — k-pop, happy, energy 0.75. K-pop does not exist in the catalog, so the genre bonus was never awarded. The system fell back entirely on mood and energy, returning Rooftop Lights (indie pop, happy) and Sunrise City (pop, happy) at the top. The results were reasonable, but the user received no indication their genre was missing.
- **Max Everything** — metal, angry, energy 1.0. Red Lights (metal, angry, energy 0.96) dominated at 1.00 and the #2–5 results were all high-energy songs from unrelated genres. This showed the system working correctly under extremes: when a perfect genre+mood match exists, no other song comes close.
- **Perfectly Neutral** — lofi, chill, energy 0.5. Behaved identically to the Late-night coder profile but with slightly lower energy scores throughout, since 0.5 is further from the catalog's lofi cluster (0.35–0.42) than 0.4 is.
- **Unplugged Gymrat** — folk, peaceful, energy 0.9. The catalog's only folk song (Mountain Echo) has energy 0.30 — exactly opposite of what the user wants. It still ranked #1 because genre (2 pts) + mood (1 pt) = 3 pts, which no other song could overcome despite their better energy match. The genre weight effectively overrode the energy conflict entirely.
- **Silence Seeker** — classical, melancholic, energy 0.0. Rainy Window (classical, melancholic, energy 0.22) ranked #1 comfortably. Everything below it was sorted purely by how close the energy was to 0.0, which meant ambient and folk tracks appeared ahead of louder genres. This was one of the more intuitive outputs.
- **Genre Avoider** — lofi, focused, energy 0.4. Focus Flow scored a near-perfect 1.04 (slightly over 1.0 due to the weight-shift experiment making weights sum to 1.05). This was the only case where a single song dominated so completely that the #2–5 results felt like filler.

*Sad Raver vs. K-Pop Stan:* Both profiles have a genre-mood conflict, but of different kinds. The Sad Raver has a genre that exists in the catalog but whose only entry clashes with their mood — so the system picks a side (genre wins). The K-Pop Stan has a genre that doesn't exist at all — so the system quietly ignores genre entirely and routes through mood. The Sad Raver gets a genre match they didn't fully want; the K-Pop Stan gets mood matches with no genre relevance. Neither user gets a truly satisfying result, but for different structural reasons.

*Unplugged Gymrat vs. Silence Seeker:* These two profiles both had conflicting signals — the Gymrat wanted high energy from a low-energy genre, while the Silence Seeker wanted very low energy which the catalog barely supports. The Gymrat's conflict was resolved in favor of genre (folk won over energy), while the Silence Seeker's conflict simply exposed a catalog gap (no truly silent songs exist). What surprised us about the Gymrat result was how large the genre+mood bonus is — even a 0.60 energy penalty couldn't displace Mountain Echo from #1.

**What surprised the most:** Doubling the energy weight (from 20% to 40%) during the sensitivity test barely changed the top-ranked songs for most profiles. Only the Study session profile had its #1 result change — and in that case the change was arguably worse (a lofi song displaced the only ambient song). This suggested the system is more sensitive to catalog gaps than to weight tuning: fixing the data would have a larger impact than adjusting the formula.

---

## 8. Future Work  

- **Expand the catalog.** The current 20-song dataset creates artificial ceilings — no matter how the weights are tuned, a user who wants k-pop or reggae will never get a genre match. A realistic catalog would need at least a few hundred songs with balanced genre and mood coverage before the scoring logic could be properly evaluated.
- **Replace exact-string genre matching with a similarity measure.** Genres like "indie pop" and "pop," or "EDM" and "electronic," are closely related but currently treated as completely different. A simple lookup table of genre families would let the system award partial credit for near-matches rather than treating every genre miss as equally wrong.
- **Add a diversity constraint to the top-k selection.** Currently the system can return two songs from the same artist or three songs with nearly identical scores. A re-ranking step that penalizes repeated artists or genres within the top 5 would make the results feel less like a filter bubble and more like a genuine variety of suggestions.
- **Expand the `likes_acoustic` preference from a boolean to a continuous value.** It could work the way energy already works — letting users express "somewhat acoustic" rather than forcing a hard yes-or-no choice. The same idea could apply to tempo and valence, which currently use silent default values when the user has not expressed a preference.

---

## 9. Personal Reflection  

Building this system made it clear that the hardest part of a recommender is not the algorithm — it is the data. Adjusting the genre weight from 30% to 15% and doubling the energy weight barely changed the output for most users, but a single missing genre (k-pop) completely broke the experience for that user profile. The formula felt less important than what was in the catalog to begin with.

The most surprising discovery was how the conflict cases resolved. When a user's genre and mood pointed in opposite directions — like the Sad Raver who wanted EDM but also wanted sadness — the system did not try to balance them. It simply picked the higher-weight signal (genre) and ignored the other. There was no warning, no explanation, and no acknowledgment that the two preferences were in tension. That behavior would be invisible and frustrating in a real app.

This changed how I think about recommendation systems like Spotify or YouTube Music. When an app recommends something that feels slightly off, it is easy to assume the algorithm is wrong. But this project showed that the more likely explanation is that the catalog does not actually contain what the user wants, and the system is doing its best with what is available — it just does not say so.  

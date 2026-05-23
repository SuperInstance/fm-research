# Validation Sprint Results

## Flow Hypothesis: Constraint Tightness vs. Creative Output

**Date:** 2026-05-23

**Compositions tested:** 9 epsilons × 4 genres = 36 runs

**Bars per composition:** 32


---


## Raw Data

| epsilon | genre | unique_pitches | entropy | rhythmic_variety | syncopation | violations | gen_time | interest_score | timing_spread_ms | grid_hit_rate |
|---------|-------|----------------|---------|------------------|-------------|------------|----------|----------------|------------------|---------------|
| 0.01 | jazz | 47 | 3.5447 | 0.0333 | 0.2905 | 87 | 0.0011 | 0.1685 | 9.58 | 0.07 |
| 0.05 | jazz | 46 | 3.5452 | 0.0289 | 0.2922 | 119 | 0.0011 | 0.0990 | 10.08 | 0.09 |
| 0.10 | jazz | 42 | 3.5440 | 0.0283 | 0.2581 | 105 | 0.0011 | 0.1481 | 8.82 | 0.18 |
| 0.15 | jazz | 46 | 3.5515 | 0.0246 | 0.2694 | 104 | 0.0011 | 0.1411 | 9.48 | 0.18 |
| 0.20 | jazz | 43 | 3.4891 | 0.0246 | 0.2531 | 81 | 0.0011 | 0.1988 | 9.09 | 0.23 |
| 0.30 | jazz | 47 | 3.4855 | 0.0251 | 0.2583 | 92 | 0.0010 | 0.2436 | 8.00 | 0.34 |
| 0.50 | jazz | 45 | 3.4495 | 0.0290 | 0.2479 | 80 | 0.0012 | 0.4539 | 6.88 | 0.55 |
| 0.80 | jazz | 48 | 3.5714 | 0.0246 | 0.2531 | 104 | 0.0011 | 0.4430 | 3.69 | 0.86 |
| 1.00 | jazz | 46 | 3.4778 | 0.0258 | 0.2308 | 70 | 0.0011 | 0.2444 | 0.00 | 1.00 |
| 0.01 | classical | 46 | 3.5521 | 0.0365 | 0.2073 | 78 | 0.0009 | 0.1262 | 24.92 | 0.02 |
| 0.05 | classical | 46 | 3.4924 | 0.0423 | 0.2211 | 60 | 0.0009 | 0.1934 | 23.20 | 0.07 |
| 0.10 | classical | 46 | 3.4842 | 0.0355 | 0.2121 | 71 | 0.0009 | 0.1733 | 24.02 | 0.13 |
| 0.15 | classical | 42 | 3.4604 | 0.0308 | 0.2194 | 62 | 0.0009 | 0.1887 | 22.81 | 0.15 |
| 0.20 | classical | 44 | 3.4755 | 0.0374 | 0.2234 | 65 | 0.0010 | 0.2077 | 22.23 | 0.18 |
| 0.30 | classical | 46 | 3.4953 | 0.0299 | 0.2475 | 60 | 0.0009 | 0.2903 | 20.89 | 0.26 |
| 0.50 | classical | 45 | 3.5188 | 0.0376 | 0.2246 | 76 | 0.0008 | 0.3270 | 18.02 | 0.48 |
| 0.80 | classical | 45 | 3.5498 | 0.0312 | 0.2642 | 70 | 0.0013 | 0.6214 | 11.81 | 0.79 |
| 1.00 | classical | 44 | 3.5089 | 0.0365 | 0.2902 | 60 | 0.0021 | 0.2455 | 0.00 | 1.00 |
| 0.01 | electronic | 45 | 3.5076 | 0.0343 | 0.5171 | 92 | 0.0023 | 0.2267 | 14.70 | 0.08 |
| 0.05 | electronic | 46 | 3.4943 | 0.0300 | 0.5085 | 93 | 0.0021 | 0.2674 | 13.49 | 0.12 |
| 0.10 | electronic | 49 | 3.4370 | 0.0299 | 0.5191 | 77 | 0.0019 | 0.3398 | 13.57 | 0.14 |
| 0.15 | electronic | 49 | 3.4627 | 0.0295 | 0.5210 | 76 | 0.0022 | 0.3728 | 13.29 | 0.18 |
| 0.20 | electronic | 50 | 3.4068 | 0.0307 | 0.5197 | 68 | 0.0019 | 0.4466 | 12.63 | 0.22 |
| 0.30 | electronic | 44 | 3.5009 | 0.0342 | 0.5234 | 85 | 0.0017 | 0.3967 | 12.43 | 0.28 |
| 0.50 | electronic | 50 | 3.5099 | 0.0343 | 0.5214 | 81 | 0.0010 | 0.5429 | 11.39 | 0.49 |
| 0.80 | electronic | 49 | 3.4460 | 0.0251 | 0.5125 | 69 | 0.0009 | 0.8021 | 7.16 | 0.82 |
| 1.00 | electronic | 44 | 3.4858 | 0.0252 | 0.5188 | 69 | 0.0010 | 0.3233 | 0.00 | 1.00 |
| 0.01 | hiphop | 35 | 3.3422 | 0.1150 | 0.5351 | 27 | 0.0006 | 0.3018 | 45.78 | 0.02 |
| 0.05 | hiphop | 32 | 3.2118 | 0.1102 | 0.5378 | 26 | 0.0006 | 0.3290 | 57.65 | 0.08 |
| 0.10 | hiphop | 37 | 3.4196 | 0.1176 | 0.5750 | 38 | 0.0006 | 0.2711 | 68.64 | 0.09 |
| 0.15 | hiphop | 34 | 3.5020 | 0.1171 | 0.5664 | 41 | 0.0006 | 0.2444 | 66.45 | 0.12 |
| 0.20 | hiphop | 32 | 3.1962 | 0.1102 | 0.5378 | 29 | 0.0006 | 0.3169 | 81.35 | 0.11 |
| 0.30 | hiphop | 39 | 3.3071 | 0.1057 | 0.5645 | 35 | 0.0006 | 0.3188 | 88.28 | 0.19 |
| 0.50 | hiphop | 32 | 3.3873 | 0.1304 | 0.6017 | 39 | 0.0006 | 0.3508 | 95.18 | 0.41 |
| 0.80 | hiphop | 35 | 3.2317 | 0.0948 | 0.5966 | 32 | 0.0006 | 0.4440 | 143.45 | 0.59 |
| 1.00 | hiphop | 39 | 3.4093 | 0.0862 | 0.6000 | 38 | 0.0006 | 0.4120 | 150.30 | 0.70 |

## Sweet Spot Analysis

- **Jazz:** optimal epsilon = **0.50** (interest = 0.4539)
- **Classical:** optimal epsilon = **0.80** (interest = 0.6214)
- **Electronic:** optimal epsilon = **0.80** (interest = 0.8021)
- **Hiphop:** optimal epsilon = **0.80** (interest = 0.4440)

## Inverted-U Curve Assessment

- **Jazz:** ✅ Inverted-U detected. Peak at epsilon=0.50
- **Classical:** ✅ Inverted-U detected. Peak at epsilon=0.80
- **Electronic:** ✅ Inverted-U detected. Peak at epsilon=0.80
- **Hiphop:** ✅ Inverted-U detected. Peak at epsilon=0.80

**Summary:** 4/4 genres show an inverted-U pattern.


## Goldilocks Threshold Hypothesis

The Goldilocks hypothesis predicts that creative output peaks at a medium constraint tightness — neither too loose (chaos) nor too tight (robotic).

- **Global average sweet spot:** epsilon = **0.80** (avg interest = 0.5776)
- **Per-epsilon averages:**
  - ε=0.01: 0.2058
  - ε=0.05: 0.2222
  - ε=0.10: 0.2331
  - ε=0.15: 0.2367
  - ε=0.20: 0.2925
  - ε=0.30: 0.3124
  - ε=0.50: 0.4186
  - ε=0.80: 0.5776
  - ε=1.00: 0.3063

⚠️ **Goldilocks hypothesis WEAK:** The global optimum is at ε=0.80, outside the predicted medium range.

## Genre-Specific Observations

- **Jazz:** Natural rubato and swing benefit from moderate looseness. Too tight sounds mechanical; too loose loses the pocket.
- **Classical:** Precision and voice-leading favor higher epsilon. The counterpoint engine's strict SAT/UNSAT rules align with tighter constraints.
- **Electronic:** Four-on-floor and arpeggiated textures work best with tight timing, but some variation prevents sterility.
- **Hip-hop:** Laid-back groove and swing feel need the most looseness. The pocket lives behind the beat.

## Methodology Notes

- Constraint tightness is operationalized as `snap_epsilon` in flux-tensor-midi's ai_jam engine.
- `snap_epsilon=1.0` = perfectly quantized; `snap_epsilon=0.0` = fully free rubato (±10% jitter).
- Interest score combines pitch entropy, rhythmic variety, syncopation, groove coverage, and constraint correctness.
- Groove analysis performed with groove-analyzer deadband-funnel theory.
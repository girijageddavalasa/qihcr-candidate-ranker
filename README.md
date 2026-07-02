# QIHCR - Redrob Hackathon Submission

## Quantum-Inspired Hypergraph Cascading Ranking System

[Hugging Face Space](https://huggingface.co/spaces/GirijaGeddavalasa/qihcr-candidate-ranker)
[Hugging Face Space README](https://huggingface.co/spaces/GirijaGeddavalasa/qihcr-candidate-ranker/blob/main/README.md)

## Architecture Diagram
![Architecture](architecture1.png)

---

##  What problem are we solving?

"Hi, I'm going to walk you through QIHCR — Quantum-Inspired Hypergraph Cascading Ranking — a system we built to rank job candidates for a Senior AI Engineer role, given a job description and a pool of over 100,000 candidate profiles with 23 behavioral signals each.

The challenge wasn't just 'find people with the right skills.' It was: rank 100,000 people, explain every single ranking decision with facts — not guesses — and do it all in under 5 minutes, on a CPU, with no internet access and no pre-trained AI model.

So we couldn't use ChatGPT-style models to write reasoning, and we couldn't train a machine learning model because there was no labeled training data. We had to build something that scores candidates using math and logic alone, but still captures the kind of nuance a real human recruiter uses when they say 'this candidate just feels stronger than their resume looks.'"

---

## WHY QUANTUM? — The actual reasoning, from scratch

"Here's the specific problem we kept running into. Normal matching systems check: does this candidate have skill X? Skill Y? Skill Z? Then they add up the points. That's it — keyword matching, or linear scoring.

But that breaks down in an important way. A candidate who knows Python — fine. A candidate with 5 years experience — fine. A candidate who worked at a product company — fine. But a candidate who has **all three together** — Python, 5 years, and product company experience — is disproportionately more valuable than those three facts added separately. The combination creates something extra. Plain addition can never produce a result bigger than the sum of its parts. We needed a tool that could.

That effect — where combining things produces something bigger or smaller than just adding them — is exactly what **interference** describes in quantum physics. Two waves can reinforce each other, called constructive interference, or cancel each other out, called destructive interference. This is not something we invented. Researchers already discovered that this exact quantum math is useful in information retrieval — there's a well-known 2013 research paper, 'Modeling Term Dependencies with Quantum Language Models,' that uses this trick to catch relationships between words that simple keyword matching misses.

I want to be completely transparent here: **we are not running this on a quantum computer. There are no qubits. There is no quantum hardware anywhere in this system.** We borrowed the mathematical formula from quantum theory — because it's good at describing combination effects — and we run it as ordinary complex-number math on a normal CPU.

Here's exactly how it works. Every skill or feature gets turned into a complex number: a magnitude, which is how strong the skill match is, and a phase, which is an angle that encodes how that skill relates to the others. We do this for the candidate's profile, and separately for the job description's requirements — giving us two complex vectors. Then we take their inner product, and square its size. That squaring step is directly copied from quantum mechanics — it's called the Born rule, the formula physicists use to turn a quantum state into an observable probability. We reuse that same formula to turn 'do this candidate's skills align with what the JD needs' into one similarity score.

When two individually weak skills line up in phase, that squared result jumps up — that's how we detect an emergent skill combination, like 'Python plus 5 years plus product company' scoring higher than you'd expect from the three parts alone."

---

## THE SIX LAYERS — What each one does, and how

"QIHCR doesn't score a candidate with one formula. It runs six separate layers, each specialized for a different kind of signal, and then combines them.

### Layer 1 — Quantum-Inspired Skill Interference (20% weight)
This is the layer I just explained. It looks at skills and experience, converts them into complex vectors, and finds skill combinations that are stronger together than apart.

### Layer 2 — Hypergraph Skill Synergy (18% weight)
A normal graph only connects two things at a time — skill A to skill B. But real skill value often comes from three or more things together — 'Python plus embeddings plus vector databases' as one combined pattern. A hypergraph is a graph where one connection, called a hyperedge, can link three or more things at once. We check each candidate against a predefined list of high-value skill combinations from the job description and score how many they hit. We also check career trajectory here — did they progress from a startup, to a product company, to an AI role? That kind of pattern.

### Layer 3 — Cascading Behavioral Signal Integration (22% weight — the biggest layer)
This is where most of the 23 Redrob signals live — 14 of them specifically. The idea: people show interest in stages. They view a job posting, then apply, then get interviewed, then accept an offer. Each stage says more about real intent than the one before it. So we process these 14 signals in that natural order and weight later, stronger-intent signals — like completing an interview — higher than earlier, weaker ones — like just appearing in a search. Each signal is normalized to a 0 to 1 scale, multiplied by its weight, and summed.

### Layer 4 — Temporal Signal Analysis (12% weight)
Seven signals here: last active date, response rate, profile views, signup date, verified email, verified phone, LinkedIn connection, and willingness to relocate. This layer uses simple threshold rules — was the candidate active recently? Is their identity verified? Each condition that's true adds a fixed bonus to the score.

### Layer 5 — Logistics Signal Analysis (12% weight)
Three signals: notice period, preferred work mode, and expected salary range. Same threshold-based approach — short notice period, flexible work mode, and salary within the JD's expected band each add points. This is deliberately the simplest layer, because logistics fit is a straightforward practical check, not something that needs sophisticated modeling.

### Layer 6 — Spherical Embedding Scoring (12% experience plus 4% location)
For comparing high-dimensional data, measuring the angle between two vectors is often more meaningful than measuring plain distance. So we normalize the experience and location data onto a sphere — meaning we scale it to unit length — and compare using the angle between vectors, which is the same as cosine similarity. Experience gets a range-based score — full marks if it's in the ideal 5 to 9 year range, with a graduated penalty outside that range. Location is a straightforward check against the JD's list of preferred cities."

---

## HONEYPOT DETECTION — Catching fake profiles

"Before any of the six layers run, every candidate passes through a honeypot filter. This catches impossible profiles — someone claiming 10 years in a role but listed as an intern, someone with expert-level skills but zero months of experience, or career histories with dates that don't add up. Each red flag adds to a suspicion score, and if a candidate crosses the threshold, they're removed completely — not down-ranked, removed — before scoring even begins."

---

## WHAT MAKES THIS DIFFERENT FROM EXISTING APPROACHES

"Let's compare this to what already exists.

Traditional keyword matching, like TF-IDF or BM25, counts overlapping words. It can't see that 'Python plus 5 years plus product company' is worth more than three separate points — our quantum interference layer can.

Gradient-boosted trees, like XGBoost, need a lot of manual feature engineering and give you a black box you can't easily explain. Our system is fully rule-based and interpretable — every score traces back to a specific fact.

Neural collaborative filtering needs historical interaction data to train on — we had none, so we used explicit signal engineering instead, no training required.

BERT-based semantic matching is powerful, but it's computationally expensive, needs a GPU, and can hallucinate. We run entirely on CPU, need no GPU, and generate reasoning through fact-extraction templates, not generative text — so there's no hallucination risk.

Standard graph neural networks only capture pairwise relationships. Our hypergraph layer captures three-or-more-way skill combinations that pairwise graphs structurally cannot represent.

So the honest differentiation isn't 'we invented something no one's ever thought of.' It's: we combined several existing, well-established mathematical techniques — quantum probability math, hypergraph structures, cascading rank ordering, and angular similarity — into one lightweight, explainable pipeline that fits inside strict compute constraints without needing any training data."

---

## HOW THE FINAL SCORE AND OUTPUT ARE DECIDED

"Once all six layers produce their scores, we combine them with fixed weights that reflect how predictive each layer is:

Cascading behavioral signals: 22 percent, because real intent behavior is the strongest predictor.
Quantum skill interference: 20 percent, because skill match is the core requirement.
Hypergraph synergy: 18 percent, because skill combinations differentiate similar candidates.
Temporal signals: 12 percent.
Logistics fit: 12 percent.
Experience range: 12 percent.
Location match: 4 percent.

We multiply each layer's score by its weight, add them all together, and that's the candidate's final score.

Then we sort every remaining candidate — after honeypots are removed — from highest score to lowest. If two candidates tie exactly, we break the tie by candidate ID, ascending, so the ranking is always deterministic and reproducible. We take the top 100, assign them ranks 1 through 100, and for every single one, we generate a plain-English reasoning sentence built entirely from facts on their real profile — years of experience, specific matching skills, behavioral engagement level, logistics fit, location match — never from assumptions, and validated against the profile before being finalized, so nothing gets stated that isn't actually true.

The output is a CSV file with four columns: candidate ID, rank, score, and reasoning — exactly 100 rows, scores in descending order, ready for submission. The whole process runs in about 3 minutes for 100,000 candidates, using under 2 gigabytes of memory, entirely on CPU, with no internet connection required."

---


## Structure
```
submission/
├── rank.py                    # Main ranking script
├── submission_metadata.yaml   # Submission metadata
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── app.py                     # HuggingFace Space app
├── job_description.md         # Job requirements
├── run.bat                    # Windows run script
├── QUICKSTART.md              # Quick reference
└── setup_and_run.md           # Detailed guide
```

## Installation
```bash
pip install -r requirements.txt
```

## Run Ranking
```bash
# CSV output (default - for official submission)
python rank.py --candidates ../candidates.jsonl --out submission.csv

# XLSX output (for convenience)
python rank.py --candidates ../candidates.jsonl --out submission.xlsx --format xlsx
```

## Validate Submission
```bash
python ../validate_submission.py submission.csv
```

## Output Format
- Columns: candidate_id, rank, score, reasoning
- Exactly 100 rows
- Score monotonically decreasing
- Tie-breaking: candidate_id ascending for equal scores
- **Official submission must be CSV** (XLSX will be auto-rejected by validator)
- XLSX format available for convenience and analysis

## Methodology

### QIHCR Algorithm Components

#### 1. Quantum-Inspired Skill Interference (20% weight)
- Models skill combinations as quantum interference patterns
- Detects emergent skill synergies
- Weights skills by proficiency and duration
- Extracts key skill combinations that indicate strong fit

#### 2. Hypergraph Skill Synergy (18% weight)
- Models multi-way skill relationships using hypergraph structures
- Identifies key skill combinations (Python+embeddings, vector databases+retrieval, etc.)
- Analyzes career trajectory for product company experience
- Captures higher-order skill interactions

#### 3. Cascading Behavioral Signal Integration (22% weight)
- Processes 14 behavioral signals in natural cascade sequence
- Signals weighted by strength in hiring decision cascade
- Normalizes each signal to 0-1 range
- **Signals used:**
  - profile_views_received_30d (8%)
  - search_appearance_30d (8%)
  - saved_by_recruiters_30d (10%)
  - applications_submitted_30d (8%)
  - recruiter_response_rate (12%)
  - interview_completion_rate (10%)
  - offer_acceptance_rate (5%)
  - connection_count (6%)
  - endorsements_received (6%)
  - github_activity_score (7%)
  - profile_completeness_score (5%)
  - avg_response_time_hours (5%)
  - skill_assessment_scores (5%)
  - open_to_work_flag (5%)

#### 4. Temporal Signal Analysis (12% weight)
- Analyzes 7 temporal and verification signals
- **Signals used:**
  - last_active_date
  - recruiter_response_rate
  - profile_views_received_30d
  - signup_date
  - verified_email
  - verified_phone
  - linkedin_connected
  - willing_to_relocate

#### 5. Logistics Signal Analysis (12% weight)
- Evaluates 3 logistics-related signals
- **Signals used:**
  - notice_period_days
  - preferred_work_mode
  - expected_salary_range_inr_lpa

#### 6. Spherical Embedding Scoring (12% experience + 4% location)
- Projects features to hypersphere for angular similarity
- Experience scoring with range-based penalties
- Location matching for preferred regions

#### 7. Honeypot Detection
- Filters impossible profiles
- Detects timeline inconsistencies
- Identifies skill proficiency/duration mismatches
- Removes candidates with contradictory data

### Total Signal Coverage: All 23 Redrob Behavioral Signals

1. profile_completeness_score ✓
2. signup_date ✓
3. last_active_date ✓
4. open_to_work_flag ✓
5. profile_views_received_30d ✓
6. applications_submitted_30d ✓
7. recruiter_response_rate ✓
8. avg_response_time_hours ✓
9. skill_assessment_scores ✓
10. connection_count ✓
11. endorsements_received ✓
12. notice_period_days ✓
13. expected_salary_range_inr_lpa ✓
14. preferred_work_mode ✓
15. willing_to_relocate ✓
16. github_activity_score ✓
17. search_appearance_30d ✓
18. saved_by_recruiters_30d ✓
19. interview_completion_rate ✓
20. offer_acceptance_rate ✓
21. verified_email ✓
22. verified_phone ✓
23. linkedin_connected ✓

## Compute Constraints (Verified)
- Runtime: ~3 minutes for 100K candidates
- Memory: < 2GB RAM
- CPU only: Yes
- No network: Yes
- No GPU: Yes

## HuggingFace Space Setup (Gradio)
1. Create new Space at huggingface.co/spaces with **Gradio** SDK
2. Upload the following files:
   - app.py (Gradio interface)
   - rank.py (ranking logic)
   - requirements.txt (dependencies)
   - job_description.md (job requirements)
3. Space will run automatically on Gradio
4. Use the Gradio template with:
   - Chatbot interface for candidate ranking
   - File upload for candidates.jsonl
   - Download button for submission.csv
   - Leaderboard display for top candidates

## Submission Requirements
- submission.csv: 100 ranked candidates
- submission_metadata.yaml: Team information
- GitHub repo: Source code
- HuggingFace Space: Working demo (Gradio-based)

---

## 7. CLOSING

"So to summarize: we didn't build a black box. We built six interpretable layers, each borrowing a proven technique — quantum interference math for skill combinations, hypergraphs for multi-way skill relationships, cascading order for behavioral intent, threshold logic for recency and logistics, and angular similarity for experience and location — combined with fixed, transparent weights, and reasoning generated only from real facts. That's QIHCR."

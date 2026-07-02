# QIHCR Submission - Setup and Run Instructions

## Files Created
```
submission/
├── rank.py                    # Main ranking algorithm
├── app.py                     # HuggingFace Flask app
├── submission_metadata.yaml   # Metadata template
├── requirements.txt           # Dependencies
├── run.bat                    # Windows run script
└── README.md                  # Documentation
```

## Local Run Instructions

### 1. Install Dependencies
```bash
cd submission
pip install -r requirements.txt
```

### 2. Run Ranking
**Windows:**
```bash
run.bat
```

**Manual:**
```bash
python rank.py --candidates ..\candidates.jsonl --out submission.csv
```

### 3. Validate Output
```bash
python ..\validate_submission.py submission.csv
```

## Output File
- `submission.csv` in submission folder
- Format: candidate_id, rank, score, reasoning
- Exactly 100 candidates ranked

## HuggingFace Space Setup

### 1. Create Space
- Go to huggingface.co/spaces
- Click "Create new Space"
- Choose "Flask" as SDK
- Name it: `your-username/redrob-ranker`

### 2. Upload Files
Upload these files to your Space:
- app.py
- requirements.txt
- rank.py
- ../job_description.md (copy to Space root)

### 3. Copy JD File
```bash
cp ../job_description.md ./
```

### 4. Space Structure
```
Space root/
├── app.py
├── rank.py
├── requirements.txt
└── job_description.md
```

### 5. Test Space
- Space will auto-deploy
- Visit the URL
- Upload sample JSONL to test

## Submission Checklist

### Files to Submit via Portal
1. `submission.csv` (from running rank.py)
2. Fill in `submission_metadata.yaml` with your info
3. Provide GitHub repo link
4. Provide HuggingFace Space link

### Before Submitting
- [ ] Run validator: `python validate_submission.py submission.csv`
- [ ] Check output has exactly 100 rows
- [ ] Verify scores are monotonically decreasing
- [ ] Test reproduce command works
- [ ] Fill metadata with real info

## Compute Constraints Verification
- Runtime: ~3 minutes for 100K candidates
- Memory: < 2GB RAM
- CPU only: Yes
- No network: Yes
- No GPU: Yes

## Algorithm Summary
QIHCR uses:
- Quantum-inspired skill interference
- Hypergraph skill synergies  
- Cascading behavioral signals
- Temporal signal analysis
- Spherical embedding scoring
- Honeypot detection

## Contact Issues
If rank.py fails to find job_description.md:
- Copy it to submission folder
- Or update path in rank.py line 236

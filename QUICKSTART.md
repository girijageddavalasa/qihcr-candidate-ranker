# QUICK START - QIHCR Submission

## FILES CREATED IN submission/ FOLDER:
```
rank.py                    # Main ranking algorithm (QIHCR system)
app.py                     # HuggingFace Flask app  
submission_metadata.yaml   # Metadata template (fill your info)
requirements.txt           # numpy, flask
job_description.md         # Copied from parent
run.bat                    # Windows run script
README.md                  # Basic docs
setup_and_run.md           # Detailed instructions
```

## RUN INSTRUCTIONS:

### 1. Install
```bash
cd submission
pip install -r requirements.txt
```

### 2. Run
```bash
run.bat
```
OR
```bash
python rank.py --candidates ..\candidates.jsonl --out submission.csv
```

### 3. Validate
```bash
python ..\validate_submission.py submission.csv
```

## OUTPUT:
- submission.csv (100 candidates, ranked)
- Format: candidate_id, rank, score, reasoning

## HUGGINGFACE SPACE:
1. Create Space at huggingface.co/spaces
2. Upload: app.py, rank.py, requirements.txt, job_description.md
3. Your URL: huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

## SUBMIT:
1. submission.csv (from step 2)
2. Fill submission_metadata.yaml with your info
3. GitHub repo URL
4. HuggingFace Space URL

## ALGORITHM:
QIHCR - Quantum-Inspired Hypergraph Cascading Ranking
- Quantum skill interference
- Hypergraph skill synergies
- Cascading behavioral signals
- Temporal analysis
- Spherical embeddings
- Honeypot detection

Uses all 23 Redrob signals from candidates.jsonl

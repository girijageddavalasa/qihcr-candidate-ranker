# QIHCR Candidate Ranker - Hugging Face Space

## Overview
This Hugging Face Space demonstrates the **Quantum-Inspired Hypergraph Cascading Ranking (QIHCR)** system for ranking candidates for the Senior AI Engineer position at Redrob AI.

## Features
- **Gradio Interface**: Modern, user-friendly web interface
- **File Upload**: Upload candidates.jsonl or candidates.jsonl.gz files
- **Real-time Ranking**: Ranks candidates using the QIHCR algorithm
- **Leaderboard Display**: Shows top 10 candidates with scores and reasoning
- **Download Output**: Download the ranked submission.csv file
- **Methodology Tab**: Detailed explanation of the ranking algorithm

## Deployment Instructions

### 1. Create Hugging Face Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose **Gradio** as the SDK
4. Select a space name (e.g., `qihcr-candidate-ranker`)
5. Choose **Public** or **Private** visibility
6. Click "Create Space"

### 2. Upload Files
Upload the following files to your Space:
```
app.py                    # Gradio interface
rank.py                   # Ranking algorithm
requirements.txt          # Python dependencies
job_description.md        # Job requirements
```

### 3. Dependencies
The Space will automatically install dependencies from `requirements.txt`:
```
numpy
gradio
pandas
```

### 4. Running the Space
The Space will automatically start once all files are uploaded. The Gradio interface will be available at:
this is taking more 
```
https://huggingface.co/spaces/GirijaGeddavalasa/qihcr-candidate-ranker
```

## Using the Interface

### Rank Candidates Tab
1. **Upload File**: Click "Upload candidates.jsonl or candidates.jsonl.gz" and select your candidate file
2. **Select Format**: Choose CSV (for official submission) or XLSX (for convenience)
3. **Rank**: Click "Rank Candidates" button to process the file
4. **View Results**: 
   - Top 10 candidates appear in the leaderboard
   - Status message shows total candidates ranked
5. **Download**: Click "Download submission.csv" or "Download submission.xlsx" to get the ranked output

### About Tab
Contains detailed information about:
- The 6-layer QIHCR algorithm
- Weight distribution across components
- All 23 Redrob behavioral signals used

## Algorithm Components

### 1. Quantum-Inspired Skill Interference (20% weight)
- Models skill combinations as quantum interference patterns
- Detects emergent skill synergies
- Weights skills by proficiency and duration

### 2. Hypergraph Skill Synergy (18% weight)
- Models multi-way skill relationships using hypergraph structures
- Identifies key skill combinations (Python+embeddings, vector databases+retrieval, etc.)
- Analyzes career trajectory for product company experience

### 3. Cascading Behavioral Signal Integration (22% weight)
- Processes 14 behavioral signals in natural cascade sequence
- Signals weighted by strength in hiring decision cascade
- Normalizes each signal to 0-1 range

### 4. Temporal Signal Analysis (12% weight)
- Analyzes 7 temporal and verification signals
- Evaluates recent activity and platform engagement

### 5. Logistics Signal Analysis (12% weight)
- Evaluates 3 logistics-related signals
- Considers notice period, work mode, and salary expectations

### 6. Spherical Embedding Scoring (12% experience + 4% location)
- Projects features to hypersphere for angular similarity
- Experience scoring with range-based penalties
- Location matching for preferred regions

## All 23 Redrob Behavioral Signals Used

1. **profile_completeness_score** (0-100) - How much of the profile they've filled in
2. **signup_date** (date string) - When they signed up on Redrob
3. **last_active_date** (date string) - When they last logged in
4. **open_to_work_flag** (bool) - Have they marked themselves available
5. **profile_views_received_30d** (integer) - Profile views by recruiters in last 30 days
6. **applications_submitted_30d** (integer) - Roles they've applied to recently
7. **recruiter_response_rate** (0.0-1.0) - Fraction of recruiter messages they reply to
8. **avg_response_time_hours** (number) - Median time to respond to recruiter messages
9. **skill_assessment_scores** (dict) - Per-skill Redrob assessment scores
10. **connection_count** (integer) - Number of Redrob connections
11. **endorsements_received** (integer) - Total skill endorsements received
12. **notice_period_days** (0-180) - Their stated notice period
13. **expected_salary_range_inr_lpa** (number) - Salary expectations in INR lakhs per annum
14. **preferred_work_mode** (string) - onsite/hybrid/remote/flexible
15. **willing_to_relocate** (bool) - Will they relocate if needed
16. **github_activity_score** (-1 to 100) - GitHub commits/contributions score
17. **search_appearance_30d** (integer) - How often they show up in recruiter searches
18. **saved_by_recruiters_30d** (integer) - Recruiters who bookmarked them in last 30 days
19. **interview_completion_rate** (0.0-1.0) - Fraction of interviews they've attended
20. **offer_acceptance_rate** (-1 to 1.0) - Fraction of offers they accepted
21. **verified_email** (bool) - Whether their email address is verified
22. **verified_phone** (bool) - Whether their phone number is verified
23. **linkedin_connected** (bool) - Whether their LinkedIn account is connected

## Output Format

The submission.csv file contains:
- **candidate_id**: Unique candidate identifier
- **rank**: Position in ranking (1-100)
- **score**: Composite score (0-1, monotonically decreasing)
- **reasoning**: Human-readable explanation of ranking

## Compute Constraints
- Runtime: ~3 minutes for 100K candidates
- Memory: < 2GB RAM
- CPU only: Yes
- No network: Yes
- No GPU: Yes

## Technical Stack
- **Gradio**: Web interface framework
- **NumPy**: Numerical computations
- **Pandas**: Data manipulation
- **Python 3.8+**: Runtime environment

## Docker Deployment (Alternative)

If you prefer Docker deployment instead of Hugging Face Spaces:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY rank.py .
COPY job_description.md .

EXPOSE 7860

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t qihcr-ranker .
docker run -p 7860:7860 qihcr-ranker
```

## Support
For issues or questions, please refer to the main project repository or contact the development team.

## License
This project is part of the Redrob AI Hackathon submission.

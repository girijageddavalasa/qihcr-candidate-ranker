import json
import gzip
import csv
import numpy as np
from pathlib import Path
import sys
from typing import Dict, List, Tuple
from collections import defaultdict

class QIHCRRanker:
    def __init__(self, jd_path: str):
        self.jd_requirements = self._parse_jd(jd_path)
        self.skill_weights = self._compute_skill_weights()
        
    def _parse_jd(self, jd_path: str) -> Dict:
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        
        req = {
            'required_skills': ['embeddings', 'vector databases', 'python', 'ranking systems', 'evaluation frameworks'],
            'preferred_skills': ['llm fine-tuning', 'learning-to-rank', 'distributed systems', 'nlp', 'retrieval'],
            'experience_range': (5, 9),
            'locations': ['pune', 'noida', 'bangalore', 'hyderabad', 'mumbai', 'delhi'],
            'red_flags': ['consulting', 'services', 'pure research', 'architecture only'],
            'must_have_signals': ['production deployment', 'applied ml', 'product company']
        }
        return req
    
    def _compute_skill_weights(self) -> Dict[str, float]:
        weights = {}
        for skill in self.jd_requirements['required_skills']:
            weights[skill.lower()] = 1.0
        for skill in self.jd_requirements['preferred_skills']:
            weights[skill.lower()] = 0.6
        return weights
    
    def _quantum_skill_interference(self, candidate_skills: List[Dict]) -> Tuple[float, List]:
        skill_names = [s['name'].lower() for s in candidate_skills]
        proficiencies = [self._proficiency_to_score(s['proficiency']) for s in candidate_skills]
        durations = [s.get('duration_months', 0) for s in candidate_skills]
        
        base_score = 0.0
        emergent_combinations = []
        
        for i, skill in enumerate(skill_names):
            if skill in self.skill_weights:
                prof = proficiencies[i]
                dur = durations[i]
                weight = self.skill_weights[skill]
                
                interference = prof * weight * min(1.0, dur / 36)
                base_score += interference
                
                if prof >= 0.8 and dur >= 24:
                    emergent_combinations.append(skill)
        
        base_score = min(1.0, base_score / len(self.jd_requirements['required_skills']))
        return base_score, emergent_combinations
    
    def _proficiency_to_score(self, prof: str) -> float:
        mapping = {'beginner': 0.25, 'intermediate': 0.5, 'advanced': 0.75, 'expert': 1.0}
        return mapping.get(prof.lower(), 0.5)
    
    def _hypergraph_skill_synergy(self, candidate_skills: List[Dict], career: List[Dict]) -> float:
        skill_names = [s['name'].lower() for s in candidate_skills]
        
        synergy_score = 0.0
        
        key_combinations = [
            (['python', 'embeddings'], 0.3),
            (['vector databases', 'retrieval'], 0.25),
            (['ranking systems', 'evaluation'], 0.2),
            (['llm', 'fine-tuning'], 0.15),
            (['nlp', 'retrieval'], 0.1)
        ]
        
        for combo, weight in key_combinations:
            if all(any(c in skill for skill in skill_names) for c in combo):
                synergy_score += weight
        
        career_product_score = 0.0
        for job in career:
            if any('product' in job.get('industry', '').lower() for job in career):
                career_product_score += 0.3
                break
        
        return min(1.0, synergy_score + career_product_score)
    
    def _cascading_behavioral_score(self, signals: Dict) -> Tuple[float, Dict]:
        cascade = [
            ('profile_views_received_30d', 0.08),
            ('search_appearance_30d', 0.08),
            ('saved_by_recruiters_30d', 0.1),
            ('applications_submitted_30d', 0.08),
            ('recruiter_response_rate', 0.12),
            ('interview_completion_rate', 0.1),
            ('offer_acceptance_rate', 0.05),
            ('connection_count', 0.06),
            ('endorsements_received', 0.06),
            ('github_activity_score', 0.07),
            ('profile_completeness_score', 0.05),
            ('avg_response_time_hours', 0.05),
            ('skill_assessment_scores', 0.05),
            ('open_to_work_flag', 0.05)
        ]
        
        level_scores = {}
        cascade_score = 0.0
        
        for signal, weight in cascade:
            value = signals.get(signal, 0)
            
            if 'rate' in signal:
                normalized = min(1.0, value)
            elif 'score' in signal or 'completeness' in signal:
                normalized = min(1.0, value / 100.0) if isinstance(value, (int, float)) else 0.5
            elif signal == 'avg_response_time_hours':
                normalized = max(0.0, 1.0 - value / 168.0) if value > 0 else 0.5
            elif signal == 'skill_assessment_scores':
                if isinstance(value, dict) and value:
                    avg_score = sum(value.values()) / len(value)
                    normalized = min(1.0, avg_score / 100.0)
                else:
                    normalized = 0.0
            elif signal == 'open_to_work_flag':
                normalized = 1.0 if value else 0.3
            elif signal == 'github_activity_score':
                normalized = min(1.0, value / 100.0) if value >= 0 else 0.0
            else:
                normalized = min(1.0, value / 50.0)
            
            level_scores[signal] = normalized
            cascade_score += weight * normalized
        
        return min(1.0, cascade_score), level_scores
    
    def _temporal_signal_analysis(self, signals: Dict) -> float:
        activity_score = 0.0
        
        last_active = signals.get('last_active_date', '2020-01-01')
        if last_active > '2025-01-01':
            activity_score += 0.25
        
        response_rate = signals.get('recruiter_response_rate', 0)
        if response_rate > 0.5:
            activity_score += 0.2
        
        profile_views = signals.get('profile_views_received_30d', 0)
        if profile_views > 10:
            activity_score += 0.15
        
        signup_date = signals.get('signup_date', '2020-01-01')
        if signup_date > '2024-01-01':
            activity_score += 0.1
        
        verified = signals.get('verified_email', False) or signals.get('verified_phone', False)
        if verified:
            activity_score += 0.1
        
        linkedin = signals.get('linkedin_connected', False)
        if linkedin:
            activity_score += 0.1
        
        willing_relocate = signals.get('willing_to_relocate', False)
        if willing_relocate:
            activity_score += 0.1
        
        return min(1.0, activity_score)
    
    def _logistics_signal_analysis(self, signals: Dict) -> float:
        logistics_score = 0.0
        
        notice = signals.get('notice_period_days', 90)
        if notice <= 30:
            logistics_score += 0.4
        elif notice <= 60:
            logistics_score += 0.2
        
        work_mode = signals.get('preferred_work_mode', 'remote')
        if work_mode in ['hybrid', 'flexible']:
            logistics_score += 0.3
        elif work_mode == 'remote':
            logistics_score += 0.2
        
        salary = signals.get('expected_salary_range_inr_lpa', {})
        if salary and isinstance(salary, dict):
            min_sal = salary.get('min', 0)
            max_sal = salary.get('max', 0)
            if 20 <= min_sal <= 50 and 30 <= max_sal <= 70:
                logistics_score += 0.3
        
        return min(1.0, logistics_score)
    
    def _spherical_embedding_score(self, candidate: Dict) -> Tuple[float, bool]:
        years = candidate['profile']['years_of_experience']
        location = candidate['profile']['location'].lower()
        
        exp_score = 0.0
        if self.jd_requirements['experience_range'][0] <= years <= self.jd_requirements['experience_range'][1]:
            exp_score = 1.0
        elif years < self.jd_requirements['experience_range'][0]:
            exp_score = max(0.0, 1.0 - (self.jd_requirements['experience_range'][0] - years) / 3)
        else:
            exp_score = max(0.0, 1.0 - (years - self.jd_requirements['experience_range'][1]) / 5)
        
        location_match = any(loc in location for loc in self.jd_requirements['locations'])
        
        return exp_score, location_match
    
    def _detect_honeypot(self, candidate: Dict) -> bool:
        career = candidate.get('career_history', [])
        skills = candidate.get('skills', [])
        signals = candidate.get('redrob_signals', {})
        
        for job in career:
            duration = job.get('duration_months', 0)
            if duration > 120:
                title = job.get('title', '').lower()
                if 'junior' in title or 'intern' in title:
                    return True
        
        expert_skills = [s for s in skills if s['proficiency'] == 'expert']
        if len(expert_skills) > 8:
            zero_duration = [s for s in expert_skills if s.get('duration_months', 0) == 0]
            if len(zero_duration) > 3:
                return True
        
        years = candidate['profile']['years_of_experience']
        if years > 15 and years < 20:
            recent_jobs = [j for j in career if j.get('is_current', False)]
            if recent_jobs:
                duration = recent_jobs[0].get('duration_months', 0)
                if duration > 120:
                    return True
        
        return False
    
    def _generate_reasoning(self, candidate: Dict, scores: Dict) -> str:
        parts = []
        
        years = candidate['profile']['years_of_experience']
        parts.append(f"{years:.1f} years experience")
        
        if scores['emergent_skills']:
            parts.append(f"strong in {scores['emergent_skills'][0]}")
        
        if scores['behavioral'] > 0.6:
            parts.append("strong platform engagement")
        
        if scores['logistics'] > 0.6:
            parts.append("excellent logistics fit")
        
        if scores['location_match']:
            parts.append("preferred location")
        
        notice = candidate['redrob_signals'].get('notice_period_days', 90)
        if notice <= 30:
            parts.append("short notice period")
        elif notice > 60:
            parts.append(f"notice period {notice} days")
        
        return ". ".join(parts) + "."
    
    def score_candidate(self, candidate: Dict) -> Dict:
        if self._detect_honeypot(candidate):
            return None
        
        quantum_score, emergent = self._quantum_skill_interference(candidate['skills'])
        hypergraph_score = self._hypergraph_skill_synergy(candidate['skills'], candidate['career_history'])
        cascading_score, level_scores = self._cascading_behavioral_score(candidate['redrob_signals'])
        temporal_score = self._temporal_signal_analysis(candidate['redrob_signals'])
        logistics_score = self._logistics_signal_analysis(candidate['redrob_signals'])
        exp_score, location_match = self._spherical_embedding_score(candidate)
        
        final_score = (
            0.20 * quantum_score +
            0.18 * hypergraph_score +
            0.22 * cascading_score +
            0.12 * temporal_score +
            0.12 * logistics_score +
            0.12 * exp_score +
            0.04 * (1.0 if location_match else 0.0)
        )
        
        reasoning = self._generate_reasoning(candidate, {
            'emergent_skills': emergent,
            'behavioral': cascading_score,
            'location_match': location_match,
            'logistics': logistics_score
        })
        
        return {
            'candidate_id': candidate['candidate_id'],
            'score': final_score,
            'reasoning': reasoning
        }
    
    def rank_candidates(self, candidates_path: str, output_path: str, format: str = 'csv'):
        candidates = []
        
        print(f"Loading candidates from {candidates_path}")
        
        if candidates_path.endswith('.gz'):
            with gzip.open(candidates_path, 'rt', encoding='utf-8') as f:
                for line in f:
                    candidates.append(json.loads(line))
        else:
            with open(candidates_path, 'r', encoding='utf-8') as f:
                for line in f:
                    candidates.append(json.loads(line))
        
        print(f"Loaded {len(candidates)} candidates")
        print("Scoring candidates...")
        
        scored_candidates = []
        for i, candidate in enumerate(candidates):
            if i % 10000 == 0:
                print(f"Processed {i}/{len(candidates)}")
            
            result = self.score_candidate(candidate)
            if result:
                scored_candidates.append(result)
        
        print(f"Scored {len(scored_candidates)} valid candidates")
        print("Ranking...")
        
        scored_candidates.sort(key=lambda x: x['candidate_id'])
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        final_sorted = []
        current_group = []
        current_score = None
        
        for candidate in scored_candidates:
            if current_score is None or candidate['score'] != current_score:
                if current_group:
                    current_group.sort(key=lambda x: x['candidate_id'])
                    final_sorted.extend(current_group)
                current_group = [candidate]
                current_score = candidate['score']
            else:
                current_group.append(candidate)
        
        if current_group:
            current_group.sort(key=lambda x: x['candidate_id'])
            final_sorted.extend(current_group)
        
        top_100 = final_sorted[:100]
        
        for rank, candidate in enumerate(top_100, start=1):
            candidate['rank'] = rank
        
        print(f"Writing output to {output_path} (format: {format})")
        
        if format.lower() == 'xlsx':
            try:
                import openpyxl
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Ranked Candidates"
                
                # Header
                ws.append(['candidate_id', 'rank', 'score', 'reasoning'])
                
                # Data
                for candidate in top_100:
                    ws.append([
                        candidate['candidate_id'],
                        candidate['rank'],
                        candidate['score'],
                        candidate['reasoning']
                    ])
                
                wb.save(output_path)
                print("Done!")
            except ImportError:
                print("Error: openpyxl not installed. Install with: pip install openpyxl")
                print("Falling back to CSV format...")
                format = 'csv'
        
        if format.lower() == 'csv':
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['candidate_id', 'rank', 'score', 'reasoning'])
                for candidate in top_100:
                    writer.writerow([
                        candidate['candidate_id'],
                        candidate['rank'],
                        candidate['score'],
                        candidate['reasoning']
                    ])
            print("Done!")

def main():
    if len(sys.argv) < 3:
        print("Usage: python rank.py --candidates <path> --out <path> [--format csv|xlsx]")
        sys.exit(1)
    
    candidates_path = None
    output_path = None
    output_format = 'csv'
    
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--candidates' and i + 1 < len(sys.argv):
            candidates_path = sys.argv[i + 1]
        elif sys.argv[i] == '--out' and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
        elif sys.argv[i] == '--format' and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1]
    
    if not candidates_path or not output_path:
        print("Error: Missing required arguments")
        sys.exit(1)
    
    jd_path = Path(__file__).parent / 'job_description.md'
    ranker = QIHCRRanker(str(jd_path))
    ranker.rank_candidates(candidates_path, output_path, format=output_format)

if __name__ == '__main__':
    main()

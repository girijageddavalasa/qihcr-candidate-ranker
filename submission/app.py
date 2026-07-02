import gradio as gr
import pandas as pd
import tempfile
import os
from pathlib import Path
from rank import QIHCRRanker

def rank_candidates(file, output_format):
    if file is None:
        return None, None, "Please upload a candidates file"
    
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl')
    with open(temp_input.name, 'wb') as f:
        f.write(file)
    temp_input.close()
    
    # Set output extension based on format
    suffix = '.xlsx' if output_format == 'xlsx' else '.csv'
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_output.close()
    
    jd_path = Path(__file__).parent / 'job_description.md'
    ranker = QIHCRRanker(str(jd_path))
    ranker.rank_candidates(temp_input.name, temp_output.name, format=output_format)
    
    os.unlink(temp_input.name)
    
    # Read the output for leaderboard
    if output_format == 'xlsx':
        df = pd.read_excel(temp_output.name)
    else:
        df = pd.read_csv(temp_output.name)
    
    # Create leaderboard display
    leaderboard = df[['rank', 'candidate_id', 'score', 'reasoning']].head(10)
    
    return temp_output.name, leaderboard, f"Successfully ranked {len(df)} candidates ({output_format.upper()})"

def create_interface():
    with gr.Blocks(title="QIHCR Candidate Ranker") as demo:
        gr.Markdown("# QIHCR Candidate Ranker")
        gr.Markdown("## Quantum-Inspired Hypergraph Cascading Ranking System")
        
        with gr.Tab("Rank Candidates"):
            with gr.Row():
                file_input = gr.File(label="Upload candidates.jsonl or candidates.jsonl.gz", file_types=[".jsonl", ".jsonl.gz"])
            
            with gr.Row():
                format_dropdown = gr.Dropdown(
                    choices=["csv", "xlsx"],
                    value="csv",
                    label="Output Format",
                    info="CSV for official submission, XLSX for convenience"
                )
            
            with gr.Row():
                rank_btn = gr.Button("Rank Candidates", variant="primary")
            
            with gr.Row():
                download_btn = gr.DownloadButton(label="Download submission.csv", visible=False)
            
            with gr.Row():
                leaderboard_output = gr.Dataframe(label="Top 10 Candidates Leaderboard", visible=False)
            
            status_output = gr.Textbox(label="Status", interactive=False)
        
        with gr.Tab("About"):
            gr.Markdown("""
            ### Methodology
            
            This system uses a novel multi-layered ranking algorithm combining:
            
            1. **Quantum-Inspired Skill Interference (20%)** - Models skill combinations as quantum interference patterns
            2. **Hypergraph Skill Synergy (18%)** - Captures multi-way skill relationships
            3. **Cascading Behavioral Signal Integration (22%)** - Processes 14 behavioral signals in natural cascade
            4. **Temporal Signal Analysis (12%)** - Analyzes temporal and verification signals
            5. **Logistics Signal Analysis (12%)** - Evaluates logistics-related signals
            6. **Spherical Embedding Scoring (12% + 4%)** - Projects features to hypersphere for angular similarity
            
            ### All 23 Redrob Behavioral Signals Used:
            - profile_completeness_score, signup_date, last_active_date, open_to_work_flag
            - profile_views_received_30d, applications_submitted_30d, recruiter_response_rate
            - avg_response_time_hours, skill_assessment_scores, connection_count
            - endorsements_received, notice_period_days, expected_salary_range_inr_lpa
            - preferred_work_mode, willing_to_relocate, github_activity_score
            - search_appearance_30d, saved_by_recruiters_30d, interview_completion_rate
            - offer_acceptance_rate, verified_email, verified_phone, linkedin_connected
            """)
        
        rank_btn.click(
            fn=rank_candidates,
            inputs=[file_input, format_dropdown],
            outputs=[download_btn, leaderboard_output, status_output]
        ).then(
            lambda fmt: gr.DownloadButton(visible=True, label=f"Download submission.{fmt}"),
            inputs=[format_dropdown],
            outputs=[download_btn]
        ).then(
            lambda: gr.Dataframe(visible=True),
            outputs=[leaderboard_output]
        )
    
    return demo

if __name__ == '__main__':
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)

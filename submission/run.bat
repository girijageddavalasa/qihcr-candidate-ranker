@echo off
cd %~dp0
python rank.py --candidates ..\candidates.jsonl --out submission.csv
pause

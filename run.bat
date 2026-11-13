@echo off
echo ============================================================
echo Starting SkillSync - Your AI-Powered Career Roadmap
echo ============================================================

REM Find Python executable
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python -m streamlit run app.py
) else (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" -m streamlit run app.py
)
pause

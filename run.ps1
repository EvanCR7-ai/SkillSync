Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Starting SkillSync - Your AI-Powered Career Roadmap" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

$pythonPath = "C:\Users\ASUS\AppData\Local\Programs\Python\Python314\python.exe"
if (Test-Path $pythonPath) {
    & $pythonPath -m streamlit run app.py
} else {
    python -m streamlit run app.py
}

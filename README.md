# 🚀 SkillSync | CareerPath AI – Your Personal AI Career Mentor

> **Your Skills Today. Your Dream Career Tomorrow.**  
> An intelligent, responsive, AI-powered Streamlit SaaS platform designed to compare your current technical skill set against live tech industry benchmarks, identifying exact competency gaps, generating an 8-week personalized learning roadmap, and architecting 3 recruiter-ready GitHub portfolio projects.

---

## 🌟 Overview & Key Capabilities

**SkillSync** acts as your personal AI Career Mentor and Principal Hiring Manager. It replaces guesswork with mathematically consistent skill-gap assessments and hyper-personalized learning plans.

- 🔍 **Dynamic Skill-Gap Analysis:** Live comparison between candidate competencies and target role demands, categorizing skills into **Matched (Green)**, **Partial (Amber)**, and **Missing (Red)** with actionable recommendations, curated learning resources, and practical labs.
- 📐 **Mathematical Career Readiness Score:** A deterministic index computed directly from your competency breakdown—never random or fabricated.
- 🗺️ **Personalized 8-Week Learning Roadmap:** Week-by-week curriculum tailored to your exact weekly study hours (3–5, 5–10, 10–15, 15–20, 20+ hrs/week) and experience level (Beginner, Intermediate, Advanced). Accelerates past skills you already have, focuses on prerequisites, and culminates in a Week 8 Capstone Project.
- 💼 **3 GitHub Portfolio Projects:** Exactly three portfolio-defining projects (Beginner, Intermediate, and Advanced) with problem statements, architectural blueprints, tech stacks, and repository deliverables.
- 📄 **Full Export Suite:** One-click instant **PDF Career Report** download and **CSV Skill Analysis** export.
- ⚡ **Dynamic AI Engine & Resilience:** Integrated with **Google Gemini API** (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) via secure REST/SDK integration with an automatic heuristic mentor fallback when running offline or without an API key.

---

## 🛠️ Technology Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) (v1.35+)
- **AI / LLM Engine:** [Google Gemini API](https://aistudio.google.com/) via direct HTTPS REST & Google GenAI SDK
- **Data Visualizations:** [Plotly](https://plotly.com/) (Radial Gauges, Status Donut Charts, Priority Stacked Bars)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **PDF Document Engine:** [ReportLab](https://www.reportlab.com/) + Pure-Python PDF stream generator fallback
- **Styling & Design System:** Custom CSS3 with Dark Navy/Deep Purple theme, electric blue & violet gradients, glassmorphism cards, and responsive layouts.

---

## 📂 Project Structure

```text
careerpath-ai/
├── app.py                  # Main Streamlit SaaS application and reactive UI
├── ai_engine.py            # Gemini API integration, JSON schema validation & fallback mentor engine
├── roadmap_generator.py    # 8-week curriculum processor, timeline metrics & milestone logic
├── utils.py                # Input validation, CSV generator, PDF report builder & Plotly charts
├── styles.css              # Custom SaaS styling: dark navy, purple & electric blue gradients
├── requirements.txt        # Pinned Python package dependencies
├── .env.example            # Environment template for Gemini API key
├── .gitignore              # Git ignore rules for virtualenvs, keys, and cache
└── README.md               # Comprehensive documentation and setup guide
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your machine.
- An internet connection to install packages and query Google Gemini.

### 2. Navigate to Project Directory
Open your terminal (PowerShell, Command Prompt, or Bash) and navigate to the project directory:

```powershell
cd "C:\Users\ASUS\.gemini\antigravity\scratch\careerpath-ai"
```

### 3. (Recommended) Create and Activate a Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Activate on macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies
Run the installation command in your terminal:

```powershell
pip install -r requirements.txt
```

---

## 🔑 Google Gemini API Key Setup

SkillSync supports both `.env` configuration and interactive sidebar key entry.

### Method A: `.env` File (Local Development)
1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` in your text editor and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   GEMINI_MODEL=gemini-2.5-flash
   ```
   *You can get a free key in 30 seconds at [Google AI Studio](https://aistudio.google.com/app/apikey).*

### Method B: Interactive Sidebar Key Input
- You can also launch the application directly without a `.env` file!
- Simply expand **"🔑 Configure Gemini API Key"** in the sidebar, paste your key, and press Enter. The key remains safely in session memory.
- If no key is configured, SkillSync activates its built-in **Mentor Reasoning Engine**, allowing complete evaluation without blocking!

---

## 💻 Running the Application

Launch the Streamlit dashboard using:

```powershell
streamlit run app.py
```

The application will open automatically in your browser at:
```text
Local URL: http://localhost:8501
Network URL: http://<your-ip>:8501
```

---

## 🎯 How to Use SkillSync

1. **Review the Homepage & Feature Cards**: Explore the hero overview and click **"Create My Career Roadmap"**.
2. **Select Target Career Role**: Choose from 12 industry benchmarks (Data Scientist, AI/ML Engineer, Full Stack Developer, DevOps, Cloud Engineer, etc.) or choose **"Other (Custom Role)"** to enter any niche title.
3. **Select Your Current Skills**: Pick from popular chips or use **"Add Custom Skill"** to include any library, language, or tool.
4. **Define Time Commitment & Experience**: Specify your weekly study hours (`3–5`, `5–10`, `10–15`, `15–20`, or `20+` hrs/week) and current experience level (`Beginner`, `Intermediate`, `Advanced`).
5. **Generate Analysis**: Click **"🚀 Create My Career Roadmap"**.
6. **Inspect the Dashboard**:
   - **Top Metrics**: View your Mathematical Readiness Index, Matched, Partial, and Missing counts, and estimated study hours.
   - **Tab 1: Skill Gap Analysis**: Filter competencies, review learning resources & practice labs, and download the full analysis as **CSV**.
   - **Tab 2: 8-Week Roadmap**: Explore weekly milestones, detailed objectives, and the Week 8 Capstone Project. Click **"Download Full Career PDF Report"** or **"Regenerate Roadmap Plan"**.
   - **Tab 3: 3 Portfolio Projects**: Review Beginner, Intermediate, and Advanced project briefs with architecture diagrams, problems solved, and repository deliverable blueprints.

---

## 📸 UI Previews & Design Highlights

- **Hero Banner:** Radiant electric blue & violet gradient typography on deep obsidian/navy backdrop (`#0b0f19`).
- **Glassmorphism Panels:** Rounded cards (`border-radius: 18px`), translucent backgrounds (`backdrop-filter: blur(12px)`), and subtle ambient glow shadows.
- **Competency Badges:** High-contrast, accessibility-tested color badges:
  - 🟢 **Matched:** `#10b981` (Solid background + pill border)
  - 🟡 **Partial:** `#f59e0b` (Amber contrast)
  - 🔴 **Missing:** `#ef4444` (Crimson indicator)
- **Interactive Gauges & Donut Charts:** Real-time visual metrics powered by Plotly.

---

## 🔮 Future Enhancements

- [ ] **Resume / LinkedIn PDF Parser:** Upload your existing resume or LinkedIn PDF to extract current skills automatically.
- [ ] **Interview Simulator:** AI-driven mock technical interviews based specifically on the user's identified "Partial" and "Missing" skills.
- [ ] **Weekly Calendar Sync:** Export the 8-week study blocks directly to Google Calendar or iCal format (.ics).
- [ ] **Interactive Code Runner:** In-browser mini code challenges for Week 1–4 practice labs.

---

## 📄 License & Attribution
Developed with precision by the Google DeepMind Antigravity Pair Programming System. Open for educational and career acceleration use.

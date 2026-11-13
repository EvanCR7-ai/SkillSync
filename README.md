# ⚡ SkillSync – Your AI-Powered Career Roadmap

> **Discover Your Skills. Bridge the Gap. Build Your Future.**

SkillSync is a modern, responsive, AI-powered career accelerator that bridges the gap between students' current abilities and their dream tech careers. Powered by **Google Gemini AI**, SkillSync analyzes technical proficiencies, calculates an objective **Skill Readiness Score**, formulates a customized **8-Week Learning Roadmap**, and generates 3 GitHub-ready **Portfolio Project Blueprints** (Beginner, Intermediate, Advanced).

---

## 🌟 Key Features

- **🧠 AI Skill Gap Analysis:**
  - Evaluates current skills against industry requirements for high-demand tech roles.
  - Generates a visual status breakdown: *Already Have* (Green), *Partially Skilled* (Amber), *Need to Learn* (Red).
  - Assigns priority ratings (*High*, *Medium*, *Low*) and actionable recommendations for every skill.

- **🎯 Mathematical Skill Readiness Score:**
  - Dynamic Plotly circular gauge chart and skills distribution donut.
  - Calculates readiness percentage objectively based on structured competency analysis.

- **🗺️ Personalized 8-Week Roadmap:**
  - Tailored to the student's exact weekly study hours (3-5h to 20+h) and experience level.
  - Automatically skips or accelerates topics the student already knows.
  - Features weekly learning objectives, recommended resources (Documentation, Courses, Books), practical exercises, and expected outcomes.
  - Concludes with a **Week 8 Final Capstone Project**.
  - One-click **Regenerate Roadmap** with custom user instructions.

- **🚀 Portfolio Project Blueprints:**
  - Recommends 3 graduated, non-trivial projects (Beginner, Intermediate, Advanced).
  - Includes problem solved, tech stack tags, skills demonstrated, time estimates, and deliverables.
  - One-click **Regenerate Alternative Projects** by industry domain (FinTech, Healthcare, Web3, etc.).

- **📥 Professional Exports:**
  - **PDF Export:** Generates an executive, publication-grade career report using ReportLab.
  - **CSV Export:** Downloads the structured skill gap matrix for spreadsheet tracking.

- **🎨 Premium Modern SaaS UI/UX:**
  - Cyberpunk-inspired dark navy & deep purple glassmorphism design.
  - Electric blue and vivid violet gradient accents with smooth micro-interactions.
  - Fully responsive across desktop, tablet, and mobile browsers.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend & UI** | [Streamlit](https://streamlit.io/) with Custom CSS Glassmorphism |
| **AI / LLM Engine** | [Google Gemini API](https://aistudio.google.com/) via `google-genai` |
| **Data & Visualizations** | [Pandas](https://pandas.pydata.org/) & [Plotly](https://plotly.com/python/) |
| **PDF Generation** | [ReportLab](https://www.reportlab.com/) |
| **Configuration** | [python-dotenv](https://github.com/theskumar/python-dotenv) |
| **Runtime** | Python 3.10+ |

---

## 📁 Project Architecture

```
skillsync/
├── app.py                  # Main Streamlit web application & UI controllers
├── ai_engine.py            # Gemini API integration, prompt orchestration & parsing
├── roadmap_generator.py    # Visual components (Plotly gauges, tables, timeline cards)
├── utils.py                # PDF report generator, CSV exporter & input validator
├── styles.css              # Custom SaaS dark navy & violet glassmorphism stylesheet
├── requirements.txt        # Production dependencies
├── .env.example            # Environment template for Gemini API key
├── .gitignore              # Ignored files, cache, and secrets
└── README.md               # Complete project documentation & setup guide
```

---

## 🚀 Quickstart & Installation

### 1. Clone or Navigate to the Repository
```bash
git clone https://github.com/your-username/skillsync.git
cd skillsync
```

### 2. Create and Activate a Virtual Environment
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key
SkillSync uses Google Gemini for real-time career intelligence. Get your free API key at **[Google AI Studio](https://aistudio.google.com/)**.

Create a `.env` file in the project root:
```bash
cp .env.example .env
```
Open `.env` and paste your key:
```ini
GEMINI_API_KEY=AIzaSyYourActualGeminiApiKeyHere
```
*(Alternatively, you can enter your API key directly in the application's sidebar interface).*

---

## 🖥️ Running the Application

Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```

The application will automatically open in your default browser at:
```
http://localhost:8501
```

---

## 📸 Application Walkthrough & Screenshots

### 1. Hero & Value Proposition
- Welcome banner, platform philosophy, and interactive 4-step workflow overview.

### 2. Student Information Form
- Multiselect input for existing technologies with custom skill tag support.
- Dropdown for 12+ industry roles (or custom role input).
- Study hours slider/select and experience level options.

### 3. Skill Gap Analysis & Readiness Dashboard
- Plotly circular gauge indicator showing current match percentage.
- Status breakdown donut chart (Matched, Partially Skilled, Missing).
- Detailed comparison table with priority flags and mentor recommendations.

### 4. Interactive 8-Week Roadmap
- Weekly expandable milestones with learning objectives, coding tasks, resources, and milestone deliverables.
- Interactive capstone milestone in Week 8.

### 5. GitHub-Ready Portfolio Projects
- Three cards (Beginner, Intermediate, Advanced) displaying tech stack pills, problem statement, and expected final output.

### 6. One-Click PDF & CSV Downloads
- Executive PDF report with student metrics, table breakdown, and curriculum summary.

---

## 🔮 Future Enhancements

- [ ] **Resume / LinkedIn Parser:** Automatically extract existing skills from an uploaded PDF resume.
- [ ] **GitHub Profile Auditor:** Scan user's public GitHub repos to verify technical competencies with AI code review.
- [ ] **Interactive Mock Interview Simulator:** Audio/chat-based technical interview for the target role using Gemini Multimodal Live API.
- [ ] **Job Board Matcher:** Real-time job posting matching based on the student's evolving skill set.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).

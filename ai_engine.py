"""
SkillSync | CareerPath AI - AI Engine
Handles Gemini API integration, prompt generation, structured JSON validation,
and career mentor reasoning.
"""

import os
import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

# Check for official Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    HAS_GENAI_SDK = True
except ImportError:
    HAS_GENAI_SDK = False

# Load local environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Graceful fallback .env loader when python-dotenv is not installed
    def load_dotenv():
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            except Exception:
                pass
    load_dotenv()

# Pre-defined benchmark knowledge base for dynamic fallbacks and prompt contextualization
ROLE_SKILL_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "Data Scientist": {
        "required_skills": [
            {"name": "Python", "category": "Core Programming", "priority": "High"},
            {"name": "SQL & Relational Databases", "category": "Data Management", "priority": "High"},
            {"name": "Pandas & Data Wrangling", "category": "Data Processing", "priority": "High"},
            {"name": "Exploratory Data Analysis (EDA)", "category": "Analysis", "priority": "Medium"},
            {"name": "Scikit-Learn & Classical ML", "category": "Machine Learning", "priority": "High"},
            {"name": "Deep Learning (PyTorch/TensorFlow)", "category": "Advanced AI", "priority": "Medium"},
            {"name": "Feature Engineering & Preprocessing", "category": "Machine Learning", "priority": "High"},
            {"name": "Data Visualization (Plotly/Seaborn)", "category": "Visualization", "priority": "Medium"},
            {"name": "Model Deployment (FastAPI/Docker)", "category": "MLOps", "priority": "Medium"},
            {"name": "Statistics & Hypothesis Testing", "category": "Mathematics", "priority": "High"},
        ],
        "default_focus": "Statistical modeling, predictive algorithms, and end-to-end data pipelines."
    },
    "Data Analyst": {
        "required_skills": [
            {"name": "SQL & Complex Queries", "category": "Data Querying", "priority": "High"},
            {"name": "Excel & Advanced Analytics", "category": "Spreadsheets", "priority": "High"},
            {"name": "Power BI / Tableau", "category": "BI Dashboards", "priority": "High"},
            {"name": "Python for Data Analysis", "category": "Scripting", "priority": "Medium"},
            {"name": "Pandas & NumPy", "category": "Data Wrangling", "priority": "Medium"},
            {"name": "Data Cleaning & Quality Auditing", "category": "Data Hygiene", "priority": "High"},
            {"name": "Business Intelligence & KPIs", "category": "Business Context", "priority": "High"},
            {"name": "Statistical Analysis & A/B Testing", "category": "Analytics", "priority": "Medium"},
            {"name": "Data Storytelling & Reporting", "category": "Communication", "priority": "High"}
        ],
        "default_focus": "Translating raw operational data into actionable business dashboards and decisions."
    },
    "AI/ML Engineer": {
        "required_skills": [
            {"name": "Python & Object-Oriented Design", "category": "Core Software", "priority": "High"},
            {"name": "PyTorch or TensorFlow", "category": "Deep Learning", "priority": "High"},
            {"name": "MLOps & CI/CD Pipelines (MLflow)", "category": "MLOps", "priority": "High"},
            {"name": "Model Optimization & Quantization", "category": "Performance", "priority": "Medium"},
            {"name": "Vector Databases & Embeddings", "category": "LLMs & Retrieval", "priority": "High"},
            {"name": "Large Language Models & LangChain", "category": "Generative AI", "priority": "High"},
            {"name": "REST APIs & FastAPI Serving", "category": "Deployment", "priority": "High"},
            {"name": "Docker & Containerization", "category": "Infrastructure", "priority": "High"},
            {"name": "Git & Collaborative Development", "category": "Tools", "priority": "Medium"},
            {"name": "Cloud AI Services (GCP/AWS)", "category": "Cloud", "priority": "Medium"}
        ],
        "default_focus": "Productionizing machine learning systems, deploying LLM pipelines, and building scalable inference engines."
    },
    "Frontend Developer": {
        "required_skills": [
            {"name": "HTML5, CSS3 & Responsive Web Design", "category": "Web Core", "priority": "High"},
            {"name": "Modern JavaScript (ES6+)", "category": "Language Core", "priority": "High"},
            {"name": "TypeScript", "category": "Type Safety", "priority": "High"},
            {"name": "React.js / Next.js", "category": "Frontend Frameworks", "priority": "High"},
            {"name": "Tailwind CSS & Component Libraries", "category": "Styling", "priority": "Medium"},
            {"name": "State Management (Zustand/Redux)", "category": "State Architecture", "priority": "High"},
            {"name": "REST & GraphQL API Integration", "category": "Networking", "priority": "High"},
            {"name": "Web Performance & Core Web Vitals", "category": "Optimization", "priority": "Medium"},
            {"name": "Testing (Jest / Playwright)", "category": "Quality Assurance", "priority": "Medium"},
            {"name": "Git & Version Control", "category": "Tools", "priority": "Medium"}
        ],
        "default_focus": "Crafting accessible, hyper-performant, and visually stunning interactive web interfaces."
    },
    "Backend Developer": {
        "required_skills": [
            {"name": "Python / Node.js / Go / Java", "category": "Core Language", "priority": "High"},
            {"name": "RESTful & GraphQL API Design", "category": "API Architecture", "priority": "High"},
            {"name": "Relational Databases (PostgreSQL)", "category": "Data Storage", "priority": "High"},
            {"name": "NoSQL Databases (MongoDB/Redis)", "category": "Caching & NoSQL", "priority": "Medium"},
            {"name": "Authentication & Security (OAuth/JWT)", "category": "Security", "priority": "High"},
            {"name": "Microservices & Distributed Systems", "category": "Architecture", "priority": "Medium"},
            {"name": "Docker & Containerization", "category": "DevOps", "priority": "High"},
            {"name": "Unit & Integration Testing (PyTest/Jest)", "category": "Testing", "priority": "Medium"},
            {"name": "Message Queues (RabbitMQ/Kafka)", "category": "Async Architecture", "priority": "Medium"},
            {"name": "CI/CD & Cloud Deployment", "category": "Infrastructure", "priority": "Medium"}
        ],
        "default_focus": "Building robust server architectures, highly secure APIs, and fault-tolerant distributed data backends."
    },
    "Full Stack Developer": {
        "required_skills": [
            {"name": "JavaScript / TypeScript", "category": "Fullstack Language", "priority": "High"},
            {"name": "React / Next.js / Vue", "category": "Frontend", "priority": "High"},
            {"name": "Node.js / Express or FastAPI / Django", "category": "Backend", "priority": "High"},
            {"name": "PostgreSQL & Database Modeling", "category": "Databases", "priority": "High"},
            {"name": "Authentication, Session & State", "category": "Security & Architecture", "priority": "High"},
            {"name": "REST & WebSockets", "category": "Protocols", "priority": "Medium"},
            {"name": "Tailwind CSS & UI Frameworks", "category": "Frontend Styling", "priority": "Medium"},
            {"name": "Docker & Cloud Deployments (AWS/Vercel)", "category": "DevOps", "priority": "High"},
            {"name": "Git, GitHub Actions & CI/CD", "category": "Workflows", "priority": "High"},
            {"name": "End-to-End Testing & Debugging", "category": "Testing", "priority": "Medium"}
        ],
        "default_focus": "Connecting frontend user experiences seamlessly with scalable backend architectures and databases."
    },
    "Cybersecurity Analyst": {
        "required_skills": [
            {"name": "Networking Protocols (TCP/IP, DNS, SSL)", "category": "Foundations", "priority": "High"},
            {"name": "Operating Systems (Linux & Windows Internals)", "category": "OS Security", "priority": "High"},
            {"name": "Security Information & Event Management (SIEM)", "category": "Monitoring", "priority": "High"},
            {"name": "Vulnerability Assessment & Penetration Basics", "category": "Offensive/Defensive", "priority": "High"},
            {"name": "Threat Intelligence & Incident Response", "category": "SecOps", "priority": "High"},
            {"name": "Python / Bash Scripting for Automation", "category": "Scripting", "priority": "Medium"},
            {"name": "Network Security & Firewalls / IDS / IPS", "category": "Infrastructure", "priority": "High"},
            {"name": "Identity & Access Management (IAM)", "category": "Access Control", "priority": "Medium"},
            {"name": "Compliance Frameworks (NIST, ISO 27001)", "category": "Governance", "priority": "Medium"}
        ],
        "default_focus": "Safeguarding organizational infrastructure, detecting active security threats, and hardening defenses."
    },
    "Cloud Engineer": {
        "required_skills": [
            {"name": "Cloud Platforms (AWS, Azure, or GCP)", "category": "Cloud Core", "priority": "High"},
            {"name": "Infrastructure as Code (Terraform)", "category": "Automation", "priority": "High"},
            {"name": "Linux System Administration", "category": "Systems", "priority": "High"},
            {"name": "Docker & Container Architecture", "category": "Containers", "priority": "High"},
            {"name": "Kubernetes Cluster Management", "category": "Orchestration", "priority": "High"},
            {"name": "Cloud Networking (VPC, Subnets, Gateways)", "category": "Networking", "priority": "High"},
            {"name": "CI/CD Pipelines & Automation Tools", "category": "DevOps", "priority": "High"},
            {"name": "Cloud Security, IAM & Compliance", "category": "Security", "priority": "High"},
            {"name": "Monitoring & Observability (Prometheus/Grafana)", "category": "Observability", "priority": "Medium"}
        ],
        "default_focus": "Designing resilient, scalable multi-region cloud infrastructures with automated deployment pipelines."
    },
    "DevOps Engineer": {
        "required_skills": [
            {"name": "Linux Administration & Shell Scripting", "category": "Core Systems", "priority": "High"},
            {"name": "CI/CD Engineering (GitHub Actions / GitLab CI)", "category": "Automation", "priority": "High"},
            {"name": "Docker & Container Lifecycle", "category": "Containers", "priority": "High"},
            {"name": "Kubernetes Deployment & Ingress", "category": "Orchestration", "priority": "High"},
            {"name": "Terraform / Ansible Configuration", "category": "IaC", "priority": "High"},
            {"name": "Cloud Infrastructure (AWS/GCP)", "category": "Cloud", "priority": "High"},
            {"name": "Observability, Logging & Alerting", "category": "Monitoring", "priority": "Medium"},
            {"name": "Security in DevOps (DevSecOps)", "category": "Security", "priority": "Medium"},
            {"name": "Git Flow & Branching Strategies", "category": "Workflows", "priority": "Medium"}
        ],
        "default_focus": "Bridging engineering and operations through automated deployment pipelines and zero-downtime reliability."
    },
    "UI/UX Designer": {
        "required_skills": [
            {"name": "Figma & Advanced Prototyping", "category": "Design Tools", "priority": "High"},
            {"name": "User Research, Personas & User Journeys", "category": "Research", "priority": "High"},
            {"name": "Information Architecture & Wireframing", "category": "UX Strategy", "priority": "High"},
            {"name": "Design Systems & Token Architecture", "category": "UI Systems", "priority": "High"},
            {"name": "Usability Testing & Heuristic Evaluation", "category": "Validation", "priority": "High"},
            {"name": "Interaction Design & Micro-animations", "category": "Visual UX", "priority": "Medium"},
            {"name": "Accessibility Standards (WCAG 2.1)", "category": "Compliance", "priority": "High"},
            {"name": "Frontend Basics (HTML/CSS Understanding)", "category": "Developer Handoff", "priority": "Medium"},
            {"name": "Responsive & Mobile-First Design", "category": "UI Design", "priority": "High"}
        ],
        "default_focus": "Conducting deep user discovery, structuring human-centered flows, and architecting scalable design systems."
    },
    "Python Developer": {
        "required_skills": [
            {"name": "Advanced Python (OOP, AsyncIO, Generators)", "category": "Core Language", "priority": "High"},
            {"name": "FastAPI / Django / Flask Web Frameworks", "category": "Web Frameworks", "priority": "High"},
            {"name": "SQL & ORM Tools (SQLAlchemy / Django ORM)", "category": "Databases", "priority": "High"},
            {"name": "REST API Development & Serialization", "category": "APIs", "priority": "High"},
            {"name": "Unit Testing & Mocking (PyTest)", "category": "Testing", "priority": "High"},
            {"name": "Data Manipulation (Pandas / NumPy)", "category": "Data", "priority": "Medium"},
            {"name": "Docker & Containerized Microservices", "category": "DevOps", "priority": "Medium"},
            {"name": "Concurrency, Multithreading & Celery", "category": "Async Processing", "priority": "Medium"},
            {"name": "Git & Collaborative Code Review", "category": "Tools", "priority": "Medium"}
        ],
        "default_focus": "Writing clean, maintainable, high-throughput Python backends and automation systems."
    },
    "Software Engineer": {
        "required_skills": [
            {"name": "Data Structures & Algorithms", "category": "Computer Science", "priority": "High"},
            {"name": "Object-Oriented & Functional Programming", "category": "Paradigms", "priority": "High"},
            {"name": "System Design & Distributed Architecture", "category": "System Design", "priority": "High"},
            {"name": "Relational & Distributed Databases", "category": "Storage", "priority": "High"},
            {"name": "API Design & Microservices", "category": "Architecture", "priority": "High"},
            {"name": "Version Control (Git) & CI/CD", "category": "Engineering Practices", "priority": "High"},
            {"name": "Automated Testing, TDD & Debugging", "category": "Quality Assurance", "priority": "High"},
            {"name": "Cloud Platforms & Docker", "category": "Infrastructure", "priority": "Medium"},
            {"name": "Performance Profiling & Memory Optimization", "category": "Optimization", "priority": "Medium"}
        ],
        "default_focus": "Architecting resilient, maintainable, and scalable software systems with robust algorithmic rigor."
    }
}


def get_gemini_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """Retrieves the Gemini API key securely from explicit input, environment, or .env."""
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()
    return os.environ.get("GEMINI_API_KEY", "").strip() or None


def mask_api_key(key: Optional[str]) -> str:
    """Returns a masked version of the API key for safe UI display."""
    if not key:
        return "Not Configured"
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


def calculate_mathematical_readiness_score(skills_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates a consistent, strictly mathematical readiness score from the structured skill list.
    Formula: ((matched * 1.0 + partial * 0.5) / total) * 100
    Guarantees no arbitrary or random numbers.
    """
    total = len(skills_analysis)
    if total == 0:
        return {
            "score": 0.0,
            "matched_count": 0,
            "partial_count": 0,
            "missing_count": 0,
            "total_skills": 0,
            "verdict": "No skills evaluated",
            "tier": "Early Stage"
        }

    matched = sum(1 for s in skills_analysis if s.get("status", "").lower() == "matched")
    partial = sum(1 for s in skills_analysis if s.get("status", "").lower() == "partial")
    missing = sum(1 for s in skills_analysis if s.get("status", "").lower() == "missing")

    weighted_score = (matched * 1.0) + (partial * 0.5)
    score_percentage = round((weighted_score / total) * 100, 1)

    if score_percentage >= 80:
        verdict = "Interview Ready & Highly Competitive"
        tier = "Ready for Senior/Mid Placement"
    elif score_percentage >= 60:
        verdict = "Strong Core – Fast-Track 8-Week Polish"
        tier = "Intermediate Professional"
    elif score_percentage >= 35:
        verdict = "Promising Foundation – Targeted Upskilling Needed"
        tier = "Emerging Talent"
    else:
        verdict = "Early Stage – Structured Guided Mentorship Recommended"
        tier = "Foundational Learner"

    return {
        "score": score_percentage,
        "matched_count": matched,
        "partial_count": partial,
        "missing_count": missing,
        "total_skills": total,
        "verdict": verdict,
        "tier": tier
    }


def _call_gemini_rest_api(api_key: str, prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Calls Google Gemini REST API directly using standard urllib.
    Eliminates external SDK wheel compilation or dependency issues.
    """
    # Prefer newer models with fallback to 1.5-flash
    models_to_try = [model, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    # De-duplicate while preserving order
    seen = set()
    models_to_try = [m for m in models_to_try if not (m in seen or seen.add(m))]

    last_error = None
    for target_model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.25,
                "topP": 0.95,
                "maxOutputTokens": 4096,
                "responseMimeType": "application/json"
            }
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=40) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                raise ValueError("Empty or malformed candidate response from Gemini API.")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            last_error = f"HTTP {e.code}: {e.reason} - {error_body}"
            # If rate limited (429) or model not found (404), try next model
            continue
        except Exception as e:
            last_error = str(e)
            continue

    raise RuntimeError(f"Gemini API request failed across tested models. Detail: {last_error}")


def _call_gemini_sdk(api_key: str, prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Calls Google Gemini using the official google-genai SDK when available.
    """
    if not HAS_GENAI_SDK:
        raise ImportError("google-genai SDK is not installed.")

    client = genai.Client(api_key=api_key)
    models_to_try = [model, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    seen = set()
    models_to_try = [m for m in models_to_try if not (m in seen or seen.add(m))]

    last_error = None
    for target_model in models_to_try:
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.25,
                max_output_tokens=4096
            )
            response = client.models.generate_content(
                model=target_model,
                contents=prompt,
                config=config
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f"google-genai SDK failed across tested models. Detail: {last_error}")


def _build_ai_prompt(current_skills: List[str], target_role: str, weekly_hours: str, experience_level: str) -> str:
    """Constructs the prompt for Gemini acting as a Technical Career Mentor."""
    skills_formatted = ", ".join(current_skills) if current_skills else "None specified"
    
    return f"""
You are SkillSync AI, a world-class Technical Career Mentor, Principal Hiring Manager, and Staff Engineer.

Analyze this candidate profile with extreme precision:
- Target Role: {target_role}
- Candidate Current Skills: {skills_formatted}
- Weekly Study Commitment: {weekly_hours}
- Candidate Experience Level: {experience_level}

YOUR TASKS:
1. Identify 8 to 12 essential technical competencies required for modern job openings in the target role "{target_role}".
2. Compare each required competency against the candidate's current skills ({skills_formatted}):
   - Mark as "Matched" if the candidate already possesses this skill or a direct equivalent.
   - Mark as "Partial" if the candidate knows a foundational or adjacent aspect but needs deeper mastery for this role.
   - Mark as "Missing" if the candidate lacks this required competency.
   - Assign Priority: "High", "Medium", or "Low".
   - Provide concrete, actionable Recommendation, Recommended Resource (e.g. documentation, book, course), and a specific Practice Exercise.
3. Generate a personalized 8-Week Learning Roadmap tailored to their weekly commitment ({weekly_hours}) and experience ({experience_level}):
   - Week 1 through 8.
   - Skip or shorten weeks on skills they have already "Matched".
   - Dedicate early weeks to high-priority missing/partial prerequisites.
   - Week 8 MUST culminate in a comprehensive practical Capstone Project demonstrating industry readiness.
   - Each week must include: week_number, topic, focus_skills (array), detailed_objectives (array of 3 items), recommended_resources (array of 2 items), practical_exercises (array of 2 items), expected_outcome, estimated_hours.
4. Generate EXACTLY 3 realistic GitHub-Portfolio Mini Projects:
   - 1 Beginner level
   - 1 Intermediate level
   - 1 Advanced level
   - Each project must be practical, portfolio-worthy, and solve a realistic problem. Include title, difficulty, description, problem_solved, technologies (array), skills_demonstrated (array), estimated_time, expected_output.
5. Provide an inspiring, empowering, and authentic motivational mentor message.

OUTPUT FORMAT REQUIREMENTS:
You MUST respond with valid, parseable JSON only. Do not wrap in markdown quotes if possible, or wrap cleanly in ```json ... ```.

Schema:
{{
  "readiness_summary": {{
    "candidate_name": "Student",
    "target_role": "{target_role}",
    "experience_level": "{experience_level}",
    "weekly_hours": "{weekly_hours}",
    "readiness_verdict": "string",
    "motivational_message": "string"
  }},
  "skills_analysis": [
    {{
      "skill_name": "string",
      "category": "string",
      "status": "Matched" | "Partial" | "Missing",
      "priority": "High" | "Medium" | "Low",
      "recommendation": "string",
      "recommended_resource": "string",
      "practice_exercise": "string"
    }}
  ],
  "roadmap": [
    {{
      "week_number": 1,
      "topic": "string",
      "focus_skills": ["string"],
      "detailed_objectives": ["string", "string", "string"],
      "recommended_resources": ["string", "string"],
      "practical_exercises": ["string", "string"],
      "expected_outcome": "string",
      "estimated_hours": "{weekly_hours}"
    }}
  ],
  "projects": [
    {{
      "difficulty": "Beginner",
      "title": "string",
      "description": "string",
      "problem_solved": "string",
      "technologies": ["string", "string"],
      "skills_demonstrated": ["string", "string"],
      "estimated_time": "string",
      "expected_output": "string"
    }},
    {{
      "difficulty": "Intermediate",
      "title": "string",
      "description": "string",
      "problem_solved": "string",
      "technologies": ["string", "string"],
      "skills_demonstrated": ["string", "string"],
      "estimated_time": "string",
      "expected_output": "string"
    }},
    {{
      "difficulty": "Advanced",
      "title": "string",
      "description": "string",
      "problem_solved": "string",
      "technologies": ["string", "string"],
      "skills_demonstrated": ["string", "string"],
      "estimated_time": "string",
      "expected_output": "string"
    }}
  ]
}}
"""


def _generate_dynamic_mentor_analysis(
    current_skills: List[str],
    target_role: str,
    weekly_hours: str,
    experience_level: str
) -> Dict[str, Any]:
    """
    Intelligent heuristic mentor engine.
    Used when Gemini API key is missing or offline, dynamically analyzing user inputs
    with role benchmarks to compute mathematical readiness and tailored roadmaps.
    """
    benchmark = ROLE_SKILL_BENCHMARKS.get(target_role)
    if not benchmark:
        # Fallback benchmark for custom roles
        benchmark = {
            "required_skills": [
                {"name": f"{target_role} Core Foundations", "category": "Foundations", "priority": "High"},
                {"name": "Domain Best Practices & Standards", "category": "Methodology", "priority": "High"},
                {"name": "Industry Standard Toolchain", "category": "Tooling", "priority": "High"},
                {"name": "Data Management & Storage", "category": "Data", "priority": "Medium"},
                {"name": "Automation & Workflow Scripting", "category": "Automation", "priority": "Medium"},
                {"name": "API & System Integration", "category": "Integration", "priority": "High"},
                {"name": "Testing, Quality Assurance & Security", "category": "Security & QA", "priority": "High"},
                {"name": "Deployment, Monitoring & Observability", "category": "DevOps", "priority": "Medium"},
            ],
            "default_focus": f"Mastery of {target_role} industry workflows, toolchains, and project delivery."
        }

    user_skills_clean = [s.strip().lower() for s in current_skills if s.strip()]

    # Skill matching logic
    skills_analysis = []
    for item in benchmark["required_skills"]:
        s_name = item["name"]
        s_lower = s_name.lower()

        # Check for direct or partial match
        matched = any(us in s_lower or s_lower in us for us in user_skills_clean)
        partial = False
        if not matched:
            # Check for related keywords
            keywords = [w for w in re.split(r"[\s/&,]+", s_lower) if len(w) > 3]
            partial = any(any(k in us or us in k for k in keywords) for us in user_skills_clean)

        if matched:
            status = "Matched"
            rec = f"You possess solid grounding in {s_name}. Focus on edge-case mastery and enterprise-scale implementations."
            res = f"Advanced {s_name} Engineering Guides & Official Docs"
            ex = f"Refactor an existing project or build a performance benchmark utilizing advanced {s_name} patterns."
        elif partial:
            status = "Partial"
            rec = f"You understand fundamentals related to {s_name}. Bridge the gap by mastering modern production conventions."
            res = f"Deep Dive {s_name} Interactive Tutorials & GitHub Best-Practice Repos"
            ex = f"Implement a standalone module focusing purely on {s_name} to solidify practical confidence."
        else:
            status = "Missing"
            rec = f"Critical requirement for {target_role}. Prioritize dedicated hands-on hours to build initial competency."
            res = f"Zero-to-Hero {s_name} Specialization & Interactive Labs"
            ex = f"Complete guided 5-part exercise building a functional prototype from scratch using {s_name}."

        skills_analysis.append({
            "skill_name": s_name,
            "category": item.get("category", "Core"),
            "status": status,
            "priority": item.get("priority", "Medium"),
            "recommendation": rec,
            "recommended_resource": res,
            "practice_exercise": ex
        })

    # Mathematical readiness calculation
    score_meta = calculate_mathematical_readiness_score(skills_analysis)

    # Dynamic 8-Week Roadmap tailored to missing/partial gaps
    gaps = [s for s in skills_analysis if s["status"] != "Matched"]
    if not gaps:
        gaps = skills_analysis

    roadmap = []
    for week_num in range(1, 9):
        if week_num == 8:
            topic = f"Capstone Project: Production-Ready {target_role} System"
            f_skills = [s["skill_name"] for s in skills_analysis[:3]]
            objs = [
                f"Synthesize all competencies into an end-to-end {target_role} showcase project",
                "Implement industry CI/CD, documentation, unit tests, and production logging",
                "Deploy live to cloud hosting and record a polished 3-minute video walkthrough"
            ]
            resources = [
                f"Full-Stack Production Blueprint for {target_role}",
                "GitHub Readme & Portfolio Presentation Mastery"
            ]
            exercises = [
                "Execute the 5-phase capstone deployment checklist",
                "Publish comprehensive open-source GitHub repository with automated tests"
            ]
            outcome = "A portfolio-defining flagship project live on GitHub and ready for recruiter demonstration."
        else:
            idx = (week_num - 1) % len(gaps)
            target_skill = gaps[idx]
            topic = f"Week {week_num}: Mastering {target_skill['skill_name']} & Architectural Integration"
            f_skills = [target_skill["skill_name"], target_skill["category"]]
            objs = [
                f"Deconstruct core syntax, patterns, and principles of {target_skill['skill_name']}",
                f"Solve common pitfalls and write maintainable, tested {target_skill['skill_name']} code",
                "Integrate with existing components and verify error resilience"
            ]
            resources = [
                target_skill["recommended_resource"],
                f"Real-World {target_skill['skill_name']} Case Studies"
            ]
            exercises = [
                target_skill["practice_exercise"],
                f"Build a mini-utility integrating {target_skill['skill_name']} with automated validation"
            ]
            outcome = f"Functional fluency in {target_skill['skill_name']} with verified code committed to version control."

        roadmap.append({
            "week_number": week_num,
            "topic": topic,
            "focus_skills": f_skills,
            "detailed_objectives": objs,
            "recommended_resources": resources,
            "practical_exercises": exercises,
            "expected_outcome": outcome,
            "estimated_hours": f"{weekly_hours} (Targeted practice)"
        })

    # Exactly 3 Portfolio Projects
    projects = [
        {
            "difficulty": "Beginner",
            "title": f"{target_role} Smart Metrics & Automation Tool",
            "description": f"A lightweight, focused tool solving data ingestion and reporting workflows for {target_role}.",
            "problem_solved": "Eliminates repetitive manual configurations and validates operational accuracy automatically.",
            "technologies": ["Python", "SQLite", "Streamlit", "PyTest", "Git"],
            "skills_demonstrated": ["Data Extraction", "Unit Testing", "Modular Architecture", "Clean Documentation"],
            "estimated_time": "15–20 hours",
            "expected_output": "Interactive dashboard app and CLI tool with 90%+ test coverage hosted on GitHub."
        },
        {
            "difficulty": "Intermediate",
            "title": f"Scalable {target_role} Analytics & Microservice API",
            "description": "Full-featured asynchronous backend service handling complex queries, caching, and rate limiting.",
            "problem_solved": "Provides resilient real-time processing and structured API responses under concurrent workloads.",
            "technologies": ["FastAPI / Node.js", "PostgreSQL", "Docker", "Redis", "JWT Auth"],
            "skills_demonstrated": ["REST API Architecture", "Database Optimization", "Containerization", "Security"],
            "estimated_time": "30–40 hours",
            "expected_output": "Dockerized microservice with Swagger documentation, automated CI/CD pipeline, and benchmark tests."
        },
        {
            "difficulty": "Advanced",
            "title": f"Enterprise AI-Driven {target_role} Intelligence Platform",
            "description": f"Production-grade distributed system leveraging Gemini AI inference, vector search, and cloud orchestration.",
            "problem_solved": "Transforms high-velocity unstructured data into actionable predictive insights with sub-second latency.",
            "technologies": ["Google Gemini API", "Vector DB", "Docker", "Kubernetes / Cloud Run", "Plotly / React"],
            "skills_demonstrated": ["LLM Orchestration", "Cloud Deployment", "Observability & Tracing", "Enterprise Architecture"],
            "estimated_time": "50–65 hours",
            "expected_output": "Live deployed web platform with cloud monitoring, load-balanced replicas, and automated schema migration."
        }
    ]

    motivational_messages = [
        f"You already hold {score_meta['matched_count']} critical skills for {target_role}! Every expert started with gaps—your 8-week path is designed to turn those exact gaps into your strongest competitive edge.",
        f"The transition into a top-tier {target_role} is built one commit at a time. With {weekly_hours} of deliberate practice, you'll build undeniable proof of your capabilities.",
        f"Consistency beats intensity. With a {score_meta['score']}% foundation in place, targeted focus on your high-priority items will prepare you for top hiring bars."
    ]

    return {
        "is_ai_generated": False,
        "engine_source": "CareerPath Mentor Heuristic Engine",
        "readiness_summary": {
            "candidate_name": "Student",
            "target_role": target_role,
            "experience_level": experience_level,
            "weekly_hours": weekly_hours,
            "overall_fit_percentage": score_meta["score"],
            "matched_count": score_meta["matched_count"],
            "partial_count": score_meta["partial_count"],
            "missing_count": score_meta["missing_count"],
            "total_skills": score_meta["total_skills"],
            "readiness_verdict": score_meta["verdict"],
            "tier": score_meta["tier"],
            "motivational_message": motivational_messages[0]
        },
        "skills_analysis": skills_analysis,
        "roadmap": roadmap,
        "projects": projects
    }


def clean_and_parse_json(raw_text: str) -> Optional[Dict[str, Any]]:
    """Sanitizes model output and extracts valid JSON."""
    if not raw_text:
        return None

    cleaned = raw_text.strip()
    # Remove markdown codeblocks if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except Exception:
        # Fallback: search for first { and last }
        match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return None


def generate_career_analysis(
    current_skills: List[str],
    target_role: str,
    weekly_hours: str,
    experience_level: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main entry point: Generates complete Skill Gap Analysis, 8-Week Roadmap, and 3 Projects.
    Queries Google Gemini API when API key is provided, with fallback to mentor heuristic.
    """
    active_key = get_gemini_api_key(api_key)

    if not active_key:
        result = _generate_dynamic_mentor_analysis(current_skills, target_role, weekly_hours, experience_level)
        result["api_status_note"] = "Generated with SkillSync Mentor Reasoning Engine (No Gemini API key supplied)."
        return result

    # Prepare prompt
    prompt = _build_ai_prompt(current_skills, target_role, weekly_hours, experience_level)

    try:
        raw_response = None
        # Try SDK first if available
        if HAS_GENAI_SDK:
            try:
                raw_response = _call_gemini_sdk(active_key, prompt)
            except Exception:
                raw_response = None

        # Fallback to direct REST API
        if not raw_response:
            raw_response = _call_gemini_rest_api(active_key, prompt)

        parsed = clean_and_parse_json(raw_response)

        if not parsed or "skills_analysis" not in parsed:
            raise ValueError("Model output did not match expected structured schema.")

        # Ensure mathematical consistency of readiness score
        skills_analysis = parsed.get("skills_analysis", [])
        calculated_meta = calculate_mathematical_readiness_score(skills_analysis)

        summary = parsed.get("readiness_summary", {})
        summary["overall_fit_percentage"] = calculated_meta["score"]
        summary["matched_count"] = calculated_meta["matched_count"]
        summary["partial_count"] = calculated_meta["partial_count"]
        summary["missing_count"] = calculated_meta["missing_count"]
        summary["total_skills"] = calculated_meta["total_skills"]
        summary["readiness_verdict"] = calculated_meta["verdict"]
        summary["tier"] = calculated_meta["tier"]
        summary["target_role"] = target_role
        summary["weekly_hours"] = weekly_hours
        summary["experience_level"] = experience_level

        parsed["readiness_summary"] = summary
        parsed["is_ai_generated"] = True
        parsed["engine_source"] = "Google Gemini Live AI"
        return parsed

    except Exception as e:
        # Graceful fallback: Never crash the application
        fallback = _generate_dynamic_mentor_analysis(current_skills, target_role, weekly_hours, experience_level)
        fallback["api_status_note"] = f"Gemini API returned an error ({str(e)}). Displaying verified mentor analysis."
        return fallback


def regenerate_roadmap_ai(
    current_skills: List[str],
    target_role: str,
    weekly_hours: str,
    experience_level: str,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Regenerates a fresh personalized 8-Week Roadmap."""
    full_result = generate_career_analysis(current_skills, target_role, weekly_hours, experience_level, api_key)
    return full_result.get("roadmap", [])


def regenerate_projects_ai(
    current_skills: List[str],
    target_role: str,
    weekly_hours: str,
    experience_level: str,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Regenerates a fresh set of exactly 3 GitHub-portfolio project ideas."""
    full_result = generate_career_analysis(current_skills, target_role, weekly_hours, experience_level, api_key)
    return full_result.get("projects", [])

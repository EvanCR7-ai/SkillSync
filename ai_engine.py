"""
SkillSync - AI Engine
Handles all interactions with Google Gemini API for skill gap analysis,
dynamic 8-week roadmap generation, and portfolio project recommendations.
Includes full offline/fallback mode when API keys are absent or services unavailable.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiAPIError(Exception):
    """Custom exception for Gemini API related errors."""
    pass


def get_api_key(provided_key: Optional[str] = None) -> str:
    """
    Retrieve Gemini API key with priority:
    1. Explicitly provided key (if provided)
    2. Streamlit Secrets (st.secrets["GEMINI_API_KEY"])
    3. Environment variable GEMINI_API_KEY from .env / system
    """
    if provided_key is not None:
        cleaned = provided_key.strip().strip("'\" \t\r\n")
        if cleaned == "" or cleaned != "your_gemini_api_key_here":
            return cleaned

    # Check Streamlit Secrets if running in Streamlit Cloud or local secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            sec_key = str(st.secrets["GEMINI_API_KEY"]).strip().strip("'\" \t\r\n")
            if sec_key and sec_key != "your_gemini_api_key_here":
                return sec_key
    except Exception:
        pass

    env_key = os.getenv("GEMINI_API_KEY", "").strip().strip("'\" \t\r\n")
    if env_key and env_key != "your_gemini_api_key_here":
        return env_key
        
    return ""


def get_engine_status(provided_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Safely determine the backend AI engine status WITHOUT exposing secrets.
    Returns:
        Dict with keys:
          - connected (bool)
          - mode (str: "gemini_ai" | "fallback")
          - label (str)
          - source_type (str)
    """
    resolved_key = get_api_key(provided_key)
    if resolved_key:
        source_type = "Server Environment"
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                if str(st.secrets["GEMINI_API_KEY"]).strip() == resolved_key:
                    source_type = "Streamlit Cloud Secrets"
        except Exception:
            pass
        return {
            "connected": True,
            "mode": "gemini_ai",
            "label": "Google Gemini AI Connected",
            "source_type": source_type
        }
    return {
        "connected": False,
        "mode": "fallback",
        "label": "Curated AI Fallback Engine Active",
        "source_type": "Offline Heuristics"
    }



def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Robustly extract and parse JSON from LLM output, handling markdown fences,
    conversational text, and occasional formatting quirks.
    """
    if not raw_text:
        raise GeminiAPIError("Empty response received from Gemini.")

    text = raw_text.strip()

    # Case 1: Look for ```json ... ``` code fence
    fence_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if fence_match:
        candidate = fence_match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Case 2: Extract outermost {...}
    brace_match = re.search(r'(\{[\s\S]*\})', text)
    if brace_match:
        candidate = brace_match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Try removing trailing commas before closing braces/brackets
            cleaned = re.sub(r',\s*([\]}])', r'\1', candidate)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError as err:
                raise GeminiAPIError(f"Could not parse JSON structure from Gemini: {err}")

    # Fallback direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise GeminiAPIError(f"Failed to decode response as JSON: {e}\nRaw output preview: {text[:250]}...")


def call_gemini_model(prompt: str, system_instruction: str, api_key: str) -> str:
    """
    Execute Gemini API call with automated model fallback and clean error diagnosis.
    """
    if not GENAI_AVAILABLE:
        raise GeminiAPIError("google-genai package is not installed. Please run: pip install google-genai")

    if not api_key:
        raise GeminiAPIError(
            "Gemini API Key is missing! Please provide your API key in the sidebar "
            "or set GEMINI_API_KEY in your .env file."
        )

    # Preferred models in order of availability & quality
    candidate_models = ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-flash-latest", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    last_error = None
    client = genai.Client(api_key=api_key)

    for model_name in candidate_models:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                max_output_tokens=7500,
                response_mime_type="application/json"
            )
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            err_msg = str(e).lower()
            if "api key not valid" in err_msg or "invalid api key" in err_msg or "permission_denied" in err_msg:
                raise GeminiAPIError(f"Invalid Gemini API Key provided. Details: {e}")
            continue

    raise GeminiAPIError(f"Gemini service currently unavailable ({last_error}).")


# ==============================================================================
# ROLE-SPECIFIC CURATED SKILLS DATABASE (FOR ROBUST OFFLINE / FALLBACK MODE)
# ==============================================================================
ROLE_CURRICULUM_DATA = {
    "Data Scientist": {
        "core_skills": [
            ("Python", "Core Programming", "Start with Python syntax, OOP, and data structures"),
            ("SQL & Database Design", "Databases", "Master complex joins, CTEs, and window functions"),
            ("Pandas & NumPy", "Data Manipulation", "Practice vectorized data cleaning and transformation"),
            ("Exploratory Data Analysis", "Data Analytics", "Use Seaborn and Plotly to discover statistical insights"),
            ("Machine Learning (Scikit-Learn)", "ML Algorithms", "Train classification, regression, and clustering models"),
            ("Feature Engineering", "Data Modeling", "Handle missing values, encoding, and scaling pipelines"),
            ("Deep Learning (PyTorch/TensorFlow)", "Advanced AI", "Understand neural networks, backpropagation, and CNNs"),
            ("Model Evaluation & Metrics", "MLOps", "Evaluate precision, recall, ROC-AUC, and cross-validation"),
            ("Git & GitHub Collaboration", "Tools & VCS", "Build clean repositories with reproducible Jupyter notebooks"),
            ("Model Deployment (FastAPI/Streamlit)", "Deployment", "Deploy interactive ML dashboards and REST endpoints")
        ],
        "projects": [
            ("Customer Churn Prediction Engine", "Beginner", "Predict customer churn using logistic regression and random forests on telco datasets.", "Builds core classification and evaluation skills.", ["Python", "Pandas", "Scikit-Learn", "Streamlit"], "1-2 weeks", "Interactive Streamlit app with live churn probability score"),
            ("End-to-End Housing Market Valuation Tool", "Intermediate", "Predict property prices using gradient boosting (XGBoost) with geospatial feature engineering.", "Demonstrates feature engineering and regression tuning.", ["Python", "XGBoost", "FastAPI", "Docker"], "2-3 weeks", "Containerized REST API predicting home values with documentation"),
            ("Real-Time Multimodal Sentiment & Financial Forecasting", "Advanced", "Analyze live financial news sentiment using fine-tuned transformer models and predict stock price trends.", "Demonstrates advanced NLP, time-series, and cloud pipelines.", ["PyTorch", "Transformers", "Kafka", "PostgreSQL", "AWS"], "3-4 weeks", "Full-stack predictive dashboard with streaming data ingestion")
        ]
    },
    "Frontend Developer": {
        "core_skills": [
            ("HTML5 & Semantic Markup", "Web Standards", "Master accessible semantic HTML and ARIA attributes"),
            ("Modern CSS & Flexbox/Grid", "Styling", "Build mobile-first, responsive layouts with CSS Grid"),
            ("JavaScript (ES6+)", "Core Language", "Understand closures, promises, event loop, and async/await"),
            ("TypeScript", "Type Safety", "Write strongly-typed interfaces, generics, and component props"),
            ("React.js", "Frontend Framework", "Master hooks, state management, and component architecture"),
            ("Tailwind CSS", "Modern Styling", "Create rapid utility-first, modern responsive UI designs"),
            ("State Management (Zustand/Redux)", "Architecture", "Manage complex client-side application state"),
            ("REST & GraphQL Integration", "API Integration", "Fetch, cache, and mutate data using React Query/TanStack"),
            ("Git & GitHub Workflow", "Tools & VCS", "Practice branching, pull requests, and semantic versioning"),
            ("Performance & SEO Optimization", "Web Performance", "Optimize Core Web Vitals, code-splitting, and lazy loading")
        ],
        "projects": [
            ("Interactive Task & Kanban Board", "Beginner", "A sleek Kanban board with drag-and-drop task management and local storage persistence.", "Demonstrates state management and interactive DOM manipulation.", ["React", "TypeScript", "Tailwind CSS"], "1 week", "Deployed responsive web app with dark/light theme"),
            ("E-Commerce Catalog with Cart & Checkout", "Intermediate", "High-performance store with product filtering, cart drawer, and Stripe mock checkout.", "Demonstrates API data caching, pagination, and forms.", ["Next.js", "React Query", "Tailwind CSS", "Stripe API"], "2 weeks", "Full-featured online store deployed on Vercel"),
            ("Collaborative Real-Time Workspace Canvas", "Advanced", "Shared digital whiteboard with real-time cursor sync and vector shape drawing.", "Showcases WebSocket communication, canvas rendering, and low-latency state sync.", ["React", "TypeScript", "WebSockets", "Canvas API", "Tailwind"], "3-4 weeks", "Multiplayer whiteboard application with room sharing")
        ]
    },
    "Backend Developer": {
        "core_skills": [
            ("Python / Node.js / Go", "Backend Language", "Master asynchronous I/O, OOP, and backend architectural patterns"),
            ("RESTful API Architecture", "API Design", "Design idempotent, versioned, and documented REST endpoints"),
            ("PostgreSQL & Relational Modeling", "Databases", "Write normalized schemas, indexes, and optimized SQL queries"),
            ("ORM & Query Builders (SQLAlchemy/Prisma)", "Data Layer", "Perform efficient migrations and transactional operations"),
            ("Authentication & JWT/OAuth", "Security", "Implement secure password hashing, JWTs, and RBAC authorization"),
            ("Redis Caching & Session Storage", "Performance", "Cache high-traffic endpoints and handle rate limiting"),
            ("Docker & Containerization", "DevOps Basics", "Containerize services with multi-stage production Dockerfiles"),
            ("Automated Testing (pytest/Jest)", "Code Quality", "Write unit, integration, and end-to-end API test suites"),
            ("CI/CD Automation (GitHub Actions)", "Automation", "Automate testing and container deployments on push"),
            ("Microservices & Message Queues (RabbitMQ/Kafka)", "Distributed Systems", "Decouple services using asynchronous event-driven messaging")
        ],
        "projects": [
            ("Scalable User Authentication & RBAC Service", "Beginner", "A production-grade auth service with JWT refresh tokens, email verification, and rate limiting.", "Covers web security, hashing, and token lifecycles.", ["Python/FastAPI", "PostgreSQL", "JWT", "Docker"], "1-2 weeks", "REST API with automated Swagger OpenAPI documentation"),
            ("High-Concurrency E-Commerce Order API", "Intermediate", "Order processing backend with inventory locking, Stripe webhooks, and Redis caching.", "Demonstrates database transactions and concurrency handling.", ["FastAPI/Express", "PostgreSQL", "Redis", "Docker"], "2-3 weeks", "Load-tested backend handling 500+ requests/second"),
            ("Distributed Event-Driven Notification System", "Advanced", "Microservice architecture processing thousands of email/SMS notifications via message queues.", "Demonstrates pub/sub architecture and resilient retry queues.", ["Python/Go", "Kafka/RabbitMQ", "PostgreSQL", "Docker", "AWS"], "3-4 weeks", "Fault-tolerant notification pipeline with worker cluster")
        ]
    },
    "AI/ML Engineer": {
        "core_skills": [
            ("Advanced Python & Vectorization", "Core Language", "Master NumPy, memory management, and performant Python"),
            ("Linear Algebra & Calculus for ML", "Math Foundations", "Understand gradients, matrix factorization, and eigenvalues"),
            ("Data Wrangling & Pipelines", "Data Engineering", "Build ETL pipelines with Pandas and Polars"),
            ("Machine Learning Fundamentals", "Classical ML", "Master decision trees, SVMs, and ensemble methods"),
            ("Deep Learning (PyTorch)", "Deep Learning", "Build custom neural network architectures and training loops"),
            ("Natural Language Processing & Transformers", "Modern AI", "Fine-tune HuggingFace models for classification and generation"),
            ("LLMs & Retrieval-Augmented Generation (RAG)", "Generative AI", "Build RAG pipelines with vector databases (Pinecone/Chroma)"),
            ("MLOps & Experiment Tracking (MLflow/W&B)", "MLOps", "Track model metrics, hyperparameters, and artifacts"),
            ("Model Serving & Optimization (ONNX/TensorRT)", "Deployment", "Quantize and deploy models with low latency via FastAPI"),
            ("Docker & Cloud GPU Workflows", "Infrastructure", "Containerize AI models and run distributed training jobs")
        ],
        "projects": [
            ("Intelligent Document Q&A with RAG", "Beginner", "Ask questions over uploaded PDF documents using LangChain and a local vector store.", "Demonstrates vector embeddings, semantic search, and prompt chains.", ["Python", "LangChain", "ChromaDB", "Streamlit"], "1-2 weeks", "Interactive document search & Q&A assistant"),
            ("Fine-Tuned Domain-Specific Code Reviewer", "Intermediate", "Fine-tune a lightweight LLM (e.g. Llama-3/Mistral) on GitHub PR datasets to generate code reviews.", "Demonstrates LoRA/PEFT fine-tuning and evaluation.", ["PyTorch", "HuggingFace", "PEFT", "FastAPI"], "2-3 weeks", "CLI tool and API that analyzes code diffs and suggests improvements"),
            ("Autonomous Multi-Agent Research Assistant", "Advanced", "Multi-agent system with web browsing, code execution, and dynamic report generation.", "Demonstrates agentic orchestration, tool-calling, and evaluation.", ["Python", "LangGraph", "Docker", "FastAPI", "React"], "3-4 weeks", "Full-stack autonomous research portal with live execution logs")
        ]
    }
}

DEFAULT_CURRICULUM = {
    "core_skills": [
        ("Core Programming & Algorithms", "Computer Science", "Master fundamental data structures, Big-O analysis, and problem-solving"),
        ("Version Control & Git Workflow", "VCS & Tools", "Use Git branching, rebasing, pull requests, and GitHub workflows"),
        ("Database Architecture & SQL", "Databases", "Design relational schemas, write optimized queries, and understand indexes"),
        ("API Design & Web Protocols", "Networking", "Understand HTTP/HTTPS, RESTful API conventions, and status codes"),
        ("System Architecture & Design Patterns", "Architecture", "Apply SOLID principles, MVC, and scalable system design"),
        ("Containerization (Docker)", "DevOps", "Build reproducible multi-stage Docker images for development and production"),
        ("Testing & Quality Assurance", "Testing", "Write comprehensive unit and integration tests with high code coverage"),
        ("Cloud Fundamentals (AWS/GCP)", "Cloud Computing", "Deploy web services, storage buckets, and serverless functions"),
        ("Security Best Practices", "Security", "Implement authentication, input sanitation, and secrets management"),
        ("Continuous Integration & Deployment (CI/CD)", "Automation", "Set up automated GitHub Actions build and deployment workflows")
    ],
    "projects": [
        ("Automated CLI Task & Resource Manager", "Beginner", "Command-line productivity tool with persistent storage, logging, and automated alerts.", "Demonstrates clean code, file I/O, and data structures.", ["Python", "SQLite", "Click"], "1 week", "Packaged CLI utility available on GitHub"),
        ("Full-Stack Enterprise Issue Tracking Dashboard", "Intermediate", "Full-stack application with user roles, ticket lifecycle workflows, and analytics charts.", "Demonstrates full-stack integration, auth, and database transactions.", ["FastAPI/Express", "React", "PostgreSQL", "Docker"], "2-3 weeks", "Deployed web application with interactive metrics"),
        ("High-Availability Microservices Notification Engine", "Advanced", "Distributed event-driven service with Redis queue, email/webhook delivery, and monitoring.", "Demonstrates scalable distributed system design and fault tolerance.", ["Python/Go", "Redis", "Docker", "Prometheus", "AWS"], "3-4 weeks", "Production-grade microservice with Grafana monitoring dashboard")
    ]
}


def generate_fallback_career_analysis(
    current_skills: List[str],
    target_role: str,
    study_hours: str,
    experience_level: str
) -> Dict[str, Any]:
    """
    Generate an intelligent, curated career gap analysis, 8-week roadmap, and 3 portfolio projects.
    Executes offline with zero external dependencies when Gemini API is unavailable or missing.
    """
    # Pick role data or fall back to general software engineering
    role_info = ROLE_CURRICULUM_DATA.get(target_role, DEFAULT_CURRICULUM)
    core_skills_raw = role_info["core_skills"]
    projects_raw = role_info["projects"]

    # Normalize existing skills for matching
    existing_lower = {s.strip().lower() for s in current_skills if s}

    skills_analysis = []
    matched_count = 0
    partial_count = 0
    missing_count = 0

    for skill_name, category, default_rec in core_skills_raw:
        s_lower = skill_name.lower()
        
        # Check exact or substring match
        is_exact = any(e in s_lower or s_lower in e for e in existing_lower)
        is_partial = any(
            any(w in s_lower for w in e.split()) or any(w in e for w in s_lower.split())
            for e in existing_lower
        )

        if is_exact:
            status = "Already Have"
            priority = "-"
            mastery = "Working proficiency"
            rec = f"Maintain and apply {skill_name} in complex production scenarios."
            matched_count += 1
        elif is_partial and not is_exact:
            status = "Partially Skilled"
            priority = "Medium"
            mastery = "Foundational understanding"
            rec = f"Deepen practical hands-on experience with {skill_name}."
            partial_count += 1
        else:
            status = "Need to Learn"
            priority = "High"
            mastery = "Not yet mastered"
            rec = default_rec
            missing_count += 1

        skills_analysis.append({
            "skill": skill_name,
            "category": category,
            "status": status,
            "priority": priority,
            "current_mastery": mastery,
            "recommendation": rec
        })

    # Prioritize skills to learn for the 8-week roadmap
    to_learn = [s for s in skills_analysis if s["status"] != "Already Have"]
    if not to_learn:
        to_learn = skills_analysis[:6]  # fallback if student already knows everything

    # Calibrate hours
    hours_num = 10
    if "3–5" in study_hours or "3-5" in study_hours:
        hours_num = 5
    elif "5–10" in study_hours or "5-10" in study_hours:
        hours_num = 8
    elif "15–20" in study_hours or "15-20" in study_hours:
        hours_num = 18
    elif "20+" in study_hours:
        hours_num = 22

    roadmap = []
    num_to_learn = len(to_learn)

    for week_idx in range(1, 9):
        if week_idx == 8:
            # Capstone Project
            w_title = f"Capstone Portfolio Project: Production {target_role} System"
            w_skills = [to_learn[0]["skill"] if to_learn else target_role, "CI/CD & Documentation", "Cloud Deployment"]
            w_objectives = [
                "Synthesize all skills learned into a cohesive production project",
                "Implement end-to-end testing with high test coverage",
                "Deploy the application to the cloud with GitHub Actions CI/CD",
                "Write comprehensive README documentation with architecture diagrams"
            ]
            w_resources = [
                {
                    "title": "GitHub Actions CI/CD Best Practices",
                    "provider": "GitHub Docs",
                    "type": "Documentation",
                    "description": "Automate build, lint, and automated test pipelines on every pull request.",
                    "link": "https://docs.github.com/en/actions"
                },
                {
                    "title": "Production Cloud Deployment & Scaling",
                    "provider": "Cloud Native Architecture",
                    "type": "Guide",
                    "description": "Deploy containerized services to managed cloud environments with zero-downtime health checks.",
                    "link": "https://docs.streamlit.io"
                }
            ]
            w_exercises = [
                "Create complete GitHub repository with semantic commit history",
                "Deploy live demo on Streamlit Cloud, Vercel, or AWS",
                "Record a 2-minute walkthrough video demonstration"
            ]
            w_outcome = "Deployable, interview-ready portfolio piece showcasing complete technical competency"
        else:
            # Distribute skills across weeks 1-7
            target_skill = to_learn[(week_idx - 1) % num_to_learn]
            skill_name = target_skill["skill"]
            category = target_skill["category"]

            w_title = f"{skill_name} Architecture & Practical Mastery"
            w_skills = [skill_name, category]
            w_objectives = [
                f"Master core syntax, design patterns, and idiomatic idioms of {skill_name}",
                f"Implement clean, modular components solving real-world engineering constraints with {skill_name}",
                f"Establish automated testing, profiling, and benchmarking to eliminate latency bottlenecks"
            ]
            w_resources = [
                {
                    "title": f"Official {skill_name} Developer Guide",
                    "provider": "Official Documentation",
                    "type": "Documentation",
                    "description": f"Comprehensive language specifications, standard libraries, and architectural paradigms for {skill_name}.",
                    "link": "https://devdocs.io"
                },
                {
                    "title": f"Production Engineering with {skill_name}",
                    "provider": "Roadmap.sh / Community",
                    "type": "Interactive Guide",
                    "description": f"Curated industry best practices, common pitfalls, and real-world system patterns for {skill_name}.",
                    "link": "https://roadmap.sh"
                }
            ]
            w_exercises = [
                f"Task 1: Core Setup & Architecture — Design and scaffold a modular service utilizing {skill_name} best practices.",
                f"Task 2: Implementation & Error Recovery — Build the primary functional pipeline with comprehensive exception handling and logging.",
                f"Task 3: Automated Verification — Write unit and integration test suites covering edge cases and performance boundaries."
            ]
            w_outcome = f"Confident production mastery of {skill_name} with verified test suites and clean architecture ready for team integration."
            w_mini_project = {
                "name": f"{skill_name} Micro-Service Sandbox",
                "objective": f"Construct an isolated, production-grade prototype implementing core capabilities of {skill_name}.",
                "technologies": [skill_name, category, "Clean Architecture"],
                "expected_output": f"Fully documented GitHub-ready repository featuring unit tests, CI config, and clean README.",
                "estimated_effort": f"{max(3, hours_num // 2)} hours"
            }

        if week_idx == 8:
            w_mini_project = {
                "name": f"Enterprise {target_role} Capstone System",
                "objective": f"Synthesize all curriculum competencies into a cohesive, deployed software system for {target_role}.",
                "technologies": w_skills + ["Docker", "CI/CD", "Cloud"],
                "expected_output": "Live deployed cloud application with automated CI/CD pipeline and architectural documentation.",
                "estimated_effort": f"{hours_num} hours"
            }

        roadmap.append({
            "week_number": week_idx,
            "week_title": w_title,
            "skills_to_develop": w_skills,
            "objectives": w_objectives,
            "resources": w_resources,
            "practical_exercises": w_exercises,
            "mini_project": w_mini_project,
            "expected_outcome": w_outcome,
            "estimated_study_hours": hours_num
        })

    portfolio_projects = []
    for title, difficulty, desc, prob, techs, est_time, deliverable in projects_raw:
        portfolio_projects.append({
            "difficulty": difficulty,
            "title": title,
            "short_description": desc,
            "problem_solved": prob,
            "technologies_required": techs,
            "skills_demonstrated": [t for t in techs[:3]],
            "estimated_completion_time": est_time,
            "expected_final_output": deliverable
        })

    matched_names = [s["skill"] for s in skills_analysis if s["status"] == "Already Have"]
    missing_names = [s["skill"] for s in skills_analysis if s["status"] == "Need to Learn"]
    partial_names = [s["skill"] for s in skills_analysis if s["status"] == "Partially Skilled"]

    strengths = [
        f"Demonstrated core proficiency in {', '.join(matched_names[:2])}." if matched_names else "Strong foundational motivation and dedication to software engineering discipline.",
        f"Existing technical baseline allows faster progression into advanced {target_role} topics.",
        "Clear goal alignment with modern industry engineering requirements."
    ]
    improvements = [
        f"Bridge high-priority gaps in {', '.join(missing_names[:2])} required for production readiness." if missing_names else f"Deepen advanced system design and edge-case testing for {target_role}.",
        f"Solidify intermediate familiarity with {', '.join(partial_names[:2])} into verified production mastery." if partial_names else "Establish automated CI/CD and deployment workflows.",
        "Translate technical knowledge into measurable, interview-ready portfolio applications."
    ]
    next_steps = [
        f"Focus initial weekly study on mastering {missing_names[0] if missing_names else 'core architecture'} through targeted hands-on code exercises.",
        "Establish a dedicated GitHub repository to track weekly deliverables and maintain semantic commit history.",
        "Complete the Week 4 mid-term project to validate full-stack competency before tackling the capstone."
    ]

    for p in portfolio_projects:
        p["why_valuable"] = (
            f"Directly showcases hands-on competency in {', '.join(p.get('technologies_required', [])[:3])}, "
            f"providing concrete proof of engineering maturity during {target_role} hiring evaluations."
        )
        p["learning_outcomes"] = [
            f"Architect and structure a production {p.get('title', 'software')} system.",
            "Implement automated testing, modular clean code, and API boundaries.",
            "Deploy a live interactive user-facing prototype with thorough technical documentation."
        ]
        p["expected_deliverables"] = p.get("expected_final_output", "Interactive live demo and repository")

    return {
        "career_summary": {
            "target_role": target_role,
            "market_demand_summary": (
                f"{target_role} is one of the highest-impact tech roles in modern engineering. "
                "Employers value engineers who combine strong core fundamentals with hands-on portfolio "
                "projects demonstrating clean architecture, testing, and cloud deployment."
            ),
            "motivational_message": (
                "Every senior engineer started with foundational steps. Your dedication of "
                f"{study_hours} weekly is the exact catalyst needed to bridge your skill gap and build your future."
            ),
            "strengths": strengths,
            "areas_to_improve": improvements,
            "next_steps": next_steps,
            "duration_weeks": 8,
            "weekly_study_hours": study_hours,
            "experience_level": experience_level,
            "source": "curated_fallback"
        },
        "skills_analysis": skills_analysis,
        "roadmap": roadmap,
        "portfolio_projects": portfolio_projects
    }


def analyze_career_path(
    current_skills: List[str],
    target_role: str,
    study_hours: str,
    experience_level: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform complete AI career analysis:
    - Attempts live Google Gemini generation if API key is present.
    - If no key is set or API service is unavailable, automatically activates
      the high-fidelity curated fallback engine so the student is never blocked.
    """
    resolved_key = get_api_key(api_key)

    if resolved_key:
        system_instruction = (
            "You are an elite Silicon Valley technical career mentor, FAANG Principal Engineer, "
            "and Curriculum Architect. Your mission is to provide an ultra-practical, objective, "
            "and deeply encouraging career roadmap that bridges a student's existing skills "
            "with their dream job requirements."
        )

        prompt = f"""
Analyze this student's profile and generate a comprehensive career gap analysis, an 8-week personalized learning roadmap, and 3 GitHub-ready portfolio projects.

STUDENT PROFILE:
- Current Existing Skills: {', '.join(current_skills)}
- Target Career Role: {target_role}
- Weekly Study Availability: {study_hours}
- Current Experience Level: {experience_level}

DETAILED INSTRUCTIONS:
1. ESSENTIAL SKILLS & GAP ANALYSIS:
   - Identify 9 to 15 core technical skills, frameworks, tools, and foundations essential in today's industry for {target_role}.
   - Compare each skill against the student's existing skills.
   - Assign status:
     * "Already Have" if the student has this skill or a direct equivalent.
     * "Partially Skilled" if they have an adjacent or foundational skill.
     * "Need to Learn" if it is a missing required competency.
   - Priority:
     * "High" for essential foundation/missing skills.
     * "Medium" for secondary tools or libraries.
     * "Low" for nice-to-have or specialized items.
     * "-" for "Already Have".
   - Recommendation: Clear, actionable 1-2 sentence advice.

2. PERSONALIZED 8-WEEK ROADMAP:
   - Exactly 8 weeks (Week 1 through Week 8).
   - Shorten or skip areas where the student already has strong skills.
   - Focus heavily on missing and partially skilled competencies.
   - Match weekly workload to {study_hours}.
   - Week 8 MUST be a Capstone Portfolio Project that synthesizes what they learned!
   - Include week_number, week_title, skills_to_develop, objectives, resources, practical_exercises, expected_outcome, estimated_study_hours.

3. PORTFOLIO PROJECT RECOMMENDATIONS:
   - Exactly 3 realistic, modern projects tailored to {target_role}: 1 Beginner, 1 Intermediate, 1 Advanced.
   - Include: title, difficulty, short_description, problem_solved, technologies_required, skills_demonstrated, estimated_completion_time, expected_final_output.

4. MOTIVATIONAL MESSAGE:
   - Provide an authentic, inspiring 2-3 sentence message reflecting their current readiness and potential.

OUTPUT FORMAT:
Respond with ONLY a valid, well-structured JSON object following this exact schema:
{{
  "career_summary": {{
    "target_role": "{target_role}",
    "market_demand_summary": "string",
    "motivational_message": "string"
  }},
  "skills_analysis": [
    {{
      "skill": "string",
      "category": "string",
      "status": "Already Have" | "Partially Skilled" | "Need to Learn",
      "priority": "High" | "Medium" | "Low" | "-",
      "current_mastery": "string",
      "recommendation": "string"
    }}
  ],
  "roadmap": [
    {{
      "week_number": 1,
      "week_title": "string",
      "skills_to_develop": ["string"],
      "objectives": ["string"],
      "resources": [
        {{"title": "string", "type": "Documentation"|"Course"|"Book"|"Interactive", "link": "https://..."}}
      ],
      "practical_exercises": ["string"],
      "expected_outcome": "string",
      "estimated_study_hours": 10
    }}
  ],
  "portfolio_projects": [
    {{
      "difficulty": "Beginner",
      "title": "string",
      "short_description": "string",
      "problem_solved": "string",
      "technologies_required": ["string"],
      "skills_demonstrated": ["string"],
      "estimated_completion_time": "string",
      "expected_final_output": "string"
    }},
    {{
      "difficulty": "Intermediate",
      "title": "string",
      "short_description": "string",
      "problem_solved": "string",
      "technologies_required": ["string"],
      "skills_demonstrated": ["string"],
      "estimated_completion_time": "string",
      "expected_final_output": "string"
    }},
    {{
      "difficulty": "Advanced",
      "title": "string",
      "short_description": "string",
      "problem_solved": "string",
      "technologies_required": ["string"],
      "skills_demonstrated": ["string"],
      "estimated_completion_time": "string",
      "expected_final_output": "string"
    }}
  ]
}}
"""
        try:
            raw_response = call_gemini_model(prompt, system_instruction, resolved_key)
            parsed_data = clean_json_response(raw_response)

            for key in ["career_summary", "skills_analysis", "roadmap", "portfolio_projects"]:
                if key not in parsed_data:
                    raise GeminiAPIError(f"Missing section '{key}' in Gemini output.")

            parsed_data["career_summary"]["source"] = "gemini_ai"
            return parsed_data
        except Exception:
            # If live Gemini call fails (e.g. 503, timeout, quota), activate fallback seamlessly
            pass

    # Fallback mode (no key configured or Gemini service temporarily unavailable)
    return generate_fallback_career_analysis(current_skills, target_role, study_hours, experience_level)


def regenerate_roadmap_ai(
    current_data: Dict[str, Any],
    custom_instructions: str = "",
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Regenerate only the 8-week roadmap with fresh focus or updated user constraints.
    """
    resolved_key = get_api_key(api_key)
    role = current_data.get("career_summary", {}).get("target_role", "Software Engineer")
    skills = [s.get("skill") for s in current_data.get("skills_analysis", []) if s.get("status") == "Already Have"]
    gaps = [s.get("skill") for s in current_data.get("skills_analysis", []) if s.get("status") != "Already Have"]

    if resolved_key:
        system_instruction = "You are a specialized curriculum architect creating an intensive 8-week technical roadmap."
        prompt = f"""
Regenerate a brand new, alternative 8-week learning roadmap for a student aiming to become a {role}.
Known Skills: {', '.join(skills)}
Key Skill Gaps: {', '.join(gaps)}
Additional Instructions: {custom_instructions or "Provide fresh, cutting-edge topics and hands-on exercises."}

Requirements:
- Exactly 8 weeks (Week 1 through Week 8).
- Week 8 must be a capstone project.
- Respond with a JSON object containing key "roadmap": [...] following the standard schema.
"""
        try:
            raw_response = call_gemini_model(prompt, system_instruction, resolved_key)
            parsed = clean_json_response(raw_response)
            if "roadmap" in parsed and isinstance(parsed["roadmap"], list):
                return parsed["roadmap"]
        except Exception:
            pass

    # Fallback regeneration: shift topics and apply custom focus
    fresh = generate_fallback_career_analysis(skills, role, "10–15 hours", "Intermediate")
    return fresh["roadmap"]


def regenerate_projects_ai(
    current_data: Dict[str, Any],
    custom_instructions: str = "",
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Regenerate 3 new portfolio projects (Beginner, Intermediate, Advanced).
    """
    resolved_key = get_api_key(api_key)
    role = current_data.get("career_summary", {}).get("target_role", "Software Engineer")
    gaps = [s.get("skill") for s in current_data.get("skills_analysis", []) if s.get("status") != "Already Have"]

    if resolved_key:
        system_instruction = "You are a senior tech hiring manager crafting standout portfolio projects for job candidates."
        prompt = f"""
Generate 3 fresh, innovative portfolio project ideas for a student targeting: {role}.
Addressing these skill gaps: {', '.join(gaps)}
User request: {custom_instructions or "Create unique, non-trivial projects that stand out from typical tutorial clones."}

Requirements:
- Exactly 3 projects: 1 Beginner, 1 Intermediate, 1 Advanced.
- Respond with a JSON object containing key "portfolio_projects": [...] following the standard schema.
"""
        try:
            raw_response = call_gemini_model(prompt, system_instruction, resolved_key)
            parsed = clean_json_response(raw_response)
            if "portfolio_projects" in parsed and isinstance(parsed["portfolio_projects"], list):
                return parsed["portfolio_projects"]
        except Exception:
            pass

    fresh = generate_fallback_career_analysis([], role, "10–15 hours", "Intermediate")
    return fresh["portfolio_projects"]


# ==============================================================================
# AI RESUME ANALYZER ENGINE
# ==============================================================================

def analyze_resume_ats(
    resume_text: str,
    job_description: str = "",
    target_role: str = "Software Engineer",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform deep ATS compatibility analysis, keyword gap detection, and actionable
    resume optimization recommendations using Gemini AI or the heuristic ATS engine.
    """
    resolved_key = get_api_key(api_key)

    if resolved_key and len(resume_text.strip()) > 30:
        system_instruction = (
            "You are an executive Technical Recruiter and ATS (Applicant Tracking System) optimization specialist. "
            "Analyze the candidate's resume strictly against their target role and optional job description."
        )
        prompt = f"""
Target Role: {target_role}
Job Description: {job_description or "General industry standards for " + target_role}

Resume Content:
\"\"\"
{resume_text[:4000]}
\"\"\"

Analyze the resume and return a JSON object with this exact schema:
{{
  "ats_score": integer (0 to 100),
  "match_level": "High Match" | "Strong Potential" | "Moderate Match" | "Needs Improvement",
  "matching_skills": ["string", "string"],
  "missing_keywords": ["string", "string"],
  "strengths": ["string", "string"],
  "improvements": ["string", "string"],
  "actionable_recommendations": ["string", "string"]
}}
"""
        try:
            raw_response = call_gemini_model(prompt, system_instruction, resolved_key)
            parsed = clean_json_response(raw_response)
            if "ats_score" in parsed and "matching_skills" in parsed:
                parsed["source"] = "gemini_ai"
                return parsed
        except Exception:
            pass

    # Heuristic Fallback ATS Engine
    resume_lower = resume_text.lower()
    role_info = ROLE_CURRICULUM_DATA.get(target_role, DEFAULT_CURRICULUM)
    core_skills = [s[0] for s in role_info.get("core_skills", [])]

    # Keyword matching
    matched = []
    missing = []
    for skill in core_skills:
        # Check if words match
        s_words = [w.lower() for w in re.split(r'[\s/&]+', skill) if len(w) > 2]
        if any(w in resume_lower for w in s_words):
            matched.append(skill)
        else:
            missing.append(skill)

    # Section checklist
    sections = ["experience", "education", "project", "skill", "certification"]
    found_sections = [sec for sec in sections if sec in resume_lower]

    # Score calculation
    skill_ratio = len(matched) / max(len(core_skills), 1)
    section_ratio = len(found_sections) / len(sections)
    length_score = 1.0 if len(resume_text.split()) > 150 else 0.5
    raw_score = int((skill_ratio * 60) + (section_ratio * 30) + (length_score * 10))
    ats_score = max(35, min(95, raw_score))

    if ats_score >= 80:
        match_level = "High Match"
    elif ats_score >= 65:
        match_level = "Strong Potential"
    elif ats_score >= 50:
        match_level = "Moderate Match"
    else:
        match_level = "Needs Improvement"

    strengths = []
    if matched:
        strengths.append(f"Demonstrates clear experience with core stack: {', '.join(matched[:3])}.")
    if "project" in found_sections:
        strengths.append("Contains dedicated project portfolio section validating practical skills.")
    if "experience" in found_sections:
        strengths.append("Chronological career history is clearly structured.")
    if not strengths:
        strengths.append("Clear educational background and foundational baseline.")

    improvements = []
    if missing:
        improvements.append(f"Incorporate missing industry keywords: {', '.join(missing[:4])}.")
    if "education" not in found_sections:
        improvements.append("Ensure educational degrees and graduation milestones are explicitly stated.")
    improvements.append("Quantify achievements using metrics (e.g. 'Improved API latency by 35%').")

    recs = [
        f"Add a dedicated 'Technical Skills' matrix highlighting {', '.join(missing[:3])}.",
        "Include active GitHub repository links to live portfolio projects.",
        "Ensure resume follows a single-column, standard ATS-friendly PDF structure."
    ]

    top_improvements = [
        {
            "title": "Quantify Engineering Impact with Key Metrics",
            "what": "Replace qualitative descriptions with measurable technical and business outcomes (latency, throughput, cost).",
            "why": "ATS scoring algorithms and engineering hiring managers rank resumes with quantified metrics 3x higher.",
            "how_to_fix": "Adopt Google's XYZ formula: Accomplished [X], as measured by [Y], by doing [Z].",
            "example_before": "Responsible for optimizing backend database queries.",
            "example_after": "Optimized PostgreSQL indexes and query plans, reducing p95 latency by 42% across 500k daily requests."
        },
        {
            "title": "Integrate Missing Production Keywords",
            "what": f"Explicitly integrate required tools and frameworks ({', '.join(missing[:3]) if missing else 'Docker, CI/CD, Cloud'}) into project bullets.",
            "why": "Automated ATS parsers score keyword density before human recruiters ever inspect your profile.",
            "how_to_fix": "Weave target keywords naturally into context rather than isolated comma lists.",
            "example_before": "Deployed web applications to web servers.",
            "example_after": "Automated containerized deployment using Docker and GitHub Actions CI/CD to AWS cloud infrastructure."
        },
        {
            "title": "Highlight System Architecture & Design Scope",
            "what": "Describe the architectural scope of your projects (e.g. microservices, REST/GraphQL, caching, data layers).",
            "why": "Signals engineering maturity, structural reasoning, and readiness for independent contribution.",
            "how_to_fix": "Specify the data flows, interface boundaries, and trade-offs made in key projects.",
            "example_before": "Built an API for users to access platform data.",
            "example_after": "Architected a scalable RESTful API with FastAPI and Redis caching, serving 10k concurrent daily active users."
        },
        {
            "title": "Categorize Technical Skills Section",
            "what": "Organize technical competencies into clear groupings: Languages, Frameworks, Databases, Tools & Platforms.",
            "why": "Allows both automated parsers and interviewers to quickly verify technical stack compatibility.",
            "how_to_fix": "Format the skills section into bold categories rather than an unsegmented paragraph.",
            "example_before": "Python, SQL, React, Git, Docker, AWS, PostgreSQL, Linux",
            "example_after": "Languages: Python, SQL • Frameworks: FastAPI, React • Databases: PostgreSQL, Redis • Cloud & Tools: Docker, AWS, Git"
        },
        {
            "title": "Tailor Summary Statement to Target Role",
            "what": f"Write a focused 2-sentence opening summary specifically targeting {target_role} opportunities.",
            "why": "Establishes immediate candidate relevance and primes recruiters for your key technical strengths.",
            "how_to_fix": "State your core specialization, years of focused practice, and primary value proposition.",
            "example_before": "Passionate developer looking to grow technical skills at an innovative company.",
            "example_after": f"Software Engineer specializing in {target_role} systems, high-throughput architectures, and automated cloud deployments."
        }
    ]

    return {
        "ats_score": ats_score,
        "match_level": match_level,
        "matching_skills": matched if matched else ["Foundational Problem Solving"],
        "missing_keywords": missing if missing else ["Advanced Architecture", "System Design"],
        "strengths": strengths,
        "formatting_issues": [
            "Use standard section headers ('Experience', 'Education', 'Technical Skills') for 100% reliable parser ingestion.",
            "Avoid multi-column tables, text boxes, or non-standard glyphs that can scramble ATS text flow."
        ],
        "experience_relevance": f"Foundational alignment with {target_role} standards, with key opportunities to spotlight production metrics and end-to-end delivery.",
        "top_improvements": top_improvements,
        "improvements": improvements,
        "actionable_recommendations": recs,
        "source": "heuristic_engine"
    }


# ==============================================================================
# AI MOCK INTERVIEW ENGINE
# ==============================================================================

MOCK_INTERVIEW_QUESTIONS_DATABASE = {
    "Data Scientist": [
        {
            "id": "ds_1",
            "category": "Machine Learning & Modeling",
            "question": "How do you detect and mitigate multicollinearity in a regression dataset, and what impact does it have on model interpretability?",
            "expected_topics": ["VIF (Variance Inflation Factor)", "Correlation Matrix", "L2 Regularization (Ridge)", "PCA"]
        },
        {
            "id": "ds_2",
            "category": "Statistics & Experimentation",
            "question": "Explain how you would design an A/B test for an e-commerce recommendation system. What statistical power, sample size, and pitfalls would you consider?",
            "expected_topics": ["Hypothesis Testing", "p-values & Type I/II errors", "Sample Size Calculation", "Novelty Effect"]
        },
        {
            "id": "ds_3",
            "category": "Practical Data Engineering",
            "question": "Suppose your training data has 40% missing values in a critical continuous feature. How do you decide whether to impute or drop it?",
            "expected_topics": ["MCAR vs MAR vs MNAR", "KNN/Iterative Imputation", "Domain Analysis", "Indicator Columns"]
        }
    ],
    "Frontend Developer": [
        {
            "id": "fe_1",
            "category": "React Architecture & Performance",
            "question": "Explain the difference between useMemo, useCallback, and React.memo. When would using them actually hurt performance?",
            "expected_topics": ["Referential Equality", "Re-render cycles", "Garbage collection overhead", "Premature optimization"]
        },
        {
            "id": "fe_2",
            "category": "Web Performance & Core Web Vitals",
            "question": "What is Largest Contentful Paint (LCP) and Cumulative Layout Shift (CLS), and what architectural steps do you take to optimize them?",
            "expected_topics": ["Asset preloading", "Image dimensions & CDN", "Font display swap", "Code splitting"]
        },
        {
            "id": "fe_3",
            "category": "JavaScript Internals",
            "question": "How does the JavaScript Event Loop handle microtasks versus macrotasks when executing async/await and Promises?",
            "expected_topics": ["Call Stack", "Microtask Queue", "Event Loop tick", "Promise resolution"]
        }
    ],
    "Backend Developer": [
        {
            "id": "be_1",
            "category": "Database & Distributed Systems",
            "question": "How do you design database indexes to optimize a query with multiple WHERE clauses and an ORDER BY? When do indexes become a liability?",
            "expected_topics": ["Composite B-Tree index", "Index cardinality", "Write amplification", "Covering index"]
        },
        {
            "id": "be_2",
            "category": "API Architecture & Concurrency",
            "question": "How do you ensure idempotency in high-concurrency payment and order processing endpoints?",
            "expected_topics": ["Idempotency keys", "Distributed locks (Redis)", "Database transactions (ACID)", "Unique constraints"]
        },
        {
            "id": "be_3",
            "category": "Microservices & Reliability",
            "question": "Describe how you implement the Circuit Breaker pattern and dead-letter queues to prevent cascading failures across microservices.",
            "expected_topics": ["Failure thresholds", "Half-open state", "Retry backoff with jitter", "Dead-letter queues"]
        }
    ]
}


def generate_mock_interview_questions(
    target_role: str = "Software Engineer",
    experience_level: str = "Intermediate",
    category: str = "Technical",
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generate realistic, role-specific interview questions.
    """
    resolved_key = get_api_key(api_key)

    if resolved_key:
        system_instruction = "You are a Principal Software Engineering hiring manager conducting realistic technical interviews."
        prompt = f"""
Generate 3 realistic, high-quality interview questions for a {experience_level} candidate applying for: {target_role}.
Interview focus: {category}.

Return a JSON object with this exact structure:
{{
  "questions": [
    {{
      "id": "q1",
      "category": "string",
      "question": "string",
      "expected_topics": ["topic1", "topic2"]
    }}
  ]
}}
"""
        try:
            raw_response = call_gemini_model(prompt, system_instruction, resolved_key)
            parsed = clean_json_response(raw_response)
            if "questions" in parsed and isinstance(parsed["questions"], list) and len(parsed["questions"]) > 0:
                return parsed["questions"]
        except Exception:
            pass

    # Curated Question Bank Fallback
    bank = MOCK_INTERVIEW_QUESTIONS_DATABASE.get(target_role)
    if not bank:
        # Generic engineering bank
        bank = [
            {
                "id": "gen_1",
                "category": "System Architecture",
                "question": f"Walk me through how you would architect a scalable, fault-tolerant backend system for {target_role}.",
                "expected_topics": ["Load balancing", "Caching", "Database partitioning", "Observability"]
            },
            {
                "id": "gen_2",
                "category": "Practical Problem Solving",
                "question": "Describe a challenging bug or performance bottleneck you encountered in production. How did you isolate and resolve it?",
                "expected_topics": ["Profiling tools", "Root cause analysis", "Hypothesis testing", "Post-mortem"]
            },
            {
                "id": "gen_3",
                "category": "Best Practices & Testing",
                "question": "How do you balance test coverage (unit vs integration vs e2e) against developer velocity in an agile engineering team?",
                "expected_topics": ["Testing Pyramid", "Mocking & Stubs", "CI/CD integration", "Contract testing"]
            }
        ]
    return bank


def evaluate_interview_answer(
    question: str,
    user_answer: str,
    target_role: str = "Software Engineer",
    experience_level: str = "Intermediate",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate the candidate's interview answer and provide scored feedback,
    strengths, improvement areas, and a model exemplary answer.
    """
    resolved_key = get_api_key(api_key)

    if resolved_key and len(user_answer.strip()) > 10:
        system_instruction = "You are a seasoned Tech Interview Coach providing constructive, rigorous feedback."
        prompt = f"""
Role: {target_role} ({experience_level})
Interview Question: {question}

Candidate's Answer:
\"\"\"
{user_answer}
\"\"\"

Evaluate the answer thoroughly and return a JSON object with this exact structure:
{{
  "score": integer (1 to 10),
  "feedback": "string summarizing response quality",
  "strengths": ["string", "string"],
  "improvement_areas": ["string", "string"],
  "model_answer": "string containing an exemplary answer"
}}
"""
        try:
            raw_response = call_gemini_model(prompt, system_instruction, resolved_key)
            parsed = clean_json_response(raw_response)
            if "score" in parsed and "feedback" in parsed:
                parsed["source"] = "gemini_ai"
                return parsed
        except Exception:
            pass

    # Heuristic Answer Evaluator Fallback
    words = user_answer.strip().split()
    word_count = len(words)

    # Heuristic scoring based on depth and articulation
    if word_count > 100:
        base_score = 8
    elif word_count > 50:
        base_score = 7
    elif word_count > 25:
        base_score = 5
    elif word_count > 5:
        base_score = 4
    else:
        base_score = 2

    strengths = [
        "Directly addressed the core interview prompt.",
        "Demonstrated working engineering terminology and logical flow."
    ]
    improvements = [
        "Include concrete real-world production metrics or trade-offs.",
        "Structure the answer using the STAR method (Situation, Task, Action, Result)."
    ]
    model_answer = (
        "An exemplary answer begins with a clear high-level thesis, outlines the trade-offs of 2-3 architectural approaches, "
        "and illustrates the solution with a concrete production example highlighting performance metrics and edge-case handling."
    )

    sub_scores = {
        "technical_accuracy": max(1, min(10, base_score + 1 if base_score < 9 else base_score)),
        "communication_quality": max(1, min(10, base_score)),
        "problem_solving": max(1, min(10, base_score - 1 if base_score > 3 else base_score)),
        "completeness": max(1, min(10, base_score))
    }
    missing_concepts = [
        "Explicitly stating time (Big-O) and space complexity trade-offs.",
        "Addressing real-world production edge cases, network timeouts, and fault tolerance.",
        "Justifying architectural tool selection over alternative approaches."
    ]
    checklist = [
        "State problem scope and clarify assumptions immediately before proposing a solution.",
        "Outline algorithmic steps clearly before diving into code or syntax specifics.",
        "Analyze time complexity O(N) and memory footprint explicitly.",
        "Discuss edge cases (null inputs, scale limits, concurrency race conditions).",
        "Conclude with how the implementation is tested and monitored in production."
    ]

    return {
        "score": base_score,
        "sub_scores": sub_scores,
        "feedback": f"Strong conceptual effort with {word_count} words. Deepening specific production trade-offs will elevate your response to senior level.",
        "strengths": strengths,
        "improvement_areas": improvements,
        "missing_concepts": missing_concepts,
        "how_to_improve": (
            "Structure your technical answers using the STAR framework (Situation, Task, Action, Result). "
            "Concretely explain your engineering reasoning and articulate architectural trade-offs."
        ),
        "model_answer": model_answer,
        "checklist": checklist,
        "source": "heuristic_evaluator"
    }


if __name__ == "__main__":
    # When Streamlit Community Cloud launches ai_engine.py as main module,
    # delegate execution seamlessly to the primary Streamlit application UI in app.py.
    import runpy
    import sys
    from pathlib import Path

    app_file = Path(__file__).resolve().parent / "app.py"
    if str(app_file.parent) not in sys.path:
        sys.path.insert(0, str(app_file.parent))
    if app_file.exists():
        runpy.run_path(str(app_file), run_name="__main__")


"""
SkillSync 2.0 – AI Career Intelligence Platform
Enterprise-grade Frontend Architecture with Obsidian Gold Design System.
Inspired by Linear, Stripe, Vercel, and modern AI SaaS platforms.
Full-stack Python Streamlit Application.
"""

import os
import sys
import html
import textwrap
import base64
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

# Internal module imports
import ai_engine
import roadmap_generator
import project_preview_engine
import utils
import icons

# Load environment variables
load_dotenv()

# Path configuration using pathlib
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "skillsync-gold-logo.png"
ICON_PATH = ASSETS_DIR / "skillsync-gold-icon.png"

# Page configuration
st.set_page_config(
    page_title="SkillSync 2.0 – AI Career Intelligence",
    page_icon=str(ICON_PATH) if ICON_PATH.exists() else "⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css(file_name: str = "styles.css"):
    candidate = BASE_DIR / file_name
    if not candidate.exists():
        candidate = Path(file_name)
    if candidate.exists():
        with open(candidate, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Native Streamlit Logo & Icon System (Expanded & Collapsed Sidebar)
if LOGO_PATH.exists():
    st.logo(
        str(LOGO_PATH),
        icon_image=str(ICON_PATH) if ICON_PATH.exists() else None,
        size="large"
    )

def get_logo_base64() -> str:
    """Helper to encode the official Obsidian Gold logo for crisp inline rendering."""
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

# ==============================================================================
# SESSION STATE INITIALIZATION & NORMALIZATION
# ==============================================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "student_profile" not in st.session_state:
    st.session_state.student_profile = None

if "readiness_data" not in st.session_state:
    st.session_state.readiness_data = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None

if "mock_interview_questions" not in st.session_state:
    st.session_state.mock_interview_questions = None

if "mock_interview_eval" not in st.session_state:
    st.session_state.mock_interview_eval = None

if "active_interview_idx" not in st.session_state:
    st.session_state.active_interview_idx = 0

# Page normalization mapping (strips any legacy emojis)
CANONICAL_PAGES = [
    "Dashboard",
    "Career Roadmap",
    "Skill Gap Analysis",
    "Resume Analyzer",
    "Mock Interview",
    "Project Recommendations",
    "Learning Resources",
    "Settings",
]

for canonical in CANONICAL_PAGES:
    if canonical in st.session_state.current_page:
        st.session_state.current_page = canonical
        break


# ==============================================================================
# DYNAMIC THEME ENGINE
# ==============================================================================
def apply_active_theme():
    if st.session_state.get("theme", "dark") == "light":
        st.markdown("""
        <style>
        :root, .stApp {
            --bg-primary: #F7F5EF !important;
            --bg-secondary: #F0EDE5 !important;
            --bg-card: #FFFFFF !important;
            --bg-card-elevated: #FAF8F2 !important;
            --gold-primary: #B58B35 !important;
            --gold-champagne: #D9BD79 !important;
            --gold-muted: #8C6B23 !important;
            --text-primary: #171717 !important;
            --text-secondary: #77716A !important;
            --text-muted: #9C948A !important;
            --border-color: #E5DED0 !important;
            --border-gold: rgba(181, 139, 53, 0.35) !important;
            --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
            --shadow-gold: 0 0 15px rgba(181, 139, 53, 0.1) !important;
            background-color: #F7F5EF !important;
            color: #171717 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #F0EDE5 !important;
            border-right: 1px solid #E5DED0 !important;
            color: #171717;
        }
        .hero-obsidian, .metric-obsidian, .panel-obsidian {
            background: #FFFFFF !important;
            border-color: #E5DED0 !important;
        }
        .hero-title, .metric-value {
            color: #171717 !important;
        }
        .hero-description, .metric-label {
            color: #77716A !important;
        }
        .stTextInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea {
            background-color: #FFFFFF !important;
            border-color: #E5DED0 !important;
            color: #171717 !important;
        }
        div[data-testid="stExpander"] {
            background: #FFFFFF !important;
            border-color: #E5DED0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        :root, .stApp {
            --bg-primary: #090909 !important;
            --bg-secondary: #101010 !important;
            --bg-card: #171717 !important;
            --bg-card-elevated: #202020 !important;
            --gold-primary: #D4AF37 !important;
            --gold-champagne: #F1D58A !important;
            --gold-muted: #A88735 !important;
            --text-primary: #F8F5EC !important;
            --text-secondary: #A5A5A5 !important;
            --text-muted: #6E6E6E !important;
            --border-color: #303030 !important;
            --border-gold: rgba(212, 175, 55, 0.35) !important;
            --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.45) !important;
            --shadow-gold: 0 0 15px rgba(212, 175, 55, 0.12) !important;
            background-color: #090909 !important;
            color: #F8F5EC !important;
        }
        [data-testid="stSidebar"] {
            background-color: #101010 !important;
            border-right: 1px solid #303030 !important;
            color: #F8F5EC;
        }
        .hero-obsidian, .metric-obsidian, .panel-obsidian {
            background: #171717 !important;
            border-color: #303030 !important;
        }
        .hero-title, .metric-value {
            color: #F8F5EC !important;
        }
        .hero-description, .metric-label {
            color: #A5A5A5 !important;
        }
        .stTextInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea {
            background-color: #171717 !important;
            border-color: #303030 !important;
            color: #F8F5EC !important;
        }
        div[data-testid="stExpander"] {
            background: #171717 !important;
            border-color: #303030 !important;
        }
        </style>
        """, unsafe_allow_html=True)

apply_active_theme()

# ==============================================================================
# ENTERPRISE SIDEBAR ARCHITECTURE (NO EMOJIS, LUCIDE & MATERIAL SYSTEM)
# ==============================================================================
NAV_GROUPS = [
    {
        "group": "WORKSPACE",
        "items": [
            ("Dashboard", ":material/dashboard:"),
            ("Career Roadmap", ":material/route:"),
            ("Skill Gap Analysis", ":material/bar_chart:"),
        ]
    },
    {
        "group": "AI TOOLS",
        "items": [
            ("Resume Analyzer", ":material/find_in_page:"),
            ("Mock Interview", ":material/forum:"),
            ("Project Recommendations", ":material/business_center:"),
        ]
    },
    {
        "group": "RESOURCES",
        "items": [
            ("Learning Resources", ":material/menu_book:"),
        ]
    },
    {
        "group": "PREFERENCES",
        "items": [
            ("Settings", ":material/settings:"),
        ]
    }
]

with st.sidebar:
    is_dark = (st.session_state.theme == "dark")
    gold_color = "#D4AF37" if is_dark else "#B58B35"
    gold_champagne = "#F1D58A" if is_dark else "#D9BD79"

    # Official SkillSync Gold Brand Header
    if LOGO_PATH.exists():
        st.markdown("<div class='sidebar-brand-divider'></div>", unsafe_allow_html=True)

    # Grouped Navigation System
    for group_data in NAV_GROUPS:
        st.markdown(f'<div class="nav-group-header">{group_data["group"]}</div>', unsafe_allow_html=True)
        for item_name, icon_name in group_data["items"]:
            is_active = (st.session_state.current_page == item_name)
            if st.button(
                item_name,
                key=f"nav_btn_{item_name}",
                type="primary" if is_active else "secondary",
                icon=icon_name,
                use_container_width=True
            ):
                st.session_state.current_page = item_name
                st.rerun()

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # Theme Switcher Control (Clean Dark Mode / Light Mode)
    theme_icon_svg = icons.get_lucide_svg("moon" if is_dark else "sun", size=14, color=gold_color)
    utils.safe_render_html(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.35rem 0.25rem 0.25rem 0.25rem; font-size: 11px; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">
        <span>Theme</span>
        <span>{theme_icon_svg}</span>
    </div>
    """)
    theme_choice = st.radio(
        "Theme Mode",
        options=["Dark Mode", "Light Mode"],
        index=0 if is_dark else 1,
        horizontal=True,
        key="theme_radio_selector",
        label_visibility="collapsed"
    )
    selected_theme = "dark" if "Dark" in theme_choice else "light"
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    # Centralized Backend Engine Status
    engine_status = ai_engine.get_engine_status()
    cpu_icon_svg = icons.get_lucide_svg("cpu", size=14, color=gold_color)
    if engine_status["connected"]:
        utils.safe_render_html(f"""
        <div class="engine-status-box">
            <span class="engine-status-dot online"></span>
            <span style="color: var(--text-secondary);">{cpu_icon_svg} Google Gemini Active</span>
        </div>
        """)
    else:
        utils.safe_render_html(f"""
        <div class="engine-status-box">
            <span class="engine-status-dot fallback"></span>
            <span style="color: var(--text-secondary);">{cpu_icon_svg} Curated Fallback Active</span>
        </div>
        """)

    # Candidate Profile Section at Sidebar Bottom
    target_role_display = "Candidate"
    if st.session_state.student_profile:
        target_role_display = st.session_state.student_profile.get("target_role", "Candidate")

    user_icon_svg = icons.get_lucide_svg("user-round", size=16, color="#090909")
    utils.safe_render_html(f"""
    <div class="sidebar-profile-card">
        <div class="sidebar-profile-avatar">{user_icon_svg}</div>
        <div style="overflow: hidden;">
            <div style="font-weight: 700; font-size: 13px; color: var(--text-primary); white-space: nowrap; text-overflow: ellipsis;">Active Candidate</div>
            <div style="font-size: 12px; color: {gold_champagne}; white-space: nowrap; text-overflow: ellipsis; font-weight: 500;">{html.escape(target_role_display)}</div>
        </div>
    </div>
    """)

    if st.session_state.analysis_result:
        if st.button("Reset Analysis", icon=":material/refresh:", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.student_profile = None
            st.session_state.readiness_data = None
            st.toast("Analysis reset.", icon=":material/info:")
            st.rerun()


# ==============================================================================
# GLOBAL CONSTANTS & SELECTION LISTS
# ==============================================================================
AVAILABLE_SKILLS = [
    "Python", "JavaScript", "HTML", "CSS", "SQL", "Data Structures & Algorithms",
    "React", "Node.js", "C", "C++", "Java", "Pandas", "NumPy", "Git & GitHub",
    "Docker", "Kubernetes", "AWS", "Linux", "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch", "Power BI", "Tableau", "REST APIs", "GraphQL",
    "Tailwind CSS", "Next.js", "Django", "FastAPI", "PostgreSQL", "MongoDB",
    "TypeScript", "Figma", "UI/UX Design", "Scikit-Learn", "Computer Networks",
    "Operating Systems", "Cybersecurity Basics"
]

TARGET_ROLES = [
    "Data Scientist",
    "Data Analyst",
    "AI/ML Engineer",
    "Python Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Cybersecurity Analyst",
    "Cloud Engineer",
    "DevOps Engineer",
    "UI/UX Designer",
    "Software Engineer",
    "Custom Role..."
]

STUDY_AVAILABILITY = [
    "3–5 hours",
    "5–10 hours",
    "10–15 hours",
    "15–20 hours",
    "20+ hours"
]

EXPERIENCE_LEVELS = [
    "Beginner",
    "Intermediate",
    "Advanced"
]


# ==============================================================================
# GLOBAL APPLICATION HEADER (RESPONSIVE BRANDING & BREADCRUMBS)
# ==============================================================================
logo_b64 = get_logo_base64()
active_page_title = st.session_state.current_page
header_html = f"""
<div class="app-header-container">
    <div class="app-header-brand">
        <div class="app-header-logo-wrap">
            <img src="data:image/png;base64,{logo_b64}" alt="SkillSync 2.0" class="app-header-logo-img" />
        </div>
    </div>
    <div class="app-header-meta">
        <span class="app-header-breadcrumb">Platform / <span class="app-header-page">{html.escape(active_page_title)}</span></span>
        <span class="app-header-badge">Obsidian Gold Edition</span>
    </div>
</div>
"""
utils.safe_render_html(header_html)


# ==============================================================================
# PAGE 1: DASHBOARD
# ==============================================================================
if st.session_state.current_page == "Dashboard":
    is_dark = (st.session_state.theme == "dark")
    gold_color = "#D4AF37" if is_dark else "#B58B35"
    champagne_color = "#F1D58A" if is_dark else "#D9BD79"

    # Hero Section
    col_hero_text, col_hero_visual = st.columns([3, 2])
    with col_hero_text:
        utils.safe_render_html("""
        <div class="hero-obsidian">
            <div class="hero-eyebrow">YOUR PERSONAL AI CAREER MENTOR</div>
            <h1 class="hero-title">Build Your Future.<br>Master Your Career.</h1>
            <p class="hero-description">
                Turn your ambitions into achievements with intelligent career insights, personalized learning roadmaps, and AI-powered skill analysis.
            </p>
        </div>
        """)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Generate Career Roadmap", key="dash_hero_cta", type="primary", icon=":material/auto_awesome:", use_container_width=True):
                st.session_state.current_page = "Career Roadmap"
                st.rerun()
        with col_btn2:
            if st.button("Explore Platform", key="dash_hero_features", icon=":material/explore:", use_container_width=True):
                st.session_state.current_page = "Skill Gap Analysis"
                st.rerun()

    with col_hero_visual:
        score_val = st.session_state.readiness_data.get("score", 0) if st.session_state.readiness_data else 0
        matched_val = st.session_state.readiness_data.get("matched", 0) if st.session_state.readiness_data else 0
        missing_val = st.session_state.readiness_data.get("missing", 0) if st.session_state.readiness_data else 0

        if st.session_state.readiness_data:
            gauge_fig = roadmap_generator.create_readiness_gauge(
                score=score_val,
                matched=matched_val,
                partial=st.session_state.readiness_data.get("partial", 0),
                missing=missing_val,
                total=st.session_state.readiness_data.get("total", 0),
                theme=st.session_state.theme
            )
            st.plotly_chart(gauge_fig, use_container_width=True)
        else:
            target_icon_svg = icons.get_lucide_svg("target", size=36, color=gold_color)
            utils.safe_render_html(f"""
            <div class="hero-obsidian" style="text-align: center; padding: 2.25rem 1.5rem; height: 100%;">
                <div style="margin-bottom: 0.75rem;">{target_icon_svg}</div>
                <div style="font-size: 1.25rem; font-weight: 700; font-family: var(--font-heading);">Personalized Career Intelligence</div>
                <div style="font-size: 14px; color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.5;">
                    Generate an analysis to benchmark your current skills against industry hiring bars with Obsidian Gold precision.
                </div>
            </div>
            """)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 4 Metric Cards Grid (Using Clean Lucide Icons)
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    completed_weeks = 0
    if st.session_state.analysis_result:
        completed_weeks = sum(
            1 for i in range(1, 9)
            if st.session_state.get(f"week_completed_{i}", False)
        )

    icon_target = icons.get_lucide_svg("target", size=20, color=gold_color)
    icon_check = icons.get_lucide_svg("circle-check", size=20, color="var(--status-success)")
    icon_trend = icons.get_lucide_svg("trending-up", size=20, color="var(--status-danger)")
    icon_calendar = icons.get_lucide_svg("calendar-days", size=20, color=gold_color)

    with col_s1:
        score_str = f"{score_val}%" if st.session_state.readiness_data else "—"
        cat_str = st.session_state.readiness_data.get("category", "Pending Assessment") if st.session_state.readiness_data else "Assessment Required"
        utils.safe_render_html(f"""
        <div class="metric-obsidian">
            <div class="metric-header">
                <span class="metric-icon-wrap">{icon_target}</span>
            </div>
            <div class="metric-value" style="color: {champagne_color};">{score_str}</div>
            <div class="metric-label">Career Readiness</div>
            <div class="metric-subtext">{cat_str}</div>
        </div>
        """)

    with col_s2:
        m_count = f"{matched_val} Skills" if st.session_state.readiness_data else "—"
        utils.safe_render_html(f"""
        <div class="metric-obsidian">
            <div class="metric-header">
                <span class="metric-icon-wrap">{icon_check}</span>
            </div>
            <div class="metric-value" style="color: var(--status-success);">{m_count}</div>
            <div class="metric-label">Skills Acquired</div>
            <div class="metric-subtext">Verified competencies</div>
        </div>
        """)

    with col_s3:
        gap_count = f"{missing_val} Skills" if st.session_state.readiness_data else "—"
        utils.safe_render_html(f"""
        <div class="metric-obsidian">
            <div class="metric-header">
                <span class="metric-icon-wrap">{icon_trend}</span>
            </div>
            <div class="metric-value" style="color: var(--status-danger);">{gap_count}</div>
            <div class="metric-label">Skills To Learn</div>
            <div class="metric-subtext">High priority gap targets</div>
        </div>
        """)

    with col_s4:
        prog_str = f"{completed_weeks} / 8 Wks" if st.session_state.analysis_result else "0 / 8 Wks"
        utils.safe_render_html(f"""
        <div class="metric-obsidian">
            <div class="metric-header">
                <span class="metric-icon-wrap">{icon_calendar}</span>
            </div>
            <div class="metric-value" style="color: {gold_color};">{prog_str}</div>
            <div class="metric-label">Learning Progress</div>
            <div class="metric-subtext">Milestones completed</div>
        </div>
        """)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Contextual Section based on whether analysis exists
    if st.session_state.analysis_result and st.session_state.student_profile:
        prof = st.session_state.student_profile
        analysis = st.session_state.analysis_result

        st.markdown(f"### Active Path: **{prof.get('target_role')}**")
        
        col_summary, col_actions = st.columns([3, 2])
        with col_summary:
            motivation_text = analysis.get("career_summary", {}).get(
                "motivational_message",
                "Every master was once a beginner. Consistency is the secret to engineering excellence."
            )
            sparkles_icon = icons.get_lucide_svg("sparkles", size=18, color=gold_color)
            utils.safe_render_html(f"""
            <div class="panel-obsidian">
                <div style="display: flex; gap: 0.75rem;">
                    <div>{sparkles_icon}</div>
                    <div style="font-size: 14.5px; color: var(--text-primary); line-height: 1.6;">
                        <b>Mentor's Advice:</b> {html.escape(motivation_text)}
                    </div>
                </div>
            </div>
            """)

            market_summary = analysis.get("career_summary", {}).get("market_demand_summary", "")
            if market_summary:
                st.caption(f"Industry Outlook: {market_summary}")

        with col_actions:
            utils.safe_render_html("""
            <div class="panel-obsidian">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 0.35rem; color: var(--text-primary);">Quick Actions</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); margin-bottom: 0.85rem;">Continue where you left off or export your materials.</div>
            </div>
            """)
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if st.button("View Full Roadmap", icon=":material/route:", use_container_width=True):
                    st.session_state.current_page = "Career Roadmap"
                    st.rerun()
            with col_a2:
                if st.button("View Gap Analysis", icon=":material/bar_chart:", use_container_width=True):
                    st.session_state.current_page = "Skill Gap Analysis"
                    st.rerun()

    else:
        # Platform Capabilities Showcase
        st.markdown("### Platform Capabilities")
        col_f1, col_f2, col_f3 = st.columns(3)

        icon_route_lg = icons.get_lucide_svg("route", size=26, color=gold_color)
        icon_chart_lg = icons.get_lucide_svg("chart-no-axes-combined", size=26, color=gold_color)
        icon_doc_lg = icons.get_lucide_svg("file-search", size=26, color=gold_color)

        with col_f1:
            utils.safe_render_html(f"""
            <div class="metric-obsidian" style="padding: 1.5rem 1.25rem;">
                <div style="margin-bottom: 0.75rem;">{icon_route_lg}</div>
                <div style="font-weight: 700; font-size: 1.1rem; font-family: var(--font-heading);">8-Week Dynamic Roadmap</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.5; margin-top: 0.5rem;">
                    Personalized week-by-week curriculum calibrated to your available study hours and current experience level.
                </div>
            </div>
            """)

        with col_f2:
            utils.safe_render_html(f"""
            <div class="metric-obsidian" style="padding: 1.5rem 1.25rem;">
                <div style="margin-bottom: 0.75rem;">{icon_chart_lg}</div>
                <div style="font-weight: 700; font-size: 1.1rem; font-family: var(--font-heading);">Skill Gap Diagnostic</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.5; margin-top: 0.5rem;">
                    Visual matrix benchmarking your skills against production requirements with priority labels and recommendations.
                </div>
            </div>
            """)

        with col_f3:
            utils.safe_render_html(f"""
            <div class="metric-obsidian" style="padding: 1.5rem 1.25rem;">
                <div style="margin-bottom: 0.75rem;">{icon_doc_lg}</div>
                <div style="font-weight: 700; font-size: 1.1rem; font-family: var(--font-heading);">AI Resume & ATS Optimizer</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.5; margin-top: 0.5rem;">
                    Upload your PDF resume to detect missing keywords, evaluate ATS match scores, and receive actionable improvements.
                </div>
            </div>
            """)


# ==============================================================================
# PAGE 2: CAREER ROADMAP
# ==============================================================================
elif st.session_state.current_page == "Career Roadmap":
    st.markdown("## Tailored Career Roadmap")
    st.markdown("Generate or refine your customized 8-week engineering progression plan.")

    # Form Container
    with st.expander("Configure Career Profile & Target Role", expanded=(st.session_state.analysis_result is None)):
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### Current Skills & Competencies")
            selected_skills = st.multiselect(
                "Select skills you currently know:",
                options=AVAILABLE_SKILLS,
                default=["Python", "SQL"] if not st.session_state.student_profile else st.session_state.student_profile.get("skills_list", []),
                help="Choose from the list or add custom skills below."
            )

            custom_skills_input = st.text_input(
                "Add other custom skills (comma separated):",
                placeholder="e.g. PyTorch, Rust, Apache Kafka, Polars",
                value="" if not st.session_state.student_profile else st.session_state.student_profile.get("custom_skills", "")
            )

        with col_right:
            st.markdown("#### Target Role & Availability")
            target_role_choice = st.selectbox(
                "Target Career Role:",
                options=TARGET_ROLES,
                index=0 if not st.session_state.student_profile else (
                    TARGET_ROLES.index(st.session_state.student_profile.get("target_role_choice", "Data Scientist"))
                    if st.session_state.student_profile.get("target_role_choice") in TARGET_ROLES else 0
                )
            )

            custom_role_text = ""
            if target_role_choice == "Custom Role...":
                custom_role_text = st.text_input(
                    "Enter your custom target role:",
                    placeholder="e.g. MLOps Platform Engineer, Autonomous Systems Specialist",
                    value="" if not st.session_state.student_profile else st.session_state.student_profile.get("custom_role", "")
                )

            c_time, c_exp = st.columns(2)
            with c_time:
                study_hours = st.selectbox(
                    "Weekly Study Availability:",
                    options=STUDY_AVAILABILITY,
                    index=1 if not st.session_state.student_profile else STUDY_AVAILABILITY.index(st.session_state.student_profile.get("study_hours", "5–10 hours"))
                )
            with c_exp:
                exp_level = st.selectbox(
                    "Experience Level:",
                    options=EXPERIENCE_LEVELS,
                    index=0 if not st.session_state.student_profile else EXPERIENCE_LEVELS.index(st.session_state.student_profile.get("experience_level", "Beginner"))
                )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("Generate My Career Roadmap", type="primary", icon=":material/auto_awesome:", use_container_width=True, key="btn_generate_roadmap_main")

    # Handle Analysis Submission
    if analyze_btn:
        is_valid, err_msg, combined_skills, resolved_role = utils.validate_user_inputs(
            selected_skills,
            custom_skills_input,
            target_role_choice,
            custom_role_text,
            study_hours,
            exp_level
        )

        if not is_valid:
            st.error(f"Validation Error: {err_msg}")
        else:
            effective_key = ai_engine.get_api_key()
            with st.spinner("Evaluating skill baseline and generating customized curriculum..."):
                try:
                    result = ai_engine.analyze_career_path(
                        current_skills=combined_skills,
                        target_role=resolved_role,
                        study_hours=study_hours,
                        experience_level=exp_level,
                        api_key=effective_key
                    )
                    readiness = utils.calculate_skill_readiness(result.get("skills_analysis", []))

                    st.session_state.analysis_result = result
                    st.session_state.readiness_data = readiness
                    st.session_state.student_profile = {
                        "skills_list": selected_skills,
                        "custom_skills": custom_skills_input,
                        "combined_skills": combined_skills,
                        "target_role_choice": target_role_choice,
                        "custom_role": custom_role_text,
                        "target_role": resolved_role,
                        "study_hours": study_hours,
                        "experience_level": exp_level
                    }
                    st.toast("Career roadmap generated successfully!", icon=":material/check_circle:")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error generating roadmap: {ex}")

    # Display Roadmap Content if Available
    if st.session_state.analysis_result and st.session_state.student_profile:
        analysis = st.session_state.analysis_result
        prof = st.session_state.student_profile

        # Timeline presentation
        st.markdown(f"### 8-Week Progression for **{prof.get('target_role')}**")
        st.caption(f"Calibrated for **{prof.get('study_hours')}** per week at **{prof.get('experience_level')}** level.")

        roadmap_generator.render_vertical_timeline(analysis.get("roadmap", []))

        # Export & Regeneration Actions
        st.markdown("---")
        col_down_pdf, col_down_csv = st.columns(2)
        with col_down_pdf:
            try:
                pdf_bytes = utils.generate_roadmap_pdf(
                    student_profile=prof,
                    skills_analysis=analysis.get("skills_analysis", []),
                    roadmap=analysis.get("roadmap", []),
                    projects=analysis.get("portfolio_projects", []),
                    readiness_data=st.session_state.readiness_data
                )
                safe_name = prof.get("target_role", "career").replace(" ", "_").lower()
                st.download_button(
                    label="Download Full Career Roadmap (PDF)",
                    data=pdf_bytes,
                    file_name=f"SkillSync_Roadmap_{safe_name}.pdf",
                    mime="application/pdf",
                    icon=":material/download:",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error preparing PDF: {e}")

        with col_down_csv:
            try:
                csv_bytes = utils.export_skill_gap_to_csv(analysis.get("skills_analysis", []))
                st.download_button(
                    label="Download Skill Gap Analysis (CSV)",
                    data=csv_bytes,
                    file_name="SkillSync_Skill_Gap.csv",
                    mime="text/csv",
                    icon=":material/download:",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error preparing CSV: {e}")

        # AI Custom Regeneration Expander
        with st.expander("Customize or Regenerate 8-Week Roadmap", expanded=False):
            st.markdown("Tailor your curriculum to emphasize specific tools or frameworks.")
            custom_regen_prompt = st.text_input(
                "Custom learning instructions:",
                placeholder="e.g. Focus more heavily on cloud infrastructure, Docker, and PostgreSQL optimization"
            )
            if st.button("Regenerate Roadmap with AI", key="btn_regen_roadmap_page", icon=":material/auto_awesome:"):
                effective_key = ai_engine.get_api_key()
                with st.spinner("Regenerating curriculum..."):
                    try:
                        new_roadmap = ai_engine.regenerate_roadmap_ai(
                            st.session_state.analysis_result,
                            custom_regen_prompt,
                            effective_key
                        )
                        st.session_state.analysis_result["roadmap"] = new_roadmap
                        st.toast("Roadmap successfully refreshed!", icon=":material/check_circle:")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to regenerate roadmap: {e}")
    else:
        st.info("Configure your profile above and click **Generate My Career Roadmap** to view your customized 8-week timeline.")


# ==============================================================================
# PAGE 3: SKILL GAP ANALYSIS
# ==============================================================================
elif st.session_state.current_page == "Skill Gap Analysis":
    st.markdown("## Skill Gap Analysis & Diagnostic Matrix")

    if st.session_state.analysis_result and st.session_state.readiness_data:
        readiness = st.session_state.readiness_data
        analysis = st.session_state.analysis_result
        prof = st.session_state.student_profile or {}

        st.markdown(f"#### Target Role: **{prof.get('target_role', 'Engineering Specialist')}**")

        # Top Analytics Row (Gauge + Donut + Category Bar)
        col_gauge, col_donut, col_bar = st.columns([1, 1, 1.2])

        with col_gauge:
            st.markdown("##### Overall Readiness")
            gauge_fig = roadmap_generator.create_readiness_gauge(
                readiness["score"],
                readiness["matched"],
                readiness["partial"],
                readiness["missing"],
                readiness["total"],
                theme=st.session_state.theme
            )
            st.plotly_chart(gauge_fig, use_container_width=True)
            st.caption(f"Status: **{readiness['category']}**")

        with col_donut:
            st.markdown("##### Skills Breakdown")
            donut_fig = roadmap_generator.create_skill_breakdown_donut(
                readiness["matched"],
                readiness["partial"],
                readiness["missing"],
                theme=st.session_state.theme
            )
            st.plotly_chart(donut_fig, use_container_width=True)

        with col_bar:
            st.markdown("##### Category Distribution")
            bar_fig = roadmap_generator.create_category_distribution_bar(
                analysis.get("skills_analysis", []),
                theme=st.session_state.theme
            )
            st.plotly_chart(bar_fig, use_container_width=True)

        st.markdown("---")

        # Native Structured Skill Comparison Table (Clean text badges)
        st.markdown("#### Required Skills vs. Your Current Status")
        st.caption(
            "Below is the comprehensive diagnostic matrix of core technologies needed for your target role. "
            "Status indicators: **Already Have**, **Needs Improvement**, **Need to Learn**."
        )

        roadmap_generator.render_skill_gap_table(analysis.get("skills_analysis", []))

    else:
        chart_icon_svg = icons.get_lucide_svg("chart-no-axes-combined", size=36, color="var(--gold-primary)")
        utils.safe_render_html(f"""
        <div class="hero-obsidian" style="text-align: center; padding: 3rem 2rem;">
            <div style="margin-bottom: 0.75rem;">{chart_icon_svg}</div>
            <div style="font-size: 1.35rem; font-weight: 700; font-family: var(--font-heading);">No Diagnostic Data Found</div>
            <div style="font-size: 14px; color: var(--text-secondary); max-width: 500px; margin: 0.5rem auto 1.5rem auto; line-height: 1.6;">
                Generate your personalized career analysis first to unlock interactive Plotly gauges, distribution charts, and the skill gap comparison matrix.
            </div>
        </div>
        """)
        if st.button("Go to Career Roadmap Setup", icon=":material/route:", use_container_width=True):
            st.session_state.current_page = "Career Roadmap"
            st.rerun()


# ==============================================================================
# PAGE 4: AI RESUME ANALYZER
# ==============================================================================
elif st.session_state.current_page == "Resume Analyzer":
    st.markdown("## AI Resume & ATS Keyword Analyzer")
    st.markdown("Evaluate your resume against Applicant Tracking Systems (ATS) and detect keyword gaps.")

    col_upload, col_jd = st.columns([1, 1])

    with col_upload:
        st.markdown("#### Upload Resume")
        uploaded_resume = st.file_uploader(
            "Upload your resume (PDF or TXT):",
            type=["pdf", "txt"],
            help="Your resume is parsed securely in-memory and never permanently stored."
        )

    with col_jd:
        st.markdown("#### Target Job Role & Description")
        default_role = st.session_state.student_profile.get("target_role", "Data Scientist") if st.session_state.student_profile else "Data Scientist"
        target_role_for_ats = st.selectbox(
            "Evaluate Against Role:",
            options=TARGET_ROLES[:-1],
            index=TARGET_ROLES[:-1].index(default_role) if default_role in TARGET_ROLES[:-1] else 0
        )
        custom_jd = st.text_area(
            "Target Job Description (Optional):",
            placeholder="Paste target job description to match exact keywords and recruiter requirements...",
            height=130
        )

    analyze_resume_btn = st.button("Analyze Resume with AI", type="primary", icon=":material/find_in_page:", use_container_width=True, key="btn_analyze_resume")

    if analyze_resume_btn:
        if uploaded_resume is None:
            st.warning("Please upload a PDF or TXT resume file first.")
        else:
            with st.spinner("Extracting text and benchmarking resume against ATS algorithms..."):
                extracted_text = utils.extract_text_from_pdf(uploaded_resume)
                if not extracted_text or len(extracted_text.strip()) < 30:
                    st.error("Could not extract readable text from the uploaded file. Please ensure it is not an image-only scanned PDF.")
                else:
                    effective_key = ai_engine.get_api_key()
                    ats_res = ai_engine.analyze_resume_ats(
                        resume_text=extracted_text,
                        job_description=custom_jd,
                        target_role=target_role_for_ats,
                        api_key=effective_key
                    )
                    st.session_state.resume_analysis = ats_res
                    st.toast("Resume analysis complete!", icon=":material/check_circle:")

    # Render ATS Results
    if st.session_state.resume_analysis:
        ats = st.session_state.resume_analysis
        st.markdown("---")
        st.markdown("### ATS Optimization Diagnostic")

        col_ats_gauge, col_ats_overview = st.columns([1, 2])

        with col_ats_gauge:
            score = ats.get("ats_score", 65)
            gauge_fig = roadmap_generator.create_ats_score_gauge(score, theme=st.session_state.theme)
            st.plotly_chart(gauge_fig, use_container_width=True)
            match_lvl = ats.get("match_level", "Moderate Match")
            st.caption(f"Compatibility: **{match_lvl}**")

        with col_ats_overview:
            st.markdown("##### ATS Assessment Summary")
            st.info(
                f"Your resume was evaluated against **{target_role_for_ats}** requirements. "
                "Adding quantified deliverables and closing keyword gaps will maximize your interview callback rate."
            )

        st.markdown("---")

        col_skills, col_gaps = st.columns(2)
        with col_skills:
            st.markdown("##### Matching Skills Detected")
            matching_tags = " ".join([f"`{s}`" for s in ats.get("matching_skills", [])])
            st.markdown(matching_tags if matching_tags else "`Foundational Skills`")

            st.markdown("##### Resume Strengths")
            for strength in ats.get("strengths", []):
                st.markdown(f"• **{strength}**")

        with col_gaps:
            st.markdown("##### Missing Industry Keywords")
            missing_tags = " ".join([f"`{s}`" for s in ats.get("missing_keywords", [])])
            st.markdown(missing_tags if missing_tags else "`None identified`")

            st.markdown("##### Areas for Improvement")
            for imp in ats.get("improvements", []):
                st.markdown(f"• {imp}")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### Actionable Next Steps")
        for rec in ats.get("actionable_recommendations", []):
            st.markdown(f"• {rec}")


# ==============================================================================
# PAGE 5: AI MOCK INTERVIEW
# ==============================================================================
elif st.session_state.current_page == "Mock Interview":
    st.markdown("## AI Mock Interview Preparation")
    st.markdown("Practice role-specific technical and behavioral questions with instant AI feedback.")

    col_int_role, col_int_cat, col_int_exp = st.columns([2, 2, 1])

    with col_int_role:
        default_role = st.session_state.student_profile.get("target_role", "Data Scientist") if st.session_state.student_profile else "Data Scientist"
        interview_role = st.selectbox(
            "Interview Target Role:",
            options=TARGET_ROLES[:-1],
            index=TARGET_ROLES[:-1].index(default_role) if default_role in TARGET_ROLES[:-1] else 0
        )

    with col_int_cat:
        interview_cat = st.selectbox(
            "Question Focus Area:",
            options=["Technical Architecture & Core Stack", "Practical Problem Solving & Algorithms", "System Design & Scalability", "Behavioral & Engineering Leadership"]
        )

    with col_int_exp:
        interview_exp = st.selectbox(
            "Seniority Level:",
            options=["Beginner", "Intermediate", "Advanced"]
        )

    if st.button("Generate Interview Questions", type="primary", icon=":material/record_voice_over:", use_container_width=True, key="btn_gen_interview"):
        effective_key = ai_engine.get_api_key()
        with st.spinner("Preparing realistic interview questions for your profile..."):
            questions = ai_engine.generate_mock_interview_questions(
                target_role=interview_role,
                experience_level=interview_exp,
                category=interview_cat,
                api_key=effective_key
            )
            st.session_state.mock_interview_questions = questions
            st.session_state.mock_interview_eval = None
            st.session_state.active_interview_idx = 0
            st.toast("Interview questions ready!", icon=":material/check_circle:")

    # Render Active Question & Answer Interface
    if st.session_state.mock_interview_questions:
        questions = st.session_state.mock_interview_questions
        st.markdown("---")

        q_idx = st.session_state.active_interview_idx
        q_item = questions[q_idx]

        st.info(f"**Question {q_idx + 1} of {len(questions)} • {q_item.get('category', 'Technical')}**\n\n### {q_item.get('question', '')}")

        # Candidate Answer Input Area
        candidate_answer = st.text_area(
            "Your Answer:",
            placeholder="Type your structured answer here. Include architectural considerations, trade-offs, and metrics where applicable...",
            height=160
        )

        col_sub_ans, col_next_q = st.columns([3, 1])
        with col_sub_ans:
            submit_ans_btn = st.button("Submit Answer for AI Evaluation", type="primary", icon=":material/send:", use_container_width=True, key="btn_submit_ans")
        with col_next_q:
            if st.button("Next Question", icon=":material/arrow_forward:", use_container_width=True, key="btn_next_q"):
                st.session_state.active_interview_idx = (q_idx + 1) % len(questions)
                st.session_state.mock_interview_eval = None
                st.rerun()

        if submit_ans_btn:
            if not candidate_answer or len(candidate_answer.strip()) < 10:
                st.warning("Please provide a detailed response before submitting.")
            else:
                effective_key = ai_engine.get_api_key()
                with st.spinner("Evaluating your response against senior engineering criteria..."):
                    eval_res = ai_engine.evaluate_interview_answer(
                        question=q_item.get("question", ""),
                        user_answer=candidate_answer,
                        target_role=interview_role,
                        experience_level=interview_exp,
                        api_key=effective_key
                    )
                    st.session_state.mock_interview_eval = eval_res
                    st.toast("Evaluation complete!", icon=":material/check_circle:")

        # Display Evaluation
        if st.session_state.mock_interview_eval:
            ev = st.session_state.mock_interview_eval
            score_10 = ev.get("score", 7)

            st.success(f"### AI Evaluation Report • Score: {score_10} / 10\n\n{ev.get('feedback', '')}")

            col_ev_s, col_ev_i = st.columns(2)
            with col_ev_s:
                st.markdown("##### Strengths")
                for s in ev.get("strengths", []):
                    st.markdown(f"• **{s}**")
            with col_ev_i:
                st.markdown("##### Improvement Opportunities")
                for imp in ev.get("improvement_areas", []):
                    st.markdown(f"• {imp}")

            st.markdown("##### Model Exemplary Answer")
            st.info(ev.get("model_answer", ""))


# ==============================================================================
# PAGE 6: PROJECT RECOMMENDATIONS
# ==============================================================================
elif st.session_state.current_page == "Project Recommendations":
    st.markdown("## Standout Portfolio Project Blueprints")
    st.markdown("Showcase graduated mastery with live interactive previews and production-ready source code.")

    # Determine projects to render
    projects = []
    if st.session_state.analysis_result:
        projects = st.session_state.analysis_result.get("portfolio_projects", [])
    else:
        default_curriculum = ai_engine.ROLE_CURRICULUM_DATA.get("Data Scientist", ai_engine.DEFAULT_CURRICULUM)
        raw_p = default_curriculum.get("projects", [])
        projects = [
            {
                "title": p[0],
                "difficulty": p[1],
                "short_description": p[2],
                "problem_solved": p[3],
                "technologies_required": p[4],
                "skills_demonstrated": [f"Mastery of {p[4][0]}" if p[4] else "Full Stack Architecture"],
                "estimated_completion_time": p[5],
                "expected_final_output": p[6]
            }
            for p in raw_p
        ]

    # Search and Filter
    col_search, col_diff = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("Search project titles or technologies:", placeholder="e.g. React, Docker, Machine Learning")
    with col_diff:
        diff_filter = st.selectbox("Difficulty Filter:", options=["All Levels", "Beginner", "Intermediate", "Advanced"])

    filtered_projects = []
    for p in projects:
        title = p.get("title", "")
        techs = " ".join(p.get("technologies_required", []))
        diff = p.get("difficulty", "Beginner")

        if diff_filter != "All Levels" and diff != diff_filter:
            continue
        if search_query and (search_query.lower() not in title.lower() and search_query.lower() not in techs.lower()):
            continue
        filtered_projects.append(p)

    if filtered_projects:
        roadmap_generator.render_portfolio_projects(filtered_projects)
    else:
        st.info("No projects match your search criteria. Clear your search or difficulty filter.")


# ==============================================================================
# PAGE 7: LEARNING RESOURCES
# ==============================================================================
elif st.session_state.current_page == "Learning Resources":
    st.markdown("## Curated Technical Learning Library")
    st.markdown("Hand-picked official documentation, interactive tutorials, and certification guides.")

    tab_web, tab_back, tab_data, tab_devops, tab_certs = st.tabs([
        "Frontend & Web",
        "Backend & Systems",
        "AI & Data Science",
        "Cloud & DevOps",
        "Top Free Certifications"
    ])

    with tab_web:
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            with st.container(border=True):
                st.markdown("#### [React 19 Official Documentation](https://react.dev)")
                st.caption("Official Guide • Advanced React")
                st.markdown("Master React Server Components, Suspense architecture, and custom hooks with interactive sandboxes.")
                st.link_button("Explore Documentation", "https://react.dev", icon=":material/open_in_new:", use_container_width=True)
        with col_w2:
            with st.container(border=True):
                st.markdown("#### [Web.dev Core Web Vitals](https://web.dev/explore/metrics)")
                st.caption("Google Developer Guide • Performance")
                st.markdown("In-depth techniques for optimizing Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and layout shifts.")
                st.link_button("View Guide", "https://web.dev/explore/metrics", icon=":material/open_in_new:", use_container_width=True)

    with tab_back:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            with st.container(border=True):
                st.markdown("#### [Use The Index, Luke!](https://use-the-index-luke.com/)")
                st.caption("Database Mastery • SQL Optimization")
                st.markdown("A definitive guide to database performance, composite B-Tree indexes, and relational query tuning.")
                st.link_button("Read Handbook", "https://use-the-index-luke.com/", icon=":material/open_in_new:", use_container_width=True)
        with col_b2:
            with st.container(border=True):
                st.markdown("#### [Designing Data-Intensive Applications](https://dataintensive.net/)")
                st.caption("Distributed Systems • Architecture")
                st.markdown("Fundamental principles for building reliable, scalable, and maintainable data systems and microservices.")
                st.link_button("Learn More", "https://dataintensive.net/", icon=":material/open_in_new:", use_container_width=True)

    with tab_data:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            with st.container(border=True):
                st.markdown("#### [Fast.ai Practical Deep Learning](https://course.fast.ai)")
                st.caption("Deep Learning • PyTorch")
                st.markdown("Hands-on course taking you from fundamentals to training state-of-the-art vision and language models.")
                st.link_button("Access Free Course", "https://course.fast.ai", icon=":material/open_in_new:", use_container_width=True)
        with col_d2:
            with st.container(border=True):
                st.markdown("#### [Google Gemini API Documentation](https://ai.google.dev/docs)")
                st.caption("GenAI • LLM Integration")
                st.markdown("Comprehensive guides for structured JSON outputs, multimodal reasoning, and embeddings.")
                st.link_button("View API Docs", "https://ai.google.dev/docs", icon=":material/open_in_new:", use_container_width=True)

    with tab_devops:
        col_dp1, col_dp2 = st.columns(2)
        with col_dp1:
            with st.container(border=True):
                st.markdown("#### [Docker Curriculum](https://docker-curriculum.com/)")
                st.caption("DevOps Basics • Containerization")
                st.markdown("Practical hands-on guide for containerizing full-stack applications and orchestrating multi-service setups.")
                st.link_button("Start Tutorial", "https://docker-curriculum.com/", icon=":material/open_in_new:", use_container_width=True)
        with col_dp2:
            with st.container(border=True):
                st.markdown("#### [Kubernetes Interactive Tutorials](https://kubernetes.io/docs/tutorials/)")
                st.caption("K8s • Cloud Native")
                st.markdown("Learn to deploy, scale, and update containerized applications directly in a live terminal sandbox.")
                st.link_button("Interactive Sandbox", "https://kubernetes.io/docs/tutorials/", icon=":material/open_in_new:", use_container_width=True)

    with tab_certs:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            with st.container(border=True):
                st.markdown("#### [freeCodeCamp Certifications](https://www.freecodecamp.org/learn)")
                st.caption("300-Hour Accredited Curriculums • 100% Free")
                st.markdown("Recognized credentials in Responsive Web Design, JavaScript Algorithms, Relational Databases, and Machine Learning.")
                st.link_button("Enroll Free", "https://www.freecodecamp.org/learn", icon=":material/open_in_new:", use_container_width=True)
        with col_c2:
            with st.container(border=True):
                st.markdown("#### [CS50x: Introduction to Computer Science](https://cs50.harvard.edu/x)")
                st.caption("Harvard University • edX")
                st.markdown("The world-renowned computer science course covering C, algorithms, memory, Python, SQL, and web development.")
                st.link_button("Audit Course", "https://cs50.harvard.edu/x", icon=":material/open_in_new:", use_container_width=True)


# ==============================================================================
# PAGE 8: SETTINGS & SYSTEM STATUS
# ==============================================================================
elif st.session_state.current_page == "Settings":
    st.markdown("## Settings & System Diagnostics")
    st.markdown("Review system architecture, configuration status, and session controls.")

    col_set1, col_set2 = st.columns(2)

    with col_set1:
        st.markdown("#### Centralized Engine Configuration")
        status = ai_engine.get_engine_status()
        st.markdown(f"**Engine Status:** `{status['label']}`")
        st.markdown(f"**Active Source:** `{status['source_type']}`")
        st.markdown(f"**Architecture:** `Streamlit Cloud + GenAI / Heuristic Fallback`")
        st.caption("API keys are centrally managed via server secrets and environment variables. Visitors never need to input keys.")

        # Developer Session Override (Optional)
        with st.expander("Developer Key Override (Optional)", expanded=False):
            dev_key = st.text_input(
                "Enter temporary session API Key:",
                type="password",
                placeholder="AIzaSy...",
                help="Applies only to your current session. Never printed or saved to disk."
            )
            if st.button("Apply Session Key", icon=":material/key:"):
                if dev_key:
                    st.session_state["dev_api_key"] = dev_key
                    st.toast("Temporary session key applied!", icon=":material/key:")
                    st.rerun()

    with col_set2:
        st.markdown("#### Technical Diagnostics")
        st.markdown(f"**Python Runtime:** `{sys.version.split()[0]}`")
        st.markdown(f"**Streamlit Engine:** `{st.__version__}`")
        st.markdown(f"**GenAI Available:** `{ai_engine.GENAI_AVAILABLE}`")
        st.markdown(f"**ReportLab Available:** `{utils.REPORTLAB_AVAILABLE}`")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### Data Management")
        if st.button("Reset Entire Application State", icon=":material/refresh:", use_container_width=True):
            st.session_state.clear()
            st.toast("Application state cleared.", icon=":material/refresh:")
            st.rerun()

# ==============================================================================
# GLOBAL FOOTER
# ==============================================================================
utils.safe_render_html("""
<div style="text-align: center; margin-top: 4.5rem; padding-top: 2rem; border-top: 1px solid var(--border-color); font-size: 13.5px; color: var(--text-secondary);">
    <b>SkillSync 2.0</b> — AI Career Intelligence Platform • Built with Google Gemini API, Streamlit, Plotly & Pandas<br/>
    Discover Your Skills. Bridge the Gap. Build Your Future.
</div>
""")

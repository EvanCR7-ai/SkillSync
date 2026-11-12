"""
SkillSync | CareerPath AI – Your Personal AI Career Mentor
A modern, responsive, AI-powered Streamlit SaaS application.
"""

import os
import base64
from pathlib import Path
from PIL import Image
import streamlit as st
from typing import List, Dict, Any

# Safely resolve project and assets directories using pathlib
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "skillsync-logo.png"

def load_logo_base64() -> str:
    """Safely loads and encodes the SkillSync logo using pathlib."""
    if LOGO_PATH.is_file():
        try:
            return base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
        except Exception:
            return ""
    return ""

LOGO_BASE64 = load_logo_base64()

# Internal modules
from ai_engine import (
    generate_career_analysis,
    regenerate_roadmap_ai,
    regenerate_projects_ai,
    get_gemini_api_key,
    mask_api_key
)
from roadmap_generator import (
    format_roadmap_for_display,
    calculate_roadmap_metrics,
    generate_roadmap_markdown_summary
)
from utils import (
    validate_user_inputs,
    generate_skills_csv,
    generate_pdf_roadmap,
    create_readiness_gauge,
    create_status_donut_chart,
    create_priority_distribution_chart,
    PRESET_ROLES,
    VALID_HOURS_OPTIONS,
    VALID_EXPERIENCE_LEVELS,
    HAS_PLOTLY
)

# Optional Pandas for table rendering if installed
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


# ==============================================================================
# Page Configuration & CSS Styling
# ==============================================================================

# Load favicon safely using pathlib
favicon = "🚀"
if LOGO_PATH.is_file():
    try:
        favicon = Image.open(LOGO_PATH)
    except Exception:
        favicon = "🚀"

st.set_page_config(
    page_title="SkillSync | CareerPath AI – AI Career Mentor",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load External CSS
def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()


# ==============================================================================
# Session State Initialization
# ==============================================================================

if "analysis_data" not in st.session_state:
    st.session_state["analysis_data"] = None

if "custom_skills_list" not in st.session_state:
    st.session_state["custom_skills_list"] = []

if "gemini_api_key_override" not in st.session_state:
    st.session_state["gemini_api_key_override"] = ""

if "last_role_queried" not in st.session_state:
    st.session_state["last_role_queried"] = ""


# Curated Popular Skills for the Multi-Select
POPULAR_SKILLS = [
    "Python", "JavaScript", "TypeScript", "SQL", "HTML/CSS", "React",
    "Node.js", "Docker", "Git & GitHub", "FastAPI", "Pandas", "PyTorch",
    "Machine Learning", "AWS", "Google Cloud", "Kubernetes", "Linux",
    "Data Analysis", "REST APIs", "PostgreSQL", "MongoDB", "Figma",
    "Tailwind CSS", "C++", "Java", "Go", "Next.js", "Data Visualization"
]


# ==============================================================================
# Sidebar Configuration & Brand Navigation
# ==============================================================================

with st.sidebar:
    # Sidebar Brand Logo (Replacing old text-based branding)
    if LOGO_BASE64:
        st.markdown(
            f'<div class="sidebar-logo-wrapper"><img src="data:image/png;base64,{LOGO_BASE64}" class="sidebar-logo-img" style="max-width: 210px; width: 100%; height: auto; object-fit: contain; display: block; margin: 0 auto;" alt="SkillSync Logo" /></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.2rem;">
    <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);">
        🚀
    </div>
    <div>
        <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">SkillSync</div>
        <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 500;">CareerPath AI Mentor</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # API Configuration Status
    active_key = get_gemini_api_key(st.session_state["gemini_api_key_override"])
    
    if active_key:
        st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 10px 14px; margin-bottom: 1rem;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #10b981; display: flex; align-items: center; gap: 6px;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
                    Gemini Live AI Active
                </div>
                <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 3px;">Key: <code>{mask_api_key(active_key)}</code></div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 10px 14px; margin-bottom: 1rem;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #f59e0b; display: flex; align-items: center; gap: 6px;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></span>
                    Mentor Reasoning Engine Active
                </div>
                <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 3px;">Add Gemini Key below or in .env for live LLM mode.</div>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("🔑 Configure Gemini API Key", expanded=False):
        user_entered_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state["gemini_api_key_override"],
            placeholder="AIzaSy...",
            help="Your key is kept strictly in session memory and never stored or logged."
        )
        if user_entered_key != st.session_state["gemini_api_key_override"]:
            st.session_state["gemini_api_key_override"] = user_entered_key
            st.rerun()

        st.markdown("""
            <p style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">
                Get a free key from <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color: #8b5cf6;">Google AI Studio</a>.
            </p>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Navigation / Reset
    if st.session_state["analysis_data"]:
        st.markdown(f"**Current Role:** `{st.session_state.get('last_role_queried', 'Analyzed')}`")
        if st.button("🔄 Reset Current Analysis", use_container_width=True):
            st.session_state["analysis_data"] = None
            st.session_state["last_role_queried"] = ""
            st.rerun()

    st.markdown("### 💡 Why SkillSync?")
    st.markdown("""
        - **Targeted Gap Diagnosis**: Stop guessing what recruiters look for.
        - **Personalized 8-Week Plan**: Skips what you know, targets what you need.
        - **Proof-of-Work Projects**: 3 GitHub-ready showcases that stand out.
    """)

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.75rem; color: #64748b; text-align: center;">
            SkillSync SaaS v2.5<br>
            Powered by Google Gemini AI
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# Hero Section with Centered Large Brand Logo
# ==============================================================================

logo_img_tag = (
    f'<div class="homepage-logo-wrapper"><img src="data:image/png;base64,{LOGO_BASE64}" class="homepage-main-logo" style="max-width: 480px; width: 100%; height: auto; object-fit: contain; display: block; margin: 0 auto 1.5rem auto;" alt="SkillSync Logo" /></div>'
    if LOGO_BASE64 else ""
)

hero_section_html = f"""<div class="hero-container">
{logo_img_tag}
<div class="hero-badge">✨ Next-Generation AI Career Acceleration</div>
<h1 class="hero-heading">Build Your Future with AI</h1>
<div class="hero-tagline">Your Skills Today. Your Dream Career Tomorrow.</div>
<p class="hero-subtitle">
Compare your current skillset against modern tech industry benchmarks. 
Receive a personalized skill-gap diagnostic, a tailored 8-week learning roadmap, 
and 3 production-grade GitHub portfolio projects.
</p>
</div>"""

st.markdown(hero_section_html, unsafe_allow_html=True)

# Feature Highlight Cards
st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon-wrapper">📊</div>
            <h3>Skill Gap Analysis</h3>
            <p>Mathematical assessment of your matched, partial, and missing competencies with actionable resources.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrapper">🗺️</div>
            <h3>8-Week Roadmap</h3>
            <p>Personalized week-by-week curriculum respecting your hours, skipping known skills, with a final Capstone.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrapper">💼</div>
            <h3>Portfolio Projects</h3>
            <p>Three realistic GitHub projects across beginner, intermediate, and advanced levels to prove your skills.</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# Interactive Assessment Input Form
# ==============================================================================

with st.container():
    st.markdown("""
        <div class="section-header">
            <h2>🎯 Start Your Skill Analysis</h2>
        </div>
    """, unsafe_allow_html=True)

    col_role, col_exp = st.columns([3, 2])
    with col_role:
        target_role_selection = st.selectbox(
            "Target Career Role",
            options=["Select a role..."] + PRESET_ROLES,
            index=0,
            help="Choose the technical job role you want to prepare for."
        )

        custom_role_name = ""
        if target_role_selection == "Other (Custom Role)":
            custom_role_name = st.text_input(
                "Enter Custom Job Title",
                placeholder="e.g. Prompt Engineer, Site Reliability Engineer, Mobile Developer"
            )

    with col_exp:
        experience_level = st.selectbox(
            "Current Experience Level",
            options=VALID_EXPERIENCE_LEVELS,
            index=0,
            help="Your current comfort and proficiency level in software and tech."
        )

    col_skills, col_hours = st.columns([3, 2])
    with col_skills:
        # Combine popular skills with any custom skills added in this session
        all_skill_options = sorted(list(set(POPULAR_SKILLS + st.session_state["custom_skills_list"])))
        selected_skills = st.multiselect(
            "Select Your Current Skills & Technologies",
            options=all_skill_options,
            default=["Python"] if "Python" in all_skill_options else [],
            help="Choose everything you have hands-on experience with."
        )

        # Custom skill text entry
        col_c_text, col_c_btn = st.columns([3, 1])
        with col_c_text:
            new_custom_skill = st.text_input(
                "Add Custom Skill (Not listed above)",
                placeholder="e.g. LangChain, Rust, Supabase",
                label_visibility="collapsed"
            )
        with col_c_btn:
            if st.button("➕ Add Skill", use_container_width=True):
                if new_custom_skill and new_custom_skill.strip():
                    cleaned_s = new_custom_skill.strip()
                    if cleaned_s not in st.session_state["custom_skills_list"]:
                        st.session_state["custom_skills_list"].append(cleaned_s)
                        st.rerun()

    with col_hours:
        weekly_study_hours = st.selectbox(
            "Weekly Study Commitment",
            options=VALID_HOURS_OPTIONS,
            index=2,  # Default 10–15
            format_func=lambda x: f"{x} hours / week",
            help="How many hours per week you can consistently dedicate to upskilling."
        )

    # Submit Button
    generate_btn = st.button("🚀 Create My Career Roadmap", use_container_width=True, type="primary")

    if generate_btn:
        # Validate inputs
        is_valid, err_msg, resolved_role = validate_user_inputs(
            selected_skills,
            target_role_selection,
            custom_role_name,
            weekly_study_hours,
            experience_level
        )

        if not is_valid:
            st.error(f"⚠️ {err_msg}")
        else:
            with st.spinner("🤖 SkillSync AI is analyzing competencies and architecting your career path..."):
                active_api_key = get_gemini_api_key(st.session_state["gemini_api_key_override"])
                analysis_result = generate_career_analysis(
                    current_skills=selected_skills,
                    target_role=resolved_role,
                    weekly_hours=weekly_study_hours,
                    experience_level=experience_level,
                    api_key=active_api_key
                )
                st.session_state["analysis_data"] = analysis_result
                st.session_state["last_role_queried"] = resolved_role
                st.session_state["selected_skills_cache"] = selected_skills
                st.session_state["weekly_hours_cache"] = weekly_study_hours
                st.session_state["experience_cache"] = experience_level
                st.toast("✅ Career Roadmap Successfully Generated!", icon="🎉")
                st.rerun()


# ==============================================================================
# Results Display Dashboard
# ==============================================================================

if st.session_state["analysis_data"]:
    data = st.session_state["analysis_data"]
    summary = data.get("readiness_summary", {})
    skills = data.get("skills_analysis", [])
    raw_roadmap = data.get("roadmap", [])
    projects = data.get("projects", [])

    formatted_roadmap = format_roadmap_for_display(raw_roadmap)
    roadmap_metrics = calculate_roadmap_metrics(formatted_roadmap, summary.get("weekly_hours", "10–15"))

    st.markdown("---")

    # ==========================================================================
    # Top Score & Metrics Bar
    # ==========================================================================
    st.markdown("""
        <div class="readiness-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #8b5cf6; text-transform: uppercase; letter-spacing: 0.05em;">Career Readiness Assessment</div>
                    <div style="font-size: 2rem; font-weight: 800; color: #ffffff;">{role}</div>
                    <div style="font-size: 0.95rem; color: #94a3b8; margin-top: 4px;">{verdict} • <b>{tier}</b></div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.8rem; font-weight: 800; color: #38bdf8; line-height: 1;">{score}%</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Mathematical Match Score</div>
                </div>
            </div>
        </div>
    """.format(
        role=summary.get("target_role", "Target Role"),
        verdict=summary.get("readiness_verdict", "Evaluation Complete"),
        tier=summary.get("tier", "Candidate"),
        score=summary.get("overall_fit_percentage", 0)
    ), unsafe_allow_html=True)

    # 4 Quick Metric Cards
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 14px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #10b981;">{summary.get('matched_count', 0)}</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-top: 4px;">Matched Skills</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Already in your toolbelt</div>
            </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 14px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #f59e0b;">{summary.get('partial_count', 0)}</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-top: 4px;">Partial Skills</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Needs practical depth</div>
            </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 14px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #ef4444;">{summary.get('missing_count', 0)}</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-top: 4px;">Missing Skills</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Roadmap focus areas</div>
            </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 14px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #818cf8;">~{roadmap_metrics['total_estimated_hours']} hrs</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-top: 4px;">Total Study Hours</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Over 8 structured weeks</div>
            </div>
        """, unsafe_allow_html=True)

    # Motivational Message Box
    if summary.get("motivational_message"):
        st.markdown(f"""
            <div class="motivational-box">
                <span style="font-size: 1.2rem; margin-right: 8px;">💡</span>
                <b>Mentor Insight:</b> "{summary.get('motivational_message')}"
            </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # Main Tabs: Skill Gap Analysis | 8-Week Roadmap | Portfolio Projects
    # ==========================================================================
    tab_skills, tab_roadmap, tab_projects = st.tabs([
        "📊 Skill Gap Analysis",
        "🗺️ 8-Week Personalized Roadmap",
        "💼 3 Portfolio Projects"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: Skill Gap Analysis
    # --------------------------------------------------------------------------
    with tab_skills:
        st.markdown("### 🔍 Detailed Skill Gap Breakdown")
        st.markdown("Compare each target competency required for this role against your current knowledge base.")

        # Plotly Charts Row
        if HAS_PLOTLY:
            c_chart1, c_chart2, c_chart3 = st.columns(3)
            with c_chart1:
                gauge = create_readiness_gauge(summary.get("overall_fit_percentage", 0), summary.get("readiness_verdict", ""))
                if gauge:
                    st.plotly_chart(gauge, use_container_width=True)
            with c_chart2:
                donut = create_status_donut_chart(summary.get("matched_count", 0), summary.get("partial_count", 0), summary.get("missing_count", 0))
                if donut:
                    st.plotly_chart(donut, use_container_width=True)
            with c_chart3:
                p_chart = create_priority_distribution_chart(skills)
                if p_chart:
                    st.plotly_chart(p_chart, use_container_width=True)

        # Search / Filter
        filter_col, csv_col = st.columns([3, 1])
        with filter_col:
            status_filter = st.selectbox(
                "Filter by Skill Status",
                options=["All Competencies", "Matched (Already Have)", "Partial (Bridge)", "Missing (Acquire)"],
                index=0
            )

        with csv_col:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            csv_data = generate_skills_csv(skills, summary.get("target_role", "Engineering"))
            st.download_button(
                label="📥 Download CSV Analysis",
                data=csv_data,
                file_name=f"SkillSync_Skill_Gap_{summary.get('target_role', 'Career')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Filtered skills list
        display_skills = skills
        if status_filter == "Matched (Already Have)":
            display_skills = [s for s in skills if s.get("status", "").lower() == "matched"]
        elif status_filter == "Partial (Bridge)":
            display_skills = [s for s in skills if s.get("status", "").lower() == "partial"]
        elif status_filter == "Missing (Acquire)":
            display_skills = [s for s in skills if s.get("status", "").lower() == "missing"]

        # ======================================================================
        # Skill Comparison Table (Required Skill, Current Status, Priority, Recommendation)
        # Green for already have, orange for partial, red for missing
        # ======================================================================
        table_rows_html = []
        for s in display_skills:
            status = s.get("status", "Missing")
            priority = s.get("priority", "Medium")
            s_name = s.get("skill_name", "Skill")
            category = s.get("category", "General")
            recommendation = s.get("recommendation", "")

            # Badge styling: Green for Already Have / Matched, Orange for Partial, Red for Missing
            if status.lower() == "matched":
                status_label = "Already Have"
                status_cls = "status-matched"
            elif status.lower() == "partial":
                status_label = "Partial"
                status_cls = "status-partial"
            else:
                status_label = "Missing"
                status_cls = "status-missing"

            p_badge_cls = f"badge-priority-{priority.lower()}"

            table_rows_html.append(f"""
                <tr>
                    <td style="font-weight: 700; color: #ffffff;">
                        {s_name}
                        <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 500; margin-top: 2px;">{category}</div>
                    </td>
                    <td><span class="badge-status {status_cls}">● {status_label}</span></td>
                    <td><span class="{p_badge_cls}">{priority}</span></td>
                    <td style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">{recommendation}</td>
                </tr>
            """)

        full_table_html = f"""
            <div class="skill-comparison-table-container">
                <table class="skill-comparison-table">
                    <thead>
                        <tr>
                            <th style="width: 26%;">Required Skill</th>
                            <th style="width: 18%;">Current Status</th>
                            <th style="width: 14%;">Priority</th>
                            <th style="width: 42%;">Recommendation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(table_rows_html)}
                    </tbody>
                </table>
            </div>
        """
        st.markdown(full_table_html, unsafe_allow_html=True)

        # Deep Dive Competency Cards & Practical Labs
        with st.expander("📚 View Interactive Learning Resources & Practice Labs", expanded=True):
            for s in display_skills:
                status = s.get("status", "Missing")
                priority = s.get("priority", "Medium")
                s_name = s.get("skill_name", "Skill")
                category = s.get("category", "General")
                resource = s.get("recommended_resource", "")
                exercise = s.get("practice_exercise", "")

                status_label = "Already Have" if status.lower() == "matched" else status
                status_cls = f"status-{status.lower()}"
                p_badge_cls = f"badge-priority-{priority.lower()}"

                st.markdown(f"""
                    <div style="background: rgba(19, 27, 46, 0.75); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.05rem; font-weight: 700; color: #ffffff;">{s_name} <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 400;">({category})</span></span>
                            <div>
                                <span class="badge-status {status_cls}">● {status_label}</span>
                                <span class="{p_badge_cls}">{priority} Priority</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.82rem; background: rgba(11, 15, 25, 0.5); padding: 8px 12px; border-radius: 8px;">
                            <div>
                                <span style="color: #38bdf8; font-weight: 600;">📚 Recommended Resource:</span>
                                <span style="color: #cbd5e1;"> {resource}</span>
                            </div>
                            <div>
                                <span style="color: #a855f7; font-weight: 600;">🛠️ Practical Exercise:</span>
                                <span style="color: #cbd5e1;"> {exercise}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 2: 8-Week Personalized Roadmap
    # --------------------------------------------------------------------------
    with tab_roadmap:
        st.markdown("### 🗺️ 8-Week Personalized Curriculum")
        st.markdown(
            f"Tailored for **{summary.get('target_role', 'Engineering')}** at **{summary.get('weekly_hours', '10–15')} hours/week**. "
            "Skills you have already matched are accelerated, while missing foundational gaps are prioritized."
        )

        col_regen_road, col_pdf = st.columns([1, 1])
        with col_regen_road:
            if st.button("🔄 Regenerate Roadmap Plan", use_container_width=True):
                with st.spinner("Re-architecting personalized 8-week curriculum..."):
                    active_api_key = get_gemini_api_key(st.session_state["gemini_api_key_override"])
                    new_roadmap = regenerate_roadmap_ai(
                        current_skills=st.session_state.get("selected_skills_cache", []),
                        target_role=summary.get("target_role", "Engineering"),
                        weekly_hours=summary.get("weekly_hours", "10–15"),
                        experience_level=summary.get("experience_level", "Beginner"),
                        api_key=active_api_key
                    )
                    st.session_state["analysis_data"]["roadmap"] = new_roadmap
                    st.toast("✅ Roadmap freshly regenerated!", icon="🚀")
                    st.rerun()

        with col_pdf:
            pdf_bytes = generate_pdf_roadmap(summary, skills, formatted_roadmap, projects)
            st.download_button(
                label="📄 Download Full Career PDF Report",
                data=pdf_bytes,
                file_name=f"SkillSync_Roadmap_{summary.get('target_role', 'Career')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Milestone Progress Indicator
        st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 12px; padding: 12px 18px; margin-bottom: 1.5rem; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div style="font-size: 0.8rem; color: #cbd5e1;"><b>Milestone 1 (W2):</b> Foundations & Core Tooling</div>
                <div style="font-size: 0.8rem; color: #cbd5e1;"><b>Milestone 2 (W4):</b> Architecture & Middleware</div>
                <div style="font-size: 0.8rem; color: #cbd5e1;"><b>Milestone 3 (W6):</b> Scalability & Pipelines</div>
                <div style="font-size: 0.8rem; color: #38bdf8;"><b>Milestone 4 (W8):</b> 🏆 Capstone Launch</div>
            </div>
        """, unsafe_allow_html=True)

        # Expandable Weekly Cards
        for w in formatted_roadmap:
            w_num = w["week_number"]
            topic = w["topic"]
            hours = w["estimated_hours"]
            is_cap = w["is_capstone"]

            cap_badge_html = '<span class="capstone-badge">🏆 Capstone Project Week</span>' if is_cap else ''
            
            expander_title = f"Week {w_num}: {topic} ({hours})"
            if is_cap:
                expander_title = f"🏆 Week {w_num}: {topic} [CAPSTONE]"

            with st.expander(expander_title, expanded=(w_num in [1, 8])):
                if is_cap:
                    st.markdown("""
                        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(236, 72, 153, 0.15)); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 10px; padding: 10px 14px; margin-bottom: 1rem;">
                            <b>🌟 Capstone Milestone:</b> This week synthesizes everything you've learned into a flagship, recruiter-facing portfolio project.
                        </div>
                    """, unsafe_allow_html=True)

                col_w_left, col_w_right = st.columns([1, 1])
                with col_w_left:
                    st.markdown("**🎯 Learning Objectives:**")
                    for obj in w["objectives"]:
                        st.markdown(f"- {obj}")

                    st.markdown("**🛠️ Practical Lab & Exercises:**")
                    for ex in w["exercises"]:
                        st.markdown(f"- {ex}")

                with col_w_right:
                    st.markdown("**📚 Recommended Study Resources:**")
                    for res in w["resources"]:
                        st.markdown(f"- {res}")

                    st.markdown(f"**🏁 Expected Outcome:** `{w['expected_outcome']}`")
                    
                    if w["focus_skills"]:
                        st.markdown("**Key Competencies Targeted:**")
                        tags_html = " ".join([f"<span class='skill-tag'>{sk}</span>" for sk in w["focus_skills"]])
                        st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 3: 3 GitHub Portfolio Projects
    # --------------------------------------------------------------------------
    with tab_projects:
        st.markdown("### 💼 GitHub Portfolio Mini-Projects")
        st.markdown(
            "Recruiters hire proof of work. Complete these **exactly 3 targeted projects** "
            "to demonstrate your capabilities from foundational code to enterprise architecture."
        )

        col_p_regen, _ = st.columns([1, 2])
        with col_p_regen:
            if st.button("🔄 Regenerate Project Ideas", use_container_width=True):
                with st.spinner("Generating fresh realistic portfolio project ideas..."):
                    active_api_key = get_gemini_api_key(st.session_state["gemini_api_key_override"])
                    new_projects = regenerate_projects_ai(
                        current_skills=st.session_state.get("selected_skills_cache", []),
                        target_role=summary.get("target_role", "Engineering"),
                        weekly_hours=summary.get("weekly_hours", "10–15"),
                        experience_level=summary.get("experience_level", "Beginner"),
                        api_key=active_api_key
                    )
                    st.session_state["analysis_data"]["projects"] = new_projects
                    st.toast("✅ Project ideas refreshed!", icon="💡")
                    st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        for p in projects:
            diff = p.get("difficulty", "Intermediate")
            title = p.get("title", "Portfolio Project")
            desc = p.get("description", "")
            prob = p.get("problem_solved", "")
            est_time = p.get("estimated_time", "20 hours")
            expected_out = p.get("expected_output", "")
            techs = p.get("technologies", [])
            skills_dem = p.get("skills_demonstrated", [])

            diff_cls = f"difficulty-{diff.lower()}"
            card_cls = f"project-card {diff.lower()}"

            tech_chips = "".join([f"<span class='tech-chip'>{t}</span>" for t in techs])
            skills_bullets = "".join([f"<li>{sd}</li>" for sd in skills_dem])

            st.markdown(f"""
                <div class="{card_cls}">
                    <div class="project-header">
                        <div>
                            <div class="project-title">{title}</div>
                            <div style="font-size: 0.85rem; color: #94a3b8;">Estimated Build Time: <b>{est_time}</b></div>
                        </div>
                        <span class="difficulty-pill {diff_cls}">{diff}</span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 0.8rem;">
                        {desc}
                    </p>
                    <div style="background: rgba(11, 15, 25, 0.6); border-radius: 10px; padding: 10px 14px; margin-bottom: 1rem; border-left: 3px solid #38bdf8;">
                        <span style="color: #38bdf8; font-weight: 700; font-size: 0.82rem; text-transform: uppercase;">Problem Solved:</span>
                        <div style="color: #f1f5f9; font-size: 0.88rem; margin-top: 2px;">{prob}</div>
                    </div>
                    <div style="margin-bottom: 0.8rem;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;">Tech Stack:</div>
                        <div>{tech_chips}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 1rem; font-size: 0.85rem;">
                        <div>
                            <b style="color: #cbd5e1;">Skills Demonstrated:</b>
                            <ul style="color: #94a3b8; margin: 4px 0 0 16px; padding: 0;">
                                {skills_bullets}
                            </ul>
                        </div>
                        <div>
                            <b style="color: #cbd5e1;">Expected Repository Output:</b>
                            <p style="color: #34d399; margin: 4px 0 0;">{expected_out}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

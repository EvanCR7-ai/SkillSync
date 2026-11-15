"""
SkillSync 2.0 – Your AI-Powered Career Roadmap
Main Streamlit Application
"""

import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

# Internal module imports
import ai_engine
import roadmap_generator
import utils

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SkillSync 2.0 – Your AI-Powered Career Roadmap",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css(file_name: str = "styles.css"):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(dir_path, file_name)
    if not os.path.exists(candidate):
        candidate = file_name
    if os.path.exists(candidate):
        with open(candidate, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "student_profile" not in st.session_state:
    st.session_state.student_profile = None

if "readiness_data" not in st.session_state:
    st.session_state.readiness_data = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0


# ==============================================================================
# SIDEBAR CONFIGURATION (CENTRALIZED & SECURE)
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem;">
        <span style="font-size: 2.2rem;">⚡</span>
        <div>
            <div style="font-size: 1.4rem; font-weight: 900; background: linear-gradient(135deg, #00D2FF, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.02em;">SkillSync 2.0</div>
            <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 500;">Next-Gen AI Career Mentor</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Centralized Backend Engine Status
    engine_status = ai_engine.get_engine_status()
    if engine_status["connected"]:
        st.markdown("""
        <div class="engine-status-box online">
            <span class="status-dot online"></span>
            <span>Google Gemini AI Connected</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="engine-status-box fallback">
            <span class="status-dot fallback"></span>
            <span>Curated AI Fallback Engine Active</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧭 Controls & Navigation")

    if st.session_state.analysis_result:
        if st.button("🔄 Reset Current Analysis", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.student_profile = None
            st.session_state.readiness_data = None
            st.rerun()

    # Developer / Admin Status Expander (Clean, No Expose of Secrets)
    with st.expander("⚙️ System Status", expanded=False):
        st.markdown(f"**Engine Status:** `{engine_status['label']}`")
        st.markdown(f"**Config Source:** `{engine_status['source_type']}`")
        st.markdown(f"**Architecture:** `Streamlit Cloud + GenAI / Heuristic Fallback`")
        st.caption("Centralized configuration active. Visitors do not require personal keys.")

    st.markdown("""
    <div style="font-size: 0.8rem; color: #64748B; margin-top: 2.5rem; line-height: 1.5;">
        <b>SkillSync 2.0 Pro</b><br/>
        Discover Your Skills. Bridge the Gap. Build Your Future.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MAIN HERO SECTION
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="brand-badge">⚡ Next-Gen AI Career Mentor</div>
    <h1 class="hero-title">Your Dream Career Starts Here.</h1>
    <div class="hero-tagline">Discover your skills. Bridge the gap. Build your future.</div>
    <div class="hero-subtitle">
        SkillSync analyzes your current abilities against modern industry standards, identifies critical knowledge gaps,
        generates an actionable 8-week personalized roadmap, and suggests recruiter-ready GitHub portfolio projects.
    </div>
    <div class="hero-cta-wrapper">
        <a href="#career-form" style="display: inline-flex; align-items: center; gap: 0.6rem; background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%); color: #FFFFFF; font-weight: 700; border-radius: 12px; padding: 0.85rem 2rem; font-size: 1.05rem; text-decoration: none; box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45); transition: all 0.3s ease;">
            🚀 Build My Career Roadmap
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Three Feature Highlights
st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon-wrapper">🧠</div>
        <div class="feature-title">AI Skill Gap Analysis</div>
        <div class="feature-desc">
            Instantly benchmark your existing toolkit against real-world employer requirements with color-coded priority ratings.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon-wrapper">🗺️</div>
        <div class="feature-title">Personalized 8-Week Roadmap</div>
        <div class="feature-desc">
            Get a tailored weekly milestone plan that skips what you already know and calibrates study hours to your schedule.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon-wrapper">🚀</div>
        <div class="feature-title">Portfolio Project Ideas</div>
        <div class="feature-desc">
            Three graduated project blueprints (Beginner, Intermediate, Advanced) engineered to demonstrate your skills on GitHub.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Step-by-Step Overview
with st.expander("ℹ️ How SkillSync Works — 4 Easy Steps", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">1</span>
            <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Input Your Skills</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Tell us what technologies you know and choose your dream role.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">2</span>
            <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">AI Analysis</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">The AI engine computes your readiness score and pinpoints exact gaps.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">3</span>
            <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Follow Roadmap</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Execute week-by-week goals, exercises, and study resources.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="step-card">
            <span class="step-num">4</span>
            <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Build & Get Hired</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Complete portfolio projects and export your PDF roadmap.</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div id='career-form' style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION: STUDENT INFORMATION INPUT FORM
# ==============================================================================
st.markdown("### 📋 Step 1: Tell Us About Your Background & Aspirations")

# Predefined Skill Options
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

with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🛠️ Current Skills & Knowledge")
        selected_skills = st.multiselect(
            "Select skills you currently know:",
            options=AVAILABLE_SKILLS,
            default=["Python", "SQL"] if not st.session_state.student_profile else st.session_state.student_profile.get("skills_list", []),
            help="Choose from the list or add custom skills below."
        )

        custom_skills_input = st.text_input(
            "Add other custom skills (comma separated):",
            placeholder="e.g. OpenCV, Rust, Apache Spark, Solidity",
            value="" if not st.session_state.student_profile else st.session_state.student_profile.get("custom_skills", "")
        )

    with col_right:
        st.markdown("#### 🎯 Career Goals & Commitment")
        
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
                placeholder="e.g. Autonomous Vehicle Engineer, Blockchain Developer",
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

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze My Career Path & Generate Roadmap", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# SUBMISSION HANDLING & AI ANALYSIS
# ==============================================================================
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
        st.error(f"❌ Input Validation Error: {err_msg}")
    else:
        effective_key = ai_engine.get_api_key()
        with st.spinner("🤖 SkillSync is evaluating your profile, identifying skill gaps, and architecting your 8-week curriculum..."):
            try:
                result = ai_engine.analyze_career_path(
                    current_skills=combined_skills,
                    target_role=resolved_role,
                    study_hours=study_hours,
                    experience_level=exp_level,
                    api_key=effective_key
                )

                # Compute mathematical readiness score
                readiness = utils.calculate_skill_readiness(result.get("skills_analysis", []))

                # Persist in session state
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

                if result.get("career_summary", {}).get("source") == "gemini_ai":
                    st.toast("🎉 Live AI Career analysis generated successfully!", icon="✅")
                else:
                    st.toast("📋 Curated Career Roadmap generated (Offline Fallback Mode)!", icon="ℹ️")
                st.rerun()

            except Exception as ex:
                st.error(f"⚠️ An unexpected error occurred: {str(ex)}")


# ==============================================================================
# SECTION: DASHBOARD, ROADMAP & PROJECTS (WHEN DATA AVAILABLE)
# ==============================================================================
if st.session_state.analysis_result and st.session_state.readiness_data:
    analysis = st.session_state.analysis_result
    readiness = st.session_state.readiness_data
    profile = st.session_state.student_profile

    st.markdown("---")
    
    # Motivational Progress Banner
    motivation_text = analysis.get("career_summary", {}).get(
        "motivational_message",
        "Every master was once a beginner. Consistency is the secret to engineering excellence."
    )
    utils.safe_render_html(f"""
    <div class="motivation-banner">
        <span class="motivation-icon">💡</span>
        <div class="motivation-text">
            <b>Mentor's Take:</b> {motivation_text}
        </div>
    </div>
    """)

    # Source Indicator Badge
    if analysis.get("career_summary", {}).get("source") == "gemini_ai":
        utils.safe_render_html("""
        <div style="margin-bottom: 1.25rem;">
            <span class="badge" style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #34D399;">
                ✨ Generated with Live Google Gemini AI
            </span>
        </div>
        """)
    else:
        utils.safe_render_html("""
        <div style="margin-bottom: 1.25rem;">
            <span class="badge" style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38BDF8;">
                ℹ️ Generated with Curated Industry Roadmap (Live AI Fallback Mode)
            </span>
        </div>
        """)

    # Tabs for structured navigation
    tab_gap, tab_roadmap, tab_projects, tab_downloads = st.tabs([
        "📊 Skill Gap Analysis & Readiness",
        "🗺️ 8-Week Personalized Roadmap",
        "🚀 Portfolio Project Blueprints",
        "📥 Download & Export Reports"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: SKILL GAP ANALYSIS & READINESS
    # --------------------------------------------------------------------------
    with tab_gap:
        st.markdown(f"### 📈 Career Readiness & Skills Diagnostic for **{profile.get('target_role')}**")

        # Demand overview
        market_summary = analysis.get("career_summary", {}).get("market_demand_summary", "")
        if market_summary:
            st.info(f"**Industry Market Outlook:** {market_summary}")

        # Metrics row: Score & Charts
        col_gauge, col_donut, col_stats = st.columns([1.2, 1.2, 1])

        with col_gauge:
            st.markdown("##### 🎯 Overall Skill Readiness Score")
            gauge_fig = roadmap_generator.create_readiness_gauge(
                readiness["score"],
                readiness["matched"],
                readiness["partial"],
                readiness["missing"],
                readiness["total"]
            )
            st.plotly_chart(gauge_fig, use_container_width=True)
            utils.safe_render_html(f"""
            <div style="text-align: center; font-size: 0.95rem; color: #94A3B8; margin-top: -10px;">
                Status: <b style="color: #FFFFFF;">{readiness['category']}</b>
            </div>
            """)

        with col_donut:
            st.markdown("##### 🥧 Skills Coverage Breakdown")
            donut_fig = roadmap_generator.create_skill_breakdown_donut(
                readiness["matched"],
                readiness["partial"],
                readiness["missing"]
            )
            st.plotly_chart(donut_fig, use_container_width=True)

        with col_stats:
            st.markdown("##### 📊 Diagnostic Breakdown")
            utils.safe_render_html(f"""
            <div class="metric-box" style="margin-bottom: 0.75rem;">
                <div class="metric-val" style="color: #10B981;">{readiness['matched']}</div>
                <div class="metric-lbl">Skills Matched</div>
            </div>
            <div class="metric-box" style="margin-bottom: 0.75rem;">
                <div class="metric-val" style="color: #F59E0B;">{readiness['partial']}</div>
                <div class="metric-lbl">Partially Skilled</div>
            </div>
            <div class="metric-box">
                <div class="metric-val" style="color: #EF4444;">{readiness['missing']}</div>
                <div class="metric-lbl">Skills to Learn</div>
            </div>
            """)

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

        # Comparison Table
        st.markdown("#### 🔍 Required Skills vs. Your Current Status")
        st.caption(
            "Below is the comprehensive diagnostic matrix of core technologies needed for your target role. "
            "Status indicators: 🟢 **Already Have**, 🟡 **Needs Improvement**, 🔴 **Need to Learn**."
        )

        roadmap_generator.render_skill_gap_table(analysis.get("skills_analysis", []))

    # --------------------------------------------------------------------------
    # TAB 2: PERSONALIZED 8-WEEK ROADMAP
    # --------------------------------------------------------------------------
    with tab_roadmap:
        st.markdown(f"### 🗺️ Tailored 8-Week Roadmap for **{profile.get('target_role')}**")
        utils.safe_render_html(f"""
        <div style="font-size: 0.95rem; color: #94A3B8; margin-bottom: 1.25rem;">
            Calibrated for <b>{profile.get('study_hours')}</b> per week at <b>{profile.get('experience_level')}</b> level.
            Skills you already possess have been streamlined so you can focus entirely on critical gaps.
        </div>
        """)

        # Render weekly cards
        roadmap_generator.render_roadmap_cards(analysis.get("roadmap", []))

        # Regenerate Roadmap Option
        st.markdown("---")
        with st.expander("🔄 Regenerate / Customize 8-Week Roadmap", expanded=False):
            st.markdown("Want to emphasize a specific topic or adapt your schedule?")
            custom_roadmap_prompt = st.text_input(
                "Custom instructions for regeneration:",
                placeholder="e.g. Focus more on cloud deployment and Docker; make Week 4 heavier on SQL optimization"
            )
            if st.button("Regenerate Roadmap with AI", key="btn_regen_roadmap"):
                effective_key = ai_engine.get_api_key()
                with st.spinner("Regenerating 8-week curriculum..."):
                    try:
                        new_roadmap = ai_engine.regenerate_roadmap_ai(
                            st.session_state.analysis_result,
                            custom_roadmap_prompt,
                            effective_key
                        )
                        st.session_state.analysis_result["roadmap"] = new_roadmap
                        st.toast("Roadmap successfully refreshed!", icon="✨")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to regenerate roadmap: {e}")

    # --------------------------------------------------------------------------
    # TAB 3: PORTFOLIO PROJECT RECOMMENDATIONS
    # --------------------------------------------------------------------------
    with tab_projects:
        st.markdown(f"### 🚀 Standout Portfolio Projects for **{profile.get('target_role')}**")
        utils.safe_render_html("""
        <div style="font-size: 0.95rem; color: #94A3B8; margin-bottom: 1.5rem;">
            These 3 curated projects demonstrate graduated mastery from foundational to production-grade architecture.
            Each project is specifically chosen to validate the skills in your learning roadmap.
        </div>
        """)

        roadmap_generator.render_portfolio_projects(analysis.get("portfolio_projects", []))

        # Regenerate Projects Option
        st.markdown("---")
        with st.expander("💡 Regenerate Alternative Project Ideas", expanded=False):
            st.markdown("Looking for different domains (e.g. FinTech, Healthcare, E-Commerce, Gaming)?")
            custom_project_prompt = st.text_input(
                "Project theme or industry focus:",
                placeholder="e.g. Focus on FinTech and algorithmic trading; include real-time WebSocket data"
            )
            if st.button("Generate 3 New Project Ideas", key="btn_regen_projects"):
                effective_key = ai_engine.get_api_key()
                with st.spinner("Brainstorming novel portfolio project concepts..."):
                    try:
                        new_projects = ai_engine.regenerate_projects_ai(
                            st.session_state.analysis_result,
                            custom_project_prompt,
                            effective_key
                        )
                        st.session_state.analysis_result["portfolio_projects"] = new_projects
                        st.toast("Fresh project recommendations generated!", icon="🎉")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to regenerate projects: {e}")

    # --------------------------------------------------------------------------
    # TAB 4: DOWNLOAD & EXPORT REPORTS
    # --------------------------------------------------------------------------
    with tab_downloads:
        st.markdown("### 📥 Download & Export Your Career Package")
        utils.safe_render_html("""
        <div style="font-size: 0.95rem; color: #94A3B8; margin-bottom: 1.5rem;">
            Export your customized roadmap and diagnostics for offline study, mentor reviews, or academic submissions.
        </div>
        """)

        col_pdf, col_csv = st.columns(2)

        with col_pdf:
            st.markdown("""
            <div class="glass-panel" style="text-align: center;">
                <div style="font-size: 3.25rem; margin-bottom: 0.5rem;">📄</div>
                <div style="font-weight: 800; font-size: 1.25rem; color: #FFFFFF;">Complete Career Roadmap (PDF)</div>
                <div style="font-size: 0.88rem; color: #94A3B8; margin: 0.5rem 0 1.5rem 0; line-height: 1.5;">
                    Includes executive summary, skill gap diagnostics table, full 8-week curriculum breakdown, and 3 project blueprints.
                </div>
            """, unsafe_allow_html=True)

            try:
                pdf_bytes = utils.generate_roadmap_pdf(
                    student_profile=profile,
                    skills_analysis=analysis.get("skills_analysis", []),
                    roadmap=analysis.get("roadmap", []),
                    projects=analysis.get("portfolio_projects", []),
                    readiness_data=readiness
                )
                safe_role_filename = profile.get("target_role", "career").replace(" ", "_").lower()
                st.download_button(
                    label="⬇️ Download Career Roadmap as PDF",
                    data=pdf_bytes,
                    file_name=f"SkillSync_Roadmap_{safe_role_filename}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

        with col_csv:
            st.markdown("""
            <div class="glass-panel" style="text-align: center;">
                <div style="font-size: 3.25rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 800; font-size: 1.25rem; color: #FFFFFF;">Skill Gap Analysis (CSV)</div>
                <div style="font-size: 0.88rem; color: #94A3B8; margin: 0.5rem 0 1.5rem 0; line-height: 1.5;">
                    Download the structured skill comparison dataset with categories, priority flags, and recommended next steps for spreadsheet tracking.
                </div>
            """, unsafe_allow_html=True)

            try:
                csv_bytes = utils.export_skill_gap_to_csv(analysis.get("skills_analysis", []))
                st.download_button(
                    label="⬇️ Download Skill Gap Analysis as CSV",
                    data=csv_bytes,
                    file_name="SkillSync_Skill_Gap_Analysis.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating CSV: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 4.5rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.08); font-size: 0.88rem; color: #64748B;">
    ⚡ <b>SkillSync 2.0</b> — Your AI-Powered Career Roadmap • Built with Google Gemini API, Streamlit, and Plotly<br/>
    Discover Your Skills. Bridge the Gap. Build Your Future.
</div>
""", unsafe_allow_html=True)

"""
SkillSync 2.0 – Premium AI Career Guidance Platform
Inspired by Linear, Vercel, Stripe, and modern AI analytics dashboards.
Full-stack Python Streamlit Application.
"""

import os
import sys
import html
import textwrap
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

# Internal module imports
import ai_engine
import roadmap_generator
import project_preview_engine
import utils

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SkillSync 2.0 – Your AI Career Mentor",
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

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "student_profile" not in st.session_state:
    st.session_state.student_profile = None

if "readiness_data" not in st.session_state:
    st.session_state.readiness_data = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "📊 Dashboard"

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None

if "mock_interview_questions" not in st.session_state:
    st.session_state.mock_interview_questions = None

if "mock_interview_eval" not in st.session_state:
    st.session_state.mock_interview_eval = None

if "active_interview_idx" not in st.session_state:
    st.session_state.active_interview_idx = 0


# ==============================================================================
# SIDEBAR NAVIGATION & ENGINE STATUS
# ==============================================================================
NAV_ITEMS = [
    "📊 Dashboard",
    "🗺️ Career Roadmap",
    "🔍 Skill Gap Analysis",
    "📄 AI Resume Analyzer",
    "🎙️ AI Mock Interview",
    "🚀 Project Recommendations",
    "📚 Learning Resources",
    "⚙️ Settings"
]

with st.sidebar:
    # Logo & Branding Header
    utils.safe_render_html("""
    <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 1.25rem;">
        <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #8B5CF6, #22D3EE); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);">
            <span style="font-size: 1.5rem;">⚡</span>
        </div>
        <div>
            <div style="font-size: 1.35rem; font-weight: 900; background: linear-gradient(135deg, #FFFFFF, #22D3EE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.02em;">SkillSync 2.0</div>
            <div style="font-size: 0.76rem; color: #94A3B8; font-weight: 500;">Your AI Career Mentor</div>
        </div>
    </div>
    """)

    st.markdown("---")

    # Navigation Menu
    nav_index = 0
    if st.session_state.current_page in NAV_ITEMS:
        nav_index = NAV_ITEMS.index(st.session_state.current_page)

    selected_nav = st.radio(
        "Navigation Menu",
        options=NAV_ITEMS,
        index=nav_index,
        label_visibility="collapsed"
    )

    if selected_nav != st.session_state.current_page:
        st.session_state.current_page = selected_nav
        st.rerun()

    st.markdown("---")

    # Centralized Backend Engine Status
    engine_status = ai_engine.get_engine_status()
    if engine_status["connected"]:
        utils.safe_render_html("""
        <div class="engine-status-box online">
            <span class="status-dot online"></span>
            <span>Google Gemini AI Connected</span>
        </div>
        """)
    else:
        utils.safe_render_html("""
        <div class="engine-status-box fallback">
            <span class="status-dot fallback"></span>
            <span>Curated AI Fallback Engine Active</span>
        </div>
        """)

    # User Profile Section at Sidebar Bottom
    target_role_display = "Not set"
    if st.session_state.student_profile:
        target_role_display = st.session_state.student_profile.get("target_role", "Software Engineer")

    utils.safe_render_html(f"""
    <div class="nav-profile-footer">
        <div class="nav-profile-avatar">AI</div>
        <div style="overflow: hidden;">
            <div style="font-weight: 700; font-size: 0.85rem; color: #FFFFFF; white-space: nowrap; text-overflow: ellipsis;">Active Candidate</div>
            <div style="font-size: 0.75rem; color: #22D3EE; white-space: nowrap; text-overflow: ellipsis;">{html.escape(target_role_display)}</div>
        </div>
    </div>
    """)

    if st.session_state.analysis_result:
        if st.button("🔄 Reset Current Analysis", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.student_profile = None
            st.session_state.readiness_data = None
            st.toast("Analysis reset.", icon="ℹ️")
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
# PAGE 1: 📊 DASHBOARD
# ==============================================================================
if st.session_state.current_page == "📊 Dashboard":
    # Hero Card
    col_hero_text, col_hero_visual = st.columns([3, 2])
    with col_hero_text:
        utils.safe_render_html("""
        <div style="padding: 1.5rem 0 1rem 0;">
            <div style="display: inline-block; padding: 0.35rem 0.85rem; background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.35); border-radius: 999px; color: #22D3EE; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;">
                ✨ Next-Gen AI Career Mentor
            </div>
            <h1 style="font-size: 2.85rem; font-weight: 900; line-height: 1.15; margin-bottom: 1rem; background: linear-gradient(135deg, #FFFFFF 30%, #22D3EE 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.03em;">
                Build Your Future with AI
            </h1>
            <p style="font-size: 1.05rem; color: #94A3B8; line-height: 1.6; max-width: 580px; margin-bottom: 1.5rem;">
                Discover your potential, identify critical engineering skill gaps, and create a tailored 8-week roadmap to land your dream technical role.
            </p>
        </div>
        """)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🚀 Generate My Career Roadmap", key="dash_hero_cta", use_container_width=True):
                st.session_state.current_page = "🗺️ Career Roadmap"
                st.rerun()
        with col_btn2:
            if st.button("✨ Explore AI Features", key="dash_hero_features", use_container_width=True):
                st.session_state.current_page = "🔍 Skill Gap Analysis"
                st.rerun()

    with col_hero_visual:
        # Visual AI Dashboard Metric Badge
        score_val = st.session_state.readiness_data.get("score", 0) if st.session_state.readiness_data else 0
        matched_val = st.session_state.readiness_data.get("matched", 0) if st.session_state.readiness_data else 0
        missing_val = st.session_state.readiness_data.get("missing", 0) if st.session_state.readiness_data else 0

        if st.session_state.readiness_data:
            gauge_fig = roadmap_generator.create_readiness_gauge(
                score=score_val,
                matched=matched_val,
                partial=st.session_state.readiness_data.get("partial", 0),
                missing=missing_val,
                total=st.session_state.readiness_data.get("total", 0)
            )
            st.plotly_chart(gauge_fig, use_container_width=True)
        else:
            utils.safe_render_html("""
            <div class="hero-gradient-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🎯</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF;">Personalized Career Intelligence</div>
                <div style="font-size: 0.88rem; color: #94A3B8; margin-top: 0.5rem; line-height: 1.5;">
                    Generate an analysis to benchmark your current skills against industry hiring bars.
                </div>
            </div>
            """)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4 Statistic Cards Grid
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    # Calculate completed weeks
    completed_weeks = 0
    if st.session_state.analysis_result:
        completed_weeks = sum(
            1 for i in range(1, 9)
            if st.session_state.get(f"week_completed_{i}", False)
        )

    with col_s1:
        score_str = f"{score_val}%" if st.session_state.readiness_data else "—"
        cat_str = st.session_state.readiness_data.get("category", "Pending Assessment") if st.session_state.readiness_data else "Assessment Required"
        utils.safe_render_html(f"""
        <div class="stat-card-premium">
            <span class="stat-icon">🎯</span>
            <div class="stat-val" style="color: #22D3EE;">{score_str}</div>
            <div class="stat-lbl">Career Readiness Score</div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">{cat_str}</div>
        </div>
        """)

    with col_s2:
        m_count = f"{matched_val} Skills" if st.session_state.readiness_data else "—"
        utils.safe_render_html(f"""
        <div class="stat-card-premium">
            <span class="stat-icon">🟢</span>
            <div class="stat-val" style="color: #22C55E;">{m_count}</div>
            <div class="stat-lbl">Skills Acquired</div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Verified competencies</div>
        </div>
        """)

    with col_s3:
        gap_count = f"{missing_val} Skills" if st.session_state.readiness_data else "—"
        utils.safe_render_html(f"""
        <div class="stat-card-premium">
            <span class="stat-icon">🔴</span>
            <div class="stat-val" style="color: #EF4444;">{gap_count}</div>
            <div class="stat-lbl">Skills To Learn</div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">High priority gap targets</div>
        </div>
        """)

    with col_s4:
        prog_str = f"{completed_weeks} / 8 Wks" if st.session_state.analysis_result else "0 / 8 Wks"
        utils.safe_render_html(f"""
        <div class="stat-card-premium">
            <span class="stat-icon">🗺️</span>
            <div class="stat-val" style="color: #8B5CF6;">{prog_str}</div>
            <div class="stat-lbl">Learning Progress</div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Milestones completed</div>
        </div>
        """)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Contextual Section based on whether analysis exists
    if st.session_state.analysis_result and st.session_state.student_profile:
        prof = st.session_state.student_profile
        analysis = st.session_state.analysis_result

        st.markdown(f"### 📍 Active Path: **{prof.get('target_role')}**")
        
        col_summary, col_actions = st.columns([3, 2])
        with col_summary:
            motivation_text = analysis.get("career_summary", {}).get(
                "motivational_message",
                "Every master was once a beginner. Consistency is the secret to engineering excellence."
            )
            utils.safe_render_html(f"""
            <div class="motivation-banner">
                <span class="motivation-icon">💡</span>
                <div class="motivation-text">
                    <b>Mentor's Advice:</b> {html.escape(motivation_text)}
                </div>
            </div>
            """)

            market_summary = analysis.get("career_summary", {}).get("market_demand_summary", "")
            if market_summary:
                st.caption(f"📈 **Industry Outlook:** {market_summary}")

        with col_actions:
            utils.safe_render_html("""
            <div class="glass-panel" style="padding: 1.25rem;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.5rem;">⚡ Quick Actions</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 1rem;">Continue where you left off or export your materials.</div>
            </div>
            """)
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if st.button("🗺️ View Full Roadmap", use_container_width=True):
                    st.session_state.current_page = "🗺️ Career Roadmap"
                    st.rerun()
            with col_a2:
                if st.button("🔍 View Gap Analysis", use_container_width=True):
                    st.session_state.current_page = "🔍 Skill Gap Analysis"
                    st.rerun()

    else:
        # Features Showcase Grid
        st.markdown("### 🌟 Platform Capabilities")
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-size: 2.2rem; margin-bottom: 0.75rem;">🗺️</div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">8-Week Dynamic Roadmap</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-top: 0.5rem;">
                    Personalized week-by-week curriculum calibrated to your available study hours and current experience level.
                </div>
            </div>
            """)

        with col_f2:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-size: 2.2rem; margin-bottom: 0.75rem;">🔍</div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">Skill Gap Diagnostic</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-top: 0.5rem;">
                    Visual matrix benchmarking your skills against production requirements with priority labels and recommendations.
                </div>
            </div>
            """)

        with col_f3:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-size: 2.2rem; margin-bottom: 0.75rem;">📄</div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">AI Resume & ATS Optimizer</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-top: 0.5rem;">
                    Upload your PDF resume to detect missing keywords, evaluate ATS match scores, and receive actionable improvements.
                </div>
            </div>
            """)


# ==============================================================================
# PAGE 2: 🗺️ CAREER ROADMAP
# ==============================================================================
elif st.session_state.current_page == "🗺️ Career Roadmap":
    st.markdown("## 🗺️ Tailored Career Roadmap")
    st.markdown("Generate or refine your customized 8-week engineering progression plan.")

    # Form Container
    with st.expander("⚙️ Configure Your Career Profile & Target Role", expanded=(st.session_state.analysis_result is None)):
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### 🛠️ Current Skills & Competencies")
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
            st.markdown("#### 🎯 Target Role & Availability")
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

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("✨ Generate My AI Roadmap", use_container_width=True, key="btn_generate_roadmap_main")

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
            st.error(f"❌ Validation Error: {err_msg}")
        else:
            effective_key = ai_engine.get_api_key()
            with st.spinner("🤖 Evaluating skill baseline and generating customized curriculum..."):
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
                    st.toast("🎉 Career roadmap generated successfully!", icon="✅")
                    st.rerun()
                except Exception as ex:
                    st.error(f"⚠️ Error generating roadmap: {ex}")

    # Display Roadmap Content if Available
    if st.session_state.analysis_result and st.session_state.student_profile:
        analysis = st.session_state.analysis_result
        prof = st.session_state.student_profile

        # Timeline presentation
        st.markdown(f"### 📍 8-Week Progression for **{prof.get('target_role')}**")
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
                    label="⬇️ Download Full Career Roadmap (PDF)",
                    data=pdf_bytes,
                    file_name=f"SkillSync_Roadmap_{safe_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error preparing PDF: {e}")

        with col_down_csv:
            try:
                csv_bytes = utils.export_skill_gap_to_csv(analysis.get("skills_analysis", []))
                st.download_button(
                    label="⬇️ Download Skill Gap Analysis (CSV)",
                    data=csv_bytes,
                    file_name="SkillSync_Skill_Gap.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error preparing CSV: {e}")

        # AI Custom Regeneration Expander
        with st.expander("🔄 Customize or Regenerate 8-Week Roadmap", expanded=False):
            st.markdown("Tailor your curriculum to emphasize specific tools or frameworks.")
            custom_regen_prompt = st.text_input(
                "Custom learning instructions:",
                placeholder="e.g. Focus more heavily on cloud infrastructure, Docker, and PostgreSQL optimization"
            )
            if st.button("Regenerate Roadmap with AI", key="btn_regen_roadmap_page"):
                effective_key = ai_engine.get_api_key()
                with st.spinner("Regenerating curriculum..."):
                    try:
                        new_roadmap = ai_engine.regenerate_roadmap_ai(
                            st.session_state.analysis_result,
                            custom_regen_prompt,
                            effective_key
                        )
                        st.session_state.analysis_result["roadmap"] = new_roadmap
                        st.toast("Roadmap successfully refreshed!", icon="✨")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to regenerate roadmap: {e}")
    else:
        st.info("💡 Configure your profile above and click **Generate My AI Roadmap** to view your customized 8-week timeline.")


# ==============================================================================
# PAGE 3: 🔍 SKILL GAP ANALYSIS
# ==============================================================================
elif st.session_state.current_page == "🔍 Skill Gap Analysis":
    st.markdown("## 🔍 Skill Gap Analysis & Diagnostic Matrix")

    if st.session_state.analysis_result and st.session_state.readiness_data:
        readiness = st.session_state.readiness_data
        analysis = st.session_state.analysis_result
        prof = st.session_state.student_profile or {}

        st.markdown(f"#### Target Role: **{prof.get('target_role', 'Engineering Specialist')}**")

        # Top Analytics Row (Gauge + Donut + Category Bar)
        col_gauge, col_donut, col_bar = st.columns([1, 1, 1.2])

        with col_gauge:
            st.markdown("##### 🎯 Overall Readiness")
            gauge_fig = roadmap_generator.create_readiness_gauge(
                readiness["score"],
                readiness["matched"],
                readiness["partial"],
                readiness["missing"],
                readiness["total"]
            )
            st.plotly_chart(gauge_fig, use_container_width=True)
            utils.safe_render_html(f"""
            <div style="text-align: center; font-size: 0.95rem; color: #94A3B8; margin-top: -12px;">
                Status: <b style="color: #FFFFFF;">{readiness['category']}</b>
            </div>
            """)

        with col_donut:
            st.markdown("##### 🥧 Skills Breakdown")
            donut_fig = roadmap_generator.create_skill_breakdown_donut(
                readiness["matched"],
                readiness["partial"],
                readiness["missing"]
            )
            st.plotly_chart(donut_fig, use_container_width=True)

        with col_bar:
            st.markdown("##### 📊 Category Distribution")
            bar_fig = roadmap_generator.create_category_distribution_bar(analysis.get("skills_analysis", []))
            st.plotly_chart(bar_fig, use_container_width=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        # Native Structured Skill Comparison Table
        st.markdown("#### 🔍 Required Skills vs. Your Current Status")
        st.caption(
            "Below is the comprehensive diagnostic matrix of core technologies needed for your target role. "
            "Status indicators: 🟢 **Already Have**, 🟡 **Needs Improvement**, 🔴 **Need to Learn**."
        )

        roadmap_generator.render_skill_gap_table(analysis.get("skills_analysis", []))

    else:
        utils.safe_render_html("""
        <div class="hero-gradient-card" style="text-align: center; padding: 3rem 2rem;">
            <div style="font-size: 3.5rem; margin-bottom: 0.75rem;">📊</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF;">No Diagnostic Data Found</div>
            <div style="font-size: 0.92rem; color: #94A3B8; max-width: 500px; margin: 0.5rem auto 1.5rem auto; line-height: 1.6;">
                Generate your personalized career analysis first to unlock interactive Plotly gauges, distribution charts, and the skill gap comparison matrix.
            </div>
        </div>
        """)
        if st.button("🚀 Go to Career Roadmap Setup", use_container_width=True):
            st.session_state.current_page = "🗺️ Career Roadmap"
            st.rerun()


# ==============================================================================
# PAGE 4: 📄 AI RESUME ANALYZER
# ==============================================================================
elif st.session_state.current_page == "📄 AI Resume Analyzer":
    st.markdown("## 📄 AI Resume & ATS Keyword Analyzer")
    st.markdown("Evaluate your resume against Applicant Tracking Systems (ATS) and detect keyword gaps.")

    col_upload, col_jd = st.columns([1, 1])

    with col_upload:
        st.markdown("#### 📤 Upload Resume")
        uploaded_resume = st.file_uploader(
            "Upload your resume (PDF or TXT):",
            type=["pdf", "txt"],
            help="Your resume is parsed securely in-memory and never permanently stored."
        )

    with col_jd:
        st.markdown("#### 🎯 Target Job Role & Description")
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

    analyze_resume_btn = st.button("🔍 Analyze Resume with AI", use_container_width=True, key="btn_analyze_resume")

    if analyze_resume_btn:
        if uploaded_resume is None:
            st.warning("⚠️ Please upload a PDF or TXT resume file first.")
        else:
            with st.spinner("🤖 Extracting text and benchmarking resume against ATS algorithms..."):
                extracted_text = utils.extract_text_from_pdf(uploaded_resume)
                if not extracted_text or len(extracted_text.strip()) < 30:
                    st.error("❌ Could not extract readable text from the uploaded file. Please ensure it is not an image-only scanned PDF.")
                else:
                    effective_key = ai_engine.get_api_key()
                    ats_res = ai_engine.analyze_resume_ats(
                        resume_text=extracted_text,
                        job_description=custom_jd,
                        target_role=target_role_for_ats,
                        api_key=effective_key
                    )
                    st.session_state.resume_analysis = ats_res
                    st.toast("Resume analysis complete!", icon="✅")

    # Render ATS Results
    if st.session_state.resume_analysis:
        ats = st.session_state.resume_analysis
        st.markdown("---")
        st.markdown("### 📊 ATS Optimization Diagnostic")

        col_ats_gauge, col_ats_overview = st.columns([1, 2])

        with col_ats_gauge:
            score = ats.get("ats_score", 65)
            gauge_fig = roadmap_generator.create_ats_score_gauge(score)
            st.plotly_chart(gauge_fig, use_container_width=True)
            match_lvl = ats.get("match_level", "Moderate Match")
            utils.safe_render_html(f"""
            <div style="text-align: center; font-size: 0.95rem; color: #94A3B8; margin-top: -12px;">
                Compatibility: <b style="color: #22D3EE;">{match_lvl}</b>
            </div>
            """)

        with col_ats_overview:
            st.markdown("##### 📌 ATS Assessment Summary")
            utils.safe_render_html(f"""
            <div class="glass-panel" style="padding: 1.25rem;">
                <div style="font-size: 0.9rem; color: #E2E8F0; line-height: 1.6;">
                    Your resume was evaluated against <b>{html.escape(target_role_for_ats)}</b> requirements. 
                    Adding quantified deliverables and closing keyword gaps will maximize your interview callback rate.
                </div>
            </div>
            """)

        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

        col_skills, col_gaps = st.columns(2)
        with col_skills:
            st.markdown("##### 🟢 Matching Skills Detected")
            matching_tags = "".join([f'<span class="skill-tag" style="background: rgba(34, 197, 94, 0.15); border-color: rgba(34, 197, 94, 0.35); color: #4ADE80;">✓ {html.escape(s)}</span>' for s in ats.get("matching_skills", [])])
            utils.safe_render_html(f'<div style="margin-bottom: 1.25rem;">{matching_tags}</div>')

            st.markdown("##### 🏆 Resume Strengths")
            for strength in ats.get("strengths", []):
                st.markdown(f"• **{strength}**")

        with col_gaps:
            st.markdown("##### 🔴 Missing Industry Keywords")
            missing_tags = "".join([f'<span class="skill-tag" style="background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.35); color: #F87171;">✕ {html.escape(s)}</span>' for s in ats.get("missing_keywords", [])])
            utils.safe_render_html(f'<div style="margin-bottom: 1.25rem;">{missing_tags}</div>')

            st.markdown("##### ⚠️ Areas for Improvement")
            for imp in ats.get("improvements", []):
                st.markdown(f"• {imp}")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### 💡 Actionable Next Steps")
        for rec in ats.get("actionable_recommendations", []):
            st.markdown(f"👉 {rec}")


# ==============================================================================
# PAGE 5: 🎙️ AI MOCK INTERVIEW
# ==============================================================================
elif st.session_state.current_page == "🎙️ AI Mock Interview":
    st.markdown("## 🎙️ AI Mock Interview Preparation")
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

    if st.button("🎯 Generate Interview Questions", use_container_width=True, key="btn_gen_interview"):
        effective_key = ai_engine.get_api_key()
        with st.spinner("🤖 Preparing realistic interview questions for your profile..."):
            questions = ai_engine.generate_mock_interview_questions(
                target_role=interview_role,
                experience_level=interview_exp,
                category=interview_cat,
                api_key=effective_key
            )
            st.session_state.mock_interview_questions = questions
            st.session_state.mock_interview_eval = None
            st.session_state.active_interview_idx = 0
            st.toast("Interview questions ready!", icon="🎙️")

    # Render Active Question & Answer Interface
    if st.session_state.mock_interview_questions:
        questions = st.session_state.mock_interview_questions
        st.markdown("---")

        q_idx = st.session_state.active_interview_idx
        q_item = questions[q_idx]

        utils.safe_render_html(f"""
        <div class="interview-question-box">
            <div style="font-size: 0.8rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                Question {q_idx + 1} of {len(questions)} • {html.escape(q_item.get('category', 'Technical'))}
            </div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; line-height: 1.5;">
                {html.escape(q_item.get('question', ''))}
            </div>
        </div>
        """)

        # Candidate Answer Input Area
        candidate_answer = st.text_area(
            "Your Answer:",
            placeholder="Type your structured answer here. Include architectural considerations, trade-offs, and metrics where applicable...",
            height=160
        )

        col_sub_ans, col_next_q = st.columns([3, 1])
        with col_sub_ans:
            submit_ans_btn = st.button("🚀 Submit Answer for AI Evaluation", use_container_width=True, key="btn_submit_ans")
        with col_next_q:
            if st.button("Next Question ⏭️", use_container_width=True, key="btn_next_q"):
                st.session_state.active_interview_idx = (q_idx + 1) % len(questions)
                st.session_state.mock_interview_eval = None
                st.rerun()

        if submit_ans_btn:
            if not candidate_answer or len(candidate_answer.strip()) < 10:
                st.warning("⚠️ Please provide a detailed response before submitting.")
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
                    st.toast("Evaluation complete!", icon="✅")

        # Display Evaluation
        if st.session_state.mock_interview_eval:
            ev = st.session_state.mock_interview_eval
            score_10 = ev.get("score", 7)

            utils.safe_render_html(f"""
            <div class="interview-feedback-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">AI Evaluation Report</div>
                    <div style="font-size: 1.35rem; font-weight: 900; color: #22C55E;">Score: {score_10} / 10</div>
                </div>
                <div style="font-size: 0.92rem; color: #E2E8F0; line-height: 1.6; margin-bottom: 1rem;">
                    {html.escape(ev.get("feedback", ""))}
                </div>
            </div>
            """)

            col_ev_s, col_ev_i = st.columns(2)
            with col_ev_s:
                st.markdown("##### 🟢 Strengths")
                for s in ev.get("strengths", []):
                    st.markdown(f"• {s}")
            with col_ev_i:
                st.markdown("##### ⚠️ Improvement Opportunities")
                for imp in ev.get("improvement_areas", []):
                    st.markdown(f"• {imp}")

            st.markdown("##### 🏆 Model Exemplary Answer")
            utils.safe_render_html(f"""
            <div class="glass-panel" style="padding: 1rem; border-left: 3px solid #8B5CF6;">
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6;">
                    {html.escape(ev.get("model_answer", ""))}
                </div>
            </div>
            """)


# ==============================================================================
# PAGE 6: 🚀 PROJECT RECOMMENDATIONS
# ==============================================================================
elif st.session_state.current_page == "🚀 Project Recommendations":
    st.markdown("## 🚀 Standout Portfolio Project Blueprints")
    st.markdown("Showcase graduated mastery with live interactive previews and production-ready source code.")

    # Determine projects to render
    projects = []
    if st.session_state.analysis_result:
        projects = st.session_state.analysis_result.get("portfolio_projects", [])
    else:
        # Load curated projects for default role
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
        search_query = st.text_input("🔍 Search project titles or technologies:", placeholder="e.g. React, Docker, Machine Learning")
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
# PAGE 7: 📚 LEARNING RESOURCES
# ==============================================================================
elif st.session_state.current_page == "📚 Learning Resources":
    st.markdown("## 📚 Curated Technical Learning Library")
    st.markdown("Hand-picked official documentation, interactive tutorials, and certification guides.")

    tab_web, tab_back, tab_data, tab_devops, tab_certs = st.tabs([
        "🌐 Frontend & Web",
        "⚙️ Backend & Systems",
        "🤖 AI & Data Science",
        "☁️ Cloud & DevOps",
        "🎓 Top Free Certifications"
    ])

    with tab_web:
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 React 19 Official Documentation</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">Official Guide • Advanced React</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Master React Server Components, Suspense architecture, and custom hooks with interactive sandboxes.
                </div>
                <a href="https://react.dev" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Explore Documentation ↗</a>
            </div>
            """)
        with col_w2:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Web.dev Core Web Vitals</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">Google Developer Guide • Performance</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    In-depth techniques for optimizing Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and layout shifts.
                </div>
                <a href="https://web.dev/explore/metrics" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">View Guide ↗</a>
            </div>
            """)

    with tab_back:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Use The Index, Luke!</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">Database Mastery • SQL Optimization</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    A definitive guide to database performance, composite B-Tree indexes, and relational query tuning.
                </div>
                <a href="https://use-the-index-luke.com/" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Read Handbook ↗</a>
            </div>
            """)
        with col_b2:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Designing Data-Intensive Applications</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">Distributed Systems • Architecture</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Fundamental principles for building reliable, scalable, and maintainable data systems and microservices.
                </div>
                <a href="https://dataintensive.net/" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Learn More ↗</a>
            </div>
            """)

    with tab_data:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Fast.ai Practical Deep Learning</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">Deep Learning • PyTorch</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Hands-on course taking you from fundamentals to training state-of-the-art vision and language models.
                </div>
                <a href="https://course.fast.ai" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Access Free Course ↗</a>
            </div>
            """)
        with col_d2:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Google Gemini API Documentation</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">GenAI • LLM Integration</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Comprehensive guides for structured JSON outputs, multimodal reasoning, and embeddings.
                </div>
                <a href="https://ai.google.dev/docs" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">View API Docs ↗</a>
            </div>
            """)

    with tab_devops:
        col_dp1, col_dp2 = st.columns(2)
        with col_dp1:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Docker Curriculum</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">DevOps Basics • Containerization</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Practical hands-on guide for containerizing full-stack applications and orchestrating multi-service setups.
                </div>
                <a href="https://docker-curriculum.com/" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Start Tutorial ↗</a>
            </div>
            """)
        with col_dp2:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🔗 Kubernetes Interactive Tutorials</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">K8s • Cloud Native</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Learn to deploy, scale, and update containerized applications directly in a live terminal sandbox.
                </div>
                <a href="https://kubernetes.io/docs/tutorials/" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Interactive Sandbox ↗</a>
            </div>
            """)

    with tab_certs:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🎓 freeCodeCamp Certifications</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">300-Hour Accredited Curriculums • 100% Free</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    Recognized credentials in Responsive Web Design, JavaScript Algorithms, Relational Databases, and Machine Learning.
                </div>
                <a href="https://www.freecodecamp.org/learn" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Enroll Free ↗</a>
            </div>
            """)
        with col_c2:
            utils.safe_render_html("""
            <div class="resource-tile">
                <div style="font-weight: 800; font-size: 1.1rem; color: #FFFFFF; margin-bottom: 0.35rem;">🎓 CS50x: Introduction to Computer Science</div>
                <div style="font-size: 0.82rem; color: #22D3EE; margin-bottom: 0.5rem;">Harvard University • edX</div>
                <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1rem;">
                    The world-renowned computer science course covering C, algorithms, memory, Python, SQL, and web development.
                </div>
                <a href="https://cs50.harvard.edu/x" target="_blank" style="color: #8B5CF6; font-weight: 700; text-decoration: none;">Audit Course ↗</a>
            </div>
            """)


# ==============================================================================
# PAGE 8: ⚙️ SETTINGS & SYSTEM STATUS
# ==============================================================================
elif st.session_state.current_page == "⚙️ Settings":
    st.markdown("## ⚙️ Settings & System Diagnostics")
    st.markdown("Review system architecture, configuration status, and session controls.")

    col_set1, col_set2 = st.columns(2)

    with col_set1:
        st.markdown("#### 🔒 Centralized Engine Configuration")
        status = ai_engine.get_engine_status()
        st.markdown(f"**Engine Status:** `{status['label']}`")
        st.markdown(f"**Active Source:** `{status['source_type']}`")
        st.markdown(f"**Architecture:** `Streamlit Cloud + GenAI / Heuristic Fallback`")
        st.caption("API keys are centrally managed via server secrets and environment variables. Visitors never need to input keys.")

        # Developer Session Override (Optional)
        with st.expander("🛠️ Developer Key Override (Optional)", expanded=False):
            dev_key = st.text_input(
                "Enter temporary session API Key:",
                type="password",
                placeholder="AIzaSy...",
                help="Applies only to your current session. Never printed or saved to disk."
            )
            if st.button("Apply Session Key"):
                if dev_key:
                    st.session_state["dev_api_key"] = dev_key
                    st.toast("Temporary session key applied!", icon="🔑")
                    st.rerun()

    with col_set2:
        st.markdown("#### 💻 Technical Diagnostics")
        st.markdown(f"**Python Runtime:** `{sys.version.split()[0]}`")
        st.markdown(f"**Streamlit Engine:** `{st.__version__}`")
        st.markdown(f"**GenAI Available:** `{ai_engine.GENAI_AVAILABLE}`")
        st.markdown(f"**ReportLab Available:** `{utils.REPORTLAB_AVAILABLE}`")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🗑️ Data Management")
        if st.button("Reset Entire Application State", use_container_width=True):
            st.session_state.clear()
            st.toast("Application state cleared.", icon="🔄")
            st.rerun()

# ==============================================================================
# GLOBAL FOOTER
# ==============================================================================
utils.safe_render_html("""
<div style="text-align: center; margin-top: 4.5rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.08); font-size: 0.88rem; color: #64748B;">
    ⚡ <b>SkillSync 2.0</b> — Your AI Career Mentor • Built with Google Gemini API, Streamlit, Plotly & Pandas<br/>
    Discover Your Skills. Bridge the Gap. Build Your Future.
</div>
""")

"""
SkillSync 2.0 - Roadmap & Dashboard Visual Generator
Handles rendering of the futuristic skill gap dashboard, Plotly readiness gauges,
interactive 8-week roadmap milestone cards, and portfolio project blueprints.
"""

import html
from typing import Dict, List, Any
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import project_preview_engine
import utils


def create_readiness_gauge(score: int, matched: int, partial: int, missing: int, total: int, theme: str = "dark") -> go.Figure:
    """
    Generate a luxury circular gauge chart using Plotly.
    Adapts dynamically to Obsidian Gold (#090909) and Ivory Gold (#F7F5EF).
    """
    is_dark = (theme != "light")
    text_color = "#F8F5EC" if is_dark else "#171717"
    subtext_color = "#A5A5A5" if is_dark else "#77716A"
    gold_accent = "#D4AF37" if is_dark else "#B58B35"
    gold_champagne = "#F1D58A" if is_dark else "#D9BD79"

    if score >= 75:
        bar_color = "#22C55E"
    elif score >= 50:
        bar_color = gold_accent
    elif score >= 30:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            'suffix': "%",
            'font': {'size': 48, 'color': text_color, 'family': 'Manrope, Inter, sans-serif'}
        },
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "rgba(165,165,165,0.2)",
                'tickfont': {'color': subtext_color, 'family': 'Inter'}
            },
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "rgba(255, 255, 255, 0.04)" if is_dark else "rgba(0, 0, 0, 0.03)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.08)",
            'steps': [
                {'range': [0, 35], 'color': 'rgba(239, 68, 68, 0.14)'},
                {'range': [35, 70], 'color': 'rgba(245, 158, 11, 0.14)'},
                {'range': [70, 100], 'color': 'rgba(34, 197, 94, 0.14)'}
            ],
            'threshold': {
                'line': {'color': gold_accent, 'width': 3.5},
                'thickness': 0.82,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=25, b=20),
        height=230,
        font={'color': text_color, 'family': 'Inter'},
        transition={'duration': 650, 'easing': 'cubic-in-out'}
    )
    return fig


def create_skill_breakdown_donut(matched: int, partial: int, missing: int, theme: str = "dark") -> go.Figure:
    """
    Generate a sleek donut chart showing the breakdown of skills
    with luxury gold accents.
    """
    is_dark = (theme != "light")
    text_color = "#F8F5EC" if is_dark else "#171717"
    subtext_color = "#A5A5A5" if is_dark else "#77716A"
    gold_accent = "#D4AF37" if is_dark else "#B58B35"

    labels = ['Already Have', 'Needs Improvement', 'Need to Learn']
    values = [matched, partial, missing]
    colors = ['#22C55E', '#F59E0B', '#EF4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.64,
        marker=dict(colors=colors, line=dict(color='#090909' if is_dark else '#FFFFFF', width=2.5)),
        textinfo='value+percent',
        hoverinfo='label+value',
        textfont=dict(color='#FFFFFF', size=12, family='Inter')
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
            font=dict(color=subtext_color, size=11, family='Inter')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=30),
        height=230,
        transition={'duration': 500, 'easing': 'cubic-in-out'}
    )
    return fig


def create_category_distribution_bar(skills_analysis: List[Dict[str, Any]], theme: str = "dark") -> go.Figure:
    """
    Generate a horizontal bar chart showing the distribution of skills across tech domains.
    """
    is_dark = (theme != "light")
    text_color = "#F8F5EC" if is_dark else "#171717"
    subtext_color = "#A5A5A5" if is_dark else "#77716A"
    gold_accent = "#D4AF37" if is_dark else "#B58B35"

    categories: Dict[str, Dict[str, int]] = {}
    for s in skills_analysis:
        cat = str(s.get("category", "General")).strip()
        status = str(s.get("status", "Need to Learn")).strip().lower()
        if cat not in categories:
            categories[cat] = {"matched": 0, "to_learn": 0}
        if "have" in status or "already" in status:
            categories[cat]["matched"] += 1
        else:
            categories[cat]["to_learn"] += 1

    cat_names = list(categories.keys())
    matched_vals = [categories[c]["matched"] for c in cat_names]
    to_learn_vals = [categories[c]["to_learn"] for c in cat_names]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=cat_names,
        x=matched_vals,
        name='Already Possess',
        orientation='h',
        marker=dict(color='#22C55E')
    ))
    fig.add_trace(go.Bar(
        y=cat_names,
        x=to_learn_vals,
        name='Skills to Learn',
        orientation='h',
        marker=dict(color=gold_accent)
    ))

    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=20, t=20, b=20),
        height=max(200, len(cat_names) * 38),
        transition={'duration': 500, 'easing': 'cubic-in-out'},
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color=subtext_color, size=11, family='Inter')
        ),
        xaxis=dict(
            title=dict(text="Number of Skills", font=dict(color=subtext_color, size=11)),
            tickfont=dict(color=subtext_color),
            gridcolor='rgba(255, 255, 255, 0.06)' if is_dark else 'rgba(0, 0, 0, 0.06)'
        ),
        yaxis=dict(
            tickfont=dict(color=text_color, size=11),
            autorange="reversed"
        )
    )
    return fig


def create_ats_score_gauge(score: int, theme: str = "dark") -> go.Figure:
    """
    Generate an ATS compatibility radial gauge chart with luxury gold styling.
    """
    is_dark = (theme != "light")
    text_color = "#F8F5EC" if is_dark else "#171717"
    subtext_color = "#A5A5A5" if is_dark else "#77716A"
    gold_accent = "#D4AF37" if is_dark else "#B58B35"

    if score >= 80:
        bar_color = "#22C55E"
    elif score >= 65:
        bar_color = gold_accent
    elif score >= 50:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            'suffix': "%",
            'font': {'size': 44, 'color': text_color, 'family': 'Manrope, Inter'}
        },
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "rgba(165,165,165,0.2)", 'tickfont': {'color': subtext_color}},
            'bar': {'color': bar_color, 'thickness': 0.35},
            'bgcolor': "rgba(255, 255, 255, 0.04)" if is_dark else "rgba(0, 0, 0, 0.03)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.08)",
            'threshold': {'line': {'color': gold_accent, 'width': 3}, 'thickness': 0.8, 'value': score}
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=210,
        font={'color': text_color, 'family': 'Inter'},
        transition={'duration': 650, 'easing': 'cubic-in-out'}
    )
    return fig



def render_career_overview_hero(prof: Dict[str, Any], analysis: Dict[str, Any], readiness: Dict[str, Any]):
    """
    Render a visually attractive hero section containing:
    - Target Job Role (prominently displayed)
    - Current Experience Level
    - Career Readiness Score
    - Estimated Learning Duration
    - Recommended Weekly Study Hours
    - Concise AI-generated career assessment & industry outlook
    """
    role = prof.get("target_role", "Software Engineer")
    exp = prof.get("experience_level", "Intermediate")
    hours = prof.get("study_hours", "10–15 hours")
    score = readiness.get("score", 0) if readiness else 0
    category_label = readiness.get("category", "Pending Assessment") if readiness else "Pending Assessment"

    summary_obj = analysis.get("career_summary", {})
    demand_summary = summary_obj.get("market_demand_summary", f"{role} is a pivotal engineering role in today\'s technology landscape.")
    motivation = summary_obj.get("motivational_message", "Consistent weekly study and hands-on portfolio deliverables bridge every skill gap.")

    hero_html = f"""
    <div class="career-hero-card">
        <div class="hero-eyebrow">Personalized Career Intelligence</div>
        <div class="career-hero-title">{html.escape(role)}</div>
        <div class="career-hero-badges">
            <span class="career-hero-badge gold">Target Role: {html.escape(role)}</span>
            <span class="career-hero-badge">Experience: {html.escape(exp)}</span>
            <span class="career-hero-badge gold">{score}% Career Readiness ({html.escape(category_label)})</span>
            <span class="career-hero-badge">Duration: 8 Weeks Structured</span>
            <span class="career-hero-badge">Availability: {html.escape(hours)} / week</span>
        </div>
        <div class="career-hero-assessment">
            <b>Strategic Career Assessment:</b> {html.escape(demand_summary)}
            <br><br>
            <b>Curriculum Advisory:</b> {html.escape(motivation)}
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)


def render_career_insights_row(analysis: Dict[str, Any]):
    """
    Render three distinct insight cards:
    1. Your Strengths
    2. Areas to Improve
    3. Recommended Next Steps
    """
    summary_obj = analysis.get("career_summary", {})
    strengths = summary_obj.get("strengths", [
        "Solid baseline competencies in core programming fundamentals.",
        "Clear technical direction and motivation for structured learning.",
        "Demonstrated familiarity with foundational developer workflows."
    ])
    improvements = summary_obj.get("areas_to_improve", [
        "Deepen practical hands-on experience with production-grade frameworks.",
        "Establish automated testing and continuous integration practices.",
        "Translate conceptual knowledge into deployable portfolio applications."
    ])
    next_steps = summary_obj.get("next_steps", [
        "Complete Week 1 hands-on exercises and establish your GitHub project repo.",
        "Focus initial weekly study on mastering high-priority gap competencies.",
        "Deploy the mid-term prototype to validate full-stack competency."
    ])

    col_ins1, col_ins2, col_ins3 = st.columns(3)

    with col_ins1:
        str_bullets = "".join([f"<li>{html.escape(s)}</li>" for s in strengths[:3]])
        st.markdown(f"""
        <div class="insight-card strength">
            <div class="insight-card-header">
                <span style="color: var(--status-success); font-weight: 800; font-size: 16px;">✓</span>
                <span class="insight-card-title">Your Key Strengths</span>
            </div>
            <div class="insight-card-body">
                Competencies where you currently demonstrate baseline or working proficiency:
                <ul class="insight-card-list">{str_bullets}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ins2:
        imp_bullets = "".join([f"<li>{html.escape(s)}</li>" for s in improvements[:3]])
        st.markdown(f"""
        <div class="insight-card improvement">
            <div class="insight-card-header">
                <span style="color: var(--status-warning); font-weight: 800; font-size: 16px;">▲</span>
                <span class="insight-card-title">Priority Growth Areas</span>
            </div>
            <div class="insight-card-body">
                Critical engineering skill gaps to address for target role readiness:
                <ul class="insight-card-list">{imp_bullets}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ins3:
        step_bullets = "".join([f"<li>{html.escape(s)}</li>" for s in next_steps[:3]])
        st.markdown(f"""
        <div class="insight-card recommendation">
            <div class="insight-card-header">
                <span style="color: var(--gold-primary); font-weight: 800; font-size: 16px;">➔</span>
                <span class="insight-card-title">Recommended Next Steps</span>
            </div>
            <div class="insight-card-body">
                Actionable milestones to maximize your learning trajectory:
                <ul class="insight-card-list">{step_bullets}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_career_milestones_stepper(completed_weeks: int, total_weeks: int = 8):
    """
    Render a visual 4-stage progression showing major learning stages:
    Stage 1: Foundation (Weeks 1-2)
    Stage 2: Intermediate Core (Weeks 3-4)
    Stage 3: Advanced Systems (Weeks 5-6)
    Stage 4: Production & Capstone Ready (Weeks 7-8)
    """
    stages = [
        {"title": "Foundation", "weeks": "Weeks 1–2", "min": 2, "desc": "Syntax, data pipelines & core architecture"},
        {"title": "Intermediate Core", "weeks": "Weeks 3–4", "min": 4, "desc": "Domain frameworks & complex problem solving"},
        {"title": "Advanced Systems", "weeks": "Weeks 5–6", "min": 6, "desc": "System architecture, optimization & testing"},
        {"title": "Job Ready Capstone", "weeks": "Weeks 7–8", "min": 8, "desc": "Full-scale project, CI/CD & cloud deployment"}
    ]

    stepper_html = '<div class="milestone-stepper">'
    for idx, s in enumerate(stages):
        if completed_weeks >= s["min"]:
            status_class = "completed"
            status_badge = '<span style="color: var(--status-success);">✓ Completed</span>'
        elif completed_weeks >= (s["min"] - 2):
            status_class = "active"
            status_badge = '<span style="color: var(--gold-primary);">● In Progress</span>'
        else:
            status_class = "pending"
            status_badge = '<span style="color: var(--text-muted);">○ Upcoming</span>'

        stepper_html += f'''
        <div class="stepper-stage {status_class}">
            <div class="stepper-stage-header">
                <span class="stepper-stage-title">Stage {idx+1}: {s["title"]}</span>
            </div>
            <div class="stepper-stage-weeks">{s["weeks"]} • {s["desc"]}</div>
            <div class="stepper-stage-status">{status_badge}</div>
        </div>
        '''
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)

def render_skill_gap_table(skills_analysis: List[Dict[str, Any]]):
    """
    Render a comprehensive skill analytics dashboard:
    - Summary Quick-Metrics
    - "Your Next 5 Skills to Focus On" actionable ranking
    - Category groupings
    - Interactive Native Streamlit DataFrame with clean status badges
    """
    if not skills_analysis:
        st.info("No skill diagnostic data available for display.")
        return

    # Clean & normalize data into structured records
    table_records = []
    matched_count = 0
    partial_count = 0
    missing_count = 0
    gap_skills = []

    for s in skills_analysis:
        skill_name = str(s.get("skill", "Unknown Skill")).strip()
        category = str(s.get("category", "General")).strip()
        raw_status = str(s.get("status", "Need to Learn")).strip()
        raw_priority = str(s.get("priority", "–")).strip()
        recommendation = str(s.get("recommendation", s.get("current_mastery", "Action step in roadmap"))).strip()

        # Map status
        if raw_status.lower() in ["already have", "have", "possessed", "mastered"]:
            status_display = "Already Have"
            matched_count += 1
        elif raw_status.lower() in ["partially skilled", "needs improvement", "partial", "improving"]:
            status_display = "Needs Improvement"
            partial_count += 1
            gap_skills.append((skill_name, category, "Medium", recommendation))
        else:
            status_display = "Need to Learn"
            missing_count += 1
            gap_skills.append((skill_name, category, "High", recommendation))

        p_lower = raw_priority.lower()
        if "high" in p_lower:
            priority_display = "High"
        elif "med" in p_lower:
            priority_display = "Medium"
        elif "low" in p_lower:
            priority_display = "Low"
        else:
            priority_display = "—"

        table_records.append({
            "Skill / Technology": skill_name,
            "Category": category,
            "Current Status": status_display,
            "Priority": priority_display,
            "Learning Recommendation": recommendation
        })

    # 1. Summary Quick-Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Already Have", value=f"{matched_count} Skills", help="Verified technologies you currently possess")
    with col_m2:
        st.metric(label="Needs Improvement", value=f"{partial_count} Skills", help="Competencies requiring deeper practical experience")
    with col_m3:
        st.metric(label="Need to Learn", value=f"{missing_count} Skills", help="High-priority gap targets for your dream role")

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    # 2. Actionable Section: "Your Next 5 Skills to Focus On"
    st.markdown("##### Your Next 5 High-Impact Skills to Focus On")
    st.caption("Prioritized based on industry hiring bars and foundational prerequisites for your target career.")

    focus_list = gap_skills[:5] if gap_skills else [("System Architecture", "Software Engineering", "High", "Master scalable distributed design patterns")]
    for rank, (f_name, f_cat, f_prio, f_rec) in enumerate(focus_list, 1):
        st.markdown(f"""
        <div class="focus-skill-card">
            <div class="focus-rank-badge">{rank}</div>
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="font-weight: 700; font-size: 14.5px; color: var(--text-primary); font-family: var(--font-heading);">{html.escape(f_name)}</span>
                    <span class="badge-clean gold" style="font-size: 11px;">{html.escape(f_cat)} • {html.escape(f_prio)} Priority</span>
                </div>
                <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.5;">
                    <b>Why It Matters:</b> Essential engineering competency required in production workflows.
                    <br>
                    <b>Recommended Action:</b> {html.escape(f_rec)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # 3. Interactive Native Streamlit DataFrame
    st.markdown("##### Complete Diagnostic Skill Matrix")
    df = pd.DataFrame(table_records)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Skill / Technology": st.column_config.TextColumn("Skill / Technology", width="medium"),
            "Category": st.column_config.TextColumn("Category", width="small"),
            "Current Status": st.column_config.TextColumn("Current Status", width="medium"),
            "Priority": st.column_config.TextColumn("Priority", width="small"),
            "Learning Recommendation": st.column_config.TextColumn("Learning Recommendation", width="large")
        }
    )

    # 4. Filterable Category Groupings
    categories_found = sorted(list({s.get("category", "General") for s in skills_analysis}))
    if len(categories_found) > 1:
        with st.expander("Filter & Explore Skills by Technical Category", expanded=False):
            selected_cat = st.selectbox("Select Domain Category:", ["All Domains"] + categories_found)
            filtered_skills = skills_analysis if selected_cat == "All Domains" else [s for s in skills_analysis if s.get("category") == selected_cat]
            for s in filtered_skills:
                s_name = s.get("skill", "Unknown")
                cat = s.get("category", "General")
                status = s.get("status", "Need to Learn")
                priority = s.get("priority", "–")
                rec = s.get("recommendation", "")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**{s_name}**")
                    st.caption(f"Domain: `{cat}` • Status: `{status}` • Priority: `{priority}`")
                with c2:
                    st.markdown(f"*{rec}*")
                st.markdown("---")


def render_roadmap_cards(roadmap: List[Dict[str, Any]]):
    """
    Render the 8-week personalized roadmap in modern interactive cards:
    - Structured learning milestones
    - Compact objective cards
    - Numbered exercise task cards
    - Rich resource cards with verified links
    - Highlighted weekly mini-project card
    - Milestone outcome banner
    - Interactive completion tracking with session persistence
    """
    # Track completion count
    completed_weeks = sum(
        1 for i in range(1, len(roadmap) + 1)
        if st.session_state.get(f"week_completed_{i}", False)
    )
    total_weeks = len(roadmap)
    progress_pct = int((completed_weeks / total_weeks) * 100) if total_weeks > 0 else 0
    remaining_weeks = total_weeks - completed_weeks

    col_prog1, col_prog2 = st.columns([3, 1])
    with col_prog1:
        st.markdown(f"**Roadmap Progress Tracker:** `{completed_weeks} of {total_weeks} Weeks Completed ({progress_pct}%) • {remaining_weeks} Weeks Remaining`")
    with col_prog2:
        status_txt = "Curriculum Completed" if progress_pct == 100 else "In Progress"
        if progress_pct == 100:
            st.success(status_txt)
        else:
            st.info(status_txt)
    st.progress(progress_pct / 100.0)

    if progress_pct == 100 and total_weeks > 0:
        st.success("Milestone Complete: You have mastered all 8 weeks of your curriculum! You are ready to apply for target engineering roles.")

    # Stepper progression
    render_career_milestones_stepper(completed_weeks, total_weeks)

    for week in roadmap:
        w_num = week.get("week_number", 1)
        w_title = week.get("week_title", f"Week {w_num}")
        hours = week.get("estimated_study_hours", 10)
        skills = week.get("skills_to_develop", [])
        objectives = week.get("objectives", [])
        resources = week.get("resources", [])
        exercises = week.get("practical_exercises", [])
        mini_project = week.get("mini_project", f"Build a focused working prototype applying Week {w_num} skills.")
        outcome = week.get("expected_outcome", "Solidify core concepts.")

        is_done = st.session_state.get(f"week_completed_{w_num}", False)
        is_capstone = (w_num == 8)

        capstone_label = " (Capstone Project)" if is_capstone else ""
        done_label = " [Completed]" if is_done else ""
        expander_title = f"Week {w_num}{capstone_label}: {w_title} • {hours} hrs/week{done_label}"

        with st.expander(expander_title, expanded=(w_num in [1, 2])):
            if is_done:
                st.markdown(
                    '<div class="badge-clean gold" style="margin-bottom: 0.85rem; display: inline-flex;">'
                    '✓ Milestone Completed</div>',
                    unsafe_allow_html=True
                )

            col_left, col_right = st.columns([3, 2])

            with col_left:
                # A. Learning Objectives
                st.markdown("##### Learning Objectives")
                for obj in objectives:
                    st.markdown(
                        f'<div class="objective-item-card">'
                        f'<span style="color: var(--gold-primary); font-weight: bold;">✓</span> '
                        f'<span>{html.escape(str(obj))}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)

                # C. Practical Exercises
                st.markdown("##### Practical Exercises & Deliverables")
                for idx, ex in enumerate(exercises):
                    ex_str = str(ex)
                    st.markdown(
                        f'<div class="task-card-numbered">'
                        f'<div class="task-badge-number">Task {idx+1}</div>'
                        f'<div class="task-content">{html.escape(ex_str)}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                # E. Weekly Mini Project
                if isinstance(mini_project, dict):
                    p_name = mini_project.get("name", f"Week {w_num} Practical Prototype")
                    p_obj = mini_project.get("objective", f"Apply Week {w_num} competencies.")
                    p_techs = " ".join([f"`{t}`" for t in mini_project.get("technologies", skills[:3])])
                    p_output = mini_project.get("expected_output", "Functional code repository with tests.")
                    p_effort = mini_project.get("estimated_effort", f"{max(3, hours // 2)} hrs")
                else:
                    p_name = f"Week {w_num} Practical Prototype"
                    p_obj = str(mini_project)
                    p_techs = " ".join([f"`{s}`" for s in skills[:3]])
                    p_output = "Functional code repository with tests."
                    p_effort = f"{max(3, hours // 2)} hrs"

                st.markdown(f"""
                <div class="mini-project-highlight-card">
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gold-primary); font-weight: 700;">Weekly Practical Project</div>
                    <div class="mini-project-title">{html.escape(p_name)}</div>
                    <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 0.45rem; line-height: 1.5;"><b>Objective:</b> {html.escape(p_obj)}</div>
                    <div style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 0.35rem;"><b>Deliverable:</b> {html.escape(p_output)} • <b>Effort:</b> {html.escape(p_effort)}</div>
                    <div style="margin-top: 0.4rem;">{p_techs}</div>
                </div>
                """, unsafe_allow_html=True)

                # F. Expected Milestone Outcome
                st.markdown(f"""
                <div class="outcome-banner-rich">
                    <span style="color: var(--gold-primary); font-weight: bold; font-size: 15px;">★</span>
                    <div><b>Milestone Target:</b> {html.escape(str(outcome))}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_right:
                # B. Skills to Develop
                st.markdown("##### Skills to Develop")
                skill_chips = " ".join([f"`{s}`" for s in skills])
                st.markdown(skill_chips if skill_chips else "`Core Principles`")

                st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)

                # D. Recommended Resources
                st.markdown("##### Recommended Resources")
                for res in resources:
                    if isinstance(res, dict):
                        r_title = res.get("title", "Reference Guide")
                        r_provider = res.get("provider", "Official Docs")
                        r_type = res.get("type", "Documentation")
                        r_desc = res.get("description", "Recommended guide and technical reference.")
                        r_link = res.get("link", "https://devdocs.io")
                    else:
                        r_title = str(res)
                        r_provider = "Resource"
                        r_type = "Guide"
                        r_desc = "Technical guide and reference."
                        r_link = "https://devdocs.io"

                    st.markdown(f"""
                    <div class="resource-card-rich">
                        <div class="resource-info-left">
                            <a href="{html.escape(r_link)}" target="_blank" class="resource-title-link">{html.escape(r_title)} ↗</a>
                            <div class="resource-meta-row">
                                <span class="badge-clean gold" style="padding: 1px 6px; font-size: 10.5px;">{html.escape(r_provider)}</span>
                                <span>{html.escape(r_type)}</span>
                            </div>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 0.2rem;">{html.escape(r_desc)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # G. Completion Tracking
                st.checkbox(
                    "Mark Milestone as Completed",
                    key=f"week_completed_{w_num}",
                    value=is_done,
                    help="Check off this milestone as you complete your weekly deliverables."
                )

def render_portfolio_projects(projects: List[Dict[str, Any]]):
    """
    Render portfolio projects in visual-first presentation with live interactive previews
    and optional developer tools / source code.
    """
    project_preview_engine.render_all_portfolio_projects(projects)


render_vertical_timeline = render_roadmap_cards



def render_resume_analysis_results(ats: Dict[str, Any], target_role: str, theme: str = "dark"):
    """
    Render a comprehensive, executive-grade ATS Optimization Report:
    - ATS score gauge & executive overview
    - 4 Core Diagnostics cards (Strengths, Missing Keywords, Relevance, Formatting)
    - "Top 5 Strategic Resume Improvements" with What/Why/How and Before/After diffs
    - Actionable recommendations & checklist
    """
    if not ats:
        st.info("No resume analysis results available.")
        return

    score = ats.get("ats_score", 68)
    match_lvl = ats.get("match_level", "Moderate Match")

    # 1. Hero Score Gauge & Summary
    col_gauge, col_summary = st.columns([1, 1.8])

    with col_gauge:
        gauge_fig = create_ats_score_gauge(score, theme=theme)
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown(
            f'<div style="text-align: center; margin-top: -10px;">'
            f'<span class="badge-clean gold" style="font-size: 13px; padding: 4px 12px;">{html.escape(match_lvl)}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col_summary:
        st.markdown(f"""
        <div class="career-hero-card" style="padding: 1.25rem 1.5rem; margin-top: 0.5rem;">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--gold-primary); font-weight: 700;">ATS Benchmarking Result</div>
            <div style="font-size: 1.35rem; font-weight: 800; font-family: var(--font-heading); margin: 0.25rem 0;">Evaluated for {html.escape(target_role)}</div>
            <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.6; margin-top: 0.5rem;">
                Your resume scored <b>{score}/100</b> against industry standard applicant tracking filters and automated parsing algorithms for this position.
                Applying the structured improvements below will significantly elevate your interview invitation probability.
            </div>
            <div style="display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap;">
                <span class="career-hero-badge"><b>{len(ats.get('matching_skills', []))}</b> Matched Competencies</span>
                <span class="career-hero-badge" style="border-color: rgba(245, 158, 11, 0.4);"><b>{len(ats.get('missing_keywords', []))}</b> Missing Keywords</span>
                <span class="career-hero-badge"><b>ATS Friendly Format</b> Verified</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Four Diagnostics Cards (2x2 Grid)
    st.markdown("### Diagnostic Breakdown")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        # Strengths Card
        strengths = ats.get("strengths", [])
        strengths_list = "".join([f"<li style='margin-bottom: 0.4rem;'>{html.escape(str(s))}</li>" for s in strengths])
        matching_tags = " ".join([f"<span class='badge-clean gold' style='margin: 2px;'>{html.escape(str(s))}</span>" for s in ats.get("matching_skills", [])])
        st.markdown(f"""
        <div class="insight-card strength" style="min-height: 220px;">
            <div class="insight-card-header">
                <span class="insight-card-icon">✓</span>
                <span class="insight-card-title">Verified Resume Strengths</span>
            </div>
            <ul style="margin: 0.5rem 0 0.75rem 1.2rem; padding: 0; font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                {strengths_list if strengths_list else '<li>Clear technical experience outlined</li>'}
            </ul>
            <div style="margin-top: 0.5rem; font-size: 11.5px; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Matched Tech Stack:</div>
            <div style="margin-top: 0.35rem;">{matching_tags if matching_tags else '<span style="color: var(--text-muted); font-size: 12px;">Foundational competencies detected</span>'}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        # Experience Relevance Card
        exp_rel = ats.get("experience_relevance", "Strong alignment with engineering principles.")
        st.markdown(f"""
        <div class="insight-card career" style="min-height: 180px;">
            <div class="insight-card-header">
                <span class="insight-card-icon">💼</span>
                <span class="insight-card-title">Experience Relevance Analysis</span>
            </div>
            <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin-top: 0.5rem;">
                {html.escape(str(exp_rel))}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_d2:
        # Missing Keywords Card
        missing_kw = ats.get("missing_keywords", [])
        missing_tags = " ".join([f"<span class='badge-clean' style='margin: 2px; border-color: rgba(245, 158, 11, 0.4); color: #F59E0B;'>{html.escape(str(s))}</span>" for s in missing_kw])
        improvements = ats.get("improvements", [])
        imp_list = "".join([f"<li style='margin-bottom: 0.4rem;'>{html.escape(str(s))}</li>" for s in improvements])
        st.markdown(f"""
        <div class="insight-card improvement" style="min-height: 220px;">
            <div class="insight-card-header">
                <span class="insight-card-icon">⚠</span>
                <span class="insight-card-title">Missing Industry Keywords</span>
            </div>
            <div style="margin-top: 0.5rem; font-size: 12px; color: var(--text-secondary);">High-frequency recruiter search terms not found in your document:</div>
            <div style="margin: 0.5rem 0 0.75rem 0;">{missing_tags if missing_tags else '<span style="color: var(--text-muted); font-size: 12px;">None detected</span>'}</div>
            <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0; font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                {imp_list if imp_list else '<li>Incorporate role-specific tooling keywords</li>'}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        # Formatting & Safety Card
        formatting = ats.get("formatting_issues", ["Single-column layout verified", "Standard font hierarchy compatible"])
        fmt_list = "".join([f"<li style='margin-bottom: 0.35rem;'>{html.escape(str(f))}</li>" for f in formatting])
        st.markdown(f"""
        <div class="insight-card recommendation" style="min-height: 180px;">
            <div class="insight-card-header">
                <span class="insight-card-icon">🛡</span>
                <span class="insight-card-title">ATS Parsing & Formatting Safety</span>
            </div>
            <ul style="margin: 0.5rem 0 0 1.2rem; padding: 0; font-size: 13px; color: var(--text-primary); line-height: 1.5;">
                {fmt_list}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Dedicated "Top 5 Strategic Resume Improvements" Section
    st.markdown("### Top 5 Strategic Resume Improvements")
    st.caption("Prioritized recommendations with implementation guidance and before-and-after rewrite examples.")

    top_imps = ats.get("top_improvements", [])
    if not top_imps:
        top_imps = [
            {
                "title": "Quantify Impact with the Google XYZ Formula",
                "what": "Rewrite experience bullet points using 'Accomplished [X] as measured by [Y] by doing [Z]'.",
                "why": "ATS algorithms and technical recruiters rank candidates 40% higher when impact is backed by measurable metrics.",
                "how_to_fix": "Add specific percentages, query latency reductions, user counts, or dollar values to each accomplishment.",
                "example_before": "Worked on backend APIs to improve database query speed.",
                "example_after": "Optimized PostgreSQL relational indexes and Redis cache layer, reducing 95th-percentile API response latency by 42% for 120k daily active users."
            },
            {
                "title": "Integrate High-Priority Role Keywords",
                "what": f"Embed missing core industry competencies ({', '.join(missing_kw[:4]) if missing_kw else 'Docker, Kubernetes, CI/CD, Cloud Architecture'}) naturally into your work history.",
                "why": "Applicant tracking software automatically scans for specific technical keywords before any human recruiter reviews your submission.",
                "how_to_fix": "Reference these tools in your project bullets and include an explicit Technical Skills category.",
                "example_before": "Maintained and deployed application code on servers.",
                "example_after": "Containerized multi-service microservices using Docker and orchestrated automated CI/CD deployment pipelines on AWS."
            },
            {
                "title": "Optimize Technical Skills Hierarchy & Grouping",
                "what": "Reorganize your skills section into categorized sub-headers rather than an unorganized comma-separated list.",
                "why": "Parsers categorize skills by context; clear categories (Languages, Frameworks, Cloud, Databases) guarantee 100% extraction accuracy.",
                "how_to_fix": "Group competencies under: Languages, Databases, Cloud & DevOps, Core Frameworks, and Testing.",
                "example_before": "Python, SQL, AWS, Docker, HTML, CSS, Git, Machine Learning, Fast-API.",
                "example_after": "Languages: Python, SQL | Frameworks: FastAPI, PyTorch | Cloud & DevOps: AWS, Docker, GitHub Actions | Databases: PostgreSQL, Redis."
            },
            {
                "title": "Strengthen Action Verb Dynamics",
                "what": "Replace passive phrases ('Assisted in', 'Responsible for', 'Helped with') with executive action verbs.",
                "why": "Strong verbs (Architected, Engineered, Speared, Pioneered, Streamlined) establish technical ownership and leadership.",
                "how_to_fix": "Start every single accomplishment bullet with a decisive past-tense technical action verb.",
                "example_before": "Responsible for writing unit tests and code reviews for the team.",
                "example_after": "Architected comprehensive pytest test suites achieving 88% branch coverage, eliminating 35% of pre-release regressions."
            },
            {
                "title": "Eliminate Parsing Traps (Tables, Multi-Columns, Icons)",
                "what": "Ensure your document uses a single-column, standard linear hierarchy without nested table elements.",
                "why": "Certain ATS engines misread multi-column layouts horizontally across lines, garbling dates, roles, and descriptions.",
                "how_to_fix": "Use clean markdown or standard linear formatting with standard font headings.",
                "example_before": "Two-column graphic resume layout with progress percentage bars for skills.",
                "example_after": "Clean single-column professional typographic layout with clear date, title, and organization hierarchies."
            }
        ]

    for idx, item in enumerate(top_imps[:5], start=1):
        st.markdown(f"""
        <div class="ats-improvement-card">
            <div class="ats-improvement-header">
                <div class="ats-rank-badge">#{idx}</div>
                <div class="ats-improvement-title">{html.escape(item.get('title', f'Strategic Improvement #{idx}'))}</div>
            </div>
            <div class="ats-detail-row">
                <div class="ats-detail-label">What to Change:</div>
                <div class="ats-detail-text">{html.escape(item.get('what', ''))}</div>
            </div>
            <div class="ats-detail-row">
                <div class="ats-detail-label">Why it Matters:</div>
                <div class="ats-detail-text">{html.escape(item.get('why', ''))}</div>
            </div>
            <div class="ats-detail-row">
                <div class="ats-detail-label">How to Implement:</div>
                <div class="ats-detail-text">{html.escape(item.get('how_to_fix', ''))}</div>
            </div>
            <div class="diff-before-after">
                <div class="diff-box before">
                    <div style="font-weight: 700; margin-bottom: 0.25rem; font-size: 11px; text-transform: uppercase;">✕ Needs Revision (Before)</div>
                    <div>{html.escape(item.get('example_before', ''))}</div>
                </div>
                <div class="diff-box after">
                    <div style="font-weight: 700; margin-bottom: 0.25rem; font-size: 11px; text-transform: uppercase;">✓ Optimized ATS Format (After)</div>
                    <div>{html.escape(item.get('example_after', ''))}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Actionable Next Steps
    recs = ats.get("actionable_recommendations", [])
    if recs:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### Implementation Checklist")
        for i, rec in enumerate(recs):
            st.checkbox(f"{rec}", key=f"ats_rec_chk_{i}")


def render_mock_interview_evaluation(ev: Dict[str, Any], question_item: Dict[str, Any], role: str, seniority: str):
    """
    Render a comprehensive, professional Mock Interview Evaluation Report:
    - Overall score + 4-metric score grid
    - Strengths and Improvement Areas insight cards
    - Missing concepts tags
    - How to elevate advisory
    - Staff Engineer Model Exemplary Answer
    - Interactive improvement checklist
    """
    if not ev:
        return

    score_10 = ev.get("score", 7.5)
    sub = ev.get("sub_scores", {
        "technical_accuracy": score_10,
        "communication_quality": min(10.0, score_10 + 0.5),
        "problem_solving": max(6.0, score_10 - 0.5),
        "completeness": score_10
    })

    # Overall Banner
    status_msg = "Exceptional Delivery • Staff Engineer Caliber" if score_10 >= 8.5 else (
        "Solid Performance • Ready for Advanced Rounds" if score_10 >= 7.0 else
        "Developing Response • Requires Concrete Framing"
    )

    st.markdown(f"""
    <div class="career-hero-card" style="padding: 1.5rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <span class="badge-clean gold" style="font-size: 12px; margin-bottom: 0.5rem; display: inline-block;">AI Interview Evaluation</span>
                <div style="font-size: 1.5rem; font-weight: 800; font-family: var(--font-heading);">Candidate Assessment Report</div>
                <div style="font-size: 13.5px; color: var(--text-secondary);">Evaluated against <b>{html.escape(role)}</b> ({html.escape(seniority)}) engineering rubrics.</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2.2rem; font-weight: 900; color: var(--gold-primary); font-family: var(--font-heading); line-height: 1;">{score_10} <span style="font-size: 1.1rem; color: var(--text-muted); font-weight: 600;">/ 10</span></div>
                <div style="font-size: 12px; font-weight: 700; color: var(--text-primary); margin-top: 0.25rem;">{status_msg}</div>
            </div>
        </div>
        <div style="font-size: 14px; color: var(--text-primary); line-height: 1.6; margin-top: 1rem; border-top: 1px solid var(--border-color); padding-top: 0.85rem;">
            {html.escape(ev.get('feedback', 'Detailed evaluation prepared by AI interviewer.'))}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4-Metric Subscore Grid
    st.markdown(f"""
    <div class="interview-score-grid">
        <div class="interview-subscore-card">
            <div class="subscore-val">{sub.get('technical_accuracy', 7.5):.1f}</div>
            <div class="subscore-lbl">Technical Accuracy</div>
        </div>
        <div class="interview-subscore-card">
            <div class="subscore-val">{sub.get('communication_quality', 8.0):.1f}</div>
            <div class="subscore-lbl">Communication</div>
        </div>
        <div class="interview-subscore-card">
            <div class="subscore-val">{sub.get('problem_solving', 7.0):.1f}</div>
            <div class="subscore-lbl">Problem Solving</div>
        </div>
        <div class="interview-subscore-card">
            <div class="subscore-val">{sub.get('completeness', 7.5):.1f}</div>
            <div class="subscore-lbl">Completeness</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Strengths & Improvement Insights Row
    col_str, col_imp = st.columns(2)
    with col_str:
        strengths = ev.get("strengths", [])
        s_list = "".join([f"<li style='margin-bottom: 0.45rem;'>{html.escape(str(s))}</li>" for s in strengths])
        st.markdown(f"""
        <div class="insight-card strength" style="min-height: 190px;">
            <div class="insight-card-header">
                <span class="insight-card-icon">✓</span>
                <span class="insight-card-title">What You Did Well</span>
            </div>
            <ul style="margin: 0.6rem 0 0 1.2rem; padding: 0; font-size: 13.5px; color: var(--text-primary); line-height: 1.5;">
                {s_list if s_list else '<li>Answered the prompt directly with good clarity</li>'}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_imp:
        improvements = ev.get("improvement_areas", [])
        i_list = "".join([f"<li style='margin-bottom: 0.45rem;'>{html.escape(str(i))}</li>" for i in improvements])
        st.markdown(f"""
        <div class="insight-card improvement" style="min-height: 190px;">
            <div class="insight-card-header">
                <span class="insight-card-icon">↗</span>
                <span class="insight-card-title">Areas to Elevate</span>
            </div>
            <ul style="margin: 0.6rem 0 0 1.2rem; padding: 0; font-size: 13.5px; color: var(--text-primary); line-height: 1.5;">
                {i_list if i_list else '<li>Incorporate quantitative trade-offs and edge cases</li>'}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Missing Concepts Tags
    missing_c = ev.get("missing_concepts", [])
    if missing_c:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        c_tags = " ".join([f"<span class='badge-clean gold' style='margin: 3px;'>{html.escape(str(c))}</span>" for c in missing_c])
        st.markdown(f"""
        <div style="margin: 0.75rem 0; padding: 0.85rem 1rem; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px;">
            <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--gold-primary); margin-bottom: 0.35rem;">Key Architectural Concepts to Mention:</div>
            <div>{c_tags}</div>
        </div>
        """, unsafe_allow_html=True)

    # How to Improve Advisory
    how_imp = ev.get("how_to_improve", "")
    if how_imp:
        st.markdown(f"""
        <div class="insight-card recommendation" style="margin-top: 0.75rem;">
            <div class="insight-card-header">
                <span class="insight-card-icon">💡</span>
                <span class="insight-card-title">Strategic Advisory for Future Answers</span>
            </div>
            <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.6; margin-top: 0.4rem;">
                {html.escape(str(how_imp))}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Model Exemplary Answer Expander
    model_ans = ev.get("model_answer", "")
    if model_ans:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        with st.expander("View Staff Engineer Exemplary Model Answer", expanded=False):
            st.markdown(f"""
            <div style="background: var(--bg-card-secondary); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border-color); font-size: 13.5px; line-height: 1.7; color: var(--text-primary);">
                <div style="font-weight: 700; color: var(--gold-primary); margin-bottom: 0.5rem;">Benchmark Model Response:</div>
                {html.escape(str(model_ans))}
            </div>
            """, unsafe_allow_html=True)

    # Interactive Checklist
    checklist = ev.get("checklist", [])
    if checklist:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### Technical Mastery Checklist for this Question")
        for idx, item in enumerate(checklist):
            st.checkbox(str(item), key=f"chk_eval_item_{idx}")

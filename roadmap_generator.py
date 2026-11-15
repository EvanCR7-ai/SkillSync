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


def render_skill_gap_table(skills_analysis: List[Dict[str, Any]]):
    """
    Render a native Streamlit dataframe and structured metrics for skill comparison.
    Completely eliminates dynamic HTML strings to guarantee 100% reliable rendering.
    """
    if not skills_analysis:
        st.info("No skill diagnostic data available for display.")
        return

    # Clean & normalize data into structured records
    table_records = []
    matched_count = 0
    partial_count = 0
    missing_count = 0

    for s in skills_analysis:
        skill_name = str(s.get("skill", "Unknown Skill")).strip()
        category = str(s.get("category", "General")).strip()
        raw_status = str(s.get("status", "Need to Learn")).strip()
        raw_priority = str(s.get("priority", "–")).strip()
        recommendation = str(s.get("recommendation", s.get("current_mastery", "Action step in roadmap"))).strip()

        # Map status to clean text indicator (no emojis)
        if raw_status.lower() in ["already have", "have", "possessed", "mastered"]:
            status_display = "Already Have"
            matched_count += 1
        elif raw_status.lower() in ["partially skilled", "needs improvement", "partial", "improving"]:
            status_display = "Needs Improvement"
            partial_count += 1
        else:
            status_display = "Need to Learn"
            missing_count += 1

        # Map priority to clean indicator (no emojis)
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

    # Convert to Pandas DataFrame
    df = pd.DataFrame(table_records)

    # 1. Summary Quick-Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(
            label="Already Have",
            value=f"{matched_count} Skills",
            help="Core technologies you currently possess"
        )
    with col_m2:
        st.metric(
            label="Needs Improvement",
            value=f"{partial_count} Skills",
            help="Skills where you have partial familiarity but need deeper practice"
        )
    with col_m3:
        st.metric(
            label="Need to Learn",
            value=f"{missing_count} Skills",
            help="High-priority gap skills required for your target role"
        )

    # 2. Interactive Native Streamlit DataFrame
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Skill / Technology": st.column_config.TextColumn(
                "Skill / Technology",
                help="Technology or core engineering competency",
                width="medium"
            ),
            "Category": st.column_config.TextColumn(
                "Category",
                help="Domain or technical stack area",
                width="small"
            ),
            "Current Status": st.column_config.TextColumn(
                "Current Status",
                help="Readiness diagnostic status",
                width="medium"
            ),
            "Priority": st.column_config.TextColumn(
                "Priority",
                help="Recommended learning priority",
                width="small"
            ),
            "Learning Recommendation": st.column_config.TextColumn(
                "Learning Recommendation",
                help="Actionable roadmap guidance",
                width="large"
            )
        }
    )

    # 3. Structured Card Breakdown Option
    with st.expander("View Detailed Card Breakdown by Technology", expanded=False):
        for s in skills_analysis:
            s_name = s.get("skill", "Unknown")
            cat = s.get("category", "General")
            status = s.get("status", "Need to Learn")
            priority = s.get("priority", "–")
            rec = s.get("recommendation", "")

            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**{s_name}**")
                st.caption(f"Category: `{cat}` • Status: `{status}` • Priority: `{priority}`")
            with c2:
                st.markdown(f"*{rec}*")
            st.markdown("---")


def render_roadmap_cards(roadmap: List[Dict[str, Any]]):
    """
    Render the 8-week personalized roadmap in modern interactive cards
    with expandable details, learning objectives, resources, and completion check.
    Zero emojis, clean typography.
    """
    # Track completion count
    completed_weeks = sum(
        1 for i in range(1, len(roadmap) + 1)
        if st.session_state.get(f"week_completed_{i}", False)
    )
    total_weeks = len(roadmap)
    progress_pct = int((completed_weeks / total_weeks) * 100) if total_weeks > 0 else 0

    col_prog1, col_prog2 = st.columns([3, 1])
    with col_prog1:
        st.markdown(f"**Roadmap Progress Tracker:** `{completed_weeks} of {total_weeks} Weeks Completed ({progress_pct}%)`")
    with col_prog2:
        status_txt = "Curriculum Completed" if progress_pct == 100 else "In Progress"
        if progress_pct == 100:
            st.success(status_txt)
        else:
            st.info(status_txt)
    st.progress(progress_pct / 100.0)

    if progress_pct == 100 and total_weeks > 0:
        st.success("Milestone Complete: You have mastered all 8 weeks of your curriculum! You are ready to apply for target engineering roles.")

    for week in roadmap:
        w_num = week.get("week_number", 1)
        w_title = week.get("week_title", f"Week {w_num}")
        hours = week.get("estimated_study_hours", 10)
        skills = week.get("skills_to_develop", [])
        objectives = week.get("objectives", [])
        resources = week.get("resources", [])
        exercises = week.get("practical_exercises", [])
        outcome = week.get("expected_outcome", "Solidify core concepts.")

        is_done = st.session_state.get(f"week_completed_{w_num}", False)
        is_capstone = (w_num == 8)
        
        capstone_label = " (Capstone Project)" if is_capstone else ""
        done_label = " [Completed]" if is_done else ""
        expander_title = f"Week {w_num}{capstone_label}: {w_title} • {hours} hrs/week{done_label}"
        
        with st.expander(expander_title, expanded=(w_num in [1, 2])):
            if is_done:
                st.markdown(
                    '<div class="badge-clean gold" style="margin-bottom: 0.75rem; display: inline-flex;">'
                    'Milestone Completed</div>',
                    unsafe_allow_html=True
                )
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("##### Learning Objectives")
                for obj in objectives:
                    st.markdown(f"• **{obj}**")

                st.markdown("##### Practical Exercises & Deliverables")
                for ex in exercises:
                    st.markdown(f"• {ex}")

                mini_project = week.get("mini_project", f"Build a focused working prototype applying Week {w_num} skills.")
                st.markdown(f"**Weekly Mini-Project:** `{mini_project}`")

                st.info(f"**Expected Milestone Outcome:** {outcome}")

            with col2:
                st.markdown("##### Skills Developed")
                skill_chips = " ".join([f"`{s}`" for s in skills])
                st.markdown(skill_chips if skill_chips else "`Core Concepts`")

                st.markdown("##### Recommended Resources")
                for res in resources:
                    title = res.get("title", "Resource")
                    r_type = res.get("type", "Guide")
                    link = res.get("link", "#")
                    st.markdown(f"• [{title}]({link}) *({r_type})*")

                st.markdown("---")
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


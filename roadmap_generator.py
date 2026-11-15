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


def create_readiness_gauge(score: int, matched: int, partial: int, missing: int, total: int) -> go.Figure:
    """
    Generate a modern, high-tech circular gauge chart using Plotly.
    Designed with deep space midnight aesthetics (#080B16), cyan/purple glowing indicators,
    and smooth gradient thresholds.
    """
    if score >= 75:
        bar_color = "#22C55E"  # Emerald Success
    elif score >= 50:
        bar_color = "#22D3EE"  # Electric Cyan
    elif score >= 30:
        bar_color = "#F59E0B"  # Vibrant Amber
    else:
        bar_color = "#EF4444"  # Rose Danger

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            'suffix': "%",
            'font': {'size': 48, 'color': '#FFFFFF', 'family': 'Plus Jakarta Sans, sans-serif'}
        },
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "rgba(255,255,255,0.2)",
                'tickfont': {'color': '#94A3B8', 'family': 'Plus Jakarta Sans'}
            },
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "rgba(255, 255, 255, 0.04)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.12)",
            'steps': [
                {'range': [0, 35], 'color': 'rgba(239, 68, 68, 0.18)'},
                {'range': [35, 70], 'color': 'rgba(245, 158, 11, 0.18)'},
                {'range': [70, 100], 'color': 'rgba(34, 197, 94, 0.18)'}
            ],
            'threshold': {
                'line': {'color': "#8B5CF6", 'width': 3.5},
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
        font={'color': '#F8FAFC', 'family': 'Plus Jakarta Sans'}
    )
    return fig


def create_skill_breakdown_donut(matched: int, partial: int, missing: int) -> go.Figure:
    """
    Generate a sleek donut chart showing the breakdown of skills
    with modern SaaS neon palette.
    """
    labels = ['Already Have', 'Needs Improvement', 'Need to Learn']
    values = [matched, partial, missing]
    colors = ['#22C55E', '#F59E0B', '#EF4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.64,
        marker=dict(colors=colors, line=dict(color='#080B16', width=2.5)),
        textinfo='value+percent',
        hoverinfo='label+value',
        textfont=dict(color='#FFFFFF', size=12, family='Plus Jakarta Sans')
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
            font=dict(color='#94A3B8', size=11, family='Plus Jakarta Sans')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=30),
        height=230
    )
    return fig


def create_category_distribution_bar(skills_analysis: List[Dict[str, Any]]) -> go.Figure:
    """
    Generate a horizontal bar chart showing the distribution of skills across tech domains.
    """
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
        marker=dict(color='#8B5CF6')
    ))

    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=20, t=20, b=20),
        height=max(200, len(cat_names) * 38),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color='#94A3B8', size=11)
        ),
        xaxis=dict(
            title=dict(text="Number of Skills", font=dict(color='#94A3B8', size=11)),
            tickfont=dict(color='#94A3B8'),
            gridcolor='rgba(255, 255, 255, 0.06)'
        ),
        yaxis=dict(
            tickfont=dict(color='#F8FAFC', size=11),
            autorange="reversed"
        )
    )
    return fig


def create_ats_score_gauge(score: int) -> go.Figure:
    """
    Generate an ATS compatibility radial gauge chart.
    """
    if score >= 80:
        bar_color = "#22C55E"
    elif score >= 65:
        bar_color = "#22D3EE"
    elif score >= 50:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            'suffix': "%",
            'font': {'size': 44, 'color': '#FFFFFF', 'family': 'Plus Jakarta Sans'}
        },
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "rgba(255,255,255,0.2)", 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': bar_color, 'thickness': 0.35},
            'bgcolor': "rgba(255, 255, 255, 0.04)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.12)",
            'threshold': {'line': {'color': "#8B5CF6", 'width': 3}, 'thickness': 0.8, 'value': score}
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=210,
        font={'color': '#F8FAFC'}
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

        # Map status to colored visual indicator
        if raw_status.lower() in ["already have", "have", "possessed", "mastered"]:
            status_display = "🟢 Already Have"
            matched_count += 1
        elif raw_status.lower() in ["partially skilled", "needs improvement", "partial", "improving"]:
            status_display = "🟡 Needs Improvement"
            partial_count += 1
        else:
            status_display = "🔴 Need to Learn"
            missing_count += 1

        # Map priority to clean indicator
        p_lower = raw_priority.lower()
        if "high" in p_lower:
            priority_display = "🔥 High"
        elif "med" in p_lower:
            priority_display = "⚡ Medium"
        elif "low" in p_lower:
            priority_display = "🌱 Low"
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
            label="🟢 Already Have",
            value=f"{matched_count} Skills",
            help="Core technologies you currently possess"
        )
    with col_m2:
        st.metric(
            label="🟡 Needs Improvement",
            value=f"{partial_count} Skills",
            help="Skills where you have partial familiarity but need deeper practice"
        )
    with col_m3:
        st.metric(
            label="🔴 Need to Learn",
            value=f"{missing_count} Skills",
            help="High-priority gap skills required for your target role"
        )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

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


def render_roadmap_cards(roadmap: List[Dict[str, Any]]):
    """
    Render the 8-week personalized roadmap in modern interactive cards
    with expandable details, learning objectives, resources, and completion check.
    """
    # Track completion count
    completed_weeks = sum(
        1 for i in range(1, len(roadmap) + 1)
        if st.session_state.get(f"week_completed_{i}", False)
    )
    total_weeks = len(roadmap)
    progress_pct = int((completed_weeks / total_weeks) * 100) if total_weeks > 0 else 0

    progress_html = (
        '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; padding: 0.75rem 1rem; background: rgba(14, 20, 36, 0.6); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">'
        '<div>'
        '<span style="font-weight: 700; color: #FFFFFF; font-size: 0.95rem;">Roadmap Progress Tracker:</span>'
        f'<span style="color: #38BDF8; font-weight: 600; margin-left: 0.5rem;">{completed_weeks} of {total_weeks} Weeks Completed ({progress_pct}%)</span>'
        '</div>'
        '<span class="badge" style="background: rgba(99, 102, 241, 0.18); color: #A78BFA; border: 1px solid rgba(99, 102, 241, 0.4);">'
        f'{"🎉 Curriculum Finished!" if progress_pct == 100 else "🚀 In Progress"}'
        '</span>'
        '</div>'
    )
    utils.safe_render_html(progress_html)
    st.progress(progress_pct / 100.0)

    utils.safe_render_html("<div style='height: 12px;'></div>")

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
        
        status_icon = "✅" if is_done else ("🏆" if is_capstone else "📅")
        pill_label = f"{status_icon} Week {w_num}{' (Capstone)' if is_capstone else ''}"

        expander_title = f"{pill_label}: {w_title} • {hours} hrs/week"
        
        with st.expander(expander_title, expanded=(w_num in [1, 2])):
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("##### 🎯 Learning Objectives")
                for obj in objectives:
                    st.markdown(f"• **{obj}**")

                st.markdown("##### 🛠️ Practical Exercises & Tasks")
                for ex in exercises:
                    st.markdown(f"💻 {ex}")

                mini_project = week.get("mini_project", f"Build a focused working prototype applying Week {w_num} skills.")
                st.markdown(f"🚀 **Weekly Mini-Project:** `{mini_project}`")

                outcome_html = (
                    '<div style="margin-top: 1rem; padding: 0.75rem 1rem; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38BDF8; border-radius: 8px;">'
                    '<span style="font-size: 0.78rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.04em;">Expected Milestone Outcome:</span><br/>'
                    f'<span style="font-size: 0.92rem; color: #E2E8F0; line-height: 1.5;">{html.escape(outcome)}</span>'
                    '</div>'
                )
                utils.safe_render_html(outcome_html)

            with col2:
                st.markdown("##### 🧠 Skills Developed")
                skill_tags_html = "".join([f'<span class="skill-tag">{html.escape(s)}</span>' for s in skills])
                utils.safe_render_html(f'<div style="margin-bottom: 1.25rem;">{skill_tags_html}</div>')

                st.markdown("##### 📚 Recommended Resources")
                for res in resources:
                    title = html.escape(res.get("title", "Resource"))
                    r_type = html.escape(res.get("type", "Guide"))
                    link = html.escape(res.get("link", "#"))
                    res_html = (
                        '<div style="margin-bottom: 0.5rem;">'
                        f'<a href="{link}" target="_blank" style="color: #00D2FF; font-weight: 600; text-decoration: none;">'
                        f'🔗 {title}'
                        '</a>'
                        f'<span style="font-size: 0.75rem; color: #94A3B8; margin-left: 0.35rem;">({r_type})</span>'
                        '</div>'
                    )
                    utils.safe_render_html(res_html)

                st.markdown("---")
                st.checkbox(
                    "Mark Week Completed",
                    key=f"week_completed_{w_num}",
                    value=is_done,
                    help="Check off this milestone as you complete your weekly exercises."
                )



def render_portfolio_projects(projects: List[Dict[str, Any]]):
    """
    Render portfolio projects in visual-first presentation with live interactive previews
    and optional developer tools / source code.
    """
    project_preview_engine.render_all_portfolio_projects(projects)


render_vertical_timeline = render_roadmap_cards


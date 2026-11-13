"""
SkillSync - Roadmap & Dashboard Visual Generator
Handles rendering of the skill gap dashboard, Plotly readiness gauges,
interactive weekly roadmap timeline, and portfolio project cards.
"""

from typing import Dict, List, Any
import plotly.graph_objects as go
import streamlit as st


def create_readiness_gauge(score: int, matched: int, partial: int, missing: int, total: int) -> go.Figure:
    """
    Generate a modern, high-tech circular gauge chart using Plotly.
    Designed with dark navy aesthetics and cyan/purple glowing indicators.
    """
    # Dynamic bar color based on score
    if score >= 75:
        bar_color = "#10B981"  # Emerald
    elif score >= 50:
        bar_color = "#38BDF8"  # Electric Blue
    elif score >= 30:
        bar_color = "#F59E0B"  # Amber
    else:
        bar_color = "#EF4444"  # Rose

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "%", 'font': {'size': 44, 'color': '#FFFFFF', 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.2)", 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': bar_color, 'thickness': 0.28},
            'bgcolor': "rgba(255, 255, 255, 0.05)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 35], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [35, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': "#A855F7", 'width': 3},
                'thickness': 0.8,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=25, b=20),
        height=220,
        font={'color': '#F8FAFC', 'family': 'Plus Jakarta Sans'}
    )
    return fig


def create_skill_breakdown_donut(matched: int, partial: int, missing: int) -> go.Figure:
    """
    Generate a sleek donut chart showing the breakdown of skills.
    """
    labels = ['Already Have', 'Partially Skilled', 'Need to Learn']
    values = [matched, partial, missing]
    colors = ['#10B981', '#F59E0B', '#EF4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color='#0A0D17', width=2)),
        textinfo='value+percent',
        hoverinfo='label+value',
        textfont=dict(color='#FFFFFF', size=12)
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color='#94A3B8', size=11)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=30),
        height=220
    )
    return fig


def render_skill_gap_table(skills_analysis: List[Dict[str, Any]]):
    """
    Render an attractive HTML table displaying the required skills,
    current status, learning priority, and recommendations with visual badges.
    """
    rows_html = ""
    for s in skills_analysis:
        skill = s.get("skill", "Skill")
        category = s.get("category", "General")
        status = s.get("status", "Need to Learn")
        priority = s.get("priority", "-")
        recommendation = s.get("recommendation", "")

        # Status badge
        if status == "Already Have":
            status_badge = '<span class="badge badge-have">✓ Already Have</span>'
        elif status == "Partially Skilled":
            status_badge = '<span class="badge badge-partial">⚡ Partially Skilled</span>'
        else:
            status_badge = '<span class="badge badge-learn">✕ Need to Learn</span>'

        # Priority badge
        if priority == "High":
            priority_badge = '<span class="badge badge-priority-high">High Priority</span>'
        elif priority == "Medium":
            priority_badge = '<span class="badge badge-priority-medium">Medium</span>'
        elif priority == "Low":
            priority_badge = '<span class="badge badge-priority-low">Low</span>'
        else:
            priority_badge = '<span style="color: var(--text-muted); font-weight: 500;">—</span>'

        rows_html += f"""
        <tr>
            <td style="font-weight: 600; color: #FFFFFF;">
                {skill}
                <div style="font-size: 0.75rem; color: #64748B; font-weight: 400; margin-top: 2px;">{category}</div>
            </td>
            <td>{status_badge}</td>
            <td>{priority_badge}</td>
            <td style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.45;">{recommendation}</td>
        </tr>
        """

    table_html = f"""
    <div style="overflow-x: auto; margin-top: 1rem;">
        <table class="custom-table">
            <thead>
                <tr>
                    <th style="width: 24%;">Required Skill & Category</th>
                    <th style="width: 18%;">Current Status</th>
                    <th style="width: 15%;">Priority</th>
                    <th style="width: 43%;">Personalized Recommendation</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)


def render_roadmap_cards(roadmap: List[Dict[str, Any]]):
    """
    Render the 8-week personalized roadmap in modern interactive cards.
    """
    for week in roadmap:
        w_num = week.get("week_number", 1)
        w_title = week.get("week_title", f"Week {w_num}")
        hours = week.get("estimated_study_hours", 10)
        skills = week.get("skills_to_develop", [])
        objectives = week.get("objectives", [])
        resources = week.get("resources", [])
        exercises = week.get("practical_exercises", [])
        outcome = week.get("expected_outcome", "Solidify core concepts.")

        # Capstone highlight for week 8
        is_capstone = (w_num == 8)
        border_color = "rgba(236, 72, 153, 0.45)" if is_capstone else "rgba(139, 92, 246, 0.25)"
        pill_label = f"🏆 Week {w_num}: Final Capstone" if is_capstone else f"📅 Week {w_num}"

        expander_title = f"{pill_label} — {w_title} ({hours} hrs)"
        
        with st.expander(expander_title, expanded=(w_num in [1, 2])):
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("##### 🎯 Learning Objectives")
                for obj in objectives:
                    st.markdown(f"• **{obj}**")

                st.markdown("##### 🛠️ Practical Exercises & Tasks")
                for ex in exercises:
                    st.markdown(f"💻 {ex}")

                st.markdown(f"""
                <div style="margin-top: 1rem; padding: 0.65rem 1rem; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38BDF8; border-radius: 6px;">
                    <span style="font-size: 0.8rem; font-weight: 700; color: #38BDF8; text-transform: uppercase;">Expected Milestone Outcome:</span><br/>
                    <span style="font-size: 0.9rem; color: #E2E8F0;">{outcome}</span>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("##### 🧠 Skills Developed")
                skill_tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
                st.markdown(f'<div style="margin-bottom: 1rem;">{skill_tags_html}</div>', unsafe_allow_html=True)

                st.markdown("##### 📚 Recommended Resources")
                for res in resources:
                    title = res.get("title", "Resource")
                    r_type = res.get("type", "Guide")
                    link = res.get("link", "#")
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem;">
                        <a href="{link}" target="_blank" style="color: #A855F7; font-weight: 600; text-decoration: none;">
                            🔗 {title}
                        </a>
                        <span style="font-size: 0.75rem; color: #94A3B8; margin-left: 0.35rem;">({r_type})</span>
                    </div>
                    """, unsafe_allow_html=True)


def render_portfolio_projects(projects: List[Dict[str, Any]]):
    """
    Render the 3 portfolio projects (Beginner, Intermediate, Advanced) in a 3-column SaaS card grid.
    """
    cols = st.columns(3)

    for idx, p in enumerate(projects):
        diff = p.get("difficulty", "Intermediate").capitalize()
        title = p.get("title", f"Project {idx+1}")
        desc = p.get("short_description", "")
        problem = p.get("problem_solved", "")
        techs = p.get("technologies_required", [])
        skills_demo = p.get("skills_demonstrated", [])
        time_est = p.get("estimated_completion_time", "1-2 weeks")
        final_output = p.get("expected_final_output", "GitHub repository with live demo")

        diff_class = diff.lower()
        if diff_class not in ["beginner", "intermediate", "advanced"]:
            diff_class = "intermediate"

        tech_pills = "".join([f'<span class="skill-tag" style="background: rgba(139, 92, 246, 0.15); border-color: rgba(139, 92, 246, 0.3);">{t}</span>' for t in techs])
        skill_pills = "".join([f'<span class="skill-tag">{s}</span>' for s in skills_demo])

        with cols[idx]:
            card_html = f"""
            <div class="project-card {diff_class}">
                <div>
                    <div class="project-difficulty {diff_class}">
                        ● {diff} Level Project • {time_est}
                    </div>
                    <div class="project-title">{title}</div>
                    <div class="project-desc">{desc}</div>
                    
                    <div class="project-section-title">Problem Solved</div>
                    <div style="font-size: 0.86rem; color: #CBD5E1; margin-bottom: 0.75rem;">
                        {problem}
                    </div>

                    <div class="project-section-title">Technologies Required</div>
                    <div style="margin-bottom: 0.75rem;">{tech_pills}</div>

                    <div class="project-section-title">Skills Demonstrated</div>
                    <div style="margin-bottom: 0.75rem;">{skill_pills}</div>
                </div>

                <div style="margin-top: 1rem; padding-top: 0.85rem; border-top: 1px solid rgba(255,255,255,0.08);">
                    <div style="font-size: 0.75rem; text-transform: uppercase; color: #38BDF8; font-weight: 700;">
                        Deliverable / Output
                    </div>
                    <div style="font-size: 0.85rem; color: #F8FAFC; margin-top: 2px;">
                        📦 {final_output}
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

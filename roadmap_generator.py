"""
SkillSync 2.0 - Roadmap & Dashboard Visual Generator
Handles rendering of the futuristic skill gap dashboard, Plotly readiness gauges,
interactive 8-week roadmap milestone cards, and portfolio project blueprints.
"""

from typing import Dict, List, Any
import plotly.graph_objects as go
import streamlit as st


def create_readiness_gauge(score: int, matched: int, partial: int, missing: int, total: int) -> go.Figure:
    """
    Generate a modern, high-tech circular gauge chart using Plotly.
    Designed with deep space midnight aesthetics, cyan/violet glowing indicators,
    and smooth gradient thresholds.
    """
    if score >= 75:
        bar_color = "#10B981"  # Emerald
    elif score >= 50:
        bar_color = "#00D2FF"  # Electric Cyan
    elif score >= 30:
        bar_color = "#F59E0B"  # Vibrant Amber
    else:
        bar_color = "#EF4444"  # Rose

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
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.18)'}
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
    labels = ['Already Have', 'Partially Skilled', 'Need to Learn']
    values = [matched, partial, missing]
    colors = ['#10B981', '#F59E0B', '#EF4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.64,
        marker=dict(colors=colors, line=dict(color='#070A13', width=2.5)),
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
            <td style="font-weight: 700; color: #FFFFFF;">
                {skill}
                <div style="font-size: 0.78rem; color: #94A3B8; font-weight: 500; margin-top: 3px;">{category}</div>
            </td>
            <td>{status_badge}</td>
            <td>{priority_badge}</td>
            <td style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.5;">{recommendation}</td>
        </tr>
        """

    table_html = f"""
    <div style="overflow-x: auto; margin-top: 1rem;">
        <table class="custom-table">
            <thead>
                <tr>
                    <th style="width: 26%;">Required Skill & Category</th>
                    <th style="width: 18%;">Current Status</th>
                    <th style="width: 15%;">Priority</th>
                    <th style="width: 41%;">Personalized Recommendation</th>
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

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; padding: 0.75rem 1rem; background: rgba(14, 20, 36, 0.6); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
        <div>
            <span style="font-weight: 700; color: #FFFFFF; font-size: 0.95rem;">Roadmap Progress Tracker:</span>
            <span style="color: #38BDF8; font-weight: 600; margin-left: 0.5rem;">{completed_weeks} of {total_weeks} Weeks Completed ({progress_pct}%)</span>
        </div>
        <span class="badge" style="background: rgba(99, 102, 241, 0.18); color: #A78BFA; border: 1px solid rgba(99, 102, 241, 0.4);">
            {'🎉 Curriculum Finished!' if progress_pct == 100 else '🚀 In Progress'}
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress_pct / 100.0)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

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

                st.markdown(f"""
                <div style="margin-top: 1rem; padding: 0.75rem 1rem; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38BDF8; border-radius: 8px;">
                    <span style="font-size: 0.78rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.04em;">Expected Milestone Outcome:</span><br/>
                    <span style="font-size: 0.92rem; color: #E2E8F0; line-height: 1.5;">{outcome}</span>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("##### 🧠 Skills Developed")
                skill_tags_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
                st.markdown(f'<div style="margin-bottom: 1.25rem;">{skill_tags_html}</div>', unsafe_allow_html=True)

                st.markdown("##### 📚 Recommended Resources")
                for res in resources:
                    title = res.get("title", "Resource")
                    r_type = res.get("type", "Guide")
                    link = res.get("link", "#")
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem;">
                        <a href="{link}" target="_blank" style="color: #00D2FF; font-weight: 600; text-decoration: none;">
                            🔗 {title}
                        </a>
                        <span style="font-size: 0.75rem; color: #94A3B8; margin-left: 0.35rem;">({r_type})</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.checkbox(
                    "Mark Week Completed",
                    key=f"week_completed_{w_num}",
                    value=is_done,
                    help="Check off this milestone as you complete your weekly exercises."
                )


def render_portfolio_projects(projects: List[Dict[str, Any]]):
    """
    Render the 3 portfolio projects (Beginner, Intermediate, Advanced) in a 3-column SaaS card grid.
    Code snippets are cleanly housed in collapsed optional expanders.
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
                    <div style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0.85rem; line-height: 1.5;">
                        {problem}
                    </div>

                    <div class="project-section-title">Technologies Required</div>
                    <div style="margin-bottom: 0.85rem;">{tech_pills}</div>

                    <div class="project-section-title">Skills Demonstrated</div>
                    <div style="margin-bottom: 0.85rem;">{skill_pills}</div>
                </div>

                <div style="margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.08);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: #00D2FF; font-weight: 700; letter-spacing: 0.05em;">
                        Deliverable / Output
                    </div>
                    <div style="font-size: 0.88rem; color: #F8FAFC; margin-top: 3px; font-weight: 500;">
                        📦 {final_output}
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # Optional Collapsed Architecture / Code Snippet Expander
            with st.expander("💻 View Architecture & Code Blueprint", expanded=False):
                tech_list_str = ", ".join(techs[:4]) if techs else "Python"
                st.markdown(f"**Recommended Project Structure ({diff} Tier):**")
                st.code(f"""# Project: {title}
# Stack: {tech_list_str}

├── src/
│   ├── app.py           # Core logic / API endpoint
│   ├── models/          # Data schemas & business logic
│   └── utils/           # Helper scripts & data pipelines
├── tests/
│   └── test_core.py     # Unit verification tests
├── requirements.txt     # Dependencies
└── README.md            # Architecture & deployment docs
""", language="text")
                st.caption(f"Tip: Build with clean commits and deploy to Streamlit/Docker for recruiter impact.")

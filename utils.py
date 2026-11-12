"""
SkillSync | CareerPath AI - Utilities
Input validation, CSV export, PDF export, Plotly visualizations, and session state management.
"""

import io
import csv
from typing import List, Dict, Any, Tuple, Optional

# Check if Plotly is available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Check if ReportLab is available
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


# ==============================================================================
# Input Validation
# ==============================================================================

VALID_HOURS_OPTIONS = ["3–5", "5–10", "10–15", "15–20", "20+"]
VALID_EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]
PRESET_ROLES = [
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
    "Other (Custom Role)"
]


def validate_user_inputs(
    current_skills: List[str],
    selected_role: str,
    custom_role: str,
    weekly_hours: str,
    experience_level: str
) -> Tuple[bool, str, str]:
    """
    Validates user form inputs.
    Returns: (is_valid: bool, error_message: str, resolved_role: str)
    """
    # Validate target role
    resolved_role = selected_role
    if selected_role == "Other (Custom Role)":
        if not custom_role or not custom_role.strip():
            return False, "Please specify your custom target career role.", ""
        resolved_role = custom_role.strip()
    elif not selected_role or selected_role == "Select a role...":
        return False, "Please choose your target career role from the dropdown.", ""

    # Validate current skills
    cleaned_skills = [s.strip() for s in current_skills if s and s.strip()]
    if not cleaned_skills:
        return False, "Please enter or select at least one of your current skills.", ""

    # Validate weekly hours
    if not weekly_hours:
        return False, "Please select your available weekly study hours.", ""

    # Validate experience level
    if not experience_level:
        return False, "Please select your current professional/academic experience level.", ""

    return True, "", resolved_role


# ==============================================================================
# CSV Generation for Skill Gap Analysis
# ==============================================================================

def generate_skills_csv(skills_analysis: List[Dict[str, Any]], target_role: str) -> str:
    """
    Exports the skill gap analysis to a formatted CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Metadata Header
    writer.writerow(["# SkillSync | CareerPath AI - Skill Gap Analysis Report"])
    writer.writerow(["# Target Role", target_role])
    writer.writerow([])

    # Table Header
    headers = [
        "Required Skill",
        "Current Status",
        "Priority",
        "Category",
        "Recommendation",
        "Recommended Resource",
        "Practice Exercise"
    ]
    writer.writerow(headers)

    # Data Rows
    for s in skills_analysis:
        writer.writerow([
            s.get("skill_name", ""),
            s.get("status", ""),
            s.get("priority", ""),
            s.get("category", ""),
            s.get("recommendation", ""),
            s.get("recommended_resource", ""),
            s.get("practice_exercise", "")
        ])

    return output.getvalue()


# ==============================================================================
# PDF Roadmap & Career Mentor Report Generation
# ==============================================================================

def _generate_reportlab_pdf(
    summary: Dict[str, Any],
    skills_analysis: List[Dict[str, Any]],
    roadmap_weeks: List[Dict[str, Any]],
    projects: List[Dict[str, Any]]
) -> bytes:
    """Generates a styled PDF using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=12
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )
    quote_style = ParagraphStyle(
        'MentorQuote',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#4338ca'),
        backColor=colors.HexColor('#f5f3ff'),
        borderColor=colors.HexColor('#a78bfa'),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=10
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("SkillSync | CareerPath AI – Career Roadmap Report", title_style))
    story.append(Paragraph("Your Skills Today. Your Dream Career Tomorrow.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

    # Candidate Profile & Readiness Score Box
    role = summary.get("target_role", "Engineering Role")
    score = summary.get("overall_fit_percentage", 0)
    verdict = summary.get("readiness_verdict", "In Progress")
    hours = summary.get("weekly_hours", "10-15")
    exp = summary.get("experience_level", "Beginner")

    profile_data = [
        [
            Paragraph(f"<b>Target Role:</b> {role}", body_style),
            Paragraph(f"<b>Readiness Score:</b> <font color='#6366f1'><b>{score}%</b></font>", body_style)
        ],
        [
            Paragraph(f"<b>Experience Level:</b> {exp}", body_style),
            Paragraph(f"<b>Weekly Commitment:</b> {hours} hrs/week", body_style)
        ],
        [
            Paragraph(f"<b>Assessment Verdict:</b> {verdict}", body_style),
            Paragraph(f"<b>Skills Breakdown:</b> {summary.get('matched_count', 0)} Matched | {summary.get('partial_count', 0)} Partial | {summary.get('missing_count', 0)} Missing", body_style)
        ]
    ]
    profile_table = Table(profile_data, colWidths=[260, 260])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 10))

    # Motivational Quote
    quote = summary.get("motivational_message", "Consistency in focused learning delivers remarkable career transformations.")
    story.append(Paragraph(f'"{quote}"', quote_style))

    # Section 1: Skill Gap Analysis
    story.append(Paragraph("1. Skill Gap Analysis Summary", section_heading))
    table_rows = [
        [
            Paragraph("<b>Required Skill</b>", bold_body),
            Paragraph("<b>Status</b>", bold_body),
            Paragraph("<b>Priority</b>", bold_body),
            Paragraph("<b>Recommendation</b>", bold_body)
        ]
    ]

    for s in skills_analysis[:8]:  # Limit top 8 for clean single-page flow
        status = s.get("status", "Missing")
        if status.lower() == "matched":
            status_color = "#059669"
        elif status.lower() == "partial":
            status_color = "#d97706"
        else:
            status_color = "#dc2626"

        table_rows.append([
            Paragraph(s.get("skill_name", ""), body_style),
            Paragraph(f"<font color='{status_color}'><b>{status}</b></font>", body_style),
            Paragraph(s.get("priority", "Medium"), body_style),
            Paragraph(s.get("recommendation", "")[:90] + "...", body_style)
        ])

    skills_table = Table(table_rows, colWidths=[120, 60, 60, 280])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e7ff')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 12))

    # Section 2: 8-Week Learning Roadmap
    story.append(Paragraph("2. 8-Week Personalized Learning Roadmap", section_heading))
    for w in roadmap_weeks:
        w_num = w.get("week_number", 1)
        w_topic = w.get("topic", "")
        w_hours = w.get("estimated_hours", "")
        objs = "; ".join(w.get("objectives", []))[:140]
        exs = "; ".join(w.get("exercises", []))[:120]

        cap_prefix = "[CAPSTONE] " if w.get("is_capstone") else ""
        story.append(Paragraph(f"<b>Week {w_num}: {cap_prefix}{w_topic}</b> ({w_hours})", bold_body))
        story.append(Paragraph(f"• <i>Objectives:</i> {objs}", body_style))
        story.append(Paragraph(f"• <i>Practical Lab:</i> {exs}", body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))

    # Section 3: Portfolio Projects
    story.append(Paragraph("3. Recommended GitHub Portfolio Projects", section_heading))
    for p in projects:
        diff = p.get("difficulty", "Level")
        p_title = p.get("title", "")
        p_desc = p.get("description", "")
        techs = ", ".join(p.get("technologies", []))
        story.append(Paragraph(f"<b>[{diff}] {p_title}</b>", bold_body))
        story.append(Paragraph(f"{p_desc} (<b>Tech Stack:</b> {techs})", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _generate_fallback_pdf(
    summary: Dict[str, Any],
    skills_analysis: List[Dict[str, Any]],
    roadmap_weeks: List[Dict[str, Any]],
    projects: List[Dict[str, Any]]
) -> bytes:
    """
    Pure Python minimal valid PDF-1.4 generator fallback.
    Guarantees PDF export works even when reportlab is not installed!
    """
    lines = []
    lines.append("SkillSync | CareerPath AI - Career Roadmap Report")
    lines.append("=" * 60)
    lines.append(f"Target Role: {summary.get('target_role', 'Engineering')}")
    lines.append(f"Readiness Score: {summary.get('overall_fit_percentage', 0)}%")
    lines.append(f"Verdict: {summary.get('readiness_verdict', 'In Progress')}")
    lines.append(f"Weekly Commitment: {summary.get('weekly_hours', '10-15')} hours/week")
    lines.append(f"Experience Level: {summary.get('experience_level', 'Beginner')}")
    lines.append("-" * 60)
    lines.append(f"Mentor Note: \"{summary.get('motivational_message', '')}\"")
    lines.append("=" * 60)
    lines.append("\n1. SKILL GAP ANALYSIS:")
    for s in skills_analysis:
        lines.append(f"  [{s.get('status', 'N/A')}] {s.get('skill_name', '')} (Priority: {s.get('priority', 'Medium')})")
        lines.append(f"    Rec: {s.get('recommendation', '')}")

    lines.append("\n2. 8-WEEK PERSONALIZED ROADMAP:")
    for w in roadmap_weeks:
        lines.append(f"  Week {w.get('week_number', '')}: {w.get('topic', '')} ({w.get('estimated_hours', '')})")
        for obj in w.get("objectives", []):
            lines.append(f"    - Objective: {obj}")
        for ex in w.get("exercises", []):
            lines.append(f"    - Exercise: {ex}")

    lines.append("\n3. PORTFOLIO PROJECTS:")
    for p in projects:
        lines.append(f"  [{p.get('difficulty', '')}] {p.get('title', '')}")
        lines.append(f"    Description: {p.get('description', '')}")
        lines.append(f"    Technologies: {', '.join(p.get('technologies', []))}")

    text_content = "\n".join(lines)

    # Convert text content to valid PDF stream
    text_escaped = text_content.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    
    # Split into lines for PostScript positioning
    stream_ops = ["BT", "/F1 9 Tf", "40 750 Td", "11 TL"]
    for l in text_escaped.split("\n"):
        # Truncate overly long lines for PDF width
        truncated = l[:95]
        stream_ops.append(f"({truncated}) '")
    stream_ops.append("ET")
    stream_data = "\n".join(stream_ops).encode("latin-1", "replace")

    stream_len = len(stream_data)

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n")
    pdf.extend(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    pdf.extend(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    pdf.extend(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n")
    pdf.extend(f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode("ascii"))
    pdf.extend(stream_data)
    pdf.extend(b"\nendstream\nendobj\n")
    pdf.extend(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n")
    pdf.extend(b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000224 00000 n \n0000000300 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n360\n%%EOF\n")

    return bytes(pdf)


def generate_pdf_roadmap(
    summary: Dict[str, Any],
    skills_analysis: List[Dict[str, Any]],
    roadmap_weeks: List[Dict[str, Any]],
    projects: List[Dict[str, Any]]
) -> bytes:
    """
    Main PDF export entry point.
    Uses ReportLab if installed, otherwise uses pure Python fallback.
    """
    if HAS_REPORTLAB:
        try:
            return _generate_reportlab_pdf(summary, skills_analysis, roadmap_weeks, projects)
        except Exception:
            return _generate_fallback_pdf(summary, skills_analysis, roadmap_weeks, projects)
    return _generate_fallback_pdf(summary, skills_analysis, roadmap_weeks, projects)


# ==============================================================================
# Plotly Chart Visualizations
# ==============================================================================

def create_readiness_gauge(score: float, verdict: str) -> Any:
    """
    Creates a radial gauge indicator for the candidate's mathematical readiness score.
    """
    if not HAS_PLOTLY:
        return None

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "%", 'font': {'color': "#ffffff", 'size': 38, 'family': 'Plus Jakarta Sans'}},
        title={'text': f"<b>Career Readiness Index</b><br><span style='font-size:12px;color:#94a3b8'>{verdict}</span>", 'font': {'size': 14, 'color': "#cbd5e1"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#8b5cf6", 'thickness': 0.3},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'borderwidth': 1,
            'bordercolor': "rgba(139, 92, 246, 0.3)",
            'steps': [
                {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.25)"},
                {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.25)"},
                {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.25)"}
            ],
            'threshold': {
                'line': {'color': "#38bdf8", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#f8fafc", 'family': 'Plus Jakarta Sans'},
        height=240,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_status_donut_chart(matched: int, partial: int, missing: int) -> Any:
    """
    Creates a donut chart displaying the breakdown of Matched, Partial, and Missing skills.
    """
    if not HAS_PLOTLY:
        return None

    labels = ["Matched (Have)", "Partial (Bridge)", "Missing (Acquire)"]
    values = [matched, partial, missing]
    colors_list = ["#10b981", "#f59e0b", "#ef4444"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors_list, line=dict(color="#0b0f19", width=2)),
        textinfo='label+value',
        textfont=dict(color="#ffffff", size=11, family='Plus Jakarta Sans'),
        hoverinfo='label+percent+value'
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=240,
        margin=dict(l=10, r=10, t=30, b=10),
        annotations=[dict(text=f"<b>{matched+partial+missing}</b><br>Skills", x=0.5, y=0.5, font_size=16, font_color="#ffffff", showarrow=False)]
    )
    return fig


def create_priority_distribution_chart(skills_analysis: List[Dict[str, Any]]) -> Any:
    """
    Creates a stacked bar chart mapping Priority (High/Medium/Low) against Skill Status.
    """
    if not HAS_PLOTLY:
        return None

    # Count frequencies
    matrix = {
        "High": {"Matched": 0, "Partial": 0, "Missing": 0},
        "Medium": {"Matched": 0, "Partial": 0, "Missing": 0},
        "Low": {"Matched": 0, "Partial": 0, "Missing": 0}
    }

    for s in skills_analysis:
        p = s.get("priority", "Medium")
        if p not in matrix:
            p = "Medium"
        st = s.get("status", "Missing")
        if st not in ["Matched", "Partial", "Missing"]:
            st = "Missing"
        matrix[p][st] += 1

    priorities = ["High", "Medium", "Low"]
    matched_vals = [matrix[p]["Matched"] for p in priorities]
    partial_vals = [matrix[p]["Partial"] for p in priorities]
    missing_vals = [matrix[p]["Missing"] for p in priorities]

    fig = go.Figure(data=[
        go.Bar(name='Matched', x=priorities, y=matched_vals, marker_color='#10b981'),
        go.Bar(name='Partial', x=priorities, y=partial_vals, marker_color='#f59e0b'),
        go.Bar(name='Missing', x=priorities, y=missing_vals, marker_color='#ef4444')
    ])

    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#94a3b8", family='Plus Jakarta Sans', size=11),
        height=240,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#f8fafc", size=10)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=dict(text="Competency Priority", font=dict(color="#cbd5e1", size=12))),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=dict(text="Skill Count", font=dict(color="#cbd5e1", size=12)))
    )
    return fig

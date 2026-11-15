"""
SkillSync - Utility Functions
Handles PDF report generation, CSV export, validation, and analytics calculations.
"""

import io
import re
from typing import Dict, List, Any, Tuple
import pandas as pd

# ReportLab imports for professional PDF generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

import textwrap
import streamlit as st


def safe_render_html(html_str: str):
    """
    Safely render HTML in Streamlit without the CommonMark parser
    misinterpreting leading whitespace as indented preformatted code blocks.
    Uses st.html when available (Streamlit 1.34+), or clean unindented st.markdown.
    """
    clean_html = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)


def sanitize_input(text: str) -> str:
    """Strip dangerous characters and extra whitespace."""
    if not text:
        return ""
    return re.sub(r'[<>{}]', '', text.strip())


def validate_user_inputs(
    skills_list: List[str],
    custom_skills: str,
    target_role: str,
    custom_role: str,
    study_hours: str,
    experience_level: str
) -> Tuple[bool, str, List[str], str]:
    """
    Validate all inputs before passing to AI engine.
    Returns: (is_valid, error_message, combined_skills_list, resolved_role)
    """
    # Combine skills
    combined = list(skills_list)
    if custom_skills:
        for s in custom_skills.split(','):
            clean_s = sanitize_input(s)
            if clean_s and clean_s not in combined:
                combined.append(clean_s)

    if not combined:
        return False, "Please select or enter at least one current skill.", [], ""

    # Resolve target role
    final_role = target_role
    if target_role == "Custom Role..." or not target_role:
        final_role = sanitize_input(custom_role)
        if not final_role:
            return False, "Please specify your custom target career role.", [], ""
    
    if not study_hours:
        return False, "Please select your weekly study availability.", [], ""

    if not experience_level:
        return False, "Please select your current experience level.", [], ""

    return True, "", combined, final_role


def calculate_skill_readiness(skills_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate mathematical readiness score from structured skills analysis.
    Ensures consistent, reproducible scoring rather than hallucinated numbers.
    """
    total = len(skills_analysis)
    if total == 0:
        return {
            "score": 0,
            "matched": 0,
            "partial": 0,
            "missing": 0,
            "total": 0,
            "category": "Initial Assessment"
        }

    matched = sum(1 for s in skills_analysis if s.get("status") == "Already Have")
    partial = sum(1 for s in skills_analysis if s.get("status") == "Partially Skilled")
    missing = sum(1 for s in skills_analysis if s.get("status") == "Need to Learn")

    # Weighted calculation: Matched = 100%, Partial = 50%, Missing = 0%
    score = round(((matched * 1.0 + partial * 0.5) / total) * 100)
    score = max(5, min(100, score))  # keep between 5 and 100

    if score >= 80:
        category = "Career Ready / Advanced Match"
    elif score >= 55:
        category = "Strong Foundation / Mid-Level Gap"
    elif score >= 30:
        category = "Emerging Potential / Moderate Gap"
    else:
        category = "Foundational Stage / Substantial Gap"

    return {
        "score": score,
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "total": total,
        "category": category
    }


def export_skill_gap_to_csv(skills_analysis: List[Dict[str, Any]]) -> bytes:
    """Generate CSV bytes for skill gap analysis."""
    records = []
    for s in skills_analysis:
        records.append({
            "Required Skill": s.get("skill", ""),
            "Category": s.get("category", "Technical"),
            "Current Status": s.get("status", "Need to Learn"),
            "Priority": s.get("priority", "Medium"),
            "Current Mastery": s.get("current_mastery", "Not specified"),
            "Recommendation": s.get("recommendation", "")
        })
    df = pd.DataFrame(records)
    return df.to_csv(index=False).encode('utf-8')


def generate_roadmap_pdf(
    student_profile: Dict[str, Any],
    skills_analysis: List[Dict[str, Any]],
    roadmap: List[Dict[str, Any]],
    projects: List[Dict[str, Any]],
    readiness_data: Dict[str, Any]
) -> bytes:
    """
    Generate a professional, multi-page PDF career roadmap report using ReportLab.
    """
    buffer = io.BytesIO()

    if not REPORTLAB_AVAILABLE:
        # Fallback simple text buffer if reportlab is absent
        plain_text = f"SkillSync Career Roadmap Report\nTarget Role: {student_profile.get('target_role')}\n"
        return plain_text.encode('utf-8')

    # Page setup
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
    brand_title_style = ParagraphStyle(
        'BrandTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A')
    )

    tagline_style = ParagraphStyle(
        'Tagline',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#6366F1')
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Header Banner
    story.append(Paragraph("<b>SkillSync</b> — AI-Powered Career Roadmap", brand_title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Discover Your Skills. Bridge the Gap. Build Your Future.", tagline_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#6366F1'), spaceBefore=2, spaceAfter=12))

    # Student Summary Box
    summary_data = [
        [
            Paragraph(f"<b>Target Role:</b> {student_profile.get('target_role', 'N/A')}", body_style),
            Paragraph(f"<b>Experience Level:</b> {student_profile.get('experience_level', 'N/A')}", body_style)
        ],
        [
            Paragraph(f"<b>Study Availability:</b> {student_profile.get('study_hours', 'N/A')}", body_style),
            Paragraph(f"<b>Skill Readiness Score:</b> <b>{readiness_data.get('score', 0)}%</b> ({readiness_data.get('category', '')})", body_style)
        ],
        [
            Paragraph(f"<b>Skills Matched:</b> {readiness_data.get('matched', 0)} / {readiness_data.get('total', 0)}", body_style),
            Paragraph(f"<b>Skills to Learn:</b> {readiness_data.get('missing', 0)} + {readiness_data.get('partial', 0)} partial", body_style)
        ]
    ]

    summary_table = Table(summary_data, colWidths=[270, 270])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # 1. Skill Gap Analysis Table
    story.append(Paragraph("1. Skill Gap Analysis Breakdown", h1_style))
    
    table_headers = [
        Paragraph("<b>Required Skill</b>", body_bold),
        Paragraph("<b>Status</b>", body_bold),
        Paragraph("<b>Priority</b>", body_bold),
        Paragraph("<b>Recommendation</b>", body_bold)
    ]
    gap_table_data = [table_headers]

    for s in skills_analysis:
        status_str = s.get("status", "Need to Learn")
        status_color = "#10B981" if status_str == "Already Have" else ("#F59E0B" if status_str == "Partially Skilled" else "#EF4444")
        
        status_p = Paragraph(f"<font color='{status_color}'><b>{status_str}</b></font>", body_style)
        priority_p = Paragraph(f"<b>{s.get('priority', '-')}</b>", body_style)
        skill_p = Paragraph(f"<b>{s.get('skill', '')}</b>", body_style)
        rec_p = Paragraph(s.get('recommendation', ''), body_style)

        gap_table_data.append([skill_p, status_p, priority_p, rec_p])

    gap_table = Table(gap_table_data, colWidths=[120, 85, 55, 280])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 16))

    # 2. Personalized 8-Week Roadmap
    story.append(Paragraph("2. Personalized 8-Week Learning Roadmap", h1_style))
    story.append(Paragraph("Tailored to your current gaps and study hours. Complete each milestone weekly.", body_style))
    story.append(Spacer(1, 6))

    for w in roadmap:
        week_num = w.get("week_number", "?")
        topic = w.get("week_title", "Topic")
        hours = w.get("estimated_study_hours", "N/A")
        skills = ", ".join(w.get("skills_to_develop", []))
        objectives = "<br/>• ".join(w.get("objectives", []))
        exercises = "<br/>• ".join(w.get("practical_exercises", []))
        outcome = w.get("expected_outcome", "Solidify concepts.")

        w_content = [
            [
                Paragraph(f"<b>Week {week_num}: {topic}</b>", body_bold),
                Paragraph(f"<b>Est. Hours:</b> {hours} hrs/wk", body_style)
            ],
            [
                Paragraph(f"<b>Skills:</b> {skills}", body_style),
                Paragraph(f"<b>Outcome:</b> {outcome}", body_style)
            ],
            [
                Paragraph(f"<b>Objectives:</b><br/>• {objectives}", body_style),
                Paragraph(f"<b>Practical Exercise:</b><br/>• {exercises}", body_style)
            ]
        ]
        w_table = Table(w_content, colWidths=[270, 270])
        w_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#C7D2FE')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E7FF')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(KeepTogether([w_table, Spacer(1, 8)]))

    story.append(Spacer(1, 10))

    # 3. Recommended Portfolio Projects
    story.append(Paragraph("3. Recommended Portfolio Projects (GitHub Ready)", h1_style))
    story.append(Paragraph("High-impact projects designed to showcase your competencies to hiring managers.", body_style))
    story.append(Spacer(1, 6))

    for p in projects:
        difficulty = p.get("difficulty", "Standard")
        title = p.get("title", "Project")
        desc = p.get("short_description", "")
        problem = p.get("problem_solved", "")
        techs = ", ".join(p.get("technologies_required", []))
        est_time = p.get("estimated_completion_time", "")
        output = p.get("expected_final_output", "")

        diff_color = "#0284C7" if difficulty == "Beginner" else ("#7C3AED" if difficulty == "Intermediate" else "#DB2777")

        proj_content = [
            [
                Paragraph(f"<b>{title}</b>", body_bold),
                Paragraph(f"<font color='{diff_color}'><b>[{difficulty.upper()}]</b></font> ({est_time})", body_style)
            ],
            [
                Paragraph(f"<b>Overview:</b> {desc}", body_style),
                Paragraph(f"<b>Problem Solved:</b> {problem}", body_style)
            ],
            [
                Paragraph(f"<b>Tech Stack:</b> {techs}", body_style),
                Paragraph(f"<b>Deliverable:</b> {output}", body_style)
            ]
        ]
        p_table = Table(proj_content, colWidths=[270, 270])
        p_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(KeepTogether([p_table, Spacer(1, 8)]))

    # Footer note
    story.append(Spacer(1, 12))
    story.append(Paragraph("Generated by SkillSync — Your AI-Powered Career Roadmap. Keep learning and building!", tagline_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def extract_text_from_pdf(file_bytes_or_buffer) -> str:
    """
    Extract readable text from an uploaded PDF resume or document.
    Gracefully handles multi-page resumes, encoding, and formatting.
    """
    if file_bytes_or_buffer is None:
        return ""

    try:
        from pypdf import PdfReader
        if hasattr(file_bytes_or_buffer, "read"):
            # Ensure seek(0) in case Streamlit already read it
            if hasattr(file_bytes_or_buffer, "seek"):
                file_bytes_or_buffer.seek(0)
            reader = PdfReader(file_bytes_or_buffer)
        else:
            reader = PdfReader(io.BytesIO(file_bytes_or_buffer))

        extracted_pages = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                extracted_pages.append(t)
        return "\n\n".join(extracted_pages).strip()
    except Exception as e:
        # Fallback byte decoding if plain text was uploaded
        try:
            if hasattr(file_bytes_or_buffer, "getvalue"):
                raw = file_bytes_or_buffer.getvalue()
            elif hasattr(file_bytes_or_buffer, "read"):
                if hasattr(file_bytes_or_buffer, "seek"):
                    file_bytes_or_buffer.seek(0)
                raw = file_bytes_or_buffer.read()
            else:
                raw = file_bytes_or_buffer
            return raw.decode("utf-8", errors="ignore").strip()
        except Exception:
            return ""

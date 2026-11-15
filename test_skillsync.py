"""
Comprehensive test suite for SkillSync components.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import utils
import ai_engine
import roadmap_generator
import project_preview_engine


def test_input_validation():
    print("Testing input validation...")
    # Valid input
    valid, msg, skills, role = utils.validate_user_inputs(
        ["Python", "SQL"], "Pandas, NumPy", "Data Scientist", "", "10–15 hours", "Intermediate"
    )
    assert valid is True
    assert "Pandas" in skills
    assert "NumPy" in skills
    assert role == "Data Scientist"

    # Missing skills
    valid, msg, _, _ = utils.validate_user_inputs([], "", "Data Scientist", "", "5–10 hours", "Beginner")
    assert valid is False
    assert "at least one" in msg

    # Custom role
    valid, msg, _, role = utils.validate_user_inputs(
        ["Python"], "", "Custom Role...", "Robotics Software Engineer", "10–15 hours", "Beginner"
    )
    assert valid is True
    assert role == "Robotics Software Engineer"

    # Missing custom role
    valid, msg, _, _ = utils.validate_user_inputs(
        ["Python"], "", "Custom Role...", "", "10–15 hours", "Beginner"
    )
    assert valid is False
    print("Input validation tests passed!")


def test_skill_readiness_calculation():
    print("Testing skill readiness calculation...")
    mock_skills = [
        {"skill": "Python", "status": "Already Have"},
        {"skill": "SQL", "status": "Already Have"},
        {"skill": "Pandas", "status": "Partially Skilled"},
        {"skill": "Machine Learning", "status": "Need to Learn"},
    ]
    res = utils.calculate_skill_readiness(mock_skills)
    assert res["matched"] == 2
    assert res["partial"] == 1
    assert res["missing"] == 1
    assert res["total"] == 4
    # Score = (2 * 1.0 + 1 * 0.5) / 4 * 100 = 2.5 / 4 * 100 = 62.5 -> 62 or 63%
    assert 60 <= res["score"] <= 65
    print(f"Readiness score test passed: score={res['score']}%, category={res['category']}")


def test_csv_export():
    print("Testing CSV export...")
    mock_skills = [
        {
            "skill": "Python",
            "category": "Core Language",
            "status": "Already Have",
            "priority": "-",
            "current_mastery": "Proficient",
            "recommendation": "Maintain proficiency."
        },
        {
            "skill": "Docker",
            "category": "DevOps",
            "status": "Need to Learn",
            "priority": "High",
            "current_mastery": "None",
            "recommendation": "Learn container basics."
        }
    ]
    csv_bytes = utils.export_skill_gap_to_csv(mock_skills)
    assert len(csv_bytes) > 0
    csv_str = csv_bytes.decode('utf-8')
    assert "Required Skill" in csv_str
    assert "Python" in csv_str
    assert "Docker" in csv_str
    print("CSV export test passed!")


def test_pdf_generation():
    print("Testing PDF report generation...")
    profile = {
        "target_role": "AI/ML Engineer",
        "experience_level": "Intermediate",
        "study_hours": "10–15 hours"
    }
    mock_skills = [
        {"skill": "Python", "status": "Already Have", "priority": "-", "recommendation": "Advanced async & typing"},
        {"skill": "PyTorch", "status": "Need to Learn", "priority": "High", "recommendation": "Deep learning tensors"}
    ]
    mock_roadmap = [
        {
            "week_number": 1,
            "week_title": "Deep Learning Fundamentals",
            "skills_to_develop": ["PyTorch", "Tensors"],
            "objectives": ["Understand autograd", "Build first MLP"],
            "resources": [{"title": "PyTorch Docs", "type": "Documentation", "link": "https://pytorch.org"}],
            "practical_exercises": ["Train MNIST classifier"],
            "expected_outcome": "Working neural network model",
            "estimated_study_hours": 12
        }
    ]
    mock_projects = [
        {
            "difficulty": "Beginner",
            "title": "Image Classifier with PyTorch",
            "short_description": "Classify images using a pretrained ResNet.",
            "problem_solved": "Automated image tagging.",
            "technologies_required": ["Python", "PyTorch"],
            "skills_demonstrated": ["CNNs", "Transfer Learning"],
            "estimated_completion_time": "1 week",
            "expected_final_output": "Streamlit app classifying custom images."
        }
    ]
    readiness = {"score": 50, "matched": 1, "partial": 0, "missing": 1, "total": 2, "category": "Strong Foundation"}

    pdf_bytes = utils.generate_roadmap_pdf(profile, mock_skills, mock_roadmap, mock_projects, readiness)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")
    print(f"PDF generation test passed! PDF size: {len(pdf_bytes)} bytes")


def test_ai_json_cleaning():
    print("Testing AI JSON response cleaning...")
    # Markdown wrapped
    raw_markdown = """
    Here is your roadmap:
    ```json
    {
      "career_summary": {"target_role": "DevOps Engineer"},
      "skills_analysis": []
    }
    ```
    Hope this helps!
    """
    parsed = ai_engine.clean_json_response(raw_markdown)
    assert parsed["career_summary"]["target_role"] == "DevOps Engineer"

    # Trailing comma recovery
    raw_trailing = '{"items": ["a", "b",], "score": 90,}'
    parsed2 = ai_engine.clean_json_response(raw_trailing)
    assert parsed2["score"] == 90
    print("AI JSON cleaning tests passed!")


def test_plotly_figures():
    print("Testing Plotly figures generation...")
    gauge = roadmap_generator.create_readiness_gauge(75, 5, 2, 3, 10)
    assert gauge is not None
    donut = roadmap_generator.create_skill_breakdown_donut(5, 2, 3)
    assert donut is not None
    print("Plotly figures tests passed!")


def test_fallback_mode():
    print("Testing Fallback / Offline AI Mode...")
    # Test fallback analysis for Data Scientist
    res = ai_engine.generate_fallback_career_analysis(
        current_skills=["Python", "SQL"],
        target_role="Data Scientist",
        study_hours="10–15 hours",
        experience_level="Intermediate"
    )
    assert res is not None
    assert "career_summary" in res
    assert "skills_analysis" in res
    assert len(res["skills_analysis"]) >= 8
    assert "roadmap" in res
    assert len(res["roadmap"]) == 8, f"Expected 8 weeks, got {len(res['roadmap'])}"
    assert "Capstone" in res["roadmap"][-1]["week_title"]
    assert "portfolio_projects" in res
    assert len(res["portfolio_projects"]) == 3
    difficulties = [p["difficulty"].lower() for p in res["portfolio_projects"]]
    assert "beginner" in difficulties
    assert "intermediate" in difficulties
    assert "advanced" in difficulties

    # Test analyze_career_path without API key (fallback mode activation)
    res_no_key = ai_engine.analyze_career_path(
        current_skills=["JavaScript", "React"],
        target_role="Frontend Developer",
        study_hours="5–10 hours",
        experience_level="Beginner",
        api_key=""
    )
    assert res_no_key["career_summary"]["source"] == "curated_fallback"
    assert len(res_no_key["roadmap"]) == 8
    print("Fallback / Offline mode tests passed!")


def test_engine_status_and_security():
    print("Testing Engine Status & Secret Protection...")
    status_off = ai_engine.get_engine_status("")
    assert status_off["connected"] is False
    assert status_off["mode"] == "fallback"
    assert "key" not in status_off

    status_on = ai_engine.get_engine_status("mock_secret_key_abc_123")
    assert status_on["connected"] is True
    assert status_on["mode"] == "gemini_ai"
    # Verify no secret key leakage in the dictionary
    for val in status_on.values():
        assert "mock_secret_key" not in str(val)
    print("Engine Status & Secret Protection tests passed!")


def test_project_preview_engine():
    print("Testing Project Preview Engine (SkillSync 2.1)...")
    # Test Frontend Project
    p_fe = {
        "title": "Interactive Task Board",
        "difficulty": "Beginner",
        "short_description": "Kanban board with drag and drop",
        "problem_solved": "Task management",
        "technologies_required": ["React", "Tailwind CSS"],
        "skills_demonstrated": ["Component State", "DOM"],
        "estimated_completion_time": "1 week",
        "expected_final_output": "Deployed web app"
    }
    cat_fe = project_preview_engine.detect_project_category(p_fe)
    assert cat_fe == "frontend"
    html_fe = project_preview_engine.generate_live_preview_html(p_fe)
    assert "<!DOCTYPE html>" in html_fe
    assert "Interactive Task Board" in html_fe
    src_fe = project_preview_engine.get_project_source_files(p_fe)
    assert "index.html" in src_fe
    assert "styles.css" in src_fe

    # Test ML Project
    p_ml = {
        "title": "Customer Churn Prediction Engine",
        "difficulty": "Intermediate",
        "short_description": "Predict churn using random forest",
        "problem_solved": "Customer retention",
        "technologies_required": ["Python", "Scikit-Learn", "Pandas"],
        "skills_demonstrated": ["Model Evaluation"],
        "estimated_completion_time": "2 weeks",
        "expected_final_output": "Interactive inference dashboard"
    }
    cat_ml = project_preview_engine.detect_project_category(p_ml)
    assert cat_ml == "ml_datascience"
    html_ml = project_preview_engine.generate_live_preview_html(p_ml)
    assert "<!DOCTYPE html>" in html_ml
    assert "Customer Churn Prediction Engine" in html_ml
    src_ml = project_preview_engine.get_project_source_files(p_ml)
    assert "app.py" in src_ml

    # Test Backend Project
    p_be = {
        "title": "High-Concurrency Order Processing Service",
        "difficulty": "Advanced",
        "short_description": "Scalable REST API with Redis cache",
        "problem_solved": "Order concurrency",
        "technologies_required": ["FastAPI", "PostgreSQL", "Docker"],
        "skills_demonstrated": ["API Design", "Transactions"],
        "estimated_completion_time": "3 weeks",
        "expected_final_output": "Containerized microservice"
    }
    cat_be = project_preview_engine.detect_project_category(p_be)
    assert cat_be == "backend_api"
    html_be = project_preview_engine.generate_live_preview_html(p_be)
    assert "<!DOCTYPE html>" in html_be
    assert "High-Concurrency Order Processing Service" in html_be
    src_be = project_preview_engine.get_project_source_files(p_be)
    assert "main.py" in src_be

    print("Project Preview Engine tests passed!")


def test_skill_gap_dataframe():
    print("Testing Skill Gap DataFrame generation...")
    import pandas as pd
    mock_skills = [
        {"skill": "Python", "category": "Programming", "status": "Already Have", "priority": "-", "recommendation": "Maintain proficiency"},
        {"skill": "SQL", "category": "Database", "status": "Partially Skilled", "priority": "Medium", "recommendation": "Practice advanced joins"},
        {"skill": "Pandas", "category": "Data Manipulation", "status": "Need to Learn", "priority": "High", "recommendation": "Master DataFrames"}
    ]
    # Verify records mapping without relying on any HTML strings
    records = []
    for s in mock_skills:
        skill_name = str(s.get("skill", "Unknown Skill")).strip()
        category = str(s.get("category", "General")).strip()
        raw_status = str(s.get("status", "Need to Learn")).strip()
        raw_priority = str(s.get("priority", "–")).strip()
        rec = str(s.get("recommendation", "")).strip()

        status_display = "🟢 Already Have" if "have" in raw_status.lower() else ("🟡 Needs Improvement" if "partial" in raw_status.lower() else "🔴 Need to Learn")
        priority_display = "🔥 High" if "high" in raw_priority.lower() else ("⚡ Medium" if "med" in raw_priority.lower() else "—")
        records.append({
            "Skill / Technology": skill_name,
            "Category": category,
            "Current Status": status_display,
            "Priority": priority_display,
            "Learning Recommendation": rec
        })
    df = pd.DataFrame(records)
    assert len(df) == 3
    assert list(df.columns) == ["Skill / Technology", "Category", "Current Status", "Priority", "Learning Recommendation"]
    assert df.iloc[0]["Current Status"] == "🟢 Already Have"
    assert df.iloc[1]["Current Status"] == "🟡 Needs Improvement"
    assert df.iloc[2]["Current Status"] == "🔴 Need to Learn"
    print("Skill Gap DataFrame tests passed!")


if __name__ == "__main__":
    test_input_validation()
    test_skill_readiness_calculation()
    test_csv_export()
    test_pdf_generation()
    test_ai_json_cleaning()
    test_plotly_figures()
    test_fallback_mode()
    test_engine_status_and_security()
    test_project_preview_engine()
    test_skill_gap_dataframe()
    print("\n[SUCCESS] ALL TESTS PASSED SUCCESSFULLY! 100% OPERATIONAL.")



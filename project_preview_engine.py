"""
SkillSync 2.1 — Live Visual Output & Interactive Project Preview Engine
Generates and renders live, sandboxed interactive web UI prototypes,
ML prediction dashboards, and API explorers for portfolio projects.
"""

from typing import Dict, List, Any
import html
import json
import streamlit as st
import streamlit.components.v1 as components


def detect_project_category(project: Dict[str, Any]) -> str:
    """
    Detect whether a project is primarily Frontend, Data Science/ML, Backend API,
    or Full-Stack / Software Engineering based on its tech stack, title, and description.
    """
    title = project.get("title", "").lower()
    desc = project.get("short_description", "").lower()
    techs = [t.lower() for t in project.get("technologies_required", [])]
    tech_str = " ".join(techs) + " " + title + " " + desc

    ml_keywords = ["scikit", "pandas", "ml", "machine learning", "pytorch", "tensorflow",
                   "xgboost", "churn", "regression", "classification", "forecast", "sentiment",
                   "nlp", "transformer", "neural", "deep learning", "model", "prediction"]
    if any(k in tech_str for k in ml_keywords):
        return "ml_datascience"

    backend_keywords = ["fastapi", "django", "flask", "express", "rest", "graphql", "api",
                        "auth", "jwt", "redis", "postgres", "microservice", "docker", "kafka",
                        "backend", "server", "endpoint", "database"]
    if any(k in tech_str for k in backend_keywords) and not any(k in tech_str for k in ["react", "vue", "html", "css", "figma"]):
        return "backend_api"

    frontend_keywords = ["react", "vue", "html", "css", "tailwind", "next.js", "javascript",
                         "typescript", "frontend", "ui/ux", "figma", "web app", "dashboard", "kanban"]
    if any(k in tech_str for k in frontend_keywords):
        return "frontend"

    return "frontend"


def generate_live_preview_html(project: Dict[str, Any]) -> str:
    """
    Generate a self-contained, responsive, sandboxed interactive HTML document
    representing the finished product prototype.
    """
    category = detect_project_category(project)
    title = html.escape(project.get("title", "Portfolio Project"))
    desc = html.escape(project.get("short_description", ""))
    diff = html.escape(project.get("difficulty", "Intermediate"))
    techs = [html.escape(t) for t in project.get("technologies_required", [])]

    if category == "ml_datascience":
        return _build_ml_preview_html(title, desc, diff, techs, project)
    elif category == "backend_api":
        return _build_api_preview_html(title, desc, diff, techs, project)
    else:
        return _build_frontend_preview_html(title, desc, diff, techs, project)


def _build_frontend_preview_html(title: str, desc: str, diff: str, techs: List[str], project: Dict[str, Any]) -> str:
    tech_badges = "".join([f'<span class="badge">{t}</span>' for t in techs[:5]])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Live Preview</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  body {{ background: #0b0f19; color: #f1f5f9; padding: 20px; font-size: 14px; min-height: 100vh; }}
  
  /* Top App Nav */
  .app-header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 18px; background: rgba(22, 30, 54, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; margin-bottom: 20px; backdrop-filter: blur(10px); }}
  .app-logo {{ display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 15px; color: #00D2FF; }}
  .app-nav {{ display: flex; gap: 10px; }}
  .nav-btn {{ background: transparent; border: 1px solid rgba(255,255,255,0.12); color: #94a3b8; padding: 6px 14px; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-size: 12px; }}
  .nav-btn.active, .nav-btn:hover {{ background: rgba(99, 102, 241, 0.2); border-color: #8B5CF6; color: #fff; }}
  
  /* Banner / Hero */
  .hero-box {{ background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(0, 210, 255, 0.1) 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 14px; padding: 18px 20px; margin-bottom: 20px; }}
  .hero-title {{ font-size: 18px; font-weight: 800; color: #ffffff; margin-bottom: 6px; }}
  .hero-desc {{ color: #94a3b8; font-size: 13px; line-height: 1.5; margin-bottom: 12px; }}
  .badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
  .badge {{ background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.12); color: #e2e8f0; font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: 500; }}

  /* Interactive Main Grid */
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 20px; }}
  .card {{ background: rgba(18, 24, 43, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; transition: transform 0.2s, border-color 0.2s; cursor: pointer; position: relative; }}
  .card:hover {{ transform: translateY(-3px); border-color: #00D2FF; box-shadow: 0 6px 18px rgba(0, 210, 255, 0.15); }}
  .card-tag {{ display: inline-block; font-size: 10px; font-weight: 700; text-transform: uppercase; padding: 2px 6px; border-radius: 4px; margin-bottom: 8px; }}
  .tag-cyan {{ background: rgba(0, 210, 255, 0.15); color: #00D2FF; border: 1px solid rgba(0, 210, 255, 0.3); }}
  .tag-purple {{ background: rgba(139, 92, 246, 0.15); color: #A78BFA; border: 1px solid rgba(139, 92, 246, 0.3); }}
  .tag-green {{ background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }}
  .card-h {{ font-weight: 700; font-size: 14px; margin-bottom: 4px; color: #fff; }}
  .card-p {{ font-size: 12px; color: #94a3b8; line-height: 1.4; }}
  
  /* Interactive Action Bar */
  .action-bar {{ display: flex; gap: 10px; align-items: center; background: rgba(26, 34, 60, 0.5); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); }}
  .input-demo {{ flex: 1; background: rgba(11, 15, 25, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); color: #fff; padding: 8px 12px; border-radius: 8px; font-size: 12px; outline: none; }}
  .input-demo:focus {{ border-color: #8B5CF6; }}
  .btn-primary {{ background: linear-gradient(135deg, #4F46E5, #7C3AED); color: #fff; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; font-size: 12px; }}
  .btn-primary:hover {{ opacity: 0.9; transform: scale(1.02); }}

  /* Interactive Toast Output */
  #toast {{ display: none; position: fixed; bottom: 20px; right: 20px; background: #10B981; color: #fff; padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.4); animation: slideIn 0.3s ease; }}
  @keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
</style>
</head>
<body>

<div class="app-header">
  <div class="app-logo">⚡ {title}</div>
  <div class="app-nav">
    <button class="nav-btn active" onclick="switchTab(this, 'Dashboard')">Overview</button>
    <button class="nav-btn" onclick="switchTab(this, 'Analytics')">Analytics</button>
    <button class="nav-btn" onclick="switchTab(this, 'Settings')">Settings</button>
  </div>
</div>

<div class="hero-box">
  <div class="hero-title">🚀 Interactive Application Prototype</div>
  <div class="hero-desc">{desc}</div>
  <div class="badges">
    <span class="badge" style="color: #34D399; border-color: #10B981;">● {diff} Tier</span>
    {tech_badges}
    <span class="badge" style="color: #00D2FF;">Live Interactive Preview</span>
  </div>
</div>

<div class="grid" id="cardContainer">
  <div class="card" onclick="triggerCard('User Metrics Module')">
    <span class="card-tag tag-cyan">Metrics</span>
    <div class="card-h">Active User Funnel</div>
    <div class="card-p">2,480 daily active events with 99.4% uptime telemetry.</div>
  </div>
  <div class="card" onclick="triggerCard('Workflow Engine')">
    <span class="card-tag tag-purple">Workflow</span>
    <div class="card-h">Automated Pipeline</div>
    <div class="card-p">Instant execution via async webhooks and worker nodes.</div>
  </div>
  <div class="card" onclick="triggerCard('Storage Service')">
    <span class="card-tag tag-green">Storage</span>
    <div class="card-h">Encrypted Data Store</div>
    <div class="card-p">Zero-knowledge local and cloud state synchronization.</div>
  </div>
</div>

<div class="action-bar">
  <input type="text" id="demoInput" class="input-demo" placeholder="Type a sample record or action item here...">
  <button class="btn-primary" onclick="submitAction()">Add to Preview</button>
</div>

<div id="toast">✅ Action completed in interactive prototype!</div>

<script>
  function switchTab(btn, tabName) {{
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    showToast('Switched view to ' + tabName);
  }}

  function triggerCard(moduleName) {{
    showToast('Clicked ' + moduleName + ' details card');
  }}

  function submitAction() {{
    const val = document.getElementById('demoInput').value.trim();
    if (!val) {{
      showToast('Please enter text to test adding an item!');
      return;
    }}
    const container = document.getElementById('cardContainer');
    const newCard = document.createElement('div');
    newCard.className = 'card';
    newCard.onclick = () => triggerCard(val);
    newCard.innerHTML = '<span class="card-tag tag-cyan">Custom Item</span><div class="card-h">' + val + '</div><div class="card-p">Dynamic user-created element inside interactive preview.</div>';
    container.prepend(newCard);
    document.getElementById('demoInput').value = '';
    showToast('Added "' + val + '" to preview grid!');
  }}

  function showToast(msg) {{
    const t = document.getElementById('toast');
    t.innerText = '⚡ ' + msg;
    t.style.display = 'block';
    clearTimeout(window._toastTimeout);
    window._toastTimeout = setTimeout(() => {{ t.style.display = 'none'; }}, 2800);
  }}
</script>
</body>
</html>"""


def _build_ml_preview_html(title: str, desc: str, diff: str, techs: List[str], project: Dict[str, Any]) -> str:
    tech_badges = "".join([f'<span class="badge">{t}</span>' for t in techs[:5]])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ML Inference Simulator</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
  body {{ background: #070A13; color: #f1f5f9; padding: 18px; font-size: 13px; min-height: 100vh; }}
  
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px; margin-bottom: 16px; }}
  .title-area h2 {{ font-size: 17px; font-weight: 800; color: #fff; }}
  .title-area p {{ font-size: 12px; color: #94a3b8; }}
  .status-badge {{ background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; }}

  /* Simulator Layout */
  .sim-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  @media (max-width: 600px) {{ .sim-container {{ grid-template-columns: 1fr; }} }}

  .panel {{ background: rgba(14, 20, 36, 0.85); border: 1px solid rgba(255, 255, 255, 0.09); border-radius: 12px; padding: 16px; backdrop-filter: blur(12px); }}
  .panel-title {{ font-size: 13px; font-weight: 700; color: #00D2FF; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 6px; }}

  /* Slider Controls */
  .control-group {{ margin-bottom: 14px; }}
  .label-row {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; margin-bottom: 6px; color: #cbd5e1; }}
  input[type=range] {{ width: 100%; accent-color: #8B5CF6; cursor: pointer; }}
  
  /* Score Meter */
  .score-card {{ text-align: center; padding: 16px; background: rgba(20, 28, 50, 0.6); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.07); margin-bottom: 14px; }}
  .score-val {{ font-size: 38px; font-weight: 900; color: #00D2FF; line-height: 1.1; }}
  .score-label {{ font-size: 12px; color: #94a3b8; margin-top: 4px; }}
  
  .prob-bar-container {{ height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; margin: 12px 0; }}
  .prob-bar {{ height: 100%; width: 28%; background: linear-gradient(90deg, #10B981, #00D2FF); transition: width 0.3s ease, background 0.3s ease; }}

  /* Metrics Grid */
  .mini-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px; }}
  .mini-box {{ background: rgba(11, 15, 25, 0.6); padding: 8px; border-radius: 6px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }}
  .mini-num {{ font-weight: 700; color: #fff; font-size: 13px; }}
  .mini-lbl {{ font-size: 10px; color: #64748b; text-transform: uppercase; }}

  .btn-predict {{ width: 100%; background: linear-gradient(135deg, #6366F1, #8B5CF6); color: #fff; border: none; padding: 10px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; transition: all 0.2s; margin-top: 6px; }}
  .btn-predict:hover {{ opacity: 0.9; transform: translateY(-1px); }}
</style>
</head>
<body>

<div class="header">
  <div class="title-area">
    <h2>🤖 {title}</h2>
    <p>Live ML Inference & Prediction Simulator • Model Serving Layer</p>
  </div>
  <span class="status-badge">● Model Loaded</span>
</div>

<div class="sim-container">
  <!-- Controls Panel -->
  <div class="panel">
    <div class="panel-title">🎛️ Input Feature Parameters</div>
    
    <div class="control-group">
      <div class="label-row">
        <span>Tenure / Experience (Months):</span>
        <span id="tenureVal" style="color: #00D2FF;">24</span>
      </div>
      <input type="range" id="tenure" min="1" max="72" value="24" oninput="updateInference()">
    </div>

    <div class="control-group">
      <div class="label-row">
        <span>Monthly Value / Activity Score:</span>
        <span id="activityVal" style="color: #00D2FF;">$85</span>
      </div>
      <input type="range" id="activity" min="10" max="250" value="85" oninput="updateInference()">
    </div>

    <div class="control-group">
      <div class="label-row">
        <span>Support Escalations / Queries:</span>
        <span id="ticketsVal" style="color: #00D2FF;">1</span>
      </div>
      <input type="range" id="tickets" min="0" max="10" value="1" oninput="updateInference()">
    </div>

    <button class="btn-predict" onclick="updateInference(true)">⚡ Recalculate Live Inference</button>
  </div>

  <!-- Real-Time Output Panel -->
  <div class="panel">
    <div class="panel-title">📊 Predicted Outcome & Confidence</div>
    
    <div class="score-card">
      <div class="score-val" id="probScore">18%</div>
      <div class="score-label" id="probCategory">Status: <b style="color: #10B981;">Low Risk / High Retention</b></div>
      <div class="prob-bar-container">
        <div class="prob-bar" id="probBar" style="width: 18%;"></div>
      </div>
      <div style="font-size: 11px; color: #94a3b8;" id="recommendation">
        Model Recommendation: Standard engagement sequence. Customer exhibits healthy retention metrics.
      </div>
    </div>

    <div class="mini-grid">
      <div class="mini-box">
        <div class="mini-num">94.8%</div>
        <div class="mini-lbl">ROC-AUC Score</div>
      </div>
      <div class="mini-box">
        <div class="mini-num">12 ms</div>
        <div class="mini-lbl">Inference Latency</div>
      </div>
    </div>
  </div>
</div>

<script>
  function updateInference(animate) {{
    const tenure = parseInt(document.getElementById('tenure').value);
    const activity = parseInt(document.getElementById('activity').value);
    const tickets = parseInt(document.getElementById('tickets').value);

    document.getElementById('tenureVal').innerText = tenure + ' mos';
    document.getElementById('activityVal').innerText = '$' + activity;
    document.getElementById('ticketsVal').innerText = tickets;

    // Deterministic simulation heuristic
    let risk = Math.round(50 - (tenure * 0.5) - (activity * 0.1) + (tickets * 12));
    if (risk < 5) risk = 5;
    if (risk > 96) risk = 96;

    const probScore = document.getElementById('probScore');
    const probBar = document.getElementById('probBar');
    const probCat = document.getElementById('probCategory');
    const rec = document.getElementById('recommendation');

    probScore.innerText = risk + '%';
    probBar.style.width = risk + '%';

    if (risk < 35) {{
      probScore.style.color = '#10B981';
      probBar.style.background = 'linear-gradient(90deg, #10B981, #00D2FF)';
      probCat.innerHTML = 'Status: <b style="color: #10B981;">Favorable / Retained</b>';
      rec.innerText = 'Model Recommendation: Standard engagement. Positive retention signals detected.';
    }} else if (risk < 65) {{
      probScore.style.color = '#F59E0B';
      probBar.style.background = 'linear-gradient(90deg, #F59E0B, #EC4899)';
      probCat.innerHTML = 'Status: <b style="color: #F59E0B;">Moderate Watch / Needs Refinement</b>';
      rec.innerText = 'Model Recommendation: Send tailored product re-engagement guide.';
    }} else {{
      probScore.style.color = '#EF4444';
      probBar.style.background = '#EF4444';
      probCat.innerHTML = 'Status: <b style="color: #EF4444;">High Churn Risk / Critical</b>';
      rec.innerText = 'Model Recommendation: Trigger senior customer success outreach immediately.';
    }}
  }}
</script>
</body>
</html>"""


def _build_api_preview_html(title: str, desc: str, diff: str, techs: List[str], project: Dict[str, Any]) -> str:
    tech_badges = "".join([f'<span class="badge">{t}</span>' for t in techs[:5]])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - API Explorer Preview</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'JetBrains Mono', Consolas, Monaco, monospace, sans-serif; }}
  body {{ background: #080C16; color: #E2E8F0; padding: 18px; font-size: 12px; min-height: 100vh; }}

  .api-nav {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px; margin-bottom: 16px; }}
  .api-title {{ font-size: 15px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px; }}
  .spec-tag {{ background: rgba(56, 189, 248, 0.15); color: #38BDF8; padding: 3px 8px; border-radius: 4px; font-size: 10px; border: 1px solid rgba(56, 189, 248, 0.3); }}

  .endpoint-bar {{ display: flex; gap: 10px; margin-bottom: 14px; background: rgba(18, 24, 43, 0.85); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); align-items: center; }}
  .method-post {{ background: #10B981; color: #000; font-weight: 800; padding: 4px 10px; border-radius: 6px; font-size: 11px; }}
  .method-get {{ background: #38BDF8; color: #000; font-weight: 800; padding: 4px 10px; border-radius: 6px; font-size: 11px; }}
  .route-select {{ flex: 1; background: transparent; border: none; color: #00D2FF; font-size: 13px; font-weight: 600; outline: none; }}
  .route-select option {{ background: #0F172A; color: #fff; }}

  .btn-send {{ background: linear-gradient(135deg, #6366F1, #8B5CF6); color: #fff; border: none; padding: 6px 16px; border-radius: 6px; font-weight: 700; cursor: pointer; transition: all 0.2s; }}
  .btn-send:hover {{ opacity: 0.9; }}

  .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  @media (max-width: 600px) {{ .cols {{ grid-template-columns: 1fr; }} }}

  .box-label {{ font-size: 11px; text-transform: uppercase; color: #94A3B8; margin-bottom: 6px; font-weight: 700; }}
  .editor {{ background: #0E1424; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px; color: #A78BFA; min-height: 160px; font-size: 12px; line-height: 1.5; white-space: pre; overflow-x: auto; }}
  
  .response-box {{ background: #090D18; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 12px; min-height: 160px; font-size: 12px; line-height: 1.5; white-space: pre; overflow-x: auto; color: #34D399; position: relative; }}
  .status-line {{ display: flex; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 4px; font-size: 11px; color: #94A3B8; }}
</style>
</head>
<body>

<div class="api-nav">
  <div class="api-title">
    ⚡ {title}
    <span class="spec-tag">OpenAPI 3.1</span>
  </div>
  <div style="font-size: 11px; color: #34D399;">● Live Microservice Simulator</div>
</div>

<div class="endpoint-bar">
  <span class="method-post" id="methodBadge">POST</span>
  <select class="route-select" id="routeSelect" onchange="switchEndpoint()">
    <option value="predict">/api/v1/predict (Process Inbound Payload)</option>
    <option value="auth">/api/v1/auth/token (OAuth2 JWT Sign-In)</option>
    <option value="health">/api/v1/health (System Diagnostic Uptime)</option>
  </select>
  <button class="btn-send" onclick="sendApiRequest()">Execute Request</button>
</div>

<div class="cols">
  <div>
    <div class="box-label">Request Payload (JSON)</div>
    <div class="editor" id="reqPayload" contenteditable="true">{{
  "client_id": "usr_99812",
  "action": "execute_pipeline",
  "parameters": {{
    "threshold": 0.85,
    "environment": "production"
  }}
}}</div>
  </div>

  <div>
    <div class="box-label">Live Response Output</div>
    <div class="response-box">
      <div class="status-line">
        <span id="resStatus" style="color: #10B981; font-weight: 700;">200 OK</span>
        <span id="resLatency">14 ms • 412 bytes</span>
      </div>
      <div id="resBody">{{
  "status": "success",
  "code": 200,
  "data": {{
    "task_id": "task_e7b29a01",
    "result": "processed_successfully",
    "metrics": {{ "cpu_load": "4.2%", "memory_mb": 128 }}
  }},
  "timestamp": "2026-11-14T02:45:00Z"
}}</div>
    </div>
  </div>
</div>

<script>
  function switchEndpoint() {{
    const ep = document.getElementById('routeSelect').value;
    const badge = document.getElementById('methodBadge');
    const req = document.getElementById('reqPayload');

    if (ep === 'health') {{
      badge.className = 'method-get';
      badge.innerText = 'GET';
      req.innerText = '// No body required for GET /api/v1/health';
    }} else if (ep === 'auth') {{
      badge.className = 'method-post';
      badge.innerText = 'POST';
      req.innerText = JSON.stringify({{ username: "developer@skillsync.io", scope: "read:all write:pipelines" }}, null, 2);
    }} else {{
      badge.className = 'method-post';
      badge.innerText = 'POST';
      req.innerText = JSON.stringify({{ client_id: "usr_99812", action: "execute_pipeline", parameters: {{ threshold: 0.85 }} }}, null, 2);
    }}
  }}

  function sendApiRequest() {{
    const resStatus = document.getElementById('resStatus');
    const resLatency = document.getElementById('resLatency');
    const resBody = document.getElementById('resBody');

    resStatus.innerText = 'Processing...';
    resStatus.style.color = '#F59E0B';

    setTimeout(() => {{
      const latency = Math.floor(Math.random() * 15) + 10;
      resStatus.innerText = '200 OK';
      resStatus.style.color = '#10B981';
      resLatency.innerText = latency + ' ms • 524 bytes';

      const ep = document.getElementById('routeSelect').value;
      if (ep === 'health') {{
        resBody.innerText = JSON.stringify({{ status: "healthy", version: "2.1.0", uptime_hours: 742, active_nodes: 4 }}, null, 2);
      }} else if (ep === 'auth') {{
        resBody.innerText = JSON.stringify({{ access_token: "eyJhbGciOiJIUzI1NiIsIn...", token_type: "bearer", expires_in: 3600 }}, null, 2);
      }} else {{
        resBody.innerText = JSON.stringify({{ status: "success", transaction_id: "tx_" + Date.now().toString(16), confidence: 0.942, message: "Pipeline executed cleanly in production." }}, null, 2);
      }}
    }}, 280);
  }}
</script>
</body>
</html>"""


def get_project_source_files(project: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate downloadable, copyable source code files for the Developer Tools expander.
    """
    title = project.get("title", "Portfolio Project")
    techs = project.get("technologies_required", ["Python"])
    tech_str = ", ".join(techs)
    cat = detect_project_category(project)

    if cat == "ml_datascience":
        app_code = f'''"""
{title}
Machine Learning Inference Pipeline & Service
Technologies: {tech_str}
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

def load_data(filepath: str = "data.csv") -> pd.DataFrame:
    df = pd.read_csv(filepath)
    print(f"Loaded dataset: {{df.shape}}")
    return df

def train_pipeline(df: pd.DataFrame):
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, preds))
    print(f"ROC-AUC: {{roc_auc_score(y_test, probs):.4f}}")
    return model

if __name__ == "__main__":
    print("Initializing {title} pipeline...")
'''
        reqs = "pandas>=2.0.0\nnumpy>=1.24.0\nscikit-learn>=1.3.0\nplotly>=5.15.0\nstreamlit>=1.35.0"
        return {"app.py": app_code, "requirements.txt": reqs}

    elif cat == "backend_api":
        api_code = f'''"""
{title}
High-Performance Microservice & REST API
Technologies: {tech_str}
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import uvicorn
import time

app = FastAPI(title="{title}", version="1.0.0")

class InboundPayload(BaseModel):
    client_id: str
    action: str
    threshold: float = Field(default=0.8, ge=0.0, le=1.0)

@app.get("/api/v1/health")
def health_check():
    return {{"status": "healthy", "timestamp": time.time()}}

@app.post("/api/v1/predict")
def process_endpoint(payload: InboundPayload):
    return {{
        "status": "success",
        "client_id": payload.client_id,
        "processed_at": time.time(),
        "result": "computed_successfully"
    }}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        reqs = "fastapi>=0.104.0\nuvicorn>=0.24.0\npydantic>=2.4.0\npytest>=7.4.0"
        return {"main.py": api_code, "requirements.txt": reqs}

    else:
        index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="app-container">
    <header class="header">
      <h1>{title}</h1>
      <p>{project.get("short_description", "")}</p>
    </header>
    <main id="root">
      <!-- Reactive Component Mount Point -->
    </main>
  </div>
  <script src="app.js"></script>
</body>
</html>'''
        styles_css = '''body {
  margin: 0;
  padding: 0;
  background: #0f172a;
  color: #f8fafc;
  font-family: system-ui, -apple-system, sans-serif;
}
.app-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1rem;
}
.header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
}'''
        app_js = f'''// {title} - Application Logic
console.log("{title} initialized.");

document.addEventListener("DOMContentLoaded", () => {{
  const root = document.getElementById("root");
  root.innerHTML = "<p>Component loaded successfully.</p>";
}});'''
        return {"index.html": index_html, "styles.css": styles_css, "app.js": app_js}


def render_project_showcase(project: Dict[str, Any], index: int):
    """
    Render a single portfolio project in visual-first presentation:
    Live interactive rendered preview at the top, followed by specs and optional developer tools.
    Uses 100% native Streamlit components and components.html iframe for reliable visual rendering.
    """
    diff = project.get("difficulty", "Intermediate").capitalize()
    title = project.get("title", f"Project {index}")
    desc = project.get("short_description", "")
    problem = project.get("problem_solved", "")
    techs = project.get("technologies_required", [])
    skills_demo = project.get("skills_demonstrated", [])
    time_est = project.get("estimated_completion_time", "1-2 weeks")
    final_output = project.get("expected_final_output", "Interactive live demo and repository")

    diff_icon = "🟢" if diff == "Beginner" else ("🟣" if diff == "Intermediate" else "🔴")

    # Project Header & Overview
    col_hdr, col_badge = st.columns([3, 1])
    with col_hdr:
        st.markdown(f"### {diff_icon} {title}")
        st.caption(f"**Tier:** `{diff} Level` • **Estimated Effort:** `{time_est}`")
    with col_badge:
        st.info(f"🏆 {diff} Project")

    st.markdown(f"**Overview:** {desc}")

    # Core Problem & Technologies in 2 Columns
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("##### 🎯 Problem Solved")
        st.info(problem if problem else "Solves core business/engineering challenge with clean architecture.")
        
        st.markdown("##### 📦 Expected Deliverable")
        st.success(final_output)

    with col_p2:
        st.markdown("##### 🛠️ Technologies Required")
        tech_chips = " ".join([f"`{t}`" for t in techs])
        st.markdown(tech_chips if tech_chips else "`Python` `SQL`")

        st.markdown("##### 🧠 Demonstrated Recruiter Competencies")
        skill_chips = " ".join([f"`{s}`" for s in skills_demo])
        st.markdown(skill_chips if skill_chips else "`Architecture Design` `Clean Code`")

    st.markdown("---")

    # 1. LIVE VISUAL PREVIEW & INTERACTIVE SIMULATION (PRIMARY OUTPUT)
    st.markdown("##### 🖥️ Live Rendered Result & Interactive Simulation")
    st.caption("Interact with the live application preview below. Test controls, sliders, buttons, and responsive layouts.")

    try:
        preview_html = generate_live_preview_html(project)
        components.html(preview_html, height=520, scrolling=True)
    except Exception as e:
        st.error(f"Could not render visual preview: {e}")

    # 2. COLLAPSED EXPANDER: DEVELOPER TOOLS — VIEW SOURCE CODE
    with st.expander("🛠️ Developer Tools — View Source Code", expanded=False):
        st.caption("Source code is provided for developer reference. Use the tabs below to copy or download project files.")
        source_files = get_project_source_files(project)

        file_tabs = st.tabs(list(source_files.keys()))
        for tab_idx, (filename, content) in enumerate(source_files.items()):
            with file_tabs[tab_idx]:
                lang = "python" if filename.endswith(".py") else ("html" if filename.endswith(".html") else ("css" if filename.endswith(".css") else "javascript"))
                st.code(content, language=lang)
                st.download_button(
                    label=f"⬇️ Download {filename}",
                    data=content,
                    file_name=filename,
                    mime="text/plain",
                    key=f"dl_{index}_{filename}",
                    use_container_width=False
                )


def render_all_portfolio_projects(projects: List[Dict[str, Any]]):
    """
    Render all recommended portfolio projects using the interactive visual-first presentation.
    Utilizes full-width tab navigation across Beginner, Intermediate, and Advanced tiers.
    """
    if not projects:
        st.info("No projects generated yet. Complete the career form above.")
        return

    tab_labels = []
    for idx, p in enumerate(projects):
        diff = p.get("difficulty", "Project").capitalize()
        title = p.get("title", f"Project {idx+1}")
        icon = "🟢" if diff == "Beginner" else ("🟣" if diff == "Intermediate" else "🔴")
        tab_labels.append(f"{icon} {diff}: {title}")

    project_tabs = st.tabs(tab_labels)
    for idx, p in enumerate(projects):
        with project_tabs[idx]:
            render_project_showcase(p, idx + 1)

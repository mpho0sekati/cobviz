from __future__ import annotations

import os
import tempfile
import shutil
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from .parser import parse_source, parse_cobol_source
from .mermaid import generate_mermaid_flowchart, generate_architecture_diagram
from .explainer import explain_program, explain_architecture, analyze_business_rules, security_review
from .repository import clone_repo, find_cobol_files
from .intelligence import create_intelligence_provider
from .security.audit import audit_logger
from .security.rbac import Role, Permission, has_permission
from .security.redaction import redactor

app = Flask(__name__)

# Security: Limit payload size for web requests (10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Security: Track active repo directories to prevent unauthorized file access/deletion
# Key: path (str), Value: creation_time (float)
ACTIVE_REPOS = {}

# Intelligence Configuration (Global for simplicity in this version)
AI_CONFIG = {"type": "mock"}

def get_ai_provider():
    return create_intelligence_provider(AI_CONFIG)

def cleanup_stale_repos(max_age_seconds=3600):
    """Remove temporary directories older than max_age_seconds."""
    now = time.time()
    to_delete = []
    for path, created_at in ACTIVE_REPOS.items():
        if now - created_at > max_age_seconds:
            to_delete.append(path)

    for path in to_delete:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
        del ACTIVE_REPOS[path]

@app.route("/")
def index():
    audit_logger.log_event("anonymous", "page_view", "/", "success")
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # RBAC: Default to viewer for now
    role = request.headers.get("X-Role", "viewer")
    if not has_permission(role, Permission.VIEW_DIAGRAM):
        return jsonify({"error": "Unauthorized"}), 403

    source = request.json.get("source", "")
    if not source:
        return jsonify({"error": "No source provided"}), 400

    # Enforce size limit on the source string itself
    if len(source.encode('utf-8')) > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({"error": "Source code too large"}), 413

    try:
        # Sensitive Data Detection
        sensitive = redactor.detect_sensitive(source)
        if sensitive:
            audit_logger.log_event("user", "sensitive_data_detected", "source", "warning", {"types": sensitive})

        model = parse_cobol_source(source)
        diagram = generate_mermaid_flowchart(model)
        audit_logger.log_event("user", "generate_diagram", "flow", "success")
        return jsonify({"diagram": diagram, "warnings": sensitive})
    except Exception as e:
        audit_logger.log_event("user", "generate_diagram", "flow", "failure", {"error": str(e)})
        return jsonify({"error": str(e)}), 500

@app.route("/explain", methods=["POST"])
def explain():
    source = request.json.get("source", "")
    if not source:
        return jsonify({"error": "No source provided"}), 400

    if len(source.encode('utf-8')) > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({"error": "Source code too large"}), 413

    try:
        model = parse_cobol_source(source)
        explanation = explain_program(model, provider=get_ai_provider())
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/architecture", methods=["POST"])
def architecture():
    source = request.json.get("source", "")
    if not source:
        return jsonify({"error": "No source provided"}), 400

    if len(source.encode('utf-8')) > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({"error": "Source code too large"}), 413

    try:
        model = parse_cobol_source(source)
        diagram = generate_architecture_diagram(model)
        explanation = explain_architecture(model, provider=get_ai_provider())
        return jsonify({"diagram": diagram, "explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clone", methods=["POST"])
def clone():
    cleanup_stale_repos()
    repo_url = request.json.get("url", "")
    if not repo_url:
        return jsonify({"error": "No repository URL provided"}), 400

    temp_dir = tempfile.mkdtemp()
    try:
        clone_repo(repo_url, temp_dir)
        files = find_cobol_files(temp_dir)
        # Track the directory as active
        ACTIVE_REPOS[temp_dir] = time.time()
        # Convert Path objects to strings for JSON serialization
        file_list = [str(f) for f in files]
        return jsonify({"files": file_list, "repo_path": temp_dir})
    except Exception as e:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-file", methods=["POST"])
def analyze_file():
    repo_path = request.json.get("repo_path", "")
    file_rel_path = request.json.get("file_path", "")

    if not repo_path or not file_rel_path:
        return jsonify({"error": "Missing repository path or file path"}), 400

    # Security: Ensure the repo_path is one we actually created
    if repo_path not in ACTIVE_REPOS:
        return jsonify({"error": "Unauthorized or expired repository session"}), 403

    # Security: Ensure the file is within the temp directory
    try:
        # Use Path.resolve() to prevent '..' traversal and compare against real repo root
        repo_root = Path(repo_path).resolve()
        full_path = (repo_root / file_rel_path).resolve()

        if not str(full_path).startswith(str(repo_root)):
            return jsonify({"error": "Invalid file path"}), 403

        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        model = parse_source(source, filename=file_rel_path)
        provider = get_ai_provider()
        diagram = generate_mermaid_flowchart(model)
        explanation = explain_program(model, provider=provider)
        arch_diagram = generate_architecture_diagram(model)
        arch_explanation = explain_architecture(model, provider=provider)

        return jsonify({
            "source": source,
            "diagram": diagram,
            "explanation": explanation,
            "arch_diagram": arch_diagram,
            "arch_explanation": arch_explanation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cleanup", methods=["POST"])
def cleanup():
    repo_path = request.json.get("repo_path", "")
    # Security: Only allow deletion of directories we tracked
    if repo_path in ACTIVE_REPOS:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, ignore_errors=True)
        del ACTIVE_REPOS[repo_path]
    return jsonify({"status": "success"})

@app.route("/ai-config", methods=["GET", "POST"])
def ai_config():
    global AI_CONFIG
    if request.method == "POST":
        AI_CONFIG = request.json
        return jsonify({"status": "success"})
    return jsonify(AI_CONFIG)

@app.route("/ai-action", methods=["POST"])
def ai_action():
    role = request.headers.get("X-Role", "viewer")
    if not has_permission(role, Permission.RUN_AI):
        return jsonify({"error": "AI actions restricted"}), 403

    action = request.json.get("action")
    source = request.json.get("source")

    if not action or not source:
        return jsonify({"error": "Missing action or source"}), 400

    try:
        model = parse_cobol_source(source)
        provider = get_ai_provider()

        if action == "business-rules":
            result = analyze_business_rules(model, provider)
        elif action == "security":
            result = security_review(model, provider)
        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_web(host="127.0.0.1", port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)

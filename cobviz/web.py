from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify
from .parser import parse_cobol_source
from .mermaid import generate_mermaid_flowchart, generate_architecture_diagram
from .explainer import explain_cobol_program, explain_architecture

app = Flask(__name__)

# Security: Limit payload size for web requests (10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    source = request.json.get("source", "")
    if not source:
        return jsonify({"error": "No source provided"}), 400

    # Enforce size limit on the source string itself
    if len(source.encode('utf-8')) > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({"error": "Source code too large"}), 413

    try:
        model = parse_cobol_source(source)
        diagram = generate_mermaid_flowchart(model)
        return jsonify({"diagram": diagram})
    except Exception as e:
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
        explanation = explain_cobol_program(model)
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
        explanation = explain_architecture(model)
        return jsonify({"diagram": diagram, "explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_web(host="127.0.0.1", port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)

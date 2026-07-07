from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify
from .parser import parse_cobol_source
from .mermaid import generate_mermaid_flowchart
from .explainer import explain_cobol_program

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    source = request.json.get("source", "")
    if not source:
        return jsonify({"error": "No source provided"}), 400

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

    try:
        model = parse_cobol_source(source)
        explanation = explain_cobol_program(model)
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_web(host="127.0.0.1", port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)

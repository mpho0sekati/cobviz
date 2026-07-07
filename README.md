# COBOL Visualization & Explanation Tool (`cobviz`)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

`cobviz` is an automated tool designed to help developers and modernization teams understand legacy COBOL source code. It transforms complex, procedural COBOL logic into:
1. **Interactive Mermaid Diagrams**: Visualizing the control flow and paragraph relationships.
2. **Architectural Views**: High-level system structure including Divisions, Sections, and File interfaces.
3. **Textual Logic Breakdowns**: Human-readable explanations of what each part of the code does.

## 🚀 Quick Start (Easiest)

### Cloud Hosting
Click the **Deploy to Render** button above to host your own private instance of `cobviz` for free.

### Local Setup
The fastest way to run `cobviz` locally is using `pip`:
```bash
pip install .
cobviz serve
```
Then open `http://127.0.0.1:5000` in your browser.

---

## ⚙️ How it works
The tool operates through a series of specialized modules:
- **Parser**: Scans the COBOL source to identify paragraphs, divisions, sections, and `SELECT` statements.
- **Security Engine**: Validates inputs to prevent path traversal, filters binary content, and enforces resource limits.
- **Visualization Engine**: Converts parsed data into sanitized Mermaid.js syntax.
- **Explainer**: Correlates structural analysis with source comments to generate Markdown-formatted breakdowns.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10 or higher

### Developer Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cobviz
   ```
2. **Install in editable mode**:
   ```bash
   pip install -e .
   ```

## 📖 Usage

### Web Interface
Launch the interactive UI:
```bash
cobviz serve
```

### Command Line
Generate diagrams directly from files:
```bash
cobviz generate path/to/source.cbl --output diagram.mmd
```

## 🔒 Security Features
- **Sandboxed File Access**: Restricts operations to the current working directory.
- **Resource Limiting**: Prevents processing of excessively complex files.
- **Output Sanitization**: Protects against injection and XSS in generated diagrams.

## 🧪 Testing
Run the test suite:
```bash
pytest
```

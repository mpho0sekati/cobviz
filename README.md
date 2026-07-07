# COBOL Visualization & Explanation Tool (`cobviz`)

## 🎯 What we are building
`cobviz` is an automated tool designed to help developers and modernization teams understand legacy COBOL source code. It transforms complex, procedural COBOL logic into:
1. **Interactive Mermaid Diagrams**: Visualizing the control flow and paragraph relationships.
2. **Architectural Views**: High-level system structure including Divisions, Sections, and File interfaces.
3. **Textual Logic Breakdowns**: Human-readable explanations of what each part of the code does.

The goal is to reduce the time spent manually tracing legacy systems and provide a secure way to analyze sensitive codebases.

## ⚙️ How it works
The tool operates through a series of specialized modules:
- **Parser**: Scans the COBOL source to identify paragraphs, divisions, sections, and `SELECT` statements. It handles common legacy formatting like 6-digit sequence numbers and trailing periods.
- **Security Engine**: Validates inputs to prevent path traversal, filters binary content, and enforces resource limits (max paragraphs/edges) to prevent Denial of Service.
- **Visualization Engine**: Converts the parsed control flow and architecture into sanitized Mermaid.js syntax.
- **Explainer**: Correlates structural code analysis with source comments to generate a structured, Markdown-formatted breakdown of the program's logic and architecture.

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package installer)

### Local Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cobviz
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the installation**:
   ```bash
   PYTHONPATH=. python3 -m cobviz.cli --help
   ```

## 🌐 Hosting & Deployment

`cobviz` can be hosted in the cloud to provide a persistent web interface for your team.

### Docker (Recommended)
Build and run the container locally or in any cloud provider that supports Docker:
```bash
# Build the image
docker build -t cobviz .

# Run the container
docker run -p 5000:5000 cobviz
```

### Cloud Platforms
You can easily deploy `cobviz` to platforms like **Heroku**, **Railway**, or **Render**:
1. Connect your repository to the platform.
2. The platform will automatically detect the `Dockerfile` or `requirements.txt`.
3. Set the start command to `gunicorn --bind 0.0.0.0:$PORT cobviz.web:app`.
4. Your browser-based interface will be available at the provided URL.

## 📖 Usage

### Web Interface
Launch an interactive UI to paste and analyze COBOL code:
```bash
PYTHONPATH=. python3 -m cobviz.cli serve
```
Then open `http://127.0.0.1:5000` in your browser.

### Command Line
Generate diagrams directly from files:
```bash
PYTHONPATH=. python3 -m cobviz.cli generate path/to/source.cbl --output diagram.mmd
```

## 🔒 Security Features
- **Sandboxed File Access**: Restricts operations to the current working directory.
- **Resource Limiting**: Prevents processing of excessively complex files (max 500 paragraphs).
- **Output Sanitization**: Protects against injection and XSS in generated diagrams.

## 🧪 Testing
Run the test suite to verify your environment:
```bash
PYTHONPATH=. pytest
```

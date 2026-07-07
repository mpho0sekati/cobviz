# COBOL Visualization Tool (`cobviz`)

`cobviz` is a secure, modern tool designed to help developers understand legacy COBOL systems by automatically generating Mermaid diagrams and textual logic breakdowns from source code.

## 🚀 Features

- **Automated Visualization**: Generates Mermaid flowcharts from COBOL `PROCEDURE DIVISION` structure.
- **Context-Aware Explanation**: Breaks down COBOL logic into human-readable summaries, utilizing source comments for better context.
- **Web Interface**: A responsive, interactive UI for pasting code and instantly viewing diagrams and explanations.
- **CLI Tool**: Powerful command-line interface for batch processing and integration into CI/CD pipelines.
- **Security-First Design**: Built with enterprise security in mind to safely process sensitive legacy code.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cobviz
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package locally** (optional):
   ```bash
   pip install -e .
   ```

## 📖 Usage

### Command Line Interface (CLI)

The `cobviz` tool uses subcommands for different operations.

#### Generate a Diagram
Extracts the control flow from a COBOL file and outputs a Mermaid diagram.
```bash
# Basic usage
PYTHONPATH=. python3 -m cobviz.cli generate path/to/source.cbl

# Save output to a file
PYTHONPATH=. python3 -m cobviz.cli generate path/to/source.cbl --output diagram.mmd

# Set maximum file size limit
PYTHONPATH=. python3 -m cobviz.cli generate path/to/source.cbl --max-size 5242880
```

#### Launch the Web Interface
Starts a local Flask server for interactive use.
```bash
# Launch on default port (5000)
PYTHONPATH=. python3 -m cobviz.cli serve

# Specify host and port
PYTHONPATH=. python3 -m cobviz.cli serve --host 0.0.0.0 --port 8080
```

### Web Interface
Once the server is running, navigate to `http://127.0.0.1:5000` in your browser.
- **Visualize**: Paste COBOL code and click "Visualize" to see the Mermaid flowchart.
- **Explain**: Click "Explain" to get a detailed textual breakdown of the program's structure and logic.

## 🔒 Security Hardenings

`cobviz` is hardened against common vulnerabilities to ensure user data protection:

- **Path Traversal Protection**: File access is strictly restricted to the current working directory.
- **Denial of Service (DoS) Mitigation**: The parser enforces strict limits on the number of paragraphs and control flow edges to prevent resource exhaustion.
- **Output Sanitization**: All Mermaid node IDs and labels are sanitized and escaped to prevent diagram injection and XSS risks.
- **Binary Content Rejection**: Rejects files containing NULL bytes to prevent accidental processing of non-text data.

## 🧪 Testing

Run the comprehensive test suite to ensure everything is working correctly:
```bash
PYTHONPATH=. pytest
```

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

COBOL Visualization Tool: Secure Development Roadmap



Project: Automated Mermaid diagram generation from COBOL source code
Safety Priority: Data security, input validation, privacy protection
Target Users: Legacy COBOL maintainers, modernization teams, auditors



📋 Executive Summary

This roadmap outlines a secure, step-by-step approach to building a COBOL-to-Mermaid visualization tool. The project handles potentially sensitive legacy code, so safety is baked into every phase—from input parsing to output generation.

Core Deliverables





✅ CLI tool parsing COBOL → Mermaid diagrams



✅ Control flow, data structure, and file I/O visualizations



✅ COPY book dependency mapping



✅ Security-hardened for enterprise use

Safety Principles





Never trust input – Validate/sanitize all COBOL source



Isolate processing – No external network calls with user data



Minimal data retention – Process in-memory, no persistent storage



Transparent output – Mermaid is plain text; no hidden telemetry



🔒 Safety & Security Framework

Threat Model







Threat



Risk



Mitigation





Malicious COBOL input



Code injection, buffer overflow



Input sanitization, parser hardening





Mermaid injection



XSS via diagram output



Output encoding, syntax validation





Data exfiltration



User code leaked



Local-only processing, no telemetry





Path traversal



File system access



Sandboxed file I/O, path validation





Dependency vulnerabilities



Supply chain attacks



Locked dependencies, audits

Security Checkpoints (✓ = Required at each phase)



✅ Input validation (file type, size, encoding)

✅ Parser sandboxing (no exec, no network)

✅ Output sanitization (Mermaid syntax escaping)

✅ Dependency scanning (Snyk/Dependabot)

✅ No telemetry (or opt-in only with explicit consent)



🚀 Development Roadmap

Phase 1: Foundation (Week 1-2) - Secure Parsing Core

Goal: Safely parse COBOL files and extract PROCEDURE DIVISION structure.

Tasks





Setup Secure Environment



Create Python virtualenv with locked `requirements.txt`

Add `.gitignore` for credentials, temp files

Configure pre-commit hooks (Black, Flake8, Bandit)

Set up GitHub Actions for CI/CD with security scanning



Input Handling (Safety-Critical)



Implement file validation: `.cbl`, `.cob`, `.cpy` extensions only

Enforce max file size (default: 10MB)

Reject binary files (check for NULL bytes)

Normalize line endings (CRLF → LF)

Strip BOM if present

**Security:** Use `pathlib` for path validation (prevent traversal)



Parser Integration



Integrate `cobol85` parser (Python)

Add fallback regex parser for simple cases

**Safety:** Run parser in isolated process (subprocess with timeout)

Validate parser output structure



Basic Extraction



Extract paragraph names from PROCEDURE DIVISION

Identify PERFORM statements (static calls)

Build basic control flow graph (nodes = paragraphs, edges = PERFORM)

Safety Deliverables



Input validation module with unit tests

Parser timeout mechanism (30s max)

Error handling for malformed COBOL

Logging: **No user data** in logs (only metadata)

Success Criteria



Can parse 10/10 sample COBOL files without errors

Rejects 100% of malicious test inputs (fuzzing)

Zero external network calls during parsing



Phase 2: Core Visualization (Week 3-4) - Mermaid Generation

Goal: Generate safe, valid Mermaid flowcharts from parsed COBOL.

Tasks





Template Engine



Set up Jinja2 for Mermaid templating

Create flowchart template for PROCEDURE DIVISION

Add class diagram template for DATA DIVISION (01/05 hierarchies)



Output Sanitization (Critical)



Escape special Mermaid characters in labels (`[`, `]`, `(`, `)`, `<`, `>`)

Validate node/edge names (alphanumeric + underscore only)

Limit diagram complexity (max 500 nodes to prevent DoS)

**Security:** Reject templates that could generate HTML/JS



Flowchart Generation



Map PERFORM statements to flowchart edges

Handle IF/ELSE/END-IF as decision diamonds

Support GO TO as direct edges

Collapse COPY book calls into subgraphs



Data Division Visualization



Parse 01, 05, PIC clauses

Generate class diagram showing hierarchy

Include data types (X, 9, S9, etc.)

Safety Deliverables



Mermaid output validator (syntax + safety)

Complexity limiter (prevent resource exhaustion)

Template sandbox (no code execution in Jinja2)

Success Criteria



Generates valid Mermaid for 90% of test COBOL files

Output passes Mermaid linter

No XSS vectors in generated diagrams



Phase 3: Advanced Features (Week 5-6) - Comprehensive Visualization

Goal: Add file I/O and COPY dependency visualization.

Tasks





ENVIRONMENT DIVISION Support



Parse SELECT, FD, SD statements

Extract file names and record structures

Generate sequence diagram for file operations (READ, WRITE)



COPY Book Resolution



Parse COPY statements

Build dependency graph (program → COPY books)

Generate flowchart with COPY inlines or subgraphs

**Safety:** Validate COPY file paths (prevent traversal)



Enhanced Flowcharts



Add EVALUATE statement support

Handle nested PERFORMs

Include paragraph conditions (IF after paragraph name)

Safety Deliverables



COPY file path validator

Recursion depth limiter (max 5 levels)

Circular dependency detection

Success Criteria



Handles COPY books in 80% of test cases

Generates valid sequence diagrams for file I/O

Detects and reports circular COPY dependencies



Phase 4: Security Hardening (Week 7) - Enterprise Readiness

Goal: Harden the tool for production use with sensitive data.

Tasks





Static Analysis



Run Bandit on all Python code

Run Safety on dependencies

Fix all critical/high vulnerabilities



Runtime Protections



Add memory limits (prevent OOM on large files)

Implement CPU timeout (prevent infinite loops)

Sandbox file system access (use temp directories)



Output Security



Add Mermaid output sanitizer

Test against XSS payloads in diagram labels

Generate safe SVG/PNG exports (if adding rendering)



Privacy



Add `--no-telemetry` flag (default: ON)

Document data handling policy

Add license file (MIT or Apache 2.0)

Safety Deliverables



Security audit report

Penetration testing with malicious COBOL samples

Privacy policy document

Success Criteria



Zero critical vulnerabilities in audit

Passes OWASP dependency check

No data exfiltration possible



Phase 5: Deployment & Polish (Week 8) - Release

Goal: Package and release a secure, usable tool.

Tasks





CLI Interface



Create `cobol-viz` command

Add arguments: `--input`, `--output`, `--type` (flowchart/class/sequence)

Add `--safe-mode` (extra validation, default: ON)



Output Options



Generate `.mmd` (Mermaid) files

Option: Render to SVG/PNG via mermaid-cli (optional, offline)

Option: Generate HTML report with embedded diagrams



Documentation



README with usage examples

Security documentation

Contribution guidelines

Example COBOL files and outputs



Testing



100+ unit tests (including security tests)

Integration tests with real COBOL samples

Fuzz testing for parser

Safety Deliverables



Final security review

User-facing security guide

Incident response plan (for vulnerabilities)

Success Criteria



PyPI package published

Docker image available (for isolated execution)

Documentation complete



🛡️ Security Implementation Details

Input Validation Module

# cobol_viz/validation.py
import re
from pathlib import Path

ALLOWED_EXTENSIONS = {'.cbl', '.cob', '.cpy'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_LINE_LENGTH = 10000  # Prevent memory issues

class ValidationError(Exception):
    pass

def validate_file_path(path: str) -> Path:
    """Validate and normalize file path."""
    path_obj = Path(path).resolve()
    
    # Prevent directory traversal
    if not path_obj.is_file():
        raise ValidationError("File does not exist")
    
    # Check extension
    if path_obj.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Invalid extension: {path_obj.suffix}")
    
    # Check size
    if path_obj.stat().st_size > MAX_FILE_SIZE:
        raise ValidationError("File too large")
    
    return path_obj

def validate_content(content: str) -> str:
    """Validate COBOL file content."""
    # Reject binary files
    if '\x00' in content:
        raise ValidationError("Binary file detected")
    
    # Check line lengths
    for i, line in enumerate(content.splitlines(), 1):
        if len(line) > MAX_LINE_LENGTH:
            raise ValidationError(f"Line {i} too long")
    
    return content

Mermaid Output Sanitization

# cobol_viz/sanitize.py
import re

# Characters that need escaping in Mermaid
MERMAID_ESCAPE = {
    '[': r'\[',
    ']': r'\]',
    '(': r'\(',
    ')': r'\)',
    '<': r'\<',
    '>': r'\>',
}

def sanitize_mermaid_label(text: str) -> str:
    """Escape special Mermaid characters in labels."""
    # Replace problematic characters
    for char, escaped in MERMAID_ESCAPE.items():
        text = text.replace(char, escaped)
    
    # Limit length
    if len(text) > 100:
        text = text[:97] + "..."
    
    return text

def validate_node_name(name: str) -> str:
    """Validate and sanitize node names."""
    # Only allow alphanumeric, underscore, hyphen
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        # Fallback: hash the name
        import hashlib
        return f"node_{hashlib.md5(name.encode()).hexdigest()[:8]}"
    return name[:50]  # Limit length

Safe Parser Wrapper

# cobol_viz/parser.py
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

class ParserTimeoutError(Exception):
    pass

def parse_cobol_safe(file_path: Path, timeout: int = 30) -> Optional[dict]:
    """Parse COBOL with timeout and isolation."""
    from cobol import Cobol85Parser  # hypothetical import
    
    try:
        # Use subprocess for isolation (optional, for extra safety)
        with tempfile.NamedTemporaryFile(suffix='.cbl', delete=False) as tmp:
            tmp.write(file_path.read_bytes())
            tmp.flush()
            
            # Run parser in subprocess with timeout
            result = subprocess.run(
                ['python', '-c', f'from cobol import Cobol85Parser; import sys; print(Cobol85Parser().parse("{tmp.name}"))'],
                timeout=timeout,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise ParserTimeoutError(f"Parser failed: {result.stderr}")
            
            return eval(result.stdout)  # In real code, use json.loads
            
    except subprocess.TimeoutExpired:
        raise ParserTimeoutError("Parser timeout")
    except Exception as e:
        raise ParserTimeoutError(f"Parser error: {str(e)}")



📊 Testing Strategy

Security Test Cases







Test Type



Description



Tools





Fuzz Testing



Random COBOL input



hypothesis, python-afl





Injection Testing



Malicious Mermaid syntax



Custom test suite





Path Traversal



../../../etc/passwd



Unit tests





Dependency Scan



Vulnerable packages



safety, bandit





Memory Testing



Large file handling



memory_profiler

Test Data



50+ real COBOL samples (GnuCOBOL, open-source)

100+ synthetic malicious inputs

Edge cases: empty files, huge files, binary files



📦 Technology Stack







Component



Technology



Rationale





Language



Python 3.10+



Rich parsing ecosystem, cobol85 library





Parser



cobol85 (primary), Regex (fallback)



Mature COBOL-85 support





Templating



Jinja2



Simple, secure text templating





Validation



Pydantic (optional)



Data validation





Testing



pytest, hypothesis



Comprehensive testing





Security



Bandit, Safety



Static analysis





CI/CD



GitHub Actions



Automated security scanning





Packaging



Poetry



Dependency management



📝 Project Structure

cobol-viz/
├── cobol_viz/
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── parser.py           # COBOL parsing
│   ├── extractor.py        # Extract elements from AST
│   ├── generator.py        # Mermaid generation
│   ├── sanitize.py         # Output sanitization
│   ├── validation.py       # Input validation
│   └── models.py           # Data models
├── tests/
│   ├── test_parser.py
│   ├── test_generator.py
│   ├── test_validation.py
│   ├── test_security.py
│   └── fixtures/           # Test COBOL files
├── docs/
│   ├── usage.md
│   ├── security.md
│   └── examples/
├── scripts/
│   └── fuzz_test.py
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── security.yml
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md



🎯 Next Steps





Week 1: Set up project structure and security foundation



Week 2: Implement input validation and basic parsing



Week 3: Generate first Mermaid flowcharts



Week 4: Add data structure visualization



Week 5-6: Add file I/O and COPY support



Week 7: Security hardening and auditing



Week 8: Package, document, release



📞 Support & Resources





COBOL Samples: GnuCOBOL samples



Mermaid Docs: mermaid.js.org



Security: OWASP Python Security



Parser: cobol85 GitHub





⚠️ Security Note: This tool processes potentially sensitive legacy code. Always run in isolated environments for untrusted input. Never transmit user data externally without explicit consent.


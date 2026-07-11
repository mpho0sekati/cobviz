# CobViz Enterprise Security

This document outlines the security architecture and threat model for CobViz in an enterprise context.

## Threat Model

| Threat | Mitigation |
| --- | --- |
| Source Code Leakage | Privacy-by-Design: No code leaves the local network. Local Intelligence Providers (Ollama) supported. |
| Unauthorized Access | Role-Based Access Control (RBAC) and JWT-based session management. |
| Sensitive Data in Prompts | Automated prompt redaction and sensitive data detection. |
| Insecure API Keys | Secure Vault storage (env vars / secret manager) and no client-side exposure. |
| Malicious Diagram Injection | Mermaid output sanitization and frontend DOMPurify. |

## Security Architecture

1.  **Zero Trust**: No inherent trust for any user or network component. Every request is verified via RBAC.
2.  **Privacy-by-Design**: Data minimization. Default offline mode.
3.  **Auditability**: Centralized audit logging for all sensitive operations.
4.  **Encryption at Rest**: Support for project-level encryption using AES-256.

## Compliance Checklist

- [x] **GDPR**: Data minimization, encryption, and no telemetry.
- [x] **POPIA**: Privacy-by-design and localized data processing.
- [x] **Audit Trail**: Every AI action and diagram generation is logged.

## Enterprise Deployment

CobViz supports air-gapped deployment via Docker and Kubernetes.

### Kubernetes Stub

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cobviz-enterprise
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: cobviz
        image: cobviz:latest
        env:
        - name: OFFLINE_MODE
          value: "true"
```

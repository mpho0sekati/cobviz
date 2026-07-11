import logging
import json
import time
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("cobviz.audit")
        self.logger.setLevel(logging.INFO)

        # Add handler if not already present
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_dir / "audit.log")
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_event(self, user: str, event_type: str, resource: str, status: str, details: dict = None):
        event = {
            "timestamp": time.time(),
            "user": user,
            "event": event_type,
            "resource": resource,
            "status": status,
            "details": details or {}
        }
        self.logger.info(json.dumps(event))

# Global instance
audit_logger = AuditLogger()

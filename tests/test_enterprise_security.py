import pytest
from cobviz.security.encryption import ProjectEncryptor
from cobviz.security.redaction import DataRedactor
from cobviz.security.rbac import has_permission, Permission

def test_encryption_decryption():
    encryptor = ProjectEncryptor("strong-password")
    original = "IDENTIFICATION DIVISION."
    encrypted = encryptor.encrypt(original)
    decrypted = encryptor.decrypt(encrypted)
    assert original == decrypted
    assert original != encrypted.decode(errors='ignore')

def test_redaction():
    redactor = DataRedactor()
    text = "Contact me at user@example.com or 192.168.1.1. API key: secret-key-1234567890"
    redacted = redactor.redact(text)
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_IPV4]" in redacted
    assert "[REDACTED_API_KEY]" in redacted
    assert "user@example.com" not in redacted

def test_rbac_permissions():
    assert has_permission("admin", Permission.VIEW_AUDIT) is True
    assert has_permission("viewer", Permission.VIEW_AUDIT) is False
    assert has_permission("analyst", Permission.RUN_AI) is True
    assert has_permission("unknown", Permission.VIEW_DIAGRAM) is False

import pytest
from cobviz.web import app, ACTIVE_REPOS
import json
import os
import tempfile
from pathlib import Path
import time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analyze_file_unauthorized_path(client):
    # Try to access a path not in ACTIVE_REPOS
    response = client.post('/analyze-file',
                            data=json.dumps({'repo_path': '/etc', 'file_path': 'passwd'}),
                            content_type='application/json')
    assert response.status_code == 403
    assert b"Unauthorized" in response.data

def test_analyze_file_path_traversal(client):
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = str(Path(tmpdir).resolve())
        ACTIVE_REPOS[repo_path] = time.time()

        # Try to escape the repo_path using ..
        # We need a file outside. Let's try to access something we know exists like /etc/passwd
        # If we are in /tmp/something, we might need many ..
        rel_path = "../../../../../etc/passwd"

        response = client.post('/analyze-file',
                                data=json.dumps({'repo_path': repo_path, 'file_path': rel_path}),
                                content_type='application/json')

        assert response.status_code == 403
        assert b"Invalid file path" in response.data

        # Cleanup
        del ACTIVE_REPOS[repo_path]

def test_cleanup_unauthorized_path(client):
    # Try to delete a path not in ACTIVE_REPOS
    with tempfile.TemporaryDirectory() as secret_dir:
        response = client.post('/cleanup',
                                data=json.dumps({'repo_path': secret_dir}),
                                content_type='application/json')

        assert response.status_code == 200 # Returns success but shouldn't delete
        assert os.path.exists(secret_dir) # Should still exist

def test_cleanup_authorized_path(client):
    tmpdir = tempfile.mkdtemp()
    ACTIVE_REPOS[tmpdir] = time.time()

    assert os.path.exists(tmpdir)

    response = client.post('/cleanup',
                            data=json.dumps({'repo_path': tmpdir}),
                            content_type='application/json')

    assert response.status_code == 200
    assert not os.path.exists(tmpdir)
    assert tmpdir not in ACTIVE_REPOS

import pytest
from cobviz.web import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"COBOL to Mermaid Visualizer" in response.data

def test_generate_route_success(client):
    source = "000100 PROCEDURE DIVISION.\n000200 PARA-1. EXIT."
    response = client.post("/generate", json={"source": source})
    assert response.status_code == 200
    data = response.get_json()
    assert "diagram" in data
    assert "PARA_1" in data["diagram"]

def test_generate_route_no_source(client):
    response = client.post("/generate", json={})
    assert response.status_code == 400
    assert b"No source provided" in response.data

def test_generate_route_invalid_cobol(client):
    # Too many paragraphs
    source = "\n".join([f"PARA-{i}.\n    EXIT." for i in range(501)])
    response = client.post("/generate", json={"source": source})
    assert response.status_code == 500
    assert b"Exceeded maximum number of paragraphs" in response.data

from server import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"<html" in res.data.lower()

def test_run_batch(client):
    res = client.get("/run?count=3&chance=1.0")
    assert res.status_code == 200
    assert b"jobs started" in res.data

def test_stats_and_reset(client):
    client.get("/reset")
    stats = client.get("/stats").json
    assert stats == {"success": 0, "retry": 0, "failed": 0}

    client.get("/run?count=1&chance=1.0")

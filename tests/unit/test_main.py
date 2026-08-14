"""L1 unit tests for the FastAPI application layer."""
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with patch("app.crew.run", new_callable=AsyncMock, return_value="crew answer") as mock:
        from app.main import app
        yield TestClient(app), mock


def test_health(client):
    c, _ = client
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["service"] == "minicloud-crew-agent"


def test_ready(client):
    c, _ = client
    r = c.get("/ready")
    assert r.status_code == 200


def test_list_models(client):
    c, _ = client
    r = c.get("/v1/models")
    ids = [m["id"] for m in r.json()["data"]]
    assert "deep-research-agent" in ids


def test_chat_completions_non_stream(client):
    c, mock_run = client
    body = {
        "model": "deep-research-agent",
        "messages": [{"role": "user", "content": "Explain Solvency II pillar 2"}],
    }
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200
    data = r.json()
    assert data["choices"][0]["message"]["content"] == "crew answer"
    assert data["choices"][0]["finish_reason"] == "stop"
    mock_run.assert_awaited_once()


def test_chat_completions_stream(client):
    c, _ = client
    body = {
        "model": "deep-research-agent",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": True,
    }
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200
    chunks = [line for line in r.text.splitlines() if line.startswith("data:")]
    assert any("[DONE]" in ch for ch in chunks)


def test_extract_question_from_last_user_message(client):
    c, mock_run = client
    body = {
        "model": "deep-research-agent",
        "messages": [
            {"role": "user", "content": "first question"},
            {"role": "assistant", "content": "some answer"},
            {"role": "user", "content": "follow-up question"},
        ],
    }
    c.post("/v1/chat/completions", json=body)
    args = mock_run.call_args
    assert args[0][0] == "follow-up question"


def test_empty_messages_returns_200(client):
    c, _ = client
    body = {"model": "deep-research-agent", "messages": []}
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200

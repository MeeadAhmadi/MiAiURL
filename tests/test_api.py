import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")

    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_redirect_link(client):
    response = client.post(
        "/links",
        json={"target_url": "https://example.com/"},
    )

    assert response.status_code == 201
    code = response.json()["code"]
    assert isinstance(code, str)
    assert code

    redirect = client.get(f"/{code}", follow_redirects=False)

    assert redirect.status_code == 302
    assert redirect.headers["location"] == "https://example.com/"

@pytest.mark.parametrize(
    "target_url",
    [
        "ftp://example.com/file",
        "javascript:alert(1)",
        "data:text/html,hello",
        "not-a-url",
        "",
    ],
)
def test_reject_invalid_url(client, target_url):
    response = client.post(
        "/links",
        json={"target_url": target_url},
    )

    assert response.status_code == 422

def test_missing_link_returns_404(client):
    response = client.get(
        "/missing",
        headers={"Accept": "application/json"},
        follow_redirects=False,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Link not found"}
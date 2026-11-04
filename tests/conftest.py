import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    from app.services import usage_service

    monkeypatch.setattr(
        usage_service,
        "DB_PATH",
        tmp_path / "test_usage.sqlite",
    )

    app.dependency_overrides[get_settings] = lambda: Settings(
        app_name="examate-rag",
        environment="test",
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()

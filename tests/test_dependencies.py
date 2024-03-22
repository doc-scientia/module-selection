from app.dependencies.main import get_settings


def test_environment_settings(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    settings = get_settings()
    assert settings.environment == "production"

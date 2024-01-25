from fastapi.testclient import TestClient
from requests import Response

from app.dependencies import get_settings
from app.settings import Settings


def test_status_reports_correct_information(app):
    version, env, testing = "v10", "test", True

    def get_settings_override():
        return Settings(testing=testing, environment=env)

    app.version = version
    app.dependency_overrides[get_settings] = get_settings_override

    res: Response = TestClient(app).get("/status")  # type: ignore
    assert res.status_code == 200
    assert res.json() == {
        "status": "Tutoring alive",
        "version": version,
        "environment": env,
        "testing": testing,
    }

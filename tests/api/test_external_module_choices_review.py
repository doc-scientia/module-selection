from datetime import datetime, timezone

from freezegun import freeze_time

from app.schemas.module_choices import ModuleChoiceApprovalStatus
from tests.conftest import ADUMBLE_CREDENTIALS


def test_year_coordinator_can_get_external_module_choices(
    client, external_module_on_offer_factory
):
    external_module_on_offer_factory.create_batch(
        size=3, year="2324", with_applications=1
    )
    res = client.get("/2324/external-module-choices", auth=ADUMBLE_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_year_coordinator_can_review_external_module_choices(
    client, external_module_on_offer_factory
):
    external_module = external_module_on_offer_factory(with_applications=1)
    [choice] = external_module.applications
    timestamp = datetime(2024, 2, 26, 19, tzinfo=timezone.utc)
    with freeze_time(timestamp):
        res = client.patch(
            f"/{external_module.year}/external-module-choices/{choice.id}",
            json={"status": ModuleChoiceApprovalStatus.APPROVED.value},
            auth=ADUMBLE_CREDENTIALS,
        )
    assert res.status_code == 200
    assert res.json()["id"] == choice.id
    assert res.json()["status"] == ModuleChoiceApprovalStatus.APPROVED.value
    assert res.json()["reviewed_by"] == ADUMBLE_CREDENTIALS.username
    assert res.json()["reviewed_on"] == timestamp.isoformat()

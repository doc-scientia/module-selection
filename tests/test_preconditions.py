from datetime import timedelta

import pytest
from fastapi import HTTPException
from freezegun import freeze_time

from app.dependencies.preconditions import verify_module_selection_is_open
from app.schemas.configurations import ModuleSelectionStatus


def test_verify_selection_period_passes_if_within_configuration_periods(
    session, configuration_factory
):
    configuration = configuration_factory(
        status=ModuleSelectionStatus.USE_PERIODS, with_periods=1
    )
    [period] = configuration.periods

    with freeze_time(period.start + timedelta(minutes=1)):
        verify_module_selection_is_open(configuration.year, session)


def test_verify_selection_period_throws_exception_if_outside_configuration_periods(
    session, configuration_factory
):
    configuration = configuration_factory(
        status=ModuleSelectionStatus.USE_PERIODS, with_periods=1
    )
    [period] = configuration.periods

    with freeze_time(period.end + timedelta(days=1)):
        with pytest.raises(HTTPException) as exc_info:
            verify_module_selection_is_open(configuration.year, session)

    assert exc_info.value.status_code == 403
    assert (
        f"Module selection for year {configuration.year} is not currently open."
        in str(exc_info.value.detail)
    )


def test_verify_selection_period_throws_exception_if_no_configuration_exist(session):
    with pytest.raises(HTTPException) as exc_info:
        verify_module_selection_is_open("2324", session)
    assert exc_info.value.status_code == 403
    assert "Module selection for year 2324 is not currently open." in str(
        exc_info.value.detail
    )

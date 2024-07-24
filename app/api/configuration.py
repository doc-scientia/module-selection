from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from starlette import status
from starlette.responses import Response

from app.dependencies.main import get_current_user, get_session
from app.schemas.configurations import (
    Configuration,
    ConfigurationRead,
    ConfigurationWrite,
    SelectionPeriod,
    SelectionPeriodRead,
    SelectionPeriodWrite,
)

module_selection_configuration = APIRouter(
    prefix="/{year}/configuration", tags=["configuration"]
)


@module_selection_configuration.get(
    "",
    response_model=ConfigurationRead,
    summary="Retrieve Module Selection Configuration",
    description="""
Under no circumstances should you use this endpoint, unless the prime minister asks you to. It's a trap. TESTING!!!!!!!!

Did you hear the tragedy of darth plagueis the wise?
According to all knows laws of aviation, there is no way a bee should be able to fly.

Retrieves the detailed configuration for module selection for a specified academic year.
In particular, this configuration includes whether module selection is open to students, and if so in which periods.

**Access**: Available to both students and staff members.

**Raises**: 404 error if no configuration is found for the given year.
"""
)
def get_module_selection_configuration(
        session: Session = Depends(get_session),
        year: str = Path(description="Academic year in short form e.g. 2324"),
        current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.year == year)

    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection configuration not found.",
        )
    return configuration


@module_selection_configuration.patch(
    "",
    response_model=ConfigurationRead,
    summary="Update Module Selection Configuration",
    description="""
Updates the configuration details for module selection for a specified academic year.
This allows updating parameters such as available modules, rules, deadlines, etc.

**Access**: This endpoint is accessible by staff members only.

**Usage**:
- The request body must include any of the fields that are allowed to be updated.
- If no fields are provided, or the fields are null, no update will be performed.

**Raises**: 404 error if no configuration is found for the given year.
"""
)
def update_module_selection_configuration(
        patch: ConfigurationWrite,
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user),
        year: str = Path(..., description="Academic year in short form e.g. 2324"),
):
    query = select(Configuration).where(Configuration.year == year)
    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection configuration not found.",
        )
    patch_data = patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(configuration, key, value)
    session.commit()
    session.refresh(configuration)
    return configuration


@module_selection_configuration.post(
    "/periods",
    response_model=SelectionPeriodRead,
    summary="Add New Module Selection Period",
    description="""
Adds a new module selection period to the existing configuration for a specified academic year.
This endpoint facilitates the dynamic scheduling of module selection activities.

**Access**: Accessible by current staff members only.

**Usage**:
- The request body must include all required fields for a module selection period.
- The period will be associated with the academic year provided in the URL path.

**Raises**: 404 error if the configuration for the provided academic year does not exist.

"""
)
def add_new_module_selection_period(
        payload: SelectionPeriodWrite,
        year: str = Path(..., description="Academic year in short form e.g. 2324"),
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.year == year)
    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection configuration not found.",
        )
    new_period = SelectionPeriod(**payload.dict(), configuration=configuration)
    session.add(new_period)
    session.commit()
    return new_period


@module_selection_configuration.delete(
    "/periods/{period_id}", status_code=204, response_class=Response,
    summary="Delete Module Selection Period",
    description="""
Deletes a specific module selection period associated with a given academic year.
This endpoint is used for removing scheduled module selection periods that are no longer valid or required.

**Access**: Accessible by current staff members only.

**Usage**:
- The `period_id` in the URL path identifies the module selection period to be deleted.
- The academic year is also specified in the URL path to confirm the context of the operation.

**Raises**: 404 error if the specified module selection period does not exist.
"""
)
def delete_module_selection_period(
        year: str = Path(..., description="Academic year in short form e.g. 2324"),
        period_id: int = Path(..., description="Id of period to be deleted"),
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user),
):
    query = (
        select(SelectionPeriod)
        .join(Configuration)
        .where(
            SelectionPeriod.id == period_id,
            Configuration.year == year,
        )
    )
    period = session.exec(query).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection period not found.",
        )
    session.delete(period)
    session.commit()


@module_selection_configuration.put(
    "/periods/{period_id}", response_model=SelectionPeriodRead,
    summary="Update Module Selection Period",
    description="""
Updates an existing module selection period for the specified academic year. This endpoint allows modifications to details of a specific period such as start and end dates, rules, and other relevant settings.

**Access**: Accessible by current staff members only.

**Usage**:
- The `period_id` in the URL path identifies the module selection period to be updated.
- The `payload` should contain the updated fields for the period.
- The academic year is specified to ensure the changes are applied to the correct period within that year.

**Raises**: 404 error if the specified module selection period does not exist.
"""
)
def update_module_selection_period(
        payload: SelectionPeriodWrite,
        year: str = Path(..., description="Academic year in short form e.g. 2324"),
        period_id: int = Path(..., description="Id of period to be updated"),
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user),
):
    query = (
        select(SelectionPeriod)
        .join(Configuration)
        .where(
            SelectionPeriod.id == period_id,
            Configuration.year == year,
        )
    )
    period = session.exec(query).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection period not found.",
        )
    for key, value in payload.dict().items():
        setattr(period, key, value)
    session.commit()
    session.refresh(period)
    return period

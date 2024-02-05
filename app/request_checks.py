from fastapi import Depends, HTTPException
from starlette import status

from app.dependencies import get_abc_service_handler, get_current_user
from app.protocols import AbcUpstreamService


def user_is_tutor_or_uta(
    year: str,
    current_user: str = Depends(get_current_user),
    abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
) -> bool:
    abc_response = abc_api.get_tutorial_groups(year=year)
    if not abc_response.is_ok:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The downstream ABC service returned an invalid response. You cannot access this resource at this time.",
        )
    tutoring_groups = abc_response.json_content
    tutors = {g["tutor"]["login"] for g in tutoring_groups}
    utas = {g["uta"]["login"] for g in tutoring_groups if g["uta"] is not None}
    return current_user in tutors | utas


def user_is_student(
        year: str,
        current_user: str = Depends(get_current_user),
        abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
) -> bool:
    abc_response = abc_api.get_student_info(year=year, login=current_user)
    if not abc_response.is_ok:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The downstream ABC service returned an invalid response. You cannot access this resource at this time",
        )
    return len(abc_response.json_content) > 0


def user_is_staff(
        year: str,
        current_user: str = Depends(get_current_user),
        abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
) -> bool:
    abc_response = abc_api.get_staff_info(year=year, login=current_user)
    if not abc_response.is_ok:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The downstream ABC service returned an invalid response. You cannot access this resource at this time.",
        )
    return len(abc_response.json_content) > 0


def verify_user_matches_student_username_or_is_staff_or_tutor(
    year: str,
    student_username: str,
    current_user: str = Depends(get_current_user),
    abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
):
    if not (
        user_matches_student_username_param(student_username, current_user)
        or user_is_staff(year, current_user, abc_api)
        or user_is_tutor_or_uta(year, current_user, abc_api)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this resource.",
        )


def user_matches_student_username_param(
    student_username: str, current_user: str = Depends(get_current_user)
) -> bool:
    return student_username == current_user


def verify_user_is_tutor_or_uta(
    year: str,
    current_user: str = Depends(get_current_user),
    abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
):
    if not user_is_tutor_or_uta(year, current_user, abc_api):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this resource.",
        )


def verify_user_is_staff(
        year: str,
        current_user: str = Depends(get_current_user),
        abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
):
    if not user_is_staff(year, current_user, abc_api):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this resource.",
        )


def verify_user_is_student(
        year: str,
        current_user: str = Depends(get_current_user),
        abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
):
    if not user_is_student(year, current_user, abc_api):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to select modules.",
        )

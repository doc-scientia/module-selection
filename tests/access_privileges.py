from app.dependencies.access_privileges import verify_user_is_admin


def test_admin_passes_admin_check(admin_factory, session):
    a = admin_factory()
    assert verify_user_is_admin(a.username, session)


def test_non_admin_fails_admin_check(session):
    assert not verify_user_is_admin("not_admin", session)

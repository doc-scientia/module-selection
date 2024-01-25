from app.protocols import Authenticator

DUMMY_USER_BASE = {
    "adumble": {
        "givenName": "Albus",
        "sn": "Dumbledore",
        "distinguishedName": {"OU": ["doc"]},
        "extensionAttribute6": "Staff",
    },
    "hpotter": {
        "givenName": "Harry",
        "sn": "Potter",
        "distinguishedName": {"OU": ["doc"]},
        "extensionAttribute6": "Student",
    },
    "role_user1": {
        "name": "role_user1",
        "givenName": "Role",
        "sn": "User 1",
        "distinguishedName": {"OU": ["doc"]},
        "extensionAttribute6": "Staff",
    },
}


class DummyLdapAuthenticator(Authenticator):
    def authenticate(self, username: str, password: str) -> dict | None:
        return DUMMY_USER_BASE[username] if username in DUMMY_USER_BASE else None

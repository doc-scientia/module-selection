from unittest.mock import Mock

import ldap
import pytest
from _ldap import INVALID_CREDENTIALS
from ldap.ldapobject import SimpleLDAPObject

from app.ldap_authentication.authenticator import (
    USERNAME_FILTER_TEMPLATE,
    DocLdapAuthenticator,
    ldap_attributes_to_dictionary,
    serialise_ldap_attributes,
    validate_affiliation_to_doc,
)

VALID_DOC_ATTRIBUTES = {"distinguishedName": {"OU": {"doc"}}}
raw_attributes, serialised_attributes = {"key": [b"value"]}, {"key": "value"}
ldap_user = "user"


@pytest.mark.parametrize(
    "ldap_attributes, validation_outcome",
    [
        ({"distinguishedName": {"OU": {"eee"}}}, False),
        (
            {
                "distinguishedName": {"OU": {"bioeng", "eee"}},
                "memberOf": {"CN": {"eee-all-students"}},
            },
            False,
        ),
        ({"distinguishedName": {"OU": {"doc"}}}, True),
        (
            {
                "distinguishedName": {"OU": {"bioeng", "eee"}},
                "memberOf": {"CN": {"doc-all-students"}},
            },
            True,
        ),
        (
            {
                "distinguishedName": {"OU": {"bioeng", "eee"}},
                "memberOf": {"CN": {"doc-staff-group"}},
            },
            True,
        ),
        (
            {
                "distinguishedName": {"OU": {"bioeng", "eee"}},
                "memberOf": {"CN": {"doc-ext-group"}},
            },
            True,
        ),
    ],
)
def test_validation_of_affiliation_to_doc_via_ldap_attributes(
    ldap_attributes, validation_outcome
):
    assert validate_affiliation_to_doc(ldap_attributes) is validation_outcome


def test_raw_attributes_extraction():
    search_result = "search_results"
    connection_res = (..., [(..., raw_attributes)])

    attributes = ["attribute1", "attribute2"]
    mock_connection = Mock(spec=SimpleLDAPObject)
    mock_connection.search = Mock(return_value=search_result)
    mock_connection.result = Mock(return_value=connection_res)

    auth = DocLdapAuthenticator()
    res = auth._raw_attributes(ldap_user, attributes, mock_connection)
    mock_connection.search.assert_called_once_with(
        auth.base_dn,
        ldap.SCOPE_SUBTREE,
        USERNAME_FILTER_TEMPLATE % ldap_user,
        attributes,
    )
    mock_connection.result.assert_called_once_with(search_result)
    assert res == raw_attributes


def test_binding(monkeypatch):
    mock_connection = Mock(spec=SimpleLDAPObject)
    monkeypatch.setattr(ldap, "initialize", Mock(return_value=mock_connection))

    auth = DocLdapAuthenticator()
    auth._raw_attributes = Mock(return_value=raw_attributes)

    res = auth._ldap_authentication(ldap_user, "password", [...])
    assert res == serialised_attributes
    mock_connection.simple_bind_s.assert_called_once()
    mock_connection.unbind_s.assert_called_once()


def test_successful_authentication():
    authenticator = DocLdapAuthenticator()
    mock_ldap_authentication = Mock(return_value=VALID_DOC_ATTRIBUTES)
    setattr(authenticator, "_ldap_authentication", mock_ldap_authentication)
    assert authenticator.authenticate("username", "password") == VALID_DOC_ATTRIBUTES
    mock_ldap_authentication.assert_called_once_with(
        "username",
        "password",
        query_attrs=(
            "extensionAttribute6",
            "givenName",
            "sn",
            "distinguishedName",
            "memberOf",
            "memberships",
        ),
    )


def test_unsuccessful_authentication():
    authenticator = DocLdapAuthenticator()
    mock_ldap_authentication = Mock(side_effect=INVALID_CREDENTIALS)
    setattr(authenticator, "_ldap_authentication", mock_ldap_authentication)
    assert authenticator.authenticate("wrong-username", "wrong-password") is None


def test_serialising_ldap_attributes():
    serialised = serialise_ldap_attributes(
        {
            "distinguishedName": [b"CN=adumble,OU=eee,OU=doc"],
            "extensionAttribute6": [b"Employee"],
        }
    )
    assert serialised == {
        "distinguishedName": {"CN": {"adumble"}, "OU": {"eee", "doc"}},
        "extensionAttribute6": "Employee",
    }


@pytest.mark.parametrize(
    "raw_attributes, dict_attributes",
    [
        ([b"NonMatchingAttribute"], {}),
        ([b"A=a,B=b1,B=b2"], {"A": {"a"}, "B": {"b1", "b2"}}),
        ([b"NonMatchingAttribute", b"A=a,B=b1,B=b2"], {"A": {"a"}, "B": {"b1", "b2"}}),
    ],
)
def test_ldap_attributes_to_dictionary_conversion(raw_attributes, dict_attributes):
    assert ldap_attributes_to_dictionary(raw_attributes) == dict_attributes

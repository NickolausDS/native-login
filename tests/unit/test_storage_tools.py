import pytest

from fair_research_login.token_storage import (
    check_scopes, flat_pack, flat_unpack
)
from fair_research_login.exc import ScopesMismatch


def test_check_scopes_with_differing_scopes(mock_tokens):
    with pytest.raises(ScopesMismatch):
        check_scopes(mock_tokens, ['custom_scope'])


def test_flat_pack_unpack(login_token_group):
    exercised_tokens = flat_unpack(flat_pack(login_token_group))
    assert exercised_tokens == login_token_group


def test_flat_unpack_rs_with_underscores(login_token_group_underscores):
    exercised_tokens = flat_unpack(flat_pack(login_token_group_underscores))
    assert exercised_tokens == login_token_group_underscores


def test_flat_unpack_with_empty_value():
    assert flat_unpack([]) == []

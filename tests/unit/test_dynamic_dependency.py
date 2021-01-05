import pytest

from fair_research_login.token_storage import get_dynamic_dependencies


@pytest.mark.parametrize("test_input,expected", [
    # Test basic scope string
    (['foo bar baz'],
     {'foo': '', 'bar': '', 'baz': ''}),

    # Test basic scope string as list
    (['foo', 'bar', 'baz'],
     {'foo': '', 'bar': '', 'baz': ''}),

    # Test single simple dynamic dependency
    (['foo[bar]'],
     {'foo': 'bar'}),

    # Test single dynamic dependency with multiple scopes
    (['foo[bar] bar baz'],
     {'foo': 'bar', 'bar': '', 'baz': ''}),

    # Test multiple dynamic dependencies
    (['foo[bar baz billy]'],
     {'foo': 'bar baz billy'}),

    # Test multiple dynamic dependencies with multiple scopes
    (['foo[bar baz billy] car dar zar[bar dar]'],
     {'foo': 'bar baz billy', 'car': '', 'dar': '',
      'zar': 'bar dar'}),

    # Test multiple dynamic dependencies properly sorts output
    (['foo[billy zilly apple]'],
     {'foo': 'apple billy zilly'}),

    # ----- Real world tests -----
    ('urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships[openid]',  # noqa
     {'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships': 'openid'}),  # noqa

    ('urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships[profile]',  # noqa
     {'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships': 'profile'}),  # noqa

    ('urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships[email]',  # noqa
     {'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships': 'email'}),  # noqa

    ('urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships[openid profile email]',  # noqa
     {'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships': 'email openid profile'}),  # noqa

    # test dynamic dep
    ('https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom[openid]',  # noqa
     {'https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom': 'openid'}),  # noqa

    # Test dynamic dep and regular scope
    ('https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom[openid] openid',  # noqa
     {'https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom': 'openid',  # noqa
      'openid': ''}),

    # Test custom scope with globus dynamic dependency
    ('https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom'  # noqa
     '[urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships]',  # noqa
     {'https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom':  # noqa
      'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships'}),  # noqa

    # Test globus dynamic dependency with custom scope (bad example, but this
    # should be possible).
    ('urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships'  # noqa
     '[https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom]',  # noqa
     {'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships':  # noqa
      'https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom'}),  # noqa

    # Test multiple dynamic dependencies on custom scope
    ('https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom'  # noqa
     '[urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships '  # noqa
     'urn:globus:auth:scope:search.api.globus.org:search]',  # noqa
     {'https://auth.globus.org/scopes/c3b0e9db-c204-4ff6-8ddf-3fa96381654a/custom':  # noqa
      'urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships '  # noqa
      'urn:globus:auth:scope:search.api.globus.org:search'}),
])
def test_parse_scope_string(test_input, expected):
    assert get_dynamic_dependencies(test_input) == expected

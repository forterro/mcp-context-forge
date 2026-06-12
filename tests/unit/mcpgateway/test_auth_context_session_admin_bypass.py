# -*- coding: utf-8 -*-
"""Location: ./tests/unit/mcpgateway/test_auth_context_session_admin_bypass.py
Copyright 2026
SPDX-License-Identifier: Apache-2.0

Regression tests for session-token admin bypass in the Layer-1 resource access
context.

Session tokens (``token_use == "session"``) do not carry an ``is_admin`` JWT
claim. For these tokens the database is the authority, and admin bypass is
encoded by ``resolve_session_teams()`` as ``token_teams=None`` (returned ONLY
for DB-admin users; non-admins always receive a concrete team list, possibly
empty).

These tests pin the behavior that:

- a DB-admin session token (token_teams=None) is granted admin bypass, and
- a non-admin session token is NEVER widened to admin bypass (deny paths), and
- non-session tokens do not inherit the session-specific signal.
"""

# Standard
from types import SimpleNamespace

# First-Party
from mcpgateway import auth_context


def _make_request(payload, token_teams):
    """Build a minimal request carrying a verified JWT payload and token_teams."""
    state = SimpleNamespace(
        _jwt_verified_payload=("token", payload),
        token_teams=token_teams,
        _mcp_internal_auth_context=None,
    )
    return SimpleNamespace(state=state, url=SimpleNamespace(path="/admin/gateways/x"))


class TestSessionTokenAdminBypass:
    """get_rpc_filter_context / get_scoped_resource_access_context for session tokens."""

    def test_session_admin_bypass_granted(self):
        """DB-admin session token (token_teams=None, no is_admin claim) → admin bypass."""
        payload = {"sub": "admin@example.com", "email": "admin@example.com", "token_use": "session", "teams": None}
        request = _make_request(payload, token_teams=None)

        email, teams, is_admin = auth_context.get_rpc_filter_context(request, {"email": "admin@example.com"})
        assert email == "admin@example.com"
        assert teams is None
        assert is_admin is True

        scoped_email, scoped_teams = auth_context.get_scoped_resource_access_context(request, {"email": "admin@example.com"})
        assert scoped_email == "admin@example.com"
        assert scoped_teams is None  # admin bypass

    def test_session_explicit_admin_claim_still_bypasses(self):
        """A session token that DOES carry is_admin=true keeps admin bypass."""
        payload = {"sub": "admin@example.com", "email": "admin@example.com", "token_use": "session", "teams": None, "is_admin": True}
        request = _make_request(payload, token_teams=None)

        _, teams, is_admin = auth_context.get_rpc_filter_context(request, {"email": "admin@example.com"})
        assert teams is None
        assert is_admin is True


class TestSessionTokenDenyPaths:
    """Deny paths — non-admin session tokens must NOT receive admin bypass."""

    def test_non_admin_session_public_only(self):
        """Non-admin session token with empty team list → public-only, no bypass."""
        payload = {"sub": "user@example.com", "email": "user@example.com", "token_use": "session", "teams": []}
        request = _make_request(payload, token_teams=[])

        email, teams, is_admin = auth_context.get_rpc_filter_context(request, {"email": "user@example.com"})
        assert email == "user@example.com"
        assert teams == []
        assert is_admin is False

        scoped_email, scoped_teams = auth_context.get_scoped_resource_access_context(request, {"email": "user@example.com"})
        assert scoped_email == "user@example.com"
        assert scoped_teams == []

    def test_non_admin_session_team_scoped(self):
        """Non-admin session token with concrete teams → team-scoped, no bypass."""
        payload = {"sub": "user@example.com", "email": "user@example.com", "token_use": "session", "teams": ["team-a"]}
        request = _make_request(payload, token_teams=["team-a"])

        _, teams, is_admin = auth_context.get_rpc_filter_context(request, {"email": "user@example.com"})
        assert teams == ["team-a"]
        assert is_admin is False

        scoped_email, scoped_teams = auth_context.get_scoped_resource_access_context(request, {"email": "user@example.com"})
        assert scoped_teams == ["team-a"]


class TestNonSessionTokensUnaffected:
    """The session-specific signal must not leak into non-session tokens."""

    def test_api_token_none_teams_without_admin_claim_no_bypass(self):
        """A non-session token with token_teams=None but no is_admin claim → no bypass.

        For API/legacy tokens, token_teams=None should only arise alongside an
        is_admin claim. If the claim is absent, the session-specific inference
        must not fire, so the request stays non-admin (and is treated as
        public-only by the scoped context).
        """
        payload = {"sub": "user@example.com", "email": "user@example.com", "token_use": "api", "teams": None}
        request = _make_request(payload, token_teams=None)

        _, teams, is_admin = auth_context.get_rpc_filter_context(request, {"email": "user@example.com"})
        assert teams is None
        assert is_admin is False

        scoped_email, scoped_teams = auth_context.get_scoped_resource_access_context(request, {"email": "user@example.com"})
        assert scoped_teams == []  # not bypass — public-only

    def test_api_token_with_admin_claim_bypasses(self):
        """A non-session API token carrying is_admin=true keeps admin bypass."""
        payload = {"sub": "admin@example.com", "email": "admin@example.com", "token_use": "api", "teams": None, "is_admin": True}
        request = _make_request(payload, token_teams=None)

        _, teams, is_admin = auth_context.get_rpc_filter_context(request, {"email": "admin@example.com"})
        assert teams is None
        assert is_admin is True

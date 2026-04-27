# Feature: Service Account Token Issuance for Agent-to-MCP Integration

**Branch**: `upstream-pr/service-account-token-issuance`
**Base**: `upstream/main` (commit `bc88d5988`)
**Status**: In Development
**Author**: Platform Team
**Date**: April 27, 2026

---

## Overview

Enable non-interactive token issuance for service principals (agents, cron jobs, background services) via OAuth 2.0 Client Credentials grant (RFC 6749 Section 4.4).

This feature unblocks MyForterro AI agent and other headless services from authenticating to ContextForge MCP gateway without user browser interaction.

---

## Dependency Analysis

### Critical Dependencies ✅

**Branch Base**: `release/1.0.0-RC4-validation` (commit `f0d29d4cb`)

| Dependency | PR/Commit | Status | Why Required |
|------------|-----------|--------|-------------|
| MCP OAuth proxy infrastructure | `fix/virtual-server-dcr-bypass-upstream` | **MERGED** on branch | Provides OAuth endpoint structure + `mcp_oauth_router` for adding new token endpoints |
| `feat/token-endpoint-auth-method-upstream` | Commit `28b0945d7` | **MERGED** on branch | Provides `client_secret_basic` token endpoint auth (RFC 6749 Section 2.3), required for client credentials exchange |
| OAuth JWT infrastructure | Available on branch | **AVAILABLE** | JWT creation/validation utilities (`mcpgateway/utils/create_jwt_token.py`, `verify_credentials.py`) |
| Per-user credential lookup | Available on branch | **AVAILABLE** | `resolve_gateway_auth_headers()` for agent credential resolution |
| Service account DB model | Available on branch | **AVAILABLE** | Service account metadata and secrets storage (A2A agent model) |

**Rationale**: This branch is rebased onto `release/1.0.0-RC4-validation` (integration branch) which includes all 17 PRs with complete OAuth infrastructure. Attempting to base on `upstream/main` would require waiting for all upstream PRs to be accepted, blocking the feature.

### Soft Dependencies (Already Available)

- A2A agent infrastructure (service account model, admin UI)
- OAuth token storage (per-user tokens)
- RBAC middleware (permission checks)

---

## Implementation Plan

### 1. New Endpoint: `POST /oauth/token/services`

**Location**: `mcpgateway/routers/mcp_oauth.py`

**Request**:
```json
{
  "grant_type": "client_credentials",
  "client_id": "myforterro-ai-agent",
  "client_secret": "base64_encoded_secret_xyz",
  "scope": "mcp:invoke"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**JWT Claims**:
```json
{
  "sub": "myforterro-ai-agent",
  "aud": "mcpgateway-api",
  "iss": "contextforge",
  "type": "service_account",
  "exp": 1234567890
}
```

### 2. Service Account Registration

**Admin UI**: `charts/forterro-ai-context-hub/templates/.../admin.html`
- Register service principal (email, credentials, permissions)
- Display client_id and client_secret
- Rotate credentials UI

### 3. Credential Resolution

**Modification**: `mcpgateway/utils/gateway_access.py::resolve_gateway_auth_headers()`
- Extract `sub` from JWT (service account ID, not user email)
- Look up service account's stored credentials
- Apply per-service credentials to outbound requests

### 4. Testing

**File**: `tests/test_service_account_token_issuance.py`
- ✅ Token exchange (valid credentials → JWT)
- ✅ Token validation (JWT signature, expiry)
- ✅ MCP gateway call with service account JWT
- ✅ Per-service credential resolution
- ✅ Error handling (invalid secret, expired token, etc.)

---

## Files to Modify

| File | Type | Purpose |
|------|------|---------|
| `mcpgateway/routers/mcp_oauth.py` | Code | Add `/oauth/token/services` endpoint |
| `mcpgateway/schemas.py` | Code | Add `ServiceAccountTokenRequest`, `TokenResponse` schemas |
| `mcpgateway/services/oauth_manager.py` | Code | Add `validate_service_account_credentials()` |
| `mcpgateway/utils/gateway_access.py` | Code | Modify `resolve_gateway_auth_headers()` to support agent identity |
| `mcpgateway/db.py` | Code | Ensure `ServiceAccount` model has `client_secret` field (if not already present) |
| `tests/test_service_account_token_issuance.py` | Test | New comprehensive tests |
| `FEATURE_SERVICE_ACCOUNT_TOKEN_ISSUANCE.md` | Doc | This file |

---

## Go/No-Go Validation (Post-Implementation)

**Required Passing Tests**:

1. ✅ **Token Exchange**: Agent exchanges `client_id + client_secret` → receives valid JWT
2. ✅ **Token Validation**: JWT is accepted on MCP gateway, JWT claims are correct
3. ✅ **Compiler Invocation**: Compiler is invoked with correct service account identity
4. ✅ **Token Refresh**: Service account JWT expiry and refresh workflow
5. ✅ **Error Handling**: Network errors, OAuth failures, invalid secrets produce proper error codes and logs

**Integration Test**: MyForterro agent (using client credentials) successfully calls ContextForge MCP compiler.

---

## Release Notes Entry

```
### New Feature: Service Account Token Issuance (Client Credentials Grant)

ContextForge now supports non-interactive token issuance for service principals (agents, cron jobs, background services) via OAuth 2.0 Client Credentials grant (RFC 6749).

**Use Case**: Enable headless services (e.g., MyForterro AI agent) to authenticate to ContextForge MCP gateway without user browser interaction.

**How It Works**:
1. Register a service account in ContextForge admin (generate client_id + client_secret)
2. Service calls `POST /oauth/token/services` with client credentials
3. ContextForge issues a JWT with `type: service_account`
4. Service uses JWT as Bearer token to call MCP gateway
5. ContextForge resolves service account's stored credentials and applies them to outbound requests

**Endpoints**:
- `POST /oauth/token/services` — Exchange client credentials for JWT
- Existing `/credentials/{gateway_id}` — Store per-service credentials (via service account email)

**References**:
- RFC 6749 Section 4.4 (Client Credentials Grant)
- RFC 7591 (Dynamic Client Registration)
- [PRD] MyForterro AI → ContextForge MCP Integration
```

---

## Notes

- DCO sign-off required on all commits (`git commit -s`)
- This PR should be merged **after** `feat/token-endpoint-auth-method-upstream` is on `upstream/main`
- Alternatively, merge directly onto `release/1.0.0-RC4-validation` which already includes the dependency
- No breaking changes; fully backward compatible
- Existing user auth flows (Authorization Code, SSO) unchanged

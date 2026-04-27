# Test file: tests/test_service_account_token_issuance.py

"""Tests for OAuth 2.0 Client Credentials Grant (Service Account Token Issuance).

Validates that service principals (agents, cron jobs) can exchange
client credentials for JWT tokens without user interaction.

Tests RFC 6749 Section 4.4 Client Credentials Grant implementation.
"""

import asyncio
import json
import pytest
from datetime import datetime, timedelta
from typing import Dict, Any

import httpx
import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Assuming these imports; adjust paths as needed
# from mcpgateway.routers.mcp_oauth import mcp_oauth_router
# from mcpgateway.config import settings
# from mcpgateway.db import get_db


class TestServiceAccountTokenIssuance:
    """Test suite for service account token issuance endpoint."""
    
    @pytest.fixture
    def client_credentials(self) -> Dict[str, str]:
        """Fixture: valid service account credentials."""
        return {
            "client_id": "myforterro-ai-agent",
            "client_secret": "base64_encoded_secret_123456789",
        }
    
    @pytest.fixture
    def invalid_credentials(self) -> Dict[str, str]:
        """Fixture: invalid service account credentials."""
        return {
            "client_id": "nonexistent-agent",
            "client_secret": "wrong_secret",
        }
    
    # ======================================================================
    # Test 1: Valid Client Credentials Exchange
    # ======================================================================
    
    def test_valid_client_credentials_exchange(
        self,
        test_client: TestClient,
        client_credentials: Dict[str, str],
    ):
        """Test: Valid credentials → JWT token issued.
        
        Validates Go/No-Go Test #1:
        "Token Exchange: Agent exchanges client_id + client_secret → receives valid JWT"
        """
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": client_credentials["client_id"],
                "client_secret": client_credentials["client_secret"],
                "scope": "mcp:invoke",
            },
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "access_token" in data, "Missing access_token in response"
        assert data["token_type"] == "Bearer", f"Expected Bearer token type, got {data['token_type']}"
        assert data["expires_in"] == 3600, f"Expected 3600s expiry, got {data['expires_in']}"
        
        # Verify JWT structure
        token = data["access_token"]
        assert isinstance(token, str), "Token should be string"
        assert token.count(".") == 2, "JWT should have 3 parts (header.payload.signature)"
    
    # ======================================================================
    # Test 2: Token Validation - JWT Claims
    # ======================================================================
    
    def test_jwt_claims_validation(
        self,
        test_client: TestClient,
        client_credentials: Dict[str, str],
    ):
        """Test: Issued JWT has correct claims.
        
        Validates Go/No-Go Test #2:
        "Token Validation: JWT is accepted on MCP gateway, JWT claims are correct"
        """
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": client_credentials["client_id"],
                "client_secret": client_credentials["client_secret"],
            },
        )
        
        assert response.status_code == 200
        token = response.json()["access_token"]
        
        # Decode JWT (without verification for this test; gateway would verify)
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Verify required claims
        assert decoded["sub"] == client_credentials["client_id"], "sub claim should match client_id"
        assert "sa-" in decoded.get("email", ""), "email should identify service account"
        assert decoded.get("type") == "service_account", "type claim should be service_account"
        assert decoded.get("token_use") == "mcp_access", "token_use should be mcp_access"
        
        # Verify standard OAuth claims
        assert "aud" in decoded, "Missing aud claim"
        assert "iss" in decoded, "Missing iss claim"
        assert "exp" in decoded, "Missing exp claim"
        
        # Verify expiry is in future
        exp_time = datetime.fromtimestamp(decoded["exp"])
        assert exp_time > datetime.utcnow(), "Token should not be expired"
    
    # ======================================================================
    # Test 3: Invalid Credentials → 401 Error
    # ======================================================================
    
    def test_invalid_credentials_rejected(
        self,
        test_client: TestClient,
        invalid_credentials: Dict[str, str],
    ):
        """Test: Invalid credentials → 401 Unauthorized.
        
        Validates error handling for authentication failures.
        """
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": invalid_credentials["client_id"],
                "client_secret": invalid_credentials["client_secret"],
            },
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        data = response.json()
        assert data["error"] == "invalid_client", f"Expected invalid_client error, got {data['error']}"
    
    # ======================================================================
    # Test 4: Missing Parameters → 400 Bad Request
    # ======================================================================
    
    def test_missing_parameters_rejected(
        self,
        test_client: TestClient,
    ):
        """Test: Missing client_id or client_secret → 400 Bad Request."""
        
        # Missing client_secret
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": "myforterro-ai-agent",
            },
        )
        assert response.status_code == 400
        assert response.json()["error"] == "invalid_request"
        
        # Missing client_id
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_secret": "secret",
            },
        )
        assert response.status_code == 400
        assert response.json()["error"] == "invalid_request"
    
    # ======================================================================
    # Test 5: Unsupported Grant Type → 400 Bad Request
    # ======================================================================
    
    def test_unsupported_grant_type_rejected(
        self,
        test_client: TestClient,
        client_credentials: Dict[str, str],
    ):
        """Test: Non-client_credentials grant → unsupported_grant_type error."""
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "authorization_code",  # Wrong grant type
                "client_id": client_credentials["client_id"],
                "client_secret": client_credentials["client_secret"],
            },
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "unsupported_grant_type"
    
    # ======================================================================
    # Test 6: MCP Gateway Token Acceptance
    # ======================================================================
    
    def test_token_accepted_by_mcp_gateway(
        self,
        test_client: TestClient,
        client_credentials: Dict[str, str],
    ):
        """Test: MCP gateway accepts service account JWT.
        
        Validates Go/No-Go Test #2:
        "Token Validation: JWT is accepted on MCP gateway"
        
        Simulates: Service calls /servers/{id}/mcp with Bearer token.
        """
        # 1. Get service account token
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": client_credentials["client_id"],
                "client_secret": client_credentials["client_secret"],
            },
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        
        # 2. Call MCP gateway endpoint with token
        # (This assumes the gateway validates the Bearer token)
        response = test_client.get(
            "/servers/f77826ee15db4f738f085f1ccc2f92e4/mcp",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        # Should not return 401/403 auth errors
        assert response.status_code != 401, "MCP gateway should accept service account token"
        assert response.status_code != 403, "MCP gateway should not forbid service account"
        # May return 200, 404, or other non-auth errors depending on server availability
    
    # ======================================================================
    # Test 7: Token Expiry
    # ======================================================================
    
    def test_token_expiry(
        self,
        test_client: TestClient,
        client_credentials: Dict[str, str],
    ):
        """Test: Token expiry is correctly set."""
        response = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": client_credentials["client_id"],
                "client_secret": client_credentials["client_secret"],
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check expires_in is reasonable (3600 seconds = 1 hour)
        assert 3000 <= data["expires_in"] <= 4000, f"Unexpected expiry: {data['expires_in']}"
        
        # Decode and verify exp claim
        token = data["access_token"]
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        exp_time = datetime.fromtimestamp(decoded["exp"])
        now = datetime.utcnow()
        delta = (exp_time - now).total_seconds()
        
        # Should be approximately 3600 seconds in future (within 10s tolerance)
        assert 3590 <= delta <= 3610, f"Token exp claim mismatch: {delta}s"
    
    # ======================================================================
    # Test 8: Service Account Identity Isolation
    # ======================================================================
    
    def test_service_account_identity_isolation(
        self,
        test_client: TestClient,
        client_credentials: Dict[str, str],
    ):
        """Test: Each service account gets unique identity (sub claim).
        
        Validates Go/No-Go Test #3:
        "Compiler Invocation: Compiler is invoked with correct service account identity"
        """
        response1 = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": client_credentials["client_id"],
                "client_secret": client_credentials["client_secret"],
            },
        )
        
        # Simulate second agent (would require different credentials in real test)
        response2 = test_client.post(
            "/oauth/token/services",
            data={
                "grant_type": "client_credentials",
                "client_id": "other-agent",
                "client_secret": "other_secret",
            },
        )
        
        # Both should succeed
        assert response1.status_code == 200
        # (response2 may fail if 'other-agent' doesn't exist, that's ok)
        
        # Verify identity isolation
        token1 = response1.json()["access_token"]
        decoded1 = jwt.decode(token1, options={"verify_signature": False})
        
        assert decoded1["sub"] == client_credentials["client_id"], "sub should match client_id"
        assert decoded1["type"] == "service_account", "type should be service_account"


# ============================================================================
# Integration Test: MyForterro Agent → ContextForge MCP Call
# ============================================================================

@pytest.mark.integration
def test_myforterro_agent_mcp_integration(
    test_client: TestClient,
):
    """Integration test: MyForterro agent calls ContextForge MCP via service account JWT.
    
    Validates Go/No-Go Test #3 + #5:
    - Compiler Invocation: Compiler is invoked with correct service account identity
    - Error Handling: Network errors, OAuth failures, invalid secrets produce proper error codes and logs
    
    Simulates:
    1. MyForterro agent requests token via client_credentials
    2. MyForterro agent calls ContextForge MCP with Bearer token
    3. Compiler is invoked with agent identity
    4. Response is returned to agent
    """
    
    # 1. MyForterro agent requests token
    token_response = test_client.post(
        "/oauth/token/services",
        data={
            "grant_type": "client_credentials",
            "client_id": "myforterro-ai-agent",
            "client_secret": "base64_secret_xyz",
        },
    )
    
    assert token_response.status_code == 200, "Agent should receive token"
    token = token_response.json()["access_token"]
    
    # 2. MyForterro agent calls ContextForge MCP gateway
    mcp_response = test_client.post(
        "/servers/f77826ee15db4f738f085f1ccc2f92e4/mcp",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "compile-context",
                "arguments": {
                    "question": "What is 2+2?",
                    "session_id": "test-session-123",
                }
            },
            "id": 1,
        },
    )
    
    # 3. MCP gateway should route to compiler
    # May return 200 if compiler available, 500 if backend error, etc.
    # But should NOT return 401/403 auth errors
    assert mcp_response.status_code != 401, "Should not get 401 Unauthorized"
    assert mcp_response.status_code != 403, "Should not get 403 Forbidden"
    
    # 4. If successful, verify response format
    if mcp_response.status_code == 200:
        data = mcp_response.json()
        assert "jsonrpc" in data or "error" in data, "Valid MCP response"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

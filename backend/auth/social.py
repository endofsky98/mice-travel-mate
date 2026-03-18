import httpx
from typing import Optional, Tuple
from config import settings
import logging

logger = logging.getLogger(__name__)


async def verify_google_token(id_token: str) -> Optional[dict]:
    """
    Verify a Google OAuth ID token.
    Returns user info dict with email, name, and sub (Google user ID) on success.
    Returns None on failure.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            )
            if response.status_code != 200:
                logger.warning("Google token verification failed: %s", response.text)
                return None

            data = response.json()

            # Verify the token was issued for our app
            if settings.GOOGLE_CLIENT_ID and data.get("aud") != settings.GOOGLE_CLIENT_ID:
                logger.warning("Google token audience mismatch")
                return None

            return {
                "email": data.get("email"),
                "name": data.get("name", data.get("email", "").split("@")[0]),
                "sub": data.get("sub"),
                "picture": data.get("picture"),
            }
    except Exception as e:
        logger.error("Google token verification error: %s", str(e))
        return None


async def verify_apple_token(authorization_code: str, id_token: str) -> Optional[dict]:
    """
    Verify an Apple Sign-In token.
    Returns user info dict with email, name, and sub (Apple user ID) on success.
    Returns None on failure.
    """
    try:
        from jose import jwt as jose_jwt

        # Fetch Apple's public keys
        async with httpx.AsyncClient() as client:
            response = await client.get("https://appleid.apple.com/auth/keys")
            if response.status_code != 200:
                logger.warning("Failed to fetch Apple public keys")
                return None

            apple_keys = response.json()

        # Decode the ID token header to get the key ID
        header = jose_jwt.get_unverified_header(id_token)
        kid = header.get("kid")

        # Find the matching key
        matching_key = None
        for key in apple_keys.get("keys", []):
            if key.get("kid") == kid:
                matching_key = key
                break

        if not matching_key:
            logger.warning("No matching Apple key found for kid: %s", kid)
            return None

        # Verify and decode the token
        from jose import jwk
        public_key = jwk.construct(matching_key)

        payload = jose_jwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"],
            audience=settings.APPLE_CLIENT_ID if settings.APPLE_CLIENT_ID else None,
            issuer="https://appleid.apple.com",
            options={"verify_aud": bool(settings.APPLE_CLIENT_ID)},
        )

        return {
            "email": payload.get("email"),
            "name": payload.get("name", payload.get("email", "").split("@")[0]),
            "sub": payload.get("sub"),
        }
    except Exception as e:
        logger.error("Apple token verification error: %s", str(e))
        return None

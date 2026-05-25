"""
Firebase ID Token Verifier without Admin SDK credentials.
Uses Google's public keys to verify tokens.
"""
import jwt
import requests
from typing import Dict, Optional
from datetime import datetime
import time


class FirebaseTokenVerifier:
    """Verify Firebase ID tokens using Google's public keys."""
    
    def __init__(self, project_id: str):
        """
        Initialize the verifier.
        
        Args:
            project_id: Firebase project ID
        """
        self.project_id = project_id
        self.public_keys_url = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
        self.issuer = f"https://securetoken.google.com/{project_id}"
        self.audience = project_id
        self._public_keys = None
        self._keys_expiry = 0
    
    def _get_public_keys(self) -> Dict[str, str]:
        """
        Fetch Google's public keys for Firebase token verification.
        
        Returns:
            Dictionary of public keys
        """
        # Check if cached keys are still valid
        if self._public_keys and time.time() < self._keys_expiry:
            return self._public_keys
        
        # Fetch new keys
        response = requests.get(self.public_keys_url)
        response.raise_for_status()
        
        # Cache keys
        self._public_keys = response.json()
        
        # Set expiry from Cache-Control header (usually 1 hour)
        cache_control = response.headers.get('Cache-Control', '')
        max_age = 3600  # Default 1 hour
        if 'max-age=' in cache_control:
            try:
                max_age = int(cache_control.split('max-age=')[1].split(',')[0])
            except:
                pass
        
        self._keys_expiry = time.time() + max_age
        
        return self._public_keys
    
    def verify_id_token(self, id_token: str) -> Dict:
        """
        Verify a Firebase ID token.
        
        Args:
            id_token: The Firebase ID token to verify
        
        Returns:
            Decoded token payload
        
        Raises:
            ValueError: If token is invalid
        """
        try:
            # Get public keys
            public_keys = self._get_public_keys()
            
            # Decode header to get key ID
            header = jwt.get_unverified_header(id_token)
            kid = header.get('kid')
            
            if not kid:
                raise ValueError("Token header missing 'kid' field")
            
            if kid not in public_keys:
                raise ValueError(f"Public key not found for kid: {kid}")
            
            # Get the public key certificate
            public_key_cert = public_keys[kid]
            
            # Load the certificate and extract the public key
            from cryptography import x509
            from cryptography.hazmat.backends import default_backend
            
            # Parse the X.509 certificate
            cert = x509.load_pem_x509_certificate(
                public_key_cert.encode('utf-8'),
                default_backend()
            )
            
            # Extract the public key from the certificate
            public_key = cert.public_key()
            
            # Verify and decode token
            decoded_token = jwt.decode(
                id_token,
                public_key,
                algorithms=['RS256'],
                audience=self.audience,
                issuer=self.issuer,
                options={
                    'verify_exp': True,
                    'verify_iat': True,
                    'verify_aud': True,
                    'verify_iss': True,
                }
            )
            
            # Additional validation
            if decoded_token.get('auth_time') is None:
                raise ValueError("Token missing 'auth_time' claim")
            
            # Check if token is issued in the future
            iat = decoded_token.get('iat', 0)
            if iat > time.time() + 300:  # Allow 5 minutes clock skew
                raise ValueError("Token issued in the future")
            
            return decoded_token
        
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch public keys: {str(e)}")
        except Exception as e:
            raise ValueError(f"Token verification failed: {str(e)}")


# Global instance
_verifier: Optional[FirebaseTokenVerifier] = None


def get_token_verifier(project_id: str = "oil-gas-f78c8") -> FirebaseTokenVerifier:
    """
    Get or create the token verifier instance.
    
    Args:
        project_id: Firebase project ID
    
    Returns:
        FirebaseTokenVerifier instance
    """
    global _verifier
    if _verifier is None:
        _verifier = FirebaseTokenVerifier(project_id)
    return _verifier

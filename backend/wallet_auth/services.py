# wallet_auth/services.py

import time
import secrets
import base58
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

class SolanaAuthService:
    def __init__(self, statement="Sign in to my Django app", domain="example.com"):
        self.statement = statement
        self.domain = domain
    
    def create_message(self, wallet_address, nonce=None, expiration_time=None):
        """Create a message for the user to sign with their Solana wallet"""
        if nonce is None:
            # Generate a random nonce
            nonce = secrets.token_hex(16)
        
        # Current time in ISO format
        issued_at = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        
        if expiration_time is None:
            # Default expiration of 1 hour
            expiration = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
                                      time.gmtime(time.time() + 3600))
        else:
            expiration = expiration_time
        
        # Create a structured message
        message = f"""
{self.domain} wants you to sign in with your Solana account:
{wallet_address}

{self.statement}

URI: https://{self.domain}
Version: 1
Nonce: {nonce}
Issued At: {issued_at}
Expiration Time: {expiration}
        """.strip()
        
        return {
            "message": message,
            "nonce": nonce,
            "issued_at": issued_at,
            "expiration": expiration
        }
    
    def verify_signature(self, message, signature, wallet_public_key):
        """Verify that the signature is valid and from the expected Solana address"""
        try:
            # Convert base58 public key to bytes
            public_key_bytes = base58.b58decode(wallet_public_key)
            
            # Create a VerifyKey instance from the public key
            verify_key = VerifyKey(public_key_bytes)
            
            # Convert base58 signature to bytes
            signature_bytes = base58.b58decode(signature)
            
            # Verify the signature
            verify_key.verify(message.encode('utf-8'), signature_bytes)
            return True
        except BadSignatureError:
            return False
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False
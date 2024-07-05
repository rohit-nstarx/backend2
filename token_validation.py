import requests
import jwt
from jwt import PyJWKClient

def validate_okta_jwt(token, okta_domain, audience):
    """
    Validates a JWT issued by Okta.

    Args:
    - token (str): The JWT to validate.
    - okta_domain (str): Your Okta domain (e.g., 'https://your-okta-domain.okta.com').
    - audience (str): The expected audience of the token.

    Returns:
    - dict: The decoded token if valid.
    - None: If the token is invalid or expired.
    """
    jwks_url = f'{okta_domain}/oauth2/ausi5gp94k3hmzYzo5d7/v1/keys'

    try:
        # Fetch the JWKS
        jwk_client = PyJWKClient(jwks_url)
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        print(signing_key.__dict__)
        print('key : ', signing_key.key)

        # Verify the JWT
        decoded_token = jwt.decode(token, signing_key.key, algorithms=['RS256'], audience=audience)
        print('decoded token : ', decoded_token)
        return decoded_token
    except requests.RequestException as e:
        print(f"Failed to fetch JWKS: {e}")
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")

    return None

# # Example usage
# if __name__ == "__main__":
#     # Replace with your Okta domain and token
#     okta_domain = 'https://your-okta-domain.okta.com'
#     audience = 'api://default'
#     token = 'eyJraWQiOiJhb...'

#     validated_token = validate_okta_jwt(token, okta_domain, audience)
#     if validated_token:
#         print("Token is valid")
#         print(validated_token)
#     else:
#         print("Token is invalid")

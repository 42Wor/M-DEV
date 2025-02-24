import secrets
import base64

# Generate a random secret key (32 bytes is a good length)
secret_key_bytes = secrets.token_bytes(32)

# Encode it to a URL-safe base64 string (common practice for secret keys)
secret_key_string = base64.urlsafe_b64encode(secret_key_bytes).decode('utf-8')

print(secret_key_string) # Copy this output and paste it into your config.json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode


def ensure_bytes(key):
    if isinstance(key, str):
        return key.encode('utf-8')
    elif not isinstance(key, bytes):
        raise TypeError("Key must be a string or bytes-like object")
    return key


def encrypt(message, key):
    key = ensure_bytes(key)[:32]  # AES-256 requires a 32-byte key
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(b'\0' * 16), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return b64encode(ciphertext).decode()


def decrypt(ciphertext, key):
    key = ensure_bytes(key)[:32]  # AES-256 requires a 32-byte key
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(b'\0' * 16), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(b64decode(ciphertext)) + decryptor.finalize()
    return decrypted_message.decode()

# message_to_encrypt = "Hello, world!"
# encryption_key = "2b7e151628aed2a6abf7158809cf4f3c"

# encrypted_message = encrypt(message_to_encrypt, encryption_key)
# print(f"Encrypted message: {encrypted_message}")

# decrypted = decrypt(encrypted_message, encryption_key)
# print(decrypted)

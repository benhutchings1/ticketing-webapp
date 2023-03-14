from datetime import datetime as dt
import random
import string
def generate_token():
    return dt.now().strftime("%S%M%H%m%d%Y") +\
        "".join(random.choice(string.ascii_letters) for i in range(114))

# Generates a random 32-byte key
def gen_key():
    key = get_random_bytes(32)

    return key


# Encrypts plain_text using AES-256-CBC
def encrypt(plain_text, key):
    # Input validation on key
    if not isinstance(key, bytes) or not len(key) == 32:
        return TypeError

    # Input validation on plain_text
    if not isinstance(plain_text, int) or abs(plain_text) != plain_text or not len(str(plain_text)) <= 8:
        return TypeError

    # Pad plain text by adding leading zeros
    plain_text = str(plain_text)
    plain_text = (8 - len(plain_text)) * '0' + plain_text

    # Encode string as bytes
    plain_text = bytes(plain_text, encoding='utf8')

    # Encrypt plain_text
    cypher = AES.new(key, AES.MODE_CBC)
    cypher_text = cypher.encrypt(pad(plain_text, AES.block_size))

    # Decode from bytes to string
    cypher_text = b64encode(cypher_text).decode()
    iv = b64encode(cypher.iv).decode()

    return cypher_text, iv


# Decrypts cypher text
def decrypt(cypher_text, iv, key):
    # Input validation on cypher text
    if not isinstance(cypher_text, str) or not len(cypher_text) == 24:
        return TypeError

    # Input validation on iv
    if not isinstance(iv, str) or not len(iv) == 24:
        return TypeError

    # Input validation on key
    if not isinstance(key, bytes) or not len(key) == 32:
        return TypeError

    # Decode from string to bytes
    cypher_text = b64decode(cypher_text)
    iv = b64decode(iv)

    # Decrypt cypher_text
    cypher = AES.new(key, AES.MODE_CBC, iv=iv)
    plain_text = unpad(cypher.decrypt(cypher_text), AES.block_size)

    return plain_text
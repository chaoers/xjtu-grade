import base64
import time

from Crypto.Cipher import AES
from config import config


def encrypt_passward(password: str) -> str:
    def pad(text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        padding = chr(amount_to_pad)
        return text + padding * amount_to_pad

    cipher = AES.new(
        config.public_key.encode('utf-8'),
        AES.MODE_ECB
    )

    encrypted_data = cipher.encrypt(pad(password).encode('utf-8'))
    return str(base64.b64encode(encrypted_data), encoding='utf-8')


def get_timestamp() -> int:
    return int(round(time.time() * 1000))

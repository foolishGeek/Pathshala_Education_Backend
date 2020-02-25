# Todo: MARK: Used to encrypt the hash/pseudo code.

import base64
import random
import string
from Crypto.Cipher import AES
from django.conf import settings


# Todo: MARK: Encrypt the string/Code.

def encrypt_val(clear_text):
    master_key = settings.SECRET_KEY
    enc_secret = AES.new(master_key[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "2")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
    print("Hashed Key is ", cipher_text)
    return cipher_text


# Todo: MARK: Decrypt the string/Code.

def decrypt_val(cipher_text):
    master_key = settings.SECRET_KEY
    dec_secret = AES.new(master_key[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("2")
    print("Decoded code", clear_val)
    return clear_val


# TODO: MARK: This func take 2 Args: (Optional parameters)
#       - Size of the Hash Code
#       - Character Set


def hash_code_generator(size=9, chars=string.ascii_uppercase + string.digits):
    coupon_code_generated = ''.join(random.SystemRandom().choice(chars) for _ in range(size))
    return coupon_code_generated



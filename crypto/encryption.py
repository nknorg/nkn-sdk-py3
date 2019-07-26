import nacl.utils

from crypto import Hash
from Crypto.Cipher import AES


class Encryption(object):
    @staticmethod
    def gen_aes_iv():
        return nacl.utils.random(16)

    @staticmethod
    def gen_aes_password():
        return nacl.utils.random(32)

    @staticmethod
    def encrypt(plaintext, password, iv, is_simple_password=False):
        password = Hash.doubleSha256(password) if is_simple_password else password
        cryptor = AES.new(password, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(plaintext)
        return ciphertext

    @staticmethod
    def decrypt(ciphertext, password, iv, is_simple_password=False):
        password = Hash.doubleSha256(password) if is_simple_password else password
        cryptor = AES.new(password, AES.MODE_CBC, iv)
        plaintext = cryptor.decrypt(ciphertext)
        return plaintext

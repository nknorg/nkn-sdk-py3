import binascii
import hashlib


class Hash(object):
    @staticmethod
    def sha256(str):
        return hashlib.new('sha256', str.encode()).hexdigest()

    @staticmethod
    def double_sha256(str):
        a = hashlib.new('sha256', str.encode()).digest()
        b = hashlib.new('sha256', a).hexdigest()
        return b

    @staticmethod
    def sha256_hex(hex_str):
        return hashlib.new('sha256', binascii.unhexlify(hex_str)).hexdigest()

    @staticmethod
    def double_sha256_hex(hex_str):
        a = hashlib.new('sha256', binascii.unhexlify(hex_str)).digest()
        b = hashlib.new('sha256', a).hexdigest()
        return b

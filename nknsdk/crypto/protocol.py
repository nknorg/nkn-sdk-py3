import binascii
import hashlib
import base58

from . import Hash


class Protocol(object):
    ADDRESS_GEN_PREFIX = '02b825'
    ADDRESS_GEN_PREFIX_LEN = int(len(ADDRESS_GEN_PREFIX) / 2)
    UINT160_LEN = 20
    CHECKSUM_LEN = 4
    ADDRESS_LEN = ADDRESS_GEN_PREFIX_LEN + UINT160_LEN + CHECKSUM_LEN

    @staticmethod
    def public_key_to_signature_redeem(public_key):
        return '20' + public_key + 'ac'

    @staticmethod
    def hex_string_to_program_hash(hex_str):
        return hashlib.new('ripemd160', hashlib.new('sha256', binascii.unhexlify(hex_str)).digest()).hexdigest()

    @staticmethod
    def gen_address_verify_bytes_from_program_hash(program_hash):
        progm_hash = Protocol.ADDRESS_GEN_PREFIX + program_hash
        verify_bytes = binascii.unhexlify(Hash.double_sha256_hex(progm_hash))
        return verify_bytes[:Protocol.CHECKSUM_LEN]

    @staticmethod
    def program_hash_string_to_address(program_hash):
        address_verify_bytes = Protocol.gen_address_verify_bytes_from_program_hash(program_hash)
        address_base_data = binascii.unhexlify(Protocol.ADDRESS_GEN_PREFIX + program_hash)
        address = base58.b58encode(address_base_data + address_verify_bytes)
        if isinstance(address, (bytes, bytearray)):
            return address.decode()
        return address

    @staticmethod
    def address_string_to_program_hash(address):
        address_bytes = base58.b58decode(address)
        program_hash_bytes = address_bytes[Protocol.ADDRESS_GEN_PREFIX_LEN:len(address_bytes) - Protocol.CHECKSUM_LEN]
        return binascii.hexlify(program_hash_bytes).decode()

    @staticmethod
    def get_address_string_verify_code(address):
        address_bytes = base58.b58decode(address)

        verify_bytes = address_bytes[-Protocol.CHECKSUM_LEN:]
        return binascii.hexlify(verify_bytes).decode()

    @staticmethod
    def gen_address_verify_code_from_program_hash(program_hash):
        verify_bytes = Protocol.gen_address_verify_bytes_from_program_hash(program_hash)
        return binascii.hexlify(verify_bytes).decode()

    @staticmethod
    def verify_address(address):
        address_bytes = base58.b58decode(address)
        if len(address_bytes) != Protocol.ADDRESS_LEN:
            return False
        address_prefix_bytes = address_bytes[:Protocol.ADDRESS_GEN_PREFIX_LEN]
        address_prefix = binascii.hexlify(address_prefix_bytes)
        if address_prefix.decode() != Protocol.ADDRESS_GEN_PREFIX:
            return False
        program_hash = Protocol.address_string_to_program_hash(address)
        address_verify_code = Protocol.get_address_string_verify_code(address)
        program_hash_verify_code = Protocol.gen_address_verify_code_from_program_hash(program_hash)
        return address_verify_code == program_hash_verify_code

    @staticmethod
    def signature_to_parameter(signature_hex):
        return format(int(len(signature_hex)/2), 'x') + signature_hex

import struct


class Serialize(object):
    maxUintBits = 48
    maxUint = 2 ** maxUintBits

    @staticmethod
    def encode_uint(value):
        if value < 0xfd:
            return Serialize.encode_uint8(value)
        elif value <= 0xffff:
            return 'fd' + Serialize.encode_uint16(value)
        elif value <= 0xffffffff:
            return 'fe' + Serialize.encode_uint32(value)
        else:
            return 'ff' + Serialize.encode_uint64(value)

    @staticmethod
    def encode_uint8(value):
        return struct.pack('B', value).hex()

    @staticmethod
    def encode_uint16(value):
        return struct.pack('H', value).hex()

    @staticmethod
    def encode_uint32(value):
        return struct.pack('I', value).hex()

    @staticmethod
    def encode_uint64(value):
        return struct.pack('Q', value).hex()

    @staticmethod
    def encode_bytes(value):
        buf = value
        return Serialize.encode_uint(len(value)) + buf.hex()

    @staticmethod
    def encode_string(value):
        buf = value.encode('utf-8')
        return Serialize.encode_uint(len(value)) + buf.hex()

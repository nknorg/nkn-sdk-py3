import binascii
from config import Config
from crypto import Hash, Protocol
from transaction import Payload
from serialize import Serialize
from pb.transaction_pb2 import UnsignedTx, Transaction as PbTransaction, Program, Payload as PbPayload


class Transaction(object):
    @staticmethod
    def serialize_unsigned_tx(unsigned_tx):
        hex_str = ''
        hex_str += Payload.serialize_payload(unsigned_tx.payload)
        hex_str += Serialize.encode_uint64(unsigned_tx.nonce)
        hex_str += Serialize.encode_uint64(unsigned_tx.fee)
        hex_str += Serialize.encode_bytes(unsigned_tx.attributes)
        return hex_str

    @staticmethod
    def sign_tx(account, txn):
        unsigned_tx = txn.unsigned_tx
        hex_str = Transaction.serialize_unsigned_tx(unsigned_tx)
        digest = Hash.sha256_hex(hex_str)
        signature = account.key.sign(binascii.unhexlify(digest))

        prgm = Program()
        prgm.code = binascii.unhexlify(account.signature_redeem)
        prgm.parameter = binascii.unhexlify(Protocol.signature_to_parameter(signature.hex()))

        prgm_item = txn.programs.add()
        prgm_item.CopyFrom(prgm)

    @staticmethod
    def new_transaction(account, pld, nonce, fee=0, attrs=''):
        fee = int(fee * Config['NKN_ACC_MUL'])
        unsigned_tx = UnsignedTx()
        unsigned_tx.payload.CopyFrom(pld)
        unsigned_tx.nonce = nonce
        unsigned_tx.fee = fee
        unsigned_tx.attributes = attrs.encode()

        txn = PbTransaction()
        txn.unsigned_tx.CopyFrom(unsigned_tx)

        Transaction.sign_tx(account, txn)

        return txn

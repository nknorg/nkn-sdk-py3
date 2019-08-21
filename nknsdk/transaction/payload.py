import binascii

from nknsdk.config import Config
from nknsdk.serialize import Serialize
from nknsdk.pb.transaction_pb2 import TransferAsset, Payload as PbPayload, PayloadType, RegisterName, DeleteName, Subscribe, NanoPay


class Payload(object):
    @staticmethod
    def new_transfer(sender, recipient, amount):
        amount = int(amount * Config['NKN_ACC_MUL'])

        transfer = TransferAsset()
        transfer.sender = binascii.unhexlify(sender)
        transfer.recipient = binascii.unhexlify(recipient)
        transfer.amount = amount

        pld = PbPayload()
        pld.type = PayloadType.TRANSFER_ASSET_TYPE
        pld.data = transfer.SerializeToString()
        return pld

    @staticmethod
    def new_register_name(public_key, name):
        register_name = RegisterName()
        register_name.registrant = binascii.unhexlify(public_key)
        register_name.name = name

        pld = PbPayload()
        pld.type = PayloadType.REGISTER_NAME_TYPE
        pld.data = register_name.SerializeToString()
        return pld

    @staticmethod
    def new_delete_name(public_key, name):
        delete_name = DeleteName()
        delete_name.registrant = binascii.unhexlify(public_key)
        delete_name.name = name

        pld = PbPayload()
        pld.type = PayloadType.DELETE_NAME_TYPE
        pld.data = delete_name.SerializeToString()
        return pld

    @staticmethod
    def new_subscribe(subscriber, identifier, topic, bucket, duration, meta):
        subscribe = Subscribe()
        subscribe.subscriber = binascii.unhexlify(subscriber)
        subscribe.identifier = identifier
        subscribe.topic = topic
        subscribe.bucket = bucket
        subscribe.duration = duration
        subscribe.meta = meta

        pld = PbPayload()
        pld.type = PayloadType.SUBSCRIBE_TYPE
        pld.data = subscribe.SerializeToString()
        return pld

    @staticmethod
    def new_nano_pay(sender, recipient, id, amount, txn_expiration, nano_pay_expiration):
        nano_pay = NanoPay()
        nano_pay.sender = binascii.unhexlify(sender)
        nano_pay.recipient = binascii.unhexlify(recipient)
        nano_pay.id = id
        nano_pay.amount = amount
        nano_pay.txn_expiration = txn_expiration
        nano_pay.nano_pay_expiration = nano_pay_expiration

        pld = PbPayload()
        pld.type = PayloadType.NANO_PAY_TYPE
        pld.data = nano_pay.SerializeToString()
        return pld

    @staticmethod
    def serialize_payload(payload):
        hex_str = ''
        hex_str += Serialize.encode_uint32(payload.type)
        hex_str += Serialize.encode_bytes(payload.data)
        return hex_str

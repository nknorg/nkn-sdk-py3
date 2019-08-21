import binascii
import json

from nknsdk.error import WalletError
from nknsdk.network import Api
from nknsdk.crypto import Encryption, Account, Protocol, Tools
from nknsdk.crypto import Hash
from nknsdk.transaction import Payload, Transaction


def to_password_hash(password):
    return Hash.double_sha256(password)


class Wallet(object):
    WALLET_VERSION = 1
    MIN_COMPATIBLE_WALLET_VERSION = 1
    MAX_COMPATIBLE_WALLET_VERSION = 1

    _api = Api()

    def __init__(self, account):
        self._account = account

    @property
    def public_key(self):
        """
        get the public key of this wallet
        :return {string}: the public key of this wallet
        """
        return self._account.public_key

    @property
    def private_key(self):
        """
        !!! anyone with the private key has the power to restore a full-featured wallet !!!!
        get the private key of this wallet
        :return {string}: the private key of this wallet
        """
        return self._account.private_key

    @property
    def seed(self):
        """
        !!! anyone with the seed has the power to restore a full-featured wallet !!!!
        get the seed of this wallet
        :return {string}: the seed of this wallet
        """
        return self._account.seed

    @property
    def address(self):
        return self._address

    @property
    def contract_data(self):
        return self._contract_data

    @property
    def master_key(self):
        return self._master_key

    @property
    def seed_encrypted(self):
        return self._seed_encrypted

    @property
    def version(self):
        return self._version

    @property
    def program_hash(self):
        return self._program_hash

    @property
    def configure(self):
        return self._api.configure

    @configure.setter
    def configure(self, new_config):
        self._api.configure.update(new_config)

    def get_balance(self):
        """
        query balance
        :return:{float} amount
        """
        return float(self._api.get_balance_by_addr(self.address)['amount'])

    def transfer_to(self, to_address, amount, **options):
        """
        transfer nkn to some valid address
        :param to_address:{string} valid nkn address
        :param amount:{float} value for transfer
        :return {string}: hash
        """
        if not Protocol.verify_address(to_address):
            raise WalletError.INVALID_ADDRESS()
        balance = self.get_balance()
        if balance < amount:
            raise WalletError.NOT_ENOUGH_NKN_COIN()
        nonce = self.get_nonce()
        pld = Payload.new_transfer(self.program_hash, Protocol.address_string_to_program_hash(to_address), amount)
        txn = Transaction.new_transaction(self._account, pld, nonce, options.get('fee', 0), options.get('attrs', ''))

        return self._api.send_raw_transaction(txn.SerializeToString().hex())

    def register_name(self, name, **options):
        """
        register name on nkn for current wallet
        :param name {string}: name to register
        :return:
        """
        nonce = self.get_nonce()
        pld = Payload.new_register_name(self.public_key, name)
        txn = Transaction.new_transaction(self._account, pld, nonce, options.get('fee', 0),
                                          options.get('attrs', ''))

        return self._api.send_raw_transaction(txn.SerializeToString().hex())

    def subscribe(self, topic, bucket, duration, identifier='', meta='', **options):
        """
        subscribe to topic on nkn for current wallet
        :param topic {string}: topic to subscribe to
        :param bucket {int}: bucket of topic to subscribe to
        :param duration {int}: subscription duration
        :param identifier {string}: optional identifier
        :param meta {string}: optional meta data
        :return:
        """
        nonce = self.get_nonce()
        pld = Payload.new_subscribe(self.public_key, identifier, topic, bucket, duration, meta)
        txn = Transaction.new_transaction(self._account, pld, nonce, options.get('fee', 0), options.get('attrs', 0))

        return self._api.send_raw_transaction(txn.SerializeToString().hex())

    def create_or_update_nano_pay(self, to_address, amount, expiration, id):
        if not Protocol.verify_address(to_address):
            raise WalletError.INVALID_ADDRESS()
        balance = self.get_balance()
        if balance < amount:
            raise WalletError.NOT_ENOUGH_NKN_COIN()
        if id is None:
            id = Tools.random_uint64()
        pld = Payload.new_nano_pay(self._program_hash, Protocol.address_string_to_program_hash(to_address), id, amount,
                                   expiration, expiration)
        txn = Transaction.new_transaction(self._account, pld)
        return txn

    def send_transaction(self, txn):
        return self._api.send_raw_transaction(txn.SerializeToString().hex())

    @classmethod
    def get_balance_by_addr(cls, address):
        """
        query balance
        :param address:{string} nkn address
        :return:{float} amount
        """
        return float(cls._api.get_balance_by_addr(address)['amount'])

    def get_nonce(self):
        return self._api.get_nonce_by_addr(self.address)['nonce']

    @classmethod
    def get_nonce_by_addr(cls, address):
        return cls._api.get_nonce_by_addr(address)['nonce']

    @classmethod
    def get_address_by_name(cls, name):
        return cls._api.get_address_by_name(name)

    @classmethod
    def get_block_count_by_name(cls, name):
        return cls._api.get_block_count_by_name(name)

    def verify_wallet_password(self, password):
        password_hash = to_password_hash(password)
        return self._password_hash == Hash.sha256_hex(password_hash)

    def to_dict(self):
        """
        generate a wallet in dict format
        :return:{dict} wallet dict
        """
        return {
            'Version': self._version,
            'PasswordHash': self._password_hash,
            'MasterKey': self._master_key,
            'IV': self._iv,
            'SeedEncrypted': self._seed_encrypted,
            'Address': self._address,
            'ProgramHash': self._program_hash,
            'ContractData': self._contract_data
        }

    def to_json(self):
        """
        generate a wallet in JSON format
        :return:{string} wallet json
        """
        return json.dumps(self.to_dict())

    def save_file(self, file):
        """
        generate a wallet and save file
        :param file:{string} file path
        """
        with open(file, 'w') as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def new_wallet(cls, password):
        """
        create a new wallet
        :param password:{string} the password to encrypt wallet
        :return:{Wallet} a NKN Wallet instance
        """
        account = Account()
        return cls.gen_wallet(account, password)

    @classmethod
    def restore_wallet_by_seed(cls, seed, password):
        """
        restore a wallet from seed
        :param seed:{string} the seed for wallet restore
        :param password:{string} password for new wallet
        :return:{Wallet} a NKN Wallet instance
        """
        account = Account.restore_account(seed)
        return cls.gen_wallet(account, password)

    @classmethod
    def restore_wallet_from_json(cls, seed, password, prev_master_key, pre_iv):
        """
        restore a wallet from json
        :param seed:{string} the seed for wallet restore
        :param password:{string} password for wallet
        :return:{Wallet} a NKN Wallet instance
        """
        account = Account.restore_account(seed)
        return cls.gen_wallet(account, password, prev_master_key, pre_iv)

    @classmethod
    def load_json_wallet(cls, wallet_json, password):
        wallet_dict = json.loads(wallet_json)
        if wallet_dict['Version'] < cls.MIN_COMPATIBLE_WALLET_VERSION or wallet_dict[
            'Version'] > cls.MAX_COMPATIBLE_WALLET_VERSION:
            raise ValueError(
                'Invalid wallet version ' + wallet_dict[
                    'Version'] + ', should be between ' + cls.MIN_COMPATIBLE_WALLET_VERSION + ' and ' + cls.MAX_COMPATIBLE_WALLET_VERSION)
        if not isinstance(wallet_dict['MasterKey'], str) or not isinstance(wallet_dict['IV'], str) or not isinstance(
                wallet_dict['SeedEncrypted'], str) or not isinstance(wallet_dict['Address'], str):
            raise ValueError('Invalid wallet format')
        pswd_hash = to_password_hash(password)
        if wallet_dict['PasswordHash'] != Hash.sha256_hex(pswd_hash):
            raise ValueError('Wrong password')
        master_key = Encryption.decrypt(binascii.unhexlify(wallet_dict['MasterKey']), binascii.unhexlify(pswd_hash),
                                        binascii.unhexlify(wallet_dict['IV']))
        seed = Encryption.decrypt(binascii.unhexlify(wallet_dict['SeedEncrypted']), master_key,
                                  binascii.unhexlify(wallet_dict['IV']))

        wallet = cls.restore_wallet_from_json(binascii.hexlify(seed).decode(), password,
                                              binascii.hexlify(master_key).decode(), wallet_dict['IV'])
        return wallet

    @classmethod
    def gen_wallet(cls, account, password, prev_master_key=None, prev_iv=None):
        wallet = cls(account)
        pswd_hash = to_password_hash(password)
        iv = Encryption.gen_aes_iv() if prev_iv is None else binascii.unhexlify(prev_iv)
        master_key = Encryption.gen_aes_password() if prev_master_key is None else binascii.unhexlify(prev_master_key)
        seed = binascii.unhexlify(account.seed)
        wallet._password_hash = Hash.sha256_hex(pswd_hash)
        wallet._iv = binascii.hexlify(iv).decode()
        wallet._master_key = binascii.hexlify(
            Encryption.encrypt(master_key, binascii.unhexlify(pswd_hash), iv)).decode()
        wallet._address = account.address
        wallet._program_hash = account.program_hash
        wallet._seed_encrypted = binascii.hexlify(Encryption.encrypt(seed, master_key, iv)).decode()
        wallet._contract_data = account.contract
        wallet._version = cls.WALLET_VERSION
        return wallet

    @staticmethod
    def verify_address(address):
        return Protocol.verify_address(address)

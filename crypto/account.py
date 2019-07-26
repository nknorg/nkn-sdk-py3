from crypto import Key, Protocol, Tools


class Account(object):

    def __init__(self, seed=None):
        self._key = Key(seed)
        self._address = Protocol.program_hash_string_to_address(self._key.program_hash)
        self._contract = self.gen_account_contract_string(self._key.signature_redeem, self._key.program_hash)

    @property
    def address(self):
        return self._address

    @property
    def contract(self):
        return self._contract

    @property
    def public_key(self):
        return self._key.public_key

    @property
    def private_key(self):
        return self._key.private_key

    @property
    def seed(self):
        return self._key.seed

    @property
    def program_hash(self):
        return self._key.program_hash

    @property
    def signature_redeem(self):
        return self._key.signature_redeem

    @classmethod
    def restore_account(cls, seed):
        if not isinstance(seed, str):
            raise ValueError('seed is not a string')
        return cls(seed)

    @staticmethod
    def gen_account_contract_string(signature_redeem, program_hash):
        contract = ''
        contract += Tools.prefix_byte_count_to_hex_string(signature_redeem)
        contract += Tools.prefix_byte_count_to_hex_string('00')
        contract += program_hash
        return contract

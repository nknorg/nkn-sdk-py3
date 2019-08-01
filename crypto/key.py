import nacl.utils
import nacl.secret
import nacl.signing
import nacl.bindings
from nacl.encoding import HexEncoder

from crypto import Protocol


class Key(object):
    def __init__(self, seed=None):
        if seed is None:
            seed = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        else:
            seed = HexEncoder.decode(seed)
        public_key, secret_key = nacl.bindings.crypto_sign_seed_keypair(seed)
        self._public_key = HexEncoder.encode(public_key).decode()
        self._private_key = HexEncoder.encode(secret_key).decode()
        self._seed = HexEncoder.encode(seed).decode()
        self._signature_redeem = Protocol.public_key_to_signature_redeem(self._public_key)
        self._program_hash = Protocol.hex_string_to_program_hash(self._signature_redeem)

    @property
    def public_key(self):
        return self._public_key

    @property
    def private_key(self):
        return self._private_key

    @property
    def seed(self):
        return self._seed

    @property
    def signature_redeem(self):
        return self._signature_redeem

    @property
    def program_hash(self):
        return self._program_hash

    def sign(self, message):
        sig = nacl.bindings.crypto_sign(message, HexEncoder.decode(self._private_key))
        return sig[:64]  # length > 64, so cut 64

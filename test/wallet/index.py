import binascii
import json

from wallet import Wallet


wallet = Wallet.new_wallet('pswd')
print(wallet.to_json())

wallet_from_json = Wallet.load_json_wallet(wallet.to_json(), 'pswd')
print(wallet_from_json.to_dict())

wallet_from_seed = Wallet.restore_wallet_by_seed(wallet.seed, 'aaa')
print(wallet_from_seed.to_dict())
print(Wallet.verify_address(wallet.address))
print(wallet.verify_wallet_password('pswd'))

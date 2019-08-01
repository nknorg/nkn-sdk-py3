from wallet import Wallet


wallet = Wallet.new_wallet('pswd')
print(wallet.to_json())
print(wallet.address)
wallet_from_json = Wallet.load_json_wallet(wallet.to_json(), 'pswd')
print(wallet_from_json.to_dict())

wallet_from_seed = Wallet.restore_wallet_by_seed(wallet.seed, 'aaa')
print(wallet_from_seed.to_dict())
print(Wallet.verify_address(wallet.address))
print(wallet.verify_wallet_password('pswd'))

print(wallet.get_balance())
print(Wallet.get_balance_by_addr(wallet.address))

print(wallet.get_nonce())
print(Wallet.get_nonce_by_addr(wallet.address))

print(Wallet.get_address_by_name('google'))
print(Wallet.get_block_count_by_name('google'))


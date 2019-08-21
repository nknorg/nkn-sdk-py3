from nknsdk.wallet import Wallet

# Create a new wallet
wallet = Wallet.new_wallet('pswd')

# Get wallet's json string
print(wallet.to_json())

# Get wallet's address
print(wallet.address)

# Load wallet from a wallet json string
wallet_from_json = Wallet.load_json_wallet(wallet.to_json(), 'pswd')

# Get wallet's json to dict
print(wallet_from_json.to_dict())

# Restore wallet from a private key
wallet_from_seed = Wallet.restore_wallet_by_seed(wallet.seed, 'aaa')

# Verify whether an address is valid
print(Wallet.verify_address(wallet.address))

# Verify password of the wallet
print(wallet.verify_wallet_password('pswd'))

# Get balance of this wallet
print(wallet.get_balance())

# Get balance of address
print(Wallet.get_balance_by_addr(wallet.address))

# Get nonce for next transaction of this wallet
print(wallet.get_nonce())

# Get nonce for next transaction of address
print(Wallet.get_nonce_by_addr(wallet.address))

# Get wallet address of a name
print(Wallet.get_address_by_name('somename'))

# Transfer token to some address
print(wallet.transfer_to(wallet.address, 1, fee=0.00000001))

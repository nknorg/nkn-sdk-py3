# nkn-sdk-py3

## Install

```shell
pip install nkn-sdk
```

## Usage

Import library
```python
from nknsdk.wallet import Wallet
```

+ Create a new wallet
```python
wallet = Wallet.new_wallet('pswd')
```

+ Get wallet's json string
```python
print(wallet.to_json())
```

+ Get wallet's address
```python
print(wallet.address)
```

+ Transfer token to some address
```python
print(wallet.transfer_to(wallet.address, 1, fee=0.00000001))
```

+ Load wallet from a wallet json string
```python
wallet_from_json = Wallet.load_json_wallet(wallet.to_json(), 'pswd')
```

+ Get wallet's json to dict
```python
print(wallet_from_json.to_dict())
```

+ Restore wallet from Ed25519 seed
```python
wallet_from_seed = Wallet.restore_wallet_by_seed(wallet.seed, 'aaa')
```

+ Verify whether an address is valid
```python
print(Wallet.verify_address(wallet.address))
```

+ Verify password of the wallet
```python
print(wallet.verify_wallet_password('pswd'))
```

+ Get balance of this wallet
```python
print(wallet.get_balance())
```

+ Get balance of address
```python
print(Wallet.get_balance_by_addr(wallet.address))
```

+ Get nonce for next transaction of this wallet
```python
print(wallet.get_nonce())
```

+ Get nonce for next transaction of address
```python
print(Wallet.get_nonce_by_addr(wallet.address))
```

+ Get wallet address of a name
```python
print(Wallet.get_address_by_name('somename'))
```

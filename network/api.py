import json

from config import Config
import requests


class Api(object):
    _configure = Config
    _timeout = 10
    _params = {
        'jsonrpc': '2.0',
        'id': 'nkn-sdk-py3'
    }

    def __init__(self, new_config=Config):
        self._configure = new_config

    @property
    def configure(self):
        return self._configure

    @configure.setter
    def configure(self, new_config):
        self._configure.update(new_config)

    def request(self, method, params, call_id=None, timeout=None):
        if self._configure['RPC_ADDR'] is None:
            raise ValueError('RPC server address is not set')
        data = self._params.copy()
        data.update({
            'method': method,
            'params': params
        })
        if call_id is not None:
            data.update({'id': call_id})

        res = requests.post(self._configure['RPC_ADDR'], json=data, timeout=timeout or self._timeout)

        if res.status_code != 200:
            raise ValueError(res.status_code)
        res_data = res.json()
        if 'error' in res_data:
            return res_data['error']
        if 'result' in res_data:
            return res_data['result']
        raise ValueError('Response format error')

    def get_balance_by_addr(self, address):
        if address is None:
            raise ValueError('Address not set')

        return self.request('getbalancebyaddr', {'address': address})

    def get_nonce_by_addr(self, address):
        if address is None:
            raise ValueError('Address not set')
        return self.request('getnoncebyaddr', {'address': address})

    def get_address_by_name(self, name):
        return self.request('getaddressbyname', {'name': name})

    def get_block_count_by_name(self, name):
        return self.request('getblockcount', {'name': name})

    def send_raw_transaction(self, tx):
        return self.request('sendrawtransaction', {'tx': tx})

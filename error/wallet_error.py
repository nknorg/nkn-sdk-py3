class WalletError(Exception):
    def __init__(self, code, msg):
        super().__init__(self)
        self._code = code
        self._msg = msg

    @classmethod
    def UNKNOWN_ERR(cls):
        return cls(0, 'UNKNOWN_ERR')

    @classmethod
    def NOT_ENOUGH_NKN_COIN(cls):
        return cls(1, 'NOT_ENOUGH_NKN_COIN')

    @classmethod
    def INVALID_ADDRESS(cls):
        return cls(2, 'INVALID_ADDRESS')

    @classmethod
    def INVALID_PASSWORD(cls):
        return cls(3, 'INVALID_PASSWORD')

    @classmethod
    def INVALID_WALLET_FORMAT(cls):
        return cls(4, 'INVALID_WALLET_FORMAT')

    @classmethod
    def INVALID_WALLET_VERSION(cls):
        return cls(5, 'INVALID_WALLET_VERSION')

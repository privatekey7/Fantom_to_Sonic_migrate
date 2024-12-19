from web3 import Web3

# Настройки задержек между кошельками (в секундах)
MIN_DELAY = 300  # минимальная задержка
MAX_DELAY = 900  # максимальная задержка

# Настройка перемешивания кошельков
SHUFFLE_WALLETS = True  # True - перемешивать, False - по порядку

# Настройки RPC
RPC_URL = 'https://rpc.ftm.tools'

# Адрес контракта (преобразуем в checksum формат)
CONTRACT_ADDRESS = Web3.to_checksum_address('0x3561607590e28e0848ba3b67074c676d6d1c9953')

# ABI контракта
CONTRACT_ABI = '''[
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "fee",
                "type": "uint256"
            }
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]''' 
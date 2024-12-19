from web3 import Web3
from eth_account import Account
import json
import time
import random
from datetime import datetime
from colorama import init, Fore
from config import *

# Инициализация colorama
init(autoreset=True)

def print_welcome_message():
    welcome_message = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗
║                                                            ║
║     {Fore.GREEN}    ███████╗████████╗███╗   ███╗   ███████╗            {Fore.CYAN}║
║     {Fore.GREEN}    ██╔════╝╚══██╔══╝████╗ ████║   ██╔════╝            {Fore.CYAN}║
║     {Fore.GREEN}    █████╗     ██║   ██╔████╔██║   ███████╗            {Fore.CYAN}║
║     {Fore.GREEN}    ██╔══╝     ██║   ██║╚██╔╝██║   ╚════██║            {Fore.CYAN}║
║     {Fore.GREEN}    ██║        ██║   ██║ ╚═╝ ██║   ███████║            {Fore.CYAN}║
║     {Fore.GREEN}    ╚═╝        ╚═╝   ╚═╝     ╚═╝   ╚══════╝            {Fore.CYAN}║
║                                                            ║
║           {Fore.YELLOW}VERSION: 1.0.0                                   {Fore.CYAN}║
║           {Fore.YELLOW}Channel: https://t.me/privatekey7                {Fore.CYAN}║
║           {Fore.YELLOW}GitHub: https://github.com/privatekey7           {Fore.CYAN}║
║           {Fore.YELLOW}Powered by Pavel Durov                           {Fore.CYAN}║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """
    print(welcome_message)

# Цвета для логирования
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'

def log_print(message, color=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if color:
        print(f"[{timestamp}] {color}{message}{Colors.RESET}")
    else:
        print(f"[{timestamp}] {message}")

# Подключаемся к Fantom
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Создаем экземпляр контракта
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def read_private_keys():
    with open('private_keys.txt', 'r') as file:
        return [key.strip() for key in file.readlines()]

def process_deposit(private_key):
    account = Account.from_key(private_key)
    address = account.address
    
    # Получаем баланс
    balance = w3.eth.get_balance(address)
    balance_in_ftm = w3.from_wei(balance, 'ether')
    
    if balance_in_ftm < 1:
        log_print(f"{address} - Баланс {balance_in_ftm:.1f} FTM (минималка 1 FTM)", Colors.RED)
        return
    
    try:
        # Получаем текущую цену газа
        gas_price = w3.eth.gas_price
        
        # Фиксированное значение fee из требований
        fee = 100000000000000000  # 0.1 FTM в wei
        
        # Оценка газа для транзакции
        gas_estimate = contract.functions.deposit(fee).estimate_gas({
            'from': address,
            'value': balance - (gas_price * 21000 * 2)  # Примерная оценка газа
        })
        
        # Рассчитываем комиссию за транзакцию
        transaction_fee = gas_price * gas_estimate
        
        # Отправляем весь баланс за вычетом комиссии за газ
        deposit_amount = balance - (transaction_fee * 2)
        
        log_print(f"{address} - Баланс {balance_in_ftm:.2f} FTM", Colors.BLUE)
        
        # Подготавливаем транзакцию
        transaction = contract.functions.deposit(fee).build_transaction({
            'from': address,
            'value': deposit_amount,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': w3.eth.get_transaction_count(address),
        })
        
        # Подписываем и отправляем транзакцию
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        log_print(f"{address} - Успешно отправлено {w3.from_wei(deposit_amount, 'ether'):.2f} FTM", Colors.GREEN)
        log_print(f"Ссылка на транзакцию: https://ftmscan.com/tx/{tx_hash.hex()}", Colors.YELLOW)
        
        # Ждем подтверждения транзакции
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt['status'] == 1:
            log_print("Транзакция подтверждена", Colors.GREEN)
        else:
            log_print("Транзакция не подтверждена", Colors.RED)
        
    except Exception as e:
        log_print(f"Ошибка при обработке кошелька {address}: {str(e)}", Colors.RED)

def main():
    print_welcome_message()
    private_keys = read_private_keys()
    
    if SHUFFLE_WALLETS:
        random.shuffle(private_keys)
        log_print("Кошельки перемешаны", Colors.YELLOW)
    
    for private_key in private_keys:
        try:
            process_deposit(private_key)
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            log_print(f"Ожидание {delay:.1f} секунд перед следующей транзакцией...", Colors.YELLOW)
            time.sleep(delay)
        except Exception as e:
            log_print(f"Ошибка при обработке кошелька: {e}", Colors.RED)

if __name__ == "__main__":
    main()
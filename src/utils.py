from typing import List, Dict
import json
import random
import string
from pathlib import Path
from loguru import logger
import sys
from config import (
    LOG_FILE, PROXY_FILE, ACCOUNTS_FILE, ADDRESSES_FILE,
    LOG_DIR, DATA_DIR
)

def setup_logger():
    LOG_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    
    logger.remove()
    
    logger.add(LOG_FILE, rotation="10 MB", compression="zip", level="DEBUG")
    
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level="INFO",
        colorize=True,
        filter=lambda record: record["level"].name not in ["DEBUG", "TRACE"]
    )

def read_proxies() -> List[str]:
    try:
        with open(PROXY_FILE, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
            logger.info(f"Loaded {len(proxies)} proxies")
            return proxies
    except FileNotFoundError:
        logger.error(f"Proxy file not found: {PROXY_FILE}")
        return []

def read_accounts() -> List[Dict[str, str]]:
    try:
        with open(ACCOUNTS_FILE, 'r') as file:
            return [json.loads(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        logger.error(f"Accounts file not found: {ACCOUNTS_FILE}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in accounts file")
        return []

def write_submission_result(filename: str, account: Dict[str, str]):
    try:
        with open(filename, 'a') as file:
            json.dump(account, file)
            file.write('\n')
    except Exception as e:
        logger.error(f"Error writing to {filename}: {str(e)}")

def read_addresses() -> List[str]:
    try:
        with open(ADDRESSES_FILE, 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]
            logger.info(f"Loaded {len(addresses)} addresses")
            return addresses
    except FileNotFoundError:
        logger.error(f"Addresses file not found: {ADDRESSES_FILE}")
        return []

def generate_random_email(nickname: str, firstname: str) -> str:
    year = random.randint(1980, 2005)
    email_providers = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    email = f"{nickname.lower()}.{firstname.lower()}{year}@{random.choice(email_providers)}"
    return email

def generate_discord_tag(username: str) -> str:
    modified_username = ''.join(random.choices(username + string.ascii_lowercase, k=len(username)))
    tag = ''.join(random.choices(string.digits, k=4))
    return f"{modified_username}#{tag}"

def generate_wallet_address() -> str:
    address = '0x' + ''.join(random.choices(string.hexdigits, k=40))
    return address.lower()

def generate_username() -> str:
    adjectives = ['crypto', 'tech', 'dev', 'code', 'web3', 'data']
    nouns = ['wizard', 'ninja', 'master', 'guru', 'pro', 'expert']
    numbers = ''.join(random.choices(string.digits, k=2))
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"

class AddressManager:
    def __init__(self, addresses_file):
        self.addresses_file = addresses_file
        self.addresses = []
        self.current_index = 0
        self._load_addresses()
    
    def _load_addresses(self):
        try:
            with open(self.addresses_file, 'r') as file:
                self.addresses = [line.strip() for line in file if line.strip()]
            logger.info(f"All {len(self.addresses)} addresses")
        except FileNotFoundError:
            logger.error(f"FileNotFoundError: {self.addresses_file}")
            self.addresses = []

    def get_next_address(self) -> str:
        if not self.addresses:
            return generate_wallet_address()
        
        address = self.addresses[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.addresses)
        return address

def generate_account_data(address_manager: AddressManager) -> Dict[str, str]:
    nickname = generate_username()
    firstname = ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
    
    return {
        "nickname": nickname,
        "firstname": firstname,
        "wallet": address_manager.get_next_address(),
        "email": generate_random_email(nickname, firstname),
        "discord": generate_discord_tag(nickname),
        "huggingface": f"hf_{generate_username()}",
        "kaggle": f"k_{generate_username()}",
        "github": f"gh_{generate_username()}"
    }
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
    
    logger.add(LOG_FILE, 
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        rotation="10 MB", 
        compression="zip", 
        level="DEBUG"
    )
    
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

def get_random_firstname() -> str:
    first_names = [
        "Alex", "Michael", "David", "John", "James", "Robert", "William", "Thomas",
        "Daniel", "Kevin", "Brian", "George", "Edward", "Richard", "Joseph", "Charles",
        "Christopher", "Andrew", "Paul", "Mark", "Donald", "Steven", "Kenneth", "Anthony",
        "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia",
        "Harper", "Evelyn", "Abigail", "Emily", "Elizabeth", "Sofia", "Avery", "Ella",
        "Scarlett", "Grace", "Victoria", "Riley", "Aria", "Lily", "Aurora", "Zoey"
    ]
    return random.choice(first_names)

def generate_random_email(username: str) -> str:
    year = random.randint(1990, 2020)
    email_providers = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    email = f"{username}{year}@{random.choice(email_providers)}"
    return email

def generate_username_for_service() -> str:
    prefixes = [
        'dev', 'hack', 'code', 'algo', 'py', 'data', 'ml', 'ai', 'web', 
        'quantum', 'cyber', 'cloud', 'deep', 'neural', 'robot', 'tech'
    ]
    suffixes = [
        'master', 'ninja', 'guru', 'wizard', 'pro', 'dev', 'hacker', 
        'coder', 'engineer', 'scientist', 'researcher', 'architect'
    ]
    
    pattern = random.choice([
        "{prefix}_{suffix}",
        "{prefix}{suffix}",
        "the_{prefix}_{suffix}",
        "{prefix}.{suffix}"
    ])
    
    username = pattern.format(
        prefix=random.choice(prefixes),
        suffix=random.choice(suffixes)
    )
    
    if random.random() > 0.5:
        username += str(random.randint(1, 99))
    
    return username

def generate_wallet_address() -> str:
    address = '0x' + ''.join(random.choices(string.hexdigits, k=40))
    return address.lower()

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
    firstname = get_random_firstname()
    base_username = generate_username_for_service()
    
    return {
        "nickname": base_username,
        "firstname": firstname,
        "wallet": address_manager.get_next_address(),
        "email": generate_random_email(base_username),
        "discord": f"{base_username}{random.randint(1000, 9999)}",
        "huggingface": generate_username_for_service(),
        "kaggle": generate_username_for_service(),
        "github": generate_username_for_service(),
        "telegram": base_username,
        "linkedin": f"{firstname.lower()}-{generate_username_for_service()}",
        "twitter": generate_username_for_service()
    }

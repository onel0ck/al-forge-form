import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
from loguru import logger
import os
import json

from config import (
    TIMEOUT_BETWEEN_ACCOUNTS, MAX_WORKERS,
    SUCCESSFUL_SUBMISSIONS_FILE, FAILED_SUBMISSIONS_FILE,
    ACCOUNTS_FILE, ADDRESSES_FILE
)
from utils import (
    read_proxies, read_accounts, write_submission_result,
    generate_account_data, setup_logger, AddressManager
)
from form_submitter import TypeformSubmitter

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_accounts():
    address_manager = AddressManager(ADDRESSES_FILE)
    
    if not address_manager.addresses:
        logger.error("No addresses found in file")
        return False

    count = len(address_manager.addresses)
    logger.info(f"Generating {count} accounts...")
    
    try:
        with open(ACCOUNTS_FILE, 'w') as file:
            for _ in range(count):
                account = generate_account_data(address_manager)
                json.dump(account, file)
                file.write('\n')
        logger.success(f"Successfully generated {count} accounts to 'accounts.txt'")
        return True
    except Exception as e:
        logger.error(f"Error generating accounts: {str(e)}")
        return False

def process_submission(account: Dict[str, str], proxies: List[str]) -> bool:
    proxy = random.choice(proxies)
    submitter = TypeformSubmitter()
    
    try:
        result = submitter.submit_full_form(account, proxy)
        
        if "error" in result:
            logger.error(f"Submission failed: {account['wallet']}")
            write_submission_result(FAILED_SUBMISSIONS_FILE, account)
            return False
        
        logger.success(f"Form submitted: {account['wallet']}")
        write_submission_result(SUCCESSFUL_SUBMISSIONS_FILE, account)
        return True
        
    except Exception as e:
        logger.error(f"Error processing: {account['wallet']}")
        write_submission_result(FAILED_SUBMISSIONS_FILE, account)
        return False

def run_form_submission():
    logger.info("Starting form submission process...")
    
    try:
        proxies = read_proxies()
        accounts = read_accounts()
        
        if not proxies or not accounts:
            logger.error("Missing proxies or accounts")
            return
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for account in accounts:
                executor.submit(process_submission, account, proxies)
                time.sleep(TIMEOUT_BETWEEN_ACCOUNTS)
                
    except Exception as e:
        logger.error(f"Process error: {str(e)}")
    
    logger.info("Form submission completed")

def main_menu():
    while True:
        clear_screen()
        print("\n=== Allora Forge Form Submitter ===")
        print("Created by: https://t.me/unluck_1l0ck")
        print("\n1. Generate Accounts")
        print("2. Run Form Submission")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            generate_accounts()
            time.sleep(2)
        elif choice == "2":
            run_form_submission()
            input("\nPress Enter to continue...")
        elif choice == "3":
            logger.info("Exiting...")
            break
        else:
            logger.warning("Invalid choice")
            time.sleep(1)

if __name__ == "__main__":
    setup_logger()
    main_menu()
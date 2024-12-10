import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / 'data'
LOG_DIR = ROOT_DIR / 'logs'
SRC_DIR = ROOT_DIR / 'src'

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

TIMEOUT_BETWEEN_ACCOUNTS = 60
TIMEOUT_BETWEEN_REQUESTS = 2

FORM_ID = "ypA2Yl1J"
FORM_BASE_URL = "https://vk4z45e3hne.typeform.com"

LOG_FILE = LOG_DIR / 'debug.log'
PROXY_FILE = DATA_DIR / 'proxies.txt'
ACCOUNTS_FILE = DATA_DIR / 'accounts.txt'
ADDRESSES_FILE = DATA_DIR / 'addresses.txt'
SUCCESSFUL_SUBMISSIONS_FILE = LOG_DIR / 'successful_submissions.txt'
FAILED_SUBMISSIONS_FILE = LOG_DIR / 'failed_submissions.txt'

MAX_WORKERS = 3
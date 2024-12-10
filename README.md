# Allora Form Submission

I have made only for introductory purposes, I do not encourage anyone to use this software, it is prohibited by law. This project automates the process of submitting forms for Allora Forge accounts.

**My Socials:**
- Telegram: https://t.me/unluck_1l0ck
- X: https://x.com/1l0ck

## Setup

1. Clone the repository:
```bash
git clone https://github.com/onel0ck/al-forge-form.git
cd al-forge-form
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# For Windows:
cd venv/Scripts
activate
cd ../..
# For Linux/MacOS:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Prepare the data files in the `data` directory:
   * `addresses.txt`: Contains wallet addresses (one per line)
   * `proxies.txt`: Contains proxy addresses in format `http://login:password@ip:port` (only static proxies)

5. Create required directories:
```
project/
├── data/
│   ├── proxies.txt
│   ├── addresses.txt
│   └── accounts.txt (will be generated automatically)
└── logs/
    ├── debug.log (will be generated automatically)
    ├── successful_submissions.txt
    └── failed_submissions.txt
```

6. Generate accounts:
   * Run the script using `python main.py`
   * Select option 1 "Generate Accounts"
   * Accounts will be generated based on your addresses in `addresses.txt`

7. Submit forms:
   * After successful generation, select option 2 "Run Form Submission"
   * The script will process all generated accounts using provided proxies

## Results
* Successfully submitted forms will be logged in `logs/successful_submissions.txt`
* Failed submissions will be logged in `logs/failed_submissions.txt`
* Detailed logs can be found in `logs/debug.log`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Support
If you have any questions, feel free to reach out:
* Telegram: [@unluck_1l0ck](https://t.me/unluck_1l0ck)
* X: [@1l0ck](https://x.com/1l0ck)

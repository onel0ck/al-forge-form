# Allora Forge Form Submission

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

5. Customize account generation (important):
   Open `utils.py` and customize these variables to make your accounts look more natural:
   * `prefixes`: Add your own prefixes for usernames
   * `suffixes`: Add your own suffixes for usernames
   * `first_names`: Add more real names to make accounts look more natural
   
   Example of customization:
   ```python
   prefixes = [
       'dev', 'hack', 'code', 'algo', 'py', 'data', 'ml', 'ai', 'web',
       # Add your own prefixes here
   ]
   
   suffixes = [
       'master', 'ninja', 'guru', 'wizard', 'pro', 'dev', 'hacker',
       # Add your own suffixes here
   ]
   
   first_names = [
       "Alex", "Michael", "David", "John",
       # Add more names here
   ]
   ```

6. Create required directories:
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

7. Generate accounts:
   * Run the script using `python main.py`
   * Select option 1 "Generate Accounts"
   * Accounts will be generated based on your addresses in `addresses.txt`

8. Submit forms:
   * After successful generation, select option 2 "Run Form Submission"
   * The script will process all generated accounts using provided proxies

## Results
* Successfully submitted forms will be logged in `logs/successful_submissions.txt`
* Failed submissions will be logged in `logs/failed_submissions.txt`
* Detailed logs can be found in `logs/debug.log`

## Important Notes
* Make sure to customize the username generation in `utils.py` before running the script
* The more diverse your custom words and names are, the more natural the generated accounts will look
* Don't use the default values - customize them according to your needs

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Support
If you have any questions, feel free to reach out:
* Telegram: [@unluck_1l0ck](https://t.me/unluck_1l0ck)
* X: [@1l0ck](https://x.com/1l0ck)

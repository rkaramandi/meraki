# Meraki Scripts
Scripts to do Meraki things. All of this code is for proof of concept and not intended for production use. Feel free to modify and adapt if you would like, at your own risk.

## Prerequisites / Installation
- Make sure you have python3 installed (I tested this on 3.8.2). Use `python3 --version` to check your version.
- Clone this repo `git clone https://github.com/rkaramandi/meraki.git`
- Use `pip` or `pip3` to install required libraries. `pip install -r requirements.txt`
- Add your Meraki API key into an environment variable. `export MERAKI_DASHBOARD_API_KEY=` and your API key after that.

## add_wpn_user.py
Adds an iPSK credential into Dashboard and creates an associated group policy. Make sure you fill out the constants near the top of the file.

## remove_wpn_user.py
Removes an iPSK credential from Dashboard and removes associated group policy. Make sure you fill out the constants near the top of the file.
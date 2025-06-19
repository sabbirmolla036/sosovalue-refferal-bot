import requests
import base64
import mail
import time
import os
import random
import string
from bs4 import BeautifulSoup  # pip install beautifulsoup4

logo = f"""
█████╗ ██████╗  █████╗ ███████╗ █████╗ ████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
███████║██████╔╝███████║█████╗  ███████║   ██║
██╔══██║██╔══██╗██╔══██║██╔══╝  ██╔══██║   ██║
██║  ██║██║  ██║██║  ██║██║     ██║  ██║   ██║
╚═╝  ╚═╝╚═╝  ██╔╝═╝╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝
----------------------------------------------------
> TG CHANNEL :  @cryptowitharyanog
> YouTube    :  @cryptowitharyan
\033[1;34m------------------------------------------\033[0m"""

os.system('cls' if os.name == 'nt' else 'clear')
print(logo)

base_url = input('> Input base url : ')
refcode = input('> Referral code : ')
target_referrals = int(input('> Enter target referral count (number of accounts to create): '))
use_free_proxy = input('> Use free proxies from internet? (y/n): ').strip().lower() == 'y'
proxy_type = input('> Proxy type (http/socks4/socks5): ').strip().lower()

if proxy_type not in ['http', 'socks4', 'socks5']:
    print('\033[1;33m[!] Invalid proxy type. Defaulting to http.\033[0m')
    proxy_type = 'http'

print('\033[1;34m------------------------------------------\033[0m')

def generate_password(length=8):
    length = max(length, 8)
    parts = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("@#$&"),
    ]
    parts += random.choices(string.ascii_letters + string.digits + "@#$&", k=length - 4)
    password = ''.join(parts)
    return base64.b64encode(password.encode()).decode()

def get_random_proxy():
    try:
        with open('proxy.txt', 'r') as f:
            proxies = [p.strip() for p in f if p.strip()]
        if not proxies:
            return None
        selected = random.choice(proxies)
        return {
            'http': f'{proxy_type}://{selected}',
            'https': f'{proxy_type}://{selected}'
        }
    except FileNotFoundError:
        return None

def fetch_free_proxy():
    try:
        resp = requests.get("https://free-proxy-list.net/", timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.select("table#proxylisttable tbody tr")
        proxies = [
            f"{r.find_all('td')[0].text}:{r.find_all('td')[1].text}"
            for r in rows if r.find_all('td')[6].text.strip().lower() == "yes"
        ]
        if not proxies:
            print("\033[1;31m[-] No HTTPS proxies found.\033[0m")
        return proxies
    except Exception as e:
        print(f"\033[1;31m[-] Free-proxy fetch error: {e}\033[0m")
        return []

def get_captcha():
    while True:
        token = requests.get(f'{base_url}/get').text
        if token != "No tokens available":
            return token
        time.sleep(0.3)

def create_account(captcha_token, password, email, proxy):
    url = 'https://gw.sosovalue.com/usercenter/email/anno/sendRegisterVerifyCode/V2'
    payload = {
        'password': password,
        'rePassword': password,
        'username': 'NEW_USER_NAME_02',
        'email': email
    }
    headers = {
        'Host': 'gw.sosovalue.com',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15)...',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://m.sosovalue.com',
        'referer': 'https://m.sosovalue.com/',
    }
    return requests.post(url, params={'cf-turnstile-response': captcha_token},
                         headers=headers, json=payload, proxies=proxy, timeout=15).json()

def verify_email(password, email, code, refcode, proxy):
    url = 'https://gw.sosovalue.com/usercenter/user/anno/v3/register'
    payload = {
        'password': password,
        'rePassword': password,
        'username': 'NEW_USER_NAME_02',
        'email': email,
        'verifyCode': code,
        'invitationCode': refcode,
        'invitationFrom': 'null'
    }
    headers = {
        'Host': 'gw.sosovalue.com',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15)...',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://m.sosovalue.com',
        'referer': 'https://m.sosovalue.com/',
    }
    return requests.post(url, headers=headers, json=payload, proxies=proxy, timeout=15).json()

def show_referral_progress(done, target):
    print(f"\033[1;34mReferral Progress: {done} done, {target-done} to go (Target: {target})\033[0m")

successful = 0
free_proxy_list = fetch_free_proxy() if use_free_proxy else []

while True:
    if successful >= target_referrals:
        print(f"\033[1;34mTarget of {target_referrals} reached. Done.\033[0m")
        break
    try:
        email = mail.getmails()
        print('> \033[1;32mNew email:', email)
        b64pass = generate_password()
        decpass = base64.b64decode(b64pass).decode()
        print('> \033[1;32mPassword:', decpass)

        token = get_captcha()

        if use_free_proxy:
            if not free_proxy_list:
                print('\033[1;31mNo free proxies available. Exiting.\033[0m')
                break
            selected = random.choice(free_proxy_list)
            proxy = {
                'http': f'{proxy_type}://{selected}',
                'https': f'{proxy_type}://{selected}'
            }
        else:
            proxy = get_random_proxy()
            if not proxy:
                print('\033[1;31mNo local proxies available. Exiting.\033[0m')
                break

        resp1 = create_account(token, b64pass, email, proxy)
        if resp1.get('code') != 0:
            print('\033[1;31mAccount creation failed:', resp1)
            continue
        print('> \033[1;32mEmail verification code sent.\033[0m')

        username, domain = email.split('@')
        code = mail.get_verification_link(email, domain)
        resp2 = verify_email(b64pass, email, code, refcode, proxy)
        if resp2.get('code') == 0:
            successful += 1
            print('> \033[1;32mEmail verified & account registered.\033[0m')
            show_referral_progress(successful, target_referrals)

            token_data = resp2['data']
            with open('accounts.txt', 'a') as f:
                f.write(f"Email: {email}\nPassword: {decpass}\nToken: {token_data.get('token')}\nRefresh: {token_data.get('refreshToken')}\n{'-'*24}\n")

        else:
            print('> \033[1;31mVerification/register failed:', resp2)

        print('\033[1;34m' + '-'*40 + '\033[0m')
    except Exception as e:
        print('\033[1;31mError:', e)
        print('\033[1;34m' + '-'*40 + '\033[0m')

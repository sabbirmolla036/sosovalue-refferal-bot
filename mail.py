import names
import random
import string
import time
from bs4 import BeautifulSoup
import requests as curl_requests
from fake_useragent import UserAgent

def get_fake_chrome_ua():
    return UserAgent().chrome

def get_headers(token=None):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp',
        'priority': 'u=1, i',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': get_fake_chrome_ua()
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers

def get_random_domain():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    keyword = random.choice(consonants) + random.choice(vowels)
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = curl_requests.get(
                f'https://generator.email/search.php?key={keyword}',
                headers=get_headers(),
                timeout=15
            )
            domains = response.json()
            valid_domains = [d for d in domains if all(ord(c) < 128 for c in d)]
            
            if valid_domains:
                return random.choice(valid_domains)
        except Exception as e:
            print(f"[!] Domain fetch failed (attempt {attempt + 1}): {e}")
            time.sleep(1)

    return None

def generate_email(domain):
    first_name = names.get_first_name().lower()
    last_name = names.get_last_name().lower()
    random_nums = ''.join(random.choices(string.digits, k=3))
    separator = random.choice(['', '.'])
    return f"{first_name}{separator}{last_name}{random_nums}@{domain}"

def get_verification_link(email, domain):
    cookies = {
        'embx': f'["{email}"]',
        'surl': f'{domain}/{email.split("@")[0]}'
    }
    
    max_attempts = 15
    for attempt in range(max_attempts):
        try:
            response = curl_requests.get(
                'https://generator.email/inbox1/',
                headers=get_headers(),
                cookies=cookies,
                timeout=15
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            code = None
            try:
                code = str(soup).split('SoSoValue - ')[1].split(' ')[0]
            except IndexError:
                pass

            if code:
                return code
            
            time.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"[!] Email check failed (attempt {attempt + 1}): {e}")
            time.sleep(2)
    return None

def getmails():
    while True:
        domain = get_random_domain()
        if domain:
            email = generate_email(domain)
            print(f"[+] Generated Email: {email}")
            return email
        else:
            print("[!] Retrying domain fetch...")

# Example Usage:
if __name__ == "__main__":
    email = getmails()
    print(f"Generated Email: {email}")

import os
import shutil
import platform
import requests
import random
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser

logo = """

███████╗███████╗███╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
╚══███╔╝██╔════╝████╗  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
  ███╔╝ █████╗  ██╔██╗ ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
 ███╔╝  ██╔══╝  ██║╚██╗██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
███████╗███████╗██║ ╚████║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚══════╝╚══════╝╚═╝  ╚═══╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝

github: https://github.com/zen-Hikari
"""

logo2 = """

    __  ____  __              __  __               __              
   / / / / /_/ /_____        / / / /__  ____ _____/ /__  __________
  / /_/ / __/ __/ __ \______/ /_/ / _ \/ __ `/ __  / _ \/ ___/ ___/
 / __  / /_/ /_/ /_/ /_____/ __  /  __/ /_/ / /_/ /  __/ /  (__  ) 
/_/ /_/\__/\__/ .___/     /_/ /_/\___/\__,_/\__,_/\___/_/  /____/  
             /_/                                                   

"""

logo3 = """

   ___     __      _          _____         __       
  / _ |___/ /_ _  (_)__  ____/ __(_)__  ___/ /__ ____
 / __ / _  /  ' \/ / _ \/___/ _// / _ \/ _  / -_) __/
/_/ |_\_,_/_/_/_/_/_//_/   /_/ /_/_//_/\_,_/\__/_/   
                                                     

"""

logo4 = """

   ____     __      __                _      _____         __       
  / __/_ __/ /  ___/ /__  __ _  ___ _(_)__  / __(_)__  ___/ /__ ____
 _\ \/ // / _ \/ _  / _ \/  ' \/ _ `/ / _ \/ _// / _ \/ _  / -_) __/
/___/\_,_/_.__/\_,_/\___/_/_/_/\_,_/_/_//_/_/ /_/_//_/\_,_/\__/_/   
                                                                    

"""

logo5 = """

    __  ___     __    __           _______ __        _____                                 
   / / / (_)___/ /___/ /__  ____  / ____(_) /__     / ___/_________ _____  ____  ___  _____
  / /_/ / / __  / __  / _ \/ __ \/ /_  / / / _ \    \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / __  / / /_/ / /_/ /  __/ / / / __/ / / /  __/   ___/ / /__/ /_/ / / / / / / /  __/ /    
/_/ /_/_/\__,_/\__,_/\___/_/ /_/_/   /_/_/\___/   /____/\___/\__,_/_/ /_/_/ /_/\___/_/     
                                                                                           
"""

colors = [
    "\033[38;2;255;0;0m",
    "\033[38;2;255;40;0m",
    "\033[38;2;255;80;0m",
    "\033[38;2;255;120;0m",
    "\033[38;2;255;160;0m",
    "\033[38;2;255;200;0m",
    "\033[38;2;255;240;0m",
]

reset = '\033[0m'

cols = shutil.get_terminal_size().columns

def terminalClear():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

# MAIN MENU
while True:
    terminalClear()
    lines = logo.splitlines()
    color_idx = 0
    for line in lines:
        if "github:" in line:
            print(line.center(cols))
        else:
            color = colors[min(color_idx, len(colors) - 1)]
            print(f"{color}{line.center(cols)}{reset}")
            color_idx += 1

    print("""
    [1] Http Header
    [2] Admin Panel Finder (crawl-based)
    [3] Subdomain Scanner
    [4] Hidden File Scanner
    [0] Exit
    """)
    x = input('Options: ')
    if x == '0':
        print('Return Exit...')
        break

    elif x == '1':
        while True:
            terminalClear()
            lines2 = logo2.splitlines()
            color_idx = 0
            for line in lines2:
                color = colors[min(color_idx, len(colors) - 1)]
                print(f"{color}{line.center(cols)}{reset}")
                color_idx += 1

            url = input('Paste link Example(https://www.google.com/): ')
            try:
                response = requests.get(url)
                print('\nHttp Request:')
                for k, v in response.request.headers.items():
                    print(k, ':', v)
                print('\nHttp Headers')
                for k, v in response.headers.items():
                    print(k, ':', v)
            except Exception as e:
                print("Error:", e)

            returnTool = input('\npress 0 to return menu, press ENTER to another link: ')
            if returnTool == '0':
                break

    elif x == '2':
        while True:
            terminalClear()
            lines3 = logo3.splitlines()
            color_idx = 0
            for line in lines3:
                color = colors[min(color_idx, len(colors) - 1)]
                print(f"{color}{line.center(cols)}{reset}")
                color_idx += 1

            try:
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36"
                ]

                class LinkParser(HTMLParser):
                    def __init__(self, domain):
                        super().__init__()
                        self.links = set()
                        self.domain = domain
                    def handle_starttag(self, tag, attrs):
                        if tag == "a":
                            href = dict(attrs).get("href")
                            if href:
                                joined = urljoin(f"https://{self.domain}", href)
                                if urlparse(joined).netloc == self.domain:
                                    self.links.add(joined)

                class LoginFormParser(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.has_password = False
                        self.has_text_input = False
                    def handle_starttag(self, tag, attrs):
                        if tag == "input":
                            atype = dict(attrs).get("type", "").lower()
                            if atype == "password":
                                self.has_password = True
                            if atype in ["text", "email"]:
                                self.has_text_input = True
                    def is_login_form(self):
                        return self.has_password and self.has_text_input

                def has_login_form(url):
                    try:
                        headers = {"User-Agent": random.choice(user_agents)}
                        res = requests.get(url, headers=headers, timeout=5)
                        if res.status_code == 200:
                            parser = LoginFormParser()
                            parser.feed(res.text)
                            if parser.is_login_form():
                                return True
                    except:
                        pass
                    return False

                target = input("Target URL (e.g. https://example.com): ")
                if not target:
                    break

                parsed = urlparse(target)
                domain = parsed.netloc

                urls_to_scan = set()
                try:
                    headers = {"User-Agent": random.choice(user_agents)}
                    res = requests.get(target, headers=headers, timeout=5)
                    if res.status_code == 200:
                        parser = LinkParser(domain)
                        parser.feed(res.text)
                        urls_to_scan.update(parser.links)
                except:
                    pass

                urls_to_scan.add(target)

                found_urls = []
                with ThreadPoolExecutor(max_workers=15) as executor:
                    futures = {executor.submit(has_login_form, url): url for url in urls_to_scan}
                    for future in as_completed(futures):
                        result = future.result()
                        url_tested = futures[future]
                        if result:
                            found_urls.append(url_tested)
                            print(f"[+] Login form detected: {url_tested}")

                if found_urls:
                    with open("hasil_admin_finder.txt", "w") as f:
                        for url in found_urls:
                            f.write(url + "\n")
                    print("[*] Saved to hasil_admin_finder.txt")
                else:
                    print("[*] No login forms found.")

            except Exception as e:
                print('Error: ', e )

            ret = input("\npress 0 to return menu, press ENTER to scan another: ")
            if ret == '0':
                break

    elif x == '3':
        while True:
            terminalClear()
            lines4 = logo4.splitlines()
            color_idx = 0
            for line in lines4:
                color = colors[min(color_idx, len(colors) - 1)]
                print(f"{color}{line.center(cols)}{reset}")
                color_idx += 1

            def find_subdomain(domain, timeout=3):
                wordlist = [
                    "api", "admin", "login", "blog", "mail", "webmail", "secure", "test", "dev", "portal",
    "vpn", "beta", "shop", "support", "ftp", "cdn", "dashboard", "office", "intranet",
    "docs", "staging", "news", "static", "images", "files", "m", "mobile", "old", "new",
    "partners", "forum", "cloud", "gw", "ns1", "ns2", "status", "payments", "billing",
    "conference", "events", "devops", "git", "jira",
    "stg", "uat", "preprod", "demo", "backup", "gateway", "monitor", "metrics", "api2", "api3",
    "media", "logs", "web", "search", "beta2", "legacy", "cdn2", "secure2", "download", "upload"
                ]
                try:
                    for subdomain in wordlist:
                        url = f"http://{subdomain}.{domain}"
                        try:
                            response = requests.get(url, timeout=timeout)
                            status = response.status_code
                            print(f"{url} - {status}")
                        except requests.exceptions.RequestException:
                            pass

                        url = f"https://{subdomain}.{domain}"
                        try:
                            response = requests.get(url, timeout=timeout)
                            status = response.status_code
                            print(f"{url} - {status}")
                        except requests.exceptions.RequestException:
                            pass
                except KeyboardInterrupt:
                    print("\n[!] The scan was stopped by the user.\n")

            domain = input("Target domain (example: google.com): ").strip()
            if not domain:
                print("No domain given, returning to menu...")
                break

            timeout = 4
            find_subdomain(domain, timeout)

            ret = input("\npress 0 to return menu, press ENTER to scan another: ")
            if ret == '0':
                break

    elif x == '4':
        while True:
            terminalClear()
            lines4 = logo4.splitlines()
            color_idx = 0
            for line in lines4:
                color = colors[min(color_idx, len(colors) - 1)]
                print(f"{color}{line.center(cols)}{reset}")
                color_idx += 1

            directories = [
                 "robots", "password", "login", "config", "admin",
    ".env", ".git", ".htaccess", ".htpasswd", "backup", "old", "dev", "test", "private", "secret",
    "db", "database", "dump", "api", "api/v1", "logs", "uploads", "uploads/images"  
            ]

            url = input("Target Domain (example: https://google.com): ")
            try:
                for directori in directories:
                    try:
                        req_url = url + directori
                        response = requests.get(req_url)
                        status = response.status_code
                        print(f"{url}{directori} - {status}")
                    except requests.exceptions.RequestException:
                        print(f"[!] failed to load {req_url} - make sure the URL format is correct")
            except KeyboardInterrupt:
                print("\n[!] The scan was stopped by the user.\n")

            res = input("\npress 0 to return menu, press ENTER to scan another: ")
            if res == '0':
                break   

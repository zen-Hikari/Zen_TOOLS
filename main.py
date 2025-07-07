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
            for line in logo2.splitlines():
                print(line.center(cols))
            url = input('Paste link Example(https://www.google.com/): ')
            try:
                response = requests.get(url)
                print('\nHttp Request:')
                for k, v in response.request.headers.items():
                    print(k, ':', v)
                print('\nHttp Headers:')
                for k, v in response.headers.items():
                    print(k, ':', v)
            except Exception as e:
                print("Error:", e)
            if input('\npress 0 to return menu, ENTER to repeat: ') == '0':
                break

    elif x == '2':
        while True:
            terminalClear()
            for line in logo3.splitlines():
                print(line.center(cols))
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
                        if future.result():
                            url_tested = futures[future]
                            found_urls.append(url_tested)
                            print(f"[+] Login form detected: {url_tested}")
                if found_urls:
                    with open("hasil_admin_finder.txt", "w") as f:
                        for u in found_urls:
                            f.write(u + "\n")
                    print("[*] Saved to hasil_admin_finder.txt")
                else:
                    print("[*] No login forms found.")
            except Exception as e:
                print("Error: ", e)
            if input('\npress 0 to return menu, ENTER to repeat: ') == '0':
                break

    elif x == '3':
        while True:
            terminalClear()
            for line in logo4.splitlines():
                print(line.center(cols))
            def find_subdomain(domain, timeout=3):
                wordlist = [
                    "api", "admin", "login", "blog", "mail", "webmail", "secure", "test", "dev", "portal",
                    "vpn", "beta", "shop", "support", "ftp", "cdn", "dashboard", "office", "intranet",
                    "docs", "staging", "news", "static", "images", "files", "m", "mobile", "old", "new",
                    "partners", "forum", "cloud", "gw", "ns1", "ns2", "status", "payments", "billing",
                    "conference", "events", "devops", "git", "jira", "stg", "uat", "preprod", "demo", "backup",
                    "gateway", "monitor", "metrics", "api2", "api3", "media", "logs", "web", "search", "beta2",
                    "legacy", "cdn2", "secure2", "download", "upload", "vps", "node", "payment", "sso", "social",
                    "auth", "forum2", "img", "cdn3", "stage", "sandbox", "api4", "files2", "secure3", "exchange",
                    "gateway2", "redis", "mysql", "mongo", "kibana", "grafana", "elasticsearch", "logstash",
                    "influxdb", "jenkins", "prometheus", "ci", "cd", "pipelines", "metrics2", "push", "pull",
                    "origin", "gitlab", "bitbucket", "jira2", "tickets", "assets", "proxy", "bastion", "mail2",
                    "mail3", "imap", "smtp", "pop", "pbx", "sip", "voip", "edge", "dmz", "mirror", "mirror2",
                    "cache", "backup2", "backup3", "archive", "legacy2", "internal", "core", "test2", "dev2",
                    "qa", "qa2", "perf", "stress", "uat2", "trial", "demo2", "new2", "old2"
                ]
                try:
                    for sub in wordlist:
                        for proto in ['http', 'https']:
                            url = f"{proto}://{sub}.{domain}"
                            try:
                                r = requests.get(url, timeout=timeout)
                                print(f"{url} - {r.status_code}")
                            except:
                                pass
                except KeyboardInterrupt:
                    print("\n[!] Stopped by user.\n")
            domain = input("Target domain (e.g. google.com): ").strip()
            if not domain:
                break
            find_subdomain(domain)
            if input('\npress 0 to return menu, ENTER to repeat: ') == '0':
                break

    elif x == '4':
        while True:
            terminalClear()
            for line in logo4.splitlines():
                print(line.center(cols))
            directories = [
                "robots", "password", "login", "config", "admin", ".env", ".git", ".htaccess", ".htpasswd",
                "backup", "old", "dev", "test", "private", "secret", "db", "database", "dump", "api",
                "api/v1", "logs", "uploads", "uploads/images", "uploads/files", "uploads/videos",
                "uploads/backups", "storage", "tmp", "temp", "old_site", "beta", "alpha", "cron",
                "cronjobs", "jobs", "scripts", "cgi-bin", "wp-admin", "wp-login", "wordpress", "drupal",
                "joomla", "laravel", "vendor", "node_modules", "composer.json", "package.json",
                "yarn.lock", "docker-compose.yml", "dockerfile", "build", "builds", "dist", "release",
                "releases", "core", "system", "system32", "conf", "cfg", "sql", "sql_dump", "pgsql", "mysql",
                "backup_old", "backup_2022", "backup_2023", "backup_2024", "test_backup"
            ]
            url = input("Target domain (example: https://google.com/): ")
            try:
                for d in directories:
                    req_url = url.rstrip("/") + "/" + d
                    try:
                        r = requests.get(req_url)
                        print(f"{req_url} - {r.status_code}")
                    except:
                        print(f"[!] Failed: {req_url}")
            except KeyboardInterrupt:
                print("\n[!] Stopped by user.\n")
            if input('\npress 0 to return menu, ENTER to repeat: ') == '0':
                break

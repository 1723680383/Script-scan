import requests
from urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style

# 定义ANSI颜色代码
class Color:
    GREEN = "\\033[92m"
    RESET = "\\033[0m"

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 设置全局默认最大重试次数和超时时间
def set_request_defaults():
    requests.adapters.DEFAULT_RETRIES = 1
    requests.adapters.DEFAULT_TIMEOUT = 3

# 图标
def print_banner():
    with open("banner.txt", "r") as file:
        content = file.read()
        colored_content = f"{Fore.GREEN}{content}{Style.RESET_ALL}"
        print(colored_content)
def print_help():
    with open("help.txt", "r", encoding='utf-8') as file:
        content = file.read()
        colored_content = content
        print(colored_content)

custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "",
        "Te": "trailers",
        "Connection": "close",
        "cookie":"TWFID=d2c3d09c522ed63e; ",
    }
import argparse
import config
import sys  # 添加这行导入语句
import create_process
from colorama import Fore, Style
from config import set_request_defaults, print_banner

# 使用 argparse 定义命令行参数和帮助信息
parser = argparse.ArgumentParser(description="script-scan  (by 叫我十一大人)")
parser.add_argument("-u", "--url", help="扫描单个URL")
parser.add_argument("-f", "--file", help="从文本文件扫描URL")
parser.add_argument("-p", "--proxy", help="使用代理，格式如 http://127.0.0.1:8080")
parser.add_argument('-c', '--cpu', help='设置多核cpu使用上限')
args = parser.parse_args()

if __name__ == "__main__":
    print_banner()
    set_request_defaults()

    if args.url:
        url_to_scan = args.url
        create_process.start([url_to_scan], proxy=args.proxy, max_cpu=args.cpu)
    elif args.file:
        with open(args.file, 'r') as file:
            target_urls = [i for i in file.read().splitlines() if i.startswith('http')]
        create_process.start(target_urls, proxy=args.proxy, max_cpu=args.cpu)
    else:
        # 如果没有提供参数，打印帮助信息
        parser.print_help()
        config.print_help()
        sys.exit(1)

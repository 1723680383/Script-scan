import os
import sys
import js_finder
from tqdm import tqdm
from colorama import Fore, Style
from config import Color
from http_requests import send_http_request

# 固定的主目录路径
main_paths = [
    '/Content/',
    '/scripts/',
    '/js/',
    '/public/',
    '/kindeditor/',
    '/ueditor/',
    '/fckeditor/',
    '/pub/',
    'assets'
]

# 创建一个结果文件
result_file = open('result.txt', 'w')

# 子路径文件夹
path_files_folder = 'path_files'

def scan_urls(scan_urls):
    # 遍历URL
    for url in tqdm(scan_urls, desc="进度"):
        print(url)
        response = send_http_request(url, verify=False, timeout=2)
        if response and response.status_code == 200:
            for main_path in main_paths:
                subpath_file = os.path.join(path_files_folder, main_path.lstrip('/') + '_paths.txt')
                if not os.path.exists(subpath_file):
                    print("子路径文件不存在:", subpath_file)
                    continue
                try:
                    with open(subpath_file, 'r') as file:
                        sub_paths = file.read().splitlines()
                except FileNotFoundError:
                    # 如果子路径文件不存在，跳过当前主目录
                    continue
                main_path_found = False  # 标记是否发现主目录的状态码为200或403
                target_url = url + main_path
                try:
                    response = send_http_request(target_url, verify=False, timeout=3)
                    if response.status_code in [200, 403]:
                        main_path_found = True
                        if response.status_code == 200:
                            if "To Parent Directory" in response.text:
                                result_file.write(f"URL: {target_url}, 状态码: 200\n")
                                print(target_url)
                                print(f"{Fore.GREEN}目录遍历漏洞存在！！{Style.RESET_ALL}")
                        if response.status_code == 403:
                            print(target_url)
                            print("目录存在，将进行组件爆破！！")    
                except Exception as e:
                    sys.stdout.flush()  # 刷新输出
                if main_path_found:
                    # 只有在主目录的状态码为200或403时才检查对应的子路径
                    for sub_path in sub_paths:
                        target_url = url + main_path + sub_path
                        try:
                            response = send_http_request(target_url, verify=False, timeout=5)
                            if response.status_code == 302:
                                # 如果状态码为302，跳过当前URL
                                print(f"URL: {target_url}, 状态码: 302 - 跳过")
                                break
                            if response.status_code == 200:
                                if "没有指定抓取源" in response.text:
                                    result_file.write(f"URL: {target_url}, 状态码: 200, 响应: 1.4.3\n")
                                    print(f"URL: {target_url}, 状态码: 200, 响应: 1.4.3\n")
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.4.3{Style.RESET_ALL}")
                                if "state" in response.text and "未知错误" in response.text:
                                    result_file.write(f"URL: {target_url}, 状态码: 200, 响应: 1.3.6\n")
                                    print(f"URL: {target_url}, 状态码: 200, 响应: 1.3.6\n")
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.3.6{Style.RESET_ALL}")
                                if '"message"' in response.text:
                                    result_file.write(f"URL: {target_url}, 状态码: 200, 响应: true\n")
                                    print(f"URL: {target_url}, 状态码: 200, 响应: 爆破成功！！！\n")
                                    print(f"{Fore.GREEN}Kindeditor 漏洞存在！！{Style.RESET_ALL}")
                                if 'File Uploader' in response.text:
                                    print(f"URL: {target_url}, 状态码: 200, 响应: 版本未知\n")
                                    result_file.write(f"URL: {target_url}, 状态码: 200, 响应: true\n")
                                    print(f"{Fore.GREEN}Fckeditor 编辑器存在！！{Style.RESET_ALL}")
                            elif response.status_code == 403:
                                if "403 - 禁止访问: 访问被拒绝" in response.text:
                                    print(f"URL: {target_url}, 状态码: 403")
                                    print("目录存在，可能有其他第三方插件，请手动测试")
                            elif response.status_code == 400 and target_url.startswith('https://'):
                                print("协议错误，跳过!!!")
                            sys.stdout.flush()  # 刷新输出
                        except Exception as e:
                            sys.stdout.flush()  # 刷新输出
        if response.status_code == 404 :
                print("常见目录不存在，开始获取网站JS目录")
                js_finder.get_js_paths(url)
                            # 继续检测
                with open('js_separated.txt', 'r') as js_file:
                    js_paths = js_file.read().splitlines()
                with open('payload.txt', 'r') as payload_file:
                    payloads = payload_file.read().splitlines()

                for js_path in js_paths:
                    for payload in payloads:
                        complete_url = url + js_path + payload
                        print(complete_url)
                        response = send_http_request(complete_url, verify=False, timeout=5)
                        print(response)
                        if response.status_code == 302:
                            # 如果状态码为302，跳过当前URL
                            print(f"URL: {complete_url}, 状态码: 302 - 跳过")
                            break
                        if response.status_code == 200:
                            if "没有指定抓取源" in response.text:
                                result_file.write(f"URL: {complete_url}, 状态码: 200, 响应: 1.4.3\n")
                                print(f"URL: {complete_url}, 状态码: 200, 响应: 1.4.3\n")
                                print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.4.3{Style.RESET_ALL}")
                                if "state" in response.text and "未知错误" in response.text:
                                    result_file.write(f"URL: {complete_url}, 状态码: 200, 响应: 1.3.6\n")
                                    print(f"URL: {complete_url}, 状态码: 200, 响应: 1.3.6\n")
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.3.6{Style.RESET_ALL}")
                                if '"message"' in response.text:
                                    result_file.write(f"URL: {complete_url}, 状态码: 200, 响应: true\n")
                                    print(f"URL: {complete_url}, 状态码: 200, 响应: 爆破成功！！！\n")
                                    print(f"{Fore.GREEN}Kindeditor 漏洞存在！！{Style.RESET_ALL}")
                                if 'File Uploader' in response.text:
                                    print(f"URL: {complete_url}, 状态码: 200, 响应: 版本未知\n")
                                    result_file.write(f"URL: {complete_url}, 状态码: 200, 响应: true\n")
                                    print(f"{Fore.GREEN}Fckeditor 编辑器存在！！{Style.RESET_ALL}")
                                elif response.status_code == 403:
                                    if "403 - 禁止访问: 访问被拒绝" in response.text:
                                        print(f"URL: {complete_url}, 状态码: 403")
                                        print("目录存在，可能有其他第三方插件，请手动测试")
                                elif response.status_code == 400 and complete_url.startswith('https://'):
                                    print("协议错误，跳过!!!")
                                    sys.stdout.flush()  # 刷新输出
    result_file.close()

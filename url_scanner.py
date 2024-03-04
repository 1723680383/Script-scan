import os
import sys
import js_finder
import config
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style
from config import Color
from http_requests import send_http_request

# 固定的主目录路径
main_paths = [
    '/kindeditor/',
    '/ueditor/',
    '/fckeditor/',
    '/ckeditor/',
    '/ckfinder/',
    '/Editor/',
    '/CuteSoft_Client/',
    '/Content/',
    '/scripts/',
    '/js/',
    '/public/',
    '/Library/',
    '/pub/',
    '/web/',
    '/assets/',
    '/plugins/',
    '/lib/',
    '/RTE/',
    '/plus/',
    '/skin/',
    '/resource/',
    '/Plugs/'
]

# 子路径文件夹
path_files_folder = 'path_files'

def scan_urls(url, proxy=None) -> str:
    res:list[str] = ['='*120 + '\n']
    try:
        print("正在测试URL:"+url+"\n")
        global_main_paths_not_found = True
        response = send_http_request(url, verify=False, timeout=5, headers=config.custom_headers, proxy=proxy)  # 传递代理参数
        if response is None:# 直接跳过
            print(f'{Fore.RED}响应错误,跳过该站点({url}){Fore.RESET}')
            return ['']
        if response.status_code == 200:
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
                #print(target_url)
                try:
                    response = send_http_request(target_url, verify=False, timeout=5, headers=config.custom_headers, proxy=proxy)
                    if response is None:
                        print(f'{Fore.RED}响应错误,跳过该站点({target_url}){Fore.RESET}')
                        break
                    if response.status_code in [200, 403]:
                        main_path_found = True
                        if response.status_code == 200:
                            #global_main_paths_not_found  = 0（找不到常见目录才爬取JS）
                            if "To Parent Directory" in response.text:
                                res.append(f"[+] [{target_url}] 状态码: 200 目录遍历漏洞存在！！\n")
                                print(f"{Fore.GREEN}目录遍历漏洞存在！！({target_url}){Style.RESET_ALL}")
                            elif "转到父目录" in response.text:
                                res.append(f"[+] [{target_url}] 状态码: 200 目录遍历漏洞存在！！\n")
                                print(f"{Fore.GREEN}目录遍历漏洞存在！！({target_url}){Style.RESET_ALL}")
                        elif response.status_code == 403:
                            #global_main_paths_not_found  = 0（找不到常见目录才爬取JS）
                            print(target_url)
                            print(f"目录存在，将进行组件爆破！！({target_url})")  
                except KeyboardInterrupt:
                    raise#丢到外层
                except Exception as e:
                    sys.stdout.flush()  # 刷新输出
                if main_path_found:
                    # 只有在主目录的状态码为200或403时才检查对应的子路径
                    for sub_path in sub_paths:
                        target_url = url + main_path + sub_path
                        try:
                            response = send_http_request(target_url, verify=False, timeout=5, headers=config.custom_headers, proxy=proxy)
                            #print(response.status_code)  # 输出状态码
                            #print(response.headers)  # 输出头部信息
                            #print(response.text)  # 输出响应体的内容
                            if response is None:
                                print(f'{Fore.RED}响应错误,跳过该站点({target_url}){Fore.RESET}')
                                break
                            if response.status_code == 302:
                                # 如果状态码为302，跳过当前URL
                                print(f"[+] [{target_url}] 状态码: 302 - 跳过")
                                break
                            if response.status_code == 200:
                                #查找Ueditor
                                if "没有指定抓取源" in response.text:
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: 1.4.3    Ueditor 漏洞存在！！版本为 - 1.4.3\n")
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: 1.4.3\n")
                                    global_main_paths_not_found  = False 
                                    #找到了编辑器就不用继续爬取
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.4.3({target_url}){Style.RESET_ALL}")

                                #查找Ueditor
                                if "state" in response.text and "未知错误" in response.text:
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: 1.3.6    Ueditor 漏洞存在！！版本为 - 1.3.6\n")
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: 1.3.6\n")
                                    global_main_paths_not_found  = False
                                    #找到了编辑器就不用继续爬取
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.3.6({target_url}){Style.RESET_ALL}")

                                #查找Kindeditor
                                if '"message"' in response.text and "UEditor" not in response.text :
                                    if "documentElement" not in response.text:                                 
                                        res.append(f"[+] [{target_url}] 状态码: 200, 响应: true Kindeditor 漏洞存在！！\n")
                                        print(f"[+] [{target_url}] 状态码: 200, 响应: 爆破成功！！！\n")
                                        print(f"{Fore.GREEN}Kindeditor 漏洞存在！！({target_url}){Style.RESET_ALL}")

                                #查找Fckeditor
                                if 'File Uploader' in response.text:
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: 版本未知  Fckeditor 编辑器存在！！\n")
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: true\n")
                                    global_main_paths_not_found  = False
                                    #找到了编辑器就不用继续爬取
                                    print(f"{Fore.GREEN}Fckeditor 编辑器存在！！({target_url}){Style.RESET_ALL}")

                                #查找Ueditor
                                if "UEditor" in response.text:
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: Ueditor.all.min.js文件存在   Ueditor配置文件存在，请手动确认是否为变种！！！\n")
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: Ueditor.all.min.js文件存在\n")
                                    print(f"{Fore.GREEN}Ueditor配置文件存在，请手动确认是否为变种！！！({target_url}){Style.RESET_ALL}")
                                    global_main_paths_not_found  = False    

                                #查找CKfinder
                                if "CKFinder.version" in response.text:
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: CKFinder.js文件存在  CKFinder配置文件存在，请手动寻找上传位置！！！\n")
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: CKFinder.js文件存在\n")
                                    print(f"{Fore.GREEN}CKFinder配置文件存在，请手动寻找上传位置！！！({target_url}){Style.RESET_ALL}")

                                #查找CuteEditor
                                if "<configuration>" in response.text:
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: CuteEdito本地包含漏洞存在    CuteEdito本地包含漏洞存在，成功读取到web.config的内容\n")
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: CuteEdito本地包含漏洞存在\n")
                                    print(f"{Fore.GREEN}CuteEdito本地包含漏洞存在，成功读取到web.config的内容({target_url}){Style.RESET_ALL}")
                                    global_main_paths_not_found  = False 

                                #查找Ckeditor
                                if "ckeditor.com" in response.text:
                                    res.append(f"[+] [{target_url}] 状态码: 200, 响应: ckeditor.js文件存在  Ckeditor配置文件存在，请手动寻找上传位置！！！\n")
                                    print(f"[+] [{target_url}] 状态码: 200, 响应: ckeditor.js文件存在\n")
                                    print(f"{Fore.GREEN}Ckeditor配置文件存在，请手动寻找上传位置！！！({target_url}){Style.RESET_ALL}")       
                            elif response.status_code == 400 and target_url.startswith('https://'):
                                print("协议错误，跳过!!!")
                            sys.stdout.flush()  # 刷新输出
                        except Exception as e:
                            sys.stdout.flush()  # 刷新输出
            #没有爆破到主目录并且响应状态码不为空                
            if global_main_paths_not_found:
                print("正在爬取获取网站JS目录再次爆破")
                res.appendjs_finder.get_js_paths(url, proxy=proxy)  # 传递代理参数
                # 继续检测
                with open('js_separated.txt', 'r') as js_file:
                    js_paths = js_file.read().splitlines()
                with open('payload.txt', 'r') as payload_file:
                    payloads = payload_file.read().splitlines()
                skip = False
                for js_path in js_paths:
                    if skip:
                        break
                    for payload in payloads:
                        complete_url = url + js_path + payload
                        response = send_http_request(complete_url, verify=False, timeout=5, headers=config.custom_headers, proxy=proxy)
                        if response is None:
                            print(f'{Fore.RED}响应错误,跳过该站点({complete_url}){Fore.RESET}')
                            skip = True
                            break
                        try:
                            if response.status_code == 200:
                                #查找Ueditor
                                if "没有指定抓取源" in response.text:
                                    res.append(f"[+] [{complete_url}] 状态码: 200, 响应: 1.4.3  Ueditor 漏洞存在！！版本为 - 1.4.3\n")
                                    print(f"[+] [{complete_url}] 状态码: 200, 响应: 1.4.3\n")
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.4.3({complete_url}){Style.RESET_ALL}")

                                #查找Ueditor
                                if "state" in response.text and "未知错误" in response.text:
                                    res.append(f"[+] [{complete_url}] 状态码: 200, 响应: 1.3.6  Ueditor 漏洞存在！！版本为 - 1.3.6\n")
                                    print(f"[+] [{complete_url}] 状态码: 200, 响应: 1.3.6\n")
                                    print(f"{Fore.GREEN}Ueditor 漏洞存在！！版本为 - 1.3.6({complete_url}){Style.RESET_ALL}")

                                #查找Kindeditor
                                if '"message"' in response.text and "UEditor" not in response.text:
                                    if "documentElement" not in response.text:    
                                        res.append(f"[+] [{complete_url}] 状态码: 200, 响应: true   Kindeditor 漏洞存在！！\n")
                                        print(f"[+] [{complete_url}] 状态码: 200, 响应: 爆破成功！！！\n")
                                        print(f"{Fore.GREEN}Kindeditor 漏洞存在！！({complete_url}){Style.RESET_ALL}")

                                #查找Ueditor
                                if "UEditor" in response.text:
                                    res.append(f"[+] [{complete_url}] 状态码: 200, 响应: Ueditor.all.min.js文件存在 Ueditor配置文件存在，请手动确认是否为变种！！！\n")
                                    print(f"[+] [{complete_url}] 状态码: 200, 响应: Ueditor.all.min.js文件存在\n")
                                    print(f"{Fore.GREEN}Ueditor配置文件存在，请手动确认是否为变种！！！({complete_url}){Style.RESET_ALL}")

                                #查找CKfinder
                                if "CKFinder.version" in response.text:
                                    res.append(f"[+] [{complete_url}] 状态码: 200, 响应: CKFinder.js文件存在  CKFinder配置文件存在，请手动寻找上传位置！！！\n")
                                    print(f"[+] [{complete_url}] 状态码: 200, 响应: CKFinder.js文件存在\n")
                                    print(f"{Fore.GREEN}CKFinder配置文件存在，请手动寻找上传位置！！！({complete_url}){Style.RESET_ALL}")

                                #查找Fckeditor
                                if 'File Uploader' in response.text:
                                    res.append(f"[+] [{complete_url}] 状态码: 200, 响应: true   Fckeditor 编辑器存在！！\n")
                                    print(f"[+] [{complete_url}] 状态码: 200, 响应: 版本未知\n")
                                    print(f"{Fore.GREEN}Fckeditor 编辑器存在！！({complete_url}){Style.RESET_ALL}")

                                #查找Ckeditor
                                if "ckeditor.com" in response.text:
                                    res.append(f"[+] [{complete_url}] 状态码: 200, 响应: ckeditor.js文件存在    Ckeditor配置文件存在，请手动寻找上传位置！！！\n")
                                    print(f"[+] [{complete_url}] 状态码: 200, 响应: ckeditor.js文件存在\n")
                                    print(f"{Fore.GREEN}Ckeditor配置文件存在，请手动寻找上传位置！！！({complete_url}){Style.RESET_ALL}")
                                    global_main_paths_not_found  = False      

                            elif response == 403:
                                if "403 - 禁止访问: 访问被拒绝" in response.text:
                                    print(f"[+] [{complete_url}] 状态码: 403")
                                    print(f"目录存在，可能有其他第三方插件，请手动测试({complete_url})")
                            elif response == 400 and complete_url.startswith('https://'):
                                    print(f"协议错误，跳过!!!({complete_url})")
                                    sys.stdout.flush()  # 刷新输出
                        except AttributeError:
                            print(f"请求错误: {complete_url}")
                global_main_paths_not_found = True
    finally:
        return res
import requests
import os
from bs4 import BeautifulSoup
from config import Color
from colorama import Fore, Style
from urllib.parse import urlparse, urljoin
import findinfo
import config

# 定义JS文件规则列表
js_rules = [
    "config",
    "JWT",
    "admin",
    "editor",
    "net",
    "Admin",
    "register",
    "Register",
    "login"
    # 添加更多规则
]

# 确保目标目录存在
js_dir = os.path.join('findinfo', 'js')
os.makedirs(js_dir, exist_ok=True)

# 设置控制目录级别的变量
max_directory_levels = 5

def delete_files_in_js_directory():
    findinfo_directory = os.path.join(os.getcwd(), 'findinfo')  # 获取findinfo目录的路径
    js_directory = os.path.join(findinfo_directory, 'JS')  # 构建JS目录的路径

    try:
        # 检查JS目录是否存在
        if os.path.exists(js_directory):
            # 删除JS目录中的所有文件
            for file_name in os.listdir(js_directory):
                file_path = os.path.join(js_directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            print('在 findinfo 目录中未找到 "JS" 目录。')
    except Exception as e:
        print(f'发生错误：{e}')


def save_js_file(base_url, js_path):
    try:
        # 获取JS文件内容
        js_url = urljoin(base_url, js_path)
        js_response = requests.get(js_url, verify=True, timeout=2,headers=config.custom_headers)
        js_response.raise_for_status()
        js_content = js_response.content  # 使用content获取二进制数据

        # 提取JS文件名
        js_filename = os.path.basename(js_path)

        # 构造保存路径
        save_path = os.path.join('findinfo', 'js', js_filename)

        # 保存JS文件
        with open(save_path, 'wb') as js_file:  # 使用二进制模式保存
            js_file.write(js_content)
    except Exception as e:
        print(f"保存JS文件时发生错误")


def get_js_paths(url, proxy=None) -> str:
    try:
        res = ''
        # 发送GET请求获取网页内容
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, verify=False, headers=config.custom_headers, timeout=5, proxies=proxies)  # 添加代理支持
        response.raise_for_status()

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取主机名
        host = urlparse(url).hostname

        # 提取每个script标签中的 src 属性
        js_paths = [tag.get('src') for tag in soup.find_all('script')]

        # 过滤JavaScript文件的路径并提取文件路径部分
        filtered_js_paths = []
        outputted_dirs = set()  # 存储已输出的不匹配目录路径

        for path in js_paths:
            if not path:
                continue
            if not urlparse(path).hostname:
                # 处理相对路径
                path = urljoin(url, path)
            if urlparse(path).hostname == host:
                # 提取文件路径部分
                path = urlparse(path).path
                filtered_js_paths.append(path)

        # 逐个分离不匹配的JavaScript目录路径
        separated_dirs = set()
        for path in filtered_js_paths:
            directory_parts = path.split('/')
            for i in range(1, min(max_directory_levels + 1, len(directory_parts) - 1)):
                subpath = '/'.join(directory_parts[:i+1]) + '/'
                separated_dirs.add(subpath)

        # 打印所有JavaScript文件的路径
        for path in filtered_js_paths:
            matching_rule = None
            for rule in js_rules:
                if rule in path:
                    matching_rule = rule
                    break

            if matching_rule:
                print(f"JavaScript文件路径:", url + path)
                print(f"{Fore.GREEN}发现匹配规则的敏感JS文件\n{Style.RESET_ALL}")

            else:
                print("目标JS文件:", path)
            # 保存JS文件到目标目录
            save_js_file(url, path)

        # 将逐个分离的不匹配的JavaScript目录路径写入文件
        path = '\n'.join(i for i in separated_dirs)
        with open('js_separated.txt', 'w', encoding='utf-8') as file:
            file.write(path)

    except requests.exceptions.RequestException as e:
        print(f"请求错误:{e}")
    except requests.exceptions.SSLError as e:
        print("SSL/TLS错误:")
        # 在此处可以添加特定的处理逻辑
    except ValueError as e:
        if "check_hostname requires server_hostname" in str(e):
            print("SSL证书错误：缺少服务器主机名")
        else:
            print("发生其他值错误:")
    except Exception as e:
        print("发生其他错误:")
    
    # 继续执行其他操作
    #提取敏感信息
    print("正在提取JS文件中加载的敏感信息")
    vars = findinfo.scan_findinfo()
    if len(vars) != 0:
        res = '-'*30 + f'\n{url+"的敏感文件":^30}\n' + '-'*30 + '\n' + '\n'.join(vars) + '\n'
    #删除js目录下的所有文件，保证网站JS文件唯一
    delete_files_in_js_directory()
    print("正在提取JS文件路径进行爆破")
    return res
if __name__ == "__main__":
    url = input("请输入网站的URL: ")
    #proxy = input("请输入代理地址（格式如 http://127.0.0.1:8080）: ")
    with open('res.txt','w') as file:
        get_js_paths(url,res_file=file)





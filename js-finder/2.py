import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# 定义JS文件规则列表
js_rules = [
    "RSA.js",
    # 添加更多规则
]

# 设置控制目录级别的变量
max_directory_levels = 4

def get_js_paths(url):
    try:
        # 发送GET请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取主机名
        host = urlparse(url).hostname

        # 提取每个script标签中的src属性
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

        # 打印所有JavaScript文件的路径
        for path in filtered_js_paths:
            # 检查是否在JS文件规则列表中
            matching_rule = None
            for rule in js_rules:
                if rule in path:
                    matching_rule = rule
                    break

            if matching_rule:
                print("JavaScript文件路径:", path)
                print("发现匹配的规则:", matching_rule)
            else:
                # 修改部分，限制不匹配的JavaScript目录路径的最多指定级别
                directory_parts = path.split('/')[:-1]
                if len(directory_parts) > max_directory_levels:
                    directory_parts = directory_parts[:max_directory_levels]
                directory_path = '/'.join(directory_parts) + '/'
                if directory_path not in outputted_dirs:
                    print("不匹配的JavaScript目录路径:", directory_path)
                    outputted_dirs.add(directory_path)

    except requests.exceptions.RequestException as e:
        print("请求错误:", e)
    except Exception as e:
        print("发生错误:", e)

if __name__ == "__main__":
    url = input("请输入网站的URL: ")
    get_js_paths(url)

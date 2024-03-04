# 打开文件
with open('test.txt', 'r') as file:
    # 读取文件内容
    lines = file.readlines()

# 过滤指定IP的URL
filtered_urls = []
for line in lines:
    url = line.strip()  # 去掉行尾的换行符
    if 'webvpn.gxnu.edu.cn' not in url:
        filtered_urls.append(url)

# 将过滤后的URL写入新文件
with open('filtered_urls.txt', 'w') as file:
    for url in filtered_urls:
        file.write(url + '\n')
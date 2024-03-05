# 简介

> 本项目是针对于ASP.NET的站点的第三方编辑器扫描器，同时还能检测目录遍历漏洞和JS文件中敏感信息的提取。


目前支持扫描的编辑器插件：
kindeditor  Ueditor  Fckeditor  Ckeditor  Ckfinder  Cuteditor

最新版本支持的功能如下：

- [x] **单个URL扫描：** 参数 -u 对单个URL进行扫描
- [x] **单多URL扫描：** 参数 -f 从txt文件中提取URL进行批量扫描
- [x] **添加扫描代理：** 参数 -p 添加代理后进行扫描
- [x] **支持多进程扫描：** 参数 -c 设置多进程数量
- [x] **提取JS中的敏感信息：** 参数 -find 启动findinfo模块，提取JS文件中的敏感信息

# 演示
运行主界面
python main.py
![微信截图_20240305140816](https://github.com/1723680383/script-scan/assets/120783630/669050f2-c889-40c3-9889-51172ff34452)
扫描单个URL
![2](https://github.com/1723680383/script-scan/assets/120783630/2bdfad72-3288-40d5-84ba-84709178efc1)


# 更新日志

>**2023.3.4：** [v1.0版本]



# 运行环境

支持 Linux、MacOS、Windows 系统，同时需安装 `Python`。
> 建议Python版本在 3.10. 以后



## 联系


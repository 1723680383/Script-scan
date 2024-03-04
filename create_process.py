#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author  : Hatanezumi
@Contact : Hatanezumi@chunshengserver.cn
@Desc    : 本部分是对任务进行多进程的调配
'''
import os
import url_scanner
import multiprocessing
from pathlib import Path
from colorama import Fore, Style
from tqdm import tqdm

class Scanner():
    def __init__(self, urls:list[str], proxy:str|None, max_cpu:int|None, force_cpu:int|None) -> None:
        self.urls = urls
        self.total = len(urls)
        self.finish = 0
        self.proxy = proxy
        self.max_cpu = max_cpu
        self.force_cpu = force_cpu
        self.res_file_path = Path('result.txt')
    def worker(self,args:tuple[str,str]) -> str:
        return url_scanner.scan_urls(args[0],args[1])
    def start(self) -> None:
        cpu_count = multiprocessing.cpu_count()
        cpu_count *= 5
        cpu_count = self.max_cpu if self.max_cpu is not None and self.max_cpu <= cpu_count * 5 else cpu_count
        cpu_count = self.force_cpu if self.force_cpu is not None else cpu_count
        try:
            with multiprocessing.Pool(cpu_count) as pool:
                res_list = pool.imap_unordered(self.worker,[(i,self.proxy) for i in self.urls])
                for res in tqdm(res_list, total=self.total, desc='当前进度'):
                    self.finish += 1
                    os.system(f'title 当前进度:{self.finish}/{self.total}')
                    res_text = ''.join(res) if len(res) != 1 else ''
                    with open(self.res_file_path,'a',encoding='utf-8') as file:
                        file.write(res_text)
        except KeyboardInterrupt:
            print(f'{Fore.GREEN}程序被终止,结果已保存到{self.res_file_path}{Fore.RESET}')
            os.system('pause')

def start(urls:list[str], proxy:str|None, max_cpu:str|None, force_cpu:str|None) -> None:
    max_cpu = int(max_cpu) if max_cpu is not None else None
    force_cpu = int(force_cpu) if force_cpu is not None else None
    scanner = Scanner(urls,proxy=proxy,max_cpu=max_cpu,force_cpu=force_cpu)
    scanner.start()
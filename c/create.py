#!/usr/bin/env python3

import os
import re
import shutil

def main():
    current_dir = os.getcwd()
    
    # 匹配 demo 或 demo+数字
    pattern = re.compile(r'^demo(\d*)$')
    
    demo_dirs = []
    for d in os.listdir(current_dir):
        if os.path.isdir(d):
            m = pattern.match(d)
            if m:
                num_str = m.group(1)
                num = int(num_str) if num_str else 0  # 没有数字当 0
                demo_dirs.append(num)
    
    if not demo_dirs:
        print("当前目录下没有符合条件的 demo 目录")
        return
    
    max_num = max(demo_dirs)
    new_num = max_num + 1
    
    src_dir = "demo"
    dst_dir = "demo" + str(new_num)
    
    # 创建新目录
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    # 手动递归复制 (因为 Python3.5 的 copytree 不能覆盖)
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dst_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    
    print("已复制 {} 到 {}".format(src_dir, dst_dir))

if __name__ == "__main__":
    main()

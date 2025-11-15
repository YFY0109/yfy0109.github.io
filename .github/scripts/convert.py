#!/usr/bin/env python3
"""
将主站链接转换为 GitHub Pages 链接的脚本
适用于 yfy0109.github.io -> yfy0109.top
"""

import os
import re
from pathlib import Path

def convert_links():
    """转换所有 HTML 文件中的链接"""
    html_files = list(Path('.').rglob('*.html'))
    
    if not html_files:
        print("未找到 HTML 文件")
        return
    
    for file_path in html_files:
        print(f"处理: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换主站域名为 GitHub Pages 域名
            new_content = content.replace(
                'yfy0109.github.io',
                'yfy0109.top', 
                )
            
            # 替换链接文本（如果需要）
            new_content = new_content.replace('访问主站', '访问备用站')
            new_content = new_content.replace('主站点', '备用站点')
            
            if content != new_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✅ 已更新: {file_path}")
            else:
                print(f"  ⏭️ 无需修改: {file_path}")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")

if __name__ == '__main__':
    print("开始转换链接...")
    convert_links()
    print("转换完成！")

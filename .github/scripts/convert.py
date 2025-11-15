#!/usr/bin/env python3
"""
将主站链接转换为 GitHub Pages 链接的脚本
适用于 yfy0109.github.io -> yfy0109.top
"""

import os
import re
import shutil
from pathlib import Path

def convert_links():
    """将项目的可发布文件复制到 public/ 并在副本中替换链接。

    行为：
    - 清空并创建 `public/` 目录
    - 递归复制所有非隐藏文件和目录（跳过 .git 和 .github）到 public/，保持相对路径
    - 在复制后的 HTML 文件中执行文本替换
    """
    src_root = Path('.')
    out_root = Path('public')

    # 清理并创建输出目录
    if out_root.exists():
        print(f"清理目录: {out_root}")
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    # 要跳过的目录（包括输出目录本身，防止将 public 复制到 public/public）
    skip_dirs = {'.git', '.github', '__pycache__', out_root.name}

    # 复制文件
    for root, dirs, files in os.walk(src_root):
        # 防止 os.walk 进入输出目录（topdown=True 时可以修改 dirs 来阻止向下遍历）
        if out_root.name in dirs:
            dirs.remove(out_root.name)

        rel_root = Path(root).relative_to(src_root)

        # 跳过隐藏或特殊目录
        if any(part in skip_dirs for part in rel_root.parts):
            continue

        target_dir = out_root.joinpath(rel_root)
        target_dir.mkdir(parents=True, exist_ok=True)

        for fname in files:
            # 跳过本脚本本身的复制（放在 .github/scripts ）
            src_path = Path(root) / fname
            # 不复制隐藏文件/目录 (以 . 开头)
            if fname.startswith('.'):
                continue

            # 相对目标路径
            rel_file = rel_root / fname
            dest_path = out_root / rel_file

            try:
                shutil.copy2(src_path, dest_path)
            except Exception as e:
                print(f"复制失败 {src_path} -> {dest_path}: {e}")

    # 替换 public 下的 HTML 文件中的链接文本
    html_files = list(out_root.rglob('*.html'))
    if not html_files:
        print("未在 public/ 中找到 HTML 文件（可能没有要发布的内容）")
        return

    for file_path in html_files:
        print(f"处理: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 将主站域名替换为备用（GitHub Pages）域名：主站 yfy0109.top -> 备用 yfy0109.github.io
            new_content = content.replace('yfy0109.top', 'yfy0109.github.io')
            # 反向替换链接文本（因为源为主站，目标为备用站）
            # 将源中表示“备用站/备用站点”的文案改为“主站/主站点”，以保持在备用站上指向主站的文本语义一致
            new_content = new_content.replace('访问备用站', '访问主站')
            new_content = new_content.replace('备用站点', '主站点')

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

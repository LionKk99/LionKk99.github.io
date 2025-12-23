import os
import re
import shutil
from datetime import datetime

# --- 路径配置 ---
OBSIDIAN_BASE = r"D:\github-repo\LionKk99.github.io\Obsidian_projects"
POSTS_DIR = r"D:\github-repo\LionKk99.github.io\_posts"
BLOG_IMAGES_BASE = r"D:\github-repo\LionKk99.github.io\images"

def process_md_files():
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)

    for root, dirs, files in os.walk(OBSIDIAN_BASE):
        for file in files:
            if file.endswith(".md"):
                old_path = os.path.join(root, file)
                pure_name = os.path.splitext(file)[0]
                
                # 1. 计算相对路径结构
                # 假设 root 是 ...\Obsidian_projects\Transformer\illustrated-transformer
                # rel_dir 则是 Transformer\illustrated-transformer
                rel_dir = os.path.relpath(root, OBSIDIAN_BASE)
                
                # 2. 为图片创建镜像目录结构
                # 目标目录: D:\github-repo\LionKk99.github.io\images\Transformer\illustrated-transformer
                current_post_img_dir = os.path.join(BLOG_IMAGES_BASE, rel_dir)
                if not os.path.exists(current_post_img_dir):
                    os.makedirs(current_post_img_dir)

                # 3. 计算 Jekyll 的分类 (Categories)
                categories = rel_dir.split(os.sep) if rel_dir != "." else ["Uncategorized"]
                
                with open(old_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # --- 核心：处理图片并镜像路径 ---
                def img_replace(match):
                    full_img_path = match.group(1)
                    img_name = os.path.basename(full_img_path)
                    
                    # 搜索图片逻辑
                    source_img = os.path.join(root, "imgs", img_name)
                    if not os.path.exists(source_img):
                        source_img = os.path.join(root, img_name)

                    if os.path.exists(source_img):
                        # 拷贝到镜像目录
                        shutil.copy2(source_img, os.path.join(current_post_img_dir, img_name))
                    
                    # 转换为 Jekyll 引用路径，必须保持与 rel_dir 一致
                    # 例如: /images/Transformer/illustrated-transformer/F1.png
                    web_rel_path = rel_dir.replace(os.sep, '/')
                    web_img_path = f"/images/{web_rel_path}/{img_name}"
                    return f'![{img_name}]({{{{ "{web_img_path}" | absolute_url }}}})'

                new_content = re.sub(r'!\[\[(.*?)\]\]', img_replace, content)

                # 4. 生成 Front Matter
                date_prefix = datetime.now().strftime("%Y-%m-%d")
                front_matter = f"""---
layout: post
title: "{pure_name}"
date: {date_prefix} 10:00:00 +0800
categories: {categories}
tags: {categories}
math: true
toc: true
---

"""
                # 5. 写入 _posts
                new_file_name = f"{date_prefix}-{pure_name}.md"
                with open(os.path.join(POSTS_DIR, new_file_name), 'w', encoding='utf-8') as f:
                    f.write(front_matter + new_content)
                
                print(f"✅ 同步成功: {rel_dir}/{file}")

if __name__ == "__main__":
    process_md_files()
    print("\n--- 镜像同步完成 ---")
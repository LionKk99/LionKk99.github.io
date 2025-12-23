import os
import re
import shutil
from datetime import datetime, timedelta

# --- 路径配置 ---
OBSIDIAN_BASE = r"D:\github-repo\LionKk99.github.io\Obsidian_projects"
POSTS_DIR = r"D:\github-repo\LionKk99.github.io\_posts"
BLOG_IMAGES_BASE = r"D:\github-repo\LionKk99.github.io\images"

def process_md_files():
    # 确保目标文件夹存在
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)

    for root, dirs, files in os.walk(OBSIDIAN_BASE):
        for file in files:
            if file.endswith(".md"):
                old_path = os.path.join(root, file)
                pure_name = os.path.splitext(file)[0]
                
                # 1. 计算相对路径结构
                rel_dir = os.path.relpath(root, OBSIDIAN_BASE)
                
                # 2. 为当前笔记创建镜像图片目录
                current_post_img_dir = os.path.join(BLOG_IMAGES_BASE, rel_dir)
                if not os.path.exists(current_post_img_dir):
                    os.makedirs(current_post_img_dir)

                # 3. 读取内容
                with open(old_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 4. 提取第一张图作为封面图 (匹配 ![[...]])
                first_img_match = re.search(r'!\[\[(.*?)\]\]', content)
                featured_image = ""
                if first_img_match:
                    img_name = os.path.basename(first_img_match.group(1))
                    web_rel_path = rel_dir.replace(os.sep, '/')
                    # 如果是根目录，去掉前面的 ./
                    if web_rel_path == ".":
                        featured_image = f"/images/{img_name}"
                    else:
                        featured_image = f"/images/{web_rel_path}/{img_name}"

                # 5. 转换图片语法并拷贝图片文件
                def img_replace(match):
                    full_img_path = match.group(1)
                    img_name = os.path.basename(full_img_path)
                    
                    # 搜索图片逻辑：优先找同级 imgs 文件夹，找不到则找 md 同级
                    source_img = os.path.join(root, "imgs", img_name)
                    if not os.path.exists(source_img):
                        source_img = os.path.join(root, img_name)

                    if os.path.exists(source_img):
                        shutil.copy2(source_img, os.path.join(current_post_img_dir, img_name))
                    
                    web_rel_path = rel_dir.replace(os.sep, '/')
                    if web_rel_path == ".":
                        web_img_path = f"/images/{img_name}"
                    else:
                        web_img_path = f"/images/{web_rel_path}/{img_name}"
                        
                    return f'![{img_name}]({{{{ "{web_img_path}" | absolute_url }}}})'

                new_content = re.sub(r'!\[\[(.*?)\]\]', img_replace, content)

                # 6. 生成 Front Matter (日期设为昨天)
                yesterday = datetime.now() - timedelta(days=1)
                date_prefix = yesterday.strftime("%Y-%m-%d")
                
                # 修正此处的变量名：使用 rel_dir 判断
                categories = rel_dir.split(os.sep) if rel_dir != "." else ["Uncategorized"]
                
                image_field = f'image: "{featured_image}"' if featured_image else ""
                
                front_matter = f"""---
layout: post
title: "{pure_name}"
date: {date_prefix} 10:00:00 +0800
categories: {categories}
tags: {categories}
{image_field}
math: true
toc: true
---

"""
                # 7. 写入新文件
                new_file_name = f"{date_prefix}-{pure_name}.md"
                with open(os.path.join(POSTS_DIR, new_file_name), 'w', encoding='utf-8') as f:
                    f.write(front_matter + new_content)
                
                print(f"✅ 已同步: {pure_name} (路径: {rel_dir})")

if __name__ == "__main__":
    process_md_files()
    print("\n--- 所有笔记同步完成 ---")
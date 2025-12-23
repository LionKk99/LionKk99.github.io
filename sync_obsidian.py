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
                
                # --- 新增：为文章创建镜像 _posts 目录 ---
                current_post_md_dir = os.path.join(POSTS_DIR, rel_dir)
                if not os.path.exists(current_post_md_dir):
                    os.makedirs(current_post_md_dir)

                # 3. 读取内容
                with open(old_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 4. 提取第一张图作为封面图 (匹配 ![[...]])
                first_img_match = re.search(r'!\[\[(.*?)\]\]', content)
                featured_image = ""
                web_rel_path = rel_dir.replace(os.sep, '/')
                
                if first_img_match:
                    img_name = os.path.basename(first_img_match.group(1))
                    if web_rel_path == ".":
                        featured_image = f"/images/{img_name}"
                    else:
                        featured_image = f"/images/{web_rel_path}/{img_name}"

                # 5. 转换图片语法并拷贝图片文件
                def img_replace(match):
                    full_img_path = match.group(1)
                    img_name = os.path.basename(full_img_path)
                    
                    source_img = os.path.join(root, "imgs", img_name)
                    if not os.path.exists(source_img):
                        source_img = os.path.join(root, img_name)

                    if os.path.exists(source_img):
                        shutil.copy2(source_img, os.path.join(current_post_img_dir, img_name))
                    
                    if web_rel_path == ".":
                        web_img_path = f"/images/{img_name}"
                    else:
                        web_img_path = f"/images/{web_rel_path}/{img_name}"
                        
                    return f'![{img_name}]({{{{ "{web_img_path}" | absolute_url }}}})'

                new_content = re.sub(r'!\[\[(.*?)\]\]', img_replace, content)

                # 6. 生成 Front Matter (日期设为昨天)
                yesterday = datetime.now() - timedelta(days=1)
                date_prefix = yesterday.strftime("%Y-%m-%d")
                
                categories = rel_dir.split(os.sep) if rel_dir != "." else ["Uncategorized"]
                image_field = f'image: "{featured_image}"' if featured_image else ""
                
                # 重点：确保 image: 字段没有缩进，且位于横线之间
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
                # 7. 写入新文件 (写入到对应的镜像子目录)
                new_file_name = f"{date_prefix}-{pure_name}.md"
                final_dest_path = os.path.join(current_post_md_dir, new_file_name)
                
                with open(final_dest_path, 'w', encoding='utf-8') as f:
                    f.write(front_matter + new_content)
                
                print(f"✅ 已同步文章: {final_dest_path}")

if __name__ == "__main__":
    process_md_files()
    print("\n--- 镜像同步完成：_posts 与 images 均已保持层级 ---")
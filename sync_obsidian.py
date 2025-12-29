import os
import re
import shutil
from datetime import datetime

# --- 路径配置 ---
OBSIDIAN_BASE = r"D:\github-repo\LionKk99.github.io\Obsidian_projects"
POSTS_DIR = r"D:\github-repo\LionKk99.github.io\_posts"
BLOG_IMAGES_BASE = r"D:\github-repo\LionKk99.github.io\images"

def slugify_path(path):
    """将路径中的空格替换为下划线，用于 Web 安全路径"""
    return path.replace(" ", "_")

def process_md_files():
    # 确保目标文件夹存在
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)

    for root, dirs, files in os.walk(OBSIDIAN_BASE):
        for file in files:
            if file.endswith(".md"):
                old_path = os.path.join(root, file)
                pure_name = os.path.splitext(file)[0]
                
                # 1. 计算相对路径并进行空格替换 (Web 安全处理)
                rel_dir_raw = os.path.relpath(root, OBSIDIAN_BASE)
                rel_dir = slugify_path(rel_dir_raw)
                
                # 2. 为当前笔记创建镜像图片目录 (路径已去空格)
                current_post_img_dir = os.path.join(BLOG_IMAGES_BASE, rel_dir)
                if not os.path.exists(current_post_img_dir):
                    os.makedirs(current_post_img_dir)
                
                # 3. 为文章创建镜像 _posts 目录 (路径已去空格)
                current_post_md_dir = os.path.join(POSTS_DIR, rel_dir)
                if not os.path.exists(current_post_md_dir):
                    os.makedirs(current_post_md_dir)

                # 4. 读取内容
                with open(old_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 5. 提取并处理第一张图路径 (针对空格做特殊处理)
                first_img_match = re.search(r'!\[\[(.*?)\]\]', content)
                featured_image = ""
                web_rel_path = rel_dir.replace(os.sep, '/') # 已是无空格版
                
                if first_img_match:
                    # 提取文件名并将文件名中的空格转为下划线
                    raw_img_name = os.path.basename(first_img_match.group(1))
                    img_name = slugify_path(raw_img_name)
                    
                    if web_rel_path == ".":
                        featured_image = f"/images/{img_name}"
                    else:
                        featured_image = f"/images/{web_rel_path}/{img_name}"

                # 6. 转换正文图片语法并拷贝图片文件 (同时处理文件名的空格)
                def img_replace(match):
                    full_img_path = match.group(1)
                    raw_img_name = os.path.basename(full_img_path)
                    img_name = slugify_path(raw_img_name) # 图片名去空格
                    
                    # 搜索原始图片（原始路径可能有空格）
                    source_img = os.path.join(root, "imgs", raw_img_name)
                    if not os.path.exists(source_img):
                        source_img = os.path.join(root, raw_img_name)

                    if os.path.exists(source_img):
                        # 拷贝到新目录，并重命名为无空格版本
                        shutil.copy2(source_img, os.path.join(current_post_img_dir, img_name))
                    
                    if web_rel_path == ".":
                        web_img_path = f"/images/{img_name}"
                    else:
                        web_img_path = f"/images/{web_rel_path}/{img_name}"
                        
                    return f'![{img_name}]({{{{ "{web_img_path}" | absolute_url }}}})'

                new_content = re.sub(r'!\[\[(.*?)\]\]', img_replace, content)

                # --- 7. 获取文件实际修改时间 (New) ---
                # 获取文件最后修改时间戳
                mod_time_timestamp = os.path.getmtime(old_path)
                # 转换为 datetime 对象
                mod_time_dt = datetime.fromtimestamp(mod_time_timestamp)
                
                # 格式化为 Jekyll 需要的格式
                # 用于文件名的日期前缀 (YYYY-MM-DD)
                date_prefix = mod_time_dt.strftime("%Y-%m-%d")
                # 用于 Front Matter 的详细时间 (YYYY-MM-DD HH:MM:SS)
                full_date_str = mod_time_dt.strftime("%Y-%m-%d %H:%M:%S")
                
                # 类别名称通常可以保留原始名称或使用处理后的，这里建议处理
                categories = [slugify_path(c) for c in rel_dir_raw.split(os.sep)] if rel_dir_raw != "." else ["Uncategorized"]
                image_field = f'image: "{featured_image}"' if featured_image else ""
                
                # 生成 Front Matter，使用文件的实际修改时间
                front_matter = f"""---
layout: post
title: "{pure_name}"
date: {full_date_str} +0800
categories: {categories}
tags: {categories}
{image_field}
math: true
toc: true
---

"""
                # 8. 写入新文件
                safe_pure_name = slugify_path(pure_name)
                # 文件名依然使用 YYYY-MM-DD 前缀
                new_file_name = f"{date_prefix}-{safe_pure_name}.md"
                final_dest_path = os.path.join(current_post_md_dir, new_file_name)
                
                with open(final_dest_path, 'w', encoding='utf-8') as f:
                    f.write(front_matter + new_content)
                
                print(f"✅ 已同步 (使用文件时间 {full_date_str}): {final_dest_path}")

if __name__ == "__main__":
    process_md_files()
    print("\n--- 镜像同步完成：日期已更新为文件修改时间 ---")
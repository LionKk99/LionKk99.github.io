import os
import re
import shutil
from datetime import datetime, timedelta

# --- 路径配置 ---
OBSIDIAN_BASE = r"D:\github-repo\LionKk99.github.io\Obsidian_projects"
POSTS_DIR = r"D:\github-repo\LionKk99.github.io\_posts"
BLOG_IMAGES_BASE = r"D:\github-repo\LionKk99.github.io\images"

def process_md_files():
    # 1. 递归清理旧的 _posts 内容
    if os.path.exists(POSTS_DIR):
        shutil.rmtree(POSTS_DIR)
    os.makedirs(POSTS_DIR)

    for root, dirs, files in os.walk(OBSIDIAN_BASE):
        for file in files:
            if file.endswith(".md"):
                old_path = os.path.join(root, file)
                pure_name = os.path.splitext(file)[0]
                
                # 计算相对路径结构 (例如: AI\Transformer\Attention-Mechanism)
                rel_dir = os.path.relpath(root, OBSIDIAN_BASE)
                
                # 2. 为文章创建镜像目录结构
                current_post_md_dir = os.path.join(POSTS_DIR, rel_dir)
                if not os.path.exists(current_post_md_dir):
                    os.makedirs(current_post_md_dir)

                # 3. 为图片创建镜像目录结构
                current_post_img_dir = os.path.join(BLOG_IMAGES_BASE, rel_dir)
                if not os.path.exists(current_post_img_dir):
                    os.makedirs(current_post_img_dir)

                # 4. 处理分类和标签 (修正后的逻辑)
                path_parts = rel_dir.split(os.sep) if rel_dir != "." else ["Uncategorized"]
                
                # tags：保留除最后一层外的所有父目录
                # 如果只有一层，则保留那一层，避免标签为空
                if len(path_parts) > 1:
                    refined_tags = path_parts[:-1] 
                else:
                    refined_tags = path_parts 
                
                with open(old_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # --- 核心：处理图片引用 ---
                def img_replace(match):
                    full_img_path = match.group(1)
                    img_name = os.path.basename(full_img_path)
                    
                    source_img = os.path.join(root, "imgs", img_name)
                    if not os.path.exists(source_img):
                        source_img = os.path.join(root, img_name)

                    if os.path.exists(source_img):
                        shutil.copy2(source_img, os.path.join(current_post_img_dir, img_name))
                    
                    web_rel_path = rel_dir.replace(os.sep, '/')
                    web_img_path = f"/images/{web_rel_path}/{img_name}"
                    return f'![{img_name}]({{{{ "{web_img_path}" | absolute_url }}}})'

                new_content = re.sub(r'!\[\[(.*?)\]\]', img_replace, content)

                # 5. 生成 Front Matter
                yesterday = datetime.now() - timedelta(days=1)
                date_prefix = yesterday.strftime("%Y-%m-%d")
                
                front_matter = f"""---
layout: post
title: "{pure_name}"
date: {date_prefix} 10:00:00 +0800
categories: {path_parts}
tags: {refined_tags}
math: true
toc: true
---

"""
                # 6. 写入 _posts 下的镜像目录
                new_file_name = f"{date_prefix}-{pure_name}.md"
                target_md_path = os.path.join(current_post_md_dir, new_file_name)
                
                with open(target_md_path, 'w', encoding='utf-8') as f:
                    f.write(front_matter + new_content)
                
                print(f"✅ 已镜像同步: {rel_dir}/{new_file_name} | Tags: {refined_tags}")

if __name__ == "__main__":
    process_md_files()
    print("\n--- 全镜像同步完成！ ---")
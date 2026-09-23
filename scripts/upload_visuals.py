#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Harness 专栏图床同步脚本
用于将 agent_harness_column 中的 visuals 目录自动同步并推送到本图床仓库
"""

import os
import shutil
import subprocess
import sys

def sync_and_push(season="season_01", commit_msg="feat(assets): sync latest visuals from column"):
    # 路径定义
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_season_dir = os.path.abspath(os.path.join(current_dir, "..", "agent_harness_column", season))
    dst_season_dir = os.path.join(current_dir, "column", season)

    if not os.path.exists(src_season_dir):
        print(f"[Error] Source season directory not found: {src_season_dir}")
        sys.exit(1)

    copied_files = 0
    print(f"[*] Syncing from {src_season_dir} to {dst_season_dir}...")
    for item in os.listdir(src_season_dir):
        vis_dir = os.path.join(src_season_dir, item, "visuals")
        if os.path.isdir(vis_dir):
            target_dir = os.path.join(dst_season_dir, item)
            os.makedirs(target_dir, exist_ok=True)
            for f in os.listdir(vis_dir):
                if f.lower().endswith(('.png', '.svg', '.jpg', '.jpeg', '.webp', '.gif')):
                    src_f = os.path.join(vis_dir, f)
                    dst_f = os.path.join(target_dir, f)
                    shutil.copy2(src_f, dst_f)
                    copied_files += 1
                    print(f"  + Synced: {item}/{f}")

    print(f"[+] Total {copied_files} images synced.")

    # 检查 Git 变更
    os.chdir(current_dir)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    if not status:
        print("[*] No changes to commit.")
        return

    print("[*] Staging and committing changes...")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    print("[*] Pushing to remote main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("[✓] Successfully synced and pushed to GitHub!")

if __name__ == "__main__":
    sync_and_push()

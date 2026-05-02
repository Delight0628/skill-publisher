#!/usr/bin/env python3
"""
GitHub 发布器
=============

通过 GitHub MCP 工具自动创建仓库并推送代码。
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from utils import (
    logger,
    ensure_dir,
    run_command,
    git_command,
    get_iso_timestamp,
    normalize_repo_name
)


class GitHubPublisher:
    """GitHub 发布器"""
    
    DEFAULT_TOPICS = [
        "roo", "agent", "skill", "ai", "automation",
    ]
    
    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.github_user = os.environ.get("GITHUB_USER")
    
    def publish(
        self,
        project_path: Path,
        repo_name: str,
        org: Optional[str] = None,
        license: Optional[str] = None,
        is_private: bool = False,
        create_release: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict]:
        """发布项目到 GitHub"""
        try:
            # 1. 创建 GitHub 仓库
            repo_info = self._create_repository(
                repo_name=repo_name, org=org, license=license,
                is_private=is_private, metadata=metadata
            )
            if not repo_info:
                return None
            
            # 2. 初始化 Git 仓库
            if not self._init_git_repo(project_path):
                return None
            
            # 3. 添加远程仓库
            remote_url = repo_info.get("clone_url") or repo_info.get("html_url")
            if not self._add_remote(project_path, remote_url):
                return None
            
            # 4. 提交代码
            if not self._commit_code(project_path, metadata):
                return None
            
            # 5. 推送代码
            if not self._push_code(project_path):
                return None
            
            # 6. 创建 Release（可选）
            if create_release:
                self._create_release(project_path, create_release, metadata)
            
            return {
                "url": repo_info.get("html_url"),
                "clone_url": repo_info.get("clone_url"),
                "ssh_url": repo_info.get("ssh_url"),
                "repo_name": repo_name,
                "org": org,
                "is_private": is_private,
            }
            
        except Exception as e:
            logger.error(f"发布失败: {e}")
            return None
    
    def _create_repository(self, repo_name, org=None, license=None, is_private=False, metadata=None):
        """创建 GitHub 仓库"""
        description = metadata.get("description", "")[:200] if metadata else ""
        
        cmd = ["gh", "repo", "create", repo_name]
        if org:
            cmd = ["gh", "repo", "create", f"{org}/{repo_name}"]
        if description:
            cmd.extend(["--description", description])
        if is_private:
            cmd.append("--private")
        else:
            cmd.append("--public")
        if license:
            cmd.extend(["--license", license])
        
        topics = self.DEFAULT_TOPICS.copy()
        if metadata and metadata.get("name"):
            topics.append(metadata["name"])
        cmd.extend(["--topic", ",".join(topics)])
        
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            return {
                "html_url": f"https://github.com/{org or self.github_user}/{repo_name}",
                "clone_url": f"https://github.com/{org or self.github_user}/{repo_name}.git",
                "ssh_url": f"git@github.com:{org or self.github_user}/{repo_name}.git",
            }
        else:
            logger.error(f"创建仓库失败: {stderr}")
            return None
    
    def _init_git_repo(self, project_path: Path) -> bool:
        returncode, stdout, stderr = git_command(["init"], project_path)
        if returncode != 0:
            return False
        git_command(["config", "user.email", "roo-agent-skills@users.noreply.github.com"], project_path)
        git_command(["config", "user.name", "Roo Agent Skills"], project_path)
        return True
    
    def _add_remote(self, project_path: Path, remote_url: str) -> bool:
        returncode, stdout, stderr = git_command(["remote", "get-url", "origin"], project_path)
        if returncode == 0:
            returncode, stdout, stderr = git_command(["remote", "set-url", "origin", remote_url], project_path)
        else:
            returncode, stdout, stderr = git_command(["remote", "add", "origin", remote_url], project_path)
        return returncode == 0
    
    def _commit_code(self, project_path: Path, metadata=None) -> bool:
        returncode, stdout, stderr = git_command(["add", "."], project_path)
        if returncode != 0:
            return False
        
        version = metadata.get("version", "1.0.0") if metadata else "1.0.0"
        skill_name = metadata.get("name", project_path.name) if metadata else project_path.name
        commit_msg = f"feat: initial release of {skill_name} v{version}"
        
        returncode, stdout, stderr = git_command(["commit", "-m", commit_msg], project_path)
        return returncode == 0
    
    def _push_code(self, project_path: Path) -> bool:
        returncode, stdout, stderr = git_command(["push", "-u", "origin", "main"], project_path)
        if returncode != 0:
            returncode, stdout, stderr = git_command(["push", "-u", "origin", "master"], project_path)
        return returncode == 0
    
    def _create_release(self, project_path, tag, metadata=None) -> bool:
        tag_msg = f"Release {tag}"
        returncode, stdout, stderr = git_command(["tag", "-a", tag, "-m", tag_msg], project_path)
        if returncode != 0:
            return False
        returncode, stdout, stderr = git_command(["push", "origin", tag], project_path)
        return returncode == 0
    
    def normalize_repo_name(self, skill_name: str) -> str:
        return normalize_repo_name(skill_name)
    
    def check_prerequisites(self) -> Dict[str, bool]:
        results = {}
        returncode, stdout, stderr = run_command(["git", "--version"])
        results["git"] = returncode == 0
        returncode, stdout, stderr = run_command(["gh", "--version"])
        results["gh_cli"] = returncode == 0
        results["github_token"] = bool(self.github_token)
        return results

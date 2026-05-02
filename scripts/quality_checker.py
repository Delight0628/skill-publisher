#!/usr/bin/env python3
"""
代码质量检查器
==============

在推送前自动执行基础的代码质量检查。
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from utils import (
    logger,
    read_text_file,
    read_json_file,
    detect_skill_type
)


class QualityChecker:
    """代码质量检查器"""
    
    SENSITIVE_PATTERNS = [
        (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][^'\"]{10,}['\"]", "API Key 硬编码"),
        (r"(?i)(secret[_-]?key|secretkey)\s*[:=]\s*['\"][^'\"]{10,}['\"]", "Secret Key 硬编码"),
        (r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{6,}['\"]", "密码硬编码"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
        (r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "私钥文件内容"),
    ]
    
    SYNTAX_CHECKERS = {
        ".py": "_check_python_syntax",
        ".sh": "_check_shell_syntax",
        ".js": "_check_javascript_syntax",
    }
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.stats = {
            "files_scanned": 0,
            "issues_found": 0,
            "warnings_found": 0,
            "sensitive_patterns_found": 0,
        }
    
    def run_checks(self) -> Dict:
        """执行所有质量检查"""
        logger.info("开始代码质量检查...")
        
        self._scan_sensitive_info()
        self._check_syntax()
        self._check_file_structure()
        self._check_dependencies()
        
        result = {
            "passed": len(self.issues) == 0,
            "issues": self.issues,
            "warnings": self.warnings,
            "stats": self.stats,
        }
        
        return result
    
    def _scan_sensitive_info(self) -> None:
        """扫描敏感信息"""
        for file_path in self._get_scannable_files():
            try:
                content = read_text_file(file_path)
                rel_path = file_path.relative_to(self.project_path)
                
                for pattern, description in self.SENSITIVE_PATTERNS:
                    matches = re.findall(pattern, content)
                    if matches:
                        self.issues.append(
                            f"[敏感信息] {rel_path}: {description} (发现 {len(matches)} 处)"
                        )
                        self.stats["sensitive_patterns_found"] += len(matches)
            except Exception as e:
                logger.debug(f"扫描文件失败 {file_path}: {e}")
    
    def _check_syntax(self) -> None:
        """检查代码语法"""
        for file_path in self._get_scannable_files():
            suffix = file_path.suffix.lower()
            if suffix in self.SYNTAX_CHECKERS:
                checker_method = getattr(self, self.SYNTAX_CHECKERS[suffix], None)
                if checker_method:
                    checker_method(file_path)
    
    def _check_python_syntax(self, file_path: Path) -> None:
        """检查 Python 语法"""
        try:
            content = read_text_file(file_path)
            compile(content, str(file_path), "exec")
        except SyntaxError as e:
            rel_path = file_path.relative_to(self.project_path)
            self.issues.append(f"[语法错误] {rel_path}: {e}")
    
    def _check_shell_syntax(self, file_path: Path) -> None:
        pass
    
    def _check_javascript_syntax(self, file_path: Path) -> None:
        pass
    
    def _check_file_structure(self) -> None:
        """检查文件结构"""
        required_files = ["SKILL.md", ".gitignore"]
        for file_name in required_files:
            file_path = self.project_path / file_name
            if not file_path.exists():
                self.warnings.append(f"[文件结构] 缺少必需文件: {file_name}")
    
    def _check_dependencies(self) -> None:
        """检查依赖配置"""
        pass
    
    def _get_scannable_files(self) -> List[Path]:
        """获取可扫描的文件列表"""
        scannable_extensions = {
            ".py", ".js", ".ts", ".sh", ".bash",
            ".json", ".yaml", ".yml", ".toml",
            ".md", ".txt", ".cfg", ".ini",
        }
        
        exclude_dirs = {
            "__pycache__", ".git", "node_modules",
            ".pytest_cache", "dist", "build",
        }
        
        files = []
        for file_path in self.project_path.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.project_path)
                parts = rel_path.parts
                if any(part in exclude_dirs for part in parts):
                    continue
                if file_path.suffix.lower() in scannable_extensions:
                    files.append(file_path)
                    self.stats["files_scanned"] += 1
        
        return files

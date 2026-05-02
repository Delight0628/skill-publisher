#!/usr/bin/env python3
"""
Skill Publisher 工具函数库
==========================

提供通用的工具函数，包括：
- 路径操作
- 元数据解析
- 日志输出
- 文件操作
"""

import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ============================================================================
# 路径配置
# ============================================================================

# 技能根目录
# 脚本路径: .roo/skills/<skill-name>/scripts/utils.py
# 向上 3 级: .roo/skills/
SKILLS_ROOT = Path(os.environ.get("SKILLS_DIR", Path(__file__).parent.parent.parent))

# 工作目录
WORK_DIR = Path(os.environ.get("WORK_DIR", Path.home() / ".roo" / "skill-publisher" / "work"))

# ============================================================================
# 日志配置
# ============================================================================

def setup_logger(name: str = "skill-publisher", level: str = "INFO") -> logging.Logger:
    """配置并返回日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))
        
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

logger = setup_logger()

# ============================================================================
# 路径操作工具
# ============================================================================

def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def clean_dir(path: Path) -> None:
    """清空目录内容"""
    if path.exists():
        for item in path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        path.mkdir(parents=True, exist_ok=True)

def copy_skill_source(skill_name: str, dest_dir: Path) -> Path:
    """复制技能源代码到目标目录"""
    skill_src = SKILLS_ROOT / skill_name
    if not skill_src.exists():
        raise FileNotFoundError(f"技能目录不存在: {skill_src}")
    
    # 排除的文件和目录
    exclude_patterns = {
        "__pycache__", "*.pyc", ".git", ".gitignore",
        "*.egg-info", "dist", "build", ".pytest_cache"
    }
    
    dest_skill = dest_dir / skill_name
    if dest_skill.exists():
        shutil.rmtree(dest_skill)
    
    # 复制整个技能目录
    shutil.copytree(skill_src, dest_skill, ignore=shutil.ignore_patterns(*exclude_patterns))
    
    return dest_skill

# ============================================================================
# 元数据解析工具
# ============================================================================

def parse_skill_metadata(skill_path: Path) -> Dict[str, Any]:
    """解析 SKILL.md 文件中的元数据"""
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        logger.warning(f"SKILL.md 不存在: {skill_md}")
        return {}
    
    metadata = {
        "name": skill_path.name,
        "version": "1.0.0",
        "author": "Unknown",
        "description": "",
        "entrypoint": None,
        "trigger": "manual"
    }
    
    try:
        content = skill_md.read_text(encoding="utf-8")
        
        # 解析 YAML front matter
        yaml_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            
            # 解析 name
            name_match = re.search(r"^name:\s*(.+)$", yaml_content, re.MULTILINE)
            if name_match:
                metadata["name"] = name_match.group(1).strip()
            
            # 解析 description
            desc_match = re.search(r"^description:\s*>?\s*(.+?)(?:\n|$)", yaml_content, re.MULTILINE)
            if desc_match:
                metadata["description"] = desc_match.group(1).strip()
            
            # 解析 version
            version_match = re.search(r"^version:\s*(.+)$", yaml_content, re.MULTILINE)
            if version_match:
                metadata["version"] = version_match.group(1).strip()
            
            # 解析 author
            author_match = re.search(r"^author:\s*(.+)$", yaml_content, re.MULTILINE)
            if author_match:
                metadata["author"] = author_match.group(1).strip()
            
            # 解析 entrypoint
            entry_match = re.search(r"^entrypoint:\s*(.+)$", yaml_content, re.MULTILINE)
            if entry_match:
                metadata["entrypoint"] = entry_match.group(1).strip()
            
            # 解析 trigger
            trigger_match = re.search(r"^trigger:\s*(.+)$", yaml_content, re.MULTILINE)
            if trigger_match:
                metadata["trigger"] = trigger_match.group(1).strip()
        
        # 从标题提取描述（如果没有 front matter description）
        if not metadata["description"]:
            title_match = re.search(r"^#\s+(.+?)\s*-.*?$", content, re.MULTILINE)
            if title_match:
                metadata["description"] = title_match.group(1).strip()
    
    except Exception as e:
        logger.warning(f"解析 SKILL.md 失败: {e}")
    
    return metadata

def normalize_repo_name(skill_name: str) -> str:
    """将技能名称转换为仓库名称（kebab-case）"""
    # 替换下划线、空格为连字符
    name = re.sub(r"[_\s]+", "-", skill_name)
    # 转换为小写
    name = name.lower()
    # 移除特殊字符
    name = re.sub(r"[^a-z0-9-]", "", name)
    # 移除多余的连字符
    name = re.sub(r"-+", "-", name)
    # 移除首尾连字符
    name = name.strip("-")
    return name

def detect_skill_type(skill_path: Path) -> str:
    """检测技能类型"""
    scripts_dir = skill_path / "scripts"
    
    if (scripts_dir / "main.py").exists() or list(scripts_dir.glob("*.py")):
        return "python"
    elif (scripts_dir / "main.sh").exists() or list(scripts_dir.glob("*.sh")):
        return "shell"
    elif (scripts_dir / "main.ps1").exists() or list(scripts_dir.glob("*.ps1")):
        return "powershell"
    elif (scripts_dir / "main.js").exists() or list(scripts_dir.glob("*.js")):
        return "nodejs"
    elif (skill_path / "package.json").exists():
        return "nodejs"
    elif (skill_path / "requirements.txt").exists() or (skill_path / "pyproject.toml").exists():
        return "python"
    
    return "unknown"

# ============================================================================
# 字符串处理工具
# ============================================================================

def to_kebab_case(text: str) -> str:
    """转换为 kebab-case"""
    return re.sub(r"[\s_]+", "-", text.lower()).strip("-")

def to_snake_case(text: str) -> str:
    """转换为 snake_case"""
    return re.sub(r"[\s-]+", "_", text.lower()).strip("_")

def to_pascal_case(text: str) -> str:
    """转换为 PascalCase"""
    return "".join(word.capitalize() for word in re.split(r"[\s_-]+", text))

# ============================================================================
# 日期时间工具
# ============================================================================

def get_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_iso_timestamp() -> str:
    """获取 ISO 格式时间戳（Windows 路径安全）"""
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

# ============================================================================
# 文件操作工具
# ============================================================================

def read_json_file(path: Path) -> Dict:
    """读取 JSON 文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json_file(path: Path, data: Dict, indent: int = 2) -> None:
    """写入 JSON 文件"""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def read_text_file(path: Path) -> str:
    """读取文本文件"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text_file(path: Path, content: str) -> None:
    """写入文本文件"""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ============================================================================
# 命令执行工具
# ============================================================================

def run_command(cmd: List[str], cwd: Optional[Path] = None, capture: bool = True) -> tuple:
    """
    执行命令
    返回: (returncode, stdout, stderr)
    """
    import subprocess
    
    logger.debug(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"命令执行超时: {' '.join(cmd)}")
        return -1, "", "Command timed out"
    except Exception as e:
        logger.error(f"命令执行失败: {e}")
        return -1, "", str(e)

def git_command(cmd: List[str], repo_dir: Path) -> tuple:
    """执行 Git 命令的便捷函数"""
    return run_command(["git"] + cmd, cwd=repo_dir)

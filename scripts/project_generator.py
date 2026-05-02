#!/usr/bin/env python3
"""
项目结构生成器
==============

将 Roo Agent Skills 转换为标准开源项目结构。
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from utils import (
    logger,
    ensure_dir,
    copy_skill_source,
    parse_skill_metadata,
    detect_skill_type,
    normalize_repo_name,
    to_pascal_case,
    get_iso_timestamp,
    write_text_file,
    read_text_file
)


class ProjectGenerator:
    """项目结构生成器"""
    
    def __init__(self, skill_path: Path, output_dir: Path):
        self.skill_path = skill_path
        self.output_dir = output_dir
        self.skill_name = skill_path.name
        self.metadata = parse_skill_metadata(skill_path)
        self.skill_type = detect_skill_type(skill_path)
        self.repo_name = normalize_repo_name(self.skill_name)
    
    def generate(self) -> Optional[Path]:
        """生成完整的项目结构"""
        try:
            project_path = self.output_dir / self.repo_name
            ensure_dir(project_path)
            
            # 1. 复制源代码
            logger.info("复制技能源代码...")
            self._copy_source_files(project_path)
            
            # 2. 生成项目配置文件
            logger.info("生成项目配置文件...")
            self._generate_config_files(project_path)
            
            # 3. 生成 .gitignore
            logger.info("生成 .gitignore...")
            self._generate_gitignore(project_path)
            
            # 4. 创建标准目录结构
            logger.info("创建标准目录结构...")
            self._create_standard_dirs(project_path)
            
            # 5. 生成测试框架
            logger.info("生成测试框架...")
            self._generate_test_framework(project_path)
            
            # 6. 生成示例文件
            logger.info("生成示例文件...")
            self._generate_examples(project_path)
            
            logger.info(f"项目结构生成完成: {project_path}")
            return project_path
            
        except Exception as e:
            logger.error(f"项目结构生成失败: {e}")
            return None
    
    def _copy_source_files(self, project_path: Path) -> None:
        """复制源代码文件到项目目录"""
        scripts_src = self.skill_path / "scripts"
        if scripts_src.exists():
            scripts_dest = project_path / "scripts"
            shutil.copytree(scripts_src, scripts_dest, dirs_exist_ok=True)
        
        refs_src = self.skill_path / "references"
        if refs_src.exists():
            refs_dest = project_path / "docs"
            shutil.copytree(refs_src, refs_dest, dirs_exist_ok=True)
        
        assets_src = self.skill_path / "assets"
        if assets_src.exists():
            assets_dest = project_path / "assets"
            shutil.copytree(assets_src, assets_dest, dirs_exist_ok=True)
        
        skill_md_src = self.skill_path / "SKILL.md"
        if skill_md_src.exists():
            shutil.copy2(skill_md_src, project_path / "SKILL.md")
    
    def _generate_config_files(self, project_path: Path) -> None:
        """根据技能类型生成配置文件"""
        if self.skill_type == "python":
            self._generate_python_config(project_path)
        elif self.skill_type == "nodejs":
            self._generate_nodejs_config(project_path)
        elif self.skill_type == "shell":
            self._generate_shell_config(project_path)
        elif self.skill_type == "powershell":
            self._generate_powershell_config(project_path)
    
    def _generate_python_config(self, project_path: Path) -> None:
        """生成 Python 项目配置文件"""
        pyproject_content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "{self.repo_name}"
version = "{self.metadata.get('version', '1.0.0')}"
description = "{self.metadata.get('description', self.skill_name)}"
readme = "README.md"
license = {{text = "MIT"}}
requires-python = ">=3.8"
authors = [
    {{name = "{self.metadata.get('author', 'Roo Agent Skills')}"}}
]
keywords = ["roo", "agent", "skill", "{self.skill_name}"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

[project.urls]
Homepage = "https://github.com/roo-agent-skills/{self.repo_name}"
Repository = "https://github.com/roo-agent-skills/{self.repo_name}"
Issues = "https://github.com/roo-agent-skills/{self.repo_name}/issues"
"""
        write_text_file(project_path / "pyproject.toml", pyproject_content)
        
        requirements_content = """# Core dependencies
# Add your dependencies here
"""
        write_text_file(project_path / "requirements.txt", requirements_content)
    
    def _generate_nodejs_config(self, project_path: Path) -> None:
        """生成 Node.js 项目配置文件"""
        pass
    
    def _generate_shell_config(self, project_path: Path) -> None:
        """生成 Shell 脚本项目配置文件"""
        pass
    
    def _generate_powershell_config(self, project_path: Path) -> None:
        """生成 PowerShell 项目配置文件"""
        pass
    
    def _generate_gitignore(self, project_path: Path) -> None:
        """生成 .gitignore 文件"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual Environment
venv/
env/
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
*.bak
*.backup

# Secrets (NEVER commit these!)
.env.local
.env.*.local
secrets.json
credentials.json
*.pem
*.key
"""
        write_text_file(project_path / ".gitignore", gitignore_content)
    
    def _create_standard_dirs(self, project_path: Path) -> None:
        """创建标准目录结构"""
        dirs = ["src", "tests", "docs", "examples", "assets"]
        
        for dir_name in dirs:
            dir_path = project_path / dir_name
            ensure_dir(dir_path)
            
            if self.skill_type == "python" and dir_name in ("src", "tests"):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    write_text_file(init_file, f'"""{dir_name} package"""\n')
            
            gitkeep = dir_path / ".gitkeep"
            if not any(dir_path.iterdir()):
                write_text_file(gitkeep, "")
    
    def _generate_test_framework(self, project_path: Path) -> None:
        """生成测试框架"""
        if self.skill_type == "python":
            self._generate_python_tests(project_path)
    
    def _generate_python_tests(self, project_path: Path) -> None:
        """生成 Python 测试文件"""
        test_content = f"""#!/usr/bin/env python3
"""
{self.skill_name} 测试套件
"""

import pytest
import sys
from pathlib import Path


class TestSkillBasic:
    """基本功能测试"""
    
    def test_skill_exists(self):
        """测试技能文件存在"""
        skill_path = Path(__file__).parent.parent / "scripts"
        assert skill_path.exists()
    
    def test_skill_md_exists(self):
        """测试 SKILL.md 存在"""
        skill_md = Path(__file__).parent.parent / "SKILL.md"
        assert skill_md.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
"""
        write_text_file(project_path / "tests" / "test_main.py", test_content)
    
    def _generate_examples(self, project_path: Path) -> None:
        """生成示例文件"""
        example_content = f"""# {self.skill_name} 使用示例

## 基本用法

```bash
# 示例命令
# TODO: 添加实际的使用示例
```
"""
        write_text_file(project_path / "examples" / "README.md", example_content)

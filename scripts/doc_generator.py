#!/usr/bin/env python3
"""
文档生成器
==========

根据 skill 的源代码和元数据自动生成标准化文档。
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from utils import (
    logger,
    ensure_dir,
    read_text_file,
    write_text_file,
    detect_skill_type,
    to_pascal_case,
    get_iso_timestamp
)


class DocGenerator:
    """文档生成器"""
    
    LICENSE_TEMPLATES = {
        "MIT": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    }
    
    def __init__(self, project_path: Path, metadata: Dict):
        self.project_path = project_path
        self.metadata = metadata
        self.skill_type = detect_skill_type(project_path)
        self.year = datetime.now().year
        self.author = metadata.get("author", "Roo Agent Skills")
    
    def generate_all(self) -> None:
        """生成所有文档"""
        self.generate_readme()
        self.generate_license()
        self.generate_changelog()
        self.generate_contributing()
    
    def generate_readme(self) -> None:
        """生成 README.md"""
        skill_name = self.metadata.get("name", self.project_path.name)
        description = self.metadata.get("description", "A Roo Agent Skill")
        version = self.metadata.get("version", "1.0.0")
        
        readme_content = f"""# {skill_name}

{description}

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-{version}-blue.svg)](https://github.com/roo-agent-skills/{skill_name})

## 概述

{description}

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/roo-agent-skills/{skill_name}.git
cd {skill_name}
```

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。
"""
        
        write_text_file(self.project_path / "README.md", readme_content)
    
    def generate_license(self, license_type: str = "MIT") -> None:
        """生成 LICENSE 文件"""
        template = self.LICENSE_TEMPLATES.get(license_type, self.LICENSE_TEMPLATES["MIT"])
        license_content = template.format(year=self.year, author=self.author)
        write_text_file(self.project_path / "LICENSE", license_content)
    
    def generate_changelog(self) -> None:
        """生成 CHANGELOG.md"""
        skill_name = self.metadata.get("name", self.project_path.name)
        version = self.metadata.get("version", "1.0.0")
        description = self.metadata.get("description", "A Roo Agent Skill")
        
        changelog_content = f"""# Changelog

## [{version}] - {datetime.now().strftime('%Y-%m-%d')}

### 新增
- {description}
- 基本功能实现
- 文档和示例
- 测试框架
"""
        
        write_text_file(self.project_path / "CHANGELOG.md", changelog_content)
    
    def generate_contributing(self) -> None:
        """生成 CONTRIBUTING.md"""
        skill_name = self.metadata.get("name", self.project_path.name)
        
        contributing_content = f"""# 贡献指南

感谢您对 {skill_name} 的关注！我们欢迎任何形式的贡献。

## 如何贡献

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 提交信息规范

请使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 规范。
"""
        
        write_text_file(self.project_path / "CONTRIBUTING.md", contributing_content)

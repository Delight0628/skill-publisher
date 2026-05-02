"""
skill-publisher 测试配置
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """项目根目录"""
    return Path(__file__).parent.parent


@pytest.fixture
def scripts_dir(project_root):
    """脚本目录"""
    return project_root / "scripts"


@pytest.fixture
def skill_md(project_root):
    """SKILL.md 文件路径"""
    return project_root / "SKILL.md"

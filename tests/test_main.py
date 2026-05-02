#!/usr/bin/env python3
"""
skill-publisher 测试套件
"""

import pytest
import sys
from pathlib import Path


class TestSkillBasic:
    """基本功能测试"""

    def test_skill_exists(self):
        """测试技能文件存在"""
        skill_path = Path(__file__).parent.parent / "scripts"
        assert skill_path.exists(), f"scripts 目录不存在: {skill_path}"

    def test_skill_md_exists(self):
        """测试 SKILL.md 存在"""
        skill_md = Path(__file__).parent.parent / "SKILL.md"
        assert skill_md.exists(), f"SKILL.md 不存在: {skill_md}"

    def test_skill_md_has_metadata(self):
        """测试 SKILL.md 包含元数据"""
        skill_md = Path(__file__).parent.parent / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            assert "---" in content, "SKILL.md 缺少 YAML front matter"
            assert "name:" in content, "SKILL.md 缺少 name 字段"
            assert "description:" in content, "SKILL.md 缺少 description 字段"

    def test_scripts_exist(self):
        """测试所有脚本文件存在"""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        expected_scripts = [
            "publish_skill.py",
            "project_generator.py",
            "quality_checker.py",
            "doc_generator.py",
            "github_publisher.py",
            "utils.py",
        ]
        for script in expected_scripts:
            script_path = scripts_dir / script
            assert script_path.exists(), f"脚本文件不存在: {script_path}"

    def test_templates_exist(self):
        """测试模板文件存在"""
        templates_dir = Path(__file__).parent.parent / "templates"
        assert templates_dir.exists(), f"templates 目录不存在: {templates_dir}"

    def test_references_exist(self):
        """测试参考文档存在"""
        refs_dir = Path(__file__).parent.parent / "references"
        assert refs_dir.exists(), f"references 目录不存在: {refs_dir}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

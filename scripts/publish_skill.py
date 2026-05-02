#!/usr/bin/env python3
"""
Skill Publisher 主发布脚本
===========================

用于将 Roo Agent Skills 全局技能发布到 GitHub 仓库。

用法:
    python publish_skill.py --skill skill-name          # 发布指定技能
    python publish_skill.py --all                        # 批量发布所有技能
    python publish_skill.py --interactive                # 交互式模式
    python publish_skill.py --skill skill-name --dry-run # 试运行
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    SKILLS_ROOT,
    WORK_DIR,
    logger,
    parse_skill_metadata,
    detect_skill_type,
    ensure_dir,
    get_iso_timestamp
)
from project_generator import ProjectGenerator
from quality_checker import QualityChecker
from doc_generator import DocGenerator
from github_publisher import GitHubPublisher


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Skill Publisher - 将 Roo Agent Skills 发布到 GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 发布单个技能
    python publish_skill.py --skill clean-chrome-bookmarks-bar

    # 发布到指定组织
    python publish_skill.py --skill clean-chrome-bookmarks-bar --org my-org

    # 批量发布所有技能
    python publish_skill.py --all

    # 试运行模式
    python publish_skill.py --skill clean-chrome-bookmarks-bar --dry-run

    # 交互式发布
    python publish_skill.py --interactive
        """
    )
    
    # 发布模式
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--skill", "-s",
        type=str,
        help="要发布的技能名称"
    )
    mode_group.add_argument(
        "--all", "-a",
        action="store_true",
        help="批量发布所有技能"
    )
    mode_group.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式模式"
    )
    
    # 发布配置
    config_group = parser.add_argument_group("发布配置")
    config_group.add_argument(
        "--org", "-o",
        type=str,
        default=None,
        help="GitHub 组织名称（默认发布到个人账户）"
    )
    config_group.add_argument(
        "--license", "-l",
        type=str,
        default=None,
        help="许可证类型（MIT/Apache-2.0/GPL-3.0/BSD-2/MIT-3）"
    )
    config_group.add_argument(
        "--private", "-p",
        action="store_true",
        help="创建私有仓库"
    )
    config_group.add_argument(
        "--repo-name",
        type=str,
        default=None,
        help="自定义仓库名称（默认基于技能名称生成）"
    )
    
    # 发布选项
    options_group = parser.add_argument_group("发布选项")
    options_group.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="试运行模式（不实际推送）"
    )
    options_group.add_argument(
        "--skip-checks",
        action="store_true",
        help="跳过代码质量检查"
    )
    options_group.add_argument(
        "--create-release", "-r",
        type=str,
        default=None,
        help="创建 Release 标签（如 v1.0.0）"
    )
    options_group.add_argument(
        "--skip-confirm",
        action="store_true",
        help="跳过发布前确认"
    )
    options_group.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细日志"
    )
    
    return parser.parse_args()


def get_skill_list() -> List[str]:
    """获取所有可用技能列表"""
    if not SKILLS_ROOT.exists():
        logger.error(f"技能目录不存在: {SKILLS_ROOT}")
        return []
    
    skills = []
    for item in SKILLS_ROOT.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item.name)
    
    return sorted(skills)


def interactive_select_skill(skills: List[str]) -> Optional[str]:
    """交互式选择技能"""
    print("\n" + "=" * 60)
    print("Skill Publisher - 交互式发布")
    print("=" * 60)
    print(f"\n找到 {len(skills)} 个可用技能:\n")
    
    for i, skill in enumerate(skills, 1):
        print(f"  {i}. {skill}")
    
    print(f"\n  0. 取消")
    print()
    
    while True:
        try:
            choice = input("请选择要发布的技能编号: ").strip()
            num = int(choice)
            
            if num == 0:
                return None
            elif 1 <= num <= len(skills):
                return skills[num - 1]
            else:
                print("无效的选择，请重新输入")
        except ValueError:
            if choice.lower() in ("q", "quit", "exit"):
                return None
            print("请输入有效的数字")


def interactive_confirm(skill_name: str, repo_name: str, org: Optional[str], is_private: bool) -> bool:
    """交互式确认发布信息"""
    print("\n" + "=" * 60)
    print("发布确认")
    print("=" * 60)
    print(f"\n技能名称: {skill_name}")
    print(f"仓库名称: {repo_name}")
    print(f"目标组织: {org or '个人账户'}")
    print(f"仓库可见性: {'私有' if is_private else '公开'}")
    print()
    
    while True:
        choice = input("确认发布？(y/n): ").strip().lower()
        if choice in ("y", "yes", "是"):
            return True
        elif choice in ("n", "no", "否"):
            return False
        print("请输入 y 或 n")


def publish_single_skill(
    skill_name: str,
    publisher: GitHubPublisher,
    args: argparse.Namespace
) -> bool:
    """发布单个技能"""
    logger.info(f"开始发布技能: {skill_name}")
    
    # 1. 检查技能目录
    skill_path = SKILLS_ROOT / skill_name
    if not skill_path.exists():
        logger.error(f"技能目录不存在: {skill_path}")
        return False
    
    # 2. 解析元数据
    logger.info("解析技能元数据...")
    metadata = parse_skill_metadata(skill_path)
    logger.info(f"技能描述: {metadata.get('description', 'N/A')}")
    logger.info(f"技能版本: {metadata.get('version', 'N/A')}")
    
    # 3. 确定仓库名称
    repo_name = args.repo_name or publisher.normalize_repo_name(skill_name)
    
    # 4. 交互式确认
    if not args.skip_confirm and not args.dry_run:
        is_private = args.private
        if not interactive_confirm(skill_name, repo_name, args.org, is_private):
            logger.info("用户取消了发布")
            return False
    
    # 5. 项目结构生成
    logger.info("生成项目结构...")
    work_dir = WORK_DIR / get_iso_timestamp() / skill_name
    ensure_dir(work_dir)
    
    generator = ProjectGenerator(skill_path, work_dir)
    project_path = generator.generate()
    
    if not project_path:
        logger.error("项目结构生成失败")
        return False
    
    # 6. 代码质量检查
    if not args.skip_checks:
        logger.info("执行代码质量检查...")
        checker = QualityChecker(project_path)
        check_result = checker.run_checks()
        
        if not check_result["passed"]:
            logger.warning(f"代码质量检查发现问题:")
            for issue in check_result["issues"]:
                logger.warning(f"  - {issue}")
            
            if not args.dry_run:
                choice = input("是否继续发布？(y/n): ").strip().lower()
                if choice not in ("y", "yes", "是"):
                    logger.info("用户取消了发布")
                    return False
    
    # 7. 文档生成
    logger.info("生成项目文档...")
    doc_gen = DocGenerator(project_path, metadata)
    doc_gen.generate_all()
    
    # 8. GitHub 发布
    if args.dry_run:
        logger.info("试运行模式 - 跳过实际发布")
        logger.info(f"项目已生成到: {project_path}")
        logger.info(f"仓库名称: {repo_name}")
        logger.info(f"目标组织: {args.org or '个人账户'}")
        return True
    
    logger.info("推送到 GitHub...")
    result = publisher.publish(
        project_path=project_path,
        repo_name=repo_name,
        org=args.org,
        license=args.license,
        is_private=args.private,
        create_release=args.create_release,
        metadata=metadata
    )
    
    if result:
        logger.info(f"发布成功! 仓库 URL: {result['url']}")
        return True
    else:
        logger.error("发布失败")
        return False


def main():
    """主函数"""
    args = parse_arguments()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel("DEBUG")
    
    # 创建工作目录
    ensure_dir(WORK_DIR)
    
    # 初始化 GitHub 发布器
    publisher = GitHubPublisher()
    
    # 获取技能列表
    if args.skill:
        skills = [args.skill]
    elif args.all:
        skills = get_skill_list()
        if not skills:
            logger.error("未找到可发布的技能")
            sys.exit(1)
    elif args.interactive:
        skills_list = get_skill_list()
        selected = interactive_select_skill(skills_list)
        if selected is None:
            logger.info("用户取消了选择")
            sys.exit(0)
        skills = [selected]
    else:
        logger.error("无效的参数组合")
        sys.exit(1)
    
    # 发布技能
    success_count = 0
    fail_count = 0
    
    for skill_name in skills:
        if publish_single_skill(skill_name, publisher, args):
            success_count += 1
        else:
            fail_count += 1
    
    # 输出总结
    print("\n" + "=" * 60)
    print("发布完成")
    print("=" * 60)
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"总计: {len(skills)}")
    
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

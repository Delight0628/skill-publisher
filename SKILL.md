---
name: skill-publisher
description: >
  将 Roo Agent Skills 全局技能进行标准化项目化处理，并通过 GitHub MCP 工具自动推送到 GitHub 仓库实现开源发布。
  支持单个或批量处理，包含项目结构生成、代码质量检查、文档自动生成、版本控制与推送等完整工作流。
version: 1.0.0
author: Roo Agent Skills
trigger: manual
---

# Skill Publisher - 技能发布自动化工具

## 概述

本技能将 `.roo/skills/` 目录下的全局技能进行标准化项目化处理，并通过 GitHub MCP 工具自动推送到 GitHub 仓库实现开源发布。

## 核心功能

### 1. Skill 项目化规范
- 自动识别技能类型（Python/Shell/Node.js 等）
- 生成标准开源项目目录结构
- 创建依赖管理文件（requirements.txt/pyproject.toml/package.json 等）
- 提取并整理元数据配置（作者、版本、描述、标签等）

### 2. GitHub 仓库自动化创建
- 通过 GitHub MCP 工具自动创建仓库
- 仓库命名规范化（kebab-case）
- 自动填充仓库描述、许可证、Topics 标签
- 匹配 .gitignore 模板

### 3. 代码质量保障
- 语法校验（Python/Shell/JavaScript）
- 敏感信息扫描（API Key、密码、内部路径等）
- 基本单元测试框架搭建
- 代码格式化建议

### 4. 文档自动生成
- 自动生成标准化 README.md
- 包含项目简介、功能特性、安装指南、使用示例
- 配置说明、API 文档、贡献指南引用、许可证声明

### 5. 版本控制与推送
- 自动执行 git init
- 首次 commit（遵循 Conventional Commits 规范）
- 关联远程仓库并 push 到 main 分支
- 返回仓库公开访问 URL

### 6. 可选增强功能
- 批量处理多个技能
- 发布前交互式确认
- 自定义远程仓库地址
- 创建 Releases 版本标签

## 快速开始

### 前置要求

- Python 3.8+
- Git 已安装并配置
- GitHub MCP 工具已配置（需要 GitHub Token）
- 网络连接正常

### 使用方式

```bash
# 发布单个技能
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar

# 批量发布所有技能
python scripts/publish_skill.py --all

# 试运行模式
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --dry-run
```

## 目录结构

```
skill-publisher/
├── SKILL.md                          # 本文件（入口）
├── scripts/
│   ├── publish_skill.py              # 主发布脚本
│   ├── project_generator.py          # 项目结构生成器
│   ├── quality_checker.py            # 代码质量检查器
│   ├── doc_generator.py              # 文档生成器
│   ├── github_publisher.py           # GitHub 发布器
│   └── utils.py                      # 工具函数
├── templates/                        # 文档模板
├── references/                       # 参考文档
└── assets/                           # 资源文件
```

## 许可证

本技能采用 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。
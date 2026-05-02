# skill-publisher

将 Roo Agent Skills 全局技能进行标准化项目化处理，并通过 GitHub MCP 工具自动推送到 GitHub 仓库实现开源发布。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Delight0628/skill-publisher)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 概述

本技能将 `.roo/skills/` 目录下的全局技能进行标准化项目化处理，并通过 GitHub MCP 工具自动推送到 GitHub 仓库实现开源发布。

## ✨ 功能特性

- 🔧 自动识别技能类型（Python/Shell/Node.js 等）
- 📁 生成标准开源项目目录结构
- 🔍 代码质量检查（敏感信息扫描、语法校验）
- 📝 文档自动生成（README/LICENSE/CHANGELOG/CONTRIBUTING）
- 🚀 GitHub 仓库自动创建与推送
- 📦 支持批量发布和交互式模式

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- Git 已安装并配置
- GitHub CLI (`gh`) 已安装并登录

### 安装

```bash
# 克隆仓库
git clone https://github.com/Delight0628/skill-publisher.git
cd skill-publisher

# 安装依赖
pip install -r requirements.txt
```

### 使用方法

```bash
# 发布单个技能
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar

# 批量发布所有技能
python scripts/publish_skill.py --all

# 试运行模式（不实际推送）
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --dry-run

# 发布到指定组织
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --org my-org
```

## 📁 项目结构

```
skill-publisher/
├── README.md              # 本文件
├── LICENSE                # MIT 许可证
├── SKILL.md               # Roo Skill 元数据
├── scripts/
│   ├── publish_skill.py   # 主发布脚本
│   ├── project_generator.py  # 项目结构生成器
│   ├── quality_checker.py    # 代码质量检查器
│   ├── doc_generator.py      # 文档生成器
│   ├── github_publisher.py   # GitHub 发布器
│   └── utils.py              # 工具函数
├── templates/             # 文档模板
├── references/            # 参考文档
├── tests/                 # 测试文件
└── examples/              # 示例
```

## 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [问题反馈](https://github.com/Delight0628/skill-publisher/issues)
- [更新日志](CHANGELOG.md)

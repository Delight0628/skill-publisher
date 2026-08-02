<div align="center">

# 🚀 Skill Publisher

### Roo Agent Skills 开源发布自动化工具

将 `.roo/skills/` 目录下的全局技能进行**标准化、项目化**处理，
并通过 GitHub MCP 工具**自动推送到 GitHub 仓库**实现开源发布。

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square&logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=flat-square&logo=semver&logoColor=white)](https://github.com/Delight0628/skill-publisher/releases)
[![Python](https://img.shields.io/badge/python-3.8+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/Delight0628/skill-publisher?style=flat-square&logo=github)](https://github.com/Delight0628/skill-publisher)
[![GitHub Forks](https://img.shields.io/github/forks/Delight0628/skill-publisher?style=flat-square&logo=github)](https://github.com/Delight0628/skill-publisher/fork)
[![Issues](https://img.shields.io/github/issues/Delight0628/skill-publisher?style=flat-square&logo=github)](https://github.com/Delight0628/skill-publisher/issues)

<br/>

<p>
<b>支持单个或批量处理 · 项目结构生成 · 代码质量检查 · 文档自动生成 · 版本控制与推送</b>
</p>

<img src="https://raw.githubusercontent.com/Delight0628/skill-publisher/main/assets/demo.png" width="600" alt="Skill Publisher Demo"/>

</div>

---

## ✨ 功能特性

<table>
<tr>
<td width="50%">

### 🔧 智能技能识别
自动检测技能类型（Python / Shell / Node.js 等），生成对应的依赖管理文件和项目配置。

</td>
<td width="50%">

### 📁 标准项目结构
自动生成开源项目标准目录结构，包含 `src/`、`tests/`、`scripts/`、`templates/` 等规范化布局。

</td>
</tr>
<tr>
<td>

### 🔍 代码质量检查
发布前自动执行敏感信息扫描（API Key / 密码 / 内部路径）、语法校验和格式化建议。

</td>
<td>

### 📝 文档自动生成
基于模板引擎自动生成 `README.md`、`LICENSE`、`CHANGELOG`、`CONTRIBUTING` 等标准文档。

</td>
</tr>
<tr>
<td>

### 🚀 GitHub 一键推送
通过 GitHub MCP 工具自动创建仓库、填充元数据、关联远程并推送到 `main` 分支。

</td>
<td>

### 📦 批量与交互模式
支持批量发布所有技能，也支持交互式选择和逐个确认，灵活适配不同场景。

</td>
</tr>
</table>

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Skill Publisher 工作流程                             │
└─────────────────────────────────────────────────────────────────────────────┘

  .roo/skills/                                                           GitHub
  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐    ┌──────┐
  │  技能目录  │───▶│  项目结构生成  │───▶│  代码质量检查  │───▶│ 文档生成  │───▶│  推送  │
  │          │    │              │    │              │    │          │    │      │
  │ • SKILL.md│    │ • 目录结构    │    │ • 敏感信息扫描 │    │ • README │    │ • git │
  │ • 源代码   │    │ • 依赖文件    │    │ • 语法校验    │    │ • LICENSE│    │ • push│
  │ • 元数据   │    │ • gitignore  │    │ • 格式化建议  │    │ • CHANGE │    │ • 仓库│
  └──────────┘    └──────────────┘    └──────────────┘    │ • CONTRI │    └──────┘
                                                          └──────────┘
```

### 详细步骤说明

| 步骤 | 模块 | 说明 |
|:---:|:---:|:---|
| 1️⃣ | **元数据解析** | 读取 `SKILL.md` 中的 frontmatter，提取名称、版本、描述、作者等信息 |
| 2️⃣ | **项目结构生成** | 基于技能类型生成标准开源项目目录，包含模板化的依赖管理文件 |
| 3️⃣ | **代码质量检查** | 扫描敏感信息、验证语法、检查代码格式，确保发布内容安全合规 |
| 4️⃣ | **文档自动生成** | 使用 Jinja2 模板引擎生成标准化的 README、LICENSE、CONTRIBUTING 等文档 |
| 5️⃣ | **GitHub 推送** | 自动 `git init` → 首次 commit（Conventional Commits）→ 创建远程仓库 → push |

---

## 🚀 快速开始

### 前置要求

- **Python** 3.8 或更高版本
- **Git** 已安装并配置
- **GitHub CLI** (`gh`) 已安装并登录
- **GitHub Token** 已配置（用于 API 调用）

### 安装

```bash
# 克隆仓库
git clone https://github.com/Delight0628/skill-publisher.git
cd skill-publisher

# 安装依赖（本项目主要使用标准库，无需安装第三方包）
pip install -r requirements.txt
```

### 使用方法

#### 📌 发布单个技能

```bash
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar
```

#### 📌 批量发布所有技能

```bash
python scripts/publish_skill.py --all
```

#### 📌 试运行模式（不实际推送）

```bash
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --dry-run
```

#### 📌 发布到指定组织

```bash
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --org my-org
```

#### 📌 交互式模式

```bash
python scripts/publish_skill.py --interactive
```

#### 📌 创建 Release 标签

```bash
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --create-release v1.0.0
```

### 完整参数列表

| 参数 | 缩写 | 说明 | 默认值 |
|:---|:---:|:---|:---:|
| `--skill` | `-s` | 发布指定技能 | - |
| `--all` | `-a` | 批量发布所有技能 | - |
| `--interactive` | `-i` | 交互式选择发布 | - |
| `--org` | `-o` | GitHub 组织名称 | 个人账户 |
| `--license` | `-l` | 许可证类型 | MIT |
| `--private` | `-p` | 创建私有仓库 | false |
| `--repo-name` | - | 自定义仓库名称 | 基于技能名生成 |
| `--dry-run` | `-d` | 试运行模式 | false |
| `--skip-checks` | - | 跳过代码质量检查 | false |
| `--create-release` | `-r` | 创建 Release 标签 | - |
| `--skip-confirm` | - | 跳过发布前确认 | false |
| `--verbose` | `-v` | 显示详细日志 | false |

---

## 📁 项目结构

```
skill-publisher/
├── README.md                  # 项目说明文档
├── LICENSE                    # MIT 许可证
├── SKILL.md                   # Roo Skill 元数据文件
├── pyproject.toml             # Python 项目配置
├── requirements.txt           # 依赖清单
├── CHANGELOG.md               # 变更日志
├── CONTRIBUTING.md            # 贡献指南
│
├── scripts/                   # 核心脚本
│   ├── publish_skill.py       # 🎯 主发布脚本（入口）
│   ├── project_generator.py   # 📁 项目结构生成器
│   ├── quality_checker.py     # 🔍 代码质量检查器
│   ├── doc_generator.py       # 📝 文档生成器
│   ├── github_publisher.py    # 🚀 GitHub 发布器
│   └── utils.py               # 🛠️  工具函数库
│
├── templates/                 # Jinja2 文档模板
│   ├── README.md.j2           # README 模板
│   ├── LICENSE.j2             # 许可证模板
│   ├── CONTRIBUTING.md.j2     # 贡献指南模板
│   ├── CHANGELOG.md.j2        # 变更日志模板
│   ├── pyproject.toml.j2      # Python 项目配置模板
│   ├── requirements.txt.j2    # 依赖清单模板
│   └── package.json.j2        # Node.js 包配置模板
│
├── tests/                     # 测试文件
│   ├── test_main.py           # 主流程测试
│   └── conftest.py            # pytest 配置
│
├── assets/                    # 资源文件
├── examples/                  # 使用示例
└── references/                # 参考文档
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是提交 Bug 报告、功能建议，还是直接提交代码。

### 如何参与

1. **Fork** 本仓库
2. **创建特性分支** (`git checkout -b feat/amazing-feature`)
3. **提交更改** (`git commit -m 'feat: add amazing feature'`)
4. **推送分支** (`git push origin feat/amazing-feature`)
5. **创建 Pull Request**

### 开发规范

- 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 提交规范
- 确保所有测试通过
- 保持代码风格一致

详细信息请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

本项目采用 **MIT 许可证** 开源 — 详见 [LICENSE](LICENSE) 文件。

---

## 🔗 相关链接

| 资源 | 链接 |
|:---|:---|
| 📦 问题反馈 | [GitHub Issues](https://github.com/Delight0628/skill-publisher/issues) |
| 📝 更新日志 | [CHANGELOG.md](CHANGELOG.md) |
| 🤝 贡献指南 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 📜 许可证 | [LICENSE](LICENSE) |

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

Made with ❤️ by [Delight0628](https://github.com/Delight0628)

</div>

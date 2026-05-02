# Skill Publisher 自定义配置说明

## 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| GITHUB_TOKEN | GitHub 访问令牌 | 必需 |
| GITHUB_USER | GitHub 用户名 | 自动检测 |
| GITHUB_ORG | 默认 GitHub 组织 | 用户个人账户 |
| DEFAULT_LICENSE | 默认许可证类型 | MIT |
| SKILLS_DIR | 技能源目录 | .roo/skills |
| WORK_DIR | 临时工作目录 | 系统临时目录 |

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| --skill | 指定技能名称 | --skill clean-chrome-bookmarks-bar |
| --all | 批量处理所有技能 | --all |
| --org | 指定 GitHub 组织 | --org my-org |
| --license | 指定许可证类型 | --license MIT |
| --private | 创建私有仓库 | --private |
| --dry-run | 试运行模式 | --dry-run |
| --skip-checks | 跳过代码质量检查 | --skip-checks |
| --create-release | 创建 Release 标签 | --create-release v1.0.0 |

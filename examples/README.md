# skill-publisher 使用示例

## 基本用法

```bash
# 发布单个技能
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar

# 批量发布所有技能
python scripts/publish_skill.py --all

# 试运行模式
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --dry-run
```

## 高级用法

```bash
# 发布到指定组织
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --org my-org

# 创建私有仓库
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --private

# 跳过质量检查
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --skip-checks

# 创建 Release 标签
python scripts/publish_skill.py --skill clean-chrome-bookmarks-bar --create-release v1.0.0
```

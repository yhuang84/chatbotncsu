# 🚀 GitHub 部署指南

本指南将帮助你将项目上传到 GitHub。

## 📋 准备工作

### 1. 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `ncsu-research-assistant` (或你喜欢的名字)
   - **Description**: "AI-powered research assistant for NC State University"
   - **Visibility**: Public 或 Private (根据你的需要)
   - **不要**勾选 "Initialize with README" (我们已经有了)
4. 点击 "Create repository"

### 2. 初始化 Git 仓库

在 `Chatbot_Deploy` 目录下运行：

```bash
cd Chatbot_Deploy

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: NCSU Research Assistant"

# 添加远程仓库 (替换 YOUR_USERNAME 和 REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 🔒 重要：保护敏感信息

### 已排除的文件 (.gitignore)

以下文件**不会**被上传到 GitHub：
- `.env` - 包含 API 密钥
- `__pycache__/` - Python 缓存文件
- `results/*` - 研究结果文件
- `*.log` - 日志文件

### 设置 GitHub Secrets (用于 GitHub Actions)

如果你的仓库使用 GitHub Actions，需要设置 Secrets：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加以下 secrets (如果需要):
   - `OPENAI_API_KEY` - 你的 OpenAI API 密钥
   - `ANTHROPIC_API_KEY` - 你的 Anthropic API 密钥 (可选)

## 📝 更新 README 中的链接

在推送之前，记得更新 `README.md` 中的以下内容：

1. **Clone URL**: 将 `yourusername` 替换为你的 GitHub 用户名
2. **Repository URL**: 更新所有指向仓库的链接

## ✅ 验证清单

上传前请确认：

- [ ] 所有文件都已添加到 Git (`git add .`)
- [ ] `.env` 文件**不在**仓库中 (已在 .gitignore)
- [ ] `results/` 目录中的文件**不在**仓库中 (已在 .gitignore)
- [ ] README.md 中的链接已更新
- [ ] LICENSE 文件已包含
- [ ] 所有文档文件都已创建

## 🎯 推送命令 (完整版)

```bash
# 1. 进入目录
cd Chatbot_Deploy

# 2. 初始化 Git (如果还没初始化)
git init

# 3. 检查状态
git status

# 4. 添加所有文件
git add .

# 5. 创建提交
git commit -m "Initial commit: NCSU Research Assistant v1.0.0"

# 6. 添加远程仓库 (替换为你的仓库 URL)
git remote add origin https://github.com/YOUR_USERNAME/ncsu-research-assistant.git

# 7. 设置主分支
git branch -M main

# 8. 推送到 GitHub
git push -u origin main
```

## 🔄 后续更新

当你修改代码后：

```bash
# 1. 查看更改
git status

# 2. 添加更改的文件
git add .

# 3. 提交更改
git commit -m "描述你的更改"

# 4. 推送到 GitHub
git push
```

## 📊 GitHub 功能设置

### 启用 GitHub Pages (可选)

如果你想创建一个项目网站：

1. Settings → Pages
2. Source: 选择 "main" 分支
3. 保存

### 启用 GitHub Actions

CI 工作流会自动运行，检查：
- 代码格式
- 导入测试
- 基本功能验证

### 添加 Topics (标签)

在仓库主页点击 ⚙️ → Topics，添加：
- `python`
- `streamlit`
- `ai`
- `research-assistant`
- `ncsu`
- `web-scraping`

## 🐛 常见问题

### Q: 如何更新 .gitignore 中已跟踪的文件？

```bash
# 从 Git 中移除但保留本地文件
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### Q: 如何撤销最后一次提交？

```bash
# 撤销提交但保留更改
git reset --soft HEAD~1

# 完全撤销提交和更改 (谨慎使用!)
git reset --hard HEAD~1
```

### Q: 如何查看 Git 历史？

```bash
git log --oneline
```

## 🎉 完成！

上传成功后，你的仓库应该包含：

- ✅ 所有源代码文件
- ✅ README.md 和文档
- ✅ LICENSE 文件
- ✅ .gitignore 文件
- ✅ GitHub Actions 工作流
- ✅ 项目结构完整

**注意**: 确保 `.env` 文件**没有**被上传！

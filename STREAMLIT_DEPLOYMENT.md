# 🚀 Streamlit Community Cloud 部署指南

本指南将帮助您将 NCSU Research Assistant 部署到 Streamlit Community Cloud。

## 📋 前置要求

1. **GitHub 账户** - 用于托管代码
2. **Streamlit Community Cloud 账户** - 免费注册：https://share.streamlit.io/
3. **OpenAI API Key** (可选) - 用于 AI 功能，如果没有可以使用 mock 模式

## 🔧 部署步骤

### 步骤 1: 准备 GitHub 仓库

1. 在 GitHub 上创建一个新仓库（例如：`ncsu-research-assistant`）
2. 将 `Chatbot_Deploy` 文件夹中的所有文件推送到仓库

```bash
cd Chatbot_Deploy
git init
git add .
git commit -m "Initial commit: NCSU Research Assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ncsu-research-assistant.git
git push -u origin main
```

### 步骤 2: 连接到 Streamlit Community Cloud

1. 访问 https://share.streamlit.io/
2. 点击 "New app"
3. 选择您的 GitHub 仓库
4. 选择分支（通常是 `main`）
5. 设置主文件路径：`app.py` 或 `user_interface.py`
6. 点击 "Deploy!"

### 步骤 3: 配置 API Key（可选）

如果您想使用 OpenAI 或 Anthropic API：

1. 在 Streamlit Community Cloud 中，点击应用设置（⚙️）
2. 进入 "Secrets" 标签
3. 添加以下内容：

```toml
[openai]
api_key = "your-openai-api-key-here"

# 或者使用 Anthropic
[anthropic]
api_key = "your-anthropic-api-key-here"
```

### 步骤 4: 等待部署完成

- Streamlit 会自动安装 `requirements.txt` 中的依赖
- 部署通常需要 2-5 分钟
- 您可以在日志中查看部署进度

## ⚙️ 配置说明

### 主文件选择

Streamlit Community Cloud 支持两种入口点：

1. **`app.py`** - 推荐用于 Streamlit Community Cloud
   - 包含错误处理和路径设置
   - 自动导入 `user_interface.py`

2. **`user_interface.py`** - 也可以直接使用
   - 更简单，适合本地开发

### 环境变量

应用会按以下优先级查找 API Key：

1. **环境变量** (`OPENAI_API_KEY`)
2. **Streamlit Secrets** (`st.secrets["openai"]["api_key"]`)
3. **`.env` 文件** (本地开发)

### 依赖管理

所有依赖都在 `requirements.txt` 中：

```
requests>=2.31.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
openai>=1.0.0
anthropic>=0.7.0
python-dotenv>=1.0.0
pyyaml>=6.0.0
lxml>=4.9.0
streamlit>=1.28.0
```

## 🐛 故障排除

### 问题 1: 应用无法启动

**解决方案：**
- 检查 `app.py` 或 `user_interface.py` 是否存在
- 查看 Streamlit 日志中的错误信息
- 确保所有导入路径正确

### 问题 2: API Key 未找到

**解决方案：**
- 检查 Streamlit Secrets 配置
- 确保 secrets.toml 格式正确
- 尝试使用 mock 模式测试（无需 API Key）

### 问题 3: Selenium 相关错误

**解决方案：**
- Streamlit Community Cloud 可能不支持 Selenium
- 在侧边栏中禁用 Selenium 选项
- 应用会自动回退到 requests 库

### 问题 4: 模块导入错误

**解决方案：**
- 确保 `src/` 目录结构完整
- 检查所有 `__init__.py` 文件存在
- 验证 Python 路径设置正确

## 📝 本地测试

在部署前，建议先在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
# 或
streamlit run user_interface.py
```

## 🔄 更新应用

每次推送到 GitHub 后，Streamlit Community Cloud 会自动重新部署：

```bash
git add .
git commit -m "Update: description of changes"
git push
```

## 📚 更多资源

- [Streamlit Community Cloud 文档](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit 部署指南](https://docs.streamlit.io/deploy)
- [GitHub Actions 集成](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/advanced-features/continuous-deployment)

## ✅ 部署检查清单

- [ ] 所有文件已推送到 GitHub
- [ ] `requirements.txt` 包含所有依赖
- [ ] `app.py` 或 `user_interface.py` 存在且正确
- [ ] `src/` 目录结构完整
- [ ] API Key 已配置（如需要）
- [ ] 本地测试通过
- [ ] Streamlit Community Cloud 连接成功
- [ ] 应用可以正常访问

## 🎉 完成！

部署成功后，您将获得一个公开的 URL，例如：
`https://your-app-name.streamlit.app`

祝您部署顺利！🐺

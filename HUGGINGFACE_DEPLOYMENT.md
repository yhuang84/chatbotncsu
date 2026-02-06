# 🚀 Hugging Face Spaces 部署指南

本指南将帮助你将 NCSU Research Assistant 部署到 Hugging Face Spaces。

## 📋 前置要求

- ✅ GitHub 仓库已创建并上传代码
- ✅ Hugging Face 账号（免费注册：https://huggingface.co/join）

## 🎯 部署步骤

### 方法 1：从 GitHub 仓库连接（推荐）

#### 步骤 1：创建 Hugging Face Space

1. 访问 https://huggingface.co/spaces
2. 点击右上角的 **"Create new Space"** 按钮
3. 填写 Space 信息：
   - **Space name**: `ncsu-research-assistant`（或你喜欢的名字）
   - **SDK**: 选择 **`Streamlit`**
   - **Visibility**: Public（公开）或 Private（私有）
   - **Hardware**: 选择 `CPU basic`（免费）或更高配置
4. 点击 **"Create Space"**

#### 步骤 2：连接 GitHub 仓库

1. 在 Space 页面，点击 **"Files and versions"** 标签
2. 点击 **"Add file"** → **"Connect repository"**
3. 选择你的 GitHub 账号和仓库
4. 选择分支（通常是 `main`）
5. 点击 **"Connect"**

**注意**: Hugging Face 会自动同步 GitHub 仓库的更改。

#### 步骤 3：验证文件结构

确保以下文件存在：
- ✅ `app.py` - 入口文件（已创建）
- ✅ `user_interface.py` - 主界面文件
- ✅ `ncsu_advanced_config_base.py` - 核心模块
- ✅ `requirements.txt` - 依赖列表
- ✅ `src/` - 源代码目录
- ✅ `README.md` - 项目说明

#### 步骤 4：设置 API 密钥（Secrets）

1. 在 Space 页面，点击 **"Settings"** 标签
2. 找到 **"Repository secrets"** 部分
3. 点击 **"New secret"**
4. 添加以下 secrets：
   - **Name**: `OPENAI_API_KEY`
   - **Value**: 你的 OpenAI API 密钥
   - 点击 **"Add secret"**

   （可选）如果需要 Anthropic：
   - **Name**: `ANTHROPIC_API_KEY`
   - **Value**: 你的 Anthropic API 密钥

#### 步骤 5：等待部署

- Hugging Face 会自动检测到代码更改并开始构建
- 构建过程通常需要 2-5 分钟
- 可以在 **"Logs"** 标签查看构建日志

### 方法 2：直接上传文件

如果不想连接 GitHub：

1. 在 Space 页面，点击 **"Files and versions"**
2. 点击 **"Add file"** → **"Upload files"**
3. 上传 `Chatbot_Deploy` 文件夹中的所有文件
4. 确保 `app.py` 文件存在
5. 设置 Secrets（同方法 1 的步骤 4）

## ⚙️ 代码修改说明

### 已完成的修改

1. ✅ **创建了 `app.py`** - Hugging Face Spaces 的入口文件
2. ✅ **更新了 `user_interface.py`** - 支持 Hugging Face Secrets
3. ✅ **更新了 `ncsu_scraper.py`** - 添加了 Selenium fallback 方法

### 关键修改点

#### 1. API 密钥加载（user_interface.py）

代码现在按以下顺序尝试加载 API 密钥：
1. Streamlit secrets（本地开发）
2. Hugging Face environment variables（Spaces）
3. .env 文件（fallback）

#### 2. Selenium Fallback（ncsu_scraper.py）

如果检测到 Hugging Face Spaces 环境，会自动使用不依赖 Selenium 的搜索方法。

## 🔍 验证部署

### 检查清单

- [ ] Space 已创建
- [ ] GitHub 仓库已连接（或文件已上传）
- [ ] `app.py` 文件存在
- [ ] `OPENAI_API_KEY` secret 已设置
- [ ] 构建日志显示成功
- [ ] 应用可以正常访问

### 查看日志

1. 点击 **"Logs"** 标签
2. 查看构建日志和运行时日志
3. 如果有错误，日志会显示详细信息

## 🐛 常见问题

### 问题 1：构建失败

**可能原因**：
- `requirements.txt` 中缺少依赖
- Python 版本不兼容

**解决方法**：
- 检查 `requirements.txt` 是否完整
- 查看构建日志中的错误信息

### 问题 2：API 密钥错误

**可能原因**：
- Secret 名称不正确
- API 密钥无效

**解决方法**：
- 确保 Secret 名称是 `OPENAI_API_KEY`（全大写）
- 验证 API 密钥是否有效

### 问题 3：Selenium 错误

**解决方法**：
- 代码已自动处理，会使用 fallback 方法
- 如果仍有问题，可以在 Space Settings 中设置环境变量 `DISABLE_SELENIUM=true`

### 问题 4：应用无法启动

**解决方法**：
1. 检查 `app.py` 文件是否存在
2. 查看 Logs 中的错误信息
3. 确保所有依赖都已安装

## 📊 部署后的访问

部署成功后，你的应用可以通过以下 URL 访问：

```
https://huggingface.co/spaces/YOUR_USERNAME/ncsu-research-assistant
```

## 🔄 更新应用

### 如果使用 GitHub 连接：

1. 在本地修改代码
2. 推送到 GitHub：
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. Hugging Face 会自动检测更改并重新部署

### 如果直接上传文件：

1. 在 Hugging Face Space 中直接编辑文件
2. 或删除旧文件后上传新文件

## 💡 优化建议

1. **使用 GPU**：如果应用需要大量计算，可以升级到 GPU 硬件
2. **缓存结果**：考虑添加结果缓存以减少 API 调用
3. **错误处理**：确保所有错误都有友好的用户提示
4. **性能监控**：定期检查 Logs 以优化性能

## 🎉 完成！

部署完成后，你的应用就可以通过 Hugging Face Spaces 访问了！

**Go Pack!** 🐺

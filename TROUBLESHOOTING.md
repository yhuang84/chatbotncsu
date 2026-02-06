# 🔧 故障排除指南 - Hugging Face Spaces

## 网页显示空白

### 可能原因和解决方法

#### 1. 检查 Logs（最重要）

在 Hugging Face Spaces 页面：
1. 点击 **"Logs"** 标签
2. 查看是否有错误信息
3. 常见的错误：
   - Import errors（导入错误）
   - Missing dependencies（缺少依赖）
   - Path errors（路径错误）

#### 2. 验证文件结构

确保以下文件存在：
- ✅ `app.py` - 入口文件
- ✅ `user_interface.py` - 主界面文件
- ✅ `ncsu_advanced_config_base.py` - 核心模块
- ✅ `src/` 目录及其所有子文件
- ✅ `requirements.txt` - 依赖列表

#### 3. 检查导入路径

如果看到导入错误，可能是路径问题。`app.py` 已经设置了正确的路径。

#### 4. 常见错误和解决方法

**错误 1: "ModuleNotFoundError: No module named 'user_interface'"**
- **原因**: 文件路径问题
- **解决**: 确保 `user_interface.py` 在根目录

**错误 2: "ModuleNotFoundError: No module named 'ncsu_advanced_config_base'"**
- **原因**: 文件不存在或路径错误
- **解决**: 确保 `ncsu_advanced_config_base.py` 在根目录

**错误 3: "ModuleNotFoundError: No module named 'src.scraper'"**
- **原因**: `src/` 目录结构不完整
- **解决**: 确保 `src/scraper/` 和 `src/utils/` 目录存在

**错误 4: "StreamlitAPIException: set_page_config() can only be called once"**
- **原因**: `set_page_config()` 被调用多次
- **解决**: 已修复，确保只在 `user_interface.py` 中调用一次

#### 5. 验证 Streamlit 配置

检查 `README.md` 中的 frontmatter：
```yaml
app_file: app.py
```

#### 6. 测试导入

如果应用仍然空白，可以创建一个简单的测试文件：

创建 `test_app.py`:
```python
import streamlit as st
st.title("Test")
st.write("If you see this, Streamlit is working!")
```

如果这个能显示，说明问题在导入。如果这个也不显示，可能是 Streamlit 配置问题。

#### 7. 检查依赖安装

查看 Logs，确认所有依赖都已安装：
- streamlit
- requests
- beautifulsoup4
- 等等

#### 8. 重新构建

如果以上都正常，尝试：
1. 在 Settings → Danger Zone → Clear Space
2. 重新推送代码
3. 等待重新构建

## 🔍 调试步骤

1. **查看 Logs** - 这是最重要的！
2. **检查文件结构** - 确保所有文件都在
3. **验证导入** - 检查是否有导入错误
4. **测试简单应用** - 创建最小测试应用
5. **检查依赖** - 确保 requirements.txt 完整

## 📞 需要帮助？

如果问题仍然存在，请：
1. 复制 Logs 中的完整错误信息
2. 检查文件结构是否正确
3. 确认所有文件都已上传

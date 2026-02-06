# 🔧 搜索功能故障排除指南

## 问题：搜索返回 0 结果

如果您遇到搜索返回 0 结果的问题，请按照以下步骤排查：

### 1. 检查网络连接

确保您的网络连接正常，可以访问 https://www.ncsu.edu

### 2. 禁用 Selenium

在 Streamlit Community Cloud 上，Selenium 可能不可用。请：

1. 打开侧边栏的 **Advanced Settings**
2. 取消勾选 **"Enable Selenium"**
3. 重新运行搜索

### 3. 检查日志

查看 Streamlit 日志以获取详细错误信息：
- 在 Streamlit Community Cloud 上，点击 "Manage app" → "Logs"
- 查找错误消息和警告

### 4. 常见问题

#### 问题 A: Selenium 相关错误

**症状：** 看到 "Selenium not available" 或 Chrome 驱动错误

**解决方案：**
- 禁用 Selenium（见步骤 2）
- 应用会自动使用 fallback 搜索方法

#### 问题 B: 网络超时

**症状：** 搜索超时或连接错误

**解决方案：**
- 增加超时时间（Advanced Settings → Timeout）
- 检查防火墙设置
- 确保可以访问 ncsu.edu

#### 问题 C: 搜索结果解析失败

**症状：** 搜索执行但返回 0 结果

**解决方案：**
- NCSU 网站可能更改了搜索页面结构
- 尝试不同的查询关键词
- 检查是否有反爬虫保护

### 5. 测试搜索功能

尝试以下测试查询：
- "computer science"
- "graduate programs"
- "textiles college"

### 6. 手动验证

访问 NCSU 搜索页面验证：
https://www.ncsu.edu/search/?q=textiles+college

如果手动搜索可以工作，但应用不行，可能是：
- 选择器需要更新
- 需要添加更多等待时间
- 需要处理 JavaScript 渲染

### 7. 报告问题

如果问题持续存在，请提供：
- 错误日志
- 查询内容
- 环境信息（本地/Streamlit Cloud）
- Selenium 是否启用

## 临时解决方案

如果搜索功能完全不可用，您可以：

1. **直接访问相关页面：**
   - Textiles College: https://textiles.ncsu.edu/
   - NCSU 主页: https://www.ncsu.edu/

2. **使用浏览器搜索：**
   - 访问 https://www.ncsu.edu/search/
   - 手动输入查询

3. **联系支持：**
   - 检查 NCSU 网站状态
   - 报告搜索功能问题

## 代码改进建议

如果搜索功能需要改进，可以考虑：

1. **使用 Google Custom Search API**（需要 API key）
2. **改进选择器**以适应页面结构变化
3. **添加重试机制**
4. **实现缓存**以减少请求

## 更新日志

- 2026-02-06: 改进了 fallback 搜索方法，添加了更多选择器
- 2026-02-06: 添加了更好的错误处理和用户提示

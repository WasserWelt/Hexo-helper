# Hexo 命令行助手

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Hexo 命令行助手是一个专为 Hexo 博客开发者设计的效率工具，通过简单的数字菜单操作即可完成所有常用 Hexo 命令，支持 Front-matter 模板功能，大幅提升博客写作和管理效率。

## ✨ 功能特性

- 🚀 **一键式操作**：数字键选择，无需记忆复杂命令
- 📝 **智能模板**：预设 Front-matter 模板，支持变量替换
- 🎨 **彩色界面**：不同信息类型使用不同颜色区分
- 🔍 **路径自动检测**：智能查找 Hexo 安装路径
- 📂 **目录快速访问**：一键打开文章/草稿目录
- ⚡ **组合命令**：生成+部署、生成+本地预览等组合操作

## 📦 安装使用

### 前提条件

- Windows 系统
- Python 3.7+
- 已安装 Node.js 和 Hexo
- Hexo 博客项目已初始化

### 快速开始

1. **下载工具**：

   ```bash
   git clone https://github.com/your-repo/Hexo-helper.git
   cd Hexo-helper
   ```
2. **安装依赖**：

   ```bash
   pip install colorama
   ```
3. **运行工具**：

   ```bash
   python hexo_assistant.py
   ```

### 打包为EXE

1. 安装 PyInstaller：

   ```bash
   pip install pyinstaller
   ```
2. 执行打包：

   ```bash
   pyinstaller --onefile --collect-all colorama hexo_helper.py
   ```
3. 打包完成后，EXE 文件位于 `dist` 目录

## 🎮 使用指南

### 主菜单

```
==================================================
  Hexo博客管理助手
==================================================
请选择操作:
 1. 新建文章
 2. 新建草稿
 3. 生成静态文件
 4. 启动本地服务器
 5. 部署到服务器
 6. 清理缓存
 7. 生成并部署
 8. 生成并启动服务器
 9. 打开博客目录
10. 模板管理
 0. 退出
```

### 常用操作示例

1. **新建技术文章**：

   - 选择 `1. 新建文章`
   - 输入标题 `Python技巧分享`
   - 选择技术模板
   - 自动生成包含技术类 Front-matter 的文章
2. **快速部署**：

   - 直接选择 `7. 生成并部署` 一键完成生成和部署
3. **本地调试**：

   - 选择 `8. 生成并启动服务器`
   - 自动打开浏览器预览

## 🛠 模板管理

工具支持自定义 Front-matter 模板，配置文件请存放至 Hexo 项目根目录的 `hexo_helper_config.json`。

### 默认模板示例

```json
{
  "templates": {
    "default": {
      "title": "",
      "date": "{{ now }}",
      "updated": "{{ now }}",
      "tags": [],
      "categories": [],
      "description": "",
      "cover": ""
    },
    "tech": {
      "title": "",
      "date": "{{ now }}",
      "tags": ["技术"],
      "categories": ["技术"],
      "description": "",
      "toc": true,
      "mathjax": false
    }
  }
}
```

### 支持的模板变量

- `{{ now }}`：当前日期时间
- `{{ title }}`：文章标题

## 📜 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

💡 **提示**：将本工具放在 Hexo 项目根目录下运行效果最佳！

Enjoy your Hexo blogging! ✍️🚀

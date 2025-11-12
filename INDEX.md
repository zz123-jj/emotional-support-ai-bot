# 📂 项目文件索引

## 🎯 从这里开始

如果你是第一次使用这个项目，建议按以下顺序阅读：

1. **README_CN.md** (或 README.md) - 了解项目概况
2. **QUICK_REFERENCE.md** - 快速开始使用
3. **start.sh** - 一键启动脚本
4. **app.py** - 运行Web应用

---

## 📋 完整文件列表

### 📖 文档文件 (Documentation)

| 文件名 | 说明 | 推荐阅读顺序 |
|--------|------|-------------|
| **README_CN.md** | 中文完整文档，包含使用教程 | ⭐ 第1步 |
| **README.md** | 英文完整文档 | 可选 |
| **QUICK_REFERENCE.md** | 快速参考指南，常用命令和操作 | ⭐ 第2步 |
| **PROJECT_SUMMARY.md** | 项目总结，功能和技术概览 | 第3步 |
| **TECHNICAL_GUIDE.md** | 技术详细文档，深入了解实现细节 | 进阶阅读 |
| **ARCHITECTURE.md** | 架构可视化，系统设计图解 | 进阶阅读 |
| **INDEX.md** | 文件索引（本文件） | 导航用 |

### 💻 核心代码文件 (Core Code)

| 文件名 | 功能 | 主要类/函数 |
|--------|------|-----------|
| **app.py** | Gradio Web界面 | `ChatInterface`, `launch_app()` |
| **chatbot.py** | 聊天机器人核心引擎 | `EmotionalSupportChatbot` |
| **rag_system.py** | RAG检索系统 | `RAGSystem`, `KnowledgeEnricher` |
| **prompt_engineering.py** | Prompt工程 | `PromptBuilder`, `EmotionAnalyzer` |
| **data_system.py** | 数据收集与学习 | `DataCollector`, `LearningSystem` |
| **config.py** | 配置管理 | `Config` |

### 🔧 工具脚本 (Utility Scripts)

| 文件名 | 用途 | 使用方式 |
|--------|------|---------|
| **start.sh** | 一键启动脚本 | `./start.sh` |
| **init_knowledge.py** | 初始化知识库 | `python init_knowledge.py` |
| **test_system.py** | 系统测试 | `python test_system.py` |
| **examples.py** | API使用示例 | `python examples.py` |

### ⚙️ 配置文件 (Configuration)

| 文件名 | 说明 | 必须修改？ |
|--------|------|-----------|
| **.env.example** | 环境变量模板 | ✅ 复制为.env并填写 |
| **requirements.txt** | Python依赖列表 | ❌ 直接安装 |
| **.gitignore** | Git忽略配置 | ❌ 无需修改 |

### 📦 运行时生成文件 (Generated at Runtime)

这些文件在首次运行时自动生成，无需手动创建：

| 文件/目录 | 说明 |
|----------|------|
| **chroma_db/** | ChromaDB向量数据库目录 |
| **chat_history.db** | SQLite对话历史数据库 |
| **venv/** | Python虚拟环境（如果创建） |

---

## 🚀 快速导航

### 我想...

#### 快速开始使用
→ 阅读 **README_CN.md** 或 **QUICK_REFERENCE.md**  
→ 运行 `./start.sh`

#### 了解技术实现
→ 阅读 **TECHNICAL_GUIDE.md**  
→ 查看 **ARCHITECTURE.md**

#### 测试系统
→ 运行 `python test_system.py`

#### 查看使用示例
→ 运行 `python examples.py`  
→ 阅读 **examples.py** 源码

#### 自定义知识库
→ 编辑 **init_knowledge.py**  
→ 运行 `python init_knowledge.py`

#### 修改配置
→ 编辑 **.env** 文件  
→ 查看 **config.py** 了解可配置项

#### 开发新功能
→ 阅读 **TECHNICAL_GUIDE.md** 的开发文档部分  
→ 查看核心代码文件的注释

---

## 📊 文件依赖关系

```
app.py (Web界面)
    ↓ 依赖
chatbot.py (核心引擎)
    ↓ 依赖
┌────────────┬──────────────┬──────────────┬──────────────┐
│            │              │              │              │
rag_system.py  prompt_       data_         config.py
               engineering.py system.py    (配置)
│            │              │              │
└────────────┴──────────────┴──────────────┘
    ↓ 依赖
requirements.txt (第三方库)
```

---

## 🎓 学习路径

### 初级（使用者）
1. README_CN.md - 了解项目
2. QUICK_REFERENCE.md - 快速上手
3. 运行 app.py - 体验功能
4. 查看 examples.py - 学习API使用

### 中级（开发者）
1. PROJECT_SUMMARY.md - 整体把握
2. ARCHITECTURE.md - 理解架构
3. 阅读核心代码 - chatbot.py, rag_system.py
4. 运行 test_system.py - 理解测试

### 高级（深入研究）
1. TECHNICAL_GUIDE.md - 技术细节
2. 研究 Prompt Engineering - prompt_engineering.py
3. 优化 RAG 系统 - rag_system.py
4. 扩展数据系统 - data_system.py

---

## 📏 代码量统计

| 类型 | 数量 | 总行数（估算） |
|------|------|---------------|
| Python代码 | 9个文件 | ~2500行 |
| 文档 | 7个文件 | ~3000行 |
| 配置 | 3个文件 | ~100行 |
| **总计** | **19个文件** | **~5600行** |

---

## 🔍 关键概念索引

### GAI (生成式AI)
- 位置: chatbot.py
- 使用: OpenAI GPT-4o-mini
- 文档: TECHNICAL_GUIDE.md

### RAG (检索增强生成)
- 位置: rag_system.py
- 技术: ChromaDB + Sentence Transformers
- 文档: TECHNICAL_GUIDE.md, ARCHITECTURE.md

### Prompt Engineering
- 位置: prompt_engineering.py
- 策略: 系统提示词 + 上下文 + RAG
- 文档: TECHNICAL_GUIDE.md

### 持续学习
- 位置: data_system.py (LearningSystem)
- 机制: 反馈驱动的知识库扩充
- 文档: PROJECT_SUMMARY.md

### 情绪分析
- 位置: prompt_engineering.py (EmotionAnalyzer)
- 方法: 关键词检测
- 支持: 8种情绪类别

---

## 💡 使用建议

### 第一次使用
1. 先看 **README_CN.md** 了解项目
2. 按 **QUICK_REFERENCE.md** 快速部署
3. 运行 **start.sh** 启动系统
4. 体验所有功能标签页

### 开发调试
1. 运行 **test_system.py** 确保环境正常
2. 查看 **examples.py** 学习API
3. 阅读 **TECHNICAL_GUIDE.md** 了解架构
4. 修改代码并测试

### 学习研究
1. 阅读 **PROJECT_SUMMARY.md** 整体把握
2. 研究 **ARCHITECTURE.md** 理解设计
3. 深入 **TECHNICAL_GUIDE.md** 学习细节
4. 实践扩展新功能

---

## 📞 获取帮助

### 问题排查顺序

1. **README_CN.md** 的"常见问题"部分
2. **QUICK_REFERENCE.md** 的"故障排除"部分
3. 运行 **test_system.py** 诊断问题
4. 查看 **TECHNICAL_GUIDE.md** 相关章节
5. 检查代码注释和文档字符串

### 文档搜索建议

| 你想了解... | 查看文件... |
|------------|-----------|
| 如何使用 | README_CN.md, QUICK_REFERENCE.md |
| 技术原理 | TECHNICAL_GUIDE.md, ARCHITECTURE.md |
| 项目概况 | PROJECT_SUMMARY.md |
| API使用 | examples.py |
| 配置参数 | config.py, .env.example |

---

## ✅ 检查清单

开始使用前，确保：

- [ ] 已阅读 README_CN.md 或 README.md
- [ ] Python 3.8+ 已安装
- [ ] 已创建虚拟环境（推荐）
- [ ] 已安装 requirements.txt 中的依赖
- [ ] 已复制 .env.example 为 .env
- [ ] 已填写 OPENAI_API_KEY
- [ ] 已运行 init_knowledge.py
- [ ] 已运行 test_system.py 确保正常

全部完成后，运行 `python app.py` 或 `./start.sh` 启动！

---

## 🎉 享受使用！

所有文档都已准备就绪，祝你使用愉快！

**从 README_CN.md 开始，按照快速开始指南部署系统。**

---

**索引版本**: v1.0  
**更新日期**: 2025-11-12

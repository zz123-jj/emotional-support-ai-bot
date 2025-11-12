# 🎓 学习伙伴 - 大学生情绪支持AI聊天机器人

[English](README.md) | 简体中文

---

## 🌟 项目简介

**学习伙伴**是一个专为大学生设计的AI情绪支持聊天机器人，使用GPT-4o-mini模型，融合了三大前沿AI技术：

- 🤖 **生成式AI (GAI)**: 使用OpenAI GPT-4o-mini模型
- 🔍 **RAG技术**: 检索增强生成，提供基于知识库的专业建议
- ✍️ **Prompt Engineering**: 精心设计的提示词工程，确保温暖、专业的回复

---

## ✨ 主要功能

| 功能 | 说明 |
|------|------|
| 💬 智能对话 | 多轮上下文对话，理解你的困扰 |
| 🧠 情绪识别 | 自动检测8种情绪状态 |
| 📚 知识检索 | 从专业知识库中检索相关建议 |
| 📊 数据追踪 | 记录情绪趋势，生成统计报告 |
| 🎓 持续学习 | 从用户反馈中自动学习，不断优化 |
| 🌐 Web界面 | 友好的Gradio界面，易于使用 |

---

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- OpenAI API密钥 ([获取方式](https://platform.openai.com/api-keys))

### 5分钟快速部署

```bash
# 1. 进入项目目录
cd /home/calebevans/SAT101

# 2. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 OPENAI_API_KEY

# 5. 初始化知识库
python init_knowledge.py

# 6. 启动应用
python app.py
```

### 或使用一键启动脚本

```bash
chmod +x start.sh
./start.sh
```

启动后访问：**http://localhost:7860**

---

## 📖 使用指南

### 基础使用

1. **开始对话**
   - 打开浏览器访问 http://localhost:7860
   - 在聊天框输入你的问题
   - 例如："我考试前总是很焦虑"

2. **查看AI回复**
   - AI会分析你的情绪
   - 从知识库检索相关建议
   - 生成温暖、实用的回复

3. **提供反馈**
   - 对有帮助的回复打分（1-5分）
   - 帮助系统学习和改进

4. **查看统计**
   - 点击"统计分析"标签
   - 查看情绪趋势和会话数据

### 界面功能

- **💬 聊天**: 与AI进行对话
- **📊 统计分析**: 查看情绪趋势和满意度
- **🧠 系统学习**: 手动触发学习过程
- **ℹ️ 使用说明**: 查看完整的使用指南

---

## 🏗️ 技术架构

```
用户界面 (Gradio)
    ↓
聊天引擎 (Chatbot)
    ↓
┌─────────┬─────────┬─────────┬─────────┐
│ Prompt  │   RAG   │  Data   │ Emotion │
│ Builder │ System  │Collector│ Analyzer│
└─────────┴─────────┴─────────┴─────────┘
    ↓
┌─────────────┬────────────┬──────────┐
│  ChromaDB   │   SQLite   │ OpenAI   │
│ (向量数据库) │ (关系数据库)│   API    │
└─────────────┴────────────┴──────────┘
```

### 核心技术栈

| 层次 | 技术 |
|------|------|
| AI模型 | GPT-4o-mini, Sentence Transformers |
| Web框架 | Gradio 4.16.0 |
| 向量数据库 | ChromaDB 0.4.22 |
| 关系数据库 | SQLite + SQLAlchemy |
| RAG框架 | LangChain |

---

## 📁 项目结构

```
SAT101/
├── app.py                    # Gradio Web应用
├── chatbot.py                # 聊天机器人核心引擎
├── rag_system.py             # RAG检索系统
├── prompt_engineering.py     # Prompt工程
├── data_system.py            # 数据收集与学习
├── config.py                 # 配置管理
├── init_knowledge.py         # 知识库初始化
├── test_system.py            # 系统测试
├── examples.py               # 使用示例
├── start.sh                  # 启动脚本
├── requirements.txt          # 依赖列表
├── .env.example              # 环境变量模板
├── README.md                 # 英文文档
├── README_CN.md              # 中文文档（本文件）
├── TECHNICAL_GUIDE.md        # 技术详细文档
├── QUICK_REFERENCE.md        # 快速参考
├── ARCHITECTURE.md           # 架构说明
└── PROJECT_SUMMARY.md        # 项目总结
```

---

## 💻 编程API使用

```python
from chatbot import create_chatbot

# 创建机器人
bot = create_chatbot()

# 开始会话
session_id = bot.start_new_session()

# 发送消息
result = bot.chat("我感到很焦虑")
print(result['response'])  # AI的回复
print(result['detected_emotions'])  # 检测到的情绪

# 添加反馈
bot.add_feedback(
    conversation_id=result['conversation_id'],
    score=5.0,
    feedback_text="很有帮助！"
)

# 查看统计
stats = bot.get_session_stats()
print(stats)

# 触发学习
learned_count = bot.trigger_learning()
print(f"学到了 {learned_count} 条新知识")
```

---

## 🔧 配置说明

### 环境变量 (.env)

```bash
# 必须配置
OPENAI_API_KEY=sk-your-api-key-here

# 可选配置
OPENAI_MODEL=gpt-4o-mini     # AI模型
TEMPERATURE=0.7               # 回复随机性 (0-1)
MAX_TOKENS=1000               # 最大回复长度
MAX_CONVERSATION_HISTORY=10   # 保留历史消息数
```

### 参数说明

- **TEMPERATURE**: 控制回复的创造性
  - 0.0-0.3: 更确定、一致
  - 0.4-0.7: 平衡（推荐）
  - 0.8-1.0: 更有创意

- **MAX_TOKENS**: 控制回复长度
  - 推荐: 800-1200

---

## 📊 RAG技术详解

### 什么是RAG？

RAG (Retrieval-Augmented Generation) = 检索增强生成

1. **检索**: 从知识库中找到相关信息
2. **增强**: 将检索到的信息加入Prompt
3. **生成**: AI基于增强的Prompt生成回复

### 工作流程

```
用户问题 "如何缓解焦虑？"
    ↓
[向量化] → [0.23, -0.45, 0.67, ...]
    ↓
[ChromaDB检索] → 找到最相关的3个文档
    ↓
[融入Prompt] → 构建增强的提示词
    ↓
[GPT生成] → 生成基于知识库的专业回复
```

### 嵌入模型

使用 `paraphrase-multilingual-MiniLM-L12-v2`

- ✅ 支持中文
- ✅ 384维向量
- ✅ 快速高效

---

## 🎯 Prompt Engineering策略

### 提示词层次

```python
系统提示词: "你是专门为大学生提供情绪支持的AI助手..."
    +
对话历史: [用户上次说的, AI的回复, ...]
    +
知识库内容: "[参考1] 深呼吸可以缓解焦虑..."
    +
当前问题: "我很焦虑"
    ↓
完整Prompt → GPT-4o-mini → 温暖的回复
```

### 设计原则

1. **角色清晰**: 定义AI是情绪支持助手
2. **行为准则**: 温暖、简洁、实用
3. **边界意识**: 不能替代专业心理咨询
4. **上下文感知**: 保持对话连贯性

---

## 📈 持续学习机制

### 学习流程

```
用户对话 → AI回复 → 用户反馈 (1-5分)
    ↓
[评分 ≥ 4] → 标记为高质量对话
    ↓
提取知识 → 向量化 → 加入知识库
    ↓
未来回复质量提升 ✨
```

### 自动优化

- 收集高评分对话（≥4分）
- 提取有价值的问答对
- 自动扩充知识库
- 改进后续回复质量

---

## 🧪 测试系统

```bash
# 运行系统测试
python test_system.py

# 查看使用示例
python examples.py
```

测试内容：
- ✅ 配置模块
- ✅ RAG系统
- ✅ Prompt工程
- ✅ 数据系统
- ✅ 集成测试

---

## ❓ 常见问题

### Q: 启动时显示 "OPENAI_API_KEY 未设置"

**A**: 检查 `.env` 文件是否存在并正确配置：

```bash
cp .env.example .env
# 编辑 .env，填入真实的API密钥
```

### Q: 如何清空所有数据？

**A**: 删除数据库文件并重新初始化：

```bash
rm chat_history.db
rm -rf chroma_db/
python init_knowledge.py
```

### Q: 回复质量不够好怎么办？

**A**: 可以尝试：
1. 添加更多专业知识到知识库
2. 调整 `TEMPERATURE` 参数
3. 修改系统提示词
4. 多提供高质量反馈

### Q: 支持多用户吗？

**A**: 当前版本支持多会话，但推荐单用户使用。多用户需要额外配置。

---

## 🔒 隐私与安全

### 数据隐私

- ✅ 所有对话数据存储在本地
- ✅ 不会自动分享给第三方
- ✅ 可随时删除所有数据
- ⚠️ OpenAI API调用会传输消息内容（遵循OpenAI隐私政策）

### 安全建议

1. 不要将 `.env` 文件提交到Git
2. 定期清理敏感对话记录
3. 生产环境使用HTTPS
4. 限制外部访问

---

## 📚 完整文档

- **README.md**: 英文完整文档
- **README_CN.md**: 中文文档（本文件）
- **TECHNICAL_GUIDE.md**: 技术详细文档
- **QUICK_REFERENCE.md**: 快速参考指南
- **ARCHITECTURE.md**: 架构可视化
- **PROJECT_SUMMARY.md**: 项目总结

---

## 🎓 适用场景

### 学习用途
- AI课程实践项目
- 毕业设计参考
- RAG技术学习
- Prompt Engineering实践

### 实际应用
- 大学生情绪支持
- 心理健康辅助工具
- 学习压力管理
- 情绪趋势分析

---

## 💡 扩展方向

可以基于此项目扩展的功能：

1. **多模态支持**
   - 语音输入/输出
   - 图片情绪分析
   - 视频内容理解

2. **个性化功能**
   - 用户专属知识库
   - 个性化回复风格
   - 学习模式推荐

3. **专业版功能**
   - 心理咨询师后台
   - 详细数据分析报告
   - 危机预警系统
   - 转介专业服务

---

## ⚠️ 重要提醒

本系统提供情绪支持，但**不能替代专业心理咨询**。

如遇严重心理问题，请及时寻求专业帮助：
- 全国心理援助热线: **12320**
- 大学心理咨询中心（校内）
- 专业心理咨询机构

---

## 🙏 致谢

感谢以下开源项目：

- [OpenAI](https://openai.com/) - GPT模型
- [LangChain](https://github.com/langchain-ai/langchain) - RAG框架
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [Gradio](https://gradio.app/) - Web界面
- [Sentence Transformers](https://www.sbert.net/) - 文本嵌入

---

## 📄 许可证

本项目仅供教育和研究使用。

---

## 📞 联系方式

如有问题或建议：
- 提交 Issue
- 查看文档
- 运行测试脚本

---

**祝你使用愉快！记得照顾好自己的情绪健康。💙**

---

**版本**: v1.0  
**更新日期**: 2025-11-12  
**技术栈**: Python, GPT-4o-mini, RAG, Gradio

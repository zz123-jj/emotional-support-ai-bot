# 🎓 学习伙伴 - 大学生情绪支持AI聊天机器人

一个基于 GPT-4o-mini 的智能情绪支持系统，专门为大学生设计，帮助解决学习和生活中的情绪问题。

## 📋 目录

- [项目简介](#项目简介)
- [核心技术](#核心技术)
- [功能特色](#功能特色)
- [技术架构](#技术架构)
- [安装指南](#安装指南)
- [使用教程](#使用教程)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [开发文档](#开发文档)
- [常见问题](#常见问题)

---

## 🎯 项目简介

**学习伙伴** 是一个智能AI聊天机器人，旨在为大学生提供情绪支持和心理辅导。系统融合了先进的AI技术，能够：

- 🤖 **理解情绪**：智能识别用户的情绪状态（焦虑、压力、困惑等）
- 💡 **专业建议**：基于心理学知识库提供科学、实用的建议
- 📈 **持续学习**：从用户反馈中不断学习，提升回复质量
- 📊 **数据追踪**：记录情绪趋势，帮助用户了解自己

---

## 🚀 核心技术

### 1. **生成式AI (GAI)**
- 使用 **GPT-4o-mini** 模型进行自然语言理解和生成
- 温暖、共情的对话风格
- 上下文感知的连贯对话

### 2. **RAG (检索增强生成)**
- **向量数据库**：ChromaDB 存储心理支持知识库
- **语义检索**：使用 Sentence Transformers 进行多语言语义搜索
- **知识融合**：将检索到的专业知识融入AI回复

### 3. **Prompt Engineering (提示词工程)**
- 精心设计的系统提示词，定义AI角色和行为准则
- 情绪感知的动态提示词构建
- RAG增强的上下文提示词

### 4. **持续学习系统**
- 收集用户对话数据和反馈评分
- 自动从高质量对话中提取知识
- 动态扩充知识库

---

## ✨ 功能特色

### 核心功能

1. **智能对话**
   - 自然流畅的多轮对话
   - 保持对话上下文
   - 个性化回复

2. **情绪分析**
   - 自动检测情绪关键词
   - 追踪情绪变化趋势
   - 情绪分布统计

3. **知识检索**
   - 基于向量相似度的知识检索
   - 支持中文语义理解
   - 多维度知识分类（策略、建议、技巧等）

4. **数据收集**
   - 记录所有对话历史
   - 收集用户反馈评分
   - 生成会话统计报告

5. **持续学习**
   - 从高评分对话中学习
   - 自动扩充知识库
   - 优化回复质量

### 用户界面

- 💬 **聊天界面**：友好的对话窗口
- 📊 **统计面板**：查看情绪趋势和会话数据
- 🧠 **学习中心**：手动触发学习过程
- ℹ️ **使用指南**：完整的使用说明

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                         用户界面层                            │
│                    (Gradio Web Interface)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      应用逻辑层                               │
│                   (chatbot.py - 核心引擎)                    │
├──────────────┬──────────────┬──────────────┬────────────────┤
│              │              │              │                │
│   Prompt     │   RAG        │   数据        │   学习         │
│   工程模块    │   系统模块    │   收集模块    │   系统模块      │
│              │              │              │                │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │              │              │                │
┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐ ┌──────▼──────┐
│   OpenAI    │ │ ChromaDB  │ │ SQLAlchemy  │ │  Learning   │
│   API       │ │ (向量库)  │ │  (关系库)    │ │  Pipeline   │
│  GPT-4o-mini│ │           │ │             │ │             │
└─────────────┘ └───────────┘ └─────────────┘ └─────────────┘
```

### 架构层次说明

#### 1. 用户界面层
- **技术**：Gradio
- **功能**：提供Web界面，处理用户输入和显示

#### 2. 应用逻辑层
- **核心引擎** (`chatbot.py`)：整合所有模块
- **Prompt工程** (`prompt_engineering.py`)：构建高质量提示词
- **RAG系统** (`rag_system.py`)：知识检索和管理
- **数据系统** (`data_system.py`)：数据存储和分析
- **学习系统**：从反馈中持续学习

#### 3. 数据存储层
- **向量数据库** (ChromaDB)：存储知识库嵌入向量
- **关系数据库** (SQLite)：存储对话历史和用户数据

#### 4. 外部服务层
- **OpenAI API**：调用 GPT-4o-mini 模型

---

## 📦 安装指南

### 环境要求

- Python 3.8+
- pip 包管理器
- OpenAI API Key

### 步骤 1: 克隆或下载项目

```bash
cd /home/calebevans/SAT101
```

### 步骤 2: 创建虚拟环境（推荐）

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 4: 配置环境变量

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 OpenAI API Key：
```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 步骤 5: 初始化知识库

```bash
python init_knowledge.py
```

### 步骤 6: 启动应用

```bash
python app.py
```

应用将在 `http://localhost:7860` 启动。

---

## 📖 使用教程

### 基础使用

#### 1. 启动对话

1. 打开浏览器访问 `http://localhost:7860`
2. 在聊天输入框中输入你的问题或困扰
3. 例如：
   - "我最近学习压力很大，怎么办？"
   - "考试前总是很焦虑"
   - "感觉很孤独，没有朋友"

#### 2. 获得AI支持

- AI会分析你的情绪（焦虑、压力、孤独等）
- 从知识库中检索相关建议
- 提供温暖、实用的回复

#### 3. 提供反馈

- 对有帮助的回复使用滑块打分（1-5分）
- 点击"提交反馈"
- 高分反馈会帮助系统学习

#### 4. 查看统计

- 切换到"📊 统计分析"标签页
- 点击"刷新统计"
- 查看：
  - 消息数量
  - 平均满意度
  - 情绪分布
  - 知识库状态

#### 5. 触发学习

- 切换到"🧠 系统学习"标签页
- 点击"触发学习"
- 系统会从高质量对话中学习新知识

### 高级功能

#### 自定义知识库

编辑 `init_knowledge.py` 添加更多专业知识：

```python
new_knowledge = [
    {
        "content": "你的专业建议内容",
        "category": "情绪类别",
        "type": "知识类型"
    }
]
```

运行：
```bash
python init_knowledge.py
```

#### 编程API使用

```python
from chatbot import create_chatbot

# 创建机器人实例
bot = create_chatbot()

# 开始会话
session_id = bot.start_new_session()

# 发送消息
result = bot.chat("我感到很焦虑")
print(result['response'])

# 添加反馈
bot.add_feedback(
    conversation_id=result['conversation_id'],
    score=5.0
)

# 触发学习
learned_count = bot.trigger_learning()
print(f"学到了 {learned_count} 条新知识")
```

---

## 📁 项目结构

```
SAT101/
├── app.py                      # Gradio Web应用主程序
├── chatbot.py                  # 聊天机器人核心引擎
├── config.py                   # 配置管理
├── data_system.py              # 数据收集和学习系统
├── prompt_engineering.py       # Prompt工程模块
├── rag_system.py               # RAG系统实现
├── init_knowledge.py           # 知识库初始化脚本
├── requirements.txt            # Python依赖
├── .env.example                # 环境变量模板
├── .gitignore                  # Git忽略文件
├── README.md                   # 项目文档（本文件）
├── TECHNICAL_GUIDE.md          # 技术详细文档
├── chroma_db/                  # ChromaDB向量数据库（自动生成）
└── chat_history.db             # SQLite对话历史（自动生成）
```

### 核心文件说明

| 文件 | 功能 | 关键技术 |
|------|------|----------|
| `app.py` | Web界面 | Gradio |
| `chatbot.py` | 核心引擎 | 整合所有模块 |
| `rag_system.py` | RAG系统 | ChromaDB, Sentence Transformers |
| `prompt_engineering.py` | Prompt工程 | 提示词模板、情绪分析 |
| `data_system.py` | 数据系统 | SQLAlchemy, 持续学习 |
| `config.py` | 配置 | 环境变量管理 |

---

## ⚙️ 配置说明

### 环境变量 (`.env`)

```bash
# OpenAI配置
OPENAI_API_KEY=your_api_key_here    # 必须：OpenAI API密钥
OPENAI_MODEL=gpt-4o-mini            # 可选：模型名称
TEMPERATURE=0.7                      # 可选：回复随机性(0-1)
MAX_TOKENS=1000                      # 可选：最大token数

# 数据库配置
DATABASE_URL=sqlite:///./chat_history.db  # 可选：数据库URL
CHROMA_PERSIST_DIRECTORY=./chroma_db      # 可选：向量库目录

# 对话配置
MAX_CONVERSATION_HISTORY=10         # 可选：保留的历史消息数
```

### 参数调优

#### Temperature (温度)
- **范围**：0.0 - 1.0
- **低值** (0.0-0.3)：回复更确定、一致
- **中值** (0.4-0.7)：平衡创造性和一致性 ✅ 推荐
- **高值** (0.8-1.0)：回复更有创意、多样

#### MAX_TOKENS (最大令牌数)
- **范围**：100 - 4096
- **推荐**：800-1200（足够详细但不冗长）

#### RAG_TOP_K (检索数量)
在 `config.py` 中调整：
```python
RAG_TOP_K = 3  # 检索前K个相关文档
```

---

## 🔧 开发文档

### 添加新功能

#### 1. 扩展情绪类别

编辑 `config.py`：
```python
EMOTION_CATEGORIES = [
    "焦虑", "压力", "困惑", "沮丧", 
    "孤独", "疲惫", "积极", "中性",
    "愤怒",  # 新增
    "兴奋"   # 新增
]
```

编辑 `prompt_engineering.py` 的 `detect_emotion_keywords()` 方法添加关键词。

#### 2. 自定义Prompt模板

编辑 `prompt_engineering.py` 中的 `PromptTemplate` 类：
```python
SYSTEM_PROMPT = """
你是... (自定义系统提示词)
"""
```

#### 3. 添加新的知识来源

实现自定义知识加载器：
```python
def load_from_file(file_path):
    rag = RAGSystem()
    with open(file_path, 'r') as f:
        data = json.load(f)
        rag.add_knowledge_batch(data)
```

### 数据库Schema

#### Conversations表
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(100),
    user_message TEXT,
    ai_response TEXT,
    detected_emotions JSON,
    rag_docs_used JSON,
    feedback_score FLOAT,
    timestamp DATETIME
);
```

#### EmotionTrends表
```sql
CREATE TABLE emotion_trends (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(100),
    emotion VARCHAR(50),
    intensity VARCHAR(20),
    timestamp DATETIME
);
```

---

## 🧪 测试

### 单元测试示例

创建 `test_chatbot.py`：
```python
from chatbot import create_chatbot

def test_basic_chat():
    bot = create_chatbot()
    bot.start_new_session()
    
    result = bot.chat("我很焦虑")
    
    assert result['response'] is not None
    assert '焦虑' in result['detected_emotions']
    print("✅ 基础聊天测试通过")

if __name__ == "__main__":
    test_basic_chat()
```

运行测试：
```bash
python test_chatbot.py
```

---

## ❓ 常见问题

### Q1: 启动时出现 "OPENAI_API_KEY 未设置" 错误？

**A**: 确保已创建 `.env` 文件并正确填写API密钥：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### Q2: ChromaDB 报错 "No such file or directory"？

**A**: 首次运行时会自动创建。如果问题持续，手动创建目录：
```bash
mkdir -p chroma_db
```

### Q3: 如何清空所有数据重新开始？

**A**: 删除数据库文件：
```bash
rm chat_history.db
rm -rf chroma_db/
python init_knowledge.py
```

### Q4: 回复质量不够好？

**A**: 尝试以下方法：
1. 增加知识库内容（编辑 `init_knowledge.py`）
2. 调整 Temperature 参数（在 `.env` 中）
3. 优化系统提示词（在 `prompt_engineering.py` 中）
4. 提供更多高质量反馈，触发学习

### Q5: 支持多用户吗？

**A**: 当前版本支持多会话，但建议单用户使用。多用户部署需要：
- 添加用户认证系统
- 使用更强大的数据库（PostgreSQL）
- 部署到云服务器

---

## 🔒 隐私和安全

### 数据隐私

- ✅ 所有数据存储在本地
- ✅ 不会自动上传到云端
- ✅ 用户可随时删除数据
- ⚠️ OpenAI API调用会发送消息内容（遵循OpenAI隐私政策）

### 安全建议

1. **保护API密钥**：不要将 `.env` 文件提交到Git
2. **限制访问**：默认只在本地运行（127.0.0.1）
3. **定期清理**：删除敏感对话记录
4. **HTTPS部署**：生产环境使用HTTPS

---

## 📊 性能优化

### 优化建议

1. **向量检索优化**
   - 定期清理低质量知识
   - 控制知识库大小（建议<10000条）

2. **数据库优化**
   - 定期清理旧对话（保留近期数据）
   - 添加索引提升查询速度

3. **API调用优化**
   - 减少MAX_TOKENS降低成本
   - 使用缓存避免重复查询

---

## 🤝 贡献指南

欢迎贡献！可以通过以下方式参与：

1. 🐛 报告Bug
2. 💡 提出新功能建议
3. 📝 改进文档
4. 🔧 提交代码改进

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 🙏 致谢

本项目使用了以下优秀的开源项目：

- [OpenAI GPT-4o-mini](https://openai.com/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://www.trychroma.com/)
- [Gradio](https://gradio.app/)
- [Sentence Transformers](https://www.sbert.net/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: [你的邮箱]
- 💬 Issues: 在项目仓库提交Issue

---

## 🎓 学习资源

### RAG技术
- [什么是RAG？](https://docs.llamaindex.ai/en/stable/getting_started/concepts.html)
- [ChromaDB文档](https://docs.trychroma.com/)

### Prompt Engineering
- [OpenAI Prompt Engineering指南](https://platform.openai.com/docs/guides/prompt-engineering)
- [提示词工程完全指南](https://www.promptingguide.ai/)

### 情绪支持资源
- 如遇严重心理问题，请拨打心理危机热线：
  - 全国：12320
  - 北京：010-82951332

---

**祝你使用愉快！记得照顾好自己的情绪健康。💙**

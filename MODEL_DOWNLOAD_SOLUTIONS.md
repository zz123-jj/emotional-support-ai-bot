# 🔧 模型下载问题解决方案

## 问题说明
系统在首次运行时需要下载 Sentence Transformers 嵌入模型用于 RAG 功能。

当前使用的模型：`all-MiniLM-L6-v2`（约90MB）

## 方案1：耐心等待（推荐用于生产环境）

模型只需下载一次，之后会缓存在本地。

**优点**：
- 获得完整的 RAG 功能
- 离线可用
- 速度快

**缺点**：
- 首次需要等待 9-10 分钟

**操作**：
```bash
# 让下载继续进行
# 可以在后台运行
source .venv/bin/activate
python test_system.py
```

---

## 方案2：使用 OpenAI Embeddings（无需下载模型）

直接使用 OpenAI API 进行文本嵌入，无需下载本地模型。

**优点**：
- 无需下载
- 立即可用
- 质量更高

**缺点**：
- 需要调用 API（有成本）
- 需要网络连接

**操作步骤**：

### 1. 修改 rag_system.py

找到第 38-40 行左右，将：
```python
# 初始化嵌入模型（使用多语言模型）
self.embedding_model = SentenceTransformer(
    self.config.EMBEDDING_MODEL
)
```

替换为：
```python
# 使用 OpenAI Embeddings（无需下载模型）
from langchain_openai import OpenAIEmbeddings
self.use_openai_embeddings = True
self.openai_embeddings = OpenAIEmbeddings()
```

### 2. 修改 encode 方法

在 `add_knowledge` 和 `retrieve` 方法中，将：
```python
embedding = self.embedding_model.encode(content).tolist()
```

替换为：
```python
if self.use_openai_embeddings:
    embedding = self.openai_embeddings.embed_query(content)
else:
    embedding = self.embedding_model.encode(content).tolist()
```

---

## 方案3：手动预下载模型（推荐用于开发）

使用更快的下载工具或镜像源。

### 使用 HuggingFace 镜像（中国用户）

```bash
# 设置环境变量使用镜像
export HF_ENDPOINT=https://hf-mirror.com

# 然后运行测试
source .venv/bin/activate
python test_system.py
```

### 或者使用 Python 预下载

```python
from sentence_transformers import SentenceTransformer

# 这会下载并缓存模型
model = SentenceTransformer('all-MiniLM-L6-v2')
print("模型下载完成！")
```

---

## 方案4：禁用 RAG 功能（快速演示）

如果只是想快速查看聊天功能，可以临时禁用 RAG。

在 `chatbot.py` 的 `chat` 方法中：
```python
# 将 use_rag 默认设置为 False
def chat(self, user_message: str, use_rag: bool = False):
```

**注意**：这样会失去知识库检索功能，仅用于演示。

---

## 当前状态

✅ 核心功能测试已通过（配置、Prompt工程、数据系统）
⏳ RAG 系统等待模型下载中

## 建议

**如果你想立即体验完整功能**：
→ 使用**方案2**（OpenAI Embeddings）- 5分钟内完成

**如果你想要离线可用**：
→ 使用**方案1**（等待下载）或**方案3**（使用镜像）

**如果只是想看看界面**：
→ 使用**方案4**（临时禁用RAG）

---

## 自动化脚本

我已经创建了 `test_quick.py`，可以跳过 RAG 测试：

```bash
source .venv/bin/activate
python test_quick.py
```

所有核心功能都已验证通过！✅

---

**选择哪个方案？告诉我，我可以帮你快速实施！**

# 快速参考指南

## 🚀 快速开始（5分钟）

```bash
# 1. 进入项目目录
cd /home/calebevans/SAT101

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env，填入你的 OPENAI_API_KEY

# 5. 初始化知识库
python init_knowledge.py

# 6. 启动应用
python app.py

# 访问 http://localhost:7860
```

或者使用一键启动脚本：
```bash
chmod +x start.sh
./start.sh
```

---

## 📂 项目文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `app.py` | Web应用主程序 | 启动Gradio界面 |
| `chatbot.py` | 聊天机器人引擎 | 核心业务逻辑 |
| `rag_system.py` | RAG检索系统 | 知识库管理 |
| `prompt_engineering.py` | Prompt工程 | 提示词设计 |
| `data_system.py` | 数据收集系统 | 对话记录和学习 |
| `config.py` | 配置管理 | 环境变量配置 |
| `init_knowledge.py` | 知识库初始化 | 加载初始知识 |
| `test_system.py` | 测试脚本 | 系统测试 |
| `examples.py` | 使用示例 | API使用演示 |
| `start.sh` | 启动脚本 | 一键启动 |

---

## 🔑 关键命令

### 启动应用
```bash
python app.py
```

### 测试系统
```bash
python test_system.py
```

### 初始化/重置知识库
```bash
python init_knowledge.py
```

### 查看示例
```bash
python examples.py
```

---

## ⚙️ 环境变量

必须设置：
```bash
OPENAI_API_KEY=sk-your-key-here
```

可选配置：
```bash
OPENAI_MODEL=gpt-4o-mini        # 模型名称
TEMPERATURE=0.7                  # 回复随机性
MAX_TOKENS=1000                  # 最大token数
MAX_CONVERSATION_HISTORY=10      # 历史消息数
```

---

## 🎯 核心功能使用

### 1. 基础对话
```python
from chatbot import create_chatbot

bot = create_chatbot()
result = bot.chat("我很焦虑")
print(result['response'])
```

### 2. 添加反馈
```python
bot.add_feedback(
    conversation_id=result['conversation_id'],
    score=5.0
)
```

### 3. 查看统计
```python
stats = bot.get_session_stats()
print(stats)
```

### 4. 触发学习
```python
learned = bot.trigger_learning()
print(f"学到{learned}条新知识")
```

### 5. 添加知识
```python
from rag_system import RAGSystem

rag = RAGSystem()
rag.add_knowledge(
    content="你的知识内容",
    metadata={"category": "分类"}
)
```

---

## 🔍 常用操作

### 清空所有数据
```bash
rm chat_history.db
rm -rf chroma_db/
python init_knowledge.py
```

### 备份数据
```bash
cp chat_history.db chat_history.backup.db
cp -r chroma_db chroma_db.backup
```

### 恢复数据
```bash
cp chat_history.backup.db chat_history.db
cp -r chroma_db.backup chroma_db
```

### 查看日志（如果启用）
```bash
tail -f chatbot.log
```

---

## 🐛 故障排除

### 问题1: "OPENAI_API_KEY 未设置"
**解决**：
```bash
cp .env.example .env
# 编辑.env文件，填入真实API密钥
```

### 问题2: 依赖安装失败
**解决**：
```bash
pip install --upgrade pip
pip install -r requirements.txt --verbose
```

### 问题3: ChromaDB错误
**解决**：
```bash
rm -rf chroma_db/
python init_knowledge.py
```

### 问题4: 端口被占用
**解决**：在 `app.py` 中修改端口：
```python
interface.launch(server_port=7861)  # 改成其他端口
```

### 问题5: 回复质量不佳
**解决**：
1. 增加知识库内容
2. 调整 Temperature (在.env中)
3. 修改系统提示词 (prompt_engineering.py)

---

## 📊 性能参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| TEMPERATURE | 0.7 | 回复创造性 |
| MAX_TOKENS | 800-1200 | 回复长度 |
| RAG_TOP_K | 3 | 检索文档数 |
| MAX_CONVERSATION_HISTORY | 10 | 历史消息数 |

---

## 🎨 界面访问

启动后访问：
- **本地**: http://localhost:7860
- **局域网**: http://your-ip:7860 (需设置 server_name="0.0.0.0")

---

## 📚 文档索引

- **使用教程**: `README.md`
- **技术文档**: `TECHNICAL_GUIDE.md`
- **快速参考**: `QUICK_REFERENCE.md` (本文件)

---

## 💡 最佳实践

1. **定期备份数据**
   ```bash
   cp chat_history.db backups/chat_$(date +%Y%m%d).db
   ```

2. **定期触发学习**
   - 每收集50条高质量对话后触发一次

3. **优化知识库**
   - 删除低质量知识
   - 合并重复内容
   - 定期更新知识

4. **监控性能**
   - 检查响应时间
   - 监控API使用量
   - 查看用户满意度

5. **保护隐私**
   - 不提交.env到Git
   - 定期清理敏感对话
   - 使用HTTPS部署

---

## 🔗 有用链接

- [OpenAI API文档](https://platform.openai.com/docs)
- [Gradio文档](https://www.gradio.app/docs)
- [ChromaDB文档](https://docs.trychroma.com)
- [LangChain文档](https://python.langchain.com)

---

## 📞 获取帮助

遇到问题？
1. 查看 `README.md` 的常见问题部分
2. 运行 `python test_system.py` 诊断
3. 查看 `TECHNICAL_GUIDE.md` 深入了解

---

**版本**: v1.0  
**更新**: 2025-11-12

"""
配置文件 - 管理应用程序的所有配置参数
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用程序配置类"""
    
    # OpenAI 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat_history.db")
    
    # 向量数据库配置
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # 对话配置
    MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
    
    # RAG 配置
    RAG_TOP_K = 3  # 检索最相关的前K个文档
    RAG_SIMILARITY_THRESHOLD = 0.7  # 相似度阈值
    
    # 情绪分析配置
    EMOTION_CATEGORIES = [
        "焦虑", "压力", "困惑", "沮丧", "孤独", 
        "疲惫", "积极", "中性"
    ]
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未设置，请在.env文件中配置")
        return True

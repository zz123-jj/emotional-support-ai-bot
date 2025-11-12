"""
RAG系统 - 检索增强生成
实现知识库管理、向量存储和相似度检索
"""
from typing import List, Dict, Tuple
import chromadb
from chromadb.config import Settings
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import json
import os
from config import Config


class RAGSystem:
    """RAG系统类 - 管理知识库和检索"""
    
    def __init__(self):
        """初始化RAG系统"""
        self.config = Config()
        
        # 初始化向量数据库
        self.client = chromadb.PersistentClient(
            path=self.config.CHROMA_PERSIST_DIRECTORY
        )
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name="emotional_support_kb",
            metadata={"description": "大学生情绪支持知识库"}
        )
        
        # 初始化嵌入模型（使用多语言模型）
        self.embedding_model = SentenceTransformer(
            self.config.EMBEDDING_MODEL
        )
        
        # 文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
        
        # 如果知识库为空，加载初始知识
        if self.collection.count() == 0:
            self._load_initial_knowledge()
    
    def _load_initial_knowledge(self):
        """加载初始知识库"""
        initial_knowledge = [
            {
                "content": "焦虑是大学生常见的情绪问题。当你感到焦虑时，可以尝试深呼吸练习：缓慢吸气4秒，保持4秒，然后呼气4秒。重复5次可以有效缓解焦虑。",
                "category": "焦虑",
                "type": "应对策略"
            },
            {
                "content": "学习压力大时，番茄工作法很有效：专注学习25分钟，然后休息5分钟。这样可以提高效率，减少疲劳感。",
                "category": "压力",
                "type": "学习方法"
            },
            {
                "content": "感到孤独是正常的。可以主动参加学校社团活动，或者约同学一起学习、运动。建立社交联系对心理健康很重要。",
                "category": "孤独",
                "type": "社交建议"
            },
            {
                "content": "考试前的紧张可以通过积极的自我对话来缓解。告诉自己'我已经准备好了'、'我可以应对'。这种正面暗示能增强信心。",
                "category": "焦虑",
                "type": "心理调节"
            },
            {
                "content": "长时间学习导致疲惫时，要注意劳逸结合。每隔1-2小时起来走动一下，看看远处，让大脑休息。保证充足睡眠也很关键。",
                "category": "疲惫",
                "type": "健康建议"
            },
            {
                "content": "遇到学习困难感到沮丧时，可以将大目标分解成小目标。完成每个小目标都给自己一个奖励，这样能保持动力。",
                "category": "沮丧",
                "type": "目标管理"
            },
            {
                "content": "运动是缓解压力的好方法。每天30分钟的有氧运动，如跑步、游泳或快走，可以释放内啡肽，改善心情。",
                "category": "压力",
                "type": "运动建议"
            },
            {
                "content": "如果情绪问题持续影响生活和学习，建议寻求专业帮助。大学一般都有心理咨询中心，提供免费或低价的咨询服务。",
                "category": "综合",
                "type": "专业建议"
            }
        ]
        
        self.add_knowledge_batch(initial_knowledge)
    
    def add_knowledge(self, content: str, metadata: Dict = None) -> str:
        """添加单条知识到知识库"""
        # 生成嵌入向量
        embedding = self.embedding_model.encode(content).tolist()
        
        # 生成ID
        doc_id = f"doc_{self.collection.count() + 1}"
        
        # 添加到集合
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        
        return doc_id
    
    def add_knowledge_batch(self, knowledge_list: List[Dict]):
        """批量添加知识"""
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        start_id = self.collection.count() + 1
        
        for idx, item in enumerate(knowledge_list):
            content = item["content"]
            metadata = {k: v for k, v in item.items() if k != "content"}
            
            documents.append(content)
            embeddings.append(self.embedding_model.encode(content).tolist())
            metadatas.append(metadata)
            ids.append(f"doc_{start_id + idx}")
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict]:
        """检索相关知识"""
        if top_k is None:
            top_k = self.config.RAG_TOP_K
        
        # 生成查询向量
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # 检索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # 格式化结果
        retrieved_docs = []
        if results['documents'] and results['documents'][0]:
            for idx, doc in enumerate(results['documents'][0]):
                retrieved_docs.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][idx] if results['metadatas'] else {},
                    'distance': results['distances'][0][idx] if results['distances'] else 0
                })
        
        return retrieved_docs
    
    def get_knowledge_count(self) -> int:
        """获取知识库中的文档数量"""
        return self.collection.count()
    
    def clear_knowledge_base(self):
        """清空知识库"""
        self.client.delete_collection("emotional_support_kb")
        self.collection = self.client.get_or_create_collection(
            name="emotional_support_kb",
            metadata={"description": "大学生情绪支持知识库"}
        )


class KnowledgeEnricher:
    """知识增强器 - 从对话中学习新知识"""
    
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system
        self.learning_buffer = []
    
    def extract_useful_exchange(self, user_message: str, ai_response: str, 
                                feedback_score: float = None) -> Dict:
        """从对话中提取有用的知识"""
        # 如果反馈分数较高，说明这是一个好的回复
        if feedback_score and feedback_score >= 4.0:
            return {
                'content': f"用户问题：{user_message}\n有效回复：{ai_response}",
                'type': '成功案例',
                'feedback_score': feedback_score
            }
        return None
    
    def add_to_buffer(self, knowledge_item: Dict):
        """添加到学习缓冲区"""
        if knowledge_item:
            self.learning_buffer.append(knowledge_item)
    
    def commit_buffer_to_kb(self, min_buffer_size: int = 5):
        """将缓冲区的知识提交到知识库"""
        if len(self.learning_buffer) >= min_buffer_size:
            self.rag_system.add_knowledge_batch(self.learning_buffer)
            count = len(self.learning_buffer)
            self.learning_buffer = []
            return count
        return 0

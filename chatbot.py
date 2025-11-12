"""
AI聊天机器人核心引擎
整合RAG、Prompt Engineering和数据收集系统
"""
from openai import OpenAI
from typing import List, Dict, Optional
import uuid
from config import Config
from rag_system import RAGSystem, KnowledgeEnricher
from prompt_engineering import PromptBuilder, EmotionAnalyzer
from data_system import DataCollector, LearningSystem


class EmotionalSupportChatbot:
    """情绪支持聊天机器人"""
    
    def __init__(self):
        """初始化聊天机器人"""
        self.config = Config()
        self.config.validate()
        
        # 初始化OpenAI客户端
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        
        # 初始化各个系统
        self.rag_system = RAGSystem()
        self.prompt_builder = PromptBuilder()
        self.emotion_analyzer = EmotionAnalyzer()
        self.data_collector = DataCollector()
        self.learning_system = LearningSystem(self.data_collector, self.rag_system)
        self.knowledge_enricher = KnowledgeEnricher(self.rag_system)
        
        # 会话管理
        self.current_session_id = None
        self.conversation_history = []
    
    def start_new_session(self, user_id: str = None) -> str:
        """开始新会话"""
        session_id = str(uuid.uuid4())
        self.current_session_id = session_id
        self.conversation_history = []
        self.data_collector.create_session(session_id, user_id)
        return session_id
    
    def chat(self, user_message: str, use_rag: bool = True) -> Dict:
        """处理用户消息并返回AI回复"""
        
        if not self.current_session_id:
            self.start_new_session()
        
        # 1. 情绪分析
        detected_emotions = self.emotion_analyzer.detect_emotion_keywords(user_message)
        
        # 记录情绪趋势
        for emotion in detected_emotions:
            self.data_collector.record_emotion_trend(
                self.current_session_id, 
                emotion
            )
        
        # 2. RAG检索（如果启用）
        rag_docs = []
        if use_rag:
            rag_docs = self.rag_system.retrieve(user_message)
        
        # 3. 构建提示词
        messages = self.prompt_builder.build_messages(
            user_message=user_message,
            conversation_history=self.conversation_history,
            rag_docs=rag_docs if use_rag else None
        )
        
        # 4. 调用GPT-4o-mini
        try:
            response = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=messages,
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS
            )
            
            ai_response = response.choices[0].message.content
            
        except Exception as e:
            ai_response = f"抱歉，我遇到了一些技术问题：{str(e)}。请稍后再试。"
        
        # 5. 更新对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        # 保持历史记录在合理长度
        if len(self.conversation_history) > self.config.MAX_CONVERSATION_HISTORY * 2:
            self.conversation_history = self.conversation_history[-self.config.MAX_CONVERSATION_HISTORY * 2:]
        
        # 6. 记录对话到数据库
        conversation_record = self.data_collector.record_conversation(
            session_id=self.current_session_id,
            user_message=user_message,
            ai_response=ai_response,
            detected_emotions=detected_emotions,
            rag_docs=[{
                'content': doc.get('content', ''),
                'metadata': doc.get('metadata', {})
            } for doc in rag_docs]
        )
        
        # 7. 返回结果
        return {
            "response": ai_response,
            "detected_emotions": detected_emotions,
            "rag_docs_count": len(rag_docs),
            "conversation_id": conversation_record.id,
            "session_id": self.current_session_id
        }
    
    def add_feedback(self, conversation_id: int, score: float, 
                    feedback_text: str = None):
        """添加用户反馈"""
        success = self.data_collector.add_feedback(
            conversation_id, 
            score, 
            feedback_text
        )
        
        # 如果反馈良好，考虑加入学习缓冲区
        if success and score >= 4.0:
            # 获取对话记录
            conv = self.data_collector.session.query(
                self.data_collector.session.query(
                    self.data_collector.Conversation
                ).filter_by(id=conversation_id).first()
            )
            if conv:
                knowledge_item = self.knowledge_enricher.extract_useful_exchange(
                    conv.user_message,
                    conv.ai_response,
                    score
                )
                if knowledge_item:
                    self.knowledge_enricher.add_to_buffer(knowledge_item)
        
        return success
    
    def get_session_stats(self) -> Dict:
        """获取当前会话统计"""
        if not self.current_session_id:
            return {}
        
        return self.data_collector.get_session_statistics(
            self.current_session_id
        )
    
    def trigger_learning(self, min_score: float = 4.0) -> int:
        """触发学习过程"""
        # 从数据库中学习高质量对话
        learned_count = self.learning_system.learn_from_feedback(min_score)
        
        # 提交缓冲区中的知识
        buffer_count = self.knowledge_enricher.commit_buffer_to_kb(min_buffer_size=1)
        
        return learned_count + buffer_count
    
    def get_knowledge_base_info(self) -> Dict:
        """获取知识库信息"""
        return {
            "total_documents": self.rag_system.get_knowledge_count(),
            "model": self.config.EMBEDDING_MODEL
        }
    
    def reset_conversation(self):
        """重置当前对话"""
        self.conversation_history = []
        self.start_new_session()
    
    def close(self):
        """关闭系统，释放资源"""
        self.data_collector.close()


# 便捷函数
def create_chatbot() -> EmotionalSupportChatbot:
    """创建聊天机器人实例"""
    return EmotionalSupportChatbot()

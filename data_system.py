"""
数据收集和学习系统
记录对话历史、分析用户反馈、实现持续学习
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Dict, Optional
import json
from config import Config

Base = declarative_base()


class Conversation(Base):
    """对话记录表"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), index=True)  # 会话ID
    user_id = Column(String(100), index=True, nullable=True)  # 用户ID（可选）
    timestamp = Column(DateTime, default=datetime.now)
    user_message = Column(Text)  # 用户消息
    ai_response = Column(Text)  # AI回复
    detected_emotions = Column(JSON)  # 检测到的情绪
    rag_docs_used = Column(JSON)  # 使用的RAG文档
    feedback_score = Column(Float, nullable=True)  # 用户反馈评分(1-5)
    feedback_text = Column(Text, nullable=True)  # 用户反馈文本
    

class UserSession(Base):
    """用户会话表"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, index=True)
    user_id = Column(String(100), nullable=True)
    start_time = Column(DateTime, default=datetime.now)
    last_active = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    message_count = Column(Integer, default=0)
    avg_feedback_score = Column(Float, nullable=True)


class EmotionTrend(Base):
    """情绪趋势表"""
    __tablename__ = 'emotion_trends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), index=True)
    timestamp = Column(DateTime, default=datetime.now)
    emotion = Column(String(50))
    intensity = Column(String(20))  # 低/中/高


class DataCollector:
    """数据收集器"""
    
    def __init__(self):
        self.config = Config()
        
        # 创建数据库引擎
        self.engine = create_engine(self.config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        
        # 创建会话
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def create_session(self, session_id: str, user_id: str = None) -> UserSession:
        """创建新会话"""
        user_session = UserSession(
            session_id=session_id,
            user_id=user_id
        )
        self.session.add(user_session)
        self.session.commit()
        return user_session
    
    def record_conversation(self, session_id: str, user_message: str, 
                          ai_response: str, detected_emotions: List[str] = None,
                          rag_docs: List[Dict] = None) -> Conversation:
        """记录对话"""
        conversation = Conversation(
            session_id=session_id,
            user_message=user_message,
            ai_response=ai_response,
            detected_emotions=detected_emotions or [],
            rag_docs_used=rag_docs or []
        )
        self.session.add(conversation)
        
        # 更新会话信息
        user_session = self.session.query(UserSession).filter_by(
            session_id=session_id
        ).first()
        
        if user_session:
            user_session.message_count += 1
            user_session.last_active = datetime.now()
        
        self.session.commit()
        return conversation
    
    def record_emotion_trend(self, session_id: str, emotion: str, 
                            intensity: str = "中"):
        """记录情绪趋势"""
        trend = EmotionTrend(
            session_id=session_id,
            emotion=emotion,
            intensity=intensity
        )
        self.session.add(trend)
        self.session.commit()
    
    def add_feedback(self, conversation_id: int, score: float, 
                    feedback_text: str = None):
        """添加用户反馈"""
        conversation = self.session.query(Conversation).filter_by(
            id=conversation_id
        ).first()
        
        if conversation:
            conversation.feedback_score = score
            conversation.feedback_text = feedback_text
            
            # 更新会话平均评分
            session_id = conversation.session_id
            avg_score = self.session.query(Conversation).filter(
                Conversation.session_id == session_id,
                Conversation.feedback_score.isnot(None)
            ).with_entities(Conversation.feedback_score).all()
            
            if avg_score:
                scores = [s[0] for s in avg_score]
                user_session = self.session.query(UserSession).filter_by(
                    session_id=session_id
                ).first()
                if user_session:
                    user_session.avg_feedback_score = sum(scores) / len(scores)
            
            self.session.commit()
            return True
        return False
    
    def get_conversation_history(self, session_id: str, 
                                limit: int = 10) -> List[Dict]:
        """获取对话历史"""
        conversations = self.session.query(Conversation).filter_by(
            session_id=session_id
        ).order_by(Conversation.timestamp.desc()).limit(limit).all()
        
        history = []
        for conv in reversed(conversations):
            history.append({
                "role": "user",
                "content": conv.user_message,
                "timestamp": conv.timestamp.isoformat()
            })
            history.append({
                "role": "assistant",
                "content": conv.ai_response,
                "timestamp": conv.timestamp.isoformat()
            })
        
        return history
    
    def get_session_statistics(self, session_id: str) -> Dict:
        """获取会话统计信息"""
        user_session = self.session.query(UserSession).filter_by(
            session_id=session_id
        ).first()
        
        if not user_session:
            return {}
        
        # 获取情绪分布
        emotions = self.session.query(EmotionTrend).filter_by(
            session_id=session_id
        ).all()
        
        emotion_counts = {}
        for emotion_record in emotions:
            emotion = emotion_record.emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            "session_id": session_id,
            "message_count": user_session.message_count,
            "avg_feedback_score": user_session.avg_feedback_score,
            "start_time": user_session.start_time.isoformat(),
            "last_active": user_session.last_active.isoformat(),
            "emotion_distribution": emotion_counts
        }
    
    def get_high_quality_conversations(self, min_score: float = 4.0, 
                                      limit: int = 50) -> List[Dict]:
        """获取高质量对话（用于学习）"""
        conversations = self.session.query(Conversation).filter(
            Conversation.feedback_score >= min_score
        ).order_by(Conversation.timestamp.desc()).limit(limit).all()
        
        results = []
        for conv in conversations:
            results.append({
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "feedback_score": conv.feedback_score,
                "emotions": conv.detected_emotions
            })
        
        return results
    
    def close(self):
        """关闭数据库连接"""
        self.session.close()


class LearningSystem:
    """持续学习系统"""
    
    def __init__(self, data_collector: DataCollector, rag_system):
        self.data_collector = data_collector
        self.rag_system = rag_system
    
    def learn_from_feedback(self, min_score: float = 4.0):
        """从高质量反馈中学习"""
        high_quality_convs = self.data_collector.get_high_quality_conversations(
            min_score=min_score
        )
        
        learned_count = 0
        for conv in high_quality_convs:
            # 将高质量对话加入知识库
            knowledge_content = (
                f"用户问题：{conv['user_message']}\n"
                f"有效回复：{conv['ai_response']}"
            )
            
            metadata = {
                "type": "成功案例",
                "feedback_score": conv['feedback_score'],
                "emotions": conv['emotions']
            }
            
            try:
                self.rag_system.add_knowledge(knowledge_content, metadata)
                learned_count += 1
            except Exception as e:
                print(f"学习失败: {e}")
        
        return learned_count
    
    def analyze_emotion_patterns(self, session_id: str) -> Dict:
        """分析情绪模式"""
        stats = self.data_collector.get_session_statistics(session_id)
        
        if not stats.get("emotion_distribution"):
            return {"pattern": "数据不足"}
        
        # 找出主要情绪
        emotion_dist = stats["emotion_distribution"]
        main_emotion = max(emotion_dist.items(), key=lambda x: x[1])
        
        return {
            "main_emotion": main_emotion[0],
            "emotion_frequency": main_emotion[1],
            "total_messages": stats["message_count"],
            "avg_satisfaction": stats.get("avg_feedback_score")
        }

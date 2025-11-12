"""
Prompt Engineering 模块
设计和管理针对大学生情绪支持的提示词工程
"""
from typing import List, Dict
from config import Config


class PromptTemplate:
    """提示词模板类"""
    
    # 系统提示词 - 定义AI的角色和行为准则
    SYSTEM_PROMPT = """你是一个专门为大学生提供情绪支持的AI助手，名叫"学习伙伴"。

你的角色和职责：
1. 理解和共情：认真倾听学生的情绪问题，给予理解和共情
2. 积极引导：用积极、温暖的语气帮助学生应对学习和生活中的情绪挑战
3. 实用建议：提供科学、可行的情绪管理和学习方法
4. 边界意识：对于严重的心理问题，建议寻求专业心理咨询

回复原则：
- 使用温暖、友善的语气
- 回复简洁明了，一般3-5句话
- 避免说教，多用引导性问题
- 承认情绪的正常性
- 提供具体可行的建议
- 如果不确定，诚实告知并建议寻求专业帮助

重要提醒：
- 你不是专业心理咨询师，不能诊断心理疾病
- 对于自杀、自残等严重问题，务必建议立即寻求专业帮助
- 保护用户隐私，不评判用户
"""

    # 情绪识别提示词
    EMOTION_DETECTION_PROMPT = """基于以下用户消息，识别主要情绪类别（从以下选项中选择1-2个）：
焦虑、压力、困惑、沮丧、孤独、疲惫、积极、中性

用户消息：{user_message}

请以JSON格式返回：{{"emotions": ["情绪1", "情绪2"], "intensity": "低/中/高"}}
"""

    # RAG增强提示词
    RAG_ENHANCED_PROMPT = """参考以下相关知识库内容，回复用户的问题：

知识库参考：
{knowledge_context}

用户问题：{user_message}

请结合知识库内容和你的理解，给出温暖、有帮助的回复。如果知识库内容不够相关，你也可以基于你的知识给出建议。
"""

    # 对话历史整合提示词
    CONVERSATION_CONTEXT_PROMPT = """对话历史：
{conversation_history}

当前用户消息：{user_message}

请基于对话历史的上下文，给出连贯、个性化的回复。
"""


class EmotionAnalyzer:
    """情绪分析器"""
    
    @staticmethod
    def detect_emotion_keywords(message: str) -> List[str]:
        """基于关键词快速检测情绪"""
        emotion_keywords = {
            "焦虑": ["焦虑", "紧张", "担心", "害怕", "恐慌", "不安"],
            "压力": ["压力", "压力大", "负担", "承受不了", "太累了"],
            "困惑": ["困惑", "迷茫", "不知道", "怎么办", "纠结"],
            "沮丧": ["沮丧", "难过", "失落", "失望", "挫败", "痛苦"],
            "孤独": ["孤独", "寂寞", "孤单", "没人", "独自"],
            "疲惫": ["疲惫", "累", "疲劳", "困", "精疲力竭"],
            "积极": ["开心", "高兴", "好", "棒", "感谢", "进步"],
        }
        
        detected_emotions = []
        message_lower = message.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions if detected_emotions else ["中性"]


class PromptBuilder:
    """提示词构建器"""
    
    def __init__(self):
        self.config = Config()
    
    def build_system_message(self) -> Dict:
        """构建系统消息"""
        return {
            "role": "system",
            "content": PromptTemplate.SYSTEM_PROMPT
        }
    
    def build_rag_enhanced_prompt(self, user_message: str, 
                                  knowledge_docs: List[Dict]) -> str:
        """构建RAG增强的提示词"""
        # 整理知识库内容
        knowledge_context = ""
        for idx, doc in enumerate(knowledge_docs, 1):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            category = metadata.get('category', '未分类')
            knowledge_context += f"\n[参考{idx}] ({category}) {content}\n"
        
        if not knowledge_context.strip():
            knowledge_context = "暂无相关知识库内容"
        
        return PromptTemplate.RAG_ENHANCED_PROMPT.format(
            knowledge_context=knowledge_context.strip(),
            user_message=user_message
        )
    
    def build_conversation_prompt(self, user_message: str, 
                                  history: List[Dict]) -> str:
        """构建包含对话历史的提示词"""
        # 格式化对话历史
        conversation_history = ""
        for msg in history[-self.config.MAX_CONVERSATION_HISTORY:]:
            role = "用户" if msg["role"] == "user" else "助手"
            conversation_history += f"{role}: {msg['content']}\n"
        
        return PromptTemplate.CONVERSATION_CONTEXT_PROMPT.format(
            conversation_history=conversation_history.strip(),
            user_message=user_message
        )
    
    def build_messages(self, user_message: str, 
                      conversation_history: List[Dict] = None,
                      rag_docs: List[Dict] = None) -> List[Dict]:
        """构建完整的消息列表"""
        messages = [self.build_system_message()]
        
        # 添加对话历史（限制长度）
        if conversation_history:
            recent_history = conversation_history[-self.config.MAX_CONVERSATION_HISTORY:]
            messages.extend(recent_history)
        
        # 如果有RAG文档，使用增强提示词
        if rag_docs and len(rag_docs) > 0:
            enhanced_prompt = self.build_rag_enhanced_prompt(user_message, rag_docs)
            messages.append({
                "role": "user",
                "content": enhanced_prompt
            })
        else:
            messages.append({
                "role": "user",
                "content": user_message
            })
        
        return messages
    
    @staticmethod
    def create_safety_check_prompt(user_message: str) -> str:
        """创建安全检查提示词"""
        return f"""请评估以下消息是否包含以下严重问题：
- 自杀倾向
- 自残行为
- 严重抑郁症状
- 其他需要紧急专业干预的情况

消息：{user_message}

请回复：{{"is_critical": true/false, "reason": "原因说明"}}
"""

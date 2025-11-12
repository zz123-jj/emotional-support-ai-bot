"""
使用示例 - 展示如何在代码中使用聊天机器人
"""
from chatbot import create_chatbot


def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===\n")
    
    # 1. 创建机器人实例
    bot = create_chatbot()
    print("✓ 创建聊天机器人实例")
    
    # 2. 开始新会话
    session_id = bot.start_new_session(user_id="student_001")
    print(f"✓ 开始新会话: {session_id[:8]}...\n")
    
    # 3. 发送消息
    print("用户: 我最近学习压力很大，总是焦虑")
    result = bot.chat("我最近学习压力很大，总是焦虑")
    
    print(f"\nAI: {result['response']}")
    print(f"\n检测到的情绪: {result['detected_emotions']}")
    print(f"使用了 {result['rag_docs_count']} 个知识库文档\n")
    
    # 4. 继续对话
    print("用户: 具体应该怎么做？")
    result = bot.chat("具体应该怎么做？")
    print(f"\nAI: {result['response']}\n")
    
    # 5. 添加反馈
    bot.add_feedback(
        conversation_id=result['conversation_id'],
        score=5.0,
        feedback_text="非常有帮助！"
    )
    print("✓ 已提交反馈评分: 5.0/5.0\n")
    
    # 6. 查看统计
    stats = bot.get_session_stats()
    print("=== 会话统计 ===")
    print(f"消息数量: {stats['message_count']}")
    print(f"平均满意度: {stats.get('avg_feedback_score', 'N/A')}")
    print(f"情绪分布: {stats.get('emotion_distribution', {})}\n")
    
    # 7. 关闭连接
    bot.close()
    print("✓ 会话结束")


def example_rag_usage():
    """RAG系统使用示例"""
    print("\n=== RAG系统使用示例 ===\n")
    
    from rag_system import RAGSystem
    
    # 创建RAG实例
    rag = RAGSystem()
    
    # 添加自定义知识
    print("添加自定义知识...")
    rag.add_knowledge(
        content="期末考试复习时，可以使用费曼学习法：把知识讲给别人听，"
                "如果能讲清楚，说明真正理解了。",
        metadata={
            "category": "学习方法",
            "type": "复习技巧"
        }
    )
    print("✓ 知识添加成功\n")
    
    # 检索相关知识
    print("检索查询: 如何高效复习？")
    docs = rag.retrieve("如何高效复习？", top_k=3)
    
    print(f"\n找到 {len(docs)} 个相关文档:\n")
    for i, doc in enumerate(docs, 1):
        print(f"[{i}] {doc['content'][:50]}...")
        print(f"    分类: {doc['metadata'].get('category', 'N/A')}")
        print(f"    相似度: {1 - doc['distance']:.2f}\n")
    
    # 查看知识库信息
    total = rag.get_knowledge_count()
    print(f"知识库总文档数: {total}")


def example_learning_system():
    """学习系统使用示例"""
    print("\n=== 学习系统使用示例 ===\n")
    
    bot = create_chatbot()
    
    # 模拟多次对话并反馈
    print("模拟用户对话和反馈...\n")
    
    conversations = [
        ("我考试前很紧张", 5.0),
        ("如何克服拖延症？", 4.5),
        ("感觉很孤独", 4.0),
    ]
    
    for message, score in conversations:
        result = bot.chat(message)
        bot.add_feedback(result['conversation_id'], score)
        print(f"✓ 对话: '{message[:15]}...' 评分: {score}")
    
    print("\n触发学习过程...")
    learned_count = bot.trigger_learning(min_score=4.0)
    print(f"✓ 从高质量对话中学到 {learned_count} 条新知识")
    
    # 查看知识库增长
    kb_info = bot.get_knowledge_base_info()
    print(f"\n知识库当前状态:")
    print(f"  总文档数: {kb_info['total_documents']}")
    print(f"  嵌入模型: {kb_info['model']}")
    
    bot.close()


def example_emotion_analysis():
    """情绪分析示例"""
    print("\n=== 情绪分析示例 ===\n")
    
    from prompt_engineering import EmotionAnalyzer
    
    analyzer = EmotionAnalyzer()
    
    test_messages = [
        "我最近很焦虑，压力特别大",
        "感觉自己很孤独，没有朋友",
        "考试考得不错，很开心！",
        "不知道该选什么专业，很困惑",
    ]
    
    for message in test_messages:
        emotions = analyzer.detect_emotion_keywords(message)
        print(f"消息: {message}")
        print(f"情绪: {', '.join(emotions)}\n")


def example_custom_prompts():
    """自定义Prompt示例"""
    print("\n=== 自定义Prompt示例 ===\n")
    
    from prompt_engineering import PromptBuilder
    
    builder = PromptBuilder()
    
    # 构建带RAG的提示词
    rag_docs = [
        {
            'content': '深呼吸可以有效缓解焦虑',
            'metadata': {'category': '焦虑'}
        }
    ]
    
    messages = builder.build_messages(
        user_message="我很焦虑",
        conversation_history=[],
        rag_docs=rag_docs
    )
    
    print("生成的Prompt消息:\n")
    for msg in messages:
        print(f"[{msg['role']}]")
        print(f"{msg['content'][:100]}...")
        print()


def main():
    """运行所有示例"""
    print("=" * 60)
    print("学习伙伴 - 使用示例集合")
    print("=" * 60)
    print("\n注意: 这些示例需要有效的OpenAI API密钥才能运行\n")
    
    try:
        # 运行各个示例
        example_basic_usage()
        example_rag_usage()
        example_emotion_analysis()
        example_custom_prompts()
        example_learning_system()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 运行示例时出错: {e}")
        print("\n可能的原因:")
        print("1. 未设置有效的OPENAI_API_KEY")
        print("2. 网络连接问题")
        print("3. 依赖包未正确安装")
        print("\n请检查配置后重试。")


if __name__ == "__main__":
    main()

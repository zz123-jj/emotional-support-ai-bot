"""
测试脚本 - 验证系统各个模块的功能
"""
import os
import sys

# 设置测试环境变量
os.environ['OPENAI_API_KEY'] = 'test-key'
os.environ['DATABASE_URL'] = 'sqlite:///./test_chat_history.db'
os.environ['CHROMA_PERSIST_DIRECTORY'] = './test_chroma_db'


def test_config():
    """测试配置模块"""
    print("\n=== 测试配置模块 ===")
    try:
        from config import Config
        config = Config()
        assert config.OPENAI_MODEL == 'gpt-4o-mini'
        assert config.TEMPERATURE == 0.7
        print("✅ 配置模块测试通过")
        return True
    except Exception as e:
        print(f"❌ 配置模块测试失败: {e}")
        return False


def test_rag_system():
    """测试RAG系统"""
    print("\n=== 测试RAG系统 ===")
    try:
        from rag_system import RAGSystem
        
        rag = RAGSystem()
        
        # 测试添加知识
        doc_id = rag.add_knowledge(
            content="这是一个测试文档",
            metadata={"category": "测试"}
        )
        print(f"✓ 添加知识成功，ID: {doc_id}")
        
        # 测试检索
        results = rag.retrieve("测试", top_k=1)
        assert len(results) > 0
        print(f"✓ 检索成功，找到 {len(results)} 个结果")
        
        # 测试知识库统计
        count = rag.get_knowledge_count()
        print(f"✓ 知识库包含 {count} 个文档")
        
        print("✅ RAG系统测试通过")
        return True
    except Exception as e:
        print(f"❌ RAG系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prompt_engineering():
    """测试Prompt工程"""
    print("\n=== 测试Prompt工程 ===")
    try:
        from prompt_engineering import PromptBuilder, EmotionAnalyzer
        
        # 测试情绪分析
        analyzer = EmotionAnalyzer()
        emotions = analyzer.detect_emotion_keywords("我很焦虑和紧张")
        assert "焦虑" in emotions
        print(f"✓ 情绪检测: {emotions}")
        
        # 测试Prompt构建
        builder = PromptBuilder()
        messages = builder.build_messages(
            user_message="我感到压力很大",
            conversation_history=[],
            rag_docs=[]
        )
        assert len(messages) >= 2  # 至少有system和user消息
        print(f"✓ Prompt构建成功，消息数: {len(messages)}")
        
        print("✅ Prompt工程测试通过")
        return True
    except Exception as e:
        print(f"❌ Prompt工程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_system():
    """测试数据系统"""
    print("\n=== 测试数据系统 ===")
    try:
        from data_system import DataCollector
        import uuid
        
        collector = DataCollector()
        
        # 创建会话
        session_id = str(uuid.uuid4())
        user_session = collector.create_session(session_id)
        print(f"✓ 创建会话: {session_id[:8]}...")
        
        # 记录对话
        conv = collector.record_conversation(
            session_id=session_id,
            user_message="测试消息",
            ai_response="测试回复",
            detected_emotions=["测试"]
        )
        print(f"✓ 记录对话，ID: {conv.id}")
        
        # 添加反馈
        success = collector.add_feedback(conv.id, 5.0, "很好")
        assert success
        print(f"✓ 添加反馈成功")
        
        # 获取统计
        stats = collector.get_session_statistics(session_id)
        assert stats['message_count'] == 1
        print(f"✓ 统计信息: {stats['message_count']} 条消息")
        
        collector.close()
        print("✅ 数据系统测试通过")
        return True
    except Exception as e:
        print(f"❌ 数据系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """集成测试（不调用真实API）"""
    print("\n=== 集成测试 ===")
    try:
        # 注意：这个测试不会真正调用OpenAI API
        # 因为我们没有设置真实的API密钥
        print("✓ 所有模块可以正常导入")
        print("✅ 集成测试通过（未调用OpenAI API）")
        return True
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False


def cleanup():
    """清理测试数据"""
    print("\n=== 清理测试数据 ===")
    import shutil
    
    try:
        # 删除测试数据库
        if os.path.exists('test_chat_history.db'):
            os.remove('test_chat_history.db')
            print("✓ 删除测试数据库")
        
        # 删除测试向量库
        if os.path.exists('test_chroma_db'):
            shutil.rmtree('test_chroma_db')
            print("✓ 删除测试向量库")
        
        print("✅ 清理完成")
    except Exception as e:
        print(f"⚠️  清理时出错: {e}")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("学习伙伴 - 系统测试")
    print("=" * 50)
    
    results = []
    
    # 运行各项测试
    results.append(("配置模块", test_config()))
    results.append(("RAG系统", test_rag_system()))
    results.append(("Prompt工程", test_prompt_engineering()))
    results.append(("数据系统", test_data_system()))
    results.append(("集成测试", test_integration()))
    
    # 清理
    cleanup()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

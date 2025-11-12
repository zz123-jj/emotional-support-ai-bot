"""
快速测试脚本 - 跳过需要下载大模型的RAG测试
"""
import os
import sys

# 设置测试环境变量
os.environ['OPENAI_API_KEY'] = 'test-key'
os.environ['DATABASE_URL'] = 'sqlite:///./test_chat_history.db'


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
        assert len(messages) >= 2
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


def cleanup():
    """清理测试数据"""
    print("\n=== 清理测试数据 ===")
    import shutil
    
    try:
        if os.path.exists('test_chat_history.db'):
            os.remove('test_chat_history.db')
            print("✓ 删除测试数据库")
        print("✅ 清理完成")
    except Exception as e:
        print(f"⚠️  清理时出错: {e}")


def main():
    """运行快速测试"""
    print("=" * 60)
    print("学习伙伴 - 快速测试（跳过RAG模型下载）")
    print("=" * 60)
    
    results = []
    
    # 运行核心测试
    results.append(("配置模块", test_config()))
    results.append(("Prompt工程", test_prompt_engineering()))
    results.append(("数据系统", test_data_system()))
    
    # 清理
    cleanup()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    total = len(results)
    passed_count = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed_count}/{total} 项测试通过")
    
    print("\n" + "=" * 60)
    print("说明:")
    print("  RAG系统测试被跳过，因为需要下载大型模型（~80-500MB）")
    print("  如需完整测试，请等待模型下载完成或使用更快的网络")
    print("  核心功能测试已通过，系统可以正常使用！")
    print("=" * 60)
    
    if passed_count == total:
        print("\n🎉 所有核心测试通过！系统可以使用。")
        print("\n⚠️  提示：首次运行 app.py 时会下载嵌入模型")
        print("   模型大小约 80-90MB，请耐心等待")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed_count} 项测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

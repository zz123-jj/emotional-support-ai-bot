"""
Gradio Web界面
提供友好的用户交互界面
"""
import gradio as gr
from chatbot import create_chatbot
from datetime import datetime
import pandas as pd


class ChatInterface:
    """聊天界面类"""
    
    def __init__(self):
        self.bot = create_chatbot()
        self.current_conversation_id = None
    
    def chat_response(self, message, history):
        """处理聊天响应"""
        if not message.strip():
            return history, ""
        
        # 调用聊天机器人
        result = self.bot.chat(message)
        
        # 保存当前对话ID用于反馈
        self.current_conversation_id = result['conversation_id']
        
        # 格式化响应
        response = result['response']
        
        # 如果检测到情绪，添加提示
        if result['detected_emotions']:
            emotions_str = "、".join(result['detected_emotions'])
            emotion_hint = f"\n\n💭 *检测到的情绪：{emotions_str}*"
            response += emotion_hint
        
        # 更新历史
        history.append((message, response))
        
        return history, ""
    
    def submit_feedback(self, score):
        """提交反馈"""
        if self.current_conversation_id:
            self.bot.add_feedback(self.current_conversation_id, float(score))
            return "✅ 感谢您的反馈！"
        return "❌ 没有可反馈的对话"
    
    def get_statistics(self):
        """获取统计信息"""
        stats = self.bot.get_session_stats()
        kb_info = self.bot.get_knowledge_base_info()
        
        if not stats:
            return "暂无统计数据"
        
        output = f"""
## 📊 会话统计

- **会话ID**: {stats.get('session_id', 'N/A')[:8]}...
- **消息数量**: {stats.get('message_count', 0)}
- **平均满意度**: {stats.get('avg_feedback_score', 'N/A')}
- **开始时间**: {stats.get('start_time', 'N/A')}

### 情绪分布
"""
        
        emotion_dist = stats.get('emotion_distribution', {})
        if emotion_dist:
            for emotion, count in emotion_dist.items():
                output += f"\n- {emotion}: {count}次"
        else:
            output += "\n暂无情绪数据"
        
        output += f"\n\n### 知识库信息\n- **文档数量**: {kb_info['total_documents']}"
        
        return output
    
    def reset_chat(self):
        """重置对话"""
        self.bot.reset_conversation()
        return [], "✅ 对话已重置，开始新的会话！"
    
    def trigger_learning(self):
        """触发学习"""
        count = self.bot.trigger_learning()
        return f"✅ 学习完成！从高质量对话中学到了 {count} 条新知识。"
    
    def build_interface(self):
        """构建Gradio界面"""
        
        # 自定义CSS
        custom_css = """
        .gradio-container {
            font-family: 'Arial', sans-serif;
        }
        .chat-message {
            padding: 10px;
            border-radius: 10px;
        }
        """
        
        with gr.Blocks(
            title="学习伙伴 - 大学生情绪支持AI助手",
            theme=gr.themes.Soft(),
            css=custom_css
        ) as interface:
            
            gr.Markdown(
                """
                # 🎓 学习伙伴 - 大学生情绪支持AI助手
                
                欢迎使用智能情绪支持系统！我在这里倾听你的困扰，提供温暖的建议。
                
                **功能特色：**
                - 💬 智能对话理解你的情绪
                - 📚 基于知识库的专业建议（RAG技术）
                - 🧠 持续学习，越用越懂你
                - 📊 追踪你的情绪变化趋势
                """
            )
            
            with gr.Tab("💬 聊天"):
                chatbot_ui = gr.Chatbot(
                    label="对话窗口",
                    height=400,
                    show_label=True
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="输入你的消息",
                        placeholder="告诉我你的困扰或问题...",
                        lines=2,
                        scale=4
                    )
                    submit_btn = gr.Button("发送", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("🔄 重置对话")
                    
                gr.Markdown("### 💝 为这次对话打分")
                with gr.Row():
                    feedback_slider = gr.Slider(
                        minimum=1,
                        maximum=5,
                        step=1,
                        value=5,
                        label="满意度评分 (1-5)"
                    )
                    feedback_btn = gr.Button("提交反馈")
                
                feedback_output = gr.Textbox(label="反馈结果", interactive=False)
                
                # 绑定事件
                submit_btn.click(
                    self.chat_response,
                    inputs=[msg_input, chatbot_ui],
                    outputs=[chatbot_ui, msg_input]
                )
                
                msg_input.submit(
                    self.chat_response,
                    inputs=[msg_input, chatbot_ui],
                    outputs=[chatbot_ui, msg_input]
                )
                
                clear_btn.click(
                    self.reset_chat,
                    outputs=[chatbot_ui, feedback_output]
                )
                
                feedback_btn.click(
                    self.submit_feedback,
                    inputs=[feedback_slider],
                    outputs=[feedback_output]
                )
            
            with gr.Tab("📊 统计分析"):
                gr.Markdown("### 查看你的情绪趋势和会话统计")
                
                stats_btn = gr.Button("刷新统计", variant="primary")
                stats_output = gr.Markdown()
                
                stats_btn.click(
                    self.get_statistics,
                    outputs=[stats_output]
                )
            
            with gr.Tab("🧠 系统学习"):
                gr.Markdown(
                    """
                    ### 持续学习系统
                    
                    系统会从高质量的对话中学习（评分≥4分的对话）。
                    点击下方按钮手动触发学习过程。
                    """
                )
                
                learn_btn = gr.Button("触发学习", variant="primary")
                learn_output = gr.Textbox(label="学习结果", interactive=False)
                
                learn_btn.click(
                    self.trigger_learning,
                    outputs=[learn_output]
                )
            
            with gr.Tab("ℹ️ 使用说明"):
                gr.Markdown(
                    """
                    ## 📖 使用指南
                    
                    ### 如何使用
                    
                    1. **开始对话**：在"聊天"标签页，输入你的问题或困扰
                    2. **获得支持**：AI会分析你的情绪，提供个性化建议
                    3. **提供反馈**：对有帮助的回复打分，帮助系统学习
                    4. **查看统计**：在"统计分析"标签页查看情绪趋势
                    
                    ### 技术特色
                    
                    - **RAG技术**：检索增强生成，提供基于知识库的专业建议
                    - **Prompt Engineering**：精心设计的提示词，确保温暖、专业的回复
                    - **持续学习**：从用户反馈中学习，不断优化回复质量
                    - **情绪分析**：自动识别和追踪你的情绪状态
                    
                    ### 隐私说明
                    
                    - 所有对话数据存储在本地数据库
                    - 不会分享给第三方
                    - 仅用于改进服务质量
                    
                    ### 重要提醒
                    
                    ⚠️ 本系统提供情绪支持，但**不能替代专业心理咨询**。
                    如遇严重心理问题，请及时寻求专业帮助。
                    
                    ---
                    
                    💡 **小贴士**：定期查看统计数据，了解自己的情绪模式！
                    """
                )
        
        return interface


def launch_app():
    """启动应用"""
    app = ChatInterface()
    interface = app.build_interface()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    launch_app()

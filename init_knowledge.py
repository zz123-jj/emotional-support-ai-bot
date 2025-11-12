"""
初始化知识库脚本
用于添加更多专业的心理支持知识
"""
from rag_system import RAGSystem


def initialize_knowledge_base():
    """初始化或扩充知识库"""
    
    rag = RAGSystem()
    
    # 扩展知识库
    extended_knowledge = [
        {
            "content": "拖延症是很多大学生面临的问题。可以使用'两分钟规则'：如果一件事不超过两分钟就能完成，立即去做。这能帮助你克服开始的障碍。",
            "category": "拖延",
            "type": "行为策略"
        },
        {
            "content": "睡眠问题会严重影响情绪和学习效率。建议保持规律作息，睡前1小时避免使用电子设备，可以尝试冥想或听轻音乐帮助入睡。",
            "category": "睡眠",
            "type": "健康建议"
        },
        {
            "content": "完美主义可能带来过度焦虑。学会接受'足够好'的标准，记住进步比完美更重要。给自己犯错的空间。",
            "category": "焦虑",
            "type": "认知调整"
        },
        {
            "content": "感到overwhelmed（不堪重负）时，停下来列出所有待办事项，按优先级排序，一次只专注一件事。这能让你重获控制感。",
            "category": "压力",
            "type": "时间管理"
        },
        {
            "content": "正念练习对减压很有效：专注当下，观察自己的呼吸、身体感觉和周围环境，不加评判。每天5-10分钟就有效果。",
            "category": "压力",
            "type": "放松技巧"
        },
        {
            "content": "人际关系压力是常见的。记住：你无法让所有人都喜欢你，也没必要。专注于建立几段真诚、深入的友谊。",
            "category": "人际关系",
            "type": "社交建议"
        },
        {
            "content": "写情绪日记是很好的自我疗愈方式。每天花10分钟记录感受和想法，有助于理清思路，发现情绪模式。",
            "category": "综合",
            "type": "自我疗愈"
        },
        {
            "content": "学习动力不足时，重新审视你的目标。问自己：为什么选择这个专业？未来想成为什么样的人？找到内在驱动力。",
            "category": "困惑",
            "type": "目标设定"
        },
        {
            "content": "适度的体育锻炼能显著改善情绪。不需要高强度，散步、瑜伽或骑自行车都很好。关键是规律进行。",
            "category": "情绪低落",
            "type": "运动建议"
        },
        {
            "content": "感到孤独时，主动伸出援手帮助他人。志愿活动或帮助同学，能建立联结感，同时提升自我价值感。",
            "category": "孤独",
            "type": "社交建议"
        }
    ]
    
    print(f"开始扩充知识库...")
    rag.add_knowledge_batch(extended_knowledge)
    print(f"✅ 成功添加 {len(extended_knowledge)} 条知识")
    print(f"📚 知识库总计：{rag.get_knowledge_count()} 条文档")


if __name__ == "__main__":
    initialize_knowledge_base()

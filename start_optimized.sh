#!/bin/bash

# 优化的启动脚本 - 支持模型镜像加速
# 用于一键部署和运行系统

echo "=================================="
echo "学习伙伴 - 优化启动脚本"
echo "=================================="
echo ""

# 询问是否使用国内镜像
read -p "是否使用 HuggingFace 镜像加速模型下载？(y/n，推荐中国用户选择y): " use_mirror

if [ "$use_mirror" = "y" ] || [ "$use_mirror" = "Y" ]; then
    export HF_ENDPOINT=https://hf-mirror.com
    echo "✓ 已启用 HuggingFace 镜像"
    echo ""
fi

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"
echo ""

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
    echo "✓ 虚拟环境已创建"
else
    echo "✓ 虚拟环境已存在"
fi
echo ""

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate
echo "✓ 虚拟环境已激活"
echo ""

# 安装依赖
echo "检查依赖..."
if [ ! -f ".venv/bin/gradio" ]; then
    echo "安装Python依赖包（首次运行可能需要几分钟）..."
    pip install -r requirements.txt -q
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已安装"
fi
echo ""

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠️  警告: .env 文件不存在"
    echo "从模板创建 .env 文件..."
    cp .env.example .env
    echo ""
    echo "❗ 重要: 请编辑 .env 文件，填入你的 OPENAI_API_KEY"
    echo "然后重新运行此脚本"
    echo ""
    exit 1
else
    echo "✓ 环境变量文件存在"
    
    # 检查API密钥是否设置
    if grep -q "your_openai_api_key_here" .env; then
        echo ""
        echo "❗ 警告: 检测到默认API密钥"
        echo "请编辑 .env 文件，填入你的真实 OPENAI_API_KEY"
        echo ""
        exit 1
    fi
fi
echo ""

# 询问是否运行快速测试
read -p "是否先运行快速测试（跳过模型下载）？(y/n): " run_quick_test

if [ "$run_quick_test" = "y" ] || [ "$run_quick_test" = "Y" ]; then
    echo ""
    echo "=================================="
    echo "运行快速测试..."
    echo "=================================="
    echo ""
    python test_quick.py
    echo ""
    read -p "测试通过！是否继续启动应用？(y/n): " continue_start
    if [ "$continue_start" != "y" ] && [ "$continue_start" != "Y" ]; then
        echo "启动已取消"
        exit 0
    fi
fi

# 初始化知识库
if [ ! -d "chroma_db" ]; then
    echo "初始化知识库..."
    echo "⚠️  注意：首次运行会下载嵌入模型（约90MB），请耐心等待"
    echo ""
    python init_knowledge.py
    echo "✓ 知识库初始化完成"
else
    echo "✓ 知识库已存在"
fi
echo ""

# 启动应用
echo "=================================="
echo "启动应用..."
echo "=================================="
echo ""
echo "应用将在 http://localhost:7860 启动"
echo "按 Ctrl+C 停止应用"
echo ""

python app.py

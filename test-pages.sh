#!/bin/bash

echo "🧪 MBTI 研究实验室 - GitHub Pages 测试脚本"
echo "=========================================="

# 定义基础URL
BASE_URL="https://tangentdomain.github.io/mbti-research-lab"

# 测试页面列表
pages=(
    "index.html"
    "mbti-battle-arena.html"
    "mbti-personality-radar.html"
    "mbti-16-personal-hard-power-ranking.html"
    "intj-entj-comparison.html"
    "mbti-quiz.html"
)

echo "📋 测试页面访问性..."
echo ""

for page in "${pages[@]}"; do
    url="${BASE_URL}/${page}"
    echo "🔍 测试: $page"

    # 使用curl检查页面是否可访问
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200"; then
        echo "✅ $page - 访问正常"
    else
        echo "❌ $page - 访问失败"
    fi
    echo ""
done

echo "🌐 测试主站..."
if curl -s -o /dev/null -w "%{http_code}" "$BASE_URL" | grep -q "200"; then
    echo "✅ 主站 - 访问正常"
else
    echo "❌ 主站 - 访问失败"
fi

echo ""
echo "📊 完整测试报告"
echo "=================="
echo "主站地址: $BASE_URL"
echo "竞技场: $BASE_URL/mbti-battle-arena.html"
echo "雷达图: $BASE_URL/mbti-personality-radar.html"
echo "排名页: $BASE_URL/mbti-16-personal-hard-power-ranking.html"
echo "对比页: $BASE_URL/intj-entj-comparison.html"
echo "测试页: $BASE_URL/mbti-quiz.html"
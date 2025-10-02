#!/bin/bash

# MBTI Research Lab 推送到GitHub脚本
echo "🚀 开始推送MBTI Research Lab到GitHub..."

# 检查git状态
echo "📋 检查当前状态..."
git status

# 添加所有文件
echo "📁 添加所有文件到暂存区..."
git add .

# 创建提交
echo "💾 创建提交..."
git commit -m "$(cat <<'EOF'
添加MBTI研究实验室项目文件

- 添加多个MBTI分析HTML页面
- 包含MBTI性格雷达图、战斗力竞技场等功能
- 添加国庆节庆祝页面
- 更新项目文档

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

echo "✅ 推送完成！"
echo "🌐 访问 https://github.com/TangentDomain/mbti-research-lab 查看项目"
#!/bin/bash

echo "🚀 CCDebugger Landing Page - GitHub Repository Setup"
echo "=================================================="

# 讀取用戶輸入
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your repository name (e.g., ccdebugger-landing): " REPO_NAME

# 更新 next.config.js 中的 basePath
echo "📝 Updating next.config.js with your repository name..."
sed -i.bak "s|/ccdebugger-landing|/$REPO_NAME|g" next.config.js
rm next.config.js.bak

# 初始化 git（如果需要）
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# 添加所有文件
echo "📦 Adding files to git..."
git add .
git commit -m "Initial commit - CCDebugger Landing Page"

# 設置遠程倉庫
echo "🔗 Setting up remote repository..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo ""
echo "2. Push your code:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to GitHub Pages:"
echo "   ./scripts/deploy-github-pages.sh"
echo ""
echo "4. Configure GitHub Pages in repository settings"
echo ""
echo "Your site will be available at:"
echo "https://$GITHUB_USERNAME.github.io/$REPO_NAME"
#!/bin/bash

echo "🚀 Deploying CCDebugger Landing Page to GitHub Pages"
echo "=================================================="

# 確保在正確的目錄
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# 檢查是否有 git 倉庫
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# 構建項目
echo "🔨 Building project for GitHub Pages..."
npm run build

# 檢查構建是否成功
if [ $? -ne 0 ]; then
    echo "❌ Build failed! Please fix errors before deploying."
    exit 1
fi

# 添加 .nojekyll 文件以支持 Next.js 的 _next 目錄
echo "📝 Adding .nojekyll file..."
touch out/.nojekyll

# 檢查是否有 gh-pages 分支
if git show-ref --verify --quiet refs/heads/gh-pages; then
    echo "🔄 gh-pages branch exists, updating..."
else
    echo "🌿 Creating gh-pages branch..."
    git checkout --orphan gh-pages
    git rm -rf .
    git checkout main
fi

# 提交 out 目錄
echo "📦 Committing build files..."
git add out/ -f
git commit -m "Deploy to GitHub Pages - $(date)"

# 推送到 gh-pages 分支
echo "🌐 Pushing to GitHub Pages..."
git subtree push --prefix out origin gh-pages

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository settings"
echo "2. Navigate to Pages section"
echo "3. Set source to 'Deploy from a branch'"
echo "4. Select 'gh-pages' branch and '/ (root)' folder"
echo "5. Your site will be available at:"
echo "   https://[your-username].github.io/[repository-name]"
echo ""
echo "🔗 Don't forget to update the basePath in next.config.js"
echo "   to match your repository name!"
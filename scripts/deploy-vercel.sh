#!/bin/bash

echo "🚀 Deploying CCDebugger Landing Page to Vercel"
echo "============================================="

# 檢查是否安裝了 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm i -g vercel
fi

# 構建項目
echo "🔨 Building project..."
npm run build

# 檢查構建是否成功
if [ $? -ne 0 ]; then
    echo "❌ Build failed! Please fix errors before deploying."
    exit 1
fi

echo "✅ Build successful!"

# 部署到 Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Visit your deployment URL"
echo "2. Configure custom domain in Vercel dashboard"
echo "3. Set up environment variables if needed"
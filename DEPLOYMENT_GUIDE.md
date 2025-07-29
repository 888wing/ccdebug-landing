# CCDebugger Landing Page 部署指南

## 🚀 部署選項

### 選項 1: Vercel (推薦)

Vercel 是 Next.js 的官方部署平台，提供最佳性能和開發體驗。

#### 快速部署步驟：

1. **安裝 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **登錄 Vercel**
   ```bash
   vercel login
   ```

3. **部署項目**
   ```bash
   vercel
   ```

4. **生產部署**
   ```bash
   vercel --prod
   ```

#### 使用 GitHub 自動部署：

1. 將代碼推送到 GitHub
2. 訪問 [vercel.com](https://vercel.com)
3. 導入 GitHub 項目
4. 自動部署完成！

### 選項 2: Netlify

#### 快速部署步驟：

1. **構建項目**
   ```bash
   npm run build
   ```

2. **安裝 Netlify CLI**
   ```bash
   npm i -g netlify-cli
   ```

3. **部署**
   ```bash
   netlify deploy
   netlify deploy --prod
   ```

### 選項 3: GitHub Pages

1. **安裝 gh-pages**
   ```bash
   npm install --save-dev gh-pages
   ```

2. **添加部署腳本到 package.json**
   ```json
   "scripts": {
     "deploy": "next build && next export && gh-pages -d out"
   }
   ```

3. **部署**
   ```bash
   npm run deploy
   ```

## 🔧 環境變量配置

創建 `.env.production` 文件：

```env
NEXT_PUBLIC_API_URL=https://api.ccdebugger.com
NEXT_PUBLIC_GITHUB_URL=https://github.com/yourusername/ccdebugger
NEXT_PUBLIC_DOCS_URL=https://docs.ccdebugger.com
```

## 📊 性能優化

### 1. 圖片優化
- 使用 Next.js Image 組件
- 提供 WebP 格式
- 設置適當的尺寸

### 2. 字體優化
- 使用 next/font 加載字體
- 預加載關鍵字體

### 3. SEO 優化
更新 `src/app/layout.tsx` 中的元數據：

```typescript
export const metadata = {
  title: 'CCDebugger - AI-Powered Error Analysis for Claude Code',
  description: 'Transform error messages into actionable debug prompts with AI-powered analysis',
  keywords: 'ccdebugger, claude code, error analysis, debugging, AI',
  openGraph: {
    title: 'CCDebugger',
    description: 'AI-Powered Error Analysis for Claude Code',
    url: 'https://ccdebugger.com',
    siteName: 'CCDebugger',
    images: [{
      url: 'https://ccdebugger.com/og-image.png',
      width: 1200,
      height: 630,
    }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CCDebugger',
    description: 'AI-Powered Error Analysis for Claude Code',
    images: ['https://ccdebugger.com/twitter-image.png'],
  },
}
```

## 🌐 自定義域名

### Vercel
1. 在 Vercel 控制台添加域名
2. 配置 DNS 記錄：
   - A 記錄：76.76.21.21
   - CNAME：cname.vercel-dns.com

### Netlify
1. 在 Netlify 控制台添加域名
2. 配置 DNS 記錄指向 Netlify

## 📱 Progressive Web App (PWA)

添加 PWA 支持：

1. **創建 manifest.json**
   ```json
   {
     "name": "CCDebugger",
     "short_name": "CCDebugger",
     "description": "AI-Powered Error Analysis",
     "theme_color": "#000000",
     "background_color": "#ffffff",
     "display": "standalone",
     "orientation": "portrait",
     "scope": "/",
     "start_url": "/",
     "icons": [
       {
         "src": "/icon-192.png",
         "sizes": "192x192",
         "type": "image/png"
       },
       {
         "src": "/icon-512.png",
         "sizes": "512x512",
         "type": "image/png"
       }
     ]
   }
   ```

2. **添加到 layout.tsx**
   ```html
   <link rel="manifest" href="/manifest.json" />
   ```

## 📈 監控和分析

### 添加 Google Analytics

1. **安裝**
   ```bash
   npm install @next/third-parties
   ```

2. **配置**
   ```typescript
   import { GoogleAnalytics } from '@next/third-parties/google'
   
   export default function RootLayout() {
     return (
       <html>
         <body>
           {children}
           <GoogleAnalytics gaId="G-YOUR-GA-ID" />
         </body>
       </html>
     )
   }
   ```

## 🛡️ 安全建議

1. **添加安全標頭**
   ```javascript
   // next.config.js
   module.exports = {
     async headers() {
       return [
         {
           source: '/:path*',
           headers: [
             {
               key: 'X-Frame-Options',
               value: 'DENY'
             },
             {
               key: 'X-Content-Type-Options',
               value: 'nosniff'
             },
             {
               key: 'X-XSS-Protection',
               value: '1; mode=block'
             }
           ]
         }
       ]
     }
   }
   ```

2. **啟用 HTTPS**（自動在 Vercel/Netlify）

## 🚦 部署檢查清單

- [ ] 環境變量已配置
- [ ] 構建無錯誤 (`npm run build`)
- [ ] SEO 元數據已更新
- [ ] 圖片資源已優化
- [ ] 404 頁面已創建
- [ ] robots.txt 已配置
- [ ] sitemap.xml 已生成
- [ ] 性能測試通過
- [ ] 移動端測試完成
- [ ] 深色模式測試完成

## 🎯 下一步

1. 選擇部署平台（推薦 Vercel）
2. 配置自定義域名
3. 設置 CI/CD 自動部署
4. 添加監控和分析
5. 定期更新內容
# GitHub Pages 部署設置指南

## 🚀 快速開始

### 1. 初始設置

首先，確保您的項目配置正確：

```bash
# 1. 修改 next.config.js 中的 basePath
# 將 'ccdebugger-landing' 替換為您的 GitHub 倉庫名稱
```

### 2. 初始化 Git 倉庫

```bash
cd /Users/chuisiufai/Desktop/PhotoflowAI/ccdebugger-landing

# 初始化 git（如果尚未初始化）
git init
git add .
git commit -m "Initial commit"

# 添加 GitHub 遠程倉庫
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. 使用自動部署腳本

```bash
# 運行部署腳本
./scripts/deploy-github-pages.sh
```

### 4. 配置 GitHub Pages

1. 訪問您的 GitHub 倉庫
2. 點擊 **Settings** 標籤
3. 在左側菜單中找到 **Pages**
4. 在 **Source** 部分：
   - 選擇 **Deploy from a branch**
   - Branch: 選擇 **gh-pages**
   - Folder: 選擇 **/ (root)**
5. 點擊 **Save**

### 5. 等待部署完成

- GitHub Pages 通常需要幾分鐘來部署
- 您可以在 Actions 標籤中查看部署狀態
- 部署完成後，訪問：`https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

## 🔧 手動部署步驟

如果自動腳本不工作，可以手動部署：

```bash
# 1. 構建項目
npm run build

# 2. 添加 .nojekyll 文件
touch out/.nojekyll

# 3. 創建 gh-pages 分支
git checkout --orphan gh-pages
git rm -rf .

# 4. 添加構建文件
cp -r out/* .
git add .
git commit -m "Deploy to GitHub Pages"

# 5. 推送到 GitHub
git push origin gh-pages

# 6. 切換回 main 分支
git checkout main
```

## 📝 重要配置

### next.config.js 配置

確保您的 `next.config.js` 包含正確的配置：

```javascript
const nextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/YOUR_REPO_NAME' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/YOUR_REPO_NAME' : '',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}
```

### 路徑注意事項

由於使用了 basePath，所有內部鏈接都需要使用 Next.js 的 Link 組件：

```tsx
import Link from 'next/link'

// 正確 ✅
<Link href="/blog">Blog</Link>

// 錯誤 ❌
<a href="/blog">Blog</a>
```

對於圖片，使用相對路徑：

```tsx
// 正確 ✅
<img src="./logo.png" alt="Logo" />

// 或使用 Next.js Image（配置 unoptimized: true）
import Image from 'next/image'
<Image src="/logo.png" alt="Logo" width={100} height={100} />
```

## 🔄 更新部署

每次更新內容後，只需運行：

```bash
./scripts/deploy-github-pages.sh
```

或使用 GitHub Actions 自動部署（推送到 main 分支時自動觸發）。

## 🐛 常見問題

### 1. 404 錯誤
- 確保 `basePath` 與您的倉庫名稱匹配
- 檢查是否添加了 `.nojekyll` 文件
- 確保 `trailingSlash: true` 已設置

### 2. 樣式丟失
- 檢查 `assetPrefix` 配置
- 確保所有資源使用相對路徑

### 3. 路由不工作
- 使用 Next.js 的 Link 組件
- 確保 `output: 'export'` 已設置

### 4. 圖片不顯示
- 設置 `images.unoptimized: true`
- 使用正確的相對路徑

## 🌟 自定義域名

如果您有自定義域名：

1. 在 `out` 目錄創建 `CNAME` 文件：
   ```bash
   echo "ccdebugger.com" > out/CNAME
   ```

2. 在 DNS 設置中添加：
   - A 記錄：185.199.108.153
   - A 記錄：185.199.109.153
   - A 記錄：185.199.110.153
   - A 記錄：185.199.111.153

3. 在 GitHub Pages 設置中配置自定義域名

## 📊 監控

添加 Google Analytics：

1. 在 `src/app/layout.tsx` 中添加：
   ```tsx
   <Script
     src={`https://www.googletagmanager.com/gtag/js?id=G-YOUR-ID`}
     strategy="afterInteractive"
   />
   <Script id="google-analytics" strategy="afterInteractive">
     {`
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', 'G-YOUR-ID');
     `}
   </Script>
   ```

## ✅ 部署檢查清單

- [ ] 修改 `next.config.js` 中的 `basePath`
- [ ] 運行 `npm run build` 測試構建
- [ ] 確保所有鏈接使用 Next.js Link 組件
- [ ] 添加 `.nojekyll` 文件
- [ ] 推送代碼到 GitHub
- [ ] 運行部署腳本
- [ ] 配置 GitHub Pages 設置
- [ ] 測試部署的網站
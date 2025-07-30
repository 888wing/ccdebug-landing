# CCDebugger Logo 使用指南

## Logo 設計理念

CCDebugger 的 logo 結合了兩個核心概念：
- **放大鏡**：代表調試、搜索和分析
- **錯誤符號 `<X>`**：代表程式碼錯誤和 bug

這個設計簡潔明瞭，在各種尺寸和背景下都能保持清晰可辨識。

## Logo 檔案

### 主要圖標（Chrome Extension 使用）
- `assets/icons/icon-16.png` - 16x16 像素
- `assets/icons/icon-32.png` - 32x32 像素
- `assets/icons/icon-48.png` - 48x48 像素
- `assets/icons/icon-128.png` - 128x128 像素

### Logo 變體
所有變體都在 `logo_variants/` 目錄：

1. **標準版本** (`logo-*.png`)
   - 白底黑圖
   - 適用於大多數場景

2. **深色模式** (`logo-dark-*.png`)
   - 黑底白圖
   - 適用於深色背景

3. **透明背景** (`logo-transparent-*.png`)
   - 無背景
   - 可疊加在任何顏色上

4. **輪廓版本** (`logo-outline-*.png`)
   - 只有輪廓線條
   - 更輕量的視覺效果

5. **彩色版本**
   - `logo-blue-*.png` - 藍色主題
   - `logo-red-*.png` - 紅色主題（錯誤/警告）
   - `logo-green-*.png` - 綠色主題（成功）
   - `logo-purple-*.png` - 紫色主題

### 向量格式
- `ccdebugger-logo.svg` - 完整版 SVG
- `ccdebugger-logo-minimal.svg` - 極簡版 SVG（支援 currentColor）

## 使用場景

### Chrome Extension
```json
"icons": {
  "16": "assets/icons/icon-16.png",
  "32": "assets/icons/icon-32.png",
  "48": "assets/icons/icon-48.png",
  "128": "assets/icons/icon-128.png"
}
```

### 網站使用
```html
<!-- 標準 logo -->
<img src="logo-128.png" alt="CCDebugger Logo" width="64" height="64">

<!-- SVG 版本（可縮放） -->
<img src="ccdebugger-logo.svg" alt="CCDebugger Logo" width="128" height="128">

<!-- 響應式深色模式 -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-dark-128.png">
  <img src="logo-128.png" alt="CCDebugger Logo">
</picture>
```

### CSS 中使用 SVG
```css
.icon-ccdebugger {
  background-image: url('ccdebugger-logo-minimal.svg');
  width: 24px;
  height: 24px;
  color: #000; /* SVG 會使用這個顏色 */
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .icon-ccdebugger {
    color: #fff;
  }
}
```

## 顏色規範

### 標準配色
- **主色（黑）**: `#000000`
- **背景（白）**: `#FFFFFF`

### 品牌色彩
- **藍色版本**: `#1E3A8A` (背景) / `#FFFFFF` (圖標)
- **錯誤紅色**: `#DC2626` (背景) / `#FFFFFF` (圖標)
- **成功綠色**: `#059669` (背景) / `#FFFFFF` (圖標)
- **特色紫色**: `#7C3AED` (背景) / `#FFFFFF` (圖標)

## 使用規範

### ✅ 建議做法
- 保持足夠的留白空間
- 確保在背景上有足夠對比度
- 使用提供的標準尺寸
- 保持圖標的完整性

### ❌ 避免做法
- 不要拉伸或壓縮 logo
- 不要旋轉 logo
- 不要改變 logo 的比例
- 不要在複雜背景上使用

## 特殊用途

### 作為載入動畫
可以使用 CSS 動畫讓放大鏡旋轉：
```css
@keyframes search {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading .icon-ccdebugger {
  animation: search 2s linear infinite;
}
```

### 錯誤狀態指示
使用紅色版本表示錯誤：
```html
<img src="logo-red-32.png" alt="Error" class="error-indicator">
```

## 檔案大小優化

- PNG 格式已經過優化壓縮
- 建議在網頁使用時採用適當的尺寸
- SVG 檔案最小，適合需要縮放的場景

## 授權

此 logo 是 CCDebugger 專案的一部分，遵循專案的開源授權。
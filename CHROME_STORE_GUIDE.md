# Chrome Web Store 上架指南

本指南將引導您完成 CCDebugger Chrome Extension 的上架流程。

## 前置準備

### 1. 已完成項目 ✅
- ✅ Chrome Extension 開發完成
- ✅ 所有核心功能測試通過（Shell、Docker 分析器）
- ✅ 建立生產版本 (`dist/` 目錄)
- ✅ 創建 ZIP 文件 (`ccdebugger-extension.zip`)
- ✅ 生成所需圖標（16x16, 32x32, 48x48, 128x128）
- ✅ 準備商店資源（在 `store_assets/` 目錄）

### 2. 需要準備的額外資料
- Google 開發者帳號（一次性費用 $5 USD）
- 隱私權政策 URL
- 服務條款 URL（可選）
- 支援網站/文檔 URL

## 測試擴展

### 本地測試步驟
1. 打開 Chrome 瀏覽器
2. 進入 `chrome://extensions/`
3. 開啟右上角的「開發者模式」
4. 點擊「載入未封裝項目」
5. 選擇 `dist/` 目錄
6. 測試功能：
   - 點擊擴展圖標查看 popup
   - 訪問有錯誤的網頁測試錯誤偵測
   - 打開 DevTools 查看 CCDebugger 面板
   - 測試選項頁面功能

## Chrome Web Store 上架步驟

### 步驟 1：註冊開發者帳號
1. 訪問 [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
2. 使用 Google 帳號登入
3. 支付一次性註冊費 $5 USD
4. 完成開發者資料設定

### 步驟 2：準備商店列表資訊

#### 基本資訊
- **擴展名稱**: CCDebugger - AI Error Assistant
- **簡短描述** (132 字符以內):
  ```
  AI-powered error debugging assistant that provides instant solutions for JavaScript, Python, and more
  ```

- **詳細描述**:
  ```
  CCDebugger is your intelligent debugging companion that helps developers fix errors faster with AI-powered analysis.

  🚀 Key Features:
  • Real-time error detection and analysis
  • AI-powered suggestions and solutions
  • Support for multiple languages: JavaScript, TypeScript, Python, Go, Rust, Shell, Docker, and more
  • Chrome DevTools integration
  • Bilingual support (English/Chinese)
  • Offline fallback analysis

  🔍 How it works:
  1. CCDebugger automatically detects errors on web pages
  2. Analyzes error patterns using advanced AI
  3. Provides actionable solutions with code examples
  4. Integrates seamlessly with Chrome DevTools

  💡 Perfect for:
  • Web developers debugging JavaScript errors
  • Full-stack developers working with multiple languages
  • Teams looking to reduce debugging time
  • Students learning to code

  🔒 Privacy First:
  • No personal data collection
  • All analysis happens locally when offline
  • Secure API communication

  Get started in seconds - just install and let CCDebugger help you debug smarter, not harder!
  ```

#### 類別和標籤
- **類別**: Developer Tools
- **標籤**: debugging, error-handling, developer-tools, ai, javascript, python, typescript

### 步驟 3：上傳資源

#### 必需文件
1. **擴展 ZIP 文件**: `ccdebugger-extension.zip`
2. **商店圖標**: 使用 `store_assets/` 中的文件
   - 小型宣傳圖 (440x280): `small_promo.png`
   - 大型宣傳圖 (920x680): `large_promo.png`
   - 跑馬燈宣傳圖 (1400x560): `marquee_promo.png`

#### 螢幕截圖（需要創建）
建議準備 4-5 張螢幕截圖 (1280x800 或 640x400)：
1. Popup 介面展示錯誤列表
2. DevTools 面板顯示 AI 分析
3. 選項頁面
4. 錯誤通知徽章
5. 實際使用案例

### 步驟 4：隱私權和權限

#### 權限說明
為每個權限提供清晰的說明：
- `storage`: 儲存用戶設定和錯誤歷史
- `tabs`: 偵測當前頁面的錯誤
- `activeTab`: 分析當前頁面的錯誤內容
- `scripting`: 注入錯誤偵測腳本
- `<all_urls>`: 在任何網站上偵測錯誤

#### 隱私權政策範本
```markdown
# CCDebugger Privacy Policy

Last updated: [Date]

## Data Collection
CCDebugger collects only technical error information for analysis:
- Error messages and stack traces
- Source file names and line numbers
- Browser and extension version

## Data Usage
- Error data is sent to our API for AI analysis
- No personal information is collected
- Data is not shared with third parties

## Data Storage
- Settings stored locally in browser
- Error history cleared on browser close
- No server-side user tracking

## Contact
For privacy concerns: privacy@ccdebugger.com
```

### 步驟 5：定價和分發

#### 定價選項
- **免費**: 基本功能免費使用
- **應用內購買** (可選): 高級功能如無限制 API 調用

#### 分發設定
- **可用地區**: 所有地區
- **語言**: 英文、中文（繁體/簡體）

### 步驟 6：提交審核

1. 填寫所有必需欄位
2. 上傳所有資源
3. 預覽商店列表
4. 提交審核

### 審核時間和注意事項

#### 審核時間
- 首次提交：1-3 個工作日
- 更新：通常在 24 小時內

#### 常見審核問題
1. **權限過多**: 確保每個權限都有明確用途
2. **描述不清**: 避免誇大功能或誤導性描述
3. **品質問題**: 確保無明顯錯誤或崩潰
4. **政策違規**: 遵守所有 Chrome Web Store 政策

### 步驟 7：發布後維護

#### 監控和分析
- 查看安裝數據和用戶評價
- 回應用戶反饋
- 定期更新修復問題

#### 版本更新流程
1. 更新 `manifest.json` 中的版本號
2. 重新構建並創建新的 ZIP 文件
3. 在開發者儀表板上傳新版本
4. 提供更新說明

## 檢查清單

發布前確認：
- [ ] 所有功能在 Chrome 中測試正常
- [ ] manifest.json 版本號正確
- [ ] 所有必需圖標存在
- [ ] 隱私權政策 URL 可訪問
- [ ] 商店描述準確無誤
- [ ] 螢幕截圖清晰展示功能
- [ ] ZIP 文件不包含不必要的文件

## 有用資源

- [Chrome Web Store 開發者文檔](https://developer.chrome.com/docs/webstore/)
- [發布清單](https://developer.chrome.com/docs/webstore/publish/)
- [審核指南](https://developer.chrome.com/docs/webstore/review-process/)
- [最佳實踐](https://developer.chrome.com/docs/webstore/best-practices/)

## 支援聯絡

如需協助：
- Chrome Web Store 支援：https://support.google.com/chrome_webstore/
- 開發者論壇：https://groups.google.com/a/chromium.org/g/chromium-extensions

---

祝您發布順利！🚀
# CCDebugger Chrome Extension 測試指南

## 快速測試步驟

### 1. 安裝擴展
1. 打開 Chrome 瀏覽器
2. 訪問 `chrome://extensions/`
3. 開啟「開發者模式」（右上角開關）
4. 點擊「載入未封裝項目」
5. 選擇 `dist/` 目錄

### 2. 測試錯誤偵測

#### JavaScript 錯誤測試
創建測試 HTML 文件：
```html
<!DOCTYPE html>
<html>
<head>
    <title>CCDebugger Test</title>
</head>
<body>
    <h1>Error Test Page</h1>
    <button onclick="testError()">觸發錯誤</button>
    
    <script>
        // 測試各種錯誤類型
        function testError() {
            // TypeError
            const obj = null;
            console.log(obj.property);
        }
        
        // ReferenceError
        setTimeout(() => {
            nonExistentFunction();
        }, 2000);
        
        // SyntaxError (在 console 中執行)
        // eval('const x = ;');
    </script>
</body>
</html>
```

### 3. 測試 DevTools 整合
1. 在任何網頁上按 F12 打開 DevTools
2. 查看是否有 "CCDebugger" 面板
3. 切換到該面板查看錯誤列表
4. 點擊錯誤查看 AI 分析

### 4. 測試 API 功能
1. 點擊擴展圖標打開 popup
2. 查看錯誤計數和列表
3. 點擊 "Settings" 進入選項頁面
4. 測試語言切換（English/中文）

### 5. 測試快捷鍵
- Windows/Linux: `Ctrl+Shift+D`
- Mac: `Cmd+Shift+D`
- 應該觸發頁面錯誤分析

### 6. 測試右鍵菜單
1. 選擇包含錯誤訊息的文字
2. 右鍵點擊
3. 選擇 "Analyze Error with CCDebugger"

## 功能檢查清單

### Popup 功能
- [ ] 顯示錯誤計數徽章
- [ ] 列出頁面上的所有錯誤
- [ ] 點擊錯誤顯示詳細資訊
- [ ] 清除錯誤按鈕正常工作
- [ ] 設置連結正常打開

### DevTools 面板
- [ ] 面板正確載入
- [ ] Errors 標籤顯示運行時錯誤
- [ ] Network 標籤顯示網絡錯誤
- [ ] Console 標籤顯示控制台錯誤
- [ ] AI Analysis 標籤顯示分析結果
- [ ] 自動分析開關正常工作

### 選項頁面
- [ ] 語言切換即時生效
- [ ] API 端點可配置
- [ ] 設定正確保存

### 錯誤分析
- [ ] AI 分析返回結果
- [ ] 顯示信心分數
- [ ] 提供程式碼建議
- [ ] 離線時使用備用分析

## 效能測試

### 記憶體使用
1. 打開 Chrome Task Manager (Shift+Esc)
2. 查看擴展的記憶體使用
3. 應該保持在 50MB 以下

### 響應時間
- 錯誤偵測：< 100ms
- AI 分析：< 2s
- UI 更新：即時

## 已知問題

1. **首次安裝**: 可能需要重新載入頁面才能開始偵測錯誤
2. **DevTools**: 必須在 DevTools 打開前載入頁面才能偵測錯誤
3. **CORS**: 某些跨域錯誤可能無法完整捕獲

## 測試不同語言錯誤

### Shell/Bash 錯誤
在控制台模擬：
```javascript
console.error("bash: command not found: gitx");
console.error("./script.sh: line 10: syntax error near unexpected token `fi'");
```

### Docker 錯誤
```javascript
console.error("docker: Error response from daemon: No such container: myapp");
console.error("ERROR: Service 'web' failed to build");
```

### Python 錯誤
```javascript
console.error("Traceback (most recent call last):\n  File 'app.py', line 10\n    print('Hello World'\n                      ^\nSyntaxError: unexpected EOF while parsing");
```

## 回報問題

如果發現任何問題，請記錄：
1. Chrome 版本
2. 錯誤描述
3. 重現步驟
4. 控制台錯誤訊息
5. 截圖（如適用）
# CCDebugger Chrome Extension Structure

## Project Directory Layout

```
ccdebugger-chrome-extension/
├── manifest.json           # Extension configuration
├── background/
│   └── service-worker.js  # Background script (Manifest V3)
├── content/
│   ├── content.js         # Content script injected into web pages
│   └── error-detector.js  # Error detection logic
├── popup/
│   ├── popup.html         # Extension popup UI
│   ├── popup.js           # Popup logic
│   └── popup.css          # Popup styles
├── devtools/
│   ├── devtools.html      # DevTools page
│   ├── panel.html         # CCDebugger panel
│   └── panel.js           # Panel functionality
├── options/
│   ├── options.html       # Settings page
│   └── options.js         # Settings logic
├── lib/
│   ├── api-client.js      # CCDebugger API communication
│   ├── error-parser.js    # Error parsing utilities
│   └── storage.js         # Chrome storage wrapper
├── assets/
│   ├── icons/             # Extension icons
│   └── styles/            # Shared styles
└── _locales/              # i18n support
    ├── en/
    └── zh/
```

## Manifest V3 Configuration

```json
{
  "manifest_version": 3,
  "name": "CCDebugger - AI Error Assistant",
  "version": "1.0.0",
  "description": "AI-powered debugging assistant for web developers",
  "permissions": [
    "storage",
    "tabs",
    "activeTab",
    "scripting"
  ],
  "optional_permissions": [
    "debugger",
    "webNavigation"
  ],
  "host_permissions": [
    "<all_urls>"
  ],
  "background": {
    "service_worker": "background/service-worker.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content/content.js", "content/error-detector.js"],
      "run_at": "document_start"
    }
  ],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "assets/icons/icon-16.png",
      "48": "assets/icons/icon-48.png",
      "128": "assets/icons/icon-128.png"
    }
  },
  "devtools_page": "devtools/devtools.html",
  "options_page": "options/options.html",
  "icons": {
    "16": "assets/icons/icon-16.png",
    "48": "assets/icons/icon-48.png",
    "128": "assets/icons/icon-128.png"
  },
  "default_locale": "en"
}
```

## Core Components Implementation

### 1. Error Detection (content/error-detector.js)
```javascript
class ErrorDetector {
  constructor() {
    this.errors = [];
    this.setupListeners();
  }

  setupListeners() {
    // Console error detection
    window.addEventListener('error', this.handleError.bind(this));
    window.addEventListener('unhandledrejection', this.handlePromiseRejection.bind(this));
    
    // Override console.error
    const originalError = console.error;
    console.error = (...args) => {
      this.captureConsoleError(args);
      originalError.apply(console, args);
    };

    // Network error detection
    this.interceptFetch();
    this.interceptXHR();
  }

  handleError(event) {
    const error = {
      type: 'runtime_error',
      message: event.message,
      source: event.filename,
      line: event.lineno,
      column: event.colno,
      stack: event.error?.stack,
      timestamp: new Date().toISOString()
    };
    this.reportError(error);
  }

  handlePromiseRejection(event) {
    const error = {
      type: 'unhandled_promise_rejection',
      reason: event.reason,
      promise: event.promise,
      timestamp: new Date().toISOString()
    };
    this.reportError(error);
  }

  interceptFetch() {
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      try {
        const response = await originalFetch(...args);
        if (!response.ok) {
          this.captureNetworkError('fetch', args[0], response);
        }
        return response;
      } catch (error) {
        this.captureNetworkError('fetch', args[0], error);
        throw error;
      }
    };
  }

  reportError(error) {
    // Send to background script
    chrome.runtime.sendMessage({
      action: 'error_detected',
      error: error
    });
  }
}
```

### 2. Background Service Worker
```javascript
// background/service-worker.js
class CCDebuggerBackground {
  constructor() {
    this.errors = new Map(); // Store errors by tab ID
    this.setupListeners();
  }

  setupListeners() {
    // Message from content scripts
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'error_detected') {
        this.handleError(sender.tab.id, request.error);
      }
    });

    // Badge update on error count
    chrome.tabs.onActivated.addListener(({ tabId }) => {
      this.updateBadge(tabId);
    });
  }

  async handleError(tabId, error) {
    // Store error
    if (!this.errors.has(tabId)) {
      this.errors.set(tabId, []);
    }
    this.errors.get(tabId).push(error);

    // Update badge
    this.updateBadge(tabId);

    // Analyze with CCDebugger API
    const analysis = await this.analyzeError(error);
    
    // Store analysis
    await chrome.storage.local.set({
      [`analysis_${Date.now()}`]: analysis
    });

    // Notify popup if open
    chrome.runtime.sendMessage({
      action: 'new_analysis',
      analysis: analysis
    });
  }

  async analyzeError(error) {
    try {
      const response = await fetch('https://api.ccdebugger.com/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          error_type: error.type,
          message: error.message,
          stack: error.stack,
          context: {
            url: error.source,
            line: error.line,
            column: error.column
          }
        })
      });
      
      return await response.json();
    } catch (e) {
      console.error('Failed to analyze error:', e);
      return null;
    }
  }

  updateBadge(tabId) {
    const errorCount = this.errors.get(tabId)?.length || 0;
    chrome.action.setBadgeText({
      text: errorCount > 0 ? errorCount.toString() : '',
      tabId: tabId
    });
    chrome.action.setBadgeBackgroundColor({
      color: '#FF0000'
    });
  }
}
```

### 3. Popup Interface
```javascript
// popup/popup.js
class CCDebuggerPopup {
  constructor() {
    this.currentTab = null;
    this.init();
  }

  async init() {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    this.currentTab = tab;

    // Load errors for current tab
    this.loadErrors();

    // Setup listeners
    this.setupListeners();
  }

  async loadErrors() {
    // Get errors from background script
    const response = await chrome.runtime.sendMessage({
      action: 'get_errors',
      tabId: this.currentTab.id
    });

    if (response?.errors?.length > 0) {
      this.displayErrors(response.errors);
    } else {
      this.displayNoErrors();
    }
  }

  displayErrors(errors) {
    const container = document.getElementById('error-list');
    container.innerHTML = '';

    errors.forEach(error => {
      const errorElement = this.createErrorElement(error);
      container.appendChild(errorElement);
    });
  }

  createErrorElement(error) {
    const div = document.createElement('div');
    div.className = 'error-item';
    div.innerHTML = `
      <div class="error-header">
        <span class="error-type">${error.type}</span>
        <span class="error-time">${this.formatTime(error.timestamp)}</span>
      </div>
      <div class="error-message">${error.message}</div>
      ${error.analysis ? `
        <div class="error-suggestions">
          <h4>AI Suggestions:</h4>
          ${error.analysis.suggestions.map(s => `
            <div class="suggestion">
              <strong>${s.title}</strong>
              <p>${s.description}</p>
            </div>
          `).join('')}
        </div>
      ` : '<div class="analyzing">Analyzing...</div>'}
    `;
    return div;
  }
}
```

## Development Roadmap

### Phase 1: MVP (2 weeks)
- [x] Basic error detection (console, runtime errors)
- [x] Popup UI with error list
- [x] Badge notification
- [ ] Basic API integration
- [ ] Chinese/English localization

### Phase 2: Enhanced Detection (2 weeks)
- [ ] Network error interception
- [ ] React/Vue/Angular specific errors
- [ ] Source map support
- [ ] Stack trace enhancement
- [ ] Performance metrics

### Phase 3: Advanced Features (2 weeks)
- [ ] DevTools panel integration
- [ ] Real-time error streaming
- [ ] Error grouping and deduplication
- [ ] Export error reports
- [ ] Team collaboration features

### Phase 4: Polish & Launch (1 week)
- [ ] Performance optimization
- [ ] Security review
- [ ] Chrome Web Store listing
- [ ] Documentation
- [ ] Marketing materials

## Technical Considerations

### Security
- Content Security Policy compliance
- Secure API communication (HTTPS only)
- No sensitive data storage
- User privacy protection

### Performance
- Minimal impact on page load
- Efficient error batching
- Lazy loading of UI components
- Memory leak prevention

### Compatibility
- Chrome 88+ support
- Manifest V3 compliance
- Cross-origin considerations
- Framework agnostic

---

*Next: Begin implementation with basic error detection and popup UI*
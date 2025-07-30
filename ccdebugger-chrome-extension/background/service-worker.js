/**
 * CCDebugger Chrome Extension - Background Service Worker
 * Handles error collection, analysis, and communication between components
 */

// Import API client
importScripts('../lib/api-client.js');

class CCDebuggerBackground {
  constructor() {
    // Store errors by tab ID
    this.errors = new Map();
    // Store analysis results
    this.analyses = new Map();
    // API client
    this.apiClient = new CCDebuggerAPI();
    // Initialize
    this.init();
  }

  async init() {
    // Load settings from storage
    const settings = await chrome.storage.sync.get({
      apiEndpoint: 'https://api.ccdebugger.com',
      apiKey: null,
      enableMonitoring: true,
      language: 'en'
    });
    
    // Configure API client
    this.apiClient.setConfig({
      endpoint: settings.apiEndpoint,
      apiKey: settings.apiKey
    });
    
    this.setupListeners();
    
    // Clear errors when tab is closed
    chrome.tabs.onRemoved.addListener((tabId) => {
      this.errors.delete(tabId);
      this.analyses.delete(tabId);
    });
  }

  setupListeners() {
    // Message from content scripts and DevTools
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'error_detected' && sender.tab) {
        this.handleError(sender.tab.id, request.error);
        sendResponse({ success: true });
      } else if (request.action === 'get_errors') {
        const errors = this.errors.get(request.tabId) || [];
        sendResponse({ errors });
      } else if (request.action === 'clear_errors') {
        this.clearErrors(request.tabId);
        sendResponse({ success: true });
      } else if (request.action === 'get_analysis') {
        const analysis = this.analyses.get(request.errorId);
        sendResponse({ analysis });
      } else if (request.action === 'analyze_error') {
        // Analyze error on demand from DevTools
        this.analyzeError(request.error).then(analysis => {
          sendResponse({ analysis });
        });
        return true; // Keep channel open for async response
      } else if (request.action === 'devtools_runtime_error' || 
                 request.action === 'devtools_network_error' || 
                 request.action === 'devtools_console_error') {
        // Handle errors from DevTools
        // Get the current active tab
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs[0]) {
            const tabId = tabs[0].id;
            if (request.action === 'devtools_runtime_error') {
              this.handleError(tabId, request.error);
            }
            // Forward to DevTools panel
            chrome.runtime.sendMessage(request).catch(() => {
              // DevTools panel might not be open
            });
          }
        });
        sendResponse({ success: true });
      }
      return true; // Keep the message channel open for async responses
    });

    // Badge update on tab activation
    chrome.tabs.onActivated.addListener(({ tabId }) => {
      this.updateBadge(tabId);
    });

    // Command shortcuts
    chrome.commands.onCommand.addListener((command) => {
      if (command === 'analyze-page') {
        this.analyzeCurrentPage();
      }
    });

    // Context menu
    chrome.runtime.onInstalled.addListener(() => {
      chrome.contextMenus.create({
        id: 'analyze-selection',
        title: 'Analyze Error with CCDebugger',
        contexts: ['selection']
      });
    });

    chrome.contextMenus.onClicked.addListener((info, tab) => {
      if (info.menuItemId === 'analyze-selection' && info.selectionText) {
        this.analyzeText(info.selectionText, tab.id);
      }
    });
  }

  async handleError(tabId, error) {
    // Initialize error array for tab if needed
    if (!this.errors.has(tabId)) {
      this.errors.set(tabId, []);
    }
    
    // Add timestamp and unique ID
    error.id = `${tabId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    error.timestamp = error.timestamp || new Date().toISOString();
    
    // Check for duplicates (same error message within 1 second)
    const errors = this.errors.get(tabId);
    const isDuplicate = errors.some(e => 
      e.message === error.message && 
      Math.abs(new Date(e.timestamp) - new Date(error.timestamp)) < 1000
    );
    
    if (!isDuplicate) {
      errors.push(error);
      this.errors.set(tabId, errors);
      
      // Update badge
      this.updateBadge(tabId);
      
      // Analyze error asynchronously
      this.analyzeError(error).then(analysis => {
        if (analysis) {
          this.analyses.set(error.id, analysis);
          // Notify popup if open
          chrome.runtime.sendMessage({
            action: 'new_analysis',
            errorId: error.id,
            analysis: analysis
          }).catch(() => {
            // Popup might not be open, ignore error
          });
        }
      });
    }
  }

  async analyzeError(error) {
    try {
      // Use API client for analysis
      const analysis = await this.apiClient.analyzeError(error);
      return analysis;
    } catch (e) {
      console.error('Failed to analyze error:', e);
      // API client already provides fallback analysis
      return null;
    }
  }


  updateBadge(tabId) {
    const errors = this.errors.get(tabId) || [];
    const errorCount = errors.length;
    
    chrome.action.setBadgeText({
      text: errorCount > 0 ? errorCount.toString() : '',
      tabId: tabId
    });
    
    chrome.action.setBadgeBackgroundColor({
      color: errorCount > 0 ? '#FF0000' : '#00000000',
      tabId: tabId
    });
    
    // Update tooltip
    const title = errorCount > 0 
      ? chrome.i18n.getMessage('errorCount', [errorCount])
      : chrome.i18n.getMessage('noErrors');
    
    chrome.action.setTitle({
      title: title,
      tabId: tabId
    });
  }

  clearErrors(tabId) {
    this.errors.delete(tabId);
    // Clear related analyses
    const analyses = this.analyses;
    for (const [key, value] of analyses) {
      if (key.startsWith(`${tabId}_`)) {
        analyses.delete(key);
      }
    }
    this.updateBadge(tabId);
  }

  async analyzeCurrentPage() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      // Inject analysis script
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          // Force error detection refresh
          window.postMessage({ type: 'CCDEBUGGER_ANALYZE' }, '*');
        }
      });
    }
  }

  async analyzeText(text, tabId) {
    const error = {
      type: 'manual_analysis',
      message: text,
      timestamp: new Date().toISOString()
    };
    
    this.handleError(tabId, error);
  }
}

// Initialize background service
const ccDebugger = new CCDebuggerBackground();

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CCDebuggerBackground;
}
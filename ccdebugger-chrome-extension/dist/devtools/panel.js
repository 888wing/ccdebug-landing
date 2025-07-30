/**
 * CCDebugger DevTools Panel JavaScript
 * Manages the DevTools panel interface and communication
 */

class CCDebuggerPanel {
  constructor() {
    this.errors = new Map();
    this.networkErrors = [];
    this.consoleErrors = [];
    this.currentTab = 'errors';
    this.selectedError = null;
    this.autoAnalyze = true;
    
    this.initializeElements();
    this.setupListeners();
    this.loadErrors();
  }
  
  initializeElements() {
    // Tab buttons
    this.tabButtons = document.querySelectorAll('.tab-btn');
    this.tabContents = document.querySelectorAll('.tab-content');
    
    // Lists
    this.errorList = document.getElementById('error-list');
    this.networkList = document.getElementById('network-list');
    this.consoleList = document.getElementById('console-list');
    this.analysisContainer = document.getElementById('analysis-container');
    
    // Controls
    this.clearBtn = document.getElementById('clear-btn');
    this.refreshBtn = document.getElementById('refresh-btn');
    this.autoAnalyzeCheckbox = document.getElementById('auto-analyze');
    
    // Error detail modal
    this.errorDetail = document.getElementById('error-detail');
    this.errorInfo = document.getElementById('error-info');
    this.errorStack = document.getElementById('error-stack');
    this.aiAnalysis = document.getElementById('ai-analysis');
  }
  
  setupListeners() {
    // Tab switching
    this.tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        this.switchTab(tab);
      });
    });
    
    // Control buttons
    this.clearBtn.addEventListener('click', () => this.clearAll());
    this.refreshBtn.addEventListener('click', () => this.refresh());
    this.autoAnalyzeCheckbox.addEventListener('change', (e) => {
      this.autoAnalyze = e.target.checked;
    });
    
    // Close detail modal
    const closeBtn = this.errorDetail.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => this.closeDetail());
    
    // Listen for messages from background
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message);
    });
    
    // Listen for errors from the inspected window
    chrome.devtools.inspectedWindow.eval(
      `window.addEventListener('error', function(e) {
        chrome.runtime.sendMessage({
          action: 'devtools_runtime_error',
          error: {
            type: 'runtime_error',
            message: e.message,
            source: e.filename,
            line: e.lineno,
            column: e.colno,
            stack: e.error ? e.error.stack : ''
          }
        });
      }, true);`,
      (result, error) => {
        if (error) {
          console.error('Failed to inject error listener:', error);
        }
      }
    );
  }
  
  handleMessage(message) {
    switch (message.action) {
      case 'error_detected':
      case 'devtools_runtime_error':
        this.addError(message.error);
        break;
      case 'devtools_network_error':
        this.addNetworkError(message.error);
        break;
      case 'devtools_console_error':
        this.addConsoleError(message);
        break;
      case 'new_analysis':
        if (this.selectedError && this.selectedError.id === message.errorId) {
          this.displayAnalysis(message.analysis);
        }
        break;
    }
  }
  
  async loadErrors() {
    // Get current tab ID
    chrome.devtools.inspectedWindow.eval(
      "chrome.devtools.inspectedWindow.tabId",
      (tabId) => {
        // Request errors from background
        chrome.runtime.sendMessage({
          action: 'get_errors',
          tabId: tabId
        }, (response) => {
          if (response && response.errors) {
            response.errors.forEach(error => this.addError(error));
          }
        });
      }
    );
  }
  
  switchTab(tab) {
    this.currentTab = tab;
    
    // Update active states
    this.tabButtons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    
    this.tabContents.forEach(content => {
      content.classList.toggle('active', content.id === `${tab}-tab`);
    });
  }
  
  addError(error) {
    if (!error.id) {
      error.id = `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    this.errors.set(error.id, error);
    this.renderError(error);
    
    if (this.autoAnalyze && !error.analysis) {
      this.requestAnalysis(error);
    }
  }
  
  addNetworkError(error) {
    error.id = `network_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    error.type = 'network_error';
    error.timestamp = new Date().toISOString();
    
    this.networkErrors.push(error);
    this.renderNetworkError(error);
  }
  
  addConsoleError(message) {
    const error = {
      id: `console_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: 'console_error',
      level: message.level,
      message: message.args.join(' '),
      timestamp: new Date().toISOString()
    };
    
    this.consoleErrors.push(error);
    this.renderConsoleError(error);
  }
  
  renderError(error) {
    const errorItem = this.createErrorElement(error);
    
    // Remove empty state if exists
    const emptyState = this.errorList.querySelector('.empty-state');
    if (emptyState) {
      emptyState.remove();
    }
    
    // Add to list
    this.errorList.appendChild(errorItem);
  }
  
  renderNetworkError(error) {
    const errorItem = this.createErrorElement(error);
    
    // Remove empty state if exists
    const emptyState = this.networkList.querySelector('.empty-state');
    if (emptyState) {
      emptyState.remove();
    }
    
    // Add to list
    this.networkList.appendChild(errorItem);
  }
  
  renderConsoleError(error) {
    const errorItem = this.createErrorElement(error);
    
    // Remove empty state if exists
    const emptyState = this.consoleList.querySelector('.empty-state');
    if (emptyState) {
      emptyState.remove();
    }
    
    // Add to list
    this.consoleList.appendChild(errorItem);
  }
  
  createErrorElement(error) {
    const div = document.createElement('div');
    div.className = 'error-item';
    div.dataset.errorId = error.id;
    
    const typeClass = error.type.replace('_', '-');
    const time = new Date(error.timestamp).toLocaleTimeString();
    
    div.innerHTML = `
      <div class="error-header">
        <span class="error-type ${typeClass}">${this.formatErrorType(error.type)}</span>
        <span class="error-time">${time}</span>
      </div>
      <div class="error-message">${this.escapeHtml(error.message)}</div>
      ${error.source ? `<div class="error-source">${this.escapeHtml(error.source)}${error.line ? `:${error.line}` : ''}</div>` : ''}
    `;
    
    div.addEventListener('click', () => this.selectError(error));
    
    return div;
  }
  
  formatErrorType(type) {
    return type.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase());
  }
  
  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
  
  selectError(error) {
    this.selectedError = error;
    
    // Update selected state
    document.querySelectorAll('.error-item').forEach(item => {
      item.classList.toggle('selected', item.dataset.errorId === error.id);
    });
    
    // Switch to analysis tab
    this.switchTab('analysis');
    
    // Display error details
    this.displayErrorDetails(error);
    
    // Request analysis if not available
    if (!error.analysis) {
      this.requestAnalysis(error);
    }
  }
  
  displayErrorDetails(error) {
    this.analysisContainer.innerHTML = `
      <div class="analysis-section">
        <h3>Error Information</h3>
        <div class="error-info">
          <p><strong>Type:</strong> ${this.formatErrorType(error.type)}</p>
          <p><strong>Message:</strong> ${this.escapeHtml(error.message)}</p>
          ${error.source ? `<p><strong>Source:</strong> ${this.escapeHtml(error.source)}${error.line ? `:${error.line}` : ''}</p>` : ''}
          <p><strong>Time:</strong> ${new Date(error.timestamp).toLocaleString()}</p>
        </div>
      </div>
      ${error.stack ? `
      <div class="analysis-section">
        <h3>Stack Trace</h3>
        <pre class="code-block">${this.escapeHtml(error.stack)}</pre>
      </div>
      ` : ''}
      <div class="analysis-section">
        <h3>AI Analysis</h3>
        <div id="analysis-content">
          <div class="loading">Analyzing error...</div>
        </div>
      </div>
    `;
  }
  
  async requestAnalysis(error) {
    chrome.runtime.sendMessage({
      action: 'analyze_error',
      error: error
    }, (response) => {
      if (response && response.analysis) {
        error.analysis = response.analysis;
        if (this.selectedError && this.selectedError.id === error.id) {
          this.displayAnalysis(response.analysis);
        }
      }
    });
  }
  
  displayAnalysis(analysis) {
    const analysisContent = document.getElementById('analysis-content');
    if (!analysisContent) return;
    
    if (!analysis || !analysis.suggestions) {
      analysisContent.innerHTML = '<p class="hint">No analysis available for this error.</p>';
      return;
    }
    
    let html = '';
    
    if (analysis.explanation) {
      html += `<p>${this.escapeHtml(analysis.explanation)}</p>`;
    }
    
    if (analysis.suggestions && analysis.suggestions.length > 0) {
      html += '<div class="suggestions">';
      analysis.suggestions.forEach(suggestion => {
        const confidenceClass = suggestion.confidence > 0.8 ? 'high' : 
                              suggestion.confidence > 0.5 ? 'medium' : 'low';
        
        html += `
          <div class="suggestion-item">
            <div class="suggestion-header">
              <span class="suggestion-title">${this.escapeHtml(suggestion.title)}</span>
              <span class="confidence-badge confidence-${confidenceClass}">
                ${Math.round(suggestion.confidence * 100)}% confidence
              </span>
            </div>
            ${suggestion.code ? `<pre class="code-block">${this.escapeHtml(suggestion.code)}</pre>` : ''}
          </div>
        `;
      });
      html += '</div>';
    }
    
    analysisContent.innerHTML = html;
  }
  
  clearAll() {
    // Clear all errors
    this.errors.clear();
    this.networkErrors = [];
    this.consoleErrors = [];
    
    // Clear UI
    this.errorList.innerHTML = '<div class="empty-state"><p>No errors detected yet.</p><p class="hint">Errors will appear here as they occur on the page.</p></div>';
    this.networkList.innerHTML = '<div class="empty-state"><p>No network errors detected.</p><p class="hint">Failed network requests will appear here.</p></div>';
    this.consoleList.innerHTML = '<div class="empty-state"><p>No console errors detected.</p><p class="hint">Console errors and warnings will appear here.</p></div>';
    this.analysisContainer.innerHTML = '<div class="empty-state"><p>Select an error to see AI-powered analysis.</p><p class="hint">Click on any error in the other tabs to analyze it.</p></div>';
    
    // Clear errors in background
    chrome.devtools.inspectedWindow.eval(
      "chrome.devtools.inspectedWindow.tabId",
      (tabId) => {
        chrome.runtime.sendMessage({
          action: 'clear_errors',
          tabId: tabId
        });
      }
    );
  }
  
  refresh() {
    this.clearAll();
    this.loadErrors();
  }
  
  closeDetail() {
    this.errorDetail.classList.add('hidden');
  }
}

// Initialize panel when loaded
function initializePanel() {
  window.ccDebuggerPanel = new CCDebuggerPanel();
}

// Initialize immediately if document is ready
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  initializePanel();
} else {
  document.addEventListener('DOMContentLoaded', initializePanel);
}

// Export for devtools.js
window.initializePanel = initializePanel;
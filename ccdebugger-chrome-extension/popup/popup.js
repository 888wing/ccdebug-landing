/**
 * CCDebugger Chrome Extension - Popup Script
 * Main logic for the extension popup interface
 */

class CCDebuggerPopup {
  constructor() {
    this.currentTab = null;
    this.errors = [];
    this.isMonitoring = true;
    this.init();
  }

  async init() {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    this.currentTab = tab;
    
    // Load localized strings
    this.localizeUI();
    
    // Display current page URL
    this.displayPageUrl();
    
    // Load monitoring state
    await this.loadMonitoringState();
    
    // Load errors for current tab
    await this.loadErrors();
    
    // Setup event listeners
    this.setupListeners();
    
    // Listen for real-time updates
    this.listenForUpdates();
  }

  localizeUI() {
    // Localize all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const messageName = element.getAttribute('data-i18n');
      const message = chrome.i18n.getMessage(messageName);
      if (message) {
        element.textContent = message;
      }
    });
    
    // Localize title attributes
    document.querySelectorAll('[title]').forEach(element => {
      const titleKey = element.getAttribute('title');
      if (titleKey.startsWith('__MSG_') && titleKey.endsWith('__')) {
        const messageName = titleKey.slice(6, -2);
        const message = chrome.i18n.getMessage(messageName);
        if (message) {
          element.setAttribute('title', message);
        }
      }
    });
  }

  displayPageUrl() {
    const urlElement = document.getElementById('page-url');
    if (this.currentTab && this.currentTab.url) {
      try {
        const url = new URL(this.currentTab.url);
        urlElement.textContent = url.hostname;
      } catch {
        urlElement.textContent = this.currentTab.url;
      }
    }
  }

  async loadMonitoringState() {
    const settings = await chrome.storage.sync.get({ enableMonitoring: true });
    this.isMonitoring = settings.enableMonitoring;
    this.updateMonitoringToggle();
  }

  async loadErrors() {
    this.showLoading(true);
    
    try {
      // Request errors from background script
      const response = await chrome.runtime.sendMessage({
        action: 'get_errors',
        tabId: this.currentTab.id
      });
      
      if (response && response.errors) {
        this.errors = response.errors;
        
        // Load analyses for each error
        for (const error of this.errors) {
          if (error.id) {
            const analysisResponse = await chrome.runtime.sendMessage({
              action: 'get_analysis',
              errorId: error.id
            });
            
            if (analysisResponse && analysisResponse.analysis) {
              error.analysis = analysisResponse.analysis;
            }
          }
        }
        
        this.displayErrors();
      }
    } catch (error) {
      console.error('Failed to load errors:', error);
      this.displayNoErrors();
    } finally {
      this.showLoading(false);
    }
  }

  displayErrors() {
    const errorCount = this.errors.length;
    document.getElementById('error-count').textContent = errorCount;
    
    // Update error count message
    const errorCountMessage = chrome.i18n.getMessage('errorCount', [errorCount.toString()]);
    document.querySelector('.summary-text h2').textContent = errorCountMessage;
    
    if (errorCount === 0) {
      this.displayNoErrors();
      return;
    }
    
    // Hide no errors message
    document.getElementById('no-errors').style.display = 'none';
    
    // Show error list
    const errorList = document.getElementById('error-list');
    errorList.style.display = 'block';
    errorList.innerHTML = '';
    
    // Sort errors by timestamp (newest first)
    const sortedErrors = [...this.errors].sort((a, b) => 
      new Date(b.timestamp) - new Date(a.timestamp)
    );
    
    // Display each error
    sortedErrors.forEach((error, index) => {
      const errorElement = this.createErrorElement(error, index);
      errorList.appendChild(errorElement);
    });
  }

  displayNoErrors() {
    document.getElementById('error-count').textContent = '0';
    document.querySelector('.summary-text h2').textContent = chrome.i18n.getMessage('noErrors');
    document.getElementById('no-errors').style.display = 'flex';
    document.getElementById('error-list').style.display = 'none';
  }

  createErrorElement(error, index) {
    const div = document.createElement('div');
    div.className = 'error-item';
    div.dataset.errorIndex = index;
    
    // Determine error type class
    const typeClass = this.getErrorTypeClass(error.type);
    
    // Format timestamp
    const timeStr = this.formatTime(error.timestamp);
    
    // Get localized error type
    const errorTypeName = this.getLocalizedErrorType(error.type);
    
    // Build error HTML
    let html = `
      <div class="error-header">
        <span class="error-type ${typeClass}">${errorTypeName}</span>
        <span class="error-time">${timeStr}</span>
      </div>
      <div class="error-message">${this.escapeHtml(error.message)}</div>
    `;
    
    // Add source info if available
    if (error.source || error.line) {
      const sourceInfo = [];
      if (error.source) {
        try {
          const url = new URL(error.source);
          sourceInfo.push(url.pathname.split('/').pop() || url.hostname);
        } catch {
          sourceInfo.push(error.source);
        }
      }
      if (error.line) {
        sourceInfo.push(`Line ${error.line}`);
        if (error.column) {
          sourceInfo.push(`Col ${error.column}`);
        }
      }
      html += `<div class="error-source">${sourceInfo.join(' • ')}</div>`;
    }
    
    // Add analysis if available
    if (error.analysis && error.analysis.suggestions) {
      html += this.createSuggestionsHTML(error.analysis);
    }
    
    div.innerHTML = html;
    
    // Add click handler to expand/collapse
    div.addEventListener('click', (e) => {
      if (!e.target.closest('.error-suggestions')) {
        this.toggleErrorDetails(div);
      }
    });
    
    return div;
  }

  createSuggestionsHTML(analysis) {
    let html = '<div class="error-suggestions" style="display: none;">';
    html += `<h4>🎯 ${chrome.i18n.getMessage('aiSuggestions')}</h4>`;
    
    if (analysis.suggestions && analysis.suggestions.length > 0) {
      analysis.suggestions.forEach(suggestion => {
        const confidence = Math.round((suggestion.confidence || 0.5) * 100);
        html += `
          <div class="suggestion">
            <strong>${this.escapeHtml(suggestion.title || suggestion.description)}</strong>
            ${suggestion.description ? `<p>${this.escapeHtml(suggestion.description)}</p>` : ''}
            <span class="suggestion-confidence">${chrome.i18n.getMessage('confidence')}: ${confidence}%</span>
          </div>
        `;
      });
    }
    
    html += '</div>';
    return html;
  }

  toggleErrorDetails(errorElement) {
    const suggestions = errorElement.querySelector('.error-suggestions');
    if (suggestions) {
      suggestions.style.display = suggestions.style.display === 'none' ? 'block' : 'none';
    }
  }

  getErrorTypeClass(type) {
    if (type.includes('runtime') || type.includes('error')) return 'runtime';
    if (type.includes('network')) return 'network';
    if (type.includes('promise')) return 'promise';
    return '';
  }

  getLocalizedErrorType(type) {
    const typeMap = {
      'runtime_error': chrome.i18n.getMessage('runtimeError'),
      'network_error': chrome.i18n.getMessage('networkError'),
      'promise_rejection': chrome.i18n.getMessage('promiseRejection'),
      'console_error': chrome.i18n.getMessage('consoleError'),
      'console_warning': 'Warning',
      'framework_error': 'Framework',
      'manual_analysis': 'Manual'
    };
    
    return typeMap[type] || type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // Less than 1 minute
    if (diff < 60000) {
      return 'Just now';
    }
    
    // Less than 1 hour
    if (diff < 3600000) {
      const minutes = Math.floor(diff / 60000);
      return `${minutes}m ago`;
    }
    
    // Less than 24 hours
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000);
      return `${hours}h ago`;
    }
    
    // Format as time
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
    document.getElementById('error-container').style.display = show ? 'none' : 'block';
  }

  setupListeners() {
    // Settings button
    document.getElementById('settings-btn').addEventListener('click', () => {
      chrome.runtime.openOptionsPage();
    });
    
    // Clear errors button
    document.getElementById('clear-btn').addEventListener('click', async () => {
      await chrome.runtime.sendMessage({
        action: 'clear_errors',
        tabId: this.currentTab.id
      });
      
      this.errors = [];
      this.displayNoErrors();
    });
    
    // Export button
    document.getElementById('export-btn').addEventListener('click', () => {
      this.exportReport();
    });
    
    // Monitor toggle
    document.getElementById('monitor-toggle').addEventListener('click', async () => {
      this.isMonitoring = !this.isMonitoring;
      await chrome.storage.sync.set({ enableMonitoring: this.isMonitoring });
      this.updateMonitoringToggle();
      
      // Notify content script
      chrome.tabs.sendMessage(this.currentTab.id, {
        action: 'toggle_monitoring',
        enabled: this.isMonitoring
      });
    });
  }

  updateMonitoringToggle() {
    const toggleBtn = document.getElementById('monitor-toggle');
    const toggleText = toggleBtn.querySelector('span');
    
    if (this.isMonitoring) {
      toggleBtn.classList.add('active');
      toggleText.textContent = chrome.i18n.getMessage('enableMonitoring');
    } else {
      toggleBtn.classList.remove('active');
      toggleText.textContent = chrome.i18n.getMessage('enableMonitoring');
    }
  }

  listenForUpdates() {
    // Listen for new error analyses
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'new_analysis') {
        // Find error and update with analysis
        const error = this.errors.find(e => e.id === request.errorId);
        if (error) {
          error.analysis = request.analysis;
          this.displayErrors();
        }
      }
    });
  }

  async exportReport() {
    const report = {
      url: this.currentTab.url,
      title: this.currentTab.title,
      timestamp: new Date().toISOString(),
      errorCount: this.errors.length,
      errors: this.errors.map(error => ({
        type: error.type,
        message: error.message,
        timestamp: error.timestamp,
        source: error.source,
        line: error.line,
        column: error.column,
        stack: error.stack,
        analysis: error.analysis
      }))
    };
    
    // Convert to JSON
    const json = JSON.stringify(report, null, 2);
    
    // Create blob and download
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const filename = `ccdebugger-report-${Date.now()}.json`;
    
    chrome.downloads.download({
      url: url,
      filename: filename,
      saveAs: true
    });
  }
}

// Initialize popup when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new CCDebuggerPopup();
});
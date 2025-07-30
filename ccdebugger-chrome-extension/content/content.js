/**
 * CCDebugger Chrome Extension - Content Script
 * Main content script that coordinates error detection and communication
 */

// Initialize content script
(function() {
  'use strict';
  
  // Check if already initialized
  if (window.ccDebuggerInitialized) {
    return;
  }
  
  window.ccDebuggerInitialized = true;
  
  // Content script coordinator
  class CCDebuggerContent {
    constructor() {
      this.isEnabled = true;
      this.init();
    }
    
    init() {
      // Check if error detector is loaded
      if (!window.ccDebuggerErrorDetector) {
        console.error('CCDebugger: Error detector not loaded');
        return;
      }
      
      // Setup message listeners
      this.setupMessageListeners();
      
      // Notify background that content script is ready
      this.notifyReady();
      
      // Log initialization
      console.log('CCDebugger: Content script initialized');
    }
    
    setupMessageListeners() {
      // Listen for messages from extension
      chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        switch (request.action) {
          case 'toggle_monitoring':
            this.toggleMonitoring(request.enabled);
            sendResponse({ success: true });
            break;
            
          case 'get_page_info':
            sendResponse({
              url: window.location.href,
              title: document.title,
              errors: window.ccDebuggerErrorDetector?.errors || []
            });
            break;
            
          case 'analyze_selection':
            if (request.text) {
              this.analyzeText(request.text);
            }
            sendResponse({ success: true });
            break;
            
          case 'force_analysis':
            if (window.ccDebuggerErrorDetector) {
              window.ccDebuggerErrorDetector.forceAnalysis();
            }
            sendResponse({ success: true });
            break;
            
          default:
            sendResponse({ success: false, error: 'Unknown action' });
        }
        
        return true; // Keep message channel open
      });
    }
    
    toggleMonitoring(enabled) {
      this.isEnabled = enabled;
      if (window.ccDebuggerErrorDetector) {
        window.ccDebuggerErrorDetector.setMonitoring(enabled);
      }
      
      // Visual feedback
      if (enabled) {
        this.showNotification('Error monitoring enabled');
      } else {
        this.showNotification('Error monitoring disabled');
      }
    }
    
    analyzeText(text) {
      // Create a manual error for analysis
      const error = {
        type: 'manual_analysis',
        message: text,
        url: window.location.href,
        timestamp: new Date().toISOString()
      };
      
      // Report to error detector
      if (window.ccDebuggerErrorDetector) {
        window.ccDebuggerErrorDetector.reportError(error);
      }
    }
    
    notifyReady() {
      // Send a message to background that content script is ready
      chrome.runtime.sendMessage({
        action: 'content_ready',
        url: window.location.href
      }).catch(err => {
        // Extension might be reloading
        console.warn('CCDebugger: Failed to notify background', err);
      });
    }
    
    showNotification(message) {
      // Create temporary notification element
      const notification = document.createElement('div');
      notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #1F2937;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 14px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 999999;
        animation: ccDebuggerSlideIn 0.3s ease-out;
      `;
      notification.textContent = message;
      
      // Add animation styles
      const style = document.createElement('style');
      style.textContent = `
        @keyframes ccDebuggerSlideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @keyframes ccDebuggerSlideOut {
          from {
            transform: translateX(0);
            opacity: 1;
          }
          to {
            transform: translateX(100%);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(style);
      
      // Add to page
      document.body.appendChild(notification);
      
      // Remove after 3 seconds
      setTimeout(() => {
        notification.style.animation = 'ccDebuggerSlideOut 0.3s ease-out';
        setTimeout(() => {
          notification.remove();
          style.remove();
        }, 300);
      }, 3000);
    }
  }
  
  // Initialize coordinator
  const ccDebuggerContent = new CCDebuggerContent();
  
  // Framework-specific error handling enhancements
  
  // React DevTools integration
  if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
    const originalOnCommitFiberRoot = window.__REACT_DEVTOOLS_GLOBAL_HOOK__.onCommitFiberRoot;
    window.__REACT_DEVTOOLS_GLOBAL_HOOK__.onCommitFiberRoot = function(...args) {
      // Check for error boundaries
      try {
        const [rendererID, root] = args;
        if (root && root.current && root.current.memoizedState && root.current.memoizedState.error) {
          const error = root.current.memoizedState.error;
          if (window.ccDebuggerErrorDetector) {
            window.ccDebuggerErrorDetector.captureFrameworkError('React', error.message, {
              stack: error.stack,
              componentStack: error.componentStack
            });
          }
        }
      } catch (e) {
        // Ignore errors in our error handling
      }
      
      // Call original function
      if (originalOnCommitFiberRoot) {
        return originalOnCommitFiberRoot.apply(this, args);
      }
    };
  }
  
  // Vue DevTools integration
  if (window.__VUE_DEVTOOLS_GLOBAL_HOOK__) {
    window.__VUE_DEVTOOLS_GLOBAL_HOOK__.emit('app:error', (app, error, info) => {
      if (window.ccDebuggerErrorDetector) {
        window.ccDebuggerErrorDetector.captureFrameworkError('Vue', error.message, {
          stack: error.stack,
          info: info
        });
      }
    });
  }
  
  // Performance monitoring
  if (window.PerformanceObserver) {
    try {
      // Monitor long tasks
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > 50) { // Tasks longer than 50ms
            // Could potentially report performance issues
            console.debug('CCDebugger: Long task detected', entry.duration + 'ms');
          }
        }
      });
      
      observer.observe({ entryTypes: ['longtask'] });
    } catch (e) {
      // PerformanceObserver might not support longtask
    }
  }
  
})();
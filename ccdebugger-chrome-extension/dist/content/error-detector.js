/**
 * CCDebugger Chrome Extension - Error Detector
 * Detects and captures various types of errors on web pages
 */

class ErrorDetector {
  constructor() {
    this.errors = [];
    this.isMonitoring = true;
    this.setupListeners();
  }

  setupListeners() {
    // Runtime errors
    window.addEventListener('error', this.handleError.bind(this), true);
    
    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', this.handlePromiseRejection.bind(this), true);
    
    // Console errors
    this.interceptConsole();
    
    // Network errors
    this.interceptFetch();
    this.interceptXHR();
    
    // React error boundaries (if React is present)
    this.detectReactErrors();
    
    // Vue error handler (if Vue is present)
    this.detectVueErrors();
    
    // Angular error handler (if Angular is present)
    this.detectAngularErrors();
    
    // Listen for messages from the page
    window.addEventListener('message', (event) => {
      if (event.data.type === 'CCDEBUGGER_ANALYZE') {
        this.forceAnalysis();
      }
    });
  }

  handleError(event) {
    if (!this.isMonitoring) return;
    
    const error = {
      type: 'runtime_error',
      message: event.message || 'Unknown error',
      source: event.filename || window.location.href,
      line: event.lineno,
      column: event.colno,
      stack: event.error?.stack || '',
      url: window.location.href,
      timestamp: new Date().toISOString()
    };
    
    // Extract error name if available
    if (event.error?.name) {
      error.errorName = event.error.name;
    }
    
    this.reportError(error);
  }

  handlePromiseRejection(event) {
    if (!this.isMonitoring) return;
    
    const error = {
      type: 'promise_rejection',
      message: event.reason?.message || event.reason?.toString() || 'Unhandled Promise Rejection',
      reason: event.reason,
      stack: event.reason?.stack || '',
      url: window.location.href,
      timestamp: new Date().toISOString()
    };
    
    this.reportError(error);
  }

  interceptConsole() {
    const originalError = console.error;
    const originalWarn = console.warn;
    
    console.error = (...args) => {
      if (this.isMonitoring) {
        this.captureConsoleError('error', args);
      }
      originalError.apply(console, args);
    };
    
    console.warn = (...args) => {
      if (this.isMonitoring && this.shouldCaptureWarning(args)) {
        this.captureConsoleError('warning', args);
      }
      originalWarn.apply(console, args);
    };
  }

  captureConsoleError(level, args) {
    // Convert arguments to string
    const message = args.map(arg => {
      if (typeof arg === 'object') {
        try {
          return JSON.stringify(arg, null, 2);
        } catch {
          return String(arg);
        }
      }
      return String(arg);
    }).join(' ');
    
    const error = {
      type: `console_${level}`,
      message: message,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };
    
    // Try to extract stack trace
    const stack = new Error().stack;
    if (stack) {
      // Remove the first few lines that are from our interceptor
      const lines = stack.split('\n');
      error.stack = lines.slice(3).join('\n');
    }
    
    this.reportError(error);
  }

  shouldCaptureWarning(args) {
    // Only capture warnings that look like errors
    const message = args.join(' ').toLowerCase();
    const errorKeywords = ['error', 'fail', 'exception', 'critical', 'fatal'];
    return errorKeywords.some(keyword => message.includes(keyword));
  }

  interceptFetch() {
    const originalFetch = window.fetch;
    
    window.fetch = async (...args) => {
      const startTime = Date.now();
      const [resource, init] = args;
      const url = typeof resource === 'string' ? resource : resource.url;
      
      try {
        const response = await originalFetch.apply(window, args);
        
        if (!response.ok && this.isMonitoring) {
          const duration = Date.now() - startTime;
          this.captureNetworkError('fetch', {
            url: url,
            method: init?.method || 'GET',
            status: response.status,
            statusText: response.statusText,
            duration: duration
          });
        }
        
        return response;
      } catch (error) {
        if (this.isMonitoring) {
          const duration = Date.now() - startTime;
          this.captureNetworkError('fetch', {
            url: url,
            method: init?.method || 'GET',
            error: error.message,
            duration: duration
          });
        }
        throw error;
      }
    };
  }

  interceptXHR() {
    const originalOpen = XMLHttpRequest.prototype.open;
    const originalSend = XMLHttpRequest.prototype.send;
    
    XMLHttpRequest.prototype.open = function(method, url, ...args) {
      this._ccDebugger = {
        method: method,
        url: url,
        startTime: null
      };
      return originalOpen.apply(this, [method, url, ...args]);
    };
    
    XMLHttpRequest.prototype.send = function(...args) {
      if (this._ccDebugger) {
        this._ccDebugger.startTime = Date.now();
        
        this.addEventListener('load', () => {
          if (this.status >= 400 && window.ccDebuggerErrorDetector?.isMonitoring) {
            const duration = Date.now() - this._ccDebugger.startTime;
            window.ccDebuggerErrorDetector.captureNetworkError('xhr', {
              url: this._ccDebugger.url,
              method: this._ccDebugger.method,
              status: this.status,
              statusText: this.statusText,
              duration: duration
            });
          }
        });
        
        this.addEventListener('error', () => {
          if (window.ccDebuggerErrorDetector?.isMonitoring) {
            const duration = Date.now() - this._ccDebugger.startTime;
            window.ccDebuggerErrorDetector.captureNetworkError('xhr', {
              url: this._ccDebugger.url,
              method: this._ccDebugger.method,
              error: 'Network request failed',
              duration: duration
            });
          }
        });
      }
      
      return originalSend.apply(this, args);
    };
  }

  captureNetworkError(type, details) {
    const error = {
      type: 'network_error',
      message: `${type.toUpperCase()} ${details.method} ${details.url} - ${details.status || details.error}`,
      networkDetails: details,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };
    
    this.reportError(error);
  }

  detectReactErrors() {
    // Check if React is present
    if (window.React || window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
      // Try to patch React's error handling
      const originalError = console.error;
      console.error = (...args) => {
        const message = args.join(' ');
        if (message.includes('React') && this.isMonitoring) {
          this.captureFrameworkError('React', message, args);
        }
        originalError.apply(console, args);
      };
    }
  }

  detectVueErrors() {
    // Check for Vue 2
    if (window.Vue) {
      window.Vue.config.errorHandler = (err, vm, info) => {
        if (this.isMonitoring) {
          this.captureFrameworkError('Vue', err.message, {
            stack: err.stack,
            info: info,
            component: vm?.$options.name || 'Unknown'
          });
        }
      };
    }
    
    // Check for Vue 3
    if (window.__VUE__) {
      // Vue 3 error handling is app-specific, log a note
      console.log('CCDebugger: Vue 3 detected. Configure error handling in your app.');
    }
  }

  detectAngularErrors() {
    // Angular errors are typically caught through zone.js
    if (window.Zone) {
      const originalError = console.error;
      console.error = (...args) => {
        const message = args.join(' ');
        if ((message.includes('Angular') || message.includes('ng')) && this.isMonitoring) {
          this.captureFrameworkError('Angular', message, args);
        }
        originalError.apply(console, args);
      };
    }
  }

  captureFrameworkError(framework, message, details) {
    const error = {
      type: 'framework_error',
      framework: framework,
      message: typeof message === 'string' ? message : String(message),
      details: details,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };
    
    if (details?.stack) {
      error.stack = details.stack;
    }
    
    this.reportError(error);
  }

  reportError(error) {
    // Deduplicate errors
    const isDuplicate = this.errors.some(e => 
      e.message === error.message && 
      e.type === error.type &&
      Math.abs(new Date(e.timestamp) - new Date(error.timestamp)) < 1000
    );
    
    if (!isDuplicate) {
      this.errors.push(error);
      
      // Send to background script
      chrome.runtime.sendMessage({
        action: 'error_detected',
        error: error
      }).catch(err => {
        // Extension might be reloading
        console.warn('CCDebugger: Failed to send error to background', err);
      });
    }
  }

  forceAnalysis() {
    // Re-send all collected errors
    this.errors.forEach(error => {
      chrome.runtime.sendMessage({
        action: 'error_detected',
        error: error
      }).catch(() => {});
    });
  }

  setMonitoring(enabled) {
    this.isMonitoring = enabled;
  }
}

// Initialize error detector
window.ccDebuggerErrorDetector = new ErrorDetector();

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ErrorDetector;
}
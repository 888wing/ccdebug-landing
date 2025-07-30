/**
 * CCDebugger Chrome Extension - DevTools Integration
 * Creates a custom panel in Chrome DevTools for error analysis
 */

// Create the CCDebugger panel
chrome.devtools.panels.create(
  "CCDebugger",
  "assets/icons/icon-32.png",
  "devtools/panel.html",
  function(panel) {
    // Panel created successfully
    console.log("CCDebugger DevTools panel created");
    
    // Set up communication with the panel
    let panelWindow = null;
    
    panel.onShown.addListener(function(window) {
      panelWindow = window;
      // Initialize panel when shown
      if (panelWindow.initializePanel) {
        panelWindow.initializePanel();
      }
    });
    
    panel.onHidden.addListener(function() {
      panelWindow = null;
    });
  }
);

// Add a sidebar pane to the Elements panel
chrome.devtools.panels.elements.createSidebarPane(
  "CCDebugger Analysis",
  function(sidebar) {
    // Update sidebar when element selection changes
    chrome.devtools.panels.elements.onSelectionChanged.addListener(function() {
      sidebar.setExpression("(() => { const el = $0; return el ? { tagName: el.tagName, id: el.id, className: el.className, attributes: Array.from(el.attributes || []).map(a => ({name: a.name, value: a.value})) } : null; })()");
    });
  }
);

// Listen for network errors
chrome.devtools.network.onRequestFinished.addListener(function(request) {
  if (request.response.status >= 400) {
    // Network error detected, notify the panel
    chrome.runtime.sendMessage({
      action: 'devtools_network_error',
      error: {
        url: request.request.url,
        method: request.request.method,
        status: request.response.status,
        statusText: request.response.statusText
      }
    });
  }
});

// Console API integration
chrome.devtools.inspectedWindow.eval(
  `
  // Override console methods to capture errors in DevTools
  (function() {
    const originalError = console.error;
    const originalWarn = console.warn;
    
    console.error = function(...args) {
      // Send to DevTools panel
      chrome.runtime.sendMessage({
        action: 'devtools_console_error',
        level: 'error',
        args: args.map(arg => {
          try {
            return typeof arg === 'object' ? JSON.stringify(arg) : String(arg);
          } catch {
            return String(arg);
          }
        })
      });
      
      return originalError.apply(console, args);
    };
    
    console.warn = function(...args) {
      const message = args.join(' ').toLowerCase();
      if (message.includes('error') || message.includes('fail')) {
        chrome.runtime.sendMessage({
          action: 'devtools_console_error',
          level: 'warning',
          args: args.map(arg => {
            try {
              return typeof arg === 'object' ? JSON.stringify(arg) : String(arg);
            } catch {
              return String(arg);
            }
          })
        });
      }
      
      return originalWarn.apply(console, args);
    };
  })();
  `,
  function(result, error) {
    if (error) {
      console.error("Failed to inject console interceptor:", error);
    }
  }
);
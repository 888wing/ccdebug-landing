/**
 * CCDebugger Chrome Extension - Options Script
 * Settings page functionality
 */

class OptionsPage {
  constructor() {
    this.init();
  }

  async init() {
    // Display version
    this.displayVersion();
    
    // Load current settings
    await this.loadSettings();
    
    // Localize UI
    this.localizeUI();
    
    // Setup event listeners
    this.setupListeners();
  }

  displayVersion() {
    const manifest = chrome.runtime.getManifest();
    document.getElementById('version').textContent = manifest.version;
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
  }

  async loadSettings() {
    try {
      // Get all settings
      const settings = await window.settingsManager.getAll();
      
      // General Settings
      document.getElementById('enableMonitoring').checked = settings.enableMonitoring;
      document.getElementById('enableNotifications').checked = settings.enableNotifications;
      document.getElementById('enableBadge').checked = settings.enableBadge;
      document.getElementById('language').value = settings.language;
      document.getElementById('maxErrors').value = settings.maxErrors;
      
      // API Configuration
      document.getElementById('apiEndpoint').value = settings.apiEndpoint;
      document.getElementById('apiKey').value = settings.apiKey || '';
      
      // Error Filtering
      document.getElementById('ignoredDomains').value = settings.ignoredDomains.join('\n');
      document.getElementById('ignoredErrors').value = settings.ignoredErrors.join('\n');
      
      // Advanced Settings
      document.getElementById('debugMode').checked = settings.debugMode;
      document.getElementById('theme').value = settings.theme;
      
    } catch (error) {
      console.error('Failed to load settings:', error);
      this.showStatus('Failed to load settings', 'error');
    }
  }

  async saveSettings() {
    try {
      // Gather all settings
      const settings = {
        // General Settings
        enableMonitoring: document.getElementById('enableMonitoring').checked,
        enableNotifications: document.getElementById('enableNotifications').checked,
        enableBadge: document.getElementById('enableBadge').checked,
        language: document.getElementById('language').value,
        maxErrors: parseInt(document.getElementById('maxErrors').value, 10),
        
        // API Configuration
        apiEndpoint: document.getElementById('apiEndpoint').value || 'https://api.ccdebugger.com/analyze',
        apiKey: document.getElementById('apiKey').value,
        
        // Error Filtering
        ignoredDomains: this.parseTextarea(document.getElementById('ignoredDomains').value),
        ignoredErrors: this.parseTextarea(document.getElementById('ignoredErrors').value),
        
        // Advanced Settings
        debugMode: document.getElementById('debugMode').checked,
        theme: document.getElementById('theme').value
      };
      
      // Validate settings
      if (!this.validateSettings(settings)) {
        return;
      }
      
      // Save settings
      await window.settingsManager.update(settings);
      
      // Show success message
      this.showStatus('Settings saved successfully!', 'success');
      
      // Apply language change if needed
      if (settings.language !== chrome.i18n.getUILanguage()) {
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      }
      
    } catch (error) {
      console.error('Failed to save settings:', error);
      this.showStatus('Failed to save settings', 'error');
    }
  }

  parseTextarea(value) {
    return value
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);
  }

  validateSettings(settings) {
    // Validate API endpoint
    if (settings.apiEndpoint) {
      try {
        new URL(settings.apiEndpoint);
      } catch {
        this.showStatus('Invalid API endpoint URL', 'error');
        document.getElementById('apiEndpoint').focus();
        return false;
      }
    }
    
    // Validate max errors
    if (settings.maxErrors < 10 || settings.maxErrors > 500) {
      this.showStatus('Maximum errors must be between 10 and 500', 'error');
      document.getElementById('maxErrors').focus();
      return false;
    }
    
    // Validate ignored error patterns (regex)
    for (const pattern of settings.ignoredErrors) {
      try {
        new RegExp(pattern);
      } catch {
        this.showStatus(`Invalid regex pattern: ${pattern}`, 'error');
        document.getElementById('ignoredErrors').focus();
        return false;
      }
    }
    
    return true;
  }

  async resetSettings() {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      try {
        await window.settingsManager.reset();
        await this.loadSettings();
        this.showStatus('Settings reset to defaults', 'success');
      } catch (error) {
        console.error('Failed to reset settings:', error);
        this.showStatus('Failed to reset settings', 'error');
      }
    }
  }

  async exportSettings() {
    try {
      const data = await window.settingsManager.export();
      const json = JSON.stringify(data, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `ccdebugger-settings-${Date.now()}.json`;
      a.click();
      
      URL.revokeObjectURL(url);
      this.showStatus('Settings exported successfully', 'success');
    } catch (error) {
      console.error('Failed to export settings:', error);
      this.showStatus('Failed to export settings', 'error');
    }
  }

  async importSettings() {
    const fileInput = document.getElementById('importFile');
    fileInput.click();
  }

  async handleImportFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      
      if (!data || !data.settings) {
        throw new Error('Invalid settings file');
      }
      
      await window.settingsManager.import(data);
      await this.loadSettings();
      this.showStatus('Settings imported successfully', 'success');
      
    } catch (error) {
      console.error('Failed to import settings:', error);
      this.showStatus('Failed to import settings. Please check the file format.', 'error');
    }
    
    // Clear file input
    event.target.value = '';
  }

  showStatus(message, type = 'success') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
    statusEl.style.display = 'block';
    
    // Auto-hide after 3 seconds
    clearTimeout(this.statusTimeout);
    this.statusTimeout = setTimeout(() => {
      statusEl.style.display = 'none';
    }, 3000);
  }

  setupListeners() {
    // Save button
    document.getElementById('saveSettings').addEventListener('click', () => {
      this.saveSettings();
    });
    
    // Reset button
    document.getElementById('resetSettings').addEventListener('click', () => {
      this.resetSettings();
    });
    
    // Export button
    document.getElementById('exportSettings').addEventListener('click', () => {
      this.exportSettings();
    });
    
    // Import button
    document.getElementById('importSettings').addEventListener('click', () => {
      this.importSettings();
    });
    
    // Import file input
    document.getElementById('importFile').addEventListener('change', (event) => {
      this.handleImportFile(event);
    });
    
    // Auto-save on Enter key in text inputs
    document.querySelectorAll('input[type="text"], input[type="url"], input[type="number"]').forEach(input => {
      input.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
          this.saveSettings();
        }
      });
    });
    
    // Theme change preview
    document.getElementById('theme').addEventListener('change', (event) => {
      this.applyTheme(event.target.value);
    });
  }

  applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.style.colorScheme = 'dark';
    } else if (theme === 'light') {
      document.documentElement.style.colorScheme = 'light';
    } else {
      document.documentElement.style.colorScheme = 'auto';
    }
  }
}

// Initialize options page when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new OptionsPage();
});
/**
 * CCDebugger Chrome Extension - Storage Helper
 * Utilities for managing extension storage
 */

class StorageHelper {
  constructor() {
    this.cache = new Map();
  }

  /**
   * Get value from storage
   * @param {string|string[]} keys - Storage key(s) to retrieve
   * @param {Object} defaults - Default values if keys don't exist
   * @returns {Promise<Object>} Retrieved values
   */
  async get(keys, defaults = {}) {
    try {
      const result = await chrome.storage.sync.get(keys);
      return { ...defaults, ...result };
    } catch (error) {
      console.error('Storage get error:', error);
      return defaults;
    }
  }

  /**
   * Set value in storage
   * @param {Object} items - Key-value pairs to store
   * @returns {Promise<void>}
   */
  async set(items) {
    try {
      await chrome.storage.sync.set(items);
      // Update cache
      Object.entries(items).forEach(([key, value]) => {
        this.cache.set(key, value);
      });
    } catch (error) {
      console.error('Storage set error:', error);
      throw error;
    }
  }

  /**
   * Remove items from storage
   * @param {string|string[]} keys - Keys to remove
   * @returns {Promise<void>}
   */
  async remove(keys) {
    try {
      await chrome.storage.sync.remove(keys);
      // Update cache
      if (Array.isArray(keys)) {
        keys.forEach(key => this.cache.delete(key));
      } else {
        this.cache.delete(keys);
      }
    } catch (error) {
      console.error('Storage remove error:', error);
      throw error;
    }
  }

  /**
   * Clear all storage
   * @returns {Promise<void>}
   */
  async clear() {
    try {
      await chrome.storage.sync.clear();
      this.cache.clear();
    } catch (error) {
      console.error('Storage clear error:', error);
      throw error;
    }
  }

  /**
   * Get storage usage
   * @returns {Promise<{bytesInUse: number, quota: number}>}
   */
  async getUsage() {
    try {
      const bytesInUse = await chrome.storage.sync.getBytesInUse();
      const quota = chrome.storage.sync.QUOTA_BYTES;
      return { bytesInUse, quota };
    } catch (error) {
      console.error('Storage usage error:', error);
      return { bytesInUse: 0, quota: 0 };
    }
  }

  /**
   * Listen for storage changes
   * @param {Function} callback - Function to call when storage changes
   * @returns {Function} Function to remove listener
   */
  onChange(callback) {
    const listener = (changes, areaName) => {
      if (areaName === 'sync') {
        callback(changes);
      }
    };
    
    chrome.storage.onChanged.addListener(listener);
    
    // Return function to remove listener
    return () => chrome.storage.onChanged.removeListener(listener);
  }
}

// Settings management
class SettingsManager {
  constructor() {
    this.storage = new StorageHelper();
    this.defaults = {
      enableMonitoring: true,
      apiEndpoint: 'https://api.ccdebugger.com/analyze',
      language: 'en',
      maxErrors: 100,
      enableNotifications: true,
      enableBadge: true,
      theme: 'auto',
      debugMode: false,
      customPatterns: [],
      ignoredDomains: [],
      ignoredErrors: []
    };
  }

  /**
   * Get all settings
   * @returns {Promise<Object>} Current settings
   */
  async getAll() {
    return await this.storage.get(Object.keys(this.defaults), this.defaults);
  }

  /**
   * Get specific setting
   * @param {string} key - Setting key
   * @returns {Promise<any>} Setting value
   */
  async get(key) {
    const settings = await this.getAll();
    return settings[key];
  }

  /**
   * Update settings
   * @param {Object} updates - Settings to update
   * @returns {Promise<void>}
   */
  async update(updates) {
    // Validate settings
    const validUpdates = {};
    Object.entries(updates).forEach(([key, value]) => {
      if (key in this.defaults) {
        validUpdates[key] = value;
      }
    });
    
    await this.storage.set(validUpdates);
  }

  /**
   * Reset settings to defaults
   * @returns {Promise<void>}
   */
  async reset() {
    await this.storage.set(this.defaults);
  }

  /**
   * Export settings
   * @returns {Promise<Object>} Settings object
   */
  async export() {
    const settings = await this.getAll();
    return {
      version: chrome.runtime.getManifest().version,
      timestamp: new Date().toISOString(),
      settings: settings
    };
  }

  /**
   * Import settings
   * @param {Object} data - Settings data to import
   * @returns {Promise<void>}
   */
  async import(data) {
    if (data && data.settings) {
      await this.update(data.settings);
    }
  }
}

// Error storage management
class ErrorStorage {
  constructor() {
    this.storage = new StorageHelper();
    this.maxErrors = 100;
  }

  /**
   * Store error for a tab
   * @param {number} tabId - Tab ID
   * @param {Object} error - Error object
   * @returns {Promise<void>}
   */
  async storeError(tabId, error) {
    const key = `errors_${tabId}`;
    const errors = await this.getErrors(tabId);
    
    // Add error with timestamp
    errors.push({
      ...error,
      id: `${tabId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: error.timestamp || new Date().toISOString()
    });
    
    // Limit number of errors
    if (errors.length > this.maxErrors) {
      errors.splice(0, errors.length - this.maxErrors);
    }
    
    await this.storage.set({ [key]: errors });
  }

  /**
   * Get errors for a tab
   * @param {number} tabId - Tab ID
   * @returns {Promise<Array>} Array of errors
   */
  async getErrors(tabId) {
    const key = `errors_${tabId}`;
    const result = await this.storage.get(key, { [key]: [] });
    return result[key] || [];
  }

  /**
   * Clear errors for a tab
   * @param {number} tabId - Tab ID
   * @returns {Promise<void>}
   */
  async clearErrors(tabId) {
    const key = `errors_${tabId}`;
    await this.storage.remove(key);
  }

  /**
   * Get all stored errors
   * @returns {Promise<Object>} Object with tabId as keys and error arrays as values
   */
  async getAllErrors() {
    const allData = await chrome.storage.sync.get(null);
    const errors = {};
    
    Object.entries(allData).forEach(([key, value]) => {
      if (key.startsWith('errors_')) {
        const tabId = key.replace('errors_', '');
        errors[tabId] = value;
      }
    });
    
    return errors;
  }

  /**
   * Clear all errors
   * @returns {Promise<void>}
   */
  async clearAll() {
    const allData = await chrome.storage.sync.get(null);
    const errorKeys = Object.keys(allData).filter(key => key.startsWith('errors_'));
    await this.storage.remove(errorKeys);
  }
}

// Export instances
window.storageHelper = new StorageHelper();
window.settingsManager = new SettingsManager();
window.errorStorage = new ErrorStorage();
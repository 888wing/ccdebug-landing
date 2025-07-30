import { ErrorData, ChromeTab } from '../types';

export async function getCurrentTab(): Promise<ChromeTab | null> {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab || null;
  } catch (error) {
    console.error('Failed to get current tab:', error);
    return null;
  }
}

export async function getStoredErrors(tabId: number): Promise<ErrorData[]> {
  try {
    const key = `errors_${tabId}`;
    const result = await chrome.storage.local.get(key);
    return result[key] || [];
  } catch (error) {
    console.error('Failed to get stored errors:', error);
    return [];
  }
}

export async function clearStoredErrors(tabId: number): Promise<void> {
  try {
    const key = `errors_${tabId}`;
    await chrome.storage.local.remove(key);
    
    // Also send message to content script to clear errors
    chrome.tabs.sendMessage(tabId, { type: 'CLEAR_ERRORS' });
  } catch (error) {
    console.error('Failed to clear stored errors:', error);
  }
}

export async function getMonitoringStatus(): Promise<boolean> {
  try {
    const result = await chrome.storage.local.get('monitoring');
    return result.monitoring || false;
  } catch (error) {
    console.error('Failed to get monitoring status:', error);
    return false;
  }
}

export async function setMonitoringStatus(enabled: boolean): Promise<void> {
  try {
    await chrome.storage.local.set({ monitoring: enabled });
  } catch (error) {
    console.error('Failed to set monitoring status:', error);
  }
}
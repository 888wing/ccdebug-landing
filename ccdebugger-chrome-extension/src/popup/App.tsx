import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ErrorSummary from './components/ErrorSummary';
import ErrorList from './components/ErrorList';
import Footer from './components/Footer';
import LoadingState from './components/LoadingState';
import { ErrorData, AppState } from './types';
import { analyzeError } from './utils/api';
import { getCurrentTab, getStoredErrors, clearStoredErrors } from './utils/chrome';

const App: React.FC = () => {
  const [state, setState] = useState<AppState>({
    errors: [],
    isLoading: false,
    isMonitoring: false,
    currentUrl: ''
  });

  // Load initial data
  useEffect(() => {
    loadInitialData();
    setupMessageListener();
  }, []);

  const loadInitialData = async () => {
    try {
      const tab = await getCurrentTab();
      if (tab?.url) {
        setState(prev => ({ ...prev, currentUrl: tab.url || '' }));
        
        // Load stored errors for this tab
        const errors = await getStoredErrors(tab.id!);
        setState(prev => ({ ...prev, errors }));
      }
      
      // Check monitoring status
      const { monitoring = false } = await chrome.storage.local.get('monitoring');
      setState(prev => ({ ...prev, isMonitoring: monitoring }));
    } catch (error) {
      console.error('Failed to load initial data:', error);
    }
  };

  const setupMessageListener = () => {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.type === 'ERROR_DETECTED') {
        handleNewError(message.error);
      }
    });
  };

  const handleNewError = async (error: ErrorData) => {
    setState(prev => ({ ...prev, isLoading: true }));
    
    try {
      // Analyze error with AI
      const analysis = await analyzeError(error);
      const enrichedError = { ...error, analysis };
      
      setState(prev => ({
        ...prev,
        errors: [...prev.errors, enrichedError],
        isLoading: false
      }));
    } catch (err) {
      console.error('Failed to analyze error:', err);
      setState(prev => ({
        ...prev,
        errors: [...prev.errors, error],
        isLoading: false
      }));
    }
  };

  const handleClearErrors = async () => {
    const tab = await getCurrentTab();
    if (tab?.id) {
      await clearStoredErrors(tab.id);
      setState(prev => ({ ...prev, errors: [] }));
    }
  };

  const handleExport = () => {
    const report = {
      url: state.currentUrl,
      timestamp: new Date().toISOString(),
      errors: state.errors
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ccdebugger-report-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const toggleMonitoring = async () => {
    const newState = !state.isMonitoring;
    await chrome.storage.local.set({ monitoring: newState });
    setState(prev => ({ ...prev, isMonitoring: newState }));
    
    // Send message to background script
    chrome.runtime.sendMessage({ 
      type: 'TOGGLE_MONITORING', 
      enabled: newState 
    });
  };

  const openSettings = () => {
    chrome.runtime.openOptionsPage();
  };

  return (
    <div className="app">
      <Header onSettingsClick={openSettings} />
      
      <ErrorSummary 
        errorCount={state.errors.length}
        currentUrl={state.currentUrl}
        onClear={handleClearErrors}
      />
      
      {state.isLoading && <LoadingState />}
      
      <ErrorList errors={state.errors} />
      
      <Footer 
        onExport={handleExport}
        isMonitoring={state.isMonitoring}
        onToggleMonitoring={toggleMonitoring}
        hasErrors={state.errors.length > 0}
      />
    </div>
  );
};

export default App;
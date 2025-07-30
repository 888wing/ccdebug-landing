import React from 'react';
import clsx from 'clsx';

interface ErrorSummaryProps {
  errorCount: number;
  currentUrl: string;
  onClear: () => void;
}

const ErrorSummary: React.FC<ErrorSummaryProps> = ({ errorCount, currentUrl, onClear }) => {
  const getDomain = (url: string) => {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname;
    } catch {
      return url;
    }
  };

  return (
    <div className="summary-section">
      <div className={clsx('summary-card', { 'has-errors': errorCount > 0 })}>
        <div className="summary-icon error-icon">
          <span>{errorCount}</span>
        </div>
        <div className="summary-text">
          <h2>
            {errorCount === 0 
              ? chrome.i18n.getMessage('noErrorsDetected') || 'No errors detected'
              : chrome.i18n.getMessage('errorCount', [errorCount.toString()]) || `${errorCount} errors detected`
            }
          </h2>
          <p className="summary-subtitle">{getDomain(currentUrl)}</p>
        </div>
        {errorCount > 0 && (
          <button 
            className="clear-btn" 
            onClick={onClear}
          >
            {chrome.i18n.getMessage('clearErrors') || 'Clear All'}
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorSummary;
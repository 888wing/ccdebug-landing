import React from 'react';
import clsx from 'clsx';
import { ErrorData } from '../types';

interface ErrorItemProps {
  error: ErrorData;
  isExpanded: boolean;
  onToggle: () => void;
}

const ErrorItem: React.FC<ErrorItemProps> = ({ error, isExpanded, onToggle }) => {
  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case 'critical': return 'error-critical';
      case 'high': return 'error-high';
      case 'medium': return 'error-medium';
      case 'low': return 'error-low';
      default: return 'error-medium';
    }
  };

  const getTimeAgo = (timestamp: number) => {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return chrome.i18n.getMessage('justNow') || 'Just now';
    if (seconds < 3600) return chrome.i18n.getMessage('minutesAgo', [Math.floor(seconds / 60).toString()]) || `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return chrome.i18n.getMessage('hoursAgo', [Math.floor(seconds / 3600).toString()]) || `${Math.floor(seconds / 3600)}h ago`;
    return chrome.i18n.getMessage('daysAgo', [Math.floor(seconds / 86400).toString()]) || `${Math.floor(seconds / 86400)}d ago`;
  };

  return (
    <div className={clsx('error-item', getSeverityColor(error.analysis?.severity))}>
      <div className="error-header" onClick={onToggle}>
        <div className="error-info">
          <span className="error-type">{error.type.toUpperCase()}</span>
          <span className="error-time">{getTimeAgo(error.timestamp)}</span>
        </div>
        <div className="error-message">{error.message}</div>
        {error.source && (
          <div className="error-location">
            {error.source}
            {error.line && `:${error.line}`}
            {error.column && `:${error.column}`}
          </div>
        )}
        <button className="expand-btn">
          <svg 
            width="16" 
            height="16" 
            viewBox="0 0 16 16" 
            fill="none"
            className={clsx({ 'rotated': isExpanded })}
          >
            <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>

      {isExpanded && error.analysis && (
        <div className="error-details">
          <div className="analysis-section">
            <h4>{chrome.i18n.getMessage('explanation') || 'Explanation'}</h4>
            <p>{error.analysis.explanation}</p>
          </div>

          {error.analysis.suggestions.length > 0 && (
            <div className="suggestions-section">
              <h4>{chrome.i18n.getMessage('suggestions') || 'Suggestions'}</h4>
              {error.analysis.suggestions.map(suggestion => (
                <div key={suggestion.id} className="suggestion-item">
                  <h5>{suggestion.title}</h5>
                  <p>{suggestion.description}</p>
                  {suggestion.codeExample && (
                    <pre className="code-example">
                      <code>{suggestion.codeExample}</code>
                    </pre>
                  )}
                  <div className="suggestion-meta">
                    <span className="confidence">
                      {chrome.i18n.getMessage('confidence') || 'Confidence'}: {Math.round(suggestion.confidence * 100)}%
                    </span>
                    {suggestion.documentationUrl && (
                      <a 
                        href={suggestion.documentationUrl} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="doc-link"
                      >
                        {chrome.i18n.getMessage('learnMore') || 'Learn more'}
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {error.stack && (
            <div className="stack-trace-section">
              <h4>{chrome.i18n.getMessage('stackTrace') || 'Stack Trace'}</h4>
              <pre className="stack-trace">
                <code>{error.stack}</code>
              </pre>
            </div>
          )}

          {error.analysis.tags && error.analysis.tags.length > 0 && (
            <div className="tags-section">
              {error.analysis.tags.map(tag => (
                <span key={tag} className="tag">{tag}</span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ErrorItem;
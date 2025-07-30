import React, { useState } from 'react';
import { ErrorData } from '../types';
import ErrorItem from './ErrorItem';

interface ErrorListProps {
  errors: ErrorData[];
}

const ErrorList: React.FC<ErrorListProps> = ({ errors }) => {
  const [expandedErrors, setExpandedErrors] = useState<Set<string>>(new Set());

  const toggleError = (errorId: string) => {
    setExpandedErrors(prev => {
      const newSet = new Set(prev);
      if (newSet.has(errorId)) {
        newSet.delete(errorId);
      } else {
        newSet.add(errorId);
      }
      return newSet;
    });
  };

  if (errors.length === 0) {
    return (
      <div className="error-container">
        <div className="no-errors">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none" className="no-errors-icon">
            <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="2" opacity="0.2"/>
            <path d="M16 24L22 30L32 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <p>{chrome.i18n.getMessage('noErrors') || 'No errors detected on this page'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="error-container">
      <div className="error-list">
        {errors.map(error => (
          <ErrorItem
            key={error.id}
            error={error}
            isExpanded={expandedErrors.has(error.id)}
            onToggle={() => toggleError(error.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default ErrorList;
import React from 'react';

const LoadingState: React.FC = () => {
  return (
    <div className="loading">
      <div className="spinner"></div>
      <p>{chrome.i18n.getMessage('analyzing') || 'Analyzing...'}</p>
    </div>
  );
};

export default LoadingState;
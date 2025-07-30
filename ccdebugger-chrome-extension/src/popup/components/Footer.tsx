import React from 'react';
import clsx from 'clsx';

interface FooterProps {
  onExport: () => void;
  isMonitoring: boolean;
  onToggleMonitoring: () => void;
  hasErrors: boolean;
}

const Footer: React.FC<FooterProps> = ({ 
  onExport, 
  isMonitoring, 
  onToggleMonitoring, 
  hasErrors 
}) => {
  return (
    <footer className="footer">
      <button 
        className="footer-btn" 
        onClick={onExport}
        disabled={!hasErrors}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M8 11V3M8 3L5 6M8 3L11 6M3 13H13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        {chrome.i18n.getMessage('exportReport') || 'Export Report'}
      </button>
      
      <button 
        className={clsx('footer-btn', 'toggle-btn', { 'active': isMonitoring })}
        onClick={onToggleMonitoring}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5"/>
          <circle cx="8" cy="8" r="2" fill="currentColor"/>
        </svg>
        <span>
          {isMonitoring 
            ? chrome.i18n.getMessage('disableMonitoring') || 'Disable Monitoring'
            : chrome.i18n.getMessage('enableMonitoring') || 'Enable Monitoring'
          }
        </span>
      </button>
    </footer>
  );
};

export default Footer;
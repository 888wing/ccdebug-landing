import React from 'react';

interface HeaderProps {
  onSettingsClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onSettingsClick }) => {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">
          <img src="/assets/icons/icon-32.png" alt="CCDebugger" className="header-icon" />
          <span>{chrome.i18n.getMessage('extensionName') || 'CCDebugger'}</span>
        </h1>
        <button 
          className="icon-btn" 
          onClick={onSettingsClick}
          title={chrome.i18n.getMessage('settings') || 'Settings'}
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 12.5C11.38 12.5 12.5 11.38 12.5 10C12.5 8.62 11.38 7.5 10 7.5C8.62 7.5 7.5 8.62 7.5 10C7.5 11.38 8.62 12.5 10 12.5Z" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M16.17 10.86L17.51 9.9C17.66 9.78 17.73 9.58 17.68 9.39L16.38 5.49C16.33 5.3 16.16 5.17 15.97 5.17L14.3 5.17C14.04 5.17 13.8 5.05 13.66 4.85L12.77 3.46C12.63 3.26 12.58 3 12.65 2.76L13.22 1.02C13.29 0.78 13.22 0.52 13.04 0.35L9.88 0.03C9.7 -0.14 9.44 -0.07 9.34 0.1L8.38 1.44C8.24 1.64 7.99 1.76 7.73 1.76L6.27 1.76C6.01 1.76 5.76 1.64 5.62 1.44L4.66 0.1C4.56 -0.07 4.3 -0.14 4.12 0.03L0.96 0.35C0.78 0.52 0.71 0.78 0.78 1.02L1.35 2.76C1.42 3 1.37 3.26 1.23 3.46L0.34 4.85C0.2 5.05 -0.04 5.17 -0.3 5.17L-1.97 5.17C-2.16 5.17 -2.33 5.3 -2.38 5.49L-3.68 9.39C-3.73 9.58 -3.66 9.78 -3.51 9.9L-2.17 10.86" stroke="currentColor" strokeWidth="1.5"/>
          </svg>
        </button>
      </div>
    </header>
  );
};

export default Header;
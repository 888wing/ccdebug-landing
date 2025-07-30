# CCDebugger Chrome Extension - React Version

This is the React-based version of the CCDebugger Chrome Extension, providing a modern and maintainable UI architecture.

## Features

- 🚀 **React 18** with TypeScript for type safety
- 📦 **Webpack 5** for optimized builds
- 🎨 **Modern UI** with responsive design and dark mode support
- 🌍 **Internationalization** support (English and Chinese)
- 🔄 **Real-time error monitoring** with AI-powered analysis
- 📊 **Export functionality** for error reports

## Development Setup

### Prerequisites

- Node.js 16+ and npm
- Chrome browser for testing

### Installation

1. Install dependencies:
```bash
cd ccdebugger-chrome-extension
npm install
```

2. Build the extension:
```bash
# Development build with watch mode
npm run dev

# Production build
npm run build
```

3. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `dist` folder

### Project Structure

```
src/
├── popup/              # Popup UI React components
│   ├── index.tsx      # Entry point
│   ├── App.tsx        # Main app component
│   ├── components/    # React components
│   ├── utils/         # Utility functions
│   ├── types.ts       # TypeScript definitions
│   └── popup.css      # Styles
├── options/           # Options page (placeholder)
└── ...

dist/                  # Built extension files
```

## React Components

### Core Components

- **App.tsx**: Main application container
- **Header**: Extension header with settings button
- **ErrorSummary**: Error count and current page info
- **ErrorList**: List of detected errors
- **ErrorItem**: Individual error with expandable details
- **Footer**: Export and monitoring controls
- **LoadingState**: Loading spinner

### State Management

The app uses React hooks for state management:
- `useState` for local component state
- `useEffect` for side effects and Chrome API integration

### Chrome API Integration

The React app integrates with Chrome Extension APIs:
- **chrome.tabs**: Get current tab information
- **chrome.storage**: Persist settings and errors
- **chrome.runtime**: Message passing with background script
- **chrome.i18n**: Internationalization support

## Build Process

The webpack configuration handles:
- TypeScript compilation
- React JSX transformation
- CSS bundling
- Asset copying (manifest, icons, locales)
- Source maps for debugging

## API Integration

The extension communicates with the CCDebugger backend API:
- Endpoint: `https://api.ccdebugger.com/analyze`
- Fallback to local analysis when offline
- Timeout handling for slow connections

## Styling

- Modern, clean design with Tailwind-inspired utility classes
- Dark mode support based on system preferences
- Responsive layout that works well at 400px width
- Smooth animations and transitions

## Future Enhancements

- [ ] Redux or Zustand for advanced state management
- [ ] React Query for API data fetching
- [ ] More comprehensive error filtering
- [ ] Custom hooks for Chrome API operations
- [ ] Unit tests with React Testing Library

## Development Tips

1. Use React DevTools extension for debugging
2. Check console for API responses and errors
3. Test with various error scenarios
4. Verify i18n works for all supported languages

## Migration from Vanilla JS

The original vanilla JS popup has been migrated to React with:
- Component-based architecture
- Better state management
- Improved type safety
- Easier maintenance and testing

All original functionality has been preserved while adding:
- Better error boundaries
- Improved performance with React optimizations
- Cleaner code organization
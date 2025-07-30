# CCDebugger Project Overview

CCDebugger is an AI-powered debugging assistant that helps developers understand and fix errors more efficiently across multiple platforms and programming languages.

## 🚀 Recent Updates (January 29, 2025)

### New Features
- **Swift Language Support**: Complete error analysis for iOS/macOS development
- **Kotlin Language Support**: Comprehensive Android development error handling
- **Chrome Extension MVP**: Real-time browser error detection and analysis
- **Enhanced API Integration**: Robust client-server communication

## 🎯 Project Components

### 1. CCDebugger Core (Python)
The main error analysis engine supporting multiple programming languages:
- Python, JavaScript, TypeScript, Java, Ruby, Go
- **NEW**: Swift (iOS/macOS)
- **NEW**: Kotlin (Android)
- C++, C, C#, PHP, Rust

### 2. Chrome Extension
Real-time error detection and analysis for web developers:
- **Manifest V3** compliant
- **Error Detection**: Console errors, network errors, promise rejections
- **Framework Support**: React, Vue, Angular
- **Internationalization**: English and Chinese (中文)
- **Features**:
  - Real-time error monitoring
  - AI-powered analysis
  - Export error reports
  - Customizable settings
  - Dark mode support

### 3. VS Code Extension
Deep IDE integration for comprehensive debugging (Enhanced in Q1 2025)

### 4. Landing Page
Modern marketing and documentation site built with:
- Next.js 15 with App Router
- Tailwind CSS & shadcn/ui
- TypeScript
- Blog system with category filtering
- Complete documentation

## 📂 Project Structure

```
ccdebugger-landing/
├── src/                      # Landing page source
├── ccdebugger-chrome-extension/  # Chrome extension
│   ├── manifest.json         # Extension configuration
│   ├── background/           # Service worker
│   ├── content/              # Content scripts
│   ├── popup/                # Extension UI
│   ├── options/              # Settings page
│   └── lib/                  # Shared libraries
├── swift_analyzer.py         # Swift language analyzer
├── kotlin_analyzer.py        # Kotlin language analyzer
├── TODO.md                   # Development roadmap
└── docs/                     # Documentation

```

## 🛠️ Installation & Development

### Chrome Extension Development
```bash
# Load extension in Chrome
1. Open chrome://extensions/
2. Enable Developer mode
3. Click "Load unpacked"
4. Select ccdebugger-chrome-extension folder
```

### Landing Page Development
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Deploy to GitHub Pages
npm run deploy
```

### Core Analyzer Testing
```bash
# Test Swift analyzer
python test_swift_analyzer.py

# Test Kotlin analyzer
python test_kotlin_analyzer.py
```

## 🔌 API Integration

The Chrome Extension communicates with the CCDebugger backend API:

### API Endpoints
- `POST /analyze` - Analyze error with AI
- `GET /patterns/{language}` - Get error patterns
- `POST /feedback` - Submit analysis feedback

### Example Request
```javascript
const analysis = await apiClient.analyzeError({
  type: 'runtime_error',
  message: 'Cannot read property of undefined',
  stack: errorStack,
  url: window.location.href
});
```

## 🌍 Supported Languages

### Programming Languages
- **Web**: JavaScript, TypeScript, HTML/CSS
- **Backend**: Python, Java, Ruby, Go, PHP
- **Mobile**: Swift (iOS), Kotlin (Android)
- **Systems**: C, C++, Rust, C#
- **Config**: YAML, JSON, Docker (coming soon)
- **Database**: SQL (coming soon)

### Natural Languages
- English
- 中文 (Chinese)

## 📈 Development Roadmap

### Q2 2025 (Current)
- ✅ Swift language support
- ✅ Kotlin language support
- ✅ Chrome Extension MVP
- ⏳ SQL language support
- ⏳ Shell/Bash scripting support
- ⏳ API documentation

### Q3 2025
- Predictive error detection
- CI/CD integration
- Custom AI model training

### Q4 2025
- Enterprise features
- Plugin ecosystem
- Real-time collaboration

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built for the Claude Code community
- Powered by AI error analysis
- Special thanks to all contributors

## 📬 Links

- **Website**: [https://888wing.github.io/ccdebug-landing/](https://888wing.github.io/ccdebug-landing/)
- **GitHub**: [https://github.com/888wing/ccdebugger](https://github.com/888wing/ccdebugger)
- **Chrome Extension**: Coming to Chrome Web Store soon
- **VS Code Extension**: Available in marketplace

---

*Last updated: January 29, 2025*
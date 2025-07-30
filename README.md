# CCDebugger Landing Page & Chrome Extension

A comprehensive debugging platform featuring an AI-powered error analysis Chrome extension and a modern landing page.

**Project Location**: `/Users/chuisiufai/Desktop/CCDebugger/ccdebugger-landing/`

## Features

- **Modern Design**: Built with Next.js 15 and shadcn/ui for a clean, minimal aesthetic
- **Dark Mode Support**: Full dark mode support with theme toggle
- **Responsive Design**: Works perfectly on all devices
- **Smooth Animations**: Subtle animations for enhanced user experience
- **Multiple Pages**:
  - Home page with features, usage guide, and installation instructions
  - Releases page showcasing version history and changelogs
  - Blog page with technical articles and tutorials

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS v3
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **Animations**: Tailwind CSS animations + custom CSS
- **TypeScript**: Full type safety

## Getting Started

### Prerequisites

- Node.js 18.17 or later
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ccdebugger-landing.git
cd ccdebugger-landing
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Build for Production

```bash
npm run build
npm run start
```

## Project Structure

```
ccdebugger-landing/
├── src/
│   ├── app/                 # Next.js app directory
│   │   ├── page.tsx        # Home page
│   │   ├── layout.tsx      # Root layout
│   │   ├── globals.css     # Global styles
│   │   ├── blog/           # Blog pages
│   │   └── releases/       # Releases page
│   ├── components/         # React components
│   │   ├── ui/            # shadcn/ui components
│   │   ├── navigation.tsx # Navigation header
│   │   └── providers/     # Theme provider
│   └── lib/               # Utility functions
├── public/                # Static assets
├── tailwind.config.js     # Tailwind configuration
└── package.json          # Project dependencies
```

## Key Features Highlighted

1. **AI-Powered Error Analysis**: Intelligent error understanding and solution suggestions
2. **Smart Command Completion**: /ccdebug command with context-aware completions
3. **VS Code Extension Support**: Seamless integration with VS Code
4. **Multi-Language Support**: Full support for Chinese and English
5. **Real-Time Monitoring**: Monitor errors as they happen
6. **Custom Templates**: Create and share debugging templates

## Customization

### Theme Colors

Update the CSS variables in `src/app/globals.css` to customize the color scheme:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  /* ... other colors */
}
```

### Adding New Pages

1. Create a new directory in `src/app/`
2. Add a `page.tsx` file
3. Update navigation in `src/components/navigation.tsx`

### Modifying Components

All UI components are in `src/components/ui/` and can be customized as needed.

## Deployment

The site is optimized for deployment on Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/ccdebugger-landing)

## License

MIT License - feel free to use this for your own projects!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
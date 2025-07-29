import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { 
  Calendar, 
  Clock, 
  ChevronLeft,
  BookOpen,
  Copy,
  Check
} from "lucide-react"
import Link from "next/link"

export default function GettingStartedPost() {
  return (
    <div className="container px-4 md:px-6 py-12">
      <article className="max-w-4xl mx-auto">
        {/* Back Navigation */}
        <Button variant="ghost" size="sm" className="-ml-2 mb-8" asChild>
          <Link href="/blog">
            <ChevronLeft className="mr-1 h-4 w-4" />
            Back to Blog
          </Link>
        </Button>

        {/* Article Header */}
        <header className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Badge variant="secondary">
              <BookOpen className="mr-1 h-3 w-3" />
              Tutorial
            </Badge>
            <Badge variant="outline">Featured</Badge>
          </div>
          
          <h1 className="text-4xl font-bold tracking-tighter mb-4">
            Getting Started with CCDebugger: A Complete Guide
          </h1>
          
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              December 10, 2024
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              5 min read
            </span>
            <span>By CCDebugger Team</span>
          </div>
        </header>

        <Separator className="mb-8" />

        {/* Article Content */}
        <div className="prose prose-gray dark:prose-invert max-w-none">
          <p className="text-lg leading-relaxed">
            Welcome to CCDebugger! This guide will walk you through everything you need to know 
            to start using our AI-powered debugging tool for Claude Code. Whether you're a 
            beginner or an experienced developer, CCDebugger will transform how you debug code.
          </p>

          <h2 className="text-2xl font-semibold mt-8 mb-4">What is CCDebugger?</h2>
          <p>
            CCDebugger is an intelligent debugging assistant that uses AI to analyze, understand, 
            and help resolve errors in your Claude Code projects. It provides context-aware 
            suggestions, smart command completion, and real-time error monitoring.
          </p>

          <h2 className="text-2xl font-semibold mt-8 mb-4">Installation</h2>
          <p>
            There are several ways to install CCDebugger. Choose the method that works best for you:
          </p>

          <h3 className="text-xl font-semibold mt-6 mb-3">Method 1: VS Code Marketplace</h3>
          <ol className="list-decimal list-inside space-y-2">
            <li>Open Visual Studio Code</li>
            <li>Go to the Extensions view (Ctrl+Shift+X / Cmd+Shift+X)</li>
            <li>Search for "CCDebugger"</li>
            <li>Click the Install button</li>
          </ol>

          <h3 className="text-xl font-semibold mt-6 mb-3">Method 2: Command Line</h3>
          <div className="bg-muted rounded-lg p-4 my-4 relative group">
            <pre className="text-sm"><code>code --install-extension ccdebugger.vscode-extension</code></pre>
            <Button
              size="icon"
              variant="ghost"
              className="absolute top-2 right-2 h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <Copy className="h-4 w-4" />
            </Button>
          </div>

          <h2 className="text-2xl font-semibold mt-8 mb-4">Configuration</h2>
          <p>
            After installation, you'll need to configure CCDebugger with your API key:
          </p>

          <div className="bg-muted rounded-lg p-4 my-4">
            <pre className="text-sm"><code>{`// settings.json
{
  "ccdebugger.apiKey": "your-api-key-here",
  "ccdebugger.language": "en", // or "zh" for Chinese
  "ccdebugger.autoAnalyze": true,
  "ccdebugger.realTimeMonitoring": true
}`}</code></pre>
          </div>

          <h2 className="text-2xl font-semibold mt-8 mb-4">Basic Usage</h2>
          <p>
            Once configured, using CCDebugger is simple. When you encounter an error in Claude Code:
          </p>

          <ol className="list-decimal list-inside space-y-3">
            <li>
              <strong>Type the command:</strong> Start by typing <code className="bg-muted px-2 py-1 rounded">/ccdebug</code> 
              in the Claude Code terminal
            </li>
            <li>
              <strong>Choose an action:</strong> Select from analyze, fix, explain, or other available commands
            </li>
            <li>
              <strong>Review AI suggestions:</strong> CCDebugger will analyze your error and provide intelligent suggestions
            </li>
            <li>
              <strong>Apply the fix:</strong> Choose the suggestion that best fits your needs
            </li>
          </ol>

          <h2 className="text-2xl font-semibold mt-8 mb-4">Advanced Features</h2>
          
          <h3 className="text-xl font-semibold mt-6 mb-3">Custom Templates</h3>
          <p>
            Create reusable debugging templates for common error patterns in your projects. 
            This saves time and ensures consistency across your team.
          </p>

          <h3 className="text-xl font-semibold mt-6 mb-3">Real-Time Monitoring</h3>
          <p>
            Enable real-time error monitoring to catch and analyze errors as they happen, 
            before they impact your development flow.
          </p>

          <h3 className="text-xl font-semibold mt-6 mb-3">Multi-Language Support</h3>
          <p>
            CCDebugger supports both English and Chinese, with automatic language detection 
            based on your system settings or manual configuration.
          </p>

          <h2 className="text-2xl font-semibold mt-8 mb-4">Tips and Best Practices</h2>
          <ul className="list-disc list-inside space-y-2">
            <li>Keep your CCDebugger extension updated for the latest features and improvements</li>
            <li>Use custom templates for recurring error patterns in your codebase</li>
            <li>Enable real-time monitoring during development for immediate feedback</li>
            <li>Leverage the command history to learn from past debugging sessions</li>
          </ul>

          <h2 className="text-2xl font-semibold mt-8 mb-4">Conclusion</h2>
          <p>
            CCDebugger is designed to make debugging faster, smarter, and more efficient. 
            With AI-powered analysis and intelligent suggestions, you can spend less time 
            debugging and more time building amazing applications.
          </p>
          <p className="mt-4">
            Ready to transform your debugging experience? 
            <Link href="/" className="text-primary hover:underline ml-1">
              Get started with CCDebugger today!
            </Link>
          </p>
        </div>

        {/* Author Section */}
        <Separator className="my-12" />
        <div className="flex items-center gap-4">
          <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
            <BookOpen className="h-8 w-8 text-muted-foreground" />
          </div>
          <div>
            <p className="font-semibold">CCDebugger Team</p>
            <p className="text-sm text-muted-foreground">
              Building intelligent tools for better developer experiences
            </p>
          </div>
        </div>

        {/* Next/Previous Navigation */}
        <div className="flex justify-between items-center mt-12 pt-8 border-t">
          <div></div>
          <Button variant="ghost" asChild>
            <Link href="/blog">
              View All Posts
            </Link>
          </Button>
        </div>
      </article>
    </div>
  )
}
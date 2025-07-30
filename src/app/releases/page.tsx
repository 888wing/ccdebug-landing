import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { 
  Download, 
  CheckCircle2, 
  Bug, 
  Sparkles, 
  Wrench,
  GitCommit,
  Calendar,
  ExternalLink
} from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function ReleasesPage() {
  return (
    <div className="container px-4 md:px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <div className="space-y-6">
          <div>
            <h1 className="text-4xl font-bold tracking-tighter">Releases</h1>
            <p className="text-muted-foreground mt-2">
              Stay up to date with the latest CCDebugger improvements and features
            </p>
          </div>

          <Separator />

          {/* Version 1.5.0 */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-2xl">Version 1.5.0</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    <Calendar className="h-4 w-4" />
                    Released on January 29, 2025
                  </CardDescription>
                </div>
                <Badge variant="default" className="ml-4">
                  <Sparkles className="mr-1 h-3 w-3" />
                  Latest
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex gap-2">
                <Button asChild>
                  <Link href="https://marketplace.visualstudio.com/items?itemName=ccdebugger.vscode-extension">
                    <Download className="mr-2 h-4 w-4" />
                    Download v1.5.0
                  </Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link href="https://github.com/yourusername/ccdebugger/releases/tag/v1.5.0">
                    <ExternalLink className="mr-2 h-4 w-4" />
                    View on GitHub
                  </Link>
                </Button>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <Sparkles className="h-5 w-5 text-primary" />
                    New Features
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Shell/Bash Support:</strong> Comprehensive error analysis for shell scripts and command-line operations
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Docker/Dockerfile Support:</strong> Intelligent debugging for Docker containers and Dockerfile syntax errors
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>YAML/JSON Configuration Analysis:</strong> Smart detection and fixes for configuration file errors
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Extended Language Support:</strong> Added Kotlin, Swift, and SQL error analysis capabilities
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Enhanced Pattern Recognition:</strong> Improved error pattern matching with 50+ new patterns per language
                      </span>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <Wrench className="h-5 w-5 text-primary" />
                    Improvements
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Enhanced error context extraction with file path and line number tracking
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Improved confidence scoring algorithm for more accurate suggestions
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Better handling of multi-line error messages and stack traces
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Optimized pattern matching performance by 60%
                      </span>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <Bug className="h-5 w-5 text-primary" />
                    Bug Fixes
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Fixed pattern conflicts in complex error message parsing
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Resolved issue with special characters in error messages
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Fixed language detection for mixed-language projects
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Version 1.1.0 */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-2xl">Version 1.1.0</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    <Calendar className="h-4 w-4" />
                    Released on December 15, 2024
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex gap-2">
                <Button asChild>
                  <Link href="https://marketplace.visualstudio.com/items?itemName=ccdebugger.vscode-extension">
                    <Download className="mr-2 h-4 w-4" />
                    Download v1.1.0
                  </Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link href="https://github.com/yourusername/ccdebugger/releases/tag/v1.1.0">
                    <ExternalLink className="mr-2 h-4 w-4" />
                    View on GitHub
                  </Link>
                </Button>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <Sparkles className="h-5 w-5 text-primary" />
                    New Features
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Multi-language Support:</strong> Full support for Chinese and English with automatic language detection
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Custom Templates:</strong> Create and share debugging templates for common error patterns
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Real-time Error Monitoring:</strong> Monitor errors as they happen with instant AI insights
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Enhanced AI Analysis:</strong> Improved context understanding and solution accuracy
                      </span>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <Wrench className="h-5 w-5 text-primary" />
                    Improvements
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Performance optimization for large codebases
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Better error context extraction and analysis
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Reduced memory usage by 40%
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Faster command completion suggestions
                      </span>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <Bug className="h-5 w-5 text-primary" />
                    Bug Fixes
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Fixed issue with command completion in nested directories
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Resolved syntax highlighting conflicts with other extensions
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        Fixed memory leak in long-running debug sessions
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Version 1.0.0 */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-2xl">Version 1.0.0</CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    <Calendar className="h-4 w-4" />
                    Released on November 1, 2024
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex gap-2">
                <Button variant="outline" asChild>
                  <Link href="https://github.com/yourusername/ccdebugger/releases/tag/v1.0.0">
                    <ExternalLink className="mr-2 h-4 w-4" />
                    View on GitHub
                  </Link>
                </Button>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold flex items-center gap-2 mb-3">
                    <GitCommit className="h-5 w-5 text-primary" />
                    Initial Release
                  </h3>
                  <ul className="space-y-2 ml-7">
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>AI-Powered Error Analysis:</strong> Intelligent error understanding and solution suggestions
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Smart Command Completion:</strong> /ccdebug command with context-aware completions
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>VS Code Integration:</strong> Seamless integration with VS Code editor
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">
                        <strong>Error History:</strong> Track and learn from debugging patterns
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Older Versions */}
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Older Versions</h2>
            <div className="space-y-3">
              <Card>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-lg">Version 0.9.0 (Beta)</CardTitle>
                      <CardDescription className="text-sm">October 15, 2024</CardDescription>
                    </div>
                    <Button variant="ghost" size="sm" asChild>
                      <Link href="https://github.com/yourusername/ccdebugger/releases/tag/v0.9.0">
                        <ExternalLink className="h-4 w-4" />
                      </Link>
                    </Button>
                  </div>
                </CardHeader>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-lg">Version 0.8.0 (Beta)</CardTitle>
                      <CardDescription className="text-sm">September 20, 2024</CardDescription>
                    </div>
                    <Button variant="ghost" size="sm" asChild>
                      <Link href="https://github.com/yourusername/ccdebugger/releases/tag/v0.8.0">
                        <ExternalLink className="h-4 w-4" />
                      </Link>
                    </Button>
                  </div>
                </CardHeader>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
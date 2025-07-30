import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  Code2, 
  Terminal, 
  Zap, 
  Brain, 
  Languages, 
  FileCode2,
  Command,
  Sparkles,
  ChevronRight,
  Download,
  Book
} from "lucide-react"
import Link from "next/link"

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center space-y-8 text-center py-24 md:py-32 animate-in">
            <Badge variant="secondary" className="px-3 py-1">
              <Sparkles className="mr-2 h-3 w-3" />
              Version 1.5.0 Released
            </Badge>
            <div className="space-y-4 max-w-3xl">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
                Debug Claude Code with
                <span className="text-primary"> AI Intelligence</span>
              </h1>
              <p className="mx-auto max-w-2xl text-muted-foreground text-lg md:text-xl">
                CCDebugger transforms error debugging into an intelligent conversation. 
                Powered by AI to analyze, understand, and resolve Claude Code errors instantly.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" asChild>
                <Link href="#installation">
                  <Download className="mr-2 h-4 w-4" />
                  Get Started
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/blog">
                  <Book className="mr-2 h-4 w-4" />
                  Documentation
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t bg-muted/50">
        <div className="container px-4 md:px-6 py-24">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Powerful Features
            </h2>
            <p className="mt-4 text-muted-foreground text-lg">
              Everything you need to debug Claude Code efficiently
            </p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card className="relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1">
              <CardHeader>
                <Brain className="h-10 w-10 text-primary mb-2" />
                <CardTitle>AI-Powered Analysis</CardTitle>
                <CardDescription>
                  Advanced error analysis using AI to understand context and provide intelligent solutions
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1">
              <CardHeader>
                <Command className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Smart Command Completion</CardTitle>
                <CardDescription>
                  Type /ccdebug and let AI complete your debugging commands with context awareness
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1">
              <CardHeader>
                <Code2 className="h-10 w-10 text-primary mb-2" />
                <CardTitle>VS Code Extension</CardTitle>
                <CardDescription>
                  Seamless integration with VS Code for a native debugging experience
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1">
              <CardHeader>
                <Languages className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Extended Language Support</CardTitle>
                <CardDescription>
                  Now supports 10+ languages including JavaScript, Python, Shell/Bash, Docker, YAML/JSON, Kotlin, Swift, SQL and more
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1">
              <CardHeader>
                <Zap className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Real-Time Monitoring</CardTitle>
                <CardDescription>
                  Monitor errors as they happen with instant AI-powered insights and suggestions
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="relative overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1">
              <CardHeader>
                <FileCode2 className="h-10 w-10 text-primary mb-2" />
                <CardTitle>Custom Templates</CardTitle>
                <CardDescription>
                  Create and share debugging templates for common error patterns
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Usage Section */}
      <section className="border-t">
        <div className="container px-4 md:px-6 py-24">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              How to Use CCDebugger
            </h2>
            <p className="mt-4 text-muted-foreground text-lg">
              Get started in minutes with our simple setup
            </p>
          </div>

          <Tabs defaultValue="quick-start" className="max-w-4xl mx-auto">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="quick-start">Quick Start</TabsTrigger>
              <TabsTrigger value="commands">Commands</TabsTrigger>
              <TabsTrigger value="examples">Examples</TabsTrigger>
            </TabsList>
            
            <TabsContent value="quick-start" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Getting Started</CardTitle>
                  <CardDescription>
                    Follow these simple steps to start debugging with CCDebugger
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <h4 className="font-medium flex items-center gap-2">
                      <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">1</span>
                      Install CCDebugger Extension
                    </h4>
                    <div className="pl-8">
                      <pre className="bg-muted p-3 rounded-md text-sm">
                        <code>ext install ccdebugger.vscode-extension</code>
                      </pre>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium flex items-center gap-2">
                      <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">2</span>
                      Configure API Key
                    </h4>
                    <div className="pl-8">
                      <pre className="bg-muted p-3 rounded-md text-sm">
                        <code>{`// settings.json
{
  "ccdebugger.apiKey": "your-api-key",
  "ccdebugger.language": "en" // or "zh"
}`}</code>
                      </pre>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium flex items-center gap-2">
                      <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">3</span>
                      Start Debugging
                    </h4>
                    <div className="pl-8">
                      <p className="text-sm text-muted-foreground">
                        Type <code className="bg-muted px-1 py-0.5 rounded">/ccdebug</code> in Claude Code 
                        when you encounter an error
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="commands" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Available Commands</CardTitle>
                  <CardDescription>
                    All CCDebugger commands and their usage
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <code className="text-sm font-mono bg-muted px-2 py-1 rounded">/ccdebug analyze</code>
                      <p className="text-sm text-muted-foreground">
                        Analyze the current error context with AI
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <code className="text-sm font-mono bg-muted px-2 py-1 rounded">/ccdebug fix</code>
                      <p className="text-sm text-muted-foreground">
                        Get AI-suggested fixes for the current error
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <code className="text-sm font-mono bg-muted px-2 py-1 rounded">/ccdebug explain</code>
                      <p className="text-sm text-muted-foreground">
                        Get a detailed explanation of what went wrong
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <code className="text-sm font-mono bg-muted px-2 py-1 rounded">/ccdebug template [name]</code>
                      <p className="text-sm text-muted-foreground">
                        Load a debugging template for common issues
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <code className="text-sm font-mono bg-muted px-2 py-1 rounded">/ccdebug history</code>
                      <p className="text-sm text-muted-foreground">
                        View your debugging history and patterns
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="examples" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Real-World Examples</CardTitle>
                  <CardDescription>
                    See CCDebugger in action with common scenarios
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-3">
                    <h4 className="font-medium">TypeScript Type Error</h4>
                    <pre className="bg-muted p-3 rounded-md text-sm overflow-x-auto">
                      <code>{`// Error: Property 'name' does not exist on type 'User'
/ccdebug analyze

// AI Response:
The error occurs because the 'User' type doesn't have a 'name' property.
Looking at your type definition...

Suggested fix:
interface User {
  id: number;
  name: string; // Add this property
  email: string;
}`}</code>
                    </pre>
                  </div>
                  
                  <div className="space-y-3">
                    <h4 className="font-medium">Runtime Error</h4>
                    <pre className="bg-muted p-3 rounded-md text-sm overflow-x-auto">
                      <code>{`// Error: Cannot read property 'map' of undefined
/ccdebug fix

// AI Response:
The error suggests that you're trying to call .map() on an undefined value.
This typically happens when:
1. Data hasn't loaded yet
2. API returned null/undefined

Suggested fix:
{data?.map((item) => (
  // Your mapping logic
)) || <Loading />}`}</code>
                    </pre>
                  </div>
                  
                  <div className="space-y-3">
                    <h4 className="font-medium">Docker Build Error (New in v1.5)</h4>
                    <pre className="bg-muted p-3 rounded-md text-sm overflow-x-auto">
                      <code>{`// Error: Service 'web' failed to build: COPY failed
/ccdebug analyze

// AI Response:
The Docker build is failing because the COPY instruction 
can't find the source files. This usually means:
1. The file path is incorrect
2. The build context doesn't include the files

Suggested fix:
# Make sure the path is relative to build context
COPY ./app /app  # Instead of COPY app /app`}</code>
                    </pre>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Installation Section */}
      <section id="installation" className="border-t bg-muted/50">
        <div className="container px-4 md:px-6 py-24">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold tracking-tighter text-center mb-8">
              Installation Guide
            </h2>
            
            <Card>
              <CardHeader>
                <CardTitle>Choose Your Installation Method</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-3">
                  <h3 className="font-medium flex items-center gap-2">
                    <Terminal className="h-5 w-5" />
                    VS Code Marketplace
                  </h3>
                  <ol className="list-decimal list-inside space-y-2 text-sm text-muted-foreground pl-7">
                    <li>Open VS Code</li>
                    <li>Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)</li>
                    <li>Search for "CCDebugger"</li>
                    <li>Click Install</li>
                  </ol>
                </div>
                
                <div className="space-y-3">
                  <h3 className="font-medium flex items-center gap-2">
                    <Code2 className="h-5 w-5" />
                    Command Line
                  </h3>
                  <pre className="bg-muted p-3 rounded-md text-sm">
                    <code>code --install-extension ccdebugger.vscode-extension</code>
                  </pre>
                </div>
                
                <div className="space-y-3">
                  <h3 className="font-medium flex items-center gap-2">
                    <FileCode2 className="h-5 w-5" />
                    Manual Installation
                  </h3>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    <p>1. Download the .vsix file from our <Link href="/releases" className="text-primary hover:underline">releases page</Link></p>
                    <p>2. Open VS Code Command Palette (Ctrl+Shift+P / Cmd+Shift+P)</p>
                    <p>3. Run "Extensions: Install from VSIX..."</p>
                    <p>4. Select the downloaded file</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t">
        <div className="container px-4 md:px-6 py-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground">
              © 2025 CCDebugger. All rights reserved.
            </p>
            <div className="flex gap-6">
              <Link href="/privacy" className="text-sm text-muted-foreground hover:text-foreground">
                Privacy
              </Link>
              <Link href="/terms" className="text-sm text-muted-foreground hover:text-foreground">
                Terms
              </Link>
              <Link href="https://github.com/888wing/ccdebugger" className="text-sm text-muted-foreground hover:text-foreground">
                GitHub
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Calendar, Clock, User, Tag, Code, Terminal, FileCode, Database, Sparkles, CheckCircle2 } from "lucide-react"
import { Separator } from "@/components/ui/separator"

export default function CCDebugger15ReleasePage() {
  return (
    <article className="container px-4 md:px-6 py-12">
      <div className="max-w-4xl mx-auto">
        <Button variant="ghost" asChild className="mb-6">
          <Link href="/blog">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Blog
          </Link>
        </Button>

        <header className="space-y-4 mb-8">
          <div className="flex flex-wrap gap-2">
            <Badge variant="secondary">
              <Tag className="mr-1 h-3 w-3" />
              Release
            </Badge>
            <Badge variant="secondary">
              <Code className="mr-1 h-3 w-3" />
              Development
            </Badge>
            <Badge variant="secondary">
              <Sparkles className="mr-1 h-3 w-3" />
              New Features
            </Badge>
          </div>
          
          <h1 className="text-4xl font-bold tracking-tighter">
            CCDebugger 1.5: Expanding Language Support for Modern Development
          </h1>
          
          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <User className="h-4 w-4" />
              CCDebugger Team
            </span>
            <span className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              January 29, 2025
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              5 min read
            </span>
          </div>
        </header>

        <div className="prose prose-gray dark:prose-invert max-w-none">
          <p className="text-lg text-muted-foreground">
            We're excited to announce CCDebugger 1.5, a major update that significantly expands our language support 
            and brings intelligent error analysis to even more development scenarios. This release focuses on modern 
            DevOps workflows, configuration management, and mobile development languages.
          </p>

          <Separator className="my-8" />

          <h2 className="text-2xl font-bold mt-8 mb-4">🚀 What's New in Version 1.5</h2>

          <Card className="mb-6">
            <CardContent className="pt-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Terminal className="h-5 w-5 text-primary" />
                Shell/Bash Script Support
              </h3>
              <p className="mb-4">
                Command-line operations and shell scripts are at the heart of modern development workflows. 
                CCDebugger now provides comprehensive error analysis for:
              </p>
              <ul className="space-y-2 mb-4">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Syntax errors in bash scripts</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Command not found issues with smart suggestions</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Permission and path-related errors</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Array and variable expansion problems</span>
                </li>
              </ul>
              <div className="bg-secondary/50 p-4 rounded-lg">
                <code className="text-sm">
                  Error: ./deploy.sh: line 42: syntax error near unexpected token `fi'<br/>
                  CCDebugger: Missing 'then' after if statement. Add 'then' on line 41.
                </code>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardContent className="pt-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FileCode className="h-5 w-5 text-primary" />
                Docker & Container Support
              </h3>
              <p className="mb-4">
                Containerization is essential for modern deployment. CCDebugger now understands:
              </p>
              <ul className="space-y-2 mb-4">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Dockerfile syntax errors and best practices</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Docker runtime errors and container issues</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Docker Compose configuration problems</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Image build failures with actionable solutions</span>
                </li>
              </ul>
              <div className="bg-secondary/50 p-4 rounded-lg">
                <code className="text-sm">
                  Error: Service 'web' failed to build: COPY failed: no source files<br/>
                  CCDebugger: The source path './app' doesn't exist. Check your build context.
                </code>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardContent className="pt-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FileCode className="h-5 w-5 text-primary" />
                YAML/JSON Configuration Analysis
              </h3>
              <p className="mb-4">
                Configuration errors can be frustrating. CCDebugger now provides intelligent analysis for:
              </p>
              <ul className="space-y-2 mb-4">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>YAML syntax and indentation issues</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>JSON parsing errors with precise location</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Kubernetes manifest validation</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>CI/CD pipeline configuration (GitHub Actions, GitLab CI, CircleCI)</span>
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card className="mb-6">
            <CardContent className="pt-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Code className="h-5 w-5 text-primary" />
                Extended Language Support
              </h3>
              <p className="mb-4">
                We've also added comprehensive error analysis for three more programming languages:
              </p>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="space-y-2">
                  <h4 className="font-semibold">Kotlin</h4>
                  <ul className="text-sm space-y-1">
                    <li>• Null safety violations</li>
                    <li>• Type inference issues</li>
                    <li>• Coroutine errors</li>
                    <li>• Android-specific patterns</li>
                  </ul>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold">Swift</h4>
                  <ul className="text-sm space-y-1">
                    <li>• Optional handling</li>
                    <li>• Protocol conformance</li>
                    <li>• Memory management</li>
                    <li>• SwiftUI errors</li>
                  </ul>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold">SQL</h4>
                  <ul className="text-sm space-y-1">
                    <li>• Syntax errors</li>
                    <li>• Join problems</li>
                    <li>• Performance hints</li>
                    <li>• Schema violations</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          <h2 className="text-2xl font-bold mt-8 mb-4">🎯 Key Improvements</h2>

          <div className="space-y-4">
            <Card>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">Enhanced Pattern Recognition</h3>
                <p className="text-sm text-muted-foreground">
                  We've added over 50 new error patterns per language, trained on real-world debugging scenarios. 
                  The pattern matching engine is now 60% faster while being more accurate.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">Better Context Extraction</h3>
                <p className="text-sm text-muted-foreground">
                  CCDebugger now captures more context around errors, including file paths, line numbers, 
                  and surrounding code, making suggestions more relevant and actionable.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <h3 className="font-semibold mb-2">Improved Confidence Scoring</h3>
                <p className="text-sm text-muted-foreground">
                  Our new confidence scoring algorithm provides more accurate reliability indicators for 
                  each suggestion, helping you prioritize which fixes to try first.
                </p>
              </CardContent>
            </Card>
          </div>

          <h2 className="text-2xl font-bold mt-8 mb-4">🔧 Under the Hood</h2>

          <p>
            This release represents months of work analyzing error patterns across thousands of real debugging 
            sessions. We've completely rewritten our pattern matching engine to be more modular and efficient, 
            allowing us to add new languages faster while maintaining high accuracy.
          </p>

          <p>
            The new architecture also improves:
          </p>
          <ul>
            <li>Multi-line error message parsing</li>
            <li>Stack trace analysis across languages</li>
            <li>Cross-language project support</li>
            <li>Error severity classification</li>
          </ul>

          <h2 className="text-2xl font-bold mt-8 mb-4">🚀 Getting Started</h2>

          <p>
            Update to CCDebugger 1.5 today to start benefiting from these new features:
          </p>

          <div className="bg-secondary/50 p-4 rounded-lg my-4">
            <code className="text-sm">
              # Update CCDebugger CLI<br/>
              npm update -g ccdebugger<br/><br/>
              # Or install fresh<br/>
              npm install -g ccdebugger@1.5.0
            </code>
          </div>

          <p>
            The new language analyzers activate automatically when CCDebugger detects errors in supported formats. 
            No configuration needed!
          </p>

          <h2 className="text-2xl font-bold mt-8 mb-4">🎉 Thank You</h2>

          <p>
            We're grateful to our community for the feedback and bug reports that shaped this release. 
            Special thanks to everyone who contributed error patterns and test cases for the new languages.
          </p>

          <p>
            As always, we'd love to hear your thoughts on this release. Try out the new features and 
            let us know what you think!
          </p>

          <div className="mt-8 p-6 bg-primary/5 rounded-lg border">
            <h3 className="font-semibold mb-2">What's Next?</h3>
            <p className="text-sm text-muted-foreground mb-4">
              We're already working on CCDebugger 2.0, which will bring AI-powered code fix suggestions, 
              team collaboration features, and integration with popular IDEs beyond VS Code.
            </p>
            <Button asChild>
              <Link href="/releases">
                View Full Release Notes
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </article>
  )
}
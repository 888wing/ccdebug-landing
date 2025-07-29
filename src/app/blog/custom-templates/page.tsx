import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import Link from "next/link"
import { ArrowLeft, Clock, Calendar, Tag, Code2 } from "lucide-react"

export default function CustomTemplates() {
  return (
    <article className="container mx-auto px-4 py-16 max-w-4xl">
      {/* Back to blog */}
      <Link 
        href="/blog" 
        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-8"
      >
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back to blog
      </Link>

      {/* Article header */}
      <header className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <Badge variant="secondary">Guide</Badge>
          <Badge variant="outline">Templates</Badge>
          <Badge variant="outline">Community</Badge>
        </div>
        
        <h1 className="text-4xl font-bold mb-4">
          Custom Templates: Share Your Debugging Patterns
        </h1>
        
        <p className="text-xl text-muted-foreground mb-6">
          How to create, use, and share custom debugging templates with the community
        </p>
        
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" />
            November 28, 2024
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            6 min read
          </span>
        </div>
      </header>

      <Separator className="mb-8" />

      {/* Article content */}
      <div className="prose prose-neutral dark:prose-invert max-w-none">
        <section className="mb-8">
          <h2>Why Custom Templates Matter</h2>
          <p>
            Every development team has unique debugging patterns, coding standards, and 
            domain-specific knowledge. While CCDebugger comes with powerful built-in 
            templates, the ability to create custom templates lets you tailor the AI's 
            responses to your specific needs.
          </p>
          <p>
            Custom templates enable you to:
          </p>
          <ul>
            <li>Encode team-specific debugging knowledge</li>
            <li>Standardize error analysis across your organization</li>
            <li>Share debugging patterns with the community</li>
            <li>Create domain-specific analysis tools</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2>Understanding Template Structure</h2>
          <p>
            CCDebugger templates use a simple but powerful YAML format that defines how 
            the AI should analyze specific types of errors. Here's the basic structure:
          </p>
          
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`# template.yaml
name: "React Hook Exhaustive Dependencies"
description: "Comprehensive analysis for React Hook dependency issues"
version: "1.0.0"
author: "Your Name"
tags: ["react", "hooks", "dependencies"]

# Pattern matching
patterns:
  - error_type: "React Hook useEffect has missing dependencies"
  - file_extension: [".jsx", ".tsx"]
  - framework: "react"

# Analysis configuration
analysis:
  focus_areas:
    - "Identify all missing dependencies"
    - "Check for stale closure issues"
    - "Suggest useCallback/useMemo where appropriate"
    - "Detect infinite loop risks"
  
  context_needed:
    - "Component full code"
    - "State and prop definitions"
    - "Parent component usage"

# Response template
response_format: |
  ## Dependency Analysis
  
  **Missing Dependencies:** {missing_deps}
  
  **Risk Assessment:** {risk_level}
  
  **Suggested Fix:**
  \`\`\`javascript
  {suggested_code}
  \`\`\`
  
  **Explanation:** {detailed_explanation}
  
  **Best Practices:**
  {best_practices_list}

# Example snippets
examples:
  - problem: |
      useEffect(() => {
        fetchUser(userId);
      }, []);
    
    solution: |
      useEffect(() => {
        fetchUser(userId);
      }, [userId]);
    
    explanation: "Add userId to dependencies to refetch when it changes"`}</code>
          </pre>
        </section>

        <section className="mb-8">
          <h2>Creating Your First Template</h2>
          
          <h3>Step 1: Identify Common Patterns</h3>
          <p>
            Start by identifying debugging patterns that appear frequently in your codebase. 
            Look for:
          </p>
          <ul>
            <li>Recurring error types</li>
            <li>Framework-specific issues</li>
            <li>Team coding conventions</li>
            <li>Domain-specific edge cases</li>
          </ul>

          <h3>Step 2: Define the Template</h3>
          <p>
            Create a new YAML file in your templates directory:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`# ~/.ccdebugger/templates/async-await-errors.yaml
name: "Async/Await Error Handler"
description: "Comprehensive async error handling patterns"

patterns:
  - error_type: ["UnhandledPromiseRejection", "TypeError"]
  - keywords: ["async", "await", "Promise"]

analysis:
  focus_areas:
    - "Check for try-catch blocks"
    - "Identify missing await keywords"
    - "Detect Promise chain issues"
    - "Suggest error boundaries"

# Custom prompts for AI
prompts:
  initial: "Analyze this async/await error with focus on Promise handling"
  follow_up: "Suggest robust error handling patterns"
  
# Code generation templates
generators:
  try_catch: |
    try {
      {original_code}
    } catch (error) {
      console.error('Error in {function_name}:', error);
      // Handle error appropriately
      {error_handling}
    }`}</code>
          </pre>

          <h3>Step 3: Test Your Template</h3>
          <p>
            Test your template with real errors from your codebase:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`# Test with a specific template
ccdebug analyze --template async-await-errors

# Validate template syntax
ccdebug template validate async-await-errors.yaml

# Run test cases
ccdebug template test async-await-errors.yaml --input error.log`}</code>
          </pre>
        </section>

        <section className="mb-8">
          <h2>Advanced Template Features</h2>
          
          <h3>Conditional Logic</h3>
          <p>
            Templates can include conditional logic to handle different scenarios:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`conditions:
  - if: "error.type == 'TypeError' && framework == 'react'"
    then:
      focus: "React-specific type checking"
      suggest: "PropTypes or TypeScript"
  
  - if: "file.extension == '.ts' || file.extension == '.tsx'"
    then:
      include_typescript_specific: true
      check_types: true`}</code>
          </pre>

          <h3>Multi-Language Support</h3>
          <p>
            Create templates that work across different programming languages:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`languages:
  javascript:
    error_patterns: ["undefined is not a function", "Cannot read property"]
    fix_patterns: 
      null_check: "if (obj && obj.property)"
      optional_chaining: "obj?.property"
  
  python:
    error_patterns: ["AttributeError", "TypeError"]
    fix_patterns:
      hasattr_check: "if hasattr(obj, 'property')"
      try_except: "try: obj.property except AttributeError: pass"`}</code>
          </pre>

          <h3>Integration with External Tools</h3>
          <p>
            Templates can integrate with linters, type checkers, and other tools:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`integrations:
  eslint:
    run_before_analysis: true
    include_warnings: true
    rules_focus: ["no-unused-vars", "react-hooks/exhaustive-deps"]
  
  typescript:
    check_types: true
    strict_mode: true
    
  custom_scripts:
    pre_analysis: "./scripts/prepare-context.sh"
    post_analysis: "./scripts/validate-fix.sh"`}</code>
          </pre>
        </section>

        <section className="mb-8">
          <h2>Sharing Templates with the Community</h2>
          
          <h3>Publishing to the Template Registry</h3>
          <p>
            Share your templates with other developers through the CCDebugger registry:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`# Login to the registry
ccdebug auth login

# Publish your template
ccdebug template publish async-await-errors.yaml

# Add metadata for better discoverability
ccdebug template update async-await-errors \
  --tags "async,error-handling,promises" \
  --category "JavaScript" \
  --license "MIT"`}</code>
          </pre>

          <h3>Using Community Templates</h3>
          <p>
            Discover and use templates created by other developers:
          </p>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`# Search for templates
ccdebug template search "react hooks"

# Install a template
ccdebug template install @username/react-hooks-analyzer

# List installed templates
ccdebug template list

# Update templates
ccdebug template update --all`}</code>
          </pre>
        </section>

        <section className="mb-8">
          <h2>Real-World Template Examples</h2>
          
          <h3>Database Query Optimization</h3>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`name: "SQL Query Optimizer"
patterns:
  - error_type: ["QueryTimeout", "SlowQueryWarning"]
  - keywords: ["SELECT", "JOIN", "WHERE"]

analysis:
  check_for:
    - "Missing indexes"
    - "N+1 queries"
    - "Unnecessary joins"
    - "Large result sets"
  
  optimizations:
    - "Suggest index creation"
    - "Recommend query restructuring"
    - "Propose caching strategies"`}</code>
          </pre>

          <h3>API Error Handling</h3>
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{`name: "RESTful API Error Analyzer"
patterns:
  - status_codes: [400, 401, 403, 404, 500]
  - keywords: ["fetch", "axios", "request"]

response_strategies:
  400:
    message: "Bad Request - Validate input data"
    check: ["Request payload", "Data types", "Required fields"]
  
  401:
    message: "Unauthorized - Check authentication"
    check: ["Auth token", "Token expiry", "Permissions"]`}</code>
          </pre>
        </section>

        <section className="mb-8">
          <h2>Best Practices for Template Creation</h2>
          
          <ol>
            <li>
              <strong>Keep Templates Focused:</strong> Each template should handle one 
              specific type of error or pattern well, rather than trying to cover everything.
            </li>
            <li>
              <strong>Provide Clear Examples:</strong> Include real-world examples that 
              demonstrate when and how to use the template.
            </li>
            <li>
              <strong>Version Your Templates:</strong> Use semantic versioning to track 
              changes and ensure compatibility.
            </li>
            <li>
              <strong>Document Thoroughly:</strong> Include clear descriptions, usage 
              instructions, and prerequisites.
            </li>
            <li>
              <strong>Test Extensively:</strong> Validate templates against various error 
              scenarios before sharing.
            </li>
            <li>
              <strong>Gather Feedback:</strong> Encourage users to report issues and 
              suggest improvements.
            </li>
          </ol>
        </section>

        <section className="mb-8">
          <h2>Template Development Workflow</h2>
          <p>
            Here's a recommended workflow for developing custom templates:
          </p>
          <div className="bg-muted p-4 rounded-lg">
            <ol className="space-y-2">
              <li>🔍 <strong>Identify:</strong> Find recurring debugging patterns</li>
              <li>📝 <strong>Document:</strong> Write down the analysis approach</li>
              <li>🛠️ <strong>Create:</strong> Build the template structure</li>
              <li>🧪 <strong>Test:</strong> Validate with real errors</li>
              <li>🔄 <strong>Iterate:</strong> Refine based on results</li>
              <li>📦 <strong>Package:</strong> Add metadata and examples</li>
              <li>🚀 <strong>Share:</strong> Publish to the community</li>
              <li>🔧 <strong>Maintain:</strong> Update based on feedback</li>
            </ol>
          </div>
        </section>

        <section className="mb-8">
          <h2>Conclusion</h2>
          <p>
            Custom templates are a powerful way to extend CCDebugger's capabilities and 
            share debugging knowledge with the community. By creating templates that encode 
            your team's expertise and domain knowledge, you can make debugging more 
            efficient and consistent across your organization.
          </p>
          <p>
            Start creating your own templates today and contribute to the growing library 
            of debugging patterns. Together, we can build a comprehensive resource that 
            helps developers debug more effectively across all languages and frameworks.
          </p>
          <p>
            Ready to create your first template? Check out our 
            <Link href="/docs/templates" className="text-primary hover:underline"> template documentation</Link> and 
            join the <Link href="/community" className="text-primary hover:underline"> CCDebugger community</Link> to 
            share your creations.
          </p>
        </section>
      </div>

      {/* Article footer */}
      <Separator className="my-8" />
      
      <div className="flex items-center justify-between">
        <Link 
          href="/blog" 
          className="text-sm text-muted-foreground hover:text-foreground"
        >
          ← Back to all posts
        </Link>
        <div className="flex gap-2">
          <Badge variant="outline">
            <Tag className="mr-1 h-3 w-3" />
            Templates
          </Badge>
          <Badge variant="outline">
            <Tag className="mr-1 h-3 w-3" />
            Community
          </Badge>
          <Badge variant="outline">
            <Tag className="mr-1 h-3 w-3" />
            Guide
          </Badge>
        </div>
      </div>
    </article>
  )
}
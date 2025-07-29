import { Check, Clock, Calendar } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import "../blog/blog.css"

export default function Roadmap() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl">
      <h1 className="text-4xl md:text-5xl font-bold mb-8">Product Roadmap</h1>
      
      <p className="text-xl text-muted-foreground mb-12">
        Our vision for making debugging with Claude Code more intelligent, efficient, and enjoyable.
      </p>

      <div className="roadmap-section">
        <h2 className="text-3xl font-bold mb-8">2025 Development Roadmap</h2>
        
        <div className="roadmap-timeline">
          {/* Q1 2025 */}
          <div className="roadmap-item completed">
            <div className="roadmap-quarter">Q1 2025 - Foundation</div>
            <div className="roadmap-title">Core Features & Launch</div>
            <div className="roadmap-description">
              Establishing the foundation with essential debugging capabilities
            </div>
            <ul className="roadmap-features">
              <li>
                <Check className="h-4 w-4 text-green-500" />
                AI-powered error analysis with Claude integration
              </li>
              <li>
                <Check className="h-4 w-4 text-green-500" />
                Smart command completion system
              </li>
              <li>
                <Check className="h-4 w-4 text-green-500" />
                VS Code extension release
              </li>
              <li>
                <Check className="h-4 w-4 text-green-500" />
                Multi-language support (English & Chinese)
              </li>
              <li>
                <Check className="h-4 w-4 text-green-500" />
                Basic template system
              </li>
            </ul>
          </div>

          {/* Q2 2025 */}
          <div className="roadmap-item in-progress">
            <div className="roadmap-quarter">Q2 2025 - Enhancement</div>
            <div className="roadmap-title">Advanced Analysis & Collaboration</div>
            <div className="roadmap-description">
              Expanding capabilities with deeper analysis and team features
            </div>
            <ul className="roadmap-features">
              <li>
                <Clock className="h-4 w-4 text-yellow-500" />
                Deep analysis mode with architectural insights
              </li>
              <li>
                <Clock className="h-4 w-4 text-yellow-500" />
                Custom template marketplace
              </li>
              <li>
                <Calendar className="h-4 w-4 text-gray-400" />
                Team collaboration features
              </li>
              <li>
                <Calendar className="h-4 w-4 text-gray-400" />
                Performance profiling integration
              </li>
              <li>
                <Calendar className="h-4 w-4 text-gray-400" />
                Git blame integration for error context
              </li>
            </ul>
          </div>

          {/* Q3 2025 */}
          <div className="roadmap-item planned">
            <div className="roadmap-quarter">Q3 2025 - Intelligence</div>
            <div className="roadmap-title">Predictive Debugging & Automation</div>
            <div className="roadmap-description">
              Introducing predictive capabilities and workflow automation
            </div>
            <ul className="roadmap-features">
              <li>Predictive error detection before runtime</li>
              <li>CI/CD integration for automated debugging</li>
              <li>Custom AI model training on your codebase</li>
              <li>Automated fix suggestions with one-click apply</li>
              <li>Debug session recording and replay</li>
            </ul>
          </div>

          {/* Q4 2025 */}
          <div className="roadmap-item planned">
            <div className="roadmap-quarter">Q4 2025 - Platform</div>
            <div className="roadmap-title">Enterprise & Ecosystem</div>
            <div className="roadmap-description">
              Building a comprehensive debugging platform
            </div>
            <ul className="roadmap-features">
              <li>Enterprise SSO and compliance features</li>
              <li>Plugin ecosystem for custom analyzers</li>
              <li>Real-time collaborative debugging</li>
              <li>Advanced analytics and reporting</li>
              <li>API for third-party integrations</li>
            </ul>
          </div>
        </div>
      </div>

      <Separator className="my-12" />

      {/* Feature Categories */}
      <div className="my-12">
        <h2 className="text-3xl font-bold mb-8">Feature Categories</h2>
        
        <div className="grid gap-6 md:grid-cols-2">
          <div className="p-6 rounded-lg border">
            <h3 className="text-xl font-semibold mb-3">🤖 AI & Analysis</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Continuously improving our AI capabilities for better debugging insights
            </p>
            <ul className="space-y-2 text-sm">
              <li>• Enhanced context understanding</li>
              <li>• Multi-file analysis</li>
              <li>• Framework-specific optimizations</li>
              <li>• Custom model training</li>
            </ul>
          </div>

          <div className="p-6 rounded-lg border">
            <h3 className="text-xl font-semibold mb-3">🛠️ Developer Experience</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Making debugging faster and more intuitive
            </p>
            <ul className="space-y-2 text-sm">
              <li>• Improved command palette</li>
              <li>• Keyboard shortcuts</li>
              <li>• Custom themes</li>
              <li>• Workflow automation</li>
            </ul>
          </div>

          <div className="p-6 rounded-lg border">
            <h3 className="text-xl font-semibold mb-3">👥 Collaboration</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Enabling teams to debug together effectively
            </p>
            <ul className="space-y-2 text-sm">
              <li>• Shared debugging sessions</li>
              <li>• Template sharing</li>
              <li>• Knowledge base integration</li>
              <li>• Team analytics</li>
            </ul>
          </div>

          <div className="p-6 rounded-lg border">
            <h3 className="text-xl font-semibold mb-3">🔌 Integrations</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Connecting with your existing development tools
            </p>
            <ul className="space-y-2 text-sm">
              <li>• GitHub/GitLab integration</li>
              <li>• JIRA/Linear tickets</li>
              <li>• Slack/Discord notifications</li>
              <li>• IDE extensions</li>
            </ul>
          </div>
        </div>
      </div>

      <Separator className="my-12" />

      {/* Long-term Vision */}
      <div className="my-12">
        <h2 className="text-3xl font-bold mb-8">Long-term Vision</h2>
        
        <div className="bg-gradient-to-br from-primary/10 to-primary/5 p-8 rounded-xl border border-primary/20">
          <h3 className="text-2xl font-semibold mb-4">The Future of Debugging</h3>
          <p className="text-lg mb-6">
            We envision a world where debugging is no longer a frustrating time sink, but an 
            intelligent, collaborative, and even enjoyable part of the development process.
          </p>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">🎯 Proactive Error Prevention</h4>
              <p className="text-sm text-muted-foreground">
                AI that learns from your codebase to prevent errors before they happen, 
                suggesting improvements as you type.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">🧠 Context-Aware Intelligence</h4>
              <p className="text-sm text-muted-foreground">
                Understanding not just your code, but your entire development context - 
                from requirements to deployment.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">🌐 Global Knowledge Network</h4>
              <p className="text-sm text-muted-foreground">
                A community-driven platform where debugging patterns and solutions are 
                shared and improved collectively.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Get Involved */}
      <div className="my-12 text-center">
        <h2 className="text-3xl font-bold mb-4">Help Shape Our Roadmap</h2>
        <p className="text-lg text-muted-foreground mb-8">
          Your feedback drives our development. Let us know what features you'd like to see!
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Badge variant="secondary" className="px-4 py-2">
            <a href="https://github.com/888wing/ccdebugger/issues/new?template=feature_request.yml" className="flex items-center gap-2" target="_blank" rel="noopener noreferrer">
              💡 Suggest a Feature
            </a>
          </Badge>
          <Badge variant="secondary" className="px-4 py-2">
            <a href="https://github.com/888wing/ccdebugger/discussions/new?category=ideas" className="flex items-center gap-2" target="_blank" rel="noopener noreferrer">
              💬 Join Discussion
            </a>
          </Badge>
          <Badge variant="secondary" className="px-4 py-2">
            <a href="/blog?category=updates" className="flex items-center gap-2">
              📰 Development Updates
            </a>
          </Badge>
        </div>
      </div>

      {/* Update Frequency */}
      <div className="text-center text-sm text-muted-foreground">
        <p>This roadmap is updated monthly. Last update: January 2025</p>
        <p className="mt-2">
          Follow our <a href="/blog" className="text-primary hover:underline">blog</a> for detailed updates on each milestone.
        </p>
      </div>
    </div>
  )
}
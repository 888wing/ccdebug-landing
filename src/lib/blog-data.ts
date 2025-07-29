import { 
  BookOpen, 
  Code2,
  Lightbulb,
  Zap,
  Users,
  type LucideIcon
} from "lucide-react"

export interface BlogPost {
  id: number
  slug: string
  title: string
  description: string
  category: string
  readTime: string
  date: string
  icon: LucideIcon
  color: string
  featured?: boolean
  tags?: string[]
  author?: string
}

export const blogPosts: BlogPost[] = [
  {
    id: 1,
    slug: "getting-started",
    title: "Getting Started with CCDebugger: A Complete Guide",
    description: "Learn how to set up and use CCDebugger to supercharge your Claude Code debugging workflow",
    category: "Tutorial",
    readTime: "5 min read",
    date: "December 10, 2024",
    icon: BookOpen,
    color: "text-blue-500",
    featured: true,
    tags: ["getting-started", "tutorial", "basics"],
    author: "CCDebugger Team"
  },
  {
    id: 2,
    slug: "understanding-ai-error-analysis",
    title: "Understanding AI-Powered Error Analysis",
    description: "Deep dive into how CCDebugger uses AI to analyze and understand your code errors",
    category: "Technical",
    readTime: "8 min read",
    date: "December 5, 2024",
    icon: Lightbulb,
    color: "text-purple-500",
    tags: ["ai", "debugging", "technical"],
    author: "CCDebugger Team"
  },
  {
    id: 3,
    slug: "custom-templates",
    title: "Custom Templates: Share Your Debugging Patterns",
    description: "How to create, use, and share custom debugging templates with the community",
    category: "Guide",
    readTime: "6 min read",
    date: "November 28, 2024",
    icon: Code2,
    color: "text-green-500",
    tags: ["templates", "community", "guide"],
    author: "CCDebugger Team"
  },
  {
    id: 4,
    slug: "performance-tips",
    title: "Performance Tips for Large Codebases",
    description: "Optimize CCDebugger performance when working with enterprise-scale projects",
    category: "Performance",
    readTime: "7 min read",
    date: "November 20, 2024",
    icon: Zap,
    color: "text-yellow-500",
    tags: ["performance", "enterprise", "optimization"],
    author: "CCDebugger Team"
  },
  {
    id: 5,
    slug: "building-ccdebugger",
    title: "Building CCDebugger: Our Journey",
    description: "The story behind CCDebugger and how we built an AI-powered debugging tool",
    category: "Story",
    readTime: "10 min read",
    date: "November 15, 2024",
    icon: Users,
    color: "text-pink-500",
    tags: ["story", "journey", "open-source"],
    author: "CCDebugger Team"
  }
]

export const categories = [
  { name: "All", count: blogPosts.length },
  { name: "Tutorial", count: blogPosts.filter(p => p.category === "Tutorial").length },
  { name: "Technical", count: blogPosts.filter(p => p.category === "Technical").length },
  { name: "Guide", count: blogPosts.filter(p => p.category === "Guide").length },
  { name: "Performance", count: blogPosts.filter(p => p.category === "Performance").length },
  { name: "Story", count: blogPosts.filter(p => p.category === "Story").length }
]

// Helper functions
export function getFeaturedPosts(): BlogPost[] {
  return blogPosts.filter(post => post.featured)
}

export function getPostsByCategory(category: string): BlogPost[] {
  if (category === "All") return blogPosts
  return blogPosts.filter(post => post.category === category)
}

export function getPostBySlug(slug: string): BlogPost | undefined {
  return blogPosts.find(post => post.slug === slug)
}

export function getRelatedPosts(currentSlug: string, limit: number = 3): BlogPost[] {
  const currentPost = getPostBySlug(currentSlug)
  if (!currentPost) return []
  
  // Find posts with similar tags or same category
  return blogPosts
    .filter(post => post.slug !== currentSlug)
    .sort((a, b) => {
      // Prioritize same category
      if (a.category === currentPost.category && b.category !== currentPost.category) return -1
      if (b.category === currentPost.category && a.category !== currentPost.category) return 1
      
      // Then by date (newer first)
      return new Date(b.date).getTime() - new Date(a.date).getTime()
    })
    .slice(0, limit)
}
"use client"

import React, { Suspense } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { 
  BookOpen, 
  Calendar, 
  Clock, 
  ChevronRight,
  Code2,
  Lightbulb,
  Zap,
  Users,
  ArrowRight
} from "lucide-react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"

const blogPosts = [
  {
    id: 0,
    slug: "january-2025-update",
    title: "January 2025 Development Update",
    description: "CCDebugger launches with AI-powered debugging, roadmap reveal, and exciting features ahead",
    category: "Update",
    readTime: "4 min read",
    date: "January 29, 2025",
    icon: Zap,
    color: "text-yellow-500",
    featured: true
  },
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
    featured: false
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
    color: "text-purple-500"
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
    color: "text-green-500"
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
    color: "text-yellow-500"
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
    color: "text-pink-500"
  }
]

const categories = [
  { name: "All", count: blogPosts.length },
  { name: "Update", count: 1 },
  { name: "Tutorial", count: 1 },
  { name: "Technical", count: 1 },
  { name: "Guide", count: 1 },
  { name: "Performance", count: 1 },
  { name: "Story", count: 1 }
]

function BlogContent() {
  const searchParams = useSearchParams()
  const selectedCategory = searchParams.get("category") || "All"
  
  const filteredPosts = selectedCategory === "All" 
    ? blogPosts 
    : blogPosts.filter(post => post.category.toLowerCase() === selectedCategory.toLowerCase())
  
  const featuredPost = filteredPosts.find(post => post.featured) || filteredPosts[0]
  const regularPosts = filteredPosts.filter(post => post.id !== featuredPost?.id)
  
  return (
    <div className="container px-4 md:px-6 py-12">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tighter mb-4">CCDebugger Blog</h1>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Technical insights, tutorials, and updates from the CCDebugger team
          </p>
        </div>

        {/* Featured Post */}
        {featuredPost && (
          <div className="mb-12">
            <h2 className="text-2xl font-semibold mb-6">Featured Post</h2>
            <Card className="overflow-hidden hover:shadow-lg transition-shadow">
              <CardHeader className="pb-4">
                <div className="flex items-start justify-between">
                  <Badge variant="secondary" className="mb-3">
                    {React.createElement(featuredPost.icon, { className: "mr-1 h-3 w-3" })}
                    {featuredPost.category}
                  </Badge>
                  <Badge variant="outline">Featured</Badge>
                </div>
                <CardTitle className="text-2xl hover:text-primary transition-colors">
                  <Link href={`/blog/${featuredPost.slug}`}>
                    {featuredPost.title}
                  </Link>
                </CardTitle>
                <CardDescription className="text-base mt-2">
                  {featuredPost.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {featuredPost.date}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {featuredPost.readTime}
                  </span>
                </div>
                <Button variant="link" className="mt-4 p-0" asChild>
                  <Link href={`/blog/${featuredPost.slug}`}>
                    Read more
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Categories */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <Link 
                key={category.name} 
                href={category.name === "All" ? "/blog" : `/blog?category=${category.name.toLowerCase()}`}
              >
                <Button
                  variant={
                    (category.name === "All" && selectedCategory === "All") ||
                    (category.name.toLowerCase() === selectedCategory.toLowerCase())
                      ? "default"
                      : "outline"
                  }
                  size="sm"
                >
                  {category.name}
                  <Badge variant="secondary" className="ml-2 h-5 px-1">
                    {category.count}
                  </Badge>
                </Button>
              </Link>
            ))}
          </div>
        </div>

        {/* Filtered Message */}
        {selectedCategory !== "All" && (
          <div className="mb-6 p-4 bg-muted rounded-lg">
            <p className="text-sm">
              Showing {filteredPosts.length} post{filteredPosts.length !== 1 ? 's' : ''} in 
              <Badge variant="secondary" className="ml-2">{selectedCategory}</Badge>
            </p>
          </div>
        )}

        {/* Blog Posts Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {regularPosts.map((post) => {
            const Icon = post.icon
            return (
              <Card key={post.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-3">
                    <Icon className={`h-8 w-8 ${post.color}`} />
                    <Badge variant="outline">{post.category}</Badge>
                  </div>
                  <CardTitle className="text-xl hover:text-primary transition-colors">
                    <Link href={`/blog/${post.slug}`}>
                      {post.title}
                    </Link>
                  </CardTitle>
                  <CardDescription className="mt-2">
                    {post.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {post.date}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {post.readTime}
                    </span>
                  </div>
                  <Button variant="ghost" size="sm" className="mt-4 -ml-2" asChild>
                    <Link href={`/blog/${post.slug}`}>
                      Read article
                      <ChevronRight className="ml-1 h-4 w-4" />
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Newsletter CTA */}
        <Card className="mt-12 bg-primary text-primary-foreground">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Stay Updated</CardTitle>
            <CardDescription className="text-primary-foreground/80">
              Get the latest CCDebugger updates, tips, and tutorials delivered to your inbox
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="max-w-md mx-auto">
              <div className="flex gap-2">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-3 py-2 rounded-md bg-background text-foreground"
                />
                <Button variant="secondary">
                  Subscribe
                </Button>
              </div>
              <p className="text-xs mt-2 text-primary-foreground/60">
                We respect your privacy. Unsubscribe at any time.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default function BlogPage() {
  return (
    <Suspense fallback={<div className="container px-4 md:px-6 py-12">Loading...</div>}>
      <BlogContent />
    </Suspense>
  )
}
"use client"

import { ReactNode } from "react"
import Link from "next/link"
import { ArrowLeft, Clock, Calendar, Tag, Share2, Twitter, Linkedin, Copy } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import "@/app/blog/blog.css"

interface BlogLayoutProps {
  children: ReactNode
  metadata: {
    title: string
    description: string
    date: string
    readTime: string
    category: string
    tags: string[]
  }
  relatedPosts?: Array<{
    title: string
    slug: string
    description: string
    readTime: string
  }>
}

export function BlogLayout({ children, metadata, relatedPosts }: BlogLayoutProps) {
  const shareUrl = typeof window !== 'undefined' ? window.location.href : ''
  
  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareUrl)
    toast.success("Link copied to clipboard!")
  }
  
  const shareOnTwitter = () => {
    window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(metadata.title)}&url=${encodeURIComponent(shareUrl)}`, '_blank')
  }
  
  const shareOnLinkedIn = () => {
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`, '_blank')
  }

  return (
    <article className="blog-article">
      {/* Back to blog */}
      <Link 
        href="/blog" 
        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-8"
      >
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back to blog
      </Link>

      {/* Article header */}
      <header className="article-header">
        <div className="flex items-center gap-2 mb-4">
          <Badge variant="secondary">{metadata.category}</Badge>
          {metadata.tags.map((tag) => (
            <Badge key={tag} variant="outline">{tag}</Badge>
          ))}
        </div>
        
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          {metadata.title}
        </h1>
        
        <p className="text-xl text-muted-foreground mb-6">
          {metadata.description}
        </p>
        
        <div className="article-meta">
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" />
            {metadata.date}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            {metadata.readTime} read
          </span>
        </div>
      </header>

      {/* Share section */}
      <div className="share-section">
        <span className="text-sm font-medium">Share this article:</span>
        <Button 
          variant="outline" 
          size="sm" 
          className="share-button"
          onClick={shareOnTwitter}
        >
          <Twitter className="h-4 w-4" />
          Twitter
        </Button>
        <Button 
          variant="outline" 
          size="sm" 
          className="share-button"
          onClick={shareOnLinkedIn}
        >
          <Linkedin className="h-4 w-4" />
          LinkedIn
        </Button>
        <Button 
          variant="outline" 
          size="sm" 
          className="share-button"
          onClick={copyToClipboard}
        >
          <Copy className="h-4 w-4" />
          Copy Link
        </Button>
      </div>

      {/* Article content */}
      <div className="blog-content">
        {children}
      </div>

      {/* Newsletter signup */}
      <div className="newsletter-signup">
        <h3 className="newsletter-title">Stay Updated</h3>
        <p className="newsletter-description">
          Get the latest debugging tips and CCDebugger updates delivered to your inbox.
        </p>
        <form className="newsletter-form" onSubmit={(e) => {
          e.preventDefault()
          toast.success("Thanks for subscribing! Check your email for confirmation.")
        }}>
          <input
            type="email"
            placeholder="Enter your email"
            className="newsletter-input"
            required
          />
          <button type="submit" className="newsletter-button">
            Subscribe
          </button>
        </form>
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
          {metadata.tags.map((tag) => (
            <Badge key={tag} variant="outline">
              <Tag className="mr-1 h-3 w-3" />
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      {/* Related posts */}
      {relatedPosts && relatedPosts.length > 0 && (
        <div className="related-posts">
          <h3 className="text-2xl font-bold mb-6">Related Articles</h3>
          <div className="related-posts-grid">
            {relatedPosts.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group p-6 bg-card rounded-lg border hover:border-primary transition-colors"
              >
                <h4 className="font-semibold mb-2 group-hover:text-primary transition-colors">
                  {post.title}
                </h4>
                <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                  {post.description}
                </p>
                <span className="text-xs text-muted-foreground">
                  {post.readTime} read
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </article>
  )
}
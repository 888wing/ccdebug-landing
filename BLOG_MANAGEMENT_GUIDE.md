# Blog Management Guide for CCDebugger Landing Page

## 📝 How to Add a New Blog Post

### Quick Steps

1. **Create a new folder** under `src/app/blog/`:
   ```
   src/app/blog/your-post-slug/
   ```

2. **Create `page.tsx`** in that folder with your blog content

3. **Update the blog listing** in `src/app/blog/page.tsx`

### Detailed Instructions

#### Step 1: Create Blog Post Directory

Choose a URL-friendly slug for your post:
```bash
# Example: "How to Debug Async Errors" becomes "debug-async-errors"
mkdir -p src/app/blog/debug-async-errors
```

#### Step 2: Create the Blog Post Page

Create `src/app/blog/debug-async-errors/page.tsx`:

```tsx
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import Link from "next/link"
import { ArrowLeft, Clock, Calendar, Tag } from "lucide-react"

export default function YourBlogPost() {
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
          <Badge variant="secondary">Tutorial</Badge>
          <Badge variant="outline">Debugging</Badge>
        </div>
        
        <h1 className="text-4xl font-bold mb-4">
          Your Blog Post Title
        </h1>
        
        <p className="text-xl text-muted-foreground mb-6">
          A brief description of what this post covers
        </p>
        
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" />
            January 15, 2025
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            5 min read
          </span>
        </div>
      </header>

      <Separator className="mb-8" />

      {/* Article content */}
      <div className="prose prose-neutral dark:prose-invert max-w-none">
        <section className="mb-8">
          <h2>Introduction</h2>
          <p>
            Your introduction paragraph here...
          </p>
        </section>

        {/* Add more sections as needed */}
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
            Tutorial
          </Badge>
        </div>
      </div>
    </article>
  )
}
```

#### Step 3: Update Blog Listing

Add your new post to the `blogPosts` array in `src/app/blog/page.tsx`:

```tsx
const blogPosts = [
  // ... existing posts
  {
    id: 6, // increment from last ID
    slug: "debug-async-errors", // matches your folder name
    title: "How to Debug Async Errors",
    description: "Master async/await debugging with CCDebugger",
    category: "Tutorial",
    readTime: "5 min read",
    date: "January 15, 2025",
    icon: BookOpen, // Choose an icon from lucide-react
    color: "text-blue-500", // Choose a color
    featured: false // Set to true to feature this post
  }
]
```

Don't forget to update the category counts:
```tsx
const categories = [
  { name: "All", count: blogPosts.length },
  { name: "Tutorial", count: 2 }, // Update count
  // ... other categories
]
```

## 🎨 Blog Post Categories

Available categories and their icons:
- **Tutorial** - `BookOpen` icon, blue color
- **Technical** - `Lightbulb` icon, purple color  
- **Guide** - `Code2` icon, green color
- **Performance** - `Zap` icon, yellow color
- **Story** - `Users` icon, pink color
- **News** - `Newspaper` icon, orange color
- **Update** - `RefreshCw` icon, cyan color

## 📅 Blog Post Metadata

Each blog post should include:
- **Title**: Clear and descriptive
- **Description**: 1-2 sentence summary
- **Category**: One of the available categories
- **Read Time**: Estimate based on ~200 words/minute
- **Date**: Publication date
- **Tags**: Relevant tags in badges
- **Featured**: Boolean to highlight important posts

## 🖼️ Adding Images

Store images in `public/blog/` directory:
```
public/
  blog/
    debug-async-errors/
      hero-image.png
      screenshot-1.png
```

Use in your blog post:
```tsx
<img 
  src="/blog/debug-async-errors/hero-image.png" 
  alt="Debugging async errors"
  className="rounded-lg"
/>
```

## 📝 Writing Tips

### Content Structure
1. **Introduction**: Hook the reader, explain what they'll learn
2. **Main Content**: Break into logical sections with headers
3. **Code Examples**: Use syntax highlighting with proper language tags
4. **Conclusion**: Summarize key points, provide next steps

### Code Blocks
```tsx
<pre className="bg-muted p-4 rounded-lg overflow-x-auto">
  <code>{`
// Your code here
const example = "Use template literals for multiline code";
  `}</code>
</pre>
```

### Formatting Options
- **Bold**: `<strong>Important text</strong>`
- **Italic**: `<em>Emphasized text</em>`
- **Links**: `<Link href="/docs" className="text-primary hover:underline">Documentation</Link>`
- **Lists**: Use `<ul>` and `<ol>` with `<li>` items
- **Quotes**: `<blockquote>Quote text</blockquote>`

## 🚀 Publishing Workflow

1. **Write**: Create your blog post following the template
2. **Review**: Check for typos, broken links, code accuracy
3. **Test**: Run `npm run dev` and preview your post
4. **Update**: Add to blog listing page
5. **Deploy**: Push to GitHub for automatic deployment

## 📊 Blog Analytics

Track performance with these metrics:
- Page views (add Google Analytics)
- Read time (actual vs estimated)
- Social shares
- Comments/feedback

## 🔄 Updating Existing Posts

To update an existing blog post:
1. Navigate to the post's directory
2. Edit the `page.tsx` file
3. Update the date in blog listing if needed
4. Consider adding an "Updated on" notice

Example update notice:
```tsx
<div className="bg-muted p-4 rounded-lg mb-6">
  <p className="text-sm">
    <strong>Updated:</strong> January 20, 2025 - Added new examples for TypeScript errors
  </p>
</div>
```

## 📁 Blog Structure Overview

```
src/app/blog/
├── page.tsx                    # Blog listing page
├── getting-started/
│   └── page.tsx               # Individual blog post
├── understanding-ai-error-analysis/
│   └── page.tsx
├── custom-templates/
│   └── page.tsx
├── performance-tips/
│   └── page.tsx
└── building-ccdebugger/
    └── page.tsx
```

## 🎯 SEO Best Practices

1. **URL Slug**: Use descriptive, keyword-rich slugs
2. **Title**: Include primary keyword, keep under 60 characters
3. **Description**: Compelling summary under 160 characters
4. **Headers**: Use proper H1, H2, H3 hierarchy
5. **Alt Text**: Add descriptive alt text to all images

## 🛠️ Maintenance Tasks

### Weekly
- Review and respond to comments
- Check for broken links
- Update outdated information

### Monthly
- Analyze popular posts
- Plan new content based on user needs
- Update category counts

### Quarterly
- Audit all posts for accuracy
- Refresh screenshots and examples
- Archive outdated content

## 💡 Content Ideas

Keep a running list of blog post ideas:
- Common error patterns and solutions
- New feature announcements
- Community spotlights
- Integration guides
- Performance case studies
- Tips and tricks
- Video tutorials (embedded)

## 🤝 Guest Posts

To accept guest posts:
1. Create author attribution component
2. Add author bio section
3. Include social links
4. Review for quality and relevance

## 📢 Promoting Blog Posts

After publishing:
1. Share on social media
2. Include in newsletter
3. Cross-link from documentation
4. Notify community channels
5. Submit to relevant aggregators

---

**Need Help?** Check existing blog posts for examples or reach out to the CCDebugger team!
#!/bin/bash

# CCDebugger Blog Post Creator Script
# Usage: ./scripts/create-blog-post.sh "post-slug" "Post Title" "Category"

echo "🚀 CCDebugger Blog Post Creator"
echo "==============================="

# Check if required arguments are provided
if [ $# -lt 3 ]; then
    echo "❌ Error: Missing arguments"
    echo "Usage: $0 <post-slug> <post-title> <category>"
    echo "Example: $0 \"debug-async-errors\" \"How to Debug Async Errors\" \"Tutorial\""
    exit 1
fi

SLUG=$1
TITLE=$2
CATEGORY=$3
DATE=$(date +"%B %d, %Y")
COMPONENT_NAME=$(echo "$SLUG" | sed 's/-\([a-z]\)/\U\1/g' | sed 's/^./\U&/')

# Create blog post directory
BLOG_DIR="src/app/blog/$SLUG"
if [ -d "$BLOG_DIR" ]; then
    echo "❌ Error: Blog post directory already exists: $BLOG_DIR"
    exit 1
fi

echo "📁 Creating directory: $BLOG_DIR"
mkdir -p "$BLOG_DIR"

# Create the blog post template
echo "📝 Creating blog post template..."
cat > "$BLOG_DIR/page.tsx" << EOF
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import Link from "next/link"
import { ArrowLeft, Clock, Calendar, Tag } from "lucide-react"

export default function ${COMPONENT_NAME}() {
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
          <Badge variant="secondary">${CATEGORY}</Badge>
          <Badge variant="outline">Tag1</Badge>
          <Badge variant="outline">Tag2</Badge>
        </div>
        
        <h1 className="text-4xl font-bold mb-4">
          ${TITLE}
        </h1>
        
        <p className="text-xl text-muted-foreground mb-6">
          A brief description of what this post covers. Update this with a compelling summary.
        </p>
        
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1">
            <Calendar className="h-4 w-4" />
            ${DATE}
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
            Start your blog post with an engaging introduction that explains what 
            readers will learn and why it matters.
          </p>
        </section>

        <section className="mb-8">
          <h2>Main Content Section 1</h2>
          <p>
            Dive into the main content of your post. Break it into logical sections 
            with clear headers.
          </p>
          
          <h3>Subsection Example</h3>
          <p>
            Use h3 tags for subsections within your main sections.
          </p>
          
          <pre className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code>{\`// Add code examples like this
const example = "Your code here";
console.log(example);\`}</code>
          </pre>
        </section>

        <section className="mb-8">
          <h2>Main Content Section 2</h2>
          <p>
            Continue with additional sections as needed. Remember to:
          </p>
          <ul>
            <li>Keep paragraphs concise and scannable</li>
            <li>Use bullet points for lists</li>
            <li>Include relevant code examples</li>
            <li>Add images where helpful</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2>Best Practices</h2>
          <p>
            Share best practices, tips, or recommendations related to your topic.
          </p>
          <ol>
            <li>First best practice</li>
            <li>Second best practice</li>
            <li>Third best practice</li>
          </ol>
        </section>

        <section className="mb-8">
          <h2>Conclusion</h2>
          <p>
            Wrap up your post by summarizing the key points and providing next steps 
            for readers. Encourage them to try CCDebugger or explore related topics.
          </p>
          <p>
            End with a call to action, such as trying out the techniques discussed or 
            <Link href="/" className="text-primary hover:underline">getting started with CCDebugger</Link>.
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
            ${CATEGORY}
          </Badge>
          <Badge variant="outline">
            <Tag className="mr-1 h-3 w-3" />
            Tag1
          </Badge>
          <Badge variant="outline">
            <Tag className="mr-1 h-3 w-3" />
            Tag2
          </Badge>
        </div>
      </div>
    </article>
  )
}
EOF

echo "✅ Blog post template created!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the blog post content in: $BLOG_DIR/page.tsx"
echo "2. Update the description and tags"
echo "3. Add your content to the sections"
echo "4. Add the post to src/app/blog/page.tsx:"
echo ""
echo "   {
     id: [NEXT_ID],
     slug: \"$SLUG\",
     title: \"$TITLE\",
     description: \"[Add description]\",
     category: \"$CATEGORY\",
     readTime: \"[X] min read\",
     date: \"$DATE\",
     icon: [Choose Icon],
     color: \"text-[color]-500\",
     featured: false
   }"
echo ""
echo "5. Update category counts in src/app/blog/page.tsx"
echo "6. Test locally with: npm run dev"
echo "7. Deploy with: npm run build && ./scripts/deploy-github-pages.sh"
echo ""
echo "🎉 Happy writing!"
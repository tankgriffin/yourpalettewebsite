  🚀 How to Add New Blog Posts:

  Method 1: Automated (Recommended)

  node create-blog-post.js
  - Follow the interactive prompts
  - Script generates the HTML file automatically
  - Provides copy-paste code for blog.html

  Method 2: Manual

  1. Copy blog-post-template.html
  2. Rename to your-post-slug.html
  3. Replace all {{PLACEHOLDER}} values
  4. Add content where {{POST_CONTENT}} is
  5. Add the post card to blog.html

  ✨ Benefits of This Approach:

  ✅ Better SEO - Each post has its own URL and meta tags✅ Easier Content Management - Edit posts
  independently✅ Cleaner Code - No complex JavaScript arrays✅ Better Performance - Individual
  files load faster✅ Scalable - Add unlimited posts easily✅ Professional URLs -
  korean-glass-skin.html vs parameters

  🎯 Example Workflow:

  1. Run: node create-blog-post.js
  2. Enter: "How to Apply Foundation Like a Pro"
  3. Generated: how-to-apply-foundation-like-a-pro.html
  4. Edit: Replace template content with your article
  5. Update: Add the provided card HTML to blog.html
  6. Done: Your new post is live!

  📋 File Structure:

  your-palette/
  ├── blog.html                          (main blog listing)
  ├── blog-post-template.html            (template)
  ├── korean-glass-skin.html             (example post)
  ├── create-blog-post.js                (generator script)
  ├── blog-post-template.md              (content guide)
  └── img/
      └── post-images.jpg
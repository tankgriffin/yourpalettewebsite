#!/usr/bin/env node

/**
 * Blog Post Generator for Your Palette Website
 * 
 * This script helps you create new blog post HTML files from the template.
 * 
 * Usage:
 * 1. Install Node.js on your system
 * 2. Run: node create-blog-post.js
 * 3. Follow the prompts to create your blog post
 * 
 * Or run with command line arguments:
 * node create-blog-post.js "Post Title" "post-slug" "category" "excerpt" "author" "date" "read-time" "image" "tags"
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Create readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Helper function to prompt user for input
function prompt(question, defaultValue = '') {
    return new Promise((resolve) => {
        const displayQuestion = defaultValue ? `${question} (${defaultValue}): ` : `${question}: `;
        rl.question(displayQuestion, (answer) => {
            resolve(answer.trim() || defaultValue);
        });
    });
}

// Helper function to create URL-friendly slug
function createSlug(title) {
    return title
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim('-');
}

// Helper function to capitalize category display name
function formatCategory(category) {
    return category.charAt(0).toUpperCase() + category.slice(1).replace('-', ' ');
}

// Helper function to create tag HTML
function createTagsHTML(tagsString) {
    const tags = tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
    return tags.map(tag => `<span class="tag-badge">${tag}</span>`).join('\n                                ');
}

// Main function to generate blog post
async function generateBlogPost() {
    console.log('\n🎨 Your Palette Blog Post Generator\n');
    console.log('Create a new blog post by filling in the details below.\n');

    try {
        // Collect blog post information
        const title = await prompt('Post Title', 'My Amazing K-Beauty Tutorial');
        const slug = await prompt('URL Slug', createSlug(title));
        const category = await prompt('Category (k-beauty/tutorials/trends/reviews/skincare)', 'tutorials');
        const excerpt = await prompt('Excerpt (brief description)', 'Discover amazing beauty techniques...');
        const author = await prompt('Author', 'Beauty Team');
        const date = await prompt('Publication Date', new Date().toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        }));
        const readTime = await prompt('Read Time', '5 min read');
        const image = await prompt('Featured Image', 'img/your-post-image.jpg');
        const tags = await prompt('Tags (comma-separated)', 'tutorial, k-beauty, makeup');
        const metaDescription = await prompt('Meta Description (SEO)', excerpt.substring(0, 150));

        // Read the template file
        const templatePath = path.join(__dirname, 'blog-post-template.html');
        let template = fs.readFileSync(templatePath, 'utf8');

        // Replace template placeholders
        const replacements = {
            '{{POST_TITLE}}': title,
            '{{META_DESCRIPTION}}': metaDescription,
            '{{OG_IMAGE}}': image,
            '{{POST_URL}}': `${slug}.html`,
            '{{CATEGORY}}': category,
            '{{CATEGORY_DISPLAY}}': formatCategory(category),
            '{{READ_TIME}}': readTime,
            '{{AUTHOR}}': author,
            '{{POST_DATE}}': date,
            '{{POST_CONTENT}}': `
                        <img src="${image}" class="img-fluid mb-4" alt="${title}">
                        
                        <h2>Introduction</h2>
                        <p>Welcome to this exciting guide about ${title.toLowerCase()}. This comprehensive article will teach you everything you need to know.</p>
                        
                        <h2>Main Content</h2>
                        <p>Add your main content here. You can include:</p>
                        <ul>
                            <li>Step-by-step instructions</li>
                            <li>Professional tips and tricks</li>
                            <li>Product recommendations</li>
                            <li>Before and after examples</li>
                        </ul>
                        
                        <h3>Your Palette Tools</h3>
                        <p>Don't forget to mention how our <a href="product-details.html">Professional Makeup Tools</a> can help achieve the best results.</p>
                        
                        <h2>Conclusion</h2>
                        <p>You now have all the knowledge needed to master this technique. Practice these tips and enjoy your beauty journey!</p>`,
            '{{TAGS}}': createTagsHTML(tags),
            '{{RELATED_POSTS}}': `
                        <div class="col-lg-4 col-md-6 mb-4">
                            <div class="card blog-post-card">
                                <div class="blog-post-image" style="background-image: url('img/korean-spatula.jpg');">
                                </div>
                                <div class="card-body">
                                    <div class="post-meta">
                                        <span class="category-tag tutorials">Tutorials</span>
                                        <span class="read-time"><i class="fas fa-clock"></i> 4 min read</span>
                                    </div>
                                    <h5 class="card-title">Essential K-Beauty Tools Every Makeup Lover Needs</h5>
                                    <p class="card-text">From mixing palettes to precision spatulas...</p>
                                    <a href="k-beauty-tools.html" class="btn btn-primary-custom btn-sm">Read Article</a>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-lg-4 col-md-6 mb-4">
                            <div class="card blog-post-card">
                                <div class="blog-post-image" style="background-image: url('img/korean-glass-skin.jpg');">
                                </div>
                                <div class="card-body">
                                    <div class="post-meta">
                                        <span class="category-tag k-beauty">K-Beauty</span>
                                        <span class="read-time"><i class="fas fa-clock"></i> 5 min read</span>
                                    </div>
                                    <h5 class="card-title">The Ultimate Guide to Korean Glass Skin</h5>
                                    <p class="card-text">Achieve that perfect luminous glow...</p>
                                    <a href="korean-glass-skin.html" class="btn btn-primary-custom btn-sm">Read Article</a>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-lg-4 col-md-6 mb-4">
                            <div class="card blog-post-card">
                                <div class="blog-post-image" style="background-image: url('img/makeup-palette-3.jpg');">
                                </div>
                                <div class="card-body">
                                    <div class="post-meta">
                                        <span class="category-tag reviews">Reviews</span>
                                        <span class="read-time"><i class="fas fa-clock"></i> 4 min read</span>
                                    </div>
                                    <h5 class="card-title">Professional Makeup Mixing Palettes Review</h5>
                                    <p class="card-text">Everything about choosing the perfect palette...</p>
                                    <a href="makeup-palette-review.html" class="btn btn-primary-custom btn-sm">Read Article</a>
                                </div>
                            </div>
                        </div>`
        };

        // Apply all replacements
        Object.keys(replacements).forEach(placeholder => {
            template = template.replace(new RegExp(placeholder, 'g'), replacements[placeholder]);
        });

        // Write the new blog post file
        const outputPath = path.join(__dirname, `${slug}.html`);
        fs.writeFileSync(outputPath, template);

        console.log('\n✅ Blog post created successfully!');
        console.log(`📁 File: ${slug}.html`);
        console.log(`🌐 URL: ${slug}.html`);
        console.log('\n📝 Next steps:');
        console.log('1. Edit the content in your new HTML file');
        console.log('2. Add your blog post card to blog.html');
        console.log('3. Upload your featured image to the img/ folder');
        console.log('4. Test your new blog post');

        // Generate blog.html card snippet
        const cardSnippet = `
                <div class="col-lg-4 col-md-6 mb-4">
                    <article class="blog-post-card">
                        <div class="blog-post-image" style="background-image: url('${image}');">
                            <div class="post-overlay">
                                <a href="${slug}.html" class="btn btn-primary-custom">Read Article</a>
                            </div>
                        </div>
                        <div class="blog-post-content">
                            <div class="post-meta">
                                <span class="category-tag ${category}">${formatCategory(category)}</span>
                                <span class="post-date">${date}</span>
                                <span class="read-time"><i class="fas fa-clock"></i> ${readTime}</span>
                            </div>
                            <h4 class="post-title">${title}</h4>
                            <p class="post-excerpt">${excerpt}</p>
                            <div class="post-actions">
                                <a href="${slug}.html" class="btn btn-outline-custom btn-sm">Read More</a>
                                <div class="social-share-mini">
                                    <a href="#" class="social-link"><i class="fas fa-share-alt"></i></a>
                                    <a href="#" class="social-link"><i class="fas fa-heart"></i></a>
                                </div>
                            </div>
                        </div>
                    </article>
                </div>`;

        console.log('\n📋 Add this card to blog.html:');
        console.log('───────────────────────────────────');
        console.log(cardSnippet);
        console.log('───────────────────────────────────');

    } catch (error) {
        console.error('❌ Error creating blog post:', error.message);
    } finally {
        rl.close();
    }
}

// Check if running from command line with arguments
if (process.argv.length > 2) {
    // Command line mode
    const [title, slug, category, excerpt, author, date, readTime, image, tags] = process.argv.slice(2);
    
    if (!title) {
        console.error('Usage: node create-blog-post.js "Title" "slug" "category" "excerpt" "author" "date" "readTime" "image" "tags"');
        process.exit(1);
    }

    // Use provided arguments or defaults
    const postData = {
        title: title,
        slug: slug || createSlug(title),
        category: category || 'tutorials',
        excerpt: excerpt || 'Discover amazing beauty techniques...',
        author: author || 'Beauty Team',
        date: date || new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
        readTime: readTime || '5 min read',
        image: image || 'img/your-post-image.jpg',
        tags: tags || 'tutorial, k-beauty, makeup'
    };

    console.log('Creating blog post with provided arguments...');
    // Process the blog post creation synchronously
    try {
        const templatePath = path.join(__dirname, 'blog-post-template.html');
        let template = fs.readFileSync(templatePath, 'utf8');

        const replacements = {
            '{{POST_TITLE}}': postData.title,
            '{{META_DESCRIPTION}}': postData.excerpt.substring(0, 150),
            '{{OG_IMAGE}}': postData.image,
            '{{POST_URL}}': `${postData.slug}.html`,
            '{{CATEGORY}}': postData.category,
            '{{CATEGORY_DISPLAY}}': formatCategory(postData.category),
            '{{READ_TIME}}': postData.readTime,
            '{{AUTHOR}}': postData.author,
            '{{POST_DATE}}': postData.date,
            '{{TAGS}}': createTagsHTML(postData.tags),
            '{{POST_CONTENT}}': `<p>Content for ${postData.title}</p>`,
            '{{RELATED_POSTS}}': ''
        };

        Object.keys(replacements).forEach(placeholder => {
            template = template.replace(new RegExp(placeholder, 'g'), replacements[placeholder]);
        });

        const outputPath = path.join(__dirname, `${postData.slug}.html`);
        fs.writeFileSync(outputPath, template);

        console.log(`✅ Blog post created: ${postData.slug}.html`);
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
} else {
    // Interactive mode
    generateBlogPost();
}
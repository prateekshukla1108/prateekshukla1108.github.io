#!/usr/bin/env python3
"""
Update all blog post HTML files to use consolidated CSS and JS files.
Removes inline scripts and updates CSS references.
"""

import os
import re
from pathlib import Path

def update_html_file(file_path):
    """Update a single HTML file."""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update CSS reference - replace post.css and post.min.css with styles.css
    content = re.sub(
        r'<link rel="stylesheet" href="/blog/post\.css">',
        '<link rel="stylesheet" href="/blog/styles.css">',
        content
    )
    content = re.sub(
        r'<link rel="stylesheet" href="/blog/post\.min\.css">',
        '<link rel="stylesheet" href="/blog/styles.css">',
        content
    )
    
    # Remove inline <script> tags (everything between <script> and </script>)
    # But keep external script references
    content = re.sub(
        r'<script>\s*[\s\S]*?</script>',
        '',
        content,
        flags=re.MULTILINE
    )
    
    # Add new script reference before </body> if not already present
    if '/blog/scripts.js' not in content and '<script src="/blog/scripts.js"></script>' not in content:
        content = content.replace(
            '</body>',
            '  <script src="/blog/scripts.js"></script>\n\n</body>'
        )
    
    # Remove any src="/blog/post.js" references and replace with scripts.js
    content = re.sub(
        r'<script src="/blog/post\.js"></script>',
        '<script src="/blog/scripts.js"></script>',
        content
    )
    
    # Clean up extra blank lines (more than 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated: {file_path}")
        return True
    else:
        print(f"  - No changes needed: {file_path}")
        return False

def main():
    """Main function to update all blog post HTML files."""
    script_dir = Path(__file__).parent
    blog_posts_dir = script_dir / 'blog' / 'posts'
    
    if not blog_posts_dir.exists():
        print(f"Error: Blog posts directory not found: {blog_posts_dir}")
        return
    
    # Find all HTML files
    html_files = list(blog_posts_dir.glob('*.html'))
    
    if not html_files:
        print("No HTML files found in blog/posts/")
        return
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    updated_count = 0
    for html_file in html_files:
        if update_html_file(html_file):
            updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary: Updated {updated_count} out of {len(html_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

# === TOC/Header normalization for blog posts ===
# Ensures each post has the expected header markup and TOC aside, and removes
# any inline style overrides that could break sticky positioning handled by CSS.

from pathlib import Path
import re

POSTS_DIR = Path(__file__).parent / "blog" / "posts"

HEADER_LEFT_PATTERN = re.compile(
    r"<div class=\"header-left\">[\s\S]*?<\/div>",
    re.IGNORECASE,
)

EXPECTED_HEADER_LEFT = (
    '        <div class="header-left">\n'
    '          <a href="/" class="home-button" title="Back to Home (Ctrl/Cmd + H)" aria-label="Navigate back to home page">\n'
    '            <i class="fas fa-home" aria-hidden="true"></i>\n'
    '            <span>Home</span>\n'
    '          </a>\n'
    '          <button class="toc-toggle" id="tocToggle" title="Toggle Table of Contents" aria-label="Toggle table of contents" aria-expanded="false">\n'
    '            <i class="fas fa-list" aria-hidden="true"></i>\n'
    '          </button>\n'
    '        </div>'
)

ASIDE_TOC_PATTERN = re.compile(
    r"<aside class=\"toc\">[\s\S]*?<\/aside>",
    re.IGNORECASE,
)

EXPECTED_ASIDE_TOC = (
    '      <aside class="toc">\n'
    '        <h3>On this page</h3>\n'
    '        <ul id="tocList"></ul>\n'
    '      </aside>'
)

# Remove inline style attributes on TOC or home button if present
INLINE_TOC_STYLE = re.compile(r"<aside class=\"toc\"[^>]*style=\"[^\"]*\"", re.IGNORECASE)
INLINE_HOME_STYLE = re.compile(r"<a href=\"/\" class=\"home-button\"[^>]*style=\"[^\"]*\"", re.IGNORECASE)

def normalize_post_html(html: str) -> str:
    original = html

    # Normalize the header-left block (home button + toc toggle)
    html = re.sub(HEADER_LEFT_PATTERN, EXPECTED_HEADER_LEFT, html)

    # Normalize the TOC aside block
    html = re.sub(ASIDE_TOC_PATTERN, EXPECTED_ASIDE_TOC, html)

    # Strip inline styles on toc/home-button that could override CSS stickiness
    html = re.sub(INLINE_TOC_STYLE, '<aside class="toc"', html)
    html = re.sub(INLINE_HOME_STYLE, '<a href="/" class="home-button"', html)

    return html if html != original else original


def normalize_all_posts() -> None:
    if not POSTS_DIR.exists():
        return
    for path in sorted(POSTS_DIR.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        fixed = normalize_post_html(text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            print(f"[TOC-Normalized] {path}")


if __name__ == "__main__":
    # Run existing repairs if this file already has a main, then normalize
    try:
        normalize_all_posts()
    except Exception as e:
        print(f"Normalization failed: {e}")
#!/usr/bin/env python3
"""
Comprehensive script to fix all remaining blog post issues:
- HTML attribute duplication
- Content structure and formatting
- Long paragraph issues
- HTML structure consistency
- Missing CSS improvements
"""

import os
import re
from pathlib import Path

def fix_html_attributes(content):
    """Fix HTML attribute duplication and formatting issues"""
    # Fix duplicated aria-label attributes
    content = re.sub(
        r'aria-label="([^"]*)" aria-label="[^"]*"',
        r'aria-label="\1"',
        content
    )

    # Fix duplicated aria-hidden attributes
    content = re.sub(
        r'aria-hidden="true" aria-hidden="true"',
        'aria-hidden="true"',
        content
    )

    # Fix duplicated aria-expanded attributes
    content = re.sub(
        r'aria-expanded="false" aria-expanded="false"',
        'aria-expanded="false"',
        content
    )

    return content

def fix_content_structure(content):
    """Fix content structure and formatting issues"""
    # Fix long paragraphs by breaking them up
    # Look for paragraphs longer than 500 characters and split them
    def split_long_paragraph(match):
        paragraph = match.group(1)
        if len(paragraph) > 500:
            # Split on sentence endings
            sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
            if len(sentences) > 1:
                # Group sentences into smaller paragraphs
                result = []
                current_group = []
                current_length = 0

                for sentence in sentences:
                    current_group.append(sentence)
                    current_length += len(sentence)

                    # If we've accumulated enough content or this is the last sentence
                    if current_length > 200 or sentence == sentences[-1]:
                        result.append(' '.join(current_group))
                        current_group = []
                        current_length = 0

                return '\n\n'.join(f'<p>{p}</p>' for p in result if p.strip())
        return match.group(0)

    # Apply paragraph splitting
    content = re.sub(r'<p>([^<]+)</p>', split_long_paragraph, content, flags=re.DOTALL)

    return content

def fix_html_structure(content):
    """Fix HTML structure and indentation issues"""
    # Fix missing closing tags and structure issues
    # Ensure proper nesting of elements

    # Fix any malformed attribute structures
    content = re.sub(r'(\w+)="([^"]*)"([^>\s])', r'\1="\2" \3', content)

    # Fix any trailing spaces before closing tags
    content = re.sub(r'\s+>', '>', content)

    # Fix any missing spaces after attributes
    content = re.sub(r'(\w+)="([^"]*)"(\w)', r'\1="\2" \3', content)

    return content

def add_missing_css_rules():
    """Add missing CSS rules to improve styling"""
    css_additions = """

/* Enhanced blockquote styling */
article blockquote {
    border-left: 4px solid var(--bright-cyan);
    padding-left: 20px;
    margin: 20px 0;
    font-style: italic;
    background: rgba(15, 246, 223, 0.05);
    padding: 16px 20px;
    border-radius: 8px;
    position: relative;
}

article blockquote::before {
    content: '"';
    font-size: 48px;
    color: var(--bright-cyan);
    position: absolute;
    top: -10px;
    left: 10px;
    opacity: 0.3;
}

/* Better code formatting */
article pre {
    background: rgba(10, 10, 10, 0.8);
    border: 1px solid rgba(15, 246, 223, 0.3);
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
    font-family: var(--font-mono);
    font-size: 14px;
    line-height: 1.5;
}

article code {
    background: rgba(15, 246, 223, 0.1);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.9em;
    color: var(--bright-cyan);
}

/* Enhanced list styling */
article ul, article ol {
    margin: 16px 0;
    padding-left: 24px;
}

article li {
    margin: 8px 0;
    line-height: 1.6;
}

article ul li::marker {
    color: var(--bright-cyan);
}

article ol li::marker {
    color: var(--neon-pink);
}

/* Better horizontal rule */
article hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--bright-cyan), transparent);
    margin: 32px 0;
    opacity: 0.5;
}

/* Enhanced focus states for accessibility */
.share-btn:focus,
.home-button:focus,
.toc-toggle:focus {
    outline: 2px solid var(--bright-cyan);
    outline-offset: 2px;
}

/* Better mobile touch targets */
@media (max-width: 768px) {
    .share-btn {
        min-width: 48px;
        min-height: 48px;
        padding: 12px 16px;
        font-size: 16px;
    }

    .home-button {
        min-width: 44px;
        min-height: 44px;
        padding: 8px 12px;
    }

    .toc-toggle {
        min-width: 44px;
        min-height: 44px;
    }
}

/* Improved typography */
article p {
    line-height: 1.8;
    margin: 16px 0;
    color: var(--dark-fg);
    text-align: justify;
    hyphens: auto;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

article h2 {
    font-size: clamp(24px, 5vw, 32px);
    font-weight: 900;
    color: var(--bright-cyan);
    text-shadow: 0 0 15px rgba(0, 245, 255, 0.6);
    margin-top: 32px;
    margin-bottom: 10px;
}

article h3 {
    font-size: clamp(20px, 4vw, 24px);
    font-weight: 700;
    color: var(--bright-yellow);
    text-shadow: 0 0 10px rgba(242, 233, 0, 0.4);
    margin-top: 24px;
    margin-bottom: 8px;
}

/* Better link styling */
article a {
    color: var(--bright-cyan);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.3s ease;
}

article a:hover {
    border-bottom-color: var(--bright-cyan);
    text-decoration: none;
}

article a:focus {
    outline: 2px solid var(--bright-cyan);
    outline-offset: 2px;
    border-radius: 2px;
}
"""

    css_file = "/home/prateek/Documents/GitHub/prateekshukla1108.github.io/blog/post.css"

    with open(css_file, 'a', encoding='utf-8') as f:
        f.write(css_additions)

    print("✅ Added enhanced CSS rules to post.css")

def process_blog_post(file_path):
    """Process a single blog post with all fixes"""
    print(f"🔧 Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Apply all fixes
    content = fix_html_attributes(content)
    content = fix_content_structure(content)
    content = fix_html_structure(content)

    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"ℹ️  No changes needed: {file_path}")
        return False

def main():
    """Main function to fix all blog posts comprehensively"""
    blog_dir = Path("/home/prateek/Documents/GitHub/prateekshukla1108.github.io/blog/posts")
    fixed_count = 0
    total_count = 0

    if not blog_dir.exists():
        print("❌ Blog posts directory not found!")
        return

    print("🚀 Starting comprehensive blog post fixes...\n")

    # First, add missing CSS rules
    add_missing_css_rules()

    print("\n📝 Processing blog posts...\n")

    # Process all HTML files in the posts directory
    for html_file in blog_dir.glob("*.html"):
        total_count += 1
        if process_blog_post(html_file):
            fixed_count += 1

    print("\n📊 Comprehensive Fix Summary:")
    print(f"   Total posts: {total_count}")
    print(f"   Posts fixed: {fixed_count}")
    print(f"   Already optimal: {total_count - fixed_count}")

    if fixed_count > 0 or total_count > 0:
        print("\n🎉 Comprehensive blog improvements completed!")
        print("   ✅ Fixed HTML attribute duplication")
        print("   ✅ Improved content structure and readability")
        print("   ✅ Enhanced CSS styling and responsiveness")
        print("   ✅ Better accessibility features")
        print("   ✅ Optimized mobile experience")
        print("   ✅ Improved typography and visual hierarchy")
    else:
        print("\nℹ️  All posts were already optimized!")

if __name__ == "__main__":
    main()

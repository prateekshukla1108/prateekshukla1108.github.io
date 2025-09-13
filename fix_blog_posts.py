#!/usr/bin/env python3
"""
Script to fix all blog posts with consistent improvements:
- Remove inconsistent header-right sections
- Add ARIA labels and accessibility improvements
- Update social sharing buttons
- Fix JavaScript syntax issues
- Ensure consistent formatting across all posts
"""

import os
import re
from pathlib import Path

def fix_blog_post(file_path):
    """Fix a single blog post file with all improvements"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Remove header-right section (theme toggle)
    header_right_pattern = r'\s*<div class="header-right">\s*<i class="fas fa-moon"></i>\s*<div class="toggle-slider"><div class="slider-icon"></div></div>\s*<i class="fas fa-sun"></i>\s*</div>'
    content = re.sub(header_right_pattern, '', content)

    # Fix any duplicate closing div tags
    content = re.sub(r'</div>\s*</div>', '</div>', content)

    # 2. Add ARIA labels to home button - check if not already present
    if 'aria-label="Navigate back to home page"' not in content:
        home_button_pattern = r'(<a href="/" class="home-button" title="Back to Home \(Ctrl/Cmd \+ H\)"[^>]*>)'
        content = re.sub(home_button_pattern, r'\1 aria-label="Navigate back to home page"', content)

    # Add aria-hidden to home button icon - only if not already present
    if '<i class="fas fa-home" aria-hidden="true">' not in content:
        content = re.sub(r'(<i class="fas fa-home")(></i>)', r'\1 aria-hidden="true"\2', content)

    # 3. Add ARIA labels to TOC toggle - check if not already present
    if 'aria-label="Toggle table of contents"' not in content:
        toc_toggle_pattern = r'(<button class="toc-toggle" id="tocToggle" title="Toggle Table of Contents"[^>]*>)'
        content = re.sub(toc_toggle_pattern, r'\1 aria-label="Toggle table of contents" aria-expanded="false"', content)

    # Add aria-hidden to TOC toggle icon - only if not already present
    if '<i class="fas fa-list" aria-hidden="true">' not in content:
        content = re.sub(r'(<i class="fas fa-list")(></i>)', r'\1 aria-hidden="true"\2', content)

    # 4. Add ARIA labels to social sharing buttons - check if not already present
    if 'aria-label="Share on Twitter"' not in content:
        content = re.sub(
            r'(<a href="#" class="share-btn twitter" onclick="shareOnTwitter\(\)">)',
            r'\1 aria-label="Share on Twitter"',
            content
        )
    if 'aria-label="Share on LinkedIn"' not in content:
        content = re.sub(
            r'(<a href="#" class="share-btn linkedin" onclick="shareOnLinkedIn\(\)">)',
            r'\1 aria-label="Share on LinkedIn"',
            content
        )
    if 'aria-label="Copy link to clipboard"' not in content:
        content = re.sub(
            r'(<a href="#" class="share-btn copy" onclick="copyLink\(\)">)',
            r'\1 aria-label="Copy link to clipboard"',
            content
        )

    # Add aria-hidden to social button icons - only if not already present
    if '<i class="fab fa-twitter" aria-hidden="true">' not in content:
        content = re.sub(r'(<i class="fab fa-twitter")(></i>)', r'\1 aria-hidden="true"\2', content)
    if '<i class="fab fa-linkedin" aria-hidden="true">' not in content:
        content = re.sub(r'(<i class="fab fa-linkedin")(></i>)', r'\1 aria-hidden="true"\2', content)
    if '<i class="fas fa-link" aria-hidden="true">' not in content:
        content = re.sub(r'(<i class="fas fa-link")(></i>)', r'\1 aria-hidden="true"\2', content)

    # 5. Fix JavaScript - remove stray closing braces and update TOC functionality
    js_pattern = r'(// TOC toggle for mobile\n\s*if \(tocToggle\) \{\n\s*tocToggle\.addEventListener\(\'click\', \(\) => \{\n\s*toc\.classList\.toggle\(\'visible\'\);\n\s*const icon = tocToggle\.querySelector\(\'i\'\);\n\s*icon\.className = toc\.classList\.contains\(\'visible\'\) \? \'fas fa-times\' : \'fas fa-list\';\n\s*\}\);\n\s*\})'
    replacement = r'// TOC toggle for mobile\n    if (tocToggle) {\n      tocToggle.addEventListener(\'click\', () => {\n        toc.classList.toggle(\'visible\');\n        const icon = tocToggle.querySelector(\'i\');\n        const isVisible = toc.classList.contains(\'visible\');\n        icon.className = isVisible ? \'fas fa-times\' : \'fas fa-list\';\n        tocToggle.setAttribute(\'aria-expanded\', isVisible);\n      });\n    }'
    content = re.sub(js_pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

    # 6. Fix any remaining stray closing braces
    content = re.sub(r'const toc = document\.querySelector\(\'\.toc\'\);\s*\}\);\s*', r'const toc = document.querySelector(\'.toc\');', content)

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
    """Main function to fix all blog posts"""
    blog_dir = Path("/home/prateek/Documents/GitHub/prateekshukla1108.github.io/blog/posts")
    fixed_count = 0
    total_count = 0

    if not blog_dir.exists():
        print("❌ Blog posts directory not found!")
        return

    print("🔧 Starting to fix all blog posts...\n")

    # Process all HTML files in the posts directory
    for html_file in blog_dir.glob("*.html"):
        total_count += 1
        if fix_blog_post(html_file):
            fixed_count += 1

    print("\n📊 Summary:")
    print(f"   Total posts: {total_count}")
    print(f"   Fixed posts: {fixed_count}")
    print(f"   Already good: {total_count - fixed_count}")

    if fixed_count > 0:
        print("\n✅ All blog posts have been updated with consistent improvements!")
        print("   - Removed inconsistent header-right sections")
        print("   - Added ARIA labels for accessibility")
        print("   - Updated social sharing buttons")
        print("   - Fixed JavaScript functionality")
    else:
        print("\nℹ️  All posts were already up to date!")

if __name__ == "__main__":
    main()

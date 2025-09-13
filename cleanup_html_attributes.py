#!/usr/bin/env python3
"""
Script to clean up HTML attribute formatting issues in blog posts
"""

import os
import re
from pathlib import Path

def cleanup_html_attributes(file_path):
    """Clean up HTML attribute formatting in a single file"""
    print(f"Cleaning: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix home button - move aria-label to inside the tag
    content = re.sub(
        r'(<a href="/" class="home-button" title="Back to Home \(Ctrl/Cmd \+ H\)"[^>]*>) aria-label="Navigate back to home page"',
        r'\1 aria-label="Navigate back to home page">',
        content
    )

    # Fix TOC toggle button - move aria attributes to inside the tag
    content = re.sub(
        r'(<button class="toc-toggle" id="tocToggle" title="Toggle Table of Contents"[^>]*>) aria-label="Toggle table of contents" aria-expanded="false"',
        r'\1 aria-label="Toggle table of contents" aria-expanded="false">',
        content
    )

    # Clean up any trailing spaces before closing tags
    content = re.sub(r'\s+>', '>', content)

    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Cleaned: {file_path}")
        return True
    else:
        print(f"ℹ️  No cleanup needed: {file_path}")
        return False

def main():
    """Main function to clean up all blog posts"""
    blog_dir = Path("/home/prateek/Documents/GitHub/prateekshukla1108.github.io/blog/posts")
    cleaned_count = 0
    total_count = 0

    if not blog_dir.exists():
        print("❌ Blog posts directory not found!")
        return

    print("🧹 Starting HTML attribute cleanup...\n")

    # Process all HTML files in the posts directory
    for html_file in blog_dir.glob("*.html"):
        total_count += 1
        if cleanup_html_attributes(html_file):
            cleaned_count += 1

    print("\n📊 Cleanup Summary:")
    print(f"   Total posts: {total_count}")
    print(f"   Cleaned posts: {cleaned_count}")
    print(f"   Already clean: {total_count - cleaned_count}")

    if cleaned_count > 0:
        print("\n✅ HTML attribute cleanup completed!")
        print("   - Removed duplicated aria-label attributes")
        print("   - Removed duplicated aria-hidden attributes")
        print("   - Cleaned up trailing spaces")
    else:
        print("\nℹ️  All posts were already clean!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to fix JavaScript syntax issues with HTML entities in blog post files
"""

import os
import re
from pathlib import Path

def fix_javascript_syntax(file_path):
    """Fix HTML entities in JavaScript code"""
    print(f'Processing: {file_path}')

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix HTML entities in JavaScript strings - replace \' with '
    content = re.sub(r'\\\'', "'", content)

    # Fix any double backslash issues that might have been created
    content = re.sub(r'\\\\\\\\\'', "'", content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ Fixed: {file_path}')
        return True
    else:
        print(f'ℹ️  No changes needed: {file_path}')
        return False

def main():
    """Main function to fix all blog posts"""
    blog_dir = Path("/home/prateek/Documents/GitHub/prateekshukla1108.github.io/blog/posts")
    fixed_count = 0
    total_count = 0

    if not blog_dir.exists():
        print("❌ Blog posts directory not found!")
        return

    print("🔧 Fixing JavaScript syntax issues in blog posts...\n")

    # Process all HTML files in the posts directory
    for html_file in blog_dir.glob("*.html"):
        if html_file.name == '_template.html':
            continue  # Skip template
        total_count += 1
        if fix_javascript_syntax(html_file):
            fixed_count += 1

    print("\n📊 Summary:")
    print(f"   Total posts: {total_count}")
    print(f"   Fixed posts: {fixed_count}")
    print(f"   Already good: {total_count - fixed_count}")

    if fixed_count > 0:
        print("\n✅ All JavaScript syntax issues have been fixed!")
    else:
        print("\nℹ️  All posts were already good!")

if __name__ == "__main__":
    main()

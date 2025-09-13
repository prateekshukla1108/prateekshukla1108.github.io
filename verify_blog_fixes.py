#!/usr/bin/env python3
"""
Script to verify that all blog posts have been properly fixed
"""

import os
import re
from pathlib import Path

def verify_blog_post(file_path):
    """Verify that a blog post has all the required fixes"""
    print(f"Verifying: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Check for header-right section (should be removed)
    if 'header-right' in content:
        issues.append("❌ Header-right section still present")

    # Check for proper aria-label on home button
    if 'aria-label="Navigate back to home page"' not in content:
        issues.append("❌ Home button missing proper aria-label")

    # Check for proper aria-label on TOC toggle
    if 'aria-label="Toggle table of contents"' not in content:
        issues.append("❌ TOC toggle missing proper aria-label")

    # Check for aria-expanded on TOC toggle
    if 'aria-expanded="false"' not in content:
        issues.append("❌ TOC toggle missing aria-expanded")

    # Check for aria-hidden on icons
    if 'aria-hidden="true"' not in content:
        issues.append("❌ Icons missing aria-hidden attributes")

    # Check for social sharing ARIA labels
    if 'aria-label="Share on Twitter"' not in content:
        issues.append("❌ Twitter share missing aria-label")

    if 'aria-label="Share on LinkedIn"' not in content:
        issues.append("❌ LinkedIn share missing aria-label")

    if 'aria-label="Copy link to clipboard"' not in content:
        issues.append("❌ Copy link missing aria-label")

    # Check JavaScript TOC functionality
    if 'tocToggle.setAttribute' not in content:
        issues.append("❌ TOC JavaScript missing aria-expanded update")

    if issues:
        print("   " + "\n   ".join(issues))
        return False
    else:
        print("   ✅ All fixes verified!")
        return True

def main():
    """Main function to verify all blog posts"""
    blog_dir = Path("/home/prateek/Documents/GitHub/prateekshukla1108.github.io/blog/posts")
    verified_count = 0
    total_count = 0

    if not blog_dir.exists():
        print("❌ Blog posts directory not found!")
        return

    print("🔍 Starting verification of all blog posts...\n")

    # Process all HTML files in the posts directory
    for html_file in blog_dir.glob("*.html"):
        total_count += 1
        if verify_blog_post(html_file):
            verified_count += 1

    print("\n📊 Verification Summary:")
    print(f"   Total posts: {total_count}")
    print(f"   Properly fixed: {verified_count}")
    print(f"   Need fixes: {total_count - verified_count}")

    if verified_count == total_count:
        print("\n🎉 All blog posts have been successfully fixed and verified!")
        print("   - Removed inconsistent header-right sections")
        print("   - Added proper ARIA labels for accessibility")
        print("   - Updated social sharing buttons")
        print("   - Fixed JavaScript functionality")
        print("   - Improved HTML attribute formatting")
    else:
        print("\n⚠️  Some posts still need fixes. Please run the fix scripts again.")

if __name__ == "__main__":
    main()

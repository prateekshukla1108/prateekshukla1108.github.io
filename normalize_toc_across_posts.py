#!/usr/bin/env python3
"""
Normalize blog post HTML to ensure consistent Home button + TOC toggle header
and standard TOC aside markup, removing any inline styles that could override
CSS sticky behavior.

Idempotent and safe to re-run.
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "blog" / "posts"

# Match the header-left block (home button + toc toggle)
HEADER_LEFT_PATTERN = re.compile(
    r"<div class=\"header-left\">[\s\S]*?<\/div>", re.IGNORECASE
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

# Match the TOC aside block
ASIDE_TOC_PATTERN = re.compile(
    r"<aside class=\"toc\">[\s\S]*?<\/aside>", re.IGNORECASE
)

EXPECTED_ASIDE_TOC = (
    '      <aside class="toc">\n'
    '        <h3>On this page</h3>\n'
    '        <ul id="tocList"></ul>\n'
    '      </aside>'
)

# Remove inline style attributes that can break sticky positioning
INLINE_TOC_STYLE = re.compile(r"<aside class=\"toc\"[^>]*style=\"[^\"]*\"", re.IGNORECASE)
INLINE_HOME_STYLE = re.compile(r"<a href=\"/\" class=\"home-button\"[^>]*style=\"[^\"]*\"", re.IGNORECASE)


def normalize_post_html(content: str) -> str:
    original = content

    # Normalize header-left block
    content = re.sub(HEADER_LEFT_PATTERN, EXPECTED_HEADER_LEFT, content)

    # Normalize TOC aside block
    content = re.sub(ASIDE_TOC_PATTERN, EXPECTED_ASIDE_TOC, content)

    # Strip inline styles on TOC and home button
    content = re.sub(INLINE_TOC_STYLE, '<aside class="toc"', content)
    content = re.sub(INLINE_HOME_STYLE, '<a href="/" class="home-button"', content)

    return content


def main() -> None:
    if not POSTS_DIR.exists():
        print(f"❌ Posts directory not found: {POSTS_DIR}")
        return

    changed = 0
    total = 0
    for path in sorted(POSTS_DIR.glob("*.html")):
        total += 1
        text = path.read_text(encoding="utf-8")
        fixed = normalize_post_html(text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            changed += 1
            print(f"✅ Normalized: {path}")
        else:
            print(f"ℹ️  No change:  {path}")

    print("\n📊 Normalization Summary:")
    print(f"   Total posts scanned: {total}")
    print(f"   Files updated:       {changed}")
    print(f"   Unchanged:           {total - changed}")


if __name__ == "__main__":
    main()



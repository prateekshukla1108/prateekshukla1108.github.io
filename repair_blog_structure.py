#!/usr/bin/env python3
"""
Repair malformed HTML structure across blog posts:
- Fix lines that contain only `/div` into proper `</div>`
- Fix malformed <i> tags like `<i ...>"` by converting to a proper closing tag `</i>`
- Optionally normalize some spacing artifacts

This script is idempotent and safe to run multiple times.
"""
import re
from pathlib import Path

POSTS_DIR = Path(__file__).parent / "blog" / "posts"

# Regexes
ONLY_SLASH_DIV_LINE = re.compile(r"^\s*/div\s*$", re.MULTILINE)
MALFORMED_I_TAG = re.compile(r"(<i[^>]*?)">")  # matches <i ...>" (quote then end)

# Some files may use self-closing-like mistakes such as <i ...>"\n or <i ...>"\r\n

def repair_content(content: str) -> str:
    original = content

    # 1) Fix lines that are exactly '/div' (possibly with surrounding whitespace)
    content = ONLY_SLASH_DIV_LINE.sub("</div>", content)

    # 2) Fix malformed <i> tags that have stray '"' instead of a closing </i>
    #    e.g., <i class="fab fa-twitter" aria-hidden="true">"
    content = MALFORMED_I_TAG.sub(r"\1"></i>", content)

    # 3) Normalize any accidental '</div\n' constructs (extra whitespace before >)
    content = re.sub(r"</div\s*>", "</div>", content)

    return content if content != original else original


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fixed = repair_content(text)
    if fixed != text:
        path.write_text(fixed, encoding="utf-8")
        print(f"✅ Fixed: {path}")
        return True
    else:
        print(f"ℹ️  No changes needed: {path}")
        return False


def main():
    if not POSTS_DIR.exists():
        print(f"❌ Posts directory not found: {POSTS_DIR}")
        return

    print("🚀 Repairing malformed HTML in blog posts...\n")
    total = 0
    changed = 0
    for html_file in sorted(POSTS_DIR.glob("*.html")):
        total += 1
        if process_file(html_file):
            changed += 1

    print("\n📊 Repair Summary:")
    print(f"   Total posts scanned: {total}")
    print(f"   Files updated:       {changed}")
    print(f"   Unchanged:           {total - changed}")
    print("\nDone.")


if __name__ == "__main__":
    main()

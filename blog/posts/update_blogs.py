#!/usr/bin/env python3
"""
Script to update all blog posts with FontAwesome icons instead of inline SVG
"""
import os
import re

# List of files to update (excluding AGI.html which is already done and Career.html which we just did)
files_to_update = [
    "Avoid Burnout.html",
    "Decisions.html",
    "Existential Crisis.html",
    "Free-Spirit.html",
    "Heidegger's Being.html",
    "Imposter Syndrome.html",
    "Setting up WSL and Python.html",
    "Test of Independence.html",
    "camus.html",
    "suckless linux.html"
]

script_dir = os.path.dirname(os.path.abspath(__file__))

for filename in files_to_update:
    filepath = os.path.join(script_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Skipping {filename} - file not found")
        continue
    
    print(f"Processing {filename}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add FontAwesome CDN link if not present
    if 'font-awesome' not in content:
        content = content.replace(
            '  <link rel="stylesheet" href="/blog/styles.css">\n</head>',
            '  <link rel="stylesheet" href="/blog/styles.css">\n  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">\n</head>'
        )
    
    # Remove SVG icon definitions
    svg_pattern = r'  <!-- SVG Icon Definitions -->.*?</svg>\n\n'
    content = re.sub(svg_pattern, '', content, flags=re.DOTALL)
    
    # Replace SVG icon usage in home button and TOC toggle
    content = re.sub(
        r'<svg width="20" height="20" aria-hidden="true"><use href="#icon-home"></use></svg>',
        '<i class="fas fa-home" aria-hidden="true"></i>',
        content
    )
    content = re.sub(
        r'<svg width="20" height="20" aria-hidden="true"><use href="#icon-list"></use></svg>',
        '<i class="fas fa-list" aria-hidden="true"></i>',
        content
    )
    
    # Replace SVG icon usage in meta section
    content = re.sub(
        r'<svg width="14" height="14" aria-hidden="true"><use href="#icon-calendar"></use></svg>',
        '<i class="far fa-calendar"></i>',
        content
    )
    content = re.sub(
        r'<svg width="14" height="14" aria-hidden="true"><use href="#icon-user"></use></svg>',
        '<i class="far fa-user"></i>',
        content
    )
    content = re.sub(
        r'<svg width="14" height="14" aria-hidden="true"><use href="#icon-clock"></use></svg>',
        '<i class="far fa-clock"></i>',
        content
    )
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {filename}")

print("\nAll files processed!")

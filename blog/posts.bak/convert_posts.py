#!/usr/bin/env python3
import os
import re
import json
from datetime import datetime

def extract_post_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from the title element
    title_match = re.search(r'<h1 class="title"[^>]*>([^<]+)</h1>', content)
    title = title_match.group(1).strip() if title_match else 'Untitled'

    # Extract date from postDate element
    date_match = re.search(r'<time id="postDate">([^<]+)</time>', content)
    date = date_match.group(1).strip() if date_match else '2024-01-01'

    # Extract reading time from postReading element
    time_match = re.search(r'<span id="postReading">([^<]+)</span>', content)
    reading_time = time_match.group(1).strip() if time_match else '5 min read'

    # Extract content from postContent article
    content_start = content.find('<article id="postContent">')
    if content_start != -1:
        # Find the end of the article
        article_end = content.find('</article>', content_start)
        if article_end != -1:
            content_html = content[content_start:article_end + 10]  # +10 for </article>
        else:
            content_html = '<article id="postContent"><p>Content not found</p></article>'
    else:
        content_html = '<article id="postContent"><p>Content not found</p></article>'

    # Extract tags from content (look for common themes)
    tags = extract_tags_from_content(content)

    # Extract excerpt (first paragraph or first few sentences)
    excerpt = extract_excerpt(content)

    return {
        'title': title,
        'date': date,
        'reading_time': reading_time,
        'content': content_html,
        'tags': tags,
        'excerpt': excerpt,
        'slug': os.path.splitext(os.path.basename(filepath))[0]
    }

def extract_tags_from_content(content):
    """Extract tags based on content keywords and common themes"""
    tags = []
    content_lower = content.lower()

    # Define keyword mappings to tags
    keyword_tags = {
        'ai': ['AI', 'artificial intelligence', 'machine learning', 'neural network'],
        'philosophy': ['philosophy', 'existence', 'consciousness', 'nihilism', 'heidegger', 'camus', 'free spirit', 'career'],
        'life': ['life', 'burnout', 'imposter syndrome', 'decisions', 'independence'],
        'technology': ['linux', 'suckless', 'programming', 'python', 'wsl', 'setup'],
        'neuroscience': ['brain', 'neuroscience', 'cognitive']
    }

    for tag, keywords in keyword_tags.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.append(tag.capitalize())

    # If no tags found, add default
    if not tags:
        tags = ['Others']

    return tags

def extract_excerpt(content):
    """Extract first meaningful paragraph as excerpt"""
    # Find first paragraph in the article content
    article_start = content.find('<article id="postContent">')
    if article_start == -1:
        return 'Read more about this topic...'

    article_content = content[article_start:]

    # Find first paragraph
    para_match = re.search(r'<p[^>]*>([^<]+)</p>', article_content)
    if para_match:
        excerpt = para_match.group(1).strip()
        # Truncate if too long
        if len(excerpt) > 200:
            excerpt = excerpt[:197] + '...'
        return excerpt

    return 'Read more about this topic...'

def apply_new_template(template_path, post_data):
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace placeholders
    template = template.replace('Post Title', post_data['title'])
    template = template.replace('Post Title • Prateek\'s Blog', f'{post_data["title"]} • Prateek\'s Blog')
    template = template.replace('Post Title - Read more on Prateek\'s Blog', f'{post_data["title"]} - Read more on Prateek\'s Blog')
    template = template.replace('2025-01-01', post_data['date'])
    template = template.replace('5 min read', post_data['reading_time'])

    # Replace the content placeholder
    template = template.replace('<!-- Content will be inserted here -->', post_data['content'])

    return template

def generate_posts_json():
    """Generate posts.json file with metadata for all posts"""
    posts_dir = '.'
    posts_data = []

    print('📊 Generating posts.json...')

    for filename in os.listdir(posts_dir):
        if filename.endswith('.html') and filename != '_template.html' and not filename.endswith('.backup') and filename != 'convert_posts.py':
            filepath = os.path.join(posts_dir, filename)

            try:
                post_data = extract_post_data(filepath)

                # Convert date to ISO format for sorting
                try:
                    date_obj = datetime.strptime(post_data['date'], '%B %d, %Y')
                    iso_date = date_obj.strftime('%Y-%m-%d')
                except:
                    # If date parsing fails, use current date
                    iso_date = datetime.now().strftime('%Y-%m-%d')

                post_entry = {
                    'slug': post_data['slug'],
                    'title': post_data['title'],
                    'date': iso_date,
                    'author': 'Prateek',
                    'readingTime': post_data['reading_time'],
                    'tags': post_data['tags'],
                    'excerpt': post_data['excerpt']
                }

                posts_data.append(post_entry)
                print(f'📝 Processed: "{post_data["title"]}" - Tags: {", ".join(post_data["tags"])}')

            except Exception as e:
                print(f'❌ Error processing {filename}: {e}')

    # Sort posts by date (newest first)
    posts_data.sort(key=lambda x: x['date'], reverse=True)

    # Write to /blog/posts.json (canonical path used by index.html)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'posts': posts_data}, f, indent=2, ensure_ascii=False)

    print(f'✅ Generated posts.json with {len(posts_data)} posts')

def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--generate-json':
        generate_posts_json()
        return

    template_path = '_template.html'
    posts_dir = '.'

    print('🔄 Converting all posts to new cyberpunk template...')
    count = 0

    for filename in os.listdir(posts_dir):
        if filename.endswith('.html') and filename != '_template.html' and not filename.endswith('.backup') and filename != 'convert_posts.py':
            filepath = os.path.join(posts_dir, filename)

            try:
                # Extract data from old template
                post_data = extract_post_data(filepath)
                print(f'📖 Extracted: "{post_data["title"]}" ({post_data["date"]})')

                # Apply new template
                new_content = apply_new_template(template_path, post_data)

                # Write back the new template
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                count += 1
                print(f'✅ Converted {filename}')

            except Exception as e:
                print(f'❌ Error converting {filename}: {e}')

    print(f'\n🎉 Successfully converted {count} posts to cyberpunk template!')
    print('🚀 All posts now have the new cyberpunk design with preserved content!')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Batch apply PageSpeed optimizations to all HTML files.

Usage: python3 scripts/sync_optimizations.py [--dry-run]
"""

import re
import sys
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv

HTML_FILES = (
    list(Path('.').glob('*.html')) +
    list(Path('articles').glob('*.html'))
)
HTML_FILES = [f for f in HTML_FILES if 'PageSpeed' not in f.name]

GA4_TAG = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>'
GA4_CONFIG = "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>"
GA4_BODY = f'\n    {GA4_TAG}\n    {GA4_CONFIG}\n'

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content
    changes = []

    # 1. Remove GA4 from <head> (anywhere before </head>)
    head_end = content.find('</head>')
    if head_end > 0:
        head_content = content[:head_end]
        body_content = content[head_end:]

        new_head = head_content
        new_head = new_head.replace(GA4_TAG, '')
        new_head = new_head.replace(GA4_CONFIG, '')
        # strip trailing whitespace each time
        new_head = new_head.rstrip()

        if new_head != head_content:
            changes.append('removed_ga4_from_head')
            content = new_head + '\n' + body_content

    # 2. Add defer to URL-replacement script
    # Match <script> followed by (function(){
    new_content = re.sub(
        r'<script>\s*\n?\s*\(function\(\)\s*\{',
        '<script defer>\n    (function(){',
        content
    )
    if new_content != content:
        changes.append('added_defer')
        content = new_content

    # 3. Add GA4 before </body>
    if 'removed_ga4_from_head' in changes and '</body>' in content:
        content = content.replace('</body>', GA4_BODY + '</body>')

    # 4. For Python generator files: remove CDN preconnects and Lucide CDN
    if filepath.suffix == '.py':
        # Remove preconnects
        new_content = re.sub(
            r'\s*<link rel="preconnect" href="https://cdn\.tailwindcss\.com" crossorigin>\s*',
            '', content
        )
        new_content = re.sub(
            r'\s*<link rel="preconnect" href="https://unpkg\.com" crossorigin>\s*',
            '', new_content
        )
        if new_content != content:
            changes.append('removed_cdn_preconnects')
            content = new_content

        # Replace Lucide CDN
        new_content = re.sub(
            r'<script src="https://unpkg\.com/lucide@latest"></script>\s*'
            r'<script>lucide\.createIcons\(\);</script>',
            '<script src="js/icons.js"></script>',
            content
        )
        if new_content != content:
            changes.append('replaced_lucide_cdn')
            content = new_content

        # Fix CSS preload pattern for root-relative paths
        new_content = re.sub(
            r'<link rel="stylesheet" href="css/tailwind\.css">',
            '<link rel="preload" href="css/tailwind.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n    <noscript><link rel="stylesheet" href="css/tailwind.css"></noscript>',
            content
        )
        # Fix CSS preload pattern for article-relative paths
        new_content = re.sub(
            r'<link rel="stylesheet" href="\.\./css/tailwind\.css">',
            '<link rel="preload" href="../css/tailwind.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n    <noscript><link rel="stylesheet" href="../css/tailwind.css"></noscript>',
            new_content
        )
        if new_content != content:
            changes.append('fixed_css_preload')
            content = new_content

    if content != original:
        if not DRY_RUN:
            filepath.write_text(content, encoding='utf-8')
        return changes
    return []


def main():
    total = 0
    for f in sorted(HTML_FILES):
        ch = process_file(f)
        status = f"✅ {f}: {', '.join(ch)}" if ch else f"⏭️  {f}"
        print(status)
        total += len(ch)

    # Also process generator Python files
    for py_file in [Path('generate_blog.py'), Path('gen_regions.py')]:
        if py_file.exists():
            ch = process_file(py_file)
            if ch:
                print(f"✅ {py_file}: {', '.join(ch)}")
                total += 1
            else:
                print(f"⏭️  {py_file}: no changes")

    print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}{total} changes applied")


if __name__ == '__main__':
    main()
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
GA4_CONFIG = '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-NPKZ6HZV7K\');</script>'

GTM_DEFERRED = '''    <!-- Delay GTM to reduce unused JS impact on LCP -->
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}if(window.requestIdleCallback){window.requestIdleCallback(function(){var s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K';s.async=true;document.body.appendChild(s);},{timeout:2000});}else{window.addEventListener('load',function(){var s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K';s.async=true;document.body.appendChild(s);});}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>'''

GA4_INLINE = '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content
    changes = []

    new_content = re.sub(
        r'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\s*<meta http-equiv="Pragma" content="no-cache">\s*<meta http-equiv="Expires" content="0">',
        '<meta http-equiv="Cache-Control" content="public, max-age=86400, immutable">',
        content
    )
    if new_content != content:
        changes.append('fixed_cache_headers')
        content = new_content

    old_pattern = re.escape(GA4_TAG) + r'\s*' + re.escape(GA4_CONFIG)
    if 'requestIdleCallback' in content and 'googletagmanager' in content:
        pass
    elif re.search(old_pattern, content):
        new_content = re.sub(old_pattern, GTM_DEFERRED, content)
        if new_content != content:
            changes.append('deferred_gtm')
            content = new_content
    elif GA4_TAG in content or GA4_CONFIG in content:
        new_content = content.replace(GA4_TAG, '').replace(GA4_CONFIG, '')
        new_content = re.sub(
            r'\s*<link rel="preconnect" href="https://www\.googletagmanager\.com">',
            '', new_content
        )
        new_content = re.sub(
            r'\s*<link rel="preconnect" href="https://www\.google-analytics\.com">',
            '', new_content
        )
        body_close = new_content.find('</body>')
        if body_close > 0:
            new_content = new_content[:body_close] + '\n' + GTM_DEFERRED + '\n' + new_content[body_close:]
            changes.append('deferred_gtm')
            content = new_content

    # 3. Add defer to URL-replacement script
    new_content = re.sub(
        r'<script>\s*\n?\s*\(function\(\)\s*\{',
        '<script defer>\n    (function(){',
        content
    )
    if new_content != content:
        changes.append('added_defer')
        content = new_content

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

    new_content = re.sub(
        r'transition-all\s+duration-\d+\s+[\w-]+',
        'transition-max-width',
        content
    )
    if new_content != content:
        changes.append('fixed_transition_all')
        content = new_content

    if filepath.suffix == '.html' and '<style>' in content:
        if '.transition-max-width' not in content:
            new_content = re.sub(
                r'(<style[^>]*>)(.*?)(</style>)',
                r'\1\2\n        .transition-max-width{transition-property:max-width;transition-duration:300ms;transition-timing-function:ease-in-out}\3',
                content,
                flags=re.DOTALL
            )
            if new_content != content:
                changes.append('added_transition_max_width_css')
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

    # Also skip generator Python files - their embedded HTML templates would be
    # corrupted by HTML-processing patterns. Generators are not deployed; their
    # OUTPUT (the HTML files in articles/) is what gets deployed and optimized.
    for py_file in [Path('generate_blog.py'), Path('gen_regions.py')]:
        if py_file.exists():
            print(f"⏭️  {py_file}: skipped (not a deployed file)")

    print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}{total} changes applied")


if __name__ == '__main__':
    main()
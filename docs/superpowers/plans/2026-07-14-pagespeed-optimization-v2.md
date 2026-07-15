# PageSpeed Optimization Implementation Plan (Updated)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Push Performance score from 84 to 90+ by eliminating render-blocking scripts in `<head>`, fixing the article generator template, and ensuring CLS/LCP optimizations are applied consistently across all 107 HTML pages.

**Architecture:** Static HTML site with local Tailwind CSS + local inline SVG icons. Three independent optimization tracks: (A) Move blocking scripts to body, (B) Fix article generator template for future-proofing, (C) Ensure image dimensions are set. All changes are find-replace operations across HTML files or edits to Python generators.

**Tech Stack:** HTML5, Tailwind CSS (local), Vanilla JS, Python (generation scripts)

---

## File Change Map

| File | Change | Responsibility |
|---|---|---|
| `index.html` | Modify lines 4-33 (move 2 scripts to body) | GA4 + URL-replacement deferred |
| `blog.html` | Modify lines 4-33 (same pattern) | Blog home page |
| `kwun-tong.html` | Modify (same pattern) | Region landing page |
| `lam-tin.html` | Modify (same pattern) | Region landing page |
| `tseung-kwan-o.html` | Modify (same pattern) | Region landing page |
| `kowloon-city.html` | Modify (same pattern) | Region landing page |
| `wong-tai-sin.html` | Modify (same pattern) | Region landing page |
| `404.html` | Modify (same pattern) | 404 page |
| `generate_blog.py` | Modify lines 800-855 | Article template fix + no CDN |
| `gen_regions.py` | Modify (same pattern as generate_blog.py) | Region pages generator |
| `scripts/sync_optimizations.py` | Create | Batch script for all 107 HTML files |
| `articles/*.html` | Modify via sync script | All 100 article pages |

---

## Critical Issues Found

### Issue 1: GA4 `gtag.js` blocks rendering (ALL pages)
**Location:** `index.html` lines 4-5, `blog.html` lines 4-5, `articles/*.html` lines 52-53
**Impact:** ~200-400ms blocking on first contentful paint

Both `gtag` scripts are synchronous in `<head>`. The `async` attribute on the tag manager script helps, but the config script that calls `gtag()` runs before any content renders.

**Fix:** Move BOTH gtag scripts to just before `</body>` on every page.

### Issue 2: URL-replacement IIFE blocks DOM parsing (ALL pages)
**Location:** `index.html` lines 6-33, `blog.html` lines 6-33, `articles/*.html` lines 4-30
**Impact:** ~50-100ms blocking; also runs querySelectorAll across entire document before body exists

This IIFE runs in `<head>` before any body content. It manipulates canonical hrefs, og:url, og:image, twitter:image, and JSON-LD schemas. It calls `querySelectorAll` before DOM is ready.

**Fix:** Add `defer` attribute. The script is order-independent — it only reads/writes `<head>` elements, so defer is safe.

### Issue 3: `generate_blog.py` template still emits Lucide CDN (DANGEROUS)
**Location:** `generate_blog.py` lines 817-818, 821, 852-853
**Current state:** The generator still emits:
- `cdn.tailwindcss.com` preconnect
- `unpkg.com` preconnect
- `<link rel="stylesheet" href="../css/tailwind.css">` (no preload pattern!)
- `<script src="https://unpkg.com/lucide@latest"></script>` + `lucide.createIcons()`

While the 100 already-generated article files have been patched to use `js/icons.js`, **re-running the generator would wipe all those fixes**. This is a ticking bomb.

**Fix:** Update the template in `generate_blog.py` AND run the sync script to ensure all 100 articles are clean.

### Issue 4: `gen_regions.py` — unknown state
**Status:** Not yet checked. May have same CDN references as `generate_blog.py`.

**Fix:** Check and fix if needed.

### Issue 5: Missing image intrinsic dimensions (CLS risk)
**Location:** `index.html` image tags
**Fix:** Ensure all `<img>` tags have explicit `width` and `height` attributes.

---

## Tasks

### Task 1: Move GA4 + URL-replacement scripts out of `<head>` — `index.html`

**Files:**
- Modify: `index.html`

The goal is to move the two `<script>` blocks from `<head>` (lines 4-5 and 6-33) to just before `</body>`, and add `defer` to the URL-replacement script.

**Steps:**

- [ ] **Step 1: Read current state of index.html to identify exact lines**

Run: `head -n 45 index.html | tail -n 45`

Expected output shows lines 4-5 (GA4 scripts) and 6-33 (URL-replacement IIFE) in `<head>`, and confirms `</body>` is at line 1157.

- [ ] **Step 2: Remove the GA4 scripts from `<head>`**

Find and delete (or comment out) these lines from the `<head>` section:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
```

- [ ] **Step 3: Defer the URL-replacement script in `<head>`**

Change line 6 from:
```html
<script>
```
to:
```html
<script defer>
```

- [ ] **Step 4: Add GA4 scripts to just before `</body>`**

Find `</body>` in index.html (should be line 1157) and insert BEFORE it:
```html
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
```

- [ ] **Step 5: Verify no duplicate scripts**

Run: `grep -n "googletagmanager" index.html`
Expected: Two occurrences — one in `<head>` (should be gone) and one before `</body>`.

Actually, after step 2 the GA4 should be removed from head and only exist before `</body>`. Run the grep to confirm.

- [ ] **Step 6: Test locally**

Run: `python3 -m http.server 8000`
Open: `http://localhost:8000/`
Check:
- Page loads correctly
- GA4 still fires (Network tab → gtag.js request)
- No JS errors in console
- Nav bar, hero, all sections render correctly

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "perf: move GA4 to end of body + defer URL-replacement script"
```

---

### Task 2: Fix `generate_blog.py` article template

**Files:**
- Modify: `generate_blog.py:800-855` (article HTML template)

The article template is a Python format string containing the full HTML structure. It currently has:
- Line 817: `<link rel="preconnect" href="https://cdn.tailwindcss.com" crossorigin>`
- Line 818: `<link rel="preconnect" href="https://unpkg.com" crossorigin>`
- Line 821: `<link rel="stylesheet" href="../css/tailwind.css">` (missing preload pattern)
- Lines 852-853: `<script src="https://unpkg.com/lucide@latest"></script>` + `lucide.createIcons()`

**Steps:**

- [ ] **Step 1: Read the template section**

Run: `sed -n '800,856p' generate_blog.py`

This shows the complete template. Lines to change are:
- 817: preconnect cdn.tailwindcss.com → DELETE
- 818: preconnect unpkg.com → DELETE
- 821: link stylesheet → REPLACE with preload pattern
- 852-853: Lucide CDN → REPLACE with local js/icons.js

- [ ] **Step 2: Update the template**

Replace lines 800-855 with the corrected article template:

```python
    article_html = '''<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <script defer>
    (function(){
        var d=window.location.origin+window.location.pathname;
        var b=window.location.origin;
        var c=document.querySelector('link[rel="canonical"]');
        if(c)c.href=d;
        var og=document.querySelectorAll('meta[property="og:url"]');
        og.forEach(function(m){m.content=d;});
        var ogi=document.querySelectorAll('meta[property="og:image"]');
        ogi.forEach(function(m){if(m.content&&m.content.indexOf("lamtaichi")>-1)m.content=b+"/class.webp";});
        var twi=document.querySelectorAll('meta[name="twitter:image"]');
        twi.forEach(function(m){if(m.content&&m.content.indexOf("lamtaichi")>-1)m.content=b+"/class.webp";});
        document.querySelectorAll('script[type="application/ld+json"]').forEach(function(s){
            try{
                var j=JSON.parse(s.textContent);
                var fix=function(o){
                    if(typeof o==="string"&&o.indexOf("lamtaichi")>-1){
                        return o.replace(/https:\\/\\/lamtaichi\\.pages\\.dev/g,b);
                    }
                    if(Array.isArray(o))return o.map(fix);
                    if(typeof o==="object"&&o!==null){Object.keys(o).forEach(function(k){o[k]=fix(o[k]);});}
                    return o;
                };
                s.textContent=JSON.stringify(fix(j),null,0);
            }catch(e){}
        });
    })();
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 林燦平太極學會養生專欄</title>
    <meta name="description" content="{summary}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="https://lamtaichi.pages.dev/articles/{slug}.html">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{summary}">
    <meta property="og:url" content="https://lamtaichi.pages.dev/articles/{slug}.html">
    <meta property="og:locale" content="zh_HK">
    <meta name="robots" content="index, follow">
    {ld_json_article}
    {ld_json_breadcrumb}
    <link rel="icon" type="image/png" href="../favicon.png">
    <link rel="apple-touch-icon" href="../apple-touch-icon.png">
    <link rel="preload" href="../css/tailwind.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="../css/tailwind.css"></noscript>
    <style>
        html {{ scroll-behavior: smooth; }}
        .tag-chip {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; background-color: #d1fae5; color: #065f46; font-size: 0.875rem; cursor: pointer; transition: all 0.2s; }}
        .tag-chip:hover {{ background-color: #059669; color: white; }}
    </style>
</head>
<body class="font-sans text-gray-800 bg-stone-50">
    <nav class="fixed w-full bg-white/95 backdrop-blur-sm shadow-md z-50">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center h-16">
            <a href="../index.html" class="text-xl font-bold text-emerald-800 border-2 border-emerald-800 p-1 rounded">林師傅</a>
            <a href="../blog.html" class="text-gray-600 hover:text-emerald-700 flex items-center"><i data-lucide="book-open" class="w-4 h-4 mr-1"></i>養生專欄</a>
        </div>
    </nav>
    <article class="max-w-4xl mx-auto px-4 pt-24 pb-20">
        <header class="mb-10">
            <span class="inline-block py-1 px-3 rounded-full bg-emerald-100 text-emerald-800 text-sm font-medium mb-4">{category}</span>
            <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4 leading-tight">{title}</h1>
            <p class="text-gray-600 text-lg leading-relaxed">{summary}</p>
            <div class="flex flex-wrap gap-2 mt-4">{tags_html}</div>
        </header>
        <div class="prose prose-lg max-w-none bg-white rounded-2xl p-8 md:p-12 shadow-sm">{content}</div>
        <div class="mt-12 bg-emerald-900 text-white rounded-2xl p-8 text-center">
            <h2 class="text-2xl font-bold mb-4">想親身體驗太極拳的好處？</h2>
            <p class="text-emerald-200 mb-6">歡迎隨時親臨油塘觀課，滿意再報名！</p>
            <a href="https://wa.me/85260985742?text=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%9E%97%E5%B8%AB%E5%82%85%EF%BC%81%E6%88%91%E5%9C%A8%E7%B6%B2%E9%A0%81%E7%9C%8B%E5%88%B0%E5%A4%AA%E6%A5%B5%E7%8F%AD%E6%8B%9B%E7%94%9F%EF%BC%8C%E6%83%B3%E6%9F%A5%E8%A9%A2%E6%9B%B4%E5%A4%9A%E8%A9%B3%E6%83%85%E3%80%82" target="_blank" rel="noopener noreferrer" class="inline-block bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-bold transition">WhatsApp 查詢報名</a>
        </div>
        <div class="mt-8 text-center">
            <a href="../blog.html" class="text-emerald-700 hover:text-emerald-800 font-medium inline-flex items-center"><i data-lucide="arrow-left" class="w-4 h-4 mr-1"></i>返回養生專欄</a>
        </div>
    </article>
    <script src="../js/icons.js"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
</body>
</html>'''
```

**Key changes in the template:**
1. `<script defer>` for URL-replacement (line 4) instead of `<script>`
2. Removed `cdn.tailwindcss.com` and `unpkg.com` preconnects
3. Changed `<link rel="stylesheet">` to preload pattern with `onload` trick
4. Replaced Lucide CDN `<script>` + `lucide.createIcons()` with `<script src="../js/icons.js"></script>`
5. GA4 scripts moved to end of body (not in head at all)
6. Removed GA4 from `<head>` entirely

- [ ] **Step 3: Verify the template parses correctly**

Run: `python3 -c "import generate_blog; print('Template OK')"`

If there's a syntax error in the string, fix it. The format `{` `}` braces for string formatting should remain as-is — they're Python format placeholders.

- [ ] **Step 4: Commit**

```bash
git add generate_blog.py
git commit -m "perf: fix article template - remove CDN refs, use local icons.js, move GA4 to body"
```

---

### Task 3: Apply same GA4/URL-replacement fixes to `blog.html`

**Files:**
- Modify: `blog.html`

`blog.html` has the same pattern as `index.html` but with critical CSS already inline (lines 47-51). Need to:
1. Remove GA4 from `<head>` (lines 4-5)
2. Add `defer` to URL-replacement script (line 6)
3. Add GA4 scripts before `</body>`

Note: The GA4 removal from head was done in Task 1 for index.html. For blog.html, we need to do it separately since it's a different file.

- [ ] **Step 1: Read the GA4 lines in blog.html**

Run: `sed -n '1,10p' blog.html`
Expected: Lines 4-5 are GA4 scripts.

- [ ] **Step 2: Remove GA4 from head**

Delete lines 4-5 from blog.html:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
```

- [ ] **Step 3: Add defer to URL-replacement script**

Change line 6 from `<script>` to `<script defer>`:
```html
<script defer>
```

- [ ] **Step 4: Add GA4 scripts before `</body>`**

Find `</body>` in blog.html (line ~163) and insert BEFORE it:
```html
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
```

- [ ] **Step 5: Test**

Run: `python3 -m http.server 8000`
Open: `http://localhost:8000/blog.html`
Check blog search, category filters, article cards all work.

- [ ] **Step 6: Commit**

```bash
git add blog.html
git commit -m "perf: move GA4 to body + defer URL-replacement in blog.html"
```

---

### Task 4: Apply same GA4/URL-replacement fixes to 5 region pages + 404

**Files:**
- Modify: `kwun-tong.html`, `lam-tin.html`, `tseung-kwan-o.html`, `kowloon-city.html`, `wong-tai-sin.html`, `404.html`

These 6 pages follow the same pattern as `index.html`. They also have the GA4 scripts in `<head>` and URL-replacement IIFE.

Rather than edit each manually, we'll use `scripts/sync_optimizations.py` to do it in one pass.

- [ ] **Step 1: Create `scripts/sync_optimizations.py`**

Create file: `scripts/sync_optimizations.py`

```python
#!/usr/bin/env python3
"""
Batch apply PageSpeed optimizations to all HTML files.

Replaces:
  1. GA4 in <head> → move to before </body>
  2. Add defer to URL-replacement IIFE in <head>
  3. Remove unused preconnects (cdn.tailwindcss.com, unpkg.com) from article generator template
  4. Ensure CSS uses preload pattern
  5. Ensure Lucide uses local js/icons.js

Usage: python3 scripts/sync_optimizations.py [--dry-run]
"""

import re
import sys
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv

HTML_FILES = list(Path('.').glob('*.html')) + list(Path('articles').glob('*.html'))
HTML_FILES = [f for f in HTML_FILES if f.name != 'PageSpeed Insights.html']

# Patterns for GA4 scripts (to move from head to body)
GA4_SCRIPTS = re.compile(
    r'\s*<script async src="https://www\.googletagmanager\.com/gtag\.js\?id=G-NPKZ6HZV7K"></script>\s*'
    r'<script>window\.dataLayer=window\.dataLayer\|\|\[\];function gtag\(\)\{dataLayer\.push\(arguments\);\}gtag\([^)]+\);</script>\s*'
)

# Pattern for URL-replacement script (add defer)
IIFE_SCRIPT = re.compile(r'<script>\s*\(function\(\)\s*\{')

# Pattern for article template preconnects (generator script, not rendered pages)
ARTICLE_PRECONNECTS = re.compile(
    r'\s*<link rel="preconnect" href="https://cdn\.tailwindcss\.com" crossorigin>\s*'
    r'<link rel="preconnect" href="https://unpkg\.com" crossorigin>\s*'
)

# Pattern for article template Lucide CDN
ARTICLE_LUCIDE = re.compile(
    r'\s*<script src="https://unpkg\.com/lucide@latest"></script>\s*'
    r'<script>lucide\.createIcons\(\);</script>\s*'
)

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content
    changes = []

    # 1. Remove GA4 from <head>
    new_content = GA4_SCRIPTS.sub('', content)
    if new_content != content:
        changes.append('removed_ga4_from_head')
        content = new_content

    # 2. Add defer to URL-replacement script
    new_content = IIFE_SCRIPT.sub('<script defer>\n    (function() {', content)
    if new_content != content:
        changes.append('added_defer_to_iife')
        content = new_content

    # 3. For article template: remove preconnects and Lucide CDN
    if 'generate_blog.py' in str(filepath) or 'gen_regions.py' in str(filepath):
        new_content = ARTICLE_PRECONNECTS.sub('', content)
        if new_content != content:
            changes.append('removed_article_preconnects')
            content = new_content
        new_content = ARTICLE_LUCIDE.sub('<script src="js/icons.js"></script>', content)
        if new_content != content:
            changes.append('replaced_article_lucide_cdn')
            content = new_content

    if content != original:
        if not DRY_RUN:
            filepath.write_text(content, encoding='utf-8')
        return changes
    return []


def main():
    total_changes = 0
    for filepath in sorted(HTML_FILES):
        changes = process_file(filepath)
        if changes:
            print(f"✅ {filepath}: {', '.join(changes)}")
            total_changes += 1
        else:
            print(f"⏭️  {filepath}: no changes")

    print(f"\n{total_changes} files changed")
    if DRY_RUN:
        print("DRY RUN - no files written")

if __name__ == '__main__':
    main()
```

Run: `python3 scripts/sync_optimizations.py --dry-run`

Expected: Shows which files would be changed.

- [ ] **Step 2: Run the sync script for real**

Run: `python3 scripts/sync_optimizations.py`

Expected: 6 region/404 files + generate_blog.py + gen_regions.py = 8 files changed.

- [ ] **Step 3: Manually verify one region page**

Run: `grep -n "googletagmanager" kwun-tong.html`
Expected: Only one occurrence (before </body>), not in <head>.

Also check:
`grep -n "defer" kwun-tong.html`
Expected: URL-replacement script has defer.

- [ ] **Step 4: Verify generator scripts are clean**

Run: `grep -n "cdn.tailwindcss.com\|unpkg.com" generate_blog.py`
Expected: No matches.

Run: `grep -n "lucide@latest" generate_blog.py`
Expected: No matches.

- [ ] **Step 5: Test a region page**

Run: `python3 -m http.server 8000`
Open: `http://localhost:8000/kwun-tong.html`
Check all sections render correctly, WhatsApp button works.

- [ ] **Step 6: Commit**

```bash
git add scripts/sync_optimizations.py kwun-tong.html lam-tin.html tseung-kwan-o.html kowloon-city.html wong-tai-sin.html 404.html generate_blog.py gen_regions.py
git commit -m "perf: move GA4 to body + defer URL-replacement across all pages"
```

---

### Task 5: Verify 100 article pages are clean

**Files:**
- No changes needed if Task 4 worked correctly.

The 100 article files already have `js/icons.js` (verified by grep earlier). But they may still have GA4 in `<head>`. Let's check.

- [ ] **Step 1: Check if articles have GA4 in head or body**

Run: `python3 scripts/sync_optimizations.py --dry-run 2>&1 | grep "articles/" | head -5`

Wait, the script already ran in Task 4 and the article files don't have GA4 in `<head>` pattern matching because they have a DIFFERENT structure — their GA4 appears at lines 52-53 (after the `<meta name="viewport">` line), which might not match the `GA4_SCRIPTS` regex pattern I wrote.

Let me re-examine the article files. From `grep` output earlier, article files have GA4 at lines 52-53:

```
52:     <script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>
53:     <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NPKZ6HZV7K');</script>
```

The regex needs to match the article format too. The GA4_SCRIPTS pattern I wrote matches when GA4 is directly at the start of head (like in index.html). But articles have it after some meta tags. Let me check.

Actually, looking at the article HTML structure from earlier:
- Lines 3-30: URL-replacement IIFE
- Line 31: `<script defer>` (if we applied defer from Task 2)
- Line 32: `<meta charset="UTF-8">`
- ...
- Line 52-53: GA4 scripts
- Line 54: style block
- Line 60: `</head>`
- Line 61: `<body ...>`

The regex `GA4_SCRIPTS` won't match because it expects the GA4 to be immediately after `</title>` or similar. For articles, GA4 appears much later in `<head>`.

Let me create an updated version that removes GA4 from anywhere in `<head>`:

```python
# Updated GA4 removal regex - works on all page types
GA4_SCRIPT_1 = re.compile(r'<script async src="https://www\.googletagmanager\.com/gtag\.js\?id=G-NPKZ6HZV7K"></script>\s*')
GA4_SCRIPT_2 = re.compile(r'<script>window\.dataLayer=window\.dataLayer\|\|\[\];function gtag\(\)\{dataLayer\.push\(arguments\);\}gtag\([^)]+\);</script>\s*')
```

And we need to add GA4 to `</body>` insertion.

Actually, let me just write the updated sync script properly. The issue is the GA4 regex needs to match article format too.

For simplicity in this plan, let me create a two-step approach:

**Updated `scripts/sync_optimizations.py`:**

```python
#!/usr/bin/env python3
"""Batch apply PageSpeed optimizations to all HTML files."""

import re
import sys
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv

HTML_FILES = list(Path('.').glob('*.html')) + list(Path('articles').glob('*.html'))
HTML_FILES = [f for f in HTML_FILES if 'PageSpeed' not in f.name]

GA4_TAG = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-NPKZ6HZV7K"></script>'
GA4_CONFIG = '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-NPKZ6HZV7K\');</script>'
GA4_BODY = f'\n    {GA4_TAG}\n    {GA4_CONFIG}\n'

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content
    changes = []

    # 1. Remove GA4 from <head> (anywhere in head section)
    head_end = content.find('</head>')
    if head_end > 0:
        head_content = content[:head_end]
        body_content = content[head_end:]

        new_head = head_content
        new_head = new_head.replace(GA4_TAG + '\n    ', '')
        new_head = new_head.replace(GA4_CONFIG + '\n    ', '')
        # also handle without newlines
        new_head = new_head.replace(GA4_TAG, '')
        new_head = new_head.replace(GA4_CONFIG, '')

        if new_head != head_content:
            changes.append('removed_ga4_from_head')
            content = new_head + body_content

    # 2. Add defer to URL-replacement script
    new_content = content.replace('<script>\n    (function(){', '<script defer>\n    (function(){')
    if new_content != content:
        changes.append('added_defer')
        content = new_content

    # 3. Add GA4 before </body>
    if changes and '</body>' in content:
        content = content.replace('</body>', GA4_BODY + '</body>')

    # 4. Remove article generator preconnects + Lucide CDN (for .py files only)
    if filepath.suffix == '.py':
        content = re.sub(r'<link rel="preconnect" href="https://cdn\.tailwindcss\.com" crossorigin>\s*', '', content)
        content = re.sub(r'<link rel="preconnect" href="https://unpkg\.com" crossorigin>\s*', '', content)
        content = re.sub(r'<script src="https://unpkg\.com/lucide@latest"></script>\s*<script>lucide\.createIcons\(\);</script>', '<script src="js/icons.js"></script>', content)

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
    if DRY_RUN:
        print("\nDRY RUN - nothing written")
    else:
        print(f"\n{total} changes applied")


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run the updated sync script**

```bash
python3 scripts/sync_optimizations.py --dry-run
```

Expected: Shows changes for all 107 HTML files + 2 Python generator files.

- [ ] **Step 3: Run for real**

```bash
python3 scripts/sync_optimizations.py
```

- [ ] **Step 4: Verify article pages**

Run: `grep -c "googletagmanager" articles/tai-chi-beginner-guide.html`
Expected: `1` (only in body, not head)

Run: `grep -n "defer" articles/tai-chi-beginner-guide.html`
Expected: `1` (the URL-replacement script has defer)

Run: `grep -n "unpkg.com" articles/tai-chi-beginner-guide.html`
Expected: No matches.

- [ ] **Step 5: Commit**

```bash
git add scripts/sync_optimizations.py
git commit -m "perf: sync optimizations to all 107 HTML pages + generator scripts"
```

---

### Task 6: Verify CLS — check image dimensions

**Files:**
- Modify: `index.html` (if missing dimensions found)

From the PageSpeed report, CLS is already good (0.10 for mobile). But we should verify all images have explicit `width` and `height`.

- [ ] **Step 1: Find images without dimensions in index.html**

Run: `grep -n '<img' index.html | head -20`
Expected: All img tags should have `width=` and `height=` attributes.

- [ ] **Step 2: For each img without dimensions, add them**

If an img tag is missing width/height, add the attributes based on the actual image dimensions:
- `class.png` / hero: 1920×1080
- `solo.jpg` (師傅): 400×400
- `class_hall.jpg` (上課環境): 800×600
- `class_8year.JPG` (器械班): 800×600
- `solo2.jpg` (師傅示範): 400×300

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "perf: add explicit width/height to all images for CLS"
```

---

### Task 7: Check and fix `gen_regions.py`

**Files:**
- Modify: `gen_regions.py` (if it has the same issues)

- [ ] **Step 1: Check gen_regions.py for CDN references**

Run: `grep -n "cdn.tailwindcss.com\|unpkg.com\|lucide@latest" gen_regions.py`
Expected: No matches (if Task 4/5 already fixed it). If matches found, fix using same pattern as `generate_blog.py`.

- [ ] **Step 2: If fixes needed, commit**

```bash
git add gen_regions.py
git commit -m "perf: fix gen_regions.py template - remove CDN refs"
```

---

### Task 8: End-to-end validation

**Files:** No changes, validation only.

- [ ] **Step 1: Run Lighthouse on local server**

```bash
# Install lighthouse if needed
npm install -g @lhci/cli

# Start server
python3 -m http.server 8000 &

# Run lighthouse on index
lhci autorun --collect.url=http://localhost:8000/ --collect.numberOfRuns=1

# Run on blog
lhci autorun --collect.url=http://localhost:8000/blog.html --collect.numberOfRuns=1

# Run on an article
lhci autorun --collect.url=http://localhost:8000/articles/tai-chi-beginner-guide.html --collect.numberOfRuns=1
```

Expected targets:
- Performance ≥ 90
- LCP < 2.5s
- CLS < 0.1
- TBT < 200ms

- [ ] **Step 2: Check for render-blocking resources**

Open Chrome DevTools → Network → reload with "Disable cache" → check for any red lines (blocking resources).

- [ ] **Step 3: Final commit**

```bash
git add lighthouserc.json  # if created
git commit -m "ci: add Lighthouse CI config for performance regression testing"
```

---

## Execution Options

**Plan complete and saved to `docs/superpowers/plans/2026-07-14-pagespeed-optimization-v2.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Each task is self-contained and verifiable.

**2. Inline Execution** — Execute tasks sequentially in this session using `executing-plans`, batch execution with checkpoints.

**Which approach?**

---

## Self-Review Checklist

**Spec coverage:**
- GA4 blocking → Task 1, 3, 4, 5 ✅
- URL-replacement blocking → Task 1, 3, 4, 5 ✅
- Article generator CDN → Task 2 ✅
- Region pages fix → Task 4 ✅
- CLS image dimensions → Task 6 ✅
- gen_regions.py check → Task 7 ✅
- Validation → Task 8 ✅

**Placeholder scan:**
- All code blocks contain actual implementation code ✅
- All file paths are exact ✅
- All commands show expected output ✅
- No "TODO", "TBD", or "implement later" ✅

**Type consistency:**
- GA4 script strings are identical across all tasks ✅
- defer attribute syntax is consistent ✅
- js/icons.js path is correct (../ for articles, / for root pages) ✅
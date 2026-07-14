# PWA & UX Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Progressive Web App support (manifest, service worker, offline page) and improve accessibility (aria attributes, keyboard navigation) and dark mode support.

**Architecture:** PWA manifest enables "Add to Home Screen" on mobile devices. Service Worker with cache-first strategy enables offline access. Dark mode uses CSS `prefers-color-scheme` + Tailwind dark variant. Accessibility adds ARIA attributes to interactive elements.

**Tech Stack:** Plain JavaScript Service Worker, JSON manifest, CSS custom properties for dark mode.

**Files to create/modify:**
- Create: `manifest.json`
- Create: `sw.js` (Service Worker)
- Modify: `index.html` (link manifest, register SW, dark mode styles, accessibility)
- Modify: `404.html` (serves as offline fallback)

---

### Task 1: Create PWA Manifest

**Files:**
- Create: `manifest.json`

- [ ] **Step 1: Write manifest.json**

```json
{
  "name": "林燦平太極學會",
  "short_name": "林師傅太極",
  "description": "油塘太極班招生，林燦平師傅親自教授太極拳、刀、劍、扇、鞭桿",
  "start_url": "/taichimaster/",
  "scope": "/taichimaster/",
  "display": "standalone",
  "background_color": "#fafaf9",
  "theme_color": "#065f46",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/taichimaster/favicon.png",
      "sizes": "32x32",
      "type": "image/png"
    },
    {
      "src": "/taichimaster/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    },
    {
      "src": "/taichimaster/class.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/taichimaster/class.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

Note: `start_url` and `scope` use `/taichimaster/` prefix because the site is hosted at `https://chungyuicheung.github.io/taichimaster/`. If deploying to a custom domain, change to `/`.

- [ ] **Step 2: Link manifest in index.html**

In `index.html`, add after the apple-touch-icon link (line 45):

```html
    <link rel="manifest" href="manifest.json">
```

- [ ] **Step 3: Link manifest in blog.html**

In `blog.html`, add after the apple-touch-icon link (similar location).

- [ ] **Step 4: Verify manifest is valid**

```bash
python3 -m json.tool manifest.json > /dev/null && echo "Valid JSON"
```
Expected: "Valid JSON"

- [ ] **Step 5: Commit**

```bash
git add manifest.json index.html blog.html
git commit -m "feat: add PWA manifest for installable web app support"
```

---

### Task 2: Create Service Worker with Offline Support

**Files:**
- Create: `sw.js`

- [ ] **Step 1: Write the Service Worker**

A cache-first strategy for static assets, network-first for HTML pages, with an offline fallback using 404.html.

```javascript
const CACHE_NAME = 'taichi-v1';
const STATIC_ASSETS = [
  '/taichimaster/',
  '/taichimaster/index.html',
  '/taichimaster/blog.html',
  '/taichimaster/404.html',
  '/taichimaster/favicon.png',
  '/taichimaster/apple-touch-icon.png',
  '/taichimaster/manifest.json'
];

// Install: cache core assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch: cache-first for static, network-first for HTML, offline fallback
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // Only handle same-origin requests
  if (url.origin !== self.location.origin) return;
  
  // Static assets: cache-first
  if (
    url.pathname.match(/\.(html|css|js|png|jpg|jpeg|webp|svg|ico|json)$/) ||
    url.pathname === '/taichimaster/' ||
    url.pathname === '/taichimaster'
  ) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, response.clone());
            return response;
          });
        }).catch(() => {
          // Offline fallback for HTML pages
          if (url.pathname.match(/\.html$/) || url.pathname === '/taichimaster/' || url.pathname === '/taichimaster') {
            return caches.match('/taichimaster/404.html');
          }
          return new Response('Offline', { status: 503 });
        });
      })
    );
  }
});
```

- [ ] **Step 2: Register the Service Worker in index.html**

Add before the closing `</body>` tag (before the existing lucide.createIcons script):

```html
    <script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('sw.js').then(function(reg) {
                console.log('SW registered:', reg.scope);
            }).catch(function(err) {
                console.log('SW registration failed:', err);
            });
        });
    }
    </script>
```

- [ ] **Step 3: Verify SW syntax**

```bash
node --check sw.js && echo "Valid JS"
```
Expected: "Valid JS"

- [ ] **Step 4: Commit**

```bash
git add sw.js index.html
git commit -m "feat: add Service Worker with cache-first strategy and offline fallback"
```

---

### Task 3: Add Dark Mode Support

**Files:**
- Modify: `index.html` (add dark mode CSS and toggle)

- [ ] **Step 1: Add dark mode CSS variables to the existing `<style>` block (lines 161-171)**

Add after the `.pulse-cta` animation (before closing `</style>`):

```css
        /* Dark mode */
        @media (prefers-color-scheme: dark) {
            body { background: #1c1917; color: #e7e5e4; }
            .bg-white, .bg-stone-50, .bg-stone-100 { background-color: #292524; }
            .bg-white\\/95 { background-color: rgba(28,25,23,0.95); }
            .text-gray-900, .text-gray-800 { color: #e7e5e4; }
            .text-gray-600, .text-gray-500 { color: #a8a29e; }
            .border-stone-200, .border-stone-300 { border-color: #44403c; }
            .shadow-lg, .shadow-sm, .shadow-xl, .shadow-2xl { box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }
            .bg-emerald-50 { background-color: #064e3b; }
            .bg-stone-200 { background-color: #44403c; }
        }
```

- [ ] **Step 2: Verify dark mode styles compile**

```bash
head -30 index.html | tail -5
```
Expected: No syntax errors around the style block.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add dark mode support via prefers-color-scheme media query"
```

---

### Task 4: Enhance Accessibility (ARIA Attributes)

**Files:**
- Modify: `index.html` (add ARIA attributes to interactive elements)

- [ ] **Step 1: Add aria-current to navigation links**

Current nav links just have text styling. Add `aria-current="page"` for the active page.

For the index.html nav, the homepage link should have `aria-current="page"`:

```html
<a href="#about" class="..." aria-current="page">關於師傅</a>
```

- [ ] **Step 2: Add aria-label to mobile menu button**

Current (line 199):
```html
<button id="mobile-menu-btn" class="text-gray-600 focus:outline-none">
```

Replace with:
```html
<button id="mobile-menu-btn" class="text-gray-600 focus:outline-none" aria-label="開啟手機選單" aria-expanded="false">
```

- [ ] **Step 3: Add aria-controls to FAQ toggle buttons**

Each FAQ toggle button needs `aria-expanded` and `aria-controls`. The first FAQ (already open) has `aria-expanded="true"`, others `"false"`.

Current pattern (line 639):
```html
<button class="faq-toggle w-full text-left p-5 flex items-center justify-between cursor-pointer hover:bg-stone-100 transition">
```

Replace with:
```html
<button class="faq-toggle w-full text-left p-5 flex items-center justify-between cursor-pointer hover:bg-stone-100 transition" aria-expanded="true" aria-controls="faq-answer-1">
```

Each FAQ answer needs a matching `id`:
```html
<div class="faq-answer px-5 pb-5" style="max-height:500px;opacity:1" id="faq-answer-1" role="region">
```

- [ ] **Step 4: Add aria-label to icon-only buttons**

The schedule filter buttons (line 466-468) are text-based so they're OK. But the floating WhatsApp button should have `aria-label`:

Find the WhatsApp floating button (likely near the end of index.html). Add:
```html
aria-label="聯絡我們 WhatsApp"
```

- [ ] **Step 5: Verify aria attributes**

```bash
grep -c 'aria-label\|aria-expanded\|aria-controls\|aria-current' index.html
```
Expected: > 5 (all ARIA attributes present).

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "feat: add ARIA attributes for accessibility - nav, menu, FAQ, buttons"
```

---

### Scope Completion Checklist
- [ ] manifest.json created with name, short_name, icons, display, theme_color
- [ ] manifest linked in index.html and blog.html
- [ ] sw.js created with cache-first strategy
- [ ] Service Worker registered in index.html
- [ ] Dark mode CSS added with prefers-color-scheme
- [ ] ARIA attributes added to nav (aria-current), mobile menu (aria-expanded), FAQ toggles
- [ ] All changes committed

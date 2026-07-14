const CACHE_NAME = 'taichi-v20260714';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/blog.html',
  '/404.html',
  '/favicon.png',
  '/apple-touch-icon.png',
  '/manifest.json',
  '/css/tailwind.css',
  '/js/icons.js'
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
          .filter((name) => name.startsWith('taichi-'))
          .map((name) => {
            if (name !== CACHE_NAME) return caches.delete(name);
          })
      );
    })
  );
  self.clients.claim();
});

// Fetch: network-first for HTML (always check for updates), cache-first for static assets
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Only handle same-origin requests
  if (url.origin !== self.location.origin) return;

  // Static assets (CSS, JS, images): cache-first with network fallback
  if (url.pathname.match(/\.(css|js|png|jpg|jpeg|webp|svg|ico|json)$/)) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          if (response.ok) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, response.clone());
            });
          }
          return response;
        });
      })
    );
    return;
  }

  // HTML pages: network-first, fall back to cache
  if (url.pathname.match(/\.html$/) || url.pathname === '/' || url.pathname === '') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response.ok) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, response.clone());
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request).then((cached) => {
            return cached || caches.match('/404.html');
          });
        })
    );
    return;
  }

  // Everything else: network only
});
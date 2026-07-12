const CACHE_NAME = 'taichi-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/blog.html',
  '/404.html',
  '/favicon.png',
  '/apple-touch-icon.png',
  '/manifest.json'
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
    url.pathname === '/' ||
    url.pathname === ''
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
          if (url.pathname.match(/\.html$/) || url.pathname === '/' || url.pathname === '') {
            return caches.match('/404.html');
          }
          return new Response('Offline', { status: 503 });
        });
      })
    );
  }
});

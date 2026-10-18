// LawSathi Prototype — Service Worker (Offline Cache)

const CACHE_NAME = "lawsathi-prototype-v1";
const ASSETS_TO_CACHE = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./manifest.json",
  "../../content/helplines.json",
  "../../content/playbooks/fir_refusal.en.json",
  "../../content/playbooks/fir_refusal.hi.json",
  "../../content/playbooks/fir_refusal.mr.json"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("[SW] Pre-caching offline assets");
      // addAll fails if any asset 404s, so catch individually
      return Promise.allSettled(ASSETS_TO_CACHE.map(url => cache.add(url)));
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => {
        if (key !== CACHE_NAME) return caches.delete(key);
      }))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  // Network-first for API calls
  if (e.request.url.includes("/v1/ask") || e.request.url.includes("localhost:8000")) {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
    return;
  }
  // Cache-first for static assets (stale-while-revalidate pattern)
  e.respondWith(
    caches.match(e.request).then(cached => {
      const networkFetch = fetch(e.request).then(res => {
        if (res && res.status === 200) {
          const resClone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, resClone));
        }
        return res;
      });
      return cached || networkFetch;
    })
  );
});

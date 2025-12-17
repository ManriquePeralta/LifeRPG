self.addEventListener("install", e => {
  e.waitUntil(
    caches.open("liferpg").then(cache => {
      return cache.addAll([
        "/",
        "/stats",
        "/actions"
      ])
    })
  )
})

self.addEventListener("fetch", e => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  )
})

# Harrooz Radio — PWA site

A two-page site: a live radio player (home page) and a podcast archive page,
both installable as an app via "Add to Home Screen."

## Files

```
index.html          live radio player (the PWA start page)
podcast.html         podcast archive (Acast embed)
style.css            shared design system
app.js                play/pause logic + connects the service worker
manifest.json         PWA config (name, colors, icons)
service-worker.js     offline app-shell caching
icons/                placeholder icons — swap these for your logo
```

## 1. Swap in your logo

I used a placeholder dial/play icon in your brand colors so the app installs
correctly right away. To use your real logo:

1. Make a square version of your logo, ideally **512×512px**, PNG, with a bit
   of padding around it (about 10% on each side) so it isn't cropped when
   phones mask it into a circle or rounded square.
2. Replace these three files with versions generated from your logo (any
   image editor or a free tool like [realfavicongenerator.net](https://realfavicongenerator.net) can resize them
   for you):
   - `icons/icon-512.png` (512×512)
   - `icons/icon-192.png` (192×192)
   - `icons/apple-touch-icon.png` (180×180, no transparency — iOS doesn't
     support it and will show black where it should be transparent)
   - `icons/favicon-32.png` and `icons/favicon-16.png` (optional, browser tab icon)
3. Keep the filenames exactly the same, and you're done — nothing else
   needs to change.

## 2. Things you may want to rename

Everything is in plain HTML/CSS, no build step. Quick edit map:

- **Station name** — search for `Harrooz` in `index.html`, `podcast.html`,
  and `manifest.json`.
- **Persian subtitle** (`هر روز`) — in the `.wordmark .fa` span in both HTML
  files.
- **Theme colors** — all named at the top of `style.css` under `:root`.
- **Stream URL** — `STREAM_URL` constant at the top of `app.js`.
- **Podcast embed** — the `<iframe>` source in `podcast.html`.

## 3. Deploy to Cloudflare Pages

**Easiest way (no account setup beyond Cloudflare):**

1. Go to the Cloudflare dashboard → **Workers & Pages** → **Create** →
   **Pages** → **Upload assets**.
2. Drag this whole folder in (or a zip of it — Cloudflare unzips it
   automatically).
3. Click **Deploy**. You'll get a free `your-project.pages.dev` URL within
   a minute.
4. Optional: in the project's **Custom domains** tab, point your own domain
   at it.

**If you'd rather connect a GitHub repo** (so future edits auto-deploy):

1. Push this folder to a new GitHub repo.
2. In Cloudflare: **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git** → pick the repo.
3. Leave the build command empty and the output directory as `/` (this is
   a static site, no build step).
4. Deploy.

## 4. Testing "Add to Home Screen"

PWAs only install over **HTTPS** (Cloudflare Pages gives you this
automatically) — it won't offer to install if you just open the HTML file
locally from disk.

- **Android (Chrome):** open the site, tap the **⋮** menu → **Add to Home
  screen**. You should see your icon and "Harrooz" as the name.
- **iPhone (Safari):** open the site, tap the **Share** icon → **Add to
  Home Screen**. Safari doesn't show an automatic install prompt — this is
  the only way on iOS, so it's worth mentioning to your listeners.

## Notes

- The radio stream always connects fresh when you tap play, so listeners
  always join live — it never tries to "resume" an old buffered position.
- Audio keeps playing if the screen locks or you switch apps (standard
  mobile browser behavior for `<audio>`).
- The service worker only caches the page itself (HTML/CSS/JS/icons) for
  fast loading — it never caches the live stream or the podcast embed, so
  listeners always get live audio, not a stale recording.

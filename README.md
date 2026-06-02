# Backlit Electric — Site Management Guide

Live site: [backlitelectric.com](https://backlitelectric.com)
Repo: [github.com/jcrews82/jcrews82.github.io](https://github.com/jcrews82/jcrews82.github.io)

Hosted free on GitHub Pages. Checkout handled by Stripe Payment Links. No subscriptions. No servers. No monthly cost.

---

## Hard Rules

- **Never open index.html in TextEdit** — it corrupts the file. Use the GitHub browser editor (pencil icon) or VS Code only.
- **Filenames are case sensitive** — `IMG_5901.JPG` and `img_5901.jpg` are different files.
- **Never upload junk files** — do not upload anything named `Attachment.png`, `image-asset.jpeg`, or `Untitled*.png`.
- **Supported image formats:** `.jpg`, `.jpeg`, `.png`, `.webp`
- **Always compress images before adding them to the repo** — see the compression step below. Uncompressed images will make the site slow.

---

## File Structure

```
jcrews82.github.io/
├── index.html              ← the entire site (HTML + CSS + JS in one file)
├── favicon.svg
├── hero-bg.jpg
├── wood-desktop.jpg
├── wood-mobile.jpg
├── CNAME                   ← tells GitHub Pages to serve from backlitelectric.com
└── images/
    ├── for-sale/           ← product photos for the shop section
    ├── pedals/
    │   ├── list.json       ← controls which pedal photos appear in gallery
    │   └── *.jpg / *.jpeg
    ├── guitars/
    │   ├── list.json
    │   └── *.jpg / *.jpeg
    └── amps/
        ├── list.json
        └── *.jpg / *.jpeg
```

---

## How the Gallery Works

The gallery shows 15 random photos per tab (Pedals / Guitars / Amps). A Shuffle button lets visitors see a different 15 without reloading.

Each tab reads a `list.json` file from its folder. **Only photos listed in `list.json` will appear on the site.** If a photo is in the folder but missing from `list.json`, it won't show.

---

## Adding Gallery Photos

### Step 1 — Compress first (required)

Every photo must be under 200kb or the gallery loads slowly. Open Terminal, navigate to your repo folder, and run:

```bash
find images/pedals images/guitars images/amps -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) | while read f; do
  sips -Z 800 --setProperty formatOptions 60 "$f" --out "$f"
done
```

To get to your repo in Terminal: open Terminal, type `cd ` with a space, drag your repo folder into the Terminal window, hit Enter.

Safe to run on already-compressed photos. Originals in iCloud are not affected.

### Step 2 — Copy photos into the right folder

- Pedal photos → `images/pedals/`
- Guitar photos → `images/guitars/`
- Amp photos → `images/amps/`

### Step 3 — Update list.json

Open the `list.json` for that folder in the GitHub browser editor and add your new filenames:

```json
[
  "IMG_5901.jpeg",
  "IMG_6040.JPG",
  "IMG_7022.jpeg"
]
```

Rules:
- Filenames must match exactly — same capitalization, same extension
- Each entry is in quotes, separated by commas
- No comma after the last entry
- Whole thing wrapped in `[ ]`

### Step 4 — Commit and push

In GitHub Desktop, write a summary and click Commit. Then Push Origin. Site updates within a minute or two.

---

## Removing Gallery Photos

1. Delete the image file from the folder
2. Remove its filename from `list.json`
3. Commit and push

---

## Adding a New Pedal for Sale

### Step 1 — Create a Stripe Payment Link

1. Go to [dashboard.stripe.com](https://dashboard.stripe.com) and log in
2. Click **Payment Links** → **+ Create payment link**
3. Add product name and price ($125)
4. Add shipping: $15 flat rate, US and Canada only
5. Click **Create link** — copy the `https://buy.stripe.com/xxxxxxxxx` URL

### Step 2 — Add product photos

Name them clearly: `pedal-name.jpg` and `pedal-name-inside.jpg`. Compress first, then upload to `images/for-sale/` via GitHub Desktop.

### Step 3 — Add the pedal card to index.html

Open `index.html` in the GitHub browser editor. Find `<div class="pedals-grid">` and paste this block inside it, filling in your details:

```html
<!-- PEDAL NAME -->
<div class="pedal-card">
  <div class="pedal-img-wrap">
    <img src="images/for-sale/YOUR-PHOTO.jpg" alt="Pedal Name">
  </div>
  <div>
    <p class="pedal-type">Fuzz</p>
    <p class="pedal-name">Pedal Name</p>
  </div>
  <p class="pedal-desc">Your description here.</p>
  <img class="pedal-inside" src="images/for-sale/YOUR-PHOTO-inside.jpg" alt="Pedal internals">
  <div class="pedal-footer">
    <span class="pedal-price">$125</span>
    <a href="https://buy.stripe.com/YOUR_LINK" target="_blank" class="buy-btn">Buy Now</a>
  </div>
</div>
```

Commit and push.

---

## Removing a Sold Pedal

1. Open `index.html` in GitHub browser editor
2. Delete the entire `<div class="pedal-card">` block for that pedal
3. Commit and push
4. Archive the Stripe Payment Link in your Stripe dashboard

---

## Current Pedals for Sale

| Pedal | Stripe Link |
|-------|-------------|
| Karma Sutra | https://buy.stripe.com/dRmdR84KEdBM0J49mb8ww03 |
| Scarab Deluxe | https://buy.stripe.com/bJe7sKb92gNY4Zk0PF8ww00 |
| The Crayon | https://buy.stripe.com/6oU28qele2X82Rc41R8ww01 |
| Black Ash | https://buy.stripe.com/00w4gydhafJU8bw9mb8ww02 |

---

## Backing Out of Netlify

You are no longer using Netlify. The site runs entirely on GitHub Pages. To fully close out Netlify:

1. Log into [app.netlify.com](https://app.netlify.com)
2. Go to your site → **Site settings** → scroll to bottom → **Delete this site**
3. After deleting the site, go to your **Team settings** → **Billing** → downgrade or cancel your plan
4. Confirm your DNS in GoDaddy no longer points to any Netlify addresses (it shouldn't — you already fixed this)

Your repo still has `netlify.toml` and `package.json` — if you haven't deleted those yet, do it now. They're dead weight.

---

## DNS Settings (GoDaddy) — Do Not Touch

| Type | Name | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | jcrews82.github.io. |

MX/email records are separate — do not touch those.

---

## If the Site Goes Down

1. Check [githubstatus.com](https://githubstatus.com)
2. Confirm DNS records in GoDaddy match the table above
3. Confirm the `CNAME` file in the repo root contains exactly: `backlitelectric.com`
4. Go to repo Settings → Pages → confirm source is `main` branch and custom domain is `backlitelectric.com`

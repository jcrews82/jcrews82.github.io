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

Every photo must be under 200kb or the gallery loads slowly. Run this in Terminal from inside your repo folder:

```bash
find images/pedals images/guitars images/amps -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) | while read f; do
  sips -Z 800 --setProperty formatOptions 60 "$f" --out "$f"
done
```

To get to your repo folder in Terminal: open GitHub Desktop → Repository menu → Open in Terminal. Or open Terminal, type `cd ` with a space, then drag your repo folder into the Terminal window and hit Enter.

This command is safe to run on already-compressed photos. Your originals in iCloud are not affected.

### Step 2 — Copy photos into the right folder

- Pedal photos → `images/pedals/`
- Guitar photos → `images/guitars/`
- Amp photos → `images/amps/`

### Step 3 — Update list.json

Open the `list.json` file for that folder in the GitHub browser editor and add your new filenames. The format is:

```json
[
  "IMG_5901.jpeg",
  "IMG_6040.JPG",
  "IMG_7022.jpeg"
]
```

Rules:
- Filenames must match exactly — same capitalization, same extension
- Each entry is in quotes and separated by commas
- No comma after the last entry
- The whole thing is wrapped in `[ ]`

### Step 4 — Commit and push

In GitHub Desktop, type a summary (e.g. "add pedal photos") and click Commit. Then click Push Origin. The site updates within a minute or two.

---

## Removing Gallery Photos

1. Delete the image file from the folder (via GitHub Desktop or the GitHub browser)
2. Remove its filename from `list.json`
3. Commit and push

---

## Adding a New Pedal for Sale

### Step 1 — Create a Stripe Payment Link

1. Go to [dashboard.stripe.com](https://dashboard.stripe.com) and log in
2. Click **Payment Links** in the left sidebar
3. Click **+ Create payment link**
4. Add a product: enter the pedal name and price (e.g. $125)
5. Under **After payment**, set the confirmation page message or leave default
6. Click **Create link**
7. Copy the link — it looks like `https://buy.stripe.com/xxxxxxxxx`

Note: Stripe does not add shipping automatically. If you want to collect $15 shipping, either set the product price to $140, or add a separate shipping line item in Stripe when creating the link.

### Step 2 — Add product photos

Name your photos clearly, e.g. `pedal-name.jpg` and `pedal-name-inside.jpg`. Compress them first (see above), then upload to `images/for-sale/` via GitHub Desktop.

### Step 3 — Add the pedal card to index.html

Open `index.html` in the GitHub browser editor (pencil icon). Find the `<div class="pedals-grid">` section. Copy this block and fill in your details:

```html
<!-- YOUR PEDAL NAME -->
<div class="pedal-card">
  <div class="pedal-img-wrap">
    <img src="images/for-sale/YOUR-PHOTO.jpg" alt="Your Pedal Name">
  </div>
  <div>
    <p class="pedal-type">Fuzz</p>
    <p class="pedal-name">Your Pedal Name</p>
  </div>
  <p class="pedal-desc">Your description here.</p>
  <img class="pedal-inside" src="images/for-sale/YOUR-PHOTO-inside.jpg" alt="Your Pedal internals">
  <div class="pedal-footer">
    <span class="pedal-price">$125</span>
    <a href="https://buy.stripe.com/YOUR_LINK_HERE" target="_blank" class="buy-btn">Buy Now</a>
  </div>
</div>
```

Replace everything in ALL CAPS with your actual values. Commit and push when done.

---

## Removing a Sold Pedal

1. Open `index.html` in the GitHub browser editor
2. Find the `<div class="pedal-card">` block for that pedal
3. Delete the entire block from `<!-- PEDAL NAME -->` through the closing `</div>`
4. Commit and push
5. Archive the Stripe Payment Link in your Stripe dashboard so it no longer accepts payments

---

## Current Pedals for Sale

| Pedal | Stripe Link |
|-------|-------------|
| Karma Sutra | https://buy.stripe.com/dRmdR84KEdBM0J49mb8ww03 |
| Scarab Deluxe | https://buy.stripe.com/bJe7sKb92gNY4Zk0PF8ww00 |
| The Crayon | https://buy.stripe.com/6oU28qele2X82Rc41R8ww01 |
| Black Ash | https://buy.stripe.com/00w4gydhafJU8bw9mb8ww02 |

---

## DNS Settings (GoDaddy)

The domain backlitelectric.com is registered at GoDaddy and points to GitHub Pages. Do not change these records unless something breaks.

| Type | Name | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | jcrews82.github.io. |

The MX records and email settings are separate — do not touch those.

---

## If the Site Goes Down

1. Check [githubstatus.com](https://githubstatus.com) — GitHub Pages outages are rare but happen
2. Check your DNS records in GoDaddy match the table above
3. Check that the `CNAME` file in the repo root contains exactly: `backlitelectric.com`
4. In your GitHub repo, go to Settings → Pages and confirm the source is set to `main` branch


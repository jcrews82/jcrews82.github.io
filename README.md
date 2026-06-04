# Backlit Electric — Site Management Guide

## IMPORTANT: Never open index.html in TextEdit
TextEdit corrupts HTML files. Always edit index.html directly in the GitHub browser editor (pencil icon).

---

## For-Sale Listings

### How it works
Each pedal card is hardcoded in `index.html`. When someone clicks Buy Now, a dark overlay opens and Stripe's embedded checkout loads directly on the page — no redirect, no new tab. Payment is handled by a Cloudflare Worker (`backlit-checkout.jeff-a-crews.workers.dev`) which talks to Stripe securely using your secret key.

---

### To ADD a new pedal for sale

**Step 1 — Upload photos**
1. Open GitHub Desktop
2. Copy the pedal's exterior and interior photos into `images/for-sale/` in your local repo
3. Name them clearly, all lowercase, no spaces: e.g. `my-pedal.jpg` and `my-pedal-inside.jpg`
4. Commit and push in GitHub Desktop

**Step 2 — Create the product in Stripe**
1. Go to [dashboard.stripe.com](https://dashboard.stripe.com) → **Product catalog** → **+ Add product**
2. Name: the pedal name
3. Price: one-time, whatever the amount is
4. Click **Save product**
5. On the product page, click the **three dots (...)** next to the price row → **Copy price ID**
6. It will look like: `price_1Abc123...`

**Step 3 — Add the card to index.html**
1. Go to your GitHub repo → click `index.html` → click the pencil icon to edit
2. Find any existing pedal card block and copy it from `<!-- PEDAL NAME -->` comment to the closing `</div>` of that card
3. Paste it right after the last pedal card, before the closing `</div>` of `.pedals-grid`
4. Update these fields in your new block:
   - `src="images/for-sale/YOUR-PHOTO.jpg"` — exterior photo filename
   - `alt="Your Pedal Name"` — pedal name
   - `pedal-type` — e.g. `Fuzz` or `Overdrive` or `Fuzz / Distortion`
   - `pedal-name` — the pedal name
   - `pedal-desc` — your description
   - `src="images/for-sale/YOUR-PHOTO-inside.jpg"` — internals photo
   - `$125` in the `pedal-price` span — your price
   - The price ID in the button: `onclick="openCheckout('price_YOUR_PRICE_ID_HERE', this)"`
5. Click **Commit changes**

**Template block to copy:**
```html
<!-- YOUR PEDAL NAME -->
<div class="pedal-card">
  <div class="pedal-img-wrap">
    <div class="sold-badge">Sold</div>
    <img src="images/for-sale/your-pedal.jpg" alt="Your Pedal Name">
  </div>
  <div>
    <p class="pedal-type">Fuzz</p>
    <p class="pedal-name">Your Pedal Name</p>
  </div>
  <p class="pedal-desc">Your description here.</p>
  <img class="pedal-inside" src="images/for-sale/your-pedal-inside.jpg" alt="Your Pedal Name internals">
  <div class="pedal-footer">
    <span class="pedal-price">$125</span>
    <button class="buy-btn" onclick="openCheckout('price_XXXXXXXXXXXXXXXXXXXX', this)">Buy Now</button>
  </div>
</div>
```

---

### To mark a pedal as SOLD

Two changes to the pedal's card in `index.html`:

**1. Add `is-sold` to the card div:**
```html
<!-- Before -->
<div class="pedal-card">

<!-- After -->
<div class="pedal-card is-sold">
```

**2. Replace the Buy Now button with a Sold label:**
```html
<!-- Before -->
<button class="buy-btn" onclick="openCheckout('price_...', this)">Buy Now</button>

<!-- After -->
<span class="sold-btn">Sold</span>
```

This will grey out the card, show a "Sold" badge over the photo, and remove the checkout button.

---

### To mark a sold pedal as AVAILABLE again

Reverse the two changes above:

**1. Remove `is-sold` from the card div:**
```html
<div class="pedal-card">
```

**2. Replace the Sold label with the Buy Now button** (you'll need the price ID — check Stripe dashboard):
```html
<button class="buy-btn" onclick="openCheckout('price_XXXXXXXXXXXXXXXXXXXX', this)">Buy Now</button>
```

---

### To REMOVE a pedal entirely
1. Go to `index.html` in GitHub → pencil icon to edit
2. Find the pedal's card block (look for the `<!-- PEDAL NAME -->` comment)
3. Delete everything from `<!-- PEDAL NAME -->` to the closing `</div>` of that card
4. Commit changes
5. Optionally archive the product in Stripe (dashboard → product → Archive)

---

## Cloudflare Worker

The checkout is powered by a Cloudflare Worker at:
`https://backlit-checkout.jeff-a-crews.workers.dev`

You should never need to touch this. But if checkout breaks:

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages** → **backlit-checkout**
2. Check **Settings → Variables and Secrets** — confirm `STRIPE_SECRET_KEY` is present
3. If the key is missing or expired, create a new secret key in Stripe dashboard → Developers → API keys → + Create secret key, then update it here
4. The worker URL is referenced in `index.html` as `WORKER_URL` near the top of the `<script>` block — confirm it matches

---

## Gallery Photos (pedals / guitars / amps)

### How it works
Each gallery folder has a `list.json` file that controls what photos appear. The gallery reads this file and displays photos in a random shuffled order.

### To ADD gallery photos
1. Open GitHub Desktop
2. Copy new photos into the correct folder in your local repo:
   - `images/pedals/` for the pedal gallery
   - `images/guitars/` for the guitar gallery
   - `images/amps/` for the amp gallery
3. Commit and push in GitHub Desktop
4. Get the updated file list from the GitHub API:
   - `https://api.github.com/repos/jcrews82/jcrews82.github.io/contents/images/pedals`
   - `https://api.github.com/repos/jcrews82/jcrews82.github.io/contents/images/guitars`
   - `https://api.github.com/repos/jcrews82/jcrews82.github.io/contents/images/amps`
5. Paste the API response to Claude and ask for a new randomized `list.json`
6. Upload the new `list.json` to the correct folder in GitHub (replacing the old one)

### To REMOVE a gallery photo
1. Delete the photo file from the folder in GitHub
2. Get a new `list.json` generated (steps 4–6 above)

---

## Rules
- Filenames are case sensitive — `IMG_5901.JPG` is not the same as `img_5901.jpg`
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
- Never open `index.html` in TextEdit — use GitHub browser editor only
- Never upload files named `Attachment.png`, `image-asset.jpeg`, or `Untitled*.png` — junk files from bad exports
- Price IDs (`price_...`) and Product IDs (`prod_...`) are different — always use the **Price ID** in the button

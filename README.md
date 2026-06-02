# Backlit Electric — Site Management Guide

## IMPORTANT: Never open index.html in TextEdit
TextEdit corrupts HTML files. Always edit index.html directly in the GitHub browser editor (pencil icon).

---

## Gallery Photos (pedals / guitars / amps)

### How it works
Each gallery folder has a `list.json` file that controls what photos appear on the site. The gallery reads this file and displays the photos in the order listed.

### To ADD photos
1. Open GitHub Desktop
2. Copy new photos into the correct folder in your local repo:
   - `images/pedals/` for pedal gallery
   - `images/guitars/` for guitar gallery
   - `images/amps/` for amp gallery
3. Commit and push in GitHub Desktop
4. Get the updated file list from the GitHub API:
   - `https://api.github.com/repos/jcrews82/jcrews82.github.io/contents/images/pedals`
   - `https://api.github.com/repos/jcrews82/jcrews82.github.io/contents/images/guitars`
   - `https://api.github.com/repos/jcrews82/jcrews82.github.io/contents/images/amps`
5. Paste the API response to Claude and ask for a new randomized list.json
6. Upload the new list.json to the correct folder in GitHub (replacing the old one)

### To REMOVE a photo
1. Delete the photo file from the folder in GitHub
2. Get a new list.json generated (step 4-6 above)

---

## For-Sale Product Photos (images/for-sale/)

These are hardcoded into index.html. Current filenames in use:
- `karma-sutra.jpg` + `karma-sutra-inside.jpg`
- `scarab-deluxe.jpeg` + `scarab-deluxe-inside.jpeg`
- `the-crayon.jpeg` + `the-crayon-inside.jpeg`
- `black-ash.jpeg` + `black-ash-inside.jpeg`

### To add a new for-sale product
1. Upload exterior and interior photos to `images/for-sale/`
2. Edit index.html in GitHub browser editor to add the new pedal card
3. Ask Claude for the updated index.html if needed

---

## Rules
- Filenames are case sensitive — `IMG_5901.JPG` is not the same as `img_5901.jpg`
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
- Never open index.html in TextEdit — use GitHub browser editor only
- Never upload files named `Attachment.png`, `image-asset.jpeg`, or `Untitled*.png` — these are junk files from bad exports

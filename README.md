# Backlit Electric — How to Manage Photos

## Folder Structure

```
images/
  pedals/       ← pedal gallery photos
  guitars/      ← guitar gallery photos
  amps/         ← amp gallery photos
  for-sale/     ← photos for active product listings
```

---

## Gallery Photos (pedals / guitars / amps)

The gallery reads folder contents automatically — **no list.json needed.**

### To ADD a photo
1. Go to github.com/jcrews82/jcrews82.github.io
2. Navigate into the right folder (`images/pedals`, `images/guitars`, or `images/amps`)
3. Click **Add file → Upload files** and drag your photo(s) in
4. Commit — done. Photos appear on the site automatically.

### To REMOVE a photo
1. Navigate to the right folder
2. Click the photo file
3. Click the trash icon to delete it
4. Commit — it disappears from the site automatically.

---

## For-Sale Product Photos (images/for-sale/)

These are wired directly into `index.html` — not automatic. Filenames must match exactly what's in the HTML.

**Current filenames in use:**
- `karma-sutra.jpg` + `karma-sutra-inside.jpg`
- `scarab-deluxe.jpeg` + `scarab-deluxe-inside.jpeg`
- `the-crayon.jpeg` + `the-crayon-inside.jpeg`
- `black-ash.jpeg` + `black-ash-inside.jpeg`

To add a new product photo, upload the file and update `index.html` to reference it.

---

## Rules
- Filenames are case sensitive — `IMG_5901.JPG` is not the same as `img_5901.jpg`
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
- Do not open `index.html` in TextEdit — it will corrupt the file. Use GitHub's browser editor instead.

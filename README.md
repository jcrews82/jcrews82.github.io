# Backlit Electric — How to Add or Remove Gallery Photos

## Folder Structure

images/
  pedals/     ← pedal gallery photos
  guitars/    ← guitar gallery photos  
  amps/       ← amp gallery photos
  for-sale/   ← photos for active product listings

Each folder has a list.json file that controls what shows on the site.

---

## To ADD a Photo

1. Go to github.com/jcrews82/jcrews82.github.io
2. Navigate into the right folder (images/pedals, images/guitars, images/amps, or images/for-sale)
3. Click Add file → Upload files and drag your photo in
4. Commit the upload
5. Click on list.json in that same folder
6. Click the pencil icon to edit it
7. Add your filename to the list:

[
  "existing-photo.jpg",
  "your-new-photo.jpg"
]

8. Commit changes — done

---

## To REMOVE a Photo

1. Navigate to the right folder
2. Click on list.json and edit it
3. Delete the filename you want to remove
4. Commit changes
5. Optionally delete the actual image file too

---

## Rules

- Filenames are case sensitive — IMG_5901.JPG is not the same as img_5901.jpg
- Always keep the square brackets [ ] at the start

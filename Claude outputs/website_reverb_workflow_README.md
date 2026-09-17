# Backlit Electric — Website + Reverb Sync Workflow (read this first)

Tell Claude to "read the website_reverb_workflow_README in Claude outputs" at the
start of a new session and it should be able to pick this project up without
re-deriving anything from scratch.

## What this project is

- Site: backlitelectric.com, static HTML, hosted on GitHub Pages.
- Repo: `jcrews82/jcrews82.github.io` (in `~/Documents/GitHub/` on Jeff's Mac).
- `index.html` is the **single source of truth** for every pedal listing —
  title, description, price, photos, sold status. Never edit it in TextEdit;
  follow the repo's own `README.md` for the pedal-card template and Stripe
  price-ID instructions.
- Checkout: Stripe, via a Cloudflare Worker
  (`backlit-checkout.jeff-a-crews.workers.dev`) that does the actual charge
  server-side. Buy buttons use the Stripe **Price ID** (`price_...`), never
  the Product ID (`prod_...`).
- Reverb: listings there are generated FROM `index.html` by
  `reverb_sync.py`, which the repo also contains. Jeff runs this script
  himself in Terminal — **never through Claude** (his explicit standing
  rule, also documented in the repo README).

## Adding a new batch of pedals — the steps, in order

1. Jeff drops raw photos in `images/ incoming/` (note: literal leading space
   in that folder name — confirmed via `ls -1 | cat -A`).
2. Claude (or Jeff) identifies/pairs exterior + interior shots, renames them
   lowercase-hyphenated (e.g. `fuzz-face-rangemaster.jpg`,
   `fuzz-face-rangemaster-inside.jpg`), and **copies** (not moves — keep the
   originals as backup) into `images/for-sale/`.
3. Ask Jeff lots of questions rather than assuming: pedal name, description
   (draft it in his voice, he'll correct), price, any trademark-sensitive
   naming (e.g. "Muff 2" instead of "Big Muff clone" to dodge Electro-Harmonix
   trademark issues), and designer credit where relevant (e.g. Bob Myer /
   Analog Noir builds — always double check the spelling with him, it's
   churned before).
4. Draft the new `pedal-card` HTML block per the existing template (sold
   badge div, pedal-type, pedal-name, pedal-desc, interior image, price span,
   Buy button) and insert it into `index.html`. Verify by counting
   `pedal-card` / `buy-btn` occurrences and checking div-tag balance before
   calling it done.
5. Jeff creates the Stripe product(s) himself and pastes back the Price
   ID(s) (`price_...`) in the order the pedals were discussed. Drop those
   into the matching Buy buttons.
6. Jeff commits/pushes via GitHub Desktop (Claude does not run git commands
   in this repo). Wait ~3 minutes for GitHub Pages to rebuild, then verify
   the live site.
7. Once the site is confirmed live, Jeff gives the go-ahead and **runs
   `reverb_sync.py` himself** in Terminal to create/update the Reverb
   listings.
8. Jeff does a manual pass on Reverb for anything newly created: shipping
   profile / local pickup / inventory — the script does not set these yet
   (see "Known gaps" below). Then he publishes the drafts live.

## reverb_sync.py — how it works

- Parses `index.html` directly (balanced-div regex extraction) as the sole
  source of truth for both what's on the site and what should be on Reverb.
  Nothing about Reverb content is hand-maintained separately.
- Computes the Reverb list price automatically from the site price so Jeff
  nets (site price + 2%) after Reverb's cut (5% selling fee + 3.19%
  processing + $0.49 flat). This is intentional — don't "fix" a Reverb price
  that looks higher than the site price, that's the fee recoup working as
  designed.
- Category resolution: pulls Reverb's live category tree from
  `/categories/flat` rather than hardcoding UUIDs, with a
  `TYPE_TO_CATEGORY_LEAF` override dict in the script for cases where the
  site's `pedal-type` text doesn't match Reverb's leaf category name
  exactly. Currently overridden: `"Overdrive" -> "Overdrive and Boost"`.
  If a future pedal type errors out with "Couldn't find a Reverb category
  for pedal type 'X'", add an override here — check Reverb's category
  browse URL structure (reverb.com/c/effects-and-pedals/...) to find the
  right leaf name.
- Shipping: currently NOT automated (see "Known gaps").
- State file: `reverb_state.json`, lives next to the script (resolved via
  `__file__`). Maps pedal name -> Reverb listing info including
  `reverb_id`. Used to diff site-vs-Reverb state (CREATE / UPDATE / END) so
  re-running the script doesn't create duplicates. It also has a "bootstrap
  adopt" safety net that matches existing Reverb listings by name/model
  before assuming something needs to be created fresh — protects against
  dupes even if this file is ever missing or empty.
- **API response shape, confirmed empirically (not from Reverb's docs):** a
  successful `POST /api/listings` returns
  `{"message": ..., "listing": {"id": <int>, ...}}` — the ID is nested
  under `"listing"`, not top-level. The script's ID-extraction logic checks
  top-level `id` first, then `listing.id`, then a self-link fallback, in
  that order. This was a real bug (fixed 2026-09) that caused
  `Created id=None` even on successful creates — if that message ever
  reappears, the response shape has probably changed again and needs a
  fresh look at the raw JSON.
- **Known footgun:** a category-resolution failure calls `sys.exit(1)`
  mid-loop, which skips `save_state()` entirely (it only runs after the
  full loop completes). That means even pedals that DID get created
  successfully on Reverb earlier in that same run won't be saved to state,
  risking duplicate-creation on the next run. If a run dies partway through
  with a fatal category error, check Reverb directly for what got created
  and manually patch `reverb_state.json` with the real listing IDs before
  re-running (there's a precedent for this — see git history / ask Claude
  about "Nobels ODR-1" state patch from Sept 2026 if it needs redoing).

## Known gaps / deliberately deprioritized

- **Shipping automation**: Reverb listings need "flat rate + local pickup"
  set manually after creation. Researched (`shipping_profile_id` referencing
  a pre-configured Shipping Profile vs. a manual `shipping.rates` +
  `local: true` object) but not implemented — Jeff said doing it by hand
  post-creation is still faster than building full automation right now.
  Revisit only if he asks.
- **Security**: the Reverb API bearer token is hardcoded in plaintext in
  `reverb_sync.py`, inside a repo that's very likely public (required for
  free GitHub Pages hosting). Flagged to Jeff once, never acted on. Worth
  resurfacing if this repo or its visibility ever comes up, but don't act
  on it unilaterally.

## Standing rules / preferences

- Shipping policy: $15 flat rate, **US and Canada** (not US-only — this was
  explicitly confirmed). Ships within 3 business days from Austin, TX. All
  sales final, lifetime warranty against defects/workmanship.
- Reverb category for all pedals so far: Effects and Pedals, using whatever
  sub-category the site's `pedal-type` maps to. Don't invent a second
  sub-category if one isn't already set up for that type.
- Don't run git commands in this repo — Jeff uses GitHub Desktop.
- Don't run `reverb_sync.py` for Jeff — walk him through it, he runs it
  himself in Terminal.
- Ask lots of clarifying questions before assuming names, prices, or
  descriptions for new listings — Jeff has said this explicitly works
  better.
- If unsure about something (API shape, category name, a spelling), say so
  plainly rather than stating it confidently — Jeff has called this out
  before as something he wants Claude to do better.

## Related but separate project

There's also a JFET Drive Booster PCB design (netlist doc in this same
folder: `jfet_drive_booster_netlist.md`) — that's a hardware/PCB project,
unrelated to the website/Reverb pipeline, currently paused. Don't conflate
the two unless Jeff brings the PCB work back up.

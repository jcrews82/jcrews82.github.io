#!/usr/bin/env python3
"""
Keep Reverb mirrored to backlitelectric.com — run this after every site update.

WHERE TO PUT THIS FILE:
  Save it in the ROOT of your jcrews82.github.io repo folder, right next to
  index.html. It reads index.html from the same folder it lives in, and it
  keeps a small reverb_state.json file (also in that folder) to remember
  which pedals it's already put on Reverb.

HOW TO RUN (on your own Mac, in a real Terminal window — not through Claude):
    cd ~/Documents/GitHub/jcrews82.github.io
    python3 reverb_sync.py

Only Python's built-in libraries are used — nothing to pip install.

WHAT IT DOES EACH RUN:
  1. Reads every pedal card currently in index.html (name, type, price,
     description, photos) — this is the single source of truth, so there's
     nothing to re-type or keep in sync by hand.
  2. Compares that against reverb_state.json (what it put on Reverb last time).
       - New pedal on the site, not on Reverb yet  -> CREATE a Reverb listing
       - Pedal on Reverb, price/desc/photos changed -> UPDATE that listing
       - Pedal that was on Reverb but is gone from the site (sold/pulled)
         -> END that Reverb listing
       - Nothing changed -> does nothing
  3. Prints the plan and asks for a y/n before touching Reverb at all.

REVERB PRICING: your Reverb price is NOT the same number as your site price.
It's calculated so that after Reverb's cut (5% selling fee + ~3.19% payment
processing + $0.49), you net your site price PLUS the 2% bump you asked for.
See the FEES section below — update those numbers if Reverb ever changes them
(check https://help.reverb.com/hc/en-us/articles/40917652290843).

THINGS IT DELIBERATELY DOESN'T TOUCH:
  - Shipping profile / rates. Set your $15 flat US+Canada shipping profile
    once in your Reverb seller settings; new listings pick up your account
    default. Just glance at each new draft to confirm it's applied.
  - Photos aren't uploaded to Reverb — it points Reverb at your live site's
    own image URLs (backlitelectric.com/images/for-sale/...), so nothing to
    upload, but the site has to actually be pushed live before you run this.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

TOKEN = "1ec7ce5ba9d54272d1ab7a7693377239765a5a950727b35626bff68915287813"
BASE = "https://api.reverb.com/api"
SITE_ROOT = "https://backlitelectric.com/"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML_PATH = os.path.join(SCRIPT_DIR, "index.html")
STATE_PATH = os.path.join(SCRIPT_DIR, "reverb_state.json")

MAKE = "Backlit Electric"
CONDITION_NAME = "Brand New"

# Maps the text in <p class="pedal-type"> on the site to the leaf category
# name Reverb uses under "Effects and Pedals" (e.g. site says "Fuzz", Reverb's
# category tree leaf is also "Fuzz"). Add an entry here if you ever add a
# pedal type that doesn't match Reverb's category name 1:1.
TYPE_TO_CATEGORY_LEAF = {
    "Fuzz": "Fuzz",
    # Reverb's actual leaf category is "Overdrive and Boost", not "Overdrive" --
    # confirmed by category browse URL (reverb.com/c/effects-and-pedals/overdrive-and-boost),
    # not by a direct /categories/flat dump. If this is wrong, the script will
    # error out cleanly again rather than silently misfiling anything.
    "Overdrive": "Overdrive and Boost",
}
CATEGORY_PARENT = "Effects and Pedals"

# End-listing reason. Reverb's API accepts "not_sold" or "reverb_sale" (the
# latter is only for a sale you found on Reverb but settled in cash/in
# person). Since these sell through the site's own Stripe checkout, not
# through Reverb, "not_sold" is the right one — it just means "delisting,
# not because of a sale made on Reverb."
END_REASON = "not_sold"

# --- Reverb fees (standard, non-Preferred-Seller account) ---
# Source: https://help.reverb.com/hc/en-us/articles/40917652290843
#         https://help.reverb.com/hc/en-us/articles/41988540155931
SELLING_FEE_PCT = 0.05       # 5% selling fee, all sellers
PROCESSING_FEE_PCT = 0.0319  # 3.19% payment processing (2.99% if you become a Preferred Seller)
PROCESSING_FLAT = 0.49       # + $0.49 per transaction
BUMP_PCT = 0.02              # the extra 2% you want on top of your site price

HEADERS = {
    "Content-Type": "application/hal+json",
    "Accept": "application/hal+json",
    "Accept-Version": "3.0",
    "Authorization": f"Bearer {TOKEN}",
}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def api_get(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def api_call(path, method, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", "replace")
        print(f"    -> HTTP {e.code} error from Reverb ({method} {path}):")
        print("    " + body_text[:2000])
        return None


# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------

def reverb_price_for(site_price):
    """Price to list on Reverb so that after Reverb's fees you net
    site_price * (1 + BUMP_PCT)."""
    net_target = site_price * (1 + BUMP_PCT)
    price = (net_target + PROCESSING_FLAT) / (1 - SELLING_FEE_PCT - PROCESSING_FEE_PCT)
    return round(price, 2)


# ---------------------------------------------------------------------------
# Parse index.html for active pedal cards
# ---------------------------------------------------------------------------

def extract_pedal_cards(html):
    """Balanced-div extraction — walks div open/close tags so nested markup
    inside a card doesn't confuse a naive regex."""
    cards = []
    tag_re = re.compile(r"<div\b|</div>")
    for m in re.finditer(r'<div\s+class="pedal-card([^"]*)"', html):
        depth = 0
        end = None
        for tm in tag_re.finditer(html, m.start()):
            if tm.group() == "</div>":
                depth -= 1
                if depth == 0:
                    end = tm.end()
                    break
            else:
                depth += 1
        if end is None:
            continue
        card_html = html[m.start():end]
        is_sold = "is-sold" in m.group(1)
        cards.append((card_html, is_sold))
    return cards


def parse_pedal(card_html):
    def find(pattern, default=None):
        mm = re.search(pattern, card_html, re.S)
        return mm.group(1).strip() if mm else default

    name = find(r'<p class="pedal-name">([^<]*)</p>')
    ptype = find(r'<p class="pedal-type">([^<]*)</p>')
    desc = find(r'<p class="pedal-desc">(.*?)</p>')
    price_text = find(r'<span class="pedal-price">\$([\d,.]+)</span>')
    imgs = re.findall(r'<img[^>]+src="(images/for-sale/[^"]+)"', card_html)

    if not (name and ptype and desc and price_text and imgs):
        return None

    desc = re.sub(r"\s+", " ", desc).strip()
    price = float(price_text.replace(",", ""))
    photos = [SITE_ROOT + src for src in imgs]

    return {
        "name": name,
        "type": ptype,
        "description": desc,
        "site_price": price,
        "photos": photos,
    }


def load_active_pedals():
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    pedals = {}
    for card_html, is_sold in extract_pedal_cards(html):
        if is_sold:
            continue
        p = parse_pedal(card_html)
        if p:
            pedals[p["name"]] = p
    return pedals


# ---------------------------------------------------------------------------
# State file
# ---------------------------------------------------------------------------

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Reverb reference lookups
# ---------------------------------------------------------------------------

def get_condition_uuid():
    data = api_get("/listing_conditions")
    conditions = data.get("conditions") or data.get("_embedded", {}).get("conditions", [])
    for c in conditions:
        if c.get("display_name", c.get("name", "")).lower() == CONDITION_NAME.lower():
            return c["uuid"]
    print(f"Couldn't find condition '{CONDITION_NAME}'. Raw response:")
    print(json.dumps(data, indent=2)[:2000])
    sys.exit(1)


def _split_category_name(full):
    parts = [p.strip() for p in re.split(r"\s*[/>]\s*", full) if p.strip()]
    return parts


def get_category_uuid_cache():
    data = api_get("/categories/flat")
    return data.get("categories") or data.get("_embedded", {}).get("categories", [])


def get_category_uuid(categories, pedal_type):
    leaf_wanted = TYPE_TO_CATEGORY_LEAF.get(pedal_type, pedal_type)
    strict, loose = [], []
    for c in categories:
        full = c.get("full_name") or c.get("name") or ""
        uuid = c.get("uuid")
        if not uuid or not full:
            continue
        parts = _split_category_name(full)
        if not parts:
            continue
        leaf = parts[-1]
        parent = parts[0] if len(parts) > 1 else None
        if leaf.lower() != leaf_wanted.lower():
            continue
        loose.append((c, parts))
        if parent and parent.lower() == CATEGORY_PARENT.lower():
            strict.append((c, parts))
    pool = strict or loose
    if not pool:
        print(f"Couldn't find a Reverb category for pedal type '{pedal_type}'.")
        print("Add an override in TYPE_TO_CATEGORY_LEAF, or check /categories/flat manually.")
        sys.exit(1)
    pool.sort(key=lambda t: len(t[1]))
    chosen = pool[0][0]
    return chosen["uuid"], (chosen.get("full_name") or chosen.get("name"))


# ---------------------------------------------------------------------------
# Bootstrap: adopt already-live Reverb listings instead of re-creating them
# ---------------------------------------------------------------------------

def fetch_my_listings():
    """state=all so this also finds drafts, not just published listings."""
    data = api_get("/my/listings?state=all")
    return data.get("listings") or data.get("_embedded", {}).get("listings", [])


def find_reverb_id_for(pedal_name, listings):
    target = pedal_name.strip().lower()
    for l in listings:
        if (l.get("model") or "").strip().lower() == target:
            return l.get("id")
    for l in listings:
        if target in (l.get("title") or "").strip().lower():
            return l.get("id")
    return None


# ---------------------------------------------------------------------------
# Build listing payload
# ---------------------------------------------------------------------------

def build_payload(pedal, condition_uuid, category_uuid):
    reverb_price = reverb_price_for(pedal["site_price"])
    return {
        "make": MAKE,
        "model": pedal["name"],
        "title": f"{MAKE} {pedal['name']}",
        "description": pedal["description"],
        "price": {"amount": f"{reverb_price:.2f}", "currency": "USD"},
        "condition": {"uuid": condition_uuid},
        "categories": [{"uuid": category_uuid}],
        "photos": pedal["photos"],
        "has_inventory": False,
        "handmade": True,
    }, reverb_price


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(INDEX_HTML_PATH):
        print(f"Can't find index.html next to this script ({INDEX_HTML_PATH}).")
        print("Move reverb_sync.py into the root of your jcrews82.github.io folder.")
        sys.exit(1)

    active = load_active_pedals()
    state = load_state()

    # Bootstrap: for any pedal on the site we have no local record of, check
    # whether it's already a live/draft listing on Reverb before assuming
    # it needs to be created (this is what makes the first run safe with
    # listings you already published and hand-fixed).
    new_names = [n for n in active if n not in state]
    adopted = []
    if new_names:
        try:
            existing_listings = fetch_my_listings()
        except Exception as e:
            print(f"Warning: couldn't fetch your existing Reverb listings ({e}).")
            print("Proceeding as if none of the new ones exist yet on Reverb — "
                  "double check for duplicates if you've already listed any by hand.")
            existing_listings = []
        for name in new_names:
            reverb_id = find_reverb_id_for(name, existing_listings)
            if reverb_id:
                pedal = active[name]
                state[name] = {
                    "reverb_id": reverb_id,
                    "site_price": pedal["site_price"],
                    "reverb_price": reverb_price_for(pedal["site_price"]),
                    "description": pedal["description"],
                    "photos": pedal["photos"],
                }
                adopted.append((name, reverb_id))

    to_create, to_update, to_end, unchanged = [], [], [], []

    for name, pedal in active.items():
        prev = state.get(name)
        if prev is None:
            to_create.append(pedal)
        else:
            changed = (
                prev.get("site_price") != pedal["site_price"]
                or prev.get("description") != pedal["description"]
                or prev.get("photos") != pedal["photos"]
            )
            if changed:
                to_update.append(pedal)
            else:
                unchanged.append(name)

    for name, prev in state.items():
        if name not in active:
            to_end.append((name, prev))

    print("=== Plan ===")
    for name, reverb_id in adopted:
        print(f"  ADOPTED {name}  (already on Reverb as id {reverb_id} — just linking it up, no changes sent)")
    for p in to_create:
        print(f"  CREATE  {p['name']}  (site ${p['site_price']:.2f} -> reverb ${reverb_price_for(p['site_price']):.2f})")
    for p in to_update:
        prev = state[p["name"]]
        print(f"  UPDATE  {p['name']}  (site ${prev.get('site_price', 0):.2f} -> ${p['site_price']:.2f}, "
              f"reverb ${prev.get('reverb_price', 0):.2f} -> ${reverb_price_for(p['site_price']):.2f})")
    for name, prev in to_end:
        print(f"  END     {name}  (id {prev.get('reverb_id')}, no longer on the site)")
    if unchanged:
        print(f"  (no changes for: {', '.join(unchanged)})")
    if not (to_create or to_update or to_end):
        print("  Nothing else to do — Reverb already matches the site.")
        save_state(state)  # persist any adoptions even when there's nothing else to do
        return

    answer = input("\nProceed? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted — no creates/updates/ends sent to Reverb.")
        save_state(state)  # still keep any adoptions found above
        return

    condition_uuid = get_condition_uuid()
    categories = get_category_uuid_cache()

    for pedal in to_create:
        category_uuid, category_name = get_category_uuid(categories, pedal["type"])
        payload, reverb_price = build_payload(pedal, condition_uuid, category_uuid)
        print(f"Creating {pedal['name']} (category: {category_name})...")
        result = api_call("/listings", "POST", payload)
        if result is None:
            print(f"  FAILED: {pedal['name']}")
            continue
        # Confirmed real shape from a live create: the id is nested at
        # result["listing"]["id"], not top-level. Top-level "id" and the
        # self-link fallback are kept just in case Reverb ever changes this.
        listing_id = (
            result.get("id")
            or (result.get("listing", {}) or {}).get("id")
        )
        if listing_id is None:
            self_href = ((result.get("_links", {}) or {}).get("self", {}) or {}).get("href", "")
            if self_href:
                listing_id = self_href.rstrip("/").split("/")[-1]
        if listing_id is None:
            print(f"  WARNING: couldn't find an id anywhere in the response for {pedal['name']}.")
            print("  Raw response:")
            print("  " + json.dumps(result, indent=2)[:1500])
        link = (result.get("_links", {}).get("web", {}) or {}).get("href")
        print(f"  Created id={listing_id} {link or ''}")
        state[pedal["name"]] = {
            "reverb_id": listing_id,
            "site_price": pedal["site_price"],
            "reverb_price": reverb_price,
            "description": pedal["description"],
            "photos": pedal["photos"],
        }

    for pedal in to_update:
        prev = state[pedal["name"]]
        listing_id = prev["reverb_id"]
        category_uuid, category_name = get_category_uuid(categories, pedal["type"])
        payload, reverb_price = build_payload(pedal, condition_uuid, category_uuid)
        print(f"Updating {pedal['name']} (id={listing_id})...")
        result = api_call(f"/listings/{listing_id}", "PUT", payload)
        if result is None:
            print(f"  FAILED: {pedal['name']}")
            continue
        print("  Updated.")
        state[pedal["name"]] = {
            "reverb_id": listing_id,
            "site_price": pedal["site_price"],
            "reverb_price": reverb_price,
            "description": pedal["description"],
            "photos": pedal["photos"],
        }

    for name, prev in to_end:
        listing_id = prev.get("reverb_id")
        print(f"Ending {name} (id={listing_id})...")
        result = api_call(f"/my/listings/{listing_id}/state/end", "PUT", {"reason": END_REASON})
        if result is None:
            print(f"  FAILED to end {name} — leaving it in state to retry next run.")
            continue
        print("  Ended.")
        del state[name]

    save_state(state)
    print("\nDone. Log in to Reverb, glance over any new drafts (shipping profile especially), then publish.")


if __name__ == "__main__":
    main()

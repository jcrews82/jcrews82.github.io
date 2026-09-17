# Fuzz Face / Tone Bender Voicing Switch

Only 2 parts actually differ between your two voicings — C1 and R2 — so this only needs a **DPDT ON-ON toggle**, one pole per part. No need for the 4PDT idea from before.

| Part | Position A (stock, as documented) | Position B (alt voicing) |
|---|---|---|
| C1 (input cap) | 1uF | 4.7uF |
| R2 (Q1 collector bias) | 33K | 47K |

## Wiring approach

Don't populate C1 and R2 on the board itself. Instead, break out the two node-pairs they'd normally bridge as flying leads, and dead-bug both values (the stock one and the alt one) directly on the switch's spare lugs — same idea as the 4PDT brainstorm, just half the parts and one smaller, easier-to-find switch.

**Pole 1 (input cap):**
- Common lug → CLEAN_OUT node (the node C1 currently sits on, coming off the Clean pot/wiper side)
- Throw A → 1uF cap → other end to Q1_BASE node
- Throw B → 4.7uF cap → other end to Q1_BASE node
- (Both caps' far leads land on the same Q1_BASE node — the switch just picks which one bridges from Clean.)

**Pole 2 (Q1 bias resistor):**
- Common lug → the supply rail node (R2's current top connection — -9V on the germanium board, +9V on the BC108 board)
- Throw A → 33K resistor → other end to Node_A (Q1 collector / Q2 base)
- Throw B → 47K resistor → other end to Node_A

## Notes

- Works the same way on either board (germanium NKT275 or NPN BC108) — same two nodes get broken out either way, just mind which rail R2 returns to.
- A small pop when flipping mid-signal is normal for this kind of switch — not a fault.
- Mounting: your panel's unused "C" hole (old power-jack reference, ~12mm) is oversized for a mini toggle (which wants ~6-7mm) — either bushing it down or drilling a new small hole in the open space up top (where the eliminated E/H/J/N/O/M positions were) both work.
- Since neither board's PCB footprint needs to change for this (it's flying leads to an off-board switch), this doesn't affect the axial-cap or layout notes already in the other two docs.

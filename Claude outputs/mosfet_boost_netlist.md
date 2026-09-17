# Mosfet Boost (muzique.com) — Schematic Netlist

Traced off the schematic, values confirmed against muzique's own parts list. One transistor (BS170), one external control (GAIN) — everything else is fixed. Target enclosure: **1590B, same as the other three** — standardizing on one enclosure size across the board instead of a separate 1590A. Uses the same shared drilling template: GAIN takes Volume's position (top-left, as this pedal's one main control), Fuzz/Clean/Bias positions are left undrilled.

## Component list

| Ref | Value | Role |
|---|---|---|
| Q1 | BS170 (N-ch MOSFET) | Single-transistor gain stage |
| D1 | 9.1V zener | Gate-source protection (clamps Vgs) |
| D2 | BAT42 (schottky) | Reverse-polarity protection on +9V |
| LED | any | Status LED *(LED/R9/switch wiring isn't shown on this schematic — assuming the same LED→resistor→SW pattern as the other three builds unless you say otherwise)* |
| R1 | 100K | Bias-filter network, parallel with C3 |
| R2 | 62K | Feeds the filtered bias reference from +9V |
| R3 | 10M | Gate bias resistor (filtered reference → gate) |
| R4 | 2.7K | Drain load resistor |
| R5 | 2.7K | Source resistor (sets self-bias) |
| R6 | **5K, C taper (reverse audio)** — GAIN, the one external pot | Variable AC bypass of R5 via C5 — sets gain |
| R7 | 100K | Fixed output load/bleed resistor to ground — **not a pot** |
| R8 | 220R | Input series resistor (with C2, forms input low-pass) |
| R9 | 4.7K | LED current-limiting resistor |
| R10 | 10M | Input pull-down resistor — **not a pot** |
| C1 | 0.1uF | Input coupling cap |
| C2 | 22pF | Input low-pass, with R8 |
| C3 | 10uF electrolytic | Bias-filter cap, parallel with R1 |
| C4 | 0.1uF | Output coupling cap |
| C5 | 100uF electrolytic | In series with R6 (GAIN), AC-bypasses part of R5 |
| C6 | not used | — |
| C7 | 100uF electrolytic | +9V supply filter cap |

**Note on R6**: muzique's own notes say a straight 5K linear pot bunches most of the gain into the last quarter-turn — they specifically recommend a 5K **reverse audio (C) taper** for an evenly-spread sweep, and had Small Bear stock it specially. Save this as **C5K**, not B5K or a plain 5K.

## Full netlist

**GND** — R10 (bottom) · C2 (bottom) · R1 (left end) · C3 (– lead) · C7 (–) · R7 (one terminal, via the jogged wire) · R5 (bottom) · R6 term./wiper (jumpered, bottom)

**+9V (post-diode rail)** — D2 cathode · C7 (+) · R2 (right end) · R4 (top)

**BIAS_FILTER** — R2 (left end) → node with R1 (right end) and C3 (+ lead) *(R1 ∥ C3 between this node and GND, fed through R2 from +9V — a filtered/decoupled reference, not a hard voltage divider to ground)*

**GATE_NODE** — BIAS_FILTER node → R3 → Q1 gate; also: IN → C1 → R8 → GATE_NODE (audio coupling); R10 → GND is the input pull-down, sitting before C1 on the IN side

**INPUT_LP** — R8/GATE_NODE junction → C2 → GND *(R8+C2 form a simple RC low-pass on the input)*

**DRAIN_NODE** — Q1 drain → R4 (bottom) → up to +9V rail; also Q1 drain → C4 → OUT

**OUT_SIG** — C4 → OUT jack tip; OUT also → R7 → GND (fixed load, no pot)

**SOURCE_NODE** — Q1 source → R5 (top) → GND; also Q1 source → C5 (+) → R6 (top terminal) → R6 wiper+bottom (jumpered) → GND

**GATE_SOURCE_PROTECT** — D1 (9.1V zener) bridges GATE_NODE ↔ SOURCE_NODE directly

## Notes for tomorrow's EasyEDA session

- **Enclosure target**: 1590A, not the shared 1590B template — this is its own small standalone build. You're confident it'll fit; add "lay out Mosfet Boost for 1590A" to the to-do list.
- **Pot**: R6 is the only external control — 5K, reverse audio (C) taper. R7 and R10 are fixed resistors, not pots, despite looking similar in size to the pots on the other boards.
- **Silkscreen**: same minimal approach as the other three — polarity marks only, on C3/C5/C7 (electrolytics), D1, D2, LED, and Q1. No ref designators or values.
- **Open item**: the LED/switch wiring isn't shown on the schematic you sent — I assumed it mirrors the other builds (LED → R9 → SW pad, off +9V), but flag it if this circuit's actual LED wiring differs.

This one's simple enough that it might be the fastest of the four to lay out tomorrow.

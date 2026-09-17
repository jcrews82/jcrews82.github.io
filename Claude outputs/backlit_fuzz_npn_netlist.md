# Backlit Fuzz — NPN (BC108) Version — Schematic Netlist

Same circuit as the first Backlit Fuzz, mirrored for NPN silicon transistors (BC108 instead of NKT275). No charge pump needed — BC108 runs straight off +9V/GND instead of a pumped -9V rail, so IC100/D100/C100/C101 are gone entirely. Same BIAS-INT / BIAS-EXT naming convention as the germanium version.

## What's different from the germanium version

- **Q1, Q2**: BC108 (NPN) instead of NKT275 (PNP germanium)
- **No charge pump**: no IC100, no C100/C101 pump caps — R2 and R4 now return to **+9V** instead of -9V
- **Power protection**: D1 (1N5817) sits directly on the +9V line; C6 (47uF) is the supply filter cap (does the job C101 did before, just simpler — no pump to filter)
- **LED resistor** is R10 here (still 4K7) instead of "CLR" — same role
- **C1's polarity is flipped** vs. the germanium version: here C1's (+) faces Q1's base, not the Clean pot side. Worth double-checking against the schematic when you place it, since it's an easy one to get backwards between the two builds.
- Everything else — Clean/Fuzz/Volume values, Bias-Int/Bias-Ext values and wiring, the LED/switch arrangement — is the same topology as the germanium version.
- **All pots are 9mm shortleg PCB-mount pots, no jumper wires anywhere** — same as the germanium version. Clean and Bias-Ext move from on-board trimmer footprints to full 9mm pot footprints; only Bias-Int stays a trimmer.

## Component list

| Ref | Value | Role |
|---|---|---|
| Q1, Q2 | BC108 (NPN silicon) | Fuzz Face-style 2-transistor gain stage |
| D1 | 1N5817 | Reverse-polarity protection, directly on +9V |
| LED | — | Status LED |
| C1 | 1uF electrolytic → **axial** | Input coupling cap ((+) toward Q1 base) |
| C2 | 22uF electrolytic → **axial** | Fuzz pot bypass to ground |
| C3 | 10nF (non-polar) | Output coupling |
| C6 | 47uF electrolytic → **axial** | +9V supply filter cap |
| R1 | 100K | Q2 emitter → Q1 base feedback/bias resistor |
| R2 | 33K | Q1 collector bias resistor, off +9V |
| R3 | 1K | In series with BIAS-INT, part of Q2's collector load |
| R4 | 470R | In series from +9V into the collector-load/output network |
| R10 | 4K7 | LED current-limiting resistor |
| CLEAN | 50K linear, 9mm shortleg PCB-mount pot | Input loading/attenuation control, moved off the on-board trimmer |
| FUZZ | B1K, 9mm shortleg PCB-mount pot | Q2 emitter degeneration + treble-bleed control |
| BIAS-EXT | 5K, 9mm shortleg PCB-mount pot | Part of Q2's collector-load chain (panel's "Bias" knob) |
| BIAS-INT | 5K trimmer | Part of Q2's collector-load chain, fine trim — internal, on-board, no shaft |
| VOLUME | A250K, 9mm shortleg PCB-mount pot | Output level |

## Full netlist

**GND** — IN jack sleeve · Q1 pin 1 (emitter) · FUZZ pot term. 1 · C2 (–) · VOLUME pot term. 1 · OUT jack sleeve · C6 (–) · power jack sleeve ("–" pad)

**+9V** — power "+" pad → D1 anode; D1 cathode → +9V rail → C6 (+) · R2 (top) · R4 (top)

**IN_SIG** — IN jack tip → CLEAN pot wiper (term. 2)

**CLEAN_OUT** — CLEAN pot term. 1 → C1 (–); term. 3 not connected *(CLEAN is a 9mm shortleg PCB-mount pot, no wires)*

**Q1_BASE** — C1 (+) → Q1 pin 2 (base) → R1 (left terminal)

**Q1_COLL / Q2_BASE** (direct-coupled node) — Q1 pin 3 (collector) → R2 (bottom) → Q2 base

**Q2_COLL** — Q2 collector → R3 (bottom terminal)

**BIAS_NODE** — R3 (top) → BIAS-INT term. 3, jumpered to wiper (term. 2)

**TAP_NODE** — BIAS-INT term. 1 → BIAS-EXT term. 1 → BIAS-EXT term. 3, jumpered to wiper (term. 2) → R4 (bottom) → C3 (left lead)

**Q2_EMIT** — Q2 emitter → R1 (right terminal) → FUZZ pot term. 3

**FUZZ_WIPER** — FUZZ pot wiper (term. 2) → C2 (+)

**OUT_COUPLED** — C3 (right lead) → VOLUME pot term. 3 (top)

**OUT_SIG** — VOLUME pot wiper (term. 2) → OUT jack tip

**LED_SIG** — LED cathode → junction with D1 anode/"+" pad; LED anode → R10 → SW pad

---

## Notes for tomorrow's EasyEDA session

- **Silkscreen**: minimal — no ref designators, no values, no logo text. Just polarity marks on the electrolytic caps, D1, the LED, and Q1/Q2.
- **Caps**: C1, C2, and C6 go from radial (box/can) to **axial** (in-line leads) footprints.
- **Transistor footprints**: BC108 is a much smaller package than the NKT275 germanium cans — you asked to use that reclaimed space to **lay Q1/Q2 down flat** (horizontal, on their side) instead of standing them upright. I'll leave the actual placement to EasyEDA tomorrow rather than guess at spacing again, but wanted this captured so it's not lost overnight.
- Board size, power-corner placement, and the pot split (Volume/Fuzz/Clean/Bias-Ext all 9mm shortleg PCB-mount, Bias-Int stays a trimmer) all carry over from the germanium version's notes.
- **One shared template**: all three pedals — this one, the germanium version, and the Range/Boost booster — now use the same 1.95×1.45in enclosure and the same 4-hole drilling template.
- **Volume is always top-left**, on every pedal. On the panel, Volume (D) is top-left and Fuzz (F) is top-right — the opposite of how PedalPCB's stock reference board silkscreened them. Mirror Volume/Fuzz left-right from the stock image when placing in EasyEDA.

Same net-by-net approach tomorrow whenever you're ready.

# Range/Boost Germanium Booster — Schematic Netlist

Traced directly off the PedalPCB schematic, pin by pin. Single germanium transistor (CV7112), no charge pump — runs straight off +9V/GND. Changes from stock: electrolytic caps go radial → axial, BIAS moves from an on-board trimmer to a full pot, and **every pot on this board — Range, Boost, and Bias — is a 9mm shortleg PCB-mount pot, no jumper wires anywhere.**

**Board size is now the same as the two fuzz boards — 1.95in × 1.45in — instead of the stock 1.95in × 1.15in**, so this build can reuse the exact same enclosure and drilling template as the fuzz pedals: one template for all three. Range and Boost occupy two of the template's four knob positions, Bias takes the standard Bias position (no more need for the offset hole under Fuzz), and the Clean position is simply left undrilled on this build.

Mapping: **Boost → Volume's position (top-left)** — Boost is this pedal's output-level control, so it follows the "Volume always top-left" rule. **Range → Fuzz's position (top-right)** — Range acts like a tone control here.

## Component list

| Ref | Value | Role |
|---|---|---|
| Q1 | CV7112 (PNP germanium) | Single-transistor gain stage |
| D1 | 1N5817 | Reverse-polarity protection |
| LED | — | Status LED |
| R1 | 1M | Input bleed resistor to ground |
| R2 | 470K | Base bias (+9V side of the divider) |
| R3 | 68K | Base bias (ground side of the divider) |
| R4 | 1M | Output bleed resistor to ground |
| R6 | 4K7 | LED current-limiting resistor *(no R5 in this design — not a typo)* |
| C2 | 5n (non-polar) | Fixed input coupling cap, IN → base |
| C3 | 22uF electrolytic → **axial** | Bias trimmer bypass cap, at Q1's emitter |
| C4 | 10n (non-polar) | Output coupling cap, Boost wiper → OUT |
| C6 | 47uF electrolytic → **axial** | +9V supply filter cap |
| C7 | 2u2 electrolytic → **axial** | Range control coupling cap, in series with the Range pot |
| RANGE | B100K, 9mm shortleg PCB-mount pot | Blends a variable low-end path (via C7) in parallel with the fixed C2 high-pass |
| BOOST | A10K, 9mm shortleg PCB-mount pot | Variable tap on Q1's collector load — sets output level/gain |
| BIAS | 5K, 9mm shortleg PCB-mount pot | Sets Q1's emitter bias point — moved off the on-board trimmer to a full pot |

## Full netlist

**GND** — IN jack sleeve · OUT jack sleeve · R1 (bottom) · R3 (bottom) · R4 (bottom) · BIAS pot term. 1, jumpered to wiper (term. 2) · C6 (–)

**+9V** — supply arrow · D1 cathode · C6 (+) · R2 (top) · BOOST pot term. 1

**IN_NODE** — IN jack tip → R1 (top) → C2 (bottom lead) → RANGE pot term. 1, jumpered to wiper (term. 2)

**BASE_BIAS** (Q1 base) — C2 (top lead) → Q1 base → R2 (bottom) → R3 (top) → C7 (+ lead)

**RANGE_PATH** — C7 (– lead) → RANGE pot term. 3 *(this is the variable-resistor-plus-cap path that parallels C2 — this is what the Range control actually adjusts)*

**Q1_COLL** — Q1 collector → BOOST pot term. 3

**BOOST_TAP** — BOOST pot wiper (term. 2) → C4 → node with R4 (top) → OUT jack tip

**Q1_EMIT** — Q1 emitter → BIAS pot term. 3 → C3 (+)

*(BIAS pot: term. 3 = Q1 emitter node; term. 1 jumpered to wiper term. 2 = ground — so it's a simple variable resistor from Q1's emitter to ground, bypassed by C3. Same wiring as before, just a 9mm shortleg PCB-mount pot instead of a trimmer footprint — no wires.)*

**LED_SIG** — SW pad → R6 → LED anode; LED cathode → junction with D1 anode → "+" power pad

## Notes

- **Silkscreen**: minimal — no ref designators, no values, no logo text. Just polarity marks on C3/C6/C7, D1, the LED, and Q1.
- **Pots**: Range, Boost, and Bias are all 9mm shortleg PCB-mount pots, no jumper wires anywhere. Bias's electrical nodes and jumper wiring (term. 1 to wiper) don't change, it just moves from a trimmer footprint to a full 9mm pot footprint — the board needs to be shaped so all three shafts line up with their panel holes.
- C2 and C4 are non-polarized (film/ceramic), so they're unaffected by the radial→axial request — that only applies to C3, C6, and C7.
- **Board size**: 1.95in × 1.45in, matching the fuzz boards — extended from the stock 1.15in depth specifically so all three pedals share one enclosure and one drilling template.
- **Panel plan**: same 4-hole template as the fuzz builds (Volume/Fuzz/Clean/Bias positions). Boost populates Volume's position (top-left, as the output-level control), Range populates Fuzz's position (top-right, acting as a tone control), Bias populates the standard Bias position, and Clean's position is left undrilled for this pedal.

This one's simpler than the fuzz — same net-by-net approach tomorrow in EasyEDA whenever you're ready for it.

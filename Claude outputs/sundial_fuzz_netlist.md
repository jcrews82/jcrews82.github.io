# Backlit Fuzz — Schematic Netlist

Traced directly off the PedalPCB schematic, pin by pin. Renamed the two bias-network controls to avoid confusion (and to drop the Analogman-associated "Sundial" name): **BIAS-INT** and **BIAS-EXT**, both 5K.

| Control | Value | Form |
|---|---|---|
| CLEAN | 50K | on-board trimmer stock → **9mm shortleg PCB-mount pot**, board positioned so the shaft lines up with the panel hole |
| BIAS-EXT *(was "Sundial")* | 5K | on-board trimmer stock → **9mm shortleg PCB-mount pot** — this is the pot behind your panel's "Bias" knob |
| BIAS-INT *(was "Bias")* | 5K | on-board trimmer → **stays internal**, on-board trimmer (no shaft, no panel hole) |

All pots on this board — Volume, Fuzz, Clean, and Bias-Ext — are **9mm shortleg PCB-mount pots**. No jumper wires anywhere: each pot solders straight to the board, and the board itself is positioned/shaped so every shaft lines up with its panel hole. Only BIAS-INT is a trimmer with no shaft.

## Component list

| Ref | Value | Role |
|---|---|---|
| Q1, Q2 | NKT275 (PNP germanium) | Fuzz Face-style 2-transistor gain stage |
| IC100 | TC1044SCPA | Charge pump, generates the -9V rail |
| D100 | 1N5817 | Reverse-polarity protection on incoming power |
| LED | — | Status LED |
| C1 | 1uF electrolytic | Input coupling cap (**your customization point** — value you swap for Fuzz Face vs. Tonebender voicing) |
| C2 | 22uF electrolytic | Fuzz pot bypass to ground |
| C3 | 10nF (non-polar) | Output coupling |
| C100 | 10uF electrolytic | Charge-pump flying capacitor (IC100 pins 2/4) |
| C101 | 47uF electrolytic | -9V rail filter cap |
| R1 | 100K | Q2 emitter → Q1 base feedback/bias resistor |
| R2 | 33K | Q1 collector bias resistor, off the -9V rail |
| R3 | 1K | In series with BIAS-INT, part of Q2's collector load |
| R4 | 470R | In series from -9V into the collector-load/output network |
| CLR | 4K7 | LED current-limiting resistor |
| CLEAN | 50K linear, 9mm shortleg PCB-mount pot | Input loading/attenuation control |
| FUZZ | B1K, 9mm shortleg PCB-mount pot | Q2 emitter degeneration + treble-bleed control |
| BIAS-EXT | 5K, 9mm shortleg PCB-mount pot | Part of Q2's collector-load chain (panel's "Bias" knob) |
| BIAS-INT | 5K trimmer | Part of Q2's collector-load chain, fine trim — internal, on-board, no shaft |
| VOLUME | A250K, 9mm shortleg PCB-mount pot | Output level |

## Full netlist

**GND** — IN jack sleeve · Q1 emitter · FUZZ pot terminal 1 · C2 (–) · VOLUME pot terminal 1 · OUT jack sleeve · C101 (–) · IC100 pin 3 · power jack sleeve ("–" pad)

**V+RAW** (raw incoming supply, pre-diode) — power "+" pad · D100 anode · LED anode

**V+REG** (protected supply feeding the charge pump) — D100 cathode · IC100 pin 1 (BOOST) · IC100 pin 8 (V+)

**PUMP_CAP** — IC100 pin 2 ↔ C100 (+) ... IC100 pin 4 ↔ C100 (–) *(C100 is the pump flying cap across pins 2/4, not a supply filter cap)*

**-9V** (pumped rail) — IC100 pin 5 · C101 (+) · R2 top · R4 top

**IC100 pins 6 (OSC) and 7 (LV)** — not connected, per standard TC1044 application

**LED_SIG** — LED cathode → CLR → SW pad (footswitch lug; lights the LED when the switch grounds this line)

**IN_SIG** — IN jack tip → CLEAN pot wiper (term. 2) *(CLEAN is a 9mm shortleg PCB-mount pot, no wires)*

**CLEAN_OUT** — CLEAN pot term. 1 → C1 (+); term. 3 not connected

**Q1_BASE** — C1 (–) → Q1 base → R1 (left terminal)

**Q1_COLL / Q2_BASE** (direct-coupled node) — Q1 collector → R2 (bottom) → Q2 base

**Q2_COLL** — Q2 collector → R3 (bottom terminal)

**BIAS_NODE** — R3 (top) → BIAS-INT term. 3, jumpered to wiper (term. 2) *(BIAS-INT stays on-board)*

**TAP_NODE** — BIAS-INT term. 1 → BIAS-EXT term. 1 → BIAS-EXT term. 3, jumpered to wiper (term. 2) → R4 (bottom) → C3 (left lead) *(BIAS-EXT is a 9mm shortleg PCB-mount pot behind the "Bias" knob — no wires)*

**Q2_EMIT** — Q2 emitter → R1 (right terminal) → FUZZ pot term. 3

**FUZZ_WIPER** — FUZZ pot wiper (term. 2) → C2 (+)

**OUT_COUPLED** — C3 (right lead) → VOLUME pot term. 3 (top)

**OUT_SIG** — VOLUME pot wiper (term. 2) → OUT jack tip

---

## Notes for tomorrow's EasyEDA session

- **Silkscreen**: minimal — no ref designators, no values, no logo text. Just polarity marks on the electrolytic caps, D100, the LED, and Q1/Q2, plus a pin-1/orientation mark for IC100.
- **Board size**: match the reference layout exactly — **1.95in × 1.45in** (49.53mm × 36.83mm).
- **Power connections** (IN/GND/SW/OUT breakout, and the +/– power pads): move to the **bottom-left corner** of the board instead of the bottom-center strip on the reference layout.
- **Caps**: swap C1, C2, C100, C101 from radial (box/can) footprints to **axial** (in-line leads) footprints.
- **Pots**: Volume, Fuzz, Clean, and Bias-Ext are all **9mm shortleg PCB-mount pots** — no jumper wires anywhere. Clean and Bias-Ext move from on-board trimmer footprints to full 9mm pot footprints; the board has to be shaped/sized so all four shafts line up with their panel holes. BIAS-INT (5K) stays as the one on-board trimmer with no shaft.
- **Layout**: center everything on the board once the Clean and Bias-Ext trimmer footprints are swapped for full-size pot footprints, rather than leaving gaps or misalignment.
- **Panel mapping reminder** (from BACKLITTEMPLATE): the panel's 4 knob positions are Volume, Fuzz, Clean, and "Bias" — that last one is wired electrically to BIAS-EXT, not to the on-board BIAS-INT trimmer.
- **Volume is always top-left**, on every pedal — that's the rule going forward. On your drilled panel, Volume (D) is already the top-left position and Fuzz (F) is top-right, which is the *opposite* of how PedalPCB's stock reference board silkscreened them (their layout shows Fuzz top-left, Volume top-right). When placing parts in EasyEDA, follow the panel's convention, not the stock image's — mirror Volume/Fuzz left-right from how the reference board drew them.
- **One shared template**: the Range/Boost board now uses this same 1.95×1.45in size and the same 4-hole template (Range/Boost take two positions, Bias takes the Bias spot, Clean's hole is left undrilled on that build) — so all three pedals share one enclosure and one drilling template.

This has every net and the naming now matches how you actually think about the two bias controls. Bring it up next to EasyEDA tomorrow and we'll go net-by-net.

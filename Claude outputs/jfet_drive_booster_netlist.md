# JFET Drive Booster ("Buffered Mini-Booster" + AMZ Drive mod) — Schematic Netlist

Confirmed this is the AMZ FX Mini-Booster (buffered version) — the Drive-control add-on diagram you just sent is muzique/AMZ's own official mod for this exact circuit, so we're building it to spec. Two J201 JFETs (Q1 gain stage, Q2 wired as a JFET active-load/current-source for Q1), one 2N3904 (Q3, emitter-follower output buffer), and now **two pots**: DRIVE (100K audio, new — input pad ahead of the board) and LEVEL/R9 (100K audio, output). Plus the C3-on-a-switch gain mod, which you've already bench-tested and confirmed sounds great.

## What changed from the first pass

- **Added DRIVE pot (100K audio taper)**, wired exactly per the muzique diagram: IN jack tip → Drive pot lug A; Drive pot lug B → GND; **Drive pot wiper → the board's existing IN node** (same node R1/C1 already land on). So the jack no longer feeds R1/C1 directly — it feeds the Drive pot, and the wiper feeds the board. Everything downstream of that node (R1, C1, Q1 gate network) is unchanged.
- **R9 (Level) confirmed at 100K audio taper** (not the 10K–100K range I noted before) — matches the Drive pot value per the AMZ note, so both knobs are the same pot value/taper.
- **C3-on-a-switch**: simplified to a plain SPST on/off for now — just the one 10uF value you've already bench-tested, no second footprint. If tomorrow's testing has you wanting a second cap value, tell me and I'll add the second footprint plus the 3-lug on/off/on switch back into the layout — easy to do whenever you're ready, no need to plan for it now.
- **Transistors going SMD**: Q1, Q2 (J201) and Q3 (2N3904) as SMD parts. Flagging this clearly: J201 doesn't have one universally standardized SOT-23 pinout across manufacturers the way TO-92 does — before I lock in the SMD footprint orientation, I need the exact part/pinout you're sourcing (e.g. which vendor's SMD J201, or a specific datasheet) so the footprint isn't guessed. Same goes for the 2N3904 SMD equivalent (commonly MMBT3904, SOT-23, pinout is standardized for that one so less of a concern).
- **Everything else stays through-hole**, per your list: all resistors, the electrolytics as axial (C3, C4, C6), the film/small caps (C1, C5 — and C2 at 22pF, which is small enough that ceramic/C0G may be more practical than true film; flagging that in case "film caps" was meant to exclude it), D1, LED, and both pots as 9mm PCB-mount.

## Component list

| Ref | Value | Package | Role |
|---|---|---|---|
| Q1 | J201 (N-ch JFET) | **SMD** | Gain stage |
| Q2 | J201 (N-ch JFET) | **SMD** | Active-load / current-source for Q1 |
| Q3 | 2N3904 (NPN) | **SMD** | Emitter-follower output buffer |
| D1 | BAT42 (schottky) | Through-hole | Reverse-polarity protection |
| LED | any | Through-hole | Status LED (wiring assumption below) |
| R1 | 2.2M | Through-hole | Bleed resistor on the (now Drive-pot-fed) input node |
| R2 | 2.2M | Through-hole | Q1 gate bias/pulldown |
| R3 | 1K | Through-hole | Q1 source resistor (self-bias) |
| R4 | 10K | Through-hole | Q3 emitter resistor |
| R6, R7 | 1M each | Through-hole | Q2 gate bias divider |
| R8 | 4.7K (select) | Through-hole | LED current-limiting resistor |
| DRIVE | 100K audio taper, 9mm PCB-mount pot | Through-hole | Input pad ahead of the board (new) |
| LEVEL (R9) | 100K audio taper, 9mm PCB-mount pot | Through-hole | Output level |
| C1 | 0.1uF | Through-hole (film) | Input coupling |
| C2 | 22pF | Through-hole (ceramic likely) | Q1 gate HF bypass |
| C3 | 10uF → axial | Through-hole | Q1 source bypass — on a simple on/off switch |
| C4 | 10uF → axial | Through-hole | Q2 gate-to-source AC bypass |
| C5 | 1.0uF | Through-hole (film) | Output coupling |
| C6 | 100uF → axial | Through-hole | Supply filter |

## Full netlist

**GND** — DRIVE pot lug B · R1 (bottom) · R2 (bottom) · C2 (bottom) · R3 (bottom) · C3 (– lead, via the bypass switch) · R7 (bottom) · R4 (bottom) · LEVEL pot term. 2 (bottom) · C6 (–) · power jack sleeve

**+9V_RAW** — power "+" pad → D1 anode; also → R8 (feeds LED branch ahead of the protection diode)

**VCC_REG** (after D1) — D1 cathode → C6 (+) · R6 (top) · Q2 drain · Q3 collector

**LED_NODE** — R8 (other end) → LED anode *(assumption carried over: cathode → SW pad, matching your other builds — flag if different)*

**IN_JACK** — 3PDT bottom-center lug (the bypass pole's engaged-side throw) → DRIVE pot lug A *(the true-bypass switch sits ahead of the Drive pot, not the input jack directly — so bypassing the pedal takes the Drive pot out of the path too, which is the correct behavior for true bypass)*

**IN_SIG** (board's original input node) — DRIVE pot wiper = R1 (top) → C1 (one lead)

**GATE2_BIAS** — R6 (bottom) = R7 (top) = Q2 gate = C4 (– lead)

**DRIVE_NODE** — Q2 source = Q1 drain = C4 (+ lead) = Q3 base

**N1** (Q1 gate node) — C1 (other lead) = R2 (top) = C2 (top) = Q1 gate

**Q1_SOURCE** — Q1 source = R3 (top) = C3 (+ lead)

**BYPASS_SWITCH** — simple on/off (SPST), in series with C3's ground leg: C3 (– lead) → switch → GND. Off = C3 disconnected (stock voicing), on = C3 engaged (bypasses R3, more gain) — this is the mod you've already bench-tested and confirmed sounds great.

**Q3_EMIT** — Q3 emitter = R4 (top) → C5 (one lead)

**OUT_COUPLED** — C5 (other lead) → node "A" → LEVEL pot term. 1 (top)

**OUT_SIG** — LEVEL pot wiper (term. 3) → OUT jack tip

## Panel mapping — this one uses all four positions

Nice side effect of adding the Drive pot: this board now fills the whole shared template, same as the fuzz boards.

- **LEVEL → Volume's position (top-left)** — it's the output-level control, so it follows the standing rule.
- **DRIVE → Fuzz's position (top-right)** — the character/gain-shaping control, same role Fuzz plays on the fuzz boards.
- **Switch → Bias's position (bottom-right, under Fuzz/Drive)** — the C3 bypass on/off/on toggle.
- **LED → Clean's position (bottom-left, under Volume/Level)**.

One open item for the switch specifically: your other controls are all 9mm PCB-mount pots with no jumper wires. Toggle switches aren't as commonly available in a PCB-mount format lining up to a panel hole the way pots are — do you want me to look for a PCB-mount mini toggle that can sit in that position with no wires (matching your pot rule), or are you fine wiring this one switch with short leads (similar to how the footswitch is already wire-mounted rather than PCB-mounted)? Let me know and I'll lock in the footprint choice.

Also still open: the exact SMD J201 part/pinout you're sourcing, so I don't guess a footprint orientation that turns out backwards.

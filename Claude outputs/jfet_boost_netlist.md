# JFET Boost (J309) — Schematic Netlist

Traced off the PedalPCB schematic, pin by pin. One transistor (J309 N-channel JFET), three controls: Input (loading), Level (output), and Bias (internal trimmer — adjust while measuring the drain until it reads ~7.0VDC, per the board's own silkscreen note). Per your call: **axial caps instead of radial, bigger/standard resistor footprints for easier hand-soldering, and a cleaner layout overall** — noted below for tomorrow.

## Component list

| Ref | Value | Role |
|---|---|---|
| Q1 | J309 (N-ch JFET) | Single-transistor gain stage |
| D100 | 1N5817 | Reverse-polarity protection on incoming power |
| LED | — | Status LED |
| C1 | 100n (non-polar) | Input coupling cap |
| C2 | 100p (non-polar) | Treble bleed around the Input pot, straight to the gate |
| C3 | 4u7, **non-polarized/bipolar electrolytic** → axial | Drain-to-Level coupling cap — marked (+) on both leads on the schematic, so this is a bipolar electrolytic, not a standard polarized one. Worth sourcing the right part, not just any axial cap. |
| C4 | 10uF electrolytic → **axial** | Source bypass, in series with R4 |
| C100 | 100uF electrolytic → **axial** | VCC filter cap |
| C101 | 100n (non-polar) | VCC filter cap (high-frequency) |
| R1 | 1M5 | Input pot's ground-leg resistor |
| R2 | 1M | Input pot wiper → gate |
| R3 | 5K6 | Source resistor, sets DC bias |
| R4 | 100R | In series with C4, source bypass path |
| CLR | 4K7 | LED current-limiting resistor |
| INPUT | B2M pot, 9mm shortleg PCB-mount | Input loading/level control |
| LEVEL | B10K pot, 9mm shortleg PCB-mount | Output level |
| BIAS | 20K trimmer | Sets Q1's drain voltage (~7.0VDC) — internal, on-board, no shaft |

## Full netlist

**GND** — IN jack sleeve · OUT jack sleeve · R1 (bottom) · R3 (bottom) · C4 (–) · C100 (–) · C101 · LEVEL pot term. 1 · INPUT pot's R1 leg · power jack sleeve ("–" pad) · SWGND's second pad

**VCC** — power "+" pad → D100 anode; D100 cathode → VCC rail → C100 (+) · C101 · BIAS pot term. 3

**IN_SIG** — IN jack tip → C1 → N1 (junction)

**N1** — C1 (other lead) → INPUT pot term. 3 (top); also → C2 (one lead)

**INPUT_GND_LEG** — INPUT pot term. 1 (bottom) → R1 → GND

**INPUT_WIPER** — INPUT pot wiper (term. 2) → R2 → GATE_NODE

**GATE_BYPASS** — C2 (other lead) → GATE_NODE *(bypasses the Input pot for treble content — same node R2 lands on)*

**GATE_NODE** — R2 and C2 both land here → Q1 gate

**BIAS_DRAIN** — BIAS pot term. 1, jumpered to wiper (term. 2) → TP1 (test point) → Q1 drain *(BIAS term. 3 = VCC — so it's a variable resistor from VCC down to the drain, setting drain voltage)*

**DRAIN_NODE** — Q1 drain → C3 (+ lead)

**OUT_COUPLED** — C3 (– lead) → LEVEL pot term. 3 (top)

**OUT_SIG** — LEVEL pot wiper (term. 2) → OUT jack tip

**SOURCE_NODE** — Q1 source → R3 (top) → GND; also Q1 source → R4 → C4 (+) → GND

**LED_SIG** — LED anode → junction with D100 anode/"+" pad; LED cathode → CLR → SWGND pad

## Notes for tomorrow's EasyEDA session

- **Board size**: staying at the reference 1.95in × 1.65in — this one doesn't need to match the fuzz boards' 1.45in depth, since that constraint was to leave clearance for a 9V battery and this build doesn't need one. The larger board eats into where the footswitch would sit on the shared panel layout, but that's fine — the footswitch mounts to the panel itself and wires over, it's not a PCB-mounted part here, so there's no physical conflict.
- **Panel**: still the same 1590B, and still uses the shared template's **top two knob positions** (Volume/Fuzz spots) — LEVEL takes Volume's position (top-left, as the output-level control, per the "Volume always top-left" rule), INPUT takes Fuzz's position (top-right). Clean and Bias's panel positions aren't used on this build — BIAS here is the internal trimmer, not panel-mounted.
- **Caps**: C3, C4, and C100 go from radial (box/can) to **axial** (in-line leads). C3 specifically needs a **non-polarized/bipolar** electrolytic — it's marked (+) on both ends on the schematic, so don't just grab a standard polarized axial cap for it.
- **Resistors**: bigger/standard-size axial resistor footprints (not the tiny ones on the reference board) for easier hand-soldering.
- **Layout**: general request for a cleaner, less cramped placement than the stock reference — nothing specific pinned down yet, just the overall direction for tomorrow.
- **Pots**: INPUT and LEVEL are both 9mm shortleg PCB-mount, consistent with the other boards. BIAS stays an internal trimmer with no shaft (adjust-to-voltage, not knob-accessible).
- **Silkscreen**: same minimal approach as the others — polarity marks only, on C3/C4/C100, D100, the LED, and Q1. No ref designators or values. Though you may want to keep some version of the "ADJUST BIAS TO X.XVDC" note, since that's actually functional info, not just decoration — your call.

This one's the simplest of the bunch — should be quick work tomorrow.

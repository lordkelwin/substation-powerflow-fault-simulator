# 3D Substation Power Flow, Short-Circuit, Protection Coordination & Power Quality Simulator

Interactive Three.js WebGL electrical substation simulator designed for EE 415 (Distribution Systems & Substation Design).

## Features
- **5 Busbar Topologies:** Single Bus (`1.0 CB`), Main & Transfer Bus (`1.25 CB`), Ring Bus (`1.0 CB`), Breaker-and-a-Half (`1.5 CB`), and Double Bus–Double Breaker (`2.0 CB`).
- **3 Enclosure Cases & 3 Voltage Classes:** Outdoor AIS, SF₆ GIS Hall, and Indoor Metal-Clad Switchgear across `69 / 13.8 kV`, `138 / 69 kV`, and `230 / 138 kV`.
- **Dynamic Land Area Calculator:** Real-time civil site dimensions (`m²` and hectares) and 3D perimeter placards across all 45 scheme × enclosure × voltage combinations.
- **Interactive SLD, Switching Interlocks & LOTO Drills (A–E):** Synchronized 2D/3D switching with IEEE/ANSI interlock protection and first-person field walk mode with IEEE C2 MAD proximity hazard detection.
- **Engineering Analysis Labs:** Per-Unit Power Flow & Voltage Drop, Symmetrical Component Pinpoint Fault Injection, Complete Protective Relay Settings Schedule (`ANSI 21/50/51/51N/51G/67/79/87B/87T`), Interactive Log-Log TCC Coordination Viewer (`IEEE Std C57.109` & CTI), and 3-Phase Power Quality / Oscilloscope Lab.

## Usage & Build
Open `substation_simulator.html` (or `index.html`) directly in any modern browser, or rebuild from the modular Python builder sources:

```bash
python generate_simulator.py
```

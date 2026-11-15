"""
sim_data.py
Engineering specifications, failure modes, checklists, exploded sub-part definitions,
and OBE quiz questions for EE 415 3D Substation Simulator.
"""

def get_js_data():
    return """
    const SUBSTATION_DATA = {
      transformer: {
        id: 'transformer',
        name: 'Main Step-Down Power Transformer (TR-01)',
        tag: 'TR-01',
        ansiNumber: '87T / 63 / 49 / 26',
        governingStandard: 'IEEE Std C57.12.00 / PEC 2017 Part 2',
        overview: 'Three-phase mineral oil-immersed step-down power transformer serving as the primary bulk substation power conversion unit, stepping 69 kV sub-transmission voltage down to 13.8 kV medium-voltage distribution.',
        specs: [
          { k: 'Rated Capacity (Base ONAN)', v: '25.0 MVA' },
          { k: 'Stage 1 Forced Air (ONAF1)', v: '33.3 MVA' },
          { k: 'Stage 2 Forced Air (ONAF2)', v: '41.7 MVA' },
          { k: 'Primary Rated Voltage (HV)', v: '69.0 kV Delta (3-wire)' },
          { k: 'Secondary Rated Voltage (LV)', v: '13.8 kV Grounded-Wye (4-wire)' },
          { k: 'Vector Group', v: 'Dyn11 (30° LV lagging phase shift)' },
          { k: 'Percentage Impedance (%Z)', v: '8.00% @ 25 MVA base' },
          { k: 'X/R Ratio', v: '18.0' },
          { k: 'Basic Impulse Level (BIL)', v: 'HV: 350 kV / LV: 110 kV' },
          { k: 'Cooling Class', v: 'ONAN / ONAF1 / ONAF2' },
          { k: 'Full-Load Current (69 kV)', v: '348.9 A @ 41.7 MVA' },
          { k: 'Full-Load Current (13.8 kV)', v: '1,744.7 A @ 41.7 MVA' },
          { k: 'No-Load Core Loss (P_nl)', v: '18.5 kW' },
          { k: 'Full-Load Winding Loss (P_fl)', v: '112.0 kW' },
          { k: 'Total Efficiency @ Full Load', v: '99.48%' }
        ],
        failureModes: [
          { title: 'Thermal Insulation Breakdown & Paper Aging', desc: 'Cellulose kraft insulation depolymerizes when winding hot-spot temperature exceeds 110°C, lowering dielectric withstand and generating CO/CO2 dissolved gases (DGA).' },
          { title: 'Dissolved Gas Analysis (DGA) Key Gases', desc: 'Arcing produces Acetylene (C2H2); high-temperature thermal faults produce Ethylene (C2H4); partial discharge produces Hydrogen (H2). Monitored via Buchholz relay and gas sampling.' },
          { title: 'Through-Fault Electromechanical Winding Deformation', desc: 'Extreme short-circuit electromagnetic repulsion forces (F ∝ I_sc²) cause radial buckling and axial tilting of transformer windings, leading to internal turn-to-turn flashovers.' },
          { title: 'Silica Gel Breather Saturation', desc: 'Moisture ingress lowers mineral oil dielectric breakdown strength below 30 kV/2.5mm, causing catastrophic internal bushing and winding flashovers.' }
        ],
        checklist: [
          'Verify silica gel crystals in breather: deep cobalt blue (dry) vs. pink/white (moisture saturated, immediate replacement required).',
          'Inspect oil level sight glass in conservator tank against ambient temperature calibration curve (-20°C to +40°C).',
          'Execute infrared (IR) thermography survey on HV/LV bushing terminal palm clamps to detect high-resistance hot spots (>5°C ΔT above ambient).',
          'Verify Buchholz relay gas accumulation sight glass for combustible gases and confirm trip/alarm float contact continuity.',
          'Test Pressure Relief Device (PRD) mechanical flag indicator and directional oil diverter pipe.',
          'Audit dual-stage forced-air cooling fan banks and thermostatic starting relays.'
        ],
        subparts: [
          { id: 'tx-hv-bushings', name: '69 kV HV Porcelain Condenser Bushings', tag: 'HV-BUSH', material: 'Glazed C130 Porcelain / Oil-Impregnated Paper Core', role: 'Provides high-dielectric insulated pass-through for 69 kV primary phase conductors with grading foil capacitors.', vector: [0, 4.2, 0] },
          { id: 'tx-lv-bushings', name: '13.8 kV LV Bushings & Neutral (X0)', tag: 'LV-BUSH', material: 'Wet-Process Porcelain / Cast Bronze Studs', role: 'Carries up to 1,745 A secondary current with X0 solidly bonded to substation ground grid.', vector: [0, 3.2, 2.5] },
          { id: 'tx-conservator', name: 'Conservator Tank & Silica Gel Breather', tag: 'CONSERV', material: 'Welded Carbon Steel / Desiccant Dehydrating Chamber', role: 'Accommodates thermal oil expansion and contraction while dehydrating inhaled atmospheric air.', vector: [0, 2.8, -3.2] },
          { id: 'tx-buchholz', name: 'Buchholz Gas & Surge Relay (ANSI 63)', tag: 'BUCH-63', material: 'Cast Bronze Housing / Mercury/Reed Float Switches', role: 'Detects internal slow gas accumulation (alarm) and violent oil surge waves from heavy internal arcing (trip).', vector: [-1.8, 2.2, -1.8] },
          { id: 'tx-core', name: 'CRGO Laminated Silicon Steel Core', tag: 'CRGO-CORE', material: 'Cold-Rolled Grain-Oriented Laminated Steel (0.27mm)', role: 'Provides high-permeability, low-hysteresis magnetic flux path forming a 3-phase 3-limb structure.', vector: [0, 0, 0] },
          { id: 'tx-windings', name: 'HV Delta & LV Grounded-Wye Windings', tag: 'WINDINGS', material: 'Oxygen-Free Electrolytic Copper / Thermally Upgraded Paper', role: 'Electromagnetic power transformation with Dyn11 vector configuration and pressboard oil cooling ducts.', vector: [0, 0.5, 0] },
          { id: 'tx-oltc', name: 'On-Load Tap Changer (OLTC) Mechanism', tag: 'OLTC', material: 'Vacuum Interrupter Diverter / Geneva Mechanism Drive', role: 'Regulates secondary voltage ±10% in 16 or 32 steps (1.25% or 0.625% per step) under full load current.', vector: [3.8, 0, 0] },
          { id: 'tx-radiators', name: 'Radiator Cooling Bank & Electric Fans', tag: 'RAD-BANK', material: 'Pressed Steel Cooling Elements / Axial Aerofoil Fans', role: 'Dissipates 130.5 kW full-load losses through natural convection (ONAN) and dual forced-air stages (ONAF1/2).', vector: [-4.2, 0, 0] },
          { id: 'tx-tank', name: 'Main Steel Tank & Pressure Relief Valve', tag: 'MAIN-TANK', material: 'Reinforced Structural Steel Plate / Mineral Insulating Oil', role: 'Hermetic oil reservoir, mechanical containment, and spring-loaded pressure relief device (PRD).', vector: [0, -1.8, 0] }
        ]
      },

      breaker: {
        id: 'breaker',
        name: '69 kV SF6 Dead-Tank Circuit Breaker (CB-69-1)',
        tag: 'CB-69-1',
        ansiNumber: '52',
        governingStandard: 'IEEE Std C37.04 / IEEE Std C37.06 / IEC 62271-100',
        overview: 'Three-phase high-voltage sulfur hexafluoride (SF6) gas outdoor circuit breaker designed for high-speed interruption of continuous full-load currents and severe symmetrical/asymmetrical short-circuit faults up to 31.5 kA within 3 cycles (50 ms).',
        specs: [
          { k: 'Rated Maximum Voltage', v: '72.5 kV RMS' },
          { k: 'Rated Continuous Current', v: '1,200 A Continuous' },
          { k: 'Symmetrical Interrupting Current', v: '31.5 kA RMS' },
          { k: 'Interrupting Time', v: '3.0 Cycles (50 ms @ 60 Hz)' },
          { k: 'Basic Impulse Insulation Level (BIL)', v: '350 kV Peak' },
          { k: 'Operating Duty Cycle', v: 'O - 0.3s - CO - 3min - CO' },
          { k: 'Arc Quenching Medium', v: 'Sulfur Hexafluoride (SF6) Gas' },
          { k: 'Nominal SF6 Operating Pressure', v: '0.60 MPa (6.0 bar @ 20°C)' },
          { k: 'Operating Mechanism Type', v: 'Spring-Charged Motor Mechanism' },
          { k: 'Closing Coil Operating Voltage', v: '125 VDC' },
          { k: 'Dual Trip Coils Operating Voltage', v: '125 VDC (Redundant Circuits)' }
        ],
        failureModes: [
          { title: 'SF6 Gas Pressure Loss & Dielectric Breakdown', desc: 'Seal degradation or thermal cycling leads to SF6 leakage. As pressure drops below lockout threshold (0.50 MPa), arc-quenching capability is lost, and electrical trip interlocks prevent opening.' },
          { title: 'Moisture Contamination & Corrosive By-products', desc: 'Moisture ingress hydrolyzes SF6 arcing by-products into Thionyl Fluoride (SOF2) and corrosive Hydrofluoric Acid (HF), corroding nozzle PTFE and eroding contacts.' },
          { title: 'Contact Erosion & High Resistance Hot Spots', desc: 'Repeated fault interruptions erode copper-tungsten arcing tips, causing premature contact degradation and excessive dynamic millivolt drop (>50 µΩ).' },
          { title: 'Mechanism Spring Failure / Latch Freezing', desc: 'Hardened grease or mechanical latch fatigue delays tripping beyond 3 cycles, causing upstream transformer damage and protection miscoordination.' }
        ],
        checklist: [
          'Verify SF6 temperature-compensated gas density monitor: green zone (0.60 MPa) vs. low gas alarm (0.52 MPa) or trip lockout (0.50 MPa).',
          'Inspect mechanical spring-charge status indicator (Yellow = CHARGED, White = DISCHARGED).',
          'Check mechanical operations counter reading to plan scheduled contact overhaul.',
          'Measure primary contact micro-ohm resistance across closed poles (< 45 µΩ per phase).',
          'Verify dual 125 VDC trip coil circuit continuity and auxiliary contact switch (52a/52b) alignment.'
        ],
        subparts: [
          { id: 'cb-bushings', name: 'HV Entrance Porcelain Bushings & BCTs', tag: 'CB-BUSH', material: 'C130 Glazed Porcelain with Internal Bushing CTs', role: 'Provides high-voltage insulated terminal connections and houses 600:5 A relaying class C800 current transformers.', vector: [0, 3.8, 0] },
          { id: 'cb-terminal-pads', name: 'High-Conductivity Terminal Palm Pads', tag: 'TERM-PADS', material: 'Silver-Plated Tinned Cast Bronze NEMA 4-Hole Pads', role: 'Bolted connections to 69 kV tubular busbars and flexible expansion jumpers.', vector: [0, 4.6, 0] },
          { id: 'cb-interrupter', name: 'SF6 Gas Puffer Interrupter Chamber', tag: 'PUFF-CHAMB', material: 'Dielectric PTFE Nozzle / High-Pressure Puffer Cylinder', role: 'Compresses SF6 gas during opening stroke, blasting a high-velocity sonic gas jet across arcing contacts.', vector: [0, 1.2, 0] },
          { id: 'cb-contacts', name: 'Fixed & Moving Copper-Tungsten Contacts', tag: 'CONTACTS', material: 'Sintered Copper-Tungsten (CuW 80/20) Arcing Tips', role: 'Carries 1,200 A continuously on main silver contacts and absorbs 31.5 kA electrical arcs on sacrificial CuW tips.', vector: [0, 1.2, 2.2] },
          { id: 'cb-operating-mech', name: 'Spring-Charged Mechanical Operating Cabinet', tag: 'MECH-CAB', material: 'Weatherproof IP55 Galvanized Steel Enclosure', role: 'Houses closing springs, motor recharging gear, dual 125 VDC trip coils, and latching pawls.', vector: [0, -1.8, 2.5] },
          { id: 'cb-gauge', name: 'SF6 Gas Density Monitor & Pressure Gauge', tag: 'SF6-GAUGE', material: 'Bimetallic Temperature-Compensated Bourdon Gauge', role: 'Continuously monitors gas mass density with dual microswitches for low gas alarm and trip lockout.', vector: [1.8, -0.8, 2.8] },
          { id: 'cb-tank', name: 'Horizontal Grounded Carbon Steel Tanks', tag: 'DEAD-TANK', material: 'Welded Carbon Steel Pressure Vessel (Dead Tank)', role: 'Ground-potential enclosure containing high-pressure SF6 gas with zero shock hazard on the outer shell.', vector: [0, -0.6, 0] }
        ]
      },

      disconnect: {
        id: 'disconnect',
        name: '69 kV Center-Break Motorized Disconnect Switch (DS-69-1)',
        tag: 'DS-69-1',
        ansiNumber: '89 / 89E',
        governingStandard: 'IEEE Std C37.30 / IEEE Std C37.32 / IEC 62271-102',
        overview: 'Three-phase gang-operated horizontal center-break air disconnect switch (isolator) equipped with motorized drive and integrated grounding/earthing blade (89E), used to provide visible physical isolation for personnel maintenance.',
        specs: [
          { k: 'Rated Maximum Voltage', v: '72.5 kV RMS' },
          { k: 'Rated Continuous Current', v: '1,200 A Continuous' },
          { k: 'Rated Short-Time Withstand (3s)', v: '31.5 kA RMS' },
          { k: 'Peak Momentary Withstand Current', v: '40.0 kA Crest' },
          { k: 'Basic Impulse Level (BIL)', v: '350 kV (Across open gap: 400 kV)' },
          { k: 'Interrupting Medium', v: 'None (Atmospheric Air - 0 A)' },
          { k: 'Operating Mechanism', v: 'Motorized Torsion Tube & Gearbox (24 VDC / 120 VAC)' },
          { k: 'Operating Speed (Full Stroke)', v: '4.0 to 6.0 Seconds' },
          { k: 'Insulator Stack Type', v: 'C10-350 Porcelain Station Post (ANSI TR-286)' },
          { k: 'Grounding Switch Rating', v: '31.5 kA 3s Short-Time Withstand (ANSI 89E)' },
          { k: 'Interlocking Scheme', v: 'Kirk Key & SCADA Electrical Interlock with CB 52' }
        ],
        failureModes: [
          { title: 'Contact Finger Oxidation & Thermal Runaway', desc: 'Atmospheric sulfur and moisture oxidize silver plating on contact jaws. Contact resistance rises from <50 µΩ to >500 µΩ, causing overheating, welding, or contact distortion.' },
          { title: 'Arc Flash Blast from Opening Under Load', desc: 'FATAL HAZARD: Disconnect switches possess zero arc-quenching capability. Opening under load current draws an unquenched open-air arc triggering a 19,000°C plasma arc flash.' },
          { title: 'Drive Mechanism Jamming / Linkage Misalignment', desc: 'Corrosion or ice accumulation in bevel gears prevents three phases from closing simultaneously, creating single-phasing conditions and unbalanced voltage.' },
          { title: 'Porcelain Post Insulator Cantilever Cracking', desc: 'Seismic vibration or excessive busbar mechanical pull cracks porcelain posts at cemented base flanges, risking structural collapse.' }
        ],
        checklist: [
          'Verify complete physical alignment and positive wipe engagement of contact blades in fixed jaw fingers.',
          'Execute infrared thermography scan across all contact fingers under full load current (<5°C temperature rise).',
          'Test mechanical and electrical interlock: confirm disconnect motor control is electrically blocked when Circuit Breaker 52 is closed.',
          'Inspect integrated grounding blade 89E: verify mechanical interference latch prevents closing earth blade when main switch is closed.',
          'Audit motor gearbox limit switches, auxiliary contacts, and manual hand-crank interlock switch.'
        ],
        subparts: [
          { id: 'ds-conducting-blades', name: 'High-Conductivity Silver-Plated Copper Blades', tag: 'BLADES', material: 'Hard-Drawn Electrolytic Copper / Silver Plated Tips', role: 'Conducts 1,200 A continuously with twin rotating arms that separate at mid-span in horizontal plane.', vector: [0, 2.5, 0] },
          { id: 'ds-jaw-contacts', name: 'Fixed Jaw Contacts with Corona Rings', tag: 'JAW-CONT', material: 'Beryllium-Copper Spring Fingers & Aluminum Corona Rings', role: 'Provides multi-point high-pressure wipe contact and suppresses corona discharge noise.', vector: [-3.2, 2.5, 0] },
          { id: 'ds-insulators', name: 'Rotating Porcelain Station Post Insulator Stacks', tag: 'ROT-INSUL', material: 'ANSI TR-286 High-Strength Glazed Porcelain', role: 'Supports conducting blades at 72.5 kV while transmitting rotational torque from base bearings.', vector: [0, 1.0, 0] },
          { id: 'ds-base-frame', name: 'Galvanized Structural Steel Channel Base', tag: 'BASE-FRAME', material: 'Hot-Dip Galvanized Structural Steel Channel', role: 'Rigid structural mounting chassis maintaining precise alignment across rotating bearing pedestals.', vector: [0, -1.5, 0] },
          { id: 'ds-operating-mech', name: 'Motorized Drive Mechanism & Torsion Linkage', tag: 'DRIVE-MECH', material: 'Weatherproof Motorized Gearbox & Interlocking Cams', role: 'Drives rotating insulators through vertical torsion pipe with internal auxiliary limit switches.', vector: [2.5, -1.2, 1.8] },
          { id: 'ds-earth-blade', name: 'Integrated Grounding Switch Blade (ANSI 89E)', tag: 'EARTH-89E', material: 'High-Strength Copper Blade & Ground Flexible Braid', role: 'Pivots upward to solidly ground de-energized line for worker safety, with mechanical interlock.', vector: [-2.2, 0.5, 2.0] }
        ]
      },

      ctvt: {
        id: 'ctvt',
        name: 'Instrument Transformers: CT-69 & VT-69 / CVT',
        tag: 'CT-69 / VT-69',
        ansiNumber: 'CT / VT / CVT',
        governingStandard: 'IEEE Std C57.13 / IEC 61869-2 & 61869-3',
        overview: 'Outdoor oil/gas-immersed high-voltage instrument transformers providing scaled secondary currents (5 A) and voltages (115 V / 120 V) for microprocessor protective relays (SEL-751/SEL-487E) and revenue-class billing meters.',
        specs: [
          { k: 'Primary Nominal Voltage', v: '69.0 kV Line-to-Line (39.8 kV L-G)' },
          { k: 'CT Multi-Ratio Taps', v: '600:5 A (100, 200, 300, 400, 500, 600:5 A)' },
          { k: 'CT Protection Accuracy Class', v: 'Relay Class C400 / C800 (IEEE C57.13)' },
          { k: 'CT Revenue Metering Class', v: 'Class 0.3 with B-0.9 / B-1.8 Burden' },
          { k: 'CT Continuous Thermal Rating Factor', v: 'RF = 1.5 @ 30°C / RF = 1.0 @ 55°C' },
          { k: 'CT Secondary Knee-Point Voltage', v: 'V_k >= 400 V' },
          { k: 'VT Voltage Ratio', v: '69,000V/√3 : 115V/√3 (Ratio 600:1)' },
          { k: 'VT Accuracy Class', v: '0.3 W, X, M, Y, Z Burden' },
          { k: 'Insulation BIL', v: '350 kV Crest' },
          { k: 'Insulating Dielectric', v: 'Inhibited Mineral Oil with N2 Cushion / SF6' }
        ],
        failureModes: [
          { title: 'CT Secondary Open-Circuit Fatal Overvoltage', desc: 'CRITICAL SAFETY HAZARD: If CT secondary is opened while primary carries current, all primary ampere-turns act as exciting current, inducing lethal peak voltages (>5,000 V) that destroy insulation and electrocute personnel.' },
          { title: 'Magnetic Core Saturation Under Faults', desc: 'High asymmetrical DC offset fault current drives core into deep magnetic saturation, distorting secondary waveform and causing protective relays to fail to trip or miscoordinate.' },
          { title: 'Capacitive Bushing Grading Layer Breakdown', desc: 'Moisture ingress causes puncture of capacitive aluminum foil layers inside CVT/CT bushing, leading to progressive dielectric thermal runaway and explosive failure.' },
          { title: 'VT Ferroresonance Oscillation', desc: 'Non-linear magnetizing inductance of inductive VT interacts with switchyard bus capacitance, causing severe overvoltages and thermal burnout.' }
        ],
        checklist: [
          'Verify CT secondary circuits are solidly grounded at a single point (star point in relay panel) and never left open-circuited.',
          'Audit CT secondary test blocks / shorting switches inside junction box before disconnecting any relay wiring.',
          'Perform insulation power factor (Doble test) on primary winding to detect moisture ingress (<0.5% PF).',
          'Measure CT secondary winding DC resistance and secondary loop burden impedance (<0.50 Ω).',
          'Inspect oil level sight glass and metallic expansion bellows expansion position.'
        ],
        subparts: [
          { id: 'ct-primary-head', name: 'Primary Conductor Pass-Through Head', tag: 'PRIM-HEAD', material: 'Cast Aluminum Tank / Electrolytic Copper Bar', role: 'Accommodates primary 69 kV conductor passing through upper toroidal core chamber.', vector: [0, 3.2, 0] },
          { id: 'ct-metering-core', name: 'Toroidal Metering Core (Class 0.3B0.9)', tag: 'MTR-CORE', material: 'High-Permeability Grain-Oriented Supermalloy', role: 'Provides high-accuracy replication of load currents up to 100% full load for revenue billing.', vector: [0, 2.4, -1.2] },
          { id: 'ct-relaying-core', name: 'Toroidal Protection Core (Class C400/C800)', tag: 'PROT-CORE', material: 'Silicon Steel Core with Linear Excitation Curve', role: 'Ensures distortion-free current transformation during 20x nominal fault currents up to 12.5 kA.', vector: [0, 2.4, 1.2] },
          { id: 'ct-porcelain-body', name: 'Porcelain Insulator Body with Weather Sheds', tag: 'PORC-BODY', material: 'High-Strength Wet Process Porcelain C130', role: 'Maintains external electrical creepage distance (31 mm/kV) to prevent pollution flashover.', vector: [0, 0.8, 0] },
          { id: 'ct-bellows', name: 'Stainless Steel Metallic Expansion Bellows', tag: 'EXP-BELLOW', material: 'Corrugated Austenitic Stainless Steel Bellows', role: 'Compensates for thermal oil expansion while maintaining hermetic seal against atmospheric moisture.', vector: [0, 3.8, 0] },
          { id: 'ct-sec-box', name: 'Secondary Terminal Junction Box (IP55)', tag: 'SEC-BOX', material: 'Cast Aluminum Weatherproof Box with Shorting Terminals', role: 'Provides test disconnect switches and shorting bars to safely ground CT secondary leads.', vector: [0, -1.8, 0] }
        ]
      },

      arrester: {
        id: 'arrester',
        name: 'Station Class Metal-Oxide Surge Arrester (SA-69)',
        tag: 'SA-69',
        ansiNumber: 'LA / MOSA',
        governingStandard: 'IEEE Std C62.11 / IEEE Std 1313.1 / IEC 60099-4',
        overview: 'Gapless station-class Zinc-Oxide (ZnO) metal-oxide surge arrester (MOSA) providing critical overvoltage surge protection for transformers and switchgear against atmospheric lightning strikes and high-energy switching transients.',
        specs: [
          { k: 'Nominal System Voltage', v: '69.0 kV Line-to-Line' },
          { k: 'Maximum Continuous Operating Voltage (MCOV)', v: '54.0 kV RMS (Phase-to-Ground)' },
          { k: 'Rated Voltage (Duty Cycle Ur)', v: '60.0 kV RMS' },
          { k: 'Nominal Discharge Current (Class)', v: '10 kA Crest (Station Class)' },
          { k: '10 kA Crest Discharge Voltage', v: '175.0 kV Peak' },
          { k: 'Front-of-Wave Protective Level (FOW)', v: '195.0 kV Peak' },
          { k: 'Basic Impulse Level (BIL) Protected', v: '350 kV (Protective Margin PR1 = 100%)' },
          { k: 'Temporary Overvoltage (TOV 10s)', v: '78.5 kV RMS' },
          { k: 'Housing Material', v: 'Dark Chocolate-Brown Wet-Process Glazed Porcelain' },
          { k: 'Energy Absorption Capability', v: '7.5 kJ / kV of MCOV' }
        ],
        failureModes: [
          { title: 'Moisture Ingress & Varistor Thermal Runaway', desc: 'Moisture penetration through end-flange seals degrades ZnO ceramic grain boundaries, increasing resistive leakage current from microamperes to milliamperes, triggering thermal runaway and explosive shattering.' },
          { title: 'Repeated Multi-Stroke Lightning Energy Exhaustion', desc: 'Consecutive high-amplitude lightning strokes exceed total joule absorption capacity (7.5 kJ/kV), causing mechanical fracturing of ZnO discs and phase-to-ground power-frequency fault.' },
          { title: 'Lead Length Separation Voltage Drop', desc: 'Excessive connecting conductor lead length adds inductive L*(di/dt) voltage drop (approx. 1 kV/meter for 10 kA/µs surge), elevating total surge voltage experienced by the transformer.' },
          { title: 'Temporary Overvoltage (TOV) Breakdown', desc: 'Extended ungrounded single-line-to-ground faults cause fundamental-frequency voltage rise beyond TOV envelope, causing varistor overheating.' }
        ],
        checklist: [
          'Record digital surge event counter reading and resistive leakage current milliammeter (normal: <100 µA, alarm: >500 µA).',
          'Execute infrared thermography scan: uniform temperature profile across polymer housing (hot patches indicate failing internal blocks).',
          'Verify ground lead connection: ensure short, direct, low-inductance connection to substation grounding grid.',
          'Inspect polymer weather sheds for hydrophobic loss, erosion, tracking, or bird fouling.',
          'Verify top aluminum corona/grading ring mechanical tightness and orientation.'
        ],
        subparts: [
          { id: 'la-terminal-stud', name: 'Stainless Steel Line Terminal Stud & Clamp', tag: 'LINE-TERM', material: 'Stainless Steel 316 / Bronze Conductor Clamp', role: 'Direct low-impedance electrical interface to high-voltage 69 kV busbar phase leads.', vector: [0, 3.5, 0] },
          { id: 'la-grading-ring', name: 'Electrostatic Corona & Voltage Grading Ring', tag: 'CORONA-RING', material: 'Seamless Spun Aluminum Toroid', role: 'Linearizes non-linear electrical field potential distribution across upper varistor disc stack.', vector: [0, 3.0, 0] },
          { id: 'la-zno-stack', name: 'Metal-Oxide Varistor (MOV) Zinc Oxide Disc Stack', tag: 'ZNO-DISCS', material: 'Sintered Zinc Oxide (ZnO) with Bismuth/Antimony Oxides', role: 'Acts as non-linear semiconductor: open-circuit at 60 Hz, transitioning to low resistance in nanoseconds during surges.', vector: [0, 0.5, 0] },
          { id: 'la-fiberglass-tube', name: 'Filament-Wound Fiberglass Reinforced Tube', tag: 'FRP-TUBE', material: 'High-Modulus Epoxy-Impregnated Fiberglass', role: 'Provides high mechanical cantilever strength (10 kN) against seismic and extreme wind forces.', vector: [0, 0.5, 1.8] },
          { id: 'la-polymer-sheds', name: 'Wet-Process Dark Porcelain Weather Sheds & Flanges', tag: 'PORC-SHEDS', material: 'Dark Brown Glazed Wet-Process Electrical Porcelain + Metallic Intermediate Flanges', role: 'Provides high creepage distance (≥31 mm/kV), salt-fog contamination withstand, and superior UV/tracking immunity.', vector: [0, 0.5, -1.8] },
          { id: 'la-surge-counter', name: 'Ground Discharge Lead & Surge Counter', tag: 'SURGE-COUNT', material: 'Hermetic Spark-Gap Impactor & Analog Milliammeter', role: 'Counts cumulative surge discharges and monitors continuous phase-to-ground resistive leakage current.', vector: [0, -2.2, 0] }
        ]
      },

      gantry: {
        id: 'gantry',
        name: 'Incoming Transmission Gantry & Busbar System',
        tag: 'GANTRY / BUS',
        ansiNumber: 'BUS-69 / OHGW',
        governingStandard: 'IEEE Std 605 / IEEE Std 998 / PEC 2017 Part 2',
        overview: 'Heavy galvanized structural steel dead-end A-frame gantry supporting incoming 69 kV ACSR sub-transmission line conductors, overhead shield wires (OHGW), strain insulator assemblies, and rigid tubular aluminum busbars.',
        specs: [
          { k: 'Gantry Height & Span', v: '16.0 m Height / 24.0 m Span' },
          { k: 'Incoming Phase Conductor', v: 'Penguin 4/0 AWG ACSR (6/1 stranding, 14.3 mm dia)' },
          { k: 'Conductor Ampacity @ 75°C', v: '360 A Continuous' },
          { k: 'Overhead Ground Wire (OHGW)', v: '7/16-inch Extra High Strength (EHS) Steel' },
          { k: 'Suspension Insulator String', v: '6 Discs ANSI Class 52-3 Porcelain Bell Insulators' },
          { k: 'Rigid Busbar Material', v: 'Schedule 40 Aluminum Pipe (6063-T6, 3-inch IPS)' },
          { k: 'Rigid Busbar Continuous Ampacity', v: '1,650 A Continuous' },
          { k: 'Busbar Phase-to-Phase Clearance', v: '1,500 mm (Min PEC/NESC: 900 mm)' },
          { k: 'Busbar Phase-to-Ground Clearance', v: '1,100 mm (Min PEC/NESC: 650 mm)' },
          { k: 'Rolling Sphere Striking Radius', v: '45.0 m (Protected across all bays per IEEE 998)' }
        ],
        failureModes: [
          { title: 'Aeolian Vibration Fatigue of Conductor Strands', desc: 'Low-velocity steady winds cause vortex shedding and high-frequency flexural fatigue in outer aluminum strands at suspension clamps, prevented by Stockbridge dampers.' },
          { title: 'Insulator Contamination & Salt-Fog Flashover', desc: 'Airborne maritime salt dust or industrial pollution builds conductive layer on insulator discs, causing wetting-induced leakage currents and full phase-to-ground flashover.' },
          { title: 'Busbar Thermal Expansion Joint Fracture', desc: 'Cyclic seasonal and daily thermal expansion (ΔL = α*L*ΔT) without flexible expansion joints shears porcelain post support insulators.' },
          { title: 'Shielding Failure from Low-Current Lightning Strokes', desc: 'Low-magnitude lightning leaders (<2.0 kA) with small striking distances can bypass shield wires if mast spacing exceeds rolling sphere geometry.' }
        ],
        checklist: [
          'Inspect porcelain suspension insulator strings for cracked bells, glazing chips, or flashover burns.',
          'Verify Stockbridge vibration damper weights are intact and properly spaced from suspension clamps.',
          'Audit bolted expansion pad connections between rigid aluminum busbars using infrared thermography.',
          'Check overhead shield wire (OHGW) downlead bonds to gantry grounding pads.',
          'Verify minimum electrical phase-to-phase (1.5 m) and phase-to-ground (1.1 m) safety clearances.'
        ],
        subparts: [
          { id: 'gantry-lattice-tower', name: 'Galvanized Lattice Steel Gantry Structure', tag: 'LATTICE-TWR', material: 'Hot-Dip Galvanized Structural Angle Steel (ASTM A36)', role: 'Rigid dead-end structural tower engineered to withstand 15 kN conductor tension and typhoon winds.', vector: [0, 0, -3.5] },
          { id: 'gantry-acsr-conductors', name: 'ACSR 4/0 AWG Phase Conductors (Penguin)', tag: 'ACSR-LINES', material: 'Stranded Aluminum Conductor Steel Reinforced', role: 'Delivers 3-phase bulk 69 kV power with high tensile strength steel core and conductive aluminum strands.', vector: [0, 2.8, 0] },
          { id: 'gantry-ohgw-shield', name: 'Overhead Ground Shield Wire (OHGW)', tag: 'OHGW-SHIELD', material: '7/16-inch Galvanized Steel / OPGW Optical Ground Wire', role: 'Intercepts incoming cloud-to-ground lightning strokes and dissipates surge energy directly to earth.', vector: [0, 4.5, 0] },
          { id: 'gantry-insulator-strings', name: 'Porcelain Suspension Insulator Strings & Horns', tag: 'INSUL-STRINGS', material: 'Wet-Process Cap-and-Pin Porcelain Discs with Arcing Horns', role: 'Provides 350 kV impulse insulation withstand while arcing horns divert destructive arc roots away from bells.', vector: [0, 2.2, 2.2] },
          { id: 'gantry-dampers', name: 'Stockbridge Aeolian Vibration Dampers', tag: 'VIB-DAMP', material: 'Cast Iron Weights with Flexible Steel Messenger Wire', role: 'Dissipates wind-induced harmonic vibrations to prevent conductor fatigue failure.', vector: [2.5, 2.5, 1.2] },
          { id: 'gantry-tubular-bus', name: 'Rigid Tubular Aluminum Busbars (6063-T6)', tag: 'RIGID-BUS', material: 'Schedule 40 High-Conductivity Aluminum Alloy Pipe', role: 'Distributes 69 kV power across bays with zero sag and high short-circuit electrodynamic stiffness.', vector: [0, -1.2, 0] }
        ]
      },

      auxiliary: {
        id: 'auxiliary',
        name: 'Station Service Transformer & Control House',
        tag: 'STATION SERVICE',
        ansiNumber: 'SST / SCADA / 125VDC',
        governingStandard: 'IEEE Std 484 / IEEE Std 485 / PEC Part 1',
        overview: 'Vital auxiliary life-support infrastructure comprising a 100 kVA step-down station service transformer (13.8 kV to 230/115 V), dual 125 VDC float/equalize battery systems, microprocessor protection racks, and SCADA remote automation.',
        specs: [
          { k: 'Transformer Rating', v: '100 kVA, 3-Phase, 60 Hz' },
          { k: 'Primary / Secondary Voltage', v: '13.8 kV Grounded-Wye to 230/115 V' },
          { k: 'Station Battery Bank', v: '125 VDC Flooded Lead-Acid / VRLA (60 Cells)' },
          { k: 'Battery Capacity (8-hr duty)', v: '200 Ampere-Hours (Ah)' },
          { k: 'Battery Chargers', v: 'Dual 50 A Redundant Solid-State SCR Chargers' },
          { k: 'Protective Relays Installed', v: 'Schweitzer SEL-751 (Feeder) & SEL-487E (Differential)' },
          { k: 'SCADA Remote Terminal Unit', v: 'DNP3.0 / IEC 61850 Station Gateway' },
          { k: 'Emergency Backup Autonomy', v: '8 Hours Full Substation Control & Tripping Power' }
        ],
        failureModes: [
          { title: 'Station 125 VDC Battery Open-Circuit Failure', desc: 'CRITICAL DISASTER SCENARIO: If station DC battery bank fails during a blackout, circuit breaker trip coils cannot energize. Short circuits will persist until upstream utility transmission lines clear, destroying the substation.' },
          { title: 'Battery Thermal Runaway & Hydrogen Gas Accumulation', desc: 'Overcharging flooded lead-acid cells generates explosive hydrogen gas (H2). Concentrations exceeding 4% in the battery room risk fatal detonation if room ventilation fails.' },
          { title: 'Station Service Transformer Single-Phasing', desc: 'Blown primary fuse on one phase causes unbalanced three-phase auxiliary voltage, burning out transformer cooling fan motors and battery charger circuits.' },
          { title: 'SCADA Fiber-Optic Communication Loss', desc: 'Loss of remote telemetry blinds utility dispatchers to breaker status, preventing remote fault isolation during grid emergency.' }
        ],
        checklist: [
          'Verify station 125 VDC battery bank float voltage: 135.0 VDC (2.25 V per cell) and check specific gravity of pilot cells (1.215 @ 25°C).',
          'Inspect battery room spark-proof exhaust ventilation fan and hydrogen gas detector calibration.',
          'Verify dual battery charger load sharing and AC supply automatic transfer switch (ATS).',
          'Audit microprocessor relay self-test diagnostic watchdog contacts (SEL-751 green ENABLED LED).',
          'Test station service transformer primary cutout fuses and secondary 230 V panelboard breakers.'
        ],
        subparts: [
          { id: 'aux-tx-bushings', name: '13.8 kV Primary Bushings & Cutout Fuses', tag: 'AUX-BUSH', material: 'Outdoor Polymer Bushings with Expulsion Fuse Cutouts', role: 'Provides high-voltage tap from 13.8 kV busbar with short-circuit fault isolation.', vector: [0, 3.2, 0] },
          { id: 'aux-tx-tank', name: '100 kVA Step-Down Transformer Tank', tag: 'AUX-TANK', material: 'Liquid-Immersed Padmount Steel Tank Enclosure', role: 'Steps down 13.8 kV to 230/115 V three-phase utility power for station lighting, pumps, and fans.', vector: [0, 0.8, 0] },
          { id: 'aux-relay-racks', name: '19-inch Microprocessor Relay Racks (SEL)', tag: 'RELAY-RACK', material: 'Standard Galvanized Steel 19-inch Relay Cabinets', role: 'Houses SEL-487E transformer differential, SEL-751 overcurrent relays, and 52CB pistol-grip control switch.', vector: [1.5, 0.4, -1.8] },
          { id: 'aux-scada-desk', name: 'SCADA / HMI Workstation & Alarm Annunciator', tag: 'SCADA-HMI', material: 'Dual LCD Operator Console, SEL-3555 RTU & IRIG-B GPS Clock', role: 'Displays live switchyard single-line mimic, SOE millisecond trip logs, and windowed annunciator alarms.', vector: [0, 1.5, -1.0] },
          { id: 'aux-battery-rack', name: '125 VDC Station Battery Bank Rack (60 Cells)', tag: 'BATT-BANK', material: 'Two-Tier Acid-Resistant Steel Rack with Translucent VRLA/Flooded Jars', role: 'Supplies uninterruptible 125 VDC control power to trip coils, spring motors, and emergency lights.', vector: [-2.0, 0.4, 1.8] },
          { id: 'aux-battery-chargers', name: 'Dual Redundant Solid-State Battery Chargers', tag: 'CHARGERS', material: 'Microprocessor Controlled SCR Float/Equalize Rectifiers', role: 'Maintains 135.0 VDC float charge while carrying steady-state DC station load with N+1 redundancy.', vector: [-1.2, 0.8, 2.4] },
          { id: 'aux-acdc-boards', name: '125 VDC & 480/240 VAC Distribution Panelboards', tag: 'AC-DC-DIST', material: 'NEMA 1 Indoor Switchboard with Molded-Case Breakers', role: 'Routes protected DC branch feeds (TC1/TC2/Relays) and essential AC feeds (OLTC, cooling fans, HVAC).', vector: [2.2, 0.4, 1.0] }
        ]
      },
      secondary: {
        id: 'secondary',
        name: '13.8 kV Secondary Switchyard, NGR & Main VCB (52-LV)',
        tag: 'SEC-13.8',
        ansiNumber: '52-LV / 89-LV / 51G / 52-CAP',
        governingStandard: 'IEEE Std C37.06 / IEEE Std 32 / PEC 2017 Part 2',
        overview: 'Complete 13.8 kV medium-voltage secondary bay receiving stepped-down power from TR-01 X1-X3 bushings via busbar throat, protected by low-resistance Neutral Grounding Resistor (NGR), 13.8 kV arresters & metering CT/VT, motor-operated 89-LV isolator, 2000 A Main Vacuum Breaker (52-LV), rigid distribution bus, and 3.6 MVAR Capacitor Bank (52-CAP).',
        specs: [
          { k: 'System Voltage (L-L / L-N)', v: '13.8 kV / 7.97 kV' },
          { k: 'Basic Impulse Level (BIL)', v: '110 kV Peak' },
          { k: 'Main VCB (52-LV) Rating', v: '15 kV, 2,000 A, 31.5 kA sym.' },
          { k: 'Neutral Grounding (NGR)', v: '10 Ω Stainless Grid, 800 A, 10 s (IEEE 32)' },
          { k: 'Shunt Capacitor Bank', v: '3.6 MVAR grounded-wye, 150 A, 52-CAP switched' },
          { k: 'Station Service Tap', v: '100 kVA 13.8 kV / 480 V (SST-100) via FU-SS' }
        ],
        failureModes: [
          { title: 'NGR Bypass / High SLG Arc-Flash Energy', desc: 'Solidly grounding the 13.8 kV neutral without the 10 Ω NGR unleashes >15 kA SLG faults, risking severe MV switchgear arc-flash destruction.' },
          { title: 'Capacitor Bank Switching Restrike Transient', desc: 'Vacuum bottle restrike during 52-CAP de-energization generates 2.5 pu transient overvoltages unless damped by iron-core inrush reactors.' },
          { title: 'X1–X3 Bus Riser Palm Heating', desc: 'Loose copper/bronze terminal flags on TR-01 secondary risers overheat (>90 °C) under 1,745 A continuous ONAF2 load.' }
        ],
        checklist: [
          'Verify 52-LV vacuum bottle integrity (27 kV AC 1-minute hi-pot check) and spring-charge indicator.',
          'Inspect NGR resistor banks for warped grids and verify 51G Neutral CT ratio (800/5 A).',
          'Confirm 52-CAP discharge resistors drain trapped bank voltage below 50 V within 5 minutes of opening.'
        ],
        subparts: [
          { id: 'sec-ngr', name: '10 Ω Neutral Grounding Resistor (NGR) & 51G CT', tag: 'NGR-51G', material: 'Edge-Wound Stainless Steel Resistor Bank on Porcelain Insulators', role: 'Connects TR-01 neutral X0 to station ground mat to cap SLG fault current at 797 A and enable sensitive 51G relaying.', vector: [-1.4, 0.3, -1.2] },
          { id: 'sec-arresters-ctvt', name: '13.8 kV Station Arresters & Secondary Metering CT/VT', tag: 'MV-MEAS', material: '12 kV MCOV Gapless MOV Arresters + Epoxy-Cast 2000/5A CTs & 13.8kV/115V VTs', role: 'Clamps switching surges exiting TR-01 LV windings and provides revenue metering + ANSI 51/87T secondary differential CT inputs.', vector: [-0.9, 1.0, 0.2] },
          { id: 'sec-lv-disconnect', name: '89-LV Secondary Isolation Disconnect Switch (2000 A)', tag: 'DS-89LV', material: 'Silver-Plated Dual-Blade Copper Knife Switch on 15 kV Post Insulators', role: 'Provides visible air-gap isolation between TR-01 X1-X3 throat and Main 52-LV Vacuum Breaker during maintenance.', vector: [-0.3, 1.2, 0.0] },
          { id: 'sec-lv-breaker', name: '52-LV Main 13.8 kV Vacuum Circuit Breaker (2000 A)', tag: 'VCB-52LV', material: 'Outdoor Dead-Tank / Porcelain-Bushing Vacuum Interrupters (31.5 kA)', role: 'Interrupts 1,744 A rated secondary load and clears 13.8 kV bus faults within 3 cycles via 50/51/51N relays.', vector: [0.2, 0.8, 0.0] },
          { id: 'sec-dist-bus', name: '13.8 kV Rigid Distribution Bus & SST-100 Fuse Tap', tag: 'BUS-13.8', material: 'Schedule 40 6063-T6 Tubular Aluminum (2.5-in) + Expulsion Fuse Cutouts', role: 'Collects 52-LV power and distributes to Feeder 01, Feeder 02, 52-CAP, and the FU-SS fused tap feeding SST-100 behind the IEEE 979 fire wall.', vector: [0.9, 1.3, 0.4] },
          { id: 'sec-cap-bank', name: '3.6 MVAR Shunt Capacitor Bank & 52-CAP Switch', tag: 'CAP-3.6', material: 'All-Film polypropylene dielectric cans + 600 A VCB + Iron-Core Inrush Reactors', role: 'Supplies 3.6 MVAR leading reactive power to hold 13.8 kV bus voltage >=0.98 pu and correct distribution PF above 0.96.', vector: [0.8, 0.5, 1.8] }
        ]
      },
      feeders: {
        id: 'feeders',
        name: '13.8 kV Outgoing Distribution Feeder Bays (F1 & F2)',
        tag: 'FDR-01-02',
        ansiNumber: '52-F1 / 52-F2 (50/51/51N/79)',
        governingStandard: 'IEEE Std C37.230 / ANSI C84.1 / PEC 2017 Part 2',
        overview: 'Dual 13.8 kV outgoing distribution bays feeding residential/commercial and industrial radial circuits via isolated 89-F1A/B and 89-F2A/B disconnects, 1200 A feeder Vacuum Circuit Breakers with ANSI 79 auto-reclosing, zero-sequence CTs, distribution surge arresters, and an H-frame steel outgoing takeoff portal.',
        specs: [
          { k: 'Feeder Design Rating', v: '13.8 kV, 1,200 A Buswork (20.8 MVA thermal cap)' },
          { k: 'Feeder Breakers (52-F1/F2)', v: '15 kV, 1,200 A, 25 kA sym., 3-cycle Vacuum' },
          { k: 'Protection & Reclosing', v: 'ANSI 50/51, 51N, 79 (0.5 s - 2.0 s - 15 s shots)' },
          { k: 'Outgoing Conductors', v: '477 kcmil ACSR Hawk (3-Phase + 4/0 Neutral)' },
          { k: 'Clearance (Ph-Ph / Exit)', v: '0.45 m min / >=5.5 m above driveway' }
        ],
        failureModes: [
          { title: 'Recloser Lockout Failure During Transient Tree Faults', desc: 'If 125 VDC trip/close coil control power drops out, ANSI 79 fails to execute automatic 3-shot restoration.' },
          { title: 'Underrated Bypass Jumpers Under Through-Fault', desc: 'Whipped bypass leads across 89-F1A/B collide or anneal during 18.4 kA through-faults unless braced rigidly.' },
          { title: 'Portal MOV Arrester Ground-Lead Blowout', desc: 'Degraded riser arresters allow steep distribution line lightning waves to propagate directly into TR-01 LV bushings.' }
        ],
        checklist: [
          'Confirm 52-F1 and 52-F2 ANSI 79 reclose shot timers coordinate selectively with downstream line reclosers.',
          'Inspect flanking disconnect blades (89-F1A/B, 89-F2A/B) for full toggle lock-over-center seating.',
          'Verify 13.8 kV outgoing riser strain insulators and drip loops maintain >=5.5 m vertical clearance above yard fence.'
        ],
        subparts: [
          { id: 'fdr-f1-breaker', name: 'Feeder 01 Isolation Assembly (89-F1A / 52-F1 / 89-F1B)', tag: 'FDR-01', material: '15 kV 1200 A Outdoor Vacuum Breaker + Twin Vertical Disconnects', role: 'Protects Commercial/Hospital Radial Feeder 01 (22 MVA peak) with fast instantaneous trip and ANSI 79 three-shot auto-reclosing.', vector: [0.0, 0.8, -1.4] },
          { id: 'fdr-f2-breaker', name: 'Feeder 02 Isolation Assembly (89-F2A / 52-F2 / 89-F2B)', tag: 'FDR-02', material: '15 kV 1200 A Outdoor Vacuum Breaker + Twin Vertical Disconnects', role: 'Protects Industrial Park Radial Feeder 02 (19 MVA peak) with directional/overcurrent coordination and transfer switching readiness.', vector: [0.0, 0.8, 1.4] },
          { id: 'fdr-ct-arresters', name: 'Feeder Exit 1200/5A CTs & Riser Surge Arresters', tag: 'FDR-SA', material: 'Window Bushing CTs + 10 kV MCOV Polymer Distribution Arresters', role: 'Samples per-feeder phase & ground currents for SCADA/fault location while arresting incoming distribution line lightning surges.', vector: [1.1, 1.1, 0.0] },
          { id: 'fdr-takeoff-gantry', name: '13.8 kV Outgoing Takeoff H-Frame Gantry & ACSR Drops', tag: 'FDR-GAN', material: 'Galvanized Steel H-Frame + 15 kV Dead-End Polymer Insulators', role: 'Terminates dual outgoing 477 kcmil ACSR feeder circuits at 8.2 m height with shield wire termination to exit the switchyard.', vector: [1.8, 2.2, 0.0] }
        ]
      },

      // --- UNBUNDLED SECONDARY & DISTRIBUTION APPARATUS ---
      ngr_01: {
        id: 'ngr_01',
        name: 'Neutral Grounding Resistor (NGR-01)',
        tag: 'NGR-10Ω / 51G',
        ansiNumber: 'ANSI 51G / IEEE Std C57.32',
        governingStandard: 'IEEE Std C57.32 / IEEE Std 142 (Green Book)',
        overview: 'Low-resistance stainless-steel grid bank inserted between Transformer TR-01 neutral bushing (X0) and station ground grid, limiting single-line-to-ground (SLG) fault current on the 13.8 kV system to 797 A.',
        specs: [
          { k: 'Resistance Value (25°C)', v: '10.0 Ω ±5% (Stainless Steel Alloy)' },
          { k: 'Let-Through SLG Fault Current', v: '796.7 A RMS @ 7.97 kV L-N (10-second duty)' },
          { k: 'Peak Power Dissipation', v: '6.35 MW during SLG Fault (760 °C max temp rise)' },
          { k: 'Neutral Sensing CT', v: '800 / 5 A Class C200 Window CT (ANSI 51G)' },
          { k: 'Insulation Class / BIL', v: '15 kV Class / 110 kV BIL Post Standoff' }
        ],
        failureModes: [
          { title: 'Open-Circuit Grid Crack (Ungrounded Conversion)', desc: 'Corrosion or weld fatigue opens the resistor path, turning the 13.8 kV bus ungrounded during SLG faults—causing sqrt(3) transient overvoltages and ANSI 51G blind spots.' },
          { title: 'Thermal Overload Beyond 10s Duty', desc: 'Failure of upstream 52-LV to clear a persistent ground fault heats grids beyond 760°C, warping louver frames.' }
        ],
        checklist: [
          'Verify 10.0 Ω DC resistance via DLRO micro-ohmmeter before energizing X0.',
          'Check louvered stainless enclosure mesh for rodent nests or bird debris.',
          'Confirm 51G Neutral CT polarity toward X0 and shorting block integrity.'
        ],
        subparts: [
          { id: 'ngr-enclosure', name: 'Galvanized Louvered Enclosure & Roof Hood', tag: 'NGR-HSG', material: 'Perforated Galvanized Steel Sheet', role: 'Protects personnel from hot resistor elements (>600°C during faults) while venting convective heat.', vector: [0, 2.2, 0] },
          { id: 'ngr-resistor-grid', name: 'AISI 304 Stainless Steel Punched Edgewound Grid Stack', tag: 'NGR-GRID', material: 'Low-TCR Chromium-Nickel Steel Alloy', role: 'Absorbs up to 63.5 MJ of SLG fault energy over 10 seconds with minimal resistance drift.', vector: [-1.4, 1.0, 0] },
          { id: 'ngr-ct-bushing', name: '15 kV X0 Roof Entry Bushing & 800/5 A 51G Neutral CT', tag: 'NGR-CT', material: '110 kV BIL Porcelain + Toroidal CT', role: 'Brings insulated X0 lead into resistor top tap and feeds residual ground relay ANSI 51G.', vector: [0, 1.6, 1.4] },
          { id: 'ngr-ground-pad', name: 'Earth Side 4/0 Cu Pigtail & Insulated Base', tag: 'NGR-GND', material: 'Tinned Copper Bar + Epoxied Standoffs', role: 'Returns limited 797 A fault current safely into the buried IEEE 80 copper ground mat.', vector: [0, -0.8, 0] }
        ]
      },

      sa_lv: {
        id: 'sa_lv',
        name: '13.8 kV Secondary MOV Surge Arrester Bank (SA-13.8)',
        tag: 'SA-LV',
        ansiNumber: 'IEEE C62.11 Distribution / Intermediate',
        governingStandard: 'IEEE Std C62.11 / IEC 60099-4',
        overview: 'Three-phase gapless Zinc-Oxide station/intermediate arresters clamping secondary lightning surges transferred capacitively across TR-01 windings and capacitive switching transients.',
        specs: [
          { k: 'Duty Cycle Voltage (Ur)', v: '12.0 kV RMS (10.2 kV MCOV)' },
          { k: '10 kA Discharge Clamping', v: '32.5 kV Peak (110 kV BIL margin > 3.3x)' },
          { k: 'Housing', v: 'Dark Chocolate Porcelain Weather Sheds' }
        ],
        failureModes: [
          { title: 'NGR Overvoltage TOV Damage', desc: 'Sustained ungrounded fault shifts phase-to-ground voltage to 13.8 kV (>10.2 kV MCOV), thermally stressing MOV blocks.' }
        ],
        checklist: [
          'Check porcelain sheds for cracks and ground lead lug continuity to bus pedestal.',
          'Verify resistive leakage below 100 µA via clamp-on surge counter.'
        ],
        subparts: [
          { id: 'sal-terminal', name: 'Top Line Clamp & Grading Cap', tag: 'SAL-CAP', material: 'Bronze / Aluminum Die-Cast Clamp', role: 'Connects directly to 13.8 kV secondary rigid copper bus drop.', vector: [0, 1.8, 0] },
          { id: 'sal-zno-core', name: '10.2 kV MCOV MOV Varistor Stack', tag: 'SAL-MOV', material: 'Sintered ZnO Disc Blocks', role: 'Conducts nanoseconds after lightning surge exceeds 25 kV peak.', vector: [1.3, 0.4, 0] },
          { id: 'sal-sheds', name: 'Porcelain Weather Shed Housing', tag: 'SAL-PORC', material: 'Dark Brown Glazed Porcelain', role: 'Provides ≥ 430 mm external creepage and cantilever support.', vector: [-1.3, 0.4, 0] },
          { id: 'sal-ground-lead', name: 'Ground Lead & Base Insulating Bracket', tag: 'SAL-GND', material: 'Insulated #2 Cu Lead', role: 'Routes surge energy directly into secondary steel rack ground bus.', vector: [0, -0.9, 0] }
        ]
      },

      ctvt_lv: {
        id: 'ctvt_lv',
        name: '13.8 kV Bus Revenue Metering & Protection CT/VT (CTVT-LV)',
        tag: 'CT/VT-13.8',
        ansiNumber: 'IEEE C57.13 / ANSI 51/27/59/81',
        governingStandard: 'IEEE Std C57.13 / ANSI C12.11',
        overview: 'Dry-type butyl/cycloaliphatic epoxy instrument transformers sampling 13.8 kV bus voltage (120 V secondary) and main TR-01 secondary current (2000:5 A) for LV overcurrent, undervoltage, and OLTC AVR control.',
        specs: [
          { k: 'CT Ratio / Class', v: '2,000 / 5 A (0.3B1.8 Metering & C200 Relay)' },
          { k: 'VT Ratio / Connection', v: '14,400 : 120 V (120:1, Grounded-Wye / Wye)' },
          { k: 'Basic Impulse Level', v: '110 kV BIL (Outdoor Cycloaliphatic Resin)' }
        ],
        failureModes: [
          { title: 'Ferroresonance on Broken-Delta VT', desc: 'Single-phasing or switching transients saturate VT core into sustained harmonic overvoltage unless 100 Ω damping resistor is fitted.' }
        ],
        checklist: [
          'Verify CT shorting blocks inside marshalling box before meter testing.',
          'Check VT primary current-limiting fuse continuity.'
        ],
        subparts: [
          { id: 'lvct-tank', name: 'Cast Epoxy Dielectric Molding & Base', tag: 'LVCT-BODY', material: 'UV-Stabilized Cycloaliphatic Epoxy', role: 'Hermetically encapsulates toroidal CT and wound PT coils for outdoor service.', vector: [0, 1.4, 0] },
          { id: 'lvct-core', name: 'Dual Silicon-Steel Metering & Relay Cores', tag: 'LVCT-CORE', material: 'Grain-Oriented Steel Toroids', role: 'Maintains 0.3% revenue accuracy while avoiding saturation at 18.4 kA fault.', vector: [1.4, 0.3, 0] },
          { id: 'lvct-bushings', name: 'Primary H1/H2 Copper Tabs & Conduit Box', tag: 'LVCT-TERM', material: 'Silver-Plated NEMA Copper + Conduit', role: 'Routes 5 A and 120 V shielded twisted pairs to Control House Panel 2.', vector: [-1.4, 0.2, 0] }
        ]
      },

      ds_lv: {
        id: 'ds_lv',
        name: '13.8 kV Secondary Main Disconnect Switches (89-LV-A / 89-LV-B)',
        tag: 'DS-89LV',
        ansiNumber: 'ANSI 89-LV',
        governingStandard: 'IEEE Std C37.30',
        overview: 'Twin 3-pole gang-operated vertical/hook-stick air-break isolators flanking 52-LV on line and bus sides to provide visual LOTO isolation.',
        specs: [
          { k: 'Rating / BIL', v: '15 kV, 2,000 A continuous, 110 kV BIL' },
          { k: 'Momentary Withstand', v: '80 kA Crest' }
        ],
        failureModes: [
          { title: 'Jaw Heating at 1,745 A Continuous', desc: 'Loose copper-finger springs elevate temperature >85°C under peak evening load.' }
        ],
        checklist: [
          'Confirm 52-LV is open and locked out before pulling 89-LV.',
          'Perform annual IR thermography across jaw contacts.'
        ],
        subparts: [
          { id: 'lvds-frame', name: 'Galvanized Channel Base & Phase Turntables', tag: 'LVDS-FRM', material: 'Hot-Dip Galvanized Steel', role: 'Supports rigid phase insulators and interphase gang torsion shaft.', vector: [0, -0.8, 0] },
          { id: 'lvds-insulators', name: '15 kV Post Insulator Stacks (TR-205)', tag: 'LVDS-INS', material: 'Wet-Process Brown Porcelain', role: 'Provides 110 kV BIL live-to-frame isolation.', vector: [0, 1.0, 1.3] },
          { id: 'lvds-blades', name: 'Silver-Plated Dual Copper Truss Blades', tag: 'LVDS-BLD', material: 'High-Conductivity ETP Copper', role: 'Carries 2,000 A steady current with minimal contact drop.', vector: [0, 1.8, 0] },
          { id: 'lvds-linkage', name: 'Interphase Pipe Linkage & Padlock Handle', tag: 'LVDS-LNK', material: 'Galvanized Pipe + Lockout Plate', role: 'Synchronizes A/B/C blades and accepts crew LOTO padlocks.', vector: [0, 0.3, -1.5] }
        ]
      },

      cb_lv: {
        id: 'cb_lv',
        name: '13.8 kV Secondary Main Vacuum Circuit Breaker (52-LV)',
        tag: '52-LV (50/51)',
        ansiNumber: 'ANSI 52-LV (50/51/51G)',
        governingStandard: 'IEEE Std C37.04 / C37.06 / IEC 62271-100',
        overview: 'Outdoor dead-tank/porcelain-clad 15 kV Vacuum Circuit Breaker protecting the 13.8 kV main bus and coordinating downstream feeder relays against 18.4 kA secondary faults.',
        specs: [
          { k: 'Rated Voltage / Current', v: '15.0 kV Max / 2,000 A Continuous' },
          { k: 'Interrupting Rating', v: '31.5 kA RMS Symmetrical (3-Cycle Clearing)' },
          { k: 'Control / Trip Supply', v: '125 VDC Dual Shunt Trip Coils + Spring Charge' }
        ],
        failureModes: [
          { title: 'Loss of Vacuum Integrity', desc: 'Microscopic bellows leak allows air inside bottle; Hi-Pot test (36 kV AC) detects compromised dielectric vacuum.' }
        ],
        checklist: [
          'Perform 36 kV 1-minute AC bottle vacuum integrity Hi-Pot annually.',
          'Measure contact resistance (<30 µΩ) & contact wear indicator gauge.'
        ],
        subparts: [
          { id: 'lvcb-frame', name: 'Outdoor Skid Frame & Elevation Pedestal', tag: 'LVCB-FRM', material: 'Painted Galvanized Steel Frame', role: 'Elevates live vacuum interrupters and encloses spring operator linkage.', vector: [0, -1.1, 0] },
          { id: 'lvcb-vacuum-bottles', name: 'Sealed Alumina-Ceramic Vacuum Interrupters (×3)', tag: 'LVCB-VAC', material: '10⁻⁶ Torr Vacuum + CuCr Contacts', role: 'Extinguishes 31.5 kA arcs at first current zero in <12 ms via metal vapor diffusion.', vector: [0, 1.8, 0] },
          { id: 'lvcb-mech', name: '125 VDC Spring-Charge Operating Mechanism', tag: 'LVCB-MCH', material: 'High-Speed Cam & Trip Solenoids', role: 'Drives rapid 10 mm contact stroke and maintains 52a/52b auxiliary status.', vector: [1.4, 0.2, 0] },
          { id: 'lvcb-bushings', name: '15 kV Roof Entrance Sheds & Line Pads', tag: 'LVCB-BSH', material: 'Cycloaliphatic Epoxy + Tin-Cu', role: 'Terminates incoming TR-01 bus drops and outgoing 13.8 kV main bus.', vector: [-1.4, 1.1, 0] }
        ]
      },

      sst_100: {
        id: 'sst_100',
        name: '100 kVA Station Service Transformer (SST-100)',
        tag: 'SST-100',
        ansiNumber: '480Y/277V Station Auxiliary',
        governingStandard: 'IEEE Std C57.12.20 / ANSI C57.12.00',
        overview: 'Three-phase pole/pad oil-immersed step-down unit feeding Control House HVAC, battery chargers (125 VDC), TR-01 ONAF cooling fans, and yard security lighting directly from the 13.8 kV bus.',
        specs: [
          { k: 'Rated kVA / Ratio', v: '100 kVA, 13.8 kV Delta / 480Y-277 V' },
          { k: 'Impedance / Protection', v: 'Z = 3.2% / 10E Expulsion Fuses' }
        ],
        failureModes: [
          { title: 'Secondary Blackout → Battery Depletion', desc: 'If SST-100 trips off and charger stops, the 125 VDC battery sustains protection for only 8 hours.' }
        ],
        checklist: [
          'Verify 480V transfer panel auto-switchover and oil level gauge.',
          'Check silica dehydrator / relief valve.'
        ],
        subparts: [
          { id: 'sst-tank', name: 'Mineral-Oil Steel Tank & Cooling Fins', tag: 'SST-TNK', material: 'Welded Mild Steel + Mineral Oil', role: 'Dissipates 1.8 kW full-load core and copper losses passively (ONAN).', vector: [0, 0.2, 0] },
          { id: 'sst-hv-fuses', name: '13.8 kV Porcelain Bushings & Bay-O-Net Fuses', tag: 'SST-HV', material: 'Brown Porcelain + Current-Limiting Fuse', role: 'Isolates internal SST faults instantly without tripping 52-LV.', vector: [0, 1.8, 0] },
          { id: 'sst-core-windings', name: '100 kVA Silicon Steel Core & Copper Coils', tag: 'SST-CORE', material: 'CRGO Steel + Enameled Copper', role: 'Steps 13.8 kV down cleanly to 480Y/277 V 3-phase station power.', vector: [1.3, 0.4, 0] },
          { id: 'sst-lv-cabinet', name: '480V Secondary Terminal Compartment', tag: 'SST-LV', material: 'NEMA 3R Steel Cabinet + Conduit', role: 'Feeds Control House AC Panelboard & Battery Charger rectifiers.', vector: [-1.3, -0.3, 0] }
        ]
      },

      cap_bank: {
        id: 'cap_bank',
        name: '3.6 MVAR Switched Shunt Capacitor Bank (52-CAP)',
        tag: 'CAP-3.6MVAR',
        ansiNumber: 'IEEE Std 18 / 52-CAP + 59N',
        governingStandard: 'IEEE Std 18 / IEEE Std C37.99',
        overview: 'Rack-mounted double-wye/grounded-wye all-film capacitor cans switched via a 600 A zero-crossing vacuum switch with iron-core inrush limiting reactors to support 13.8 kV voltage and correct PF to ≥0.96.',
        specs: [
          { k: 'Reactive Output', v: '3.6 MVAR @ 13.8 kV (150.6 A nominal)' },
          { k: 'Unit Construction', v: '6x 200 kVAR All-Film Internall-Fused Cans per Phase' },
          { k: 'Switching Control', v: '600 A Synchronous Zero-Cross Vacuum Switch (52-CAP)' }
        ],
        failureModes: [
          { title: '5th/7th Harmonic Resonance Amplification', desc: 'Shunt capacitance may tune near harmonic system impedances; series reactors detune notch below 4.7th harmonic.' }
        ],
        checklist: [
          'Wait minimum 5 minutes after opening 52-CAP so internal discharge resistors drain cans below 50 V!',
          'Measure individual unit µF capacitance (±2% alert) and inspect cans for swelling.'
        ],
        subparts: [
          { id: 'cap-rack', name: 'Elevated Galvanized Aluminum/Steel Insulator Rack', tag: 'CAP-RCK', material: 'Hot-Dip Steel + 15 kV Standoffs', role: 'Elevates energized capacitor racks safely above ground with neutral imbalance CT.', vector: [0, -0.9, 0] },
          { id: 'cap-cans', name: 'All-Film Stainless Dielectric Capacitor Cans', tag: 'CAP-CANS', material: 'Polypropylene Film + Biodegradable Fluid', role: 'Supplies 3.6 MVAR leading reactive vars with <0.15 W/kVAR dielectric loss.', vector: [0, 1.5, 0] },
          { id: 'cap-reactors', name: 'Current-Limiting Air/Iron Inrush Reactors', tag: 'CAP-IND', material: 'Epoxy-Cast Copper Coils', role: 'Limits high-frequency back-to-back switching inrush currents (<5 kA).', vector: [1.4, 0.8, 0] },
          { id: 'cap-vcb', name: '15 kV 600 A Synchronous Capacitor Vacuum Switch (52-CAP)', tag: 'CAP-VCB', material: 'Transient-Free Restrike-Free VCB', role: 'Switches bank automatically on var/voltage schedule with minimal transient spikes.', vector: [-1.5, 0.6, 0] }
        ]
      },

      cb_f1: {
        id: 'cb_f1',
        name: 'Feeder 01 Vacuum Breaker & Bay (52-F1 / 89-F1)',
        tag: '52-F1 Bay',
        ansiNumber: 'ANSI 52-F1 (50/51/51N/79)',
        governingStandard: 'IEEE Std C37.230',
        overview: 'Primary 13.8 kV feeder bay supplying the Commercial, Industrial & Residential distribution trunk via 1,200 A vacuum breaker, 4-shot ANSI 79 auto-reclosing, and flanked isolation disconnects.',
        specs: [
          { k: 'Breaker Rating', v: '15 kV, 1,200 A, 25 kA Symmetrical' },
          { k: 'Reclosing Sequence', v: '79: Instantaneous + 0.5 s + 2.0 s + 15 s Lockout' }
        ],
        failureModes: [
          { title: 'Sympathetic Tripping on Adjacent Feeder Fault', desc: 'Excessive voltage sag or poorly set 51N ground pickup causes unnecessary trip.' }
        ],
        checklist: [
          'Verify ANSI 79 recloser enable selector switch position before live-line work.',
          'Check 1200/5 A feeder CT secondary links.'
        ],
        subparts: [
          { id: 'f1-frame', name: 'Galvanized Breaker Pedestal & Bypass Rack', tag: 'F1-FRM', material: 'Hot-Dip Structural Steel', role: 'Supports 52-F1 tank, disconnects, and bypass bus work.', vector: [0, -0.9, 0] },
          { id: 'f1-vcb', name: '52-F1 1,200 A Vacuum Circuit Breaker Tank', tag: 'F1-VCB', material: '15 kV Vacuum Interrupter Unit', role: 'Clears persistent distribution faults in 3 cycles and auto-recloses per 79.', vector: [0, 1.5, 0] },
          { id: 'f1-disconnects', name: '89-F1A / 89-F1B Flanking Air-Break Disconnects', tag: 'F1-DISC', material: '15 kV Copper-Blade Isolators', role: 'Visually isolates 52-F1 for maintenance while Feeder 02 remains live.', vector: [-1.3, 1.1, 0] },
          { id: 'f1-relay-ct', name: '1200/5 A Feeder Sensing CTs & Ground Box', tag: 'F1-CT', material: 'Window CTs + Shielded Harness', role: 'Feeds 50/51/51N Feeder Relay on Panel 2 inside Control House.', vector: [1.3, 0.7, 0] }
        ]
      },

      cb_f2: {
        id: 'cb_f2',
        name: 'Feeder 02 Vacuum Breaker & Bay (52-F2 / 89-F2)',
        tag: '52-F2 Bay',
        ansiNumber: 'ANSI 52-F2 (50/51/51N/79)',
        governingStandard: 'IEEE Std C37.230',
        overview: 'Parallel 13.8 kV distribution feeder bay serving heavy industrial backup and south feeder zone via 1,200 A vacuum circuit breaker and twin disconnect switches.',
        specs: [
          { k: 'Breaker Rating', v: '15 kV, 1,200 A, 25 kA Symmetrical' },
          { k: 'Normal Load Share', v: '19.7 MVA (824 A @ 13.8 kV)' }
        ],
        failureModes: [
          { title: 'Cold Load Pickup Trip', desc: 'Extended outage magnetizes distribution transformers and inrush motors up to 3x rated; cold-load timer raises pickup temporarily.' }
        ],
        checklist: [
          'Check 89-F2A/B alignment and mechanical stop bolts.',
          'Test local/remote trip & close control switches.'
        ],
        subparts: [
          { id: 'f2-frame', name: 'Galvanized Breaker Pedestal & Support Channel', tag: 'F2-FRM', material: 'Hot-Dip Structural Steel', role: 'Mounts Feeder 02 switchgear and 15 kV riser insulators.', vector: [0, -0.9, 0] },
          { id: 'f2-vcb', name: '52-F2 1,200 A Vacuum Circuit Breaker', tag: 'F2-VCB', material: '15 kV Vacuum Interrupter Unit', role: 'Protects Feeder 02 trunk with programmable TCC and ANSI 79 auto-reclosing.', vector: [0, 1.5, 0] },
          { id: 'f2-disconnects', name: '89-F2A / 89-F2B Isolation Switches', tag: 'F2-DISC', material: '15 kV Copper-Blade Isolators', role: 'Provides double air-break isolation for LOTO clearance on Feeder 02.', vector: [-1.3, 1.1, 0] },
          { id: 'f2-relay-ct', name: '1200/5 A Metering/Protection CTs', tag: 'F2-CT', material: 'Resin-Cast Window CTs', role: 'Supplies phase & residual currents to Feeder 02 protection relay.', vector: [1.3, 0.7, 0] }
        ]
      },

      dist_recloser: {
        id: 'dist_recloser',
        name: 'Pole-Mounted Automatic Circuit Recloser (79-ACR1)',
        tag: '79-ACR1',
        ansiNumber: 'ANSI 79 / IEEE C37.60',
        governingStandard: 'IEEE Std C37.60 / IEC 62271-111',
        overview: 'Microprocessor-controlled 15.5 kV three-phase vacuum recloser installed on Pole #1 of Feeder 01 implementing a 2-Fast (Curve A) + 2-Slow (Curve B/C) Fuse-Saving coordination scheme.',
        specs: [
          { k: 'Voltage / Continuous Current', v: '15.5 kV Max / 560 A Continuous (110 kV BIL)' },
          { k: 'Interrupting Capacity', v: '12.5 kA RMS Symmetrical (Vacuum in Solid Dielectric)' },
          { k: 'Reclosing Sequence', v: '2 Fast Shots (Curve A, 0.5 s dead) + 2 Slow (Curve B/C, 2.0 s dead) -> Lockout' },
          { k: 'Transient Clearing Share', v: 'Clears ~80% of temporary lightning/tree faults before 100K lateral fuse melts' }
        ],
        failureModes: [
          { title: 'Loss of Fast Curve Enable (Switch in Slow-Only)', desc: 'Disabling fast curve allows temporary lightning faults to blow lateral fuses unnecessarily, worsening utility SAIDI/SAIFI.' }
        ],
        checklist: [
          'Verify Form 6 / SEL-651R controller AC PT supply and 24V sealed battery backup.',
          'Confirm yellow manual-trip/non-reclose hookstick handle hangs straight down in AUTO mode.'
        ],
        subparts: [
          { id: 'rec-tank', name: 'Solid Epoxy / Stainless Top Manifold Tank', tag: 'REC-TNK', material: 'Hydrophobic Cycloaliphatic Epoxy & 304 SS', role: 'Houses magnetic actuator coils and internal toroidal CTs in maintenance-free housing.', vector: [0, 0.4, 0] },
          { id: 'rec-interrupters', name: '3-Phase Embedded Vacuum Interrupter Modules', tag: 'REC-VAC', material: 'Alumina Ceramic + CuCr Contacts', role: 'Interrupts 12.5 kA fault currents rapidly under magnetic actuator drive (<15 ms).', vector: [0, 1.5, 0] },
          { id: 'rec-bushings', name: '15.5 kV Silicone Polymer Creepage Bushings', tag: 'REC-BSH', material: 'HTV Silicone Polymer + Bird Guards', role: 'Provides wildlife-safe overhead connections and 110 kV BIL insulation.', vector: [1.3, 1.1, 0] },
          { id: 'rec-control-box', name: 'Pole-Base Digital Recloser Control Cabinet', tag: 'REC-CTL', material: 'NEMA 4X Aluminum + SEL/Form-6 Relay', role: 'Tracks fault count, executes Curve A/B/C timing, and communicates SCADA FLISR status.', vector: [-1.4, -1.2, 0] }
        ]
      },

      dist_sectionalizer: {
        id: 'dist_sectionalizer',
        name: 'Automatic Line Sectionalizer (34-SECT)',
        tag: '34-SECT',
        ansiNumber: 'ANSI 34 / IEEE C37.63',
        governingStandard: 'IEEE Std C37.63',
        overview: 'Fault-counting sectionalizing switch installed downstream of Recloser 79-ACR1. It NEVER interrupts fault current itself; instead it counts upstream recloser fault-zero open pulses and drops open ONLY during the recloser zero-current dead time (Count = 2).',
        specs: [
          { k: 'Voltage / Continuous Current', v: '15.5 kV, 400 A Continuous' },
          { k: 'Interrupting Rating', v: '0 A Fault Interrupting (Opens Strictly Under Zero-Current Dead Time!)' },
          { k: 'Actuation Logic', v: 'Armed above 160 A fault -> Opens during Recloser #2 Dead-Time (<0.5 s)' },
          { k: 'Coordination Benefit', v: 'Needs NO time-current margin (CTI = 0 s) because it counts shots instead of racing curves' }
        ],
        failureModes: [
          { title: 'Wrong Count Setting vs Upstream Recloser', desc: 'Setting Sectionalizer count ≥ Recloser lockout shots causes upstream lockout before sectionalizer can isolate the faulted branch.' }
        ],
        checklist: [
          'Verify mechanical/electronic shot count set strictly ≤ (Upstream Recloser Lockout - 1).',
          'Check manual drop-out isolator links after dead-time operation.'
        ],
        subparts: [
          { id: 'sect-frame', name: 'Hot-Dip Steel Crossarm Mounting Frame', tag: 'SECT-FRM', material: 'Galvanized Channel Assembly', role: 'Spans 3-phase pole crossarm and anchors torsional trip shafts.', vector: [0, -0.7, 0] },
          { id: 'sect-insulators', name: '15.5 kV Silicone Suspension/Post Standoffs', tag: 'SECT-INS', material: 'Silicone Rubber Over FRP Rod', role: 'Supports switched contact hinge blades at 110 kV BIL.', vector: [1.2, 0.8, 0] },
          { id: 'sect-actuators', name: 'Latch Release Solenoid & Dropout Drop-Blades', tag: 'SECT-ACT', material: 'Spring-Loaded Copper Dropout Contacts', role: 'Releases latch precisely during upstream recloser open interval to clear dead branch.', vector: [0, 1.5, 0] },
          { id: 'sect-counter', name: 'Current-Sensing Toroid & Pulse Count Register', tag: 'SECT-CNT', material: 'Self-Powered CT + Electronic Logic', role: 'Detects fault pickup (>160 A) followed by current-zero dead-time transition.', vector: [-1.3, -0.3, 0] }
        ]
      },

      dist_fuse_cutout: {
        id: 'dist_fuse_cutout',
        name: '15 kV Expulsion Fuse Cutout (100K Lateral Tap)',
        tag: 'FUSE-100K',
        ansiNumber: 'IEEE C37.41 / 100K',
        governingStandard: 'IEEE Std C37.41 / C37.42',
        overview: 'Lateral branch expulsion cutout fitted with a 100K tin fuse link, coordinated in Fuse-Saving mode with upstream Recloser 79-ACR1 so transient faults clear on Curve A while permanent lateral faults blow and visibly drop open the fiberglass fuse tube at 180 deg.',
        specs: [
          { k: 'Voltage / Frame Current', v: '15 kV Class / 100 A Frame (100K Tin Link)' },
          { k: 'Interrupting Rating', v: '10 kA Asymmetrical RMS' },
          { k: 'Coordination Window', v: 'Coordinated strictly between 79-ACR1 Curve A (Fast) and Curve B (Slow)' }
        ],
        failureModes: [
          { title: 'Nuisance Fuse Blowing on Lightning Transient', desc: 'Occurs if upstream 79-ACR1 fast shot is disabled or improperly sized.' }
        ],
        checklist: [
          'Verify arc-chute bore inside fiberglass tube is unobstructed before re-fusing.',
          'Always pull/close with insulated telescopic hot-stick and loadbreak tool.'
        ],
        subparts: [
          { id: 'fuse-bracket', name: 'NEMA Crossarm Steel Mounting Bracket', tag: 'FUSE-BRK', material: 'Galvanized Steel Hook Bracket', role: 'Bolts directly to wooden/concrete utility crossarm.', vector: [0, -0.7, 0] },
          { id: 'fuse-insulator', name: '15 kV Zig-Zag Silicone C-Shaped Insulator', tag: 'FUSE-INS', material: 'Shedded Silicone / Porcelain C-Frame', role: 'Holds top bronze contact hood and bottom trunnion hinge.', vector: [-1.2, 0.4, 0] },
          { id: 'fuse-tube', name: 'Bone-Fiber Lined Fiberglass Arc-Quench Fuseholder', tag: 'FUSE-TUBE', material: 'Vulcanized Bone Fiber + Epoxiglass', role: 'Generates high-pressure non-conductive gas blast during melt to quench fault arc and drops 180° visually open.', vector: [1.3, 0.9, 0] },
          { id: 'fuse-link', name: '100K Tin Fuse Button & Flexible Copper Leader Tail', tag: 'FUSE-LNK', material: 'Eutectic Tin Element + Braided Cu Tail', role: 'Melts along IEEE K-speed curve on persistent overcurrent to unlatch tube.', vector: [0.4, -1.2, 0] }
        ]
      },

      dist_arrester: {
        id: 'dist_arrester',
        name: '10 kV Heavy-Duty Distribution Surge Arrester (SA-DIST)',
        tag: 'SA-10kV',
        ansiNumber: 'IEEE C62.11 Distribution',
        governingStandard: 'IEEE Std C62.11',
        overview: 'Compact dark-porcelain/polymer distribution MOV arrester safeguarding overhead pole transformers, reclosers, and lateral risers from induced lightning surges, equipped with an explosive ground-lead disconnector cartridge.',
        specs: [
          { k: 'Rating / MCOV', v: '10 kV Duty Cycle / 8.4 kV MCOV (69/13.8kV Grounded Wye)' },
          { k: 'Ground Isolator', v: 'Explosive Cartridge Disconnector flags blown arrester visually' }
        ],
        failureModes: [
          { title: 'Failed Arrester Ground Fault Lockout', desc: 'If cartridge disconnector fails to fire, a shorted MOV block holds a permanent SLG fault on Feeder 01.' }
        ],
        checklist: [
          'Scan pole crossarm visually from road for dangling white ground isolator flag.',
          'Confirm bird guard wildlife cap is snapped over hot top stud.'
        ],
        subparts: [
          { id: 'da-cap', name: 'Insulated Wildlife Bird-Guard Cap & Stud', tag: 'DA-CAP', material: 'UV Polycarbonate + Bronze Clamp', role: 'Prevents raptor/squirrel phase-to-crossarm flashovers.', vector: [0, 1.5, 0] },
          { id: 'da-zno', name: '8.4 kV MCOV Zinc-Oxide Varistor Pellets', tag: 'DA-MOV', material: 'Pressed MOV Disc Stack', role: 'Diverts up to 65 kA high-current 4/10 µs nearby lightning strikes.', vector: [1.1, 0.4, 0] },
          { id: 'da-sheds', name: 'Distribution Weather Shed Housing', tag: 'DA-SHED', material: 'Dark Glazed Porcelain / Polymer', role: 'Encapsulates ZnO stack across 15 kV BIL clearance.', vector: [-1.1, 0.4, 0] },
          { id: 'da-isolator', name: 'Explosive Ground-Lead Disconnector Cartridge', tag: 'DA-DISC', material: 'Arc-Triggered Powder Capsule', role: 'Cleanly severs ground tail during internal MOV failure so recloser 79 can re-energize line.', vector: [0, -1.0, 0] }
        ]
      },

      substation_b: {
        id: 'substation_b',
        name: 'Neighboring Tie Substation B & Loop Tie Recloser (79-TIE)',
        tag: 'SUB-B / 79-TIE',
        ansiNumber: 'FLISR N-1 Tie Source',
        governingStandard: 'IEEE Std 1547 / SCADA FLISR Loop Scheme',
        overview: 'Adjacent 69/13.8 kV distribution substation located at the eastern boundary of Feeder 01, interconnected via Normally-Open Automated Loop Tie Recloser 79-TIE. Executes automated Fault Location, Isolation, and Service Restoration (FLISR) to back-feed un-faulted downstream Commercial & Industrial loads.',
        specs: [
          { k: 'Substation B Capacity', v: '41.7 MVA, 69 / 13.8 kV Tie Source' },
          { k: 'Normal Tie State', v: '79-TIE NORMALLY OPEN (Prevents Parallel Circulating Current)' },
          { k: 'FLISR Auto-Transfer Time', v: '< 4.2 seconds (Isolate 79-ACR1/34-SECT -> Close 79-TIE)' },
          { k: 'Customers Served Downstream', v: 'Industrial Plant (1500 kVA) + Commercial Center (750 kVA)' }
        ],
        failureModes: [
          { title: 'Out-of-Phase Sync Closure', desc: 'Tie recloser sync-check relay (ANSI 25) must confirm delta-V < 5% and delta-angle < 15 deg or dead-bus on Feeder 01 before closing.' }
        ],
        checklist: [
          'Verify ANSI 25 Synchrocheck & Dead-Line-One-Side logic enabled before FLISR transfer.',
          'Check SCADA DNP3 comms heartbeats between Main Substation and Substation B RTUs.'
        ],
        subparts: [
          { id: 'subb-xfmr', name: 'Substation B 69/13.8 kV Tie Power Transformer', tag: 'SUBB-TX', material: '41.7 MVA Mineral-Oil Tie Unit', role: 'Maintains independent 13.8 kV (1.00 pu) voltage source for N-1 loop transfer.', vector: [1.8, 0.8, 0] },
          { id: 'subb-tie-recloser', name: 'Normally-Open Automated Loop Tie Recloser (79-TIE)', tag: '79-TIE', material: '15.5 kV 630 A Motorized Vacuum Recloser', role: 'Automatically closes upon SCADA FLISR command to back-feed healthy eastern load sections.', vector: [-1.8, 0.5, 0] },
          { id: 'subb-bus-rack', name: 'Substation B 13.8 kV Dead-End Tie Gantry', tag: 'SUBB-BUS', material: 'Galvanized Steel H-Frame', role: 'Receives the 13.8 kV open-tie overhead span from Feeder 01 east boundary.', vector: [0, 1.8, 0] },
          { id: 'subb-rtu', name: 'Substation B DNP3 SCADA RTU & Sync-Check Panel', tag: 'SUBB-RTU', material: 'NEMA Control Enclosure + ANSI 25', role: 'Coordinates phase verification and directional fault isolation with Main Control House.', vector: [0, -1.0, 1.5] }
        ]
      },

      dt_res_50: {
        id: 'dt_res_50',
        name: 'Residential Pole-Mounted Distribution Transformer (DT-RES-50)',
        tag: 'DT-RES-50 (50 kVA)',
        ansiNumber: 'IEEE C57.12.20 Overhead 1φ / ANSI 46',
        governingStandard: 'IEEE Std C57.12.20 / NESC / PEC Part 2',
        overview: '50 kVA 7,967Y/13.8 kV-to-240/120 V single-phase pole-mounted overhead distribution transformer feeding the residential lateral. Complete with ANSI 70 steel tank, radiator cooling fins, glazed porcelain HV/LV bushings with wildlife guard, expulsion fuse cutout (ANSI 46), hot-line tap clamp, SA-10kV surge arrester, and driven ground rod.',
        specs: [
          { k: 'Rated kVA & Voltage', v: '50 kVA Continuous (65°C Rise) | 7.97 kV L-N -> 240/120 V 3-Wire' },
          { k: 'Primary / Secondary FLA', v: 'I1 = 6.28 A @ 7.97 kV | I2 = 208.3 A @ 240 V (2.1% Z)' },
          { k: 'Primary Cutout & Link', v: '15 kV 100 A Expulsion Cutout (ANSI 46) w/ 10T (1.6x I1) Fuse Link' },
          { k: 'Surge Protection & Ground', v: '10 kV / 8.4 kV MCOV Tank-Boss MOV Arrester -> 5/8" x 8 ft Cu Rod' }
        ],
        failureModes: [
          { title: 'Bird / Squirrel Flashover at H1 Bushing', desc: 'Mitigated by cover-mounted polymer wildlife guard over glazed porcelain H1/H2 bushings and insulated primary riser lead.' },
          { title: 'Neutral / Case Float Under Fault', desc: 'Secondary center-tap X2 is solidly bonded to tank ground strap and driven copper-clad pole butt rod alongside arrester ground.' }
        ],
        checklist: [
          'Verify 10T/10K fuse link seated cleanly in cutout toggle trunnion and hot-line clamp tight on 13.8 kV stirrup.',
          'Confirm arrester ground-lead disconnector intact and common bonding between arrester, tank lug, and X2 neutral.'
        ],
        subparts: [
          { id: 'dt-tank-fins', name: 'ANSI 70 Rolled-Steel Tank, Radiator Fins & Mounting Brackets', tag: 'TANK', material: ' Mild Steel ANSI 70 Gray + Galvanized Lug Brackets', role: 'Contains dielectric mineral oil, dissipates core/I²R heat, and bolts onto wood distribution pole.', vector: [-0.9, 0.0, 0.0] },
          { id: 'dt-core-coil', name: 'Silicon-Steel Core, HV/LV Windings & Tap Changer', tag: 'CORE', material: 'CRGO Steel + Formvar Copper/Al Windings', role: 'Steps 7,967 V L-N down to center-tapped 240/120 V split-phase via +/-2.5% de-energized tap changer.', vector: [0.0, 1.35, 0.0] },
          { id: 'dt-hv-bushing', name: 'Glazed Brown Porcelain H1/H2 Bushing & Wildlife Guard', tag: 'H1/H2', material: 'Wet-Process Glazed Porcelain + UV Polymer Guard', role: 'Maintains 95 kV BIL clearance from tank cover while shielding live terminal from raptor/squirrel contact.', vector: [0.0, 2.1, -0.45] },
          { id: 'dt-lv-bushings', name: 'Side-Wall X1/X2/X3 Secondary Bushings & Triplex Drops', tag: 'X1-X3', material: 'Porcelain Spade Studs + #2/0 ACSR Triplex', role: 'Feeds 240/120 V split-phase power out to adjacent residential customer weatherhead service entrances.', vector: [0.95, 0.25, 0.85] },
          { id: 'dt-fuse-cutout', name: 'Primary Expulsion Fuse Cutout (ANSI 46) & Hot-Line Clamp', tag: '46-FUSE', material: '15 kV Silicone C-Frame + Bronze Tap Clamp', role: 'Isolates internal transformer faults with visible dropout tube and allows hot-stick live tapping via stirrup.', vector: [-0.85, 1.55, 0.65] },
          { id: 'dt-arrester-ground', name: 'Distribution Surge Arrester (SA-10kV) & Driven Ground Rod', tag: 'SA-GND', material: '8.4 kV MCOV ZnO Discs + 5/8"x8ft Cu-Clad Rod', role: 'Diverts lightning surges cleanly into earth while isolating failed arresters via explosive disconnector.', vector: [0.85, 0.95, -0.75] }
        ]
      },

      dt_com_750: {
        id: 'dt_com_750',
        name: 'Commercial Business District (CBD) 750 kVA Pad-Mounted Transformer & ATS (DT-COM-750)',
        tag: 'DT-COM-750 (CBD · 750 kVA)',
        ansiNumber: 'IEEE C57.12.34 Pad / Hospital ATS & Office Towers',
        governingStandard: 'IEEE Std C57.12.34 / NFPA 110 / NEC Art. 450 & 700',
        overview: '750 kVA three-phase pad-mounted distribution transformer (13.8 kV Delta primary to 480Y/277 V secondary) serving the Commercial Business District: multi-story Glass Curtain-Wall Office Tower, Shopping Mall / Supermarket Complex, and Regional Hospital (equipped with emergency diesel backup generator & Automatic Transfer Switch ATS).',
        specs: [
          { k: 'Rated kVA & CBD Loads', v: '750 kVA Continuous | Office Tower + Mall + Hospital + LED Blvd Lighting' },
          { k: 'Primary / Secondary FLA', v: 'I1 = 31.4 A @ 13.8 kV | I2 = 902.1 A @ 480 V (5.3% Z)' },
          { k: 'Riser Fuses & Hospital ATS', v: '3× 50T/65K Riser Fuses + NFPA 110 10-sec Emergency Diesel Generator ATS' },
          { k: 'Lightning & Grounding', v: '3× SA-10kV (8.4 kV MCOV) Arresters + Dual Driven 5/8"x8ft Ground Rods' }
        ],
        failureModes: [
          { title: 'Single-Phasing Motor Damage & Hospital Transfer', desc: 'Expulsion fuse blowout on one phase triggers hospital under-voltage relay (27), starting the backup diesel generator and shifting critical life-safety loads via ATS.' }
        ],
        checklist: [
          'Verify 3-phase fuse links matched to 50T/65K coordination table above 480 V main breaker.',
          'Confirm hospital emergency generator fuel level and ATS transfer test readiness.',
          'Check cooling fin louvers and secondary X0 neutral ground grid bonding.'
        ],
        subparts: [
          { id: 'dt-tank-fins', name: '750 kVA Heavy-Gauge Tank, Cooling Radiators & Mounting Skid', tag: 'TANK', material: 'Pad-Green Coated Steel (Munsell 7GY)', role: 'Encapsulates 3-phase core-coil bank with welded vertical radiator fin banks and pressure relief device.', vector: [-0.9, 0.0, 0.0] },
          { id: 'dt-core-coil', name: '3-Phase 3-Leg Core, Coils & 5-Tap De-Energized Changer', tag: 'CORE', material: 'Silicon Steel + Copper Foil LV Windings', role: 'Transforms 13.8 kV three-phase down to 480Y/277 V commercial building distribution.', vector: [0.0, 1.35, 0.0] },
          { id: 'dt-hv-bushing', name: '3-Phase Porcelain Primary Bushings (H1-H2-H3) & Wildlife Guards', tag: 'H1-H3', material: 'Glazed Brown Porcelain (95 kV BIL)', role: 'Receives 13.8 kV primary riser cables feeding the Commercial District.', vector: [0.0, 2.1, -0.45] },
          { id: 'dt-lv-bushings', name: 'Secondary 480Y/277 V Spade Bushings (X0-X1-X2-X3) & Drops', tag: 'X0-X3', material: 'Tin-Plated Copper Spades + Parallel 500 kcmil', role: 'Delivers 902 A secondary service to Office Tower, Mall, and Hospital ATS.', vector: [0.95, 0.25, 0.85] },
          { id: 'dt-fuse-cutout', name: '3-Phase Expulsion Fuse Cutouts & Bay-O-Net Loadbreak Fuses', tag: '46-3PH', material: '15 kV Cutout Trio + Dual-Sensing Bay-O-Net', role: 'Protects commercial riser bank while maintaining selective coordination with 34-SECT.', vector: [-0.85, 1.55, 0.65] },
          { id: 'dt-arrester-ground', name: '3× SA-10kV Arresters & Common Ground Rod Loop', tag: 'SA-3PH', material: '8.4 kV MCOV MOV + 4/0 Cu Ground Lead', role: 'Clamps switching and lightning transients before HV bushings.', vector: [0.85, 0.95, -0.75] }
        ]
      },

      dt_ind_1500: {
        id: 'dt_ind_1500',
        name: 'Dedicated HV Customer Industrial Substation (69 / 138 kV · 20–30 MVA)',
        tag: 'CUST-IND-HV (52-CUST · 25 MVA)',
        ansiNumber: 'IEEE C57.12.10 Customer-Owned HV Step-Down Station',
        governingStandard: 'IEEE Std C57.12.10 / IEEE 141 / IEEE 242 Buff Book',
        overview: 'Customer-owned high-voltage industrial substation isolated on the North Industrial ROW corridor and supplied directly at 69 kV (or 138 kV on EHV tiers) via dedicated sub-transmission bay 52-IND—never from the 13.8 kV public city feeders. Steps bulk sub-transmission down via a 25 MVA power transformer (52-CUST) to 4.16 kV / 13.8 kV plant switchgear feeding electric-arc steel furnaces, rolling mills, and cooling towers.',
        specs: [
          { k: 'Dedicated HV Supply', v: '69 kV (Tiers 1–2) or 138 kV (Tiers 3–4) Sub-Transmission Line off 52-IND' },
          { k: 'Customer Power TX', v: '25 MVA (20/26.7/33 MVA) ONAN/ONAF Dyn11 | 69→4.16 kV or 138→13.8 kV (Z = 8.5%)' },
          { k: 'HV / Plant FLA', v: 'I_HV = 209.2 A @ 69 kV (104.6 A @ 138 kV) | I_LV = 3,470 A @ 4.16 kV' },
          { k: 'Protection & Perimeter', v: 'Dedicated 52-CUST HV Breaker + 87T Diff + 3.0 m Precast Concrete Security Wall' }
        ],
        failureModes: [
          { title: 'Arc-Furnace Flicker & Harmonic Injection', desc: 'Large industrial EAF / rolling mill VFD loads draw high reactive swings; dedicated 69/138 kV feeder 52-IND completely decouples voltage flicker from city 13.8 kV residential/hospital buses!' }
        ],
        checklist: [
          'Confirm 52-IND substation bay and 52-CUST customer main breaker maintain selective 21/51-IND coordination.',
          'Inspect 69/138 kV steel lattice sub-transmission corridor clearances and customer precast security wall interlocks.'
        ],
        subparts: [
          { id: 'dt-tank-fins', name: 'Customer 25 MVA Steel Tank, Oil Conservator & ONAF Radiator Banks', tag: 'TANK', material: 'ANSI 70 Welded Steel + Forced-Air Cooling Banks', role: 'Dissipates continuous heavy steel-mill and motor-starting thermal duty.', vector: [-0.95, 0.0, 0.0] },
          { id: 'dt-core-coil', name: '25 MVA Grain-Oriented Core, LTC Winding & Tap Changer', tag: 'CORE/LTC', material: 'CRGO Silicon Core + Copper Helical Windings', role: 'Steps dedicated 69/138 kV sub-transmission down to 4.16/13.8 kV plant utilization bus.', vector: [0.0, 1.45, 0.0] },
          { id: 'dt-hv-bushing', name: '69 / 138 kV Condenser Porcelain Bushings (H1/H2/H3) & Corona Rings', tag: 'HV-BUSH', material: '350/650 kV BIL Oil-Impregnated Condenser Bushings', role: 'Terminates incoming 69/138 kV steel-tower sub-transmission leads cleanly into tank.', vector: [0.0, 2.35, -0.5] },
          { id: 'dt-lv-bushings', name: '3,470 A Enclosed Bus-Duct Throat & 4.16/13.8 kV Switchgear Feed', tag: 'BUS-DUCT', material: 'Ventilated Copper Busway into Metal-Clad Switchgear', role: 'Delivers bulk industrial power directly into 4.16 kV plant switchgear lineup.', vector: [1.05, 0.25, 0.85] },
          { id: 'dt-fuse-cutout', name: '52-CUST Customer Main SF6 Breaker & 89-CUST Motor Disconnect', tag: '52-CUST', material: '69/138 kV Live-Tank SF6 Breaker + 1200 A Knife Switch', role: 'Provides local customer fault clearing and visible air-gap isolation off the utility HV line.', vector: [-0.95, 1.65, 0.7] },
          { id: 'dt-arrester-ground', name: 'Station-Class HV MOV Arresters & Customer IEEE 80 Ground Grid', tag: 'SA-GND', material: '60/120 kV Polymer MOV Arresters + 4/0 Cu Mesh', role: 'Protects customer 25 MVA winding BIL against switching and sub-transmission lightning surges.', vector: [0.9, 1.0, -0.8] }
        ]
      },

      urd_riser_pole: {
        id: 'urd_riser_pole',
        name: 'URD Subdivision Overhead-to-Underground Transition (Dip / Riser) Pole',
        tag: 'URD RISER POLE (15 kV)',
        ansiNumber: 'IEEE Std 48 / NESC Rule 239',
        governingStandard: 'IEEE Std 48 / IEEE C62.11 / NESC Rule 239',
        overview: 'Three-phase Overhead-to-Underground transition structure at the Gated Residential Subdivision entrance. Steps Feeder 01 lateral overhead conductors down into buried 15 kV / 25 kV XLPE concentric-neutral URD primary loop cables via expulsion fuse cutouts, riser-pole MOV surge arresters, cold-shrink stress-cone pothead terminations, and Schedule 80 galvanized steel conduit dipping underground.',
        specs: [
          { k: 'Primary Transition Rating', v: '15 kV Class (13.8 kV L-L / 7.97 kV L-N) · 95 kV / 110 kV BIL' },
          { k: 'Cable Terminations', v: '3× IEEE Std 48 Class 1 Silicone Rubber Stress-Cone Potheads w/ Rain Sheds' },
          { k: 'Traveling-Wave Protection', v: '3× 10 kV MOV Riser Arresters (8.4 kV MCOV) Mounted Closest to Potheads' },
          { k: 'Riser Conduit & Bending', v: '4" Galvanized RGS / Schedule 80 U-Guard Conduit · Sweep R ≥ 12× Cable OD' }
        ],
        failureModes: [
          { title: 'Traveling-Wave Reflected Overvoltage', desc: 'Because underground XLPE surge impedance (~35 Ω) transitions to an open/radial loop end (~2× reflection), riser arresters MUST stay connected tightly at the pothead top.' },
          { title: 'Water Treeing & Moisture Ingress', desc: 'Cracked weather-seal boots at the stress cone allow moisture into stranded aluminum/copper conductor and accelerate insulation failure.' }
        ],
        checklist: [
          'Verify riser arresters use shortest possible lead length directly to pothead lugs and #4 Cu down-ground.',
          'Check 3-phase expulsion cutout fuses (65T/80K) and Schedule 80 U-guard seal at concrete apron grade.'
        ],
        subparts: [
          { id: 'riser-potheads', name: '3-Phase Stress-Cone Cable Terminations (Potheads)', tag: 'POTHEAD', material: 'Silicone Rubber Tracking-Resistant Sheds + Stress Cone', role: 'Relieves longitudinal electric field stress where grounded XLPE shield ends and exposes HV conductor to air.', vector: [0.0, 1.5, 0.0] },
          { id: 'riser-arresters-cutouts', name: 'Riser Expulsion Fuse Cutouts & 10 kV MOV Arresters', tag: '46 / SA', material: '15 kV Cutouts + Polymer MOV Riser Arresters', role: 'Interrupts underground loop cable faults cleanly and clamps surge reflections entering XLPE cable.', vector: [-0.9, 1.1, -0.6] },
          { id: 'riser-conduit-duct', name: 'Galvanized Steel Riser Conduit, Stand-Off Brackets & U-Guard', tag: 'CONDUIT', material: 'Schedule 80 RGS Pipe + Concrete Sweep Elbow', role: 'Protects 15 kV XLPE concentric-neutral cables from UV, mechanical impact, and mowing crews down into trench.', vector: [0.8, -0.6, 0.7] }
        ]
      },

      dt_urd_pad: {
        id: 'dt_urd_pad',
        name: 'Gated URD Dead-Front Loop-Feed Pad-Mounted Transformer (150 kVA)',
        tag: 'DT-URD-PAD (ANSI C57.12.26)',
        ansiNumber: 'IEEE C57.12.26 / IEEE 386 Dead-Front',
        governingStandard: 'IEEE Std C57.12.26 / IEEE Std 386 / ANSI Z535',
        overview: 'Low-profile, tamper-resistant green (Munsell 7GY 3.29/1.5) dead-front loop-feed pad-mounted transformer inside the Gated URD Subdivision. Zero exposed live parts or overhead wires: 15 kV XLPE cables terminate via 200 A Loadbreak Elbows on H1A/H1B feed-thru bushing wells allowing bidirectional sectionalizing around any faulted underground segment.',
        specs: [
          { k: 'Rating & Voltage', v: '150 kVA ONAN 65°C Rise | 13.8 kV Loop Primary -> 240/120 V URD Street Pedestals' },
          { k: 'HV Compartments (IEEE 386)', v: '200 A 15/25 kV Loadbreak Elbow Connectors on H1A / H1B Loop-Feed Wells' },
          { k: 'Internal Protection', v: 'Externally Removable Bay-O-Net Expulsion Fuse + Partial-Range ELSP Limit Fuse' },
          { k: 'Clearance & Vault Pad', v: 'Precast Concrete Box Pad + Locking Penta-Bolt Cabinet (Zero Exposed Live Metal)' }
        ],
        failureModes: [
          { title: 'Improper Loadbreak Elbow Parking / Flash', desc: 'Failure to use insulated hot-stick shotgun tool when pulling 200 A loadbreak elbows or failing to ground concentric neutral drains causes internal compartment arc-flash.' },
          { title: 'Bay-O-Net Drip onto Oil Tank', desc: 'Must relieve internal tank gas pressure via pull-ring valve before withdrawing Bay-O-Net fuse cartridge.' }
        ],
        checklist: [
          'Confirm Munsell green cabinet penta-bolt lock and padlock engaged after switching.',
          'Check 200 A loadbreak elbows seated to yellow latch indicator ring and parking stand arrester bonded.'
        ],
        subparts: [
          { id: 'dt-tank-fins', name: 'Munsell Green Tamper-Proof Steel Hood, Sill & Precast Pad', tag: 'CABINET', material: '12-Ga Corrosion-Resistant Steel + Precast Pad', role: 'Forms a dead-front, child-safe weatherproof enclosure flush against subdivision landscaping.', vector: [-0.9, 0.0, 0.0] },
          { id: 'dt-core-coil', name: 'Low-Loss CRGO Core & Interleaved Aluminum/Copper Coils', tag: 'CORE', material: 'CRGO Steel + FR3 Envirotemp Oil', role: 'Quietly steps primary underground loop voltage to 240/120 V residential URD pedestals.', vector: [0.0, 1.2, 0.0] },
          { id: 'dt-hv-bushing', name: '200 A Dead-Front Loadbreak Elbows (H1A / H1B Loop-Feed)', tag: 'ELBOWS', material: 'IEEE 386 EPDM Molded Peroxide-Cured Shielded Elbows', role: 'Permits hot-stick loop sectionalizing so adjacent homes keep power during cable fault repair.', vector: [-0.6, 0.9, 0.85] },
          { id: 'dt-lv-bushings', name: '240/120 V Secondary Spade Bushings & Underground Service Leads', tag: 'X1-X0-X2', material: 'Tin-Plated Cu Spades + 350 kcmil USE-2 Cable', role: 'Exits bottom vault window directly to underground secondary pedestals serving subdivision homes.', vector: [0.95, 0.25, 0.85] },
          { id: 'dt-fuse-cutout', name: 'Drawout Bay-O-Net Expulsion Fuse & Drip Shield', tag: 'BAY-O-NET', material: 'Drawout Cartridge Holder + ELSP Backup', role: 'Provides external overload/fault clearing without opening the main transformer tank cover.', vector: [-0.85, 1.25, -0.45] },
          { id: 'dt-arrester-ground', name: 'Dead-Front Elbow MOV Arrester & Concentric Neutral Ground Bus', tag: 'SA-URD', material: 'EPDM Dead-Front Arrester + Cu Drain Bus', role: 'Protects radial open-point reflections inside the loop and bonds all cable concentric neutrals.', vector: [0.85, 0.85, -0.75] }
        ]
      },

      urd_vista_swgr: {
        id: 'urd_vista_swgr',
        name: 'Pad-Mounted SF6 / Solid-Dielectric Underground Switchgear (Vista / PMH-9)',
        tag: 'URD VISTA SWGR (600A)',
        ansiNumber: 'IEEE C37.74 / PMH-9 Loop Switchgear',
        governingStandard: 'IEEE Std C37.74 / IEEE Std 386',
        overview: 'Low-profile pad-mounted 4-way SF6 / solid-dielectric Vista underground distribution switchgear anchoring the Gated URD Subdivision main loop. Provides two 600 A loadbreak source ways (bolted dead-front T-bodies) and two 200 A vacuum fault-interrupter (VFI) tap ways feeding residential loop branches with micro-processor overcurrent protection and visible open-gap viewing windows.',
        specs: [
          { k: 'Main Loop Bus Rating', v: '15.5 kV / 25 kV · 600 A Continuous Main Bus · 25 kA Symmetrical Fault Duty' },
          { k: 'Ways Configuration', v: '2× 600 A Three-Phase Loadbreak Switches + 2× 200 A Resettable Vacuum Fault Interrupters' },
          { k: 'Dead-Front Interfaces', v: '600 A Bolted T-Body Connectors + Capacitive Voltage Test Points' },
          { k: 'Insulation Medium', v: 'Hermetically Sealed Low-Pressure SF6 Tank (or Solid EPDM Dielectric) w/ Viewing Window' }
        ],
        failureModes: [
          { title: 'Low SF6 Gas / Vacuum Loss', desc: 'Color-coded gas pressure gauge enters red lockout zone; switch cannot safely interrupt load until gas pressure or solid module integrity is restored.' }
        ],
        checklist: [
          'Verify pressure gauge needle in green zone before operating 600 A loadbreak handle.',
          'Visually confirm open blade / visible break position through illuminated polycarbonate viewing window.'
        ],
        subparts: [
          { id: 'vista-enclosure', name: 'Tamper-Resistant Stainless/Green Enclosure & Concrete Vault', tag: 'VAULT', material: 'Stainless 304 / Powder-Coat Steel', role: 'Shields SF6 switchgear module above underground 600 A / 200 A cable pulling pit.', vector: [0.0, 1.3, 0.0] },
          { id: 'vista-sf6-tank', name: 'Sealed SF6 / Solid-Dielectric Tank w/ Visible Viewing Windows', tag: 'SF6-TANK', material: 'Laser-Welded 304L SS + Polycarbonate Windows', role: 'Houses 3-position loadbreak switches (Closed-Open-Ground) and vacuum interrupters.', vector: [-0.8, 0.5, 0.0] },
          { id: 'vista-elbows-bus', name: '600 A T-Body Source Ways & 200 A VFI Underground Loop Taps', tag: 'WAYS 1-4', material: 'IEEE 386 600A T-Bodies + 200A Elbows', role: 'Distributes underground primary power along West and East subdivision URD loop trenches.', vector: [0.8, 0.2, 0.8] }
        ]
      },

      dist_pole_p1: {
        id: 'dist_pole_p1',
        name: 'Distribution Pole #1 — Galvanized Tubular Steel Recloser Structure (79-ACR1)',
        tag: 'POLE P1 (Galv. Tubular Steel)',
        ansiNumber: 'NESC Grade B Tubular Steel Structure',
        governingStandard: 'ASCE 48 / NESC C2 Rules 232 & 250 / RUS Bull. 1724E',
        overview: '40 ft tapered dodecagonal galvanized tubular steel utility pole mounted on a drilled concrete pier with an 8-bolt anchor flange, supporting the 13.8 kV Feeder 01 main trunk and the 79-ACR1 Automatic Circuit Recloser, complete with galvanized steel channel crossarm, polymer pin insulators, secondary spool rack, and copper ground lug.',
        specs: [
          { k: 'Pole Material & Foundation', v: '40 ft Dodecagonal Tapered Galv. Steel (ASTM A572) on Drilled Concrete Pier + 8× Anchor Bolts' },
          { k: 'NESC Vertical Clearance', v: '26.2 ft (8.0 m) Phase Wire Height >= 18.5 ft NESC Road Crossing Min' },
          { k: 'Crossarm & Insulators', v: '8 ft Galvanized Steel Channel Crossarm w/ Bolted Gusset Collar + Polymer Pin Insulators' },
          { k: 'Conductor Span & Sag', v: '60 m Ruling Span (#4/0 ACSR Penguin) -> Sag S = wL²/(8T) = 0.42 m' }
        ],
        failureModes: [
          { title: 'Crossarm Tracking / Pole-Top Fire', desc: 'Caused by contaminated porcelain pin insulators or loose hardware bonding under damp coastal fog.' }
        ],
        checklist: [
          'Confirm 6.0 ft burial depth mark, intact PVC ground wire molding, and V-brace lag bolts.',
          'Verify 13.8 kV vertical ground clearance well above 18.5 ft NESC minimum over service road.'
        ],
        subparts: [
          { id: 'pole-shaft-ground', name: 'Class 2 Treated Pole Shaft, Ground Wire & Butt Rod', tag: 'POLE', material: 'CCA Wood / Pre-Stressed Concrete + 5/8"x8ft Rod', role: 'Transfers wind & conductor weight into soil via 6.0 ft embedment depth and earths hardware.', vector: [0.0, -0.6, 0.0] },
          { id: 'pole-crossarm-brace', name: 'Treated Timber/FRP Crossarm & Galvanized V-Braces', tag: 'X-ARM', material: '8 ft Treated Crossarm + Hot-Dip Galv. Flat Braces', role: 'Maintains horizontal 1.65 m phase-to-phase spacing along Feeder 01 corridor.', vector: [0.0, 1.2, -0.9] },
          { id: 'pole-insulators', name: 'ANSI 55-5 Porcelain Pin & Post Line Insulators', tag: 'INSUL', material: 'Glazed Brown Porcelain (110 kV BIL Wet/Dry)', role: 'Supports energized 13.8 kV #4/0 ACSR phase conductors atop crossarm pins.', vector: [0.0, 1.95, 0.85] },
          { id: 'pole-guy-anchor', name: 'EHS Down-Guy Strand, Strain Insulator & Anchor Guard', tag: 'GUY', material: '3/8" EHS Galvanized Steel + Yellow HDPE Guard', role: 'Counteracts longitudinal/transverse tension unbalance without bending the pole.', vector: [-1.35, -0.35, 1.1] },
          { id: 'pole-spool-rack', name: '3-Wire Secondary Spool Rack (ANSI 53-2 Spools)', tag: 'RACK', material: 'Galvanized Rack + White Porcelain Spools', role: 'Carries joint-use 240/120 V secondary/streetlighting neutral & service drops.', vector: [1.15, 0.45, -0.8] }
        ]
      },

      dist_pole_p2: {
        id: 'dist_pole_p2',
        name: 'Distribution Pole #2 — Tubular Steel Sectionalizer Structure (34-SECT)',
        tag: 'POLE P2 (Galv. Steel Tangent)',
        ansiNumber: 'NESC Line Tangent & Sectionalizer Support',
        governingStandard: 'ASCE 48 / NESC C2 Rule 232',
        overview: 'Intermediate 40 ft tapered galvanized tubular steel pole on a reinforced concrete pier carrying 3-phase 13.8 kV conductors, 34-SECT line sectionalizer steel crossarm assembly, polymer pin insulators, secondary neutral rack, and copper base ground lug.',
        specs: [
          { k: 'Pole Class & Setting', v: '40 ft Class 2 Pole | Setting Depth = 6.0 ft (10% L + 2 ft)' },
          { k: 'Phase Separation', v: '1.65 m Horizontal Phase-to-Phase (Feeder 01 Mainline)' },
          { k: 'Insulator Rating', v: 'ANSI Class 55-5 Brown Porcelain Pin Insulators (57 kV Wet CFO)' },
          { k: 'Parabolic Span Sag', v: 'Span L = 18.0 m (scaled field corridor) | Ground Clearance = 7.4 m' }
        ],
        failureModes: [
          { title: 'Broken Tie-Wire Conductor Release', desc: 'Wind-induced aeolian vibration can fatigue top-groove aluminum tie wire at pin insulator necks.' }
        ],
        checklist: [
          'Check top-tie preformed armor rods and sectionalizer crossarm thru-bolts.',
          'Confirm intact ground molding down to earth rod.'
        ],
        subparts: [
          { id: 'pole-shaft-ground', name: 'Class 2 Treated Pole Shaft, Ground Wire & Butt Rod', tag: 'POLE', material: 'Treated Timber + #4 Copper Ground Lead', role: 'Supports mainline 34-SECT sectionalizer frame and grounds metal braces.', vector: [0.0, -0.6, 0.0] },
          { id: 'pole-crossarm-brace', name: '8 ft Mainline Crossarm & Steel V-Braces', tag: 'X-ARM', material: 'Wood/FRP Arm + Galvanized Braces', role: 'Holds phases A-B-C at equal elevation ahead of lateral tap.', vector: [0.0, 1.2, -0.9] },
          { id: 'pole-insulators', name: 'ANSI 55-5 Pin Insulators & Polymer Standoffs', tag: 'INSUL', material: 'Wet-Process Glazed Porcelain', role: 'Insulates 13.8 kV mainline wires from grounded crossarm hardware.', vector: [0.0, 1.95, 0.85] },
          { id: 'pole-guy-anchor', name: 'Storm / Lateral Balance Guy & Anchor Assembly', tag: 'GUY', material: 'EHS Steel Guy + Helical Screw Anchor', role: 'Provides storm stability against 150 km/h typhoon wind loading.', vector: [-1.35, -0.35, 1.1] },
          { id: 'pole-spool-rack', name: '3-Wire Secondary Spool Rack & Neutral Clamp', tag: 'RACK', material: 'ANSI 53-2 Porcelain Spools', role: 'Dead-ends common multi-grounded neutral (MGN) continuous through feeder.', vector: [1.15, 0.45, -0.8] }
        ]
      },

      dist_pole_p3: {
        id: 'dist_pole_p3',
        name: 'Distribution Pole #3 — Tubular Steel Double-Arm Lateral & Guy Structure',
        tag: 'POLE P3 (Galv. Steel Double-Arm)',
        ansiNumber: 'NESC Grade B Double-Crossarm Junction',
        governingStandard: 'ASCE 48 / NESC C2 Rules 250–261',
        overview: 'Heavy-duty double-arm galvanized tubular steel junction pole where the North Residential lateral branches off Feeder 01 via the 100K Expulsion Fuse Cutout. Equipped with double steel channel crossarms, polymer suspension dead-end bells, angled down-guy anchor to a galvanized stub pole, and secondary spool rack.',
        specs: [
          { k: 'Pole Class & Structure', v: '45 ft Class 1 Junction Pole | Setting Depth = 6.5 ft (0.10*45+2 ft)' },
          { k: 'Double Crossarm Buck-Arm', v: 'Mainline Double Arm + Perpendicular Lateral Buck-Arm (0.18 m Steel Spacer)' },
          { k: 'Dead-End & Guy Hardware', v: '2-Bell Polymer/Porcelain Dead-End Strings + 3/8" EHS Down-Guy & Anchor' },
          { k: 'Guy Lead-to-Height', v: 'Lead = 4.2 m on Height = 6.9 m (Down-Guy Guard Installed Bottom 2.4 m)' }
        ],
        failureModes: [
          { title: 'Slack Down-Guy Leaning Pole', desc: 'Anchor creep under soaked soil causes pole lean and reduced conductor ground clearance.' }
        ],
        checklist: [
          'Inspect double-arm spacer bolts, dead-end shoes, and yellow pedestrian guy guard visibility.',
          'Verify lateral cutout hot-line clamps and buck-arm minimum vertical separation.'
        ],
        subparts: [
          { id: 'pole-shaft-ground', name: '45 ft Class 1 Heavy Junction Pole & Earth Ground', tag: 'POLE', material: 'Class 1 Pole + Copper Grounding Molding', role: 'Sustains bidirectional longitudinal tension of mainline + north lateral takeoff.', vector: [0.0, -0.6, 0.0] },
          { id: 'pole-crossarm-brace', name: 'Double-Crossarm Assembly & Heavy V-Braces', tag: 'DBL-ARM', material: 'Dual 8 ft Arms + Through-Bolted V-Braces', role: 'Handles dead-end pull of lateral tap conductors without crossarm twist.', vector: [0.0, 1.2, -0.9] },
          { id: 'pole-insulators', name: 'Dead-End Suspension Strain Bells & Pin Insulators', tag: 'BELLS', material: 'ANSI 52-1 Porcelain Strain Discs + Pins', role: 'Terminates full mechanical conductor tension (10 kN/phase) at takeoff.', vector: [0.0, 1.95, 0.85] },
          { id: 'pole-guy-anchor', name: 'Anchored Down-Guy Wire, Johnny-Ball & Yellow Guard', tag: 'GUY-ANCH', material: 'EHS Guy + Guy Strain Insulator + Yellow HDPE Guard', role: 'Transfers unbalanced horizontal lateral pull safely into soil anchor.', vector: [-1.35, -0.35, 1.1] },
          { id: 'pole-spool-rack', name: 'Secondary MGN Neutral Spool Rack', tag: 'RACK', material: '3-Wire Spool Bracket + Split-Bolt Neutral Tap', role: 'Bonds multi-grounded neutral seamlessly across mainline and lateral tap.', vector: [1.15, 0.45, -0.8] }
        ]
      },

      dist_pole_p4: {
        id: 'dist_pole_p4',
        name: 'Distribution Pole #4 — Tubular Steel Double-Arm Dead-End & Tie Boundary',
        tag: 'POLE P4 (Galv. Steel Dead-End)',
        ansiNumber: 'NESC Dead-End + Tie Boundary',
        governingStandard: 'ASCE 48 / NESC C2 / IEEE Std 524',
        overview: 'Heavy-class tapered galvanized tubular steel double-arm dead-end pole anchoring the Feeder 01 trunk ahead of the 79-TIE1 loop recloser switch. Mounted on a drilled concrete caisson pier with bolted anchor plate, polymer suspension dead-end bells, EHS down-guy anchor, and base grounding lug.',
        specs: [
          { k: 'Pole Class & Setting', v: '45 ft Class 1 Dead-End Pole | Setting Depth = 6.5 ft' },
          { k: 'Dead-End Strength', v: 'Double Crossarm + Dual Strain Insulators Rated 15 klbf per Phase' },
          { k: 'Guy & Anchor Spec', v: '3/8" 7-Strand EHS Guy (15,400 lbf UTS) -> Expanding Soil Anchor' },
          { k: 'Clearance Check', v: '7.4 m Mainline Elevation (+1.9 m NESC Margin above Highway Envelope)' }
        ],
        failureModes: [
          { title: 'Dead-End Clamp Corona / Slip', desc: 'Improperly torqued bolted dead-end U-bolts can allow conductor slip and heated splice joints.' }
        ],
        checklist: [
          'Verify infrared thermal parity across bolted dead-end jumpers feeding Commercial & Industrial taps.',
          'Check guy wire tension and yellow guy guard integrity near public corridor.'
        ],
        subparts: [
          { id: 'pole-shaft-ground', name: '45 ft Class 1 Dead-End Pole & Butt Ground Rod', tag: 'POLE', material: 'Heavy-Class Treated Shaft + 5/8"x8ft Cu Rod', role: 'Anchors eastern span termination and bonds dead-end hardware to common earth.', vector: [0.0, -0.6, 0.0] },
          { id: 'pole-crossarm-brace', name: 'Double-Crossarm Dead-End & Heavy Steel V-Braces', tag: 'DBL-ARM', material: 'Double Steel/Timber Crossarms + Spacers', role: 'Transfers equal tension across outer/inner phase dead-end shackles.', vector: [0.0, 1.2, -0.9] },
          { id: 'pole-insulators', name: 'Dead-End Strain Bells & Overhead Jumper Posts', tag: 'STRAIN', material: 'Glazed Porcelain/Silicone Suspension Bells', role: 'Provides full mechanical dead-ending plus slack loop jumper clearance.', vector: [0.0, 1.95, 0.85] },
          { id: 'pole-guy-anchor', name: 'Down-Guy Strand, Strain Insulator & Anchor Guard', tag: 'GUY-ANCH', material: 'EHS Steel + Helical Anchor + Yellow Guard', role: 'Opposes dead-end span tension during open-tie conditions.', vector: [-1.35, -0.35, 1.1] },
          { id: 'pole-spool-rack', name: '3-Wire Secondary Spool Rack & Neutral Clamp', tag: 'RACK', material: 'Porcelain Spools + Parallel Groove Clamp', role: 'Links feeder neutral to Commercial & Industrial substation ground electrodes.', vector: [1.15, 0.45, -0.8] }
        ]
      },

      ind_hv_bay: {
        id: 'ind_hv_bay',
        name: 'Dedicated HV Industrial Sub-Transmission Feeder Bay (52-IND)',
        tag: '52-IND BAY (69 / 138 kV)',
        ansiNumber: 'ANSI 52-IND / 89-INDA / 89-INDB / 21-IND',
        governingStandard: 'IEEE Std C37.04 / IEEE Std 1427 / IEEE C37.113',
        overview: 'Dedicated sub-transmission outgoing bay located at the North-East quadrant of Substation A. Taps directly from the 69 kV (Tiers 1–2) or 138 kV (Tiers 3–4) busbar—bypassing the 13.8 kV city distribution buses completely—to supply the Customer-Owned 25 MVA Heavy Industrial Steel Mill Substation via a private 3-phase steel lattice/monopole line.',
        specs: [
          { k: 'Tap Bus Voltage', v: '69 kV (Tiers 1–2) or 138 kV (Tiers 3–4) Dedicated Sub-Transmission' },
          { k: 'Switching Lineup', v: '89-INDA Line Isolator -> 52-IND Live-Tank SF6 Breaker -> 89-INDB Line Disconnect' },
          { k: 'Metering & Protection', v: '600/5 A C800 Bushing/Free-Standing CTs + ANSI 21-IND / 50/51-IND / 67N Relay' },
          { k: 'Surge & Takeoff', v: 'Station-Class MOV Arresters + North-East Lattice Takeoff Gantry (No City Overlap)' }
        ],
        failureModes: [
          { title: 'Sub-Transmission Arc-Furnace Flicker', desc: 'Isolating industrial steel mill arc furnaces onto 52-IND at 69/138 kV prevents ΔV > 1% light flicker on residential 13.8 kV Feeders F1–F4.' },
          { title: 'Selective Coordination Loss with 52-CUST', desc: 'If 52-IND 51-IND pickup drops below 1.25× 52-CUST curve, plant-side motor faults nuisance-trip the utility bay.' }
        ],
        checklist: [
          'Verify interlocking between 89-INDA, 52-IND, and 89-INDB before operating North ROW line disconnects.',
          'Confirm North ROW steel tower overhead conductors clear Substation A precast perimeter security wall cleanly.'
        ],
        subparts: [
          { id: 'ind-hv-cb', name: '52-IND Live-Tank SF6 Industrial Feeder Breaker', tag: '52-IND', material: '72.5 / 145 kV SF6 Puffer Interrupter', role: 'Interrupts dedicated HV industrial sub-transmission fault currents up to 40 kA.', vector: [0.0, 1.3, 0.0] },
          { id: 'ind-hv-ds', name: '89-INDA & 89-INDB Motor-Operated Flanking Disconnects', tag: '89-IND', material: 'Center-Break Copper Blades + Polymer Posts', role: 'Provides visible air-gap LOTO isolation on both sides of 52-IND.', vector: [-1.1, 0.8, 0.5] },
          { id: 'ind-hv-gantry', name: 'North-East HV Industrial Takeoff Gantry & Arresters', tag: 'GANTRY', material: 'Galvanized Lattice Portal + Station MOV Stacks', role: 'Anchors tensioned ACSR conductors spanning North ROW toward 52-CUST.', vector: [1.1, 1.8, -0.5] }
        ]
      },

      dt_uni_500: {
        id: 'dt_uni_500',
        name: 'East University Campus & Residential Pad-Mounted Substation (500 kVA)',
        tag: 'DT-UNI-500 (SUB B · 52-F3)',
        ansiNumber: 'IEEE C57.12.34 Dead-Front Loop-Feed Pad-Mount',
        governingStandard: 'IEEE Std C57.12.34 / NEC Art. 450 / IEEE 1547 Solar Readiness',
        overview: '500 kVA ONAN three-phase pad-mounted distribution transformer energized by Substation B Feeder 03 (52-F3) along the 13.8 kV East Residential & University Campus corridor. Supplies Engineering Hall (with rooftop solar PV micro-generation), Science Library, and East Apartment blocks, while backstopping Loop 1 through normally-open tie 79-TIE1.',
        specs: [
          { k: 'Rating & Voltage', v: '500 kVA ONAN 65°C Rise | 13.8 kV (Dyn11) -> 208Y/120 V Campus Distribution' },
          { k: 'Feeder Source', v: 'Substation B 52-F3 (13.8 kV) via 140 m East ROW Overhead + Campus Dip Riser' },
          { k: 'Primary / Secondary FLA', v: 'I1 = 20.9 A @ 13.8 kV | I2 = 1,388 A @ 208Y/120 V (Z = 4.9%)' },
          { k: 'FLISR Tie Role', v: 'Coordinates with 79-TIE1 (Normally Open) for bidirectional Loop 1 restoration' }
        ],
        failureModes: [
          { title: 'PV Reverse Power Flow', desc: 'Campus rooftop PV backfeed on 52-F3 can raise local feeder voltage by +1.5% under light summer load.' }
        ],
        checklist: [
          'Check Bay-O-Net primary fuses and secondary 1,600 A campus main molded-case breaker.',
          'Verify IEEE 1547 anti-islanding sync ahead of closing 79-TIE1.'
        ],
        subparts: [
          { id: 'dt-tank-fins', name: 'Munsell Green Corrugated Steel Tank & Cooling Fins', tag: 'TANK', material: 'Tamper-Resistant Steel Cabinet + Radiator Fins', role: 'Cools continuous academic HVAC and laboratory equipment loads.', vector: [-0.85, 0.0, 0.0] },
          { id: 'dt-core-coil', name: 'Low-Loss Amorphous / CRGO 3-Phase Core & Coil', tag: 'CORE', material: 'CRGO Steel + Vacuum-Impregnated Coils', role: 'Steps 13.8 kV 52-F3 primary down to 208Y/120 V campus utilization.', vector: [0.0, 1.35, 0.0] },
          { id: 'dt-hv-bushing', name: 'IEEE 386 200 A Loadbreak Loop Bushings (H1A/H1B)', tag: 'H1A/B', material: 'Dead-Front Separable EPDM Wells + Elbows', role: 'Connects enclosed 15 kV campus XLPE loop cables with zero exposed live metal.', vector: [0.0, 2.0, -0.4] },
          { id: 'dt-lv-bushings', name: '1,388 A Low-Voltage X0-X3 Copper Spades & Bus Duct', tag: 'X0-X3', material: 'Copper Spades + Multi-Conduit Campus Feeders', role: 'Feeds Engineering Hall, Science Library, and East Residential apartments.', vector: [0.9, 0.25, 0.8] },
          { id: 'dt-fuse-cutout', name: 'Bay-O-Net Expulsion & Current-Limiting Fuse Cartridge', tag: 'FUSE', material: 'Externally Draw-Out Dual-Sensing Fuse', role: 'Isolates internal transformer faults cleanly without disturbing 52-F3 trunk.', vector: [-0.8, 1.5, 0.6] },
          { id: 'dt-arrester-ground', name: 'Elbow-Connected MOV Arresters & Campus Ground Rods', tag: 'SA-GND', material: 'Dead-Front Parking Arrester + Cu-Clad Rods', role: 'Clamps switching transients on underground campus loop.', vector: [0.85, 0.9, -0.7] }
        ]
      },

      dt_mun_1000: {
        id: 'dt_mun_1000',
        name: 'Municipal Water Pumping & Logistics Hub Substation (1,000 kVA)',
        tag: 'DT-MUN-1000 (SUB B · 52-F4)',
        ansiNumber: 'IEEE C57.12.34 Primary-Metered Pad-Mount Station',
        governingStandard: 'IEEE Std C57.12.34 / NEC Art. 450 / NFPA 20 Water Supply',
        overview: '1,000 kVA ONAN/ONAF pad-mounted distribution substation supplied by Substation B Feeder 04 (52-F4). Energizes the Municipal Water Pumping Station (dual elevated/ground storage tanks, booster VFD pumps) and East Logistics Hub, anchored to Loop 2 normally-open tie switch 89-TIE2.',
        specs: [
          { k: 'Rating & Voltage', v: '1,000 kVA ONAN | 13.8 kV -> 480Y/277 V Municipal Booster MCC (Z = 5.5%)' },
          { k: 'Feeder Source', v: 'Substation B 52-F4 (13.8 kV) via 140 m East ROW Overhead Pole Line' },
          { k: 'Primary / Secondary FLA', v: 'I1 = 41.8 A @ 13.8 kV | I2 = 1,203 A @ 480 V (Isc = 21.9 kA sym)' },
          { k: 'Loop Restoration', v: 'Transferable onto Sub A 52-F2 via normally-open motorized tie switch 89-TIE2' }
        ],
        failureModes: [
          { title: 'Booster Pump VFD Inrush & Tank Overflow Risk', desc: 'Loss of 52-F4 stops potable water pressure; rapid FLISR transfer via 89-TIE2 restores municipal pumping within <5 s.' }
        ],
        checklist: [
          'Verify VFD active harmonic filter and 480 V main 1,600 A MCC breaker readiness.',
          'Confirm 89-TIE2 SCADA synchrocheck permissives between 52-F2 (CBD) and 52-F4 (Water Plant).'
        ],
        subparts: [
          { id: 'dt-tank-fins', name: '1,000 kVA Welded ANSI 70 / Pad Tank & Radiators', tag: 'TANK', material: 'Heavy Gauge Steel + Panel Radiators', role: 'Sustains continuous 24/7 municipal water booster pumping heat load.', vector: [-0.9, 0.0, 0.0] },
          { id: 'dt-core-coil', name: 'K-Rated VFD-Duty CRGO Core & Winding Assembly', tag: 'CORE', material: 'K-13 Harmonic-Rated Copper Windings', role: 'Handles non-linear booster VFD currents while maintaining 480Y/277 V regulation.', vector: [0.0, 1.35, 0.0] },
          { id: 'dt-hv-bushing', name: '15 kV High-Creepage Bushings & Riser Pothead Leads', tag: 'H1-H3', material: 'Porcelain/EPDM Dead-Front Loop Bushings', role: 'Terminates 13.8 kV 52-F4 feed inside locked HV compartment.', vector: [0.0, 2.05, -0.45] },
          { id: 'dt-lv-bushings', name: '1,203 A Secondary X0-X3 Spades into Pump MCC', tag: 'X0-X3', material: 'Tin-Plated Cu Bus Bars', role: 'Connects 480 V pump motor control center and logistics bay distribution.', vector: [0.95, 0.25, 0.85] },
          { id: 'dt-fuse-cutout', name: 'Primary 15 kV Current-Limiting Fuse & Loadbreak Switch', tag: 'FUSE', material: '65E Partial-Range CL Fuse + LB Switch', role: 'Clears municipal station internal faults without tripping 52-F4.', vector: [-0.85, 1.55, 0.65] },
          { id: 'dt-arrester-ground', name: 'Heavy MOV Arresters & Water-Pipe Equipotential Grid', tag: 'SA-GND', material: '10 kV Station-Grade Elbow Arresters + Cu Grid', role: 'Equalizes ground potential across metallic water mains and pump frames.', vector: [0.85, 0.95, -0.75] }
        ]
      },

      city_gate: {
        id: 'city_gate',
        name: 'Urban Utility District & URD Subdivision Entrance Gatehouse Archway',
        tag: 'CITY ENTRANCE GATE',
        ansiNumber: 'NESC Rule 232 Highway Clearance / Community Security Gate',
        governingStandard: 'NESC C2 Bridge & Overpass Clearances / Municipal Access Code',
        overview: 'Illuminated municipal boulevard entrance archway and motorized sliding barrier gate spanning the public highway right at the 140 m buffer boundary entering the 4-District City & URD Subdivision. Guarantees full 140 m high-voltage buffer setback from both Substation A and Substation B precast security walls.',
        specs: [
          { k: 'Setback Location', v: 'At City Entrance (140.0 m East of Substation A Security Wall)' },
          { k: 'Portal Overhead Clearance', v: '6.8 m Clear Steel Archway Height (Exceeds NESC/DOT Freight Truck Limit)' },
          { k: 'Gate Mechanism', v: 'Dual Motorized Sliding Barrier Arms + RF Guardhouse Security Kiosk' },
          { k: 'Walk Mode Operation', v: 'Click 3D Gate or Press [E] Near Guardhouse to Toggle Open / Closed' }
        ],
        failureModes: [
          { title: 'Closed Gate Vehicle / Crew Collision', desc: 'Reflective yellow/amber beacon and solid collision boundaries protect incoming maintenance boom trucks when secured.' }
        ],
        checklist: [
          'Verify overhead portal sign illumination and clear width for line bucket trucks.',
          'Confirm unobstructed emergency fire & ambulance lane bypass.'
        ],
        subparts: [
          { id: 'city-gate-arch', name: 'Steel Boulevard Archway Portal & Illuminated District Sign', tag: 'ARCHWAY', material: 'Structural HSS Steel Frame + LED Marquee', role: 'Demarcates the 140 m utility safety buffer boundary entering the city corridor.', vector: [0.0, 1.6, 0.0] },
          { id: 'city-gate-boom', name: 'Motorized Barrier Arms, Security Booth & Stop Bollards', tag: 'BARRIER', material: 'Reflective Aluminum Arms + Concrete Kiosk', role: 'Controls vehicular entry while clearing field crew walk-through when opened.', vector: [-1.1, 0.4, 0.7] }
        ]
      },

      substation_gate: {
        id: 'substation_gate',
        name: 'Substation 3.0 m Precast Concrete Security Wall & Motorized Gate',
        tag: 'CONCRETE WALL / GATE',
        ansiNumber: 'NESC Section 110 / IEEE Std 80 / NERC CIP-014 Physical Security',
        governingStandard: 'NESC C2 Rule 110.A1 / IEEE Std 80 / NERC CIP-014',
        overview: 'Solid 3.0 m reinforced precast concrete panel and pilaster ballistic/anti-climb perimeter security wall topped with 45° angled 3-strand barbed wire & razor coil (3.55 m total height), complete with motorized 6.4 m double-leaf steel vehicle gate, pedestrian man-gate, security guardhouse, RFID keycard bollard, and IEEE 80 flexible copper gate ground braids.',
        specs: [
          { k: 'Wall Height & Construction', v: '3.0 m Precast Concrete Panels & Pilasters + 0.55 m Barbed/Razor Topping' },
          { k: 'Vehicular Clear Width', v: '6.4 m Double-Leaf Heavy-Haul Gate + 1.4 m Pedestrian Man-Gate' },
          { k: 'IEEE 80 Touch Voltage', v: 'Flexible 4/0 Copper Hinge Braid + Perimeter Ground Loop (<50 V Touch)' },
          { k: 'Field Walk & Cutaway', v: 'Press [E] or Click Gate to Open | Use Wall Cutaway Toggle for Low Sightlines' }
        ],
        failureModes: [
          { title: 'Broken Gate Hinge Ground Braid', desc: 'Loss of flexible copper jumper turns the steel gate frame into an ungrounded touch-potential hazard during SLG faults.' }
        ],
        checklist: [
          'Inspect flexible braided copper strap jumping across both gate hinges to grounded wall steel embed.',
          'Confirm HV Danger signage readable at 15 m approach along entrance driveway apron.'
        ],
        subparts: [
          { id: 'gate-leaves', name: 'Heavy Steel Vehicular Swing Gate & Man-Gate', tag: 'LEAVES', material: 'Tubular Steel Crash Gate + Panic Man-Gate', role: 'Pivots open 90 degrees for transformer rigging access and personnel egress.', vector: [-1.4, 0.5, 0.6] },
          { id: 'gate-posts-barbed', name: '3.0 m Concrete Wall Pilasters & Barbed/Razor Outriggers', tag: 'WALL/BARB', material: 'Precast Concrete + 45° Galvanized Razor-Coil Arms', role: 'Meets NERC CIP & NESC Rule 110 anti-intrusion and ballistic arc shielding.', vector: [0.0, 1.5, 0.0] },
          { id: 'gate-guardhouse', name: 'Security Guardhouse Booth & RFID Access Bollard', tag: 'GUARD', material: 'Insulated Security Kiosk + Safety Amber Beacon', role: 'Enforces LOTO & PPE sign-in before unauthorized entry into live HV switchyard.', vector: [1.6, 0.4, 0.9] },
          { id: 'gate-apron-ground', name: 'Asphalt Highway Driveway Apron & 4/0 Cu Hinge Braids', tag: 'APRON', material: 'Paved Asphalt Transition + Flexible Cu Straps', role: 'Connects internal substation road seamlessly to highway while bonding gate to earth grid.', vector: [0.0, -0.45, 1.4] }
        ]
      }
    };

    // Deep Engineering Sub-Part Inspector Profiles (Keyed by 3D subpartId)
    const SUBPART_DEEP_DIVE = {
      // --- MAIN POWER TRANSFORMER (TR-01) ---
      'tx-tank': {
        ansiCode: 'IEEE C57.12.00 / Type ONAN-ONAF Steel Vessel',
        fieldSpot: 'Corrugated olive-grey welded carbon steel tank with vertical stiffening ribs, jacking pads at corners, drain valve, and red-capped gooseneck Pressure Relief Device (PRD) on top deck.',
        workingPrinciple: 'Sealed under full head of naphthenic mineral oil from the elevated conservator. Withstands full vacuum dehydration (-100 kPa) and rapid internal arc overpressure. During severe internal fault (>55 kPa), the spring-loaded PRD diaphragm lifts in milliseconds to prevent tank rupture.',
        maintenance: 'Ratings: 10 mm A36 steel plate, full vacuum rated. Failure Modes: Gasket weeping at manhole covers, micro-cracks at radiator flange welds, corrosion at base skirt. Checks: DGA oil sampling from bottom drain valve, paint film thickness, PRD microswitch alarm continuity test.'
      },
      'tx-hv-bushings': {
        ansiCode: 'ANSI/IEEE C57.19.01 — 69 kV OIP Condenser Bushings (H1–H3)',
        fieldSpot: 'Three tall angled wet-process brown porcelain columns with alternating large/small weather sheds, raised steel mounting turrets, top aluminum oil expansion sight dome, and twin crescent arcing horns.',
        workingPrinciple: 'Uses Oil-Impregnated Paper (OIP) wound with coaxial aluminum foil grading layers inside to equalize radial and axial electric field stress—preventing partial discharge along the grounded mounting flange. Capacitance C1 tap at base flange supports power-factor monitoring.',
        maintenance: 'Ratings: 69 kV nominal, 350 kV BIL, 1200 A copper center draw-lead. Failure Modes: Moisture ingress via top cap gasket raising dissipation factor (tan δ > 0.5%). Checks: Doble C1/C2 Power Factor & Capacitance test, IR thermography on top stud clamp.'
      },
      'tx-lv-bushings': {
        ansiCode: 'IEEE C57.19.00 — 13.8 kV Secondary & Neutral Bushings (X1–X3, X0)',
        fieldSpot: 'Four shorter brown porcelain insulators with alternating sheds on the secondary deck: three phase bushings (X1, X2, X3) and one Solidly-Grounded Neutral bushing (X0) bonded to station earth.',
        workingPrinciple: 'Delivers stepped-down 13.8 kV (1,745 A at 41.7 MVA ONAF) from the grounded-Wye secondary winding. X0 carries zero-sequence ground-fault return current and serves as CT neutral ground-fault sensing point (ANSI 51N).',
        maintenance: 'Ratings: 15 kV class, 110 kV BIL, 2000 A NEMA 4-hole bronze flag terminals. Failure Modes: Loose bolted palm overheating under high LV current. Checks: Torque check, IR camera hotspot scan, neutral ground CT polarity check.'
      },
      'tx-conservator': {
        ansiCode: 'IEEE C57.12 — Expansion Tank, MOG Dial & Silica Gel Breather',
        fieldSpot: 'Elevated horizontal cylinder on A-frame steel brackets above top cover, fitted with round Magnetic Oil-Level Gauge (MOG) on front end cap and translucent cylinder below filled with cobalt-blue crystals.',
        workingPrinciple: 'Maintains positive static head of oil above the main tank while absorbing ~8% thermal volume expansion between -5°C and +105°C. As oil cools and contracts, air inhaled from atmosphere passes up through the oil seal cup and hygroscopic silica gel crystals to strip 99% of moisture.',
        maintenance: 'Ratings: ~10% of main tank oil volume. Failure Modes: Saturated silica gel turning pale pink (allowing humidity into oil, cutting dielectric breakdown below 30 kV) or jammed MOG float. Checks: Replace silica when >50% pink, top up breather oil seal cup.'
      },
      'tx-buchholz': {
        ansiCode: 'ANSI 63 / IEC 60076-22 — Gas & Oil-Surge Relay',
        fieldSpot: 'Brass/cast-bronze flanged chamber spliced inline along the 5-degree inclined pipe between main tank cover and conservator, with transparent inspection sight glass revealing top/bottom floats and top gas test petcock.',
        workingPrinciple: 'Dual-stage internal fault detector. Stage 1 (Slow Incipient Fault): Partial discharges or core hot spots crack mineral oil into H2, CH4, C2H2 gas bubbles; gas rises along the inclined pipe and collects inside top chamber, dropping the upper float to sound a SCADA Alarm. Stage 2 (Violent Arc Fault): Rapid gas pressure blast drives an oil surge wave (>1.0 m/s) that deflects the lower hinged baffle plate, energizing the 86T Lockout Trip coil instantaneously.',
        maintenance: 'Operating Pipe Slope: 3°–7° upward toward conservator. Failure Modes: False surge trip during earthquakes or oil pump startup if vane damper is worn. Checks: Test both Alarm & Trip mercury/magnetic reed switches via hand air-pump; draw collected gas with syringe for field acetylene odor/flammability screening.'
      },
      'tx-core': {
        ansiCode: 'M4 Grain-Oriented Electrical Steel (CRGO) 3-Limb Core',
        fieldSpot: 'Internal assembly visible in Exploded Mode: three circular stepped vertical magnetic limbs clamped by heavy top/bottom horizontal steel yokes and tie-bolt channels.',
        workingPrinciple: 'Built from 0.27 mm laser-scribed CRGO silicon steel laminations coated with Carlite insulation to slash hysteresis and eddy-current no-load losses. Stepped circular cross-section maximizes copper window fill factor and conducts 60 Hz mutual flux (Φ ≈ 1.65 T peak) from HV to LV coils.',
        maintenance: 'Design Flux: 1.65 T (saturation knee at 1.9 T). Single-Point Core Ground: Core frame is grounded at ONE point via removable external bushing; an inadvertent second ground creates a shorted circulating turn (hot spot + ethanes/methane in DGA). Checks: Megger core-to-tank insulation (>1000 MΩ at 2.5 kV DC).'
      },
      'tx-windings': {
        ansiCode: 'IEC Vector Group Dyn11 — Concentric Copper Coils',
        fieldSpot: 'Bright electrolytic copper concentric cylinders around each core limb—inner helical LV coil (13.8 kV) and outer continuous-disc HV coil (69 kV) braced by pressboard spacer blocks.',
        workingPrinciple: 'Delta-connected 69 kV primary traps triplen (3rd, 9th) magnetizing harmonics inside the closed delta loop, while Grounded-Wye 13.8 kV secondary provides stable neutral reference and 30° (-11 o’clock) phase shift. Oil circulation ducts between discs extract I²R + stray eddy heat.',
        maintenance: 'Impedance Z ≈ 8.5% on 25 MVA base; Class A thermally-upgraded Kraft paper insulation (65°C rise). Failure Modes: Radial buckling of inner LV coil under unbraced external bolted 3-phase fault. Checks: Sweep Frequency Response Analysis (SFRA), Turns Ratio (TTR ±0.5%), Winding Resistance.'
      },
      'tx-oltc': {
        ansiCode: 'ANSI 90 / IEEE C57.131 — On-Load Tap Changer (±10%, 33 Steps)',
        fieldSpot: 'Separate side oil compartment welded onto the +X tank wall with vertical bevel drive shaft descending into a galvanized motor cabinet bearing a numbered Circular Tap Position Dial.',
        workingPrinciple: 'Regulates secondary 13.8 kV bus voltage within ±1% during live load swings without interrupting current. Uses a two-stage sequence: a no-load Selector Switch pre-positions the next tap on the HV neutral/delta winding, then a rapid spring-driven Vacuum/Oil Diverter Switch transfers load across transition resistors in <45 ms.',
        maintenance: 'Range: +10% to -10% in thirty-two 0.625% steps. CRITICAL SAFETY: OLTC oil is carbonized by diverter arcing and is kept strictly segregated from main tank oil! Checks: Separate DGA & dielectric oil test (<30 kV swap oil), contact wear counter check, AVR 90 voltage bandwidth calibration.'
      },
      'tx-radiators': {
        ansiCode: 'ONAN / ONAF Forced-Air Radiator Cooling System (ANSI 26/49)',
        fieldSpot: 'Two multi-fin pressed-steel vertical cooling banks hung off the -X tank wall via top/bottom manifold headers and shutoff valves, carrying circular ONAF cooling fan shrouds with multi-blade impellers.',
        workingPrinciple: 'Natural thermosiphon effect (ONAN, 25 MVA): Hot low-density oil at top of windings flows out the upper manifold, sheds heat down narrow pressed-steel fins, and returns cool to bottom of tank. Above 60% load or 65°C top-oil, Winding Temperature Indicator (49W) starts Stage 1 & 2 fans (ONAF, 33.3/41.7 MVA).',
        maintenance: 'Ratings: Stage 1 ONAF = 33.3 MVA; Stage 2 ONAF = 41.7 MVA. Failure Modes: Closed butterfly radiator valves after maintenance causing severe thermal trip, seized fan bearings. Checks: Verify butterfly valve handles OPEN & locked, check fan rotation direction & thermal switch setpoints (Fan1=65°C, Alarm=95°C, Trip=105°C).'
      },

      // --- 69 kV SF6 CIRCUIT BREAKER (CB-69-1) ---
      'cb-tank': {
        ansiCode: 'IEEE C37.06 — Grounded Dead-Tank Pressure Vessel (0.60 MPa SF6)',
        fieldSpot: 'Three horizontal olive-grey cast-aluminum pressure cylinders mounted at waist height on a hot-dip galvanized frame, with bolted end domes and copper SF6 fill manifold beneath.',
        workingPrinciple: 'Unlike live-tank breakers where interrupters sit at line potential, the dead-tank enclosure is solidly bolted to substation ground. This safely lowers center of gravity (superior seismic rating) and places internal Bushing Current Transformers (BCTs) at ground potential around every phase.',
        maintenance: 'Normal SF6 Pressure: 0.60 MPa @ 20°C; Lockout: 0.48 MPa. Failure Modes: O-ring flange gasket fatigue releasing SF6 (potent greenhouse gas, GWP = 23,500). Checks: Handheld SF6 sniffer leak test around flanges, verify tank ground strap continuity (<0.1 Ω).'
      },
      'cb-bushings': {
        ansiCode: 'IEEE C37.04 — Alternating-Shed Porcelain Bushings & Internal BCTs',
        fieldSpot: 'Six V-angled wet-process porcelain columns with alternating large/small sheds protruding from top of dead-tanks, surrounded by dark steel BCT collars at their bases and topped by arcing horns.',
        workingPrinciple: 'Each condenser bushing feeds 69 kV phase current down into the pressurized tank while toroidal BCTs wrapped around the grounded base turret simultaneously step current down (600:5 A C800) for overlapping Bus (87B) and Transformer (87T) differential protection zones.',
        maintenance: 'BIL: 350 kV crest; Creepage: 31 mm/kV. Checks: Verify all unused BCT taps are shorted (NEVER open-circuit a CT!), inspect porcelain sheds for hairline cracks or bird/salt contamination.'
      },
      'cb-terminal-pads': {
        ansiCode: 'NEMA CC1 — Silver-Plated 4-Hole Terminal Pads & Braided Shunts',
        fieldSpot: 'Bright silver-plated flat copper blocks atop each bushing head connected to flexible woven copper laminate expansion shunts.',
        workingPrinciple: 'Provides low-resistance bolted electrical connection (<10 µΩ contact drop) to rigid/stranded bus drops. Braided copper shunts decouple thermal expansion and breaker mechanical trip recoil from porcelain stems so switching shocks cannot snap brittle porcelain.',
        maintenance: 'Rating: 2,000 A continuous, 40 kA momentary. Checks: Apply oxidation inhibitor on aluminum-to-copper bimetallic transitions; torque 1/2" stainless hardware to 55 N·m; IR thermography under peak load.'
      },
      'cb-interrupter': {
        ansiCode: 'ANSI 52 — SF6 Single-Pressure Puffer Interrupter Chamber',
        fieldSpot: 'Cutaway translucent cyan cylinder inside each dead-tank showing concentric aluminum dielectric field shields around the central axis.',
        workingPrinciple: 'Contains electronegative Sulfur Hexafluoride (SF6) gas with ~2.5× dielectric strength of air. When arcing occurs during opening, SF6 captures free electrons to form heavy slow negative ions (SF6⁻) and thermally quenches plasma arcs at the very next 60 Hz current zero within 2 cycles (33 ms).',
        maintenance: 'Interrupting Rating: 40 kA RMS symmetrical. Failure Modes: Decomposition byproducts (SF4, SOF2, HF acid) forming toxic white powder when moisture enters. Checks: Dew-point hygrometer (< -35°C), SF6 purity (>97% volume).'
      },
      'cb-contacts': {
        ansiCode: 'Silver-Tungsten Arcing Contacts & PTFE Ablation Nozzle',
        fieldSpot: 'Internal concentric rod-and-tulip copper/silver contacts shrouded by a white tapered Teflon (PTFE) Venturi puffer nozzle.',
        workingPrinciple: 'Two-stage separation: Main silver-plated copper fingers separate first without arcing, diverting all 40 kA fault current onto refractory Cu-W (Copper-Tungsten) arcing tips inside the PTFE throat. As moving cylinder compresses SF6, supersonic pressurized gas blasts axially through the nozzle to cool and stretch the arc out at current zero.',
        maintenance: 'Mechanical Endurance: 10,000 CO ops; Electrical: 20 full 40 kA interruptions. Checks: Dynamic Contact Resistance Measurement (DCRM < 45 µΩ) & contact travel-time analyzer (trip coil energized to main contact part < 18 ms).'
      },
      'cb-operating-mech': {
        ansiCode: 'Spring-Charged Motor Operator w/ Dual 125 VDC Trip Coils',
        fieldSpot: 'Galvanized steel side cabinet featuring a transparent inspection window showing a heavy yellow vertical helical closing spring, charging motor, and dual red (Trip) & green (Close) DC solenoids.',
        workingPrinciple: 'Opening springs are compressed automatically whenever the breaker closes—ensuring "Trip-Free" stored energy to clear faults instantly even during station blackout. Two independent 125V DC trip coils (TC1 & TC2) eliminate single-point tripping failure. Re-charging motor winds closing spring back in ~8 seconds.',
        maintenance: 'Duty Cycle: O-0.3s-CO-3min-CO. Failure Modes: Sticky trip latch grease ("dried-out mechanism") delaying first-trip time. Checks: First-trip coil current waveform profiling, anti-condensation heater check, 52a/52b auxiliary switch check.'
      },
      'cb-gauge': {
        ansiCode: 'Temperature-Compensated SF6 Gas Density Monitor (ANSI 63G)',
        fieldSpot: 'Round dial bezel mounted on upper cabinet face with copper capillary tube and unmistakable Green (0.60 MPa) / Yellow (Alarm) / Red (Lockout) colored pressure arc zones.',
        workingPrinciple: 'Uses an internal bimetallic reference bellows to compensate pressure readings for ambient temperature changes (because SF6 pressure fluctuates with °C even with zero gas leaks). Microswitches inside trip a Stage 1 SCADA Alarm at 0.52 MPa and hardwire-block BOTH Trip & Close coils at 0.48 MPa to prevent explosive low-gas arc failure.',
        maintenance: 'Setpoints @ 20°C: Nominal = 0.60 MPa, Alarm = 0.52 MPa, Block = 0.48 MPa. Checks: Daily operator log reading; verify Stage 1/Stage 2 alarm/block interlock contacts annually.'
      },

      // --- DISCONNECT SWITCH (DS-69-1) & EARTH BLADE (89E) ---
      'ds-base-frame': {
        ansiCode: 'IEEE C37.30 — Hot-Dip Galvanized C-Channel Steel Frame & Bearings',
        fieldSpot: 'Three elevated structural steel pedestals with diagonal cross-bracing, anchor footplates, and heavy dark-steel cylindrical turntable bearing housings at both outer ends.',
        workingPrinciple: 'Maintains rigid phase-to-phase spacing (3.5 m) and elevates live 69 kV bus height above NESC/PEC pedestrian safety minimum (2.7 m to lowest energized metal, 4.78 m blade height). Tapered roller bearings sealed for life ensure smooth synchronous rotation of outer insulator stacks.',
        maintenance: 'Torque / Deflection rated for 25 mm glaze ice + 140 km/h wind + 100 kA peak short-circuit whip forces. Checks: Foundation anchor nut torque, copper ground grid pigtails, bearing grease seal inspection.'
      },
      'ds-insulators': {
        ansiCode: 'ANSI C29.9 — TR-278 Rotating Porcelain Station Post Insulators',
        fieldSpot: 'Twin vertical columns per phase of dark chocolate-brown glazed porcelain with alternating sheds, mounted on rotary turntables and capped with cast aluminum blade hinges.',
        workingPrinciple: 'Provides full 350 kV BIL phase-to-ground withstand while withstanding both cantilever bending (wind/ice) and torsional twisting torque transmitted up from the vertical interphase pipe linkage to swing blades 90 degrees open.',
        maintenance: 'Cantilever strength: 8.9 kN; BIL: 350 kV. Failure Modes: Cement-grout expansion cracking porcelain flanges or bird streamer bridging. Checks: Ultrasonic crack testing on rotating posts, inspect clean glaze and check vertical plumb alignment.'
      },
      'ds-conducting-blades': {
        ansiCode: 'ANSI 89 — Double Center-Break Copper Tubular Main Blades',
        fieldSpot: 'Pair of cylindrical bright copper tubes per phase hinged at outer insulator heads with silver-plated flat spade tips meeting cleanly in the center.',
        workingPrinciple: 'Carries continuous 1,200 A load current and establishes an unmistakable visible 1.4-meter physical air-break gap when rotated 90° horizontally. ZERO arc-extinguishing chamber exists—electrical interlocks strictly prohibit opening while Breaker 52 is closed!',
        maintenance: 'Ratings: 69 kV, 1200 A, 40 kA momentary withstand (kA²t). Checks: Verify blade-to-jaw wipe alignment when closed, check silver-plated contact tip pitting (file/dress never with sandpaper that removes silver plating—use Scotch-Brite only).'
      },
      'ds-jaw-contacts': {
        ansiCode: 'High-Pressure Silver Jaw Fingers & Corona Grading Rings',
        fieldSpot: 'Twin spring-loaded bright silver jaw plates clasping the central blade tip, encircled by sleek spun-aluminum toroidal corona rings.',
        workingPrinciple: 'Phosphor-bronze backup springs force silver-to-silver point contacts together; during a 40 kA through-fault, electromagnetic reverse-loop pinch forces squeeze the jaws even tighter instead of blowing them open. Aluminum corona rings shield sharp jaw edges to prevent 69 kV ionization hissing/corona.',
        maintenance: 'Contact Resistance: <25 µΩ jaw-to-hinge. Checks: IR thermography scan at peak evening load (ΔT > 15°C requires contact dressing); test jaw clamp pinch tension.'
      },
      'ds-operating-mech': {
        ansiCode: 'Motor Operator Cabinet & Interphase Torsion Pipe Linkage',
        fieldSpot: 'Galvanized steel drive cabinet on Phase C leg with glass inspection window, removable yellow manual crank handle, vertical galvanized steel pipe, and horizontal 8.6-meter phase-ganging torsion bar.',
        workingPrinciple: 'A 125V DC reversible gearmotor drives the vertical operating rod and horizontal gang-torsion pipe so all three phases (A, B, C) rotate simultaneously within ±2°. Contains a mechanical Kirk-Key interlock and Breaker 52b series blocking contact so DS-89 cannot operate under load.',
        maintenance: 'Stroke time: 6–8 seconds motorized. Checks: Verify 52b interlock prevents motor start when CB-52 is closed; confirm auxiliary limit switches (89a/89b) toggle cleanly; lubricate pillow-block joints.'
      },
      'ds-earth-blade': {
        ansiCode: 'ANSI 89E — Mechanically Interlocked Substation Earthing Switch',
        fieldSpot: 'Slender copper rod arms hinged at the left phase base legs with visible braided copper shunts descending straight to the buried copper grounding grid.',
        workingPrinciple: 'Provides positive, solid metallic earthing of the isolated 69 kV bus section before maintenance crews touch conductors. Bleeds off deadly electrostatic coupling from adjacent live 69 kV buses and trapped capacitor charges. Mechanically cam-interlocked so 89E CANNOT close unless main blades 89 are fully OPEN.',
        maintenance: 'Short-circuit fault closing rated up to 40 kA for 1 second. Checks: Verify mechanical interlock blocks 89E movement while main switch is closed; inspect flexible braided copper ground shunt for frayed strands.'
      },

      // --- INSTRUMENT TRANSFORMERS (CT-69 / PT) ---
      'ct-primary-head': {
        ansiCode: 'IEEE C57.13 — Hermetic Oil-Filled Aluminum Primary Dome & P1/P2 Studs',
        fieldSpot: 'Heavy cast-aluminum top tank dome perched atop the tall porcelain column, sporting bolted NEMA H1/H2 primary aluminum pads and external copper nameplate.',
        workingPrinciple: 'Hairpin ("live-tank" U-turn) or bar-type copper primary loop enters P1, passes cleanly through the laminated toroidal cores inside the top head, and exits P2—maximizing short-circuit dynamic withstand while confining high-voltage insulation to a single oil-impregnated porcelain stem.',
        maintenance: 'Primary thermal rating factor RF = 1.5× (up to 1,800 A continuous). Checks: Check oil sight glass level inside top dome, scan P1/P2 palm clamps for thermal imbalance with IR camera.'
      },
      'ct-metering-core': {
        ansiCode: 'Revenue Metering Toroidal Core (IEEE Class 0.15S / 0.3 B-1.8)',
        fieldSpot: 'Translucent internal cutaway inside top head: sleek bright silicon/nickel-steel (Permalloy/Mu-metal) ring wrapped tightly in fine secondary copper wire.',
        workingPrinciple: 'Engineered from high-permeability nickel-iron alloy that reaches saturation EARLY (~1.5–2.0× nominal current). This gives ultra-accurate ±0.15% phase & ratio fidelity for billing meters during normal load while deliberately saturating during 40 kA faults to shield delicate digital energy meters from destructive overcurrent.',
        maintenance: 'Ratio: 600:5 A, Burden B-1.8. Checks: Ratio, polarity ("dot test"), and excitation saturation knee curve (typically <60 V knee).'
      },
      'ct-relaying-core': {
        ansiCode: 'Protective Relaying Core (IEEE Class C800, ALF > 20)',
        fieldSpot: 'Large heavy dark-laminated silicon steel toroidal core wound with robust #12 AWG enameled copper secondary turns.',
        workingPrinciple: 'Built with large cross-sectional iron area (CRGO steel) so it MUST NOT saturate even at 20× fault current (12,000 A primary / 100 A secondary into 8 Ω relay burden = 800 V!). Ensures instantaneous 50/87T/21 numerical relays receive faithful undistorted fault waveforms during the critical first cycle.',
        maintenance: 'Accuracy Class: C800 (capable of sustaining 800 V across 8 Ω burden at 100 A secondary with <10% ratio error). CRITICAL: NEVER open-circuit secondary while energized! Checks: Megger secondary >500 MΩ, confirm single ground at relay panel.'
      },
      'ct-porcelain-body': {
        ansiCode: 'Oil-Paper Capacitive Graded Porcelain Stem (350 kV BIL)',
        fieldSpot: 'Tall hollow brown porcelain insulator column with alternating large/small sheds protecting the internal oil-impregnated paper graded condenser cone.',
        workingPrinciple: 'Separates the live 69 kV top head from grounded steel base while routing insulated secondary twisted leads down inside an oil-filled central tube surrounded by foil grading screens. Eliminates corona and ensures uniform vertical voltage gradient.',
        maintenance: 'Oil dielectric > 35 kV / 2.5 mm. Checks: Inspect sheds for flashover tracking, ultrasonic partial discharge (PD) scan, power factor dissipation test (pf < 0.4%).'
      },
      'ct-bellows': {
        ansiCode: 'Stainless Steel Hermetic Oil Expansion Bellows & Level Window',
        fieldSpot: 'Corrugated metallic dome/cap crowning the top head with a vertical oil-level gauge window showing green/red oil meniscus.',
        workingPrinciple: 'Flexes silently like an accordion to compensate for thermal oil expansion/contraction without ever letting ambient moist air touch the mineral oil. Preserves dry gas-free insulation over a 35-year service life—if ruptured, oil level drops and moisture contaminates the paper cone.',
        maintenance: 'Hermetically sealed nitrogen/vacuum-filled assembly. Checks: Visually verify oil sight window from yard using binoculars every patrol (low level indicates bellows rupture or base leak -> immediate de-energization!).'
      },
      'ct-sec-box': {
        ansiCode: 'NEMA 4X Secondary Marshalling Box w/ Shorting Terminal Blocks',
        fieldSpot: 'Stainless/galvanized IP55 junction cabinet bolted onto the support base at waist height, with rigid steel conduit pipes carrying wires underground toward Control House trenches.',
        workingPrinciple: 'Terminates all CT secondary cores (1S1-1S2 Metering, 2S1-2S2 Relaying) onto heavy-duty make-before-break sliding shorting terminal links. Sliding the shorting bar connects S1 to S2 before lifting relay wires—guaranteeing zero risk of fatal 5,000 V open-circuit CT explosion.',
        maintenance: 'Conductor: 10 AWG stranded shielded cable to control room. Checks: Confirm shorting screws are REMOVED on active protection cores and INSTALLED on spare unused cores; check cabinet anti-condensation heater & seal against insects.'
      },

      // --- SURGE ARRESTER (SA-69) ---
      'la-terminal-stud': {
        ansiCode: 'IEEE C62.11 — Stainless HV Line Terminal Stud & Bronze Clamp',
        fieldSpot: 'Polished stainless steel top threaded cap clamped directly onto the 69 kV overhead drop conductor with minimal lead length.',
        workingPrinciple: 'Every meter of connecting lead adds ~1 µH inductance, creating L·(di/dt) ≈ 1 kV/m during steep 10 kA/µs lightning fronts. Keeping the line lead ultra-short guarantees the arrester clamps overvoltages below the transformer 350 kV BIL threshold.',
        maintenance: 'Torque: 60 N·m. Checks: Verify shortest possible straight-line connection to TR-01 HV bushings; inspect clamp for bi-metallic galvanic pitting.'
      },
      'la-grading-ring': {
        ansiCode: 'Dual Spun-Aluminum Electrostatic Corona & Voltage Grading Rings',
        fieldSpot: 'Sleek tubular double-toroid aluminum halo loops mounted immediately beneath the top line stud.',
        workingPrinciple: 'Because stray capacitance to earth robs voltage along vertical ZnO stacks, the upper 20% of discs naturally endure ~65% of line-to-ground voltage stress without grading rings. The aluminum toroids project capacitive coupling downward to linearize electric field gradient across every MOV block.',
        maintenance: 'Required on all arresters ≥ 69 kV. Checks: Inspect mounting struts for wind-induced loosening or ice tilt; verify clean smooth finish free of deep arc burns.'
      },
      'la-zno-stack': {
        ansiCode: 'Gapless Metal-Oxide Varistor (ZnO) Ceramic Disc Column',
        fieldSpot: 'Cutaway dark charcoal-grey stacked ceramic pucks inside the central axis, spring-loaded to eliminate micro-air gaps.',
        workingPrinciple: 'Each sintered Zinc-Oxide grain behaves like back-to-back Zener micro-diodes (I = k·V^α where exponent α ≈ 30–50!). At normal 39.8 kV L-N operating voltage, current is a negligible <0.5 mA capacitive leak. When lightning pushes voltage past 115 kV, impedance plummets in nanoseconds to shunt 10 kA safely to earth, then instantly reseals against 60 Hz follow current.',
        maintenance: 'MCOV = 54.0 kV, Duty Cycle Ur = 60.0 kV, Residual @ 10 kA = 175 kV. Checks: Track resistive 3rd-harmonic leakage current (normal <100 µA; replace immediately if >500 µA due to aging/thermal runaway!).'
      },
      'la-fiberglass-tube': {
        ansiCode: 'Filament-Wound Epoxy Fiberglass (FRP) Mechanical Core',
        fieldSpot: 'Translucent structural filament tube encircling the internal ZnO disc stack inside the silicone housing.',
        workingPrinciple: 'Withstands high cantilever wind/seismic forces while providing safe "non-shattering" fault behavior: if an arrester suffers catastrophic overload, pressure vents safely through soft polymer tears instead of hurling lethal porcelain shrapnel 50 meters across the switchyard.',
        maintenance: 'Cantilever SSL = 10 kN. Checks: Verify vertical alignment on insulated base pedestals and inspect pedestal ground insulators (<10 kV insulated standoff for surge counter operation).'
      },
      'la-polymer-sheds': {
        ansiCode: 'Wet-Process Brown Glazed Porcelain Alternating Weather Sheds',
        fieldSpot: 'Rich chocolate-brown wet-process glazed porcelain skirt stack joined by bolted metallic intermediate flanges and silver aluminum grading rings.',
        workingPrinciple: 'Dense vitrified porcelain with silica glaze sheds rain cleanly along long alternate under-rib creepage paths (≥2,140 mm), preventing salt-fog leakage flashovers while intermediate steel flanges dissipate internal heat.',
        maintenance: 'Creepage distance ≥ 2,140 mm (31 mm/kV). Checks: Inspect glazed sheds for chips or cracks; verify metallic flange fasteners and insulated base pedestal integrity.'
      },
      'la-surge-counter': {
        ansiCode: 'Ground Discharge Lead, Insulating Base & Surge Event Counter + µA Meter',
        fieldSpot: 'Eye-level grey instrument dial box mounted along the ground lead beneath a porcelain/polymer insulating standoff pedestal, reading digital surge counts and continuous µA leakage.',
        workingPrinciple: 'Because the arrester base is isolated from steel support by insulating standoffs, 100% of surge and leakage currents must pass through the counter box to the earth grid. A internal spark-gap/CT rectifier advances the mechanical/digital counter on each discharge >100 A while a microammeter continuously flags early ZnO thermal degradation.',
        maintenance: 'Normal leakage: <100 µA; Alarm threshold: >500 µA. Checks: Log counter digits after every thunderstorm; inspect ground cable (#2/0 AWG copper) continuity to station ground grid.'
      },

      // --- GANTRY & BUSBAR SYSTEM ---
      'gantry-lattice-tower': {
        ansiCode: 'IEEE Std 605 — Dead-End Galvanized Lattice A-Frame Gantry',
        fieldSpot: 'Twin 16 m tall steel truss columns connected by a heavy 24 m horizontal boxed truss beam framing incoming 69 kV lines and lightning peaks.',
        workingPrinciple: 'Resists unbalanced dead-end line tension (15 kN per phase × 3 + shield wires) plus typhoon wind loads while maintaining elevated air clearances across all switchyard apparatus below. Connected directly at all column feet to the buried IEEE 80 ground grid.',
        maintenance: 'ASTM A36 hot-dip galvanized steel. Checks: Visual bolt tightness check, baseplate grout cracking, dual copper ground bond continuity.'
      },
      'gantry-acsr-conductors': {
        ansiCode: 'Penguin 4/0 AWG ACSR (6 Al / 1 Steel) Incoming 69 kV Phase Leads',
        fieldSpot: 'Three sagging bare metallic cables sweeping down from the gantry dead-end insulators and dropping cleanly to Surge Arresters & CTs.',
        workingPrinciple: 'Combines high-tensile galvanized steel center strand (mechanical pull strength) with six pure EC-grade aluminum outer strands carrying 60 Hz power (Skin effect concentrates AC current in aluminum exterior). Rated 360 A @ 75°C conductor temp.',
        maintenance: 'Sags adjusted per sag-tension chart for max 75°C ambient + load. Checks: Infrared scan compression dead-end sleeves and bolted parallel-groove tee connectors.'
      },
      'gantry-ohgw-shield': {
        ansiCode: 'IEEE Std 998 — Overhead Ground Shield Wires (OHGW) & Peak Finials',
        fieldSpot: 'Slender galvanized steel wires strung between the very highest pinnacle spires (16 m) of the dead-end gantry above all phase wires.',
        workingPrinciple: 'Forms an electrostatic Faraday-like shielding umbrella based on the Rolling Sphere Method (r_s = 10 × I^0.65). Direct 30 kA cloud-to-ground lightning strikes terminate harmlessly on the overhead shield wire instead of hitting energized 69 kV equipment, routing surge current straight down steel legs into earth.',
        maintenance: '7/16" EHS Steel (or OPGW fiber ground wire). Checks: Inspect pinnacle down-leads and ground clamps; verify 45 m rolling sphere coverage across expanded bays.'
      },
      'gantry-insulator-strings': {
        ansiCode: 'ANSI Class 52-3 Dead-End Porcelain Disc Insulator Strings & Horns',
        fieldSpot: 'Chains of six glazed brown bell discs coupled in tension between steel gantry crossarm lugs and ACSR line dead-end clamps, flanked by protective arcing horns.',
        workingPrinciple: 'Each 10-inch ball-and-socket porcelain disc withstands ~70 kV wet power-frequency flashover; stacking 6 discs yields >380 kV BIL impulse withstand. Even if one disc cracks ("punctured cap-and-pin"), remaining 5 still hold line voltage safely until scheduled outage.',
        maintenance: 'Checks: Binocular inspection for chipped porcelain skirts; infrared/live-line buzzer testing to spot "cold" zero-voltage punctured bells.'
      },
      'gantry-dampers': {
        ansiCode: 'Stockbridge Aeolian Vibration Dampers',
        fieldSpot: 'Dumbbell-shaped cast-iron twin weights clamped ~1.2 m in front of each gantry dead-end insulator string.',
        workingPrinciple: 'Steady 5–25 km/h laminar winds shed alternate Kármán vortices behind circular cables, setting up high-frequency resonant singing (10–80 Hz) that breaks aluminum strands right at rigid dead-end clamps. Out-of-phase flexing of the damper’s stranded steel messenger wire turns vibrational kinetic energy into harmless inter-strand friction heat.',
        maintenance: 'Checks: Ensure damper clamp bolts haven’t slipped down-span and weights hang level without striking the conductor.'
      },
      'gantry-tubular-bus': {
        ansiCode: 'Schedule 40 6063-T6 Rigid Tubular Aluminum Busbars (3-inch IPS)',
        fieldSpot: 'Straight thick silver-grey seamless aluminum pipes mounted horizontally on porcelain station post insulators spanning between bays.',
        workingPrinciple: 'Tubular cross-section gives maximum bending section modulus per kg—spanning 8+ meters without sag—while eliminating high-resistance skin-effect wasted core metal. Reconfigured dynamically across Single, Main & Transfer, Ring, or Breaker-and-a-Half schemes.',
        maintenance: 'Ampacity: 1,650 A; Phase-to-Phase: 1,500 mm. Checks: Inspect flexible laminated expansion joints at supports and check internal "vibration-damping bare conductor" inside long spans.'
      },

      // --- WALK-IN CONTROL HOUSE & STATION SERVICE ---
      'aux-tx-tank': {
        ansiCode: '100 kVA Oil-Immersed Station Service Transformer Tank (13.8kV–230/115V)',
        fieldSpot: 'Dedicated fenced concrete pad along the 13.8 kV secondary bay, shielded behind an IEEE Std 979 reinforced concrete fire/blast barrier wall North of the Control House (>10 m clear of the paved entrance walkway).',
        workingPrinciple: 'Supplies vital 230/115 VAC essential auxiliary power for TR-01 cooling fans, OLTC motor, Breaker 52 spring charging motors, HVAC climate control, and dual redundant battery chargers so substation remains self-sustaining without external utility mains.',
        maintenance: 'Ratings: 100 kVA, 3-ph, Impedance 3.5%. Checks: Verify oil level gauge, inspect tank ground strap, confirm secondary main breaker rating, and verify intact perimeter safety enclosure & fire wall.'
      },
      'aux-tx-bushings': {
        ansiCode: '13.8 kV Station Service Primary Bushings & Expulsion Fuse Cutouts',
        fieldSpot: 'Three compact brown alternating-shed bushings atop the 100 kVA tank wired via tilted brown porcelain dropout cutout fuse holders.',
        workingPrinciple: 'Protects the auxiliary transformer and keeps station faults off the 13.8 kV distribution bus: if an internal fault happens inside the 100 kVA tank, the boric-acid/horn-fiber fuse tube melts and drops open visibly under spring tension within 1 cycle.',
        maintenance: 'Fuse link: 6 A K-link expulsion. Checks: Inspect cutout hinge silver contacts via binoculars; check primary lightning arresters adjacent to tank.'
      },
      'aux-relay-racks': {
        ansiCode: 'ANSI 87T / 21 / 50-51 / 79 / 86 — Numerical Protection & 52CB Control Panels',
        fieldSpot: 'Four tall 19-inch steel cubicles inside the North Control Room wall displaying SEL-487E, SEL-421, SEL-751 LED mimic screens, orange 86 Lockout handles, and Panel 4’s clickable Pistol-Grip 52-CS Control Switch.',
        workingPrinciple: 'Panel 1 (SEL-487E) runs 87T harmonic-restrained current differential across TR-01; Panel 2 (SEL-421) protects 69 kV line distance (21) & breaker failure (50BF); Panel 3 (SEL-751) oversees 13.8 kV feeder overcurrent (50/51) & auto-reclosing (79). Any fault latches electromechanical Lockout Relay 86 (forcing manual reset) and energizes both 125V DC Breaker Trip Coils within <15 ms.',
        maintenance: 'Interactive Test: Click the Pistol-Grip 52-CS switch directly on Panel 4 inside Control House to remotely Trip/Close outdoor Breaker CB-69-1! Checks: Relay watchdog healthy green LED, annual secondary-injection Omicron test, confirm 86 lockout flag reset after clearing.'
      },
      'aux-scada-desk': {
        ansiCode: 'DNP3 / IEC 61850 SCADA HMI Workstation, SEL-3555 RTU & Annunciator',
        fieldSpot: 'Operator console desk centered in the Control Room featuring dual live SCADA display monitors, nearby RTU/GPS clock cabinet, and angled overhead 16-window Alarm Annunciator lightbox.',
        workingPrinciple: 'Aggregates real-time telemetry (kV, A, MW, MVAR, SF6 MPa, Oil °C) and Sequence-of-Events (SOE) timestamps synchronized to ±1 microsecond via GPS IRIG-B satellites. Relays encrypted DNP3/IEC 61850 commands from regional Grid Control Center down to protection racks and switches.',
        maintenance: 'Protocol: IEC 61850 MMS + DNP3 over fiber optic ring. Checks: Verify IRIG-B GPS satellite lock LED, test Annunciator Lamp Test push-button, audit SOE event clock sync.'
      },
      'aux-battery-rack': {
        ansiCode: 'IEEE Std 484/485 — 125 VDC Station Battery Bank (60 Translucent Cells)',
        fieldSpot: 'Located inside the partitioned South Battery Room: two-tier seismic-braced steel rack supporting 60 clear battery jars bridged by bare copper inter-cell links.',
        workingPrinciple: 'The true "heartbeat" of substation reliability: wired 60 cells in series (2.25 V float/cell = 135.0 VDC) and operated UNGROUNDED so a single accidental ground fault cannot blow control fuses or blind breaker tripping during a grid short circuit. Supplies 200 Ah autonomy for 8 hours of total AC blackout.',
        maintenance: 'CRITICAL: Without healthy 125V DC, breakers CANNOT trip during faults! Checks: Check pilot cell specific gravity (1.215) & float voltage (135.0V), verify DC ground detector balance (+67.5V/-67.5V to earth), test Battery Room H2 exhaust fan (explosive limit <1%).'
      },
      'aux-battery-chargers': {
        ansiCode: 'Dual Redundant 50 A Solid-State SCR Float / Equalize Chargers',
        fieldSpot: 'Pair of ventilated galvanized cabinets (Charger A & Charger B) inside the Battery Room displaying digital 135.2 V Float status panels.',
        workingPrinciple: 'Converts 240 VAC station service power into ultra-low-ripple regulated 135 VDC via phase-controlled Silicon Controlled Rectifiers (SCRs). Under normal conditions, chargers supply 100% of steady-state relay/LED loads while holding battery cells on gentle float charge; configured in N+1 parallel redundancy with blocking diodes.',
        maintenance: 'Float: 135.0 VDC (2.25 V/cell); Equalize: 141.0 VDC (2.35 V/cell). Checks: Verify AC Fail, Charger Fail, and High/Low DC Voltage alarms report cleanly to SCADA.'
      },
      'aux-acdc-boards': {
        ansiCode: '125 VDC & 480/240 VAC Essential Auxiliary Distribution Panelboards',
        fieldSpot: 'Two side-by-side steel dead-front distribution switchboards flush against the East Control Room wall labeled 125VDC DIST PANEL and 480/240VAC AUX PANEL.',
        workingPrinciple: 'Separates DC and AC power domains strictly into dedicated raceways to avoid catastrophic AC-into-DC relay misoperations. Dual molded-case DC breakers selectively feed Trip Coil 1 (Panel 1) vs Trip Coil 2 (Panel 2) from physically isolated bus legs so no single DC short disables protection.',
        maintenance: 'Checks: Verify breaker trip-curve coordination between Battery Main Fuse and Panelboard Branch Breakers; exercise 480/240V Manual Transfer Switch during preventative outages.'
      },
      'sec-ngr': {
        ansiCode: 'ANSI 51G / IEEE Std 32 — 10 Ω Neutral Grounding Resistor (NGR)',
        fieldSpot: 'Elevated perforated galvanized stainless enclosure directly behind TR-01 X0 bushing housing stacked zig-zag edge-wound resistor grids and a 800/5 A Neutral CT on the insulated down-riser.',
        workingPrinciple: 'Without an NGR, a solidly grounded 13.8 kV wye neutral delivers devastating (>15 kA) SLG fault currents inside MV breakers. Inserting R_NGR = 7967 V / 800 A = 10 Ω cleanly limits steady SLG faults to 797 A while supplying ample zero-sequence current for reliable 51G selective tripping.',
        maintenance: 'Checks: Measure cold resistance (10.0 Ω +-5%), inspect resistor porcelain standoffs for tracking, and test NGR continuity monitor relay.'
      },
      'sec-arresters-ctvt': {
        ansiCode: 'IEEE C62.11 / C57.13 — 13.8 kV MOV Arresters & MV Metering CT/VT',
        fieldSpot: 'Compact trio of light-gray polymer gapless arresters and cast-epoxy CT/VT combination units on a single galvanized portal frame immediately east of TR-01 LV throat.',
        workingPrinciple: 'Clamps fast-front lightning and switching surges entering from the 13.8 kV bus before they reflect against the LV transformer winding capacitance. Epoxy CTs (2000/5 A) drive ANSI 87T low-side differential and revenue kWh meters.',
        maintenance: 'Checks: Verify CT secondary shorting blocks are strictly closed before meter calibration; clean polymer arrester sheds and inspect ground bond straps.'
      },
      'sec-lv-disconnect': {
        ansiCode: 'IEEE C37.30 — 89-LV Secondary Main Isolator (15 kV, 2000 A)',
        fieldSpot: 'Three-pole single-break vertical copper blade disconnect mounted on elevated structural steel ahead of 52-LV with a keyed Kirk-Key interlock box.',
        workingPrinciple: 'Provides an unmistakable visible air-gap downstream of TR-01 so crews working on 52-LV vacuum bottles have verified physical isolation. Strictly interlocked with 52-LV closed contact (52b) so it cannot open under 1,744 A secondary load.',
        maintenance: 'Checks: Torque silver-plated jaw contact fingers, lubricate interphase pushrod bearings, and test mechanical Kirk-Key interlock against 52-LV.'
      },
      'sec-lv-breaker': {
        ansiCode: 'ANSI 52-LV — 15 kV, 2000 A, 31.5 kA Vacuum Circuit Breaker',
        fieldSpot: 'Heavy-duty outdoor porcelain-bushing vacuum breaker on a concrete pad housing three sealed Al2O3 ceramic vacuum interrupter bottles driven by a stored-energy spring mechanism.',
        workingPrinciple: 'Separates copper-chrome butt contacts only ~12 mm inside a <10^-5 Pa high vacuum; metal vapor plasma condenses onto the sputter shield within microseconds at the very first AC current zero, interrupting up to 31.5 kA in <=3 cycles with zero SF6 gas.',
        maintenance: 'Checks: Perform 27 kV AC 1-minute vacuum bottle withstand test, verify 12 mm contact erosion gauge, and exercise trip-coil 1 & 2.'
      },
      'sec-dist-bus': {
        ansiCode: 'IEEE 605 — 13.8 kV Tubular Aluminum Distribution Bus & SST-100 Fuse Tap',
        fieldSpot: 'Overhead 2.5-in rigid tubular aluminum bus supported on gray 15 kV post insulators spanning Feeder 01, Feeder 02, Capacitor Tap, and FU-SS expulsion cutouts feeding SST-100 behind the fire wall.',
        workingPrinciple: 'Collects 2,000 A output from 52-LV and fans it cleanly via welded/bolted aluminum tee connectors to both outgoing radial feeders, the reactive compensation bank, and the essential 100 kVA station service transformer.',
        maintenance: 'Checks: Perform annual IR thermography scan at peak evening load (<65 °C rise), verify bus expansion joints, and check FU-SS 10E fuse links.'
      },
      'sec-cap-bank': {
        ansiCode: 'IEEE 18 / 52-CAP — 3.6 MVAR 13.8 kV Switched Shunt Capacitor Bank',
        fieldSpot: 'Elevated structural rack holding 12 stainless-steel 300 kVAR capacitor cans, individual expulsion fuse links, air-core inrush limiting reactors, and dedicated 600 A 52-CAP vacuum switch.',
        workingPrinciple: 'Injects 3.6 MVAR of leading reactive current (150.6 A/phase) to cancel inductive motor/transformer VAR demand, boosting 13.8 kV bus voltage by ~2.4% and reducing I^2R feeder losses.',
        maintenance: 'Checks: Wait >=5 min after opening 52-CAP and verify <50 V before grounding; measure individual can capacitance (+-5% tolerance) for blown internal elements.'
      },
      'fdr-f1-breaker': {
        ansiCode: 'ANSI 52-F1 / 89-F1A / 89-F1B — Feeder 01 1200 A Isolation Bay',
        fieldSpot: 'Northern 13.8 kV feeder bay holding line/bus disconnect switches flanking a 1200 A Vacuum Breaker controlled by an ANSI 50/51/51N/79 feeder protection relay.',
        workingPrinciple: 'Dedicated isolation & auto-reclose bay serving critical commercial/hospital loads on Feeder 01. Flanking 89-F1A/B disconnects permit complete maintenance removal of 52-F1 without dropping Feeder 02.',
        maintenance: 'Checks: Verify 79 auto-reclose lockout timer, record 52-F1 operation counter, and check contact resistance (<60 uOhm across interrupter).'
      },
      'fdr-f2-breaker': {
        ansiCode: 'ANSI 52-F2 / 89-F2A / 89-F2B — Feeder 02 1200 A Isolation Bay',
        fieldSpot: 'Southern 13.8 kV feeder bay mirroring Feeder 01 with twin vertical-break disconnects flanking 52-F2 Vacuum Circuit Breaker.',
        workingPrinciple: 'Coordinates inverse-time overcurrent (ANSI 51 Very Inverse) curves with industrial substation fuses and reclosers downstream on Feeder 02 so temporary faults clear cleanly.',
        maintenance: 'Checks: Verify mechanical trip-free linkage, test battery trip under 105 VDC minimum voltage, and check heater strip against cabinet condensation.'
      },
      'fdr-ct-arresters': {
        ansiCode: 'ANSI C57.13 / C62.11 — Feeder Exit CTs & Polymer Arresters',
        fieldSpot: 'Mounted directly on the west side of the 13.8 kV outgoing H-frame portal where riser cables or overhead conductors climb to the dead-end insulators.',
        workingPrinciple: 'Provides high-accuracy phase/residual current measurements (1200/5 A) for fault distance impedance calculations while draining incoming overhead line lightning strikes immediately at the substation gate.',
        maintenance: 'Checks: Inspect arrester disconnector ground leads for blown cartridge indication and verify CT conduit weather seals.'
      },
      'fdr-takeoff-gantry': {
        ansiCode: 'NESC / PEC Part 2 — 13.8 kV Dual-Circuit Outgoing Takeoff Gantry',
        fieldSpot: 'Galvanized steel H-frame portal at the eastern fence line carrying six 15 kV dead-end polymer strings and overhead static shield wire.',
        workingPrinciple: 'Transfers full mechanical line tension of two outgoing 477 kcmil ACSR feeders to concrete pier foundations while guaranteeing >=5.5 m ground clearance over service roads.',
        maintenance: 'Checks: Inspect dead-end compression clamps for broken strands, verify vibration dampers, and check portal leg ground connections.'
      },
      'ngr-enclosure': { ansiCode: 'IEEE C57.32 — Louvered Resistor Housing', fieldSpot: 'Slatted galvanized metal housing perched on 15 kV base insulators beside TR-01.', workingPrinciple: 'Protects staff from 700°C steel grids during SLG fault limitation while venting heat cleanly.', maintenance: 'Check louver screens for nests/rust and verify grounding pad integrity.' },
      'ngr-resistor-grid': { ansiCode: 'Stainless Steel Punched Grid Stack (10.0 Ω)', fieldSpot: 'Multi-tier zig-zag stainless resistor plates visible inside cutaway side.', workingPrinciple: 'Limits X0 SLG fault to I_g = 7,967V / 10Ω = 797 A for 10 seconds to save TR-01 core and windings from iron burning.', maintenance: 'Measure cold resistance (10.0 Ω ±5%) annually via DLRO.' },
      'ngr-ct-bushing': { ansiCode: 'X0 Entry Bushing & ANSI 51G Neutral CT (800/5 A)', fieldSpot: 'Porcelain roof insulator topped with X0 copper bus drop and toroidal window CT.', workingPrinciple: 'Samples true zero-sequence 3I0 ground return directly into Control House ANSI 51G relay.', maintenance: 'Confirm CT shorting bar is open in service and check polarity markings.' },
      'ngr-ground-pad': { ansiCode: '4/0 Cu Earth Return Pad & 15 kV Standoffs', fieldSpot: 'Insulated mounting legs separating neutral housing from ground with single copper earth strap.', workingPrinciple: 'Forces 100% of ground return current through the CT and calibrated 10 Ω bank before entering IEEE 80 earth grid.', maintenance: 'Torque ground pad bolts and keep standoff insulators clean.' },
      'sal-terminal': { ansiCode: 'Top Bronze Stud & Line Jumper', fieldSpot: 'Clamps tying each 13.8 kV secondary riser directly onto MOV arrester crown.', workingPrinciple: 'Low-inductance straight lead prevents inductive L(di/dt) surge rise above 110 kV BIL.', maintenance: 'Keep connecting lead short (<0.5 m) and torque bronze clamps.' },
      'sal-zno-core': { ansiCode: '10.2 kV MCOV ZnO Varistor Discs', fieldSpot: 'Stacked ceramic discs inside each arrester column.', workingPrinciple: 'Transition from insulator to micro-second conductor above 24 kV surge crest.', maintenance: 'Infrared check annually for uneven disc heating.' },
      'sal-sheds': { ansiCode: '15 kV Wet-Process Dark Porcelain Housing', fieldSpot: 'Three dark brown ribbed columns protecting secondary LV bus.', workingPrinciple: 'Delivers ≥430 mm creepage distance against coastal mist pollution.', maintenance: 'Inspect skirts visually with binoculars for hairline glaze cracks.' },
      'sal-ground-lead': { ansiCode: 'Direct Secondary Rack Ground Lead', fieldSpot: 'Heavy copper pigtail linking arrester bottom base directly to rack ground bar.', workingPrinciple: 'Shunts lightning surges locally to protect TR-01 X1–X3 bushings.', maintenance: 'Verify continuity to IEEE 80 grid.' },
      'lvct-tank': { ansiCode: 'Outdoor Cycloaliphatic Epoxy Instrument Body', fieldSpot: 'Molded resin metering/protection units inline after 13.8 kV bus.', workingPrinciple: 'Combines high hydrophobic outdoor tracking strength with maintenance-free solid dielectric.', maintenance: 'Wipe chalking resin and inspect secondary conduit box gaskets.' },
      'lvct-core': { ansiCode: 'Dual Metering (0.3%) & Protection (C200) Cores', fieldSpot: 'Embedded steel toroids carrying 2000/5 A and 120:1 ratios.', workingPrinciple: 'Isolated cores prevent revenue meter burn-out while keeping protection unsaturated at 18.4 kA faults.', maintenance: 'Verify secondary burden below 45 VA and check CT shorting screws.' },
      'lvct-bushings': { ansiCode: 'Primary Copper Tabs & Secondary Conduit', fieldSpot: 'Bolted NEMA flags on crown and sealed armored conduit to Panel 2.', workingPrinciple: 'Delivers phase currents & voltages continuously to AVR/OLTC and ANSI 51/27 relays.', maintenance: 'Check conduit seals against ant/moisture ingress.' },
      'lvds-frame': { ansiCode: 'Galvanized Rack Channel & Bearings', fieldSpot: 'Steel base channel mounted on the 13.8 kV overhead support structure.', workingPrinciple: 'Maintains aligned phase spacing and torsional stability for gang opening.', maintenance: 'Grease sealed turntable bearings every 5 years.' },
      'lvds-insulators': { ansiCode: '15 kV TR-205 Porcelain Post Insulators', fieldSpot: 'Brown vertical porcelain columns beneath disconnect jaws and hinges.', workingPrinciple: '110 kV BIL standoff insulation under 80 kA momentary short-circuit forces.', maintenance: 'Check cement caps and porcelain glaze cleanliness.' },
      'lvds-blades': { ansiCode: '2,000 A Dual ETP Copper Blades', fieldSpot: 'Bright parallel copper blade arms engaging spring jaw contacts.', workingPrinciple: 'Pinch-effect geometry tightens contacts magnetically under fault spikes.', maintenance: 'Verify silver contact wipe and check IR delta-T < 10°C.' },
      'lvds-linkage': { ansiCode: 'Vertical Torsion Pipe & LOTO Handle', fieldSpot: 'Operating pipe descending to eye-level lockable handle on rack leg.', workingPrinciple: 'Key/electrical interlock blocks actuation whenever 52-LV is closed.', maintenance: 'Check mechanical stops and padlock hasp alignment.' },
      'lvcb-frame': { ansiCode: 'Outdoor 15 kV Vacuum Breaker Pedestal', tag: 'LVCB-FRM', fieldSpot: 'Painted steel frame supporting main 52-LV enclosure.', workingPrinciple: 'Anchors breaker against electromagnetic opening shock forces.', maintenance: 'Inspect frame paint and ground braid.' },
      'lvcb-vacuum-bottles': { ansiCode: '3× Sealed CuCr Vacuum Interrupter Bottles', fieldSpot: 'Concentric ceramic/copper vacuum cylinders inside pole heads.', workingPrinciple: 'Vacuum recovers dielectric strength at ~10 kV/µs after zero-crossing, quenching 31.5 kA arcs inside 12 ms.', maintenance: '36 kV 1-min AC vacuum check + contact erosion travel mark check.' },
      'lvcb-mech': { ansiCode: '125 VDC Spring Mechanism & Dual Trip Coils', fieldSpot: 'Front cabinet housing motor-wound closing spring and Flag indicator (RED/GREEN).', workingPrinciple: 'Stored-energy opening spring guarantees instant trip even if DC motor fails.', maintenance: 'Check anti-condensation strip heater and trip coil resistance.' },
      'lvcb-bushings': { ansiCode: '15 kV Entrance Sheds & Line Flag Pads', fieldSpot: 'Three primary/three load side epoxy bushings topped with 2000 A pads.', workingPrinciple: 'Bridges TR-01 buswork seamlessly to 13.8 kV Main Bus.', maintenance: 'IR scan bolted flags annually at peak substation MVA.' },
      'sst-tank': { ansiCode: '100 kVA Corrugated Mineral-Oil Steel Tank', fieldSpot: 'Compact radiator-finned oil tank supplying Control House auxiliary power.', workingPrinciple: 'Passive ONAN cooling handles continuous auxiliary station loads silently.', maintenance: 'Inspect radiator welds and check top oil temperature.' },
      'sst-hv-fuses': { ansiCode: '13.8 kV Porcelain Entry & Expulsion Fuses', fieldSpot: 'Roof-mounted brown porcelain bushings fed from 13.8 kV Main Bus.', workingPrinciple: 'Fused tap isolates internal SST fault instantly without darkening feeders.', maintenance: 'Inspect fuse tubes and check silicone animal guards.' },
      'sst-core-windings': { ansiCode: '100 kVA Step-Down Core (13.8 kV / 480Y-277V)', fieldSpot: 'Internal laminated core and copper coils delivering auxiliary AC.', workingPrinciple: 'Maintains stable 480/277 V power for HVAC, chargers, and ONAF2 transformer fans.', maintenance: 'Verify primary tap changer matches 13.8 kV nominal.' },
      'sst-lv-cabinet': { ansiCode: '480V Station Service Terminal Box', fieldSpot: 'Side NEMA 3R cabinet routed via buried conduit into Control House.', workingPrinciple: 'Protects main 150 A MCCB feeding AC Panelboard and dual 125V DC battery chargers.', maintenance: 'Verify conduit sealing compound and phase rotation.' },
      'cap-rack': { ansiCode: 'Insulated Elevated Capacitor Bank Rack', fieldSpot: 'Aluminum rack mounted on 15 kV base insulators beside Feeder bays.', workingPrinciple: 'Floating rack isolates 13.8 kV grounded-wye bank cleanly with neutral CT monitoring.', maintenance: 'Inspect base insulators and neutral imbalance wiring.' },
      'cap-cans': { ansiCode: '3.6 MVAR All-Film Capacitor Can Units', fieldSpot: 'Rows of steel-cased silver cans topped by dual 15 kV porcelain bushings.', workingPrinciple: 'Supplies 150.6 A leading VARs to counteract inductive feeder motor loads.', maintenance: 'Wait 5 min discharge before touching! Inspect cans for bulged walls.' },
      'cap-reactors': { ansiCode: 'Current-Limiting Inrush Iron/Air Reactors', fieldSpot: 'Coiled cylindrical inductors ahead of each phase row.', workingPrinciple: 'Blunts transient di/dt inrush spikes during capacitor energization.', maintenance: 'Check coil tie-down bolts against electromagnetic vibration.' },
      'cap-vcb': { ansiCode: '52-CAP Synchronous Vacuum Capacitor Switch', fieldSpot: 'Dedicated pole/rack vacuum switch with restrike-free contacts.', workingPrinciple: 'Zero-crossing point-on-wave closing suppresses transient overvoltages <1.2 pu.', maintenance: 'Log daily switching counter (<5,000 ops without contact check).' },
      'f1-frame': { ansiCode: 'Feeder 01 Support Channel & Bypass Rack', fieldSpot: 'Steel structure carrying Feeder 01 breaker and disconnects.', workingPrinciple: 'Organizes radial exit bay clearance cleanly inside 13.8 kV bus zone.', maintenance: 'Verify steel ground grid lugs.' },
      'f1-vcb': { ansiCode: '52-F1 1,200 A Vacuum Feeder Breaker', fieldSpot: 'Primary breaker guarding Commercial/Industrial Feeder 01 with 79 recloser.', workingPrinciple: 'Clears persistent feeder faults and executes automated 3-shot reclosing.', maintenance: 'Download relay event oscillography after every 79 lockout.' },
      'f1-disconnects': { ansiCode: '89-F1A / 89-F1B Line & Bus Disconnects', fieldSpot: 'Hook-stick copper blades flanking 52-F1.', workingPrinciple: 'Allows safe isolated breaker rack maintenance while Bus remains live.', maintenance: 'Confirm padlock brackets and latch spring tension.' },
      'f1-relay-ct': { ansiCode: 'Feeder 01 1200/5 A CTs & Residual Sensing', fieldSpot: 'Epoxy toroidal CTs driving Panel 2 Feeder 01 relay.', workingPrinciple: 'Measures phase and zero-sequence currents for selective 50/51/51N tripping.', maintenance: 'Secondary injection check annually.' },
      'f2-frame': { ansiCode: 'Feeder 02 Support Channel & Rack', fieldSpot: 'Steel bay frame adjacent to Feeder 01.', workingPrinciple: 'Supports Feeder 02 isolation and 15 kV takeoff conductors.', maintenance: 'Verify anchor bolts and zinc galvanization.' },
      'f2-vcb': { ansiCode: '52-F2 1,200 A Vacuum Feeder Breaker', fieldSpot: 'Dedicated vacuum breaker controlling radial Feeder 02.', workingPrinciple: 'Provides fast transient clearing and SCADA supervisory switching.', maintenance: 'Check travel time (<3 cycles) and counter increments.' },
      'f2-disconnects': { ansiCode: '89-F2A / 89-F2B Isolation Switches', fieldSpot: 'Flanking air-break copper blades around 52-F2.', workingPrinciple: 'Visible physical air break for crew LOTO clearances.', maintenance: 'Clean silver jaw faces and inspect porcelain skirts.' },
      'f2-relay-ct': { ansiCode: 'Feeder 02 1200/5 A Protection CTs', fieldSpot: 'Phase & ground sensing CTs feeding Panel 2 Relay.', workingPrinciple: 'Feeds 50/51/51N elements with accurate fault current wave reproduction.', maintenance: 'Test saturation knee voltage during 5-year PM.' },
      'rec-tank': { ansiCode: '79-ACR1 Solid-Dielectric Manifold & Top Head', fieldSpot: 'Compact pole-top epoxy housing painted weather-grey on Pole #1.', workingPrinciple: 'Encapsulates magnetic actuator linkages for sub-cycle repeatable opening and reclosing.', maintenance: 'Visual inspection for wildlife nesting or tracking marks.' },
      'rec-interrupters': { ansiCode: 'Embedded Vacuum Bottles (12.5 kA Sym)', fieldSpot: 'Three vertical cylindrical poles protruding upwards from manifold.', workingPrinciple: 'Executes 2 Fast (Curve A) trips ahead of downstream 100K fuse melt + 2 Slow (Curve B) trips.', maintenance: 'Check mechanical yellow non-reclose handle indicator.' },
      'rec-bushings': { ansiCode: '15.5 kV Silicone Creepage Sheds', fieldSpot: 'Alternate weather sheds with incoming & outgoing hot-line clamps.', workingPrinciple: 'Guarantees 110 kV BIL across coastal contamination conditions.', maintenance: 'Check bird guards and hot-line clamp compression.' },
      'rec-control-box': { ansiCode: 'Pole-Base Recloser SEL/Form-6 Control Box', fieldSpot: 'Eye-level aluminum cabinet strapped to lower Pole #1.', workingPrinciple: 'Computes Inverse/Fast curves and reports SCADA FLISR telemetry via radio/fiber.', maintenance: 'Test 24 VDC backup battery under load annually.' },
      'sect-frame': { ansiCode: 'Crossarm Sectionalizer Mounting Steel', fieldSpot: 'Galvanized channel holding three-phase sectionalizer poles on Pole #2.', workingPrinciple: 'Maintains exact contact geometry while dropout actuators trip.', maintenance: 'Verify pole thru-bolt tightness.' },
      'sect-insulators': { ansiCode: '15.5 kV Composite Silicone Standoffs', fieldSpot: 'Three insulated support columns along crossarm.', workingPrinciple: 'Provides full 110 kV BIL phase-to-crossarm dielectric withstand.', maintenance: 'Inspect silicone sheds with binoculars.' },
      'sect-actuators': { ansiCode: 'Zero-Current Dead-Time Dropout Mechanism', fieldSpot: 'Spring-latched hinge blades designed to drop visibly open at count = 2.', workingPrinciple: 'Counts upstream 79-ACR1 current-zero intervals; opens strictly when de-energized—requiring zero arc-quenching chamber!', maintenance: 'Test latch drop torque using calibrated spring scale during line outage.' },
      'sect-counter': { ansiCode: 'Self-Powered Fault Pulse Counter Module', fieldSpot: 'Enclosed sensing housing registering fault impulses (>160 A -> 0 A).', workingPrinciple: 'Requires NO CTI coordination time curve against upstream recloser—100% selective by pulse count.', maintenance: 'Reset mechanical flags carefully after restoration.' },
      'fuse-bracket': { ansiCode: 'NEMA Cutout Crossarm Mounting Hook', fieldSpot: 'Compact galvanized J-bracket clamping onto lateral Pole #3 crossarm.', workingPrinciple: 'Anchors C-frame cutout at standard 15-degree forward tilt for clean gravity drop.', maintenance: 'Confirm tight carriage bolt grip on crossarm timber.' },
      'fuse-insulator': { ansiCode: '15 kV Silicone/Porcelain C-Frame Body', fieldSpot: 'Distinct C-shaped insulator separating live top contact hood from lower trunnion hinge.', workingPrinciple: 'Full 110 kV BIL rating between energized lateral tap and grounded crossarm.', maintenance: 'Inspect top arc-hood copper spring leaf.' },
      'fuse-tube': { ansiCode: 'Bone-Fiber Fiberglass Expulsion Fuse Tube', fieldSpot: 'Inclined cream/tan cylinder hanging visibly straight down at 180° when blown!', workingPrinciple: 'Arc heat vaporizes internal bone-fiber liner, blasting deionized gas out the bottom muzzle to extinguish fault arcs up to 10 kA.', maintenance: 'Replace charred tube if inner bore diameter expands >10% after repeated faults.' },
      'fuse-link': { ansiCode: '100K Tin Fuse Link & Braided Leader', fieldSpot: 'Taut copper pigtail exiting bottom cap held by toggle trunnion latch.', workingPrinciple: 'On permanent fault beyond 79-ACR1 fast shots, tin element melts cleanly, releasing toggle latch so tube drops open visually.', maintenance: 'Always replace blown links with identical 100K speed rating (never substitute copper wire!).' },
      'da-cap': { ansiCode: 'Insulated Raptor/Squirrel Guard Top Cap', fieldSpot: 'Orange/grey slotted dome capping pole-top MOV arresters.', workingPrinciple: 'Blocks birds spanning live 13.8 kV riser clamps to steel brackets.', maintenance: 'Inspect locking snap tabs.' },
      'da-zno': { ansiCode: '8.4 kV MCOV Distribution MOV Discs', fieldSpot: 'Internal ZnO stack clamped in series ahead of transformers and lateral poles.', workingPrinciple: 'Clamps fast-front lightning waves safely below 35 kV peak.', maintenance: 'IR check during line patrol.' },
      'da-sheds': { ansiCode: 'Compact 15 kV Polymer/Porcelain Sheds', fieldSpot: 'Slender dark ribbed columns alongside cutout on Pole #3.', workingPrinciple: 'Short-profile lightning protection mounted right at protected transformer terminals.', maintenance: 'Inspect housing for burst tracking.' },
      'da-isolator': { ansiCode: 'Explosive Ground-Lead Disconnector', fieldSpot: 'Small white cartridge hanging below arrester base feeding earth lead.', workingPrinciple: 'Detonates a tiny primer if ZnO discs short permanently, blowing off ground lead visibly so crew spots faulty unit from truck.', maintenance: 'Never touch dangling disconnector lead until line isolated.' },
      'subb-xfmr': { ansiCode: 'Substation B 69/13.8 kV Tie Transformer', fieldSpot: 'Eastern remote tie substation feeding 13.8 kV Bus B at 1.00 pu.', workingPrinciple: 'Maintains independent N-1 alternate generation path for automated FLISR back-feeding.', maintenance: 'Telemetry polled continuously by SCADA Master.' },
      'subb-tie-recloser': { ansiCode: '79-TIE Normally-Open Loop Tie Recloser', fieldSpot: 'Tie recloser sitting at eastern Feeder 01 boundary marked NORMALLY OPEN.', workingPrinciple: 'Closes upon FLISR command only after upstream faulted segment is locked open, restoring Industrial & Commercial customers in <4.2 s.', maintenance: 'Verify ANSI 25 synchrocheck relay health monthly.' },
      'subb-bus-rack': { ansiCode: 'Substation B Dead-End Tie Gantry', fieldSpot: 'Steel H-frame facing west toward Main Substation Feeder 01.', workingPrinciple: 'Establishes mechanical open-tie span separation between two independent 69 kV sources.', maintenance: 'Check dead-end clamps and ground bonds.' },
      'subb-rtu': { ansiCode: 'Substation B FLISR SCADA RTU Cabinet', fieldSpot: 'Control box monitoring tie voltage magnitude & phase angle.', workingPrinciple: 'Communicates via DNP3 peer-to-peer FLISR loop automation protocol.', maintenance: 'Confirm redundant fiber/cellular link latency <50 ms.' },
      'dt-tank-fins': { ansiCode: 'ANSI 70 Tank, Fin Radiators, Lid & Lifting Lugs', fieldSpot: 'Cylindrical rolled-steel or corrugated pad-mounted weatherproof tank painted light utility gray with bolted top cover and kVA stencil.', workingPrinciple: 'Houses dielectric mineral oil (65°C rise) circulating by natural thermosiphon convection (ONAN) through vertical radiator fins to dissipate I²R winding and core hysteresis losses.', maintenance: 'Inspect weld seams for oil weeping, check oil level gauge at 25°C reference mark, and test tank-to-ground continuity.' },
      'dt-core-coil': { ansiCode: 'CRGO Wound Core & Kraft-Insulated Copper/Al Windings', fieldSpot: 'Internal magnetic silicon-steel core and concentric HV/LV winding assembly suspended beneath the top cover.', workingPrinciple: 'Transfers energy by mutual magnetic induction at 7.967 kV L-N (or 13.8 kV L-L) down to 240/120 V or 480Y/277 V utilization voltage with 1.8–4.5% series leakage impedance.', maintenance: 'Perform Turns Ratio (TTR), winding resistance, and insulation Megger tests whenever tank cover is unbolted.' },
      'dt-hv-bushing': { ansiCode: 'Glazed Brown Porcelain HV Bushing (H₁ / H₂) & Wildlife Guard', fieldSpot: 'Skyward-pointing ribbed wet-process porcelain insulator petticoats topped with brass eyebolt terminal and snapped-on polymer squirrel guard.', workingPrinciple: 'Provides ≥95 kV BIL basic impulse insulation level and leakage creepage across 13.8 kV primary leads while shielding live bronze caps against avian/squirrel phase-to-ground bridging.', maintenance: 'Clean salt/dust contamination, inspect porcelain skirts for tracking or chips, and verify wildlife cap latches securely.' },
      'dt-lv-bushings': { ansiCode: 'Secondary Bushings (X₁, X₀, X₂ / X₁–X₃) & Triplex Drops', fieldSpot: 'Side-wall molded polymer/porcelain LV terminals bonded to insulated aluminum triplex/quadruplex service drop cables.', workingPrinciple: 'Delivers high-current utilization power (up to >1,800 A on 1,500 kVA pads) with X₀ rigidly bonded to both the neutral messenger and tank ground strap per NEC/NESC.', maintenance: 'Torque spade NEMA compression lugs, infrared-scan for hot spots >15°C above ambient, and verify drip loops keep water out of conduit.' },
      'dt-fuse-cutout': { ansiCode: 'ANSI C37.41 Expulsion Fuse Cutout (15 kV, 100 A Frame)', fieldSpot: 'Porcelain C-frame cutout mounted on a fiberglass crossarm bracket with a hot-line clamp tapping the primary overhead phase via a stirrup.', workingPrinciple: 'Contains a replaceable Type K (fast) or Type T (slow) silver-alloy fuse link inside a boric-acid/fiber expulsion tube; fault gas pressure extinguishes the arc and drops the barrel open for visible isolation.', maintenance: 'Never re-fuse with oversized links; verify fuseholder trunnion alignment and operate only under load with a Loadbuster tool.' },
      'dt-arrester-ground': { ansiCode: '10 kV MOV Surge Arrester (MCOV 8.4 kV) & Driven Ground Rod', fieldSpot: 'Gray polymer-housed ZnO surge arrester mounted beside the cutout and bonded down the pole molding to a 5/8" × 8 ft copper-clad ground rod.', workingPrinciple: 'Clips lightning and switching overvoltages (>28 kV) directly to earth via highly nonlinear zinc-oxide varistor blocks, shunting up to 10 kA impulses away from transformer turn insulation.', maintenance: 'Check fault-indicator isolator cap at the arrester base and measure ground rod resistance (≤25 Ω per NESC Rule 94B).' },
      'pole-shaft-ground': { ansiCode: '40 ft Class 3 Pole Shaft, Ground Wire & Butt Plate', fieldSpot: 'Treated Class 3 Douglas Fir / spun-concrete shaft planted 6.0 ft deep with plastic stapled #4 Cu ground wire down to base electrode.', workingPrinciple: 'Resists combined Grade B/C wind (90 mph NESC) and conductor tension bending moments while providing an uninterrupted earth path for pole-top hardware bonds.', maintenance: 'Sound wood poles at groundline for internal decay every 8–10 years; verify PVC molding covers the #4 Cu ground riser from grade up 8 ft.' },
      'pole-crossarm-brace': { ansiCode: '8 ft Crossarm(s), Steel V-Braces & Lag Hardware', fieldSpot: 'Single tangent or double dead-end pressure-treated crossarm bolted at the pole gain with galvanized flat steel V-braces and square washers.', workingPrinciple: 'Maintains 30–36 in horizontal phase-to-phase air clearance (13.8 kV) and transfers transverse/longitudinal wire loads cleanly into the pole bolt.', maintenance: 'Retighten through-bolts after wood shrinkage cycles and check for split ends or rusted V-brace lag screws.' },
      'pole-insulators': { ansiCode: 'ANSI 55-5 Pin/Post Insulators & Dead-End Strain Bells', fieldSpot: 'Ribbed porcelain/polymer insulators mounted along the top of the crossarm (tangent) or horizontal suspension bells at tap/dead-end corners.', workingPrinciple: 'Maintains ≥105 kV BIL impulse withstand between energized 13.8 kV ACSR conductors and grounded/bonded crossarm hardware under rain and fog.', maintenance: 'Binocular-inspect tie wires, armor rods, and polymer sheds for corona erosion or gunshot damage.' },
      'pole-guy-anchor': { ansiCode: 'Down-Guy Strand, Yellow Guy Guard & Helical Anchor', fieldSpot: 'Angle-pull 3/8" EHS galvanized steel guy wire running from an eye-bolt/guy-hook near the crossarm down through an 8 ft yellow visibility guard into a screw anchor.', workingPrinciple: 'Balances unbalanced longitudinal conductor tension at dead-ends, tap corners, and heavy equipment poles so the pole shaft remains in compression rather than excessive cantilever bending.', maintenance: 'Confirm turnbuckle/preformed dead-end grip tension and verify the 8 ft bright yellow safety guard is free of brush.' },
      'pole-spool-rack': { ansiCode: '3-Wire Secondary Spool Rack & Neutral Clevis', fieldSpot: 'Galvanized steel vertical secondary rack holding three white porcelain spools with bare ACSR neutral and insulated 120/240 V secondary conductors.', workingPrinciple: 'Carries low-voltage secondary mains and establishes the Multi-Grounded Neutral (MGN) reference tying pole grounds, transformer X₀, and customer service drops together.', maintenance: 'Check spool clevis pins and neutral compression sleeves for galvanic corrosion.' },
      'gate-leaves': { ansiCode: 'Heavy Steel Vehicular Swing Gate & Man-Gate', fieldSpot: 'Motorized twin 3.2 m steel crash gate leaves anchored into concrete pilasters, flanked by an outward pedestrian gate.', workingPrinciple: 'Maintains continuous NERC CIP-014 & NESC Rule 110 anti-intrusion exclusion around live HV/MV equipment while swinging open 90° for crane trucks.', maintenance: 'Lubricate pintle hinges, test motorized limit switches, and verify center drop-rod alignment.' },
      'gate-posts-barbed': { ansiCode: '3.0 m Precast Concrete Wall Pilasters & 45° Razor/Barb Arms', fieldSpot: 'Reinforced concrete columns and panels topped with 45° galvanized V-outriggers carrying 3-strand barbed wire and concertina razor coil.', workingPrinciple: 'Establishes a solid 3.55 m anti-climb ballistic/arc barrier eliminating public line-of-sight hazards per NERC CIP & NESC 110A.', maintenance: 'Inspect concrete panel joint sealants, barbed wire tension >= 150 lbf, and ANSI Z535 HV danger plaques.' },
      'gate-guardhouse': { ansiCode: 'Security Guardhouse Booth & Card-Reader Entry Bollard', fieldSpot: 'Climate-controlled pre-fab steel/glass booth beside the driveway apron plus yellow steel card-reader pedestal reachable from truck cab height.', workingPrinciple: 'Enforces two-factor utility access control, visitor sign-in logbook, PPE inspection (FR clothing/hard hat/voltage-rated gloves), and clearance-hold verification.', maintenance: 'Test badge reader fail-secure relay, intercom link to System Control Center, and exterior floodlight photocell.' },
      'gate-apron-ground': { ansiCode: 'Asphalt Driveway Apron & Flexible Copper Gate Ground Braids', fieldSpot: 'Paved asphalt approach tying the highway curb to the crushed-stone yard apron, plus tinned flexible copper braid straps spanning each gate hinge.', workingPrinciple: 'Supports heavy oil-filled transformer haulers (HS-20 axle load) across the ditch culvert while keeping swing gate leaves solidly bonded at <1 Ω to the buried IEEE 80 ground grid.', maintenance: 'Inspect flexible hinge copper braids for metal fatigue cracks every quarterly yard walkdown — never rely on dry hinges for fault grounding.' },
      'city-gate-arch': { ansiCode: '6.8 m Clear Steel Boulevard Archway & District Marquee', fieldSpot: 'Spanning public highway 140 m East of Substation A at the City & URD Subdivision entrance.', workingPrinciple: 'Guarantees 140 m HV setback clearance from substation perimeter walls and maintains >6.8 m NESC/DOT heavy truck vertical clearance.', maintenance: 'Check structural anchor bolts, LED marquee visibility, and retroreflective stripes.' },
      'city-gate-boom': { ansiCode: 'Motorized Sliding Barrier Arms & Entry Kiosk', fieldSpot: 'Bilateral yellow-striped traffic barriers flanking the highway guardhouse kiosk.', workingPrinciple: 'Restricts unauthorized non-utility vehicles entering the gated utility district; opens interactively via click or [E].', maintenance: 'Test optical safety beam sensors and manual hand-crank override.' },
      'ind-hv-cb': { ansiCode: '52-IND Dedicated 69/138 kV Industrial Feeder SF6 Breaker', fieldSpot: 'North-East Substation A bay dead-end ahead of the private steel sub-transmission corridor.', workingPrinciple: 'Isolates heavy customer steel mill & arc-furnace faults within 2–3 cycles at 69/138 kV without disturbing city 13.8 kV feeders.', maintenance: 'Monitor SF6 pressure gauge, trip-coil continuity, and contact wear counter.' },
      'ind-hv-ds': { ansiCode: '89-INDA / 89-INDB Industrial Feeder Isolation Disconnects', fieldSpot: 'Motor-operated center-break air disconnects flanking 52-IND.', workingPrinciple: 'Establishes visible air-gap clearance under LOTO whenever servicing 52-IND or patrolling the private North ROW.', maintenance: 'Inspect silver-plated hinge contacts and mechanical block interlocks.' },
      'ind-hv-gantry': { ansiCode: 'North-East Industrial Sub-Transmission Takeoff Gantry & Arresters', fieldSpot: 'Galvanized steel H-frame gantry + station-class MOV arresters aimed North-East toward 52-CUST.', workingPrinciple: 'Suspends tensioned 69/138 kV ACSR sub-transmission conductors cleanly above the 3.0 m precast perimeter concrete wall.', maintenance: 'Thermographic check on dead-end compression clamps and arrester surge counters.' }
    };

    // 4th-Year EE Field Engineer Diagnostic Quiz Questions (FA1 & SA1 Aligned)
    const QUIZ_QUESTIONS = [
      {
        question: "In the 69 kV / 13.8 kV Power Transformer (Dyn11), what is the exact physical meaning of the vector notation 'Dyn11'?",
        options: [
          "(Recommended) Primary is Delta, Secondary is Grounded-Wye with neutral, and LV voltage lags HV voltage by 30° (or leads by 330°).",
          "Primary is Grounded-Wye, Secondary is Delta, and LV leads HV by 11 degrees.",
          "Both windings are Delta connected with an 11% impedance margin.",
          "Primary has 11 tap changer positions with dynamic neutral regulation."
        ],
        correct: 0,
        explanation: "In IEC/IEEE vector nomenclature, D = Delta primary, y = Wye secondary, n = neutral brought out, 11 = clock position of secondary voltage vector relative to primary (11 o'clock corresponds to 330° or -30° phase lag)."
      },
      {
        question: "What catastrophic event occurs if an operator opens a 69 kV Disconnect Switch (ANSI 89) while Circuit Breaker 52 is CLOSED and carrying load?",
        options: [
          "(Recommended) Violent plasma arc flashover (>19,000°C) occurs across the air gap, destroying equipment and threatening life safety.",
          "The disconnect switch opens smoothly because air has high natural dielectric strength.",
          "The transformer OLTC automatically compensates for the open circuit.",
          "The Buchholz relay trips before any arcing can develop."
        ],
        correct: 0,
        explanation: "Disconnect switches have zero arc-quenching capability (0 A interrupting capacity). Attempting to interrupt load current in open air produces an incandescent plasma channel exceeding 19,000°C, causing catastrophic explosive vaporization of copper."
      },
      {
        question: "Why must Current Transformer (CT) secondary terminals NEVER be left open-circuited while the primary winding is energized?",
        options: [
          "(Recommended) Total primary current acts as magnetizing current, inducing lethal peak voltages (>5 kV) that destroy insulation and pose fatal shock hazards.",
          "The CT will freeze its mechanical mechanism and trip the circuit breaker.",
          "The secondary current will surge to thousands of amperes and melt the relay wiring.",
          "The voltage transformer will experience extreme ferroresonance."
        ],
        correct: 0,
        explanation: "When the secondary is open, there is no demagnetizing secondary MMF (N2*I2 = 0). The entire primary current excites the core into deep saturation, producing very sharp, high-magnitude peak secondary voltage pulses exceeding several thousand volts."
      },
      {
        question: "Per IEEE Std 80-2013, what is the primary engineering purpose of spreading a 100 mm layer of crushed rock (ρ_s = 2,500 to 3,000 Ω·m) across the switchyard?",
        options: [
          "(Recommended) It elevates human contact resistance beneath feet, dramatically raising tolerable touch and step potential limits.",
          "It lowers the total grounding grid resistance Rg to below 1.0 Ω.",
          "It prevents weeds from short-circuiting the high-voltage busbars.",
          "It acts as a magnetic shield against 60 Hz electromagnetic radiation."
        ],
        correct: 0,
        explanation: "High-resistivity surface rock adds series foot resistance (Rf = 3*Cs*ρs). This limits the body shock current during a fault, significantly elevating tolerable touch and step voltages without requiring excessive underground copper."
      },
      {
        question: "In transformer differential protection (ANSI 87T), what is the function of the percentage restraint characteristic?",
        options: [
          "(Recommended) Prevents false tripping during external through-faults caused by CT saturation and tap changer ratio mismatches.",
          "Restrains the circuit breaker from tripping during normal load switching.",
          "Restricts the transformer cooling fans from operating at low oil temperatures.",
          "Maintains the primary bus voltage within ±5% of nominal PDC limits."
        ],
        correct: 0,
        explanation: "Through-faults induce high currents that cause unequal CT saturation and tap mismatch errors. The percentage restraint (slope) ensures the relay only trips when the differential operating current exceeds a percentage of the circulating through-current."
      },
      {
        question: "What is the function of the Buchholz Relay (ANSI 63) in a mineral oil-immersed power transformer?",
        options: [
          "(Recommended) Detects internal slow gas accumulation (incipient faults) via a top float and heavy oil surge waves (violent arcs) via a bottom flap.",
          "Regulates the tap changer motor speed during peak load conditions.",
          "Measures the temperature of the ambient air surrounding the radiator banks.",
          "Pumps mineral oil through the winding ducts during emergency overloads."
        ],
        correct: 0,
        explanation: "The Buchholz relay is mounted in the pipe between the main tank and conservator. Minor electrical discharges generate gas bubbles that rise and trip the top float (alarm), while severe arcing produces a rapid pressure wave that deflects the bottom flap (instantaneous trip)."
      },
      {
        question: "What is the IEEE Std 998 Rolling Sphere Method (RSM) striking distance (r_s) based upon?",
        options: [
          "(Recommended) The prospective lightning stroke current magnitude (I_s) via the electrogeometric equation r_s = 10 * (I_s)^0.65.",
          "The height of the dead-end gantry divided by the soil resistivity.",
          "The diameter of the metal-oxide varistor surge arrester discs.",
          "The maximum continuous operating voltage (MCOV) of the 69 kV bus."
        ],
        correct: 0,
        explanation: "The Electrogeometric Model (EGM) states that the final striking distance of a downward stepped leader depends on the return stroke current magnitude: r_s = 10 * (I)^0.65. Substation equipment completely below the rolling sphere surface is protected."
      },
      {
        question: "Why are substation DC battery systems (125 VDC) ungrounded or high-resistance grounded rather than solidly grounded?",
        options: [
          "(Recommended) A single ground fault on an ungrounded battery system does not blow fuses or cause breaker trip coils to fail to operate.",
          "Solid grounding would cause too much DC current to enter the AC grounding grid.",
          "Ungrounded batteries have higher chemical energy density.",
          "Solid grounding causes rapid chemical degradation of battery lead plates."
        ],
        correct: 0,
        explanation: "Maintaining an ungrounded 125 VDC system allows continuous operation during a single inadvertent ground fault without tripping DC supply breakers. A ground detector alarm alerts operators to locate the ground fault before a second ground fault can occur."
      }
    ];

    // Safe Switching Order Challenge Steps
    const SWITCHING_STEPS = [
      { id: 1, name: 'Step 1: Open / Trip Circuit Breaker 52', target: 'breaker_open', desc: 'Trip CB-69-1 to safely extinguish 348 A load current inside SF6 chamber.' },
      { id: 2, name: 'Step 2: Verify Telemetry Zero Current (0 A)', target: 'verify_zero_current', desc: 'Confirm via instrument CT readings that bus current has dropped to 0.0 A.' },
      { id: 3, name: 'Step 3: Open Line Disconnect Switch 89', target: 'disconnect_open', desc: 'Open DS-69-1 under verified no-load to establish a visible physical air gap.' },
      { id: 4, name: 'Step 4: Close Grounding / Earth Switch 89E', target: 'earth_close', desc: 'Close integrated grounding blade 89E to drain trapped capacitive charges to earth.' },
      { id: 5, name: 'Step 5: Apply Lockout / Tagout (LOTO) Padlocks', target: 'apply_loto', desc: 'Apply safety lockouts and danger tags per OSH Rule 1210 / DOLE guidelines.' }
    ];

    // Step-by-Step Numerical Sizing Calculations for 41.7 MVA, 69 / 13.8 kV Substation
    const SIZING_CALCS = {
      transformer: {
        title: 'TR-01 Main Power Transformer (25/33.3/41.7 MVA)',
        dutyNormal: 'HV Load I_HV = 41.7 MVA / (sqrt(3) * 69 kV) = 348.9 A | LV Load I_LV = 41.7 MVA / (sqrt(3) * 13.8 kV) = 1,744.6 A',
        dutyFault: 'Max Through-Fault I_sc,LV = I_LV / Z_pu = 1,744.6 A / 0.095 = 18.36 kA (3-Phase Bolted)',
        steps: [
          '1. Peak Load Forecast: 38.2 MVA diversified demand -> Select 25/33.3/41.7 MVA ONAN/ONAF/ONAF2 (~9% headroom).',
          '2. Rated HV / LV Currents: I_1 = 41,700 / (1.732 * 69) = 348.9 A; I_2 = 41,700 / (1.732 * 13.8) = 1,744.6 A.',
          '3. Per-Unit Impedance Selection: Choose Z = 9.5% @ 25 MVA base so 13.8 kV fault <= 18.4 kA (< 31.5 kA VCB rating).',
          '4. BIL & OLTC Range: 69 kV class -> 350 kV BIL HV bushings; +-10% (32 steps x 0.625%) OLTC holds LV within +-1%.',
          '5. Cooling Capacity: ONAN handles 60% load silently; two automatic fan banks boost thermal capacity by +67%.'
        ]
      },
      breaker: {
        title: '69 kV SF6 Circuit Breaker (52-69) Sizing',
        dutyNormal: 'I_rated,continuous = 1.25 * 348.9 A = 436 A -> Standard 1200 A frame',
        dutyFault: 'Available 69 kV Bus 3-Phase Fault = 19.8 kA sym -> Select 40 kA @ 72.5 kV',
        steps: [
          '1. Voltage Class & BIL: 69 kV nominal -> 72.5 kV max design voltage, 350 kV BIL (IEEE C37.06).',
          '2. Continuous Current: 348.9 A max load x 1.25 margin = 436 A -> Select standard 1,200 A interrupter.',
          '3. Interrupting Rating: 69 kV system MVA_sc = 2,366 MVA -> I_sc = 19.8 kA -> Select 40 kA (2x margin).',
          '4. Interrupting Time & TRV: 3-cycle (50 ms) clearing time limits I^2*t thermal stress in busbar & TR-01.'
        ]
      },
      disconnect: {
        title: '69 kV Vertical-Break Disconnect Switch (89) Sizing',
        dutyNormal: 'I_continuous >= 1200 A (matches 52-69 frame), Momentary Peak >= 104 kA',
        dutyFault: 'Short-Time Withstand (I_th, 3 s): >= 40 kA sym.',
        steps: [
          '1. Standard Matching Frame: Match 72.5 kV, 350 kV BIL, 1,200 A continuous rating of adjacent 52-69.',
          '2. Peak Close-and-Latch / Momentary Current: I_peak = 2.6 * I_sc = 2.6 * 19.8 kA = 51.5 kA -> Select 104 kA peak.',
          '3. Phase Spacing: >= 2.13 m (7 ft) per IEEE C37.32 vertical-break horn-gap air clearance at 72.5 kV.',
          '4. Grounding Blade 89E: Copper ground braid sized >= 4/0 AWG to carry capacitive & induced currents.'
        ]
      },
      arrester: {
        title: '69 kV Station-Class MOV Surge Arrester Sizing',
        dutyNormal: 'Max Continuous Operating Voltage (MCOV) >= V_LL / sqrt(3) * 1.05 = 41.8 kV',
        dutyFault: '60 kV Rated (48 kV MCOV) -> 10 kA Discharge V_res = 148 kV',
        steps: [
          '1. Line-to-Ground Operating Voltage: 69 kV / sqrt(3) = 39.84 kV; with 5% overvoltage = 41.8 kV -> Select 48 kV MCOV (60 kV duty-cycle).',
          '2. Temporary Overvoltage (TOV) Check: Effectively grounded coeff 1.25 * 39.84 = 49.8 kV < 60 kV rating (Safe).',
          '3. Protective Margin (PM) vs 350 kV BIL: PM = (350 - 148) / 148 = 136% (exceeds IEEE C62.22 >= 20% minimum).',
          '4. Lead Separation: Mount <= 3.0 m from TR-01 HV bushings to avoid traveling-wave doubling.'
        ]
      },
      ctvt: {
        title: '69 kV Instrument CT & CCVT Sizing',
        dutyNormal: 'CT Ratio = 600:5 A (or multi-ratio 1200:5), Class C800 (800 V @ 100 A)',
        dutyFault: 'Max Secondary Burden Check: V_sat = 800 V > I_fault,sec * (R_ct + R_lead + R_relay) = 495 V',
        steps: [
          '1. CT Primary Selection: Full load 348.9 A -> Select 600/5 A tap on 1200/5 A multi-ratio C800 core (~58% normal tap).',
          '2. Knee-Point Anti-Saturation Check: At 19.8 kA fault (165 A sec), V_req = 165 * (0.4 + 1.8 + 0.8) = 495 V < 800 V C-rating.',
          '3. VT Ratio & Burden: 69 kV / sqrt(3) = 39.84 kV : 115 V (Ratio 346.4 : 1 -> 600/350 tap), Dual 0.3WXYZ accuracy.',
          '4. Ferroresonance Damping: Load open-delta VT winding with permanent resistive damping module.'
        ]
      },
      gantry: {
        title: '69 kV Portal Gantry, Rigid Bus & Shielding Sizing',
        dutyNormal: '3-in Sch 40 6063-T6 Al Tube: Ampacity 2,350 A >> 348.9 A load',
        dutyFault: 'Cantilever & Rolling Sphere R = 45 m for Level I Shielding (0% direct strokes)',
        steps: [
          '1. Rigid Tubular Bus Ampacity: 3-inch Sch 40 6063-T6 Aluminum rated 2,350 A keeps steady conductor rise < 30 °C.',
          '2. Short-Circuit Deflection (IEEE 605): F = 0.2 * I_sc^2 / D_ph = 0.2 * 19.8^2 / 2.4 = 32.7 N/m -> span <= 7.5 m.',
          '3. Electrical Clearances (PEC / IEEE 1427): 2.40 m Ph-Ph (>= 1.8 m min) & 1.85 m Ph-Gnd (>= 0.8 m min).',
          '4. Rolling Sphere Shielding: Mast peaks at +14.8 m overlap 45 m arcs, placing every live busbar strictly in zero-penetration zone.'
        ]
      },
      auxiliary: {
        title: 'Control House, 125 VDC Battery & SST-100 Sizing',
        dutyNormal: 'SST-100 = 100 kVA (13.8kV / 480V); Battery 125 VDC, 200 Ah (8-hr rate)',
        dutyFault: 'Momentary 1-Min Simultaneous Trip Duty (8x Breakers @ 12 A) = 96 A -> V_dc >= 108 V',
        steps: [
          '1. Station Service kVA: TR-01 fans (18 kW) + HVAC (15 kW) + Battery Chargers (10 kW) + Lighting (12 kW) = 55 kW -> Select 100 kVA SST-100.',
          '2. DC Continuous & Momentary Load (IEEE 485): Relays/SCADA = 14 A x 8 hr = 112 Ah; 200 Ah Flooded Lead-Calcium provides 44% aging/temp margin.',
          '3. IEEE 80 Ground Grid Sizing: Conductor >= 4/0 AWG bare Cu (107 mm^2) handles 19.8 kA * 0.5 s without fusing; mesh yields R_g = 0.842 Ohm.'
        ]
      },
      secondary: {
        title: '13.8 kV Secondary Bay, NGR & 3.6 MVAR Cap Sizing',
        dutyNormal: 'I_sec = 1,744.6 A -> 2,000 A Main 52-LV; NGR = 10 Ohm; Cap = 150.6 A',
        dutyFault: 'SLG Fault Limited by NGR: I_SLG = (13,800 / sqrt(3)) / 10 Ohm = 796.7 A (10 s)',
        steps: [
          '1. Main VCB (52-LV): 1,744.6 A TR-01 ONAF2 output x 1.15 = 2,006 A -> 15 kV, 2,000 A, 31.5 kA Vacuum Breaker (> 18.4 kA fault).',
          '2. NGR Sizing (IEEE 32): Choose I_g = 800 A limit -> R_ngr = 7,967 V / 800 A = 9.96 Ohm (~10 Ohm, 10 s duty), energy = 6.37 MW.',
          '3. Capacitor Compensation: Raise 35 MW @ 0.88 PF -> 0.96 PF requires Q = 35*(tan 28.4 - tan 16.3) = 8.6 MVAR -> 3.6 MVAR switched stage 1.'
        ]
      },
      feeders: {
        title: '13.8 kV Outgoing Feeders (F1 & F2) Sizing',
        dutyNormal: 'Split 41.7 MVA -> ~20.8 MVA/Feeder = 872 A each -> 1,200 A Bay Rating',
        dutyFault: 'Through Fault I_f = 18.36 kA -> Select 25 kA / 1,200 A VCB + 477 kcmil ACSR',
        steps: [
          '1. Feeder Ampacity: 20.85 MVA per circuit / (1.732 * 13.8 kV) = 872.3 A -> 1,200 A VCB & 89-F disconnects give 37% contingency tie margin.',
          '2. Overhead Conductor: 477 kcmil ACSR "Hawk" rated 670 A continuous (or bundled twin-4/0) keeps thermal margin under N-1 feeder tie.',
          '3. Protection Coordination: ANSI 50 inst. @ 6.0 kA, ANSI 51 pickup @ 960 A (1.1x max), 79 auto-reclose shots 0.5 s / 2.0 s.'
        ]
      },
      ngr_01: {
        title: 'Neutral Grounding Resistor (NGR-01, 10 Ω) Sizing',
        dutyNormal: 'Steady Neutral Unbalance < 15 A; X0 = 0 V normal',
        dutyFault: 'I_SLG,max = V_LN / R_ngr = 7,967 V / 10.0 Ω = 796.7 A (Limits 18.4 kA down by 95%!)',
        steps: [
          '1. Target Fault Limit: Select 800 A limit to prevent TR-01 core iron burning and keep step/touch safe.',
          '2. Ohmic Sizing (IEEE C57.32): R = (13,800 / sqrt(3)) / 800 A = 9.96 Ω -> Standard 10.0 Ω stainless steel grid.',
          '3. Thermal Duty: P = I^2 * R = 796.7^2 * 10 = 6.35 MW for 10 s -> AISI 304 alloy < 760°C max rise.',
          '4. Ground Protection: ANSI 51G Neutral CT = 800/5 A, pickup @ 0.25x = 200 A (4:1 sensitivity margin).'
        ]
      },
      sa_lv: {
        title: '13.8 kV Secondary MOV Surge Arrester Sizing',
        dutyNormal: 'MCOV >= (13.8 / sqrt(3)) * 1.05 = 8.37 kV -> Select 10.2 kV MCOV (12 kV Rated)',
        dutyFault: '10 kA Clamping = 32.5 kV Peak vs 110 kV BIL -> Protective Margin = 238%',
        steps: [
          '1. Grounded-Wye Factor: With 10 Ω NGR, TOV during SLG approaches 1.73 pu -> choose 12 kV Duty Cycle (10.2 kV MCOV) intermediate class.',
          '2. BIL Margin: 110 kV LV BIL / 32.5 kV discharge = 3.38x safety margin (exceeds IEEE C62.22 20% rule).'
        ]
      },
      ctvt_lv: {
        title: '13.8 kV Bus CT (2000/5 A) & VT (14.4kV/120V) Sizing',
        dutyNormal: 'I_full = 1,744.6 A -> Select 2,000 / 5 A CT (87% continuous loading)',
        dutyFault: 'Max Fault = 18.36 kA (45.9 A sec) @ Z_burden = 0.8 Ω -> V_req = 36.7 V << 200 V (C200)',
        steps: [
          '1. Ratio Match: 1,745 A secondary load fits inside 2,000 A standard frame with RF = 1.33 thermal headroom.',
          '2. Knee Voltage Check: C200 accuracy avoids CT saturation up to 20x rated current without distorting ANSI 51 inverse timing.'
        ]
      },
      ds_lv: {
        title: '13.8 kV Secondary Disconnect Switch (89-LV) Sizing',
        dutyNormal: '2,000 A Continuous @ 15 kV, 110 kV BIL (matches 52-LV frame)',
        dutyFault: '80 kA Crest Momentary >= 2.6 * 18.36 kA (47.7 kA peak)',
        steps: [
          '1. Match 2,000 A rating of 52-LV and TR-01 ONAF2 1,745 A output.',
          '2. Enforce mechanical/Kirk-Key interlock with 52-LV so zero-current opening holds.'
        ]
      },
      cb_lv: {
        title: '13.8 kV Main Vacuum Breaker (52-LV) Sizing',
        dutyNormal: '2,000 A Continuous (> 1,745 A TR-01 ONAF2)',
        dutyFault: '31.5 kA Symmetrical Interrupting (> 18.36 kA Bus Fault, +71% margin)',
        steps: [
          '1. Standard IEEE C37.06 Frame: 15 kV, 110 kV BIL, 2,000 A, 31.5 kA 3-cycle Vacuum.',
          '2. Coordination Interval: Delayed 0.25 s above 52-F1/F2 instantaneous/inverse curves for full bus selectivity.'
        ]
      },
      sst_100: {
        title: '100 kVA Station Service Transformer (SST-100) Sizing',
        dutyNormal: 'TR-01 Fans (18 kW) + HVAC (15 kW) + DC Chargers (12 kW) + Lights (10 kW) = 55 kW (64 kVA)',
        dutyFault: '13.8 kV Primary 10E Expulsion Fuse clears 480V bolted fault (~3.7 kA) inside 0.04 s',
        steps: [
          '1. Load Diversification: 64 kVA connected demand -> 100 kVA standard frame leaves +56% station growth margin.',
          '2. Dual Feed Consideration: Backed by 125 VDC 200 Ah station battery for 8-hour blackout ride-through.'
        ]
      },
      cap_bank: {
        title: '3.6 MVAR Shunt Capacitor Bank Sizing',
        dutyNormal: 'I_cap = 3,600 kVAR / (sqrt(3) * 13.8 kV) = 150.6 A nominal (x 1.35 IEEE 18 = 203 A switch)',
        dutyFault: 'PF lifts from 0.88 lag to 0.96 lag -> cuts feeder I^2*R losses by ~16% & raises V_bus +2.1%',
        steps: [
          '1. Reactive Requirement: delta_Q = 35 MW * (tan(acos 0.88) - tan(acos 0.96)) = 8.6 MVAR -> 3.6 MVAR first switched step.',
          '2. Voltage Rise Check: delta_V % = (Q_MVAR * Z_tx %) / S_tx = (3.6 * 9.5) / 41.7 = +0.82% across TR-01 (+ feeder drop).'
        ]
      },
      cb_f1: {
        title: 'Feeder 01 Vacuum Breaker (52-F1) Sizing',
        dutyNormal: 'Normal Split Load ~920 A (22.0 MVA) -> 1,200 A Vacuum Breaker',
        dutyFault: '25 kA Symmetrical Interrupting (> 18.36 kA Head-End Bus Fault)',
        steps: [
          '1. Emergency N-1 Tie Duty: Can carry combined F1 + Sub-Zone transfer up to 1,200 A (28.7 MVA).',
          '2. ANSI 79 Reclosing: Coordinates downstream with 79-ACR1 using 0.25 s CTI zone delay.'
        ]
      },
      cb_f2: {
        title: 'Feeder 02 Vacuum Breaker (52-F2) Sizing',
        dutyNormal: 'Normal Split Load ~824 A (19.7 MVA) -> 1,200 A Vacuum Breaker',
        dutyFault: '25 kA Symmetrical Interrupting (> 18.36 kA Head-End Bus Fault)',
        steps: [
          '1. Sized identically to 52-F1 (15 kV, 1,200 A, 25 kA) for spares interchangeability.',
          '2. Cold-load pickup delay prevents false tripping after 30-min blackout.'
        ]
      },
      dist_recloser: {
        title: 'Line Recloser (79-ACR1) Fuse-Saving Coordination Sizing',
        dutyNormal: 'Load through Pole 1 ~410 A -> 560 A 15.5 kV Vacuum Recloser',
        dutyFault: '12.5 kA Sym. Rating >> 6.2 kA Pole-1 Fault -> 2x Fast (Curve A) < 100K Min Melt',
        steps: [
          '1. Fault Current Drop Along 477 ACSR: Line impedance limits Pole-1 3φ fault to 6.2 kA (vs 18.4 kA at bus).',
          '2. Fuse-Saving Window (IEEE C37.48): At 3.0 kA lateral fault, 79-ACR1 Curve A (0.04 s) beats 100K Fuse Min-Melt (0.11 s), saving ~80% transient outages!',
          '3. Permanent Fault Transfer: Curve B/C Slow shots (0.38 s) wait AFTER 100K Fuse Total Clear (0.24 s) so permanent lateral faults blow only the fuse.'
        ]
      },
      dist_sectionalizer: {
        title: 'Line Sectionalizer (34-SECT) Count & Reach Sizing',
        dutyNormal: 'Downstream Trunk Load ~280 A -> 400 A Frame, 0 A Fault Interrupting',
        dutyFault: 'Armed I_pickup = 160 A -> Opens strictly during Recloser Dead-Time #2 (t = 0 A)',
        steps: [
          '1. Selectivity Rule: Count setting = 2 fault-zero openings < 79-ACR1 4-shot lockout (leaves upstream intact!).',
          '2. Zero-CTI Advantage: Unlike overcurrent relays, sectionalizers do not need 0.3 s vertical time gaps on congested TCC plots.'
        ]
      },
      dist_fuse_cutout: {
        title: '100K Lateral Expulsion Fuse Cutout Sizing',
        dutyNormal: 'Lateral Commercial/Tap Peak = 65 A -> 100K Tin Link (1.5x thermal margin)',
        dutyFault: '10 kA Asymmetrical Rating >> 3.8 kA Lateral Tap Fault',
        steps: [
          '1. Speed Selection (K-Type Fast Melt): K-link speed factor (~6-8) allows steep clearing curves between Recloser Curve A and Curve B.',
          '2. Minimum-Melt vs Total-Clear Band: Checked cleanly against 79-ACR1 Curve A * 0.75 pre-load margin and Curve B.'
        ]
      },
      dist_arrester: {
        title: 'Distribution Line MOV Arrester (10 kV / 8.4 kV MCOV) Sizing',
        dutyNormal: 'V_LG = 7.97 kV * 1.05 = 8.37 kV -> 8.4 kV MCOV (10 kV Duty Cycle)',
        dutyFault: 'Discharge V_10kA = 31 kV Peak << 95-110 kV BIL Crossarm Insulation',
        steps: [
          '1. Match effectively-grounded 13.8Y/7.97 kV neutral system factor (1.25 TOV factor).',
          '2. Direct mount within 0.3 m of transformer/recloser bushings limits surge reflection doubling.'
        ]
      },
      substation_b: {
        title: 'Substation B & FLISR Automated Tie (79-TIE) Sizing',
        dutyNormal: 'Normally Open (0 A Transfer); Closes up to 630 A (15 MVA) on N-1 Back-Feed',
        dutyFault: 'FLISR Restoration Window < 4.2 s (Isolates faulted zone, restores 100% healthy Commercial/Industrial load)',
        steps: [
          '1. Thermal Reserve: Substation B carries ~58% nominal load, leaving 17 MVA reserve capacity to pick up Feeder 01 Commercial & Industrial zones.',
          '2. Sync & Cold-Load Check: ANSI 25 confirms dead-bus or ΔV < 5% / Δθ < 15° before 79-TIE closes automatically.'
        ]
      },
      dt_res_50: {
        title: '50 kVA Single-Phase Pole-Mounted Distribution Transformer Sizing & Protection',
        standard: 'IEEE C57.12.20 / ANSI C37.41 / NESC Rule 232',
        inputs: '16 Residential Homes · Connected Load: 8.5 kW/home · DF: 0.48 · PF: 0.92 lag · V₁: 7.967 kV (L-N) · V₂: 240/120 V · Z = 1.9%',
        steps: [
          '1. Diversified kVA Demand: S_div = (16 × 8.5 kW × 0.48) / 0.92 = 70.96 kVA ÷ Coincidence Factor (1.58) ≈ 44.9 kVA → Select next standard rating: 50 kVA.',
          '2. Primary & Secondary Rated Currents: I₁ = 50,000 / 7,967 = 6.28 A; I₂ = 50,000 / 240 = 208.3 A (load utilization = 44.9 / 50 = 89.8%).',
          '3. Primary Fuse Cutout Selection: 1.5 × I₁ = 9.42 A → Select 10K (or 12K cold-load) Type K expulsion link inside 15 kV, 100 A ANSI C37.41 cutout.',
          '4. Lightning Protection & Grounding: 10 kV MOV Arrester (MCOV 8.4 kV) bonded to #4 Cu lead & 5/8" × 8 ft ground rod (R_g ≤ 25 Ω). Full-load %VD ≈ 1.85%.'
        ]
      },
      dt_com_750: {
        title: '750 kVA 3-Phase Pad-Mounted Transformer & Fuse Coordination',
        standard: 'IEEE C57.12.34 / NEC Art. 450 / ANSI C37.47',
        inputs: 'Commercial Plaza · Diversified Peak: 625 kVA (83.3% load) · PF: 0.90 lag · V₁: 13.8 kV (Δ) · V₂: 480Y/277 V · Z = 5.25%',
        steps: [
          '1. Standard Pad-Mount Selection: Peak 625 kVA × 1.15 growth margin = 718.8 kVA → Select 750 kVA, ONAN 65°C rise, Dyn11 dead-front padmount.',
          '2. Rated Line Currents: I₁ = 750 / (√3 × 13.8) = 31.38 A; I₂ = 750 / (√3 × 0.48) = 902.1 A.',
          '3. Overcurrent Protection (NEC 450.3): Bay-O-Net Dual-Sensing + ELSP current-limiting fuse at 1.4 × I₁ = 43.9 A → 45 A / 50E fuse; Secondary Main = 1,200 A frame AT (1,000 A trip).',
          '4. Available Symmetrical Fault Current: I_sc2 ≈ I₂ / Z_pu = 902.1 / 0.0525 = 17.18 kA sym (requires ≥25 kAIC commercial switchboard).'
        ]
      },
      dt_ind_1500: {
        title: 'Dedicated 69 / 138 kV Customer Industrial Substation (25 MVA · 52-CUST)',
        standard: 'IEEE C57.12.10 / IEEE 141 (Red Book) / IEEE C37.113',
        inputs: 'Steel Mill & Arc-Furnace Complex · 22.4 MVA Peak · V₁: 69 or 138 kV Dedicated Sub-Transmission → V₂: 4.16 kV / 13.8 kV Plant Switchgear · Z = 8.5%',
        steps: [
          '1. Dedicated Sub-Transmission Feed (52-IND): Heavy Industrial flicker/arc-furnace surges are segregated onto 69 kV (Tiers 1–2) or 138 kV (Tiers 3–4) so 13.8 kV city residential/hospital voltage remains strictly <= 0.5% flicker.',
          '2. Line Currents @ 25 MVA: At 69 kV: I_HV = 25,000 / (√3 × 69) = 209.2 A; At 138 kV: I_HV = 104.6 A; Plant 4.16 kV bus: I_LV = 3,470 A.',
          '3. Customer Protection (52-CUST & 87T): 69/138 kV SF6 breaker + percentage differential 87T + 51-CUST pickup = 260 A (69 kV eq), CTI >= 0.35 s below utility 52-IND.',
          '4. Short-Circuit Withstand: Plant 4.16 kV symmetrical fault = 3,470 / 0.085 = 40.8 kA -> Specify 50 kAIC metal-clad vacuum switchgear.'
        ]
      },
      ind_hv_bay: {
        title: '52-IND Sub-Transmission Industrial Bay Sizing (69 / 138 kV)',
        standard: 'IEEE C37.04 / IEEE Std 1427 / IEC 62271-100',
        inputs: 'Dedicated Customer Tap off 69 or 138 kV Substation A Bus · 25 MVA Contract Demand · #477 kcmil ACSR "Hawk" Line',
        steps: [
          '1. Continuous Rating: I_load = 209.2 A (@ 69 kV) -> #477 ACSR rated 670 A provides >3.2x ampacity margin; bay breaker 52-IND rated 1,200 A / 31.5–40 kA.',
          '2. Line Distance Relay (21-IND): Zone 1 = 80% of North ROW line impedance (instantaneous), Zone 2 = 120% overlapping 52-CUST primary winding.',
          '3. Overcurrent Backup (51-IND): Pickup = 320 A @ 69 kV eq, IEEE Very Inverse, TDS 2.6, selectively coordinated >= 0.35 s above customer 52-CUST.'
        ]
      },
      dt_uni_500: {
        title: '500 kVA East Campus & Residential Pad-Mount (Sub B · 52-F3)',
        standard: 'IEEE C57.12.34 / IEEE 1547 / NEC Art. 450',
        inputs: 'University Hall + Library + Apartments · 410 kVA Diversified · V₁: 13.8 kV (52-F3) -> V₂: 208Y/120 V · Z = 4.9%',
        steps: [
          '1. Ampacity Selection: I₁ = 20.9 A @ 13.8 kV; I₂ = 1,388 A @ 208 V -> 500 kVA padmount runs at 82% load with roof PV shaving ~65 kVA midday.',
          '2. Protection & Tie Transfer: Bay-O-Net 30 A dual-sensing + 40E ELSP fuse; Loop 1 FLISR closes 79-TIE1 if Sub B F3 loses source.'
        ]
      },
      dt_mun_1000: {
        title: '1,000 kVA Municipal Water & Logistics Station (Sub B · 52-F4)',
        standard: 'IEEE C57.12.34 / NFPA 20 / IEEE 519 Harmonics',
        inputs: 'Booster Pumps (4×175 HP VFD) + Logistics Hub · 820 kVA · V₁: 13.8 kV (52-F4) -> V₂: 480Y/277 V · Z = 5.5%',
        steps: [
          '1. Primary & Secondary Currents: I₁ = 41.8 A @ 13.8 kV; I₂ = 1,203 A @ 480 V (I_sc2 = 21.9 kA sym).',
          '2. Critical Water Pumping Transfer: Loop 2 tie 89-TIE2 restores municipal pumping cleanly from Sub A 52-F2 under N-1 contingency.'
        ]
      },
      substation_gate: {
        title: '3.0 m Precast Concrete Perimeter Security Wall & NERC CIP Checks',
        standard: 'NERC CIP-014 / NESC Rule 110.A1 / IEEE Std 80',
        inputs: '3.0 m Precast Concrete Panels + 0.55 m 45° Razor/Barb Arms · Yard Ground Grid Rg < 1.0 Ohm',
        steps: [
          '1. Height Verification: 3.0 m concrete + 0.55 m angled barbed/razor arms = 3.55 m (11.6 ft) >> 2.13 m (7 ft) NESC Rule 110 minimum.',
          '2. Step & Touch Bonding: Hinged steel gates bonded via 4/0 Cu braids to 1.0 m setback ground loop (<50 V touch under 19.8 kA SLG).'
        ]
      },
      city_gate: {
        title: '140 m Buffer Setback & Urban Entrance Portal Clearances',
        standard: 'NESC C2 Rule 232 / OSHA 1910.303 Utility ROW',
        inputs: 'West ROW Buffer = 140.0 m | East ROW Buffer = 140.0 m | Boulevard Archway Clear Height = 6.8 m',
        steps: [
          '1. Safety Buffer Corridor: Keeping both substations 140.0 m clear of public buildings eliminates blast-radius, EM field, and acoustic transformer noise complaints.',
          '2. Vertical Truck Envelope: 6.8 m steel portal clears legal 4.15 m tractor-trailers and line bucket trucks with 2.65 m safety margin.'
        ]
      },
      dist_pole_p1: {
        title: 'Pole P1 — Feeder Takeoff & Tangent Overhead Design',
        standard: 'NESC Rule 232 / Rule 250B / ANSI O5.1',
        inputs: '40 ft Class 3 Pole · 3× #2/0 ACSR Quail + #1/0 Neutral · Span: 55 m · Conductor Tension: 4.8 kN · w = 2.71 N/m',
        steps: [
          '1. Embedment Depth Rule of Thumb: D = 0.10 × L + 2.0 ft = 0.10(40) + 2.0 = 6.0 ft (1.83 m); above-grade height = 34.0 ft (10.36 m).',
          '2. Midspan Sag & Roadway Clearance: S = w·L² / (8·T) = (2.71 × 55²) / (8 × 4,800) = 0.214 m (0.70 ft); Minimum phase height = 9.45 m − 0.21 m = 9.24 m >> 5.64 m NESC 18.5 ft highway limit.',
          '3. Double Crossarm Bending Check: Horizontal pin spacing = 0.90 m (35.4 in) ≥ 30 in minimum for 13.8 kV.',
          '4. Pole Grounding Electrode: Continuous #4 Cu riser stapled under PVC molding bonded to 5/8" × 8 ft butt ground (R_g ≤ 25 Ω).'
        ]
      },
      dist_pole_p2: {
        title: 'Pole P2 — Residential 50 kVA Transformer Tap & Down-Guy Statics',
        standard: 'NESC Rule 250 / Rule 261C / RUS 1728F-803',
        inputs: '40 ft Class 3 Pole · Equipment Weight: 335 kg · Tap Pull: 5.0 kN at 9.1 m height · Anchor Lead: 4.2 m',
        steps: [
          '1. Vertical Buckling Load: W_equip = 335 kg × 9.81 = 3.29 kN vertical cantilever + ice/wind moment comfortably within Class 3 13.3 kN horizontal rating.',
          '2. Down-Guy Angle & Tension: θ_guy = arctan(4.2 / 9.1) = 24.8° from pole axis; T_guy = T_tap / sin(24.8°) = 5.0 / 0.419 = 11.93 kN.',
          '3. Guy Strand Factor of Safety: 3/8" EHS 7-strand galvanized steel UTS = 68.5 kN → SF = 68.5 / 11.93 = 5.74 (passes NESC Grade B SF ≥ 2.0).',
          '4. Cutout & Arrester Separation: Primary riser tap cleared ≥0.45 m above X₁/X₂ secondary spool rack.'
        ]
      },
      dist_pole_p3: {
        title: 'Pole P3 — Commercial Pad-Mount Underground Riser Dip Pole',
        standard: 'NESC Rule 239 / IEEE 404 (15 kV Terminations)',
        inputs: '40 ft Class 3 Dead-End Pole · 3× 1/C #1/0 Cu 15 kV EPR-JCN Cable in 4" RGS Riser · Bend Radius ≥ 12×OD',
        steps: [
          '1. Dead-End Bell Tension: Full line tension (~3 × 4.8 kN = 14.4 kN) transferred via double crossarm & polymer dead-end insulators.',
          '2. Riser Arrester Protection: 10 kV riser-pole MOV arresters mounted immediately above heat-shrink potheads to protect underground cable from traveling-wave doubling.',
          '3. Conduit Mechanical Protection: Galvanized rigid steel (RGS) U-guard & schedule-80 sweep elbow extend ≥2.5 m (8 ft) above grade.',
          '4. Guying Balance: Opposing 3/8" EHS down-guy anchored 4.4 m back into Grade-A helical screw anchor.'
        ]
      },
      dist_pole_p4: {
        title: 'Pole P4 — Industrial Corner & 79-TIE Span Termination',
        standard: 'NESC Grade B Heavy Loading / IEEE 1366 FLISR',
        inputs: '40 ft Class 3 Double-Arm Corner Pole · Span to 79-TIE: 52 m · Faulted Line Sectionalizing Boundary',
        steps: [
          '1. Dead-End Strain Assembly: Double crossarms carry back-to-back dead-end strain bells separating the Feeder 01 main trunk from Industrial Tap & Normally Open 79-TIE.',
          '2. Longitudinal Balancing: Corner resultant pull neutralized by 3/8" EHS guy strand + 8 ft high-visibility yellow guy guard.',
          '3. FLISR Sectionalizing Clearance: Phase spacing opened to 1.00 m on outer arm ends for hot-line bucket truck / live-line work clearance.',
          '4. NESC Vertical Clearance: Lowest neutral spool maintained ≥7.2 m above industrial entrance road grade.'
        ]
      },
      substation_gate: {
        title: 'Substation Perimeter Vehicular Gate, Guardhouse & Touch-Potential Bonding',
        standard: 'NESC Rule 110A / IEEE Std 80 Section 16.5 / ANSI Z535',
        inputs: '7.2 m Double-Leaf Swing Gate + 1.1 m Man-Gate · Fabric: 7 ft (2.13 m) Chain Link + 1 ft Barbed Wire · Ground Grid Tie',
        steps: [
          '1. NESC Rule 110A Fence Height Check: 2.13 m (7.0 ft) chain-link fabric + 0.35 m (1.15 ft) 45° 3-strand barbed outrigger = 2.48 m (8.1 ft) ≥ 7.0 ft minimum requirement.',
          '2. Vehicular Access Clearance: Twin 3.6 m leaves open to full 7.2 m clear width — accommodates 100+ MVA lowboy transformer trailers and 55 ft utility bucket trucks.',
          '3. IEEE 80 Flexible Hinge Grounding: Each gate leaf is bonded across its pintle hinges by ≥#2 AWG (or 2/0 equiv.) tinned flexible copper braid to the fence post ground grid riser, keeping gate touch potential V_touch < V_tolerable.',
          '4. Apron & Crushed Stone Transition: 100 mm high-resistivity (3,000 Ω·m) clean crushed granite layer extends ≥1.0 m beyond the fence perimeter at pedestrian zones.'
        ]
      },
      urd_riser_pole: {
        title: 'URD Transition (Dip / Riser) Pole Travel-Wave & Conduit Design',
        standard: 'IEEE Std 48 / IEEE C62.11 / NESC Rule 239',
        inputs: '13.8 kV URD Lateral · 3× #1/0 Al 15 kV 100% TR-XLPE Concentric Neutral · Z₀_oh = 400 Ω, Z₀_ug = 38 Ω',
        steps: [
          '1. Traveling-Wave Doubling at Open Loop Tie: Lightning impulse entering cable sees Z₀_ug = 38 Ω; at normally-open H1B elbow end reflection coeff Γ = +1.0 doubles surge crest.',
          '2. Riser Arrester Discharge Voltage: 10 kV Heavy-Duty Riser Arrester (8.4 kV MCOV) holds 28.5 kV @ 10 kA; doubled crest = 57.0 kV << 95 kV BIL (40% insulation margin).',
          '3. Ampacity & Conduit Fill: 3× #1/0 Al (1.06" OD) inside 4" Schedule 80 RGS riser = 21.8% fill < 40% NEC Ch.9 limit with 24" minimum sweep radius.',
          '4. Primary Lateral Fusing: 65T / 80K cutout coordinated below 79-ACR1 slow curve.'
        ]
      },
      dt_urd_pad: {
        title: '150 kVA Dead-Front Loop-Feed URD Pad-Mounted Transformer & Bay-O-Net Check',
        standard: 'IEEE C57.12.26 / IEEE 386 / NEC Art. 450',
        inputs: '24 URD Subdivision Homes · 12 kW/home × 0.42 DF ÷ 0.90 PF = 134.4 kVA · V₁ = 7.97 kV L-N / 13.8 kV · V₂ = 240/120 V',
        steps: [
          '1. Standard Dead-Front Rating: Peak diversified load 134.4 kVA / 150 kVA = 89.6% loading (65°C FR3 fluid rise compliant).',
          '2. Primary & Loop-Feed Loadbreak Rating: I₁ = 150,000 / 7,967 = 18.8 A (1φ equiv.) or 6.28 A/φ << 200 A IEEE 386 elbow continuous & loop switching rating.',
          '3. Dual-Element Protection: 25 A Bay-O-Net Dual-Sensing expulsion fuse backed up by 40 A partial-range current-limiting ELSP fuse.',
          '4. Underground Service Drop Drop: #4/0 Al USE-2 sweetbriar triplex in 2" HDPE duct to URD street pedestals yields ΔV = 1.92% < 3% utility service limit.'
        ]
      },
      urd_vista_swgr: {
        title: 'Pad-Mounted SF6 / Solid-Dielectric Vista Switchgear Sectionalizing & Loop Check',
        standard: 'IEEE C37.74 / IEEE 386 (600 A T-Body + 200 A VFI)',
        inputs: '600 A Main Loop Bus · 2× 200 A Vacuum Fault Interrupter Ways · Isc = 11.4 kA sym',
        steps: [
          '1. 600 A T-Body Main Bus Capacity: Carries up to 14.3 MVA @ 13.8 kV with zero exposed live metal inside vault.',
          '2. Vacuum Fault Interrupter TCC Curve: Electronic trip set to E-Curve Equivalent (Pickup 140 A, Instantaneous 1,200 A) clearing downstream URD cable faults in < 35 ms.',
          '3. Visible Break Verification: Illuminated viewing window confirms Open-Closed-Ground switch blade status before applying grounded test leads.'
        ]
      }
    };

    // Substation Insulation & Enclosure Comparative Engineering Matrix
    const ENCLOSURE_COMPARISON = [
      { metric: '69 kV Phase-to-Phase Clearance', ais: '2.40 m (Air-Insulated)', gis: '0.28 m (SF6 @ 450 kPa)', indoor: '0.45 m (Solid/Air Bus Duct)' },
      { metric: 'Total Switchyard Footprint (Single Bus)', ais: '100% (~1,540 m^2)', gis: '~28% (~430 m^2 Indoor Hall)', indoor: '~52% (~800 m^2 Split Building)' },
      { metric: 'Typical Installed Capital Cost (CAPEX)', ais: '1.0x Baseline (Lowest)', gis: '2.1x - 2.6x Higher', indoor: '1.45x - 1.75x Moderate' },
      { metric: 'Maintenance Cycle & Environmental Immunity', ais: 'Every 1-2 yrs; exposed to salt, birds, lightning', gis: 'Every 10-15 yrs; hermetically sealed immune to salt/typhoons', indoor: 'Every 3-5 yrs; walk-in draw-out VCB trucks inside HVAC room' },
      { metric: 'Arc-Flash / Public Safety Profile', ais: 'Open yard standoff distance', gis: 'Grounded aluminum enclosures (low external hazard)', indoor: 'IEEE C37.20.7 Arc-Resistant plenum vents to roof' },
      { metric: 'Best Philippine / Utility Application', ais: 'Rural / Provincial 69 kV transmission taps', gis: 'Dense Metro Manila / Coastal Industrial Cities', indoor: 'Commercial High-Rise / Hospital Primary Vaults' }
    ];

    // Interactive Breaker Maintenance Switching & Interlock Scenarios
    const MAINTENANCE_DRILLS = {
      A: {
        title: 'Scenario A: Single Bus 52-69 Maintenance (Planned Outage)',
        desc: 'In Single Bus topology there is NO bypass path. Taking 52-69 out of service drops TR-01 and the 13.8 kV yard.',
        steps: [
          { target: 'cbMain', action: false, label: '1. Open Main Breaker 52-69 (extinguish 348 A under SF6)' },
          { target: 'dsMain', action: false, label: '2. Open Isolator 89-69 (strictly under zero current!)' },
          { target: 'earthMain', action: true, label: '3. Close Earthing Switch 89E (drain trapped charge to ground)' }
        ]
      },
      B: {
        title: 'Scenario B: Main & Transfer Bus Live Bypass (Zero Outage)',
        desc: 'Transfer TR-01 load smoothly onto the Transfer Breaker (52-BT) before isolating Main Breaker 52-69 with ZERO customer interruption!',
        steps: [
          { target: 'dsBT', action: true, label: '1. Verify 89-BT Isolators Closed on Transfer Bus' },
          { target: 'cbBT', action: true, label: '2. Close Transfer Breaker 52-BT to energize Transfer Bus' },
          { target: 'dsBYP', action: true, label: '3. Close Bypass Switch 89-BYP (parallels 52-69 & 52-BT safely!)' },
          { target: 'cbMain', action: false, label: '4. Open Main Breaker 52-69 (load shifts seamlessly to 52-BT!)' },
          { target: 'dsMain', action: false, label: '5. Open Main Isolator 89-69 (52-69 isolated while TR-01 stays 100% live!)' }
        ]
      },
      C: {
        title: 'Scenario C: Ring Bus 4-Corner Loop Isolation (Zero Outage)',
        desc: 'In a closed 4-breaker Ring Bus (52-1..52-4), opening ANY one ring breaker leaves every corner line and TR-01 continuously fed via the alternate ring leg!',
        steps: [
          { target: 'cb1', action: false, label: '1. Open Ring Breaker 52-1 (West Leg opens; East/South ring path keeps Line 1 & TR-01 100% live!)' },
          { target: 'ds1A', action: false, label: '2. Open Corner Disconnect 89-1A (Zero-load interlock verified)' },
          { target: 'ds1B', action: false, label: '3. Open Corner Disconnect 89-1B (52-1 fully isolated inside live 4-breaker ring!)' }
        ]
      },
      D: {
        title: 'Scenario D: Breaker-and-a-Half (1½ CB) Bay Isolation (Zero Outage)',
        desc: 'Dual parallel Main Bus A & Main Bus B feed TR-01 and Line 1 through 3 breakers (52-A, 52-TIE, 52-B). Isolating Bus-A Breaker 52-A shifts feed through Main Bus B & 52-TIE seamlessly!',
        steps: [
          { target: 'cbA', action: false, label: '1. Open Bus-A Breaker 52-A (Power flows via Main Bus B → 52-B → Ckt 2 & 52-TIE → Ckt 1!)' },
          { target: 'dsA1', action: false, label: '2. Open Flanking Isolator 89-A1 (Zero-current interlock verified)' },
          { target: 'dsA2', action: false, label: '3. Open Flanking Isolator 89-A2 (52-A completely isolated while Bus A & Bus B both stay live!)' }
        ]
      },
      E: {
        title: 'Scenario E: Double Bus–Double Breaker (2.0 CB) Live Breaker & Bus Isolation',
        desc: 'Each circuit has 2 dedicated parallel breakers connected to Main Bus A and Main Bus B. Isolating 52-1A (or Bus A entirely) keeps 100% load flowing seamlessly through 52-1B & Bus B with ZERO switching transfers and ZERO outage!',
        steps: [
          { target: 'cb1A', action: false, label: '1. Open Bus-A Line Breaker 52-1A (100% power routes via Bus B & parallel 52-1B with ZERO outage!)' },
          { target: 'ds1A1', action: false, label: '2. Open Bus-A Side Disconnect 89-1A1 (Zero-current interlock verified)' },
          { target: 'ds1A2', action: false, label: '3. Open Circuit-Side Disconnect 89-1A2 (52-1A fully isolated while TR-01 & Bus B carry 100% load!)' }
        ]
      }
    };

    // Multi-Voltage Substation Class Specifications (IEEE Std 1427 / IEEE C2 / PEC Part 2 Scaling)
    const VOLTAGE_CLASSES = {
      '69_13': {
        id: '69_13',
        shortLabel: '69 / 13.8 kV',
        cascadeLabel: '69 → 13.8 kV',
        stageKvs: [69.0, 13.8],
        distKv: 13.8,
        indSubKv: 69.0,
        indCustMva: 25.0,
        tierName: 'Distribution Substation (1-Stage Step-Down)',
        hvKv: 69.0,
        lvKv: 13.8,
        mva: 41.7,
        stages: [
          { name: 'TR-01', hv: 69.0, lv: 13.8, mva: 41.7, vector: 'Dyn11', xPu: 0.105 }
        ],
        totalCascadeXPu: 0.105,
        bilHv: '350 kV',
        bilLv: '110 kV',
        phaseSpacing: 2.4,
        minPhaseClearance: 1.8,
        bayPhaseZ: 3.5,
        insScale: 1.0,
        shedsCount: 9,
        hvShedsCount: 14,
        mad: 2.2,
        coronaRings: false,
        twinBundle: false,
        hvCbKa: 31.5,
        lvCbKa: 25.0,
        rPu: 0.0085,
        xPu: 0.105,
        pCoreKw: 38.0,
        pCuFullKw: 185.0,
        z1SysPu: 0.035,
        z0SysPu: 0.042,
        z0TxPu: 0.095,
        ngrOhms: 10.0,
        capMvar: 3.6,
        vectorGroup: 'Dyn11',
        arcClearingSec: 0.08
      },
      '138_69': {
        id: '138_69',
        shortLabel: '138 → 69 → 13.8 kV',
        cascadeLabel: '138 → 69 → 13.8 kV',
        stageKvs: [138.0, 69.0, 13.8],
        distKv: 13.8,
        indSubKv: 69.0,
        indCustMva: 25.0,
        tierName: 'Sub-Transmission Cascade (2-Stage: 138→69→13.8 kV)',
        hvKv: 138.0,
        lvKv: 69.0,
        mva: 100.0,
        stages: [
          { name: 'ATR-138', hv: 138.0, lv: 69.0, mva: 100.0, vector: 'YNa0d1', xPu: 0.115 },
          { name: 'TR-01', hv: 69.0, lv: 13.8, mva: 41.7, vector: 'Dyn11', xPu: 0.105 }
        ],
        totalCascadeXPu: 0.153,
        bilHv: '650 kV',
        bilLv: '350 kV',
        phaseSpacing: 3.2,
        minPhaseClearance: 3.2,
        bayPhaseZ: 4.2,
        insScale: 1.65,
        shedsCount: 15,
        hvShedsCount: 18,
        mad: 3.4,
        coronaRings: true,
        twinBundle: false,
        hvCbKa: 40.0,
        lvCbKa: 31.5,
        rPu: 0.0062,
        xPu: 0.115,
        pCoreKw: 72.0,
        pCuFullKw: 385.0,
        z1SysPu: 0.028,
        z0SysPu: 0.036,
        z0TxPu: 0.102,
        ngrOhms: 20.0,
        capMvar: 12.0,
        vectorGroup: 'YNa0d1',
        arcClearingSec: 0.065
      },
      '230_138': {
        id: '230_138',
        shortLabel: '230 → 138 → 69 → 13.8 kV',
        cascadeLabel: '230 → 138 → 69 → 13.8 kV',
        stageKvs: [230.0, 138.0, 69.0, 13.8],
        distKv: 13.8,
        indSubKv: 138.0,
        indCustMva: 30.0,
        tierName: 'EHV Bulk Transmission Cascade (3-Stage: 230→138→69→13.8 kV)',
        hvKv: 230.0,
        lvKv: 138.0,
        mva: 300.0,
        stages: [
          { name: 'ATR-230', hv: 230.0, lv: 138.0, mva: 300.0, vector: 'YNa0d1', xPu: 0.125 },
          { name: 'ATR-138', hv: 138.0, lv: 69.0, mva: 100.0, vector: 'YNa0d1', xPu: 0.115 },
          { name: 'TR-01', hv: 69.0, lv: 13.8, mva: 41.7, vector: 'Dyn11', xPu: 0.105 }
        ],
        totalCascadeXPu: 0.170,
        bilHv: '1050 kV',
        bilLv: '650 kV',
        phaseSpacing: 4.8,
        minPhaseClearance: 4.8,
        bayPhaseZ: 5.4,
        insScale: 2.35,
        shedsCount: 24,
        hvShedsCount: 26,
        mad: 4.6,
        coronaRings: true,
        twinBundle: true,
        quadBundle: false,
        hvCbKa: 50.0,
        lvCbKa: 40.0,
        rPu: 0.0045,
        xPu: 0.125,
        pCoreKw: 145.0,
        pCuFullKw: 820.0,
        z1SysPu: 0.022,
        z0SysPu: 0.030,
        z0TxPu: 0.110,
        ngrOhms: 40.0,
        capMvar: 30.0,
        vectorGroup: 'YNa0d1 (Autotransformer)',
        arcClearingSec: 0.05
      },
      '500_230': {
        id: '500_230',
        shortLabel: '500 → 230 → 138 → 69 → 13.8 kV',
        cascadeLabel: '500 → 230 → 138 → 69 → 13.8 kV',
        stageKvs: [500.0, 230.0, 138.0, 69.0, 13.8],
        distKv: 13.8,
        indSubKv: 138.0,
        indCustMva: 30.0,
        tierName: 'EHV Bulk Grid Cascade (4-Stage: 500→230→138→69→13.8 kV)',
        hvKv: 500.0,
        lvKv: 230.0,
        mva: 1000.0,
        stages: [
          { name: 'ATR-500', hv: 500.0, lv: 230.0, mva: 1000.0, vector: 'YNa0d11', xPu: 0.138 },
          { name: 'ATR-230', hv: 230.0, lv: 138.0, mva: 300.0, vector: 'YNa0d1', xPu: 0.125 },
          { name: 'ATR-138', hv: 138.0, lv: 69.0, mva: 100.0, vector: 'YNa0d1', xPu: 0.115 },
          { name: 'TR-01', hv: 69.0, lv: 13.8, mva: 41.7, vector: 'Dyn11', xPu: 0.105 }
        ],
        totalCascadeXPu: 0.176,
        bilHv: '1800 kV',
        bilLv: '1050 kV',
        phaseSpacing: 8.2,
        minPhaseClearance: 4.8,
        bayPhaseZ: 8.6,
        insScale: 3.45,
        shedsCount: 36,
        hvShedsCount: 38,
        mad: 8.2,
        coronaRings: true,
        twinBundle: true,
        quadBundle: true,
        autoTxBank: true,
        liveTankMultiChamber: true,
        hvCbKa: 63.0,
        lvCbKa: 50.0,
        rPu: 0.0028,
        xPu: 0.138,
        pCoreKw: 310.0,
        pCuFullKw: 1850.0,
        z1SysPu: 0.015,
        z0SysPu: 0.022,
        z0TxPu: 0.115,
        ngrOhms: 60.0,
        capMvar: 90.0,
        vectorGroup: 'YNa0d11 (3×333 MVA 1φ AutoTx Bank)',
        arcClearingSec: 0.033
      }
    };
    """

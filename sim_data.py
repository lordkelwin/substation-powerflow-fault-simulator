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
          { k: 'Housing Material', v: 'Hydrophobic Silicone Rubber Polymer' },
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
          { id: 'la-polymer-sheds', name: 'Hydrophobic Silicone Rubber Weather Sheds', tag: 'POLY-SHEDS', material: 'High-Temperature Vulcanized (HTV) Silicone Rubber', role: 'Prevents moisture and contamination flashover through superior water repellency (hydrophobicity).', vector: [0, 0.5, -1.8] },
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
        ansiCode: 'HTV Silicone Rubber Alternating Weather Sheds',
        fieldSpot: 'Light grey-blue silicone polymer housing molded with alternating large and small horizontal skirts.',
        workingPrinciple: 'Low-molecular-weight silicone chains continuously migrate to the surface, imparting permanent hydrophobicity—rainwater beads up into isolated spheres rather than forming conductive wet films. Eliminates salt-fog external surface flashovers without requiring periodic washing.',
        maintenance: 'Creepage distance ≥ 2,140 mm (31 mm/kV). Checks: Hydrophobicity HC1–HC2 water spray check; inspect for chalking or electrical treeing marks.'
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
      }
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
        tierName: 'Distribution Substation',
        hvKv: 69.0,
        lvKv: 13.8,
        mva: 41.7,
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
        shortLabel: '138 / 69 kV',
        tierName: 'Sub-Transmission Substation',
        hvKv: 138.0,
        lvKv: 69.0,
        mva: 100.0,
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
        shortLabel: '230 / 138 kV',
        tierName: 'EHV Bulk Transmission Substation',
        hvKv: 230.0,
        lvKv: 138.0,
        mva: 300.0,
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
      }
    };
    """

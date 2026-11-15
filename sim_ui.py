"""
sim_ui.py
HTML UI markup for EE 415 3D Substation Simulator.
"""

def get_html_ui():
    return """
  <!-- 3D Canvas -->
  <canvas id="canvas3d"></canvas>

  <!-- Runtime Error Diagnostic Banner -->
  <div id="runtime-error-banner">
    <div style="display: flex; align-items: center; justify-content: space-between;">
      <strong style="font-size: 13.5px; display: flex; align-items: center; gap: 8px;">
        ⚠️ 3D ENGINE / JAVASCRIPT RUNTIME EXCEPTION:
      </strong>
      <button class="btn" style="padding: 2px 8px; font-size: 11px;" onclick="document.getElementById('runtime-error-banner').style.display='none'">Dismiss</button>
    </div>
    <pre id="runtime-error-msg" style="margin-top: 10px; white-space: pre-wrap; font-size: 11px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2);"></pre>
  </div>

  <!-- Floating 3D HTML Callout Pins Container -->
  <div id="callout-container" style="position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:50;"></div>

  <!-- TOP HEADER -->
  <header id="top-bar">
    <div class="brand">
      <div class="brand-badge" title="High-Voltage Power &amp; Distribution Engineering Emblem">
        <svg class="brand-emblem-svg" width="32" height="32" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Electrical Engineering Shield Emblem">
          <polygon points="18,2 32,9 32,25 18,34 4,25 4,9" fill="rgba(2,6,23,0.85)" stroke="#38bdf8" stroke-width="1.6"/>
          <path d="M18 5 L14 27 M18 5 L22 27 M11.5 11.5 H24.5 M12.5 16.5 H23.5" stroke="#94a3b8" stroke-width="1.2" stroke-linecap="round"/>
          <path d="M6 21 C9 15, 12 27, 15 21 C18 15, 21 27, 24 21 C27 15, 29 24, 30 21" stroke="#34d399" stroke-width="1.4" stroke-linecap="round"/>
          <circle cx="13" cy="21" r="3.4" stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.8"/>
          <circle cx="23" cy="21" r="3.4" stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.8"/>
          <polygon points="19.5,6.5 13.5,18.5 18,18.5 16,28.5 23.5,15.5 18.8,15.5" fill="#fbbf24" stroke="#0f172a" stroke-width="0.6"/>
        </svg>
      </div>
      <div class="brand-title" title="Substation and Distribution Simulation — High-Voltage Switchyard, Protection Coordination &amp; Distribution Network Simulator (69 / 13.8 kV, 41.7 MVA Dyn11)">
        <h1>Substation and Distribution Simulation</h1>
        <p id="subtitle-rating" title="High-Voltage Switchyard, Protection Coordination &amp; Distribution Network Simulator | 69 / 13.8 kV, 41.7 MVA Dyn11">High-Voltage Switchyard &amp; Distribution Simulator | 69 / 13.8 kV, 41.7 MVA Dyn11</p>
      </div>
    </div>

    <!-- Compact Grid Status Pill + Telemetry Drawer Trigger -->
    <div class="telem-compact-bar">
      <div class="grid-status-pill" id="telem-compact-pill">
        <div class="dot pulse" id="telem-grid-dot"></div>
        <span id="telem-compact-summary">GRID: <span id="telem-grid-status">ENERGIZED</span> | <span id="telem-compact-kv">69/13.8 kV</span></span>
      </div>
      <button id="btn-telem-drawer" onclick="toggleLiveTelemetryDrawer()" title="Toggle Live System Telemetry & Grid Metrics Dashboard">
        ⚡ System Telemetry &amp; Grid Metrics ▾
      </button>
    </div>

    <div class="header-actions">
      <button class="btn" id="btn-open-analysis" onclick="openAnalysisModal('pf')" style="background: rgba(14, 165, 233, 0.22); border-color: #38bdf8; color: #bae6fd;">
        📊 Power Flow &amp; Fault Lab
      </button>
      <button class="btn" id="btn-open-tcc" onclick="openAnalysisModal('tcc')" style="background: rgba(16, 185, 129, 0.22); border-color: #10b981; color: #a7f3d0;">
        🛡️ Relay &amp; TCC Lab
      </button>
      <button class="btn" id="btn-open-pq" onclick="openAnalysisModal('pq')" style="background: rgba(168, 85, 247, 0.22); border-color: #c084fc; color: #e9d5ff;">
        📈 Power Quality Lab
      </button>
      <button class="btn btn-primary" id="btn-open-challenge" onclick="openChallengeModal()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
        4th-Year Field Challenge
      </button>
      <button class="btn" id="btn-audio-toggle" onclick="toggleAudio()" title="Toggle Switchyard Sound Effects">
        <span id="audio-icon">🔊</span> Audio
      </button>
      <button class="btn" id="btn-help" onclick="openHelpModal()">
        ℹ Help
      </button>
    </div>
  </header>

  <!-- FLOATING LIVE SYSTEM TELEMETRY & GRID METRICS POP-UP DRAWER -->
  <section id="live-telemetry-drawer" aria-label="Live Substation Telemetry Dashboard">
    <div class="telem-drawer-header">
      <div class="telem-drawer-title">
        <span>⚡ Live Substation &amp; Distribution System Telemetry</span>
        <span class="vr-badge" id="telem-vr">VR 0.0%</span>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <button class="btn" onclick="openAnalysisModal('pf')" style="padding:3px 9px; font-size:10px; border-color:#38bdf8; color:#bae6fd;">Open PF Lab</button>
        <button class="btn" onclick="toggleLiveTelemetryDrawer(false)" style="padding:3px 9px; font-size:10px;">✕ Close</button>
      </div>
    </div>
    <div class="telem-drawer-grid">
      <div class="telem-metric-card hv">
        <span class="lbl">Primary HV Bus Voltage</span>
        <span class="val" id="telem-hv-voltage">69.0 kV</span>
        <span class="sub"><span id="telem-hv-pu">(1.00 pu)</span> &bull; IEEE C84.1 Range A</span>
      </div>
      <div class="telem-metric-card lv">
        <span class="lbl">Secondary LV Bus Voltage</span>
        <span class="val" id="telem-lv-voltage">13.80 kV</span>
        <span class="sub"><span id="telem-lv-pu">(1.00 pu)</span> &bull; OLTC Regulated</span>
      </div>
      <div class="telem-metric-card hv">
        <span class="lbl">HV / LV Transformer Currents</span>
        <span class="val" id="telem-current">348.9 / 1744 A</span>
        <span class="sub" id="telem-phase-split">3&phi; Balanced &bull; TR-01 Loading</span>
      </div>
      <div class="telem-metric-card lv">
        <span class="lbl">Feeders F1 / F2 &amp; Tie Current</span>
        <span class="val" id="telem-feeder-currents">F1: 920 A | F2: 824 A</span>
        <span class="sub" id="telem-tie-status">79-TIE (Sub B): OPEN (0 A)</span>
      </div>
      <div class="telem-metric-card pwr">
        <span class="lbl">Apparent Power &amp; PF</span>
        <span class="val" id="telem-power">41.7 MVA | PF 0.92</span>
        <span class="sub" id="telem-mw-mvar">P = 38.4 MW | Q = +16.3 MVAR</span>
      </div>
      <div class="telem-metric-card gnd">
        <span class="lbl">Frequency &amp; Ground Resistance</span>
        <span class="val" id="telem-freq-rg" style="color:#34d399;">60.00 Hz | 0.842 &Omega;</span>
        <span class="sub" id="telem-gpr-live">Live GPR: 18 V (IEEE 80 Safe)</span>
      </div>
      <div class="telem-metric-card pwr">
        <span class="lbl">Civil Substation Footprint</span>
        <span class="val" id="telem-land-area" style="color:#fbbf24;">68&times;48m | 3,264 m&sup2; (0.33 ha)</span>
        <span class="sub" id="telem-footprint-note">Fenced Yard + Outgoing Feeders</span>
      </div>
    </div>
  </section>

  <!-- LEFT DOCK: NAVIGATION, BUSBAR SELECTION, SIMULATION -->
  <aside id="left-dock">
    <!-- Camera & Bay Presets -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 10l5 5-5 5"/><path d="M4 4v7a4 4 0 0 0 4 4h12"/></svg>
          Bay Navigation Presets
        </div>
      </div>
      <div class="preset-grid">
        <button class="btn-preset active" onclick="setCameraPreset('overview')">Yard Overview</button>
        <button class="btn-preset" onclick="setCameraPreset('gantry')">1. Gantry &amp; Lines</button>
        <button class="btn-preset" onclick="setCameraPreset('arrester')">2. Surge Arrester</button>
        <button class="btn-preset" onclick="setCameraPreset('ctvt')">3. CT &amp; VT Bay</button>
        <button class="btn-preset" onclick="setCameraPreset('disconnect')">4. Disconnect (89)</button>
        <button class="btn-preset" onclick="setCameraPreset('breaker')">5. SF6 Breaker (52)</button>
        <button class="btn-preset" onclick="setCameraPreset('transformer')">6. Transformer (TR-1)</button>
        <button class="btn-preset" onclick="setCameraPreset('busbar')">7. Busbar System</button>
        <button class="btn-preset" onclick="setCameraPreset('control')">8. Control House</button>
        <button class="btn-preset" onclick="setCameraPreset('ground')">9. Ground Grid X-Ray</button>
        <button class="btn-preset" onclick="setCameraPreset('secondary')">10. 13.8 kV Secondary</button>
        <button class="btn-preset" onclick="setCameraPreset('feeders')">11. Feeders 01 &amp; 02</button>
        <button class="btn-preset" onclick="setCameraPreset('recloser')">12. Recloser &amp; Sect.</button>
        <button class="btn-preset" onclick="setCameraPreset('cutout_loads')">13. Cutout &amp; Dist. Xfmrs</button>
        <button class="btn-preset" onclick="setCameraPreset('substation_b')">14. Tie &amp; Substation B</button>
      </div>
    </div>

    <!-- Walk vs Orbit Mode -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="7" r="4"/><path d="M5.5 21v-7a6.5 6.5 0 0 1 13 0v7"/></svg>
          Field Walk Mode
        </div>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">1st-Person Field Walk (1.75m)</span>
        <label class="switch">
          <input type="checkbox" id="toggle-walk-mode" onchange="toggleWalkMode(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">Substation A, B &amp; City Gates (Open / [E])</span>
        <label class="switch">
          <input type="checkbox" id="toggle-sub-gates" onchange="toggleSubstationGate('both', this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">Concrete Perimeter Wall Cutaway (Low View)</span>
        <label class="switch">
          <input type="checkbox" id="toggle-wall-cutaway" onchange="togglePerimeterWallCutaway(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">Power Flow Animation</span>
        <label class="switch">
          <input type="checkbox" id="toggle-power-flow" checked onchange="togglePowerFlow(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">Ground Grid X-Ray (IEEE 80)</span>
        <label class="switch">
          <input type="checkbox" id="toggle-ground-xray" onchange="toggleGroundXray(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">Rolling Sphere Canopy (IEEE 998)</span>
        <label class="switch">
          <input type="checkbox" id="toggle-rolling-sphere" onchange="toggleRollingSphere(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">Control House Cutaway Roof</span>
        <label class="switch">
          <input type="checkbox" id="toggle-ctrl-roof" onchange="toggleCtrlHouseRoof(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
      <div class="toggle-row">
        <span class="toggle-label">URD Underground Cables X-Ray</span>
        <label class="switch">
          <input type="checkbox" id="toggle-urd-xray" checked onchange="toggleUrdTrenchXray(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <!-- Substation Voltage Class (kV Scale) Selector -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title" style="color: #38bdf8;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
          Cascading Voltage Step-Down Chain
        </div>
      </div>
      <div class="bus-selector">
        <div class="bus-option selected" id="vclass-opt-69_13" onclick="setVoltageClass('69_13')">
          <span>69 &rarr; 13.8 kV (1-Stage)</span>
          <span class="bus-badge">350 kV BIL</span>
        </div>
        <div class="bus-option" id="vclass-opt-138_69" onclick="setVoltageClass('138_69')">
          <span>138 &rarr; 69 &rarr; 13.8 kV (2-Stg)</span>
          <span class="bus-badge">650 kV BIL</span>
        </div>
        <div class="bus-option" id="vclass-opt-230_138" onclick="setVoltageClass('230_138')">
          <span>230 &rarr; 138 &rarr; 69 &rarr; 13.8 kV</span>
          <span class="bus-badge">1050 kV BIL</span>
        </div>
        <div class="bus-option" id="vclass-opt-500_230" onclick="setVoltageClass('500_230')">
          <span>500&rarr;230&rarr;138&rarr;69&rarr;13.8 kV</span>
          <span class="bus-badge">1800 kV BIL</span>
        </div>
      </div>
      <button class="btn" style="width: 100%; justify-content: center; margin-top: 8px; font-size: 10.5px;" onclick="openVoltageClassModal()">
        📏 Cascading Tiers &amp; Clearances (IEEE 1427)
      </button>
    </div>

    <!-- Target Substation Selector (Independent Customization for Main A vs Tie B) -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title" style="color: #10b981;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="8" height="16" rx="1"/><rect x="14" y="4" width="8" height="16" rx="1"/><path d="M10 12h4"/></svg>
          Target Substation (A vs. Tie B)
        </div>
      </div>
      <div class="substation-target-toggle">
        <button class="btn-sub-target active" id="target-sub-a" onclick="setTargetSubstation('A')">
          <span>● Substation A (Main)</span>
          <small id="sub-a-cfg-summary">Single Bus · AIS</small>
        </button>
        <button class="btn-sub-target" id="target-sub-b" onclick="setTargetSubstation('B')">
          <span>○ Substation B (Tie)</span>
          <small id="sub-b-cfg-summary">Ring Bus · AIS</small>
        </button>
      </div>
    </div>

    <!-- Switchyard Busbar Architecture Selector -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/><line x1="10" y1="3" x2="10" y2="21"/><line x1="16" y1="3" x2="16" y2="21"/></svg>
          Busbar Scheme (Topology)
        </div>
      </div>
      <div class="bus-selector">
        <div class="bus-option selected" id="bus-opt-single" onclick="selectBusTopology('single')">
          <span>Single Bus Scheme</span>
          <span class="bus-badge" id="bus-badge-single">1.0 CB/ckt | 1.00×</span>
        </div>
        <div class="bus-option" id="bus-opt-maintransfer" onclick="selectBusTopology('maintransfer')">
          <span>Main & Transfer Bus</span>
          <span class="bus-badge" id="bus-badge-maintransfer">1.25 CB/ckt | ~1.28×</span>
        </div>
        <div class="bus-option" id="bus-opt-ring" onclick="selectBusTopology('ring')">
          <span>Ring Bus Scheme</span>
          <span class="bus-badge" id="bus-badge-ring">1.0 CB/ckt | ~1.18×</span>
        </div>
        <div class="bus-option" id="bus-opt-breakerhalf" onclick="selectBusTopology('breakerhalf')">
          <span>Breaker-and-a-Half (1½ CB)</span>
          <span class="bus-badge" id="bus-badge-breakerhalf">1.5 CB/ckt | ~1.55×</span>
        </div>
        <div class="bus-option" id="bus-opt-doublebreaker" onclick="selectBusTopology('doublebreaker')">
          <span>Double Bus–Double Breaker (2 CB)</span>
          <span class="bus-badge" id="bus-badge-doublebreaker">2.0 CB/ckt | ~1.75×</span>
        </div>
      </div>
      <div class="land-area-summary-box" id="busbar-land-area-readout"></div>
    </div>

    <!-- Substation Enclosure & Insulation Case Selector -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
          Enclosure & Insulation Case
        </div>
      </div>
      <div class="bus-selector">
        <div class="bus-option selected" id="enc-opt-ais" onclick="setEnclosureType('ais')">
          <span>Outdoor AIS (Air-Insulated)</span>
          <span class="bus-badge" id="enc-badge-ais">100% Yard</span>
        </div>
        <div class="bus-option" id="enc-opt-gis" onclick="setEnclosureType('gis')">
          <span>SF₆ Gas-Insulated (GIS)</span>
          <span class="bus-badge" id="enc-badge-gis">~27% Area</span>
        </div>
        <div class="bus-option" id="enc-opt-indoor" onclick="setEnclosureType('indoor')">
          <span>Indoor Metal-Clad (13.8 kV)</span>
          <span class="bus-badge" id="enc-badge-indoor">~35%–52% Area</span>
        </div>
      </div>
      <div class="land-area-summary-box" id="enclosure-land-area-readout"></div>
      <label class="toggle-item" style="margin-top: 8px; padding: 6px 8px; background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;">
        <span style="font-size: 11px;">GIS / Indoor Cutaway Walls</span>
        <input type="checkbox" id="toggle-enc-cutaway" checked onchange="toggleEnclosureCutaway(this.checked)">
      </label>
      <button class="btn" style="width: 100%; justify-content: center; margin-top: 8px; font-size: 10.5px;" onclick="openEnclosureModal()">
        ⚖ Compare AIS/GIS/Indoor &amp; Land Area Matrix
      </button>
    </div>

    <!-- Interactive Switching & Interlock Matrix -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title" style="color: var(--accent-green);">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Switching & Interlock Matrix
        </div>
      </div>
      <div class="switch-matrix" id="switch-matrix-list"></div>
      <button class="btn btn-primary" style="width: 100%; justify-content: center; margin-top: 8px; font-size: 10.5px;" onclick="openChallengeModal('drill')">
        🛡 Launch Breaker Maintenance Drill (A/B/C/D/E)
      </button>
    </div>

    <!-- Fault & Dynamics Simulator -->
    <div class="dock-card">
      <div class="card-header">
        <div class="card-title" style="color: var(--accent-gold);">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
          Power Flow & Fault Events
        </div>
      </div>
      <div class="sim-actions">
        <button class="btn btn-primary" style="width: 100%; justify-content: center;" onclick="triggerNormalState()">
          ✓ Normal Load (348 A / 41.7 MVA)
        </button>
        <button class="btn" style="width: 100%; justify-content: center; background: rgba(245, 158, 11, 0.2); border-color: var(--accent-gold); color: #fde68a;" onclick="triggerLightningEvent()">
          ⚡ Simulate Lightning Surge (2.0 kA, IEEE 998)
        </button>
        <button class="btn btn-danger" style="width: 100%; justify-content: center;" onclick="triggerBusFaultEvent()">
          💥 Symmetrical 3-Phase Bus Fault (12.5 kA)
        </button>
        <button class="btn" style="width: 100%; justify-content: center; background: rgba(239, 68, 68, 0.15); border-color: #f87171; color: #fca5a5;" onclick="triggerFeederFaultEvent()">
          ⚡ Feeder SLG Fault (3.2 kA, ANSI 51N)
        </button>
        <button class="btn" id="btn-flisr-loop" style="width: 100%; justify-content: center; background: rgba(16, 185, 129, 0.18); border-color: #10b981; color: #a7f3d0;" onclick="triggerFlisrLoopRestoration()">
          🔁 FLISR Auto-Loop Transfer (Sub B Back-Feed)
        </button>
        <div id="flisr-status-readout" class="flisr-status-box">
          Feeder Loop: 52-F1 CLOSED | 79-ACR1 CLOSED | 34-SECT CLOSED | 79-TIE (Sub B) OPEN (Normal Radial)
        </div>
        <button class="btn" style="width: 100%; justify-content: center; background: rgba(148, 163, 184, 0.2); border-color: #94a3b8; color: #f1f5f9;" onclick="toggleBreakerState()">
          🔄 Manual Breaker Trip (52)
        </button>
        <button class="btn" style="width: 100%; justify-content: center; background: rgba(16, 185, 129, 0.18); border-color: #34d399; color: #6ee7b7;" onclick="triggerSafeIsolationSequence()">
          🔒 LOTO / Safe Isolation Sequence
        </button>
        <button class="btn" style="width: 100%; justify-content: center; background: rgba(14, 165, 233, 0.22); border-color: #38bdf8; color: #bae6fd;" onclick="openAnalysisModal('pf')">
          📊 Power Flow & Fault Analysis Lab
        </button>
        <button class="btn" id="btn-pinpoint-fault-mode" style="width: 100%; justify-content: center; background: rgba(244, 63, 94, 0.22); border-color: #f43f5e; color: #fecdd3;" onclick="togglePinpointFaultMode()">
          🎯 Pinpoint Fault Location Mode: OFF
        </button>
        <div id="pinpoint-fault-readout" class="pinpoint-status-box">
          Pinpoint Mode: Toggle ON then click any 3D equipment or SLD node to inject fault & compute Z₁/Z₂/Z₀.
        </div>
        <button class="btn" style="width: 100%; justify-content: center; background: rgba(168, 85, 247, 0.22); border-color: #c084fc; color: #e9d5ff;" onclick="openAnalysisModal('pq')">
          📈 Open Power Quality (PQ) Analyzer
        </button>
      </div>
    </div>
  </aside>

  <!-- BOTTOM EXPLODED VIEW DOCK (Activated in Explode Mode) -->
  <section id="explode-dock">
    <div class="explode-header">
      <div class="explode-title">
        <span id="explode-comp-name">Main Power Transformer (TR-01)</span>
        <span class="tag" id="explode-comp-tag">ANSI 87T / IEEE C57</span>
      </div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-preset" onclick="toggleAutoRotate()" id="btn-auto-rotate">🔄 Auto-Rotate</button>
        <button class="btn btn-danger" onclick="exitExplodedMode()">✕ Return to Yard</button>
      </div>
    </div>

    <div class="slider-container">
      <label>EXPLODE:</label>
      <input type="range" min="0" max="100" value="0" class="range-slider" id="explode-slider" oninput="setExplodePercentage(this.value)">
      <span class="slider-pct" id="explode-pct-label">0%</span>
    </div>

    <div class="explode-btn-row">
      <div style="display: flex; gap: 6px;">
        <button class="btn" onclick="animateExplode(0)">Assemble</button>
        <button class="btn btn-primary" onclick="animateExplode(100)">Explode (100%)</button>
      </div>
      <div class="parts-scroll" id="parts-chips-container">
        <!-- Sub-parts dynamically populated -->
      </div>
    </div>
  </section>

  <!-- UNIFIED RIGHT DOCK: EQUIPMENT SPECS + LIVE SINGLE-LINE DIAGRAM -->
  <div id="right-dock">
    <!-- RIGHT TELEMETRY & SPEC DRAWER -->
    <aside id="telemetry-drawer">
      <div class="drawer-header">
        <h2 id="drawer-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          <span id="drawer-comp-name">Power Transformer</span>
        </h2>
        <div style="display: flex; gap: 6px; align-items: center;">
          <button class="btn btn-primary" onclick="launchSelectedEquipmentModalExplode()" style="padding: 4px 8px; font-size: 10.5px;" title="Open interactive 3D exploded assembly pop-up">🔍 3D Exploded</button>
          <button class="btn" onclick="toggleTelemetryDrawer()" style="padding: 4px 8px;">✕</button>
        </div>
      </div>

      <div class="drawer-tabs">
        <div class="drawer-tab active" onclick="setDrawerTab('specs')">Ratings</div>
        <div class="drawer-tab" onclick="setDrawerTab('calc')">Function & Calc</div>
        <div class="drawer-tab" onclick="setDrawerTab('failures')">Failures</div>
        <div class="drawer-tab" onclick="setDrawerTab('checklist')">Checklist</div>
        <div class="drawer-tab" onclick="setDrawerTab('standards')">Standards</div>
      </div>

      <div class="drawer-content" id="drawer-content-body">
        <!-- Dynamically rendered based on active component and tab -->
      </div>
    </aside>

    <!-- Button to reopen collapsed drawer -->
    <button class="btn btn-primary drawer-toggle-btn" id="btn-reopen-drawer" onclick="toggleTelemetryDrawer()" style="display: none;">
      📊 Show Equipment Specs
    </button>

    <!-- BOTTOM-RIGHT INTERACTIVE SINGLE-LINE DIAGRAM (SLD) OVERLAY -->
    <div id="sld-overlay">
      <div class="sld-header">
        <span>LIVE SLD (ANSI C37.2)</span>
        <div style="display: flex; gap: 4px; align-items: center;">
          <button class="btn" style="padding: 2px 6px; font-size: 9px;" onclick="toggleBreakerState()" id="btn-sld-breaker">CB: CLOSED (52)</button>
          <button class="btn" style="padding: 2px 6px; font-size: 9px;" onclick="toggleDisconnectState()" id="btn-sld-disconnect">DISC: CLOSED (89)</button>
          <button class="btn" style="padding: 2px 6px; font-size: 9px; background: rgba(14,165,233,0.28); border-color: #38bdf8; color: #e0f2fe;" onclick="openExpandedSLD()" id="btn-expand-sld" title="Expand Live SLD Window">⛶ Expand</button>
        </div>
      </div>
      <div id="sld-svg-container">
        <!-- Live SVG SLD will be drawn here -->
      </div>
    </div>
  </div>

  <!-- FIRST PERSON WALK HUD WITH LIVE PROXIMITY HAZARD BANNER -->
  <div id="fps-hud">
    <div class="reticle"></div>
    <div id="proximity-hazard-banner" class="stage-warning">
      <span id="proximity-hazard-icon">⚠️</span>
      <span id="proximity-hazard-text">CAUTION: APPROACHING ENERGIZED 69 kV BUS</span>
      <span id="proximity-hazard-dist" style="color: #fff; background: rgba(0,0,0,0.35); padding: 2px 7px; border-radius: 4px; font-weight: bold;">MAD: 4.5m</span>
    </div>
    <div id="walk-inspect-prompt" style="display:none;"></div>
    <div class="fps-controls-hint">
      <strong>FIELD ENGINEER WALK MODE:</strong><br>
      • [W, A, S, D] / Arrow Keys: Move across gravel pad<br>
      • Mouse Drag: Look around yard (Eye-height 1.75m)<br>
      • Press [E] or Click focused apparatus / SCADA HMI to inspect<br>
      • Press [ESC] or toggle switch to exit Walk Mode
    </div>
  </div>

  <!-- 4TH-YEAR EE FIELD ENGINEER CHALLENGE MODAL -->
  <div class="modal-backdrop" id="challenge-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h3>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          EE 415 4th-Year Field Engineer Challenge
        </h3>
        <button class="btn" onclick="closeChallengeModal()">✕</button>
      </div>

      <div class="drawer-tabs">
        <div class="drawer-tab active" id="tab-drill-quiz" onclick="switchChallengeTab('quiz')">Drill A: Component & Sub-Part Diagnostic</div>
        <div class="drawer-tab" id="tab-drill-switching" onclick="switchChallengeTab('switching')">Drill B: Maintenance Switching Order Isolation</div>
      </div>

      <div class="modal-body" id="challenge-modal-body">
        <!-- Injected dynamically -->
      </div>

      <div class="modal-footer">
        <span id="challenge-score-display" style="font-family: var(--font-mono); font-weight: 700; color: var(--accent-gold); margin-right: auto;">SCORE: 0 / 100</span>
        <button class="btn" onclick="closeChallengeModal()">Close</button>
        <button class="btn btn-primary" id="btn-challenge-action" onclick="handleChallengeAction()">Submit Answer</button>
      </div>
    </div>
  </div>

  <!-- ARC FLASH DISASTER WARNING MODAL -->
  <div class="modal-backdrop" id="arc-flash-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h3 style="color: #fca5a5;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          FATAL ELECTRICAL SAFETY VIOLATION: ARC FLASH BLAST!
        </h3>
        <button class="btn" onclick="closeArcFlashModal()">✕</button>
      </div>
      <div class="modal-body">
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: 8px; padding: 14px; color: #fecaca;">
          <h4 style="font-size: 14px; font-weight: 700; margin-bottom: 6px; color: #ef4444;">DISCONNECT SWITCH (ANSI 89) OPENED UNDER LOAD!</h4>
          <p style="font-size: 12px; line-height: 1.5;">
            You attempted to open the 69 kV Disconnect Switch while Circuit Breaker CB-69-1 was CLOSED and carrying 348.9 A of full load current.
          </p>
        </div>
        <div style="font-size: 12px; line-height: 1.6; color: #cbd5e1;">
          <strong style="color: var(--accent-gold);">ENGINEERING & OSH RULE 1210 PRINCIPLES:</strong>
          <ul style="margin-left: 20px; margin-top: 6px;">
            <li><strong>No Arc-Extinguishing Medium:</strong> Disconnect switches (isolators) separate copper contacts in atmospheric air. They have zero interrupting capacity ($0\text{ kA}$).</li>
            <li><strong>Plasma Arc Flashover:</strong> Attempting to break 348.9 A across an air gap ionizes air into an incandescent plasma channel exceeding <strong>19,000°C (35,000°F)</strong>—four times hotter than the surface of the sun.</li>
            <li><strong>Catastrophic Blast Pressure:</strong> Copper expands 67,000 times into vapor, generating an explosive blast wave, shrapnel, and lethal third-degree radiation burns.</li>
            <li><strong>Strict Interlock Rule:</strong> In high-voltage substations, mechanical and electrical key interlocks (Kirk key / SCADA logic) <strong>MUST NEVER PERMIT</strong> opening Disconnect 89 unless Circuit Breaker 52 is confirmed OPEN with line current verified at $0\text{ A}$!</li>
          </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="resetAfterArcFlash()">Acknowledge & Reset Switchyard</button>
      </div>
    </div>
  </div>

  <!-- SUB-PART ENGINEERING DEEP-DIVE POP-UP MODAL -->
  <div class="modal-backdrop" id="subpart-modal">
    <div class="modal-box subpart-modal-box">
      <div class="modal-header">
        <div>
          <span class="subpart-ansi-badge" id="subpart-modal-ansi">ANSI / IEEE</span>
          <h3 id="subpart-modal-title" style="margin-top: 4px;">Sub-Part Engineering Inspector</h3>
        </div>
        <button class="btn" onclick="closeSubpartModal()" title="Close (Esc)">✕</button>
      </div>
      <div class="subpart-modal-grid">
        <div class="subpart-visual-col">
          <div class="subpart-view-tabs">
            <button class="subpart-tab active" id="tab-btn-3d" onclick="switchSubpartVisualTab('3d')">3D Sub-Assembly</button>
            <button class="subpart-tab" id="tab-btn-full3d" onclick="switchSubpartVisualTab('full3d')">🔍 Full Exploded 3D</button>
            <button class="subpart-tab" id="tab-btn-svg" onclick="switchSubpartVisualTab('svg')">Schematic</button>
          </div>
          <div class="subpart-stage">
            <canvas id="subpart-turntable-canvas" width="420" height="310"></canvas>
            <div id="subpart-svg-diagram" style="display: none;"></div>
            <div class="subpart-stage-hint" id="subpart-stage-hint">Drag inside 3D preview to rotate • Scroll to zoom</div>
          </div>
          <div id="subpart-modal-explode-controls" style="display: none;">
            <div class="modal-explode-row">
              <span style="font-size: 10px; font-family: var(--font-mono); color: #94a3b8;">ASSEMBLE</span>
              <input type="range" id="modal-explode-slider" min="0" max="100" value="65" oninput="setModalExplodePercentage(this.value)" style="flex:1; accent-color: var(--accent-cyan);">
              <span id="modal-explode-pct" style="font-size: 11px; font-family: var(--font-mono); color: var(--accent-cyan); min-width: 34px; text-align: right;">65%</span>
              <button class="btn" id="modal-autorotate-btn" onclick="toggleModalAutoRotate()" style="padding: 3px 8px; font-size: 10px;">↻ Spin</button>
            </div>
            <div id="modal-subpart-chips" class="modal-subpart-chips"></div>
          </div>
          <div id="subpart-action-bar" class="subpart-action-bar" style="display: none;"></div>
        </div>
        <div class="subpart-info-col">
          <div class="subpart-detail-card">
            <div class="subpart-detail-title">1. Physical Appearance &amp; Field Spotting Cues</div>
            <p id="subpart-field-spot"></p>
          </div>
          <div class="subpart-detail-card">
            <div class="subpart-detail-title">2. Internal Working Principle (Normal &amp; Fault Conditions)</div>
            <p id="subpart-working-principle"></p>
          </div>
          <div class="subpart-detail-card">
            <div class="subpart-detail-title">3. Construction Material &amp; System Role</div>
            <p id="subpart-material-role"></p>
          </div>
          <div class="subpart-detail-card warn">
            <div class="subpart-detail-title">4. Ratings, Failure Modes &amp; Field Maintenance Diagnostics</div>
            <p id="subpart-maintenance"></p>
          </div>
        </div>
      </div>
      <div class="modal-footer" style="justify-content: space-between;">
        <div style="display: flex; gap: 8px;">
          <button class="btn" onclick="stepSubpartModal(-1)">◀ Prev Sub-Part</button>
          <button class="btn" onclick="stepSubpartModal(1)">Next Sub-Part ▶</button>
        </div>
        <button class="btn btn-primary" onclick="closeSubpartModal()">Return to Switchyard</button>
      </div>
    </div>
  </div>

  <!-- HELP / ABOUT MODAL -->
  <div class="modal-backdrop" id="help-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h3>ℹ About Substation and Distribution Simulation</h3>
        <button class="btn" onclick="closeHelpModal()">✕</button>
      </div>
      <div class="modal-body" style="font-size: 12px; line-height: 1.6; color: #cbd5e1;">
        <p><strong>Substation and Distribution Simulation Suite</strong><br>
        Power Systems Protection, Substation Design &amp; Distribution Engineering Workbench</p>
        <hr style="border: none; border-top: 1px solid var(--surface-border); margin: 8px 0;">
        <p><strong>Interactive Features & Navigation:</strong></p>
        <ul style="margin-left: 20px;">
          <li><strong>Orbit Controls:</strong> Left-click and drag to rotate, right-click and drag to pan, scroll wheel to zoom.</li>
          <li><strong>Click-to-Explode:</strong> Click directly on any primary component in the 3D switchyard to inspect its internals and activate the exploded-view slider.</li>
          <li><strong>Live Single-Line Diagram (SLD):</strong> Interactive schematic in the bottom right reflects electrical status and lets you select components.</li>
          <li><strong>Switchyard Busbar Topologies:</strong> Toggle between Single Bus, Main & Transfer Bus, Ring Bus, and Breaker-and-a-Half schemes in real time.</li>
          <li><strong>Fault & Protection Simulations:</strong> Trigger lightning strikes and symmetrical 3-phase short circuits to observe surge arresters and circuit breaker trips.</li>
          <li><strong>4th-Year Field Challenge:</strong> Complete diagnostic quizzes and safe switching isolation drills.</li>
        </ul>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="closeHelpModal()">Got It</button>
      </div>
    </div>
  </div>

  <!-- IEEE 80 GROUND GRID X-RAY COLOR-SCALE GRADIENT LEGEND -->
  <div id="ground-legend">
    <div class="ground-legend-header">
      <span>IEEE Std 80 GPR & Touch Potential Scale</span>
      <span style="color:#10b981;">SAFE MARGIN</span>
    </div>
    <div class="ground-colorbar"></div>
    <div class="ground-scale-ticks">
      <span>0 V (Ref)</span>
      <span>280 V</span>
      <span>578 V Etouch</span>
      <span>1,940 V Estep</span>
      <span>3,840 V GPR</span>
    </div>
    <div class="ground-ieee-metrics">
      <div>Grid Rg: <strong style="color:#38bdf8;">0.842 Ω</strong></div>
      <div>Max GPR: <strong style="color:#f87171;">3,840 V</strong></div>
      <div>Etouch (70kg): <strong>578 V</strong></div>
      <div>Actual Em: <strong style="color:#10b981;">442 V ✓</strong></div>
      <div>Estep (70kg): <strong>1,940 V</strong></div>
      <div>Actual Es: <strong style="color:#10b981;">610 V ✓</strong></div>
    </div>
  </div>

  <!-- ENCLOSURE COMPARISON MATRIX MODAL -->
  <div class="modal-backdrop" id="enclosure-modal">
    <div class="modal-box" style="width: 780px;">
      <div class="modal-header">
        <h3>⚖ Substation Architecture Comparison: AIS vs. SF₆ GIS vs. Indoor Metal-Clad</h3>
        <button class="btn" onclick="closeEnclosureModal()">✕</button>
      </div>
      <div class="modal-body" id="enclosure-modal-body" style="padding: 14px 18px;"></div>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="closeEnclosureModal()">Close Comparison</button>
      </div>
    </div>
  </div>

  <!-- FULL-SCREEN FLASHING HV DANGER BORDER -->
  <div id="hv-screen-flash"></div>

  <!-- HIGH-VOLTAGE MINIMUM APPROACH DISTANCE (MAD) VIOLATION & CONSEQUENCE REPORT MODAL -->
  <div class="modal-backdrop" id="hv-danger-modal">
    <div class="modal-box hv-danger-box">
      <div class="hv-hazard-stripes"></div>
      <div class="hv-danger-body">
        <div class="hv-danger-icon">⚡</div>
        <div class="hv-danger-badge">ANSI Z535 / IEEE C2 TABLE 441-1 / OSHA 1910.269 MAD BREACH</div>
        <h2>⚡ HIGH-VOLTAGE CLEARANCE VIOLATION & CONSEQUENCE REPORT</h2>
        <p id="hv-danger-desc" class="hv-danger-desc">
          You have breached the Minimum Approach Distance (MAD) to live uninsulated high-voltage equipment!
        </p>
        <div class="hv-danger-metrics">
          <div>
            <span>Nearest Live Terminal</span>
            <strong id="hv-danger-node">69 kV Bus / Bushing</strong>
          </div>
          <div>
            <span>3D Air-Gap Distance</span>
            <strong id="hv-danger-dist" style="color: #fca5a5;">1.45 m (&lt; 2.2 m MAD)</strong>
          </div>
          <div>
            <span>Air Electric Field</span>
            <strong id="hv-danger-efield" style="color: #fde047;">2.75 kV/cm</strong>
          </div>
          <div>
            <span>Body Touch Current</span>
            <strong id="hv-danger-ibody" style="color: #f87171;">4,200 mA (FATAL)</strong>
          </div>
        </div>

        <div class="hv-consequence-grid">
          <div class="hv-conseq-card">
            <h4>1. Dielectric Breakdown of Air</h4>
            <div id="hv-conseq-air">
              Dry air breaks down at <strong>~30 kV/cm peak (~3 kV/mm)</strong>. Even without physical contact, an ionized plasma arc jumps across the remaining air gap directly to your body.
            </div>
          </div>
          <div class="hv-conseq-card">
            <h4>2. Arc-Flash Blast (IEEE 1584 / NFPA 70E)</h4>
            <div id="hv-conseq-arc">
              Incident Energy: <strong style="color:#f87171;">48.2 cal/cm²</strong>. Arc plasma reaches <strong>&gt; 19,000 °C</strong> (4× hotter than the sun's surface) with vaporized copper pressure blast and fatal 3rd-degree burns.
            </div>
          </div>
          <div class="hv-conseq-card">
            <h4>3. Ventricular Fibrillation (IEEE Std 80)</h4>
            <div id="hv-conseq-phys">
              Assuming human body resistance <strong>R_body = 1,000 Ω</strong>, touch/step current exceeds the Dalziel threshold (<strong>100–200 mA</strong>), inducing cardiac arrest, respiratory paralysis, and internal thermal necrosis.
            </div>
          </div>
        </div>

        <div class="hv-danger-actions">
          <button class="btn hv-retreat-btn" onclick="stepBackToSafeZone()">⚠️ Acknowledge Hazard &amp; Retreat to Safe Perimeter (≥ 3.5m)</button>
          <button class="btn" onclick="dismissHvDangerModal()" style="font-size: 11px;">Retreat &amp; Close</button>
        </div>
      </div>
      <div class="hv-hazard-stripes"></div>
    </div>
  </div>

  <!-- VOLTAGE SCALING & IEEE 1427 CLEARANCE COMPARISON MODAL -->
  <div class="modal-backdrop" id="voltage-scale-modal">
    <div class="modal-box" style="width: 820px;">
      <div class="modal-header">
        <h3>📏 Multi-Voltage Scaling & Clearances (IEEE Std 1427 / IEEE C2 NESC / PEC Part 2)</h3>
        <button class="btn" onclick="closeVoltageClassModal()">✕</button>
      </div>
      <div class="modal-body" id="voltage-scale-body" style="padding: 14px 18px;"></div>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="closeVoltageClassModal()">Close Scaling Table</button>
      </div>
    </div>
  </div>

  <!-- INTERACTIVE POWER FLOW, SHORT-CIRCUIT & POWER QUALITY LAB MODAL -->
  <div class="modal-backdrop" id="analysis-modal">
    <div class="modal-box" style="width: 1060px; max-width: 96vw; max-height: 92vh;">
      <div class="modal-header">
        <h3>📊 EE 415 Power Flow, Short-Circuit, Protection Coordination (TCC) &amp; PQ Lab</h3>
        <button class="btn" onclick="closeAnalysisModal()">✕</button>
      </div>
      <div class="drill-tabs">
        <button class="drill-tab active" id="tab-analysis-pf" onclick="switchAnalysisTab('pf')">⚡ Per-Unit Power Flow & Voltage Drop</button>
        <button class="drill-tab" id="tab-analysis-sc" onclick="switchAnalysisTab('sc')">💥 Short-Circuit & Pinpoint Fault Lab</button>
        <button class="drill-tab" id="tab-analysis-tcc" onclick="switchAnalysisTab('tcc')">🛡️ Relay Settings &amp; TCC Coordination Lab</button>
        <button class="drill-tab" id="tab-analysis-pq" onclick="switchAnalysisTab('pq')">📈 Power Quality (PQ) & Waveform Lab</button>
      </div>
      <div class="modal-body" id="analysis-modal-body" style="padding: 14px 18px; overflow-y: auto;"></div>
      <div class="modal-footer">
        <span id="analysis-footer-note" style="font-size: 11px; color: var(--text-muted); margin-right: auto;">Synced live to top telemetry bar & 3D OLTC/Capacitor states</span>
        <button class="btn btn-primary" onclick="closeAnalysisModal()">Apply & Close</button>
      </div>
    </div>
  </div>

  <!-- EXPANDED INTERACTIVE MASTER SINGLE-LINE DIAGRAM WINDOW -->
  <div class="modal-backdrop" id="sld-expanded-modal">
    <div class="sld-exp-box">
      <div class="sld-exp-toolbar">
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
          <span style="font-weight: 700; font-size: 13px; color: #38bdf8;">📐 Master SLD (ANSI/IEEE C37.2)</span>
          <div class="sld-fault-type-bar" title="Select Short-Circuit Fault Type for SLD Simulation">
            <span style="font-size: 9.5px; color: #fca5a5; font-weight: 700; font-family: monospace; margin-right: 2px;">FAULT:</span>
            <button class="sld-ft-pill active" id="sld-ft-3ph" onclick="setSldFaultType('3ph')">3Φ LLL</button>
            <button class="sld-ft-pill" id="sld-ft-slg" onclick="setSldFaultType('slg')">SLG (A-G)</button>
            <button class="sld-ft-pill" id="sld-ft-ll" onclick="setSldFaultType('ll')">L-L (B-C)</button>
            <button class="sld-ft-pill" id="sld-ft-dlg" onclick="setSldFaultType('dlg')">DLG (B-C-G)</button>
          </div>
        </div>
        <div style="display: flex; gap: 5px; align-items: center; flex-wrap: wrap;">
          <button class="btn" onclick="zoomExpandedSLD(1.2)" style="padding: 4px 8px;">➕</button>
          <button class="btn" onclick="zoomExpandedSLD(0.83)" style="padding: 4px 8px;">➖</button>
          <button class="btn" onclick="resetExpandedSLDView()" style="padding: 4px 8px;">↺ Reset</button>
          <button class="btn" id="btn-sld-exp-pinpoint" onclick="togglePinpointFaultMode()" style="padding: 4px 9px; background: rgba(244,63,94,0.22); border-color: #f43f5e; color: #fecdd3;">🎯 Pinpoint Fault on SLD</button>
          <button class="btn" id="btn-sld-exp-plot-tcc" onclick="plotActiveFaultOnTcc()" style="padding: 4px 9px; background: rgba(250,204,21,0.18); border-color: #facc15; color: #fef08a;">📈 Plot Fault on TCC</button>
          <button class="btn sld-clear-fault-btn" id="btn-sld-exp-clear-fault" onclick="clearFaultAndResetSystem()" style="padding: 4px 9px;">🔄 Clear Fault &amp; Reset System</button>
          <button class="btn btn-primary" onclick="closeExpandedSLD()" style="padding: 4px 10px;">🗕 Dock</button>
        </div>
      </div>
      <div class="sld-exp-viewport" id="sld-expanded-viewport">
        <div id="sld-expanded-svg-container"></div>
      </div>
      <div class="sld-exp-telemetry-strip" id="sld-expanded-footer">
        Live SLD Telemetry Ready
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast"></div>
"""

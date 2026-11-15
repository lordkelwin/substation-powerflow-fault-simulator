"""
sim_css.py
Styles for the EE 415 3D Substation Simulator.
Includes scrollable docks, proximity hazard HUD, and dynamic styling.
"""

def get_css_styles():
    return """
    <style>
      :root {
        --bg-dark: #0f172a;
        --surface: rgba(15, 23, 42, 0.92);
        --surface-border: rgba(148, 163, 184, 0.20);
        --surface-hover: rgba(30, 41, 59, 0.95);
        --primary: #0284c7;
        --primary-glow: #38bdf8;
        --accent-cyan: #06b6d4;
        --accent-gold: #f59e0b;
        --accent-red: #ef4444;
        --accent-green: #10b981;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --font-ui: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
      }

      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
      }

      body {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background-color: var(--bg-dark);
        color: var(--text-main);
        font-family: var(--font-ui);
        font-size: 13px;
        position: relative;
      }

      /* 3D WebGL Canvas - explicitly fixed full viewport */
      #canvas3d {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
        display: block;
      }

      /* RUNTIME ERROR DIAGNOSTIC BANNER */
      #runtime-error-banner {
        display: none;
        position: fixed;
        top: 66px;
        left: 20px;
        right: 20px;
        background: rgba(185, 28, 28, 0.95);
        color: #fff;
        padding: 16px 20px;
        border-radius: 8px;
        z-index: 9999;
        font-family: var(--font-mono);
        font-size: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        border: 2px solid #f87171;
      }

      /* TOP BAR */
      header#top-bar {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        min-height: 54px;
        height: auto;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.88) 100%);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--surface-border);
        display: grid;
        grid-template-columns: minmax(215px, 290px) minmax(0, 1fr) auto;
        align-items: center;
        gap: 8px;
        padding: 4px 12px;
        z-index: 100;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 9px;
        flex-shrink: 0;
        min-width: 210px;
        max-width: 290px;
        overflow: hidden;
      }

      .brand-badge {
        width: 38px;
        height: 38px;
        padding: 3px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.22), rgba(245, 158, 11, 0.18));
        border: 1px solid rgba(56, 189, 248, 0.55);
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        flex-shrink: 0;
      }

      .brand-emblem-svg {
        display: block;
        width: 32px;
        height: 32px;
      }

      .brand-title {
        min-width: 0;
        max-width: 235px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .brand-title h1 {
        font-size: 13px;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.2px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .brand-title p {
        font-size: 9.5px;
        color: var(--text-muted);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      /* LIVE TELEMETRY CHIPS */
      .telemetry-bar {
        display: flex;
        align-items: center;
        flex-wrap: nowrap;
        overflow-x: auto;
        scrollbar-width: none;
        gap: 5px;
        font-family: var(--font-mono);
        white-space: nowrap;
        min-width: 0;
        width: 100%;
        margin: 0;
        padding: 2px 2px;
      }

      .telemetry-bar::-webkit-scrollbar {
        display: none;
      }

      .telem-chip {
        display: flex;
        align-items: center;
        gap: 4px;
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid var(--surface-border);
        padding: 3px 7px;
        border-radius: 6px;
        font-size: 10px;
        white-space: nowrap;
        min-width: max-content;
        flex-shrink: 0;
      }

      .telem-voltage-card {
        display: flex;
        align-items: center;
        gap: 4px;
        background: rgba(8, 20, 38, 0.88);
        border: 1px solid rgba(56, 189, 248, 0.32);
        padding: 2px 6px;
        border-radius: 7px;
        white-space: nowrap;
        min-width: max-content;
        flex-shrink: 0;
      }

      .vpill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 5px;
        border-radius: 5px;
        font-size: 10px;
        font-weight: 700;
        white-space: nowrap;
      }

      .vpill-hv {
        background: rgba(6, 182, 212, 0.16);
        border: 1px solid rgba(6, 182, 212, 0.45);
        color: #67e8f9;
      }

      .vpill-lv {
        background: rgba(245, 158, 11, 0.16);
        border: 1px solid rgba(245, 158, 11, 0.45);
        color: #fde68a;
      }

      .vpill-pu {
        font-size: 9px;
        opacity: 0.9;
        color: #cbd5e1;
      }

      .vr-badge {
        font-size: 9px;
        font-weight: 700;
        padding: 2px 5px;
        border-radius: 4px;
        background: rgba(16, 185, 129, 0.18);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
      }

      .telem-chip .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--accent-green);
        box-shadow: 0 0 8px var(--accent-green);
      }

      .telem-chip .dot.pulse {
        animation: pulse 1.5s infinite;
      }

      @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
      }

      .telem-chip span.label {
        color: var(--text-muted);
        font-size: 9px;
      }

      .telem-chip span.val {
        color: var(--primary-glow);
        font-weight: 700;
      }

      .header-actions {
        display: flex;
        align-items: center;
        gap: 5px;
        flex-shrink: 0;
        white-space: nowrap;
      }

      .header-actions .btn {
        padding: 4px 8px;
        font-size: 10.5px;
        white-space: nowrap;
      }

      /* BUTTONS */
      .btn {
        background: var(--surface);
        border: 1px solid var(--surface-border);
        color: var(--text-main);
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 11.5px;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s ease;
      }

      .btn:hover {
        background: var(--surface-hover);
        border-color: var(--primary-glow);
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
        color: #fff;
      }

      .btn-primary {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border-color: #38bdf8;
        color: #fff;
        box-shadow: 0 0 12px rgba(2, 132, 199, 0.4);
      }

      .btn-primary:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.5);
      }

      .btn-danger {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.4);
        color: #fca5a5;
      }

      .btn-danger:hover {
        background: rgba(239, 68, 68, 0.3);
        border-color: #ef4444;
        color: #fff;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
      }

      .btn-active {
        background: rgba(2, 132, 199, 0.3) !important;
        border-color: var(--primary-glow) !important;
        color: var(--primary-glow) !important;
      }

      /* LEFT CONTROL DOCK - FULLY SCROLLABLE WITH CUSTOM SCROLLBAR */
      #left-dock {
        position: absolute;
        top: 68px;
        left: 20px;
        width: 260px;
        max-height: calc(100vh - 84px);
        overflow-y: auto;
        overflow-x: hidden;
        z-index: 90;
        display: flex;
        flex-direction: column;
        gap: 10px;
        pointer-events: auto;
        padding-right: 4px;
      }

      #left-dock::-webkit-scrollbar {
        width: 6px;
      }

      #left-dock::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 4px;
      }

      #left-dock::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.05);
      }

      #left-dock::-webkit-scrollbar-thumb:hover {
        background: #0284c7;
      }

      .dock-card {
        background: var(--surface);
        backdrop-filter: blur(12px);
        border: 1px solid var(--surface-border);
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        flex-shrink: 0;
      }

      .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      }

      .card-title {
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: var(--accent-cyan);
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .preset-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
      }

      .btn-preset {
        font-size: 10.5px;
        padding: 5px 8px;
        text-align: left;
        justify-content: flex-start;
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 4px;
        color: #cbd5e1;
      }

      .btn-preset:hover {
        background: rgba(2, 132, 199, 0.25);
        color: #fff;
        border-color: var(--primary-glow);
      }

      .btn-preset.active {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.4), rgba(14, 165, 233, 0.2));
        border-color: var(--primary-glow);
        color: #fff;
        font-weight: 700;
      }

      /* TOGGLES LIST */
      .toggle-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 5px 0;
        font-size: 11px;
      }

      .toggle-label {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #e2e8f0;
      }

      .switch {
        position: relative;
        display: inline-block;
        width: 32px;
        height: 18px;
      }

      .switch input {
        opacity: 0;
        width: 0;
        height: 0;
      }

      .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #334155;
        transition: .3s;
        border-radius: 18px;
      }

      .slider:before {
        position: absolute;
        content: "";
        height: 12px;
        width: 12px;
        left: 3px;
        bottom: 3px;
        background-color: white;
        transition: .3s;
        border-radius: 50%;
      }

      input:checked + .slider {
        background-color: var(--primary);
      }

      input:checked + .slider:before {
        transform: translateX(14px);
      }

      /* BUSBAR TOPOLOGY SELECTOR */
      .bus-selector {
        display: flex;
        flex-direction: column;
        gap: 5px;
      }

      .bus-option {
        padding: 6px 8px;
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 4px;
        cursor: pointer;
        font-size: 10.5px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.2s;
      }

      .bus-option:hover {
        background: rgba(2, 132, 199, 0.2);
        border-color: rgba(56, 189, 248, 0.4);
      }

      .bus-option.selected {
        background: rgba(2, 132, 199, 0.35);
        border-color: var(--primary-glow);
        color: #fff;
        font-weight: 700;
        box-shadow: 0 0 8px rgba(56, 189, 248, 0.25);
      }

      .bus-badge {
        font-size: 9px;
        padding: 2px 5px;
        border-radius: 3px;
        background: rgba(255, 255, 255, 0.1);
        font-family: var(--font-mono);
      }

      /* SIMULATION ACTIONS */
      .sim-actions {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }

      /* EXPLODED VIEW BOTTOM DOCK */
      #explode-dock {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        max-width: 90vw;
        background: var(--surface);
        backdrop-filter: blur(16px);
        border: 1px solid var(--surface-border);
        border-radius: 12px;
        padding: 14px 20px;
        z-index: 95;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        display: none;
        flex-direction: column;
        gap: 10px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }

      .explode-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .explode-title {
        font-size: 13px;
        font-weight: 700;
        color: var(--accent-cyan);
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .explode-title span.tag {
        font-size: 10px;
        padding: 2px 6px;
        background: rgba(2, 132, 199, 0.3);
        border: 1px solid var(--primary-glow);
        border-radius: 4px;
        color: #fff;
        font-family: var(--font-mono);
      }

      .slider-container {
        display: flex;
        align-items: center;
        gap: 14px;
      }

      .slider-container label {
        font-size: 11px;
        font-weight: 600;
        color: var(--text-muted);
        min-width: 70px;
      }

      .range-slider {
        flex: 1;
        -webkit-appearance: none;
        appearance: none;
        height: 6px;
        border-radius: 3px;
        background: #334155;
        outline: none;
      }

      .range-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--primary-glow);
        cursor: pointer;
        box-shadow: 0 0 10px var(--primary-glow);
        transition: transform 0.1s;
      }

      .range-slider::-webkit-slider-thumb:hover {
        transform: scale(1.2);
      }

      .slider-pct {
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 700;
        color: var(--primary-glow);
        min-width: 45px;
        text-align: right;
      }

      .explode-btn-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }

      /* SUB-PARTS CHIPS BAR */
      .parts-scroll {
        display: flex;
        align-items: center;
        gap: 6px;
        overflow-x: auto;
        padding-bottom: 4px;
      }

      .parts-scroll::-webkit-scrollbar {
        height: 4px;
      }

      .parts-scroll::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 2px;
      }

      .part-chip {
        padding: 4px 8px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        font-size: 10px;
        white-space: nowrap;
        cursor: pointer;
        transition: all 0.2s;
        color: #94a3b8;
      }

      .part-chip:hover, .part-chip.active {
        background: rgba(2, 132, 199, 0.3);
        border-color: var(--primary-glow);
        color: #fff;
      }

      /* UNIFIED RIGHT-HAND DOCK: SPECS DRAWER + LIVE SLD */
      #right-dock {
        position: fixed;
        top: 72px;
        right: 16px;
        bottom: 16px;
        width: 380px;
        max-width: calc(100vw - 32px);
        display: flex;
        flex-direction: column;
        gap: 12px;
        pointer-events: none;
        z-index: 90;
      }

      /* TOP RIGHT PANEL: TELEMETRY & SPEC DRAWER */
      #telemetry-drawer {
        position: relative;
        width: 100%;
        flex: 1 1 auto;
        min-height: 0;
        max-height: calc(100% - 272px);
        background: var(--surface);
        backdrop-filter: blur(16px);
        border: 1px solid var(--surface-border);
        border-radius: 12px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        pointer-events: auto;
      }

      #telemetry-drawer.collapsed {
        display: none;
      }

      .drawer-header {
        padding: 12px 16px;
        background: rgba(15, 23, 42, 0.95);
        border-bottom: 1px solid var(--surface-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
      }

      .drawer-header h2 {
        font-size: 14px;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .drawer-tabs {
        display: flex;
        background: rgba(30, 41, 59, 0.5);
        border-bottom: 1px solid var(--surface-border);
        flex-shrink: 0;
      }

      .drawer-tab {
        flex: 1;
        padding: 7px 4px;
        text-align: center;
        font-size: 9.8px;
        font-weight: 600;
        cursor: pointer;
        color: var(--text-muted);
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
        white-space: nowrap;
      }

      .drawer-tab:hover {
        color: #fff;
      }

      .drawer-tab.active {
        color: var(--primary-glow);
        border-bottom-color: var(--primary-glow);
        background: rgba(2, 132, 199, 0.1);
      }

      .drawer-content {
        padding: 14px 16px;
        overflow-y: auto;
        flex: 1 1 auto;
        min-height: 0;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .drawer-content::-webkit-scrollbar {
        width: 5px;
      }

      .drawer-content::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 3px;
      }

      .spec-group {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        padding: 10px 12px;
      }

      .spec-group-title {
        font-size: 10.5px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--accent-cyan);
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .spec-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        font-size: 11px;
      }

      .spec-row:last-child {
        border-bottom: none;
      }

      .spec-row .k {
        color: var(--text-muted);
      }

      .spec-row .v {
        font-family: var(--font-mono);
        color: #f1f5f9;
        font-weight: 600;
      }

      .drawer-toggle-btn {
        align-self: flex-end;
        pointer-events: auto;
      }

      /* BOTTOM RIGHT PANEL: LIVE SINGLE-LINE DIAGRAM (SLD) */
      #sld-overlay {
        position: relative;
        width: 100%;
        flex: 0 0 260px;
        height: 260px;
        margin-top: auto;
        background: rgba(11, 15, 25, 0.94);
        backdrop-filter: blur(12px);
        border: 1px solid var(--surface-border);
        border-radius: 10px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.55);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        pointer-events: auto;
      }

      .sld-header {
        padding: 6px 12px;
        background: rgba(15, 23, 42, 0.95);
        border-bottom: 1px solid var(--surface-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .sld-header span {
        font-size: 10px;
        font-weight: 700;
        color: var(--accent-gold);
        letter-spacing: 0.5px;
      }

      #sld-svg-container {
        flex: 1;
        width: 100%;
        height: 100%;
        cursor: crosshair;
      }

      /* MODALS */
      .modal-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.78);
        backdrop-filter: blur(8px);
        z-index: 200;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 20px;
      }

      .modal-box {
        width: 650px;
        max-width: 95vw;
        max-height: 90vh;
        background: #0f172a;
        border: 1px solid #38bdf8;
        border-radius: 14px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(56, 189, 248, 0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: modalIn 0.25s ease-out;
      }

      @keyframes modalIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
      }

      .modal-header {
        padding: 16px 22px;
        background: linear-gradient(90deg, #0369a1 0%, #0f172a 100%);
        border-bottom: 1px solid var(--surface-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .modal-header h3 {
        font-size: 15px;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .modal-body {
        padding: 20px 22px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .modal-footer {
        padding: 14px 22px;
        background: rgba(15, 23, 42, 0.95);
        border-top: 1px solid var(--surface-border);
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
      }

      /* 3D FLOATING CALLOUT LABELS */
      .callout-pin {
        position: absolute;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid var(--primary-glow);
        border-radius: 4px;
        padding: 3px 8px;
        font-size: 10px;
        font-family: var(--font-mono);
        color: #fff;
        pointer-events: auto;
        cursor: pointer;
        transform: translate(-50%, -100%);
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 5px;
        transition: transform 0.1s ease;
        z-index: 50;
      }

      .callout-pin:hover {
        background: #0284c7;
        transform: translate(-50%, -100%) scale(1.08);
        border-color: #fff;
      }

      .callout-pin::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 50%;
        transform: translateX(-50%);
        border-width: 4px 4px 0 4px;
        border-style: solid;
        border-color: var(--primary-glow) transparent transparent transparent;
      }

      /* ARC FLASH WARNING BANNER */
      #arc-flash-modal .modal-box {
        border-color: #ef4444;
        box-shadow: 0 0 50px rgba(239, 68, 68, 0.6);
      }

      #arc-flash-modal .modal-header {
        background: linear-gradient(90deg, #b91c1c 0%, #0f172a 100%);
      }

      /* FIRST PERSON HUD OVERLAY & LIVE PROXIMITY HAZARD SYSTEM */
      #fps-hud {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 40;
        display: none;
        transition: box-shadow 0.2s ease;
      }

      /* Critical Hazard Strobe Border */
      #fps-hud.hazard-critical {
        box-shadow: inset 0 0 70px rgba(239, 68, 68, 0.85);
        animation: strobeRed 0.6s infinite alternate;
      }

      #fps-hud.hazard-warning {
        box-shadow: inset 0 0 40px rgba(245, 158, 11, 0.6);
      }

      @keyframes strobeRed {
        from { box-shadow: inset 0 0 30px rgba(239, 68, 68, 0.5); }
        to { box-shadow: inset 0 0 85px rgba(239, 68, 68, 0.95); }
      }

      .reticle {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 12px;
        height: 12px;
        transform: translate(-50%, -50%);
        border: 2px solid rgba(255, 255, 255, 0.7);
        border-radius: 50%;
      }

      /* Proximity Alert Banner */
      #proximity-hazard-banner {
        position: absolute;
        top: 68px;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 18px;
        border-radius: 8px;
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 700;
        display: none;
        align-items: center;
        gap: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        pointer-events: auto;
        z-index: 45;
        transition: all 0.2s ease;
      }

      #proximity-hazard-banner.stage-warning {
        display: flex;
        background: rgba(245, 158, 11, 0.95);
        color: #0f172a;
        border: 2px solid #fbbf24;
        animation: pulseWarning 1.0s infinite;
      }

      #proximity-hazard-banner.stage-danger {
        display: flex;
        background: rgba(220, 38, 38, 0.96);
        color: #fff;
        border: 2px solid #f87171;
        animation: pulseDanger 0.5s infinite;
      }

      #proximity-hazard-banner.stage-safe {
        display: flex;
        background: rgba(16, 185, 129, 0.92);
        color: #fff;
        border: 2px solid #34d399;
      }

      @keyframes pulseWarning {
        0%, 100% { transform: translateX(-50%) scale(1); }
        50% { transform: translateX(-50%) scale(1.02); }
      }

      @keyframes pulseDanger {
        0%, 100% { transform: translateX(-50%) scale(1); }
        50% { transform: translateX(-50%) scale(1.04); }
      }

      .fps-controls-hint {
        position: absolute;
        bottom: 24px;
        left: 24px;
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid var(--surface-border);
        border-radius: 8px;
        padding: 10px 16px;
        font-family: var(--font-mono);
        font-size: 11px;
        color: #cbd5e1;
        pointer-events: auto;
        line-height: 1.5;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
      }

      /* NOTIFICATION TOAST */
      #toast {
        position: absolute;
        top: 70px;
        left: 50%;
        transform: translateX(-50%) translateY(-20px);
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid var(--primary-glow);
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 12px;
        font-weight: 600;
        color: #fff;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        z-index: 250;
        opacity: 0;
        pointer-events: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }

      #toast.show {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
      }

      /* SUB-PART DEEP-DIVE POP-UP MODAL */
      .subpart-modal-box {
        width: min(940px, 94vw);
        max-height: 90vh;
        display: flex;
        flex-direction: column;
      }

      .subpart-ansi-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #7dd3fc;
        font-family: var(--font-mono);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.4px;
      }

      .subpart-modal-grid {
        display: grid;
        grid-template-columns: 420px 1fr;
        gap: 16px;
        padding: 16px 20px;
        overflow-y: auto;
      }

      @media (max-width: 860px) {
        .subpart-modal-grid {
          grid-template-columns: 1fr;
        }
      }

      .subpart-visual-col {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .subpart-view-tabs {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
      }

      .subpart-tab {
        padding: 7px 10px;
        border-radius: 6px;
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid var(--surface-border);
        color: var(--text-muted);
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
      }

      .subpart-tab.active {
        background: rgba(14, 165, 233, 0.22);
        border-color: var(--primary-glow);
        color: #e0f2fe;
      }

      .subpart-stage {
        position: relative;
        width: 100%;
        height: 310px;
        border-radius: 10px;
        background: radial-gradient(circle at 50% 42%, #1e293b 0%, #090e1a 100%);
        border: 1px solid rgba(148, 163, 184, 0.22);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      #subpart-turntable-canvas {
        width: 100%;
        height: 100%;
        display: block;
        cursor: grab;
      }

      #subpart-turntable-canvas:active {
        cursor: grabbing;
      }

      #subpart-svg-diagram {
        width: 100%;
        height: 100%;
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .subpart-stage-hint {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 23, 42, 0.85);
        padding: 3px 10px;
        border-radius: 12px;
        font-family: var(--font-mono);
        font-size: 10px;
        color: #94a3b8;
        pointer-events: none;
        white-space: nowrap;
      }

      .subpart-action-bar {
        display: flex;
        gap: 8px;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        background: rgba(14, 165, 233, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 8px;
        font-size: 11px;
        color: #bae6fd;
      }

      .subpart-info-col {
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .subpart-detail-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-left: 3px solid var(--primary-glow);
        border-radius: 8px;
        padding: 10px 12px;
      }

      .subpart-detail-card.warn {
        border-left-color: var(--accent-gold);
        background: rgba(245, 158, 11, 0.06);
      }

      .subpart-detail-title {
        font-family: var(--font-mono);
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #7dd3fc;
        margin-bottom: 5px;
      }

      .subpart-detail-card.warn .subpart-detail-title {
        color: #fcd34d;
      }

      .subpart-detail-card p {
        font-size: 12px;
        line-height: 1.52;
        color: #e2e8f0;
        margin: 0;
      }

      /* GROUND GRID X-RAY COLOR-SCALE GRADIENT LEGEND (IEEE STD 80) */
      #ground-legend {
        position: fixed;
        left: 296px;
        bottom: 20px;
        width: 340px;
        max-width: calc(100vw - 320px);
        background: rgba(15, 23, 42, 0.94);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(245, 158, 11, 0.55);
        border-radius: 10px;
        padding: 10px 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.65);
        z-index: 95;
        display: none;
        flex-direction: column;
        gap: 7px;
        pointer-events: auto;
      }

      .ground-legend-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 10.5px;
        font-weight: 700;
        color: #fbbf24;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .ground-colorbar {
        height: 12px;
        width: 100%;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        background: linear-gradient(90deg, #1d4ed8 0%, #06b6d4 26%, #10b981 52%, #facc15 76%, #ef4444 100%);
      }

      .ground-scale-ticks {
        display: flex;
        justify-content: space-between;
        font-family: var(--font-mono);
        font-size: 9px;
        color: #cbd5e1;
      }

      .ground-ieee-metrics {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4px 8px;
        font-family: var(--font-mono);
        font-size: 9.5px;
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 6px;
        padding: 6px 8px;
        color: #e2e8f0;
      }

      /* INTERACTIVE SWITCHING & INTERLOCK MATRIX */
      .switch-matrix {
        display: flex;
        flex-direction: column;
        gap: 5px;
        max-height: 210px;
        overflow-y: auto;
        padding-right: 2px;
      }

      .sw-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 5px;
        padding: 4px 6px;
        font-size: 10px;
      }

      .sw-label {
        font-family: var(--font-mono);
        font-weight: 600;
        color: #e2e8f0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .sw-btn {
        font-family: var(--font-mono);
        font-size: 9.5px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        border: 1px solid;
        cursor: pointer;
        flex-shrink: 0;
        transition: all 0.15s;
      }

      .sw-btn-closed {
        background: rgba(239, 68, 68, 0.2);
        border-color: #ef4444;
        color: #fca5a5;
      }

      .sw-btn-open {
        background: rgba(16, 185, 129, 0.2);
        border-color: #10b981;
        color: #6ee7b7;
      }

      /* ENCLOSURE COMPARISON MODAL TABLE & CALC CARDS */
      .enclosure-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
        color: #e2e8f0;
      }

      .enclosure-table th, .enclosure-table td {
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 7px 9px;
        text-align: left;
        vertical-align: top;
      }

      .enclosure-table th {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        font-family: var(--font-mono);
        font-size: 10px;
        text-transform: uppercase;
      }

      .calc-step-box {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(56, 189, 248, 0.24);
        border-left: 3px solid var(--accent-cyan);
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 11px;
        line-height: 1.5;
        color: #e2e8f0;
      }

      .drill-scenario-tabs {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        margin-bottom: 10px;
      }

      /* EMBEDDED MODAL FULL-EQUIPMENT EXPLODED VIEW CONTROLS */
      #subpart-modal-explode-controls {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 8px;
        padding: 8px 10px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 6px;
      }

      .modal-explode-row {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .modal-subpart-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        max-height: 76px;
        overflow-y: auto;
      }

      .modal-chip-btn {
        font-family: var(--font-mono);
        font-size: 9.5px;
        padding: 3px 7px;
        border-radius: 4px;
        border: 1px solid rgba(148, 163, 184, 0.28);
        background: rgba(30, 41, 59, 0.8);
        color: #cbd5e1;
        cursor: pointer;
        transition: all 0.15s;
      }

      .modal-chip-btn:hover {
        border-color: var(--accent-cyan);
        color: #fff;
      }

      .modal-chip-btn.active {
        background: rgba(14, 165, 233, 0.28);
        border-color: #38bdf8;
        color: #f8fafc;
        font-weight: 700;
      }

      /* HIGH-CONTRAST HV DANGER POP-UP MODAL */
      #hv-screen-flash {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 2450;
        display: none;
        border: 8px solid #ef4444;
        box-shadow: inset 0 0 65px rgba(239, 68, 68, 0.72);
        animation: hvFlashBorder 0.6s infinite alternate;
      }

      @keyframes hvFlashBorder {
        from { border-color: rgba(239, 68, 68, 0.95); box-shadow: inset 0 0 70px rgba(239, 68, 68, 0.78); }
        to { border-color: rgba(250, 204, 21, 0.75); box-shadow: inset 0 0 36px rgba(239, 68, 68, 0.35); }
      }

      #hv-danger-modal {
        z-index: 2500;
        background: rgba(15, 5, 5, 0.8);
      }

      .hv-danger-box {
        width: 720px;
        max-width: 96vw;
        max-height: 92vh;
        background: #180909;
        border: 3px solid #ef4444;
        box-shadow: 0 0 46px rgba(239, 68, 68, 0.62);
        padding: 0;
        overflow-y: auto;
      }

      .hv-hazard-stripes {
        height: 12px;
        background: repeating-linear-gradient(
          -45deg,
          #eab308,
          #eab308 14px,
          #111827 14px,
          #111827 28px
        );
      }

      .hv-danger-body {
        padding: 16px 20px;
        text-align: center;
      }

      .hv-danger-icon {
        font-size: 36px;
        line-height: 1;
        margin-bottom: 4px;
      }

      .hv-danger-badge {
        display: inline-block;
        font-family: var(--font-mono);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.08em;
        padding: 3px 10px;
        border-radius: 4px;
        background: #dc2626;
        color: #fff;
        margin-bottom: 6px;
      }

      .hv-danger-body h2 {
        margin: 0 0 6px 0;
        font-size: 17px;
        color: #fecaca;
        letter-spacing: 0.04em;
      }

      .hv-danger-desc {
        font-size: 11.5px;
        line-height: 1.45;
        color: #f8fafc;
        margin: 0 0 10px 0;
      }

      .hv-danger-metrics {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        background: rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(239, 68, 68, 0.42);
        border-radius: 6px;
        padding: 8px 10px;
        margin-bottom: 10px;
        text-align: left;
      }

      .hv-danger-metrics span {
        display: block;
        font-size: 9px;
        color: #94a3b8;
        text-transform: uppercase;
      }

      .hv-danger-metrics strong {
        font-family: var(--font-mono);
        font-size: 11px;
        color: #f8fafc;
      }

      .hv-consequence-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 9px;
        margin-bottom: 14px;
        text-align: left;
      }

      .hv-conseq-card {
        background: rgba(30, 10, 10, 0.85);
        border: 1px solid rgba(248, 113, 113, 0.35);
        border-radius: 7px;
        padding: 9px 10px;
        font-size: 10.5px;
        line-height: 1.45;
        color: #e2e8f0;
      }

      .hv-conseq-card h4 {
        margin: 0 0 5px 0;
        font-size: 11px;
        color: #fde047;
        font-family: var(--font-mono);
      }

      .hv-danger-actions {
        display: flex;
        justify-content: center;
        gap: 10px;
      }

      .hv-retreat-btn {
        background: #dc2626 !important;
        border-color: #f87171 !important;
        color: #fff !important;
        font-weight: 700;
        padding: 8px 16px;
      }

      /* POWER FLOW & SHORT-CIRCUIT ANALYSIS MODAL + VOLTAGE SCALING MODAL */
      .analysis-grid {
        display: grid;
        grid-template-columns: 310px 1fr;
        gap: 14px;
        align-items: start;
      }

      .analysis-panel {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid var(--surface-border);
        border-radius: 8px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .analysis-control label {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: #cbd5e1;
        margin-bottom: 4px;
        font-family: var(--font-mono);
      }

      .analysis-control input[type="range"] {
        width: 100%;
        accent-color: var(--accent-cyan);
      }

      .analysis-kpis {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
      }

      .analysis-kpi {
        background: rgba(2, 6, 23, 0.68);
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 6px;
        padding: 8px 10px;
      }

      .analysis-kpi .ak-lbl {
        font-size: 9.5px;
        color: #94a3b8;
        text-transform: uppercase;
      }

      .analysis-kpi .ak-val {
        font-family: var(--font-mono);
        font-size: 13px;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 2px;
      }

      .duty-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 5px;
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 700;
      }

      .duty-badge.pass {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid #10b981;
        color: #6ee7b7;
      }

      .duty-badge.fail {
        background: rgba(239, 68, 68, 0.25);
        border: 1px solid #ef4444;
        color: #fca5a5;
      }

      .vscale-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11.5px;
      }

      .vscale-table th, .vscale-table td {
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 7px 10px;
        text-align: left;
      }

      .vscale-table th {
        background: rgba(15, 23, 42, 0.9);
        color: #38bdf8;
        font-family: var(--font-mono);
        font-size: 10.5px;
      }

      .vscale-table tr.active-tier {
        background: rgba(2, 132, 199, 0.18);
      }

      /* ANIMATED LIVE POWER FLOW INSIDE SLD (DOCKED & EXPANDED) */
      .sld-flow-line {
        stroke-dasharray: 6 4;
        animation: sldMarch 0.75s linear infinite;
      }

      .sld-flow-line-fast {
        stroke-dasharray: 7 4;
        animation: sldMarch 0.25s linear infinite;
      }

      @keyframes sldMarch {
        to { stroke-dashoffset: -20; }
      }

      .sld-fault-pulse {
        animation: sldFaultPulse 0.45s ease-in-out infinite alternate;
      }

      @keyframes sldFaultPulse {
        from { r: 4px; opacity: 1.0; }
        to { r: 8.5px; opacity: 0.45; }
      }

      /* PINPOINT FAULT CURSOR & READOUT */
      body.pinpoint-fault-cursor #canvas3d,
      body.pinpoint-fault-cursor svg {
        cursor: crosshair !important;
      }

      .pinpoint-status-box {
        font-family: var(--font-mono);
        font-size: 10px;
        line-height: 1.4;
        padding: 6px 8px;
        border-radius: 5px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(248, 113, 113, 0.35);
        color: #cbd5e1;
      }

      /* EXPANDED MASTER SINGLE-LINE DIAGRAM WINDOW */
      #sld-expanded-modal {
        z-index: 2300;
      }

      .sld-exp-box {
        width: 86vw;
        height: 82vh;
        max-width: 1360px;
        background: rgba(8, 13, 26, 0.98);
        border: 1px solid rgba(56, 189, 248, 0.45);
        border-radius: 12px;
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.85);
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }

      .sld-exp-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 16px;
        background: rgba(15, 23, 42, 0.96);
        border-bottom: 1px solid rgba(148, 163, 184, 0.22);
        gap: 10px;
        flex-wrap: wrap;
      }

      .sld-exp-viewport {
        flex: 1;
        background: radial-gradient(circle at center, #091224 0%, #030712 100%);
        overflow: hidden;
        position: relative;
        cursor: grab;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .sld-exp-viewport:active {
        cursor: grabbing;
      }

      #sld-expanded-svg-container {
        width: 96%;
        height: 94%;
        transform-origin: center center;
        transition: transform 0.08s ease-out;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .sld-exp-telemetry-strip {
        padding: 9px 16px;
        background: rgba(15, 23, 42, 0.96);
        border-top: 1px solid rgba(148, 163, 184, 0.22);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        font-family: var(--font-mono);
        font-size: 11px;
        color: #e2e8f0;
        flex-wrap: wrap;
      }

      /* POWER QUALITY (PQ) SIMULATION LAB */
      .pq-osc-grid {
        display: grid;
        grid-template-columns: 1.08fr 0.92fr;
        gap: 12px;
      }

      .pq-canvas-wrap {
        background: #020617;
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 7px;
        padding: 8px;
      }

      .pq-scenario-tabs {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        margin-bottom: 10px;
      }

      .pq-diag-card {
        margin-top: 8px;
        padding: 9px 11px;
        background: rgba(15, 23, 42, 0.85);
        border-left: 3px solid #38bdf8;
        border-radius: 5px;
        font-size: 11px;
        color: #cbd5e1;
        line-height: 1.48;
      }

      /* WALK MODE RETICLE SAFE-INSPECTION PROMPT */
      #walk-inspect-prompt {
        position: fixed;
        bottom: 92px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(8, 20, 38, 0.94);
        border: 1.5px solid #38bdf8;
        box-shadow: 0 8px 28px rgba(2, 132, 199, 0.42);
        border-radius: 10px;
        padding: 9px 16px;
        font-family: var(--font-mono);
        font-size: 11.5px;
        font-weight: 600;
        color: #e0f2fe;
        z-index: 165;
        display: none;
        align-items: center;
        gap: 10px;
        pointer-events: none;
        backdrop-filter: blur(8px);
        white-space: nowrap;
      }

      #walk-inspect-prompt.scada-focus {
        border-color: #10b981;
        box-shadow: 0 8px 28px rgba(16, 185, 129, 0.42);
        color: #d1fae5;
      }

      .walk-key-badge {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 4px;
        background: rgba(56, 189, 248, 0.25);
        border: 1px solid #38bdf8;
        color: #fff;
        font-weight: 800;
      }

      /* INTERACTIVE MASTER SLD FAULT TYPE SELECTOR & CLEAR CONTROLS */
      .sld-fault-type-bar {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(244, 63, 94, 0.35);
        border-radius: 6px;
        padding: 2px 5px;
      }

      .sld-ft-pill {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.35);
        color: #cbd5e1;
        border-radius: 4px;
        padding: 3px 7px;
        font-size: 10px;
        font-weight: 700;
        font-family: var(--font-mono);
        cursor: pointer;
        transition: all 0.15s ease;
      }

      .sld-ft-pill:hover {
        border-color: #fb7185;
        color: #fff;
      }

      .sld-ft-pill.active {
        background: rgba(244, 63, 94, 0.32);
        border-color: #f43f5e;
        color: #fef08a;
        box-shadow: 0 0 8px rgba(244, 63, 94, 0.4);
      }

      .sld-clear-fault-btn {
        background: rgba(16, 185, 129, 0.22) !important;
        border-color: #10b981 !important;
        color: #a7f3d0 !important;
        font-weight: 700;
      }

      .sld-clear-fault-btn:hover {
        background: rgba(16, 185, 129, 0.38) !important;
        color: #ffffff !important;
      }

      /* DYNAMIC LAND AREA FOOTPRINT BADGE CARDS */
      .land-area-summary-box {
        margin-top: 8px;
        padding: 7px 9px;
        background: linear-gradient(135deg, rgba(8, 25, 48, 0.92) 0%, rgba(15, 23, 42, 0.88) 100%);
        border: 1px solid rgba(56, 189, 248, 0.36);
        border-radius: 6px;
        font-family: var(--font-mono);
        font-size: 10px;
        color: #e2e8f0;
        line-height: 1.45;
      }

      .land-area-summary-box .la-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 6px;
      }

      .land-area-summary-box .la-val {
        color: #38bdf8;
        font-weight: 700;
      }

      .land-area-summary-box .la-ha {
        color: #34d399;
        font-weight: 700;
      }

      /* RELAY SETTINGS SCHEDULE & TCC LOG-LOG COORDINATION LAB */
      .tcc-topo-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        align-items: center;
        margin-bottom: 8px;
        padding: 6px 8px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 7px;
      }

      .tcc-topo-pill {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.32);
        color: #cbd5e1;
        border-radius: 5px;
        padding: 4px 8px;
        font-size: 10.5px;
        font-weight: 700;
        font-family: var(--font-mono);
        cursor: pointer;
        transition: all 0.15s ease;
      }

      .tcc-topo-pill:hover {
        border-color: #38bdf8;
        color: #fff;
      }

      .tcc-topo-pill.active {
        background: rgba(14, 165, 233, 0.28);
        border-color: #38bdf8;
        color: #fef08a;
        box-shadow: 0 0 8px rgba(56, 189, 248, 0.35);
      }

      .tcc-lab-layout {
        display: grid;
        grid-template-columns: 1.25fr 0.75fr;
        gap: 10px;
        align-items: start;
      }

      .tcc-canvas-wrap {
        background: #020617;
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 8px;
        padding: 8px;
      }

      .tcc-verdict-banner {
        margin-top: 6px;
        padding: 7px 10px;
        border-radius: 6px;
        font-family: var(--font-mono);
        font-size: 10.5px;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .tcc-verdict-ok {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid #10b981;
        color: #a7f3d0;
      }

      .tcc-verdict-warn {
        background: rgba(244, 63, 94, 0.18);
        border: 1px solid #f43f5e;
        color: #fecdd3;
      }

      .relay-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
        gap: 8px;
        margin-top: 10px;
      }

      .relay-setting-card {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 7px;
        padding: 9px 10px;
      }

      .relay-setting-card.focused {
        border-color: #f59e0b;
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.28);
      }

      .relay-setting-card h5 {
        font-size: 11px;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
      }

      .relay-schedule-table {
        width: 100%;
        border-collapse: collapse;
        font-family: var(--font-mono);
        font-size: 9.8px;
      }

      .relay-schedule-table td {
        padding: 2.5px 4px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        color: #cbd5e1;
      }

      .relay-schedule-table td:last-child {
        text-align: right;
        color: #fef08a;
        font-weight: 700;
      }

      /* COMPACT HEADER TELEMETRY & FLOATING DRAWER */
      .telem-compact-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1 1 auto;
        min-width: 0;
        justify-content: flex-start;
        overflow: hidden;
      }

      .grid-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.14);
        border: 1px solid rgba(52, 211, 153, 0.45);
        font-family: var(--font-mono);
        font-size: 10.5px;
        font-weight: 700;
        color: #a7f3d0;
        white-space: nowrap;
        flex-shrink: 0;
      }

      .grid-status-pill.fault {
        background: rgba(239, 68, 68, 0.2);
        border-color: rgba(248, 113, 113, 0.65);
        color: #fecaca;
      }

      .grid-status-pill.deenergized {
        background: rgba(245, 158, 11, 0.16);
        border-color: rgba(251, 191, 36, 0.5);
        color: #fde68a;
      }

      #btn-telem-drawer {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 11px;
        border-radius: 7px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.22), rgba(15, 23, 42, 0.92));
        border: 1px solid rgba(56, 189, 248, 0.55);
        color: #e0f2fe;
        font-family: var(--font-sans);
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
        flex-shrink: 0;
        transition: all 0.15s ease;
      }

      #btn-telem-drawer:hover,
      #btn-telem-drawer.active {
        background: rgba(14, 165, 233, 0.34);
        border-color: #38bdf8;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
      }

      #live-telemetry-drawer {
        display: none;
        position: fixed;
        top: calc(var(--header-h) + 8px);
        left: 50%;
        transform: translateX(-50%);
        width: min(880px, calc(100vw - 32px));
        max-height: calc(100vh - var(--header-h) - 24px);
        overflow-y: auto;
        background: rgba(9, 14, 26, 0.96);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.45);
        border-radius: 12px;
        padding: 12px 14px 14px;
        z-index: 320;
        box-shadow: 0 18px 46px rgba(0, 0, 0, 0.72), 0 0 0 1px rgba(255, 255, 255, 0.05);
      }

      #live-telemetry-drawer.open {
        display: block;
      }

      .telem-drawer-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 8px;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.22);
      }

      .telem-drawer-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: 0.4px;
        text-transform: uppercase;
      }

      .telem-drawer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
        gap: 8px;
      }

      .telem-metric-card {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 8px;
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .telem-metric-card.hv { border-left: 3px solid #22d3ee; }
      .telem-metric-card.lv { border-left: 3px solid #f59e0b; }
      .telem-metric-card.pwr { border-left: 3px solid #10b981; }
      .telem-metric-card.gnd { border-left: 3px solid #a855f7; }

      .telem-metric-card .lbl {
        font-size: 9.5px;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.4px;
      }

      .telem-metric-card .val {
        font-family: var(--font-mono);
        font-size: 13px;
        font-weight: 800;
        color: #f8fafc;
      }

      .telem-metric-card .sub {
        font-family: var(--font-mono);
        font-size: 9.8px;
        color: #94a3b8;
      }

      /* RELAY PROTECTION SCHEMATIC & 3D ZONE HIGHLIGHT */
      .relay-schematic-box {
        margin-top: 10px;
        background: #040914;
        border: 1px solid rgba(56, 189, 248, 0.38);
        border-radius: 8px;
        padding: 10px 12px;
      }

      .relay-schematic-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 8px;
      }

      .relay-schematic-header h5 {
        margin: 0;
        font-size: 11px;
        font-weight: 800;
        color: #67e8f9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .btn-zone-3d {
        background: rgba(14, 165, 233, 0.2);
        border: 1px solid #38bdf8;
        color: #e0f2fe;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        cursor: pointer;
      }

      .btn-zone-3d.active {
        background: rgba(244, 63, 94, 0.28);
        border-color: #fb7185;
        color: #ffe4e6;
        box-shadow: 0 0 10px rgba(244, 63, 94, 0.35);
      }

      /* FLISR DISTRIBUTION LOOP STATUS */
      .flisr-status-box {
        margin-top: 4px;
        padding: 6px 8px;
        border-radius: 6px;
        background: rgba(6, 78, 59, 0.25);
        border: 1px solid rgba(52, 211, 153, 0.35);
        font-family: var(--font-mono);
        font-size: 9.8px;
        color: #a7f3d0;
        line-height: 1.35;
      }

      /* TARGET SUBSTATION (A vs. TIE B) SELECTOR */
      .substation-target-toggle {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
      }

      .btn-sub-target {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 2px;
        padding: 7px 8px;
        border-radius: 7px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.25);
        color: #cbd5e1;
        font-size: 10.5px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.16s ease;
        text-align: left;
      }

      .btn-sub-target:hover {
        border-color: rgba(56, 189, 248, 0.55);
        background: rgba(14, 165, 233, 0.12);
      }

      .btn-sub-target.active {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(14, 165, 233, 0.22));
        border-color: #10b981;
        color: #ecfdf5;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.28);
      }

      .btn-sub-target small {
        font-family: var(--font-mono);
        font-size: 9px;
        font-weight: 500;
        color: #94a3b8;
      }

      .btn-sub-target.active small {
        color: #6ee7b7;
      }
    </style>
    """

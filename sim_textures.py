"""
sim_textures.py
Procedural HTML5 Canvas Texture Generators for Three.js.
Ensures zero external image file dependencies!
"""

def get_js_procedural_textures():
    return """
    const TextureGen = {
      createGravelTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Base dark gravel gray
        ctx.fillStyle = '#262930';
        ctx.fillRect(0, 0, 512, 512);

        // Multi-toned gravel specks
        const colors = ['#1e2026', '#323640', '#414754', '#555d6e', '#191b20', '#3b404d'];
        for (let i = 0; i < 40000; i++) {
          const x = Math.random() * 512;
          const y = Math.random() * 512;
          const r = Math.random() * 2.2 + 0.5;
          ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)];
          ctx.beginPath();
          ctx.arc(x, y, r, 0, Math.PI * 2);
          ctx.fill();
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set(16, 16);
        return texture;
      },

      createConcreteTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#64748b';
        ctx.fillRect(0, 0, 256, 256);

        // Noise
        for (let i = 0; i < 8000; i++) {
          const x = Math.random() * 256;
          const y = Math.random() * 256;
          ctx.fillStyle = Math.random() > 0.5 ? '#475569' : '#94a3b8';
          ctx.fillRect(x, y, 1.5, 1.5);
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        return texture;
      },

      createHazardSignTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');

        // White background with red border
        ctx.fillStyle = '#f8fafc';
        ctx.fillRect(0, 0, 512, 256);

        // Red danger header
        ctx.fillStyle = '#dc2626';
        ctx.fillRect(10, 10, 492, 70);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 42px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('DANGER', 256, 60);

        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 28px sans-serif';
        ctx.fillText('HIGH VOLTAGE 69,000 V', 256, 130);

        ctx.font = '600 20px sans-serif';
        ctx.fillStyle = '#334155';
        ctx.fillText('AUTHORIZED PERSONNEL ONLY', 256, 175);
        ctx.font = '500 15px sans-serif';
        ctx.fillText('OSH RULE 1210 / IEEE STD 80 COMPLIANT', 256, 215);

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
      },

      createGroundHeatmapTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // IEEE Std 80 GPR / Touch-Potential Blue -> Cyan -> Green -> Yellow -> Red gradient
        const bgGrad = ctx.createRadialGradient(256, 256, 30, 256, 256, 265);
        bgGrad.addColorStop(0.0, 'rgba(239, 68, 68, 0.72)');   // Red: Peak GPR near faulted bay/TR-01
        bgGrad.addColorStop(0.28, 'rgba(250, 204, 21, 0.58)'); // Yellow: Inner mesh potential Em
        bgGrad.addColorStop(0.54, 'rgba(16, 185, 129, 0.48)'); // Green: Safe inner yard mesh
        bgGrad.addColorStop(0.78, 'rgba(6, 182, 212, 0.34)');  // Cyan: Perimeter transition
        bgGrad.addColorStop(1.0, 'rgba(37, 99, 235, 0.16)');   // Blue: Remote low potential

        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, 512, 512);

        // Localized high-potential hotspots at TR-01 NGR / CB fault ground nodes
        [[185, 256, 75], [305, 256, 65]].forEach(([hx, hy, hr]) => {
          const spot = ctx.createRadialGradient(hx, hy, 4, hx, hy, hr);
          spot.addColorStop(0, 'rgba(239, 68, 68, 0.65)');
          spot.addColorStop(0.5, 'rgba(245, 158, 11, 0.35)');
          spot.addColorStop(1, 'rgba(245, 158, 11, 0)');
          ctx.fillStyle = spot;
          ctx.fillRect(0, 0, 512, 512);
        });

        // Overlay grid lines for IEEE 80 buried copper mesh
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.38)';
        ctx.lineWidth = 1.4;
        for (let i = 0; i <= 512; i += 512 / 12) {
          ctx.beginPath();
          ctx.moveTo(i, 0); ctx.lineTo(i, 512);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(0, i); ctx.lineTo(512, i);
          ctx.stroke();
        }

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
      },

      createFenceTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 64;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');

        ctx.clearRect(0, 0, 64, 64);
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1.5;

        // Diamond mesh pattern
        ctx.beginPath();
        ctx.moveTo(32, 0); ctx.lineTo(64, 32); ctx.lineTo(32, 64); ctx.lineTo(0, 32); ctx.closePath();
        ctx.stroke();

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set(40, 4);
        return texture;
      },

      createRelayPanelTexture: function(panelTitle, relayModel, ansiList) {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Industrial ANSI 61 Gray Steel Panel
        ctx.fillStyle = '#475569';
        ctx.fillRect(0, 0, 256, 512);
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 6;
        ctx.strokeRect(3, 3, 250, 506);

        // Top Nameplate
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(16, 16, 224, 34);
        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 14px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(panelTitle || 'PROTECTION PANEL', 128, 38);

        // Microprocessor Numerical Relay Chassis
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(24, 70, 208, 120);
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 2;
        ctx.strokeRect(24, 70, 208, 120);

        // Relay LCD Screen
        ctx.fillStyle = '#064e3b';
        ctx.fillRect(38, 86, 118, 42);
        ctx.fillStyle = '#34d399';
        ctx.font = 'bold 11px monospace';
        ctx.textAlign = 'left';
        ctx.fillText(relayModel || 'SEL-487E', 44, 102);
        ctx.font = '10px monospace';
        ctx.fillText(ansiList || '87T / 50 / 51', 44, 118);

        // LED Status Target Array
        const ledColors = ['#10b981', '#10b981', '#ef4444', '#f59e0b', '#10b981', '#38bdf8'];
        for (let i = 0; i < 6; i++) {
          ctx.fillStyle = ledColors[i];
          ctx.beginPath();
          ctx.arc(178 + (i % 2) * 24, 92 + Math.floor(i / 2) * 16, 5, 0, Math.PI * 2);
          ctx.fill();
        }

        // ANSI 86 Lockout Relay with Orange Flag
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(32, 212, 84, 70);
        ctx.fillStyle = '#f97316';
        ctx.fillRect(42, 224, 24, 14);
        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 10px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('ANSI 86', 74, 266);

        // Pistol-Grip Breaker Control Switch + Red/Green Indicator Lamps
        ctx.fillStyle = '#ef4444';
        ctx.beginPath(); ctx.arc(154, 232, 9, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#10b981';
        ctx.beginPath(); ctx.arc(198, 232, 9, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#0f172a';
        ctx.beginPath(); ctx.arc(176, 262, 14, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#cbd5e1';
        ctx.fillRect(172, 244, 8, 36);

        // Mimic Bus Schematic
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(40, 330); ctx.lineTo(216, 330);
        ctx.moveTo(128, 330); ctx.lineTo(128, 430);
        ctx.stroke();

        ctx.fillStyle = '#ef4444';
        ctx.fillRect(114, 362, 28, 28);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px monospace';
        ctx.fillText('52', 128, 381);

        // Test Blocks (FT-1 Switches)
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(36, 448, 184, 36);
        for (let x = 46; x < 210; x += 18) {
          ctx.fillStyle = '#94a3b8';
          ctx.fillRect(x, 456, 10, 20);
        }

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
      },

      createScadaScreenTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#020617';
        ctx.fillRect(0, 0, 512, 256);
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 3;
        ctx.strokeRect(4, 4, 504, 248);

        // Header
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(6, 6, 500, 32);
        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 14px monospace';
        ctx.fillText('SCADA HMI - OBRERO 69/13.8kV SUBSTATION', 16, 27);

        // Live SLD Graphic on SCADA Screen
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(40, 80); ctx.lineTo(470, 80);
        ctx.moveTo(160, 80); ctx.lineTo(160, 190);
        ctx.moveTo(350, 80); ctx.lineTo(350, 190);
        ctx.stroke();

        // Breakers
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(148, 110, 24, 24);
        ctx.fillRect(338, 110, 24, 24);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px monospace';
        ctx.fillText('52-1', 146, 150);
        ctx.fillText('52-2', 336, 150);

        // Telemetry table box
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(20, 195, 472, 46);
        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 13px monospace';
        ctx.fillText('V_BUS: 69.0 kV  |  I_LOAD: 348.9 A  |  41.7 MVA  |  60.00 Hz', 30, 223);

        return new THREE.CanvasTexture(canvas);
      },

      createAnnunciatorTexture: function() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, 512, 128);

        const alarms = [
          { lbl: '87T DIFF TRIP', col: '#334155', txt: '#94a3b8' },
          { lbl: 'BUCHHOLZ 63', col: '#334155', txt: '#94a3b8' },
          { lbl: 'SF6 LOW LOCK', col: '#334155', txt: '#94a3b8' },
          { lbl: '125VDC NORMAL', col: '#065f46', txt: '#34d399' },
          { lbl: 'OLTC AUTO', col: '#075985', txt: '#38bdf8' },
          { lbl: 'SCADA ONLINE', col: '#065f46', txt: '#34d399' },
          { lbl: 'OIL TEMP HIGH', col: '#78350f', txt: '#fbbf24' },
          { lbl: '50/51 PICKUP', col: '#334155', txt: '#94a3b8' }
        ];

        alarms.forEach((a, idx) => {
          const colIdx = idx % 4;
          const rowIdx = Math.floor(idx / 4);
          const x = 10 + colIdx * 124;
          const y = 10 + rowIdx * 56;
          ctx.fillStyle = a.col;
          ctx.fillRect(x, y, 116, 48);
          ctx.strokeStyle = '#475569';
          ctx.lineWidth = 2;
          ctx.strokeRect(x, y, 116, 48);
          ctx.fillStyle = a.txt;
          ctx.font = 'bold 12px monospace';
          ctx.textAlign = 'center';
          ctx.fillText(a.lbl, x + 58, y + 29);
        });

        return new THREE.CanvasTexture(canvas);
      },

      createGaugeDialTexture: function(mode) {
        const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#f8fafc';
        ctx.beginPath();
        ctx.arc(64, 64, 60, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 6;
        ctx.stroke();

        if (mode === 'sf6') {
          // Red, Yellow, Green Pressure Arcs
          ctx.lineWidth = 14;
          ctx.strokeStyle = '#ef4444';
          ctx.beginPath(); ctx.arc(64, 64, 42, Math.PI * 0.8, Math.PI * 1.15); ctx.stroke();
          ctx.strokeStyle = '#f59e0b';
          ctx.beginPath(); ctx.arc(64, 64, 42, Math.PI * 1.15, Math.PI * 1.4); ctx.stroke();
          ctx.strokeStyle = '#10b981';
          ctx.beginPath(); ctx.arc(64, 64, 42, Math.PI * 1.4, Math.PI * 2.1); ctx.stroke();

          ctx.fillStyle = '#0f172a';
          ctx.font = 'bold 13px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('SF6 MPa', 64, 96);
        } else if (mode === 'oltc') {
          ctx.fillStyle = '#0f172a';
          ctx.font = 'bold 18px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('TAP 9N', 64, 58);
          ctx.font = 'bold 11px monospace';
          ctx.fillText('69.0 kV', 64, 82);
        } else if (mode === 'surge') {
          ctx.fillStyle = '#0f172a';
          ctx.fillRect(20, 26, 88, 30);
          ctx.fillStyle = '#10b981';
          ctx.font = 'bold 16px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('0014', 64, 47);
          ctx.fillStyle = '#334155';
          ctx.font = 'bold 11px monospace';
          ctx.fillText('68 uA LEAK', 64, 88);
        } else {
          // Oil level dial
          ctx.strokeStyle = '#0284c7';
          ctx.lineWidth = 10;
          ctx.beginPath(); ctx.arc(64, 64, 40, Math.PI * 0.9, Math.PI * 2.1); ctx.stroke();
          ctx.fillStyle = '#0f172a';
          ctx.font = 'bold 13px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('25°C OIL', 64, 96);
        }

        // Needle
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(64, 64);
        ctx.lineTo(92, 36);
        ctx.stroke();

        return new THREE.CanvasTexture(canvas);
      }
    };
    """

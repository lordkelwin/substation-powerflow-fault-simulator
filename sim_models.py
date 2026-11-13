"""
sim_models.py
Procedural 3D Mesh Builders in Three.js for EE 415 Substation Simulator.
Includes procedural geometries for all 7 primary substation apparatus,
sub-assemblies, busbar topologies, grounding grid, and rolling sphere canopy.
"""

def get_js_models():
    return """
    // Global Materials Dictionary with tuned PBR metalness/roughness for realistic field appearance
    const MatLib = {
      steelLattice: new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.58, roughness: 0.38 }),
      galvanizedSteel: new THREE.MeshStandardMaterial({ color: 0xb8c4d0, metalness: 0.62, roughness: 0.34 }),
      darkSteel: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.72, roughness: 0.36 }),
      porcelainBrown: new THREE.MeshStandardMaterial({ color: 0x4a2511, roughness: 0.14, metalness: 0.10 }),
      porcelainGray: new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.18, metalness: 0.08 }),
      siliconePolymer: new THREE.MeshStandardMaterial({ color: 0xa8b3c2, roughness: 0.32, metalness: 0.04 }),
      aluminumBus: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.82, roughness: 0.22 }),
      copperConductor: new THREE.MeshStandardMaterial({ color: 0xb45309, metalness: 0.78, roughness: 0.28 }),
      silverContact: new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.88, roughness: 0.14 }),
      transformerTank: new THREE.MeshStandardMaterial({ color: 0x3b4958, metalness: 0.38, roughness: 0.44 }),
      radiatorFin: new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.42, roughness: 0.48 }),
      crgoCoreSteel: new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.72, roughness: 0.40 }),
      copperWinding: new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.82, roughness: 0.22 }),
      glassBreather: new THREE.MeshPhysicalMaterial({ color: 0xbae6fd, transparent: true, opacity: 0.45, roughness: 0.10, metalness: 0.1 }),
      cabinetGlass: new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.30, roughness: 0.08, metalness: 0.05 }),
      silicaBlue: new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.75 }),
      concrete: new THREE.MeshStandardMaterial({ color: 0x78909c, roughness: 0.88, metalness: 0.05 }),
      concretePad: new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.88, metalness: 0.05 }),
      fireWallConcrete: new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.85, metalness: 0.05 }),
      groundCopper: new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.72, roughness: 0.28, emissive: 0xb45309, emissiveIntensity: 0.25 }),
      brassContact: new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.70, roughness: 0.28 }),
      znoCeramic: new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.48, metalness: 0.25 }),
      fiberglassTube: new THREE.MeshStandardMaterial({ color: 0xa7f3d0, transparent: true, opacity: 0.65, roughness: 0.32 }),
      relayPanelSteel: new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.45, roughness: 0.48 }),
      yellowHighlight: new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.35, metalness: 0.25 }),
      hazardRed: new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.35, metalness: 0.2 }),
      safeGreen: new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.35, metalness: 0.2 }),
      glowElectric: new THREE.MeshBasicMaterial({ color: 0x00f0ff }),
      glowFault: new THREE.MeshBasicMaterial({ color: 0xef4444 }),
      phaseA: new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.35, metalness: 0.2 }), // Phase A (Red)
      phaseB: new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.35, metalness: 0.2 }), // Phase B (Yellow)
      phaseC: new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.35, metalness: 0.2 }), // Phase C (Blue)
      groundHeatmapMat: null // Initialized dynamically with canvas texture
    };

    // Dynamic Multi-Voltage Substation Spatial Layouts (IEEE Std 1427 / IEEE C2 / IEC 60071 Compliant)
    // Computes equipment bay bounds FIRST for every (voltageClass x scheme x enclosure), then places civil roads, Control House & fence strictly clear!
    function getVoltageSpec(vClass) {
      const id = vClass || (typeof AppState !== 'undefined' && AppState.voltageClass) || '69_13';
      return (typeof VOLTAGE_CLASSES !== 'undefined' && VOLTAGE_CLASSES[id]) || {
        id: '69_13', shortLabel: '69 / 13.8 kV', hvKv: 69.0, lvKv: 13.8, mva: 41.7,
        phaseSpacing: 2.4, bayPhaseZ: 3.5, insScale: 1.0, shedsCount: 9, hvShedsCount: 14,
        mad: 2.2, coronaRings: false, twinBundle: false
      };
    }

    const SUBSTATION_LAYOUTS = {
      single: {
        scheme: 'single',
        gantryX: -22.0, laX: -16.5, ctX: -11.5, dsX: -6.0, dsZ: 0, dsRot: 0,
        cbX: 0.0, cbZ: 0, cbRot: 0,
        dsBX: 6.0,
        txX: 16.5, txZ: 0,
        priMinZ: -8.0, priMaxZ: 8.0,
        gisW: 9.2, gisL: 11.4
      },
      maintransfer: {
        scheme: 'maintransfer',
        gantryX: -22.0, laX: -16.5, ctX: -11.5, dsX: -6.0, dsZ: 0, dsRot: 0,
        cbX: 0.0, cbZ: 0, cbRot: 0,
        dsBX: 5.5,
        tieX: 14.0,
        txX: 25.5, txZ: 0,
        priMinZ: -17.0, priMaxZ: 17.0,
        gisW: 12.2, gisL: 14.2
      },
      ring: {
        scheme: 'ring',
        gantryX: -25.0, laX: -20.0, ctX: -15.0, dsX: -10.0, dsZ: 0, dsRot: 0,
        cbX: 0.0, cbZ: 0, cbRot: Math.PI / 2,
        ringX1: 0.0, ringX2: 22.0, ringZ1: -16.0, ringZ2: 16.0,
        txX: 34.0, txZ: 0,
        priMinZ: -21.5, priMaxZ: 21.5,
        gisW: 13.8, gisL: 15.8
      },
      breakerhalf: {
        scheme: 'breakerhalf',
        gantryX: -25.0, laX: -20.0, ctX: -15.0, dsX: -10.0, dsZ: 0, dsRot: 0,
        cbX: 4.0, cbZ: 0, cbRot: Math.PI / 2,
        busAZ: -27.5, busBZ: 27.5,
        txX: 22.0, txZ: 0,
        priMinZ: -32.0, priMaxZ: 32.0,
        gisW: 12.8, gisL: 18.2
      },
      doublebreaker: {
        scheme: 'doublebreaker',
        gantryX: -27.0, laX: -22.0, ctX: -17.0, dsX: -12.0, dsZ: 0, dsRot: 0,
        cbX: -2.0, cbZ: -11.5, cbRot: Math.PI / 2,
        bay2X: 11.5,
        busAZ: -25.0, busBZ: 25.0,
        txX: 29.0, txZ: 0,
        priMinZ: -30.5, priMaxZ: 30.5,
        gisW: 15.6, gisL: 19.6
      }
    };

    function finalizeCivilLayout(cfg) {
      const vSpec = cfg.vSpec || getVoltageSpec(cfg.voltageClass);
      const padMargin = cfg.enclosure === 'gis' ? 2.0 : (vSpec.insScale > 1.8 ? 5.2 : 4.0);
      const eqMinX = cfg.gantryX - padMargin;
      const eqMaxX = cfg.fdrGantryX + padMargin;
      const secMinZ = Math.min(cfg.capZ - 3.6 * (vSpec.lvKv > 40 ? 1.25 : 1.0), cfg.fdr1Z - 4.0 * (vSpec.lvKv > 40 ? 1.2 : 1.0));
      const secMaxZ = Math.max(cfg.sstZ + 3.8, cfg.fdr2Z + 4.0 * (vSpec.lvKv > 40 ? 1.2 : 1.0));
      const priMinZ = cfg.enclosure === 'gis' ? -(cfg.gisL / 2 + 1.8) : cfg.priMinZ;
      const priMaxZ = cfg.enclosure === 'gis' ? (cfg.gisL / 2 + 1.8) : cfg.priMaxZ;
      const eqMinZ = Math.min(priMinZ, secMinZ);
      const eqMaxZ = Math.max(priMaxZ, secMaxZ);

      // Perimeter Maintenance Road (>= 4.6 m clear outside ALL equipment pads!) & Heavy-Haul TR-01 Spur
      const roadW = 4.0;
      const setback = 4.6;
      const roadNorthZ = eqMinZ - setback - roadW / 2;
      const roadSouthZ = eqMaxZ + setback + roadW / 2;
      const roadWestX = eqMinX - setback - roadW / 2;
      const roadEastX = eqMaxX + setback + roadW / 2;

      // Control House placed cleanly South of South Access Road with >= 2.6 m road setback (zero bay overlap in ALL 12 x 3 cases!)
      const ctrlX = cfg.txX + 2.5;
      const ctrlZ = roadSouthZ + roadW / 2 + 2.6 + 6.4;

      const yardMinX = roadWestX - roadW / 2 - 2.4;
      const yardMaxX = roadEastX + roadW / 2 + 2.4;
      const yardMinZ = roadNorthZ - roadW / 2 - 2.4;
      const yardMaxZ = Math.max(roadSouthZ + roadW / 2, ctrlZ + 6.4) + 2.8;

      return Object.assign(cfg, {
        vSpec,
        eqBounds: { minX: eqMinX, maxX: eqMaxX, minZ: eqMinZ, maxZ: eqMaxZ },
        roads: { roadW, northZ: roadNorthZ, southZ: roadSouthZ, westX: roadWestX, eastX: roadEastX },
        ctrlX, ctrlZ,
        yardMinX, yardMaxX, yardMinZ, yardMaxZ,
        yardCenterX: (yardMinX + yardMaxX) / 2,
        yardCenterZ: (yardMinZ + yardMaxZ) / 2,
        yardW: yardMaxX - yardMinX,
        yardL: yardMaxZ - yardMinZ
      });
    }

    function getBusLayoutConfig(scheme, enclosureType = 'ais', vClass) {
      const vSpec = getVoltageSpec(vClass);
      const base = SUBSTATION_LAYOUTS[scheme] || SUBSTATION_LAYOUTS.single;
      const xScale = vSpec.id === '230_138' ? 1.46 : (vSpec.id === '138_69' ? 1.24 : 1.0);
      const zScale = vSpec.id === '230_138' ? 1.44 : (vSpec.id === '138_69' ? 1.22 : 1.0);
      const lvScale = vSpec.lvKv >= 138 ? 1.38 : (vSpec.lvKv >= 69 ? 1.18 : 1.0);

      if (enclosureType === 'gis') {
        const gisTxShift = ({ single: 10.5, maintransfer: 12.2, ring: 13.5, breakerhalf: 13.0, doublebreaker: 15.0 }[base.scheme] || 10.5) * (0.85 + 0.15 * xScale);
        const txX = gisTxShift;
        return finalizeCivilLayout({
          scheme: base.scheme,
          voltageClass: vSpec.id,
          vSpec,
          enclosure: 'gis',
          gantryX: -10.5 * xScale, laX: -6.8 * xScale, ctX: -4.2 * xScale, dsX: -2.2 * xScale, dsZ: base.dsZ || 0, dsRot: base.dsRot || 0,
          cbX: 0.0, cbZ: base.cbZ ? +(base.cbZ * 0.45 * zScale).toFixed(2) : 0, cbRot: base.cbRot || 0, dsBX: 2.2 * xScale,
          bay2X: base.bay2X !== undefined ? +(4.5 * xScale).toFixed(2) : undefined,
          tieX: 4.5 * xScale,
          ringX1: -1.5 * xScale, ringX2: 3.5 * xScale, ringZ1: -6.5 * zScale, ringZ2: 6.5 * zScale,
          busAZ: -12.0 * zScale, busBZ: 12.0 * zScale,
          gisX: -1.5, gisW: base.gisW * (0.9 + 0.1 * xScale), gisL: base.gisL * (0.9 + 0.1 * zScale),
          txX, txZ: 0,
          priMinZ: -(base.gisL / 2 + 1.8) * zScale, priMaxZ: (base.gisL / 2 + 1.8) * zScale,
          secArresterX: txX + 6.4 * lvScale, secDsAX: txX + 8.6 * lvScale, secCbX: txX + 12.0 * lvScale, secDsBX: txX + 15.2 * lvScale, secBusX: txX + 19.2 * lvScale,
          fdr1Z: -9.5 * lvScale, fdr2Z: 5.0 * lvScale, fdrGantryX: txX + 36.5 * lvScale,
          capX: txX + 15.5 * lvScale, capZ: -18.5 * lvScale,
          sstX: txX + 27.5 * lvScale, sstZ: 16.5 * lvScale
        });
      }

      const scaledBase = {
        scheme: base.scheme,
        voltageClass: vSpec.id,
        vSpec,
        gantryX: +(base.gantryX * xScale).toFixed(2),
        laX: +(base.laX * xScale).toFixed(2),
        ctX: +(base.ctX * xScale).toFixed(2),
        dsX: +(base.dsX * xScale).toFixed(2),
        dsZ: base.dsZ,
        dsRot: base.dsRot,
        cbX: +(base.cbX * xScale).toFixed(2),
        cbZ: +(base.cbZ * zScale).toFixed(2),
        cbRot: base.cbRot,
        bay2X: base.bay2X !== undefined ? +(base.bay2X * xScale).toFixed(2) : undefined,
        dsBX: base.dsBX !== undefined ? +(base.dsBX * xScale).toFixed(2) : undefined,
        tieX: base.tieX !== undefined ? +(base.tieX * xScale).toFixed(2) : undefined,
        ringX1: base.ringX1 !== undefined ? +(base.ringX1 * xScale).toFixed(2) : undefined,
        ringX2: base.ringX2 !== undefined ? +(base.ringX2 * xScale).toFixed(2) : undefined,
        ringZ1: base.ringZ1 !== undefined ? +(base.ringZ1 * zScale).toFixed(2) : undefined,
        ringZ2: base.ringZ2 !== undefined ? +(base.ringZ2 * zScale).toFixed(2) : undefined,
        busAZ: base.busAZ !== undefined ? +(base.busAZ * zScale).toFixed(2) : undefined,
        busBZ: base.busBZ !== undefined ? +(base.busBZ * zScale).toFixed(2) : undefined,
        txX: +(base.txX * xScale).toFixed(2),
        txZ: base.txZ,
        priMinZ: +(base.priMinZ * zScale).toFixed(2),
        priMaxZ: +(base.priMaxZ * zScale).toFixed(2),
        gisW: base.gisW,
        gisL: base.gisL
      };

      const txX = scaledBase.txX;
      if (enclosureType === 'indoor') {
        return finalizeCivilLayout(Object.assign({}, scaledBase, {
          enclosure: 'indoor',
          secArresterX: txX + 5.8 * lvScale,
          secDsAX: txX + 8.0 * lvScale,
          secCbX: txX + 11.0 * lvScale,
          secDsBX: txX + 14.0 * lvScale,
          secBusX: txX + 17.5 * lvScale,
          fdr1Z: -8.0 * lvScale,
          fdr2Z: 4.8 * lvScale,
          fdrGantryX: txX + 31.0 * lvScale,
          capX: txX + 13.5 * lvScale,
          capZ: -17.5 * lvScale,
          sstX: txX + 23.5 * lvScale,
          sstZ: 16.5 * lvScale
        }));
      }

      return finalizeCivilLayout(Object.assign({}, scaledBase, {
        enclosure: 'ais',
        secArresterX: txX + 6.8 * lvScale,
        secDsAX: txX + 9.2 * lvScale,
        secCbX: txX + 12.8 * lvScale,
        secDsBX: txX + 16.4 * lvScale,
        secBusX: txX + 20.6 * lvScale,
        fdr1Z: -10.0 * lvScale,
        fdr2Z: 5.0 * lvScale,
        fdrGantryX: txX + 38.5 * lvScale,
        capX: txX + 16.2 * lvScale,
        capZ: -18.5 * lvScale,
        sstX: txX + 28.5 * lvScale,
        sstZ: 16.8 * lvScale
      }));
    }

    // Helper: Single source of truth for terminal heights, phase spacings & TR-01 stud coords across all 3 voltage classes
    function getPrimaryTerminals(L) {
      const vSpec = (L && L.vSpec) || getVoltageSpec(L && L.voltageClass);
      const s = vSpec.insScale || 1.0;
      const pz = vSpec.bayPhaseZ || 3.5;
      const unitPz = vSpec.phaseSpacing || 2.4;
      const lvS = vSpec.lvKv >= 138 ? 1.48 : (vSpec.lvKv >= 69 ? 1.18 : 1.0);
      const lvSp = vSpec.lvKv >= 138 ? 3.2 : (vSpec.lvKv >= 69 ? 2.4 : 1.65);

      const laTopY = +(2.58 + 2.85 * s + 0.22).toFixed(3);
      const ctTopY = +(2.20 + 2.85 * s + 0.26).toFixed(3);
      const dsTermY = +(2.35 + 2.35 * s + 0.14).toFixed(3);
      const cbTilt = Math.PI / 10;
      const cbBushingH = 2.25 * s;
      const cbTermOffsetX = +(0.72 + cbBushingH * Math.sin(cbTilt)).toFixed(3);
      const cbTermY = +(2.38 + cbBushingH * Math.cos(cbTilt) + 0.04).toFixed(3);
      const busY = +(Math.max(ctTopY + 0.45, dsTermY + 0.95)).toFixed(3);

      const txTankScale = vSpec.id === '230_138' ? 1.32 : (vSpec.id === '138_69' ? 1.16 : 1.0);
      const txCoverY = +(0.2 + 3.8 * txTankScale).toFixed(3);
      const txHvTilt = Math.PI / 22;
      const txHvH = 2.65 * s;
      const txHvTopX = -1.0 * txTankScale - txHvH * Math.sin(txHvTilt);
      const txHvTopY = txCoverY + 0.20 + txHvH * Math.cos(txHvTilt);
      const txHvStudX = +(txHvTopX - 0.22 * Math.sin(txHvTilt)).toFixed(3);
      const txHvStudY = +(txHvTopY + 0.22 * Math.cos(txHvTilt)).toFixed(3);
      const txHvPhaseZ = [-1.65 * txTankScale, 0, 1.65 * txTankScale];
      const txLvStudX = +(1.5 * txTankScale).toFixed(3);
      const txLvStudY = +(txCoverY + 0.48 + 1.55 * lvS + 0.10).toFixed(3);
      const txLvPhaseZ = [-1.8 * txTankScale, -0.6 * txTankScale, 0.6 * txTankScale, 1.8 * txTankScale];
      return {
        vSpec, s, lvS, lvSp, pz, unitPz,
        gantryWireY: +(7.6 + 2.0 * (s - 1.0) + 3.55).toFixed(3),
        laTopY, ctTopY, dsTermY, cbTermY, cbTermOffsetX, busY,
        txTankScale, txCoverY,
        txHvStudX, txHvStudY, txHvPhaseZ,
        txLvStudX, txLvStudY, txLvPhaseZ,
        secTermY: +(1.95 + 1.28 * lvS).toFixed(3)
      };
    }

    // Helper: Tag an object/terminal as a live energized node for 1st-person MAD proximity detection
    function tagEnergizedTerminal(obj, circuitTag = 'main_path', voltageTag = '69kV') {
      if (!obj) return obj;
      obj.userData.energizedNode = true;
      obj.userData.circuitTag = circuitTag;
      obj.userData.voltageTag = voltageTag;
      return obj;
    }

    // Helper: Aluminum toroidal corona / stress-grading ring for 138 kV & 230 kV bushings and insulators
    function createCoronaRing(radius = 0.36, tubeRadius = 0.032) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(radius, tubeRadius, 10, 24), MatLib.aluminumBus);
      ring.name = 'coronaRing';
      ring.rotation.x = Math.PI / 2;
      ring.castShadow = true;
      return ring;
    }

    // Helper: Recursively tag every mesh in a sub-assembly with its subpartId for direct 3D raycasting
    function tagSubpartHierarchy(obj, subpartId) {
      if (!obj) return;
      obj.userData.subpartId = subpartId;
      if (obj.children) {
        obj.children.forEach(child => tagSubpartHierarchy(child, subpartId));
      }
    }

    // Helper: Create a realistic ribbed porcelain/polymer insulator with alternating large/small weather sheds & metal flanges
    function createRibbedInsulator(height, baseRadius, shedsCount, material, alternating = true) {
      const group = new THREE.Group();
      // Core dielectric column
      const shaftGeo = new THREE.CylinderGeometry(baseRadius * 0.68, baseRadius * 0.78, height, 18);
      const shaft = new THREE.Mesh(shaftGeo, material);
      shaft.castShadow = true;
      group.add(shaft);

      // Top and bottom cast-metal bolted mounting flanges
      const flangeGeo = new THREE.CylinderGeometry(baseRadius * 1.15, baseRadius * 1.15, Math.min(0.08, height * 0.06), 16);
      const topFlange = new THREE.Mesh(flangeGeo, MatLib.galvanizedSteel);
      topFlange.position.y = height / 2;
      const botFlange = new THREE.Mesh(flangeGeo, MatLib.galvanizedSteel);
      botFlange.position.y = -height / 2;
      group.add(topFlange, botFlange);

      // Alternating large & small tapered weather-shed skirts
      const shedSpacing = (height * 0.88) / (shedsCount + 1);
      const bigShedGeo = new THREE.CylinderGeometry(baseRadius * 1.35, baseRadius * 1.95, height * 0.032, 18);
      const smallShedGeo = new THREE.CylinderGeometry(baseRadius * 1.10, baseRadius * 1.50, height * 0.025, 18);
      for (let i = 1; i <= shedsCount; i++) {
        const useBig = !alternating || (i % 2 === 1);
        const shed = new THREE.Mesh(useBig ? bigShedGeo : smallShedGeo, material);
        shed.position.y = -height * 0.44 + i * shedSpacing;
        shed.castShadow = true;
        group.add(shed);
      }
      return group;
    }

    // Helper: Create 3-phase Arcing Horns for bushings
    function createArcingHorns(gapHeight) {
      const group = new THREE.Group();
      const hornMat = MatLib.galvanizedSteel;
      const topHorn = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, gapHeight * 0.45, 8), hornMat);
      topHorn.position.set(0.18, gapHeight * 0.25, 0);
      topHorn.rotation.z = Math.PI / 6;
      group.add(topHorn);

      const botHorn = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, gapHeight * 0.45, 8), hornMat);
      botHorn.position.set(0.18, -gapHeight * 0.25, 0);
      botHorn.rotation.z = -Math.PI / 6;
      group.add(botHorn);
      return group;
    }

    // Helper: Create a lattice steel structural tower leg
    function createLatticeMast(height, baseWidth, topWidth) {
      const group = new THREE.Group();
      const mat = MatLib.steelLattice;
      const legGeo = new THREE.CylinderGeometry(0.06, 0.09, height, 6);

      // 4 Corner legs
      const hwB = baseWidth / 2;
      const hwT = topWidth / 2;
      const positions = [
        [-hwB, -hwT, -hwB, -hwT],
        [hwB, hwT, -hwB, -hwT],
        [hwB, hwT, hwB, hwT],
        [-hwB, -hwT, hwB, hwT]
      ];

      positions.forEach(p => {
        const leg = new THREE.Mesh(legGeo, mat);
        leg.position.set((p[0] + p[1]) / 2, height / 2, (p[2] + p[3]) / 2);
        const angleX = Math.atan2(p[3] - p[2], height);
        const angleZ = Math.atan2(p[0] - p[1], height);
        leg.rotation.x = angleX;
        leg.rotation.z = angleZ;
        leg.castShadow = true;
        group.add(leg);
      });

      // Diagonal cross-bracing ties
      const tiers = 8;
      const tierH = height / tiers;
      const braceGeo = new THREE.CylinderGeometry(0.025, 0.025, baseWidth * 1.4, 6);
      for (let i = 0; i < tiers; i++) {
        const y = i * tierH + tierH / 2;
        const brace1 = new THREE.Mesh(braceGeo, mat);
        brace1.position.set(0, y, 0);
        brace1.rotation.z = Math.PI / 4;
        group.add(brace1);
        const brace2 = new THREE.Mesh(braceGeo, mat);
        brace2.position.set(0, y, 0);
        brace2.rotation.z = -Math.PI / 4;
        group.add(brace2);
      }

      // Lightning rod spike at top
      const spike = new THREE.Mesh(new THREE.ConeGeometry(0.04, 1.8, 8), mat);
      spike.position.y = height + 0.9;
      group.add(spike);

      return group;
    }

    // Helper: Create a catenary overhead jumper conductor between two 3D points using TubeGeometry (carries exact flowCurve)
    function createCatenaryJumper(p1, p2, sag = 0.45, segments = 10, mat = MatLib.copperConductor, voltageTag = '69kV', circuitTag = 'main_path', twinBundle = false) {
      const group = new THREE.Group();
      const points = [];
      for (let i = 0; i <= segments; i++) {
        const t = i / segments;
        const x = p1.x + (p2.x - p1.x) * t;
        const z = p1.z + (p2.z - p1.z) * t;
        const yLinear = p1.y + (p2.y - p1.y) * t;
        const ySag = 4.0 * sag * t * (1.0 - t);
        points.push(new THREE.Vector3(x, yLinear - ySag, z));
      }
      const curve = new THREE.CatmullRomCurve3(points);
      const tubeRadius = mat === MatLib.aluminumBus ? 0.026 : 0.022;
      if (twinBundle) {
        [-0.08, 0.08].forEach(dz => {
          const offsetCurve = new THREE.CatmullRomCurve3(points.map(pt => new THREE.Vector3(pt.x, pt.y, pt.z + dz)));
          const mesh = new THREE.Mesh(new THREE.TubeGeometry(offsetCurve, segments * 2, tubeRadius * 0.9, 8, false), mat);
          mesh.castShadow = true;
          group.add(mesh);
        });
        [0.28, 0.5, 0.72].forEach(st => {
          const sp = curve.getPointAt(st);
          const spacer = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.18), MatLib.aluminumBus);
          spacer.position.copy(sp);
          group.add(spacer);
        });
      } else {
        const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, segments * 2, tubeRadius, 8, false), mat);
        mesh.castShadow = true;
        group.add(mesh);
      }
      group.userData.flowCurve = curve;
      group.userData.voltageTag = voltageTag;
      group.userData.circuitTag = circuitTag;
      return group;
    }

    // Helper: Create a rigid tubular bus or enclosed GIS duct between two 3D points (carries exact flowCurve)
    function createRigidBusSegment(p1, p2, radius = 0.055, mat = MatLib.aluminumBus, voltageTag = '69kV', circuitTag = 'main_path', twinBundle = false) {
      const dist = Math.max(0.01, p1.distanceTo(p2));
      const curve = new THREE.LineCurve3(p1.clone(), p2.clone());
      if (twinBundle) {
        const grp = new THREE.Group();
        const dir = p2.clone().sub(p1).normalize();
        const lat = new THREE.Vector3(-dir.z, 0, dir.x);
        if (lat.lengthSq() < 0.001) lat.set(0, 0, 1);
        lat.normalize().multiplyScalar(0.085);
        [-1, 1].forEach(side => {
          const seg = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.85, radius * 0.85, dist, 12), mat);
          seg.position.copy(p1).add(p2).multiplyScalar(0.5).addScaledVector(lat, side);
          seg.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
          seg.castShadow = true;
          grp.add(seg);
        });
        grp.userData.flowCurve = curve;
        grp.userData.voltageTag = voltageTag;
        grp.userData.circuitTag = circuitTag;
        return grp;
      }
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, dist, 16), mat);
      mesh.position.copy(p1).add(p2).multiplyScalar(0.5);
      mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p2.clone().sub(p1).normalize());
      mesh.castShadow = true;
      mesh.userData.flowCurve = curve;
      mesh.userData.voltageTag = voltageTag;
      mesh.userData.circuitTag = circuitTag;
      return mesh;
    }

    // Helper: Phase Identification Marker Sleeve
    function createPhaseMarker(phaseIndex, radius = 0.08, length = 0.22) {
      const mats = [MatLib.phaseA, MatLib.phaseB, MatLib.phaseC];
      const mat = mats[phaseIndex % 3];
      const marker = new THREE.Mesh(new THREE.CylinderGeometry(radius * 1.3, radius * 1.3, length, 12), mat);
      return marker;
    }

    // Helper: Create a high-detail 3-phase SF6 Dead-Tank Circuit Breaker Unit scaled by voltage class
    function createCompactBreakerUnit(x, y, z, rotY = 0, tag = '52', vSpec = getVoltageSpec(), circuitTag = 'main_path') {
      const group = new THREE.Group();
      group.position.set(x, y, z);
      group.rotation.y = rotY;

      const s = vSpec.insScale || 1.0;
      const pzStep = vSpec.phaseSpacing || 2.4;
      const sheds = vSpec.shedsCount || 10;
      const bHeight = +(1.75 * s).toFixed(3);
      const padLen = pzStep * 2 + 1.6;
      const vTag = vSpec.hvKv + 'kV';

      const pad = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.26, padLen), MatLib.concrete);
      pad.position.set(0, 0.13, 0);
      pad.receiveShadow = true;
      group.add(pad);

      const phaseOffsets = [-pzStep, 0, pzStep];
      phaseOffsets.forEach((pz, idx) => {
        [-0.9, 0.9].forEach(lx => {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.14, 1.45, 0.16), MatLib.galvanizedSteel);
          leg.position.set(lx, 0.95, pz);
          leg.castShadow = true;
          group.add(leg);
        });
        const cradle = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.12, 0.26), MatLib.galvanizedSteel);
        cradle.position.set(0, 1.55, pz);
        group.add(cradle);

        const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 2.3, 20), MatLib.transformerTank);
        tank.position.set(0, 2.02, pz);
        tank.rotation.z = Math.PI / 2;
        tank.castShadow = true;
        group.add(tank);

        [-1.16, 1.16].forEach(fx => {
          const fl = new THREE.Mesh(new THREE.CylinderGeometry(0.47, 0.47, 0.06, 20), MatLib.darkSteel);
          fl.position.set(fx, 2.02, pz);
          fl.rotation.z = Math.PI / 2;
          group.add(fl);
        });

        const cbUnitTilt = Math.PI / 14;
        const bTopX = +(0.68 + bHeight * Math.sin(cbUnitTilt)).toFixed(3);
        const bTopY = +(2.32 + bHeight * Math.cos(cbUnitTilt) + 0.04).toFixed(3);
        const palmL = new THREE.Vector3(-bTopX, bTopY, pz);
        const palmR = new THREE.Vector3(bTopX, bTopY, pz);
        [-0.68, 0.68].forEach((bx, bIdx) => {
          const sign = bIdx === 0 ? -1 : 1;
          const bct = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.26, 0.28, 16), MatLib.darkSteel);
          bct.position.set(bx, 2.32, pz);
          const bushing = createRibbedInsulator(bHeight, 0.17, sheds, MatLib.porcelainBrown, true);
          bushing.position.set(sign * (0.68 + 0.5 * bHeight * Math.sin(cbUnitTilt)), 2.32 + 0.5 * bHeight * Math.cos(cbUnitTilt), pz);
          bushing.rotation.z = bIdx === 0 ? cbUnitTilt : -cbUnitTilt;
          group.add(bct, bushing);

          const palmPos = bIdx === 0 ? palmL : palmR;
          const palm = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.18), MatLib.silverContact);
          palm.position.copy(palmPos);
          tagEnergizedTerminal(palm, circuitTag, vTag);
          const pMark = createPhaseMarker(idx, 0.06, 0.10);
          pMark.position.set(palmPos.x, palmPos.y + 0.06, pz);
          if (vSpec.coronaRings) {
            const cRing = createCoronaRing(0.32 * Math.min(1.35, 0.85 + s * 0.22), 0.026);
            cRing.position.set(palmPos.x, palmPos.y - 0.10, pz);
            group.add(cRing);
          }
          group.add(palm, pMark);
        });

        // Hidden continuous internal flow spline through SF6 interrupter & entrance bushings
        const intPath = new THREE.Object3D();
        intPath.userData.flowCurve = new THREE.CatmullRomCurve3([
          palmL.clone(),
          new THREE.Vector3(-0.55, 2.02, pz),
          new THREE.Vector3(0.55, 2.02, pz),
          palmR.clone()
        ]);
        intPath.userData.voltageTag = vTag;
        intPath.userData.circuitTag = circuitTag;
        group.add(intPath);
      });

      [-0.9, 0.9].forEach(lx => {
        const tieBeam = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.14, pzStep * 2 + 0.4), MatLib.galvanizedSteel);
        tieBeam.position.set(lx, 0.85, 0);
        group.add(tieBeam);
      });

      const mechBox = new THREE.Mesh(new THREE.BoxGeometry(0.75, 1.35, 0.85), MatLib.galvanizedSteel);
      mechBox.position.set(1.25, 1.35, 0);
      const gaugeFace = new THREE.Mesh(
        new THREE.CircleGeometry(0.12, 18),
        new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('sf6') })
      );
      gaugeFace.position.set(1.63, 1.75, -0.18);
      gaugeFace.rotation.y = Math.PI / 2;
      const statusFlag = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.22, 0.26), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
      statusFlag.position.set(1.63, 1.32, 0.16);
      group.add(mechBox, gaugeFace, statusFlag);
      group.userData.statusFlag = statusFlag;
      group.userData.tag = tag;
      const cbUnitTiltRef = Math.PI / 14;
      group.userData.termHeight = +(2.32 + bHeight * Math.cos(cbUnitTiltRef) + 0.04).toFixed(3);
      group.userData.termOffsetX = +(0.68 + bHeight * Math.sin(cbUnitTiltRef)).toFixed(3);

      return group;
    }

    // Helper: Create a realistic 3-phase Center-Break Disconnect Switch Unit scaled by voltage class
    function createCompactDisconnectUnit(x, y, z, rotY = 0, isOpen = false, tag = '89', vSpec = getVoltageSpec(), circuitTag = 'main_path') {
      const group = new THREE.Group();
      group.position.set(x, y, z);
      group.rotation.y = rotY;

      const s = vSpec.insScale || 1.0;
      const pzStep = vSpec.phaseSpacing || 2.4;
      const sheds = vSpec.shedsCount || 10;
      const postH = +(1.85 * s).toFixed(3);
      const jawY = +(1.92 + postH).toFixed(3);
      const padLen = pzStep * 2 + 1.4;
      const vTag = vSpec.hvKv + 'kV';

      const pad = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.24, padLen), MatLib.concrete);
      pad.position.set(0, 0.12, 0);
      pad.receiveShadow = true;
      group.add(pad);

      const phaseOffsets = [-pzStep, 0, pzStep];
      const bladeAngle = isOpen ? Math.PI / 2.6 : 0;
      const bladePairs = [];

      phaseOffsets.forEach((pz, idx) => {
        const chan = new THREE.Mesh(new THREE.BoxGeometry(1.75, 0.14, 0.28), MatLib.galvanizedSteel);
        chan.position.set(0, 1.85, pz);
        group.add(chan);

        [-0.65, 0.65].forEach(px => {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.11, 1.68, 0.11), MatLib.galvanizedSteel);
          leg.position.set(px, 1.0, pz);
          leg.castShadow = true;
          const post = createRibbedInsulator(postH, 0.15, sheds, MatLib.porcelainBrown, true);
          post.position.set(px, 1.92 + postH / 2, pz);
          const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.15, 0.10, 12), MatLib.aluminumBus);
          cap.position.set(px, jawY + 0.02, pz);
          tagEnergizedTerminal(cap, circuitTag, vTag);
          if (vSpec.coronaRings) {
            const cRing = createCoronaRing(0.28, 0.022);
            cRing.position.set(px, jawY - 0.06, pz);
            group.add(cRing);
          }
          group.add(leg, post, cap);
        });

        const blade1 = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.62, 10), MatLib.copperConductor);
        blade1.rotation.z = Math.PI / 2;
        blade1.position.set(-0.32, jawY + 0.05, pz);
        blade1.rotation.y = -bladeAngle;

        const blade2 = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.62, 10), MatLib.copperConductor);
        blade2.rotation.z = Math.PI / 2;
        blade2.position.set(0.32, jawY + 0.05, pz);
        blade2.rotation.y = bladeAngle;
        bladePairs.push({ blade1, blade2 });

        const corona = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.018, 6, 16), MatLib.aluminumBus);
        corona.position.set(0, jawY + 0.05, pz);
        corona.rotation.y = Math.PI / 2;

        const pMark = createPhaseMarker(idx, 0.055, 0.1);
        pMark.position.set(0, jawY + 0.08, pz);
        group.add(blade1, blade2, corona, pMark);

        // Continuous internal flow line across jaw-blade-jaw
        const bladeFlow = new THREE.Object3D();
        bladeFlow.userData.flowCurve = new THREE.LineCurve3(
          new THREE.Vector3(-0.65, jawY + 0.05, pz),
          new THREE.Vector3(0.65, jawY + 0.05, pz)
        );
        bladeFlow.userData.voltageTag = vTag;
        bladeFlow.userData.circuitTag = circuitTag;
        group.add(bladeFlow);
      });

      const torsionBar = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, pzStep * 2 + 0.6, 8), MatLib.galvanizedSteel);
      torsionBar.position.set(0, 1.92, 0);
      torsionBar.rotation.x = Math.PI / 2;
      const vertRod = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.0, 8), MatLib.galvanizedSteel);
      vertRod.position.set(0.65, 1.45, pzStep + 0.14);
      const ctrlBox = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.65, 0.38), MatLib.galvanizedSteel);
      ctrlBox.position.set(0.65, 1.05, pzStep + 0.24);
      group.add(torsionBar, vertRod, ctrlBox);

      group.userData.bladePairs = bladePairs;
      group.userData.tag = tag;
      group.userData.termHeight = jawY + 0.05;
      group.userData.termOffsetX = 0.65;
      return group;
    }

    // BUILDER 1: SWITCHYARD GROUND, CONCRETE PADS, CABLE TRENCHES, PERIMETER FENCE & CONTROL HOUSE
    function buildSwitchyardEnvironment(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const envGroup = new THREE.Group();
      envGroup.name = 'environment';

      // 1. Dynamic Crushed Rock Switchyard Pad (100mm gravel per IEEE 80, expands per busbar topology)
      const gravelTex = TextureGen.createGravelTexture();
      gravelTex.repeat.set(Math.round(L.yardW / 8), Math.round(L.yardL / 8));
      gravelTex.needsUpdate = true;
      const groundMat = new THREE.MeshStandardMaterial({
        color: 0x334155,
        map: gravelTex,
        roughness: 0.9,
        metalness: 0.05
      });
      const groundGeo = new THREE.PlaneGeometry(L.yardW, L.yardL);
      const ground = new THREE.Mesh(groundGeo, groundMat);
      ground.rotation.x = -Math.PI / 2;
      ground.position.set(L.yardCenterX, 0, L.yardCenterZ);
      ground.receiveShadow = true;
      envGroup.add(ground);

      // Surrounding native soil terrain
      const outerTerrainGeo = new THREE.PlaneGeometry(240, 220);
      const outerMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 1.0 });
      const outerTerrain = new THREE.Mesh(outerTerrainGeo, outerMat);
      outerTerrain.rotation.x = -Math.PI / 2;
      outerTerrain.position.set(L.yardCenterX, -0.04, L.yardCenterZ);
      outerTerrain.receiveShadow = true;
      envGroup.add(outerTerrain);

      // IEEE Std 80 Switchyard Ground Grid Wireframe Helper scaled to exact yard dimensions
      const gridMax = Math.max(L.yardW, L.yardL);
      const gridHelper = new THREE.GridHelper(gridMax, 36, 0x0284c7, 0x475569);
      gridHelper.scale.set(L.yardW / gridMax, 1, L.yardL / gridMax);
      gridHelper.position.set(L.yardCenterX, 0.015, L.yardCenterZ);
      envGroup.add(gridHelper);

      // Concrete equipment foundation pads scaled to active topology & enclosure
      const fdrMidX = (L.secBusX + L.fdrGantryX) / 2;
      const fdrSpanW = Math.max(7.5, L.fdrGantryX - L.secBusX - 5.2);
      const pads = [
        { x: L.gantryX, z: 0, w: 6.5, l: 14, h: 0.35, desc: 'Gantry Pad' },
        { x: L.txX, z: L.txZ, w: 8.0, l: 14, h: 0.45, desc: 'Transformer Main Pad & Oil Retention Pit' },
        { x: L.secArresterX, z: 0, w: 3.4, l: 8.5, h: 0.28, desc: '13.8 kV Secondary Arrester/CT/89-LV Pad' },
        { x: L.secCbX, z: 0, w: 4.0, l: 8.5, h: 0.32, desc: '13.8 kV Main VCB 52-LV Pad' },
        { x: L.capX, z: L.capZ, w: 4.8, l: 5.2, h: 0.28, desc: '3.6 MVAR Shunt Capacitor Bank Pad' },
        { x: fdrMidX, z: L.fdr1Z, w: fdrSpanW, l: 5.5, h: 0.28, desc: 'Feeder 01 Bay (52-F1) Pad' },
        { x: fdrMidX, z: L.fdr2Z, w: fdrSpanW, l: 5.5, h: 0.28, desc: 'Feeder 02 Bay (52-F2) Pad' },
        { x: L.fdrGantryX, z: (L.fdr1Z + L.fdr2Z) / 2, w: 4.5, l: 21.0, h: 0.32, desc: '13.8 kV Outgoing Gantry Pad' },
        { x: L.ctrlX, z: L.ctrlZ, w: 10.2, l: 12.8, h: 0.4, desc: 'Control House Pad' },
        { x: L.sstX, z: L.sstZ, w: 4.8, l: 5.0, h: 0.38, desc: 'Station Service Transformer SST-100 Pad' }
      ];

      if (L.enclosure === 'gis') {
        pads.push({ x: L.gisX, z: 0, w: L.gisW + 0.8, l: L.gisL + 0.8, h: 0.35, desc: 'SF6 GIS Hall Foundation Pad' });
      } else {
        pads.push(
          { x: L.laX, z: 0, w: 3.0, l: 10.5, h: 0.3, desc: 'Surge Arrester Pad' },
          { x: L.ctX, z: 0, w: 3.0, l: 10.5, h: 0.3, desc: 'CT/VT Metering Pad' },
          { x: L.dsX, z: L.dsZ, w: 4.0, l: 10.5, h: 0.3, desc: 'Line Disconnect Switch Pad' }
        );
        if (L.scheme === 'single') {
          pads.push({ x: L.cbX, z: 0, w: 4.5, l: 10.5, h: 0.35, desc: 'Main Breaker 52 Pad' });
        } else if (L.scheme === 'maintransfer') {
          pads.push({ x: L.cbX, z: 0, w: 4.5, l: 10.5, h: 0.35, desc: 'Main Breaker 52 Pad' });
          pads.push({ x: L.cbX, z: -6.0, w: 8.5, l: 3.4, h: 0.28, desc: '89-M Selector Pad' });
          pads.push({ x: L.cbX, z: 6.0, w: 8.5, l: 3.4, h: 0.28, desc: '89-BYP Transfer Selector Pad' });
          pads.push({ x: L.tieX, z: 0, w: 9.0, l: 16.5, h: 0.35, desc: 'Bus Tie Breaker 52-BT & Isolators Pad' });
        } else if (L.scheme === 'ring') {
          pads.push({ x: L.ringX1, z: 0, w: 8.5, l: 19.5, h: 0.35, desc: 'West Ring CB-1 Branch Pad' });
          pads.push({ x: L.ringX2, z: 0, w: 8.5, l: 19.5, h: 0.35, desc: 'East Ring CB-3 Branch Pad' });
          pads.push({ x: (L.ringX1 + L.ringX2) / 2, z: L.ringZ1, w: 17.5, l: 8.5, h: 0.35, desc: 'North Ring CB-2 Branch Pad' });
          pads.push({ x: (L.ringX1 + L.ringX2) / 2, z: L.ringZ2, w: 17.5, l: 8.5, h: 0.35, desc: 'South Ring CB-4 Branch Pad' });
        } else if (L.scheme === 'breakerhalf') {
          pads.push({ x: L.cbX, z: -16.5, w: 9.0, l: 13.5, h: 0.35, desc: 'Breaker CB-A Bay Pad' });
          pads.push({ x: L.cbX, z: 0, w: 9.0, l: 14.0, h: 0.35, desc: 'Tie Breaker CB-TIE Bay Pad' });
          pads.push({ x: L.cbX, z: 16.5, w: 9.0, l: 13.5, h: 0.35, desc: 'Breaker CB-B Bay Pad' });
        } else if (L.scheme === 'doublebreaker') {
          const b2x = L.bay2X !== undefined ? L.bay2X : (L.cbX + 13.5);
          const cbzAbs = Math.abs(L.cbZ || 11.5);
          pads.push({ x: L.cbX, z: -cbzAbs, w: 8.8, l: 14.0, h: 0.35, desc: 'Bay 1 CB-1A Pad' });
          pads.push({ x: L.cbX, z: cbzAbs, w: 8.8, l: 14.0, h: 0.35, desc: 'Bay 1 CB-1B Pad' });
          pads.push({ x: b2x, z: -cbzAbs, w: 8.8, l: 14.0, h: 0.35, desc: 'Bay 2 CB-2A Pad' });
          pads.push({ x: b2x, z: cbzAbs, w: 8.8, l: 14.0, h: 0.35, desc: 'Bay 2 CB-2B Pad' });
        }
      }

      pads.forEach(p => {
        const padMesh = new THREE.Mesh(new THREE.BoxGeometry(p.w, p.h, p.l), MatLib.concrete);
        padMesh.position.set(p.x, p.h / 2, p.z);
        padMesh.receiveShadow = true;
        padMesh.castShadow = true;
        envGroup.add(padMesh);
      });

      // TRANSFORMER OIL RETENTION BUND WALL (BERM) - IEEE Std 980 Spill Containment
      const bundGroup = new THREE.Group();
      bundGroup.name = 'tx-oil-containment-berm';
      const wallMat = MatLib.concrete;
      const wallH = 0.65;
      const wallThick = 0.28;
      const bW = 8.8, bL = 14.8;

      const wallN = new THREE.Mesh(new THREE.BoxGeometry(bW, wallH, wallThick), wallMat);
      wallN.position.set(L.txX, wallH / 2, L.txZ - bL / 2);
      const wallS = new THREE.Mesh(new THREE.BoxGeometry(bW, wallH, wallThick), wallMat);
      wallS.position.set(L.txX, wallH / 2, L.txZ + bL / 2);

      const wallE = new THREE.Mesh(new THREE.BoxGeometry(wallThick, wallH, bL - wallThick * 2), wallMat);
      wallE.position.set(L.txX + bW / 2 - wallThick / 2, wallH / 2, L.txZ);
      const wallW = new THREE.Mesh(new THREE.BoxGeometry(wallThick, wallH, bL - wallThick * 2), wallMat);
      wallW.position.set(L.txX - bW / 2 + wallThick / 2, wallH / 2, L.txZ);

      // Crushed rock fire-quenching gravel bed inside bund (IEEE 979/980 flame arrestor gravel)
      const gravelBedMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.95 });
      const gravelBed = new THREE.Mesh(new THREE.BoxGeometry(bW - 0.6, 0.2, bL - 0.6), gravelBedMat);
      gravelBed.position.set(L.txX, 0.1, L.txZ);

      const sumpGrating = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.24, 1.4), MatLib.galvanizedSteel);
      sumpGrating.position.set(L.txX + bW / 2 - 1.2, 0.12, L.txZ + bL / 2 - 1.2);
      const sumpPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.9, 8), MatLib.galvanizedSteel);
      sumpPipe.position.set(L.txX + bW / 2 - 1.2, 0.5, L.txZ + bL / 2 - 1.2);

      bundGroup.add(wallN, wallS, wallE, wallW, gravelBed, sumpGrating, sumpPipe);
      envGroup.add(bundGroup);

      // DEDICATED SST-100 FENCED ENCLOSURE & IEEE STD 979 CONCRETE FIRE/BLAST BARRIER WALL
      const sstSafetyGroup = new THREE.Group();
      sstSafetyGroup.name = 'sst-fire-barrier-enclosure';
      // 4.0m tall reinforced concrete fire barrier wall (1m above SST-100) shielding Control House Westwards
      const fireWall = new THREE.Mesh(new THREE.BoxGeometry(0.35, 4.0, 5.8), MatLib.fireWallConcrete);
      fireWall.position.set(L.sstX - 2.95, 2.0, L.sstZ);
      fireWall.castShadow = true;
      fireWall.receiveShadow = true;
      sstSafetyGroup.add(fireWall);

      const fwStripe = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.22, 5.84), MatLib.yellowHighlight);
      fwStripe.position.set(L.sstX - 2.95, 0.15, L.sstZ);
      sstSafetyGroup.add(fwStripe);

      // Steel perimeter fence enclosing SST-100 North, East, South sides
      const sstFenceTex = TextureGen.createFenceTexture();
      sstFenceTex.needsUpdate = true;
      const sstFenceMat = new THREE.MeshStandardMaterial({
        map: sstFenceTex, transparent: true, opacity: 0.78, roughness: 0.5, metalness: 0.8, side: THREE.DoubleSide
      });
      const sstFenceN = new THREE.Mesh(new THREE.PlaneGeometry(5.8, 2.2), sstFenceMat);
      sstFenceN.position.set(L.sstX, 1.1, L.sstZ - 2.9);
      const sstFenceS = new THREE.Mesh(new THREE.PlaneGeometry(5.8, 2.2), sstFenceMat);
      sstFenceS.position.set(L.sstX, 1.1, L.sstZ + 2.9);
      const sstFenceE = new THREE.Mesh(new THREE.PlaneGeometry(5.8, 2.2), sstFenceMat);
      sstFenceE.position.set(L.sstX + 2.9, 1.1, L.sstZ);
      sstFenceE.rotation.y = Math.PI / 2;
      sstSafetyGroup.add(sstFenceN, sstFenceS, sstFenceE);
      envGroup.add(sstSafetyGroup);

      // DYNAMIC PAVED PERIMETER MAINTENANCE ROADS, TR-01 HEAVY-HAUL SPUR & PERSONNEL WALKWAY TO CONTROL HOUSE
      // Strictly placed outside equipment bounding box (L.eqBounds) so ZERO roads or buildings ever clip any bay!
      const civilRoadGroup = new THREE.Group();
      civilRoadGroup.name = 'civil-access-roads';
      const roadMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.88, metalness: 0.05 });
      const stripeMat = MatLib.yellowHighlight;
      const rd = L.roads;
      const rdSpanX = rd.eastX - rd.westX + rd.roadW;
      const rdMidX = (rd.westX + rd.eastX) / 2;
      const rdSpanZ = rd.southZ - rd.northZ + rd.roadW;
      const rdMidZ = (rd.northZ + rd.southZ) / 2;

      const addRoadStrip = (x, z, w, l) => {
        const slab = new THREE.Mesh(new THREE.BoxGeometry(w, 0.09, l), roadMat);
        slab.position.set(x, 0.045, z);
        slab.receiveShadow = true;
        civilRoadGroup.add(slab);
      };
      // North, South, West & East perimeter maintenance loop
      addRoadStrip(rdMidX, rd.northZ, rdSpanX, rd.roadW);
      addRoadStrip(rdMidX, rd.southZ, rdSpanX, rd.roadW);
      addRoadStrip(rd.westX, rdMidZ, rd.roadW, rdSpanZ);
      addRoadStrip(rd.eastX, rdMidZ, rd.roadW, rdSpanZ);

      // Dashed yellow centerline along South main service driveway
      const cLine = new THREE.Mesh(new THREE.BoxGeometry(rdSpanX - 4.0, 0.015, 0.1), stripeMat);
      cLine.position.set(rdMidX, 0.095, rd.southZ);
      civilRoadGroup.add(cLine);

      // Heavy-Haul Rigging / Crane Access Spur North from South Road right to TR-01 South oil-pit apron
      const spurZStart = L.txZ + 7.45;
      const spurZEnd = rd.southZ - rd.roadW / 2;
      if (spurZEnd > spurZStart + 1.0) {
        const spurLen = spurZEnd - spurZStart;
        addRoadStrip(L.txX, spurZStart + spurLen / 2, 4.2, spurLen);
      }

      // Personnel Walkway & Safety Bollards from South Road into Control House West Double Doorway
      const walkwayGroup = new THREE.Group();
      const doorWorldX = L.ctrlX - 4.2;
      const apronZStart = rd.southZ + rd.roadW / 2;
      const apronLen = Math.max(2.0, L.ctrlZ - apronZStart + 1.2);
      const walkNS = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.12, apronLen), MatLib.concrete);
      walkNS.position.set(doorWorldX - 2.2, 0.06, apronZStart + apronLen / 2);
      walkNS.receiveShadow = true;
      const walkEW = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.12, 2.6), MatLib.concrete);
      walkEW.position.set(doorWorldX - 1.5, 0.06, L.ctrlZ);
      walkEW.receiveShadow = true;
      walkwayGroup.add(walkNS, walkEW);
      [-1.35, 1.35].forEach(dz => {
        const bollard = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 1.05, 12), MatLib.yellowHighlight);
        bollard.position.set(doorWorldX - 1.2, 0.52, L.ctrlZ + dz);
        bollard.castShadow = true;
        walkwayGroup.add(bollard);
      });
      envGroup.add(civilRoadGroup, walkwayGroup);

      // COPPER GROUNDING RISERS (4/0 AWG copper conductors with Cadweld lugs bonding equipment to ground grid)
      const riserLocations = [
        { x: L.gantryX, z: -5.0 }, { x: L.gantryX, z: 5.0 },
        { x: L.laX, z: -3.5 }, { x: L.laX, z: 3.5 },
        { x: L.ctX, z: -3.5 }, { x: L.ctX, z: 3.5 },
        { x: L.dsX, z: L.dsZ - 3.5 }, { x: L.dsX, z: L.dsZ + 3.5 },
        { x: L.cbX, z: -4.0 }, { x: L.cbX, z: 4.0 },
        { x: L.txX - 2.5, z: -2.5 }, { x: L.txX + 2.5, z: 2.5 },
        { x: L.secCbX, z: -2.5 }, { x: L.secCbX, z: 2.5 },
        { x: (L.secBusX + L.fdrGantryX) / 2, z: L.fdr1Z - 2.2 }, { x: (L.secBusX + L.fdrGantryX) / 2, z: L.fdr2Z + 2.2 },
        { x: L.sstX - 1.5, z: L.sstZ + 1.5 }, { x: L.sstX + 1.5, z: L.sstZ - 1.5 }
      ];
      riserLocations.forEach(r => {
        const riser = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.6, 6), MatLib.groundCopper);
        riser.position.set(r.x, 0.8, r.z);
        const lug = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.07, 0.09), MatLib.brassContact);
        lug.position.set(r.x, 0.04, r.z);
        envGroup.add(riser, lug);
      });

      // Concrete cable trenches placed cleanly South of equipment bays -> Control House (zero pad collisions!)
      const trenchMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8 });
      const trenchZ = L.eqBounds.maxZ + 1.6;
      const trenchStart = L.laX;
      const trenchEnd = L.fdrGantryX - 4.0;
      const mainTrench = new THREE.Mesh(new THREE.BoxGeometry(trenchEnd - trenchStart, 0.1, 1.2), trenchMat);
      mainTrench.position.set((trenchStart + trenchEnd) / 2, 0.05, trenchZ);
      envGroup.add(mainTrench);

      const branchLen = Math.max(2.0, L.ctrlZ - 5.4 - trenchZ + 1.0);
      const branchTrench = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.1, branchLen), trenchMat);
      branchTrench.position.set(L.ctrlX, 0.05, trenchZ + branchLen / 2);
      envGroup.add(branchTrench);

      // Perimeter Security Chain-Link Fence (dynamic yardW x yardL with Warning Signs)
      const fenceH = 2.4;
      const fenceTex = TextureGen.createFenceTexture();
      fenceTex.repeat.set(Math.round(L.yardW / 2), 1);
      fenceTex.needsUpdate = true;
      const fenceMat = new THREE.MeshStandardMaterial({
        map: fenceTex,
        transparent: true,
        opacity: 0.8,
        roughness: 0.5,
        metalness: 0.8,
        side: THREE.DoubleSide
      });

      const minX = L.yardCenterX - L.yardW / 2;
      const maxX = L.yardCenterX + L.yardW / 2;
      const minZ = L.yardCenterZ - L.yardL / 2;
      const maxZ = L.yardCenterZ + L.yardL / 2;

      const fenceSides = [
        { w: L.yardW, h: fenceH, x: L.yardCenterX, y: fenceH / 2, z: minZ, ry: 0 },
        { w: L.yardW, h: fenceH, x: L.yardCenterX, y: fenceH / 2, z: maxZ, ry: 0 },
        { w: L.yardL, h: fenceH, x: minX, y: fenceH / 2, z: L.yardCenterZ, ry: Math.PI / 2 },
        { w: L.yardL, h: fenceH, x: maxX, y: fenceH / 2, z: L.yardCenterZ, ry: Math.PI / 2 }
      ];

      fenceSides.forEach(f => {
        const sideMesh = new THREE.Mesh(new THREE.PlaneGeometry(f.w, f.h), fenceMat);
        sideMesh.position.set(f.x, f.y, f.z);
        sideMesh.rotation.y = f.ry;
        envGroup.add(sideMesh);
      });

      // High-Voltage Hazard Signs along fence
      const signTex = TextureGen.createHazardSignTexture();
      signTex.needsUpdate = true;
      const signMat = new THREE.MeshBasicMaterial({ map: signTex, side: THREE.DoubleSide });
      const signGeo = new THREE.PlaneGeometry(1.4, 0.7);

      const signLocations = [
        { x: L.yardCenterX - L.yardW * 0.25, y: 1.4, z: minZ + 0.05, ry: 0 },
        { x: L.yardCenterX + L.yardW * 0.25, y: 1.4, z: minZ + 0.05, ry: 0 },
        { x: L.yardCenterX, y: 1.4, z: maxZ - 0.05, ry: Math.PI },
        { x: minX + 0.05, y: 1.4, z: L.yardCenterZ, ry: Math.PI / 2 },
        { x: L.sstX - 2.84, y: 1.4, z: L.sstZ, ry: -Math.PI / 2 }
      ];

      signLocations.forEach(s => {
        const sign = new THREE.Mesh(signGeo, signMat);
        sign.position.set(s.x, s.y, s.z);
        sign.rotation.y = s.ry;
        envGroup.add(sign);
      });

      // 3D ARCHITECTURAL LAND AREA DIMENSION LINES & PERIMETER PLACARDS
      const landMeta = (typeof computeSubstationLandMetrics === 'function')
        ? computeSubstationLandMetrics(L.scheme, L.enclosure || 'ais', L.voltageClass)
        : {
            lengthM: Math.round(L.yardW),
            widthM: Math.round(L.yardL),
            areaM2: Math.round(L.yardW * L.yardL),
            areaHa: (L.yardW * L.yardL / 10000).toFixed(2)
          };
      const dimMat = new THREE.LineBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.85 });
      const arrowMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24 });

      // North Dimension Line (Length in X)
      const dimZ = minZ - 1.6;
      const nLineGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(minX, 0.25, dimZ),
        new THREE.Vector3(maxX, 0.25, dimZ)
      ]);
      envGroup.add(new THREE.Line(nLineGeo, dimMat));
      [minX, maxX].forEach((tx, idx) => {
        const tick = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.95, 6), arrowMat);
        tick.position.set(tx + (idx === 0 ? 0.45 : -0.45), 0.25, dimZ);
        tick.rotation.z = idx === 0 ? Math.PI / 2 : -Math.PI / 2;
        envGroup.add(tick);
      });

      // West Dimension Line (Width in Z)
      const dimX = minX - 1.6;
      const wLineGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(dimX, 0.25, minZ),
        new THREE.Vector3(dimX, 0.25, maxZ)
      ]);
      envGroup.add(new THREE.Line(wLineGeo, dimMat));
      [minZ, maxZ].forEach((tz, idx) => {
        const tick = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.95, 6), arrowMat);
        tick.position.set(dimX, 0.25, tz + (idx === 0 ? 0.45 : -0.45));
        tick.rotation.x = idx === 0 ? -Math.PI / 2 : Math.PI / 2;
        envGroup.add(tick);
      });

      const makeDimPlacard = (titleTxt) => {
        const cv = document.createElement('canvas');
        cv.width = 768;
        cv.height = 112;
        const c = cv.getContext('2d');
        c.fillStyle = 'rgba(2, 6, 23, 0.92)';
        c.fillRect(0, 0, cv.width, cv.height);
        c.strokeStyle = '#fbbf24';
        c.lineWidth = 6;
        c.strokeRect(4, 4, cv.width - 8, cv.height - 8);
        c.fillStyle = '#fef08a';
        c.font = 'bold 34px monospace';
        c.textAlign = 'center';
        c.textBaseline = 'middle';
        c.fillText(titleTxt, cv.width / 2, cv.height / 2);
        const tex = new THREE.CanvasTexture(cv);
        const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
        const m = new THREE.Mesh(new THREE.PlaneGeometry(11.5, 1.7), mat);
        return m;
      };

      const northBoard = makeDimPlacard(`◄── YARD LENGTH: ${landMeta.lengthM} m | AREA: ${landMeta.areaM2.toLocaleString()} m² (${landMeta.areaHa} ha) ──►`);
      northBoard.position.set(L.yardCenterX, 1.35, dimZ);
      northBoard.rotation.x = -0.35;
      envGroup.add(northBoard);

      const westBoard = makeDimPlacard(`◄── YARD WIDTH: ${landMeta.widthM} m (${L.scheme.toUpperCase()} / ${(L.enclosure || 'ais').toUpperCase()}) ──►`);
      westBoard.position.set(dimX, 1.35, L.yardCenterZ);
      westBoard.rotation.y = Math.PI / 2;
      westBoard.rotation.z = 0;
      envGroup.add(westBoard);

      // Substation Control & Protection House (Walk-In Architectural Cutaway Building at L.ctrlX, L.ctrlZ)
      const ctrlHouse = new THREE.Group();
      ctrlHouse.position.set(L.ctrlX, 0, L.ctrlZ);

      const wallExtMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.72, metalness: 0.08 });
      const wallIntMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.85, metalness: 0.02 });
      const floorMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55, metalness: 0.15 });
      const chWallH = 4.2, chW = 8.4, chL = 10.8, chWT = 0.25;

      // Interior industrial epoxy floor
      const intFloor = new THREE.Mesh(new THREE.BoxGeometry(chW - 0.2, 0.12, chL - 0.2), floorMat);
      intFloor.position.set(0, 0.42, 0);
      intFloor.receiveShadow = true;
      ctrlHouse.add(intFloor);

      // North Wall (Relay Board Wall)
      const chWallN = new THREE.Mesh(new THREE.BoxGeometry(chW, chWallH, chWT), wallExtMat);
      chWallN.position.set(0, chWallH / 2 + 0.4, -chL / 2 + chWT / 2);
      chWallN.castShadow = true; chWallN.receiveShadow = true;
      ctrlHouse.add(chWallN);

      // South Wall (Battery Room Wall)
      const chWallS = new THREE.Mesh(new THREE.BoxGeometry(chW, chWallH, chWT), wallExtMat);
      chWallS.position.set(0, chWallH / 2 + 0.4, chL / 2 - chWT / 2);
      chWallS.castShadow = true; chWallS.receiveShadow = true;
      ctrlHouse.add(chWallS);

      // East Wall (with Cable Entry Trunk & Exhaust Louvers)
      const chWallE = new THREE.Mesh(new THREE.BoxGeometry(chWT, chWallH, chL - chWT * 2), wallExtMat);
      chWallE.position.set(chW / 2 - chWT / 2, chWallH / 2 + 0.4, 0);
      chWallE.castShadow = true; chWallE.receiveShadow = true;
      ctrlHouse.add(chWallE);

      // West Wall (Switchyard Facing Wall with OPEN WALK-IN DOUBLE DOORWAY z in [-1.2, +1.2])
      const wallWLeft = new THREE.Mesh(new THREE.BoxGeometry(chWT, chWallH, 4.0), wallExtMat);
      wallWLeft.position.set(-chW / 2 + chWT / 2, chWallH / 2 + 0.4, -3.4);
      const wallWRight = new THREE.Mesh(new THREE.BoxGeometry(chWT, chWallH, 4.0), wallExtMat);
      wallWRight.position.set(-chW / 2 + chWT / 2, chWallH / 2 + 0.4, 3.4);
      const wallWHeader = new THREE.Mesh(new THREE.BoxGeometry(chWT, 1.4, 2.8), wallExtMat);
      wallWHeader.position.set(-chW / 2 + chWT / 2, 3.9, 0);
      ctrlHouse.add(wallWLeft, wallWRight, wallWHeader);

      // Swung-open Double Steel Entry Doors & Danger Sign
      const doorMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.75, roughness: 0.35 });
      const openDoor = new THREE.Mesh(new THREE.BoxGeometry(1.1, 2.6, 0.08), doorMat);
      openDoor.position.set(-chW / 2 + 0.7, 1.7, -1.3);
      const doorSign = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.42), signMat);
      doorSign.position.set(-chW / 2 - 0.02, 2.1, -2.5);
      doorSign.rotation.y = -Math.PI / 2;
      ctrlHouse.add(openDoor, doorSign);

      // Partition Wall inside Control House separating 125V DC Battery Room (z > 1.8 local)
      const partWallL = new THREE.Mesh(new THREE.BoxGeometry(5.6, chWallH - 0.3, 0.18), wallIntMat);
      partWallL.position.set(1.2, chWallH / 2 + 0.25, 1.8);
      const partWallR = new THREE.Mesh(new THREE.BoxGeometry(1.4, chWallH - 0.3, 0.18), wallIntMat);
      partWallR.position.set(-3.3, chWallH / 2 + 0.25, 1.8);
      ctrlHouse.add(partWallL, partWallR);

      // Cutaway/Toggleable Control House Roof Slab
      const roofMat = new THREE.MeshStandardMaterial({
        color: 0x1e293b, roughness: 0.45, transparent: true, opacity: 0.92, side: THREE.DoubleSide
      });
      const roof = new THREE.Mesh(new THREE.BoxGeometry(chW + 0.6, 0.28, chL + 0.6), roofMat);
      roof.position.y = 4.75;
      ctrlHouse.add(roof);
      envGroup.userData.ctrlHouseRoof = roof;

      // Bright Interior LED Lighting for Control Room & Battery Room
      const ctrlRoomLight = new THREE.PointLight(0xf8fafc, 1.4, 18, 1.5);
      ctrlRoomLight.position.set(0, 3.8, -1.5);
      const battRoomLight = new THREE.PointLight(0xe0f2fe, 0.9, 12, 1.5);
      battRoomLight.position.set(0, 3.8, 3.5);
      ctrlHouse.add(ctrlRoomLight, battRoomLight);

      envGroup.add(ctrlHouse);

      // 4 Corner 16.0m Lightning Protection Masts (IEEE Std 998)
      const mastLocations = [
        { x: minX + 2.5, z: minZ + 2.5 },
        { x: maxX - 2.5, z: minZ + 2.5 },
        { x: maxX - 2.5, z: maxZ - 2.5 },
        { x: minX + 2.5, z: maxZ - 2.5 }
      ];

      mastLocations.forEach((m, idx) => {
        const mast = createLatticeMast(16.0, 1.8, 0.4);
        mast.position.set(m.x, 0, m.z);
        mast.name = `mast-${idx + 1}`;
        envGroup.add(mast);
      });

      scene.add(envGroup);
      return envGroup;
    }

    // BUILDER 2: INCOMING HV GANTRY TOWER & CONDUCTORS
    function buildGantryAndLines(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const pz = T.pz;
      const phaseZ = [-pz, 0, pz];
      const mastZ = Math.max(5.0, pz * 1.44);
      const gantryY = T.gantryWireY;
      const mastH = +(gantryY + 2.6).toFixed(2);
      const bellCount = vSpec.id === '230_138' ? 14 : (vSpec.id === '138_69' ? 10 : 6);
      const strLen = bellCount * 0.22;

      const gantryGroup = new THREE.Group();
      gantryGroup.name = 'gantry';
      gantryGroup.userData = { componentId: 'gantry' };
      gantryGroup.position.set(L.gantryX, 0, 0);

      const subparts = {};

      // 1. Lattice Steel Dead-End A-Frame Structure
      const latticeTower = new THREE.Group();
      latticeTower.name = 'gantry-lattice-tower';

      const legMat = MatLib.galvanizedSteel;
      const leftMast = createLatticeMast(mastH, 1.6, 0.5);
      leftMast.position.set(0, 0, -mastZ);
      latticeTower.add(leftMast);

      const rightMast = createLatticeMast(mastH, 1.6, 0.5);
      rightMast.position.set(0, 0, mastZ);
      latticeTower.add(rightMast);

      const crossarm = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.0, mastZ * 2 + 2.0), legMat);
      crossarm.position.set(0, gantryY, 0);
      crossarm.castShadow = true;
      latticeTower.add(crossarm);

      gantryGroup.add(latticeTower);
      latticeTower.userData.basePos = latticeTower.position.clone();
      subparts['gantry-lattice-tower'] = latticeTower;

      // 2. Overhead Ground Shield Wire (OHGW) at Gantry Apex
      const ohgwGroup = new THREE.Group();
      ohgwGroup.name = 'gantry-ohgw-shield';
      const ohgwGeo = new THREE.CylinderGeometry(0.015, 0.015, 16.0, 8);
      const ohgwMat = MatLib.galvanizedSteel;

      [-mastZ, mastZ].forEach(z => {
        const peakSpike = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 2.0, 6), legMat);
        peakSpike.position.set(0, mastH + 0.5, z);
        ohgwGroup.add(peakSpike);
        const wire = new THREE.Mesh(ohgwGeo, ohgwMat);
        wire.position.set(-8.0, mastH + 1.0, z);
        wire.rotation.z = Math.PI / 2;
        ohgwGroup.add(wire);
      });

      gantryGroup.add(ohgwGroup);
      ohgwGroup.userData.basePos = ohgwGroup.position.clone();
      subparts['gantry-ohgw-shield'] = ohgwGroup;

      // 3. 3-Phase Suspension Insulator Strings with Arcing Horns & Corona Rings
      const stringsGroup = new THREE.Group();
      stringsGroup.name = 'gantry-insulator-strings';

      phaseZ.forEach(z => {
        const string = new THREE.Group();
        string.position.set(0, gantryY - 0.5, z);

        for (let i = 0; i < bellCount; i++) {
          const bell = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.08, 0.15, 12), MatLib.porcelainBrown);
          bell.position.x = i * 0.22;
          bell.rotation.z = Math.PI / 2;
          bell.castShadow = true;
          string.add(bell);
        }

        const horns = createArcingHorns(0.8 * Math.min(1.4, 0.8 + 0.2 * T.s));
        horns.position.set(strLen * 0.5, 0, 0);
        string.add(horns);

        if (vSpec.coronaRings) {
          const ring = createCoronaRing(0.34, 0.025);
          ring.rotation.x = 0;
          ring.rotation.z = Math.PI / 2;
          ring.position.set(strLen - 0.1, 0, 0);
          string.add(ring);
        }

        stringsGroup.add(string);
      });

      gantryGroup.add(stringsGroup);
      stringsGroup.userData.basePos = stringsGroup.position.clone();
      subparts['gantry-insulator-strings'] = stringsGroup;

      // 4. ACSR Phase Conductors + Continuous Curved Dropper to Rigid Bus (carries exact flowCurve)
      const acsrGroup = new THREE.Group();
      acsrGroup.name = 'gantry-acsr-conductors';
      const pipeStartX = Math.max(2.1, strLen + 0.65);
      const busEndX = Math.max(pipeStartX + 1.8, (L.laX - L.gantryX) + 0.15);
      phaseZ.forEach((z, idx) => {
        const linePt = new THREE.Vector3(-15.0, gantryY, z);
        const spanEnd = new THREE.Vector3(-0.3, gantryY - 0.35, z);
        const span = createCatenaryJumper(linePt, spanEnd, 0.32, 10, MatLib.copperConductor, vTag, 'incoming', vSpec.twinBundle);
        acsrGroup.add(span);

        const deadEndLoop = createCatenaryJumper(spanEnd, new THREE.Vector3(pipeStartX, gantryY - 0.5, z), 0.55, 8, MatLib.copperConductor, vTag, 'incoming', vSpec.twinBundle);
        acsrGroup.add(deadEndLoop);

        const dropStart = new THREE.Vector3(pipeStartX, gantryY - 0.5, z);
        const dropEnd = new THREE.Vector3(pipeStartX, T.busY, z);
        const dropper = createCatenaryJumper(dropStart, dropEnd, 0.12, 8, MatLib.aluminumBus, vTag, 'incoming', vSpec.twinBundle);
        acsrGroup.add(dropper);

        const pMark = createPhaseMarker(idx, 0.06, 0.16);
        pMark.position.copy(dropEnd);
        tagEnergizedTerminal(pMark, 'incoming', vTag);
        acsrGroup.add(pMark);
      });

      gantryGroup.add(acsrGroup);
      acsrGroup.userData.basePos = acsrGroup.position.clone();
      subparts['gantry-acsr-conductors'] = acsrGroup;

      // 5. Stockbridge Aeolian Vibration Dampers
      const damperGroup = new THREE.Group();
      damperGroup.name = 'gantry-dampers';
      phaseZ.forEach(z => {
        const d = new THREE.Group();
        d.position.set(-1.8, gantryY - 0.35, z);
        const clamp = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 0.08), MatLib.galvanizedSteel);
        const mWire = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.45, 6), MatLib.galvanizedSteel);
        mWire.rotation.x = Math.PI / 2;
        const w1 = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.12, 8), MatLib.galvanizedSteel);
        w1.position.z = -0.22;
        const w2 = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.14, 8), MatLib.galvanizedSteel);
        w2.position.z = 0.22;
        d.add(clamp, mWire, w1, w2);
        damperGroup.add(d);
      });

      gantryGroup.add(damperGroup);
      damperGroup.userData.basePos = damperGroup.position.clone();
      subparts['gantry-dampers'] = damperGroup;

      // 6. Rigid Tubular Aluminum Busbars spanning cleanly toward Surge Arrester / Line Bay
      const busGroup = new THREE.Group();
      busGroup.name = 'gantry-tubular-bus';
      phaseZ.forEach(z => {
        const pipe = createRigidBusSegment(
          new THREE.Vector3(pipeStartX, T.busY, z),
          new THREE.Vector3(busEndX, T.busY, z),
          0.045, MatLib.aluminumBus, vTag, 'incoming', vSpec.twinBundle
        );
        const supPed = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, T.busY - 0.1, 8), MatLib.galvanizedSteel);
        supPed.position.set(pipeStartX, (T.busY - 0.1) * 0.35, z);
        supPed.scale.y = 0.7;
        busGroup.add(pipe);
      });

      gantryGroup.add(busGroup);
      busGroup.userData.basePos = busGroup.position.clone();
      subparts['gantry-tubular-bus'] = busGroup;

      gantryGroup.userData.subparts = subparts;
      Object.keys(subparts).forEach(id => tagSubpartHierarchy(subparts[id], id));
      scene.add(gantryGroup);
      return gantryGroup;
    }

    // BUILDER 3: STATION CLASS SURGE ARRESTERS (SA)
    function buildSurgeArresters(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const shedsCount = Math.max(12, Math.round(16 * s));
      const colH = +(2.85 * s).toFixed(3);
      const phaseZ = [-T.pz, 0, T.pz];

      const arresterGroup = new THREE.Group();
      arresterGroup.name = 'arrester';
      arresterGroup.userData = { componentId: 'arrester' };
      arresterGroup.position.set(L.laX, 0, 0);

      const subparts = {};

      phaseZ.forEach(z => {
        const ped = new THREE.Group();
        ped.position.set(0, 0, z);
        const legGeo = new THREE.BoxGeometry(0.08, 2.3, 0.08);
        [[-0.32, -0.32], [0.32, -0.32], [-0.32, 0.32], [0.32, 0.32]].forEach(([lx, lz]) => {
          const leg = new THREE.Mesh(legGeo, MatLib.galvanizedSteel);
          leg.position.set(lx, 1.15, lz);
          leg.castShadow = true;
          ped.add(leg);
        });
        [0.65, 1.45, 2.24].forEach(y => {
          const ringX = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.06, 0.06), MatLib.galvanizedSteel);
          ringX.position.set(0, y, -0.32);
          const ringX2 = ringX.clone(); ringX2.position.z = 0.32;
          const ringZ = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.72), MatLib.galvanizedSteel);
          ringZ.position.set(-0.32, y, 0);
          const ringZ2 = ringZ.clone(); ringZ2.position.x = 0.32;
          ped.add(ringX, ringX2, ringZ, ringZ2);
        });
        const capPlate = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.08, 0.82), MatLib.galvanizedSteel);
        capPlate.position.y = 2.3;
        ped.add(capPlate);

        const insBase = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.30, 0.25, 12), MatLib.darkSteel);
        insBase.position.set(0, 2.46, z);
        arresterGroup.add(ped, insBase);
      });

      // 1. Line Terminal Studs & NEMA 4-Hole Clamps
      const termGroup = new THREE.Group();
      termGroup.name = 'la-terminal-stud';
      phaseZ.forEach((z, idx) => {
        const term = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.038, 0.28, 10), MatLib.silverContact);
        term.position.set(0, T.laTopY - 0.10, z);
        const clamp = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.08, 0.22), MatLib.aluminumBus);
        clamp.position.set(0, T.laTopY, z);
        tagEnergizedTerminal(clamp, 'incoming', vTag);
        const pMark = createPhaseMarker(idx, 0.05, 0.10);
        pMark.position.set(0, T.laTopY - 0.16, z);
        termGroup.add(term, clamp, pMark);
      });
      arresterGroup.add(termGroup);
      termGroup.userData.basePos = termGroup.position.clone();
      subparts['la-terminal-stud'] = termGroup;

      // 2. Electrostatic Double-Toroid Corona / Grading Rings
      const ringGroup = new THREE.Group();
      ringGroup.name = 'la-grading-ring';
      const ringY = 2.58 + colH - 0.15;
      const ringR = 0.46 * Math.min(1.45, 0.85 + 0.22 * s);
      phaseZ.forEach(z => {
        const ring = createCoronaRing(ringR, 0.032);
        ring.position.set(0, ringY, z);
        const innerRing = createCoronaRing(ringR * 0.70, 0.022);
        innerRing.position.set(0, ringY + 0.15, z);
        for (let a = 0; a < 3; a++) {
          const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, ringR, 6), MatLib.aluminumBus);
          strut.position.set(Math.cos(a * 2.09) * ringR * 0.5, ringY, z + Math.sin(a * 2.09) * ringR * 0.5);
          strut.rotation.z = Math.PI / 2;
          strut.rotation.y = -a * 2.09;
          ringGroup.add(strut);
        }
        ringGroup.add(ring, innerRing);
      });
      arresterGroup.add(ringGroup);
      ringGroup.userData.basePos = ringGroup.position.clone();
      subparts['la-grading-ring'] = ringGroup;

      // 3. Stacked Metal-Oxide Varistor (MOV) Zinc-Oxide Disc Column
      const znoGroup = new THREE.Group();
      znoGroup.name = 'la-zno-stack';
      const discCount = Math.round(12 * s);
      const discStep = (colH * 0.92) / discCount;
      phaseZ.forEach(z => {
        for (let d = 0; d < discCount; d++) {
          const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.135, 0.135, discStep * 0.86, 18), MatLib.znoCeramic);
          disc.position.set(0, 2.68 + d * discStep, z);
          znoGroup.add(disc);
        }
      });
      arresterGroup.add(znoGroup);
      znoGroup.userData.basePos = znoGroup.position.clone();
      subparts['la-zno-stack'] = znoGroup;

      // 4. Filament-Wound Fiberglass Reinforcing Tube
      const frpGroup = new THREE.Group();
      frpGroup.name = 'la-fiberglass-tube';
      phaseZ.forEach(z => {
        const frp = new THREE.Mesh(new THREE.CylinderGeometry(0.165, 0.165, colH * 0.97, 16), MatLib.fiberglassTube);
        frp.position.set(0, 2.58 + colH / 2, z);
        frpGroup.add(frp);
      });
      arresterGroup.add(frpGroup);
      frpGroup.userData.basePos = frpGroup.position.clone();
      subparts['la-fiberglass-tube'] = frpGroup;

      // 5. Alternating Polymer Silicone Rubber Weather Sheds
      const shedsGroup = new THREE.Group();
      shedsGroup.name = 'la-polymer-sheds';
      phaseZ.forEach(z => {
        const sheds = createRibbedInsulator(colH, 0.22, shedsCount, MatLib.siliconePolymer, true);
        sheds.position.set(0, 2.58 + colH / 2, z);
        shedsGroup.add(sheds);
      });
      arresterGroup.add(shedsGroup);
      shedsGroup.userData.basePos = shedsGroup.position.clone();
      subparts['la-polymer-sheds'] = shedsGroup;

      // 6. Eye-Level Digital Surge Counters, Milliammeters & Low-Inductance Ground Leads
      const countGroup = new THREE.Group();
      countGroup.name = 'la-surge-counter';
      const surgeTex = TextureGen.createGaugeDialTexture('surge');
      const surgeDialMat = new THREE.MeshBasicMaterial({ map: surgeTex });
      phaseZ.forEach(z => {
        const box = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.36, 0.28), MatLib.galvanizedSteel);
        box.position.set(0.52, 1.55, z);
        const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.04, 18), MatLib.crgoCoreSteel);
        bezel.position.set(0.66, 1.55, z);
        bezel.rotation.z = Math.PI / 2;
        const meter = new THREE.Mesh(new THREE.CircleGeometry(0.10, 18), surgeDialMat);
        meter.position.set(0.685, 1.55, z);
        meter.rotation.y = Math.PI / 2;
        const strapTop = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 1.1, 8), MatLib.copperConductor);
        strapTop.position.set(0.32, 2.25, z);
        strapTop.rotation.z = Math.PI / 4;
        const gWire = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 1.4, 8), MatLib.groundCopper);
        gWire.position.set(0.52, 0.7, z);
        countGroup.add(box, bezel, meter, strapTop, gWire);
      });
      arresterGroup.add(countGroup);
      countGroup.userData.basePos = countGroup.position.clone();
      subparts['la-surge-counter'] = countGroup;

      arresterGroup.userData.subparts = subparts;
      Object.keys(subparts).forEach(id => tagSubpartHierarchy(subparts[id], id));
      scene.add(arresterGroup);
      return arresterGroup;
    }

    // BUILDER 4: INSTRUMENT TRANSFORMERS (CT & VT)
    function buildInstrumentTransformers(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const colH = +(2.85 * s).toFixed(3);
      const shedsCount = Math.max(12, vSpec.hvShedsCount || 14);
      const phaseZ = [-T.pz, 0, T.pz];
      const headY = T.ctTopY;

      const ctvtGroup = new THREE.Group();
      ctvtGroup.name = 'ctvt';
      ctvtGroup.userData = { componentId: 'ctvt' };
      ctvtGroup.position.set(L.ctX, 0, 0);

      const subparts = {};

      phaseZ.forEach(z => {
        const stand = new THREE.Mesh(new THREE.BoxGeometry(0.9, 2.2, 0.9), MatLib.galvanizedSteel);
        stand.position.set(0, 1.1, z);
        stand.castShadow = true;
        ctvtGroup.add(stand);
      });

      // 1. Primary Conductor Pass-Through Aluminum Head Chamber & Bolted Terminals (carries internal flowCurve)
      const headGroup = new THREE.Group();
      headGroup.name = 'ct-primary-head';
      phaseZ.forEach((z, idx) => {
        const head = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.38, 0.65, 20), MatLib.aluminumBus);
        head.position.set(0, headY, z);
        head.rotation.z = Math.PI / 2;
        const busStud = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 1.35, 12), MatLib.copperConductor);
        busStud.position.set(0, headY, z);
        busStud.rotation.z = Math.PI / 2;
        [-0.65, 0.65].forEach(px => {
          const pad = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 0.14), MatLib.silverContact);
          pad.position.set(px, headY, z);
          tagEnergizedTerminal(pad, 'incoming', vTag);
          headGroup.add(pad);
        });
        if (vSpec.coronaRings) {
          const cRing = createCoronaRing(0.48, 0.026);
          cRing.position.set(0, headY - 0.35, z);
          headGroup.add(cRing);
        }
        const intFlow = new THREE.Object3D();
        intFlow.userData.flowCurve = new THREE.LineCurve3(new THREE.Vector3(-0.65, headY, z), new THREE.Vector3(0.65, headY, z));
        intFlow.userData.voltageTag = vTag;
        intFlow.userData.circuitTag = 'incoming';
        const pMark = createPhaseMarker(idx, 0.06, 0.14);
        pMark.position.set(-0.5, headY, z);
        pMark.rotation.z = Math.PI / 2;
        headGroup.add(head, busStud, pMark, intFlow);
      });
      ctvtGroup.add(headGroup);
      headGroup.userData.basePos = headGroup.position.clone();
      subparts['ct-primary-head'] = headGroup;

      // 2. Toroidal Metering Core
      const mtrCoreGroup = new THREE.Group();
      mtrCoreGroup.name = 'ct-metering-core';
      phaseZ.forEach(z => {
        const toroid = new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.075, 14, 28), new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.65, roughness: 0.35 }));
        toroid.position.set(-0.16, headY, z);
        toroid.rotation.y = Math.PI / 2;
        mtrCoreGroup.add(toroid);
      });
      ctvtGroup.add(mtrCoreGroup);
      mtrCoreGroup.userData.basePos = mtrCoreGroup.position.clone();
      subparts['ct-metering-core'] = mtrCoreGroup;

      // 3. Toroidal Protection Relaying Core
      const protCoreGroup = new THREE.Group();
      protCoreGroup.name = 'ct-relaying-core';
      phaseZ.forEach(z => {
        const toroid = new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.085, 14, 28), new THREE.MeshStandardMaterial({ color: 0xb91c1c, metalness: 0.65, roughness: 0.35 }));
        toroid.position.set(0.16, headY, z);
        toroid.rotation.y = Math.PI / 2;
        protCoreGroup.add(toroid);
      });
      ctvtGroup.add(protCoreGroup);
      protCoreGroup.userData.basePos = protCoreGroup.position.clone();
      subparts['ct-relaying-core'] = protCoreGroup;

      // 4. Porcelain Insulator Body with Alternating Weather Sheds
      const porcGroup = new THREE.Group();
      porcGroup.name = 'ct-porcelain-body';
      phaseZ.forEach(z => {
        const col = createRibbedInsulator(colH, 0.28, shedsCount, MatLib.porcelainBrown, true);
        col.position.set(0, 2.2 + colH / 2, z);
        porcGroup.add(col);
      });
      ctvtGroup.add(porcGroup);
      porcGroup.userData.basePos = porcGroup.position.clone();
      subparts['ct-porcelain-body'] = porcGroup;

      // 5. Stainless Steel Expansion Bellows Dome & Oil Sight Window
      const bellowsGroup = new THREE.Group();
      bellowsGroup.name = 'ct-bellows';
      const oilDialMat = new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('oillevel') });
      phaseZ.forEach(z => {
        const bellow = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.36, 20), MatLib.silverContact);
        bellow.position.set(0, headY + 0.48, z);
        const cap = new THREE.Mesh(new THREE.SphereGeometry(0.34, 18, 10, 0, Math.PI * 2, 0, Math.PI / 2), MatLib.aluminumBus);
        cap.position.set(0, headY + 0.66, z);
        const sight = new THREE.Mesh(new THREE.CircleGeometry(0.08, 16), oilDialMat);
        sight.position.set(0.35, headY + 0.48, z);
        sight.rotation.y = Math.PI / 2;
        bellowsGroup.add(bellow, cap, sight);
      });
      ctvtGroup.add(bellowsGroup);
      bellowsGroup.userData.basePos = bellowsGroup.position.clone();
      subparts['ct-bellows'] = bellowsGroup;

      // 6. Secondary Terminal Marshalling Box (IP55) with Conduit Drops (bolted flush to steel stand)
      const boxGroup = new THREE.Group();
      boxGroup.name = 'ct-sec-box';
      phaseZ.forEach(z => {
        const box = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.58, 0.44), MatLib.galvanizedSteel);
        box.position.set(0.46, 1.65, z);
        const conduit = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.65, 8), MatLib.galvanizedSteel);
        conduit.position.set(0.46, 0.825, z);
        boxGroup.add(box, conduit);
      });
      ctvtGroup.add(boxGroup);
      boxGroup.userData.basePos = boxGroup.position.clone();
      subparts['ct-sec-box'] = boxGroup;

      ctvtGroup.userData.subparts = subparts;
      Object.keys(subparts).forEach(id => tagSubpartHierarchy(subparts[id], id));
      scene.add(ctvtGroup);
      return ctvtGroup;
    }

    // BUILDER 5: MOTORIZED DISCONNECT / ISOLATOR SWITCH (DS-69-1 with Earth Blade 89E)
    function buildDisconnectSwitch(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const pz = T.pz;
      const phaseZ = [-pz, 0, pz];
      const postH = +(2.35 * s).toFixed(3);
      const termY = T.dsTermY;
      const shedsCount = Math.max(10, vSpec.shedsCount || 12);

      const discGroup = new THREE.Group();
      discGroup.name = 'disconnect';
      discGroup.userData = { componentId: 'disconnect', isOpen: false, isEarthClosed: false, termHeight: termY, termOffsetX: 0.75 };
      discGroup.position.set(L.dsX, 0, L.dsZ || 0);
      discGroup.rotation.y = L.dsRot || 0;

      const subparts = {};

      // 1. Galvanized C-Channel Steel Base Frame & Rotary Bearing Housings
      const baseGroup = new THREE.Group();
      baseGroup.name = 'ds-base-frame';
      phaseZ.forEach(z => {
        const channelBeam = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.18, 0.42), MatLib.galvanizedSteel);
        channelBeam.position.set(0, 2.1, z);
        channelBeam.castShadow = true;
        baseGroup.add(channelBeam);

        [-0.95, 0.95].forEach(lx => {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.14, 2.05, 0.14), MatLib.galvanizedSteel);
          leg.position.set(lx, 1.025, z);
          leg.castShadow = true;
          const foot = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.06, 0.3), MatLib.galvanizedSteel);
          foot.position.set(lx, 0.03, z);
          baseGroup.add(leg, foot);
        });

        const crossBrace = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.06, 0.06), MatLib.galvanizedSteel);
        crossBrace.position.set(0, 1.0, z);
        crossBrace.rotation.z = 0.35;
        baseGroup.add(crossBrace);

        [-0.75, 0.75].forEach(bx => {
          const bearing = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.16, 16), MatLib.darkSteel);
          bearing.position.set(bx, 2.27, z);
          baseGroup.add(bearing);
        });
      });
      discGroup.add(baseGroup);
      baseGroup.userData.basePos = baseGroup.position.clone();
      subparts['ds-base-frame'] = baseGroup;

      // 2. Rotating Alternating-Shed Porcelain Station Post Insulator Stacks
      const insulGroup = new THREE.Group();
      insulGroup.name = 'ds-insulators';
      const postMeshes = [];
      phaseZ.forEach(z => {
        [-0.75, 0.75].forEach((x, idx) => {
          const post = createRibbedInsulator(postH, 0.19, shedsCount, MatLib.porcelainBrown, true);
          post.position.set(x, 2.35 + postH / 2, z);
          insulGroup.add(post);

          const headCap = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.18, 0.14, 16), MatLib.aluminumBus);
          headCap.position.set(x, termY - 0.06, z);
          tagEnergizedTerminal(headCap, idx === 0 ? 'incoming' : 'post_dsA', vTag);
          insulGroup.add(headCap);
          if (vSpec.coronaRings) {
            const cRing = createCoronaRing(0.30, 0.024);
            cRing.position.set(x, termY - 0.16, z);
            insulGroup.add(cRing);
          }
          postMeshes.push(post);
        });
      });
      discGroup.add(insulGroup);
      insulGroup.userData.basePos = insulGroup.position.clone();
      subparts['ds-insulators'] = insulGroup;

      // 3. Tubular Copper Conducting Blades (Horizontal Center-Break)
      const bladesGroup = new THREE.Group();
      bladesGroup.name = 'ds-conducting-blades';
      const bladeArms = [];
      phaseZ.forEach(z => {
        const makeArmGroup = (xCenter) => {
          const armGrp = new THREE.Group();
          const tube = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.042, 0.74, 12), MatLib.copperConductor);
          tube.rotation.z = Math.PI / 2;
          const silverTip = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.09, 0.08), MatLib.silverContact);
          silverTip.position.set(xCenter < 0 ? 0.34 : -0.34, 0, 0);
          const pivotCollar = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.12, 12), MatLib.aluminumBus);
          pivotCollar.position.set(xCenter < 0 ? -0.34 : 0.34, 0, 0);
          armGrp.add(tube, silverTip, pivotCollar);
          armGrp.position.set(xCenter, termY, z);
          return armGrp;
        };
        const arm1 = makeArmGroup(-0.37);
        const arm2 = makeArmGroup(0.37);
        const bFlow = new THREE.Object3D();
        bFlow.userData.flowCurve = new THREE.LineCurve3(new THREE.Vector3(-0.75, termY, z), new THREE.Vector3(0.75, termY, z));
        bFlow.userData.voltageTag = vTag;
        bFlow.userData.circuitTag = 'post_dsA';
        bladesGroup.add(arm1, arm2, bFlow);
        bladeArms.push({ arm1, arm2, z });
      });
      discGroup.add(bladesGroup);
      bladesGroup.userData.basePos = bladesGroup.position.clone();
      subparts['ds-conducting-blades'] = bladesGroup;
      discGroup.userData.bladeArms = bladeArms;

      // 4. Silver-Plated Fixed Jaw Fingers & Twin Corona Grading Rings
      const jawsGroup = new THREE.Group();
      jawsGroup.name = 'ds-jaw-contacts';
      phaseZ.forEach(z => {
        [-0.04, 0.04].forEach(jz => {
          const finger = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.14, 0.03), MatLib.silverContact);
          finger.position.set(0, termY, z + jz);
          jawsGroup.add(finger);
        });
        const corona = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.022, 8, 20), MatLib.aluminumBus);
        corona.position.set(0, termY, z);
        corona.rotation.y = Math.PI / 2;
        jawsGroup.add(corona);
      });
      discGroup.add(jawsGroup);
      jawsGroup.userData.basePos = jawsGroup.position.clone();
      subparts['ds-jaw-contacts'] = jawsGroup;

      // 5. Motor Operating Mechanism Cabinet & Vertical/Torsion Pipe Linkage
      const mechGroup = new THREE.Group();
      mechGroup.name = 'ds-operating-mech';
      const cabZ = pz + 1.35;
      const cabinet = new THREE.Mesh(new THREE.BoxGeometry(0.68, 1.15, 0.56), MatLib.galvanizedSteel);
      cabinet.position.set(0, 1.25, cabZ);
      cabinet.castShadow = true;
      const cabWindow = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.35, 0.32), MatLib.cabinetGlass);
      cabWindow.position.set(0.35, 1.4, cabZ);
      const handCrank = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.35, 8), MatLib.yellowHighlight);
      handCrank.position.set(0.38, 1.0, cabZ);
      handCrank.rotation.x = Math.PI / 2;
      const vertPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 1.35, 8), MatLib.galvanizedSteel);
      vertPipe.position.set(0, 1.9, cabZ - 0.35);
      const torsionPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, pz * 2 + 1.6, 10), MatLib.galvanizedSteel);
      torsionPipe.position.set(0, 2.25, 0.2);
      torsionPipe.rotation.x = Math.PI / 2;
      mechGroup.add(cabinet, cabWindow, handCrank, vertPipe, torsionPipe);
      discGroup.add(mechGroup);
      mechGroup.userData.basePos = mechGroup.position.clone();
      subparts['ds-operating-mech'] = mechGroup;

      // 6. Mechanically Interlocked Earthing Switch Blade (ANSI 89E) & Ground Shunt
      const earthGroup = new THREE.Group();
      earthGroup.name = 'ds-earth-blade';
      const earthBlades = [];
      phaseZ.forEach(z => {
        const eBlade = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.026, 2.35 * Math.min(1.6, s), 10), MatLib.copperConductor);
        eBlade.position.set(-0.82, 2.3 + 1.02 * s, z);
        eBlade.rotation.z = Math.PI / 3;
        const earthHinge = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 0.14), MatLib.copperConductor);
        earthHinge.position.set(-0.92, 2.28, z);
        const shunt = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.2, 0.08), MatLib.copperConductor);
        shunt.position.set(-1.02, 1.15, z);
        earthGroup.add(eBlade, earthHinge, shunt);
        earthBlades.push(eBlade);
      });
      discGroup.add(earthGroup);
      earthGroup.userData.basePos = earthGroup.position.clone();
      subparts['ds-earth-blade'] = earthGroup;
      discGroup.userData.earthBlades = earthBlades;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      discGroup.userData.subparts = subparts;
      scene.add(discGroup);
      return discGroup;
    }

    // BUILDER 6: HV SF6 DEAD-TANK CIRCUIT BREAKER (52-69 / 52-TIE)
    function buildCircuitBreaker(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const pz = T.pz;
      const phaseZ = [-pz, 0, pz];
      const bushH = +(2.25 * s).toFixed(3);
      const tilt = Math.PI / 10;
      const padX = T.cbTermOffsetX;
      const padY = T.cbTermY;
      const shedsCount = Math.max(10, vSpec.shedsCount || 12);

      const cbGroup = new THREE.Group();
      cbGroup.name = 'breaker';
      cbGroup.userData = { componentId: 'breaker', isTripped: false, termHeight: padY, termOffsetX: padX };
      cbGroup.position.set(L.cbX, 0, L.cbZ || 0);
      cbGroup.rotation.y = L.cbRot || 0;

      const subparts = {};

      // Open Galvanized Steel Portal Support Legs & Sill Beams
      const portalFrame = new THREE.Group();
      phaseZ.forEach(z => {
        [-1.05, 1.05].forEach(lx => {
          const post = new THREE.Mesh(new THREE.BoxGeometry(0.18, 1.5, 0.2), MatLib.galvanizedSteel);
          post.position.set(lx, 0.75, z);
          post.castShadow = true;
          portalFrame.add(post);
        });
        const crossCradle = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.16, 0.34), MatLib.galvanizedSteel);
        crossCradle.position.set(0, 1.48, z);
        portalFrame.add(crossCradle);
      });
      [-1.05, 1.05].forEach(lx => {
        const longBeam = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.18, pz * 2 + 0.6), MatLib.galvanizedSteel);
        longBeam.position.set(lx, 0.65, 0);
        portalFrame.add(longBeam);
      });
      cbGroup.add(portalFrame);

      // 1. Ribbed Cast-Aluminum Dead-Tanks & Bolted Flanges
      const tankGroup = new THREE.Group();
      tankGroup.name = 'cb-tank';
      phaseZ.forEach(z => {
        const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.56, 0.56, 2.85, 24), MatLib.transformerTank);
        tank.position.set(0, 2.1, z);
        tank.rotation.z = Math.PI / 2;
        tank.castShadow = true;
        tankGroup.add(tank);

        [-1.44, 1.44].forEach(fx => {
          const endFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.07, 24), MatLib.darkSteel);
          endFlange.position.set(fx, 2.1, z);
          endFlange.rotation.z = Math.PI / 2;
          tankGroup.add(endFlange);
        });
        const manifold = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.65, 8), MatLib.copperConductor);
        manifold.position.set(0.65, 1.5, z);
        tankGroup.add(manifold);
      });
      cbGroup.add(tankGroup);
      tankGroup.userData.basePos = tankGroup.position.clone();
      subparts['cb-tank'] = tankGroup;

      // 2. Alternating-Shed Porcelain Bushings, BCT Toroids & Arcing Horns
      const bushGroup = new THREE.Group();
      bushGroup.name = 'cb-bushings';
      phaseZ.forEach(z => {
        [-0.82, 0.82].forEach((x, bIdx) => {
          const sign = bIdx === 0 ? -1 : 1;
          // Seat bushing base inside turret flange at (sign * 0.78, 2.45, z) and align exact axis to (padX, padY)
          const bxMid = sign * (0.78 + 0.5 * bushH * Math.sin(tilt));
          const byMid = 2.45 + 0.5 * bushH * Math.cos(tilt);
          const bushing = createRibbedInsulator(bushH, 0.22, shedsCount, MatLib.porcelainBrown, true);
          bushing.position.set(bxMid, byMid, z);
          bushing.rotation.z = bIdx === 0 ? tilt : -tilt;
          bushGroup.add(bushing);

          const bctCollar = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.34, 0.36, 18), MatLib.darkSteel);
          bctCollar.position.set(sign * (0.78 + 0.22 * Math.sin(tilt)), 2.45 + 0.22 * Math.cos(tilt), z);
          bctCollar.rotation.z = bIdx === 0 ? tilt : -tilt;
          bushGroup.add(bctCollar);

          const horns = createArcingHorns(0.7);
          horns.position.set(sign * (padX - 0.08), padY - 0.16, z);
          bushGroup.add(horns);

          if (vSpec.coronaRings) {
            const cRing = createCoronaRing(0.38, 0.028);
            cRing.position.set(sign * padX, padY - 0.18, z);
            bushGroup.add(cRing);
          }
        });
      });
      cbGroup.add(bushGroup);
      bushGroup.userData.basePos = bushGroup.position.clone();
      subparts['cb-bushings'] = bushGroup;

      // 3. Silver-Plated NEMA Terminal Palm Pads & Braided Copper Shunts (carries internal flowCurve)
      const padGroup = new THREE.Group();
      padGroup.name = 'cb-terminal-pads';
      phaseZ.forEach(z => {
        [-padX, padX].forEach((x, idx) => {
          const pad = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.08, 0.22), MatLib.silverContact);
          pad.position.set(x, padY, z);
          tagEnergizedTerminal(pad, idx === 0 ? 'post_dsA' : 'post_cbMain', vTag);
          const braid = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.04, 0.14), MatLib.copperConductor);
          braid.position.set(x * 0.94, padY - 0.07, z);
          padGroup.add(pad, braid);
        });
        const intFlow = new THREE.Object3D();
        intFlow.userData.flowCurve = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-padX, padY, z),
          new THREE.Vector3(-0.6, 2.1, z),
          new THREE.Vector3(0.6, 2.1, z),
          new THREE.Vector3(padX, padY, z)
        ]);
        intFlow.userData.voltageTag = vTag;
        intFlow.userData.circuitTag = 'post_cbMain';
        padGroup.add(intFlow);
      });
      cbGroup.add(padGroup);
      padGroup.userData.basePos = padGroup.position.clone();
      subparts['cb-terminal-pads'] = padGroup;

      // 4. SF6 Interrupter Chambers
      const intGroup = new THREE.Group();
      intGroup.name = 'cb-interrupter';
      phaseZ.forEach(z => {
        const chamber = new THREE.Mesh(new THREE.CylinderGeometry(0.29, 0.29, 1.85, 18), new THREE.MeshStandardMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.48, roughness: 0.2 }));
        chamber.position.set(0, 2.1, z);
        chamber.rotation.z = Math.PI / 2;
        [-0.7, 0.7].forEach(sx => {
          const shield = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.12, 16), MatLib.aluminumBus);
          shield.position.set(sx, 2.1, z);
          shield.rotation.z = Math.PI / 2;
          intGroup.add(shield);
        });
        intGroup.add(chamber);
      });
      cbGroup.add(intGroup);
      intGroup.userData.basePos = intGroup.position.clone();
      subparts['cb-interrupter'] = intGroup;

      // 5. Fixed Tulip & Moving Arcing Contacts + PTFE Puffer Nozzle
      const contGroup = new THREE.Group();
      contGroup.name = 'cb-contacts';
      const contactsList = [];
      phaseZ.forEach(z => {
        const fixedCont = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.52, 12), MatLib.copperWinding);
        fixedCont.position.set(-0.35, 2.1, z);
        fixedCont.rotation.z = Math.PI / 2;

        const movingCont = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 0.52, 12), MatLib.silverContact);
        movingCont.position.set(0.35, 2.1, z);
        movingCont.rotation.z = Math.PI / 2;

        const nozzle = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.38, 18), new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.18 }));
        nozzle.position.set(0.1, 2.1, z);
        nozzle.rotation.z = -Math.PI / 2;

        contGroup.add(fixedCont, movingCont, nozzle);
        contactsList.push({ movingCont, fixedCont, z });
      });
      cbGroup.add(contGroup);
      contGroup.userData.basePos = contGroup.position.clone();
      subparts['cb-contacts'] = contGroup;
      cbGroup.userData.contactsList = contactsList;

      // 6. Spring-Charged Operating Mechanism Cabinet
      const mechCabGroup = new THREE.Group();
      mechCabGroup.name = 'cb-operating-mech';
      const cabBox = new THREE.Mesh(new THREE.BoxGeometry(1.18, 1.82, 1.04), MatLib.galvanizedSteel);
      cabBox.position.set(1.42, 1.5, 0);
      const glassWindow = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.15, 0.72), MatLib.cabinetGlass);
      glassWindow.position.set(2.02, 1.55, 0);

      const springCore = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.85, 12), MatLib.yellowHighlight);
      springCore.position.set(1.85, 1.55, 0.16);
      const chargeMotor = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.34, 12), MatLib.darkSteel);
      chargeMotor.position.set(1.85, 1.18, -0.18);
      chargeMotor.rotation.z = Math.PI / 2;
      const tripCoil = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.24, 10), MatLib.hazardRed);
      tripCoil.position.set(1.88, 1.85, -0.16);
      const closeCoil = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.24, 10), MatLib.safeGreen);
      closeCoil.position.set(1.88, 1.55, -0.16);

      mechCabGroup.add(cabBox, glassWindow, springCore, chargeMotor, tripCoil, closeCoil);
      cbGroup.add(mechCabGroup);
      mechCabGroup.userData.basePos = mechCabGroup.position.clone();
      subparts['cb-operating-mech'] = mechCabGroup;

      // 7. SF6 Gas Density / Pressure Gauge Dial (bolted flush to cabinet front face x = 2.01)
      const gaugeGroup = new THREE.Group();
      gaugeGroup.name = 'cb-gauge';
      const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.06, 20), MatLib.darkSteel);
      bezel.position.set(2.01, 2.08, -0.22);
      bezel.rotation.z = Math.PI / 2;
      const dialFace = new THREE.Mesh(
        new THREE.CircleGeometry(0.13, 24),
        new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('sf6') })
      );
      dialFace.position.set(2.045, 2.08, -0.22);
      dialFace.rotation.y = Math.PI / 2;
      const capillary = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.75, 8), MatLib.copperConductor);
      capillary.position.set(1.58, 2.08, -0.22);
      capillary.rotation.z = Math.PI / 2;
      const cabBracket = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.08, 0.45), MatLib.darkSteel);
      cabBracket.position.set(1.22, 2.05, 0);
      gaugeGroup.add(bezel, dialFace, capillary, cabBracket);
      cbGroup.add(gaugeGroup);
      gaugeGroup.userData.basePos = gaugeGroup.position.clone();
      subparts['cb-gauge'] = gaugeGroup;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      cbGroup.userData.subparts = subparts;
      scene.add(cbGroup);
      return cbGroup;
    }

    // BUILDER 7: MAIN POWER TRANSFORMER (TR-01)
    function buildPowerTransformer(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vHvTag = vSpec.hvKv + 'kV';
      const vLvTag = vSpec.lvKv + 'kV';
      const k = T.txTankScale;
      const s = T.s;
      const lvS = T.lvS;
      const coverY = T.txCoverY;
      const tankH = +(3.8 * k).toFixed(3);
      const tankW = +(4.2 * k).toFixed(3);
      const tankL = +(5.6 * k).toFixed(3);
      const hvBushH = +(2.65 * s).toFixed(3);
      const lvBushH = +(1.55 * lvS).toFixed(3);
      const hvTilt = Math.PI / 22;

      const txGroup = new THREE.Group();
      txGroup.name = 'transformer';
      txGroup.userData = { componentId: 'transformer' };
      txGroup.position.set(L.txX, 0, L.txZ || 0);

      const subparts = {};

      // 1. Corrugated Steel Tank, Explosion Vent Pipe & Pressure Relief Device (PRD)
      const tankGroup = new THREE.Group();
      tankGroup.name = 'tx-tank';
      const tankMesh = new THREE.Mesh(new THREE.BoxGeometry(tankW, tankH, tankL), MatLib.transformerTank);
      tankMesh.position.y = 0.2 + tankH / 2;
      tankMesh.castShadow = true;
      tankMesh.receiveShadow = true;
      tankGroup.add(tankMesh);

      for (let y = 0.8; y <= coverY - 0.3; y += 1.35 * k) {
        const rib = new THREE.Mesh(new THREE.BoxGeometry(tankW + 0.12, 0.09, tankL + 0.12), MatLib.radiatorFin);
        rib.position.y = y;
        tankGroup.add(rib);
      }
      for (let z = -tankL * 0.42; z <= tankL * 0.42; z += 0.6 * k) {
        [-(tankW / 2 + 0.04), (tankW / 2 + 0.04)].forEach(rx => {
          const vRib = new THREE.Mesh(new THREE.BoxGeometry(0.08, tankH * 0.95, 0.1), MatLib.radiatorFin);
          vRib.position.set(rx, 0.2 + tankH / 2, z);
          tankGroup.add(vRib);
        });
      }
      for (let x = -tankW * 0.4; x <= tankW * 0.4; x += 0.68 * k) {
        [-(tankL / 2 + 0.04), (tankL / 2 + 0.04)].forEach(rz => {
          const vRibZ = new THREE.Mesh(new THREE.BoxGeometry(0.1, tankH * 0.95, 0.08), MatLib.radiatorFin);
          vRibZ.position.set(x, 0.2 + tankH / 2, rz);
          tankGroup.add(vRibZ);
        });
      }
      [[-(tankW / 2 + 0.02), -2.6 * k], [(tankW / 2 + 0.02), -2.6 * k], [-(tankW / 2 + 0.02), 2.6 * k], [(tankW / 2 + 0.02), 2.6 * k]].forEach(([jx, jz]) => {
        const jack = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.25, 0.24), MatLib.darkSteel);
        jack.position.set(jx, 0.45, jz);
        tankGroup.add(jack);
      });

      const ventRiser = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 1.55, 16), MatLib.transformerTank);
      ventRiser.position.set(0.95 * k, coverY + 0.75, -1.9 * k);
      const ventBend = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.75, 16), MatLib.transformerTank);
      ventBend.position.set(1.22 * k, coverY + 1.42, -1.9 * k);
      ventBend.rotation.z = -Math.PI / 3;
      const prdBase = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.22, 0.28, 16), MatLib.silverContact);
      prdBase.position.set(1.2 * k, coverY + 0.14, -0.9 * k);
      const prdCap = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.18, 16), MatLib.hazardRed);
      prdCap.position.set(1.2 * k, coverY + 0.35, -0.9 * k);
      tankGroup.add(ventRiser, ventBend, prdBase, prdCap);

      txGroup.add(tankGroup);
      tankGroup.userData.basePos = tankGroup.position.clone();
      subparts['tx-tank'] = tankGroup;

      // 2. High-Voltage Alternating-Shed Condenser Bushings (H1, H2, H3)
      const hvBushGroup = new THREE.Group();
      hvBushGroup.name = 'tx-hv-bushings';
      T.txHvPhaseZ.forEach(z => {
        const turret = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.36, 0.42, 18), MatLib.transformerTank);
        turret.position.set(-1.0 * k, coverY + 0.18, z);
        hvBushGroup.add(turret);

        const bushMidX = -1.0 * k - 0.5 * hvBushH * Math.sin(hvTilt);
        const bushMidY = coverY + 0.22 + 0.5 * hvBushH * Math.cos(hvTilt);
        const bushing = createRibbedInsulator(hvBushH, 0.25, vSpec.hvShedsCount || 14, MatLib.porcelainBrown, true);
        bushing.position.set(bushMidX, bushMidY, z);
        bushing.rotation.z = hvTilt;
        hvBushGroup.add(bushing);

        const dome = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.15, 0.24, 14), MatLib.aluminumBus);
        dome.position.set(T.txHvStudX + 0.02 * Math.sin(hvTilt), T.txHvStudY - 0.16, z);
        const stud = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.28, 10), MatLib.copperConductor);
        stud.position.set(T.txHvStudX, T.txHvStudY, z);
        tagEnergizedTerminal(stud, 'tx_hv', vHvTag);
        hvBushGroup.add(dome, stud);

        const horns = createArcingHorns(0.85 * Math.min(1.4, 0.8 + 0.2 * s));
        horns.position.set(T.txHvStudX + 0.06, T.txHvStudY - 0.36, z);
        hvBushGroup.add(horns);

        if (vSpec.coronaRings) {
          const cRing = createCoronaRing(0.42, 0.03);
          cRing.position.set(T.txHvStudX, T.txHvStudY - 0.22, z);
          hvBushGroup.add(cRing);
        }
      });
      txGroup.add(hvBushGroup);
      hvBushGroup.userData.basePos = hvBushGroup.position.clone();
      subparts['tx-hv-bushings'] = hvBushGroup;

      // 3. Low/Secondary-Voltage Bushings (X1, X2, X3, X0 Neutral) elevated on upper roof throat compartment
      const lvBushGroup = new THREE.Group();
      lvBushGroup.name = 'tx-lv-bushings';
      const throatH = 0.52;
      const lvThroatBox = new THREE.Mesh(new THREE.BoxGeometry(0.88, throatH, 3.35), MatLib.transformerTank);
      lvThroatBox.position.set(T.txLvStudX, coverY + throatH / 2 - 0.04, -0.32);
      lvThroatBox.castShadow = true;
      lvBushGroup.add(lvThroatBox);
      T.txLvPhaseZ.forEach((z, idx) => {
        const turret = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.26, 0.32, 16), MatLib.transformerTank);
        turret.position.set(T.txLvStudX, coverY + throatH + 0.08, z);
        const bushBaseY = coverY + throatH + 0.16;
        const bushing = createRibbedInsulator(lvBushH, 0.18, Math.max(8, Math.round(10 * lvS)), MatLib.porcelainBrown, true);
        bushing.position.set(T.txLvStudX, bushBaseY + lvBushH / 2, z);
        const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.13, 0.14, 14), MatLib.aluminumBus);
        cap.position.set(T.txLvStudX, T.txLvStudY - 0.10, z);
        const flag = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.22, 0.06), idx === 3 ? MatLib.silverContact : MatLib.copperConductor);
        flag.position.set(T.txLvStudX, T.txLvStudY, z);
        if (idx < 3) tagEnergizedTerminal(flag, 'sec_lv', vLvTag);
        if (vSpec.lvKv >= 138) {
          const cRing = createCoronaRing(0.32, 0.022);
          cRing.position.set(T.txLvStudX, T.txLvStudY - 0.18, z);
          lvBushGroup.add(cRing);
        }
        lvBushGroup.add(turret, bushing, cap, flag);
      });
      txGroup.add(lvBushGroup);
      lvBushGroup.userData.basePos = lvBushGroup.position.clone();
      subparts['tx-lv-bushings'] = lvBushGroup;

      // 4. Elevated Conservator Tank, Cantilever Brackets, Oil-Level Dial Gauge & Eye-Level Silica Gel Breather
      const conservGroup = new THREE.Group();
      conservGroup.name = 'tx-conservator';
      const conY = coverY + 2.25;
      const conZ = -(tankL / 2 + 0.85);
      const cTank = new THREE.Mesh(new THREE.CylinderGeometry(0.58 * k, 0.58 * k, 3.6 * k, 24), MatLib.transformerTank);
      cTank.position.set(0.0, conY, conZ);
      cTank.rotation.z = Math.PI / 2;
      cTank.castShadow = true;

      [-1.82 * k, 1.82 * k].forEach(ex => {
        const endCap = new THREE.Mesh(new THREE.CylinderGeometry(0.61 * k, 0.61 * k, 0.07, 24), MatLib.darkSteel);
        endCap.position.set(ex, conY, conZ);
        endCap.rotation.z = Math.PI / 2;
        conservGroup.add(endCap);
      });

      [-1.15 * k, 1.15 * k].forEach(bx => {
        const vertPost = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.15, 0.14), MatLib.galvanizedSteel);
        vertPost.position.set(bx, coverY + 0.95, -(tankL / 2 + 0.02));
        const horizArm = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.14, 1.15), MatLib.galvanizedSteel);
        horizArm.position.set(bx, conY - 0.53, conZ + 0.33);
        const diagStrut = new THREE.Mesh(new THREE.BoxGeometry(0.10, 1.45, 0.10), MatLib.galvanizedSteel);
        diagStrut.position.set(bx, coverY + 1.05, conZ + 0.43);
        diagStrut.rotation.x = Math.PI / 4.2;
        conservGroup.add(vertPost, horizArm, diagStrut);
      });

      const mogFace = new THREE.Mesh(
        new THREE.CircleGeometry(0.24, 24),
        new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('oillevel') })
      );
      mogFace.position.set(-1.86 * k, conY, conZ);
      mogFace.rotation.y = -Math.PI / 2;

      const sightGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.72, 10), MatLib.glassBreather);
      sightGlass.position.set(0.0, conY, conZ + 0.63 * k);
      sightGlass.rotation.z = Math.PI / 2;

      const breatherX = -(1.82 * k + 0.36);
      const breatherTopBend = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.45, 8), MatLib.galvanizedSteel);
      breatherTopBend.position.set(breatherX + 0.2, conY + 0.3, conZ);
      breatherTopBend.rotation.z = Math.PI / 2;
      const pipeLen = Math.max(2.5, conY + 0.3 - 2.4);
      const breatherPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, pipeLen, 10), MatLib.galvanizedSteel);
      breatherPipe.position.set(breatherX, 2.45 + pipeLen / 2, conZ);
      const breatherGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.62, 16), MatLib.glassBreather);
      breatherGlass.position.set(breatherX, 2.25, conZ);
      const silica = new THREE.Mesh(new THREE.CylinderGeometry(0.145, 0.145, 0.5, 14), MatLib.silicaBlue);
      silica.position.set(breatherX, 2.25, conZ);
      const oilSealCup = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.12, 0.16, 14), MatLib.copperConductor);
      oilSealCup.position.set(breatherX, 1.86, conZ);

      conservGroup.add(cTank, mogFace, sightGlass, breatherTopBend, breatherPipe, breatherGlass, silica, oilSealCup);
      txGroup.add(conservGroup);
      conservGroup.userData.basePos = conservGroup.position.clone();
      subparts['tx-conservator'] = conservGroup;

      // 5. Inclined Buchholz Gas & Oil-Surge Relay Pipework
      const buchGroup = new THREE.Group();
      buchGroup.name = 'tx-buchholz';

      const coverRiser = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.095, 1.15, 14), MatLib.galvanizedSteel);
      coverRiser.position.set(-1.55 * k, coverY + 0.58, -tankL * 0.43);
      const riserFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.08, 14), MatLib.darkSteel);
      riserFlange.position.set(-1.55 * k, coverY + 0.04, -tankL * 0.43);

      const pPipeStart = new THREE.Vector3(-1.55 * k, coverY + 1.12, -tankL * 0.43);
      const pPipeEnd = new THREE.Vector3(0.45 * k, conY - 0.57, conZ + 0.1);
      const pipeVec = new THREE.Vector3().subVectors(pPipeEnd, pPipeStart);
      const pipeMid = new THREE.Vector3().addVectors(pPipeStart, pPipeEnd).multiplyScalar(0.5);
      const inclinedPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, pipeVec.length(), 14), MatLib.galvanizedSteel);
      inclinedPipe.position.copy(pipeMid);
      inclinedPipe.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), pipeVec.clone().normalize());

      const sumpStub = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, 0.25, 14), MatLib.galvanizedSteel);
      sumpStub.position.set(0.45 * k, conY - 0.5, conZ + 0.1);

      const relayHousing = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.48, 0.44), MatLib.brassContact);
      relayHousing.position.copy(pipeMid);
      const buchGlass = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.36, 0.03), MatLib.cabinetGlass);
      buchGlass.position.set(pipeMid.x, pipeMid.y, pipeMid.z - 0.23);
      const upperFloat = new THREE.Mesh(new THREE.SphereGeometry(0.065, 12, 10), MatLib.yellowHighlight);
      upperFloat.position.set(pipeMid.x + 0.05, pipeMid.y + 0.12, pipeMid.z - 0.14);
      const lowerFloat = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.12, 0.12), MatLib.hazardRed);
      lowerFloat.position.set(pipeMid.x - 0.05, pipeMid.y - 0.10, pipeMid.z - 0.14);
      const petcock = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.2, 8), MatLib.silverContact);
      petcock.position.set(pipeMid.x, pipeMid.y + 0.34, pipeMid.z);

      [0.24, 0.76].forEach(tVal => {
        const vPos = new THREE.Vector3().lerpVectors(pPipeStart, pPipeEnd, tVal);
        const vFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 14), MatLib.darkSteel);
        vFlange.position.copy(vPos);
        vFlange.quaternion.copy(inclinedPipe.quaternion);
        const vWheel = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.022, 8, 16), MatLib.hazardRed);
        vWheel.position.set(vPos.x, vPos.y + 0.2, vPos.z);
        vWheel.rotation.x = Math.PI / 2;
        buchGroup.add(vFlange, vWheel);
      });

      buchGroup.add(coverRiser, riserFlange, inclinedPipe, sumpStub, relayHousing, buchGlass, upperFloat, lowerFloat, petcock);
      txGroup.add(buchGroup);
      buchGroup.userData.basePos = buchGroup.position.clone();
      subparts['tx-buchholz'] = buchGroup;

      // 6. Stepped CRGO Laminated Silicon Steel Core (Internal 3-limb)
      const coreGroup = new THREE.Group();
      coreGroup.name = 'tx-core';
      coreGroup.position.set(0, 0.2 + tankH / 2, 0);

      const topYoke = new THREE.Mesh(new THREE.BoxGeometry(0.62 * k, 0.52 * k, 3.9 * k), MatLib.crgoCoreSteel);
      topYoke.position.y = 1.32 * k;
      const botYoke = new THREE.Mesh(new THREE.BoxGeometry(0.62 * k, 0.52 * k, 3.9 * k), MatLib.crgoCoreSteel);
      botYoke.position.y = -1.32 * k;
      const clampChannelTop = new THREE.Mesh(new THREE.BoxGeometry(0.76 * k, 0.14, 4.05 * k), MatLib.darkSteel);
      clampChannelTop.position.y = 1.32 * k;
      coreGroup.add(topYoke, botYoke, clampChannelTop);

      [-1.3 * k, 0, 1.3 * k].forEach(z => {
        const limb = new THREE.Mesh(new THREE.CylinderGeometry(0.31 * k, 0.31 * k, 2.22 * k, 16), MatLib.crgoCoreSteel);
        limb.position.set(0, 0, z);
        coreGroup.add(limb);
      });
      txGroup.add(coreGroup);
      coreGroup.userData.basePos = coreGroup.position.clone();
      subparts['tx-core'] = coreGroup;

      // 7. Concentric Copper Windings + Internal HV-to-LV Magnetic Energy Flow Path
      const windGroup = new THREE.Group();
      windGroup.name = 'tx-windings';
      windGroup.position.set(0, 0.2 + tankH / 2, 0);
      const coreMidY = 0.2 + tankH / 2;
      [-1.3 * k, 0, 1.3 * k].forEach((z, pIdx) => {
        const lvWind = new THREE.Mesh(new THREE.CylinderGeometry(0.43 * k, 0.43 * k, 1.82 * k, 20), MatLib.copperWinding);
        lvWind.position.set(0, 0, z);
        const hvWind = new THREE.Mesh(new THREE.CylinderGeometry(0.56 * k, 0.56 * k, 1.92 * k, 20), MatLib.copperWinding);
        hvWind.position.set(0, 0, z);
        [-0.98 * k, 0.98 * k].forEach(sy => {
          const spacer = new THREE.Mesh(new THREE.CylinderGeometry(0.6 * k, 0.6 * k, 0.06, 20), MatLib.brassContact);
          spacer.position.set(0, sy, z);
          windGroup.add(spacer);
        });
        // Internal flow curve from HV stud down through winding and out LV stud (local to windGroup)
        const wFlow = new THREE.Object3D();
        wFlow.userData.flowCurve = new THREE.CatmullRomCurve3([
          new THREE.Vector3(T.txHvStudX, T.txHvStudY - coreMidY, T.txHvPhaseZ[pIdx]),
          new THREE.Vector3(-0.35 * k, 0.85 * k, z),
          new THREE.Vector3(0.35 * k, -0.5 * k, z),
          new THREE.Vector3(T.txLvStudX, T.txLvStudY - coreMidY, T.txLvPhaseZ[pIdx])
        ]);
        wFlow.userData.voltageTag = vLvTag;
        wFlow.userData.circuitTag = 'sec_lv';
        windGroup.add(lvWind, hvWind, wFlow);
      });
      txGroup.add(windGroup);
      windGroup.userData.basePos = windGroup.position.clone();
      subparts['tx-windings'] = windGroup;

      // 8. On-Load Tap Changer (OLTC) Diverter Tank & Motor Drive Mechanism Cabinet
      const oltcGroup = new THREE.Group();
      oltcGroup.name = 'tx-oltc';
      const oltcTank = new THREE.Mesh(new THREE.BoxGeometry(1.15, 2.45 * k, 1.45), MatLib.transformerTank);
      oltcTank.position.set(tankW / 2 + 0.35, 2.4 * k, 0);
      const motorCab = new THREE.Mesh(new THREE.BoxGeometry(0.55, 1.15, 0.85), MatLib.galvanizedSteel);
      motorCab.position.set(tankW / 2 + 0.55, 1.2, 1.25);
      const driveShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.65, 8), MatLib.galvanizedSteel);
      driveShaft.position.set(tankW / 2 + 0.45, 2.25, 0.95);
      const tapDial = new THREE.Mesh(
        new THREE.CircleGeometry(0.18, 24),
        new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('oltc') })
      );
      tapDial.position.set(tankW / 2 + 0.84, 1.38, 1.25);
      tapDial.rotation.y = Math.PI / 2;
      oltcGroup.add(oltcTank, motorCab, driveShaft, tapDial);
      txGroup.add(oltcGroup);
      oltcGroup.userData.basePos = oltcGroup.position.clone();
      subparts['tx-oltc'] = oltcGroup;

      // 9. Dual Multi-Fin Vertical Radiator Banks, Manifold Headers & ONAF Cooling Fans
      const radGroup = new THREE.Group();
      radGroup.name = 'tx-radiators';
      const radZs = vSpec.id === '230_138' ? [-2.1, 0, 2.1] : [-1.55 * k, 1.55 * k];
      radZs.forEach(bankZ => {
        const bank = new THREE.Group();
        bank.position.set(-(tankW / 2 + 0.62), 0.25 + tankH / 2, bankZ);

        [-1.32 * k, 1.32 * k].forEach(hy => {
          const header = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 1.85, 12), MatLib.radiatorFin);
          header.rotation.x = Math.PI / 2;
          header.position.set(0, hy, 0);
          const neckPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.72, 10), MatLib.radiatorFin);
          neckPipe.rotation.z = Math.PI / 2;
          neckPipe.position.set(0.35, hy, 0);
          bank.add(header, neckPipe);
        });

        for (let fz = -0.85; fz <= 0.85; fz += 0.21) {
          const fin = new THREE.Mesh(new THREE.BoxGeometry(0.88, 2.65 * k, 0.04), MatLib.radiatorFin);
          fin.position.set(0, 0, fz);
          bank.add(fin);
        }

        [-0.45, 0.45].forEach(fz => {
          const fanCasing = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.18, 18), MatLib.darkSteel);
          fanCasing.position.set(-0.52, -0.35, fz);
          fanCasing.rotation.z = Math.PI / 2;
          const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.1, 10), MatLib.galvanizedSteel);
          hub.position.set(-0.54, -0.35, fz);
          hub.rotation.z = Math.PI / 2;
          const b1 = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.62, 0.12), MatLib.silverContact);
          b1.position.set(-0.54, -0.35, fz);
          const b2 = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.12, 0.62), MatLib.silverContact);
          b2.position.set(-0.54, -0.35, fz);
          bank.add(fanCasing, hub, b1, b2);
        });

        radGroup.add(bank);
      });
      txGroup.add(radGroup);
      radGroup.userData.basePos = radGroup.position.clone();
      subparts['tx-radiators'] = radGroup;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      txGroup.userData.subparts = subparts;
      scene.add(txGroup);
      return txGroup;
    }

    // BUILDER 8: CONFIGURABLE SWITCHYARD BUSBAR SYSTEM (Single, Main/Transfer, Ring, 1.5 Breaker)
    function buildBusbarSystem(scene, topology = 'single', enclosureType = 'ais', layout = null) {
      const L = layout || getBusLayoutConfig(topology, enclosureType);
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const pz = T.pz;
      const unitPz = T.unitPz;
      const zScale = vSpec.id === '230_138' ? 1.44 : (vSpec.id === '138_69' ? 1.22 : 1.0);
      const twin = !!vSpec.twinBundle;

      const busGroup = new THREE.Group();
      busGroup.name = 'busbar-system';
      busGroup.userData = { componentId: 'gantry', isSpanningBusbar: true, currentTopology: topology, switches: {} };

      const pipeMat = MatLib.aluminumBus;
      const mainPhaseZ = [-pz, 0, pz];
      const unitPhaseZ = [-unitPz, 0, unitPz];
      const txHvTarget = (pIdx) => new THREE.Vector3(L.txX + T.txHvStudX, T.txHvStudY, T.txHvPhaseZ[pIdx]);

      // Incoming HV bay conductor jumpers (Gantry -> Surge Arrester -> CT/VT -> Line Disconnect 89-69A)
      mainPhaseZ.forEach(z => {
        busGroup.add(createCatenaryJumper(new THREE.Vector3(L.laX, T.busY, z), new THREE.Vector3(L.laX, T.laTopY, z), 0.14, 6, MatLib.copperConductor, vTag, 'incoming', twin));
        busGroup.add(createCatenaryJumper(new THREE.Vector3(L.laX, T.laTopY, z), new THREE.Vector3(L.ctX - 0.65, T.ctTopY, z), 0.16, 6, MatLib.copperConductor, vTag, 'incoming', twin));
        busGroup.add(createCatenaryJumper(new THREE.Vector3(L.ctX + 0.65, T.ctTopY, z), new THREE.Vector3(L.dsX - 0.75, T.dsTermY, z), 0.16, 6, MatLib.copperConductor, vTag, 'incoming', twin));
      });

      // Open 4-leg galvanized truss support + dark chocolate brown post insulator
      function addSupport(x, z, h = T.busY) {
        const insH = Math.min(h - 1.2, Math.max(2.4, 2.35 * s));
        const pedH = Math.max(1.2, h - insH);
        const post = createRibbedInsulator(insH, 0.16, Math.max(10, vSpec.shedsCount || 10), MatLib.porcelainBrown, true);
        post.position.set(x, pedH + insH / 2, z);
        busGroup.add(post);

        const legGeo = new THREE.BoxGeometry(0.08, pedH, 0.08);
        [[-0.24, -0.24], [0.24, -0.24], [-0.24, 0.24], [0.24, 0.24]].forEach(([lx, lz]) => {
          const leg = new THREE.Mesh(legGeo, MatLib.galvanizedSteel);
          leg.position.set(x + lx, pedH / 2, z + lz);
          leg.castShadow = true;
          busGroup.add(leg);
        });
        const cap = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.07, 0.62), MatLib.galvanizedSteel);
        cap.position.set(x, pedH, z);
        busGroup.add(cap);
      }

      // 1. SINGLE BUS SCHEME: 89-69A -> 52-69 -> 89-69B -> Single Overhead Bus -> TR-01 HV
      if (topology === 'single') {
        const dsB = createCompactDisconnectUnit(L.dsBX, 0, 0, 0, false, '89-69B', vSpec, 'main_path');
        busGroup.add(dsB);
        busGroup.userData.switches['89-69B'] = dsB;
        const dsBTermY = dsB.userData.termHeight;
        const dsBOff = dsB.userData.termOffsetX;

        const busStartX = L.dsBX + dsBOff + 0.8;
        const busEndX = L.txX - 3.2;
        const busMidX = (busStartX + busEndX) / 2;
        const busBarY = +(Math.max(T.busY, T.cbTermY + 0.85)).toFixed(3);

        mainPhaseZ.forEach((z, pIdx) => {
          const uz = unitPhaseZ[pIdx];
          // 89-69A -> 52-69 -> 89-69B -> Single Overhead Bus -> TR-01 HV NEMA stud
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsX + 0.75, T.dsTermY, z), new THREE.Vector3(L.cbX - T.cbTermOffsetX, T.cbTermY, z), 0.18, 6, MatLib.copperConductor, vTag, 'post_dsA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.cbX + T.cbTermOffsetX, T.cbTermY, z), new THREE.Vector3(L.dsBX - dsBOff, dsBTermY, uz), 0.18, 6, MatLib.copperConductor, vTag, 'post_cbMain', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsBX + dsBOff, dsBTermY, uz), new THREE.Vector3(busStartX, busBarY, z), 0.16, 6, MatLib.copperConductor, vTag, 'main_path', twin));

          const bus = createRigidBusSegment(
            new THREE.Vector3(busStartX, busBarY, z),
            new THREE.Vector3(busEndX, busBarY, z),
            0.06, pipeMat, vTag, 'main_path', twin
          );
          busGroup.add(bus);

          [busStartX + 1.0, busMidX, busEndX - 1.0].forEach(px => {
            const pm = createPhaseMarker(pIdx, 0.075, 0.24);
            pm.position.set(px, busBarY, z);
            pm.rotation.z = Math.PI / 2;
            busGroup.add(pm);
          });

          addSupport(busStartX + 0.6, z, busBarY);
          addSupport(busEndX - 0.6, z, busBarY);

          busGroup.add(createCatenaryJumper(new THREE.Vector3(busEndX, busBarY, z), txHvTarget(pIdx), 0.25, 8, MatLib.copperConductor, vTag, 'tx_hv', twin));
        });

      // 2. MAIN & TRANSFER BUS SCHEME
      } else if (topology === 'maintransfer') {
        const dsB = createCompactDisconnectUnit(L.dsBX, 0, 0, 0, false, '89-69B', vSpec, 'main_path');
        busGroup.add(dsB);
        busGroup.userData.switches['89-69B'] = dsB;
        const dsBTermY = dsB.userData.termHeight;
        const dsBOff = dsB.userData.termOffsetX;

        const bus1Z = [-8.4 * zScale - 2 * unitPz, -8.4 * zScale - unitPz, -8.4 * zScale];
        const bus2Z = [8.4 * zScale, 8.4 * zScale + unitPz, 8.4 * zScale + 2 * unitPz];
        const bus1Y = +(Math.max(6.2, T.cbTermY + 1.15)).toFixed(3);
        const bus2Y = +(bus1Y + 1.55).toFixed(3);
        const busStartX = L.dsX - 1.5;
        const busEndX = L.txX - 3.2;

        bus1Z.forEach((z, pIdx) => {
          const mainBus = createRigidBusSegment(
            new THREE.Vector3(busStartX, bus1Y, z),
            new THREE.Vector3(busEndX, bus1Y, z),
            0.055, pipeMat, vTag, 'main_path', twin
          );
          busGroup.add(mainBus);
          const pm = createPhaseMarker(pIdx, 0.075, 0.24);
          pm.position.set(busStartX + 3.5, bus1Y, z);
          pm.rotation.z = Math.PI / 2;
          busGroup.add(pm);
          addSupport(L.cbX - 2.0, z, bus1Y);
          addSupport(L.tieX - 2.0, z, bus1Y);
          addSupport(busEndX - 1.5, z, bus1Y);
        });

        bus2Z.forEach((z, pIdx) => {
          const transBus = createRigidBusSegment(
            new THREE.Vector3(busStartX, bus2Y, z),
            new THREE.Vector3(busEndX, bus2Y, z),
            0.055, pipeMat, vTag, 'bypass_path', twin
          );
          busGroup.add(transBus);
          const pm = createPhaseMarker(pIdx, 0.075, 0.24);
          pm.position.set(busStartX + 3.5, bus2Y, z);
          pm.rotation.z = Math.PI / 2;
          busGroup.add(pm);
          addSupport(L.cbX - 2.0, z, bus2Y);
          addSupport(L.tieX - 2.0, z, bus2Y);
          addSupport(busEndX - 1.5, z, bus2Y);
        });

        const selZ = 5.2 * zScale + unitPz;
        const btDsZ = 5.0 * zScale + unitPz * 0.5;
        const discMainSel = createCompactDisconnectUnit(L.dsBX + 3.2, 0, -selZ, Math.PI / 2, false, '89-M', vSpec, 'main_path');
        const discBypass = createCompactDisconnectUnit(L.dsBX + 3.2, 0, selZ, Math.PI / 2, true, '89-BYP', vSpec, 'bypass_path');
        busGroup.add(discMainSel, discBypass);
        busGroup.userData.switches['89-M'] = discMainSel;
        busGroup.userData.switches['89-BYP'] = discBypass;

        const discBT1 = createCompactDisconnectUnit(L.tieX, 0, -btDsZ, Math.PI / 2, false, '89-BT1', vSpec, 'bypass_path');
        const tieBreaker = createCompactBreakerUnit(L.tieX, 0, 0, Math.PI / 2, '52-BT', vSpec, 'bypass_path');
        tieBreaker.name = 'bus-tie-breaker-52-bt';
        const discBT2 = createCompactDisconnectUnit(L.tieX, 0, btDsZ, Math.PI / 2, false, '89-BT2', vSpec, 'bypass_path');
        busGroup.add(discBT1, tieBreaker, discBT2);
        busGroup.userData.switches['89-BT1'] = discBT1;
        busGroup.userData.switches['52-BT'] = tieBreaker;
        busGroup.userData.switches['89-BT2'] = discBT2;

        const btCbOff = tieBreaker.userData.termOffsetX;
        const btCbY = tieBreaker.userData.termHeight;
        for (let p = 0; p < 3; p++) {
          const pxTie = L.tieX + unitPhaseZ[p];
          const pxSel = (L.dsBX + 3.2) + unitPhaseZ[p];
          const zBay = mainPhaseZ[p];
          const uz = unitPhaseZ[p];

          // 89-69A -> 52-69 -> 89-69B -> TR-01 HV
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsX + 0.75, T.dsTermY, zBay), new THREE.Vector3(L.cbX - T.cbTermOffsetX, T.cbTermY, zBay), 0.18, 6, MatLib.copperConductor, vTag, 'post_dsA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.cbX + T.cbTermOffsetX, T.cbTermY, zBay), new THREE.Vector3(L.dsBX - dsBOff, dsBTermY, uz), 0.18, 6, MatLib.copperConductor, vTag, 'post_cbMain', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsBX + dsBOff, dsBTermY, uz), new THREE.Vector3(L.tieX + 2.5, bus1Y - 0.5, zBay), 0.25, 6, MatLib.copperConductor, vTag, 'main_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.tieX + 2.5, bus1Y - 0.5, zBay), txHvTarget(p), 0.35, 8, MatLib.copperConductor, vTag, 'tx_hv', twin));

          // Tee to Selector 89-M / 89-BYP & Bus Tie 52-BT
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsBX + dsBOff + 0.5, dsBTermY, uz), new THREE.Vector3(pxSel, dsBTermY, -selZ + dsBOff), 0.25, 6, MatLib.copperConductor, vTag, 'main_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsBX + dsBOff + 0.5, dsBTermY, uz), new THREE.Vector3(pxSel, dsBTermY, selZ - dsBOff), 0.25, 6, MatLib.copperConductor, vTag, 'bypass_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(pxSel, dsBTermY, -selZ - dsBOff), new THREE.Vector3(L.dsBX + 3.2, bus1Y, bus1Z[p]), 0.3, 6, MatLib.copperConductor, vTag, 'main_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(pxSel, dsBTermY, selZ + dsBOff), new THREE.Vector3(L.dsBX + 3.2, bus2Y, bus2Z[p]), 0.3, 6, MatLib.copperConductor, vTag, 'bypass_path', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.tieX, bus1Y, bus1Z[p]), new THREE.Vector3(pxTie, dsBTermY, -btDsZ - dsBOff), 0.35, 6, MatLib.copperConductor, vTag, 'bypass_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(pxTie, dsBTermY, -btDsZ + dsBOff), new THREE.Vector3(pxTie, btCbY, -btCbOff), 0.25, 5, MatLib.copperConductor, vTag, 'bypass_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(pxTie, btCbY, btCbOff), new THREE.Vector3(pxTie, dsBTermY, btDsZ - dsBOff), 0.25, 5, MatLib.copperConductor, vTag, 'bypass_path', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(pxTie, dsBTermY, btDsZ + dsBOff), new THREE.Vector3(L.tieX, bus2Y, bus2Z[p]), 0.35, 6, MatLib.copperConductor, vTag, 'bypass_path', twin));
        }

      // 3. RING BUS SCHEME (Closed 4-Breaker Symmetrical Rectangular Loop: CB-1, CB-2, CB-3, CB-4)
      } else if (topology === 'ring') {
        const ringX1 = L.ringX1, ringX2 = L.ringX2;
        const ringZ1 = L.ringZ1, ringZ2 = L.ringZ2;
        const ringMidX = (ringX1 + ringX2) / 2;
        const ringY = +(Math.max(6.8, T.cbTermY + 1.8)).toFixed(3);
        const dsSep = Math.max(5.5, (ringX2 - ringX1) * 0.25);
        const zDsSep = Math.max(6.5, Math.abs(ringZ1) * 0.42);

        unitPhaseZ.forEach((pOff, pIdx) => {
          busGroup.add(createRigidBusSegment(new THREE.Vector3(ringX1 + pOff, ringY, ringZ1 + pOff), new THREE.Vector3(ringX2 + pOff, ringY, ringZ1 + pOff), 0.055, pipeMat, vTag, 'ring_leg2', twin));
          busGroup.add(createRigidBusSegment(new THREE.Vector3(ringX1 + pOff, ringY, ringZ2 + pOff), new THREE.Vector3(ringX2 + pOff, ringY, ringZ2 + pOff), 0.055, pipeMat, vTag, 'ring_leg4', twin));
          busGroup.add(createRigidBusSegment(new THREE.Vector3(ringX1 + pOff, ringY, ringZ1 + pOff), new THREE.Vector3(ringX1 + pOff, ringY, ringZ2 + pOff), 0.055, pipeMat, vTag, 'ring_leg1', twin));
          busGroup.add(createRigidBusSegment(new THREE.Vector3(ringX2 + pOff, ringY, ringZ1 + pOff), new THREE.Vector3(ringX2 + pOff, ringY, ringZ2 + pOff), 0.055, pipeMat, vTag, 'ring_leg3', twin));

          const pmN = createPhaseMarker(pIdx, 0.07, 0.24);
          pmN.position.set(ringMidX, ringY, ringZ1 + pOff);
          pmN.rotation.z = Math.PI / 2;
          busGroup.add(pmN);

          addSupport(ringX1 + pOff, ringZ1 + pOff, ringY);
          addSupport(ringX2 + pOff, ringZ2 + pOff, ringY);
        });

        const cb2 = createCompactBreakerUnit(ringMidX, 0, ringZ1, 0, '52-2', vSpec, 'ring_leg2');
        const cb3 = createCompactBreakerUnit(ringX2, 0, 0, Math.PI / 2, '52-3', vSpec, 'ring_leg3');
        const cb4 = createCompactBreakerUnit(ringMidX, 0, ringZ2, 0, '52-4', vSpec, 'ring_leg4');
        busGroup.add(cb2, cb3, cb4);
        busGroup.userData.switches['52-2'] = cb2;
        busGroup.userData.switches['52-3'] = cb3;
        busGroup.userData.switches['52-4'] = cb4;

        const ds1a = createCompactDisconnectUnit(ringX1, 0, -zDsSep, Math.PI / 2, false, '89-1A', vSpec, 'ring_leg1');
        const ds1b = createCompactDisconnectUnit(ringX1, 0, zDsSep, Math.PI / 2, false, '89-1B', vSpec, 'ring_leg1');
        const ds2a = createCompactDisconnectUnit(ringMidX - dsSep, 0, ringZ1, 0, false, '89-2A', vSpec, 'ring_leg2');
        const ds2b = createCompactDisconnectUnit(ringMidX + dsSep, 0, ringZ1, 0, false, '89-2B', vSpec, 'ring_leg2');
        const ds3a = createCompactDisconnectUnit(ringX2, 0, -zDsSep, Math.PI / 2, false, '89-3A', vSpec, 'ring_leg3');
        const ds3b = createCompactDisconnectUnit(ringX2, 0, zDsSep, Math.PI / 2, false, '89-3B', vSpec, 'ring_leg3');
        const ds4a = createCompactDisconnectUnit(ringMidX - dsSep, 0, ringZ2, 0, false, '89-4A', vSpec, 'ring_leg4');
        const ds4b = createCompactDisconnectUnit(ringMidX + dsSep, 0, ringZ2, 0, false, '89-4B', vSpec, 'ring_leg4');
        busGroup.add(ds1a, ds1b, ds2a, ds2b, ds3a, ds3b, ds4a, ds4b);
        Object.assign(busGroup.userData.switches, {
          '89-1A': ds1a, '89-1B': ds1b,
          '89-2A': ds2a, '89-2B': ds2b,
          '89-3A': ds3a, '89-3B': ds3b,
          '89-4A': ds4a, '89-4B': ds4b
        });

        const dsTermY = ds1a.userData.termHeight;
        const dsOff = ds1a.userData.termOffsetX;
        unitPhaseZ.forEach((pOff, pIdx) => {
          const dsZ = mainPhaseZ[pIdx];
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsX + 0.75, T.dsTermY, dsZ), new THREE.Vector3(ringX1 + pOff, ringY, ringZ1 + pOff), 0.45, 8, MatLib.copperConductor, vTag, 'post_dsA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX2 + pOff, ringY, ringZ1 + pOff), txHvTarget(pIdx), 0.60, 8, MatLib.copperConductor, vTag, 'tx_hv', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX1 + pOff, ringY, -(zDsSep + dsOff)), new THREE.Vector3(ringX1 + pOff, dsTermY, -(zDsSep + dsOff)), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg1', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX1 + pOff, dsTermY, -(zDsSep - dsOff)), new THREE.Vector3(ringX1 + pOff, T.cbTermY, -T.cbTermOffsetX), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg1', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX1 + pOff, T.cbTermY, T.cbTermOffsetX), new THREE.Vector3(ringX1 + pOff, dsTermY, zDsSep - dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg1', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX1 + pOff, dsTermY, zDsSep + dsOff), new THREE.Vector3(ringX1 + pOff, ringY, zDsSep + dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg1', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX2 + pOff, ringY, -(zDsSep + dsOff)), new THREE.Vector3(ringX2 + pOff, dsTermY, -(zDsSep + dsOff)), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg3', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringX2 + pOff, dsTermY, zDsSep + dsOff), new THREE.Vector3(ringX2 + pOff, ringY, zDsSep + dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg3', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringMidX - dsSep - dsOff, ringY, ringZ1 + pOff), new THREE.Vector3(ringMidX - dsSep - dsOff, dsTermY, ringZ1 + pOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg2', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringMidX + dsSep + dsOff, ringY, ringZ1 + pOff), new THREE.Vector3(ringMidX + dsSep + dsOff, dsTermY, ringZ1 + pOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg2', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringMidX - dsSep - dsOff, ringY, ringZ2 + pOff), new THREE.Vector3(ringMidX - dsSep - dsOff, dsTermY, ringZ2 + pOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg4', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(ringMidX + dsSep + dsOff, ringY, ringZ2 + pOff), new THREE.Vector3(ringMidX + dsSep + dsOff, dsTermY, ringZ2 + pOff), 0.2, 5, MatLib.copperConductor, vTag, 'ring_leg4', twin));
        });

      // 4. BREAKER-AND-A-HALF (1.5 CB) SCHEME (Dual Outer Parallel Main Buses A & B + Longitudinal 3-Breaker Column)
      } else if (topology === 'breakerhalf') {
        const busAZ = L.busAZ;
        const busBZ = L.busBZ;
        const busY = +(Math.max(7.4, T.cbTermY + 2.0)).toFixed(3);
        const busStartX = L.cbX - 9.0 * zScale;
        const busEndX = L.cbX + 10.0 * zScale;
        const busMidX = (busStartX + busEndX) / 2;

        unitPhaseZ.forEach((dz, pIdx) => {
          busGroup.add(createRigidBusSegment(new THREE.Vector3(busStartX, busY, busAZ + dz), new THREE.Vector3(busEndX, busY, busAZ + dz), 0.06, pipeMat, vTag, 'bh_busA', twin));
          busGroup.add(createRigidBusSegment(new THREE.Vector3(busStartX, busY, busBZ + dz), new THREE.Vector3(busEndX, busY, busBZ + dz), 0.06, pipeMat, vTag, 'bh_busB', twin));

          const pmA = createPhaseMarker(pIdx, 0.075, 0.24);
          pmA.position.set(busMidX - 4, busY, busAZ + dz);
          pmA.rotation.z = Math.PI / 2;
          const pmB = createPhaseMarker(pIdx, 0.075, 0.24);
          pmB.position.set(busMidX - 4, busY, busBZ + dz);
          pmB.rotation.z = Math.PI / 2;
          busGroup.add(pmA, pmB);

          addSupport(busStartX + 1.5, busAZ + dz, busY);
          addSupport(busEndX - 1.5, busAZ + dz, busY);
          addSupport(busStartX + 1.5, busBZ + dz, busY);
          addSupport(busEndX - 1.5, busBZ + dz, busY);
        });

        const zA = -16.5 * zScale, zB = 16.5 * zScale;
        const zA1 = -21.5 * zScale, zA2 = -11.5 * zScale, zT1 = -5.5 * zScale, zT2 = 5.5 * zScale, zB1 = 11.5 * zScale, zB2 = 21.5 * zScale;
        const cbA = createCompactBreakerUnit(L.cbX, 0, zA, Math.PI / 2, '52-A', vSpec, 'bh_busA');
        const cbB = createCompactBreakerUnit(L.cbX, 0, zB, Math.PI / 2, '52-B', vSpec, 'bh_busB');
        busGroup.add(cbA, cbB);
        busGroup.userData.switches['52-A'] = cbA;
        busGroup.userData.switches['52-B'] = cbB;

        const dsA1 = createCompactDisconnectUnit(L.cbX, 0, zA1, Math.PI / 2, false, '89-A1', vSpec, 'bh_busA');
        const dsA2 = createCompactDisconnectUnit(L.cbX, 0, zA2, Math.PI / 2, false, '89-A2', vSpec, 'bh_busA');
        const dsT1 = createCompactDisconnectUnit(L.cbX, 0, zT1, Math.PI / 2, false, '89-T1', vSpec, 'bh_tie');
        const dsT2 = createCompactDisconnectUnit(L.cbX, 0, zT2, Math.PI / 2, false, '89-T2', vSpec, 'bh_tie');
        const dsB1 = createCompactDisconnectUnit(L.cbX, 0, zB1, Math.PI / 2, false, '89-B1', vSpec, 'bh_busB');
        const dsB2 = createCompactDisconnectUnit(L.cbX, 0, zB2, Math.PI / 2, false, '89-B2', vSpec, 'bh_busB');
        busGroup.add(dsA1, dsA2, dsT1, dsT2, dsB1, dsB2);
        Object.assign(busGroup.userData.switches, {
          '89-A1': dsA1, '89-A2': dsA2,
          '89-T1': dsT1, '89-T2': dsT2,
          '89-B1': dsB1, '89-B2': dsB2
        });

        const dsTermY = dsA1.userData.termHeight;
        const dsOff = dsA1.userData.termOffsetX;
        const cbOff = cbA.userData.termOffsetX;
        const cbY = cbA.userData.termHeight;
        const node1Z = -8.5 * zScale;
        const node2Z = 8.5 * zScale;

        unitPhaseZ.forEach((pOff, pIdx) => {
          const bx = L.cbX + pOff;
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, busY, busAZ + pOff), new THREE.Vector3(bx, dsTermY, zA1 - dsOff), 0.35, 6, MatLib.copperConductor, vTag, 'bh_busA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, zA1 + dsOff), new THREE.Vector3(bx, cbY, zA - cbOff), 0.2, 5, MatLib.copperConductor, vTag, 'bh_busA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, cbY, zA + cbOff), new THREE.Vector3(bx, dsTermY, zA2 - dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'bh_busA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, zA2 + dsOff), new THREE.Vector3(bx, dsTermY, zT1 - dsOff), 0.25, 6, MatLib.copperConductor, vTag, 'bh_tie', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, zT1 + dsOff), new THREE.Vector3(bx, T.cbTermY, -T.cbTermOffsetX), 0.25, 6, MatLib.copperConductor, vTag, 'bh_tie', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, T.cbTermY, T.cbTermOffsetX), new THREE.Vector3(bx, dsTermY, zT2 - dsOff), 0.25, 6, MatLib.copperConductor, vTag, 'bh_tie', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, zT2 + dsOff), new THREE.Vector3(bx, dsTermY, zB1 - dsOff), 0.25, 6, MatLib.copperConductor, vTag, 'bh_tie', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, zB1 + dsOff), new THREE.Vector3(bx, cbY, zB - cbOff), 0.2, 5, MatLib.copperConductor, vTag, 'bh_busB', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, cbY, zB + cbOff), new THREE.Vector3(bx, dsTermY, zB2 - dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'bh_busB', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, zB2 + dsOff), new THREE.Vector3(bx, busY, busBZ + pOff), 0.35, 6, MatLib.copperConductor, vTag, 'bh_busB', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsX + 0.75, T.dsTermY, mainPhaseZ[pIdx]), new THREE.Vector3(bx, dsTermY, node1Z), 0.45, 8, MatLib.copperConductor, vTag, 'post_dsA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(bx, dsTermY, node2Z), txHvTarget(pIdx), 0.55, 8, MatLib.copperConductor, vTag, 'tx_hv', twin));
        });

      // 5. DOUBLE BUS–DOUBLE BREAKER (2.0 CB) SCHEME (2 Full Main Buses A/B + 2 Dedicated Breakers Per Circuit)
      } else if (topology === 'doublebreaker') {
        const busAZ = L.busAZ;
        const busBZ = L.busBZ;
        const busY = +(Math.max(7.6, T.cbTermY + 2.1)).toFixed(3);
        const bay1X = L.cbX;
        const bay2X = L.bay2X !== undefined ? L.bay2X : (L.cbX + 13.5 * zScale);
        const busStartX = bay1X - 7.5 * zScale;
        const busEndX = bay2X + 7.5 * zScale;
        const busMidX = (busStartX + busEndX) / 2;

        unitPhaseZ.forEach((dz, pIdx) => {
          busGroup.add(createRigidBusSegment(new THREE.Vector3(busStartX, busY, busAZ + dz), new THREE.Vector3(busEndX, busY, busAZ + dz), 0.062, pipeMat, vTag, 'db_busA', twin));
          busGroup.add(createRigidBusSegment(new THREE.Vector3(busStartX, busY, busBZ + dz), new THREE.Vector3(busEndX, busY, busBZ + dz), 0.062, pipeMat, vTag, 'db_busB', twin));

          const pmA = createPhaseMarker(pIdx, 0.075, 0.24);
          pmA.position.set(busMidX, busY, busAZ + dz);
          pmA.rotation.z = Math.PI / 2;
          const pmB = createPhaseMarker(pIdx, 0.075, 0.24);
          pmB.position.set(busMidX, busY, busBZ + dz);
          pmB.rotation.z = Math.PI / 2;
          busGroup.add(pmA, pmB);

          addSupport(busStartX + 1.2, busAZ + dz, busY);
          addSupport(busEndX - 1.2, busAZ + dz, busY);
          addSupport(busStartX + 1.2, busBZ + dz, busY);
          addSupport(busEndX - 1.2, busBZ + dz, busY);
        });

        const zCbA = L.cbZ || (-11.5 * zScale);
        const zCbB = Math.abs(zCbA);
        const zA1 = -17.5 * zScale, zA2 = -5.5 * zScale, zB1 = 5.5 * zScale, zB2 = 17.5 * zScale;

        // Primary 52-1A sits at (bay1X, 0, zCbA); build 52-1B, 52-2A, 52-2B + all 8 flanking disconnects
        const cb1B = createCompactBreakerUnit(bay1X, 0, zCbB, Math.PI / 2, '52-1B', vSpec, 'db_b1B');
        const cb2A = createCompactBreakerUnit(bay2X, 0, zCbA, Math.PI / 2, '52-2A', vSpec, 'db_b2A');
        const cb2B = createCompactBreakerUnit(bay2X, 0, zCbB, Math.PI / 2, '52-2B', vSpec, 'db_b2B');
        busGroup.add(cb1B, cb2A, cb2B);
        busGroup.userData.switches['52-1B'] = cb1B;
        busGroup.userData.switches['52-2A'] = cb2A;
        busGroup.userData.switches['52-2B'] = cb2B;

        const ds1A1 = createCompactDisconnectUnit(bay1X, 0, zA1, Math.PI / 2, false, '89-1A1', vSpec, 'db_b1A');
        const ds1A2 = createCompactDisconnectUnit(bay1X, 0, zA2, Math.PI / 2, false, '89-1A2', vSpec, 'db_b1A');
        const ds1B1 = createCompactDisconnectUnit(bay1X, 0, zB1, Math.PI / 2, false, '89-1B1', vSpec, 'db_b1B');
        const ds1B2 = createCompactDisconnectUnit(bay1X, 0, zB2, Math.PI / 2, false, '89-1B2', vSpec, 'db_b1B');

        const ds2A1 = createCompactDisconnectUnit(bay2X, 0, zA1, Math.PI / 2, false, '89-2A1', vSpec, 'db_b2A');
        const ds2A2 = createCompactDisconnectUnit(bay2X, 0, zA2, Math.PI / 2, false, '89-2A2', vSpec, 'db_b2A');
        const ds2B1 = createCompactDisconnectUnit(bay2X, 0, zB1, Math.PI / 2, false, '89-2B1', vSpec, 'db_b2B');
        const ds2B2 = createCompactDisconnectUnit(bay2X, 0, zB2, Math.PI / 2, false, '89-2B2', vSpec, 'db_b2B');

        busGroup.add(ds1A1, ds1A2, ds1B1, ds1B2, ds2A1, ds2A2, ds2B1, ds2B2);
        Object.assign(busGroup.userData.switches, {
          '89-1A1': ds1A1, '89-1A2': ds1A2, '89-1B1': ds1B1, '89-1B2': ds1B2,
          '89-2A1': ds2A1, '89-2A2': ds2A2, '89-2B1': ds2B1, '89-2B2': ds2B2
        });

        const dsTermY = ds1A1.userData.termHeight;
        const dsOff = ds1A1.userData.termOffsetX;
        const cbOff = cb1B.userData.termOffsetX;
        const cbY = cb1B.userData.termHeight;

        unitPhaseZ.forEach((pOff, pIdx) => {
          const b1x = bay1X + pOff;
          const b2x = bay2X + pOff;
          // Bay 1: Incoming Line 1 Center Node (z=0) splits through (89-1A2 -> 52-1A -> 89-1A1 -> Bus A) and (89-1B1 -> 52-1B -> 89-1B2 -> Bus B)
          busGroup.add(createCatenaryJumper(new THREE.Vector3(L.dsX + 0.75, T.dsTermY, mainPhaseZ[pIdx]), new THREE.Vector3(b1x, dsTermY, 0), 0.38, 7, MatLib.copperConductor, vTag, 'post_dsA', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, dsTermY, 0), new THREE.Vector3(b1x, dsTermY, zA2 + dsOff), 0.16, 5, MatLib.copperConductor, vTag, 'db_b1A', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, dsTermY, zA2 - dsOff), new THREE.Vector3(b1x, T.cbTermY, zCbA + T.cbTermOffsetX), 0.2, 5, MatLib.copperConductor, vTag, 'db_b1A', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, T.cbTermY, zCbA - T.cbTermOffsetX), new THREE.Vector3(b1x, dsTermY, zA1 + dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b1A', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, dsTermY, zA1 - dsOff), new THREE.Vector3(b1x, busY, busAZ + pOff), 0.35, 6, MatLib.copperConductor, vTag, 'db_busA', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, dsTermY, 0), new THREE.Vector3(b1x, dsTermY, zB1 - dsOff), 0.16, 5, MatLib.copperConductor, vTag, 'db_b1B', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, dsTermY, zB1 + dsOff), new THREE.Vector3(b1x, cbY, zCbB - cbOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b1B', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, cbY, zCbB + cbOff), new THREE.Vector3(b1x, dsTermY, zB2 - dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b1B', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b1x, dsTermY, zB2 + dsOff), new THREE.Vector3(b1x, busY, busBZ + pOff), 0.35, 6, MatLib.copperConductor, vTag, 'db_busB', twin));

          // Bay 2: Main Bus A & Bus B feed through (89-2A1 -> 52-2A -> 89-2A2) and (89-2B2 -> 52-2B -> 89-2B1) into Center TR-01 Node (z=0) -> TR-01 HV
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, busY, busAZ + pOff), new THREE.Vector3(b2x, dsTermY, zA1 - dsOff), 0.35, 6, MatLib.copperConductor, vTag, 'db_b2A', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, dsTermY, zA1 + dsOff), new THREE.Vector3(b2x, cbY, zCbA - cbOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b2A', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, cbY, zCbA + cbOff), new THREE.Vector3(b2x, dsTermY, zA2 - dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b2A', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, dsTermY, zA2 + dsOff), new THREE.Vector3(b2x, dsTermY, 0), 0.16, 5, MatLib.copperConductor, vTag, 'db_b2A', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, busY, busBZ + pOff), new THREE.Vector3(b2x, dsTermY, zB2 + dsOff), 0.35, 6, MatLib.copperConductor, vTag, 'db_b2B', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, dsTermY, zB2 - dsOff), new THREE.Vector3(b2x, cbY, zCbB + cbOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b2B', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, cbY, zCbB - cbOff), new THREE.Vector3(b2x, dsTermY, zB1 + dsOff), 0.2, 5, MatLib.copperConductor, vTag, 'db_b2B', twin));
          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, dsTermY, zB1 - dsOff), new THREE.Vector3(b2x, dsTermY, 0), 0.16, 5, MatLib.copperConductor, vTag, 'db_b2B', twin));

          busGroup.add(createCatenaryJumper(new THREE.Vector3(b2x, dsTermY, 0), txHvTarget(pIdx), 0.45, 7, MatLib.copperConductor, vTag, 'tx_hv', twin));
        });
      }

      scene.add(busGroup);
      return busGroup;
    }

    // BUILDER 9: STATION SERVICE TRANSFORMER & WALK-IN CONTROL HOUSE INTERIOR
    function buildStationService(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const auxGroup = new THREE.Group();
      auxGroup.name = 'auxiliary';
      auxGroup.userData = { componentId: 'auxiliary' };
      auxGroup.position.set(0, 0, 0);

      const subparts = {};
      const floorY = 0.48; // Matches ctrlHouse interior epoxy floor top
      const chShiftX = L.ctrlX - 7.0;
      const chShiftZ = L.ctrlZ;

      // 1. 100 kVA Outdoor Auxiliary Step-Down Transformer Tank & Cooling Fins (Relocated to Fenced 13.8 kV Secondary Bay)
      const auxTankGroup = new THREE.Group();
      auxTankGroup.name = 'aux-tx-tank';
      auxTankGroup.position.set(L.sstX, 0, L.sstZ);
      const auxPad = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.24, 2.0), MatLib.concretePad);
      auxPad.position.set(0, 0.12, 0);
      const tank = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.4, 1.2), MatLib.transformerTank);
      tank.position.set(0, 0.94, 0);
      tank.castShadow = true;
      for (let z = -0.45; z <= 0.45; z += 0.225) {
        const finL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 1.05, 0.04), MatLib.radiatorFin);
        finL.position.set(-0.78, 0.9, z);
        const finR = new THREE.Mesh(new THREE.BoxGeometry(0.16, 1.05, 0.04), MatLib.radiatorFin);
        finR.position.set(0.78, 0.9, z);
        auxTankGroup.add(finL, finR);
      }
      auxTankGroup.add(auxPad, tank);
      auxGroup.add(auxTankGroup);
      auxTankGroup.userData.basePos = auxTankGroup.position.clone();
      subparts['aux-tx-tank'] = auxTankGroup;

      // 2. 13.8 kV Primary Bushings & Expulsion Cutout Fuses
      const auxBushGroup = new THREE.Group();
      auxBushGroup.name = 'aux-tx-bushings';
      auxBushGroup.position.set(L.sstX, 0, L.sstZ);
      [-0.4, 0, 0.4].forEach(x => {
        const b = createRibbedInsulator(0.65, 0.085, 5, MatLib.porcelainBrown, true);
        b.position.set(x, 1.94, 0);
        const fuseHolder = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.42, 8), MatLib.porcelainBrown);
        fuseHolder.position.set(x, 2.41, -0.15);
        fuseHolder.rotation.x = Math.PI / 5;
        auxBushGroup.add(b, fuseHolder);
      });
      auxGroup.add(auxBushGroup);
      auxBushGroup.userData.basePos = auxBushGroup.position.clone();
      subparts['aux-tx-bushings'] = auxBushGroup;

      // 3. Row of 4 Protection & Control Relay Cubicles (Positioned inside Control House at L.ctrlX, L.ctrlZ)
      const rackGroup = new THREE.Group();
      rackGroup.name = 'aux-relay-racks';
      rackGroup.position.set(chShiftX, 0, chShiftZ);
      const panelDefs = [
        { x: 4.9, title: 'PANEL 1: TR-01 DIFF', model: 'SEL-487E (87T)', relays: ['87T', '86T', '50/51', '63'] },
        { x: 5.85, title: 'PANEL 2: 69kV LINE/BUS', model: 'SEL-421 (21/87B)', relays: ['21', '50BF', '87B', '25'] },
        { x: 6.8, title: 'PANEL 3: FDR 13.8kV', model: 'SEL-751 (50/51)', relays: ['50/51', '50N', '79', '86F'] },
        { x: 7.75, title: 'PANEL 4: 52CB CONTROL', model: 'MIMIC & TRIP/CLS', relays: ['52CS', '86M', '27/59', 'SYNC'] }
      ];
      panelDefs.forEach((p, idx) => {
        const cab = new THREE.Mesh(new THREE.BoxGeometry(0.9, 2.25, 0.78), MatLib.relayPanelSteel);
        cab.position.set(p.x, floorY + 1.125, -4.35);
        cab.castShadow = true;

        const faceTex = TextureGen.createRelayPanelTexture(p.title, p.model, p.relays);
        const face = new THREE.Mesh(
          new THREE.PlaneGeometry(0.84, 2.15),
          new THREE.MeshBasicMaterial({ map: faceTex })
        );
        face.position.set(p.x, floorY + 1.125, -3.955);
        if (idx < 3) {
          const rFocus = ['tx_87t', 'line_21_87b', 'fdr_50_51'][idx];
          cab.userData.action = 'openRelayTccLab';
          cab.userData.relayFocus = rFocus;
          face.userData.action = 'openRelayTccLab';
          face.userData.relayFocus = rFocus;
        }
        rackGroup.add(cab, face);

        if (idx === 0 || idx === 2) {
          const lockout = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.06, 10), new THREE.MeshBasicMaterial({ color: 0xf97316 }));
          lockout.rotation.x = Math.PI / 2;
          lockout.position.set(p.x + 0.25, floorY + 1.18, -3.92);
          rackGroup.add(lockout);
        }

        if (idx === 3) {
          const pistolBase = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.05, 14), MatLib.darkSteel);
          pistolBase.rotation.x = Math.PI / 2;
          pistolBase.position.set(p.x, floorY + 1.12, -3.92);
          const pistolHandle = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.14, 0.1), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.35 }));
          pistolHandle.position.set(p.x, floorY + 1.12, -3.86);
          pistolHandle.userData.action = 'toggleBreaker';
          pistolBase.userData.action = 'toggleBreaker';

          const redLamp = new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 8), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
          redLamp.position.set(p.x - 0.12, floorY + 1.24, -3.93);
          const greenLamp = new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 8), new THREE.MeshBasicMaterial({ color: 0x10b981 }));
          greenLamp.position.set(p.x + 0.12, floorY + 1.24, -3.93);

          auxGroup.userData.pistolHandle = pistolHandle;
          auxGroup.userData.ctrlRedLamp = redLamp;
          auxGroup.userData.ctrlGreenLamp = greenLamp;
          rackGroup.add(pistolBase, pistolHandle, redLamp, greenLamp);
        }
      });
      auxGroup.add(rackGroup);
      rackGroup.userData.basePos = rackGroup.position.clone();
      subparts['aux-relay-racks'] = rackGroup;

      // 4. SCADA / HMI Operator Workstation, Dual Monitors, RTU/SOE Rack & Alarm Annunciator
      const scadaGroup = new THREE.Group();
      scadaGroup.name = 'aux-scada-desk';
      scadaGroup.position.set(chShiftX, 0, chShiftZ);
      const scadaHoverMsg = '🖥️ Click SCADA HMI Terminal (or Press [E]) to Open Interactive Master SLD';
      const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.06, 0.95), new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 }));
      deskTop.position.set(6.5, floorY + 0.75, -1.6);
      deskTop.userData.action = 'openMasterSLD';
      deskTop.userData.hoverPrompt = scadaHoverMsg;
      [-0.95, 0.95].forEach(dx => {
        const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.74, 0.8), MatLib.darkSteel);
        leg.position.set(6.5 + dx, floorY + 0.37, -1.6);
        scadaGroup.add(leg);
      });
      [-0.48, 0.48].forEach((mx, mIdx) => {
        const monitorBezel = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.46, 0.04), MatLib.darkSteel);
        monitorBezel.position.set(6.5 + mx, floorY + 1.05, -1.78);
        monitorBezel.rotation.y = mIdx === 0 ? 0.14 : -0.14;
        monitorBezel.userData.action = 'openMasterSLD';
        monitorBezel.userData.hoverPrompt = scadaHoverMsg;
        const screen = new THREE.Mesh(
          new THREE.PlaneGeometry(0.72, 0.40),
          new THREE.MeshBasicMaterial({ map: TextureGen.createScadaScreenTexture() })
        );
        screen.position.set(0, 0, 0.022);
        screen.userData.action = 'openMasterSLD';
        screen.userData.hoverPrompt = scadaHoverMsg;
        monitorBezel.add(screen);
        const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.04, 0.18, 8), MatLib.darkSteel);
        stand.position.set(6.5 + mx, floorY + 0.84, -1.78);
        scadaGroup.add(monitorBezel, stand);
      });
      const chairSeat = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.08, 0.48), MatLib.darkSteel);
      chairSeat.position.set(6.5, floorY + 0.48, -0.82);
      const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.56, 0.08), MatLib.darkSteel);
      chairBack.position.set(6.5, floorY + 0.78, -0.58);
      const rtuCab = new THREE.Mesh(new THREE.BoxGeometry(0.8, 2.15, 0.75), MatLib.relayPanelSteel);
      rtuCab.position.set(8.85, floorY + 1.075, -4.35);
      const rtuFace = new THREE.Mesh(
        new THREE.PlaneGeometry(0.74, 2.05),
        new THREE.MeshBasicMaterial({ map: TextureGen.createRelayPanelTexture('SCADA RTU / SOE', 'SEL-3555 + IRIG-B', ['RTU', 'SOE', 'GPS', 'ETH']) })
      );
      rtuFace.position.set(8.85, floorY + 1.075, -3.97);
      const annBox = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.58, 0.25), MatLib.darkSteel);
      annBox.position.set(6.3, floorY + 2.68, -4.15);
      annBox.rotation.x = 0.22;
      const annFace = new THREE.Mesh(
        new THREE.PlaneGeometry(2.48, 0.5),
        new THREE.MeshBasicMaterial({ map: TextureGen.createAnnunciatorTexture() })
      );
      annFace.position.set(0, 0, 0.13);
      annFace.userData.action = 'openMasterSLD';
      annFace.userData.hoverPrompt = scadaHoverMsg;
      annBox.add(annFace);

      scadaGroup.add(deskTop, chairSeat, chairBack, rtuCab, rtuFace, annBox);
      auxGroup.add(scadaGroup);
      scadaGroup.userData.basePos = scadaGroup.position.clone();
      subparts['aux-scada-desk'] = scadaGroup;

      // 5. 125 VDC Station Battery Bank (Two-Tier 60-Cell Flooded/VRLA Seismic Rack)
      const battGroup = new THREE.Group();
      battGroup.name = 'aux-battery-rack';
      battGroup.position.set(chShiftX, 0, chShiftZ);
      const rackFrame = new THREE.Mesh(new THREE.BoxGeometry(3.4, 1.35, 0.85), MatLib.galvanizedSteel);
      rackFrame.position.set(7.8, floorY + 0.675, 4.1);
      battGroup.add(rackFrame);
      [floorY + 0.58, floorY + 1.18].forEach(tierY => {
        for (let cx = 6.35; cx <= 9.25; cx += 0.24) {
          const jar = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.34, 0.28), MatLib.glassBreather);
          jar.position.set(cx, tierY, 4.1);
          const plate = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.24, 0.2), MatLib.darkSteel);
          plate.position.set(cx, tierY - 0.02, 4.1);
          const link = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.025, 0.06), MatLib.copperConductor);
          link.position.set(cx + 0.1, tierY + 0.18, 4.1);
          battGroup.add(jar, plate, link);
        }
      });
      auxGroup.add(battGroup);
      battGroup.userData.basePos = battGroup.position.clone();
      subparts['aux-battery-rack'] = battGroup;

      // 6. Dual Redundant SCR Float/Boost Battery Chargers (Battery Room West)
      const chgGroup = new THREE.Group();
      chgGroup.name = 'aux-battery-chargers';
      chgGroup.position.set(chShiftX, 0, chShiftZ);
      [4.2, 5.1].forEach((cx, cIdx) => {
        const chgCab = new THREE.Mesh(new THREE.BoxGeometry(0.78, 1.85, 0.72), MatLib.galvanizedSteel);
        chgCab.position.set(cx, floorY + 0.925, 4.1);
        const chgFace = new THREE.Mesh(
          new THREE.PlaneGeometry(0.7, 1.72),
          new THREE.MeshBasicMaterial({ map: TextureGen.createRelayPanelTexture('125VDC CHGR ' + (cIdx === 0 ? 'A' : 'B'), '135.2V FLOAT | 12A', ['SCR', 'FLT', 'EQZ', 'ALM']) })
        );
        chgFace.position.set(cx, floorY + 0.925, 3.735);
        chgFace.rotation.y = Math.PI;
        chgGroup.add(chgCab, chgFace);
      });
      auxGroup.add(chgGroup);
      chgGroup.userData.basePos = chgGroup.position.clone();
      subparts['aux-battery-chargers'] = chgGroup;

      // 7. 125V DC & 480V/240V AC Essential Distribution Panelboards (East Wall) + Underground Slab Entry Conduit from SST-100
      const acdcGroup = new THREE.Group();
      acdcGroup.name = 'aux-acdc-boards';
      acdcGroup.position.set(chShiftX, 0, chShiftZ);
      [-2.1, -0.8].forEach((bz, bIdx) => {
        const panel = new THREE.Mesh(new THREE.BoxGeometry(0.48, 2.05, 1.05), MatLib.relayPanelSteel);
        panel.position.set(10.65, floorY + 1.025, bz);
        const bFace = new THREE.Mesh(
          new THREE.PlaneGeometry(0.95, 1.92),
          new THREE.MeshBasicMaterial({
            map: TextureGen.createRelayPanelTexture(
              bIdx === 0 ? '125VDC DIST PANEL' : '480/240VAC AUX PANEL',
              bIdx === 0 ? 'TC1 / TC2 / RELAYS' : 'MTS / FANS / HVAC',
              bIdx === 0 ? ['TC1', 'TC2', '86', 'HMI'] : ['FAN1', 'OLTC', 'HTR', 'LTS']
            )
          })
        );
        bFace.position.set(10.405, floorY + 1.025, bz);
        bFace.rotation.y = -Math.PI / 2;
        acdcGroup.add(panel, bFace);
      });
      // Rigid steel 480V secondary feeder conduit exiting SST-100 -> underground duct -> up through Control House floor slab into 480VAC Panel
      const sstRelX = L.sstX - chShiftX;
      const sstRelZ = L.sstZ - chShiftZ;
      const slabPt = new THREE.Vector3(10.65, -0.35, -0.8);
      const sstConduitPts = [
        new THREE.Vector3(sstRelX, 1.25, sstRelZ + 0.72),
        new THREE.Vector3(sstRelX, -0.35, sstRelZ + 0.72),
        new THREE.Vector3(10.65, -0.35, sstRelZ + 0.72),
        slabPt,
        new THREE.Vector3(10.65, floorY + 0.35, -0.8)
      ];
      for (let i = 0; i < sstConduitPts.length - 1; i++) {
        acdcGroup.add(createRigidBusSegment(sstConduitPts[i], sstConduitPts[i + 1], 0.048, MatLib.galvanizedSteel, '480V', 'sst_tap'));
      }
      const sstJBox = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.36, 0.24), MatLib.galvanizedSteel);
      sstJBox.position.set(sstRelX, 1.25, sstRelZ + 0.72);
      const floorFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.08, 12), MatLib.darkSteel);
      floorFlange.position.set(10.65, floorY + 0.04, -0.8);
      acdcGroup.add(sstJBox, floorFlange);

      auxGroup.add(acdcGroup);
      acdcGroup.userData.basePos = acdcGroup.position.clone();
      subparts['aux-acdc-boards'] = acdcGroup;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      auxGroup.userData.subparts = subparts;
      scene.add(auxGroup);
      return auxGroup;
    }

    // BUILDER 10: SUBSURFACE COPPER GROUNDING GRID (IEEE Std 80-2013)
    function buildGroundingGrid(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const gridGroup = new THREE.Group();
      gridGroup.name = 'grounding-grid';
      gridGroup.visible = false;

      const cuMat = MatLib.groundCopper;
      const xMin = L.yardCenterX - L.yardW / 2 + 2.5;
      const xMax = L.yardCenterX + L.yardW / 2 - 2.5;
      const zMin = L.yardCenterZ - L.yardL / 2 + 2.5;
      const zMax = L.yardCenterZ + L.yardL / 2 - 2.5;
      const spanX = xMax - xMin;
      const spanZ = zMax - zMin;

      for (let z = zMin; z <= zMax + 0.01; z += 4.5) {
        const wire = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, spanX, 6), cuMat);
        wire.position.set(L.yardCenterX, -0.5, z);
        wire.rotation.z = Math.PI / 2;
        gridGroup.add(wire);
      }

      for (let x = xMin; x <= xMax + 0.01; x += 5.0) {
        const wire = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, spanZ, 6), cuMat);
        wire.position.set(x, -0.5, L.yardCenterZ);
        wire.rotation.x = Math.PI / 2;
        gridGroup.add(wire);
      }

      const rodLocations = [
        { x: xMin, z: zMin }, { x: xMax, z: zMin }, { x: xMax, z: zMax }, { x: xMin, z: zMax },
        { x: L.yardCenterX - spanX * 0.25, z: zMin }, { x: L.yardCenterX, z: zMin }, { x: L.yardCenterX + spanX * 0.25, z: zMin },
        { x: L.yardCenterX - spanX * 0.25, z: zMax }, { x: L.yardCenterX, z: zMax }, { x: L.yardCenterX + spanX * 0.25, z: zMax },
        { x: xMin, z: L.yardCenterZ - 10 }, { x: xMin, z: L.yardCenterZ + 10 },
        { x: xMax, z: L.yardCenterZ - 10 }, { x: xMax, z: L.yardCenterZ + 10 },
        { x: L.cbX, z: 0 }, { x: L.txX, z: 0 },
        { x: L.secCbX, z: 0 }, { x: L.secBusX, z: L.fdr1Z }, { x: L.secBusX, z: L.fdr2Z }
      ];

      rodLocations.forEach(r => {
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 3.0, 6), cuMat);
        rod.position.set(r.x, -2.0, r.z);
        gridGroup.add(rod);
      });

      const heatTex = TextureGen.createGroundHeatmapTexture();
      heatTex.needsUpdate = true;
      const heatMat = new THREE.MeshBasicMaterial({
        map: heatTex,
        transparent: true,
        opacity: 0.7,
        side: THREE.DoubleSide
      });
      MatLib.groundHeatmapMat = heatMat;
      const heatPlane = new THREE.Mesh(new THREE.PlaneGeometry(spanX + 2, spanZ + 2), heatMat);
      heatPlane.rotation.x = -Math.PI / 2;
      heatPlane.position.set(L.yardCenterX, 0.02, L.yardCenterZ);
      gridGroup.add(heatPlane);

      scene.add(gridGroup);
      return gridGroup;
    }

    // BUILDER 11: ROLLING SPHERE LIGHTNING CANOPY (IEEE Std 998-2012)
    function buildRollingSphereShielding(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const shieldGroup = new THREE.Group();
      shieldGroup.name = 'rolling-sphere';
      shieldGroup.visible = false;

      const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x38bdf8,
        wireframe: true,
        transparent: true,
        opacity: 0.25
      });

      const radius = Math.max(45.0, L.yardW * 0.65);
      const sphereGeo = new THREE.SphereGeometry(radius, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.42);
      const canopy = new THREE.Mesh(sphereGeo, sphereMat);
      canopy.position.set(L.yardCenterX, -29.0, L.yardCenterZ);
      shieldGroup.add(canopy);

      scene.add(shieldGroup);
      return shieldGroup;
    }

    // Helper: Compact Secondary Air Disconnect Switch (89-MV) scaled by secondary voltage class
    function createMVDisconnectUnit(x, z, isOpen = false, tag = '89-MV', T = null, circuitTag = 'sec_lv') {
      const termInfo = T || getPrimaryTerminals(getBusLayoutConfig('single'));
      const lvS = termInfo.lvS || 1.0;
      const lvSp = termInfo.lvSp || 1.2;
      const vLvTag = termInfo.vSpec.lvKv + 'kV';
      const postH = +(0.95 * lvS).toFixed(3);
      const termY = +(2.20 + postH + 0.03).toFixed(3);
      const shedsCount = Math.max(6, Math.round(6 * lvS));
      const grp = new THREE.Group();
      grp.position.set(x, 0, z);
      const blades = [];
      [-lvSp, 0, lvSp].forEach((pz, idx) => {
        [-0.45, 0.45].forEach((lx, pSide) => {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.2, 0.08), MatLib.galvanizedSteel);
          leg.position.set(lx, 1.1, pz);
          grp.add(leg);
          const ins = createRibbedInsulator(postH, 0.11, shedsCount, MatLib.porcelainBrown, true);
          ins.position.set(lx, 2.20 + postH / 2, pz);
          const cap = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.06, 0.12), MatLib.aluminumBus);
          cap.position.set(lx, termY - 0.01, pz);
          tagEnergizedTerminal(cap, circuitTag, vLvTag);
          grp.add(ins, cap);
          if (termInfo.vSpec.lvKv >= 138 && pSide >= 0) {
            const cRing = createCoronaRing(0.24, 0.02);
            cRing.position.set(lx, termY - 0.1, pz);
            grp.add(cRing);
          }
        });
        const beam = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.1, 0.18), MatLib.galvanizedSteel);
        beam.position.set(0, 2.18, pz);
        grp.add(beam);

        const pivot = new THREE.Group();
        pivot.position.set(-0.45, termY + 0.02, pz);
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.05, 0.04), MatLib.copperConductor);
        blade.position.set(0.45, 0, 0);
        pivot.add(blade);
        pivot.rotation.z = isOpen ? Math.PI / 3.2 : 0;
        grp.add(pivot);
        blades.push(pivot);

        const intFlow = new THREE.Object3D();
        intFlow.userData.flowCurve = new THREE.LineCurve3(new THREE.Vector3(-0.45, termY, pz), new THREE.Vector3(0.45, termY, pz));
        intFlow.userData.voltageTag = vLvTag;
        intFlow.userData.circuitTag = circuitTag;
        grp.add(intFlow);

        const pMark = createPhaseMarker(idx, 0.04, 0.08);
        pMark.position.set(0.45, termY + 0.05, pz);
        grp.add(pMark);
      });
      grp.userData.bladePivots = blades;
      grp.userData.tag = tag;
      grp.userData.termHeight = termY;
      grp.userData.termOffsetX = 0.45;
      grp.userData.phaseZ = [-lvSp, 0, lvSp];
      return grp;
    }

    // Helper: Compact Secondary Circuit Breaker / Recloser (52-MV) scaled by secondary voltage class
    function createMVBreakerUnit(x, z, isClosed = true, tag = '52-MV', T = null, circuitTag = 'sec_lv') {
      const termInfo = T || getPrimaryTerminals(getBusLayoutConfig('single'));
      const lvS = termInfo.lvS || 1.0;
      const lvSp = termInfo.lvSp || 1.2;
      const vLvTag = termInfo.vSpec.lvKv + 'kV';
      const bushH = +(0.95 * lvS).toFixed(3);
      const tilt = Math.PI / 10;
      const termX = +(0.50 + bushH * Math.sin(tilt)).toFixed(3);
      const termY = +(2.42 + bushH * Math.cos(tilt)).toFixed(3);
      const shedsCount = Math.max(6, Math.round(6 * lvS));
      const grp = new THREE.Group();
      grp.position.set(x, 0, z);
      const movingContacts = [];

      const sideZ = lvSp + 0.15;
      [[-0.6, -sideZ], [0.6, -sideZ], [-0.6, sideZ], [0.6, sideZ]].forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(new THREE.BoxGeometry(0.11, 2.25, 0.11), MatLib.galvanizedSteel);
        leg.position.set(lx, 1.125, lz);
        leg.castShadow = true;
        grp.add(leg);
      });
      [-0.6, 0.6].forEach(lx => {
        const cross = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, lvSp * 2 + 0.6), MatLib.galvanizedSteel);
        cross.position.set(lx, 2.18, 0);
        grp.add(cross);
      });
      const ctrlCab = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.95, 0.72), MatLib.galvanizedSteel);
      ctrlCab.position.set(-0.62, 1.25, 0);
      grp.add(ctrlCab);

      [-lvSp, 0, lvSp].forEach((pz, idx) => {
        const cradle = new THREE.Mesh(new THREE.BoxGeometry(1.28, 0.12, 0.24), MatLib.galvanizedSteel);
        cradle.position.set(0, 2.18, pz);
        grp.add(cradle);

        const housing = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 1.15, 14), MatLib.siliconePolymer);
        housing.position.set(0, 2.35, pz);
        housing.rotation.z = Math.PI / 2;
        grp.add(housing);

        const bushIn = createRibbedInsulator(bushH, 0.12, shedsCount, MatLib.porcelainBrown, true);
        bushIn.position.set(-0.50 - 0.5 * bushH * Math.sin(tilt), 2.42 + 0.5 * bushH * Math.cos(tilt), pz);
        bushIn.rotation.z = tilt;
        const bushOut = createRibbedInsulator(bushH, 0.12, shedsCount, MatLib.porcelainBrown, true);
        bushOut.position.set(0.50 + 0.5 * bushH * Math.sin(tilt), 2.42 + 0.5 * bushH * Math.cos(tilt), pz);
        bushOut.rotation.z = -tilt;

        const padIn = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.06, 0.14), MatLib.silverContact);
        padIn.position.set(-termX, termY, pz);
        tagEnergizedTerminal(padIn, circuitTag, vLvTag);
        const padOut = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.06, 0.14), MatLib.silverContact);
        padOut.position.set(termX, termY, pz);
        tagEnergizedTerminal(padOut, circuitTag, vLvTag);
        grp.add(bushIn, bushOut, padIn, padOut);

        const intFlow = new THREE.Object3D();
        intFlow.userData.flowCurve = new THREE.CatmullRomCurve3([
          new THREE.Vector3(-termX, termY, pz),
          new THREE.Vector3(-0.4, 2.35, pz),
          new THREE.Vector3(0.4, 2.35, pz),
          new THREE.Vector3(termX, termY, pz)
        ]);
        intFlow.userData.voltageTag = vLvTag;
        intFlow.userData.circuitTag = circuitTag;
        grp.add(intFlow);

        const contactStem = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.4, 8), MatLib.silverContact);
        contactStem.position.set(isClosed ? 0 : 0.25, 2.35, pz);
        contactStem.rotation.z = Math.PI / 2;
        grp.add(contactStem);
        movingContacts.push(contactStem);

        const pMark = createPhaseMarker(idx, 0.045, 0.09);
        pMark.position.set(-termX, termY + 0.05, pz);
        grp.add(pMark);
      });

      const indColor = isClosed ? 0xef4444 : 0x10b981;
      const flag = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.2, 0.24), new THREE.MeshBasicMaterial({ color: indColor }));
      flag.position.set(-0.91, 1.5, 0);
      grp.add(flag);
      grp.userData.statusFlag = flag;
      grp.userData.movingContacts = movingContacts;
      grp.userData.tag = tag;
      grp.userData.termHeight = termY;
      grp.userData.termOffsetX = termX;
      grp.userData.phaseZ = [-lvSp, 0, lvSp];
      return grp;
    }

    // BUILDER 12: SECONDARY MAIN BAY, NGR, BUSBAR, UNDERGROUND SST CONDUIT & SHUNT CAPACITOR BANK
    function buildSecondaryBay(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const lvS = T.lvS;
      const lvSp = T.lvSp;
      const vLvTag = T.vSpec.lvKv + 'kV';
      const twinLv = T.vSpec.lvKv >= 138;
      const secZCenter = -0.6;
      const secPhaseZ = [-lvSp, 0, lvSp];
      const busBarY = +(Math.max(5.2, 4.2 + lvS * 1.15)).toFixed(3);

      const secGroup = new THREE.Group();
      secGroup.name = 'secondary';
      secGroup.userData = { componentId: 'secondary' };
      secGroup.position.set(0, 0, 0);

      const subparts = {};
      const txLvZ = T.txLvPhaseZ;

      // 1. Neutral Grounding Assembly (X0 -> Neutral CT 51G -> Neutral Grounding Resistor -> Ground Grid)
      const ngrGroup = new THREE.Group();
      ngrGroup.name = 'sec-ngr';
      const ngrX = L.txX + 3.4 * T.txTankScale, ngrZ = 2.8 * T.txTankScale;
      const ngrBush = createRibbedInsulator(0.28, 0.08, 3, MatLib.porcelainBrown, false);
      ngrBush.position.set(ngrX - 0.45, 2.54, ngrZ);
      ngrGroup.add(createCatenaryJumper(new THREE.Vector3(L.txX + T.txLvStudX, T.txLvStudY, txLvZ[3]), new THREE.Vector3(ngrX - 0.45, 2.68, ngrZ), 0.15, 6, MatLib.copperConductor, vLvTag, 'none'));
      const nctToroid = new THREE.Mesh(new THREE.TorusGeometry(0.20, 0.06, 10, 18), MatLib.darkSteel);
      nctToroid.position.set(ngrX - 0.45, 2.52, ngrZ);
      nctToroid.rotation.x = Math.PI / 2;
      [[-0.55, -0.45], [0.55, -0.45], [-0.55, 0.45], [0.55, 0.45]].forEach(([dx, dz]) => {
        const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.9, 0.08), MatLib.galvanizedSteel);
        leg.position.set(ngrX + dx, 0.45, ngrZ + dz);
        const post = createRibbedInsulator(0.42, 0.07, 4, MatLib.porcelainBrown, false);
        post.position.set(ngrX + dx, 1.1, ngrZ + dz);
        ngrGroup.add(leg, post);
      });
      const ngrCabinet = new THREE.Mesh(new THREE.BoxGeometry(1.45, 1.1, 1.15), MatLib.galvanizedSteel);
      ngrCabinet.position.set(ngrX, 1.85, ngrZ);
      ngrCabinet.castShadow = true;
      const ngrGroundStrap = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.35, 0.12), MatLib.groundCopper);
      ngrGroundStrap.position.set(ngrX + 0.76, 0.68, ngrZ);
      ngrGroup.add(ngrBush, nctToroid, ngrCabinet, ngrGroundStrap);
      secGroup.add(ngrGroup);
      ngrGroup.userData.basePos = ngrGroup.position.clone();
      subparts['sec-ngr'] = ngrGroup;

      // 2. Secondary Surge Arresters & Revenue Metering CTs/VTs
      const arrCtGroup = new THREE.Group();
      arrCtGroup.name = 'sec-arresters-ctvt';
      const arrTopY = +(1.95 + 1.20 * lvS).toFixed(3);
      secPhaseZ.forEach((pOff, idx) => {
        const z = secZCenter + pOff;
        const ped = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.95, 0.12), MatLib.galvanizedSteel);
        ped.position.set(L.secArresterX - 1.2, 0.975, z);
        const sa = createRibbedInsulator(1.20 * lvS, 0.12, Math.max(8, Math.round(8 * lvS)), MatLib.siliconePolymer, true);
        sa.position.set(L.secArresterX - 1.2, 1.95 + 0.60 * lvS, z);
        const ctPed = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.95, 0.12), MatLib.galvanizedSteel);
        ctPed.position.set(L.secArresterX, 0.975, z);
        const ctIns = createRibbedInsulator(0.75 * lvS, 0.14, 6, MatLib.porcelainBrown, true);
        ctIns.position.set(L.secArresterX, 1.95 + 0.375 * lvS, z);
        const ctHead = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.45 * lvS, 14), MatLib.porcelainBrown);
        ctHead.position.set(L.secArresterX, 1.95 + 0.975 * lvS, z);
        const pMark = createPhaseMarker(idx, 0.045, 0.09);
        pMark.position.set(L.secArresterX, arrTopY, z);
        tagEnergizedTerminal(pMark, 'sec_lv', vLvTag);
        arrCtGroup.add(ped, sa, ctPed, ctIns, ctHead, pMark);

        arrCtGroup.add(createCatenaryJumper(new THREE.Vector3(L.txX + T.txLvStudX, T.txLvStudY, txLvZ[idx]), new THREE.Vector3(L.secArresterX - 1.2, arrTopY, z), 0.22, 6, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
        arrCtGroup.add(createCatenaryJumper(new THREE.Vector3(L.secArresterX - 1.2, arrTopY, z), new THREE.Vector3(L.secArresterX, arrTopY, z), 0.08, 4, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
      });
      secGroup.add(arrCtGroup);
      arrCtGroup.userData.basePos = arrCtGroup.position.clone();
      subparts['sec-arresters-ctvt'] = arrCtGroup;

      // 3. Secondary Main Flanking Disconnects (89-LVA & 89-LVB) & Main Circuit Breaker (52-LV)
      const lvDisc = createMVDisconnectUnit(L.secDsAX, secZCenter, false, '89-LVA', T, 'sec_lv');
      lvDisc.name = 'sec-lv-disconnect';
      const lvDsTermY = lvDisc.userData.termHeight;
      const lvDsOff = lvDisc.userData.termOffsetX;
      secPhaseZ.forEach((pz) => {
        const z = secZCenter + pz;
        lvDisc.add(createCatenaryJumper(new THREE.Vector3(L.secArresterX - L.secDsAX, arrTopY, pz), new THREE.Vector3(-lvDsOff, lvDsTermY, pz), 0.1, 4, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
      });
      secGroup.add(lvDisc);
      lvDisc.userData.basePos = lvDisc.position.clone();
      subparts['sec-lv-disconnect'] = lvDisc;
      secGroup.userData.lvDisc = lvDisc;

      const lvCb = createMVBreakerUnit(L.secCbX, secZCenter, true, '52-LV', T, 'sec_lv');
      lvCb.name = 'sec-lv-breaker';
      const lvCbTermY = lvCb.userData.termHeight;
      const lvCbOff = lvCb.userData.termOffsetX;
      secPhaseZ.forEach(pz => {
        lvCb.add(createCatenaryJumper(new THREE.Vector3((L.secDsAX + lvDsOff) - L.secCbX, lvDsTermY, pz), new THREE.Vector3(-lvCbOff, lvCbTermY, pz), 0.12, 5, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
      });

      // Downstream Flanking Isolate 89-LVB mounted cleanly between 52-LV and Secondary Busbar
      const lvDiscB = createMVDisconnectUnit(L.secDsBX, secZCenter, false, '89-LVB', T, 'sec_bus');
      lvDiscB.name = 'sec-lv-disconnect-b';
      secPhaseZ.forEach(pz => {
        lvCb.add(createCatenaryJumper(new THREE.Vector3(lvCbOff, lvCbTermY, pz), new THREE.Vector3((L.secDsBX - lvDsOff) - L.secCbX, lvDsTermY, pz), 0.12, 5, MatLib.copperConductor, vLvTag, 'sec_bus', twinLv));
      });
      secGroup.add(lvCb, lvDiscB);
      lvCb.userData.basePos = lvCb.position.clone();
      subparts['sec-lv-breaker'] = lvCb;
      secGroup.userData.lvBreaker = lvCb;
      secGroup.userData.lvDiscB = lvDiscB;

      // 4. Secondary Rigid Aluminum Distribution Busbar & Underground Trench Conduit Tap to SST-100 (Zero Aerial Wall Clipping!)
      const distBusGroup = new THREE.Group();
      distBusGroup.name = 'sec-dist-bus';
      const busZMin = Math.min(-15.5, L.capZ + 1.0);
      const busZMax = Math.max(12.5, L.fdr2Z + 6.0);
      const tapZ = Math.min(busZMax - 0.8, L.sstZ - 3.6);
      const potheadX = L.secBusX + 1.8;

      secPhaseZ.forEach((pxOff, idx) => {
        const bx = L.secBusX + pxOff;
        const busTube = createRigidBusSegment(
          new THREE.Vector3(bx, busBarY, busZMin),
          new THREE.Vector3(bx, busBarY, busZMax),
          0.048, MatLib.aluminumBus, vLvTag, 'sec_bus', twinLv
        );
        distBusGroup.add(busTube);

        [busZMin + 2.5, -2, busZMax - 2.5].forEach(sz => {
          const insH = 1.4 * lvS;
          const pedH = busBarY - insH;
          const postPed = new THREE.Mesh(new THREE.BoxGeometry(0.1, pedH, 0.1), MatLib.galvanizedSteel);
          postPed.position.set(bx, pedH / 2, sz);
          const postIns = createRibbedInsulator(insH, 0.12, Math.max(7, Math.round(7 * lvS)), MatLib.porcelainBrown, true);
          postIns.position.set(bx, pedH + insH / 2, sz);
          distBusGroup.add(postPed, postIns);
        });
        const pm = createPhaseMarker(idx, 0.06, 0.22);
        pm.position.set(bx, busBarY, 0);
        pm.rotation.x = Math.PI / 2;
        distBusGroup.add(pm);

        // 89-LVB -> Secondary Busbar
        distBusGroup.add(createCatenaryJumper(new THREE.Vector3(L.secDsBX + lvDsOff, lvDsTermY, secZCenter + pxOff), new THREE.Vector3(bx, busBarY, secZCenter + pxOff), 0.22, 6, MatLib.copperConductor, vLvTag, 'sec_bus', twinLv));

        // Underground Armored Cable Pothead Riser + Sub-Grade Trench Duct -> SST-100 Primary Throat (0 wall/air clipping)
        const phTop = new THREE.Vector3(potheadX, 2.65, tapZ + idx * 0.45);
        const phTrench = new THREE.Vector3(potheadX, -0.35, tapZ + idx * 0.45);
        const sstTrench = new THREE.Vector3(L.sstX + [-0.4, 0, 0.4][idx], -0.35, L.sstZ - 0.15);
        const sstTerm = new THREE.Vector3(L.sstX + [-0.4, 0, 0.4][idx], 2.25, L.sstZ - 0.15);
        const potStand = new THREE.Mesh(new THREE.BoxGeometry(0.14, 2.02, 0.14), MatLib.galvanizedSteel);
        potStand.position.set(phTop.x, 1.01, phTop.z);
        const potIns = createRibbedInsulator(0.65, 0.065, 5, MatLib.porcelainBrown, false);
        potIns.position.set(phTop.x, 2.35, phTop.z);
        distBusGroup.add(potStand, potIns);
        distBusGroup.add(createCatenaryJumper(new THREE.Vector3(bx, busBarY, tapZ + idx * 0.45), phTop, 0.18, 5, MatLib.copperConductor, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(phTop, phTrench, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(phTrench, sstTrench, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(sstTrench, sstTerm, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
      });
      // Visible Precast Concrete Cable Trench Cover along pothead-to-SST run
      const trenchLen = Math.max(2.0, L.sstX - potheadX + 1.5);
      const trenchRunZ = (tapZ + L.sstZ) / 2;
      const trenchCap = new THREE.Mesh(new THREE.BoxGeometry(trenchLen, 0.08, 0.9), MatLib.concretePad);
      trenchCap.position.set((potheadX + L.sstX) / 2, 0.05, trenchRunZ);
      distBusGroup.add(trenchCap);

      secGroup.add(distBusGroup);
      distBusGroup.userData.basePos = distBusGroup.position.clone();
      subparts['sec-dist-bus'] = distBusGroup;

      // 5. Switched Shunt Capacitor Bank (89-CAPA -> 52-CAP -> 89-CAPB -> Capacitor Rack)
      const capGroup = new THREE.Group();
      capGroup.name = 'sec-cap-bank';
      const rackCols = [[-1.6, -1.5], [1.6, -1.5], [-1.6, 1.5], [1.6, 1.5]];
      rackCols.forEach(([dx, dz]) => {
        const col = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3.0, 0.1), MatLib.galvanizedSteel);
        col.position.set(L.capX + dx, 1.5, L.capZ + dz);
        capGroup.add(col);
      });
      const capTopRail = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 3.1), MatLib.galvanizedSteel);
      capTopRail.position.set(L.capX + 1.45, 2.95, L.capZ);
      const capLeftRail = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 3.1), MatLib.galvanizedSteel);
      capLeftRail.position.set(L.capX - 1.55, 2.95, L.capZ);
      const capSideRailF = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.10, 0.12), MatLib.galvanizedSteel);
      capSideRailF.position.set(L.capX, 2.95, L.capZ + 1.5);
      const capSideRailB = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.10, 0.12), MatLib.galvanizedSteel);
      capSideRailB.position.set(L.capX, 2.95, L.capZ - 1.5);
      capGroup.add(capTopRail, capLeftRail, capSideRailF, capSideRailB);

      const capSwZ = Math.min(busZMin + 1.8, L.capZ + 3.2);
      const dsCapA = createMVDisconnectUnit(L.capX + 6.4, capSwZ, false, '89-CAPA', T, 'cap_bank');
      const cbCap = createMVBreakerUnit(L.capX + 4.4, capSwZ, true, '52-CAP', T, 'cap_bank');
      const dsCapB = createMVDisconnectUnit(L.capX + 2.4, capSwZ, false, '89-CAPB', T, 'cap_bank');
      capGroup.add(dsCapA, cbCap, dsCapB);
      secGroup.userData.capDiscA = dsCapA;
      secGroup.userData.capBreaker = cbCap;
      secGroup.userData.capDiscB = dsCapB;

      [-1.1, 0, 1.1].forEach((cz, idx) => {
        const shelf = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.09, 0.36), MatLib.galvanizedSteel);
        shelf.position.set(L.capX, 1.85, L.capZ + cz);
        capGroup.add(shelf);
        [-1.0, -0.35, 0.35, 1.0].forEach(cx => {
          const can = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.72, 0.22), MatLib.radiatorFin);
          can.position.set(L.capX + cx, 2.28, L.capZ + cz);
          const bush = createRibbedInsulator(0.35, 0.05, 3, MatLib.porcelainBrown, false);
          bush.position.set(L.capX + cx, 2.8, L.capZ + cz);
          capGroup.add(can, bush);
        });
        const sw = createRibbedInsulator(0.6, 0.08, 4, MatLib.siliconePolymer, true);
        sw.position.set(L.capX + 1.45, 3.25, L.capZ + cz);
        capGroup.add(sw);

        const pOff = secPhaseZ[idx];
        // Secondary Bus -> 89-CAPA -> 52-CAP -> 89-CAPB -> Capacitor Bank Rack
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.secBusX + pOff, busBarY, busZMin + 0.8 + idx * 0.35), new THREE.Vector3(L.capX + 6.4 + lvDsOff, lvDsTermY, capSwZ + pOff), 0.22, 6, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.capX + 6.4 - lvDsOff, lvDsTermY, capSwZ + pOff), new THREE.Vector3(L.capX + 4.4 + lvCbOff, lvCbTermY, capSwZ + pOff), 0.12, 5, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.capX + 4.4 - lvCbOff, lvCbTermY, capSwZ + pOff), new THREE.Vector3(L.capX + 2.4 + lvDsOff, lvDsTermY, capSwZ + pOff), 0.12, 5, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.capX + 2.4 - lvDsOff, lvDsTermY, capSwZ + pOff), new THREE.Vector3(L.capX + 1.45, 3.55, L.capZ + cz), 0.20, 6, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
      });
      secGroup.add(capGroup);
      capGroup.userData.basePos = capGroup.position.clone();
      subparts['sec-cap-bank'] = capGroup;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      secGroup.userData.subparts = subparts;
      scene.add(secGroup);
      return secGroup;
    }

    // BUILDER 13: DUAL OUTGOING DISTRIBUTION FEEDER BAYS (FEEDER 01 & FEEDER 02)
    function buildFeederBays(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const lvS = T.lvS;
      const lvSp = T.lvSp;
      const vLvTag = T.vSpec.lvKv + 'kV';
      const twinLv = T.vSpec.lvKv >= 138;
      const busBarY = +(Math.max(5.2, 4.2 + lvS * 1.15)).toFixed(3);

      const fdrGroup = new THREE.Group();
      fdrGroup.name = 'feeders';
      fdrGroup.userData = { componentId: 'feeders', switches: {} };

      const subparts = {};
      const fSpan = Math.max(12.0, L.fdrGantryX - L.secBusX);
      const xDsA = L.secBusX + fSpan * 0.22;
      const xCb = L.secBusX + fSpan * 0.48;
      const xDsB = L.secBusX + fSpan * 0.74;
      const xCtSa = L.secBusX + fSpan * 0.89;

      function buildFeederLine(bayId, zCenter, labelA, labelCB, labelB, cTag) {
        const bayGroup = new THREE.Group();
        bayGroup.name = bayId;

        const dsA = createMVDisconnectUnit(xDsA, zCenter, false, labelA, T, cTag);
        const cb = createMVBreakerUnit(xCb, zCenter, true, labelCB, T, cTag);
        const dsB = createMVDisconnectUnit(xDsB, zCenter, false, labelB, T, cTag);
        bayGroup.add(dsA, cb, dsB);

        const dsY = dsA.userData.termHeight;
        const dsO = dsA.userData.termOffsetX;
        const cbY = cb.userData.termHeight;
        const cbO = cb.userData.termOffsetX;

        fdrGroup.userData.switches[labelA] = dsA;
        fdrGroup.userData.switches[labelCB] = cb;
        fdrGroup.userData.switches[labelB] = dsB;

        [-lvSp, 0, lvSp].forEach((pz) => {
          const z = zCenter + pz;
          bayGroup.add(createCatenaryJumper(new THREE.Vector3(L.secBusX + pz, busBarY, z), new THREE.Vector3(xDsA - dsO, dsY, z), 0.25, 6, MatLib.copperConductor, vLvTag, cTag, twinLv));
          bayGroup.add(createCatenaryJumper(new THREE.Vector3(xDsA + dsO, dsY, z), new THREE.Vector3(xCb - cbO, cbY, z), 0.14, 5, MatLib.copperConductor, vLvTag, cTag, twinLv));
          bayGroup.add(createCatenaryJumper(new THREE.Vector3(xCb + cbO, cbY, z), new THREE.Vector3(xDsB - dsO, dsY, z), 0.14, 5, MatLib.copperConductor, vLvTag, cTag, twinLv));
        });
        return bayGroup;
      }

      const f1Group = buildFeederLine('fdr-f1-breaker', L.fdr1Z, '89-F1A', '52-F1', '89-F1B', 'fdr1');
      fdrGroup.add(f1Group);
      f1Group.userData.basePos = f1Group.position.clone();
      subparts['fdr-f1-breaker'] = f1Group;

      const f2Group = buildFeederLine('fdr-f2-breaker', L.fdr2Z, '89-F2A', '52-F2', '89-F2B', 'fdr2');
      fdrGroup.add(f2Group);
      f2Group.userData.basePos = f2Group.position.clone();
      subparts['fdr-f2-breaker'] = f2Group;

      const ctTopY = +(2.05 + 1.05 * lvS).toFixed(3);
      const refDsY = +(2.20 + 0.95 * lvS + 0.03).toFixed(3);
      const fdrCtGroup = new THREE.Group();
      fdrCtGroup.name = 'fdr-ct-arresters';
      [L.fdr1Z, L.fdr2Z].forEach((zC, fIdx) => {
        const cTag = fIdx === 0 ? 'fdr1' : 'fdr2';
        [-lvSp, 0, lvSp].forEach((pz) => {
          const z = zC + pz;
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2.05, 0.1), MatLib.galvanizedSteel);
          leg.position.set(xCtSa, 1.025, z);
          const sa = createRibbedInsulator(1.05 * lvS, 0.1, Math.max(7, Math.round(7 * lvS)), MatLib.siliconePolymer, true);
          sa.position.set(xCtSa, 2.05 + 0.525 * lvS, z);
          const ctRing = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.045, 8, 16), MatLib.darkSteel);
          ctRing.position.set(xCtSa, ctTopY - 0.08, z);
          ctRing.rotation.x = Math.PI / 2;
          fdrCtGroup.add(leg, sa, ctRing);
          fdrCtGroup.add(createCatenaryJumper(new THREE.Vector3(xDsB + 0.45, refDsY, z), new THREE.Vector3(xCtSa, ctTopY, z), 0.1, 4, MatLib.copperConductor, vLvTag, cTag, twinLv));
        });
      });
      fdrGroup.add(fdrCtGroup);
      fdrCtGroup.userData.basePos = fdrCtGroup.position.clone();
      subparts['fdr-ct-arresters'] = fdrCtGroup;

      const gantryOutGroup = new THREE.Group();
      gantryOutGroup.name = 'fdr-takeoff-gantry';
      const outGantryY = +(7.2 + (lvS - 1.0) * 1.8).toFixed(2);
      [L.fdr1Z, L.fdr2Z].forEach((zC, fIdx) => {
        const cTag = fIdx === 0 ? 'fdr1' : 'fdr2';
        const mastW = lvSp + 1.0;
        [-mastW, mastW].forEach(dz => {
          const pole = createLatticeMast(outGantryY + 1.6, 0.9, 0.32);
          pole.position.set(L.fdrGantryX, 0, zC + dz);
          gantryOutGroup.add(pole);
        });
        const xarm = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.45, mastW * 2 + 0.8), MatLib.galvanizedSteel);
        xarm.position.set(L.fdrGantryX, outGantryY, zC);
        xarm.castShadow = true;
        gantryOutGroup.add(xarm);

        [-lvSp, 0, lvSp].forEach(pz => {
          const z = zC + pz;
          const ins = createRibbedInsulator(0.8 * Math.min(1.4, lvS), 0.08, 6, MatLib.siliconePolymer, true);
          ins.position.set(L.fdrGantryX + 0.55, outGantryY, z);
          ins.rotation.z = Math.PI / 2;
          const lineOut = createRigidBusSegment(
            new THREE.Vector3(L.fdrGantryX + 0.95, outGantryY, z),
            new THREE.Vector3(L.fdrGantryX + 18.95, outGantryY, z),
            0.018, MatLib.aluminumBus, vLvTag, cTag, twinLv
          );
          gantryOutGroup.add(ins, lineOut);
          gantryOutGroup.add(createCatenaryJumper(new THREE.Vector3(xCtSa, ctTopY, z), new THREE.Vector3(L.fdrGantryX - 0.15, outGantryY - 0.05, z), 0.35, 7, MatLib.copperConductor, vLvTag, cTag, twinLv));
        });
      });
      fdrGroup.add(gantryOutGroup);
      gantryOutGroup.userData.basePos = gantryOutGroup.position.clone();
      subparts['fdr-takeoff-gantry'] = gantryOutGroup;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      fdrGroup.userData.subparts = subparts;
      scene.add(fdrGroup);
      return fdrGroup;
    }

    // BUILDER 14: ENCLOSURE ARCHITECTURE (SF6 GIS OR INDOOR METAL-CLAD SWITCHGEAR W/ THROUGH-WALL BUSHINGS)
    function buildEnclosureArchitecture(scene, layout, enclosureType = 'ais') {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vHvTag = vSpec.hvKv + 'kV';
      const vLvTag = vSpec.lvKv + 'kV';
      const s = T.s;
      const lvSp = T.lvSp;

      const encGroup = new THREE.Group();
      encGroup.name = 'enclosure-arch';
      encGroup.userData = { shells: [], indoorMetalCladCubicles: null };
      if (enclosureType === 'ais') {
        encGroup.visible = false;
        scene.add(encGroup);
        return encGroup;
      }

      if (enclosureType === 'gis') {
        const gisW = L.gisW || 10.0, gisL = L.gisL || 12.0, gisH = +(5.4 + (s - 1.0) * 1.4).toFixed(2);
        const gisX = L.gisX !== undefined ? L.gisX : -1.5;
        const wallCutMat = new THREE.MeshPhysicalMaterial({
          color: 0x38bdf8, transparent: true, opacity: 0.16, roughness: 0.15, side: THREE.DoubleSide
        });
        const hallFloor = new THREE.Mesh(new THREE.BoxGeometry(gisW, 0.3, gisL), MatLib.concrete);
        hallFloor.position.set(gisX, 0.15, 0);
        const hallShell = new THREE.Mesh(new THREE.BoxGeometry(gisW, gisH, gisL), wallCutMat);
        hallShell.position.set(gisX, gisH / 2 + 0.3, 0);
        hallShell.userData.isCutawayShell = true;
        encGroup.userData.shells.push(hallShell);
        encGroup.add(hallFloor, hallShell);

        const addGisBreakerCapsule = (cx, cz, ry = 0, tag = '52') => {
          const cap = new THREE.Group();
          cap.position.set(cx, 2.2, cz);
          cap.rotation.y = ry;
          const drum = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.46, 1.8, 20), MatLib.transformerTank);
          drum.rotation.z = Math.PI / 2;
          const fl1 = new THREE.Mesh(new THREE.CylinderGeometry(0.54, 0.54, 0.1, 20), MatLib.yellowHighlight);
          fl1.position.x = -0.85; fl1.rotation.z = Math.PI / 2;
          const fl2 = fl1.clone(); fl2.position.x = 0.85;
          const drv = new THREE.Mesh(new THREE.BoxGeometry(0.65, 1.15, 0.55), MatLib.relayPanelSteel);
          drv.position.set(0, -1.1, 0.58);
          const ind = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.16, 0.18), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
          ind.position.set(0, -0.75, 0.88);
          cap.add(drum, fl1, fl2, drv, ind);
          cap.userData.statusFlag = ind;
          cap.userData.tag = tag;
          encGroup.add(cap);
          return cap;
        };

        const addGisBushingsPair = (inX, outX, phaseZs, cInTag = 'incoming', cOutTag = 'tx_hv') => {
          const bushH = +(2.4 * s).toFixed(2);
          const bushTopY = +(2.6 + bushH).toFixed(2);
          phaseZs.forEach((pz, pIdx) => {
            const bIn = createRibbedInsulator(bushH, 0.2, Math.max(10, Math.round(12 * s)), MatLib.siliconePolymer, true);
            bIn.position.set(inX, 2.6 + bushH / 2, pz);
            const bOut = createRibbedInsulator(bushH, 0.2, Math.max(10, Math.round(12 * s)), MatLib.siliconePolymer, true);
            bOut.position.set(outX, 2.6 + bushH / 2, pz);
            const capIn = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 12), MatLib.aluminumBus);
            capIn.position.set(inX, bushTopY, pz);
            tagEnergizedTerminal(capIn, cInTag, vHvTag);
            const capOut = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 12), MatLib.aluminumBus);
            capOut.position.set(outX, bushTopY, pz);
            tagEnergizedTerminal(capOut, cOutTag, vHvTag);
            if (vSpec.coronaRings) {
              const r1 = createCoronaRing(0.36, 0.026); r1.position.set(inX, bushTopY - 0.15, pz);
              const r2 = createCoronaRing(0.36, 0.026); r2.position.set(outX, bushTopY - 0.15, pz);
              encGroup.add(r1, r2);
            }
            encGroup.add(bIn, bOut, capIn, capOut);
            encGroup.add(createCatenaryJumper(new THREE.Vector3(L.ctX + 0.65, T.ctTopY, [-T.pz, 0, T.pz][pIdx]), new THREE.Vector3(inX, bushTopY, pz), 0.25, 6, MatLib.copperConductor, vHvTag, cInTag, vSpec.twinBundle));
            encGroup.add(createCatenaryJumper(new THREE.Vector3(outX, bushTopY, pz), new THREE.Vector3(L.txX + T.txHvStudX, T.txHvStudY, T.txHvPhaseZ[pIdx]), 0.25, 6, MatLib.copperConductor, vHvTag, cOutTag, vSpec.twinBundle));
          });
        };

        const ph3 = [-2.0, 0, 2.0];
        if (L.scheme === 'single') {
          ph3.forEach(pz => {
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 3.2, 2.2, pz), new THREE.Vector3(gisX + 3.2, 2.2, pz), 0.30, MatLib.aluminumBus, vHvTag, 'main_path'));
            [-2.2, 0.0, 2.2].forEach(fx => {
              const fl = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.12, 18), MatLib.yellowHighlight);
              fl.position.set(gisX + fx, 2.2, pz); fl.rotation.z = Math.PI / 2;
              encGroup.add(fl);
            });
          });
          addGisBreakerCapsule(gisX + 0.5, 0, 0, '52-69');
          addGisBushingsPair(gisX - 3.2, gisX + 3.2, ph3);
        } else if (L.scheme === 'maintransfer') {
          const zMain = [-3.6, -2.4, -1.2], zXfer = [1.2, 2.4, 3.6];
          for (let p = 0; p < 3; p++) {
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 4.2, 2.2, zMain[p]), new THREE.Vector3(gisX + 4.2, 2.2, zMain[p]), 0.24, MatLib.aluminumBus, vHvTag, 'main_path'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 4.2, 3.2, zXfer[p]), new THREE.Vector3(gisX + 4.2, 3.2, zXfer[p]), 0.24, MatLib.aluminumBus, vHvTag, 'bypass_path'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX + 2.2, 2.2, zMain[p]), new THREE.Vector3(gisX + 2.2, 3.2, zXfer[p]), 0.18, MatLib.aluminumBus, vHvTag, 'bypass_path'));
          }
          addGisBreakerCapsule(gisX - 0.8, -2.4, 0, '52-69');
          addGisBreakerCapsule(gisX + 2.2, 0.0, Math.PI / 2, '52-BT');
          addGisBushingsPair(gisX - 4.2, gisX + 4.2, zMain);
        } else if (L.scheme === 'ring') {
          const rx1 = gisX - 3.6, rx2 = gisX + 3.6, rz1 = -4.2, rz2 = 4.2;
          [-0.9, 0, 0.9].forEach(pOff => {
            encGroup.add(createRigidBusSegment(new THREE.Vector3(rx1 + pOff, 2.3, rz1 + pOff), new THREE.Vector3(rx2 + pOff, 2.3, rz1 + pOff), 0.20, MatLib.aluminumBus, vHvTag, 'ring_leg2'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(rx1 + pOff, 2.3, rz2 + pOff), new THREE.Vector3(rx2 + pOff, 2.3, rz2 + pOff), 0.20, MatLib.aluminumBus, vHvTag, 'ring_leg4'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(rx1 + pOff, 2.3, rz1 + pOff), new THREE.Vector3(rx1 + pOff, 2.3, rz2 + pOff), 0.20, MatLib.aluminumBus, vHvTag, 'ring_leg1'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(rx2 + pOff, 2.3, rz1 + pOff), new THREE.Vector3(rx2 + pOff, 2.3, rz2 + pOff), 0.20, MatLib.aluminumBus, vHvTag, 'ring_leg3'));
          });
          addGisBreakerCapsule(rx1, 0, Math.PI / 2, '52-1');
          addGisBreakerCapsule(gisX, rz1, 0, '52-2');
          addGisBreakerCapsule(rx2, 0, Math.PI / 2, '52-3');
          addGisBreakerCapsule(gisX, rz2, 0, '52-4');
          addGisBushingsPair(rx1 - 1.2, rx2 + 1.2, [-1.4, 0, 1.4]);
        } else if (L.scheme === 'breakerhalf') {
          const zA = -6.2, zB = 6.2;
          [-1.0, 0, 1.0].forEach(pOff => {
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 4.4, 2.6, zA + pOff), new THREE.Vector3(gisX + 4.4, 2.6, zA + pOff), 0.22, MatLib.aluminumBus, vHvTag, 'bh_busA'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 4.4, 2.6, zB + pOff), new THREE.Vector3(gisX + 4.4, 2.6, zB + pOff), 0.22, MatLib.aluminumBus, vHvTag, 'bh_busB'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX + pOff, 2.2, zA), new THREE.Vector3(gisX + pOff, 2.2, zB), 0.20, MatLib.aluminumBus, vHvTag, 'bh_tie'));
          });
          addGisBreakerCapsule(gisX, -3.5, Math.PI / 2, '52-A');
          addGisBreakerCapsule(gisX, 0.0, Math.PI / 2, '52-TIE');
          addGisBreakerCapsule(gisX, 3.5, Math.PI / 2, '52-B');
          addGisBushingsPair(gisX - 4.2, gisX + 4.2, [-1.8, 0, 1.8]);
        } else if (L.scheme === 'doublebreaker') {
          const zA = -6.5, zB = 6.5;
          [-1.0, 0, 1.0].forEach(pOff => {
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 5.4, 2.6, zA + pOff), new THREE.Vector3(gisX + 5.4, 2.6, zA + pOff), 0.22, MatLib.aluminumBus, vHvTag, 'db_busA'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 5.4, 2.6, zB + pOff), new THREE.Vector3(gisX + 5.4, 2.6, zB + pOff), 0.22, MatLib.aluminumBus, vHvTag, 'db_busB'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX - 2.6 + pOff, 2.2, zA), new THREE.Vector3(gisX - 2.6 + pOff, 2.2, zB), 0.20, MatLib.aluminumBus, vHvTag, 'db_b1A'));
            encGroup.add(createRigidBusSegment(new THREE.Vector3(gisX + 2.6 + pOff, 2.2, zA), new THREE.Vector3(gisX + 2.6 + pOff, 2.2, zB), 0.20, MatLib.aluminumBus, vHvTag, 'db_b2A'));
          });
          addGisBreakerCapsule(gisX - 2.6, -3.2, Math.PI / 2, '52-1A');
          addGisBreakerCapsule(gisX - 2.6, 3.2, Math.PI / 2, '52-1B');
          addGisBreakerCapsule(gisX + 2.6, -3.2, Math.PI / 2, '52-2A');
          addGisBreakerCapsule(gisX + 2.6, 3.2, Math.PI / 2, '52-2B');
          addGisBushingsPair(gisX - 5.2, gisX + 5.2, [-1.8, 0, 1.8]);
        }

        const lcc = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.9, 0.75), MatLib.relayPanelSteel);
        lcc.position.set(gisX, 1.25, gisL / 2 - 1.1);
        encGroup.add(lcc);

      } else if (enclosureType === 'indoor') {
        const fwLen = Math.max(13.5, T.txTankScale * 6.5 * 2);
        const fireWall = new THREE.Mesh(new THREE.BoxGeometry(0.45, 6.2 * Math.min(1.3, T.lvS), fwLen), MatLib.fireWallConcrete);
        fireWall.position.set(L.txX + 4.2 * T.txTankScale, 3.1 * Math.min(1.3, T.lvS), 0);
        fireWall.castShadow = true;
        encGroup.add(fireWall);

        const swX = (L.secCbX + L.secBusX) / 2;
        const swZ = (L.fdr1Z + L.fdr2Z) / 2;
        const swW = (L.secBusX - L.secCbX) + 6.4;
        const swL = Math.max(20.5, Math.abs(L.fdr2Z - L.fdr1Z) + 10.0);
        const swH = 5.4;

        const mcSlab = new THREE.Mesh(new THREE.BoxGeometry(swW, 0.35, swL), MatLib.concrete);
        mcSlab.position.set(swX, 0.175, swZ);
        const wallMat = new THREE.MeshPhysicalMaterial({
          color: 0x94a3b8, transparent: true, opacity: 0.22, roughness: 0.4, side: THREE.DoubleSide
        });
        const mcShell = new THREE.Mesh(new THREE.BoxGeometry(swW, swH, swL), wallMat);
        mcShell.position.set(swX, swH / 2 + 0.35, swZ);
        mcShell.userData.isCutawayShell = true;
        encGroup.userData.shells.push(mcShell);
        encGroup.add(mcSlab, mcShell);

        // 3-Phase Porcelain Through-Wall Entrance Bushings through West Hall Wall (Zero Wall Clipping!)
        const westWallX = swX - swW / 2;
        const busYIndoor = 3.22 + (T.lvS - 1.0) * 0.8;
        [-lvSp, 0, lvSp].forEach(pOff => {
          const z = -0.6 + pOff;
          const collar = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.14, 14), MatLib.darkSteel);
          collar.rotation.z = Math.PI / 2;
          collar.position.set(westWallX, busYIndoor, z);
          const wallBush = createRibbedInsulator(1.1, 0.12, 6, MatLib.porcelainBrown, false);
          wallBush.rotation.z = Math.PI / 2;
          wallBush.position.set(westWallX, busYIndoor, z);
          encGroup.add(collar, wallBush);

          encGroup.add(createCatenaryJumper(new THREE.Vector3(L.secArresterX + 0.2, 2.0 + 1.15 * T.lvS + 0.08, z), new THREE.Vector3(westWallX - 0.55, busYIndoor, z), 0.12, 5, MatLib.copperConductor, vLvTag, 'sec_lv'));
          encGroup.add(createRigidBusSegment(new THREE.Vector3(westWallX - 0.55, busYIndoor, z), new THREE.Vector3(L.secBusX - 0.8, busYIndoor, z), 0.055, MatLib.copperConductor, vLvTag, 'sec_lv'));
          encGroup.add(createRigidBusSegment(new THREE.Vector3(L.secBusX - 0.8, 3.85, swZ - swL * 0.38), new THREE.Vector3(L.secBusX - 0.8, 3.85, swZ + swL * 0.38), 0.06, MatLib.aluminumBus, vLvTag, 'sec_bus'));
        });

        const labels = ['52-LV IN', 'PT/MET', 'AUX TAP', '52-CAP', '52-F1 OUT', '52-F2 OUT'];
        labels.forEach((lbl, idx) => {
          const cz = swZ - 7.5 + idx * 3.0;
          const cub = new THREE.Mesh(new THREE.BoxGeometry(2.4, 2.6, 1.9), MatLib.relayPanelSteel);
          cub.position.set(L.secBusX - 0.8, 1.65, cz);
          const face = new THREE.Mesh(
            new THREE.PlaneGeometry(1.7, 2.4),
            new THREE.MeshBasicMaterial({ map: TextureGen.createRelayPanelTexture(lbl, vLvTag + ' DRAW-OUT VCB', ['52', '50/51', '27', '86']) })
          );
          face.position.set(L.secBusX - 2.01, 1.65, cz);
          face.rotation.y = -Math.PI / 2;
          encGroup.add(cub, face);
        });
      }

      scene.add(encGroup);
      return encGroup;
    }
    """

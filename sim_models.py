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
      arresterPorcelainGlaze: new THREE.MeshStandardMaterial({ color: 0x6e2c14, roughness: 0.16, metalness: 0.12 }), // Dark reddish-brown glazed porcelain
      insulatedGroundLead: new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.32, metalness: 0.18 }), // High-visibility insulated surge ground lead
      utilityWoodPole: new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.88, metalness: 0.04 }), // Legacy wood ref
      galvanizedTubularSteel: new THREE.MeshStandardMaterial({ color: 0xb0bec5, metalness: 0.68, roughness: 0.32 }), // Octagonal/dodecagonal tapered galvanized tubular steel pole
      spoolTanComposite: new THREE.MeshStandardMaterial({ color: 0xd6bfa2, roughness: 0.35, metalness: 0.08 }), // Bone-fiber expulsion cutout fuse tube
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
      const secMaxZ = cfg.fdr2Z + 4.0 * (vSpec.lvKv > 40 ? 1.2 : 1.0);
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

      // Control House placed cleanly South of South Access Road with >= 2.6 m road setback (zero bay overlap in ALL 15 cases!)
      const ctrlX = +(cfg.txX + 2.5).toFixed(2);
      const ctrlZ = +(roadSouthZ + roadW / 2 + 2.6 + 6.4).toFixed(2);

      // Anchor SST-100 Station Service Transformer strictly adjacent (5-6 m) to East side of Control House across ALL schemes & enclosures
      const sstX = +(ctrlX + 7.6).toFixed(2);
      const sstZ = ctrlZ;

      const yardMinX = roadWestX - roadW / 2 - 2.4;
      const yardMaxX = Math.max(roadEastX + roadW / 2 + 2.4, sstX + 3.8);
      const yardMinZ = roadNorthZ - roadW / 2 - 2.4;
      const yardMaxZ = Math.max(roadSouthZ + roadW / 2, ctrlZ + 6.4) + 2.8;

      return Object.assign(cfg, {
        vSpec,
        eqBounds: { minX: eqMinX, maxX: eqMaxX, minZ: eqMinZ, maxZ: eqMaxZ },
        roads: { roadW, northZ: roadNorthZ, southZ: roadSouthZ, westX: roadWestX, eastX: roadEastX },
        ctrlX, ctrlZ,
        sstX, sstZ,
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
      const xScale = vSpec.id === '500_230' ? 1.78 : (vSpec.id === '230_138' ? 1.46 : (vSpec.id === '138_69' ? 1.24 : 1.0));
      const zScale = vSpec.id === '500_230' ? 1.76 : (vSpec.id === '230_138' ? 1.44 : (vSpec.id === '138_69' ? 1.22 : 1.0));
      const lvScale = vSpec.lvKv >= 230 ? 1.56 : (vSpec.lvKv >= 138 ? 1.38 : (vSpec.lvKv >= 69 ? 1.18 : 1.0));

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

    // Helper: Single source of truth for terminal heights, phase spacings & TR-01 stud coords across all 4 voltage classes
    function getPrimaryTerminals(L) {
      const vSpec = (L && L.vSpec) || getVoltageSpec(L && L.voltageClass);
      const s = vSpec.insScale || 1.0;
      const pz = vSpec.bayPhaseZ || 3.5;
      const unitPz = vSpec.phaseSpacing || 2.4;
      const lvS = vSpec.lvKv >= 230 ? 1.62 : (vSpec.lvKv >= 138 ? 1.48 : (vSpec.lvKv >= 69 ? 1.18 : 1.0));
      const lvSp = vSpec.lvKv >= 230 ? 3.8 : (vSpec.lvKv >= 138 ? 3.2 : (vSpec.lvKv >= 69 ? 2.4 : 1.65));

      const laTopY = +(2.58 + 2.85 * s + 0.22).toFixed(3);
      const ctTopY = +(2.20 + 2.85 * s + 0.26).toFixed(3);
      const dsTermY = +(2.35 + 2.35 * s + 0.14).toFixed(3);
      const cbTilt = Math.PI / 10;
      const cbBushingH = 2.25 * s;
      const cbTermOffsetX = vSpec.liveTankMultiChamber ? +(2.15 + 0.35 * s).toFixed(3) : +(0.72 + cbBushingH * Math.sin(cbTilt)).toFixed(3);
      const cbTermY = vSpec.liveTankMultiChamber ? +(2.25 + 2.20 * s).toFixed(3) : +(2.38 + cbBushingH * Math.cos(cbTilt) + 0.04).toFixed(3);
      const busY = +(Math.max(ctTopY + 0.45, dsTermY + 0.95)).toFixed(3);

      const txTankScale = vSpec.id === '500_230' ? 1.42 : (vSpec.id === '230_138' ? 1.32 : (vSpec.id === '138_69' ? 1.16 : 1.0));
      const txCoverY = +(0.2 + 3.8 * txTankScale).toFixed(3);
      const txHvTilt = Math.PI / 22;
      const txHvH = 2.65 * s;
      const txHvTopX = -1.0 * txTankScale - txHvH * Math.sin(txHvTilt);
      const txHvTopY = txCoverY + 0.20 + txHvH * Math.cos(txHvTilt);
      const txHvStudX = +(txHvTopX - 0.22 * Math.sin(txHvTilt)).toFixed(3);
      const txHvStudY = +(txHvTopY + 0.22 * Math.cos(txHvTilt)).toFixed(3);
      const autoBank = !!vSpec.autoTxBank;
      const txHvPhaseZ = autoBank ? [-pz, 0, pz] : [-1.65 * txTankScale, 0, 1.65 * txTankScale];
      const txLvStudX = +(1.5 * txTankScale).toFixed(3);
      const txLvStudY = +(txCoverY + 0.48 + 1.55 * lvS + 0.10).toFixed(3);
      const txLvPhaseZ = autoBank ? [-pz, 0, pz, pz + 2.6] : [-1.8 * txTankScale, -0.6 * txTankScale, 0.6 * txTankScale, 1.8 * txTankScale];
      const gantryWireY = +(7.6 + 2.0 * (s - 1.0) + 3.55).toFixed(3);
      return {
        vSpec, s, lvS, lvSp, pz, unitPz,
        distS: 1.0,
        distSp: 1.65,
        distKv: 13.8,
        quadBundle: !!vSpec.quadBundle,
        bundleHv: vSpec.quadBundle ? 'quad' : !!vSpec.twinBundle,
        gantryWireY,
        gantryStrainY: +(gantryWireY - 0.35).toFixed(3),
        laTopY, ctTopY, dsTermY, cbTermY, cbTermOffsetX, busY,
        txTankScale, txCoverY, autoBank,
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
    function tagSubpartHierarchy(obj, subpartId, preserveExisting = false) {
      if (!obj) return;
      if (!preserveExisting || !obj.userData.subpartId) {
        obj.userData.subpartId = subpartId;
      }
      if (obj.children) {
        obj.children.forEach(child => tagSubpartHierarchy(child, subpartId, preserveExisting));
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

    // Helper: Create a catenary overhead jumper conductor between two 3D points (supports Single, Twin, and EHV Quad-Bundle + Spacer-Dampers)
    function createCatenaryJumper(p1, p2, sag = 0.45, segments = 10, mat = MatLib.copperConductor, voltageTag = '69kV', circuitTag = 'main_path', bundleMode = false) {
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
      const isQuad = (bundleMode === 'quad' || bundleMode === 4 || (bundleMode === true && String(voltageTag).startsWith('500')));
      if (isQuad) {
        const qOff = 0.14;
        [[-qOff, -qOff], [qOff, -qOff], [-qOff, qOff], [qOff, qOff]].forEach(([dy, dz]) => {
          const offsetCurve = new THREE.CatmullRomCurve3(points.map(pt => new THREE.Vector3(pt.x, pt.y + dy, pt.z + dz)));
          const mesh = new THREE.Mesh(new THREE.TubeGeometry(offsetCurve, segments * 2, tubeRadius * 0.85, 7, false), mat);
          mesh.castShadow = true;
          group.add(mesh);
        });
        [0.22, 0.48, 0.74].forEach(st => {
          const sp = curve.getPointAt(st);
          const spFrame = new THREE.Group();
          spFrame.position.copy(sp);
          const sH1 = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.03, qOff * 2.1), MatLib.aluminumBus); sH1.position.y = qOff;
          const sH2 = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.03, qOff * 2.1), MatLib.aluminumBus); sH2.position.y = -qOff;
          const sV1 = new THREE.Mesh(new THREE.BoxGeometry(0.035, qOff * 2.1, 0.03), MatLib.aluminumBus); sV1.position.z = qOff;
          const sV2 = new THREE.Mesh(new THREE.BoxGeometry(0.035, qOff * 2.1, 0.03), MatLib.aluminumBus); sV2.position.z = -qOff;
          spFrame.add(sH1, sH2, sV1, sV2);
          group.add(spFrame);
        });
      } else if (bundleMode) {
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

    // Helper: Create a rigid tubular bus or enclosed GIS duct between two 3D points (supports Single, Twin, Quad)
    function createRigidBusSegment(p1, p2, radius = 0.055, mat = MatLib.aluminumBus, voltageTag = '69kV', circuitTag = 'main_path', bundleMode = false) {
      const dist = Math.max(0.01, p1.distanceTo(p2));
      const curve = new THREE.LineCurve3(p1.clone(), p2.clone());
      const isQuad = (bundleMode === 'quad' || bundleMode === 4 || (bundleMode === true && String(voltageTag).startsWith('500')));
      if (isQuad) {
        const grp = new THREE.Group();
        const dir = p2.clone().sub(p1).normalize();
        const lat = new THREE.Vector3(-dir.z, 0, dir.x);
        if (lat.lengthSq() < 0.001) lat.set(0, 0, 1);
        lat.normalize();
        const up = new THREE.Vector3(0, 1, 0);
        const qOff = 0.13;
        [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sL, sU]) => {
          const seg = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.72, radius * 0.72, dist, 10), mat);
          seg.position.copy(p1).add(p2).multiplyScalar(0.5).addScaledVector(lat, sL * qOff).addScaledVector(up, sU * qOff);
          seg.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
          seg.castShadow = true;
          grp.add(seg);
        });
        [0.25, 0.5, 0.75].forEach(st => {
          const sp = new THREE.Mesh(new THREE.BoxGeometry(0.05, qOff * 2.2, qOff * 2.2), MatLib.aluminumBus);
          sp.position.copy(p1).lerp(p2, st);
          grp.add(sp);
        });
        grp.userData.flowCurve = curve;
        grp.userData.voltageTag = voltageTag;
        grp.userData.circuitTag = circuitTag;
        return grp;
      }
      if (bundleMode) {
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
      const isLiveTank = !!vSpec.liveTankMultiChamber;
      const bHeight = isLiveTank ? +(2.20 * s).toFixed(3) : +(1.75 * s).toFixed(3);
      const padLen = pzStep * 2 + (isLiveTank ? 2.8 : 1.6);
      const vTag = vSpec.hvKv + 'kV';

      const pad = new THREE.Mesh(new THREE.BoxGeometry(isLiveTank ? 4.6 : 3.2, 0.26, padLen), MatLib.concrete);
      pad.position.set(0, 0.13, 0);
      pad.receiveShadow = true;
      group.add(pad);

      const phaseOffsets = [-pzStep, 0, pzStep];
      if (isLiveTank) {
        const padX = +(2.15 + 0.35 * s).toFixed(3);
        const padY = +(2.25 + bHeight).toFixed(3);
        const chLen = +(padX * 0.44).toFixed(3);
        phaseOffsets.forEach((pz, idx) => {
          [-0.95, 0.95].forEach(lx => {
            const leg = new THREE.Mesh(new THREE.BoxGeometry(0.16, 2.05, 0.18), MatLib.galvanizedSteel);
            leg.position.set(lx, 1.15, pz);
            leg.castShadow = true;
            group.add(leg);
          });
          const frameBeam = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.18, 0.42), MatLib.galvanizedSteel);
          frameBeam.position.set(0, 2.18, pz);
          group.add(frameBeam);

          // Tall porcelain support column carrying operating pushrod up to live T-head
          const supCol = createRibbedInsulator(bHeight - 0.16, 0.23, sheds, MatLib.porcelainBrown, true);
          supCol.position.set(0, 2.25 + (bHeight - 0.16) / 2, pz);
          group.add(supCol);

          const gearBox = new THREE.Mesh(new THREE.BoxGeometry(0.74, 0.56, 0.62), MatLib.aluminumBus);
          gearBox.position.set(0, padY, pz);
          gearBox.castShadow = true;
          group.add(gearBox);

          // 4 series horizontal SF6 interrupter chambers + parallel grading capacitors
          [-0.75 * padX, -0.25 * padX, 0.25 * padX, 0.75 * padX].forEach(chX => {
            const chCyl = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, chLen, 16), MatLib.porcelainBrown);
            chCyl.position.set(chX, padY, pz);
            chCyl.rotation.z = Math.PI / 2;
            chCyl.castShadow = true;
            const flL = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.08, 16), MatLib.darkSteel);
            flL.position.set(chX - chLen * 0.48, padY, pz);
            flL.rotation.z = Math.PI / 2;
            const flR = flL.clone();
            flR.position.x = chX + chLen * 0.48;
            const gradCap = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, chLen * 0.88, 12), MatLib.arresterPorcelainGlaze);
            gradCap.position.set(chX, padY + 0.42, pz);
            gradCap.rotation.z = Math.PI / 2;
            [-chLen * 0.42, chLen * 0.42].forEach(bx => {
              const br = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.34, 0.08), MatLib.aluminumBus);
              br.position.set(chX + bx, padY + 0.24, pz);
              group.add(br);
            });
            group.add(chCyl, flL, flR, gradCap);
          });

          const palmL = new THREE.Vector3(-padX, padY, pz);
          const palmR = new THREE.Vector3(padX, padY, pz);
          [palmL, palmR].forEach((palmPos, bIdx) => {
            const palm = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.1, 0.24), MatLib.silverContact);
            palm.position.copy(palmPos);
            tagEnergizedTerminal(palm, circuitTag, vTag);
            const pMark = createPhaseMarker(idx, 0.065, 0.12);
            pMark.position.set(palmPos.x, palmPos.y + 0.08, pz);
            const cRingOuter = createCoronaRing(0.48, 0.032);
            cRingOuter.rotation.x = 0;
            cRingOuter.rotation.z = Math.PI / 2;
            cRingOuter.position.set(palmPos.x + (bIdx === 0 ? 0.12 : -0.12), padY, pz);
            group.add(palm, pMark, cRingOuter);
          });

          const intPath = new THREE.Object3D();
          intPath.userData.flowCurve = new THREE.CatmullRomCurve3([
            palmL.clone(),
            new THREE.Vector3(-padX * 0.5, padY, pz),
            new THREE.Vector3(padX * 0.5, padY, pz),
            palmR.clone()
          ]);
          intPath.userData.voltageTag = vTag;
          intPath.userData.circuitTag = circuitTag;
          group.add(intPath);
        });

        [-0.95, 0.95].forEach(lx => {
          const tieBeam = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.16, pzStep * 2 + 0.4), MatLib.galvanizedSteel);
          tieBeam.position.set(lx, 1.05, 0);
          group.add(tieBeam);
        });
        const mechBox = new THREE.Mesh(new THREE.BoxGeometry(0.88, 1.5, 0.95), MatLib.galvanizedSteel);
        mechBox.position.set(1.45, 1.45, 0);
        const gaugeFace = new THREE.Mesh(
          new THREE.CircleGeometry(0.13, 18),
          new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('sf6') })
        );
        gaugeFace.position.set(1.9, 1.88, -0.2);
        gaugeFace.rotation.y = Math.PI / 2;
        const statusFlag = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.24, 0.28), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
        statusFlag.position.set(1.9, 1.4, 0.18);
        group.add(mechBox, gaugeFace, statusFlag);
        group.userData.statusFlag = statusFlag;
        group.userData.tag = tag;
        group.userData.termHeight = padY;
        group.userData.termOffsetX = padX;
        return group;
      }

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
    function buildSwitchyardEnvironment(scene, layout = getBusLayoutConfig('single'), opts = {}) {
      const L = layout;
      const isSubB = !!opts.isSubB;
      const envGroup = new THREE.Group();
      envGroup.name = isSubB ? 'environment_b' : 'environment';

      // Resolve world-scale East-West highway Z coordinate cleanly south of both Substations
      let subBSouthWorldZ = L.yardMaxZ || (L.yardCenterZ + L.yardL / 2);
      if (opts.subBSouthWorldZ !== undefined) {
        subBSouthWorldZ = opts.subBSouthWorldZ;
      } else if (!isSubB && typeof AppState !== 'undefined') {
        const lbPrev = getBusLayoutConfig(AppState.subBTopology || 'ring', AppState.subBEnclosure || 'ais', L.voltageClass);
        const subBZ0 = L.fdr1Z + lbPrev.fdr1Z;
        subBSouthWorldZ = subBZ0 - lbPrev.yardMinZ;
      }
      const subASouthZ = L.yardMaxZ !== undefined ? L.yardMaxZ : (L.yardCenterZ + L.yardL / 2);
      const mainRoadZ = opts.mainRoadZ !== undefined ? opts.mainRoadZ : (Math.max(subASouthZ, subBSouthWorldZ) + 15.0);
      envGroup.userData.mainRoadZ = mainRoadZ;

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
      ground.userData.noCollider = true;
      envGroup.add(ground);

      // Expanded Open-World Landscape (Sky Dome, 1600m Graded Earth, Public Highway & West HV Transmission Corridor)
      if (!isSubB) {
        const skyCnv = document.createElement('canvas');
        skyCnv.width = 4; skyCnv.height = 512;
        const sCtx = skyCnv.getContext('2d');
        const grad = sCtx.createLinearGradient(0, 0, 0, 512);
        grad.addColorStop(0.0, '#050b18');
        grad.addColorStop(0.32, '#0f1f3d');
        grad.addColorStop(0.54, '#24456e');
        grad.addColorStop(0.72, '#476b8f');
        grad.addColorStop(0.86, '#64748b');
        grad.addColorStop(1.0, '#1e293b');
        sCtx.fillStyle = grad;
        sCtx.fillRect(0, 0, 4, 512);
        const skyTex = new THREE.CanvasTexture(skyCnv);
        const skyDome = new THREE.Mesh(
          new THREE.SphereGeometry(1180, 32, 20),
          new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, depthWrite: false, fog: false })
        );
        skyDome.name = 'sky-dome';
        skyDome.position.set(320, 0, 0);
        skyDome.scale.set(1.85, 1.85, 1.85);
        skyDome.userData.noCollider = true;
        envGroup.add(skyDome);

        // Distant Horizon Ridge Band
        const horizonBand = new THREE.Mesh(
          new THREE.CylinderGeometry(1650, 1750, 52, 48, 1, true),
          new THREE.MeshBasicMaterial({ color: 0x0f172a, side: THREE.BackSide, transparent: true, opacity: 0.72, depthWrite: false })
        );
        horizonBand.position.set(320, 22, 0);
        horizonBand.userData.noCollider = true;
        envGroup.add(horizonBand);

        // 2800m x 2000m Graded Utility Corridor Terrain (covers Substation A, 140m buffers, City & Substation B)
        const outerTerrain = new THREE.Mesh(
          new THREE.PlaneGeometry(2800, 2000),
          new THREE.MeshStandardMaterial({ color: 0x1c2b22, roughness: 0.98, metalness: 0.0 })
        );
        outerTerrain.name = 'ground-plane';
        outerTerrain.rotation.x = -Math.PI / 2;
        outerTerrain.position.set(320, -0.05, 0);
        outerTerrain.receiveShadow = true;
        outerTerrain.userData.noCollider = true;
        envGroup.add(outerTerrain);

        const worldGrid = new THREE.GridHelper(2200, 88, 0x334155, 0x1e293b);
        worldGrid.name = 'world-survey-grid';
        worldGrid.position.set(320, -0.03, 0);
        worldGrid.material.transparent = true;
        worldGrid.material.opacity = 0.28;
        worldGrid.userData.noCollider = true;
        envGroup.add(worldGrid);

        // East-West Two-Lane Paved Public Access Highway
        const hwyGroup = new THREE.Group();
        hwyGroup.name = 'public-highway';
        const hwyLen = 1700;
        const hwyCX = 320;
        const hwyMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.88, metalness: 0.05 });
        const curbMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.85 });
        const asphalt = new THREE.Mesh(new THREE.BoxGeometry(hwyLen, 0.08, 9.6), hwyMat);
        asphalt.position.set(hwyCX, -0.01, mainRoadZ);
        asphalt.receiveShadow = true;
        asphalt.userData.noCollider = true;
        hwyGroup.add(asphalt);

        [-5.55, 5.55].forEach(sz => {
          const walk = new THREE.Mesh(new THREE.BoxGeometry(hwyLen, 0.14, 1.5), curbMat);
          walk.position.set(hwyCX, 0.02, mainRoadZ + sz);
          walk.receiveShadow = true;
          walk.userData.noCollider = true;
          hwyGroup.add(walk);
        });
        const whiteLineMat = new THREE.MeshBasicMaterial({ color: 0xe2e8f0 });
        [-4.1, 4.1].forEach(lz => {
          const edgeStripe = new THREE.Mesh(new THREE.BoxGeometry(hwyLen, 0.012, 0.14), whiteLineMat);
          edgeStripe.position.set(hwyCX, 0.035, mainRoadZ + lz);
          edgeStripe.userData.noCollider = true;
          hwyGroup.add(edgeStripe);
        });
        const yellowDashMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24 });
        for (let dx = -340; dx <= 1120; dx += 11) {
          const dash = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.014, 0.16), yellowDashMat);
          dash.position.set(dx, 0.036, mainRoadZ);
          dash.userData.noCollider = true;
          hwyGroup.add(dash);
        }

        // Highway Cobra-Head LED Streetlights + Green Corridor Buffer Trees
        const lampGlowMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
        const foliageMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.9 });
        const trunkMat = new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.92 });
        for (let sx = -260; sx <= 980; sx += 48) {
          const poleH = 8.4;
          const post = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.14, poleH, 8), MatLib.galvanizedSteel);
          post.position.set(sx, poleH / 2, mainRoadZ + 6.8);
          const arm = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 2.2), MatLib.galvanizedSteel);
          arm.position.set(sx, poleH - 0.15, mainRoadZ + 5.7);
          const head = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.12, 0.65), MatLib.galvanizedSteel);
          head.position.set(sx, poleH - 0.18, mainRoadZ + 4.7);
          const lens = new THREE.Mesh(new THREE.PlaneGeometry(0.34, 0.48), lampGlowMat);
          lens.rotation.x = Math.PI / 2;
          lens.position.set(sx, poleH - 0.25, mainRoadZ + 4.7);
          hwyGroup.add(post, arm, head, lens);

          // Roadside Buffer Tree South of Highway
          const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.34, 2.2, 7), trunkMat);
          trunk.position.set(sx + 16, 1.1, mainRoadZ + 12.2);
          const crown1 = new THREE.Mesh(new THREE.ConeGeometry(2.3, 4.8, 7), foliageMat);
          crown1.position.set(sx + 16, 4.2, mainRoadZ + 12.2);
          const crown2 = new THREE.Mesh(new THREE.ConeGeometry(1.7, 3.6, 7), foliageMat);
          crown2.position.set(sx + 16, 6.4, mainRoadZ + 12.2);
          hwyGroup.add(trunk, crown1, crown2);
        }
        envGroup.add(hwyGroup);

        // Western Incoming HV Lattice Transmission Corridor (3 Towers -> Direct Zero-Gap Gantry Termination)
        const T_env = getPrimaryTerminals(L);
        const gantryY = T_env.gantryWireY;
        const strainY = T_env.gantryStrainY;
        const pz = T_env.pz;
        const bundleHv = T_env.bundleHv;
        const vTag = L.vSpec.hvKv + 'kV';
        const mastZ = Math.max(5.0, pz * 1.44);
        const mastPeakY = +(gantryY + 2.6 + 1.4).toFixed(2);
        const westCorridor = new THREE.Group();
        westCorridor.name = 'west-tx-corridor';
        const buildHorizonLatticeTower = (tx, tz, topY) => {
          const tg = createLatticeMast(topY + 3.2, L.vSpec.hvKv >= 500 ? 4.4 : 3.4, L.vSpec.hvKv >= 500 ? 1.2 : 0.9);
          tg.position.set(tx, 0, tz);
          const xArm = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.52, pz * 2 + 2.8), MatLib.galvanizedSteel);
          xArm.position.set(tx, topY + 0.8, tz);
          westCorridor.add(tg, xArm);
          [-pz, 0, pz].forEach(zOff => {
            const ins = createRibbedInsulator(L.vSpec.hvKv >= 500 ? 2.4 : 1.2, 0.14, L.vSpec.hvKv >= 500 ? 14 : 7, MatLib.porcelainBrown, false);
            ins.position.set(tx, topY - (L.vSpec.hvKv >= 500 ? 0.45 : -0.1), tz + zOff);
            westCorridor.add(ins);
          });
        };
        const wT1 = L.gantryX - 54, wT2 = L.gantryX - 114, wT3 = L.gantryX - 176;
        const twWireY = +(gantryY + (L.vSpec.hvKv >= 500 ? 5.2 : 4.0)).toFixed(2);
        [wT1, wT2, wT3].forEach(tx => buildHorizonLatticeTower(tx, 0, twWireY + 0.6));
        [-pz, 0, pz].forEach(zOff => {
          westCorridor.add(createCatenaryJumper(new THREE.Vector3(wT1, twWireY, zOff), new THREE.Vector3(L.gantryX - 0.35, strainY, zOff), 1.45, 12, MatLib.copperConductor, vTag, 'incoming', bundleHv));
          westCorridor.add(createCatenaryJumper(new THREE.Vector3(wT2, twWireY, zOff), new THREE.Vector3(wT1, twWireY, zOff), 1.65, 10, MatLib.copperConductor, vTag, 'incoming', bundleHv));
          westCorridor.add(createCatenaryJumper(new THREE.Vector3(wT3, twWireY, zOff), new THREE.Vector3(wT2, twWireY, zOff), 1.65, 10, MatLib.copperConductor, vTag, 'incoming', bundleHv));
          westCorridor.add(createCatenaryJumper(new THREE.Vector3(wT3 - 68, twWireY + 0.6, zOff), new THREE.Vector3(wT3, twWireY, zOff), 1.5, 8, MatLib.copperConductor, vTag, 'incoming', bundleHv));
        });
        [-mastZ, mastZ].forEach((sz, sIdx) => {
          const peakZ = sIdx === 0 ? -0.9 : 0.9;
          westCorridor.add(createCatenaryJumper(new THREE.Vector3(wT3 - 68, twWireY + 4.4, peakZ), new THREE.Vector3(wT1, twWireY + 3.8, peakZ), 1.1, 8, MatLib.galvanizedSteel, vTag, 'none'));
          westCorridor.add(createCatenaryJumper(new THREE.Vector3(wT1, twWireY + 3.8, peakZ), new THREE.Vector3(L.gantryX, mastPeakY, sz), 0.95, 8, MatLib.galvanizedSteel, vTag, 'none'));
        });
        envGroup.add(westCorridor);
      }

      // IEEE Std 80 Switchyard Ground Grid Wireframe Helper scaled to exact yard dimensions
      const gridMax = Math.max(L.yardW, L.yardL);
      const gridHelper = new THREE.GridHelper(gridMax, 36, 0x0284c7, 0x475569);
      gridHelper.scale.set(L.yardW / gridMax, 1, L.yardL / gridMax);
      gridHelper.position.set(L.yardCenterX, 0.015, L.yardCenterZ);
      envGroup.add(gridHelper);

      // Concrete equipment foundation pads scaled to active topology & enclosure
      const fdrMidX = (L.secBusX + L.fdrGantryX) / 2;
      const fdrSpanW = Math.max(7.5, L.fdrGantryX - L.secBusX - 5.2);
      const T_pads = getPrimaryTerminals(L);
      const txPadW = T_pads.autoBank ? 10.6 : 8.0;
      const txPadL = T_pads.autoBank ? +(T_pads.pz * 2 + 7.2).toFixed(1) : 14.0;
      const gantryPadL = Math.max(14.0, +(T_pads.pz * 2 + 5.2).toFixed(1));
      const pads = [
        { x: L.gantryX, z: 0, w: 6.5, l: gantryPadL, h: 0.35, desc: 'Gantry Pad' },
        { x: L.txX, z: L.txZ, w: txPadW, l: txPadL, h: 0.45, desc: 'Transformer Main Pad & Oil Retention Pit' },
        { x: L.secArresterX, z: 0, w: 3.4, l: Math.max(8.5, T_pads.lvSp * 2 + 3.2), h: 0.28, desc: 'Secondary Arrester/CT/89-LV Pad' },
        { x: L.secCbX, z: 0, w: 4.0, l: Math.max(8.5, T_pads.lvSp * 2 + 3.2), h: 0.32, desc: 'Main Secondary CB 52-LV Pad' },
        { x: L.capX, z: L.capZ, w: 4.8, l: 5.2, h: 0.28, desc: 'Shunt Capacitor Bank Pad' },
        { x: fdrMidX, z: L.fdr1Z, w: fdrSpanW, l: Math.max(5.5, T_pads.lvSp * 2 + 2.2), h: 0.28, desc: 'Feeder 01 Bay (52-F1) Pad' },
        { x: fdrMidX, z: L.fdr2Z, w: fdrSpanW, l: Math.max(5.5, T_pads.lvSp * 2 + 2.2), h: 0.28, desc: 'Feeder 02 Bay (52-F2) Pad' },
        { x: L.fdrGantryX, z: (L.fdr1Z + L.fdr2Z) / 2, w: 4.5, l: Math.max(21.0, Math.abs(L.fdr2Z - L.fdr1Z) + T_pads.lvSp * 2 + 4.5), h: 0.32, desc: 'Outgoing Feeder Gantry Pad' },
        { x: L.ctrlX, z: L.ctrlZ, w: 10.2, l: 12.8, h: 0.4, desc: 'Control House Pad' },
        { x: L.sstX, z: L.sstZ, w: 4.8, l: 5.0, h: 0.38, desc: 'Station Service Transformer SST-100 Pad' }
      ];

      if (L.enclosure === 'gis') {
        pads.push({ x: L.gisX, z: 0, w: L.gisW + 0.8, l: L.gisL + 0.8, h: 0.35, desc: 'SF6 GIS Hall Foundation Pad' });
      } else {
        const bayPadL = Math.max(10.5, +(T_pads.pz * 2 + 3.5).toFixed(1));
        pads.push(
          { x: L.laX, z: 0, w: 3.0, l: bayPadL, h: 0.3, desc: 'Surge Arrester Pad' },
          { x: L.ctX, z: 0, w: 3.0, l: bayPadL, h: 0.3, desc: 'CT/VT Metering Pad' },
          { x: L.dsX, z: L.dsZ, w: 4.0, l: bayPadL, h: 0.3, desc: 'Line Disconnect Switch Pad' }
        );
        if (L.scheme === 'single') {
          pads.push({ x: L.cbX, z: 0, w: 4.5, l: bayPadL, h: 0.35, desc: 'Main Breaker 52 Pad' });
        } else if (L.scheme === 'maintransfer') {
          pads.push({ x: L.cbX, z: 0, w: 4.5, l: bayPadL, h: 0.35, desc: 'Main Breaker 52 Pad' });
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
      const bW = T_pads.autoBank ? 11.4 : 8.8, bL = T_pads.autoBank ? +(T_pads.pz * 2 + 8.0).toFixed(1) : 14.8;

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

      // PERIMETER 3.0 m PRECAST CONCRETE SECURITY WALL WITH PILASTERS, COPING CAP & RAZOR/BARBED WIRE
      const perimWallH = 3.0;
      const precastMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.88, metalness: 0.08 });
      const copingMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.78, metalness: 0.1 });
      const razorMat = new THREE.MeshStandardMaterial({ color: 0xd1d5db, roughness: 0.35, metalness: 0.88 });

      const minX = L.yardCenterX - L.yardW / 2;
      const maxX = L.yardCenterX + L.yardW / 2;
      const minZ = L.yardCenterZ - L.yardL / 2;
      const maxZ = L.yardCenterZ + L.yardL / 2;

      const gateX = Math.max(minX + 8.0, Math.min(maxX - 8.0, L.txX - 7.5));
      const gateZ = isSubB ? minZ : maxZ;
      const gateGapMinX = isSubB ? (gateX - 3.6) : (gateX - 5.0);
      const gateGapMaxX = isSubB ? (gateX + 5.0) : (gateX + 3.6);
      const leftWallW = Math.max(1.0, gateGapMinX - minX);
      const rightWallW = Math.max(1.0, maxX - gateGapMaxX);

      const perimeterWallGroup = new THREE.Group();
      perimeterWallGroup.name = 'perimeter-wall';
      perimeterWallGroup.userData.normalHeight = perimWallH;

      const addWallSpan = (len, cx, cz, rotY, outSign) => {
        const spanGrp = new THREE.Group();
        spanGrp.position.set(cx, 0, cz);
        spanGrp.rotation.y = rotY;
        const panel = new THREE.Mesh(new THREE.BoxGeometry(len, perimWallH, 0.28), precastMat);
        panel.position.y = perimWallH / 2;
        panel.castShadow = true;
        panel.receiveShadow = true;
        const coping = new THREE.Mesh(new THREE.BoxGeometry(len + 0.06, 0.14, 0.38), copingMat);
        coping.position.y = perimWallH + 0.07;
        spanGrp.add(panel, coping);
        // Pilasters every 6.5 m + end pilasters
        const pilCount = Math.max(2, Math.round(len / 6.5) + 1);
        for (let pi = 0; pi < pilCount; pi++) {
          const px = -len / 2 + (len * pi) / Math.max(1, pilCount - 1);
          const pilaster = new THREE.Mesh(new THREE.BoxGeometry(0.42, perimWallH + 0.16, 0.44), precastMat);
          pilaster.position.set(px, (perimWallH + 0.16) / 2, 0);
          pilaster.castShadow = true;
          const arm = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.56, 0.06), MatLib.galvanizedSteel);
          arm.position.set(px, perimWallH + 0.34, outSign * 0.16);
          arm.rotation.x = outSign * 0.68;
          spanGrp.add(pilaster, arm);
        }
        // 3 tensioned barbed-wire strands + concertina razor-wire helix rings atop wall
        [3.24, 3.38, 3.52].forEach((by, bIdx) => {
          const strand = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, len, 4), razorMat);
          strand.rotation.z = Math.PI / 2;
          strand.position.set(0, by, outSign * (0.14 + bIdx * 0.09));
          spanGrp.add(strand);
        });
        const ringStep = 2.4;
        for (let rx = -len / 2 + 1.0; rx <= len / 2 - 1.0; rx += ringStep) {
          const coil = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.014, 6, 12), razorMat);
          coil.position.set(rx, perimWallH + 0.32, outSign * 0.18);
          coil.rotation.y = Math.PI * 0.35;
          spanGrp.add(coil);
        }
        perimeterWallGroup.add(spanGrp);
      };

      const backWallZ = isSubB ? maxZ : minZ;
      addWallSpan(L.yardW, L.yardCenterX, backWallZ, 0, isSubB ? 1 : -1);
      addWallSpan(leftWallW, minX + leftWallW / 2, gateZ, 0, isSubB ? -1 : 1);
      addWallSpan(rightWallW, gateGapMaxX + rightWallW / 2, gateZ, 0, isSubB ? -1 : 1);
      addWallSpan(L.yardL, minX, L.yardCenterZ, Math.PI / 2, -1);
      addWallSpan(L.yardL, maxX, L.yardCenterZ, Math.PI / 2, 1);

      if (typeof AppState !== 'undefined' && AppState.wallCutawayActive) {
        perimeterWallGroup.scale.y = 0.30;
      }
      envGroup.add(perimeterWallGroup);
      envGroup.userData.perimeterWallGroup = perimeterWallGroup;

      // Keep SST-100 steel mesh material solely for inner SST-100 grille reference if needed cleanly
      const gateSteelMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.45, metalness: 0.72 });

      // High-Voltage Hazard Signs mounted flush on Exterior Concrete Security Wall Faces
      const signTex = TextureGen.createHazardSignTexture();
      signTex.needsUpdate = true;
      const signMat = new THREE.MeshBasicMaterial({ map: signTex, side: THREE.DoubleSide });
      const signGeo = new THREE.PlaneGeometry(1.45, 0.72);

      const signLocations = [
        { x: L.yardCenterX - L.yardW * 0.25, y: 1.55, z: (isSubB ? maxZ + 0.16 : minZ - 0.16), ry: (isSubB ? 0 : Math.PI) },
        { x: L.yardCenterX + L.yardW * 0.25, y: 1.55, z: (isSubB ? maxZ + 0.16 : minZ - 0.16), ry: (isSubB ? 0 : Math.PI) },
        { x: maxX + 0.16, y: 1.55, z: L.yardCenterZ, ry: Math.PI / 2 },
        { x: minX - 0.16, y: 1.55, z: L.yardCenterZ, ry: -Math.PI / 2 },
        { x: L.sstX - 2.84, y: 1.4, z: L.sstZ, ry: -Math.PI / 2 }
      ];

      signLocations.forEach(s => {
        const sign = new THREE.Mesh(signGeo, signMat);
        sign.position.set(s.x, s.y, s.z);
        sign.rotation.y = s.ry;
        envGroup.add(sign);
      });

      // FUNCTIONAL PERIMETER ENTRANCE DRIVEWAY GATE & SECURITY GUARDHOUSE (substation_gate)
      const gateAction = isSubB ? 'toggleGateB' : 'toggleGateA';
      const gateGroup = new THREE.Group();
      gateGroup.name = 'substation_gate';
      gateGroup.position.set(gateX, 0, gateZ);
      gateGroup.rotation.y = isSubB ? Math.PI : 0; // Local +Z always faces exterior public highway
      gateGroup.userData = {
        componentId: 'substation_gate',
        action: gateAction,
        isSubB,
        subparts: {}
      };

      const buildGateLeaf = (leafW, isRight) => {
        const pivot = new THREE.Group();
        const leafDir = isRight ? -1 : 1;
        pivot.position.set(isRight ? 3.6 : -3.6, 0, 0);
        const cx = leafDir * (leafW / 2);
        const h = 2.85;
        const tubeMat = MatLib.galvanizedSteel;
        const topRail = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.038, leafW, 8), tubeMat);
        topRail.rotation.z = Math.PI / 2; topRail.position.set(cx, h, 0);
        const midRail = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, leafW, 8), tubeMat);
        midRail.rotation.z = Math.PI / 2; midRail.position.set(cx, h * 0.52, 0);
        const botRail = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, leafW, 8), tubeMat);
        botRail.rotation.z = Math.PI / 2; botRail.position.set(cx, 0.14, 0);
        const hingeStile = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.042, h + 0.12, 8), tubeMat);
        hingeStile.position.set(leafDir * 0.04, h / 2, 0);
        const latchStile = new THREE.Mesh(new THREE.CylinderGeometry(0.036, 0.036, h + 0.12, 8), tubeMat);
        latchStile.position.set(leafDir * (leafW - 0.04), h / 2, 0);
        // Heavy vertical security pickets + yellow crash stripe
        for (let px = -leafW * 0.42; px <= leafW * 0.42; px += 0.35) {
          const picket = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, h - 0.18, 6), gateSteelMat);
          picket.position.set(cx + px, h / 2 + 0.04, 0);
          pivot.add(picket);
        }
        const crashBar = new THREE.Mesh(new THREE.BoxGeometry(leafW - 0.12, 0.12, 0.07), MatLib.yellowHighlight);
        crashBar.position.set(cx, 1.05, 0);
        const signLeaf = new THREE.Mesh(new THREE.PlaneGeometry(1.25, 0.6), signMat);
        signLeaf.position.set(cx, 1.85, 0.055);
        // 3 barbed strands + razor trim atop gate leaf frame
        [2.98, 3.12, 3.26].forEach(by => {
          const bw = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, leafW, 4), razorMat);
          bw.rotation.z = Math.PI / 2; bw.position.set(cx, by, 0.08);
          pivot.add(bw);
        });
        pivot.add(topRail, midRail, botRail, hingeStile, latchStile, crashBar, signLeaf);
        return pivot;
      };

      const gateLeavesSub = new THREE.Group();
      const leafL = buildGateLeaf(3.55, false);
      const leafR = buildGateLeaf(3.55, true);
      // Pedestrian man-gate (-5.0 to -3.85)
      const manPivot = new THREE.Group();
      manPivot.position.set(-4.95, 0, 0);
      const mFrame = new THREE.Mesh(new THREE.BoxGeometry(1.1, 2.7, 0.05), gateSteelMat);
      mFrame.position.set(0.55, 1.4, 0);
      const mTop = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 1.12, 8), MatLib.galvanizedSteel);
      mTop.rotation.z = Math.PI / 2; mTop.position.set(0.55, 2.75, 0);
      const mPushBar = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.08, 0.08), new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.4 }));
      mPushBar.position.set(0.55, 1.0, -0.06);
      manPivot.add(mFrame, mTop, mPushBar);
      gateLeavesSub.add(leafL, leafR, manPivot);
      gateGroup.userData.leafL = leafL;
      gateGroup.userData.leafR = leafR;
      gateGroup.userData.manLeaf = manPivot;

      const gatePostsSub = new THREE.Group();
      [-5.02, -3.72, 3.72].forEach(px => {
        const pilPost = new THREE.Mesh(new THREE.BoxGeometry(0.46, 3.16, 0.46), precastMat);
        pilPost.position.set(px, 1.58, 0);
        pilPost.castShadow = true;
        const cap = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.14, 0.56), copingMat);
        cap.position.set(px, 3.22, 0);
        // 45 deg outward barbed/razor outrigger arm
        const arm = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.52, 0.06), MatLib.galvanizedSteel);
        arm.position.set(px, 3.36, 0.16);
        arm.rotation.x = 0.68;
        gatePostsSub.add(pilPost, cap, arm);
      });
      // Fixed overhead beacon & danger signs
      const beaconMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
      const beaconPostL = new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 8), beaconMat);
      beaconPostL.position.set(-3.72, 3.45, 0.22);
      const beaconPostR = new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 8), beaconMat);
      beaconPostR.position.set(3.72, 3.45, 0.22);
      const extDangerSign = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 0.72), signMat);
      extDangerSign.position.set(-4.35, 1.85, 0.08);
      gatePostsSub.add(beaconPostL, beaconPostR, extDangerSign);

      // Guardhouse Booth & Card-Reader Entry Bollard
      const gateGuardSub = new THREE.Group();
      const gCurb = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.22, 2.5), MatLib.concrete);
      gCurb.position.set(-5.6, 0.11, 2.5);
      const gBooth = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2.45, 2.1), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55, metalness: 0.25 }));
      gBooth.position.set(-5.6, 1.44, 2.5);
      gBooth.castShadow = true;
      const gGlassMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0ea5e9, emissiveIntensity: 0.25, roughness: 0.2, metalness: 0.1 });
      const gWinDrive = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 0.95), gGlassMat);
      gWinDrive.scale.x = 24;
      gWinDrive.rotation.y = Math.PI / 2;
      gWinDrive.position.set(-4.48, 1.65, 2.5);
      const gWinFront = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.95), gGlassMat);
      gWinFront.position.set(-5.6, 1.65, 3.57);
      const gRoof = new THREE.Mesh(new THREE.BoxGeometry(2.85, 0.16, 2.75), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.45 }));
      gRoof.position.set(-5.45, 2.74, 2.5);
      // Yellow card-reader entry pedestal
      const rfidPed = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.095, 1.35, 8), new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.4 }));
      rfidPed.position.set(-4.1, 0.675, 4.35);
      const rfidHead = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.34, 0.18), MatLib.relayPanelSteel);
      rfidHead.position.set(-4.1, 1.42, 4.35);
      const rfidLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.04), new THREE.MeshBasicMaterial({ color: 0x22c55e }));
      rfidLed.position.set(-3.98, 1.48, 4.35);
      gateGuardSub.userData.rfidLed = rfidLed;
      gateGuardSub.add(gCurb, gBooth, gWinDrive, gWinFront, gRoof, rfidPed, rfidHead, rfidLed);

      // Paved Heavy-Haul Driveway Apron connecting Gate seamlessly to Public Highway + Hinge Ground Braids
      const gateApronSub = new THREE.Group();
      const subBWorldSouth = opts.subBOriginZ !== undefined ? (opts.subBOriginZ - minZ) : subBSouthWorldZ;
      const apronOuterLen = Math.max(7.0, (mainRoadZ - 4.8) - (isSubB ? subBWorldSouth : maxZ));
      const totalApronLen = apronOuterLen + 2.4;
      const apronMesh = new THREE.Mesh(
        new THREE.BoxGeometry(8.2, 0.06, totalApronLen),
        new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 })
      );
      apronMesh.position.set(0, 0.025, -2.4 + totalApronLen / 2);
      apronMesh.receiveShadow = true;
      apronMesh.userData.noCollider = true;
      const stopLine = new THREE.Mesh(
        new THREE.BoxGeometry(7.2, 0.015, 0.32),
        new THREE.MeshBasicMaterial({ color: 0xf8fafc })
      );
      stopLine.position.set(0, 0.06, 4.8);
      stopLine.userData.noCollider = true;
      gateApronSub.add(apronMesh, stopLine);
      // Tinned Flexible Copper Gate Hinge Ground Braids (IEEE 80 Touch-Potential Bonding)
      [-3.65, 3.65].forEach(bx => {
        const braidPts = [
          new THREE.Vector3(bx, 0.55, 0),
          new THREE.Vector3(bx > 0 ? bx - 0.14 : bx + 0.14, 0.36, 0.12),
          new THREE.Vector3(bx > 0 ? bx + 0.12 : bx - 0.12, 0.12, 0)
        ];
        const braid = new THREE.Mesh(
          new THREE.TubeGeometry(new THREE.CatmullRomCurve3(braidPts), 6, 0.018, 6, false),
          MatLib.groundCopper
        );
        gateApronSub.add(braid);
      });

      const gateSubparts = {
        'gate-leaves': gateLeavesSub,
        'gate-posts-barbed': gatePostsSub,
        'gate-guardhouse': gateGuardSub,
        'gate-apron-ground': gateApronSub
      };
      Object.entries(gateSubparts).forEach(([id, grp]) => {
        grp.name = id;
        grp.userData.basePos = grp.position.clone();
        tagSubpartHierarchy(grp, id);
        grp.traverse(child => {
          child.userData.componentId = 'substation_gate';
          child.userData.action = gateAction;
        });
        gateGroup.add(grp);
        gateGroup.userData.subparts[id] = grp;
      });
      const gPlateCnv = document.createElement('canvas');
      gPlateCnv.width = 384; gPlateCnv.height = 84;
      const gpCtx = gPlateCnv.getContext('2d');
      gpCtx.fillStyle = 'rgba(2, 6, 23, 0.92)'; gpCtx.fillRect(4, 4, 376, 76);
      gpCtx.strokeStyle = '#fbbf24'; gpCtx.lineWidth = 4; gpCtx.strokeRect(4, 4, 376, 76);
      gpCtx.fillStyle = '#fef08a'; gpCtx.font = 'bold 26px Consolas, monospace'; gpCtx.textAlign = 'center';
      gpCtx.fillText(isSubB ? 'SUB B GATE [CLICK/E]' : 'MAIN GATE [CLICK/E]', 192, 52);
      const gatePlateSpr = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(gPlateCnv), transparent: true }));
      gatePlateSpr.position.set(0, 3.15, 0.35);
      gatePlateSpr.scale.set(4.2, 0.92, 1);
      gatePlateSpr.userData.componentId = 'substation_gate';
      gatePlateSpr.userData.action = gateAction;
      gateGroup.add(gatePlateSpr);
      envGroup.add(gateGroup);
      envGroup.userData.gateGroup = gateGroup;
      envGroup.userData.gateX = gateX;
      envGroup.userData.gateZ = gateZ;
      envGroup.userData.gateGapMinX = gateGapMinX;
      envGroup.userData.gateGapMaxX = gateGapMaxX;
      envGroup.userData.unbundled = { substation_gate: gateGroup };

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
      const strainY = T.gantryStrainY;
      const mastH = +(gantryY + 2.6).toFixed(2);
      const mastPeakY = +(mastH + 1.4).toFixed(2);
      const isEhv = vSpec.hvKv >= 500;
      const bellCount = isEhv ? 24 : (vSpec.id === '230_138' ? 14 : (vSpec.id === '138_69' ? 10 : 6));
      const strStep = isEhv ? 0.19 : 0.22;
      const strLen = +(bellCount * strStep).toFixed(3);

      const gantryGroup = new THREE.Group();
      gantryGroup.name = 'gantry';
      gantryGroup.userData = { componentId: 'gantry' };
      gantryGroup.position.set(L.gantryX, 0, 0);

      const subparts = {};

      // 1. Lattice Steel Dead-End A-Frame Structure (wide-base EHV A-frame legs at 500 kV)
      const latticeTower = new THREE.Group();
      latticeTower.name = 'gantry-lattice-tower';

      const legMat = MatLib.galvanizedSteel;
      const mastBaseW = isEhv ? 2.4 : 1.6;
      const mastTopW = isEhv ? 0.75 : 0.5;
      const leftMast = createLatticeMast(mastH, mastBaseW, mastTopW);
      leftMast.position.set(0, 0, -mastZ);
      latticeTower.add(leftMast);

      const rightMast = createLatticeMast(mastH, mastBaseW, mastTopW);
      rightMast.position.set(0, 0, mastZ);
      latticeTower.add(rightMast);

      if (isEhv) {
        [-mastZ, mastZ].forEach(z => {
          const pier = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.42, 2.8), MatLib.concrete);
          pier.position.set(0, 0.21, z);
          pier.receiveShadow = true;
          latticeTower.add(pier);
        });
      }

      const crossarm = new THREE.Mesh(
        new THREE.BoxGeometry(isEhv ? 1.65 : 1.2, isEhv ? 1.3 : 1.0, mastZ * 2 + (isEhv ? 2.8 : 2.0)),
        legMat
      );
      crossarm.position.set(0, gantryY, 0);
      crossarm.castShadow = true;
      latticeTower.add(crossarm);

      gantryGroup.add(latticeTower);
      latticeTower.userData.basePos = latticeTower.position.clone();
      subparts['gantry-lattice-tower'] = latticeTower;

      // 2. Overhead Ground Shield Wire (OHGW) Peaks & Transverse Peak Tie (no floating west stub)
      const ohgwGroup = new THREE.Group();
      ohgwGroup.name = 'gantry-ohgw-shield';
      [-mastZ, mastZ].forEach(z => {
        const peakSpike = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 2.0, 6), legMat);
        peakSpike.position.set(0, mastH + 0.5, z);
        const peakYoke = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.16, 0.18), legMat);
        peakYoke.position.set(0, mastPeakY, z);
        ohgwGroup.add(peakSpike, peakYoke);
      });
      const ohgwBridge = createCatenaryJumper(
        new THREE.Vector3(0, mastPeakY, -mastZ),
        new THREE.Vector3(0, mastPeakY, mastZ),
        0.18, 8, legMat, vTag, 'none', false
      );
      ohgwGroup.add(ohgwBridge);

      gantryGroup.add(ohgwGroup);
      ohgwGroup.userData.basePos = ohgwGroup.position.clone();
      subparts['gantry-ohgw-shield'] = ohgwGroup;

      // 3. 3-Phase Dead-End / V-String Suspension Insulators with Arcing Horns & Dual/Triple Corona Rings
      const stringsGroup = new THREE.Group();
      stringsGroup.name = 'gantry-insulator-strings';

      phaseZ.forEach(z => {
        const string = new THREE.Group();
        string.position.set(0, strainY, z);

        // Steel dead-end strain yoke plate connecting outside transmission span directly at (-0.35, strainY, z)
        const strainYoke = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.16, 0.22), legMat);
        strainYoke.position.set(-0.22, 0, 0);
        string.add(strainYoke);

        for (let i = 0; i < bellCount; i++) {
          const bell = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.08, 0.15, 12), MatLib.porcelainBrown);
          bell.position.x = i * strStep;
          bell.rotation.z = Math.PI / 2;
          bell.castShadow = true;
          string.add(bell);
        }

        // V-string upper stabilizing crossarm suspension struts for 500 kV EHV gantry
        if (isEhv) {
          [-0.85, 0.85].forEach(zTilt => {
            const vStart = new THREE.Vector3(strLen * 0.65, 0, 0);
            const vEnd = new THREE.Vector3(0, gantryY - strainY + 0.12, zTilt);
            const vVec = new THREE.Vector3().subVectors(vEnd, vStart);
            const vStrut = createRibbedInsulator(vVec.length(), 0.11, 14, MatLib.porcelainBrown, false);
            vStrut.position.copy(vStart).addScaledVector(vVec, 0.5);
            vStrut.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vVec.clone().normalize());
            string.add(vStrut);
          });
        }

        const horns = createArcingHorns(0.8 * Math.min(1.45, 0.8 + 0.2 * T.s));
        horns.position.set(strLen * 0.5, 0, 0);
        string.add(horns);

        if (vSpec.coronaRings) {
          const ring = createCoronaRing(isEhv ? 0.52 : 0.34, isEhv ? 0.036 : 0.025);
          ring.rotation.x = 0;
          ring.rotation.z = Math.PI / 2;
          ring.position.set(strLen - 0.1, 0, 0);
          string.add(ring);
          if (isEhv) {
            const ring2 = createCoronaRing(0.42, 0.028);
            ring2.rotation.x = 0;
            ring2.rotation.z = Math.PI / 2;
            ring2.position.set(strLen - 0.34, 0, 0);
            const deadEndRing = createCoronaRing(0.44, 0.03);
            deadEndRing.rotation.x = 0;
            deadEndRing.rotation.z = Math.PI / 2;
            deadEndRing.position.set(-0.22, 0, 0);
            string.add(ring2, deadEndRing);
          }
        }

        stringsGroup.add(string);
      });

      gantryGroup.add(stringsGroup);
      stringsGroup.userData.basePos = stringsGroup.position.clone();
      subparts['gantry-insulator-strings'] = stringsGroup;

      // 4. ACSR Dead-End Compression Jumper + Continuous Curved Dropper (zero-gap splice to westCorridor / eT1)
      const acsrGroup = new THREE.Group();
      acsrGroup.name = 'gantry-acsr-conductors';
      const pipeStartX = Math.max(2.1, strLen + 0.65);
      const busEndX = Math.max(pipeStartX + 1.8, (L.laX - L.gantryX) + 0.15);
      phaseZ.forEach((z, idx) => {
        const spanEnd = new THREE.Vector3(-0.35, strainY, z);
        const tensionClamp = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.42, 10), MatLib.aluminumBus);
        tensionClamp.position.copy(spanEnd);
        tensionClamp.rotation.z = Math.PI / 2;
        tagEnergizedTerminal(tensionClamp, 'incoming', vTag);
        acsrGroup.add(tensionClamp);

        const deadEndLoop = createCatenaryJumper(spanEnd, new THREE.Vector3(pipeStartX, strainY, z), 0.72, 10, MatLib.copperConductor, vTag, 'incoming', T.bundleHv);
        acsrGroup.add(deadEndLoop);

        const dropStart = new THREE.Vector3(pipeStartX, strainY, z);
        const dropEnd = new THREE.Vector3(pipeStartX, T.busY, z);
        const dropper = createCatenaryJumper(dropStart, dropEnd, 0.14, 8, MatLib.aluminumBus, vTag, 'incoming', T.bundleHv);
        acsrGroup.add(dropper);

        const pMark = createPhaseMarker(idx, 0.06, 0.16);
        pMark.position.copy(dropEnd);
        tagEnergizedTerminal(pMark, 'incoming', vTag);
        acsrGroup.add(pMark);
      });

      gantryGroup.add(acsrGroup);
      acsrGroup.userData.basePos = acsrGroup.position.clone();
      subparts['gantry-acsr-conductors'] = acsrGroup;

      // 5. Stockbridge Aeolian Vibration Dampers mounted right on the dead-end clamp transition
      const damperGroup = new THREE.Group();
      damperGroup.name = 'gantry-dampers';
      phaseZ.forEach(z => {
        const d = new THREE.Group();
        d.position.set(-0.52, strainY + 0.03, z);
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
          0.045, MatLib.aluminumBus, vTag, 'incoming', T.bundleHv
        );
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

      // 2. Electrostatic Double/Triple-Toroid Corona / Grading Rings
      const ringGroup = new THREE.Group();
      ringGroup.name = 'la-grading-ring';
      const ringY = 2.58 + colH - 0.15;
      const ringR = 0.46 * Math.min(1.65, 0.85 + 0.22 * s);
      phaseZ.forEach(z => {
        const ring = createCoronaRing(ringR, 0.034);
        ring.position.set(0, ringY, z);
        const innerRing = createCoronaRing(ringR * 0.72, 0.024);
        innerRing.position.set(0, ringY + 0.15, z);
        if (vSpec.hvKv >= 500) {
          const midRing = createCoronaRing(ringR * 0.92, 0.03);
          midRing.position.set(0, ringY - 0.45, z);
          const lowRing = createCoronaRing(ringR * 0.78, 0.024);
          lowRing.position.set(0, 2.58 + colH * 0.68, z);
          ringGroup.add(midRing, lowRing);
        }
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

      // 5. Wet-Process Dark Glazed Porcelain Weather Sheds & Metallic Intermediate Coupling Flanges
      const shedsGroup = new THREE.Group();
      shedsGroup.name = 'la-polymer-sheds';
      phaseZ.forEach(z => {
        const sheds = createRibbedInsulator(colH, 0.22, shedsCount, MatLib.arresterPorcelainGlaze, true);
        sheds.position.set(0, 2.58 + colH / 2, z);
        shedsGroup.add(sheds);

        // Two intermediate heavy metallic unit coupling flanges + insulated base standoff block
        [0.34, 0.68].forEach(frac => {
          const midFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.245, 0.245, 0.065, 18), MatLib.galvanizedSteel);
          midFlange.position.set(0, 2.58 + colH * frac, z);
          shedsGroup.add(midFlange);
        });
        const baseIsolator = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.20, 0.14, 16), MatLib.porcelainBrown);
        baseIsolator.position.set(0, 2.50, z);
        shedsGroup.add(baseIsolator);
      });
      arresterGroup.add(shedsGroup);
      shedsGroup.userData.basePos = shedsGroup.position.clone();
      subparts['la-polymer-sheds'] = shedsGroup;

      // 6. Eye-Level Digital Surge Counters, Milliammeters & High-Visibility Insulated Ground Discharge Leads
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
        const strapTop = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.12, 10), MatLib.insulatedGroundLead);
        strapTop.position.set(0.32, 2.24, z);
        strapTop.rotation.z = Math.PI / 4;
        const gWire = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.4, 10), MatLib.insulatedGroundLead);
        gWire.position.set(0.52, 0.7, z);
        const topLug = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.08), MatLib.brassContact);
        topLug.position.set(0.52, 1.75, z);
        countGroup.add(box, bezel, meter, strapTop, gWire, topLug);
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

    // BUILDER 6: HV SF6 CIRCUIT BREAKER (Dead-Tank or 500 kV Live-Tank Multi-Chamber SF6)
    function buildCircuitBreaker(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const pz = T.pz;
      const phaseZ = [-pz, 0, pz];
      const isLiveTank = !!vSpec.liveTankMultiChamber;
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

      if (isLiveTank) {
        const chCenters = [-0.75 * padX, -0.25 * padX, 0.25 * padX, 0.75 * padX];
        const chLen = +(padX * 0.44).toFixed(3);
        const colH = +(padY - 2.35).toFixed(3);

        // Steel lattice pedestal support frame for 500 kV Live-Tank poles
        const portalFrame = new THREE.Group();
        phaseZ.forEach(z => {
          [-1.05, 1.05].forEach(lx => {
            const post = new THREE.Mesh(new THREE.BoxGeometry(0.18, 2.25, 0.2), MatLib.galvanizedSteel);
            post.position.set(lx, 1.125, z);
            post.castShadow = true;
            portalFrame.add(post);
          });
          const crossCradle = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.2, 0.46), MatLib.galvanizedSteel);
          crossCradle.position.set(0, 2.22, z);
          portalFrame.add(crossCradle);
        });
        [-1.05, 1.05].forEach(lx => {
          const longBeam = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.2, pz * 2 + 0.8), MatLib.galvanizedSteel);
          longBeam.position.set(lx, 1.05, 0);
          portalFrame.add(longBeam);
        });
        cbGroup.add(portalFrame);

        // 1. Live-Tank T-Head Gearboxes & Outer 4-Chamber Pressurized Housings
        const tankGroup = new THREE.Group();
        tankGroup.name = 'cb-tank';
        phaseZ.forEach(z => {
          const gearHead = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.62, 0.68), MatLib.transformerTank);
          gearHead.position.set(0, padY, z);
          gearHead.castShadow = true;
          tankGroup.add(gearHead);
          chCenters.forEach(chX => {
            [-chLen * 0.47, chLen * 0.47].forEach(fx => {
              const flange = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.08, 20), MatLib.darkSteel);
              flange.position.set(chX + fx, padY, z);
              flange.rotation.z = Math.PI / 2;
              tankGroup.add(flange);
            });
          });
          const endCapL = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.14, 18), MatLib.darkSteel);
          endCapL.position.set(-padX + 0.08, padY, z);
          endCapL.rotation.z = Math.PI / 2;
          const endCapR = endCapL.clone();
          endCapR.position.x = padX - 0.08;
          tankGroup.add(endCapL, endCapR);
        });
        cbGroup.add(tankGroup);
        tankGroup.userData.basePos = tankGroup.position.clone();
        subparts['cb-tank'] = tankGroup;

        // 2. Vertical Graded Porcelain Support Columns, Line Insulation Sleeves & Corona Rings
        const bushGroup = new THREE.Group();
        bushGroup.name = 'cb-bushings';
        phaseZ.forEach(z => {
          const supCol = createRibbedInsulator(colH, 0.26, shedsCount, MatLib.porcelainBrown, true);
          supCol.position.set(0, 2.32 + colH / 2, z);
          bushGroup.add(supCol);
          [0.34, 0.68].forEach(frac => {
            const flange = new THREE.Mesh(new THREE.CylinderGeometry(0.31, 0.31, 0.07, 18), MatLib.galvanizedSteel);
            flange.position.set(0, 2.32 + colH * frac, z);
            bushGroup.add(flange);
          });
          chCenters.forEach(chX => {
            const chIns = createRibbedInsulator(chLen * 0.88, 0.22, 10, MatLib.porcelainBrown, true);
            chIns.position.set(chX, padY, z);
            chIns.rotation.z = Math.PI / 2;
            bushGroup.add(chIns);
          });
          [-1, 1].forEach(sign => {
            const cRing1 = createCoronaRing(0.54, 0.036);
            cRing1.rotation.x = 0;
            cRing1.rotation.z = Math.PI / 2;
            cRing1.position.set(sign * (padX - 0.14), padY, z);
            const cRing2 = createCoronaRing(0.44, 0.028);
            cRing2.rotation.x = 0;
            cRing2.rotation.z = Math.PI / 2;
            cRing2.position.set(sign * (padX - 0.36), padY, z);
            const horns = createArcingHorns(0.95);
            horns.position.set(sign * (padX - 0.18), padY + 0.15, z);
            bushGroup.add(cRing1, cRing2, horns);
          });
        });
        cbGroup.add(bushGroup);
        bushGroup.userData.basePos = bushGroup.position.clone();
        subparts['cb-bushings'] = bushGroup;

        // 3. Silver-Plated NEMA Terminal Palm Pads & Internal Multi-Chamber Flow Spline
        const padGroup = new THREE.Group();
        padGroup.name = 'cb-terminal-pads';
        phaseZ.forEach(z => {
          [-padX, padX].forEach((x, idx) => {
            const pad = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.12, 0.28), MatLib.silverContact);
            pad.position.set(x, padY, z);
            tagEnergizedTerminal(pad, idx === 0 ? 'post_dsA' : 'post_cbMain', vTag);
            padGroup.add(pad);
          });
          const intFlow = new THREE.Object3D();
          intFlow.userData.flowCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(-padX, padY, z),
            new THREE.Vector3(-padX * 0.5, padY, z),
            new THREE.Vector3(padX * 0.5, padY, z),
            new THREE.Vector3(padX, padY, z)
          ]);
          intFlow.userData.voltageTag = vTag;
          intFlow.userData.circuitTag = 'post_cbMain';
          padGroup.add(intFlow);
        });
        cbGroup.add(padGroup);
        padGroup.userData.basePos = padGroup.position.clone();
        subparts['cb-terminal-pads'] = padGroup;

        // 4. 4 Series Live-Tank SF6 Interrupter Chambers & Voltage-Grading Capacitors
        const intGroup = new THREE.Group();
        intGroup.name = 'cb-interrupter';
        phaseZ.forEach(z => {
          chCenters.forEach(chX => {
            const chamber = new THREE.Mesh(
              new THREE.CylinderGeometry(0.28, 0.28, chLen * 0.84, 18),
              new THREE.MeshStandardMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.48, roughness: 0.2 })
            );
            chamber.position.set(chX, padY, z);
            chamber.rotation.z = Math.PI / 2;
            const gradCap = new THREE.Mesh(new THREE.CylinderGeometry(0.095, 0.095, chLen * 0.86, 12), MatLib.arresterPorcelainGlaze);
            gradCap.position.set(chX, padY + 0.46, z);
            gradCap.rotation.z = Math.PI / 2;
            [-chLen * 0.42, chLen * 0.42].forEach(bx => {
              const arm = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.4, 0.09), MatLib.aluminumBus);
              arm.position.set(chX + bx, padY + 0.24, z);
              intGroup.add(arm);
            });
            intGroup.add(chamber, gradCap);
          });
        });
        cbGroup.add(intGroup);
        intGroup.userData.basePos = intGroup.position.clone();
        subparts['cb-interrupter'] = intGroup;

        // 5. 4 Series Contact Assemblies (nested in unit groups so position.x trips all 4 cleanly)
        const contGroup = new THREE.Group();
        contGroup.name = 'cb-contacts';
        const contactsList = [];
        phaseZ.forEach(z => {
          chCenters.forEach(chX => {
            const chUnit = new THREE.Group();
            chUnit.position.set(chX, padY, z);
            const fixedCont = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.46, 12), MatLib.copperWinding);
            fixedCont.position.set(-0.35, 0, 0);
            fixedCont.rotation.z = Math.PI / 2;
            const movingCont = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.46, 12), MatLib.silverContact);
            movingCont.position.set(0.35, 0, 0);
            movingCont.rotation.z = Math.PI / 2;
            const nozzle = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.34, 16), new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.18 }));
            nozzle.position.set(0.08, 0, 0);
            nozzle.rotation.z = -Math.PI / 2;
            chUnit.add(fixedCont, movingCont, nozzle);
            contGroup.add(chUnit);
            contactsList.push({ movingCont, fixedCont, z });
          });
        });
        cbGroup.add(contGroup);
        contGroup.userData.basePos = contGroup.position.clone();
        subparts['cb-contacts'] = contGroup;
        cbGroup.userData.contactsList = contactsList;

        // 6. Spring-Hydraulic Operating Mechanism Cabinet & Vertical Pull-Rods
        const mechCabGroup = new THREE.Group();
        mechCabGroup.name = 'cb-operating-mech';
        const cabBox = new THREE.Mesh(new THREE.BoxGeometry(1.25, 1.95, 1.15), MatLib.galvanizedSteel);
        cabBox.position.set(1.52, 1.55, 0);
        const glassWindow = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.2, 0.78), MatLib.cabinetGlass);
        glassWindow.position.set(2.16, 1.6, 0);
        const springCore = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.9, 12), MatLib.yellowHighlight);
        springCore.position.set(1.96, 1.6, 0.18);
        const chargeMotor = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.36, 12), MatLib.darkSteel);
        chargeMotor.position.set(1.96, 1.2, -0.18);
        chargeMotor.rotation.z = Math.PI / 2;
        const tripCoil = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.25, 10), MatLib.hazardRed);
        tripCoil.position.set(1.98, 1.92, -0.18);
        const closeCoil = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.25, 10), MatLib.safeGreen);
        closeCoil.position.set(1.98, 1.6, -0.18);
        mechCabGroup.add(cabBox, glassWindow, springCore, chargeMotor, tripCoil, closeCoil);
        phaseZ.forEach(z => {
          const pullRod = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, colH + 0.6, 10), MatLib.galvanizedSteel);
          pullRod.position.set(0.55, 2.0 + colH * 0.5, z);
          mechCabGroup.add(pullRod);
        });
        cbGroup.add(mechCabGroup);
        mechCabGroup.userData.basePos = mechCabGroup.position.clone();
        subparts['cb-operating-mech'] = mechCabGroup;

        // 7. SF6 Gas Density / Pressure Gauge Dial
        const gaugeGroup = new THREE.Group();
        gaugeGroup.name = 'cb-gauge';
        const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.06, 20), MatLib.darkSteel);
        bezel.position.set(2.15, 2.18, -0.24);
        bezel.rotation.z = Math.PI / 2;
        const dialFace = new THREE.Mesh(
          new THREE.CircleGeometry(0.14, 24),
          new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('sf6') })
        );
        dialFace.position.set(2.185, 2.18, -0.24);
        dialFace.rotation.y = Math.PI / 2;
        const capillary = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.85, 8), MatLib.copperConductor);
        capillary.position.set(1.65, 2.18, -0.24);
        capillary.rotation.z = Math.PI / 2;
        gaugeGroup.add(bezel, dialFace, capillary);
        cbGroup.add(gaugeGroup);
        gaugeGroup.userData.basePos = gaugeGroup.position.clone();
        subparts['cb-gauge'] = gaugeGroup;

        Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
        cbGroup.userData.subparts = subparts;
        scene.add(cbGroup);
        return cbGroup;
      }

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

    // BUILDER 7: MAIN POWER TRANSFORMER (TR-01: 3-Phase Tank or 500/230 kV 3x1-Phase Autotransformer Bank)
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
      const unitTankL = T.autoBank ? +(T.pz * 0.54).toFixed(2) : +(5.6 * k).toFixed(3);
      const tankL = T.autoBank ? unitTankL : +(5.6 * k).toFixed(3);
      const bankUnitZs = T.autoBank ? T.txHvPhaseZ : [0];
      const hvBushH = +(2.65 * s).toFixed(3);
      const lvBushH = +(1.55 * lvS).toFixed(3);
      const hvTilt = Math.PI / 22;

      const txGroup = new THREE.Group();
      txGroup.name = 'transformer';
      txGroup.userData = { componentId: 'transformer' };
      txGroup.position.set(L.txX, 0, L.txZ || 0);

      const subparts = {};

      // 1. Corrugated Steel Tank(s), Fire/Blast Barrier Walls (500 kV Bank), Explosion Vent Pipe & PRD
      const tankGroup = new THREE.Group();
      tankGroup.name = 'tx-tank';
      bankUnitZs.forEach(zUnit => {
        const tankMesh = new THREE.Mesh(new THREE.BoxGeometry(tankW, tankH, tankL), MatLib.transformerTank);
        tankMesh.position.set(0, 0.2 + tankH / 2, zUnit);
        tankMesh.castShadow = true;
        tankMesh.receiveShadow = true;
        tankGroup.add(tankMesh);

        for (let y = 0.8; y <= coverY - 0.3; y += 1.35 * k) {
          const rib = new THREE.Mesh(new THREE.BoxGeometry(tankW + 0.12, 0.09, tankL + 0.12), MatLib.radiatorFin);
          rib.position.set(0, y, zUnit);
          tankGroup.add(rib);
        }
        for (let z = -tankL * 0.42; z <= tankL * 0.42; z += 0.6 * k) {
          [-(tankW / 2 + 0.04), (tankW / 2 + 0.04)].forEach(rx => {
            const vRib = new THREE.Mesh(new THREE.BoxGeometry(0.08, tankH * 0.95, 0.1), MatLib.radiatorFin);
            vRib.position.set(rx, 0.2 + tankH / 2, zUnit + z);
            tankGroup.add(vRib);
          });
        }
        for (let x = -tankW * 0.4; x <= tankW * 0.4; x += 0.68 * k) {
          [-(tankL / 2 + 0.04), (tankL / 2 + 0.04)].forEach(rz => {
            const vRibZ = new THREE.Mesh(new THREE.BoxGeometry(0.1, tankH * 0.95, 0.08), MatLib.radiatorFin);
            vRibZ.position.set(x, 0.2 + tankH / 2, zUnit + rz);
            tankGroup.add(vRibZ);
          });
        }
        const jzOff = tankL * 0.46;
        [[-(tankW / 2 + 0.02), -jzOff], [(tankW / 2 + 0.02), -jzOff], [-(tankW / 2 + 0.02), jzOff], [(tankW / 2 + 0.02), jzOff]].forEach(([jx, jz]) => {
          const jack = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.25, 0.24), MatLib.darkSteel);
          jack.position.set(jx, 0.45, zUnit + jz);
          tankGroup.add(jack);
        });

        const ventRiser = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 1.55, 16), MatLib.transformerTank);
        ventRiser.position.set(0.95 * k, coverY + 0.75, zUnit - tankL * 0.34);
        const ventBend = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.75, 16), MatLib.transformerTank);
        ventBend.position.set(1.22 * k, coverY + 1.42, zUnit - tankL * 0.34);
        ventBend.rotation.z = -Math.PI / 3;
        const prdBase = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.22, 0.28, 16), MatLib.silverContact);
        prdBase.position.set(1.2 * k, coverY + 0.14, zUnit - tankL * 0.16);
        const prdCap = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.18, 16), MatLib.hazardRed);
        prdCap.position.set(1.2 * k, coverY + 0.35, zUnit - tankL * 0.16);
        tankGroup.add(ventRiser, ventBend, prdBase, prdCap);
      });

      if (T.autoBank) {
        // Two reinforced concrete fire/blast barrier walls between the 3 single-phase autotransformer tanks
        const wallH = +(coverY + 2.4).toFixed(2);
        const wallW = +(tankW + 3.6).toFixed(2);
        [-T.pz * 0.5, T.pz * 0.5].forEach(wz => {
          const blastWall = new THREE.Mesh(new THREE.BoxGeometry(wallW, wallH, 0.46), MatLib.concrete);
          blastWall.position.set(0, wallH / 2, wz);
          blastWall.castShadow = true;
          blastWall.receiveShadow = true;
          const capCoping = new THREE.Mesh(new THREE.BoxGeometry(wallW + 0.18, 0.16, 0.62), MatLib.darkSteel);
          capCoping.position.set(0, wallH + 0.08, wz);
          tankGroup.add(blastWall, capCoping);
        });
      }

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
          const cRing = createCoronaRing(vSpec.hvKv >= 500 ? 0.58 : 0.42, vSpec.hvKv >= 500 ? 0.036 : 0.03);
          cRing.position.set(T.txHvStudX, T.txHvStudY - 0.22, z);
          hvBushGroup.add(cRing);
          if (vSpec.hvKv >= 500) {
            const cRingMid = createCoronaRing(0.48, 0.028);
            cRingMid.position.set(T.txHvStudX + 0.04, T.txHvStudY - 0.58, z);
            const cRingLow = createCoronaRing(0.40, 0.024);
            cRingLow.position.set(T.txHvStudX + 0.08, T.txHvStudY - 0.94, z);
            hvBushGroup.add(cRingMid, cRingLow);
          }
        }
      });
      txGroup.add(hvBushGroup);
      hvBushGroup.userData.basePos = hvBushGroup.position.clone();
      subparts['tx-hv-bushings'] = hvBushGroup;

      // 3. Low/Secondary-Voltage Bushings (X1, X2, X3, X0 Neutral + 13.8 kV Tertiary Delta Bus Duct on AutoBank)
      const lvBushGroup = new THREE.Group();
      lvBushGroup.name = 'tx-lv-bushings';
      const throatH = 0.52;
      if (T.autoBank) {
        bankUnitZs.forEach(zUnit => {
          const unitThroat = new THREE.Mesh(new THREE.BoxGeometry(0.95, throatH, 1.35), MatLib.transformerTank);
          unitThroat.position.set(T.txLvStudX, coverY + throatH / 2 - 0.04, zUnit);
          unitThroat.castShadow = true;
          lvBushGroup.add(unitThroat);
        });
        // Neutral X0 collector pedestal at txLvPhaseZ[3] + tie bus header
        const nZ = T.txLvPhaseZ[3];
        const nPed = new THREE.Mesh(new THREE.BoxGeometry(0.85, coverY + throatH, 0.85), MatLib.galvanizedSteel);
        nPed.position.set(T.txLvStudX, (coverY + throatH) / 2, nZ);
        lvBushGroup.add(nPed);
        // Overhead 13.8 kV Tertiary Delta Stabilizing Bus Duct tying all 3 single-phase autotransformers
        const tertY = +(coverY + 0.62).toFixed(2);
        const tertDuct = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.42, T.pz * 2 + 1.4), MatLib.aluminumBus);
        tertDuct.position.set(0.32 * k, tertY, 0);
        tertDuct.castShadow = true;
        lvBushGroup.add(tertDuct);
        bankUnitZs.forEach(zUnit => {
          const tertTap = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.68, 0.46), MatLib.transformerTank);
          tertTap.position.set(0.32 * k, coverY + 0.3, zUnit);
          lvBushGroup.add(tertTap);
        });
      } else {
        const lvThroatBox = new THREE.Mesh(new THREE.BoxGeometry(0.88, throatH, 3.35), MatLib.transformerTank);
        lvThroatBox.position.set(T.txLvStudX, coverY + throatH / 2 - 0.04, -0.32);
        lvThroatBox.castShadow = true;
        lvBushGroup.add(lvThroatBox);
      }
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
          const cRing = createCoronaRing(vSpec.lvKv >= 230 ? 0.38 : 0.32, 0.025);
          cRing.position.set(T.txLvStudX, T.txLvStudY - 0.18, z);
          lvBushGroup.add(cRing);
        }
        lvBushGroup.add(turret, bushing, cap, flag);
      });
      txGroup.add(lvBushGroup);
      lvBushGroup.userData.basePos = lvBushGroup.position.clone();
      subparts['tx-lv-bushings'] = lvBushGroup;

      // 4. Elevated Conservator Tank(s), Cantilever Brackets, Oil-Level Dial Gauge & Silica Gel Breather
      const conservGroup = new THREE.Group();
      conservGroup.name = 'tx-conservator';
      const conY = coverY + 2.25;
      bankUnitZs.forEach(zUnit => {
        const conZ = zUnit - (tankL / 2 + 0.72);
        const cLen = T.autoBank ? 3.0 * k : 3.6 * k;
        const cRad = T.autoBank ? 0.46 * k : 0.58 * k;
        const cTank = new THREE.Mesh(new THREE.CylinderGeometry(cRad, cRad, cLen, 24), MatLib.transformerTank);
        cTank.position.set(0.0, conY, conZ);
        cTank.rotation.z = Math.PI / 2;
        cTank.castShadow = true;

        [-cLen * 0.505, cLen * 0.505].forEach(ex => {
          const endCap = new THREE.Mesh(new THREE.CylinderGeometry(cRad + 0.03, cRad + 0.03, 0.07, 24), MatLib.darkSteel);
          endCap.position.set(ex, conY, conZ);
          endCap.rotation.z = Math.PI / 2;
          conservGroup.add(endCap);
        });

        [-cLen * 0.32, cLen * 0.32].forEach(bx => {
          const vertPost = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.15, 0.14), MatLib.galvanizedSteel);
          vertPost.position.set(bx, coverY + 0.95, zUnit - tankL / 2);
          const horizArm = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.14, 1.05), MatLib.galvanizedSteel);
          horizArm.position.set(bx, conY - 0.5, conZ + 0.32);
          const diagStrut = new THREE.Mesh(new THREE.BoxGeometry(0.10, 1.4, 0.10), MatLib.galvanizedSteel);
          diagStrut.position.set(bx, coverY + 1.05, conZ + 0.4);
          diagStrut.rotation.x = Math.PI / 4.2;
          conservGroup.add(vertPost, horizArm, diagStrut);
        });

        const mogFace = new THREE.Mesh(
          new THREE.CircleGeometry(0.24, 24),
          new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('oillevel') })
        );
        mogFace.position.set(-cLen * 0.515, conY, conZ);
        mogFace.rotation.y = -Math.PI / 2;

        const sightGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.72, 10), MatLib.glassBreather);
        sightGlass.position.set(0.0, conY, conZ + cRad + 0.04);
        sightGlass.rotation.z = Math.PI / 2;

        const breatherX = -(cLen * 0.5 + 0.36);
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
      });
      txGroup.add(conservGroup);
      conservGroup.userData.basePos = conservGroup.position.clone();
      subparts['tx-conservator'] = conservGroup;

      // 5. Inclined Buchholz Gas & Oil-Surge Relay Pipework
      const buchGroup = new THREE.Group();
      buchGroup.name = 'tx-buchholz';
      bankUnitZs.forEach(zUnit => {
        const conZ = zUnit - (tankL / 2 + 0.72);
        const coverRiser = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.095, 1.15, 14), MatLib.galvanizedSteel);
        coverRiser.position.set(-1.35 * k, coverY + 0.58, zUnit - tankL * 0.42);
        const riserFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.08, 14), MatLib.darkSteel);
        riserFlange.position.set(-1.35 * k, coverY + 0.04, zUnit - tankL * 0.42);

        const pPipeStart = new THREE.Vector3(-1.35 * k, coverY + 1.12, zUnit - tankL * 0.42);
        const pPipeEnd = new THREE.Vector3(0.45 * k, conY - 0.52, conZ + 0.1);
        const pipeVec = new THREE.Vector3().subVectors(pPipeEnd, pPipeStart);
        const pipeMid = new THREE.Vector3().addVectors(pPipeStart, pPipeEnd).multiplyScalar(0.5);
        const inclinedPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, pipeVec.length(), 14), MatLib.galvanizedSteel);
        inclinedPipe.position.copy(pipeMid);
        inclinedPipe.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), pipeVec.clone().normalize());

        const sumpStub = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, 0.25, 14), MatLib.galvanizedSteel);
        sumpStub.position.set(0.45 * k, conY - 0.46, conZ + 0.1);

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
      });
      txGroup.add(buchGroup);
      buchGroup.userData.basePos = buchGroup.position.clone();
      subparts['tx-buchholz'] = buchGroup;

      // 6. Stepped CRGO Laminated Silicon Steel Core (Internal 3-limb or 3x 1-Phase Wound Cores)
      const coreGroup = new THREE.Group();
      coreGroup.name = 'tx-core';
      coreGroup.position.set(0, 0.2 + tankH / 2, 0);

      if (T.autoBank) {
        bankUnitZs.forEach(zUnit => {
          const uTopYoke = new THREE.Mesh(new THREE.BoxGeometry(0.62 * k, 0.52 * k, 2.4 * k), MatLib.crgoCoreSteel);
          uTopYoke.position.set(0, 1.32 * k, zUnit);
          const uBotYoke = new THREE.Mesh(new THREE.BoxGeometry(0.62 * k, 0.52 * k, 2.4 * k), MatLib.crgoCoreSteel);
          uBotYoke.position.set(0, -1.32 * k, zUnit);
          const uLimb = new THREE.Mesh(new THREE.CylinderGeometry(0.36 * k, 0.36 * k, 2.22 * k, 16), MatLib.crgoCoreSteel);
          uLimb.position.set(0, 0, zUnit);
          coreGroup.add(uTopYoke, uBotYoke, uLimb);
        });
      } else {
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
      }
      txGroup.add(coreGroup);
      coreGroup.userData.basePos = coreGroup.position.clone();
      subparts['tx-core'] = coreGroup;

      // 7. Concentric Copper Windings + Internal HV-to-LV Magnetic Energy Flow Path
      const windGroup = new THREE.Group();
      windGroup.name = 'tx-windings';
      windGroup.position.set(0, 0.2 + tankH / 2, 0);
      const coreMidY = 0.2 + tankH / 2;
      const windZs = T.autoBank ? T.txHvPhaseZ : [-1.3 * k, 0, 1.3 * k];
      windZs.forEach((z, pIdx) => {
        const lvWind = new THREE.Mesh(new THREE.CylinderGeometry(0.45 * k, 0.45 * k, 1.82 * k, 20), MatLib.copperWinding);
        lvWind.position.set(0, 0, z);
        const hvWind = new THREE.Mesh(new THREE.CylinderGeometry(0.58 * k, 0.58 * k, 1.92 * k, 20), MatLib.copperWinding);
        hvWind.position.set(0, 0, z);
        [-0.98 * k, 0.98 * k].forEach(sy => {
          const spacer = new THREE.Mesh(new THREE.CylinderGeometry(0.62 * k, 0.62 * k, 0.06, 20), MatLib.brassContact);
          spacer.position.set(0, sy, z);
          windGroup.add(spacer);
        });
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

      // 8. On-Load Tap Changer (OLTC) Diverter Tank(s) & Motor Drive Mechanism Cabinet
      const oltcGroup = new THREE.Group();
      oltcGroup.name = 'tx-oltc';
      bankUnitZs.forEach(zUnit => {
        const oltcTank = new THREE.Mesh(new THREE.BoxGeometry(1.15, 2.45 * k, 1.45), MatLib.transformerTank);
        oltcTank.position.set(tankW / 2 + 0.35, 2.4 * k, zUnit);
        const motorCab = new THREE.Mesh(new THREE.BoxGeometry(0.55, 1.15, 0.85), MatLib.galvanizedSteel);
        motorCab.position.set(tankW / 2 + 0.55, 1.2, zUnit + 1.25);
        const driveShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.65, 8), MatLib.galvanizedSteel);
        driveShaft.position.set(tankW / 2 + 0.45, 2.25, zUnit + 0.95);
        const tapDial = new THREE.Mesh(
          new THREE.CircleGeometry(0.18, 24),
          new THREE.MeshBasicMaterial({ map: TextureGen.createGaugeDialTexture('oltc') })
        );
        tapDial.position.set(tankW / 2 + 0.84, 1.38, zUnit + 1.25);
        tapDial.rotation.y = Math.PI / 2;
        oltcGroup.add(oltcTank, motorCab, driveShaft, tapDial);
      });
      if (T.autoBank) {
        const syncShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, T.pz * 2 + 0.4, 8), MatLib.galvanizedSteel);
        syncShaft.position.set(tankW / 2 + 0.65, 2.4 * k, 0);
        syncShaft.rotation.x = Math.PI / 2;
        oltcGroup.add(syncShaft);
      }
      txGroup.add(oltcGroup);
      oltcGroup.userData.basePos = oltcGroup.position.clone();
      subparts['tx-oltc'] = oltcGroup;

      // 9. Multi-Fin Vertical Radiator Banks, Manifold Headers & ONAF Cooling Fans
      const radGroup = new THREE.Group();
      radGroup.name = 'tx-radiators';
      const radZs = T.autoBank
        ? T.txHvPhaseZ.flatMap(zu => [zu - 1.05, zu + 1.05])
        : (vSpec.id === '230_138' ? [-2.1, 0, 2.1] : [-1.55 * k, 1.55 * k]);
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
      txGroup.userData.baseNominalMva = vSpec.mva || 41.7;
      scene.add(txGroup);
      return txGroup;
    }

    // Dynamic 3D Transformer Physical Auto-Sizing Helper (scales TR-01 & TR-02 tanks/radiators to MVA slider in Mode B)
    window.scale3DTransformerToMva = function(baseMva, subBMva) {
      try {
        const applyScale = (txObj, mvaVal, defaultMva) => {
          if (!txObj || !txObj.userData) return;
          const nom = txObj.userData.baseNominalMva || defaultMva || 41.7;
          const ratio = Math.max(0.65, Math.min(2.2, Math.cbrt((mvaVal || nom) / nom)));
          const sMap = txObj.userData.subparts || {};
          ['tx-tank', 'tx-radiators', 'tx-conservator', 'tx-tapchanger'].forEach(k => {
            const sub = sMap[k];
            if (sub && sub.scale) {
              sub.scale.set(ratio, Math.min(1.35, 0.45 + 0.55 * ratio), ratio);
            }
          });
          txObj.userData.currentScaledMva = mvaVal;
        };
        if (typeof simObjects !== 'undefined' && simObjects) {
          if (simObjects.transformer) {
            const defA = (typeof getVoltageSpec === 'function' ? getVoltageSpec().mva : 41.7);
            applyScale(simObjects.transformer, baseMva, defA);
          }
          if (simObjects.distribution && simObjects.distribution.userData && simObjects.distribution.userData.subBLayout) {
            const sb = simObjects.distribution.userData.unbundled && simObjects.distribution.userData.unbundled.substation_b;
            const sbTx = sb && sb.userData && sb.userData.subparts && sb.userData.subparts['subb-xfmr'];
            if (sbTx) applyScale(sbTx, subBMva || 15, 15);
          }
        }
      } catch (e) {}
    };

    // BUILDER 8: CONFIGURABLE SWITCHYARD BUSBAR SYSTEM (Single, Main/Transfer, Ring, 1.5 Breaker)
    function buildBusbarSystem(scene, topology = 'single', enclosureType = 'ais', layout = null) {
      const L = layout || getBusLayoutConfig(topology, enclosureType);
      const T = getPrimaryTerminals(L);
      const vSpec = T.vSpec;
      const vTag = vSpec.hvKv + 'kV';
      const s = T.s;
      const pz = T.pz;
      const unitPz = T.unitPz;
      const zScale = vSpec.id === '500_230' ? 1.76 : (vSpec.id === '230_138' ? 1.44 : (vSpec.id === '138_69' ? 1.22 : 1.0));
      const twin = T.bundleHv;

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

      // 1. 100 kVA Outdoor Auxiliary Step-Down Transformer (Unbundled as Independent SST-100 Component)
      const sstGroup = new THREE.Group();
      sstGroup.name = 'sst_100';
      sstGroup.userData = { componentId: 'sst_100', subparts: {} };
      sstGroup.position.set(L.sstX, 0, L.sstZ);

      const auxTankGroup = new THREE.Group();
      auxTankGroup.name = 'sst-tank';
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
      sstGroup.add(auxTankGroup);
      auxTankGroup.userData.basePos = auxTankGroup.position.clone();
      sstGroup.userData.subparts['sst-tank'] = auxTankGroup;

      // 2. 13.8 kV Primary Bushings & Expulsion Cutout Fuses
      const auxBushGroup = new THREE.Group();
      auxBushGroup.name = 'sst-hv-fuses';
      [-0.4, 0, 0.4].forEach(x => {
        const b = createRibbedInsulator(0.65, 0.085, 5, MatLib.porcelainBrown, true);
        b.position.set(x, 1.94, 0);
        const fuseHolder = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.42, 8), MatLib.porcelainBrown);
        fuseHolder.position.set(x, 2.41, -0.15);
        fuseHolder.rotation.x = Math.PI / 5;
        auxBushGroup.add(b, fuseHolder);
      });
      sstGroup.add(auxBushGroup);
      auxBushGroup.userData.basePos = auxBushGroup.position.clone();
      sstGroup.userData.subparts['sst-hv-fuses'] = auxBushGroup;

      // 2b. Internal CRGO Laminated Core & Copper Windings (Revealed in Explode Mode)
      const sstCoreSub = new THREE.Group();
      sstCoreSub.name = 'sst-core-windings';
      const coreFrame = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.88, 0.22), MatLib.crgoCoreSteel);
      coreFrame.position.set(0, 0.92, 0);
      sstCoreSub.add(coreFrame);
      [-0.32, 0, 0.32].forEach(cx => {
        const coil = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.62, 14), MatLib.copperWinding);
        coil.position.set(cx, 0.92, 0);
        sstCoreSub.add(coil);
      });
      sstGroup.add(sstCoreSub);
      sstCoreSub.userData.basePos = sstCoreSub.position.clone();
      sstGroup.userData.subparts['sst-core-windings'] = sstCoreSub;

      // 2c. 480V Secondary Terminal Compartment
      const sstLvSub = new THREE.Group();
      sstLvSub.name = 'sst-lv-cabinet';
      const lvBox = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.65, 0.56), MatLib.galvanizedSteel);
      lvBox.position.set(0.78, 0.92, 0.15);
      const stub = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.45, 8), MatLib.galvanizedSteel);
      stub.position.set(0.78, 0.38, 0.15);
      sstLvSub.add(lvBox, stub);
      sstGroup.add(sstLvSub);
      sstLvSub.userData.basePos = sstLvSub.position.clone();
      sstGroup.userData.subparts['sst-lv-cabinet'] = sstLvSub;

      Object.entries(sstGroup.userData.subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id));
      auxGroup.add(sstGroup);
      auxGroup.userData.unbundled = { sst_100: sstGroup };
      subparts['aux-tx-tank'] = auxTankGroup;
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
      // Rigid steel 480V secondary feeder conduit exiting SST-100 West face -> underground duct -> East Wall entry into Control House 480VAC Panel
      const sstRelX = L.sstX - chShiftX;
      const sstRelZ = L.sstZ - chShiftZ;
      const eastWallEntryX = 11.2; // Control House East Wall world-local x (L.ctrlX + 4.2 -> 7.0 + 4.2 = 11.2)
      const sstConduitPts = [
        new THREE.Vector3(sstRelX - 0.72, 1.25, sstRelZ + 0.45),
        new THREE.Vector3(sstRelX - 0.72, -0.35, sstRelZ + 0.45),
        new THREE.Vector3(eastWallEntryX, -0.35, 0.45),
        new THREE.Vector3(eastWallEntryX, floorY + 0.35, 0.45),
        new THREE.Vector3(10.65, floorY + 0.35, -0.8)
      ];
      for (let i = 0; i < sstConduitPts.length - 1; i++) {
        acdcGroup.add(createRigidBusSegment(sstConduitPts[i], sstConduitPts[i + 1], 0.048, MatLib.galvanizedSteel, '480V', 'sst_tap'));
      }
      const sstJBox = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.36, 0.24), MatLib.galvanizedSteel);
      sstJBox.position.set(sstRelX - 0.72, 1.25, sstRelZ + 0.45);
      const eastWallGland = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.44, 0.38), MatLib.galvanizedSteel);
      eastWallGland.position.set(eastWallEntryX + 0.06, floorY + 0.35, 0.45);
      const floorFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.08, 12), MatLib.darkSteel);
      floorFlange.position.set(10.65, floorY + 0.04, -0.8);
      acdcGroup.add(sstJBox, eastWallGland, floorFlange);

      auxGroup.add(acdcGroup);
      acdcGroup.userData.basePos = acdcGroup.position.clone();
      subparts['aux-acdc-boards'] = acdcGroup;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id, true));
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

    function organizeMVDisconnectSubparts(discGroup, prefix) {
      const sp = {
        [`${prefix}-frame`]: new THREE.Group(),
        [`${prefix}-insulators`]: new THREE.Group(),
        [`${prefix}-blades`]: new THREE.Group(),
        [`${prefix}-linkage`]: new THREE.Group()
      };
      const bladeSet = new Set();
      (discGroup.userData.bladePairs || []).forEach(bp => {
        if (bp.blade1) bladeSet.add(bp.blade1);
        if (bp.blade2) bladeSet.add(bp.blade2);
      });
      const children = discGroup.children.slice();
      children.forEach(ch => {
        if (ch.userData && ch.userData.flowCurve) return; // Keep internal conductor flow lines pinned at group origin
        if (bladeSet.has(ch) || ch.material === MatLib.copperConductor || ch.material === MatLib.silverContact || ch.material === MatLib.phaseA || ch.material === MatLib.phaseB || ch.material === MatLib.phaseC || ch.position.y >= (discGroup.userData.termHeight - 0.14)) {
          sp[`${prefix}-blades`].add(ch);
        } else if (ch instanceof THREE.Group || ch.material === MatLib.porcelainBrown) {
          sp[`${prefix}-insulators`].add(ch);
        } else if (ch.position.y < 1.8 && Math.abs(ch.position.x) < 0.75) {
          sp[`${prefix}-frame`].add(ch);
        } else {
          sp[`${prefix}-linkage`].add(ch);
        }
      });
      Object.entries(sp).forEach(([id, grp]) => {
        grp.name = id;
        grp.userData.basePos = grp.position.clone();
        tagSubpartHierarchy(grp, id);
        discGroup.add(grp);
      });
      return sp;
    }

    function organizeMVBreakerSubparts(cbGroup, prefix, T, phaseZ) {
      const sp = {
        [`${prefix}-frame`]: new THREE.Group(),
        [`${prefix}-vacuum-bottles`]: new THREE.Group(),
        [`${prefix}-mech`]: new THREE.Group(),
        [`${prefix}-bushings`]: new THREE.Group()
      };
      const termH = cbGroup.userData.termHeight || 3.1;
      const children = cbGroup.children.slice();
      children.forEach(ch => {
        if (ch.userData && ch.userData.flowCurve) return;
        if (ch === cbGroup.userData.statusFlag || (ch.position.x < -0.55 && ch.position.y < 1.95)) {
          sp[`${prefix}-mech`].add(ch);
        } else if (ch instanceof THREE.Group || ch.material === MatLib.porcelainBrown || ch.material === MatLib.siliconePolymer || ch.material === MatLib.aluminumBus || ch.material === MatLib.phaseA || ch.material === MatLib.phaseB || ch.material === MatLib.phaseC || ch.position.y >= termH - 0.25) {
          sp[`${prefix}-bushings`].add(ch);
        } else if (ch.position.y < 1.85) {
          sp[`${prefix}-frame`].add(ch);
        } else {
          sp[`${prefix}-vacuum-bottles`].add(ch);
        }
      });
      // Add visible internal ceramic & CuCr vacuum bottles (revealed clearly in Explode mode)
      const pzs = cbGroup.userData.phaseZ || phaseZ || [-1.0, 0, 1.0];
      pzs.forEach(pz => {
        const bottle = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.42, 14), MatLib.silverContact);
        bottle.position.set(0, 2.35, pz);
        const copperCol = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 0.56, 10), MatLib.copperWinding);
        copperCol.position.set(0, 2.35, pz);
        sp[`${prefix}-vacuum-bottles`].add(bottle, copperCol);
      });
      Object.entries(sp).forEach(([id, grp]) => {
        grp.name = id;
        grp.userData.basePos = grp.position.clone();
        tagSubpartHierarchy(grp, id);
        cbGroup.add(grp);
      });
      return sp;
    }

    // BUILDER 12: SECONDARY MAIN BAY, NGR, BUSBAR, UNDERGROUND SST CONDUIT & SHUNT CAPACITOR BANK
    function buildSecondaryBay(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const lvS = T.lvS;
      const lvSp = T.lvSp;
      const vLvTag = T.vSpec.lvKv + 'kV';
      const twinLv = T.vSpec.lvKv >= 230 ? 'quad' : (T.vSpec.lvKv >= 138);
      const secZCenter = -0.6;
      const secPhaseZ = [-lvSp, 0, lvSp];
      const busBarY = +(Math.max(5.2, 4.2 + lvS * 1.15)).toFixed(3);

      const secGroup = new THREE.Group();
      secGroup.name = 'secondary';
      secGroup.userData = { componentId: 'secondary' };
      secGroup.position.set(0, 0, 0);

      const subparts = {};
      const unbundled = {};
      const txLvZ = T.txLvPhaseZ;

      // 1. Neutral Grounding Assembly (X0 -> Neutral CT 51G -> Neutral Grounding Resistor -> Ground Grid) - UNBUNDLED as ngr_01
      const ngrX = L.txX + 3.4 * T.txTankScale, ngrZ = T.autoBank ? (T.pz + 4.8) : 2.8 * T.txTankScale;
      const ngrGroup = new THREE.Group();
      ngrGroup.name = 'ngr_01';
      ngrGroup.position.set(ngrX, 0, ngrZ);
      ngrGroup.userData = { componentId: 'ngr_01', subparts: {} };

      const ngrEncSub = new THREE.Group();
      const ngrCabinet = new THREE.Mesh(new THREE.BoxGeometry(1.45, 1.1, 1.15), MatLib.galvanizedSteel);
      ngrCabinet.position.set(0, 1.85, 0);
      ngrCabinet.castShadow = true;
      for (let vy = -0.3; vy <= 0.3; vy += 0.2) {
        const louver = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.06, 0.92), MatLib.darkSteel);
        louver.position.set(0, 1.85 + vy, 0);
        ngrEncSub.add(louver);
      }
      ngrEncSub.add(ngrCabinet);

      const ngrGridSub = new THREE.Group();
      for (let gz = -0.36; gz <= 0.36; gz += 0.18) {
        const gridPlate = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.65, 0.045), MatLib.crgoCoreSteel);
        gridPlate.position.set(0, 1.82, gz);
        ngrGridSub.add(gridPlate);
      }

      const ngrCtSub = new THREE.Group();
      const ngrBush = createRibbedInsulator(0.28, 0.08, 3, MatLib.porcelainBrown, false);
      ngrBush.position.set(-0.45, 2.54, 0);
      const nctToroid = new THREE.Mesh(new THREE.TorusGeometry(0.20, 0.06, 10, 18), MatLib.darkSteel);
      nctToroid.position.set(-0.45, 2.52, 0);
      nctToroid.rotation.x = Math.PI / 2;
      ngrCtSub.add(ngrBush, nctToroid);

      const ngrGndSub = new THREE.Group();
      [[-0.55, -0.45], [0.55, -0.45], [-0.55, 0.45], [0.55, 0.45]].forEach(([dx, dz]) => {
        const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.9, 0.08), MatLib.galvanizedSteel);
        leg.position.set(dx, 0.45, dz);
        const post = createRibbedInsulator(0.42, 0.07, 4, MatLib.porcelainBrown, false);
        post.position.set(dx, 1.1, dz);
        ngrGndSub.add(leg, post);
      });
      const ngrGroundStrap = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.35, 0.12), MatLib.groundCopper);
      ngrGroundStrap.position.set(0.76, 0.68, 0);
      ngrGndSub.add(ngrGroundStrap);

      Object.entries({
        'ngr-enclosure': ngrEncSub,
        'ngr-resistor-grid': ngrGridSub,
        'ngr-ct-bushing': ngrCtSub,
        'ngr-ground-pad': ngrGndSub
      }).forEach(([id, grp]) => {
        grp.name = id;
        grp.userData.basePos = grp.position.clone();
        tagSubpartHierarchy(grp, id);
        ngrGroup.add(grp);
        ngrGroup.userData.subparts[id] = grp;
      });
      secGroup.add(createCatenaryJumper(new THREE.Vector3(L.txX + T.txLvStudX, T.txLvStudY, txLvZ[3]), new THREE.Vector3(ngrX - 0.45, 2.68, ngrZ), 0.15, 6, MatLib.copperConductor, vLvTag, 'none'));
      secGroup.add(ngrGroup);
      ngrGroup.userData.basePos = ngrGroup.position.clone();
      subparts['sec-ngr'] = ngrGroup;
      unbundled.ngr_01 = ngrGroup;

      // 2. Secondary Surge Arresters (sa_lv) & Revenue Metering CTs/VTs (ctvt_lv) - UNBUNDLED
      const arrCtGroup = new THREE.Group();
      arrCtGroup.name = 'sec-arresters-ctvt';
      const arrTopY = +(1.95 + 1.20 * lvS).toFixed(3);

      const saLvGroup = new THREE.Group();
      saLvGroup.name = 'sa_lv';
      saLvGroup.position.set(L.secArresterX - 1.2, 0, secZCenter);
      saLvGroup.userData = { componentId: 'sa_lv', subparts: {} };
      const salTermSub = new THREE.Group();
      const salCoreSub = new THREE.Group();
      const salShedSub = new THREE.Group();
      const salGndSub = new THREE.Group();

      const ctvtLvGroup = new THREE.Group();
      ctvtLvGroup.name = 'ctvt_lv';
      ctvtLvGroup.position.set(L.secArresterX, 0, secZCenter);
      ctvtLvGroup.userData = { componentId: 'ctvt_lv', subparts: {} };
      const lvctTankSub = new THREE.Group();
      const lvctCoreSub = new THREE.Group();
      const lvctBushSub = new THREE.Group();

      secPhaseZ.forEach((pOff, idx) => {
        const z = secZCenter + pOff;
        // SA-LV subparts (local around saLvGroup)
        const saCap = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.12, 12), MatLib.aluminumBus);
        saCap.position.set(0, arrTopY, pOff);
        salTermSub.add(saCap);

        const znoCol = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.95 * lvS, 12), MatLib.znoCeramic);
        znoCol.position.set(0, 1.95 + 0.60 * lvS, pOff);
        salCoreSub.add(znoCol);

        const ped = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.95, 0.12), MatLib.galvanizedSteel);
        ped.position.set(0, 0.975, pOff);
        const sa = createRibbedInsulator(1.20 * lvS, 0.12, Math.max(8, Math.round(8 * lvS)), MatLib.arresterPorcelainGlaze, true);
        sa.position.set(0, 1.95 + 0.60 * lvS, pOff);
        salShedSub.add(ped, sa);

        const gLead = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 1.85, 8), MatLib.insulatedGroundLead);
        gLead.position.set(0.14, 0.95, pOff);
        salGndSub.add(gLead);

        // CTVT-LV subparts (local around ctvtLvGroup)
        const ctPed = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.95, 0.12), MatLib.galvanizedSteel);
        ctPed.position.set(0, 0.975, pOff);
        const ctIns = createRibbedInsulator(0.75 * lvS, 0.14, 6, MatLib.porcelainBrown, true);
        ctIns.position.set(0, 1.95 + 0.375 * lvS, pOff);
        lvctTankSub.add(ctPed, ctIns);

        const ctCore = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.055, 8, 16), MatLib.crgoCoreSteel);
        ctCore.position.set(0, 1.95 + 0.95 * lvS, pOff);
        lvctCoreSub.add(ctCore);

        const ctHead = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.45 * lvS, 14), MatLib.porcelainBrown);
        ctHead.position.set(0, 1.95 + 0.975 * lvS, pOff);
        const pMark = createPhaseMarker(idx, 0.045, 0.09);
        pMark.position.set(0, arrTopY, pOff);
        tagEnergizedTerminal(pMark, 'sec_lv', vLvTag);
        lvctBushSub.add(ctHead, pMark);

        arrCtGroup.add(createCatenaryJumper(new THREE.Vector3(L.txX + T.txLvStudX, T.txLvStudY, txLvZ[idx]), new THREE.Vector3(L.secArresterX - 1.2, arrTopY, z), 0.22, 6, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
        arrCtGroup.add(createCatenaryJumper(new THREE.Vector3(L.secArresterX - 1.2, arrTopY, z), new THREE.Vector3(L.secArresterX, arrTopY, z), 0.08, 4, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
      });

      Object.entries({ 'sal-terminal': salTermSub, 'sal-zno-core': salCoreSub, 'sal-sheds': salShedSub, 'sal-ground-lead': salGndSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); saLvGroup.add(grp); saLvGroup.userData.subparts[id] = grp;
      });
      Object.entries({ 'lvct-tank': lvctTankSub, 'lvct-core': lvctCoreSub, 'lvct-bushings': lvctBushSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); ctvtLvGroup.add(grp); ctvtLvGroup.userData.subparts[id] = grp;
      });

      arrCtGroup.add(saLvGroup, ctvtLvGroup);
      secGroup.add(arrCtGroup);
      arrCtGroup.userData.basePos = arrCtGroup.position.clone();
      subparts['sec-arresters-ctvt'] = arrCtGroup;
      unbundled.sa_lv = saLvGroup;
      unbundled.ctvt_lv = ctvtLvGroup;

      // 3. Secondary Main Flanking Disconnects (ds_lv) & Main Circuit Breaker (cb_lv) - UNBUNDLED
      const lvDisc = createMVDisconnectUnit(L.secDsAX, secZCenter, false, '89-LVA', T, 'sec_lv');
      lvDisc.name = 'ds_lv';
      lvDisc.userData.componentId = 'ds_lv';
      const lvDsTermY = lvDisc.userData.termHeight;
      const lvDsOff = lvDisc.userData.termOffsetX;
      lvDisc.userData.subparts = organizeMVDisconnectSubparts(lvDisc, 'lvds');

      const lvCb = createMVBreakerUnit(L.secCbX, secZCenter, true, '52-LV', T, 'sec_lv');
      lvCb.name = 'cb_lv';
      lvCb.userData.componentId = 'cb_lv';
      const lvCbTermY = lvCb.userData.termHeight;
      const lvCbOff = lvCb.userData.termOffsetX;
      lvCb.userData.subparts = organizeMVBreakerSubparts(lvCb, 'lvcb', T, secPhaseZ);

      const lvDiscB = createMVDisconnectUnit(L.secDsBX, secZCenter, false, '89-LVB', T, 'sec_bus');
      lvDiscB.name = 'sec-lv-disconnect-b';
      lvDiscB.userData.componentId = 'ds_lv';
      lvDiscB.userData.subparts = organizeMVDisconnectSubparts(lvDiscB, 'lvds');

      secPhaseZ.forEach((pz) => {
        const z = secZCenter + pz;
        secGroup.add(createCatenaryJumper(new THREE.Vector3(L.secArresterX, arrTopY, z), new THREE.Vector3(L.secDsAX - lvDsOff, lvDsTermY, z), 0.1, 4, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
        secGroup.add(createCatenaryJumper(new THREE.Vector3(L.secDsAX + lvDsOff, lvDsTermY, z), new THREE.Vector3(L.secCbX - lvCbOff, lvCbTermY, z), 0.12, 5, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
        secGroup.add(createCatenaryJumper(new THREE.Vector3(L.secCbX + lvCbOff, lvCbTermY, z), new THREE.Vector3(L.secDsBX - lvDsOff, lvDsTermY, z), 0.12, 5, MatLib.copperConductor, vLvTag, 'sec_bus', twinLv));
      });
      secGroup.add(lvDisc, lvCb, lvDiscB);
      lvDisc.userData.basePos = lvDisc.position.clone();
      lvCb.userData.basePos = lvCb.position.clone();
      subparts['sec-lv-disconnect'] = lvDisc;
      subparts['sec-lv-breaker'] = lvCb;
      secGroup.userData.lvDisc = lvDisc;
      secGroup.userData.lvBreaker = lvCb;
      secGroup.userData.lvDiscB = lvDiscB;
      unbundled.ds_lv = lvDisc;
      unbundled.cb_lv = lvCb;

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

        // Underground Armored Cable Pothead Riser + Sub-Grade Trench Duct -> SST-100 Primary Throat (routed East of Control House)
        const phTop = new THREE.Vector3(potheadX, 2.65, tapZ + idx * 0.45);
        const phTrench = new THREE.Vector3(potheadX, -0.35, tapZ + idx * 0.45);
        const sstTurn = new THREE.Vector3(L.sstX + [-0.4, 0, 0.4][idx], -0.35, tapZ + idx * 0.45);
        const sstTrench = new THREE.Vector3(L.sstX + [-0.4, 0, 0.4][idx], -0.35, L.sstZ - 0.15);
        const sstTerm = new THREE.Vector3(L.sstX + [-0.4, 0, 0.4][idx], 2.25, L.sstZ - 0.15);
        const potStand = new THREE.Mesh(new THREE.BoxGeometry(0.14, 2.02, 0.14), MatLib.galvanizedSteel);
        potStand.position.set(phTop.x, 1.01, phTop.z);
        const potIns = createRibbedInsulator(0.65, 0.065, 5, MatLib.porcelainBrown, false);
        potIns.position.set(phTop.x, 2.35, phTop.z);
        distBusGroup.add(potStand, potIns);
        distBusGroup.add(createCatenaryJumper(new THREE.Vector3(bx, busBarY, tapZ + idx * 0.45), phTop, 0.18, 5, MatLib.copperConductor, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(phTop, phTrench, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(phTrench, sstTurn, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(sstTurn, sstTrench, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
        distBusGroup.add(createRigidBusSegment(sstTrench, sstTerm, 0.036, MatLib.galvanizedSteel, vLvTag, 'sst_tap'));
      });
      // Visible Precast Concrete Cable Trench Cover along pothead-to-SST East-of-House run
      const trenchLen = Math.max(2.0, L.sstX - potheadX + 1.2);
      const trenchCapEW = new THREE.Mesh(new THREE.BoxGeometry(trenchLen, 0.08, 0.9), MatLib.concretePad);
      trenchCapEW.position.set((potheadX + L.sstX) / 2, 0.05, tapZ + 0.45);
      const trenchNSLen = Math.max(2.0, L.sstZ - tapZ);
      const trenchCapNS = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.08, trenchNSLen), MatLib.concretePad);
      trenchCapNS.position.set(L.sstX, 0.05, (tapZ + L.sstZ) / 2);
      distBusGroup.add(trenchCapEW, trenchCapNS);

      secGroup.add(distBusGroup);
      distBusGroup.userData.basePos = distBusGroup.position.clone();
      subparts['sec-dist-bus'] = distBusGroup;

      // 5. Switched Shunt Capacitor Bank (Unbundled as cap_bank: 89-CAPA -> 52-CAP -> 89-CAPB -> Capacitor Rack)
      const capGroup = new THREE.Group();
      capGroup.name = 'sec-cap-bank';
      const capBankGroup = new THREE.Group();
      capBankGroup.name = 'cap_bank';
      capBankGroup.position.set(L.capX, 0, L.capZ);
      capBankGroup.userData = { componentId: 'cap_bank', subparts: {} };

      const capRackSub = new THREE.Group();
      const capCansSub = new THREE.Group();
      const capReactSub = new THREE.Group();
      const capSwZ = Math.min(busZMin + 1.8, L.capZ + 3.2);
      const capVcbSub = new THREE.Group();
      capVcbSub.position.set(4.4, 0, capSwZ - L.capZ);

      const rackCols = [[-1.6, -1.5], [1.6, -1.5], [-1.6, 1.5], [1.6, 1.5]];
      rackCols.forEach(([dx, dz]) => {
        const col = new THREE.Mesh(new THREE.BoxGeometry(0.1, 3.0, 0.1), MatLib.galvanizedSteel);
        col.position.set(dx, 1.5, dz);
        capRackSub.add(col);
      });
      const capTopRail = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 3.1), MatLib.galvanizedSteel);
      capTopRail.position.set(1.45, 2.95, 0);
      const capLeftRail = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 3.1), MatLib.galvanizedSteel);
      capLeftRail.position.set(-1.55, 2.95, 0);
      const capSideRailF = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.10, 0.12), MatLib.galvanizedSteel);
      capSideRailF.position.set(0, 2.95, 1.5);
      const capSideRailB = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.10, 0.12), MatLib.galvanizedSteel);
      capSideRailB.position.set(0, 2.95, -1.5);
      capRackSub.add(capTopRail, capLeftRail, capSideRailF, capSideRailB);

      const dsCapA = createMVDisconnectUnit(2.0, 0, false, '89-CAPA', T, 'cap_bank');
      const cbCap = createMVBreakerUnit(0, 0, true, '52-CAP', T, 'cap_bank');
      const dsCapB = createMVDisconnectUnit(-2.0, 0, false, '89-CAPB', T, 'cap_bank');
      capVcbSub.add(dsCapA, cbCap, dsCapB);
      secGroup.userData.capDiscA = dsCapA;
      secGroup.userData.capBreaker = cbCap;
      secGroup.userData.capDiscB = dsCapB;

      [-1.1, 0, 1.1].forEach((cz, idx) => {
        const shelf = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.09, 0.36), MatLib.galvanizedSteel);
        shelf.position.set(0, 1.85, cz);
        capRackSub.add(shelf);
        [-1.0, -0.35, 0.35, 1.0].forEach(cx => {
          const can = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.72, 0.22), MatLib.radiatorFin);
          can.position.set(cx, 2.28, cz);
          const bush = createRibbedInsulator(0.35, 0.05, 3, MatLib.porcelainBrown, false);
          bush.position.set(cx, 2.8, cz);
          capCansSub.add(can, bush);
        });
        const sw = createRibbedInsulator(0.6, 0.08, 4, MatLib.siliconePolymer, true);
        sw.position.set(1.45, 3.25, cz);
        const reactor = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.42, 12), MatLib.copperWinding);
        reactor.position.set(1.45, 3.68, cz);
        capReactSub.add(sw, reactor);

        const pOff = secPhaseZ[idx];
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.secBusX + pOff, busBarY, busZMin + 0.8 + idx * 0.35), new THREE.Vector3(L.capX + 6.4 + lvDsOff, lvDsTermY, capSwZ + pOff), 0.22, 6, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.capX + 6.4 - lvDsOff, lvDsTermY, capSwZ + pOff), new THREE.Vector3(L.capX + 4.4 + lvCbOff, lvCbTermY, capSwZ + pOff), 0.12, 5, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.capX + 4.4 - lvCbOff, lvCbTermY, capSwZ + pOff), new THREE.Vector3(L.capX + 2.4 + lvDsOff, lvDsTermY, capSwZ + pOff), 0.12, 5, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
        capGroup.add(createCatenaryJumper(new THREE.Vector3(L.capX + 2.4 - lvDsOff, lvDsTermY, capSwZ + pOff), new THREE.Vector3(L.capX + 1.45, 3.85, L.capZ + cz), 0.20, 6, MatLib.copperConductor, vLvTag, 'cap_bank', twinLv));
      });
      Object.entries({ 'cap-rack': capRackSub, 'cap-cans': capCansSub, 'cap-reactors': capReactSub, 'cap-vcb': capVcbSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); capBankGroup.add(grp); capBankGroup.userData.subparts[id] = grp;
      });
      capGroup.add(capBankGroup);
      secGroup.add(capGroup);
      capGroup.userData.basePos = capGroup.position.clone();
      subparts['sec-cap-bank'] = capGroup;
      unbundled.cap_bank = capBankGroup;

      // 6. MULTI-STAGE CASCADING STEP-DOWN STAGES (ATR-230 -> ATR-138 -> TR-69/13.8 kV) FOR 138/230/500 kV TIERS
      const distSp = T.distSp || 1.65;
      const distBusY = 5.35;
      const distBusX = L.secBusX + (T.vSpec.stageKvs && T.vSpec.stageKvs.length > 2 ? 2.4 : 0);
      if (T.vSpec.stageKvs && T.vSpec.stageKvs.length > 2) {
        const cascadeGroup = new THREE.Group();
        cascadeGroup.name = 'sec-cascade-stages';
        const stagesToRender = T.vSpec.stages.slice(1); // intermediate + final 69->13.8 kV step-down modules
        const stageZ = -6.8 * lvS;
        const stageStartX = L.txX + 4.2 * lvS;
        const stageSpacingX = Math.max(4.6, (L.secBusX - stageStartX) / Math.max(1, stagesToRender.length));

        // 13.8 kV Distribution Bus Riser at distBusX receiving final TR-01 (69/13.8 kV) output
        [-distSp, 0, distSp].forEach((pxOff, idx) => {
          const rbx = distBusX + pxOff * 0.45;
          const rTube = createRigidBusSegment(
            new THREE.Vector3(rbx, distBusY, Math.min(L.fdr1Z - 2.0, -11.5)),
            new THREE.Vector3(rbx, distBusY, Math.max(L.fdr2Z + 2.0, 9.5)),
            0.044, MatLib.aluminumBus, '13.8kV', 'sec_bus'
          );
          const pPed = new THREE.Mesh(new THREE.BoxGeometry(0.1, distBusY - 1.35, 0.1), MatLib.galvanizedSteel);
          pPed.position.set(rbx, (distBusY - 1.35) / 2, L.fdr1Z + (idx - 1) * 1.2);
          const pIns = createRibbedInsulator(1.35, 0.11, 7, MatLib.porcelainBrown, true);
          pIns.position.set(rbx, distBusY - 0.675, L.fdr1Z + (idx - 1) * 1.2);
          cascadeGroup.add(rTube, pPed, pIns);
        });

        stagesToRender.forEach((st, sIdx) => {
          const sx = stageStartX + sIdx * stageSpacingX;
          const isFinalDistStage = (st.lv <= 15);
          const stScale = st.hv >= 230 ? 1.15 : (st.hv >= 138 ? 0.96 : 0.82);
          const pad = new THREE.Mesh(new THREE.BoxGeometry(2.9 * stScale, 0.22, 3.6 * stScale), MatLib.concretePad);
          pad.position.set(sx, 0.11, stageZ);
          const tank = new THREE.Mesh(new THREE.BoxGeometry(2.1 * stScale, 2.3 * stScale, 2.5 * stScale), MatLib.transformerTank);
          tank.position.set(sx, 0.22 + 1.15 * stScale, stageZ);
          tank.castShadow = true;
          const cons = new THREE.Mesh(new THREE.CylinderGeometry(0.32 * stScale, 0.32 * stScale, 1.5 * stScale, 12), MatLib.transformerTank);
          cons.rotation.x = Math.PI / 2;
          cons.position.set(sx - 0.55 * stScale, 0.22 + 2.65 * stScale, stageZ);
          const finL = new THREE.Mesh(new THREE.BoxGeometry(0.42 * stScale, 1.7 * stScale, 2.1 * stScale), MatLib.radiatorFin);
          finL.position.set(sx - 1.25 * stScale, 0.22 + 1.05 * stScale, stageZ);
          const finR = new THREE.Mesh(new THREE.BoxGeometry(0.42 * stScale, 1.7 * stScale, 2.1 * stScale), MatLib.radiatorFin);
          finR.position.set(sx + 1.25 * stScale, 0.22 + 1.05 * stScale, stageZ);
          // Inter-stage SF6 / VCB breaker cabinet adjacent to stage tank
          const cbCab = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.85, 2.4), MatLib.galvanizedSteel);
          cbCab.position.set(sx + 2.15 * stScale, 0.925, stageZ);
          cascadeGroup.add(pad, tank, cons, finL, finR, cbCab);

          [-0.75 * stScale, 0, 0.75 * stScale].forEach((pzOff, pIdx) => {
            const bH = st.hv >= 138 ? 1.35 : 0.85;
            const bIn = createRibbedInsulator(bH, 0.11, st.hv >= 138 ? 12 : 8, MatLib.porcelainBrown, true);
            bIn.position.set(sx - 0.45 * stScale, 0.22 + 2.3 * stScale + bH / 2, stageZ + pzOff);
            const bOut = createRibbedInsulator(bH * 0.72, 0.09, 6, MatLib.porcelainGray, true);
            bOut.position.set(sx + 0.45 * stScale, 0.22 + 2.3 * stScale + (bH * 0.72) / 2, stageZ + pzOff);
            const cbP = createRibbedInsulator(0.65, 0.08, 5, MatLib.siliconePolymer, true);
            cbP.position.set(sx + 2.15 * stScale, 2.15, stageZ + pzOff);
            cascadeGroup.add(bIn, bOut, cbP);

            const inTerm = new THREE.Vector3(sx - 0.45 * stScale, 0.22 + 2.3 * stScale + bH, stageZ + pzOff);
            const outTerm = new THREE.Vector3(sx + 0.45 * stScale, 0.22 + 2.3 * stScale + bH * 0.72, stageZ + pzOff);
            const cbTerm = new THREE.Vector3(sx + 2.15 * stScale, 2.48, stageZ + pzOff);
            if (sIdx === 0) {
              const srcPt = new THREE.Vector3(L.secBusX + secPhaseZ[pIdx], busBarY, stageZ + secPhaseZ[pIdx] * 0.4);
              cascadeGroup.add(createCatenaryJumper(srcPt, inTerm, 0.3, 6, MatLib.copperConductor, vLvTag, 'sec_lv', twinLv));
            } else {
              const prevX = stageStartX + (sIdx - 1) * stageSpacingX + 2.15 * (stagesToRender[sIdx - 1].hv >= 138 ? 0.96 : 1.15);
              cascadeGroup.add(createCatenaryJumper(new THREE.Vector3(prevX, 2.48, stageZ + pzOff), inTerm, 0.25, 5, MatLib.copperConductor, st.hv + 'kV', 'sec_lv'));
            }
            cascadeGroup.add(createCatenaryJumper(outTerm, cbTerm, 0.14, 4, MatLib.copperConductor, st.lv + 'kV', isFinalDistStage ? 'sec_bus' : 'sec_lv'));
            if (isFinalDistStage) {
              const distBusPt = new THREE.Vector3(distBusX + (pIdx - 1) * distSp * 0.45, distBusY, L.fdr1Z + (pIdx - 1) * distSp * 0.5);
              cascadeGroup.add(createCatenaryJumper(cbTerm, distBusPt, 0.35, 6, MatLib.copperConductor, '13.8kV', 'sec_bus'));
            }
          });
        });

        // Floating Cascade Engineering Plaque above intermediate bays
        const cCanvas = document.createElement('canvas');
        cCanvas.width = 512; cCanvas.height = 96;
        const cCtx = cCanvas.getContext('2d');
        cCtx.fillStyle = 'rgba(2, 6, 23, 0.92)'; cCtx.fillRect(4, 4, 504, 88);
        cCtx.strokeStyle = '#38bdf8'; cCtx.lineWidth = 4; cCtx.strokeRect(4, 4, 504, 88);
        cCtx.fillStyle = '#38bdf8'; cCtx.font = 'bold 26px Consolas, monospace'; cCtx.textAlign = 'center';
        cCtx.fillText(`CASCADING STEP-DOWN: ${T.vSpec.cascadeLabel}`, 256, 56);
        const cSpr = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cCanvas), transparent: true }));
        cSpr.position.set(stageStartX + (stagesToRender.length - 1) * stageSpacingX * 0.5, 6.2, stageZ);
        cSpr.scale.set(6.8, 1.3, 1);
        cascadeGroup.add(cSpr);

        secGroup.add(cascadeGroup);
        cascadeGroup.userData.basePos = cascadeGroup.position.clone();
        subparts['sec-cascade-stages'] = cascadeGroup;
      }

      secGroup.userData.distBusX = distBusX;
      secGroup.userData.distBusY = distBusY;

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id, true));
      secGroup.userData.subparts = subparts;
      secGroup.userData.unbundled = unbundled;
      scene.add(secGroup);
      return secGroup;
    }

    // BUILDER 13: 13.8 kV OUTGOING DISTRIBUTION FEEDER BAYS (52-F1 & 52-F2) + DEDICATED 69/138 kV INDUSTRIAL BAY (52-IND)
    function buildFeederBays(scene, layout = getBusLayoutConfig('single')) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      const isCascade = !!(T.vSpec.stageKvs && T.vSpec.stageKvs.length > 2);
      const srcBusX = isCascade ? (L.secBusX + 2.4) : L.secBusX;
      const srcBusY = isCascade ? 5.35 : +(Math.max(5.2, 4.2 + T.lvS * 1.15)).toFixed(3);
      const distS = T.distS || 1.0;
      const distSp = T.distSp || 1.65;
      const vDistTag = '13.8kV';
      const distBusBarY = 5.35;
      // Local 13.8 kV terminal profile so urban feeders NEVER scale up to 138/230 kV geometry!
      const TD = Object.assign({}, T, {
        lvS: distS,
        lvSp: distSp,
        vSpec: Object.assign({}, T.vSpec, { lvKv: 13.8 })
      });

      const fdrGroup = new THREE.Group();
      fdrGroup.name = 'feeders';
      fdrGroup.userData = { componentId: 'feeders', switches: {}, unbundled: {} };

      const subparts = {};
      const fSpan = Math.max(12.0, L.fdrGantryX - srcBusX);
      const xDsA = srcBusX + fSpan * 0.22;
      const xCb = srcBusX + fSpan * 0.48;
      const xDsB = srcBusX + fSpan * 0.74;
      const xCtSa = srcBusX + fSpan * 0.89;

      function buildFeederLine(bayId, compKey, prefix, zCenter, labelA, labelCB, labelB, cTag) {
        const bayGroup = new THREE.Group();
        bayGroup.name = bayId;
        bayGroup.position.set(xCb, 0, zCenter);
        bayGroup.userData = { componentId: compKey, subparts: {} };

        const fFrameSub = new THREE.Group();
        const padFrame = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.16, distSp * 2 + 1.2), MatLib.concretePad);
        padFrame.position.set(0, 0.08, 0);
        fFrameSub.add(padFrame);

        const dsA = createMVDisconnectUnit(xDsA - xCb, 0, false, labelA, TD, cTag);
        const cb = createMVBreakerUnit(0, 0, true, labelCB, TD, cTag);
        const dsB = createMVDisconnectUnit(xDsB - xCb, 0, false, labelB, TD, cTag);

        const dsY = dsA.userData.termHeight;
        const dsO = dsA.userData.termOffsetX;
        const cbY = cb.userData.termHeight;
        const cbO = cb.userData.termOffsetX;

        const fVcbSub = new THREE.Group();
        fVcbSub.add(cb);
        const fDiscSub = new THREE.Group();
        fDiscSub.add(dsA, dsB);
        const fCtSub = new THREE.Group();
        [-distSp, 0, distSp].forEach(pz => {
          const ctRing = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.042, 8, 16), MatLib.crgoCoreSteel);
          ctRing.position.set(xDsB - xCb + 1.0, dsY - 0.18, pz);
          ctRing.rotation.x = Math.PI / 2;
          fCtSub.add(ctRing);
        });

        fdrGroup.userData.switches[labelA] = dsA;
        fdrGroup.userData.switches[labelCB] = cb;
        fdrGroup.userData.switches[labelB] = dsB;

        Object.entries({
          [`${prefix}-frame`]: fFrameSub,
          [`${prefix}-vcb`]: fVcbSub,
          [`${prefix}-disconnects`]: fDiscSub,
          [`${prefix}-relay-ct`]: fCtSub
        }).forEach(([id, grp]) => {
          grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); bayGroup.add(grp); bayGroup.userData.subparts[id] = grp;
        });

        [-distSp, 0, distSp].forEach((pz, pIdx) => {
          const z = zCenter + pz;
          const busXPt = isCascade ? (srcBusX + (pIdx - 1) * distSp * 0.45) : (L.secBusX + (pIdx - 1) * T.lvSp);
          fdrGroup.add(createCatenaryJumper(new THREE.Vector3(busXPt, srcBusY, z), new THREE.Vector3(xDsA - dsO, dsY, z), 0.25, 6, MatLib.copperConductor, vDistTag, cTag));
          fdrGroup.add(createCatenaryJumper(new THREE.Vector3(xDsA + dsO, dsY, z), new THREE.Vector3(xCb - cbO, cbY, z), 0.14, 5, MatLib.copperConductor, vDistTag, cTag));
          fdrGroup.add(createCatenaryJumper(new THREE.Vector3(xCb + cbO, cbY, z), new THREE.Vector3(xDsB - dsO, dsY, z), 0.14, 5, MatLib.copperConductor, vDistTag, cTag));
        });
        return bayGroup;
      }

      const f1Group = buildFeederLine('fdr-f1-breaker', 'cb_f1', 'f1', L.fdr1Z, '89-F1A', '52-F1', '89-F1B', 'fdr1');
      fdrGroup.add(f1Group);
      f1Group.userData.basePos = f1Group.position.clone();
      subparts['fdr-f1-breaker'] = f1Group;
      fdrGroup.userData.unbundled.cb_f1 = f1Group;

      const f2Group = buildFeederLine('fdr-f2-breaker', 'cb_f2', 'f2', L.fdr2Z, '89-F2A', '52-F2', '89-F2B', 'fdr2');
      fdrGroup.add(f2Group);
      f2Group.userData.basePos = f2Group.position.clone();
      subparts['fdr-f2-breaker'] = f2Group;
      fdrGroup.userData.unbundled.cb_f2 = f2Group;

      const ctTopY = +(2.05 + 1.05 * distS).toFixed(3);
      const refDsY = +(2.20 + 0.95 * distS + 0.03).toFixed(3);
      const fdrCtGroup = new THREE.Group();
      fdrCtGroup.name = 'fdr-ct-arresters';
      [L.fdr1Z, L.fdr2Z].forEach((zC, fIdx) => {
        const cTag = fIdx === 0 ? 'fdr1' : 'fdr2';
        [-distSp, 0, distSp].forEach((pz) => {
          const z = zC + pz;
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2.05, 0.1), MatLib.galvanizedSteel);
          leg.position.set(xCtSa, 1.025, z);
          const sa = createRibbedInsulator(1.05 * distS, 0.1, 7, MatLib.siliconePolymer, true);
          sa.position.set(xCtSa, 2.05 + 0.525 * distS, z);
          const ctRing = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.045, 8, 16), MatLib.darkSteel);
          ctRing.position.set(xCtSa, ctTopY - 0.08, z);
          ctRing.rotation.x = Math.PI / 2;
          fdrCtGroup.add(leg, sa, ctRing);
          fdrCtGroup.add(createCatenaryJumper(new THREE.Vector3(xDsB + 0.45, refDsY, z), new THREE.Vector3(xCtSa, ctTopY, z), 0.1, 4, MatLib.copperConductor, vDistTag, cTag));
        });
      });
      fdrGroup.add(fdrCtGroup);
      fdrCtGroup.userData.basePos = fdrCtGroup.position.clone();
      subparts['fdr-ct-arresters'] = fdrCtGroup;

      const gantryOutGroup = new THREE.Group();
      gantryOutGroup.name = 'fdr-takeoff-gantry';
      const outGantryY = 7.2;
      [L.fdr1Z, L.fdr2Z].forEach((zC, fIdx) => {
        const cTag = fIdx === 0 ? 'fdr1' : 'fdr2';
        const mastW = distSp + 1.0;
        [-mastW, mastW].forEach(dz => {
          const pole = createLatticeMast(outGantryY + 1.6, 0.9, 0.32);
          pole.position.set(L.fdrGantryX, 0, zC + dz);
          gantryOutGroup.add(pole);
        });
        const xarm = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.45, mastW * 2 + 0.8), MatLib.galvanizedSteel);
        xarm.position.set(L.fdrGantryX, outGantryY, zC);
        xarm.castShadow = true;
        gantryOutGroup.add(xarm);

        [-distSp, 0, distSp].forEach(pz => {
          const z = zC + pz;
          const ins = createRibbedInsulator(0.8, 0.08, 6, MatLib.siliconePolymer, true);
          ins.position.set(L.fdrGantryX + 0.55, outGantryY, z);
          ins.rotation.z = Math.PI / 2;
          const lineOut = createRigidBusSegment(
            new THREE.Vector3(L.fdrGantryX + 0.95, outGantryY, z),
            new THREE.Vector3(L.fdrGantryX + 18.95, outGantryY, z),
            0.018, MatLib.aluminumBus, vDistTag, cTag
          );
          gantryOutGroup.add(ins, lineOut);
          gantryOutGroup.add(createCatenaryJumper(new THREE.Vector3(xCtSa, ctTopY, z), new THREE.Vector3(L.fdrGantryX - 0.15, outGantryY - 0.05, z), 0.35, 7, MatLib.copperConductor, vDistTag, cTag));
        });
      });
      fdrGroup.add(gantryOutGroup);
      gantryOutGroup.userData.basePos = gantryOutGroup.position.clone();
      subparts['fdr-takeoff-gantry'] = gantryOutGroup;

      // DEDICATED 69/138 kV SUB-TRANSMISSION INDUSTRIAL BAY (52-IND · North-East Substation A)
      if (!L.isSubB) {
        const indKv = T.vSpec.indSubKv || 69.0;
        const indS = indKv >= 138 ? 1.55 : 1.05;
        const indSp = indKv >= 138 ? 2.65 : 2.15;
        const vIndTag = indKv + 'kV';
        const zInd = L.roads ? (L.roads.northZ + 8.6) : (L.fdr1Z - 7.5);
        const indBayGroup = new THREE.Group();
        indBayGroup.name = 'ind_hv_bay';
        indBayGroup.position.set(xCb, 0, zInd);
        indBayGroup.userData = { componentId: 'ind_hv_bay', subparts: {} };

        const indSpec = Object.assign({}, T.vSpec, { hvKv: indKv, insScale: indS, phaseSpacing: indSp, shedsCount: indKv >= 138 ? 16 : 12 });
        const indCbSub = new THREE.Group();
        const cbInd = createCompactBreakerUnit(0, 0, 0, 0, '52-IND', indSpec, 'ind_hv');
        indCbSub.add(cbInd);

        const indDsSub = new THREE.Group();
        const TI = Object.assign({}, T, { lvS: indS, lvSp: indSp, vSpec: Object.assign({}, T.vSpec, { lvKv: indKv }) });
        const dsIndA = createMVDisconnectUnit(xDsA - xCb, 0, false, '89-INDA', TI, 'ind_hv');
        const dsIndB = createMVDisconnectUnit(xDsB - xCb, 0, false, '89-INDB', TI, 'ind_hv');
        indDsSub.add(dsIndA, dsIndB);

        const indGantryY = +(8.4 + (indS - 1.0) * 1.4).toFixed(2);
        const indGantrySub = new THREE.Group();
        const indMastW = indSp + 1.2;
        [-indMastW, indMastW].forEach(dz => {
          const pole = createLatticeMast(indGantryY + 2.2, 1.05, 0.36);
          pole.position.set(L.fdrGantryX - xCb, 0, dz);
          indGantrySub.add(pole);
        });
        const indXarm = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.48, indMastW * 2 + 0.9), MatLib.galvanizedSteel);
        indXarm.position.set(L.fdrGantryX - xCb, indGantryY, 0);
        indGantrySub.add(indXarm);

        const dsIndY = dsIndA.userData.termHeight;
        const dsIndO = dsIndA.userData.termOffsetX;
        const cbIndY = cbInd.userData.termHeight || (2.4 + indS * 1.15);
        const cbIndO = cbInd.userData.termOffsetX || 1.1;

        [-indSp, 0, indSp].forEach((pz, pIdx) => {
          // HV Overhead Tap directly off HV Primary Bus (69/138 kV), bypassing 13.8 kV city buses!
          const hvTapX = Math.min(L.txX - 1.5, L.cbX + 3.2);
          const hvTapPt = new THREE.Vector3(hvTapX - xCb, T.busY || 6.8, (pIdx - 1) * T.pz - zInd);
          const midRisePt = new THREE.Vector3(xDsA - xCb - 3.0, Math.max(indGantryY + 1.4, (T.busY || 6.8) + 1.2), pz);
          const supportLeg = createLatticeMast(midRisePt.y, 0.55, 0.24);
          supportLeg.position.set(midRisePt.x, 0, pz);
          const supportIns = createRibbedInsulator(indS * 1.15, 0.11, 10, MatLib.porcelainBrown, true);
          supportIns.position.set(midRisePt.x, midRisePt.y + 0.55, pz);
          indGantrySub.add(supportLeg, supportIns);
          indGantrySub.add(createCatenaryJumper(hvTapPt, midRisePt.clone().setY(midRisePt.y + 1.1 * indS), 0.45, 7, MatLib.copperConductor, vIndTag, 'ind_hv', indKv >= 138));
          indGantrySub.add(createCatenaryJumper(midRisePt.clone().setY(midRisePt.y + 1.1 * indS), new THREE.Vector3(xDsA - xCb - dsIndO, dsIndY, pz), 0.25, 5, MatLib.copperConductor, vIndTag, 'ind_hv'));
          indGantrySub.add(createCatenaryJumper(new THREE.Vector3(xDsA - xCb + dsIndO, dsIndY, pz), new THREE.Vector3(-cbIndO, cbIndY, pz), 0.16, 5, MatLib.copperConductor, vIndTag, 'ind_hv'));
          indGantrySub.add(createCatenaryJumper(new THREE.Vector3(cbIndO, cbIndY, pz), new THREE.Vector3(xDsB - xCb - dsIndO, dsIndY, pz), 0.16, 5, MatLib.copperConductor, vIndTag, 'ind_hv'));
          // CT/Arrester post ahead of Industrial Takeoff Gantry
          const iSaLeg = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.2, 0.12), MatLib.galvanizedSteel);
          iSaLeg.position.set(xCtSa - xCb, 1.1, pz);
          const iSa = createRibbedInsulator(1.2 * indS, 0.11, 9, MatLib.siliconePolymer, true);
          iSa.position.set(xCtSa - xCb, 2.2 + 0.6 * indS, pz);
          indGantrySub.add(iSaLeg, iSa);
          const saTopY = 2.2 + 1.2 * indS;
          indGantrySub.add(createCatenaryJumper(new THREE.Vector3(xDsB - xCb + dsIndO, dsIndY, pz), new THREE.Vector3(xCtSa - xCb, saTopY, pz), 0.14, 4, MatLib.copperConductor, vIndTag, 'ind_hv'));
          const indIns = createRibbedInsulator(0.95 * indS, 0.09, 7, MatLib.siliconePolymer, true);
          indIns.position.set(L.fdrGantryX - xCb + 0.6, indGantryY, pz);
          indIns.rotation.z = Math.PI / 2;
          indGantrySub.add(indIns);
          indGantrySub.add(createCatenaryJumper(new THREE.Vector3(xCtSa - xCb, saTopY, pz), new THREE.Vector3(L.fdrGantryX - xCb - 0.15, indGantryY, pz), 0.35, 6, MatLib.copperConductor, vIndTag, 'ind_hv'));
        });

        fdrGroup.userData.switches['89-INDA'] = dsIndA;
        fdrGroup.userData.switches['52-IND'] = cbInd;
        fdrGroup.userData.switches['89-INDB'] = dsIndB;

        Object.entries({
          'ind-hv-cb': indCbSub,
          'ind-hv-ds': indDsSub,
          'ind-hv-gantry': indGantrySub
        }).forEach(([id, grp]) => {
          grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); indBayGroup.add(grp); indBayGroup.userData.subparts[id] = grp;
        });

        // Bay Nameplate
        const iCnv = document.createElement('canvas');
        iCnv.width = 420; iCnv.height = 84;
        const iCtx = iCnv.getContext('2d');
        iCtx.fillStyle = 'rgba(2, 6, 23, 0.92)'; iCtx.fillRect(4, 4, 412, 76);
        iCtx.strokeStyle = '#fbbf24'; iCtx.lineWidth = 4; iCtx.strokeRect(4, 4, 412, 76);
        iCtx.fillStyle = '#fef08a'; iCtx.font = 'bold 26px Consolas, monospace'; iCtx.textAlign = 'center';
        iCtx.fillText(`52-IND (${indKv} kV IND FEEDER)`, 210, 52);
        const iSpr = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(iCnv), transparent: true }));
        iSpr.position.set(0, indGantryY + 2.4, 0);
        iSpr.scale.set(5.4, 1.1, 1);
        indBayGroup.add(iSpr);

        fdrGroup.add(indBayGroup);
        indBayGroup.userData.basePos = indBayGroup.position.clone();
        subparts['ind-hv-bay'] = indBayGroup;
        fdrGroup.userData.unbundled.ind_hv_bay = indBayGroup;
        fdrGroup.userData.indTakeoffWorld = {
          x: L.fdrGantryX + 1.05,
          y: indGantryY,
          z: zInd,
          sp: indSp,
          kv: indKv
        };
      }

      Object.entries(subparts).forEach(([id, grp]) => tagSubpartHierarchy(grp, id, true));
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
            encGroup.add(createCatenaryJumper(new THREE.Vector3(L.ctX + 0.65, T.ctTopY, [-T.pz, 0, T.pz][pIdx]), new THREE.Vector3(inX, bushTopY, pz), 0.25, 6, MatLib.copperConductor, vHvTag, cInTag, T.bundleHv));
            encGroup.add(createCatenaryJumper(new THREE.Vector3(outX, bushTopY, pz), new THREE.Vector3(L.txX + T.txHvStudX, T.txHvStudY, T.txHvPhaseZ[pIdx]), 0.25, 6, MatLib.copperConductor, vHvTag, cOutTag, T.bundleHv));
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

    // BUILDER 15: INTERACTIVE 3D PROTECTION ZONE & CT/VT/DC-TRIP SCHEMATIC OVERLAY
    function buildProtectionZoneOverlay(scene, L, relayKey) {
      if (!relayKey) return null;
      const overlay = new THREE.Group();
      overlay.name = 'protection-zone-overlay';
      const T = getPrimaryTerminals(L);
      const ctrlPos = new THREE.Vector3(L.ctrlX + 1.0, 2.2, L.ctrlZ - 1.5);

      function addDashedPath(points, colorHex, tubeR = 0.045) {
        const mat = new THREE.MeshBasicMaterial({ color: colorHex, transparent: true, opacity: 0.92 });
        for (let i = 0; i < points.length - 1; i++) {
          const pA = points[i], pB = points[i + 1];
          const len = pA.distanceTo(pB);
          const steps = Math.max(2, Math.floor(len / 0.85));
          for (let s = 0; s < steps; s++) {
            if (s % 2 === 1) continue;
            const a = pA.clone().lerp(pB, s / steps);
            const b = pA.clone().lerp(pB, Math.min(1, (s + 0.68) / steps));
            const seg = new THREE.Mesh(new THREE.CylinderGeometry(tubeR, tubeR, Math.max(0.05, a.distanceTo(b)), 8), mat);
            seg.position.copy(a).add(b).multiplyScalar(0.5);
            seg.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
            overlay.add(seg);
          }
        }
        points.forEach((pt, idx) => {
          if (idx === 0 || idx === points.length - 1) {
            const node = new THREE.Mesh(new THREE.SphereGeometry(tubeR * 3.0, 12, 12), mat);
            node.position.copy(pt);
            overlay.add(node);
          }
        });
      }

      function addZoneHull(x1, x2, z1, z2, yTop, colorHex, title) {
        const cx = (x1 + x2) / 2, cz = (z1 + z2) / 2;
        const w = Math.max(2.5, Math.abs(x2 - x1)), d = Math.max(2.5, Math.abs(z2 - z1));
        const boxGeo = new THREE.BoxGeometry(w, yTop, d);
        const edges = new THREE.EdgesGeometry(boxGeo);
        const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: colorHex }));
        line.position.set(cx, yTop / 2 + 0.15, cz);
        const fill = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: colorHex, transparent: true, opacity: 0.08, side: THREE.DoubleSide, depthWrite: false }));
        fill.position.copy(line.position);
        overlay.add(line, fill);

        const cnv = document.createElement('canvas');
        cnv.width = 512; cnv.height = 96;
        const ctx = cnv.getContext('2d');
        ctx.fillStyle = 'rgba(2, 6, 23, 0.90)';
        ctx.fillRect(4, 4, 504, 88);
        ctx.strokeStyle = '#' + colorHex.toString(16).padStart(6, '0');
        ctx.lineWidth = 4;
        ctx.strokeRect(4, 4, 504, 88);
        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 26px Segoe UI, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(title, 256, 56);
        const spr = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cnv), transparent: true, depthTest: false }));
        spr.position.set(cx, yTop + 1.35, cz);
        spr.scale.set(6.8, 1.3, 1);
        overlay.add(spr);
      }

      const ctCy = 0x22d3ee; // Cyan = CT/VT Sensing Circuit
      const tripRd = 0xf43f5e; // Crimson = 125V DC Trip Coil Path
      const zoneGr = 0x38bdf8;
      const distStart = L.fdrGantryX + 18.95;

      if (relayKey === '21') {
        addZoneHull(L.gantryX - 2.0, L.cbX + 2.0, L.priMinZ - 0.5, L.priMaxZ + 0.5, 9.2, 0x38bdf8, 'ANSI 21 DISTANCE ZONE 1 (69 kV LINE -> CB)');
        addDashedPath([new THREE.Vector3(L.ctX, T.ctTopY, 0), new THREE.Vector3(L.ctX, 0.4, L.ctrlZ - 2.2), ctrlPos], ctCy);
        addDashedPath([ctrlPos, new THREE.Vector3(L.cbX, 0.4, L.ctrlZ - 2.2), new THREE.Vector3(L.cbX, 1.5, L.cbZ || 0)], tripRd);
      } else if (relayKey === '87B') {
        addZoneHull(L.dsX - 1.5, L.txX - 3.0, L.priMinZ - 1.0, L.priMaxZ + 1.0, 8.2, 0x10b981, 'ANSI 87B BUS DIFFERENTIAL ZONE');
        addDashedPath([new THREE.Vector3(L.ctX, T.ctTopY, 0), new THREE.Vector3(L.ctX, 0.4, L.ctrlZ - 2.0), ctrlPos], ctCy);
        addDashedPath([ctrlPos, new THREE.Vector3(L.cbX, 0.4, L.ctrlZ - 2.2), new THREE.Vector3(L.cbX, 1.5, L.cbZ || 0)], tripRd);
      } else if (relayKey === '87T') {
        addZoneHull(L.txX - 4.2, L.txX + 4.5, -4.5, 4.5, 8.0, 0xf59e0b, 'ANSI 87T TRANSFORMER DIFFERENTIAL ZONE (HV CT <-> LV CT)');
        addDashedPath([new THREE.Vector3(L.ctX, T.ctTopY, 0), new THREE.Vector3(L.ctX, 0.35, L.ctrlZ - 2.4), ctrlPos], ctCy);
        addDashedPath([new THREE.Vector3(L.secArresterX, 3.0, 0), new THREE.Vector3(L.secArresterX, 0.35, L.ctrlZ - 2.4), ctrlPos], ctCy);
        addDashedPath([ctrlPos, new THREE.Vector3(L.cbX, 0.4, L.ctrlZ - 2.2), new THREE.Vector3(L.cbX, 1.5, L.cbZ || 0)], tripRd);
        addDashedPath([ctrlPos, new THREE.Vector3(L.secCbX, 0.4, L.ctrlZ - 2.2), new THREE.Vector3(L.secCbX, 1.5, (L.fdr1Z + L.fdr2Z) / 2)], tripRd);
      } else if (relayKey === '50_51_lv') {
        addZoneHull(L.secArresterX - 2.0, L.secBusX + 1.5, L.secMinZ || -12, L.secMaxZ || 12, 6.8, 0xf59e0b, 'ANSI 50/51-LV SECONDARY BUS PROTECTION ZONE');
        addDashedPath([new THREE.Vector3(L.secArresterX, 3.0, (L.fdr1Z + L.fdr2Z) / 2), new THREE.Vector3(L.secArresterX, 0.4, L.ctrlZ - 2.2), ctrlPos], ctCy);
        addDashedPath([ctrlPos, new THREE.Vector3(L.secCbX, 0.4, L.ctrlZ - 2.2), new THREE.Vector3(L.secCbX, 1.5, (L.fdr1Z + L.fdr2Z) / 2)], tripRd);
      } else if (relayKey === '51G') {
        const ngrX = L.txX + 3.4 * T.txTankScale, ngrZ = T.autoBank ? (T.pz + 4.8) : 2.8 * T.txTankScale;
        addZoneHull(ngrX - 1.8, ngrX + 1.8, ngrZ - 1.8, ngrZ + 1.8, 4.2, 0xa855f7, 'ANSI 51G X0 NEUTRAL NGR GROUND FAULT ZONE');
        addDashedPath([new THREE.Vector3(ngrX - 0.45, 2.5, ngrZ), new THREE.Vector3(ngrX, 0.35, L.ctrlZ - 1.8), ctrlPos], ctCy);
        addDashedPath([ctrlPos, new THREE.Vector3(L.secCbX, 0.4, L.ctrlZ - 2.0), new THREE.Vector3(L.secCbX, 1.5, (L.fdr1Z + L.fdr2Z) / 2)], tripRd);
      } else if (relayKey === '50_51_f1') {
        const fCbX = L.secBusX + Math.max(12.0, L.fdrGantryX - L.secBusX) * 0.48;
        addZoneHull(L.secBusX, L.fdrGantryX + 2.0, L.fdr1Z - 3.0, L.fdr1Z + 3.0, 6.8, 0xef4444, 'ANSI 50/51/79 FEEDER 01 PROTECTION ZONE');
        addDashedPath([new THREE.Vector3(L.fdrGantryX - 2.5, 2.8, L.fdr1Z), new THREE.Vector3(L.fdrGantryX - 2.5, 0.4, L.ctrlZ - 2.0), ctrlPos], ctCy);
        addDashedPath([ctrlPos, new THREE.Vector3(fCbX, 0.4, L.ctrlZ - 2.0), new THREE.Vector3(fCbX, 1.5, L.fdr1Z)], tripRd);
      } else {
        // Recloser / Sectionalizer / Lateral Fuse Distribution Protection Zone
        addZoneHull(distStart + 2.0, distStart + 70.0, L.fdr1Z - 22.0, L.fdr1Z + 18.0, 10.5, zoneGr, '79-ACR1 -> 34-SECT -> 100K FUSE COORDINATION ZONE');
        addDashedPath([new THREE.Vector3(distStart + 6.5, 6.8, L.fdr1Z), new THREE.Vector3(distStart + 6.5, 2.0, L.fdr1Z + 0.5)], ctCy);
        addDashedPath([new THREE.Vector3(distStart + 6.5, 2.0, L.fdr1Z + 0.5), new THREE.Vector3(distStart + 24.5, 2.2, L.fdr1Z), new THREE.Vector3(distStart + 24.5, 6.8, L.fdr1Z)], tripRd);
      }

      scene.add(overlay);
      return overlay;
    }

    // REUSABLE FULL-SCALE SUBSTATION INSTANCE BUILDER (SHARED BY SUBSTATION A & TIE SUBSTATION B)
    function buildSubstationInstance(substationId, parentGroup, originX, originZ, rotY, scheme, enclosureCase, voltageClass, opts = {}) {
      const LB = getBusLayoutConfig(scheme, enclosureCase, voltageClass);
      LB.isSubB = (substationId === 'B');
      parentGroup.position.set(originX, 0, originZ);
      parentGroup.rotation.y = rotY;
      while (parentGroup.children.length > 0) {
        parentGroup.remove(parentGroup.children[0]);
      }

      const subEnv = buildSwitchyardEnvironment(parentGroup, LB, {
        isSubB: substationId === 'B',
        mainRoadZ: opts.mainRoadZ,
        subBOriginZ: originZ
      });
      const gGantry = buildGantryAndLines(parentGroup, LB);
      const gLa = buildSurgeArresters(parentGroup, LB);
      const gCt = buildInstrumentTransformers(parentGroup, LB);
      const gDs = buildDisconnectSwitch(parentGroup, LB);
      const gCb = buildCircuitBreaker(parentGroup, LB);
      const gTx = buildPowerTransformer(parentGroup, LB);
      const gBus = buildBusbarSystem(parentGroup, LB.scheme, LB.enclosure, LB);
      const gAux = buildStationService(parentGroup, LB);
      const gSec = buildSecondaryBay(parentGroup, LB);
      const gFdr = buildFeederBays(parentGroup, LB);
      let gEnc = null;
      if (LB.enclosure !== 'ais') {
        gEnc = buildEnclosureArchitecture(parentGroup, LB, LB.enclosure);
      }

      // Enforce GIS / Indoor enclosure visibility cleanly on Substation B instance as well
      const showOutdoorPrimary = (LB.enclosure !== 'gis');
      [gLa, gCt, gDs, gCb, gBus].forEach(g => {
        if (g) g.visible = showOutdoorPrimary;
      });
      if (gGantry && gGantry.userData && gGantry.userData.subparts && gGantry.userData.subparts['gantry-tubular-bus']) {
        gGantry.userData.subparts['gantry-tubular-bus'].visible = showOutdoorPrimary;
      }
      if (LB.enclosure === 'indoor') {
        if (gSec && gSec.userData) {
          if (gSec.userData.lvBreaker) gSec.userData.lvBreaker.visible = false;
          if (gSec.userData.lvDisc) gSec.userData.lvDisc.visible = false;
          if (gSec.userData.lvDiscB) gSec.userData.lvDiscB.visible = false;
        }
        if (gFdr && gFdr.userData && gFdr.userData.subparts) {
          ['fdr1-vcb', 'fdr1-ds-a', 'fdr1-ds-b', 'fdr2-vcb', 'fdr2-ds-a', 'fdr2-ds-b'].forEach(k => {
            if (gFdr.userData.subparts[k]) gFdr.userData.subparts[k].visible = false;
          });
        }
      }

      return { layout: LB, env: subEnv, tx: gTx, gantry: gGantry, busbar: gBus, enclosure: gEnc };
    }

    // BUILDER 16: OUTGOING 13.8 kV 4-DISTRICT URBAN/URD NETWORK, 140m SETBACKS, SUB B & ISOLATED 69/138 kV INDUSTRIAL LINE
    function buildDistributionNetwork(scene, layout = getBusLayoutConfig('single'), opts = {}) {
      const L = layout;
      const T = getPrimaryTerminals(L);
      // Enforced Requirement #2: Public overhead/underground urban feeders are ALWAYS 13.8 kV across all upstream HV tiers!
      const lvS = 1.0;
      const lvSp = 1.65;
      const vLvTag = '13.8kV';
      const twinLv = false;
      const lineY = 7.2;
      const distStart = L.fdrGantryX + 18.95;
      const z1 = L.fdr1Z;
      const z2 = L.fdr2Z;
      const pzOffs = [-lvSp, 0, lvSp];
      const mainRoadZ = opts.mainRoadZ || (L.yardMaxZ + 11.5);

      // Enforced Requirement #3: Minimum 140.0 m buffer setback between BOTH Substations and the City
      const cityStartX = +(distStart + 140.0).toFixed(2);
      const cityEndX = +(cityStartX + 98.0).toFixed(2);
      const eastEntryX = +(cityEndX + 140.0).toFixed(2);
      const subBX = +(eastEntryX + 10.0).toFixed(2);
      const tieCityX = +(cityStartX + 62.0).toFixed(2); // Mid-city Loop Split: F1/F2 (West) <-> Tie <-> F3/F4 (East)
      const tieX = tieCityX;

      // West 140m ROW Buffer Poles (Feeder 01 & Feeder 02)
      const p1X = distStart + 28.0;  // 79-ACR1 Auto-Recloser (West ROW Entry)
      const wP2X = distStart + 64.0;
      const wP3X = distStart + 100.0;
      const wP4X = distStart + 132.0;

      // Urban City Corridor Poles & Load Hubs
      const p2X = cityStartX + 12.0; // Pole 2: 34-SECT Sectionalizer + Gated URD Riser Tap (52-F1)
      const p3X = cityStartX + 42.0; // Pole 3: 100K Lateral Fuse Cutout + OH Residential (52-F1)
      const p4X = tieCityX;          // Mid-City Tie Boundary (79-TIE1 on z1, 89-TIE2 on z2)
      const uniTapX = cityStartX + 82.0; // District 3: University Campus & East Apartments (Sub B 52-F3)
      const munTapX = cityStartX + 82.0; // District 4: Municipal Water Pumping & Logistics (Sub B 52-F4)

      // East 140m ROW Buffer Poles (Sub B 52-F3 & 52-F4 carrying East City back to Substation B)
      const eP1X = cityEndX + 12.0;
      const eP2X = cityEndX + 48.0;
      const eP3X = cityEndX + 88.0;
      const eP4X = cityEndX + 126.0;

      const distGroup = new THREE.Group();
      distGroup.name = 'distribution';
      distGroup.userData = {
        componentId: 'distribution',
        unbundled: {},
        switches: {},
        loadLights: { res: [], comm: [], ind: [], urd: [], uni: [], mun: [] },
        urdTrenchGroup: null,
        cityGateGroup: null,
        roads: []
      };

      // 1. Paved Corridor, District Streets & Roadways (with 140m setback approaches & clean North Industrial ROW spur)
      const roadMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.92 });
      const addPavedRoad = (name, cx, cz, w, l) => {
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, 0.04, l), roadMat);
        mesh.position.set(cx, 0.02, cz);
        mesh.receiveShadow = true;
        mesh.userData.noCollider = true;
        distGroup.add(mesh);
        distGroup.userData.roads.push({
          name,
          minX: +(cx - w / 2).toFixed(2),
          maxX: +(cx + w / 2).toFixed(2),
          minZ: +(cz - l / 2).toFixed(2),
          maxZ: +(cz + l / 2).toFixed(2)
        });
        return mesh;
      };
      addPavedRoad('corrRoad', cityStartX + 49.0, (z1 + z2) / 2, 108.0, 4.6);
      addPavedRoad('latRoad', p3X + 3.6, z1 - 17.5, 4.0, 38.0);
      addPavedRoad('urdMainAve', p2X + 1.5, z1 - 16.0, 3.8, 34.0);
      addPavedRoad('urdLoopStreet', p2X + 1.5, z1 - 21.5, 28.0, 3.8);
      addPavedRoad('uniAve', uniTapX, z1 - 16.0, 4.0, 34.0);
      addPavedRoad('commBlvd', cityStartX + 34.0, z2 + 12.5, 26.0, 4.2);
      addPavedRoad('commDrive', cityStartX + 34.0, z2 + 7.5, 4.2, 14.0);
      addPavedRoad('munBlvd', munTapX, z2 + 12.5, 22.0, 4.2);
      addPavedRoad('munDrive', munTapX, z2 + 7.5, 4.2, 14.0);

      // INTERACTIVE CITY & SUBDIVISION ENTRANCE ARCHWAY GATE & GUARDHOUSE (city_gate at 140m Setback Boundary)
      const cityGateX = cityStartX - 6.0;
      const cityGateGroup = new THREE.Group();
      cityGateGroup.name = 'city_gate';
      cityGateGroup.position.set(cityGateX, 0, mainRoadZ);
      cityGateGroup.userData = { componentId: 'city_gate', action: 'toggleCityGate', subparts: {} };

      const cgArchSub = new THREE.Group();
      const cgPrecastMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.72, metalness: 0.25 });
      const cgTrimMat = new THREE.MeshStandardMaterial({ color: 0x0ea5e9, emissive: 0x0284c7, emissiveIntensity: 0.35, roughness: 0.35 });
      [-6.8, 6.8].forEach(pz => {
        const pier = new THREE.Mesh(new THREE.BoxGeometry(1.1, 7.2, 1.1), cgPrecastMat);
        pier.position.set(0, 3.6, pz);
        pier.castShadow = true;
        const cap = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.35, 1.4), MatLib.concretePad);
        cap.position.set(0, 7.35, pz);
        cgArchSub.add(pier, cap);
      });
      const portalBeam = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.1, 14.8), cgPrecastMat);
      portalBeam.position.set(0, 7.35, 0);
      const portalBand = new THREE.Mesh(new THREE.BoxGeometry(1.36, 0.24, 14.9), cgTrimMat);
      portalBand.position.set(0, 6.95, 0);
      cgArchSub.add(portalBeam, portalBand);
      [-1.4, 1.4].forEach((sideSign, sIdx) => {
        const sc = document.createElement('canvas');
        sc.width = 640; sc.height = 112;
        const sctx = sc.getContext('2d');
        sctx.fillStyle = '#0f172a'; sctx.fillRect(0, 0, 640, 112);
        sctx.strokeStyle = '#38bdf8'; sctx.lineWidth = 6; sctx.strokeRect(4, 4, 632, 104);
        sctx.fillStyle = '#f8fafc'; sctx.font = 'bold 30px Consolas, monospace'; sctx.textAlign = 'center';
        sctx.fillText('UTILITY DISTRICT & URD GATE · 140m SETBACK', 320, 48);
        sctx.fillStyle = '#38bdf8'; sctx.font = 'bold 22px Consolas, monospace';
        sctx.fillText('CLEAR HEIGHT 6.8m · CLICK / [E] TO OPERATE', 320, 84);
        const sFace = new THREE.Mesh(new THREE.PlaneGeometry(11.6, 1.25), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sc) }));
        sFace.position.set(sideSign < 0 ? -0.68 : 0.68, 7.45, 0);
        sFace.rotation.y = sIdx === 0 ? -Math.PI / 2 : Math.PI / 2;
        cgArchSub.add(sFace);
      });

      const cgBoomSub = new THREE.Group();
      const cgBooth = new THREE.Mesh(new THREE.BoxGeometry(2.8, 2.75, 2.2), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5 }));
      cgBooth.position.set(-1.6, 1.375, -8.2);
      const cgGlass = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 1.0), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
      cgGlass.position.set(-1.6, 1.65, -7.08);
      const buildBarrierArm = (isSouth) => {
        const piv = new THREE.Group();
        piv.position.set(0, 1.15, isSouth ? 6.1 : -6.1);
        const armDir = isSouth ? -1 : 1;
        const post = new THREE.Mesh(new THREE.BoxGeometry(0.42, 1.25, 0.42), MatLib.yellowHighlight);
        post.position.set(0, -0.52, 0);
        const boom = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 5.4), MatLib.hazardRed);
        boom.position.set(0, 0, armDir * 2.7);
        const stripe1 = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.16, 1.1), new THREE.MeshBasicMaterial({ color: 0xf8fafc }));
        stripe1.position.set(0, 0, armDir * 1.6);
        const stripe2 = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.16, 1.1), new THREE.MeshBasicMaterial({ color: 0xf8fafc }));
        stripe2.position.set(0, 0, armDir * 3.8);
        piv.add(post, boom, stripe1, stripe2);
        return piv;
      };
      const boomN = buildBarrierArm(false);
      const boomS = buildBarrierArm(true);
      cgBoomSub.add(cgBooth, cgGlass, boomN, boomS);
      cityGateGroup.userData.boomN = boomN;
      cityGateGroup.userData.boomS = boomS;

      Object.entries({ 'city-gate-arch': cgArchSub, 'city-gate-boom': cgBoomSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone();
        tagSubpartHierarchy(grp, id);
        grp.traverse(c => { c.userData.componentId = 'city_gate'; c.userData.action = 'toggleCityGate'; });
        cityGateGroup.add(grp);
        cityGateGroup.userData.subparts[id] = grp;
      });
      distGroup.add(cityGateGroup);
      distGroup.userData.cityGateGroup = cityGateGroup;
      distGroup.userData.cityGateX = cityGateX;
      distGroup.userData.cityGateZ = mainRoadZ;
      distGroup.userData.unbundled.city_gate = cityGateGroup;

      function addTextPlate(text, x, y, z, colorHex = '#38bdf8') {
        const cnv = document.createElement('canvas');
        cnv.width = 360; cnv.height = 84;
        const ctx = cnv.getContext('2d');
        ctx.fillStyle = 'rgba(2, 6, 23, 0.92)';
        ctx.fillRect(4, 4, 352, 76);
        ctx.strokeStyle = colorHex;
        ctx.lineWidth = 4;
        ctx.strokeRect(4, 4, 352, 76);
        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 26px Consolas, monospace';
        ctx.textAlign = 'center';
        ctx.fillText(text, 180, 52);
        const spr = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cnv), transparent: true }));
        spr.position.set(x, y, z);
        spr.scale.set(4.0, 0.95, 1);
        return spr;
      }

      // Selectable & Explodable Tapered Galvanized Tubular Steel Utility Pole Builder (IEEE C2 / RUS Grade B + Base Pier + Davit/Steel Crossarm)
      function buildSelectableUtilityPole(poleId, labelText, x, z, armRotY = 0, isDoubleArm = false, guyConfig = false, plateOffset = null) {
        const g = new THREE.Group();
        g.position.set(x, 0, z);
        if (poleId) {
          g.name = poleId;
          g.userData = { componentId: poleId, subparts: {}, poleX: x, poleZ: z };
        }

        // 1. Dodecagonal Tapered Galvanized Tubular Steel Pole Shaft + 0.42m Concrete Pier + Bolted Steel Base Plate & Grounding Lug
        const shaftSub = new THREE.Group();
        const poleH = lineY + 1.35;
        const pierPedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.42, 0.42, 16), MatLib.concretePad);
        pierPedestal.position.set(0, 0.21, 0);
        pierPedestal.receiveShadow = true;
        const baseFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.05, 8), MatLib.galvanizedSteel);
        baseFlange.position.set(0, 0.445, 0);
        for (let b = 0; b < 8; b++) {
          const ang = (b * Math.PI) / 4;
          const aBolt = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.14, 6), MatLib.darkSteel);
          aBolt.position.set(Math.cos(ang) * 0.29, 0.48, Math.sin(ang) * 0.29);
          shaftSub.add(aBolt);
        }
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.255, poleH - 0.44, 12), MatLib.galvanizedTubularSteel);
        pole.position.set(0, 0.44 + (poleH - 0.44) / 2, 0);
        pole.castShadow = true;
        const poleCap = new THREE.Mesh(new THREE.CylinderGeometry(0.155, 0.155, 0.04, 12), MatLib.darkSteel);
        poleCap.position.set(0, poleH + 0.01, 0);
        const idBand = new THREE.Mesh(new THREE.CylinderGeometry(0.228, 0.232, 0.48, 12), MatLib.yellowHighlight);
        idBand.position.set(0, 2.25, 0);
        const gMolding = new THREE.Mesh(new THREE.BoxGeometry(0.032, 2.2, 0.032), MatLib.galvanizedSteel);
        gMolding.position.set(0.22, 1.45, 0);
        const gWire = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, lineY + 0.7, 6), MatLib.groundCopper);
        gWire.position.set(0.20, 0.45 + (lineY + 0.4) / 2, 0);
        const gLug = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.09, 0.07), MatLib.brassContact);
        gLug.position.set(0.25, 0.56, 0);
        const gRodClamp = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.22, 8), MatLib.groundCopper);
        gRodClamp.position.set(0.32, 0.14, 0);
        shaftSub.add(pierPedestal, baseFlange, pole, poleCap, idBand, gMolding, gWire, gLug, gRodClamp);

        // 2. Single / Double Galvanized Steel Channel Crossarm & Bolted Steel Gusset Davit Braces
        const armSub = new THREE.Group();
        armSub.rotation.y = armRotY;
        const armW = lvSp * 2 + 1.05;
        const armOffsets = isDoubleArm ? [-0.15, 0.15] : [0];
        armOffsets.forEach(ax => {
          const arm = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.17, armW), MatLib.galvanizedSteel);
          arm.position.set(ax, lineY - 0.35, 0);
          armSub.add(arm);
        });
        const gussetCollar = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.21, 0.28, 12), MatLib.darkSteel);
        gussetCollar.position.set(0, lineY - 0.35, 0);
        armSub.add(gussetCollar);
        [-0.55, 0.55].forEach(bz => {
          const braceLen = Math.hypot(0.55, 0.68);
          const brace = new THREE.Mesh(new THREE.BoxGeometry(0.035, braceLen, 0.05), MatLib.galvanizedSteel);
          brace.position.set(isDoubleArm ? 0.18 : 0.10, lineY - 0.72, bz * 0.52);
          brace.rotation.x = bz > 0 ? -0.68 : 0.68;
          armSub.add(brace);
        });
        const bolt = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, isDoubleArm ? 0.55 : 0.35, 6), MatLib.darkSteel);
        bolt.rotation.z = Math.PI / 2;
        bolt.position.set(0, lineY - 0.35, 0);
        armSub.add(bolt);

        // 3. ANSI 55-5 Pin/Post Insulators, MGCN Neutral Spool & Dead-End Polymer Bells w/ Jumper Loops
        const insSub = new THREE.Group();
        insSub.rotation.y = armRotY;
        pzOffs.forEach(pz => {
          const pin = createRibbedInsulator(0.34, 0.058, 3, MatLib.siliconePolymer, false);
          pin.position.set(0, lineY - 0.14, pz);
          insSub.add(pin);
          if (isDoubleArm) {
            [-1, 1].forEach(dir => {
              const bell = createRibbedInsulator(0.38, 0.075, 4, MatLib.siliconePolymer, false);
              bell.rotation.z = dir * Math.PI / 2;
              bell.position.set(dir * 0.36, lineY - 0.35, pz);
              insSub.add(bell);
            });
            // Preform dead-end under-crossarm jumper loop across double arm
            insSub.add(createCatenaryJumper(
              new THREE.Vector3(-0.36, lineY - 0.35, pz),
              new THREE.Vector3(0.36, lineY - 0.35, pz),
              0.28, 6, MatLib.copperConductor, vLvTag, 'none'
            ));
          }
        });
        // Multi-Grounded Common Neutral (MGCN) porcelain spool bracket at y = lineY - 1.20
        const mgcnBracket = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.14, 0.08), MatLib.galvanizedSteel);
        mgcnBracket.position.set(0.04, lineY - 1.20, 0.14);
        const mgcnSpool = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 0.10, 10), MatLib.porcelainGray);
        mgcnSpool.position.set(0.04, lineY - 1.20, 0.22);
        insSub.add(mgcnBracket, mgcnSpool);

        // 4. Road-Safe Guy Wire Assembly: Down-Guy onto Grass Verge OR Overhead Span Guy to Galvanized Tubular Steel Stub Pole
        const guySub = new THREE.Group();
        const guyHook = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.12, 0.28), MatLib.galvanizedSteel);
        guyHook.position.set(0, lineY - 0.68, 0);
        guySub.add(guyHook);
        if (guyConfig) {
          const cfg = (typeof guyConfig === 'object') ? guyConfig : { type: 'down', dirX: 0, dirZ: -1, dist: 2.8 };
          const dirLen = Math.hypot(cfg.dirX || 0, cfg.dirZ || 0) || 1;
          const dx = (cfg.dirX || 0) / dirLen;
          const dz = (cfg.dirZ || 0) / dirLen;
          let anchorLocalX = dx * (cfg.dist || 2.8);
          let anchorLocalZ = dz * (cfg.dist || 2.8);

          const addDownGuySpan = (startVec, endVec) => {
            const vec = endVec.clone().sub(startVec);
            const len = vec.length();
            const strand = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, len, 6), MatLib.galvanizedSteel);
            strand.position.copy(startVec).addScaledVector(vec, 0.5);
            strand.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vec.clone().normalize());
            const guardLen = 2.4;
            const guard = new THREE.Mesh(
              new THREE.CylinderGeometry(0.038, 0.044, guardLen, 8),
              new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.4 })
            );
            guard.position.copy(endVec).addScaledVector(vec.clone().normalize(), -guardLen * 0.52);
            guard.quaternion.copy(strand.quaternion);
            const anchorRod = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.34, 8), MatLib.galvanizedSteel);
            anchorRod.position.set(endVec.x, 0.10, endVec.z);
            const strainEgg = new THREE.Mesh(new THREE.SphereGeometry(0.068, 8, 8), MatLib.porcelainBrown);
            strainEgg.position.copy(startVec).addScaledVector(vec, 0.28);
            guySub.add(strand, guard, anchorRod, strainEgg);
          };

          if (cfg.type === 'span') {
            // Overhead Span Guy (Head Guy) high across paved roadway (y = lineY - 0.65) to dedicated Galvanized Steel Guy Stub Pole
            const sDist = cfg.spanDist || 7.4;
            const stubX = dx * sDist;
            const stubZ = dz * sDist;
            const stubH = lineY - 0.2;
            const stubPier = new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.34, 0.36, 12), MatLib.concretePad);
            stubPier.position.set(stubX, 0.18, stubZ);
            const stubPole = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.20, stubH - 0.36, 12), MatLib.galvanizedTubularSteel);
            stubPole.position.set(stubX, 0.36 + (stubH - 0.36) / 2, stubZ);
            stubPole.castShadow = true;
            const spanTop = new THREE.Vector3(dx * 0.16, lineY - 0.65, dz * 0.16);
            const stubTop = new THREE.Vector3(stubX, lineY - 0.68, stubZ);
            const spanVec = stubTop.clone().sub(spanTop);
            const spanWire = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, spanVec.length(), 6), MatLib.galvanizedSteel);
            spanWire.position.copy(spanTop).addScaledVector(spanVec, 0.5);
            spanWire.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), spanVec.clone().normalize());
            const spanEgg = new THREE.Mesh(new THREE.SphereGeometry(0.068, 8, 8), MatLib.porcelainBrown);
            spanEgg.position.copy(spanTop).addScaledVector(spanVec, 0.35);
            guySub.add(stubPier, stubPole, spanWire, spanEgg);

            anchorLocalX = stubX + dx * (cfg.dist || 2.8);
            anchorLocalZ = stubZ + dz * (cfg.dist || 2.8);
            addDownGuySpan(
              new THREE.Vector3(stubX + dx * 0.16, lineY - 0.72, stubZ + dz * 0.16),
              new THREE.Vector3(anchorLocalX, 0.06, anchorLocalZ)
            );
          } else {
            addDownGuySpan(
              new THREE.Vector3(dx * 0.16, lineY - 0.68, dz * 0.16),
              new THREE.Vector3(anchorLocalX, 0.06, anchorLocalZ)
            );
          }
          guySub.userData.guyAnchorWorld = {
            poleId: poleId || labelText || 'aux_pole',
            x: +(x + anchorLocalX).toFixed(2),
            z: +(z + anchorLocalZ).toFixed(2),
            type: cfg.type || 'down'
          };
        }

        // 5. Vertical 3-Wire Secondary Spool Rack (240/120 V underbuild)
        const spoolSub = new THREE.Group();
        const rackBack = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.72, 0.06), MatLib.galvanizedSteel);
        rackBack.position.set(-0.20, lineY - 1.95, 0);
        spoolSub.add(rackBack);
        [-0.22, 0, 0.22].forEach(sy => {
          const spool = new THREE.Mesh(new THREE.CylinderGeometry(0.048, 0.048, 0.08, 10), MatLib.porcelainGray);
          spool.position.set(-0.26, lineY - 1.95 + sy, 0);
          spoolSub.add(spool);
        });

        const subMap = {
          'pole-shaft-ground': shaftSub,
          'pole-crossarm-brace': armSub,
          'pole-insulators': insSub,
          'pole-guy-anchor': guySub,
          'pole-spool-rack': spoolSub
        };
        Object.entries(subMap).forEach(([id, grp]) => {
          grp.name = id;
          grp.userData.basePos = grp.position.clone();
          if (poleId) {
            tagSubpartHierarchy(grp, id);
            grp.traverse(child => { child.userData.componentId = poleId; });
            g.userData.subparts[id] = grp;
          }
          g.add(grp);
        });

        if (poleId && labelText) {
          const po = plateOffset || { x: 0, y: lineY + 2.35, z: 0 };
          const plt = addTextPlate(labelText, po.x, po.y, po.z, '#94a3b8');
          plt.scale.set(2.8, 0.68, 1);
          plt.userData.componentId = poleId;
          g.add(plt);
        }
        if (poleId) {
          distGroup.userData.unbundled[poleId] = g;
        }
        return g;
      }
      const createUtilityPole = buildSelectableUtilityPole;

      // Ultra-Detailed Distribution Transformer Builder (Pole-Mounted 50kVA / URD Loop-Feed / Commercial 750kVA / Industrial 1500kVA)
      function buildDetailedDistributionTransformer(compId, x, y, z, options = {}) {
        const isPad = options.type === 'pad';
        const kvaLabel = options.kvaLabel || (isPad ? '750 kVA' : '50 kVA');
        const accentHex = options.accentHex || '#fde047';
        const tankColor = isPad && (compId === 'dt_com_750' || compId === 'dt_urd_pad') ? MatLib.safeGreen : MatLib.transformerTank;
        const scale = options.scale || 1.0;

        const dtGroup = new THREE.Group();
        dtGroup.name = compId;
        dtGroup.position.set(x, y, z);
        dtGroup.userData = { componentId: compId, subparts: {} };

        const tankSub = new THREE.Group();
        const coreSub = new THREE.Group();
        const hvSub = new THREE.Group();
        const lvSub = new THREE.Group();
        const fuseSub = new THREE.Group();
        const arrSub = new THREE.Group();

        if (!isPad) {
          const tankR = 0.34, tankH = 1.12;
          const tankCyl = new THREE.Mesh(new THREE.CylinderGeometry(tankR, tankR, tankH, 18), tankColor);
          tankCyl.castShadow = true;
          const lid = new THREE.Mesh(new THREE.CylinderGeometry(tankR + 0.03, tankR + 0.03, 0.08, 18), MatLib.galvanizedSteel);
          lid.position.y = tankH / 2 + 0.03;
          [-1.3, -0.75, 0.75, 1.3].forEach(ang => {
            const fin = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.78, 0.03), MatLib.radiatorFin);
            fin.position.set(Math.cos(ang) * (tankR + 0.05), -0.05, Math.sin(ang) * (tankR + 0.05));
            fin.rotation.y = -ang;
            tankSub.add(fin);
          });
          [-0.38, 0.38].forEach(by => {
            const brk = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.08, 0.24), MatLib.galvanizedSteel);
            brk.position.set(0, by, tankR + 0.08);
            tankSub.add(brk);
          });
          [-0.30, 0.30].forEach(lx => {
            const lug = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.14, 0.08), MatLib.galvanizedSteel);
            lug.position.set(lx, 0.42, 0);
            tankSub.add(lug);
          });
          const stCnv = document.createElement('canvas'); stCnv.width = 180; stCnv.height = 80;
          const stCtx = stCnv.getContext('2d');
          stCtx.fillStyle = '#0f172a'; stCtx.fillRect(0, 0, 180, 80);
          stCtx.fillStyle = '#fde047'; stCtx.font = 'bold 34px monospace'; stCtx.textAlign = 'center';
          stCtx.fillText(kvaLabel, 90, 50);
          const stencil = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.19), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(stCnv) }));
          stencil.position.set(0, 0.12, -tankR - 0.015);
          stencil.rotation.y = Math.PI;
          tankSub.add(tankCyl, lid, stencil);

          const coreYoke = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.64, 0.18), new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.78, roughness: 0.35 }));
          const coilCu = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.48, 16), new THREE.MeshStandardMaterial({ color: 0xb45309, metalness: 0.65, roughness: 0.3 }));
          coreSub.add(coreYoke, coilCu);

          [-0.10, 0.10].forEach((bx, bi) => {
            const hvBush = createRibbedInsulator(0.42, 0.055, 5, MatLib.porcelainBrown, false);
            hvBush.position.set(bx, tankH / 2 + 0.28, -0.05);
            hvSub.add(hvBush);
            if (bi === 0) {
              const guardCap = new THREE.Mesh(new THREE.ConeGeometry(0.10, 0.11, 12), new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 }));
              guardCap.position.set(bx, tankH / 2 + 0.50, -0.05);
              hvSub.add(guardCap);
            }
          });

          [-0.14, 0, 0.14].forEach(lx => {
            const lvB = createRibbedInsulator(0.18, 0.036, 2, MatLib.porcelainGray, false);
            lvB.rotation.x = -Math.PI / 2;
            lvB.position.set(lx, 0.24, -tankR - 0.10);
            lvSub.add(lvB);
          });
          const x0Strap = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.18, 0.02), MatLib.groundCopper);
          x0Strap.position.set(0, 0.15, -tankR - 0.04);
          lvSub.add(x0Strap);
          if (Array.isArray(options.dropTargets)) {
            options.dropTargets.forEach(tgt => {
              const localTgt = new THREE.Vector3(tgt.x - x, tgt.y - y, tgt.z - z);
              lvSub.add(createCatenaryJumper(new THREE.Vector3(0, 0.24, -tankR - 0.18), localTgt, 0.55, 8, MatLib.copperConductor, '240V', 'dist_lateral'));
            });
          }

          const coBody = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.36, 0.14), MatLib.porcelainGray);
          coBody.position.set(-0.46, 1.38, 0.22);
          const coTube = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.38, 8), MatLib.porcelainBrown);
          coTube.position.set(-0.46, 1.36, 0.10);
          coTube.rotation.x = 0.38;
          const coArm = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.06, 0.06), MatLib.galvanizedSteel);
          coArm.position.set(-0.22, 1.44, 0.26);
          const riserLead = createCatenaryJumper(new THREE.Vector3(-0.46, 1.20, 0.08), new THREE.Vector3(-0.10, tankH / 2 + 0.52, -0.05), 0.14, 6, MatLib.copperConductor, '13.8kV', 'dist_lateral');
          const feedRiser = createCatenaryJumper(new THREE.Vector3(-0.46, 1.56, 0.18), new THREE.Vector3(-0.45, 2.22, 0.35), 0.10, 5, MatLib.copperConductor, '13.8kV', 'dist_lateral');
          fuseSub.add(coBody, coTube, coArm, riserLead, feedRiser);

          const movBody = createRibbedInsulator(0.32, 0.044, 4, MatLib.porcelainGray, false);
          movBody.position.set(0.34, tankH / 2 + 0.22, 0.10);
          const movWire = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, tankH + 0.55, 6), MatLib.groundCopper);
          movWire.position.set(0.34, 0.12, 0.22);
          arrSub.add(movBody, movWire);
        } else {
          const w = 1.95 * scale, h = 1.50 * scale, d = 1.65 * scale;
          const housePad = new THREE.Mesh(new THREE.BoxGeometry(w + 0.65, 0.22, d + 0.65), MatLib.concretePad);
          housePad.position.set(0, 0.11, 0);
          const cabinet = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), tankColor);
          cabinet.position.set(0, 0.22 + h / 2, 0);
          cabinet.castShadow = true;
          const seam = new THREE.Mesh(new THREE.BoxGeometry(0.03, h * 0.85, 0.03), MatLib.galvanizedSteel);
          seam.position.set(0, 0.22 + h / 2, d / 2 + 0.015);
          [-0.65, -0.35, 0.35, 0.65].forEach(rx => {
            const radBank = new THREE.Mesh(new THREE.BoxGeometry(0.08 * scale, h * 0.72, 0.24 * scale), MatLib.radiatorFin);
            radBank.position.set(rx * scale, 0.22 + h * 0.48, -d / 2 - 0.12 * scale);
            tankSub.add(radBank);
          });
          const stCnv = document.createElement('canvas'); stCnv.width = 220; stCnv.height = 88;
          const stCtx = stCnv.getContext('2d');
          stCtx.fillStyle = '#0f172a'; stCtx.fillRect(0, 0, 220, 88);
          stCtx.strokeStyle = accentHex; stCtx.lineWidth = 4; stCtx.strokeRect(3, 3, 214, 82);
          stCtx.fillStyle = '#f8fafc'; stCtx.font = 'bold 30px monospace'; stCtx.textAlign = 'center';
          stCtx.fillText(kvaLabel, 110, 54);
          const plate = new THREE.Mesh(new THREE.PlaneGeometry(0.75 * scale, 0.30 * scale), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(stCnv) }));
          plate.position.set(-w * 0.24, 0.22 + h * 0.62, d / 2 + 0.02);
          tankSub.add(housePad, cabinet, seam, plate);

          [-0.42 * scale, 0, 0.42 * scale].forEach(cx => {
            const leg = new THREE.Mesh(new THREE.BoxGeometry(0.22 * scale, h * 0.72, 0.26 * scale), new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.75 }));
            leg.position.set(cx, 0.22 + h * 0.45, 0);
            const winding = new THREE.Mesh(new THREE.CylinderGeometry(0.18 * scale, 0.18 * scale, h * 0.56, 14), new THREE.MeshStandardMaterial({ color: 0xb45309, metalness: 0.6 }));
            winding.position.set(cx, 0.22 + h * 0.45, 0);
            coreSub.add(leg, winding);
          });

          if (options.deadFrontUrd) {
            // IEEE 386 Dead-Front 200 A Loadbreak Elbows on H1A / H1B loop-feed bushing wells
            [-0.65 * scale, -0.45 * scale, -0.25 * scale].forEach(hx => {
              const elbowBody = new THREE.Mesh(new THREE.CylinderGeometry(0.055 * scale, 0.055 * scale, 0.28 * scale, 10), MatLib.darkSteel);
              elbowBody.position.set(hx, 0.22 + h * 0.62, d / 2 + 0.10);
              elbowBody.rotation.x = Math.PI / 2;
              const yellowRing = new THREE.Mesh(new THREE.TorusGeometry(0.06 * scale, 0.012 * scale, 8, 12), MatLib.yellowHighlight);
              yellowRing.position.set(hx, 0.22 + h * 0.62, d / 2 + 0.18);
              hvSub.add(elbowBody, yellowRing);
            });
          } else {
            [-0.65 * scale, -0.45 * scale, -0.25 * scale].forEach(hx => {
              const hb = createRibbedInsulator(0.42 * scale, 0.055 * scale, 4, MatLib.porcelainBrown, false);
              hb.position.set(hx, 0.22 + h + 0.18 * scale, 0.12);
              hvSub.add(hb);
            });
          }

          [0.18 * scale, 0.36 * scale, 0.54 * scale, 0.72 * scale].forEach(lx => {
            const lb = createRibbedInsulator(0.24 * scale, 0.04 * scale, 2, MatLib.porcelainGray, false);
            lb.rotation.x = Math.PI / 2;
            lb.position.set(lx, 0.22 + h * 0.55, d / 2 + 0.12);
            lvSub.add(lb);
          });
          if (Array.isArray(options.dropTargets)) {
            options.dropTargets.forEach(tgt => {
              const localTgt = new THREE.Vector3(tgt.x - x, tgt.y - y, tgt.z - z);
              lvSub.add(createCatenaryJumper(new THREE.Vector3(0.45 * scale, 0.45, 0), localTgt, 0.05, 5, MatLib.aluminumBus, '480V', 'dist_f1_sec2'));
            });
          }

          const bayHandle = new THREE.Mesh(new THREE.BoxGeometry(0.48 * scale, 0.28 * scale, 0.16 * scale), new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.4 }));
          bayHandle.position.set(-w * 0.24, 0.22 + h * 0.38, d / 2 + 0.06);
          const riserPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.85, 8), MatLib.galvanizedSteel);
          riserPipe.position.set(-w * 0.36, 0.45, -d / 2 - 0.15);
          fuseSub.add(bayHandle, riserPipe);

          const padArr = createRibbedInsulator(0.32 * scale, 0.042 * scale, 3, MatLib.porcelainGray, false);
          padArr.position.set(-w * 0.40, 0.22 + h * 0.82, d / 2 + 0.04);
          const padGndWire = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.45, 6), MatLib.groundCopper);
          padGndWire.position.set(w * 0.48, 0.22, d * 0.48);
          arrSub.add(padArr, padGndWire);
        }

        const dtSubMap = {
          'dt-tank-fins': tankSub,
          'dt-core-coil': coreSub,
          'dt-hv-bushing': hvSub,
          'dt-lv-bushings': lvSub,
          'dt-fuse-cutout': fuseSub,
          'dt-arrester-ground': arrSub
        };
        Object.entries(dtSubMap).forEach(([id, grp]) => {
          grp.name = id;
          grp.userData.basePos = grp.position.clone();
          tagSubpartHierarchy(grp, id);
          grp.traverse(child => { child.userData.componentId = compId; });
          dtGroup.add(grp);
          dtGroup.userData.subparts[id] = grp;
        });

        distGroup.userData.unbundled[compId] = dtGroup;
        return dtGroup;
      }

      // Main Feeder 01 Poles across West 140m ROW Buffer, Urban City, Mid-City Tie & East 140m ROW Buffer
      distGroup.add(
        buildSelectableUtilityPole('dist_pole_p1', 'POLE P1 (79-ACR1)', p1X, z1, 0, false, false, { x: 0, y: lineY + 2.55, z: -2.6 }),
        buildSelectableUtilityPole(null, null, wP2X, z1, 0, false),
        buildSelectableUtilityPole(null, null, wP3X, z1, 0, false),
        buildSelectableUtilityPole(null, null, wP4X, z1, 0, false),
        buildSelectableUtilityPole('dist_pole_p2', 'POLE P2 (URD/34-SECT)', p2X, z1, 0, false, { type: 'down', dirX: 0, dirZ: -1, dist: 2.8 }, { x: 0, y: lineY + 2.55, z: -2.6 }),
        buildSelectableUtilityPole('dist_pole_p3', 'POLE P3 (SPAN GUY)', p3X, z1, 0, true, { type: 'span', dirX: 0, dirZ: 1, spanDist: 7.4, dist: 2.8 }, { x: 0, y: lineY + 2.85, z: -2.8 }),
        buildSelectableUtilityPole('dist_pole_p4', 'POLE P4 (MID-TIE N)', tieCityX, z1, 0, true, { type: 'down', dirX: 0, dirZ: -1, dist: 2.8 }, { x: 0, y: lineY + 2.55, z: -2.6 }),
        buildSelectableUtilityPole(null, null, uniTapX, z1, 0, true, { type: 'down', dirX: 0, dirZ: -1, dist: 2.8 }),
        buildSelectableUtilityPole(null, null, eP1X, z1, 0, false),
        buildSelectableUtilityPole(null, null, eP2X, z1, 0, false),
        buildSelectableUtilityPole(null, null, eP3X, z1, 0, false),
        buildSelectableUtilityPole(null, null, eP4X, z1, 0, false),
        buildSelectableUtilityPole(null, null, eastEntryX, z1, 0, true, { type: 'down', dirX: 0, dirZ: -1, dist: 2.8 })
      );

      // 2. POLE 1: Automatic Circuit Recloser (dist_recloser / 79-ACR1) - Explodable
      const recGroup = new THREE.Group();
      recGroup.name = 'dist_recloser';
      recGroup.position.set(p1X, 0, z1);
      recGroup.userData = { componentId: 'dist_recloser', subparts: {}, tag: '79-ACR1' };

      const recTankSub = new THREE.Group();
      const manifold = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.46, lvSp * 2 + 0.55), MatLib.galvanizedSteel);
      manifold.position.set(0, lineY - 0.72, 0);
      recTankSub.add(manifold);

      const recIntSub = new THREE.Group();
      const recBushSub = new THREE.Group();
      pzOffs.forEach(pz => {
        const vacHead = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.14, 0.62, 14), MatLib.porcelainGray);
        vacHead.position.set(0, lineY - 0.22, pz);
        recIntSub.add(vacHead);

        [-0.26, 0.26].forEach(bx => {
          const b = createRibbedInsulator(0.42, 0.065, 4, MatLib.siliconePolymer, true);
          b.position.set(bx, lineY + 0.12, pz);
          b.rotation.z = bx < 0 ? 0.35 : -0.35;
          recBushSub.add(b);
        });
      });

      const recCtrlSub = new THREE.Group();
      const recCabinet = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.62, 0.36), MatLib.relayPanelSteel);
      recCabinet.position.set(0.32, 1.95, 0.12);
      const recFlag = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.20, 0.20), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
      recFlag.position.set(0.35, 2.38, 0.12);
      const recConduit = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, lineY - 2.6, 8), MatLib.galvanizedSteel);
      recConduit.position.set(0.24, (lineY + 1.8) / 2, 0.12);
      recCtrlSub.add(recCabinet, recFlag, recConduit);

      Object.entries({ 'rec-tank': recTankSub, 'rec-interrupters': recIntSub, 'rec-bushings': recBushSub, 'rec-control-box': recCtrlSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); recGroup.add(grp); recGroup.userData.subparts[id] = grp;
      });
      recGroup.userData.statusFlag = recFlag;
      recGroup.add(addTextPlate('79-ACR1 RECLOSER', 0, lineY + 1.45, 0, '#38bdf8'));
      distGroup.add(recGroup);
      distGroup.userData.unbundled.dist_recloser = recGroup;
      distGroup.userData.switches['79-ACR1'] = recGroup;

      // 3. POLE 2: Automatic Line Sectionalizer (dist_sectionalizer / 34-SECT) - Explodable
      const sectGroup = new THREE.Group();
      sectGroup.name = 'dist_sectionalizer';
      sectGroup.position.set(p2X, 0, z1);
      sectGroup.userData = { componentId: 'dist_sectionalizer', subparts: {}, tag: '34-SECT', bladePairs: [] };

      const sectFrameSub = new THREE.Group();
      const sChan = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.16, lvSp * 2 + 0.5), MatLib.galvanizedSteel);
      sChan.position.set(0, lineY - 0.62, 0);
      sectFrameSub.add(sChan);

      const sectInsSub = new THREE.Group();
      const sectActSub = new THREE.Group();
      pzOffs.forEach(pz => {
        [-0.35, 0.35].forEach(ox => {
          const ins = createRibbedInsulator(0.45, 0.06, 4, MatLib.siliconePolymer, true);
          ins.position.set(ox, lineY - 0.30, pz);
          sectInsSub.add(ins);
        });
        const blade = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.72, 10), MatLib.copperConductor);
        blade.rotation.z = Math.PI / 2;
        blade.position.set(0, lineY - 0.02, pz);
        sectActSub.add(blade);
        sectGroup.userData.bladePairs.push({ blade1: blade, blade2: null });
      });

      const sectCntSub = new THREE.Group();
      const cntBox = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.44, 0.30), MatLib.brassContact);
      cntBox.position.set(-0.28, lineY - 1.15, 0.25);
      sectCntSub.add(cntBox);

      Object.entries({ 'sect-frame': sectFrameSub, 'sect-insulators': sectInsSub, 'sect-actuators': sectActSub, 'sect-counter': sectCntSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); sectGroup.add(grp); sectGroup.userData.subparts[id] = grp;
      });
      sectGroup.add(addTextPlate('34-SECT COUNT=2', 0, lineY + 1.45, 0, '#fbbf24'));
      distGroup.add(sectGroup);
      distGroup.userData.unbundled.dist_sectionalizer = sectGroup;
      distGroup.userData.switches['34-SECT'] = sectGroup;

      // 4. POLE 3: Lateral Fuse Cutout (dist_fuse_cutout / 100K) & Distribution Arrester (dist_arrester)
      const fuseGroup = new THREE.Group();
      fuseGroup.name = 'dist_fuse_cutout';
      fuseGroup.position.set(p3X - 0.9, 0, z1 - 0.8);
      fuseGroup.userData = { componentId: 'dist_fuse_cutout', subparts: {}, fuseTubes: [] };

      const fBrkSub = new THREE.Group();
      const fInsSub = new THREE.Group();
      const fTubeSub = new THREE.Group();
      const fLinkSub = new THREE.Group();

      [-0.45, 0, 0.45].forEach(fx => {
        const brk = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.10, 0.45), MatLib.galvanizedSteel);
        brk.position.set(fx, lineY - 0.45, -0.2);
        fBrkSub.add(brk);

        const cIns = createRibbedInsulator(0.45, 0.055, 4, MatLib.siliconePolymer, true);
        cIns.position.set(fx, lineY - 0.25, -0.45);
        cIns.rotation.x = Math.PI / 2;
        fInsSub.add(cIns);

        const pivot = new THREE.Group();
        pivot.position.set(fx, lineY - 0.48, -0.68);
        const tube = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.026, 0.56, 10), MatLib.spoolTanComposite);
        tube.position.set(0, 0.26, -0.06);
        tube.rotation.x = -0.24;
        const capTop = new THREE.Mesh(new THREE.CylinderGeometry(0.036, 0.036, 0.06, 10), MatLib.brassContact);
        capTop.position.set(0, 0.52, -0.12);
        pivot.add(tube, capTop);
        fTubeSub.add(pivot);
        fuseGroup.userData.fuseTubes.push(pivot);

        const link = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.22, 6), MatLib.copperConductor);
        link.position.set(fx, lineY - 0.56, -0.72);
        fLinkSub.add(link);
      });

      Object.entries({ 'fuse-bracket': fBrkSub, 'fuse-insulator': fInsSub, 'fuse-tube': fTubeSub, 'fuse-link': fLinkSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); fuseGroup.add(grp); fuseGroup.userData.subparts[id] = grp;
      });
      fuseGroup.add(addTextPlate('100K FUSE CUTOUT', 0, lineY + 1.15, -0.6, '#fca5a5'));
      distGroup.add(fuseGroup);
      distGroup.userData.unbundled.dist_fuse_cutout = fuseGroup;
      distGroup.userData.switches['FUSE-100K'] = fuseGroup;

      const daGroup = new THREE.Group();
      daGroup.name = 'dist_arrester';
      daGroup.position.set(p3X + 0.9, 0, z1 + 0.8);
      daGroup.userData = { componentId: 'dist_arrester', subparts: {} };

      const daCapSub = new THREE.Group();
      const daZnoSub = new THREE.Group();
      const daShedSub = new THREE.Group();
      const daIsoSub = new THREE.Group();
      pzOffs.forEach(pz => {
        const cap = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.14, 12), MatLib.insulatedGroundLead);
        cap.position.set(0, lineY + 0.18, pz * 0.45);
        daCapSub.add(cap);
        const zno = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.35, 10), MatLib.znoCeramic);
        zno.position.set(0, lineY - 0.04, pz * 0.45);
        daZnoSub.add(zno);
        const shed = createRibbedInsulator(0.40, 0.06, 5, MatLib.arresterPorcelainGlaze, true);
        shed.position.set(0, lineY - 0.05, pz * 0.45);
        daShedSub.add(shed);
        const cart = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.10, 8), MatLib.silverContact);
        cart.position.set(0, lineY - 0.30, pz * 0.45);
        daIsoSub.add(cart);
      });
      Object.entries({ 'da-cap': daCapSub, 'da-zno': daZnoSub, 'da-sheds': daShedSub, 'da-isolator': daIsoSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id); daGroup.add(grp); daGroup.userData.subparts[id] = grp;
      });
      distGroup.add(daGroup);
      distGroup.userData.unbundled.dist_arrester = daGroup;

      // 5. FEEDER 01 (WEST) & FEEDER 03 (EAST) PRIMARY + CONTINUOUS MGCN NEUTRAL + UNDERBUILT SECONDARY CONDUCTORS
      const wireMat = MatLib.aluminumBus;
      pzOffs.forEach((pz) => {
        const z = z1 + pz;
        // Sub A 52-F1 through 140m West ROW buffer -> 79-ACR1 -> wP2..wP4 -> 34-SECT (p2X) -> p3X -> 79-TIE1 (tieCityX)
        distGroup.add(createCatenaryJumper(new THREE.Vector3(distStart, lineY, z), new THREE.Vector3(p1X - 0.35, lineY + 0.25, z), 0.32, 6, wireMat, vLvTag, 'fdr1'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(p1X + 0.35, lineY + 0.25, z), new THREE.Vector3(wP2X, lineY, z), 0.42, 7, wireMat, vLvTag, 'dist_f1_sec1'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(wP2X, lineY, z), new THREE.Vector3(wP3X, lineY, z), 0.44, 7, wireMat, vLvTag, 'dist_f1_sec1'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(wP3X, lineY, z), new THREE.Vector3(wP4X, lineY, z), 0.44, 7, wireMat, vLvTag, 'dist_f1_sec1'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(wP4X, lineY, z), new THREE.Vector3(p2X - 0.35, lineY, z), 0.36, 6, wireMat, vLvTag, 'dist_f1_sec1'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(p2X + 0.35, lineY, z), new THREE.Vector3(p3X, lineY, z), 0.42, 7, wireMat, vLvTag, 'dist_f1_sec2'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(p3X, lineY, z), new THREE.Vector3(tieCityX - 0.35, lineY + 0.2, z), 0.38, 6, wireMat, vLvTag, 'dist_f1_sec2'));
        // Sub B 52-F3 westward from Substation B through 140m East ROW buffer -> uniTapX (District 3) -> 79-TIE1 (tieCityX)
        distGroup.add(createCatenaryJumper(new THREE.Vector3(tieCityX + 0.35, lineY + 0.2, z), new THREE.Vector3(uniTapX, lineY, z), 0.34, 6, wireMat, vLvTag, 'dist_f3'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(uniTapX, lineY, z), new THREE.Vector3(eP1X, lineY, z), 0.42, 7, wireMat, vLvTag, 'dist_f3'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eP1X, lineY, z), new THREE.Vector3(eP2X, lineY, z), 0.44, 7, wireMat, vLvTag, 'dist_f3'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eP2X, lineY, z), new THREE.Vector3(eP3X, lineY, z), 0.44, 7, wireMat, vLvTag, 'dist_f3'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eP3X, lineY, z), new THREE.Vector3(eP4X, lineY, z), 0.44, 7, wireMat, vLvTag, 'dist_f3'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eP4X, lineY, z), new THREE.Vector3(eastEntryX, lineY, z), 0.32, 6, wireMat, vLvTag, 'dist_f3'));
      });
      // Continuous Multi-Grounded Common Neutral (MGCN) & underbuilt secondary spans along North Loop poles
      const poleSpanXs = [distStart, p1X, wP2X, wP3X, wP4X, p2X, p3X, tieCityX, uniTapX, eP1X, eP2X, eP3X, eP4X, eastEntryX];
      for (let i = 0; i < poleSpanXs.length - 1; i++) {
        distGroup.add(createCatenaryJumper(
          new THREE.Vector3(poleSpanXs[i], lineY - 1.20, z1 + 0.22),
          new THREE.Vector3(poleSpanXs[i + 1], lineY - 1.20, z1 + 0.22),
          0.32, 6, wireMat, 'N', 'none'
        ));
        if (poleSpanXs[i] >= cityStartX - 2 && poleSpanXs[i + 1] <= cityEndX + 2) {
          [-0.22, 0, 0.22].forEach(sy => {
            distGroup.add(createCatenaryJumper(
              new THREE.Vector3(poleSpanXs[i] - 0.26, lineY - 1.95 + sy, z1),
              new THREE.Vector3(poleSpanXs[i + 1] - 0.26, lineY - 1.95 + sy, z1),
              0.24, 5, wireMat, '240V', 'none'
            ));
          });
        }
      }

      // 6. FOUR REALISTIC MULTI-ZONE CITY & URD DISTRIBUTION DISTRICTS
      function buildLoadHouse(hx, hz, w, h, d, roofColor, winList) {
        const g = new THREE.Group();
        const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.78 }));
        body.position.set(hx, h / 2, hz);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(Math.max(w, d) * 0.78, h * 0.55, 4), new THREE.MeshStandardMaterial({ color: roofColor, roughness: 0.65 }));
        roof.position.set(hx, h + h * 0.26, hz);
        roof.rotation.y = Math.PI / 4;
        const winMat = new THREE.MeshBasicMaterial({ color: 0xfde047 });
        const winF = new THREE.Mesh(new THREE.PlaneGeometry(w * 0.62, h * 0.42), winMat);
        winF.position.set(hx, h * 0.55, hz + d / 2 + 0.02);
        const winS = new THREE.Mesh(new THREE.PlaneGeometry(d * 0.62, h * 0.42), winMat);
        winS.position.set(hx - w / 2 - 0.02, h * 0.55, hz);
        winS.rotation.y = -Math.PI / 2;
        winList.push(winMat);
        g.add(body, roof, winF, winS);
        return g;
      }

      function buildModernSubdivisionHome(hx, hz, rotY, accentHex, winList) {
        const hg = new THREE.Group();
        hg.position.set(hx, 0, hz);
        hg.rotation.y = rotY;
        const wallMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.72 });
        const trimMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55 });
        const mainBody = new THREE.Mesh(new THREE.BoxGeometry(5.6, 4.6, 4.4), wallMat);
        mainBody.position.set(0, 2.3, 0);
        mainBody.castShadow = true;
        const garage = new THREE.Mesh(new THREE.BoxGeometry(3.2, 2.7, 3.6), wallMat);
        garage.position.set(-4.2, 1.35, 0.3);
        const roof = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.35, 5.0), trimMat);
        roof.position.set(0, 4.75, 0);
        const upperDeck = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.22, 4.0), trimMat);
        upperDeck.position.set(-4.2, 2.8, 0.3);
        const garDoor = new THREE.Mesh(new THREE.BoxGeometry(2.5, 2.1, 0.1), new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.5 }));
        garDoor.position.set(-4.2, 1.05, 2.12);
        const winMat = new THREE.MeshBasicMaterial({ color: accentHex });
        [1.4, 3.4].forEach(wy => {
          const wPane = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 0.95), winMat);
          wPane.position.set(0, wy, 2.22);
          hg.add(wPane);
        });
        winList.push(winMat);
        hg.add(mainBody, garage, roof, upperDeck, garDoor);
        return hg;
      }

      // DISTRICT 1: HIGH-END GATED URD RESIDENTIAL SUBDIVISION (ZERO OVERHEAD WIRES INSIDE)
      const urdCx = p2X + 1.5;
      const urdZCenter = z1 - 21.5;
      const urdZone = new THREE.Group();
      urdZone.name = 'urd_subdivision';

      // Subdivision masonry perimeter wall + gated guardhouse entrance at (urdCx, z1 - 6.0)
      const wallMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.85 });
      const perimWallFrontL = new THREE.Mesh(new THREE.BoxGeometry(10.5, 1.95, 0.34), wallMat);
      perimWallFrontL.position.set(urdCx - 8.4, 0.975, z1 - 6.0);
      const perimWallFrontR = new THREE.Mesh(new THREE.BoxGeometry(10.5, 1.95, 0.34), wallMat);
      perimWallFrontR.position.set(urdCx + 8.4, 0.975, z1 - 6.0);
      const guardHouse = new THREE.Mesh(new THREE.BoxGeometry(2.4, 2.7, 2.2), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.45 }));
      guardHouse.position.set(urdCx + 3.0, 1.35, z1 - 5.2);
      const boomArm = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.08, 0.08), MatLib.hazardRed);
      boomArm.position.set(urdCx, 1.15, z1 - 6.0);
      urdZone.add(perimWallFrontL, perimWallFrontR, guardHouse, boomArm);

      // Decorative subdivision trees & bollards (no guy wires, no overhead wires inside)
      const treeTrunkMat = new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.9 });
      const treeLeafMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.8 });
      [[urdCx - 5.5, z1 - 12.5], [urdCx + 5.5, z1 - 12.5], [urdCx - 9.0, z1 - 24.5], [urdCx + 9.0, z1 - 24.5]].forEach(([tx, tz]) => {
        const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 1.9, 8), treeTrunkMat);
        tr.position.set(tx, 0.95, tz);
        const cr = new THREE.Mesh(new THREE.SphereGeometry(1.15, 10, 8), treeLeafMat);
        cr.position.set(tx, 2.55, tz);
        urdZone.add(tr, cr);
      });

      // URD Dip/Riser Pole (urd_riser_pole) outside subdivision wall, tapped overhead from POLE P2 (p2X, z1)
      const riserX = p2X - 4.0, riserZ = z1 - 3.6;
      const riserGroup = new THREE.Group();
      riserGroup.name = 'urd_riser_pole';
      riserGroup.position.set(riserX, 0, riserZ);
      riserGroup.userData = { componentId: 'urd_riser_pole', subparts: {} };

      const rPoleH = lineY + 1.25;
      const rPier = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.42, 0.42, 16), MatLib.concretePad);
      rPier.position.set(0, 0.21, 0);
      const rBasePlate = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.05, 8), MatLib.galvanizedSteel);
      rBasePlate.position.set(0, 0.445, 0);
      const rShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.145, 0.255, rPoleH - 0.44, 12), MatLib.galvanizedTubularSteel);
      rShaft.position.set(0, 0.44 + (rPoleH - 0.44) / 2, 0);
      rShaft.castShadow = true;
      const rArm = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 2.6), MatLib.galvanizedSteel);
      rArm.position.set(0, lineY - 0.35, 0);
      const rGroundLug = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.09, 0.08), MatLib.brassContact);
      rGroundLug.position.set(0.24, 0.56, 0);
      const potSub = new THREE.Group();
      const cutArrSub = new THREE.Group();
      const condSub = new THREE.Group();
      [-0.85, 0, 0.85].forEach(rz => {
        const pot = createRibbedInsulator(0.42, 0.06, 5, MatLib.siliconePolymer, true);
        pot.position.set(0.28, lineY - 0.78, rz);
        const co = createRibbedInsulator(0.36, 0.05, 4, MatLib.porcelainBrown, false);
        co.position.set(-0.26, lineY - 0.16, rz);
        const arr = createRibbedInsulator(0.36, 0.048, 4, MatLib.arresterPorcelainGlaze, true);
        arr.position.set(0.28, lineY - 0.16, rz);
        potSub.add(pot);
        cutArrSub.add(co, arr);
      });
      cutArrSub.add(rArm);
      const riserConduit = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, lineY - 0.65, 10), MatLib.galvanizedSteel);
      riserConduit.position.set(0.24, (lineY - 0.65) / 2, 0);
      const vaultPad = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.25, 1.1), MatLib.concretePad);
      vaultPad.position.set(0.24, 0.12, 0);
      condSub.add(rPier, rBasePlate, rShaft, rGroundLug, riserConduit, vaultPad);

      Object.entries({ 'riser-potheads': potSub, 'riser-arresters-cutouts': cutArrSub, 'riser-conduit-duct': condSub, 'riser-conduit-vault': condSub }).forEach(([id, grp]) => {
        if (!grp.userData.subpartTagged) {
          grp.name = id;
          grp.userData.basePos = grp.position.clone();
          grp.userData.subpartTagged = true;
          tagSubpartHierarchy(grp, id);
          grp.traverse(c => { c.userData.componentId = 'urd_riser_pole'; });
          riserGroup.add(grp);
        }
        riserGroup.userData.subparts[id] = grp;
      });
      riserGroup.add(addTextPlate('URD DIP/RISER POLE', 0, lineY + 1.5, 0, '#a7f3d0'));
      distGroup.add(riserGroup);
      distGroup.userData.unbundled.urd_riser_pole = riserGroup;

      // Overhead Feeder Tap ONLY from POLE P2 (p2X, z1) to Riser Pole Outside Wall (zero overhead inside URD!)
      [-0.85, 0, 0.85].forEach((rz, idx) => {
        distGroup.add(createCatenaryJumper(
          new THREE.Vector3(p2X, lineY, z1 + pzOffs[idx]),
          new THREE.Vector3(riserX - 0.26, lineY - 0.02, riserZ + rz),
          0.16, 5, wireMat, vLvTag, 'dist_f1_sec1', twinLv
        ));
      });

      // Pad-Mounted SF6 / Solid-Dielectric Vista Underground Switchgear (urd_vista_swgr / PMH-9)
      const vistaX = urdCx + 5.8, vistaZ = z1 - 15.0;
      const vistaGroup = new THREE.Group();
      vistaGroup.name = 'urd_vista_swgr';
      vistaGroup.position.set(vistaX, 0, vistaZ);
      vistaGroup.userData = { componentId: 'urd_vista_swgr', subparts: {} };

      const vEncSub = new THREE.Group();
      const vPad = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.24, 1.8), MatLib.concretePad);
      vPad.position.y = 0.12;
      const vCab = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.35, 1.45), MatLib.safeGreen);
      vCab.position.y = 0.24 + 0.675;
      vCab.castShadow = true;
      vEncSub.add(vPad, vCab);

      const vTankSub = new THREE.Group();
      const sf6Vessel = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.85, 1.05), MatLib.galvanizedSteel);
      sf6Vessel.position.set(0, 0.88, 0);
      const viewWin = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.36), MatLib.cabinetGlass);
      viewWin.position.set(0, 1.05, 0.74);
      vTankSub.add(sf6Vessel, viewWin);

      const vElbowsSub = new THREE.Group();
      [-0.45, 0, 0.45].forEach(ex => {
        const tBody = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.32, 10), MatLib.darkSteel);
        tBody.rotation.x = Math.PI / 2;
        tBody.position.set(ex, 0.58, 0.72);
        vElbowsSub.add(tBody);
      });

      Object.entries({ 'vista-enclosure': vEncSub, 'vista-sf6-tank': vTankSub, 'vista-elbows-bus': vElbowsSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone();
        tagSubpartHierarchy(grp, id);
        grp.traverse(c => { c.userData.componentId = 'urd_vista_swgr'; });
        vistaGroup.add(grp);
        vistaGroup.userData.subparts[id] = grp;
      });
      vistaGroup.add(addTextPlate('VISTA URD SWGR (600A)', 0, 2.75, 0, '#34d399'));
      distGroup.add(vistaGroup);
      distGroup.userData.unbundled.urd_vista_swgr = vistaGroup;

      // Green Dead-Front Loop-Feed URD Pad-Mounted Transformer (dt_urd_pad / 150 kVA) + Street Pedestals + 4 Modern Homes
      const dtUrdX = urdCx - 5.2, dtUrdZ = z1 - 15.2;
      const urdTxGroup = buildDetailedDistributionTransformer('dt_urd_pad', dtUrdX, 0, dtUrdZ, {
        type: 'pad',
        scale: 0.92,
        deadFrontUrd: true,
        kvaLabel: '150 kVA URD',
        accentHex: '#34d399'
      });
      const dtUrdPlate = addTextPlate('URD LOOP PAD 150kVA', dtUrdX, 2.8, dtUrdZ, '#34d399');
      dtUrdPlate.userData.componentId = 'dt_urd_pad';
      distGroup.add(urdTxGroup, dtUrdPlate);

      const urdHomeSpecs = [
        { x: urdCx - 7.0, z: z1 - 10.5, rot: 0, pedX: urdCx - 5.0, pedZ: z1 - 13.5 },
        { x: urdCx + 6.8, z: z1 - 10.5, rot: 0, pedX: urdCx + 5.0, pedZ: z1 - 13.5 },
        { x: urdCx + 6.8, z: z1 - 28.0, rot: Math.PI, pedX: urdCx + 3.2, pedZ: z1 - 23.0 },
        { x: urdCx - 7.0, z: z1 - 28.0, rot: Math.PI, pedX: urdCx - 4.0, pedZ: z1 - 23.0 },
        { x: urdCx - 13.5, z: z1 - 16.5, rot: Math.PI / 2, pedX: urdCx - 9.5, pedZ: z1 - 16.5 },
        { x: urdCx - 13.5, z: z1 - 25.5, rot: Math.PI / 2, pedX: urdCx - 9.5, pedZ: z1 - 24.5 }
      ];
      urdHomeSpecs.forEach(h => {
        urdZone.add(buildModernSubdivisionHome(h.x, h.z, h.rot, '#fde047', distGroup.userData.loadLights.urd));
        const ped = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.65, 10), MatLib.safeGreen);
        ped.position.set(h.pedX, 0.325, h.pedZ);
        urdZone.add(ped);
      });
      distGroup.add(urdZone);

      // Toggleable X-Ray Underground 15 kV XLPE Cable Trenches (riser -> Vista -> dt_urd_pad -> home pedestals)
      const urdTrenchGroup = new THREE.Group();
      urdTrenchGroup.name = 'urd_trench_xray';
      const xlpeMat = new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0x7f1d1d, emissiveIntensity: 0.35, roughness: 0.4 });
      const ductMat = new THREE.MeshStandardMaterial({ color: 0xf97316, transparent: true, opacity: 0.28, roughness: 0.3 });
      const addUndergroundCableSegment = (pA, pB, cTag = 'dist_f1_sec1', vTagStr = '13.8kV', rad = 0.045) => {
        const yU = -0.45;
        const a = new THREE.Vector3(pA.x, yU, pA.z);
        const b = new THREE.Vector3(pB.x, yU, pB.z);
        const v = b.clone().sub(a);
        const len = v.length();
        const mid = a.clone().addScaledVector(v, 0.5);
        const cable = createCatenaryJumper(a, b, 0.02, 5, xlpeMat, vTagStr, cTag);
        const duct = new THREE.Mesh(new THREE.BoxGeometry(rad * 4.5, 0.22, len), ductMat);
        duct.position.copy(mid);
        duct.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), v.clone().normalize());
        urdTrenchGroup.add(cable, duct);
      };
      addUndergroundCableSegment({ x: riserX + 0.24, z: riserZ }, { x: vistaX, z: vistaZ }, 'dist_f1_sec1', '13.8kV', 0.055);
      addUndergroundCableSegment({ x: vistaX, z: vistaZ }, { x: dtUrdX, z: dtUrdZ }, 'dist_f1_sec1', '13.8kV', 0.055);
      urdHomeSpecs.forEach(h => {
        addUndergroundCableSegment({ x: dtUrdX, z: dtUrdZ }, { x: h.pedX, z: h.pedZ }, 'dist_f1_sec1', '240V', 0.032);
        addUndergroundCableSegment({ x: h.pedX, z: h.pedZ }, { x: h.x, z: h.z }, 'dist_f1_sec1', '240V', 0.028);
      });
      urdTrenchGroup.visible = (typeof AppState !== 'undefined' && AppState.urdXrayActive !== undefined) ? !!AppState.urdXrayActive : true;
      distGroup.add(urdTrenchGroup);
      distGroup.userData.urdTrenchGroup = urdTrenchGroup;

      // DISTRICT 2: OVERHEAD SUBURBAN RESIDENTIAL DISTRICT (50 kVA Pole-Mount + 5 Homes + Triplex Drops)
      const resPoleZ = z1 - 12.5;
      const resPoleZ2 = z1 - 26.5;
      distGroup.add(
        buildSelectableUtilityPole(null, null, p3X - 1.2, resPoleZ, Math.PI / 2, false, { type: 'down', dirX: -1, dirZ: 0, dist: 2.8 }),
        buildSelectableUtilityPole(null, null, p3X - 1.2, resPoleZ2, Math.PI / 2, true, { type: 'down', dirX: 0, dirZ: -1, dist: 2.8 })
      );
      [-0.45, 0, 0.45].forEach((ox, idx) => {
        distGroup.add(createCatenaryJumper(new THREE.Vector3(p3X + ox, lineY, z1 + pzOffs[idx]), new THREE.Vector3(p3X - 1.2 + ox, lineY - 0.1, z1 - 1.5), 0.12, 4, MatLib.copperConductor, vLvTag, 'dist_lateral'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(p3X - 1.2 + ox, lineY - 0.4, z1 - 1.5), new THREE.Vector3(p3X - 1.2 + ox, lineY, resPoleZ), 0.32, 6, wireMat, vLvTag, 'dist_lateral'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(p3X - 1.2 + ox, lineY, resPoleZ), new THREE.Vector3(p3X - 1.2 + ox, lineY, resPoleZ2), 0.35, 6, wireMat, vLvTag, 'dist_lateral'));
      });
      const resTxGroup = buildDetailedDistributionTransformer('dt_res_50', p3X - 1.2, lineY - 2.25, resPoleZ - 0.40, {
        type: 'pole',
        kvaLabel: '50 kVA 1φ',
        accentHex: '#fde047',
        dropTargets: [
          { x: p3X - 6.8, y: 2.35, z: resPoleZ - 1.8 },
          { x: p3X - 6.8, y: 2.35, z: resPoleZ - 8.2 },
          { x: p3X + 0.2, y: 2.35, z: resPoleZ - 11.2 }
        ]
      });
      distGroup.add(resTxGroup);
      distGroup.add(
        buildLoadHouse(p3X - 6.8, resPoleZ - 1.8, 4.2, 2.7, 3.8, 0x7c2d12, distGroup.userData.loadLights.res),
        buildLoadHouse(p3X - 6.8, resPoleZ - 8.2, 4.4, 2.8, 4.0, 0x1e3a8a, distGroup.userData.loadLights.res),
        buildLoadHouse(p3X - 6.8, resPoleZ2 - 3.5, 4.1, 2.7, 3.8, 0x3f6212, distGroup.userData.loadLights.res),
        buildLoadHouse(p3X + 0.2, resPoleZ2 + 3.0, 4.2, 2.8, 3.9, 0x701a75, distGroup.userData.loadLights.res),
        buildLoadHouse(p3X + 0.2, resPoleZ2 - 4.0, 4.3, 2.7, 3.8, 0x991b1b, distGroup.userData.loadLights.res)
      );
      const resTxPlate = addTextPlate('SUBURBAN OH 50kVA', p3X - 1.2, 5.2, resPoleZ - 4.8, '#fde047');
      resTxPlate.userData.componentId = 'dt_res_50';
      distGroup.add(resTxPlate);

      // DISTRICT 3 (SOUTH-WEST · SUB A 52-F2): COMMERCIAL BUSINESS DISTRICT (CBD), OFFICE TOWER, SHOPPING MALL & HOSPITAL + EMERGENCY GEN
      const commTapX = cityStartX + 34.0;
      const commZ = z2 + 16.5;
      distGroup.add(buildSelectableUtilityPole(null, null, commTapX, z2 + 8.0, Math.PI / 2, true, { type: 'down', dirX: -1, dirZ: 0, dist: 2.8 }));
      [-1.0, 0, 1.0].forEach((ox, i) => {
        distGroup.add(createCatenaryJumper(new THREE.Vector3(commTapX + ox, lineY, z2 + pzOffs[i]), new THREE.Vector3(commTapX + ox, lineY, z2 + 8.0), 0.24, 5, wireMat, vLvTag, 'dist_f2_main'));
      });
      const commTxGroup = buildDetailedDistributionTransformer('dt_com_750', commTapX + 3.8, 0, commZ - 1.2, {
        type: 'pad',
        scale: 1.08,
        kvaLabel: '750 kVA 3φ',
        accentHex: '#38bdf8',
        dropTargets: [{ x: commTapX - 2.0, y: 0.45, z: commZ + 7.5 }]
      });
      const commGlassMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
      distGroup.userData.loadLights.comm.push(commGlassMat);
      const tower = new THREE.Mesh(new THREE.BoxGeometry(6.8, 14.8, 5.8), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.25, metalness: 0.5 }));
      tower.position.set(commTapX - 5.2, 7.4, commZ + 8.5);
      for (let fy = 2.0; fy <= 13.0; fy += 2.2) {
        const glassBand = new THREE.Mesh(new THREE.BoxGeometry(6.92, 0.9, 5.92), commGlassMat);
        glassBand.position.set(commTapX - 5.2, fy, commZ + 8.5);
        distGroup.add(glassBand);
      }
      const mall = new THREE.Mesh(new THREE.BoxGeometry(10.5, 4.2, 6.0), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.48 }));
      mall.position.set(commTapX + 5.0, 2.1, commZ + 8.2);
      const mallSign = new THREE.Mesh(new THREE.PlaneGeometry(8.5, 1.3), commGlassMat);
      mallSign.position.set(commTapX + 5.0, 2.5, commZ + 5.18);
      mallSign.rotation.y = Math.PI;
      const hospX = commTapX + 14.8, hospZ = commZ + 8.0;
      const hosp = new THREE.Mesh(new THREE.BoxGeometry(7.2, 5.6, 5.4), new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.6 }));
      hosp.position.set(hospX, 2.8, hospZ);
      const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.45, 1.45, 0.1), MatLib.hazardRed);
      crossV.position.set(hospX, 3.8, hospZ - 2.72);
      const crossH = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.45, 0.1), MatLib.hazardRed);
      crossH.position.set(hospX, 3.8, hospZ - 2.72);
      const hospWin = new THREE.Mesh(new THREE.PlaneGeometry(6.0, 1.1), commGlassMat);
      hospWin.position.set(hospX, 1.75, hospZ - 2.72);
      hospWin.rotation.y = Math.PI;
      const dieselGen = new THREE.Mesh(new THREE.BoxGeometry(2.8, 1.65, 1.4), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.45 }));
      dieselGen.position.set(hospX - 2.0, 0.825, hospZ - 4.3);
      const atsCab = new THREE.Mesh(new THREE.BoxGeometry(0.95, 1.6, 0.65), MatLib.galvanizedSteel);
      atsCab.position.set(hospX + 0.6, 0.8, hospZ - 4.1);
      [commTapX - 3.0, commTapX + 6.0].forEach(lx => {
        const sPole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 4.8, 8), MatLib.galvanizedSteel);
        sPole.position.set(lx, 2.4, commZ + 3.2);
        const sHead = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.12, 0.25), commGlassMat);
        sHead.position.set(lx, 4.8, commZ + 3.6);
        distGroup.add(sPole, sHead);
      });
      const commTxPlate = addTextPlate('CBD + HOSPITAL 750kVA (F2)', commTapX + 3.8, 4.8, commZ, '#38bdf8');
      commTxPlate.userData.componentId = 'dt_com_750';
      distGroup.add(commTxGroup, tower, mall, mallSign, hosp, crossV, crossH, hospWin, dieselGen, atsCab, commTxPlate);

      // DISTRICT 3B (NORTH-EAST CITY · SUB B 52-F3): EAST RESIDENTIAL & UNIVERSITY CAMPUS (500 kVA Pad-Mount + PV Hall + Library + Apts)
      const uniZ = z1 - 15.5;
      distGroup.add(buildSelectableUtilityPole(null, null, uniTapX, z1 - 8.5, Math.PI / 2, true, { type: 'down', dirX: 1, dirZ: 0, dist: 2.8 }));
      [-0.8, 0, 0.8].forEach((ox, i) => {
        distGroup.add(createCatenaryJumper(new THREE.Vector3(uniTapX + ox, lineY, z1 + pzOffs[i]), new THREE.Vector3(uniTapX + ox, lineY, z1 - 8.5), 0.24, 5, wireMat, vLvTag, 'dist_f3'));
      });
      const uniTxGroup = buildDetailedDistributionTransformer('dt_uni_500', uniTapX + 3.2, 0, uniZ + 1.2, {
        type: 'pad',
        scale: 1.0,
        deadFrontUrd: true,
        kvaLabel: '500 kVA UNI',
        accentHex: '#a78bfa'
      });
      const uniLightMat = new THREE.MeshBasicMaterial({ color: 0xa78bfa });
      distGroup.userData.loadLights.uni.push(uniLightMat);
      // Engineering Hall w/ Rooftop PV Solar Array
      const engHall = new THREE.Mesh(new THREE.BoxGeometry(11.0, 5.2, 6.2), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55 }));
      engHall.position.set(uniTapX - 2.0, 2.6, uniZ - 9.2);
      const pvMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, metalness: 0.6, roughness: 0.25 });
      [-3.2, 0, 3.2].forEach(px => {
        const pv = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.1, 3.8), pvMat);
        pv.position.set(uniTapX - 2.0 + px, 5.45, uniZ - 9.2);
        pv.rotation.x = 0.22;
        distGroup.add(pv);
      });
      const engWin = new THREE.Mesh(new THREE.PlaneGeometry(9.2, 1.3), uniLightMat);
      engWin.position.set(uniTapX - 2.0, 3.1, uniZ - 6.08);
      // Science Library & East Campus Apartments
      const sciLib = new THREE.Mesh(new THREE.BoxGeometry(7.2, 4.4, 5.8), new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.5 }));
      sciLib.position.set(uniTapX + 8.5, 2.2, uniZ - 9.0);
      const libWin = new THREE.Mesh(new THREE.PlaneGeometry(5.6, 1.6), uniLightMat);
      libWin.position.set(uniTapX + 8.5, 2.2, uniZ - 6.08);
      const uniApts = new THREE.Mesh(new THREE.BoxGeometry(8.5, 6.8, 5.2), new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.72 }));
      uniApts.position.set(uniTapX + 8.2, 3.4, uniZ - 1.5);
      const aptWin = new THREE.Mesh(new THREE.PlaneGeometry(6.8, 1.1), uniLightMat);
      aptWin.position.set(uniTapX + 8.2, 4.2, uniZ - 4.12);
      aptWin.rotation.y = Math.PI;
      const uniTxPlate = addTextPlate('UNIV CAMPUS 500kVA (F3)', uniTapX + 3.0, 4.6, uniZ + 1.5, '#a78bfa');
      uniTxPlate.userData.componentId = 'dt_uni_500';
      distGroup.add(uniTxGroup, engHall, engWin, sciLib, libWin, uniApts, aptWin, uniTxPlate);

      // DISTRICT 4 (SOUTH-EAST CITY · SUB B 52-F4): MUNICIPAL WATER PUMPING STATION & LOGISTICS HUB (1,000 kVA Pad-Mount)
      const munZ = z2 + 16.8;
      distGroup.add(buildSelectableUtilityPole(null, null, munTapX, z2 + 8.2, Math.PI / 2, true, { type: 'down', dirX: -1, dirZ: 0, dist: 2.8 }));
      [-0.8, 0, 0.8].forEach((ox, i) => {
        distGroup.add(createCatenaryJumper(new THREE.Vector3(munTapX + ox, lineY, z2 + pzOffs[i]), new THREE.Vector3(munTapX + ox, lineY, z2 + 8.2), 0.24, 5, wireMat, vLvTag, 'dist_f4'));
      });
      const munTxGroup = buildDetailedDistributionTransformer('dt_mun_1000', munTapX - 3.6, 0, munZ - 1.4, {
        type: 'pad',
        scale: 1.14,
        kvaLabel: '1,000 kVA MUN',
        accentHex: '#2dd4bf',
        dropTargets: [{ x: munTapX + 2.0, y: 0.45, z: munZ + 6.5 }]
      });
      const munLightMat = new THREE.MeshBasicMaterial({ color: 0x2dd4bf });
      distGroup.userData.loadLights.mun.push(munLightMat);
      // Booster Pump Hall & Logistics Warehouse + Dual Municipal Water Storage Tanks
      const pumpHall = new THREE.Mesh(new THREE.BoxGeometry(8.6, 4.4, 5.8), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55 }));
      pumpHall.position.set(munTapX - 2.0, 2.2, munZ + 7.5);
      const pumpWin = new THREE.Mesh(new THREE.PlaneGeometry(6.8, 1.0), munLightMat);
      pumpWin.position.set(munTapX - 2.0, 2.6, munZ + 4.58);
      pumpWin.rotation.y = Math.PI;
      const logWh = new THREE.Mesh(new THREE.BoxGeometry(9.2, 4.0, 6.2), new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.65 }));
      logWh.position.set(munTapX + 8.8, 2.0, munZ + 7.5);
      [-5.2, -1.2].forEach(tx => {
        const tank = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 5.4, 16), MatLib.galvanizedSteel);
        tank.position.set(munTapX + tx, 2.7, munZ + 13.8);
        const cap = new THREE.Mesh(new THREE.ConeGeometry(2.0, 0.9, 16), new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.4 }));
        cap.position.set(munTapX + tx, 5.85, munZ + 13.8);
        distGroup.add(tank, cap);
      });
      const munTxPlate = addTextPlate('MUNICIPAL WATER 1MVA (F4)', munTapX - 3.6, 5.2, munZ, '#2dd4bf');
      munTxPlate.userData.componentId = 'dt_mun_1000';
      distGroup.add(munTxGroup, pumpHall, pumpWin, logWh, munTxPlate);

      // 7. FEEDER 02 (SUB A) -> WEST 140m ROW -> 79-F2 & CAP-F2 -> CBD/HOSPITAL -> 89-TIE2 -> FEEDER 04 (SUB B) -> EAST 140m ROW
      const f2P1 = p1X; // Recloser 79-F2 + Switched Pole Cap Bank
      const f2GuyDirZ = (z2 + 1.5 > z1 + 5.8) ? 1 : -1;
      [f2P1, wP2X, wP3X, wP4X, commTapX, tieCityX, munTapX, eP1X, eP2X, eP3X, eP4X].forEach((fx, idx) => {
        const isCorner = (fx === f2P1 || fx === commTapX || fx === tieCityX || fx === munTapX);
        distGroup.add(buildSelectableUtilityPole(null, null, fx, z2, 0, isCorner, isCorner ? { type: 'down', dirX: 0, dirZ: f2GuyDirZ, dist: 2.8 } : false));
      });
      // 79-F2 Automatic Pole Recloser + Pole Capacitor Bank at f2P1
      const rec2Group = new THREE.Group();
      rec2Group.name = 'dist_f2_recloser';
      rec2Group.position.set(f2P1, 0, z2);
      rec2Group.userData = { tag: '79-F2' };
      const r2Box = new THREE.Mesh(new THREE.BoxGeometry(0.92, 0.44, lvSp * 2 + 0.5), MatLib.galvanizedSteel);
      r2Box.position.set(0, lineY - 0.70, 0);
      const r2Flag = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.22, 0.22), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
      r2Flag.position.set(0.35, 2.38, 0.14);
      const r2Ctrl = new THREE.Mesh(new THREE.BoxGeometry(0.40, 0.58, 0.34), MatLib.relayPanelSteel);
      r2Ctrl.position.set(0.32, 1.95, 0.14);
      rec2Group.add(r2Box, r2Flag, r2Ctrl);
      pzOffs.forEach(pz => {
        const vb = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.56, 12), MatLib.porcelainGray);
        vb.position.set(0, lineY - 0.22, pz);
        rec2Group.add(vb);
      });
      rec2Group.userData.statusFlag = r2Flag;
      rec2Group.add(addTextPlate('79-F2 RECLOSER', 0, lineY + 1.45, 0, '#67e8f9'));
      distGroup.add(rec2Group);
      distGroup.userData.switches['79-F2'] = rec2Group;

      // Pole-mounted 900 kVAR Switched Shunt Capacitor CAP-F2 on wP2X
      const capF2Rack = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.65, lvSp * 2 + 0.3), MatLib.galvanizedSteel);
      capF2Rack.position.set(wP2X, lineY - 1.35, 0 + z2);
      distGroup.add(capF2Rack, addTextPlate('CAP-F2 900kVAR', wP2X, lineY + 1.35, z2, '#67e8f9'));

      // 89-TIE2 Normally-Open Tie Switch on South Loop at (tieCityX, z2)
      const tie2Group = new THREE.Group();
      tie2Group.name = 'tie2_switch';
      tie2Group.position.set(tieCityX, 0, z2);
      tie2Group.userData = { tag: '89-TIE2', bladePairs: [] };
      const tie2Base = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.16, lvSp * 2 + 0.5), MatLib.galvanizedSteel);
      tie2Base.position.set(0, lineY - 0.58, 0);
      tie2Group.add(tie2Base);
      pzOffs.forEach(pz => {
        [-0.34, 0.34].forEach(ox => {
          const ins = createRibbedInsulator(0.42, 0.055, 4, MatLib.siliconePolymer, true);
          ins.position.set(ox, lineY - 0.28, pz);
          tie2Group.add(ins);
        });
        const bl = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.68, 8), MatLib.copperConductor);
        bl.position.set(-0.34, lineY + 0.25, pz);
        bl.rotation.z = 0.65;
        tie2Group.add(bl);
        tie2Group.userData.bladePairs.push({ blade1: bl, blade2: null });
      });
      tie2Group.add(addTextPlate('89-TIE2 (NO)', 0, lineY + 1.45, 0, '#2dd4bf'));
      distGroup.add(tie2Group);
      distGroup.userData.switches['89-TIE2'] = tie2Group;

      const f2WestSpans = [distStart, f2P1, wP2X, wP3X, wP4X, commTapX, tieCityX];
      const f4EastSpans = [tieCityX, munTapX, eP1X, eP2X, eP3X, eP4X, eastEntryX];
      pzOffs.forEach(pz => {
        const z = z2 + pz;
        for (let i = 0; i < f2WestSpans.length - 1; i++) {
          const cTag = i === 0 ? 'fdr2' : 'dist_f2_main';
          distGroup.add(createCatenaryJumper(new THREE.Vector3(f2WestSpans[i], lineY, z), new THREE.Vector3(f2WestSpans[i + 1], lineY, z), 0.36, 6, wireMat, vLvTag, cTag));
        }
        for (let j = 0; j < f4EastSpans.length - 1; j++) {
          distGroup.add(createCatenaryJumper(new THREE.Vector3(f4EastSpans[j], lineY, z), new THREE.Vector3(f4EastSpans[j + 1], lineY, z), 0.36, 6, wireMat, vLvTag, 'dist_f4'));
        }
      });

      // 8. FULL-SCALE DYNAMIC TIE SUBSTATION B VIA buildSubstationInstance & 140m EAST BUFFER CORRIDOR
      const subBScheme = (typeof AppState !== 'undefined' && AppState.subBTopology) ? AppState.subBTopology : 'ring';
      const subBEnc = (typeof AppState !== 'undefined' && AppState.subBEnclosure) ? AppState.subBEnclosure : 'ais';
      const LB_pre = getBusLayoutConfig(subBScheme, subBEnc, L.voltageClass);
      const subBOriginX = +(eastEntryX + (LB_pre.fdrGantryX + 18.95)).toFixed(2);
      const subBOriginZ = +(z1 + LB_pre.fdr1Z).toFixed(2);
      const subBMidWorldX = +(subBOriginX - LB_pre.yardCenterX).toFixed(2);
      const subBMidWorldZ = +(subBOriginZ - LB_pre.yardCenterZ).toFixed(2);

      const subBYardGroup = new THREE.Group();
      subBYardGroup.name = 'substation_b_yard';
      const subBInst = buildSubstationInstance('B', subBYardGroup, subBOriginX, subBOriginZ, Math.PI, subBScheme, subBEnc, L.voltageClass, {
        mainRoadZ: opts.mainRoadZ,
        subBOriginZ
      });
      const LB = subBInst.layout;
      const subBEnv = subBInst.env;
      const sbTxGrp = subBInst.tx;

      subBYardGroup.traverse(obj => {
        if (obj.userData) {
          if (obj.userData.flowCurve && obj.userData.circuitTag && obj.userData.circuitTag !== 'none') {
            if (obj.userData.circuitTag === 'fdr1') obj.userData.circuitTag = 'dist_f3';
            else if (obj.userData.circuitTag === 'fdr2') obj.userData.circuitTag = 'dist_f4';
            else obj.userData.circuitTag = 'dist_sub_b';
          }
          const isGateObj = obj.userData.action === 'toggleGateB' || obj.userData.componentId === 'substation_gate';
          if (isGateObj) {
            obj.userData.componentId = 'substation_gate';
            obj.userData.action = 'toggleGateB';
          } else if (obj.userData.componentId) {
            obj.userData.componentId = 'substation_b';
          }
        }
      });

      const subBFdr2Z = subBOriginZ - LB.fdr2Z;
      distGroup.add(buildSelectableUtilityPole(null, null, eastEntryX, subBFdr2Z, 0, true, { type: 'down', dirX: 1, dirZ: 0, dist: 2.8 }));
      pzOffs.forEach(pz => {
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eastEntryX, lineY, z2 + pz), new THREE.Vector3(eastEntryX, lineY, subBFdr2Z + pz), 0.25, 5, wireMat, vLvTag, 'dist_f4'));
      });

      // Eastern Incoming HV Lattice Transmission Corridor -> Zero-Gap Termination directly onto Sub B East HV Gantry
      const TB = getPrimaryTerminals(LB);
      const sbGantryWorldX = subBOriginX - LB.gantryX;
      const sbGantryWorldZ = subBOriginZ;
      const sbGantryY = TB.gantryWireY;
      const sbStrainY = TB.gantryStrainY;
      const sbMastPeakY = +(sbGantryY + 2.6 + 1.4).toFixed(2);
      const sbPz = TB.pz;
      const sbMastZ = Math.max(5.0, sbPz * 1.44);
      const sbTwWireY = +(sbGantryY + (LB.vSpec.hvKv >= 500 ? 5.2 : 4.0)).toFixed(2);
      const eT1 = sbGantryWorldX + 54, eT2 = sbGantryWorldX + 114;
      [eT1, eT2].forEach(ex => {
        const tg = createLatticeMast(sbTwWireY + 3.8, LB.vSpec.hvKv >= 500 ? 4.4 : 3.4, LB.vSpec.hvKv >= 500 ? 1.2 : 0.9);
        tg.position.set(ex, 0, sbGantryWorldZ);
        const xArm = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.52, sbPz * 2 + 2.8), MatLib.galvanizedSteel);
        xArm.position.set(ex, sbTwWireY + 1.4, sbGantryWorldZ);
        distGroup.add(tg, xArm);
      });
      [-sbPz, 0, sbPz].forEach(zOff => {
        const tz = sbGantryWorldZ - zOff;
        const strainPt = new THREE.Vector3(sbGantryWorldX + 0.35, sbStrainY, tz);
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eT1, sbTwWireY, tz), strainPt, 1.45, 12, MatLib.copperConductor, LB.vSpec.hvKv + 'kV', 'dist_sub_b', TB.bundleHv));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eT1, sbTwWireY, tz), new THREE.Vector3(eT2, sbTwWireY, tz), 1.65, 10, MatLib.copperConductor, LB.vSpec.hvKv + 'kV', 'dist_sub_b', TB.bundleHv));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eT2, sbTwWireY, tz), new THREE.Vector3(eT2 + 68, sbTwWireY + 0.6, tz), 1.5, 8, MatLib.copperConductor, LB.vSpec.hvKv + 'kV', 'dist_sub_b', TB.bundleHv));
      });
      [-sbMastZ, sbMastZ].forEach((sz, sIdx) => {
        const peakZ = sbGantryWorldZ + (sIdx === 0 ? -0.9 : 0.9);
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eT2 + 68, sbTwWireY + 4.4, peakZ), new THREE.Vector3(eT1, sbTwWireY + 3.8, peakZ), 1.1, 8, MatLib.galvanizedSteel, LB.vSpec.hvKv + 'kV', 'none'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(eT1, sbTwWireY + 3.8, peakZ), new THREE.Vector3(sbGantryWorldX, sbMastPeakY, sbGantryWorldZ + sz), 0.95, 8, MatLib.galvanizedSteel, LB.vSpec.hvKv + 'kV', 'none'));
      });
      distGroup.add(subBYardGroup);

      // 9. DEDICATED 69/138 kV SUB-TRANSMISSION NORTH CORRIDOR & ISOLATED HEAVY INDUSTRIAL COMPLEX (dt_ind_1500 / 52-CUST)
      const indTakeoff = opts.indTakeoff || {
        x: L.fdrGantryX + 1.05,
        y: (T.vSpec.indSubKv || 69) >= 138 ? 9.17 : 8.47,
        z: L.roads ? (L.roads.northZ + 8.6) : (z1 - 7.5),
        sp: (T.vSpec.indSubKv || 69) >= 138 ? 2.65 : 2.15,
        kv: T.vSpec.indSubKv || 69.0
      };
      const vIndTag = indTakeoff.kv + 'kV';
      const indSubX = distStart + 86.0;
      const indSubZ = Math.min(L.yardMinZ - 38.0, z1 - 68.0);
      const indSp = indTakeoff.sp;
      const indLineH = indTakeoff.kv >= 138 ? 14.5 : 12.0;

      // North Industrial ROW 69/138 kV Tapered Galvanized Tubular Steel Monopoles w/ Davit Crossarms & Polymer Suspension Insulators
      const indTowers = [
        { x: indTakeoff.x + 24.0, z: Math.min(L.yardMinZ - 14.0, (indTakeoff.z + indSubZ) * 0.45), y: indTakeoff.y + 3.2 },
        { x: distStart + 44.0, z: indSubZ + 8.0, y: indLineH },
        { x: indSubX - 24.0, z: indSubZ, y: indLineH }
      ];
      indTowers.forEach(tw => {
        const pier = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.62, 0.55, 16), MatLib.concretePad);
        pier.position.set(tw.x, 0.275, tw.z);
        const flg = new THREE.Mesh(new THREE.CylinderGeometry(0.52, 0.52, 0.08, 12), MatLib.galvanizedSteel);
        flg.position.set(tw.x, 0.59, tw.z);
        const poleH = tw.y + 2.2;
        const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.20, 0.42, poleH - 0.62, 12), MatLib.galvanizedTubularSteel);
        mast.position.set(tw.x, 0.62 + (poleH - 0.62) / 2, tw.z);
        mast.castShadow = true;
        const arm = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.36, indSp * 2 + 2.0), MatLib.galvanizedSteel);
        arm.position.set(tw.x, tw.y + 0.55, tw.z);
        const gLug = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.12, 0.10), MatLib.groundCopper);
        gLug.position.set(tw.x + 0.44, 0.72, tw.z);
        distGroup.add(pier, flg, mast, arm, gLug);
        [-indSp, 0, indSp].forEach(pz => {
          const ins = createRibbedInsulator(0.85, 0.075, 7, MatLib.siliconePolymer, true);
          ins.position.set(tw.x, tw.y + 0.08, tw.z + pz);
          distGroup.add(ins);
        });
      });
      // Customer-Owned Dead-End Receiving Portal & Precast Concrete Yard Wall at (indSubX, indSubZ)
      const custPortalX = indSubX - 11.5;
      [-indSp - 1.0, indSp + 1.0].forEach(dz => {
        const leg = createLatticeMast(indLineH * 0.78, 1.0, 0.35);
        leg.position.set(custPortalX, 0, indSubZ + dz);
        distGroup.add(leg);
      });
      const custBeam = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.45, indSp * 2 + 2.4), MatLib.galvanizedSteel);
      custBeam.position.set(custPortalX, indLineH * 0.68, indSubZ);
      distGroup.add(custBeam);

      [-indSp, 0, indSp].forEach(pz => {
        const pStart = new THREE.Vector3(indTakeoff.x, indTakeoff.y, indTakeoff.z + pz);
        const p1 = new THREE.Vector3(indTowers[0].x, indTowers[0].y, indTowers[0].z + pz);
        const p2 = new THREE.Vector3(indTowers[1].x, indTowers[1].y, indTowers[1].z + pz);
        const p3 = new THREE.Vector3(indTowers[2].x, indTowers[2].y, indTowers[2].z + pz);
        const pCust = new THREE.Vector3(custPortalX, indLineH * 0.68, indSubZ + pz);
        distGroup.add(
          createCatenaryJumper(pStart, p1, 0.85, 8, MatLib.copperConductor, vIndTag, 'ind_hv'),
          createCatenaryJumper(p1, p2, 1.05, 8, MatLib.copperConductor, vIndTag, 'ind_hv'),
          createCatenaryJumper(p2, p3, 1.05, 8, MatLib.copperConductor, vIndTag, 'ind_hv'),
          createCatenaryJumper(p3, pCust, 0.72, 7, MatLib.copperConductor, vIndTag, 'ind_hv')
        );
      });

      // Isolated Customer 25 MVA Substation & Heavy Steel Mill Complex (Zero City Feeder Overlap)
      const custPad = new THREE.Mesh(new THREE.BoxGeometry(34.0, 0.14, 28.0), MatLib.concrete);
      custPad.position.set(indSubX + 2.0, 0.07, indSubZ);
      distGroup.add(custPad);
      const custWallMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.88 });
      [[indSubX + 2.0, indSubZ - 14.0, 34.0, 0.3], [indSubX - 15.0, indSubZ, 0.3, 28.0], [indSubX + 19.0, indSubZ, 0.3, 28.0]].forEach(([wx, wz, ww, wd]) => {
        const cw = new THREE.Mesh(new THREE.BoxGeometry(ww, 3.0, wd), custWallMat);
        cw.position.set(wx, 1.5, wz);
        distGroup.add(cw);
      });
      // Customer 52-CUST HV Breaker
      const indSpecCust = Object.assign({}, T.vSpec, { hvKv: indTakeoff.kv, insScale: indTakeoff.kv >= 138 ? 1.4 : 1.0, phaseSpacing: indSp, shedsCount: 12 });
      const custCb = createCompactBreakerUnit(indSubX - 6.5, 0, indSubZ, 0, '52-CUST', indSpecCust, 'ind_hv');
      distGroup.add(custCb);
      const custCbY = custCb.userData.termHeight || 4.0;
      const custCbO = custCb.userData.termOffsetX || 1.1;
      // 25 MVA Customer Step-Down Power Transformer (dt_ind_1500 w/ preserved dt-* explodeable subparts)
      const indTxGroup = buildDetailedDistributionTransformer('dt_ind_1500', indSubX - 0.5, 0, indSubZ, {
        type: 'pad',
        scale: 1.65,
        kvaLabel: (T.vSpec.indCustMva || 25) + ' MVA ' + indTakeoff.kv + 'kV',
        accentHex: '#fbbf24',
        dropTargets: [{ x: indSubX + 5.0, y: 1.4, z: indSubZ }]
      });
      [-indSp, 0, indSp].forEach((pz, pIdx) => {
        distGroup.add(createCatenaryJumper(new THREE.Vector3(custPortalX, indLineH * 0.68, indSubZ + pz), new THREE.Vector3(indSubX - 6.5 - custCbO, custCbY, indSubZ + pz), 0.35, 5, MatLib.copperConductor, vIndTag, 'ind_hv'));
        distGroup.add(createCatenaryJumper(new THREE.Vector3(indSubX - 6.5 + custCbO, custCbY, indSubZ + pz), new THREE.Vector3(indSubX - 1.2, 2.85, indSubZ + (pIdx - 1) * 0.35), 0.35, 5, MatLib.copperConductor, vIndTag, 'ind_hv'));
      });
      // Customer 4.16 kV Switchgear House, Heavy Steel Mill & Arc Furnace Complex, Cooling Towers & Harmonic Filter
      const custSwgrHouse = new THREE.Mesh(new THREE.BoxGeometry(5.8, 3.8, 7.6), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55 }));
      custSwgrHouse.position.set(indSubX + 6.2, 1.9, indSubZ);
      const steelMillHall = new THREE.Mesh(new THREE.BoxGeometry(12.5, 6.2, 8.2), new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.4, roughness: 0.5 }));
      steelMillHall.position.set(indSubX + 11.5, 3.1, indSubZ + 7.5);
      const indGlowMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24 });
      distGroup.userData.loadLights.ind.push(indGlowMat);
      const millBayWin = new THREE.Mesh(new THREE.PlaneGeometry(10.2, 1.4), indGlowMat);
      millBayWin.position.set(indSubX + 11.5, 4.0, indSubZ + 3.38);
      millBayWin.rotation.y = Math.PI;
      [-3.5, 3.5].forEach(sx => {
        const stack = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.54, 4.2, 12), MatLib.radiatorFin);
        stack.position.set(indSubX + 11.5 + sx, 8.2, indSubZ + 7.5);
        const coolTwr = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.55, 4.0, 12), MatLib.galvanizedSteel);
        coolTwr.position.set(indSubX + 11.5 + sx, 2.0, indSubZ - 7.5);
        distGroup.add(stack, coolTwr);
      });
      const harmonicRack = new THREE.Mesh(new THREE.BoxGeometry(3.2, 1.9, 1.4), MatLib.galvanizedSteel);
      harmonicRack.position.set(indSubX + 5.5, 0.95, indSubZ - 8.2);
      const indTxPlate = addTextPlate(`CUST INDUSTRIAL ${T.vSpec.indCustMva || 25}MVA (${indTakeoff.kv}kV)`, indSubX + 2.0, 7.6, indSubZ, '#fbbf24');
      indTxPlate.userData.componentId = 'dt_ind_1500';
      distGroup.add(indTxGroup, custSwgrHouse, steelMillHall, millBayWin, harmonicRack, indTxPlate);

      // 10. 79-TIE1 RECLOSER POLE ASSEMBLY + SCADA FLISR RTU CABINET AT MID-CITY LOOP 1 BOUNDARY (tieCityX, z1)
      const subBGroup = new THREE.Group();
      subBGroup.name = 'substation_b';
      subBGroup.position.set(tieCityX, 0, z1);
      subBGroup.userData = { componentId: 'substation_b', subparts: {}, tag: '79-TIE' };

      const subbTieSub = new THREE.Group();
      const tieBox = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.48, lvSp * 2 + 0.5), MatLib.galvanizedSteel);
      tieBox.position.set(0, lineY - 0.7, 0);
      const tieFlag = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.24, 0.24), new THREE.MeshBasicMaterial({ color: 0x10b981 }));
      tieFlag.position.set(0.35, 2.35, 0.15);
      const tieCtrl = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.60, 0.34), MatLib.relayPanelSteel);
      tieCtrl.position.set(0.30, 1.95, 0.15);
      subbTieSub.add(tieBox, tieCtrl, tieFlag);
      pzOffs.forEach(pz => {
        const tp = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.56, 12), MatLib.porcelainGray);
        tp.position.set(0, lineY - 0.22, pz);
        subbTieSub.add(tp);
      });

      const subbBusSub = new THREE.Group();
      const sbTiePortal = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.32, lvSp * 2 + 1.2), MatLib.galvanizedSteel);
      sbTiePortal.position.set(1.4, lineY - 0.15, 0);
      subbBusSub.add(sbTiePortal);

      const subbRtuSub = new THREE.Group();
      const sbRtu = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.1, 1.5), MatLib.relayPanelSteel);
      sbRtu.position.set(1.2, 1.15, -2.4);
      subbRtuSub.add(sbRtu);

      sbTxGrp.userData.basePos = sbTxGrp.position.clone();
      Object.entries({ 'subb-tie-recloser': subbTieSub, 'subb-bus-rack': subbBusSub, 'subb-rtu': subbRtuSub }).forEach(([id, grp]) => {
        grp.name = id; grp.userData.basePos = grp.position.clone(); tagSubpartHierarchy(grp, id);
        grp.traverse(c => { c.userData.componentId = 'substation_b'; });
        subBGroup.add(grp); subBGroup.userData.subparts[id] = grp;
      });
      subBGroup.userData.subparts['subb-xfmr'] = sbTxGrp;
      subBGroup.userData.tieFlag = tieFlag;
      const sbPlate = addTextPlate(`SUBSTATION B (${LB.scheme.toUpperCase()} / ${LB.enclosure.toUpperCase()})`, subBOriginX - LB.txX - tieCityX, 11.8, subBOriginZ - LB.txZ - z1, '#10b981');
      sbPlate.scale.set(7.5, 1.4, 1);
      sbPlate.userData.componentId = 'substation_b';
      const tiePlate = addTextPlate('79-TIE1 (NO)', 0, lineY + 1.45, 0, '#10b981');
      tiePlate.userData.componentId = 'substation_b';
      subBGroup.add(sbPlate, tiePlate);
      distGroup.add(subBGroup);
      distGroup.userData.unbundled.substation_b = subBGroup;
      distGroup.userData.unbundled.substation_gate_b = subBEnv.userData.gateGroup;
      distGroup.userData.subBEnv = subBEnv;
      distGroup.userData.subBYardGroup = subBYardGroup;
      distGroup.userData.subBLayout = LB;
      distGroup.userData.subBOriginX = subBOriginX;
      distGroup.userData.subBOriginZ = subBOriginZ;
      distGroup.userData.subBMidWorldX = subBMidWorldX;
      distGroup.userData.subBMidWorldZ = subBMidWorldZ;
      distGroup.userData.cityStartX = cityStartX;
      distGroup.userData.cityEndX = cityEndX;
      distGroup.userData.switches['79-TIE'] = subBGroup;

      scene.add(distGroup);
      return distGroup;
    }
    """

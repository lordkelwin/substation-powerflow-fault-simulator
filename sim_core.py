"""
sim_core.py
Core application logic, Three.js render loop, camera presets, exploded view animation,
power flow particles, fault simulator, SLD live sync, and quiz/switching challenge engine.
"""

def get_js_app_core():
    return """
    // Global Error Handler for On-Screen Diagnostic Banner
    window.onerror = function(msg, url, line, col, error) {
      console.error("3D ENGINE EXCEPTION:", msg, "at", url, line, col, error);
      const banner = document.getElementById('runtime-error-banner');
      const msgEl = document.getElementById('runtime-error-msg');
      if (banner && msgEl) {
        banner.style.display = 'block';
        msgEl.innerText = `${msg}\\nLocation: ${url || 'inline'}:${line}:${col}\\n${error && error.stack ? error.stack : ''}`;
      }
    };

    // Application State
    const AppState = {
      mode: 'field', // 'field' or 'explode'
      isWalkMode: false,
      powerFlowActive: true,
      groundXrayActive: false,
      rollingSphereActive: false,
      ctrlRoofManualCutaway: false,
      encCutaway: true,
      busTopology: 'single',
      enclosureType: 'ais', // 'ais' | 'gis' | 'indoor'
      voltageClass: '69_13', // '69_13' | '138_69' | '230_138'
      pfLoadPct: 100,
      pfPowerFactor: 0.92,
      oltcTapPct: 0,
      scFaultLoc: 'lv_bus',
      scFaultType: '3ph',
      scNgrGrounded: true,
      activeAnalysisTab: 'pf',
      selectedComponent: 'transformer',
      explodePercentage: 0,
      autoRotate: false,
      currentDrawerTab: 'specs',
      breakerClosed: true,
      disconnectClosed: true,
      earthClosed: false,
      switchStates: {
        dsMain: true, cbMain: true, dsMainB: true, earthMain: false,
        dsBT: true, cbBT: false, dsBYP: false,
        cb1: true, ds1A: true, ds1B: true,
        cb2: true, ds2A: true, ds2B: true,
        cb3: true, ds3A: true, ds3B: true,
        cb4: true, ds4A: true, ds4B: true,
        cbA: true, dsA1: true, dsA2: true,
        cbTIE: true, dsT1: true, dsT2: true,
        cbB: true, dsB1: true, dsB2: true,
        cb1A: true, ds1A1: true, ds1A2: true,
        cb1B: true, ds1B1: true, ds1B2: true,
        cb2A: true, ds2A1: true, ds2A2: true,
        cb2B: true, ds2B1: true, ds2B2: true,
        dsLV: true, cbLV: true, dsLVB: true,
        dsCapA: true, cbCap: true, dsCapB: true,
        dsF1A: true, cbF1: true, dsF1B: true,
        dsF2A: true, cbF2: true, dsF2B: true,
        cbACR1: true, sec34: true, fuseCutout: true, cbTieB: false,
        dsIndA: true, cbIndHv: true, dsIndB: true,
        cbF2Rec: true, cbTie2: false,
        dsLVBA: true, cbLVB: true, dsLVBB: true,
        dsF3A: true, cbF3: true, dsF3B: true,
        dsF4A: true, cbF4: true, dsF4B: true
      },
      activeProtectionZone3D: null,
      flisrRestored: false,
      liveTelemetryOpen: false,
      targetSubstation: 'A',
      subBTopology: 'ring',
      subBEnclosure: 'ais',
      gateAOpen: false,
      gateBOpen: false,
      cityGateOpen: false,
      wallCutawayActive: false,
      collisionBoxes: [],
      hvDangerSuppressedUntilSafe: false,
      isHazardModalLocked: false,
      lastHazardPos: null,
      nearestSafePos: { x: 0, z: 0 },
      walkFocusedTarget: null,
      isFaultActive: false,
      faultType: 'none',
      surgeCounter: 14,
      score: 0,
      currentQuizIndex: 0,
      switchingStepIndex: 0,
      activeDrillScenario: 'B',
      drillStepIndex: 0,
      yardBounds: { minX: -30, maxX: 52, minZ: -24, maxZ: 24 },
      ctrlHousePos: { x: 23.0, z: 14.5 },
      flowStartX: -20,
      flowEndX: 40,
      pinpointFaultMode: false,
      pinpointFaultNode: 'node5_lv_bus',
      pinpointFeederDistPct: 50,
      pinpointWorldPos: null,
      sldExpOpen: false,
      sldZoom: 1.0,
      sldPanX: 0,
      sldPanY: 0,
      urdXrayActive: true,
      pqState: {
        scenario: 'sag_swell',
        sagDepthPu: 0.72,
        swellMagPu: 1.18,
        eventMode: 'sag',
        eventCycles: 3.5,
        faultClearingCycles: 5,
        vfdLoadPct: 35,
        h3Pct: 14,
        h5Pct: 18,
        h7Pct: 11,
        h11Pct: 6,
        detunedFilterOn: false,
        nativePf: 0.78,
        capStageMvar: 3.6,
        unbalancePct: 3.2,
        singlePhaseLoadKw: 850,
        transientType: 'cap_energize',
        saClampActive: true,
        eafSeverity: 60,
        statcomActive: false,
        oscPaused: false,
        probeNodeA: 'bus_a_138',
        probeNodeB: 'tr01_pri_delta',
        showOverlayB: true
      },
      tccState: {
        topo: 'single',
        refSide: 'lv',
        splitContingency: false,
        cursorAmp: 4200,
        focusedRelay: 'all',
        viewMode: 'highlight',
        pinnedFault: null
      },
      mvaScaling: {
        mode: 'autosize',
        txMvaOverride: null,
        subBTxMva: 15,
        resKva: 50,
        urdKva: 900,
        cbdKva: 750,
        uniKva: 500,
        munKva: 1000,
        indMva: 25.0
      }
    };

    // Three.js Globals
    let scene, camera, renderer, controls;
    let clock, raycaster, mouse;
    let switchyardObjects = {};
    let solidColliders = [];
    let faultMarker3D = null;
    let pinpointTripTimer = null;
    let pqAnimFrameId = null;
    let pqPhaseOffset = 0;
    let powerParticles, leaderLinesGroup;
    let powerFlowCurves = [];
    let powerParticleMeta = [];
    let activeCameraTweenId = 0;
    let dynamicArcLight;

    // Camera Presets (Position and LookAt Target in 3D Switchyard)
    const CAMERA_PRESETS = {
      overview: { pos: [-26, 26, 36], target: [8, 3, 0] },
      gantry: { pos: [-24, 12, 10], target: [-18, 7, 0] },
      arrester: { pos: [-16, 6, 6], target: [-12, 4, 0] },
      ctvt: { pos: [-11, 6, 6], target: [-7.5, 4, 0] },
      disconnect: { pos: [-6, 6, 5], target: [-2, 3.5, 0] },
      breaker: { pos: [2, 5, 6], target: [6, 3, 0] },
      transformer: { pos: [10, 8, 9], target: [16, 3.5, 0] },
      busbar: { pos: [0, 14, 18], target: [0, 6, 0] },
      control: { pos: [16.5, 5.4, 15.8], target: [22.2, 1.6, 11.4] },
      ground: { pos: [6, 22, 28], target: [6, 0, 0] },
      secondary: { pos: [18, 9.5, 13], target: [26, 2.5, 0] },
      feeders: { pos: [28, 10.5, 15], target: [38, 3.2, 0] },
      recloser: { pos: [70, 10, 14], target: [86, 5, -6] },
      cutout_loads: { pos: [215, 28, 46], target: [236, 4.5, 0] },
      city_gate: { pos: [164, 10.5, 36], target: [182, 3.2, 22] },
      industrial: { pos: [115, 24, -40], target: [144, 5, -86] },
      substation_b: { pos: [470, 28, 52], target: [540, 5.5, 0] }
    };

    // First-Person Walk Controls State
    const WalkState = {
      moveForward: false,
      moveBackward: false,
      moveLeft: false,
      moveRight: false,
      velocity: new THREE.Vector3(),
      direction: new THREE.Vector3(),
      isMouseDown: false,
      lastMouseX: 0,
      lastMouseY: 0,
      pitch: 0,
      yaw: 0
    };

    // INIT FUNCTION
    function init() {
      try {
        const canvas = document.getElementById('canvas3d');
        if (!canvas) throw new Error("Could not find canvas3d element.");

        // 1. Scene & Atmospheric Background (Deep Slate Blue, not pitch black)
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);
        scene.fog = new THREE.FogExp2(0x0f172a, 0.00048);

        clock = new THREE.Clock();
        raycaster = new THREE.Raycaster();
        mouse = new THREE.Vector2();

        // Canvas Dimensions
        const width = window.innerWidth || 800;
        const height = window.innerHeight || 600;

        camera = new THREE.PerspectiveCamera(50, width / height, 0.2, 3200);

        renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;

        // 2. Instantiate OrbitControls BEFORE calling setCameraPreset! (Panning + Orbit + Zoom unlocked)
        if (typeof THREE.OrbitControls === 'function') {
          controls = new THREE.OrbitControls(camera, renderer.domElement);
          controls.enableDamping = true;
          controls.dampingFactor = 0.06;
          controls.enablePan = true;
          controls.screenSpacePanning = true;
          controls.panSpeed = 1.25;
          controls.enableRotate = true;
          controls.enableZoom = true;
          controls.maxPolarAngle = Math.PI / 2 - 0.02; // Prevent going below ground
          controls.minDistance = 2.0;
          controls.maxDistance = 1100.0;
          controls.addEventListener('start', () => { activeCameraTweenId++; });
          renderer.domElement.addEventListener('contextmenu', e => e.preventDefault());
        } else {
          console.warn("THREE.OrbitControls not found. Fallback dummy controls initialized.");
          controls = { target: new THREE.Vector3(), update: () => {}, enabled: true };
        }

        // 3. Set camera position and target
        setCameraPreset('overview', false);

        // 4. Strong, Bright Multi-Source Lighting
        setupLighting();

        // 5. Build 3D Switchyard Mesh Hierarchy
        buildSubstationYard();
        setupPowerFlowParticles();

        leaderLinesGroup = new THREE.Group();
        leaderLinesGroup.name = 'leaderLines';
        scene.add(leaderLinesGroup);

        // 6. Listeners (strict canvas-only pointerdown/up drag-threshold prevents UI click bleed-through)
        window.addEventListener('resize', onWindowResize);
        let pointerDownPos = { x: 0, y: 0, active: false };
        renderer.domElement.addEventListener('pointerdown', (e) => {
          if (e.target !== renderer.domElement) return;
          pointerDownPos = { x: e.clientX, y: e.clientY, active: true };
        });
        renderer.domElement.addEventListener('pointerup', (e) => {
          if (!pointerDownPos.active) return;
          pointerDownPos.active = false;
          if (e.target !== renderer.domElement || isAnyModalOpen()) return;
          const distPx = Math.hypot(e.clientX - pointerDownPos.x, e.clientY - pointerDownPos.y);
          if (distPx < 5) {
            onCanvasClick(e);
          }
        });
        setupWalkEventListeners();

        // 7. UI Initializations
        updateTelemetryUI();
        renderLiveSLD();
        selectComponent('transformer', false);

        // 8. Start Animation Loop safely
        animate();
        console.log("Substation and Distribution Simulation successfully initialized.");
      } catch (err) {
        console.error("FATAL INITIALIZATION ERROR:", err);
        const banner = document.getElementById('runtime-error-banner');
        const msgEl = document.getElementById('runtime-error-msg');
        if (banner && msgEl) {
          banner.style.display = 'block';
          msgEl.innerText = `Initialization Exception:\\n${err.message}\\n${err.stack || ''}`;
        }
      }
    }

    // LIGHTING SETUP: Bright diffuse and directional illumination
    function setupLighting() {
      // 1. Strong Ambient Light for diffuse visibility of all apparatus
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
      scene.add(ambientLight);

      // 2. Hemisphere Light (sky light / ground bounce)
      const hemiLight = new THREE.HemisphereLight(0xe0f2fe, 0x334155, 0.7);
      hemiLight.position.set(0, 50, 0);
      scene.add(hemiLight);

      // 3. Main Sun Light (Key Light)
      const sunLight = new THREE.DirectionalLight(0xffffff, 1.25);
      sunLight.position.set(35, 55, 30);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 2048;
      sunLight.shadow.mapSize.height = 2048;
      sunLight.shadow.camera.near = 10;
      sunLight.shadow.camera.far = 160;
      sunLight.shadow.camera.left = -45;
      sunLight.shadow.camera.right = 45;
      sunLight.shadow.camera.top = 45;
      sunLight.shadow.camera.bottom = -45;
      sunLight.shadow.bias = -0.0004;
      scene.add(sunLight);

      // 4. Electric Blue Fill Light from opposite side
      const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.65);
      fillLight.position.set(-35, 35, -30);
      scene.add(fillLight);

      // 5. Dynamic Point Light for electrical arcs & lightning
      dynamicArcLight = new THREE.PointLight(0x00f0ff, 0, 50, 2);
      dynamicArcLight.position.set(0, 6, 0);
      scene.add(dynamicArcLight);
    }

    function toggleEnclosureCutaway(isCutaway) {
      AppState.encCutaway = !!isCutaway;
      const enc = switchyardObjects.enclosure;
      if (enc && enc.userData && enc.userData.shells) {
        enc.userData.shells.forEach(s => {
          if (s && s.material) {
            s.material.opacity = AppState.encCutaway ? 0.16 : 0.90;
            s.material.needsUpdate = true;
          }
        });
      }
      if (typeof buildCollisionBoxes === 'function') buildCollisionBoxes();
    }

    function registerUnbundledSwitchyardObjects() {
      ['env', 'auxiliary', 'secondary', 'feeders', 'distribution'].forEach(parentKey => {
        const grp = switchyardObjects[parentKey];
        if (grp && grp.userData && grp.userData.unbundled) {
          Object.entries(grp.userData.unbundled).forEach(([k, uObj]) => {
            switchyardObjects[k] = uObj;
          });
        }
      });
      if (scene && typeof scene.updateMatrixWorld === 'function') scene.updateMatrixWorld(true);
    }

    // BUILD COMPLETE 3D SUBSTATION SWITCHYARD
    function buildSubstationYard() {
      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);
      switchyardObjects.env = buildSwitchyardEnvironment(scene, L);
      switchyardObjects.gantry = buildGantryAndLines(scene, L);
      switchyardObjects.arrester = buildSurgeArresters(scene, L);
      switchyardObjects.ctvt = buildInstrumentTransformers(scene, L);
      switchyardObjects.disconnect = buildDisconnectSwitch(scene, L);
      switchyardObjects.breaker = buildCircuitBreaker(scene, L);
      switchyardObjects.transformer = buildPowerTransformer(scene, L);
      switchyardObjects.busbar = buildBusbarSystem(scene, AppState.busTopology, AppState.enclosureType, L);
      switchyardObjects.auxiliary = buildStationService(scene, L);
      switchyardObjects.secondary = buildSecondaryBay(scene, L);
      switchyardObjects.feeders = buildFeederBays(scene, L);
      switchyardObjects.distribution = buildDistributionNetwork(scene, L, {
        mainRoadZ: switchyardObjects.env?.userData?.mainRoadZ,
        indTakeoff: switchyardObjects.feeders?.userData?.indTakeoffWorld
      });
      switchyardObjects.enclosure = buildEnclosureArchitecture(scene, L, AppState.enclosureType);
      switchyardObjects.groundGrid = buildGroundingGrid(scene, L);
      switchyardObjects.rollingSphere = buildRollingSphereShielding(scene, L);
      registerUnbundledSwitchyardObjects();
      applySubstationLayout(AppState.busTopology, false, false);
    }

    function applySubstationLayout(scheme, rebuildEnv = true, rebuildPrimary = false) {
      const L = getBusLayoutConfig(scheme, AppState.enclosureType, AppState.voltageClass);
      AppState.yardBounds = {
        minX: L.yardCenterX - L.yardW / 2 + 2.0,
        maxX: L.yardCenterX + L.yardW / 2 - 2.0,
        minZ: L.yardCenterZ - L.yardL / 2 + 2.0,
        maxZ: L.yardCenterZ + L.yardL / 2 - 2.0
      };
      AppState.ctrlHousePos = { x: L.ctrlX, z: L.ctrlZ };
      AppState.flowStartX = L.gantryX;
      AppState.flowEndX = L.fdrGantryX;

      if (rebuildPrimary) {
        ['gantry', 'arrester', 'ctvt', 'disconnect', 'breaker', 'transformer'].forEach(k => {
          if (switchyardObjects[k]) scene.remove(switchyardObjects[k]);
        });
        switchyardObjects.gantry = buildGantryAndLines(scene, L);
        switchyardObjects.arrester = buildSurgeArresters(scene, L);
        switchyardObjects.ctvt = buildInstrumentTransformers(scene, L);
        switchyardObjects.disconnect = buildDisconnectSwitch(scene, L);
        switchyardObjects.breaker = buildCircuitBreaker(scene, L);
        switchyardObjects.transformer = buildPowerTransformer(scene, L);
      }

      // Update Dynamic Camera Presets to frame expanded Primary + Secondary + Feeder Yard
      CAMERA_PRESETS.overview = {
        pos: [L.yardCenterX - L.yardW * 0.44, Math.max(24, L.yardL * 0.42), L.yardL * 0.62],
        target: [L.yardCenterX, 3, L.yardCenterZ]
      };
      CAMERA_PRESETS.gantry = { pos: [L.gantryX - 6, 12, 10], target: [L.gantryX, 7, 0] };
      CAMERA_PRESETS.arrester = { pos: [L.laX - 5, 6, 6], target: [L.laX, 4, 0] };
      CAMERA_PRESETS.ctvt = { pos: [L.ctX - 4, 6, 6], target: [L.ctX, 4, 0] };
      CAMERA_PRESETS.disconnect = { pos: [L.dsX - 4, 6, 5], target: [L.dsX, 3.5, L.dsZ] };
      CAMERA_PRESETS.breaker = { pos: [L.cbX - 5, 6, 7], target: [L.cbX, 3, L.cbZ] };
      CAMERA_PRESETS.transformer = { pos: [L.txX - 6, 8, 9], target: [L.txX, 3.5, L.txZ] };
      CAMERA_PRESETS.busbar = {
        pos: [L.cbX - 4, Math.max(16, L.yardL * 0.25), Math.max(20, L.yardL * 0.42)],
        target: [L.cbX + 3, 6, 0]
      };
      CAMERA_PRESETS.control = {
        pos: [L.ctrlX - 5.5, 5.4, L.ctrlZ + 3.8],
        target: [L.ctrlX + 0.2, 1.6, L.ctrlZ - 0.6]
      };
      CAMERA_PRESETS.ground = {
        pos: [L.yardCenterX, Math.max(20, L.yardL * 0.36), L.yardL * 0.54],
        target: [L.yardCenterX, 0, L.yardCenterZ]
      };
      CAMERA_PRESETS.secondary = {
        pos: [L.secCbX - 5.5, 8.8, 12.5],
        target: [L.secCbX + 2.0, 2.2, 0]
      };
      CAMERA_PRESETS.feeders = {
        pos: [L.secBusX + 1.5, 10.5, 15.0],
        target: [L.fdrGantryX - 2.5, 3.2, 0]
      };
      const distStartX = L.fdrGantryX + 18.95;
      const cityStartX = +(distStartX + 140.0).toFixed(2);
      const cityEndX = +(cityStartX + 98.0).toFixed(2);
      const eastEntryX = +(cityEndX + 140.0).toFixed(2);
      CAMERA_PRESETS.recloser = {
        pos: [distStartX + 14.5, 10.2, L.fdr1Z + 14.0],
        target: [distStartX + 28.0, 5.2, L.fdr1Z]
      };
      CAMERA_PRESETS.cutout_loads = {
        pos: [cityStartX + 32.0, 28.0, L.fdr1Z + 52.0],
        target: [cityStartX + 49.0, 4.5, (L.fdr1Z + L.fdr2Z) / 2]
      };
      const mainRoadZ_cam = switchyardObjects.env?.userData?.mainRoadZ || (L.yardMaxZ + 11.5);
      CAMERA_PRESETS.city_gate = {
        pos: [cityStartX - 24.0, 10.5, mainRoadZ_cam + 18.0],
        target: [cityStartX - 6.0, 3.2, mainRoadZ_cam]
      };
      const indSubZ_cam = Math.min(L.yardMinZ - 38.0, L.fdr1Z - 68.0);
      CAMERA_PRESETS.industrial = {
        pos: [distStartX + 58.0, 24.0, indSubZ_cam + 46.0],
        target: [distStartX + 86.0, 5.0, indSubZ_cam]
      };
      const LB_cam = getBusLayoutConfig(AppState.subBTopology || 'ring', AppState.subBEnclosure || 'ais', AppState.voltageClass);
      const subBOriginX_cam = +(eastEntryX + (LB_cam.fdrGantryX + 18.95)).toFixed(2);
      const subBOriginZ_cam = +(L.fdr1Z + LB_cam.fdr1Z).toFixed(2);
      CAMERA_PRESETS.substation_b = {
        pos: [subBOriginX_cam - LB_cam.txX - 42.0, 28.0, subBOriginZ_cam + 52.0],
        target: [subBOriginX_cam - LB_cam.txX, 5.5, subBOriginZ_cam]
      };

      // Reposition primary HV bay assemblies to IEEE-compliant bay offsets
      if (switchyardObjects.gantry) switchyardObjects.gantry.position.set(L.gantryX, 0, 0);
      if (switchyardObjects.arrester) switchyardObjects.arrester.position.set(L.laX, 0, 0);
      if (switchyardObjects.ctvt) switchyardObjects.ctvt.position.set(L.ctX, 0, 0);
      if (switchyardObjects.disconnect) {
        switchyardObjects.disconnect.position.set(L.dsX, 0, L.dsZ);
        switchyardObjects.disconnect.rotation.y = L.dsRot;
      }
      if (switchyardObjects.breaker) {
        switchyardObjects.breaker.position.set(L.cbX, 0, L.cbZ);
        switchyardObjects.breaker.rotation.y = L.cbRot;
      }
      if (switchyardObjects.transformer) switchyardObjects.transformer.position.set(L.txX, 0, L.txZ);

      if (rebuildEnv) {
        if (switchyardObjects.env) scene.remove(switchyardObjects.env);
        switchyardObjects.env = buildSwitchyardEnvironment(scene, L);

        if (switchyardObjects.busbar) scene.remove(switchyardObjects.busbar);
        switchyardObjects.busbar = buildBusbarSystem(scene, scheme, AppState.enclosureType, L);

        if (switchyardObjects.auxiliary) scene.remove(switchyardObjects.auxiliary);
        switchyardObjects.auxiliary = buildStationService(scene, L);

        if (switchyardObjects.secondary) scene.remove(switchyardObjects.secondary);
        switchyardObjects.secondary = buildSecondaryBay(scene, L);

        if (switchyardObjects.feeders) scene.remove(switchyardObjects.feeders);
        switchyardObjects.feeders = buildFeederBays(scene, L);

        if (switchyardObjects.distribution) scene.remove(switchyardObjects.distribution);
        switchyardObjects.distribution = buildDistributionNetwork(scene, L, {
          mainRoadZ: switchyardObjects.env?.userData?.mainRoadZ,
          indTakeoff: switchyardObjects.feeders?.userData?.indTakeoffWorld
        });

        if (switchyardObjects.protectionOverlay) scene.remove(switchyardObjects.protectionOverlay);
        switchyardObjects.protectionOverlay = AppState.activeProtectionZone3D ? buildProtectionZoneOverlay(scene, L, AppState.activeProtectionZone3D) : null;

        if (switchyardObjects.enclosure) scene.remove(switchyardObjects.enclosure);
        switchyardObjects.enclosure = buildEnclosureArchitecture(scene, L, AppState.enclosureType);

        if (switchyardObjects.groundGrid) scene.remove(switchyardObjects.groundGrid);
        switchyardObjects.groundGrid = buildGroundingGrid(scene, L);
        switchyardObjects.groundGrid.visible = AppState.groundXrayActive;

        if (switchyardObjects.rollingSphere) scene.remove(switchyardObjects.rollingSphere);
        switchyardObjects.rollingSphere = buildRollingSphereShielding(scene, L);
        switchyardObjects.rollingSphere.visible = AppState.rollingSphereActive;

        registerUnbundledSwitchyardObjects();
        if (typeof syncGateVisualsTo3D === 'function') syncGateVisualsTo3D();
        if (typeof syncWallCutawayVisualsTo3D === 'function') syncWallCutawayVisualsTo3D();
      }

      // Toggle GIS outdoor primary air-insulated masts when housed in pressurized SF6 GIS hall
      const showOutdoorPrimary = (AppState.enclosureType !== 'gis');
      ['arrester', 'ctvt', 'disconnect', 'breaker', 'busbar'].forEach(k => {
        if (switchyardObjects[k]) switchyardObjects[k].visible = showOutdoorPrimary;
      });
      if (switchyardObjects.gantry && switchyardObjects.gantry.userData && switchyardObjects.gantry.userData.subparts) {
        const gtBus = switchyardObjects.gantry.userData.subparts['gantry-tubular-bus'];
        if (gtBus) gtBus.visible = showOutdoorPrimary;
      }
      if (switchyardObjects.secondary && switchyardObjects.secondary.userData && switchyardObjects.secondary.userData.lvBreaker) {
        switchyardObjects.secondary.userData.lvBreaker.visible = (AppState.enclosureType !== 'indoor');
      }
      toggleEnclosureCutaway(AppState.encCutaway);
      if (typeof syncGateVisualsTo3D === 'function') syncGateVisualsTo3D();
      if (AppState.mode === 'explode' && typeof applyExplodedTransform === 'function') {
        applyExplodedTransform(AppState.selectedComponent, AppState.explodePercentage / 100);
      }
      if (typeof buildCollisionBoxes === 'function') buildCollisionBoxes();

      if (typeof syncAllSwitchesTo3D === 'function') syncAllSwitchesTo3D();
      if (typeof renderSwitchMatrix === 'function') renderSwitchMatrix();
      if (typeof updateSubtitleAndTelemetry === 'function') updateSubtitleAndTelemetry();
    }

    function setVoltageClass(vClass) {
      if (!VOLTAGE_CLASSES[vClass]) return;
      AppState.voltageClass = vClass;
      document.querySelectorAll('[id^="vclass-opt-"]').forEach(el => el.classList.remove('selected'));
      const opt = document.getElementById(`vclass-opt-${vClass}`);
      if (opt) opt.classList.add('selected');
      applySubstationLayout(AppState.busTopology, true, true);
      if (!AppState.isWalkMode && AppState.mode !== 'explode') {
        setCameraPreset('overview');
      }
      renderLiveSLD();
      const vs = getVoltageSpec(vClass);
      showToast(`Scaled Substation Voltage Class: ${vs.shortLabel} (${vs.mva} MVA, BIL ${vs.bilHv} kV, Phase Spacing ${vs.phaseSpacing.toFixed(1)} m, MAD ${vs.mad.toFixed(1)} m)`);
    }

    function openVoltageClassModal() {
      const modal = document.getElementById('voltage-scale-modal');
      const body = document.getElementById('voltage-scale-body');
      if (!modal || !body || typeof VOLTAGE_CLASSES === 'undefined') return;
      const rows = Object.values(VOLTAGE_CLASSES);
      body.innerHTML = `
        <p style="font-size:11.5px; color:#cbd5e1; margin-bottom:10px; line-height:1.5;">
          Substation geometry, porcelain shed count, phase-to-phase spacing, corona grading rings, conductor bundling, and OSHA/IEEE C2 Minimum Approach Distance scale dynamically with system voltage rating:
        </p>
        <table class="vscale-table">
          <thead>
            <tr>
              <th>Cascading Path</th>
              <th>Public City Bus</th>
              <th>Industrial HV</th>
              <th>HV BIL</th>
              <th>Phase Spacing</th>
              <th>Sheds / Hardware</th>
              <th>MAD (IEEE C2)</th>
              <th>Cascade X / CB</th>
            </tr>
          </thead>
          <tbody>
            ${rows.map(v => `
              <tr style="${v.id === AppState.voltageClass ? 'background: rgba(14,165,233,0.16);' : ''}">
                <td style="color:${v.id === AppState.voltageClass ? '#38bdf8' : '#f1f5f9'}; font-weight:700;">${v.cascadeLabel || v.shortLabel}</td>
                <td style="color:#34d399; font-weight:700;">${(v.distKv || 13.8).toFixed(1)} kV (Fixed)</td>
                <td style="color:#fbbf24;">${v.indSubKv || 69} kV (${v.indCustMva || 25} MVA)</td>
                <td>${v.bilHv} kV</td>
                <td>${v.phaseSpacing.toFixed(1)} m</td>
                <td>${v.hvShedsCount}s · ${v.quadBundle ? 'Quad ACSR + 3×1φ' : (v.twinBundle ? 'Twin ACSR + Corona' : (v.coronaRings ? 'Corona Rings' : 'Single ACSR'))}</td>
                <td style="color:#f59e0b; font-weight:700;">${v.mad.toFixed(1)} m</td>
                <td>${(v.totalCascadeXPu || v.xPu).toFixed(3)} pu / ${v.hvCbKa} kA</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      modal.style.display = 'flex';
    }

    function closeVoltageClassModal() {
      const modal = document.getElementById('voltage-scale-modal');
      if (modal) modal.style.display = 'none';
    }

    function syncTargetSubstationUI() {
      const target = AppState.targetSubstation || 'A';
      const btnA = document.getElementById('target-sub-a');
      const btnB = document.getElementById('target-sub-b');
      if (btnA) {
        btnA.classList.toggle('active', target === 'A');
        const sp = btnA.querySelector('span');
        if (sp) sp.textContent = `${target === 'A' ? '●' : '○'} Substation A (Main)`;
      }
      if (btnB) {
        btnB.classList.toggle('active', target === 'B');
        const sp = btnB.querySelector('span');
        if (sp) sp.textContent = `${target === 'B' ? '●' : '○'} Substation B (Tie)`;
      }
      const schemeNames = {
        single: 'Single Bus',
        maintransfer: 'Main & Transfer',
        ring: 'Ring Bus',
        breakerhalf: 'Breaker & Half',
        doublebreaker: 'Double Breaker'
      };
      const encNames = { ais: 'AIS', gis: 'GIS SF₆', indoor: 'Indoor' };
      const sumA = document.getElementById('sub-a-cfg-summary');
      const sumB = document.getElementById('sub-b-cfg-summary');
      if (sumA) sumA.textContent = `${schemeNames[AppState.busTopology] || AppState.busTopology} · ${encNames[AppState.enclosureType] || 'AIS'}`;
      if (sumB) sumB.textContent = `${schemeNames[AppState.subBTopology || 'ring'] || AppState.subBTopology} · ${encNames[AppState.subBEnclosure || 'ais'] || 'AIS'}`;

      const activeTopo = (target === 'B') ? (AppState.subBTopology || 'ring') : AppState.busTopology;
      const activeEnc = (target === 'B') ? (AppState.subBEnclosure || 'ais') : AppState.enclosureType;
      document.querySelectorAll('#bus-opt-single, #bus-opt-maintransfer, #bus-opt-ring, #bus-opt-breakerhalf, #bus-opt-doublebreaker').forEach(o => o.classList.remove('selected'));
      const busEl = document.getElementById(`bus-opt-${activeTopo}`);
      if (busEl) busEl.classList.add('selected');
      document.querySelectorAll('#enc-opt-ais, #enc-opt-gis, #enc-opt-indoor').forEach(el => el.classList.remove('selected'));
      const encEl = document.getElementById(`enc-opt-${activeEnc}`);
      if (encEl) encEl.classList.add('selected');
    }

    function setTargetSubstation(target) {
      AppState.targetSubstation = (target === 'B') ? 'B' : 'A';
      syncTargetSubstationUI();
      if (!AppState.isWalkMode && AppState.mode !== 'explode') {
        setCameraPreset(AppState.targetSubstation === 'B' ? 'substation_b' : 'overview');
      }
      showToast(AppState.targetSubstation === 'B'
        ? `Target Switched: TIE SUBSTATION B (${(AppState.subBTopology || 'ring').toUpperCase()} / ${(AppState.subBEnclosure || 'ais').toUpperCase()})`
        : `Target Switched: MAIN SUBSTATION A (${AppState.busTopology.toUpperCase()} / ${AppState.enclosureType.toUpperCase()})`);
    }

    function syncWallCutawayVisualsTo3D() {
      const sy = AppState.wallCutawayActive ? 0.30 : 1.0;
      const wallA = switchyardObjects.env?.userData?.perimeterWallGroup;
      if (wallA) wallA.scale.y = sy;
      const wallB = switchyardObjects.distribution?.userData?.subBEnv?.userData?.perimeterWallGroup;
      if (wallB) wallB.scale.y = sy;
      const chk = document.getElementById('toggle-wall-cutaway');
      if (chk) chk.checked = !!AppState.wallCutawayActive;
    }

    function togglePerimeterWallCutaway(enabled) {
      AppState.wallCutawayActive = !!enabled;
      syncWallCutawayVisualsTo3D();
      showToast(`3.0m Precast Perimeter Wall Cutaway: ${AppState.wallCutawayActive ? 'CUTAWAY (0.9m Low View)' : 'FULL 3.0m SECURITY HEIGHT'}`);
    }

    function syncGateVisualsTo3D() {
      const applyDoorPose = (gateGrp, isOpen) => {
        if (!gateGrp || !gateGrp.userData) return;
        if (gateGrp.userData.leafL) gateGrp.userData.leafL.rotation.y = isOpen ? 1.48 : 0;
        if (gateGrp.userData.leafR) gateGrp.userData.leafR.rotation.y = isOpen ? -1.48 : 0;
        if (gateGrp.userData.manLeaf) gateGrp.userData.manLeaf.rotation.y = isOpen ? 1.35 : 0;
        const gSub = gateGrp.userData.subparts && gateGrp.userData.subparts['gate-guardhouse'];
        if (gSub && gSub.userData && gSub.userData.rfidLed && gSub.userData.rfidLed.material) {
          gSub.userData.rfidLed.material.color.setHex(isOpen ? 0x22c55e : 0xf59e0b);
        }
      };
      applyDoorPose(switchyardObjects.env?.userData?.gateGroup, !!AppState.gateAOpen);
      applyDoorPose(switchyardObjects.distribution?.userData?.subBEnv?.userData?.gateGroup, !!AppState.gateBOpen);
      const cg = switchyardObjects.distribution?.userData?.cityGateGroup;
      if (cg && cg.userData) {
        if (cg.userData.boomN) cg.userData.boomN.rotation.x = AppState.cityGateOpen ? -1.32 : 0;
        if (cg.userData.boomS) cg.userData.boomS.rotation.x = AppState.cityGateOpen ? 1.32 : 0;
      }
      const chk = document.getElementById('toggle-sub-gates');
      if (chk) chk.checked = !!(AppState.gateAOpen || AppState.gateBOpen || AppState.cityGateOpen);
    }

    function toggleSubstationGate(which = 'both', forceState = null) {
      if (which === 'A') {
        AppState.gateAOpen = (forceState !== null) ? !!forceState : !AppState.gateAOpen;
      } else if (which === 'B') {
        AppState.gateBOpen = (forceState !== null) ? !!forceState : !AppState.gateBOpen;
      } else if (which === 'city') {
        AppState.cityGateOpen = (forceState !== null) ? !!forceState : !AppState.cityGateOpen;
      } else {
        const next = (forceState !== null) ? !!forceState : !(AppState.gateAOpen && AppState.gateBOpen && AppState.cityGateOpen);
        AppState.gateAOpen = next;
        AppState.gateBOpen = next;
        AppState.cityGateOpen = next;
      }
      syncGateVisualsTo3D();
      if (typeof buildCollisionBoxes === 'function') buildCollisionBoxes();
      if (which === 'A') showToast(`Substation A Entrance Gate ${AppState.gateAOpen ? 'OPEN — Drive/Walk Access Unlocked' : 'CLOSED & LOCKED'}`);
      else if (which === 'B') showToast(`Substation B Entrance Gate ${AppState.gateBOpen ? 'OPEN — Drive/Walk Access Unlocked' : 'CLOSED & LOCKED'}`);
      else if (which === 'city') showToast(`Utility District & URD City Gate ${AppState.cityGateOpen ? 'BARRIER RAISED — Access Unlocked' : 'BARRIER LOWERED — Controlled Access'}`);
      else showToast(`Perimeter & City Gates (A, B, City): ${(AppState.gateAOpen && AppState.gateBOpen && AppState.cityGateOpen) ? 'ALL OPEN (Sub A ↔ City ↔ Sub B Walkable)' : 'CLOSED (Secured Perimeters)'}`);
    }

    function setEnclosureType(encType) {
      const target = AppState.targetSubstation || 'A';
      if (target === 'B') {
        AppState.subBEnclosure = encType;
        applySubstationLayout(AppState.busTopology, true, true);
        if (!AppState.isWalkMode && AppState.mode !== 'explode') {
          setCameraPreset('substation_b');
        }
      } else {
        AppState.enclosureType = encType;
        applySubstationLayout(AppState.busTopology, true, true);
        if (!AppState.isWalkMode && AppState.mode !== 'explode') {
          setCameraPreset('overview');
        }
      }
      syncTargetSubstationUI();
      renderLiveSLD();
      updateSubtitleAndTelemetry();
      const desc = {
        ais: `Substation ${target} — Outdoor Air-Insulated (AIS): Open-air phase clearances & tubular bus`,
        gis: `Substation ${target} — SF₆ Gas-Insulated (GIS): ~28% primary footprint inside sealed 450 kPa SF₆ hall`,
        indoor: `Substation ${target} — Indoor Metal-Clad Switchgear Hall (IEEE C37.20.2): Walk-in cutaway VCB cabinets`
      };
      showToast(desc[encType] || encType);
    }

    // =========================================================================
    // SUBSTATION LAND AREA CALCULATOR (ALL 5 TOPOLOGIES x 3 ENCLOSURES x 3 VOLTAGES)
    // =========================================================================
    const LAND_TOPO_FACTORS = {
      single:        { label: 'Single Bus',              cbPerCkt: '1.0 CB/ckt',  relIndex: '82% (Base)',  factor: 1.00, capex: 1.00 },
      maintransfer:  { label: 'Main & Transfer',         cbPerCkt: '1.25 CB/ckt', relIndex: '91% (Maint.)',factor: 1.28, capex: 1.32 },
      ring:          { label: 'Ring Bus',                cbPerCkt: '1.0 CB/ckt',  relIndex: '94% (N-1)',   factor: 1.18, capex: 1.25 },
      breakerhalf:   { label: 'Breaker-and-a-Half',      cbPerCkt: '1.5 CB/ckt',  relIndex: '98% (2-Bus)', factor: 1.55, capex: 1.65 },
      doublebreaker: { label: 'Double Bus–Double CB',    cbPerCkt: '2.0 CB/ckt',  relIndex: '99.9% (Max)', factor: 1.75, capex: 2.05 }
    };

    const LAND_ENC_FACTORS = {
      ais:    { label: 'Outdoor AIS',      factor: 1.00, capex: 1.00 },
      gis:    { label: 'SF₆ GIS Hall',     factor: 0.27, capex: 2.15 },
      indoor: { label: 'Indoor Metal-Clad',factor: 0.38, capex: 1.52 }
    };

    function computeSubstationLandMetrics(scheme, enclosureType, vClass) {
      const sch = LAND_TOPO_FACTORS[scheme] ? scheme : 'single';
      const enc = LAND_ENC_FACTORS[enclosureType] ? enclosureType : 'ais';
      const vc = vClass || AppState.voltageClass || '69_13';

      const baseL = (typeof getBusLayoutConfig === 'function')
        ? getBusLayoutConfig('single', 'ais', vc)
        : { yardW: 68, yardL: 48 };
      const curL = (typeof getBusLayoutConfig === 'function')
        ? getBusLayoutConfig(sch, enc, vc)
        : { yardW: 68, yardL: 48 };

      const baseSingleAisM2 = Math.round(baseL.yardW * baseL.yardL);
      const tMeta = LAND_TOPO_FACTORS[sch];
      const eMeta = LAND_ENC_FACTORS[enc];

      const sameSchemeAisM2 = Math.round(baseSingleAisM2 * tMeta.factor);
      const areaM2 = Math.round(sameSchemeAisM2 * eMeta.factor);
      const areaHa = +(areaM2 / 10000).toFixed(2);

      // Preserve 3D layout aspect ratio while locking widthM * lengthM tightly to areaM2
      const aspect = Math.max(1.05, curL.yardW / Math.max(20, curL.yardL));
      const lengthM = Math.round(Math.sqrt(areaM2 * aspect));
      const widthM = Math.max(12, Math.round(areaM2 / Math.max(12, lengthM)));

      const pctVsSingleAis = Math.round((areaM2 / baseSingleAisM2) * 100);
      const pctVsSameSchemeAis = Math.round((areaM2 / sameSchemeAisM2) * 100);
      const landSavedVsAisM2 = Math.max(0, sameSchemeAisM2 - areaM2);
      const capexMult = +(tMeta.capex * eMeta.capex).toFixed(2);

      return {
        scheme: sch,
        enclosure: enc,
        vClass: vc,
        lengthM,
        widthM,
        areaM2,
        areaHa,
        cbPerCkt: tMeta.cbPerCkt,
        relIndex: tMeta.relIndex,
        topoFactor: tMeta.factor,
        encFactor: eMeta.factor,
        baseSingleAisM2,
        sameSchemeAisM2,
        pctVsSingleAis,
        pctVsSameSchemeAis,
        landSavedVsAisM2,
        capexMult
      };
    }

    function updateLandAreaUI() {
      const top = AppState.busTopology || 'single';
      const enc = AppState.enclosureType || 'ais';
      const vc = AppState.voltageClass || '69_13';
      const cur = computeSubstationLandMetrics(top, enc, vc);

      const telemLand = document.getElementById('telem-land-area');
      if (telemLand) {
        telemLand.innerText = `${cur.lengthM}×${cur.widthM}m | ${cur.areaM2.toLocaleString()} m² (${cur.areaHa.toFixed(2)} ha)`;
      }

      ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'].forEach(k => {
        const b = document.getElementById(`bus-badge-${k}`);
        if (b) {
          const m = computeSubstationLandMetrics(k, enc, vc);
          b.innerText = `${m.cbPerCkt.replace(' CB/ckt', ' CB')} · ${m.areaM2.toLocaleString()} m² (${m.topoFactor.toFixed(2)}×)`;
        }
      });

      ['ais', 'gis', 'indoor'].forEach(eKey => {
        const b = document.getElementById(`enc-badge-${eKey}`);
        if (b) {
          const m = computeSubstationLandMetrics(top, eKey, vc);
          b.innerText = `${m.pctVsSameSchemeAis}% · ${m.areaM2.toLocaleString()} m²`;
        }
      });

      const busReadout = document.getElementById('busbar-land-area-readout');
      if (busReadout) {
        busReadout.innerHTML = `
          <div><span>Active Plot (${LAND_TOPO_FACTORS[top].label}):</span><strong style="color:#fbbf24;">${cur.lengthM} m × ${cur.widthM} m</strong></div>
          <div><span>Total Civil Area:</span><strong style="color:#38bdf8;">${cur.areaM2.toLocaleString()} m² (${cur.areaHa.toFixed(2)} ha)</strong></div>
          <div><span>Reliability / Footprint:</span><strong>${cur.relIndex} · ${cur.pctVsSingleAis}% of 1-Bus AIS</strong></div>
        `;
      }

      const encReadout = document.getElementById('enclosure-land-area-readout');
      if (encReadout) {
        const savedTxt = cur.landSavedVsAisM2 > 0
          ? `<strong style="color:#10b981;">-${cur.landSavedVsAisM2.toLocaleString()} m² saved vs AIS</strong>`
          : `<strong style="color:#94a3b8;">Baseline AIS Footprint (100%)</strong>`;
        encReadout.innerHTML = `
          <div><span>${LAND_ENC_FACTORS[enc].label} Civil Site:</span><strong style="color:#fbbf24;">${cur.areaM2.toLocaleString()} m² (${cur.pctVsSameSchemeAis}% of ${LAND_TOPO_FACTORS[top].label} AIS)</strong></div>
          <div><span>Land Space Trade-off:</span>${savedTxt}</div>
          <div><span>Est. Relative CAPEX Index:</span><strong style="color:#c084fc;">${cur.capexMult.toFixed(2)}× Base AIS</strong></div>
        `;
      }
    }

    function openEnclosureModal() {
      const body = document.getElementById('enclosure-modal-body');
      const vc = AppState.voltageClass || '69_13';
      const vs = getVoltageSpec(vc);
      const top = AppState.busTopology || 'single';
      const enc = AppState.enclosureType || 'ais';
      if (body && typeof ENCLOSURE_COMPARISON !== 'undefined') {
        const topoRows = Object.keys(LAND_TOPO_FACTORS).map(k => {
          const ais = computeSubstationLandMetrics(k, 'ais', vc);
          const gis = computeSubstationLandMetrics(k, 'gis', vc);
          const ind = computeSubstationLandMetrics(k, 'indoor', vc);
          const isCur = (k === top);
          return `
            <tr style="${isCur ? 'background:rgba(56,189,248,0.12);' : ''}">
              <td><strong style="color:#f8fafc;">${LAND_TOPO_FACTORS[k].label}</strong><div style="font-size:9.5px;color:#94a3b8;">${ais.cbPerCkt} | ${ais.relIndex}</div></td>
              <td>${ais.lengthM}×${ais.widthM}m<br><strong style="color:#fbbf24;">${ais.areaM2.toLocaleString()} m²</strong> (${ais.areaHa.toFixed(2)} ha)</td>
              <td style="color:#67e8f9;">${gis.lengthM}×${gis.widthM}m<br><strong>${gis.areaM2.toLocaleString()} m²</strong> (${gis.pctVsSameSchemeAis}%)</td>
              <td style="color:#fde68a;">${ind.lengthM}×${ind.widthM}m<br><strong>${ind.areaM2.toLocaleString()} m²</strong> (${ind.pctVsSameSchemeAis}%)</td>
            </tr>
          `;
        }).join('');

        body.innerHTML = `
          <p style="font-size:11.5px; color:#cbd5e1; margin-bottom:10px; line-height:1.5;">
            Dynamic civil land footprint &amp; engineering trade-off for <strong style="color:#38bdf8;">${vs.hvKv} / ${vs.lvKv} kV (${vs.mva} MVA)</strong>
            showing active <strong style="color:#fbbf24;">${LAND_TOPO_FACTORS[top].label} · ${LAND_ENC_FACTORS[enc].label}</strong> across all 5 busbar schemes × 3 enclosures:
          </p>
          <table class="enclosure-table" style="margin-bottom:12px;">
            <thead>
              <tr>
                <th>Busbar Topology</th>
                <th>Outdoor AIS (100%)</th>
                <th>SF₆ GIS (~27%)</th>
                <th>Indoor Metal-Clad (~38%)</th>
              </tr>
            </thead>
            <tbody>${topoRows}</tbody>
          </table>
          <table class="enclosure-table">
            <thead>
              <tr>
                <th>Engineering Parameter</th>
                <th>Outdoor AIS (Base)</th>
                <th>SF₆ Gas-Insulated (GIS)</th>
                <th>Indoor Metal-Clad (MV)</th>
              </tr>
            </thead>
            <tbody>
              ${ENCLOSURE_COMPARISON.map(r => `
                <tr>
                  <td><strong style="color:#f8fafc;">${r.metric}</strong></td>
                  <td>${r.ais}</td>
                  <td style="color:#67e8f9;">${r.gis}</td>
                  <td style="color:#fde68a;">${r.indoor}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
      }
      const m = document.getElementById('enclosure-modal');
      if (m) m.style.display = 'flex';
    }

    function closeEnclosureModal() {
      const m = document.getElementById('enclosure-modal');
      if (m) m.style.display = 'none';
    }

    // TOPOLOGY- & SWITCH-AWARE MULTI-BRANCH 3D POWER FLOW ENGINE (69 kV + 13.8 kV)
    function computeEnergizedBranches() {
      const s = AppState.switchStates;
      const top = AppState.busTopology;

      const main_path = !!(s.dsMain && s.cbMain && s.dsMainB && !s.earthMain);
      const bypass_path = (top === 'maintransfer') && !!(s.dsBT && s.cbBT && s.dsBYP);

      const ring_leg1 = !!(s.cb1 && s.ds1A && s.ds1B);
      const ring_leg2 = !!(s.cb2 && s.ds2A && s.ds2B);
      const ring_leg3 = !!(s.cb3 && s.ds3A && s.ds3B);
      const ring_leg4 = !!(s.cb4 && s.ds4A && s.ds4B);

      const bh_busA = !!(s.cbA && s.dsA1 && s.dsA2);
      const bh_tie = !!(s.cbTIE && s.dsT1 && s.dsT2);
      const bh_busB = !!(s.cbB && s.dsB1 && s.dsB2);

      const db_b1A = !!(s.cb1A && s.ds1A1 && s.ds1A2);
      const db_b1B = !!(s.cb1B && s.ds1B1 && s.ds1B2);
      const db_b2A = !!(s.cb2A && s.ds2A1 && s.ds2A2);
      const db_b2B = !!(s.cb2B && s.ds2B1 && s.ds2B2);
      const db_busA = !!(db_b1A && db_b2A);
      const db_busB = !!(db_b1B && db_b2B);

      let txFeed = false;
      if (top === 'single') {
        txFeed = main_path;
      } else if (top === 'maintransfer') {
        txFeed = main_path || bypass_path;
      } else if (top === 'ring') {
        // Incoming enters Corner 1 (NW), TR-01 taps Corner 2 (NE) -> fed if North Leg 2 OR South-East loop (1 -> 4 -> 3) is intact
        txFeed = ring_leg2 || (ring_leg1 && ring_leg4 && ring_leg3);
      } else if (top === 'breakerhalf') {
        // Line 1 enters Node 1 (between 52-A & 52-TIE); TR-01 taps Node 2 (between 52-TIE & 52-B)
        txFeed = bh_tie || (bh_busA && bh_busB);
      } else if (top === 'doublebreaker') {
        // Bay 1 (Line 1) feeds Bus A (via 52-1A) and Bus B (via 52-1B); Bay 2 (TR-01) takes power from Bus A (52-2A) and/or Bus B (52-2B)
        txFeed = db_busA || db_busB;
      }

      const post_dsA = (top === 'single' || top === 'maintransfer')
        ? !!(s.dsMain && !s.earthMain)
        : (top === 'doublebreaker' ? !!(db_b1A || db_b1B) : !!(s.dsMain));
      const post_cbMain = (top === 'single' || top === 'maintransfer') ? !!(s.dsMain && s.cbMain && !s.earthMain) : txFeed;

      const secMain = !!(txFeed && s.dsLV && s.cbLV && s.dsLVB);
      const ind_hv = !!(txFeed && s.dsIndA !== false && s.cbIndHv !== false && s.dsIndB !== false);
      const capBank = !!(secMain && s.dsCapA && s.cbCap && s.dsCapB);
      const sst100 = !!secMain;

      // TRUE BIDIRECTIONAL GRAPH CONNECTIVITY & POWER-FLOW BFS SOLVER ACROSS SUB A <-> TIES <-> SUB B
      const subBSourceOn = !!(s.cbTieA !== false && s.dsLVBA !== false && s.cbLVB !== false && s.dsLVBB !== false);
      const adj = {
        subA_lv_bus: [], fdr1_head: [], fdr1_sec1: [], fdr1_sec2: [], res_lat: [],
        fdr2_head: [], fdr2_main: [],
        subB_lv_bus: [], fdr3_east: [], fdr4_east: []
      };
      const addEdge = (u, v) => { adj[u].push(v); adj[v].push(u); };
      if (s.dsF1A && s.cbF1 && s.dsF1B) addEdge('subA_lv_bus', 'fdr1_head');
      if (s.cbACR1) addEdge('fdr1_head', 'fdr1_sec1');
      if (s.sec34) addEdge('fdr1_sec1', 'fdr1_sec2');
      if (s.fuseCutout) addEdge('fdr1_sec2', 'res_lat');
      if (s.dsF2A && s.cbF2 && s.dsF2B) addEdge('subA_lv_bus', 'fdr2_head');
      if (s.cbF2Rec !== false) addEdge('fdr2_head', 'fdr2_main');

      if (s.dsF3A !== false && s.cbF3 !== false && s.dsF3B !== false) addEdge('subB_lv_bus', 'fdr3_east');
      if (s.dsF4A !== false && s.cbF4 !== false && s.dsF4B !== false) addEdge('subB_lv_bus', 'fdr4_east');

      // Normally-Open Bidirectional Tie Switches (79-TIE1 North Loop, 89-TIE2 South Loop)
      if (s.cbTieB) addEdge('fdr1_sec2', 'fdr3_east');
      if (s.cbTie2) addEdge('fdr2_main', 'fdr4_east');

      const runBfs = (startNode, isOn) => {
        const visited = new Set();
        if (!isOn) return visited;
        const q = [startNode];
        visited.add(startNode);
        while (q.length > 0) {
          const cur = q.shift();
          for (const nxt of (adj[cur] || [])) {
            if (!visited.has(nxt)) {
              visited.add(nxt);
              q.push(nxt);
            }
          }
        }
        return visited;
      };

      const reachA = runBfs('subA_lv_bus', secMain);
      const reachB = runBfs('subB_lv_bus', subBSourceOn);
      const isLive = (node) => reachA.has(node) || reachB.has(node);

      const fdr1 = isLive('fdr1_head') || !!(secMain && s.dsF1A && s.cbF1 && s.dsF1B);
      const fdr2 = isLive('fdr2_head') || !!(secMain && s.dsF2A && s.cbF2 && s.dsF2B);
      const dist_f1_sec1 = isLive('fdr1_sec1');
      const dist_f1_sec2 = isLive('fdr1_sec2');
      const dist_lateral = isLive('res_lat');
      const dist_f2_main = isLive('fdr2_main');
      const dist_f3 = isLive('fdr3_east');
      const dist_f4 = isLive('fdr4_east');
      const dist_sub_b = subBSourceOn;
      const secMainEff = secMain || reachB.has('subA_lv_bus');
      const subBLvEff = subBSourceOn || reachA.has('subB_lv_bus');

      const fdr1_from_subB = !!(reachB.has('fdr1_sec2') && !reachA.has('fdr1_sec2'));
      const fdr2_from_subB = !!(reachB.has('fdr2_main') && !reachA.has('fdr2_main'));
      const fdr3_from_subA = !!(reachA.has('fdr3_east') && !reachB.has('fdr3_east'));
      const fdr4_from_subA = !!(reachA.has('fdr4_east') && !reachB.has('fdr4_east'));
      const subA_lv_backfed_from_B = !secMain && reachB.has('subA_lv_bus');
      const subB_lv_backfed_from_A = !subBSourceOn && reachA.has('subB_lv_bus');

      const tie1Closed = !!s.cbTieB;
      const tie2Closed = !!s.cbTie2;
      const tie1_dir = !tie1Closed ? 'NONE'
        : ((reachA.has('fdr1_sec2') && !reachB.has('fdr3_east')) ? 'A_TO_B'
          : ((reachB.has('fdr3_east') && !reachA.has('fdr1_sec2')) ? 'B_TO_A'
            : ((reachA.has('fdr1_sec2') && reachB.has('fdr3_east')) ? 'PARALLEL' : 'NONE')));
      const tie2_dir = !tie2Closed ? 'NONE'
        : ((reachA.has('fdr2_main') && !reachB.has('fdr4_east')) ? 'A_TO_B'
          : ((reachB.has('fdr4_east') && !reachA.has('fdr2_main')) ? 'B_TO_A'
            : ((reachA.has('fdr2_main') && reachB.has('fdr4_east')) ? 'PARALLEL' : 'NONE')));

      let loopModeBanner = 'MODE: NORMAL RADIAL SPLIT-LOOP (79-TIE1 & 89-TIE2 OPEN)';
      if (fdr3_from_subA || fdr4_from_subA) {
        const tieList = [fdr3_from_subA ? '79-TIE1' : null, fdr4_from_subA ? '89-TIE2' : null].filter(Boolean).join(' & ');
        loopModeBanner = `MODE: BACK-FEED TRANSFER (SUB A FEEDING CITY LOADS VIA CLOSED ${tieList})`;
      } else if (fdr1_from_subB || fdr2_from_subB) {
        const tieList = [fdr1_from_subB ? '79-TIE1' : null, fdr2_from_subB ? '89-TIE2' : null].filter(Boolean).join(' & ');
        loopModeBanner = `MODE: BACK-FEED TRANSFER (TIE SUB B FEEDING CITY LOADS VIA CLOSED ${tieList})`;
      } else if (tie1_dir === 'PARALLEL' || tie2_dir === 'PARALLEL') {
        loopModeBanner = 'MODE: CLOSED-LOOP PARALLEL TIE OPERATION (SUB A || SUB B)';
      } else if (!dist_f1_sec2 && !dist_f2_main && !dist_f3 && !dist_f4) {
        loopModeBanner = 'MODE: DISTRIBUTION OUTAGE (NO ACTIVE SOURCE PATH)';
      }

      return {
        incoming: true,
        post_dsA,
        post_cbMain,
        main_path: (top === 'single' || top === 'maintransfer') ? main_path : txFeed,
        bypass_path,
        ring_leg1, ring_leg2, ring_leg3, ring_leg4,
        bh_busA, bh_tie, bh_busB,
        db_b1A, db_b1B, db_b2A, db_b2B, db_busA, db_busB,
        txFeed,
        tx_hv: txFeed,
        sec_lv: txFeed,
        secMain,
        secMainEff,
        subBLvEff,
        sec_bus: secMainEff,
        fdr1,
        fdr2,
        ind_hv,
        capBank,
        cap_bank: capBank,
        sst100,
        sst_tap: sst100,
        dist_f1_sec1,
        dist_f1_sec2,
        dist_f2_main,
        dist_f3,
        dist_f4,
        dist_lateral,
        dist_sub_b,
        fdr1_from_subB,
        fdr2_from_subB,
        fdr3_from_subA,
        fdr4_from_subA,
        subA_lv_backfed_from_B,
        subB_lv_backfed_from_A,
        tie1_dir,
        tie2_dir,
        loopModeBanner,
        reachA: Array.from(reachA),
        reachB: Array.from(reachB)
      };
    }

    function rebuildPowerFlowPaths() {
      if (!powerParticles || !scene) return;
      const b = computeEnergizedBranches();
      powerFlowCurves = [];

      // Traverse scene so every particle samples EXACT 3D world coordinates from actual rendered conductors!
      scene.updateMatrixWorld(true);
      const colorMap = {
        incoming: [0.22, 0.78, 0.98],
        post_dsA: [0.20, 0.80, 0.98],
        post_cbMain: [0.19, 0.82, 0.99],
        main_path: [0.18, 0.82, 0.99],
        bypass_path: [0.25, 0.94, 0.85],
        ring_leg1: [0.18, 0.82, 0.99],
        ring_leg2: [0.18, 0.82, 0.99],
        ring_leg3: [0.18, 0.82, 0.99],
        ring_leg4: [0.18, 0.82, 0.99],
        bh_busA: [0.18, 0.82, 0.99],
        bh_tie: [0.25, 0.90, 0.98],
        bh_busB: [0.18, 0.82, 0.99],
        db_b1A: [0.18, 0.82, 0.99],
        db_b1B: [0.25, 0.90, 0.98],
        db_b2A: [0.18, 0.82, 0.99],
        db_b2B: [0.25, 0.90, 0.98],
        db_busA: [0.18, 0.82, 0.99],
        db_busB: [0.25, 0.90, 0.98],
        tx_hv: [0.18, 0.82, 0.99],
        sec_lv: [0.98, 0.72, 0.15],
        sec_bus: [0.96, 0.82, 0.25],
        fdr1: [0.16, 0.90, 0.56],
        fdr2: [0.16, 0.90, 0.56],
        ind_hv: [0.96, 0.62, 0.04],
        cap_bank: [0.38, 0.95, 0.88],
        sst_tap: [0.98, 0.58, 0.16],
        dist_f1_sec1: [0.16, 0.90, 0.56],
        dist_f1_sec2: [0.18, 0.94, 0.62],
        dist_f2_main: [0.16, 0.90, 0.56],
        dist_f3: [0.16, 0.90, 0.56],
        dist_f4: [0.16, 0.90, 0.56],
        dist_lateral: [0.98, 0.80, 0.22],
        dist_sub_b: [0.22, 0.85, 0.98]
      };

      const isObjVisible = (obj) => {
        let p = obj;
        while (p) {
          if (p.visible === false) return false;
          p = p.parent;
        }
        return true;
      };

      scene.traverse(obj => {
        if (!obj.userData || !obj.userData.flowCurve) return;
        const cTag = obj.userData.circuitTag || 'main_path';
        if (cTag === 'none' || !b[cTag]) return;
        if (!isObjVisible(obj)) return;

        const srcCurve = obj.userData.flowCurve;
        let worldCurve = null;
        // Bidirectional 3D particle direction (West->East vs East->West during FLISR back-feed transfer)
        const isInSubBYard = (() => {
          let p = obj;
          while (p) { if (p.name === 'substation_b_yard') return true; p = p.parent; }
          return false;
        })();
        const revSec1 = (cTag === 'dist_f1_sec1' || cTag === 'fdr1') && b.fdr1_from_subB;
        const revSec2 = (cTag === 'dist_f1_sec2') && b.fdr1_from_subB;
        const revF2 = (cTag === 'dist_f2_main' || cTag === 'fdr2') && b.fdr2_from_subB;
        // Outside Sub B yard, f3/f4 catenaries are built West->East (tieCityX->eastEntryX), so Sub B normal feed reverses them; Sub A backfeed keeps West->East
        const revF3 = (cTag === 'dist_f3') && (!isInSubBYard ? !b.fdr3_from_subA : b.fdr3_from_subA);
        const revF4 = (cTag === 'dist_f4') && (!isInSubBYard ? !b.fdr4_from_subA : b.fdr4_from_subA);
        const reverseFlow = revSec1 || revSec2 || revF2 || revF3 || revF4;
        if (srcCurve instanceof THREE.LineCurve3 || (srcCurve.v1 && srcCurve.v2)) {
          const p0 = srcCurve.v1.clone().applyMatrix4(obj.matrixWorld);
          const p1 = srcCurve.v2.clone().applyMatrix4(obj.matrixWorld);
          if (p0.distanceToSquared(p1) < 1e-6) return;
          worldCurve = reverseFlow
            ? new THREE.LineCurve3(p1, p0)
            : new THREE.LineCurve3(p0, p1);
        } else {
          const sampleCount = 10;
          const worldPts = [];
          for (let i = 0; i <= sampleCount; i++) {
            const pt = srcCurve.getPoint(i / sampleCount).clone().applyMatrix4(obj.matrixWorld);
            worldPts.push(pt);
          }
          if (reverseFlow) {
            worldPts.reverse();
          }
          if (worldPts.length < 2) return;
          worldCurve = new THREE.CatmullRomCurve3(worldPts);
        }

        const vTag = obj.userData.voltageTag || 'HV';
        const isLv = (vTag === 'LV' || vTag === '13.8kV' || vTag === '480V');
        const spd = isLv ? (cTag === 'fdr1' || cTag === 'fdr2' ? 0.52 : (vTag === '480V' ? 0.34 : 0.45)) : 0.36;
        powerFlowCurves.push({
          curve: worldCurve,
          color: colorMap[cTag] || (isLv ? [0.98, 0.72, 0.15] : [0.22, 0.78, 0.98]),
          speed: spd
        });
      });

      // Refresh per-particle curve index, offset, and voltage color
      const count = powerParticleMeta.length;
      const colAttr = powerParticles.geometry.attributes.color.array;
      const nCurves = powerFlowCurves.length;
      for (let i = 0; i < count; i++) {
        if (nCurves === 0) continue;
        const cIdx = i % nCurves;
        const meta = powerParticleMeta[i];
        meta.curveIndex = cIdx;
        const c = powerFlowCurves[cIdx].color;
        colAttr[i * 3] = c[0];
        colAttr[i * 3 + 1] = c[1];
        colAttr[i * 3 + 2] = c[2];
      }
      powerParticles.geometry.attributes.color.needsUpdate = true;
    }

    function setupPowerFlowParticles() {
      const particleCount = 360;
      const geo = new THREE.BufferGeometry();
      const pos = new Float32Array(particleCount * 3);
      const col = new Float32Array(particleCount * 3);
      powerParticleMeta = [];

      for (let i = 0; i < particleCount; i++) {
        powerParticleMeta.push({
          curveIndex: 0,
          t: (i / particleCount + (i % 7) * 0.13) % 1.0
        });
        col[i * 3] = 0.22; col[i * 3 + 1] = 0.78; col[i * 3 + 2] = 0.98;
      }

      geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      geo.setAttribute('color', new THREE.BufferAttribute(col, 3));

      const pMat = new THREE.PointsMaterial({
        size: 0.36,
        vertexColors: true,
        transparent: true,
        opacity: 0.92,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });

      powerParticles = new THREE.Points(geo, pMat);
      powerParticles.name = 'powerParticles';
      scene.add(powerParticles);
      rebuildPowerFlowPaths();
    }

    // UPDATE POWER FLOW PARTICLES
    function updatePowerParticles(delta) {
      if (!powerParticles || !AppState.powerFlowActive || powerFlowCurves.length === 0) {
        if (powerParticles) powerParticles.visible = false;
        return;
      }
      powerParticles.visible = true;

      const pos = powerParticles.geometry.attributes.position.array;
      const count = powerParticleMeta.length;
      const tmpPt = new THREE.Vector3();

      for (let i = 0; i < count; i++) {
        const meta = powerParticleMeta[i];
        const curveObj = powerFlowCurves[meta.curveIndex % powerFlowCurves.length];
        meta.t = (meta.t + curveObj.speed * delta) % 1.0;
        curveObj.curve.getPointAt(meta.t, tmpPt);
        pos[i * 3] = tmpPt.x;
        pos[i * 3 + 1] = tmpPt.y;
        pos[i * 3 + 2] = tmpPt.z;
      }
      powerParticles.geometry.attributes.position.needsUpdate = true;
    }

    const MODAL_IDS_CHECK = [
      'challenge-modal', 'arc-flash-modal', 'subpart-modal', 'help-modal',
      'enclosure-modal', 'hv-danger-modal', 'voltage-scale-modal', 'analysis-modal',
      'sld-expanded-modal'
    ];

    function isAnyModalOpen() {
      for (const id of MODAL_IDS_CHECK) {
        const el = document.getElementById(id);
        if (el && el.style.display && el.style.display !== 'none') return true;
      }
      return false;
    }

    function isIgnoredRaycastMesh(obj) {
      if (!obj || !obj.isMesh || !obj.visible) return true;
      if (obj === powerParticles) return true;
      let curr = obj;
      while (curr && curr !== scene) {
        if (curr.visible === false) return true;
        const nm = (curr.name || '').toLowerCase();
        if (nm === 'ground-plane' || nm === 'gravel-pad' || nm === 'perimeter-fence' || nm === 'perimeter-wall' || nm === 'world-survey-grid' || nm === 'sky-dome' || nm === 'pinpoint-fault-marker' || nm === 'leaderlines') {
          return true;
        }
        curr = curr.parent;
      }
      return false;
    }

    // RAYCASTING CLICK-TO-EXPLODE / SUB-PART DEEP-DIVE / CONTROL ROOM SWITCH / PINPOINT FAULT
    function onCanvasClick(event) {
      if (event && event.target && renderer && event.target !== renderer.domElement) return;
      if (isAnyModalOpen()) return;

      if (AppState.isWalkMode) {
        if (!AppState.isHazardModalLocked) {
          triggerWalkFocusedAction();
        }
        return;
      }

      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / Math.max(1, rect.width)) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / Math.max(1, rect.height)) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children, true).filter(hit => !isIgnoredRaycastMesh(hit.object));

      // Pinpoint Fault Mode: click any 3D equipment or conductor in the switchyard to inject a fault at that exact point
      if (AppState.pinpointFaultMode) {
        for (let hit of intersects) {
          let curr = hit.object;
          let foundCompId = null;
          let cTag = (curr && curr.userData && curr.userData.circuitTag) ? curr.userData.circuitTag : null;
          while (curr && curr !== scene) {
            if (!cTag && curr.userData && curr.userData.circuitTag) cTag = curr.userData.circuitTag;
            if (curr.userData && curr.userData.componentId) {
              foundCompId = curr.userData.componentId;
              break;
            }
            curr = curr.parent;
          }
          if (foundCompId && foundCompId !== 'control' && foundCompId !== 'ground') {
            const pt = hit.point ? hit.point.clone() : null;
            const mapped = map3DHitToPinpointNode(foundCompId, cTag, pt);
            triggerPinpointedFault(mapped.nodeId, mapped.distPct, pt);
            return;
          }
        }
      }

      // Build candidate equipment hits with priority: SCADA HMI / 52-CS -> Specific Apparatus -> Gantry/Busbar
      let firstSpecificHit = null;
      let firstGantryHit = null;

      for (let hit of intersects) {
        let curr = hit.object;
        let foundSubpartId = null;
        let foundCompId = null;
        let hasFlowCurve = false;
        let inSpanningBusbar = false;
        let actionTag = null;
        let relayFocus = null;

        while (curr && curr !== scene) {
          if (!actionTag && curr.userData && curr.userData.action) actionTag = curr.userData.action;
          if (!relayFocus && curr.userData && curr.userData.relayFocus) relayFocus = curr.userData.relayFocus;
          if (!foundSubpartId && curr.userData && curr.userData.subpartId) foundSubpartId = curr.userData.subpartId;
          if (curr.userData && curr.userData.flowCurve) hasFlowCurve = true;
          if (curr.userData && curr.userData.isSpanningBusbar) inSpanningBusbar = true;
          if (curr.userData && curr.userData.componentId) {
            foundCompId = curr.userData.componentId;
            break;
          }
          curr = curr.parent;
        }

        // Direct interactive Control House SCADA/HMI Workstation -> Master SLD
        if (actionTag === 'openMasterSLD') {
          openExpandedSLD();
          showToast('SCADA HMI Workstation: Opened Interactive Master Single-Line Diagram (ANSI C37.2)');
          return;
        }

        // Direct interactive Control House Relay Panels 1-3 -> Relay Settings & TCC Coordination Lab
        if (actionTag === 'openRelayTccLab') {
          openAnalysisModal('tcc', relayFocus || 'all');
          showToast('Control House Protection Rack: Opened Relay Settings Schedule & Interactive TCC Lab');
          return;
        }

        // Direct interactive Control House Pistol-Grip 52-CS Breaker Control Switch
        if (actionTag === 'toggleBreaker') {
          toggleBreakerState();
          showToast(`Control House Panel 4 (52-CS): CB-69-1 Remotely ${AppState.breakerClosed ? 'CLOSED' : 'TRIPPED'}`);
          return;
        }

        // Direct interactive Substation A, B & City Entrance Gates (Swing/Lift open + inspect)
        if (actionTag === 'toggleGateA' || actionTag === 'toggleGateB') {
          toggleSubstationGate(actionTag === 'toggleGateB' ? 'B' : 'A');
          selectComponent('substation_gate', false);
          return;
        }
        if (actionTag === 'toggleCityGate') {
          toggleSubstationGate('city');
          selectComponent('city_gate', false);
          return;
        }

        if (!foundCompId || foundCompId === 'ground') continue;

        // Ignore incidental raycast hits on spanning overhead catenary jumpers to stop ghost Gantry selection
        if (inSpanningBusbar && hasFlowCurve) continue;

        if (foundCompId === 'gantry') {
          if (!firstGantryHit) firstGantryHit = { foundCompId, foundSubpartId, distance: hit.distance };
        } else {
          if (!firstSpecificHit) firstSpecificHit = { foundCompId, foundSubpartId, distance: hit.distance };
          break;
        }
      }

      // Prefer dedicated bay apparatus over spanning Gantry/Busbar unless Gantry is clearly in front (>3.5m closer)
      const chosen = (firstSpecificHit && (!firstGantryHit || firstSpecificHit.distance <= firstGantryHit.distance + 3.5))
        ? firstSpecificHit
        : (firstGantryHit || firstSpecificHit);

      if (chosen) {
        if (
          chosen.foundSubpartId &&
          AppState.mode === 'explode' &&
          AppState.explodePercentage > 0 &&
          AppState.selectedComponent === chosen.foundCompId
        ) {
          openSubpartModal(chosen.foundCompId, chosen.foundSubpartId);
          return;
        }
        selectComponent(chosen.foundCompId, true);
      }
    }

    // SELECT COMPONENT & TRANSITION TO EXPLODED INSPECTION
    function selectComponent(compKey, enterExploded = false) {
      if (!SUBSTATION_DATA[compKey]) return;
      AppState.selectedComponent = compKey;

      renderTelemetryDrawer(compKey);
      renderLiveSLD();

      if (enterExploded) {
        enterExplodedMode(compKey, false);
      }
    }

    // ENTER EXPLODED INSPECTION MODE
    function enterExplodedMode(compKey, keepWalkCamera = false) {
      AppState.mode = 'explode';
      document.getElementById('explode-dock').style.display = 'flex';

      const data = SUBSTATION_DATA[compKey];
      document.getElementById('explode-comp-name').innerText = data.name;
      document.getElementById('explode-comp-tag').innerText = `${data.ansiNumber} | ${data.governingStandard}`;

      document.getElementById('explode-slider').value = AppState.explodePercentage;
      document.getElementById('explode-pct-label').innerText = `${AppState.explodePercentage}%`;

      const chipsCont = document.getElementById('parts-chips-container');
      chipsCont.innerHTML = '';
      data.subparts.forEach((sp, idx) => {
        const chip = document.createElement('div');
        chip.className = 'part-chip';
        chip.id = `chip-${sp.id}`;
        chip.innerText = `${idx + 1}. ${sp.name}`;
        chip.onclick = () => focusSubpart(sp.id);
        chipsCont.appendChild(chip);
      });

      const targetObj = switchyardObjects[compKey];
      if (targetObj && !keepWalkCamera && !AppState.isWalkMode) {
        const box = new THREE.Box3().setFromObject(targetObj);
        const center = new THREE.Vector3();
        box.getCenter(center);

        tweenCameraTo(
          [center.x + 8, center.y + 5, center.z + 8],
          [center.x, center.y, center.z],
          1100
        );
      }

      applyExplodedTransform(compKey, AppState.explodePercentage / 100);
      showToast(`Inspecting: ${data.name}`);
    }

    // EXIT EXPLODED MODE & RETURN TO SWITCHYARD
    function exitExplodedMode() {
      AppState.mode = 'field';
      AppState.autoRotate = false;
      document.getElementById('explode-dock').style.display = 'none';

      if (AppState.selectedComponent) {
        applyExplodedTransform(AppState.selectedComponent, 0);
      }
      AppState.explodePercentage = 0;
      clearCalloutPins();

      if (!AppState.isWalkMode) {
        setCameraPreset('overview');
        showToast('Returned to Switchyard Field Immersion View');
      } else {
        showToast('Closed Exploded Inspector — Resumed Field Walk Mode');
      }
    }

    // SET EXPLODE PERCENTAGE (SLIDER EVENT)
    function setExplodePercentage(val) {
      AppState.explodePercentage = parseInt(val);
      document.getElementById('explode-pct-label').innerText = `${AppState.explodePercentage}%`;
      if (AppState.selectedComponent) {
        applyExplodedTransform(AppState.selectedComponent, AppState.explodePercentage / 100);
      }
    }

    // ANIMATE EXPLODE TO TARGET PERCENTAGE
    function animateExplode(targetPct) {
      const startPct = AppState.explodePercentage;
      const duration = 600;
      const startTime = performance.now();

      function update(t) {
        const elapsed = t - startTime;
        const progress = Math.min(elapsed / duration, 1.0);
        const ease = 0.5 - Math.cos(progress * Math.PI) / 2;
        const currentVal = Math.round(startPct + (targetPct - startPct) * ease);

        document.getElementById('explode-slider').value = currentVal;
        setExplodePercentage(currentVal);

        if (progress < 1.0) {
          requestAnimationFrame(update);
        }
      }
      requestAnimationFrame(update);
    }

    // APPLY PROCEDURAL EXPLODED DISPLACEMENT VECTORS & LEADER LINES
    function applyExplodedTransform(compKey, factor) {
      const compObj = switchyardObjects[compKey];
      const data = SUBSTATION_DATA[compKey];
      if (!compObj || !data || !compObj.userData.subparts) return;

      while (leaderLinesGroup.children.length > 0) {
        leaderLinesGroup.remove(leaderLinesGroup.children[0]);
      }

      clearCalloutPins();

      const lineMat = new THREE.LineDashedMaterial({
        color: 0x38bdf8,
        dashSize: 0.15,
        gapSize: 0.08,
        linewidth: 1.5
      });

      data.subparts.forEach(sp => {
        const subMesh = compObj.userData.subparts[sp.id];
        if (subMesh) {
          if (!subMesh.userData.basePos) {
            subMesh.userData.basePos = subMesh.position.clone();
          }
          const base = subMesh.userData.basePos;
          const v = sp.vector;

          subMesh.position.set(
            base.x + v[0] * factor,
            base.y + v[1] * factor,
            base.z + v[2] * factor
          );

          if (factor > 0) {
            const worldOrigin = base.clone().applyMatrix4(compObj.matrixWorld);
            const worldExploded = subMesh.position.clone().applyMatrix4(compObj.matrixWorld);

            const points = [worldOrigin, worldExploded];
            const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
            const line = new THREE.Line(lineGeo, lineMat);
            line.computeLineDistances();
            leaderLinesGroup.add(line);

            createCalloutPin(sp, worldExploded);
          }
        }
      });
    }

    // CREATE 3D FLOATING HTML CALLOUT PIN
    function createCalloutPin(subpart, worldPos) {
      const container = document.getElementById('callout-container');
      const pin = document.createElement('div');
      pin.className = 'callout-pin';
      pin.id = `pin-${subpart.id}`;
      pin.innerHTML = `<strong>${subpart.tag}:</strong> ${subpart.name}`;
      pin.dataset.worldX = worldPos.x;
      pin.dataset.worldY = worldPos.y;
      pin.dataset.worldZ = worldPos.z;

      pin.onclick = (e) => {
        e.stopPropagation();
        focusSubpart(subpart.id);
      };

      container.appendChild(pin);
    }

    function clearCalloutPins() {
      const container = document.getElementById('callout-container');
      container.innerHTML = '';
    }

    // UPDATE 3D-TO-2D SCREEN POSITION OF CALLOUT PINS
    function updateCalloutPins() {
      if (AppState.mode !== 'explode' || AppState.explodePercentage <= 0) {
        clearCalloutPins();
        return;
      }

      const pins = document.querySelectorAll('.callout-pin');
      const tempV = new THREE.Vector3();

      pins.forEach(pin => {
        tempV.set(
          parseFloat(pin.dataset.worldX),
          parseFloat(pin.dataset.worldY),
          parseFloat(pin.dataset.worldZ)
        );

        tempV.project(camera);

        if (tempV.z > 1.0) {
          pin.style.display = 'none';
        } else {
          const x = (tempV.x * 0.5 + 0.5) * window.innerWidth;
          const y = (-(tempV.y * 0.5) + 0.5) * window.innerHeight;
          pin.style.display = 'flex';
          pin.style.left = `${x}px`;
          pin.style.top = `${y}px`;
        }
      });
    }

    // FOCUS SPECIFIC SUB-PART & LAUNCH DEEP-DIVE POP-UP MODAL
    function focusSubpart(subpartId) {
      const data = SUBSTATION_DATA[AppState.selectedComponent];
      if (!data) return;
      const sp = data.subparts.find(s => s.id === subpartId);
      if (!sp) return;

      document.querySelectorAll('.part-chip').forEach(c => c.classList.remove('active'));
      const chip = document.getElementById(`chip-${subpartId}`);
      if (chip) chip.classList.add('active');

      openSubpartModal(AppState.selectedComponent, subpartId);
    }

    // TOGGLE AUTO-ROTATE
    function toggleAutoRotate() {
      AppState.autoRotate = !AppState.autoRotate;
      if (controls && 'autoRotate' in controls) {
        controls.autoRotate = AppState.autoRotate;
        controls.autoRotateSpeed = 2.0;
      }
      const btn = document.getElementById('btn-auto-rotate');
      if (AppState.autoRotate) {
        btn.classList.add('btn-active');
      } else {
        btn.classList.remove('btn-active');
      }
    }

    // CAMERA PRESET SMOOTH TWEEN
    function setCameraPreset(presetKey, animate = true) {
      const p = CAMERA_PRESETS[presetKey];
      if (!p) return;

      document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.btn-preset')).find(b => {
        const oc = b.getAttribute('onclick') || '';
        return oc.includes(`'${presetKey}'`);
      });
      if (activeBtn) activeBtn.classList.add('active');

      // Auto-toggle ground grid layer & floating IEEE 80 legend if Ground Preset selected
      if (presetKey === 'ground') {
        AppState.groundXrayActive = true;
        if (switchyardObjects.groundGrid) switchyardObjects.groundGrid.visible = true;
        const chk = document.getElementById('toggle-ground-xray');
        if (chk) chk.checked = true;
        const gl = document.getElementById('ground-legend');
        if (gl) gl.style.display = 'flex';
      }

      // Auto-cutaway Control House roof when inspecting Control House preset
      if (presetKey === 'control') {
        AppState.ctrlRoofManualCutaway = true;
        const roofChk = document.getElementById('toggle-ctrl-roof');
        if (roofChk) roofChk.checked = true;
      }

      // Map bay preset to component selection
      const presetCompMap = {
        gantry: 'gantry',
        arrester: 'arrester',
        ctvt: 'ctvt',
        disconnect: 'disconnect',
        breaker: 'breaker',
        transformer: 'transformer',
        control: 'auxiliary',
        secondary: 'secondary',
        feeders: 'feeders',
        recloser: 'dist_recloser',
        cutout_loads: 'dist_fuse_cutout',
        substation_b: 'substation_b'
      };
      if (presetCompMap[presetKey]) {
        selectComponent(presetCompMap[presetKey], false);
      }

      if (animate && controls && typeof tweenCameraTo === 'function') {
        tweenCameraTo(p.pos, p.target, 900);
      } else {
        activeCameraTweenId++;
        camera.position.set(p.pos[0], p.pos[1], p.pos[2]);
        if (controls && controls.target) {
          controls.target.set(p.target[0], p.target[1], p.target[2]);
          if (typeof controls.update === 'function') controls.update();
        }
      }
    }

    function tweenCameraTo(targetPos, targetLookAt, duration = 900) {
      const myTweenId = ++activeCameraTweenId;
      const startPos = camera.position.clone();
      const startTarget = controls && controls.target ? controls.target.clone() : new THREE.Vector3();
      const endPos = new THREE.Vector3(...targetPos);
      const endTarget = new THREE.Vector3(...targetLookAt);
      const startTime = performance.now();

      function update(now) {
        if (myTweenId !== activeCameraTweenId) return;
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1.0);
        const ease = 0.5 - Math.cos(progress * Math.PI) / 2;

        camera.position.lerpVectors(startPos, endPos, ease);
        if (controls && controls.target) {
          controls.target.lerpVectors(startTarget, endTarget, ease);
          if (typeof controls.update === 'function') controls.update();
        }

        if (progress < 1.0) {
          requestAnimationFrame(update);
        }
      }
      requestAnimationFrame(update);
    }

    // DEDICATED FUNCTION: REBUILD BUSBAR TOPOLOGY (PHYSICAL 3D RECONFIGURATION FOR SUB A OR SUB B)
    function rebuildBusbarTopology(scheme) {
      const target = AppState.targetSubstation || 'A';
      if (target === 'B') {
        AppState.subBTopology = scheme;
        applySubstationLayout(AppState.busTopology, true, true);
        if (!AppState.isWalkMode && AppState.mode !== 'explode') {
          setCameraPreset('substation_b');
        }
      } else {
        AppState.busTopology = scheme;
        if (AppState.tccState) AppState.tccState.topo = scheme;
        applySubstationLayout(scheme, true, true);
        if (!AppState.isWalkMode && AppState.mode !== 'explode') {
          setCameraPreset('overview');
        }
      }

      syncTargetSubstationUI();

      const topNames = {
        single: 'Single Bus Scheme (1 Bus, 1 CB per bay - Lowest Capital Cost)',
        maintransfer: 'Main & Transfer Bus Scheme (2 Buses, Dedicated 52-BT Bus Tie, 89-BYP)',
        ring: 'Ring Bus Scheme (Closed 4-Breaker Loop, Flanking Disconnects, High Reliability)',
        breakerhalf: 'Breaker-and-a-Half Scheme (1½ CB - 2 Outer Main Buses, 3 Breakers / 2 Circuits)',
        doublebreaker: 'Double Bus–Double Breaker (2.0 CB/ckt - Dual Main Buses A & B, Zero-Interruption Switching)'
      };

      renderLiveSLD();
      updateSubtitleAndTelemetry();
      showToast(`Reconfigured Substation ${target}: ${topNames[scheme] || scheme}`);
    }

    function selectBusTopology(topology) {
      rebuildBusbarTopology(topology);
    }

    // INTERACTIVE SWITCHING & INTERLOCK METADATA (SEPARATED TOPOLOGIES + SECONDARY + FEEDERS)
    const SWITCH_CATALOG = [
      // Single Bus & Main & Transfer Bus (Flanking 89-69A & 89-69B around 52-69)
      { id: 'dsMain', label: '89-69A Line Disc', kind: 'ds', seriesCb: 'cbMain', topologies: ['single', 'maintransfer'] },
      { id: 'cbMain', label: '52-69 Main HV CB', kind: 'cb', topologies: ['single', 'maintransfer'] },
      { id: 'dsMainB', label: '89-69B Bus Disc', kind: 'ds', seriesCb: 'cbMain', topologies: ['single', 'maintransfer'] },
      { id: 'earthMain', label: '89E Ground Switch', kind: 'earth', guardDs: 'dsMain', topologies: ['single', 'maintransfer'] },
      { id: 'dsBT', label: '89-BT Bus-Tie Disc', kind: 'ds', seriesCb: 'cbBT', topologies: ['maintransfer'] },
      { id: 'cbBT', label: '52-BT Bus-Tie CB', kind: 'cb', topologies: ['maintransfer'] },
      { id: 'dsBYP', label: '89-BYP Bypass Disc', kind: 'ds', isBypass: true, topologies: ['maintransfer'] },

      // Ring Bus (Closed 4-Corner Loop: 52-1..52-4 & 89-1A..4B)
      { id: 'cb1', label: '52-1 Ring West CB', kind: 'cb', topologies: ['ring'] },
      { id: 'ds1A', label: '89-1A West N Disc', kind: 'ds', seriesCb: 'cb1', topologies: ['ring'] },
      { id: 'ds1B', label: '89-1B West S Disc', kind: 'ds', seriesCb: 'cb1', topologies: ['ring'] },
      { id: 'cb2', label: '52-2 Ring North CB', kind: 'cb', topologies: ['ring'] },
      { id: 'ds2A', label: '89-2A North W Disc', kind: 'ds', seriesCb: 'cb2', topologies: ['ring'] },
      { id: 'ds2B', label: '89-2B North E Disc', kind: 'ds', seriesCb: 'cb2', topologies: ['ring'] },
      { id: 'cb3', label: '52-3 Ring East CB', kind: 'cb', topologies: ['ring'] },
      { id: 'ds3A', label: '89-3A East N Disc', kind: 'ds', seriesCb: 'cb3', topologies: ['ring'] },
      { id: 'ds3B', label: '89-3B East S Disc', kind: 'ds', seriesCb: 'cb3', topologies: ['ring'] },
      { id: 'cb4', label: '52-4 Ring South CB', kind: 'cb', topologies: ['ring'] },
      { id: 'ds4A', label: '89-4A South W Disc', kind: 'ds', seriesCb: 'cb4', topologies: ['ring'] },
      { id: 'ds4B', label: '89-4B South E Disc', kind: 'ds', seriesCb: 'cb4', topologies: ['ring'] },

      // Breaker-and-a-Half (1.5 CB: Bus A / TIE / Bus B 3-Breaker String)
      { id: 'cbA', label: '52-A Bus-A CB', kind: 'cb', topologies: ['breakerhalf'] },
      { id: 'dsA1', label: '89-A1 Bus-A Disc', kind: 'ds', seriesCb: 'cbA', topologies: ['breakerhalf'] },
      { id: 'dsA2', label: '89-A2 Ckt1 Disc', kind: 'ds', seriesCb: 'cbA', topologies: ['breakerhalf'] },
      { id: 'cbTIE', label: '52-TIE Center CB', kind: 'cb', topologies: ['breakerhalf'] },
      { id: 'dsT1', label: '89-T1 Mid N Disc', kind: 'ds', seriesCb: 'cbTIE', topologies: ['breakerhalf'] },
      { id: 'dsT2', label: '89-T2 Mid S Disc', kind: 'ds', seriesCb: 'cbTIE', topologies: ['breakerhalf'] },
      { id: 'cbB', label: '52-B Bus-B CB', kind: 'cb', topologies: ['breakerhalf'] },
      { id: 'dsB1', label: '89-B1 Ckt2 Disc', kind: 'ds', seriesCb: 'cbB', topologies: ['breakerhalf'] },
      { id: 'dsB2', label: '89-B2 Bus-B Disc', kind: 'ds', seriesCb: 'cbB', topologies: ['breakerhalf'] },

      // Double Bus–Double Breaker (2.0 CB per Circuit: Bay 1 Line + Bay 2 TR-01)
      { id: 'cb1A', label: '52-1A L1-BusA CB', kind: 'cb', topologies: ['doublebreaker'] },
      { id: 'ds1A1', label: '89-1A1 Bus-A Disc', kind: 'ds', seriesCb: 'cb1A', topologies: ['doublebreaker'] },
      { id: 'ds1A2', label: '89-1A2 Line Disc', kind: 'ds', seriesCb: 'cb1A', topologies: ['doublebreaker'] },
      { id: 'cb1B', label: '52-1B L1-BusB CB', kind: 'cb', topologies: ['doublebreaker'] },
      { id: 'ds1B1', label: '89-1B1 Line Disc', kind: 'ds', seriesCb: 'cb1B', topologies: ['doublebreaker'] },
      { id: 'ds1B2', label: '89-1B2 Bus-B Disc', kind: 'ds', seriesCb: 'cb1B', topologies: ['doublebreaker'] },
      { id: 'cb2A', label: '52-2A TX-BusA CB', kind: 'cb', topologies: ['doublebreaker'] },
      { id: 'ds2A1', label: '89-2A1 Bus-A Disc', kind: 'ds', seriesCb: 'cb2A', topologies: ['doublebreaker'] },
      { id: 'ds2A2', label: '89-2A2 TX Disc', kind: 'ds', seriesCb: 'cb2A', topologies: ['doublebreaker'] },
      { id: 'cb2B', label: '52-2B TX-BusB CB', kind: 'cb', topologies: ['doublebreaker'] },
      { id: 'ds2B1', label: '89-2B1 TX Disc', kind: 'ds', seriesCb: 'cb2B', topologies: ['doublebreaker'] },
      { id: 'ds2B2', label: '89-2B2 Bus-B Disc', kind: 'ds', seriesCb: 'cb2B', topologies: ['doublebreaker'] },

      // LV Secondary & Distribution Feeders (Flanking 89-A/B Around Every Breaker 52)
      { id: 'dsLV', label: '89-LVA Tx-Side Disc', kind: 'ds', seriesCb: 'cbLV', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbLV', label: '52-LV Main LV CB', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsLVB', label: '89-LVB Bus-Side Disc', kind: 'ds', seriesCb: 'cbLV', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsCapA', label: '89-CAPA Bus Disc', kind: 'ds', seriesCb: 'cbCap', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbCap', label: '52-CAP Shunt Cap CB', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsCapB', label: '89-CAPB Bank Disc', kind: 'ds', seriesCb: 'cbCap', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF1A', label: '89-F1A Bus Disc', kind: 'ds', seriesCb: 'cbF1', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbF1', label: '52-F1 Feeder 01', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF1B', label: '89-F1B Line Disc', kind: 'ds', seriesCb: 'cbF1', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF2A', label: '89-F2A Bus Disc', kind: 'ds', seriesCb: 'cbF2', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbF2', label: '52-F2 Feeder 02', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF2B', label: '89-F2B Line Disc', kind: 'ds', seriesCb: 'cbF2', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsIndA', label: '89-INDA Ind Disc', kind: 'ds', seriesCb: 'cbIndHv', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbIndHv', label: '52-IND HV Ind CB', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsIndB', label: '89-INDB Line Disc', kind: 'ds', seriesCb: 'cbIndHv', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      // Outgoing 13.8 kV Distribution Automation & Protection (FLISR) & Tie Substation B
      { id: 'cbACR1', label: '79-ACR1 F1 Recloser', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'sec34', label: '34-SECT Sectionalizer', kind: 'ds', seriesCb: 'cbACR1', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'fuseCutout', label: '100K Lateral Fuse Cutout', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbTieB', label: '79-TIE1 North Loop Tie', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbF2Rec', label: '79-F2 South Recloser', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbTie2', label: '89-TIE2 South Loop Tie', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsLVBA', label: '89-LVBA SubB Tx Disc', kind: 'ds', seriesCb: 'cbLVB', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbLVB', label: '52-LVB SubB Main CB', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsLVBB', label: '89-LVBB SubB Bus Disc', kind: 'ds', seriesCb: 'cbLVB', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF3A', label: '89-F3A SubB F3 Disc', kind: 'ds', seriesCb: 'cbF3', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbF3', label: '52-F3 SubB Feeder 03', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF3B', label: '89-F3B SubB F3 Line', kind: 'ds', seriesCb: 'cbF3', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF4A', label: '89-F4A SubB F4 Disc', kind: 'ds', seriesCb: 'cbF4', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'cbF4', label: '52-F4 SubB Feeder 04', kind: 'cb', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] },
      { id: 'dsF4B', label: '89-F4B SubB F4 Line', kind: 'ds', seriesCb: 'cbF4', topologies: ['single', 'maintransfer', 'ring', 'breakerhalf', 'doublebreaker'] }
    ];

    function syncAllSwitchesTo3D() {
      const s = AppState.switchStates;
      const top = AppState.busTopology;
      AppState.breakerClosed = top === 'ring' ? !!s.cb1 : (top === 'breakerhalf' ? !!s.cbTIE : (top === 'doublebreaker' ? !!s.cb1A : !!s.cbMain));
      AppState.disconnectClosed = !!s.dsMain;
      AppState.earthClosed = !!s.earthMain;

      // Primary Line Disconnect 89-69A & Earth 89E
      animateDisconnectBlades(s.dsMain);
      const disc = switchyardObjects.disconnect;
      if (disc && disc.userData && disc.userData.earthBlades) {
        disc.userData.earthBlades.forEach(eb => {
          eb.rotation.z = s.earthMain ? 0 : Math.PI / 2.2;
        });
      }

      // Primary Breaker Contacts + Control House Pistol-Grip
      const cb = switchyardObjects.breaker;
      if (cb && cb.userData && cb.userData.contactsList) {
        cb.userData.contactsList.forEach(c => {
          c.movingCont.position.x = AppState.breakerClosed ? 0.35 : 0.65;
        });
      }
      const aux = switchyardObjects.auxiliary;
      if (aux && aux.userData && aux.userData.pistolHandle) {
        aux.userData.pistolHandle.rotation.z = AppState.breakerClosed ? -0.45 : 0.45;
        if (aux.userData.ctrlRedLamp) aux.userData.ctrlRedLamp.visible = AppState.breakerClosed;
        if (aux.userData.ctrlGreenLamp) aux.userData.ctrlGreenLamp.visible = !AppState.breakerClosed;
      }

      // Dynamic Primary Busbar Switchgear (89-69B, 52-BT, 89-M/BYP, Ring 52-2..4/89-1A..4B, 1.5CB 52-A/B/89-A1..B2)
      const busObj = switchyardObjects.busbar;
      if (busObj && busObj.userData && busObj.userData.switches) {
        const bsw = busObj.userData.switches;
        const hvStateMap = {
          '89-69B': s.dsMainB,
          '52-BT': s.cbBT, '89-BT1': s.dsBT, '89-BT2': s.dsBT, '89-M': s.dsMain, '89-BYP': s.dsBYP,
          '52-2': s.cb2, '52-3': s.cb3, '52-4': s.cb4,
          '89-1A': s.ds1A, '89-1B': s.ds1B, '89-2A': s.ds2A, '89-2B': s.ds2B,
          '89-3A': s.ds3A, '89-3B': s.ds3B, '89-4A': s.ds4A, '89-4B': s.ds4B,
          '52-A': s.cbA, '52-B': s.cbB,
          '89-A1': s.dsA1, '89-A2': s.dsA2, '89-T1': s.dsT1, '89-T2': s.dsT2, '89-B1': s.dsB1, '89-B2': s.dsB2,
          '52-1B': s.cb1B, '52-2A': s.cb2A, '52-2B': s.cb2B,
          '89-1A1': s.ds1A1, '89-1A2': s.ds1A2, '89-1B1': s.ds1B1, '89-1B2': s.ds1B2,
          '89-2A1': s.ds2A1, '89-2A2': s.ds2A2, '89-2B1': s.ds2B1, '89-2B2': s.ds2B2
        };
        Object.entries(bsw).forEach(([tag, unit]) => {
          const isClosed = hvStateMap[tag] !== undefined ? !!hvStateMap[tag] : true;
          if (unit.userData && unit.userData.bladePairs) {
            const ang = isClosed ? 0 : Math.PI / 2.6;
            unit.userData.bladePairs.forEach(pair => {
              pair.blade1.rotation.y = -ang;
              pair.blade2.rotation.y = ang;
            });
          }
          if (unit.userData && unit.userData.statusFlag && unit.userData.statusFlag.material) {
            unit.userData.statusFlag.material.color.setHex(isClosed ? 0xef4444 : 0x10b981);
          }
        });
      }

      // Helper for Secondary MV/LV switches built via createMVDisconnectUnit / createMVBreakerUnit
      const updateMvDisc = (grp, isClosed) => {
        if (!grp || !grp.userData || !grp.userData.bladePivots) return;
        grp.userData.bladePivots.forEach(p => { p.rotation.z = isClosed ? 0 : Math.PI / 3.2; });
      };
      const updateMvCb = (grp, isClosed) => {
        if (!grp || !grp.userData) return;
        if (grp.userData.movingContacts) {
          grp.userData.movingContacts.forEach(m => { m.position.y = isClosed ? 1.56 : 1.72; });
        }
        if (grp.userData.statusFlag && grp.userData.statusFlag.material) {
          grp.userData.statusFlag.material.color.setHex(isClosed ? 0xef4444 : 0x10b981);
        }
      };

      const sec = switchyardObjects.secondary;
      if (sec && sec.userData) {
        updateMvDisc(sec.userData.lvDisc, s.dsLV);
        updateMvCb(sec.userData.lvBreaker, s.cbLV);
        updateMvDisc(sec.userData.lvDiscB, s.dsLVB);
        updateMvDisc(sec.userData.capDiscA, s.dsCapA);
        updateMvCb(sec.userData.capBreaker, s.cbCap);
        updateMvDisc(sec.userData.capDiscB, s.dsCapB);
      }
      const fdr = switchyardObjects.feeders;
      if (fdr && fdr.userData && fdr.userData.switches) {
        const sw = fdr.userData.switches;
        updateMvDisc(sw['89-F1A'], s.dsF1A);
        updateMvCb(sw['52-F1'], s.cbF1);
        updateMvDisc(sw['89-F1B'], s.dsF1B);
        updateMvDisc(sw['89-F2A'], s.dsF2A);
        updateMvCb(sw['52-F2'], s.cbF2);
        updateMvDisc(sw['89-F2B'], s.dsF2B);
        updateMvDisc(sw['89-INDA'], s.dsIndA !== false);
        updateMvCb(sw['52-IND'], s.cbIndHv !== false);
        if (sw['52-IND'] && sw['52-IND'].userData && sw['52-IND'].userData.contactsList) {
          sw['52-IND'].userData.contactsList.forEach(c => {
            if (c.movingCont) c.movingCont.position.x = (s.cbIndHv !== false) ? 0.35 : 0.65;
          });
        }
        updateMvDisc(sw['89-INDB'], s.dsIndB !== false);
      }

      // Distribution Poles & Neighboring Tie Substation B Animation
      const dist = switchyardObjects.distribution;
      const br = computeEnergizedBranches();
      if (dist && dist.userData) {
        const dsw = dist.userData.switches || {};
        const rec = dsw['79-ACR1'];
        if (rec && rec.userData && rec.userData.statusFlag && rec.userData.statusFlag.material) {
          rec.userData.statusFlag.material.color.setHex(s.cbACR1 ? 0xef4444 : 0x10b981);
        }
        const rec2 = dsw['79-F2'];
        if (rec2 && rec2.userData && rec2.userData.statusFlag && rec2.userData.statusFlag.material) {
          rec2.userData.statusFlag.material.color.setHex(s.cbF2Rec !== false ? 0xef4444 : 0x10b981);
        }
        const sect = dsw['34-SECT'];
        if (sect && sect.userData && sect.userData.bladePairs) {
          sect.userData.bladePairs.forEach(p => {
            if (p.blade1) p.blade1.rotation.z = s.sec34 ? Math.PI / 2 : Math.PI / 8;
          });
        }
        const tie2 = dsw['89-TIE2'];
        if (tie2 && tie2.userData && tie2.userData.bladePairs) {
          tie2.userData.bladePairs.forEach(p => {
            if (p.blade1) {
              p.blade1.rotation.z = s.cbTie2 ? Math.PI / 2 : 0.65;
              p.blade1.position.x = s.cbTie2 ? 0 : -0.34;
              p.blade1.position.y = s.cbTie2 ? 7.14 : 7.45;
            }
          });
        }
        const fuseU = dsw['FUSE-100K'];
        if (fuseU && fuseU.userData && fuseU.userData.fuseTubes) {
          fuseU.userData.fuseTubes.forEach(piv => {
            piv.rotation.x = s.fuseCutout ? 0 : -2.45;
          });
        }
        const subB = dsw['79-TIE'];
        if (subB && subB.userData && subB.userData.tieFlag && subB.userData.tieFlag.material) {
          subB.userData.tieFlag.material.color.setHex(s.cbTieB ? 0xef4444 : 0x10b981);
        }
        if (dist.userData.loadLights) {
          const uniLit = !!br.dist_f3;
          const munLit = !!br.dist_f4;
          dist.userData.loadLights.res.forEach(m => m.color.setHex(br.dist_lateral ? 0xfde047 : 0x1e293b));
          dist.userData.loadLights.comm.forEach(m => m.color.setHex(br.dist_f2_main ? 0x38bdf8 : 0x1e293b));
          dist.userData.loadLights.ind.forEach(m => m.color.setHex(br.ind_hv ? 0xfbbf24 : 0x1e293b));
          if (dist.userData.loadLights.urd) {
            dist.userData.loadLights.urd.forEach(m => m.color.setHex(br.dist_f1_sec2 ? 0xfde047 : 0x1e293b));
          }
          if (dist.userData.loadLights.uni) {
            dist.userData.loadLights.uni.forEach(m => m.color.setHex(uniLit ? 0xfde047 : 0x1e293b));
          }
          if (dist.userData.loadLights.mun) {
            dist.userData.loadLights.mun.forEach(m => m.color.setHex(munLit ? 0x38bdf8 : 0x1e293b));
          }
        }
        if (dist.userData.urdTrenchGroup) {
          dist.userData.urdTrenchGroup.visible = AppState.urdXrayActive !== false;
        }
      }

      const flisrEl = document.getElementById('flisr-status-readout');
      if (flisrEl) {
        flisrEl.innerText = `${br.loopModeBanner} | 52-F1:${s.cbF1?'CLS':'OPN'} 79-TIE1:${s.cbTieB?'CLS':'NO'} 52-F3:${s.cbF3!==false?'CLS':'OPN'} | 52-F2:${s.cbF2?'CLS':'OPN'} 89-TIE2:${s.cbTie2?'CLS':'NO'} 52-F4:${s.cbF4!==false?'CLS':'OPN'}`;
        flisrEl.style.borderColor = (br.fdr3_from_subA || br.fdr4_from_subA || br.fdr1_from_subB || br.fdr2_from_subB) ? '#38bdf8' : (br.dist_f1_sec2 || br.dist_f3 ? 'rgba(52,211,153,0.35)' : '#ef4444');
      }

      if (typeof updateSubtitleAndTelemetry === 'function') updateSubtitleAndTelemetry();
      rebuildPowerFlowPaths();
    }

    function renderSwitchMatrix() {
      const host = document.getElementById('switch-matrix-list');
      if (!host) return;
      const top = AppState.busTopology;
      const s = AppState.switchStates;
      const visible = SWITCH_CATALOG.filter(item => item.topologies.includes(top));
      host.innerHTML = visible.map(item => {
        const isClosed = !!s[item.id];
        const cls = isClosed ? 'sw-btn-closed' : 'sw-btn-open';
        const txt = isClosed ? 'CLOSED' : 'OPEN';
        return `
          <div class="sw-row">
            <span class="sw-label" title="${item.label}">${item.label}</span>
            <button class="sw-btn ${cls}" onclick="operateSwitch('${item.id}')">${txt}</button>
          </div>
        `;
      }).join('');
    }

    function operateSwitch(swId, silent = false) {
      const meta = SWITCH_CATALOG.find(x => x.id === swId);
      if (!meta) return false;
      const s = AppState.switchStates;
      const nextState = !s[swId];

      // 1. IEEE / ANSI Switch Interlock Guards
      if (meta.kind === 'ds') {
        if (meta.isBypass) {
          // 89-BYP can safely close when Transfer Breaker 52-BT & 89-BT parallel the bus (equal potential),
          // or when 52-69 is already open. Only block breaking active parallel load if 52-BT and 52-69 carry split current unsafely.
          if (nextState && (!s.cbBT || !s.dsBT)) {
            showToast('INTERLOCK BLOCKED: Close 89-BT & 52-BT first before closing Bypass 89-BYP!');
            return false;
          }
          if (!nextState && s.cbBT && !s.cbMain) {
            triggerArcFlashDisaster();
            showToast('ARC-FLASH VIOLATION: Opened 89-BYP while carrying full TR-01 load on Transfer Bus!');
            return false;
          }
        } else if (meta.seriesCb && s[meta.seriesCb]) {
          // Special Main & Transfer case: if 89-69 series breaker cbMain is closed WITHOUT bypass holding load, ARC FLASH!
          triggerArcFlashDisaster();
          showToast(`INTERLOCK VIOLATION: Cannot operate ${meta.label} while series Circuit Breaker is CLOSED!`);
          return false;
        }
      }

      if (meta.kind === 'earth') {
        if (nextState && (s[meta.guardDs] || s.cbMain)) {
          showToast(`INTERLOCK BLOCKED: Cannot close ${meta.label} onto closed ${meta.guardDs}/52-69! Open isolator first.`);
          return false;
        }
      }

      // If closing disconnect onto an already-closed Earth Switch, block!
      if (swId === 'dsMain' && nextState && s.earthMain) {
        showToast('INTERLOCK BLOCKED: Open Grounding Switch 89E before closing 89-69!');
        return false;
      }

      // Commit state transition + sound
      s[swId] = nextState;
      if (meta.kind === 'cb') soundEngine.playBreakerTrip();
      else soundEngine.playDisconnectOperate();

      syncAllSwitchesTo3D();
      renderSwitchMatrix();
      renderLiveSLD();
      if (typeof refreshSubpartActionBar === 'function') refreshSubpartActionBar();

      if (!silent) {
        showToast(`${meta.label}: ${nextState ? 'CLOSED' : 'OPENED'} (Interlock Check Passed)`);
      }
      return true;
    }

    // SIMULATION EVENT 1: NORMAL ENERGIZED STATE
    function triggerNormalState() {
      Object.assign(AppState.switchStates, {
        dsMain: true, cbMain: true, dsMainB: true, earthMain: false,
        dsBT: true, cbBT: false, dsBYP: false,
        cb1: true, ds1A: true, ds1B: true,
        cb2: true, ds2A: true, ds2B: true,
        cb3: true, ds3A: true, ds3B: true,
        cb4: true, ds4A: true, ds4B: true,
        cbA: true, dsA1: true, dsA2: true,
        cbTIE: true, dsT1: true, dsT2: true,
        cbB: true, dsB1: true, dsB2: true,
        cb1A: true, ds1A1: true, ds1A2: true,
        cb1B: true, ds1B1: true, ds1B2: true,
        cb2A: true, ds2A1: true, ds2A2: true,
        cb2B: true, ds2B1: true, ds2B2: true,
        dsLV: true, cbLV: true, dsLVB: true,
        dsCapA: true, cbCap: true, dsCapB: true,
        dsF1A: true, cbF1: true, dsF1B: true,
        dsF2A: true, cbF2: true, dsF2B: true,
        cbACR1: true, sec34: true, fuseCutout: true, cbTieB: false,
        dsIndA: true, cbIndHv: true, dsIndB: true,
        cbF2Rec: true, cbTie2: false,
        dsLVBA: true, cbLVB: true, dsLVBB: true,
        dsF3A: true, cbF3: true, dsF3B: true,
        dsF4A: true, cbF4: true, dsF4B: true
      });
      AppState.flisrRestored = false;
      AppState.isFaultActive = false;
      AppState.faultType = 'none';
      if (pinpointTripTimer) { clearTimeout(pinpointTripTimer); pinpointTripTimer = null; }
      if (faultMarker3D && scene) {
        scene.remove(faultMarker3D);
        faultMarker3D = null;
      }
      const ro = document.getElementById('pinpoint-fault-readout');
      if (ro) ro.innerHTML = 'System Normal. Enable Pinpoint Mode and click any 3D bus, transformer, or feeder (or SLD node) to inject a localized fault.';

      dynamicArcLight.intensity = 0;
      soundEngine.resumeTransformerHum();

      syncAllSwitchesTo3D();
      renderSwitchMatrix();
      renderLiveSLD();
      const vs = getVoltageSpec(AppState.voltageClass);
      showToast(`System Normal: ${vs.shortLabel}, ${vs.mva} MVA Load (${vs.vectorGroup})`);
    }

    // SIMULATION EVENT 2: LIGHTNING STRIKE & SURGE ARRESTER DISCHARGE
    function triggerLightningEvent() {
      AppState.isFaultActive = true;
      AppState.faultType = 'lightning';
      AppState.surgeCounter++;
      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);

      dynamicArcLight.color.setHex(0xe0f2fe);
      dynamicArcLight.position.set(L.gantryX, 16, 0);
      dynamicArcLight.intensity = 15;

      soundEngine.playLightning();

      const boltPts = [];
      let curX = L.gantryX, curY = 40, curZ = 0;
      boltPts.push(new THREE.Vector3(curX, curY, curZ));
      while (curY > 16) {
        curY -= (Math.random() * 3 + 2);
        curX += (Math.random() - 0.5) * 3;
        curZ += (Math.random() - 0.5) * 3;
        boltPts.push(new THREE.Vector3(curX, curY, curZ));
      }
      boltPts.push(new THREE.Vector3(L.gantryX, 14.5, 0));

      const boltGeo = new THREE.BufferGeometry().setFromPoints(boltPts);
      const boltMat = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 3 });
      const boltLine = new THREE.Line(boltGeo, boltMat);
      scene.add(boltLine);

      setTimeout(() => {
        dynamicArcLight.intensity = 0;
        scene.remove(boltLine);
        showToast(`Lightning Surge Diverted: SA-HV Arrester Discharged 2.0 kA to Ground Grid (Counter: ${AppState.surgeCounter})`);
        AppState.isFaultActive = false;
      }, 500);
    }

    // SIMULATION EVENT 3: 3-PHASE BUS SHORT CIRCUIT FAULT & TRIP
    function triggerBusFaultEvent() {
      AppState.isFaultActive = true;
      AppState.faultType = 'busfault';
      const vs = getVoltageSpec(AppState.voltageClass);

      const stEl = document.getElementById('telem-grid-status');
      const iEl = document.getElementById('telem-current');
      if (stEl) { stEl.innerText = 'FAULT (3-PHASE)'; stEl.style.color = '#ef4444'; }
      if (iEl) iEl.innerText = '12,500 A';

      dynamicArcLight.color.setHex(0xf59e0b);
      dynamicArcLight.position.set(0, 6, 0);
      dynamicArcLight.intensity = 10;

      soundEngine.playNoiseBurst(0.4, 0.8);

      showToast(`FAULT DETECTED: ${vs.hvKv} kV Bus Short Circuit! SEL-751 Relay Tripping HV Breaker in 3 Cycles...`);

      setTimeout(() => {
        AppState.switchStates.cbMain = false;
        AppState.switchStates.cb1 = false;
        AppState.switchStates.cb2 = false;
        AppState.switchStates.cbA = false;
        AppState.switchStates.cbTIE = false;
        AppState.switchStates.cbB = false;
        soundEngine.playBreakerTrip();
        dynamicArcLight.intensity = 0;

        AppState.isFaultActive = false;
        syncAllSwitchesTo3D();
        renderSwitchMatrix();

        if (stEl) { stEl.innerText = 'TRIPPED (ISOLATED)'; stEl.style.color = '#f59e0b'; }
        renderLiveSLD();
        showToast('FAULT CLEARED: Primary Circuit Breaker Tripped. SF6 Puffer Extinguished Arc.');
      }, 650);
    }

    // SIMULATION EVENT 4: LV FEEDER SINGLE LINE-TO-GROUND (SLG) FAULT
    function triggerFeederFaultEvent() {
      AppState.isFaultActive = true;
      AppState.faultType = 'feederfault';

      const stEl = document.getElementById('telem-grid-status');
      const iEl = document.getElementById('telem-current');
      if (stEl) { stEl.innerText = 'FAULT (FEEDER SLG)'; stEl.style.color = '#ef4444'; }
      if (iEl) iEl.innerText = '797 A (NGR Limited)';

      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);
      dynamicArcLight.color.setHex(0xef4444);
      dynamicArcLight.position.set(L.fdrGantryX - 2, 4.5, L.fdr1Z);
      dynamicArcLight.intensity = 12;

      soundEngine.playNoiseBurst(0.35, 0.7);
      showToast('FEEDER SLG FAULT: 10 Ω NGR limits ground fault current! ANSI 51G/51N Tripping 52-F1...');

      setTimeout(() => {
        dynamicArcLight.intensity = 0;
        AppState.switchStates.cbF1 = false;
        AppState.isFaultActive = false;
        soundEngine.playBreakerTrip();
        syncAllSwitchesTo3D();
        renderSwitchMatrix();
        if (stEl) { stEl.innerText = 'FEEDER 1 ISOLATED'; stEl.style.color = '#f59e0b'; }
        renderLiveSLD();
        showToast('FAULT CLEARED: Feeder 1 Breaker (52-F1) Tripped via 51N. TR-01 & Feeder 2 remain energized.');
      }, 700);
    }

    // SIMULATION EVENT 5: SCADA FLISR AUTOMATED LOOP ISOLATION & SUBSTATION B BACK-FEED TRANSFER
    function triggerFlisrLoopRestoration() {
      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);
      const distStart = L.fdrGantryX + 18.95;
      AppState.isFaultActive = true;
      AppState.faultType = 'flisr_fault';
      AppState.switchStates.cbF1 = true;
      AppState.switchStates.cbACR1 = true;
      AppState.switchStates.sec34 = true;
      AppState.switchStates.cbTieB = false;
      AppState.switchStates.cbF3 = true;
      AppState.switchStates.cbLVB = true;

      if (dynamicArcLight) {
        dynamicArcLight.color.setHex(0xef4444);
        dynamicArcLight.position.set(distStart + 15.0, 6.8, L.fdr1Z);
        dynamicArcLight.intensity = 10;
      }
      if (soundEngine && soundEngine.playNoiseBurst) soundEngine.playNoiseBurst(0.32, 0.6);
      showToast('FLISR STEP 1/3: Permanent fault between 79-ACR1 & 34-SECT! Recloser executing Curve A/B lockout...');

      setTimeout(() => {
        AppState.switchStates.cbACR1 = false;
        AppState.switchStates.sec34 = false; // Drops open cleanly during 79-ACR1 dead-time count=2!
        if (soundEngine && soundEngine.playBreakerTrip) soundEngine.playBreakerTrip();
        syncAllSwitchesTo3D();
        renderSwitchMatrix();
        renderLiveSLD();
        showToast('FLISR STEP 2/3: 79-ACR1 locked OPEN & 34-SECT dropped open during zero-current dead-time! Verifying ANSI 25...');
      }, 550);

      setTimeout(() => {
        if (dynamicArcLight) dynamicArcLight.intensity = 0;
        AppState.switchStates.cbTieB = true;
        AppState.flisrRestored = true;
        AppState.isFaultActive = false;
        if (soundEngine && soundEngine.playBreakerTrip) soundEngine.playBreakerTrip();
        syncAllSwitchesTo3D();
        renderSwitchMatrix();
        renderLiveSLD();
        showToast('FLISR COMPLETE: 79-TIE CLOSED! Commercial (750 kVA) & Industrial (1.5 MVA) restored by Substation B!');
      }, 1250);
    }

    // INTERACTIVE 23-NODE END-TO-END SYSTEM PINPOINT FAULT ENGINE (SUB A <-> CITY LOOP <-> TIE SUB B <-> HV IND)
    const PINPOINT_FAULT_NODES = {
      node1_incoming: {
        id: 'node1_incoming', group: 'Substation A (HV/EHV)',
        name: 'Node 1: Incoming EHV/HV Line / Gantry Dead-End',
        zone: 'ANSI 21 Distance + 67 Directional OC',
        breakers: ['cbMain', 'cb1', 'cb4', 'cbA', 'cbTIE', 'cb1A', 'cb1B'],
        breakerNames: (top) => (top === 'ring' ? '52-1, 52-4' : (top === 'breakerhalf' ? '52-A, 52-TIE' : (top === 'doublebreaker' ? '52-1A, 52-1B' : '52-69'))),
        upstreamDevices: () => ['51-HV (67/21 Zone-1)', '51-HV (Backup)'],
        tccKeys: ['topo'], refSide: 'hv', xrRatio: 16.0,
        defaultPos: (L) => ({ x: L.gantryX + 2.5, y: 6.8, z: 0 })
      },
      node_cascade_mid: {
        id: 'node_cascade_mid', group: 'Substation A (HV/EHV)',
        name: 'Node 1B: Intermediate Cascading Step-Down Bus (230/138/69 kV)',
        zone: 'ANSI 87T Autotransformer Diff + 51-HV Cascade OC',
        breakers: ['cbMain', 'cb1', 'cb2', 'cbTIE', 'cb2A', 'cb2B'],
        breakerNames: () => '52-ATR Cascade Interstage Breaker',
        upstreamDevices: () => ['87T Autotransformer Diff', '51-HV Backup'],
        tccKeys: ['topo', 'diff'], refSide: 'hv', xrRatio: 15.0,
        defaultPos: (L) => ({ x: L.txX - 5.5, y: 6.2, z: 0 })
      },
      node2_hv_bus: {
        id: 'node2_hv_bus', group: 'Substation A (HV/EHV)',
        name: 'Node 2: Substation A Primary HV Busbar',
        zone: 'ANSI 87B High-Voltage Bus Differential + 50BF',
        breakers: ['cbMain', 'cbBT', 'cb1', 'cb2', 'cb3', 'cb4', 'cbA', 'cbTIE', 'cbB', 'cb1A', 'cb2A'],
        breakerNames: (top) => (top === 'ring' ? '52-1..52-4' : (top === 'breakerhalf' ? '52-A, 52-TIE, 52-B' : (top === 'doublebreaker' ? '52-1A, 52-2A (Bus A Diff)' : (top === 'maintransfer' ? '52-69, 52-BT' : '52-69')))),
        upstreamDevices: () => ['87B Bus Diff (0.025 s)', '51-HV Backup'],
        tccKeys: ['diff', 'topo'], refSide: 'hv', xrRatio: 14.5,
        defaultPos: (L) => ({ x: L.busbarX || L.cbX, y: 5.8, z: 0 })
      },
      node3_tx_hv: {
        id: 'node3_tx_hv', group: 'Substation A (HV/EHV)',
        name: 'Node 3: TR-01 Primary HV Bushings (H1/H2/H3)',
        zone: 'ANSI 87T Transformer Differential + 63 Buchholz',
        breakers: ['cbMain', 'cb1', 'cb2', 'cbTIE', 'cbB', 'cb2A', 'cb2B', 'cbLV'],
        breakerNames: (top) => (top === 'ring' ? '52-1, 52-2 + 52-LV' : (top === 'breakerhalf' ? '52-TIE, 52-B + 52-LV' : (top === 'doublebreaker' ? '52-2A, 52-2B + 52-LV' : '52-69 + 52-LV'))),
        upstreamDevices: () => ['87T Differential (0.025 s)', '51-HV Backup'],
        tccKeys: ['diff', 'topo'], refSide: 'hv', xrRatio: 14.0,
        defaultPos: (L) => ({ x: L.txX - 1.2, y: 4.8, z: 0 })
      },
      node4_tx_lv: {
        id: 'node4_tx_lv', group: 'Substation A (LV)',
        name: 'Node 4: TR-01 Secondary Bushings / NGR Lead (X1/X2/X3/X0)',
        zone: 'ANSI 87T Differential + 51G Neutral Overcurrent',
        breakers: ['cbMain', 'cb1', 'cb2', 'cbTIE', 'cbB', 'cb2A', 'cb2B', 'cbLV'],
        breakerNames: (top) => (top === 'ring' ? '52-1, 52-2 + 52-LV' : (top === 'breakerhalf' ? '52-TIE, 52-B + 52-LV' : (top === 'doublebreaker' ? '52-2A, 52-2B + 52-LV' : '52-69 + 52-LV'))),
        upstreamDevices: () => ['87T Diff (0.025 s)', '51-LV', '51-HV'],
        tccKeys: ['diff', 'lv', 'topo'], refSide: 'lv', xrRatio: 12.0,
        defaultPos: (L) => ({ x: L.txX + 1.4, y: 4.4, z: 0 })
      },
      node5_lv_bus: {
        id: 'node5_lv_bus', group: 'Substation A (LV)',
        name: 'Node 5: Substation A Secondary Main Bus (13.8 kV Bus A)',
        zone: 'ANSI 87B-LV / 50/51-LV Secondary Main VCB',
        breakers: ['cbLV', 'cbCap'],
        breakerNames: () => '52-LV (Main LV VCB), 52-CAP',
        upstreamDevices: () => ['50/51-LV Main', '51-HV Backup'],
        tccKeys: ['lv', 'topo'], refSide: 'lv', xrRatio: 11.2,
        defaultPos: (L) => ({ x: L.secBusX, y: 4.8, z: 0 })
      },
      node7_ind_hv: {
        id: 'node7_ind_hv', group: 'HV Industrial Corridor',
        name: 'Node 7: Dedicated HV Industrial Sub-Tx Feeder (52-IND)',
        zone: 'ANSI 50/51-IND & 21-IND Distance OC (Backup 51-HV)',
        breakers: ['cbIndHv'],
        breakerNames: () => '52-IND (Dedicated 69/138 kV Industrial Bay)',
        upstreamDevices: () => ['50/51-IND', '51-HV Backup'],
        tccKeys: ['ind', 'topo'], refSide: 'hv', xrRatio: 9.5, defaultDistPct: 40,
        defaultPos: (L) => ({ x: L.fdrGantryX + 6.0, y: 7.5, z: L.fdr1Z - 26.0 })
      },
      node8_ind_sub: {
        id: 'node8_ind_sub', group: 'HV Industrial Corridor',
        name: 'Node 8: Customer Heavy Industrial Substation (25 MVA, 52-CUST)',
        zone: 'ANSI 52-CUST + 50/51-IND Selective Backup',
        breakers: ['cbIndHv'],
        breakerNames: () => '52-CUST (Customer) -> Backup 52-IND',
        upstreamDevices: () => ['52-CUST', '50/51-IND', '51-HV Backup'],
        tccKeys: ['ind', 'topo'], refSide: 'hv', xrRatio: 7.8, defaultDistPct: 100,
        defaultPos: (L) => ({ x: L.fdrGantryX + 104.0, y: 5.5, z: L.fdr1Z - 68.0 })
      },
      node6_fdr1: {
        id: 'node6_fdr1', group: '13.8 kV City Loop (West)',
        name: 'Node 6A: Feeder 01 Main Overhead Trunk (52-F1)',
        zone: 'ANSI 50/51-F1 Phase OC + 51N Ground OC',
        breakers: ['cbF1'],
        breakerNames: () => '52-F1 ONLY (F2 & TR-01 remain live)',
        upstreamDevices: () => ['50/51-F1', '50/51-LV Main', '51-HV'],
        tccKeys: ['fdr', 'lv', 'topo'], refSide: 'lv', xrRatio: 6.5, defaultDistPct: 35,
        defaultPos: (L) => ({ x: L.fdrGantryX + 18.0, y: 7.2, z: L.fdr1Z })
      },
      node9_acr1: {
        id: 'node9_acr1', group: '13.8 kV City Loop (West)',
        name: 'Node 9: Pole Recloser 79-ACR1 Load-Side Trunk',
        zone: 'ANSI 79-ACR1 (Fast Curve A -> Slow B) -> Backup 52-F1',
        breakers: ['cbACR1'],
        breakerNames: () => '79-ACR1 Recloser (Backup: 52-F1)',
        upstreamDevices: () => ['79-ACR1 Fast/Slow', '50/51-F1', '50/51-LV'],
        tccKeys: ['recFast', 'recSlow', 'fdr', 'lv'], refSide: 'lv', xrRatio: 4.8, defaultDistPct: 50,
        defaultPos: (L) => ({ x: L.fdrGantryX + 48.0, y: 7.2, z: L.fdr1Z })
      },
      node10_res_lat: {
        id: 'node10_res_lat', group: '13.8 kV City Loop (West)',
        name: 'Node 10: 34-SECT & 100K Fuse Overhead Residential Lateral (RES 50 kVA)',
        zone: 'Fuse-Saving: 79-ACR1 Fast < 100K Fuse Clear < 79-ACR1 Slow',
        breakers: ['fuseCutout'],
        breakerNames: () => '100K Fuse Cutout / 34-SECT (Saved by 79-ACR1 Fast)',
        upstreamDevices: () => ['100K Fuse', '79-ACR1', '50/51-F1', '50/51-LV'],
        tccKeys: ['recFast', 'fuseMin', 'fuseClear', 'recSlow', 'fdr'], refSide: 'lv', xrRatio: 3.4, defaultDistPct: 75,
        defaultPos: (L) => ({ x: L.fdrGantryX + 201.0, y: 7.0, z: L.fdr1Z - 8.5 })
      },
      node11_urd_pad: {
        id: 'node11_urd_pad', group: '13.8 kV City Loop (West)',
        name: 'Node 11: Gated URD Riser Pole & Loop Pad-Mounts (150 kVA × 6)',
        zone: '34-SECT Sectionalizer (Count=2) + Bay-O-Net Fuse + 79-ACR1',
        breakers: ['sec34'],
        breakerNames: () => '34-SECT Sectionalizer / Bay-O-Net Fuse',
        upstreamDevices: () => ['34-SECT (Arm=160A)', '79-ACR1 Slow', '50/51-F1', '50/51-LV'],
        tccKeys: ['sect', 'recSlow', 'fdr', 'lv'], refSide: 'lv', xrRatio: 4.0, defaultDistPct: 65,
        defaultPos: (L) => ({ x: L.fdrGantryX + 170.0, y: 2.2, z: L.fdr1Z - 14.0 })
      },
      node6_fdr2: {
        id: 'node6_fdr2', group: '13.8 kV City Loop (West)',
        name: 'Node 6B: Feeder 02 Commercial Express Trunk (52-F2 / 79-F2)',
        zone: 'ANSI 50/51-F2 + 79-F2 Commercial Recloser',
        breakers: ['cbF2Rec'],
        breakerNames: () => '79-F2 / 52-F2 (F1 & TR-01 stay energized)',
        upstreamDevices: () => ['79-F2 / 50/51-F2', '50/51-LV Main', '51-HV'],
        tccKeys: ['recSlow', 'fdr', 'lv', 'topo'], refSide: 'lv', xrRatio: 5.8, defaultDistPct: 45,
        defaultPos: (L) => ({ x: L.fdrGantryX + 47.0, y: 7.2, z: L.fdr2Z })
      },
      node12_cbd_bus: {
        id: 'node12_cbd_bus', group: '13.8 kV City Loop (West)',
        name: 'Node 12: CBD Commercial District & Hospital 750 kVA Bus',
        zone: '750 kVA Pad-Mount Fuse + 79-F2 / 52-F2 Selective Trip',
        breakers: ['cbF2Rec'],
        breakerNames: () => '79-F2 Recloser (Backup: 52-F2)',
        upstreamDevices: () => ['100K/Bay-O-Net Fuse', '79-F2', '50/51-F2', '50/51-LV'],
        tccKeys: ['fuseClear', 'recSlow', 'fdr', 'lv'], refSide: 'lv', xrRatio: 4.2, defaultDistPct: 80,
        defaultPos: (L) => ({ x: L.fdrGantryX + 206.0, y: 2.2, z: L.fdr2Z + 12.0 })
      },
      node13_tie1: {
        id: 'node13_tie1', group: 'Loop Ties & East City',
        name: 'Node 13: North Loop Tie Recloser 79-TIE1 (F1 ↔ F3 Boundary)',
        zone: 'Loop Automation: Trips Active Source Feed (F1 or F3) + Opens Tie',
        breakers: ['cbTieB'],
        breakerNames: (top, br) => (br && br.fdr3_from_subA ? '79-TIE1 (Sub A Back-Feed Active)' : '79-TIE1 Boundary / 52-F1 / 52-F3'),
        upstreamDevices: (br) => (br && br.fdr3_from_subA ? ['79-TIE1', '79-ACR1', '50/51-F1', '50/51-LV'] : ['79-TIE1', '50/51-F3 (Sub B)', '50/51-LVB']),
        tccKeys: ['recSlow', 'fdr', 'lv'], refSide: 'lv', xrRatio: 3.6, defaultDistPct: 90,
        defaultPos: (L) => ({ x: L.fdrGantryX + 221.0, y: 7.2, z: L.fdr1Z })
      },
      node14_tie2: {
        id: 'node14_tie2', group: 'Loop Ties & East City',
        name: 'Node 14: South Loop Tie Switch 89-TIE2 (F2 ↔ F4 Boundary)',
        zone: 'Loop Automation: Cleared by Active Source Recloser/Breaker',
        breakers: ['cbTie2'],
        breakerNames: () => '89-TIE2 Tie / Active Feeder Breaker (52-F2 or 52-F4)',
        upstreamDevices: (br) => (br && br.fdr4_from_subA ? ['79-F2', '50/51-F2', '50/51-LV'] : ['50/51-F4 (Sub B)', '50/51-LVB']),
        tccKeys: ['fdr', 'lv'], refSide: 'lv', xrRatio: 3.5, defaultDistPct: 90,
        defaultPos: (L) => ({ x: L.fdrGantryX + 221.0, y: 7.2, z: L.fdr2Z })
      },
      node15_uni_bus: {
        id: 'node15_uni_bus', group: 'Loop Ties & East City',
        name: 'Node 15: East University Campus Pad-Mount Bus (500 kVA, Feeder 03)',
        zone: 'ANSI 50/51-F3 (Normal) OR 79-TIE1 / 52-F1 (Back-Feed Transfer)',
        breakers: ['cbF3'],
        breakerNames: (top, br) => (br && br.fdr3_from_subA ? '79-TIE1 -> 52-F1 (Sub A Back-Feed Path)' : '52-F3 ONLY (Tie Substation B)'),
        upstreamDevices: (br) => (br && br.fdr3_from_subA ? ['79-TIE1 / 79-ACR1', '50/51-F1 (Sub A)', '50/51-LV'] : ['50/51-F3 (Sub B)', '50/51-LVB', '51-HV (Sub B)']),
        tccKeys: ['recSlow', 'fdr', 'lv'], refSide: 'lv', xrRatio: 3.9, defaultDistPct: 85,
        defaultPos: (L) => ({ x: L.fdrGantryX + 244.0, y: 2.2, z: L.fdr1Z - 14.0 })
      },
      node16_mun_bus: {
        id: 'node16_mun_bus', group: 'Loop Ties & East City',
        name: 'Node 16: Municipal Water & Logistics Park Bus (1 MVA, Feeder 04)',
        zone: 'ANSI 50/51-F4 (Normal) OR 89-TIE2 / 52-F2 (Back-Feed Transfer)',
        breakers: ['cbF4'],
        breakerNames: (top, br) => (br && br.fdr4_from_subA ? '79-F2 -> 52-F2 (Sub A Back-Feed via 89-TIE2)' : '52-F4 ONLY (Tie Substation B)'),
        upstreamDevices: (br) => (br && br.fdr4_from_subA ? ['79-F2', '50/51-F2 (Sub A)', '50/51-LV'] : ['50/51-F4 (Sub B)', '50/51-LVB', '51-HV (Sub B)']),
        tccKeys: ['fdr', 'lv', 'topo'], refSide: 'lv', xrRatio: 4.1, defaultDistPct: 85,
        defaultPos: (L) => ({ x: L.fdrGantryX + 244.0, y: 2.2, z: L.fdr2Z + 15.0 })
      },
      node17_subb_hv: {
        id: 'node17_subb_hv', group: 'Tie Substation B',
        name: 'Node 17: Tie Substation B HV Busbar',
        zone: 'ANSI 87B-SubB High-Speed Bus Differential',
        breakers: ['cbTieA'],
        breakerNames: () => 'Sub B HV Ring/Main Breakers + 52-LVB',
        upstreamDevices: () => ['87B-SubB Diff (0.025 s)', '51-HV (Sub B)'],
        tccKeys: ['diff', 'topo'], refSide: 'hv', xrRatio: 13.5,
        defaultPos: (L) => ({ x: L.fdrGantryX + 435.0, y: 5.5, z: L.fdr1Z })
      },
      node18_tr02: {
        id: 'node18_tr02', group: 'Tie Substation B',
        name: 'Node 18: Tie Transformer TR-02 Terminals (15 MVA)',
        zone: 'ANSI 87T-TR02 Transformer Differential + 63 Buchholz',
        breakers: ['cbLVB', 'cbTieA'],
        breakerNames: () => 'Sub B HV Breaker + 52-LVB',
        upstreamDevices: () => ['87T-TR02 Diff (0.025 s)', '50/51-LVB', '51-HV (Sub B)'],
        tccKeys: ['diff', 'lv', 'topo'], refSide: 'lv', xrRatio: 11.5,
        defaultPos: (L) => ({ x: L.fdrGantryX + 415.0, y: 4.4, z: L.fdr1Z })
      },
      node19_subb_lv: {
        id: 'node19_subb_lv', group: 'Tie Substation B',
        name: 'Node 19: Tie Substation B 13.8 kV Main Bus B',
        zone: 'ANSI 50/51-LVB Secondary Bus Overcurrent',
        breakers: ['cbLVB'],
        breakerNames: () => '52-LVB (Sub B Main VCB — East loads ready for Sub A back-feed)',
        upstreamDevices: () => ['50/51-LVB Main', '51-HV (Sub B)'],
        tccKeys: ['lv', 'topo'], refSide: 'lv', xrRatio: 10.2,
        defaultPos: (L) => ({ x: L.fdrGantryX + 395.0, y: 4.5, z: L.fdr1Z })
      },
      node20_fdr3: {
        id: 'node20_fdr3', group: 'Tie Substation B',
        name: 'Node 20: Tie Substation B Feeder 03 Head (52-F3)',
        zone: 'ANSI 50/51-F3 Feeder Overcurrent + 51N',
        breakers: ['cbF3'],
        breakerNames: () => '52-F3 ONLY (52-F4 stays live)',
        upstreamDevices: () => ['50/51-F3', '50/51-LVB Main', '51-HV (Sub B)'],
        tccKeys: ['fdr', 'lv', 'topo'], refSide: 'lv', xrRatio: 6.2, defaultDistPct: 25,
        defaultPos: (L) => ({ x: L.fdrGantryX + 382.0, y: 4.5, z: L.fdr1Z })
      },
      node21_fdr4: {
        id: 'node21_fdr4', group: 'Tie Substation B',
        name: 'Node 21: Tie Substation B Feeder 04 Head (52-F4)',
        zone: 'ANSI 50/51-F4 Feeder Overcurrent + 51N',
        breakers: ['cbF4'],
        breakerNames: () => '52-F4 ONLY (52-F3 stays live)',
        upstreamDevices: () => ['50/51-F4', '50/51-LVB Main', '51-HV (Sub B)'],
        tccKeys: ['fdr', 'lv', 'topo'], refSide: 'lv', xrRatio: 6.0, defaultDistPct: 25,
        defaultPos: (L) => ({ x: L.fdrGantryX + 382.0, y: 4.5, z: L.fdr2Z })
      }
    };

    function togglePinpointFaultMode(forceVal) {
      AppState.pinpointFaultMode = (typeof forceVal === 'boolean') ? forceVal : !AppState.pinpointFaultMode;
      document.body.classList.toggle('pinpoint-fault-cursor', AppState.pinpointFaultMode);
      const btn = document.getElementById('btn-pinpoint-fault-mode');
      const btnExp = document.getElementById('btn-sld-exp-pinpoint');
      if (btn) {
        btn.classList.toggle('active', AppState.pinpointFaultMode);
        btn.innerText = AppState.pinpointFaultMode
          ? '🎯 Pinpoint Fault Mode: ON (Click Yard / SLD)'
          : '🎯 Pinpoint Fault Location Mode (Off)';
      }
      if (btnExp) {
        btnExp.classList.toggle('active', AppState.pinpointFaultMode);
        btnExp.innerText = AppState.pinpointFaultMode ? '🎯 Click SLD Node to Inject Fault (ON)' : '🎯 Pinpoint Fault Mode (SLD)';
      }
      if (AppState.pinpointFaultMode) {
        showToast('Pinpoint Fault Mode ACTIVE: Click any 3D equipment/bus or any of 23 SLD nodes to inject a fault.');
      }
    }

    function map3DHitToPinpointNode(compId, circuitTag, hitPoint) {
      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);
      let nodeId = 'node2_hv_bus';
      let distPct = 50;
      if (compId === 'gantry' || compId === 'arrester' || compId === 'ctvt' || circuitTag === 'incoming' || circuitTag === 'post_dsA') {
        nodeId = 'node1_incoming';
      } else if (compId === 'disconnect' || compId === 'breaker' || compId === 'busbar') {
        nodeId = 'node2_hv_bus';
      } else if (compId === 'transformer') {
        const splitX = L.txX + 0.1;
        nodeId = (hitPoint && hitPoint.x > splitX) ? 'node4_tx_lv' : 'node3_tx_hv';
      } else if (compId === 'secondary' || compId === 'auxiliary' || compId === 'sst_100') {
        nodeId = (circuitTag === 'sec_lv' && hitPoint && hitPoint.x < L.secCbX) ? 'node4_tx_lv' : 'node5_lv_bus';
      } else if (compId === 'ind_hv_bay') {
        nodeId = 'node7_ind_hv'; distPct = 40;
      } else if (compId === 'dt_ind_1500' || (circuitTag === 'ind_hv' && hitPoint && hitPoint.x > L.fdrGantryX + 60)) {
        nodeId = 'node8_ind_sub'; distPct = 100;
      } else if (circuitTag === 'ind_hv') {
        nodeId = 'node7_ind_hv'; distPct = 40;
      } else if (compId === 'dist_recloser') {
        nodeId = 'node9_acr1'; distPct = 50;
      } else if (compId === 'dt_res_50' || compId === 'dist_fuse_cutout' || circuitTag === 'dist_lateral') {
        nodeId = 'node10_res_lat'; distPct = 75;
      } else if (compId === 'dt_urd_pad' || compId === 'urd_riser_pole' || compId === 'urd_vista_swgr' || compId === 'dist_sectionalizer') {
        nodeId = 'node11_urd_pad'; distPct = 65;
      } else if (compId === 'dt_com_750') {
        nodeId = 'node12_cbd_bus'; distPct = 80;
      } else if (compId === 'dt_uni_500') {
        nodeId = 'node15_uni_bus'; distPct = 85;
      } else if (compId === 'dt_mun_1000') {
        nodeId = 'node16_mun_bus'; distPct = 85;
      } else if (compId === 'substation_b' || compId === 'substation_gate') {
        if (hitPoint && hitPoint.x < L.fdrGantryX + 260) {
          nodeId = 'node13_tie1';
        } else if (circuitTag === 'dist_f3') {
          nodeId = 'node20_fdr3';
        } else if (circuitTag === 'dist_f4') {
          nodeId = 'node21_fdr4';
        } else if (circuitTag === 'dist_sub_b') {
          nodeId = (hitPoint && hitPoint.x > L.fdrGantryX + 410) ? 'node17_subb_hv' : 'node18_tr02';
        } else {
          nodeId = 'node19_subb_lv';
        }
      } else if (circuitTag === 'dist_f3') {
        nodeId = 'node20_fdr3'; distPct = 50;
      } else if (circuitTag === 'dist_f4') {
        nodeId = 'node21_fdr4'; distPct = 50;
      } else if (compId === 'feeders' || circuitTag === 'fdr1' || circuitTag === 'fdr2' || circuitTag === 'dist_f1_sec1' || circuitTag === 'dist_f1_sec2' || circuitTag === 'dist_f2_main') {
        const useFdr2 = circuitTag === 'fdr2' || circuitTag === 'dist_f2_main' || (hitPoint && Math.abs(hitPoint.z - L.fdr2Z) < Math.abs(hitPoint.z - L.fdr1Z));
        nodeId = useFdr2 ? 'node6_fdr2' : 'node6_fdr1';
        if (hitPoint) {
          const span = Math.max(6.0, L.fdrGantryX - L.secBusX);
          const raw = Math.round(((hitPoint.x - L.secBusX) / span) * 100);
          distPct = Math.max(5, Math.min(100, raw));
        }
      }
      return { nodeId, distPct };
    }

    function placeFaultMarker3D(pos) {
      if (!scene || !pos) return;
      if (faultMarker3D) {
        scene.remove(faultMarker3D);
        faultMarker3D = null;
      }
      const grp = new THREE.Group();
      grp.name = 'pinpoint-fault-marker';
      grp.position.set(pos.x, pos.y, pos.z);
      const core = new THREE.Mesh(
        new THREE.OctahedronGeometry(0.45, 0),
        new THREE.MeshBasicMaterial({ color: 0xfef08a })
      );
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(0.85, 0.06, 8, 24),
        new THREE.MeshBasicMaterial({ color: 0xef4444, wireframe: true })
      );
      ring.rotation.x = Math.PI / 2;
      const spire = new THREE.Mesh(
        new THREE.ConeGeometry(0.22, 1.4, 6),
        new THREE.MeshBasicMaterial({ color: 0xf43f5e, transparent: true, opacity: 0.85 })
      );
      spire.position.y = 0.8;
      spire.rotation.x = Math.PI;
      grp.add(core, ring, spire);
      scene.add(grp);
      faultMarker3D = grp;
    }

    window.plotActiveFaultOnTcc = function(optNodeId) {
      const targetNode = optNodeId || AppState.scFaultLoc || AppState.pinpointFaultNode || 'node5_lv_bus';
      AppState.scFaultLoc = targetNode;
      AppState.pinpointFaultNode = targetNode;
      const meta = PINPOINT_FAULT_NODES[targetNode] || PINPOINT_FAULT_NODES.node5_lv_bus;
      const sc = computeShortCircuitMetrics();
      const vs = sc.vs;
      const refSide = meta.refSide || (sc.vBaseKv > 40 ? 'hv' : 'lv');
      const ampAtRef = (refSide === 'hv' && sc.vBaseKv < vs.hvKv)
        ? Math.round((sc.iSymKa * 1000) * (sc.vBaseKv / vs.hvKv))
        : ((refSide === 'lv' && sc.vBaseKv > vs.lvKv)
          ? Math.round((sc.iSymKa * 1000) * (sc.vBaseKv / vs.hvKv) * (vs.hvKv / (vs.distKv || 13.8)))
          : Math.round(sc.iSymKa * 1000));

      if (AppState.tccState) {
        AppState.tccState.topo = AppState.busTopology || AppState.tccState.topo || 'single';
        AppState.tccState.refSide = refSide;
        AppState.tccState.cursorAmp = Math.max(40, Math.min(90000, ampAtRef || 4200));
        AppState.tccState.focusedRelay = (meta.tccKeys && meta.tccKeys[0] === 'fdr') ? '50_51_f1' : ((meta.tccKeys && meta.tccKeys[0] === 'recFast') ? 'recloser' : 'all');
        AppState.tccState.viewMode = 'highlight';
        AppState.tccState.pinnedFault = {
          nodeId: meta.id,
          nodeLabel: meta.name,
          faultType: AppState.scFaultType || '3ph',
          iSymKa: sc.iSymKa,
          iPeakKa: sc.iPeakKa,
          iAmpsPlot: AppState.tccState.cursorAmp,
          vBaseKv: sc.vBaseKv,
          upstreamDevices: sc.upstreamDevices || [],
          highlightKeys: meta.tccKeys || ['fdr', 'lv', 'topo']
        };
      }
      openAnalysisModal('tcc');
      showToast(`📈 Plotted ${meta.name} (I_f = ${sc.iSymKa.toFixed(2)} kA @ ${sc.vBaseKv} kV) on TCC Coordination Graph!`);
    };

    function updatePinpointFaultReadout(nodeId, sc, trippedListTxt, vs, meta) {
      const ro = document.getElementById('pinpoint-fault-readout');
      if (!ro) return;
      const isFdr = (nodeId === 'node6_fdr1' || nodeId === 'node6_fdr2' || nodeId === 'node9_acr1' || nodeId === 'node10_res_lat' || nodeId === 'node11_urd_pad' || nodeId === 'node12_cbd_bus' || nodeId === 'node15_uni_bus' || nodeId === 'node16_mun_bus');
      const d = AppState.pinpointFeederDistPct || 50;
      const sliderHtml = isFdr ? `
        <div style="margin-top:6px; padding-top:5px; border-top:1px solid rgba(248,113,113,0.3);">
          <label style="display:flex; justify-content:space-between; font-size:9.5px; color:#fca5a5;">
            <span>Feeder Fault Distance:</span><strong>${d}% (${(d * 0.02).toFixed(2)} km)</strong>
          </label>
          <input type="range" min="5" max="100" step="5" value="${d}" style="width:100%;"
            oninput="AppState.pinpointFeederDistPct=parseInt(this.value,10); triggerPinpointedFault('${nodeId}', AppState.pinpointFeederDistPct, AppState.pinpointWorldPos);">
        </div>` : '';
      ro.innerHTML = `
        <div style="color:#f87171; font-weight:700; margin-bottom:2px;">⚡ FAULT: ${meta.name} (${sc.vBaseKv} kV)</div>
        <div>I<sub>f,sym</sub>: <strong style="color:#fef08a;">${sc.iSymKa.toFixed(2)} kA</strong> | I<sub>peak</sub>: <strong>${sc.iPeakKa.toFixed(2)} kA</strong> | X/R: <strong>${(sc.xrRatio || 10).toFixed(1)}</strong></div>
        <div>Zone: <span style="color:#67e8f9;">${meta.zone}</span></div>
        <div>Tripped: <span style="color:#fde68a;">${trippedListTxt}</span></div>
        ${sliderHtml}
        <button class="btn" style="width:100%; justify-content:center; margin-top:6px; padding:4px 8px; font-size:10px; background:rgba(250,204,21,0.18); border-color:#facc15; color:#fef08a;" onclick="plotActiveFaultOnTcc('${meta.id}')">
          📈 Plot This Fault on TCC Coordination Graph
        </button>
      `;
    }

    function triggerPinpointedFault(nodeId, distPct = 50, worldPt = null) {
      const meta = PINPOINT_FAULT_NODES[nodeId] || PINPOINT_FAULT_NODES.node5_lv_bus;
      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);
      const vs = getVoltageSpec(AppState.voltageClass);
      const top = AppState.busTopology || 'single';
      const br = computeEnergizedBranches();

      AppState.pinpointFaultNode = meta.id;
      AppState.pinpointFeederDistPct = distPct;
      AppState.scFaultLoc = meta.id;
      AppState.isFaultActive = true;
      AppState.faultType = meta.id;

      const pos = worldPt ? { x: worldPt.x, y: Math.max(1.8, worldPt.y), z: worldPt.z } : meta.defaultPos(L);
      AppState.pinpointWorldPos = pos;
      placeFaultMarker3D(pos);

      const sc = computeShortCircuitMetrics();
      if (AppState.tccState) {
        const isHvFault = (meta.refSide === 'hv');
        AppState.tccState.refSide = isHvFault ? 'hv' : 'lv';
        AppState.tccState.cursorAmp = Math.max(80, Math.min(85000, Math.round(sc.iSymKa * 1000)));
        AppState.tccState.topo = top;
        AppState.tccState.pinnedFault = {
          nodeId: meta.id,
          nodeLabel: meta.name,
          faultType: AppState.scFaultType || '3ph',
          iSymKa: sc.iSymKa,
          iPeakKa: sc.iPeakKa,
          iAmpsPlot: AppState.tccState.cursorAmp,
          vBaseKv: sc.vBaseKv,
          upstreamDevices: sc.upstreamDevices || [],
          highlightKeys: meta.tccKeys || ['fdr', 'lv', 'topo']
        };
      }
      const stEl = document.getElementById('telem-grid-status');
      const iEl = document.getElementById('telem-current');
      if (stEl) { stEl.innerText = `FAULT: ${meta.name.split(':')[0].toUpperCase()}`; stEl.style.color = '#ef4444'; }
      if (iEl) iEl.innerText = `${(sc.iSymKa * 1000).toFixed(0)} A`;

      if (dynamicArcLight) {
        dynamicArcLight.color.setHex(0xf43f5e);
        dynamicArcLight.position.set(pos.x, pos.y + 0.6, pos.z);
        dynamicArcLight.intensity = 14;
      }
      if (soundEngine && typeof soundEngine.playNoiseBurst === 'function') {
        soundEngine.playNoiseBurst(0.35, 0.75);
      }

      const trippedListTxt = meta.breakerNames(top, br);
      updatePinpointFaultReadout(meta.id, sc, trippedListTxt, vs, meta);
      renderLiveSLD();

      showToast(`⚡ ${meta.name}: I_f = ${sc.iSymKa.toFixed(2)} kA (${meta.zone}) — Tripping ${trippedListTxt}...`);

      if (pinpointTripTimer) clearTimeout(pinpointTripTimer);
      pinpointTripTimer = setTimeout(() => {
        pinpointTripTimer = null;
        const activeMetaIds = new Set(
          (typeof SWITCH_CATALOG !== 'undefined' ? SWITCH_CATALOG : [])
            .filter(item => item.topologies.includes(top))
            .map(item => item.id)
        );
        // Adapt East load breaker tripping if back-fed from Substation A via closed ties
        let clearBreakers = meta.breakers.slice();
        if (meta.id === 'node15_uni_bus' && br.fdr3_from_subA) clearBreakers = ['cbTieB'];
        if (meta.id === 'node16_mun_bus' && br.fdr4_from_subA) clearBreakers = ['cbTie2'];
        if (meta.id === 'node10_res_lat' && br.fdr1_from_subB) clearBreakers = ['fuseCutout'];
        clearBreakers.forEach(swKey => {
          if (Object.prototype.hasOwnProperty.call(AppState.switchStates, swKey) && (activeMetaIds.size === 0 || activeMetaIds.has(swKey))) {
            AppState.switchStates[swKey] = false;
          }
        });
        AppState.isFaultActive = false;
        if (dynamicArcLight) dynamicArcLight.intensity = 0;
        if (soundEngine && typeof soundEngine.playBreakerTrip === 'function') {
          soundEngine.playBreakerTrip();
        }
        syncAllSwitchesTo3D();
        renderSwitchMatrix();
        renderLiveSLD();
        if (stEl) { stEl.innerText = `ISOLATED (${meta.id.replace('node', 'Z')})`; stEl.style.color = '#f59e0b'; }
      }, 550);
    }

    // SIMULATION EVENT 5: AUTOMATED LOTO SAFE SWITCHING ISOLATION SEQUENCE
    function triggerSafeIsolationSequence() {
      showToast('Initiating Life-Safe Maintenance Isolation Sequence (OSH Rule 1210 / PEC 2017)...');

      // Step 1: Open CB-69-1 to interrupt load current
      setTimeout(() => {
        AppState.switchStates.cbMain = false;
        soundEngine.playBreakerTrip();
        syncAllSwitchesTo3D();
        renderSwitchMatrix();
        renderLiveSLD();
        showToast('Step 1/4: Circuit Breaker 52 Opened. Arc extinguished.');

        // Step 2: Open Disconnect Switch 89 under zero load
        setTimeout(() => {
          AppState.switchStates.dsMain = false;
          soundEngine.playDisconnectOperate();
          syncAllSwitchesTo3D();
          renderSwitchMatrix();
          renderLiveSLD();
          showToast('Step 2/4: Disconnect Switch 89 Opened. Visible physical air gap established.');

          // Step 3: Close Earth Blade 89E to drain trapped electrostatic charge
          setTimeout(() => {
            AppState.switchStates.earthMain = true;
            soundEngine.playDisconnectOperate();
            syncAllSwitchesTo3D();
            renderSwitchMatrix();
            renderLiveSLD();
            showToast('Step 3/4: Earth Switch 89E Closed. Trapped capacitive charges discharged to earth grid.');

            // Step 4: Apply Padlocks & LOTO Danger Tags
            setTimeout(() => {
              renderLiveSLD();
              showToast('Step 4/4: Padlocks & LOTO Danger Tags Applied. SAFE: ZERO ENERGY STATE VERIFIED!');
            }, 600);
          }, 800);
        }, 800);
      }, 400);
    }

    // INTERLOCK ENFORCEMENT & DANGEROUS ARC FLASH DEMO
    function toggleDisconnectState() {
      operateSwitch('dsMain');
    }

    function animateDisconnectBlades(isClosed) {
      const disc = switchyardObjects.disconnect;
      if (!disc || !disc.userData.bladeArms) return;
      const targetAngle = isClosed ? 0 : Math.PI / 2.5;

      disc.userData.bladeArms.forEach(ba => {
        ba.arm1.rotation.y = -targetAngle;
        ba.arm2.rotation.y = targetAngle;
      });
    }

    function toggleBreakerState() {
      operateSwitch('cbMain');
    }

    // TRIGGER ARC FLASH BLAST DISASTER
    function triggerArcFlashDisaster() {
      AppState.isFaultActive = true;
      AppState.faultType = 'arcflash';

      dynamicArcLight.color.setHex(0xffffff);
      dynamicArcLight.position.set(-2, 4.6, 0);
      dynamicArcLight.intensity = 25;

      soundEngine.playArcFlashBlast();

      const origX = camera.position.x;
      let shakeCount = 0;
      const shakeInterval = setInterval(() => {
        camera.position.x = origX + (Math.random() - 0.5) * 0.8;
        shakeCount++;
        if (shakeCount > 15) {
          clearInterval(shakeInterval);
          camera.position.x = origX;
        }
      }, 30);

      setTimeout(() => {
        document.getElementById('arc-flash-modal').style.display = 'flex';
      }, 400);
    }

    function closeArcFlashModal() {
      document.getElementById('arc-flash-modal').style.display = 'none';
      dynamicArcLight.intensity = 0;
    }

    function resetAfterArcFlash() {
      closeArcFlashModal();
      triggerNormalState();
    }

    // LAYER TOGGLES
    function togglePowerFlow(enabled) {
      AppState.powerFlowActive = enabled;
      if (powerParticles) powerParticles.visible = enabled;
      showToast(`Power Flow Particle Animation: ${enabled ? 'ON' : 'OFF'}`);
    }

    function toggleGroundXray(enabled) {
      AppState.groundXrayActive = enabled;
      if (switchyardObjects.groundGrid) {
        switchyardObjects.groundGrid.visible = enabled;
      }
      const gl = document.getElementById('ground-legend');
      if (gl) gl.style.display = enabled ? 'flex' : 'none';
      showToast(`IEEE Std 80 Ground Grid X-Ray: ${enabled ? 'VISIBLE (Legend Enabled)' : 'HIDDEN'}`);
    }

    function toggleUrdTrenchXray(enabled) {
      AppState.urdXrayActive = !!enabled;
      const dist = switchyardObjects.distribution;
      if (dist && dist.userData && dist.userData.urdTrenchGroup) {
        dist.userData.urdTrenchGroup.visible = AppState.urdXrayActive;
      }
      if (typeof rebuildPowerFlowPaths === 'function') {
        rebuildPowerFlowPaths();
      }
      showToast(`URD Underground 15 kV Cable Trench X-Ray: ${AppState.urdXrayActive ? 'VISIBLE' : 'HIDDEN (Pavement Covered)'}`);
    }

    function toggleRollingSphere(enabled) {
      AppState.rollingSphereActive = enabled;
      if (switchyardObjects.rollingSphere) {
        switchyardObjects.rollingSphere.visible = enabled;
      }
      showToast(`IEEE Std 998 Rolling Sphere Canopy (rs=45m): ${enabled ? 'VISIBLE' : 'HIDDEN'}`);
    }

    // FIRST PERSON WALK MODE CONTROLS
    function toggleWalkMode(enabled) {
      AppState.isWalkMode = enabled;
      if (controls) controls.enabled = !enabled;
      const hud = document.getElementById('fps-hud');

      if (enabled) {
        hud.style.display = 'block';
        const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType);
        if (typeof buildCollisionBoxes === 'function') buildCollisionBoxes();
        const spawnX = L.ctrlX - 6.5;
        const spawnZ = L.roads ? L.roads.southZ : L.ctrlZ;
        camera.position.set(spawnX, 1.75, spawnZ);
        WalkState.yaw = 0;
        WalkState.pitch = 0;
        AppState.nearestSafePos = { x: spawnX, z: spawnZ };
        AppState.hvDangerSuppressedUntilSafe = false;
        if (controls && controls.target) controls.target.set(spawnX, 1.75, spawnZ - 5);
        showToast('Entered Field Engineer Walk Mode (WASD to Move, Collision & MAD Safety Active)');
      } else {
        hud.style.display = 'none';
        const hm = document.getElementById('hv-danger-modal');
        if (hm) hm.style.display = 'none';
        const wp = document.getElementById('walk-inspect-prompt');
        if (wp) wp.style.display = 'none';
        AppState.isHazardModalLocked = false;
        AppState.walkFocusedTarget = null;
        setCameraPreset('overview');
      }
    }

    function setupWalkEventListeners() {
      window.addEventListener('keydown', (e) => {
        if (e.target && ['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;
        if (AppState.isHazardModalLocked) {
          WalkState.moveForward = WalkState.moveBackward = WalkState.moveLeft = WalkState.moveRight = false;
          WalkState.isMouseDown = false;
          return;
        }
        if (e.code === 'KeyE' && AppState.isWalkMode && !isAnyModalOpen()) {
          if (AppState.walkFocusedTarget) {
            e.preventDefault();
            triggerWalkFocusedAction();
          }
          return;
        }
        switch (e.code) {
          case 'KeyW': case 'ArrowUp': WalkState.moveForward = true; break;
          case 'KeyS': case 'ArrowDown': WalkState.moveBackward = true; break;
          case 'KeyA': case 'ArrowLeft': WalkState.moveLeft = true; break;
          case 'KeyD': case 'ArrowRight': WalkState.moveRight = true; break;
        }
      });

      window.addEventListener('keyup', (e) => {
        switch (e.code) {
          case 'KeyW': case 'ArrowUp': WalkState.moveForward = false; break;
          case 'KeyS': case 'ArrowDown': WalkState.moveBackward = false; break;
          case 'KeyA': case 'ArrowLeft': WalkState.moveLeft = false; break;
          case 'KeyD': case 'ArrowRight': WalkState.moveRight = false; break;
        }
      });

      window.addEventListener('blur', () => {
        WalkState.moveForward = WalkState.moveBackward = WalkState.moveLeft = WalkState.moveRight = false;
        WalkState.isMouseDown = false;
      });

      window.addEventListener('mousedown', (e) => {
        if (AppState.isHazardModalLocked) return;
        if (AppState.isWalkMode && e.target && e.target.id === 'canvas3d') {
          WalkState.isMouseDown = true;
          WalkState.lastMouseX = e.clientX;
          WalkState.lastMouseY = e.clientY;
        }
      });

      window.addEventListener('mouseup', () => {
        WalkState.isMouseDown = false;
      });

      window.addEventListener('mousemove', (e) => {
        if (!AppState.isWalkMode || !WalkState.isMouseDown || AppState.isHazardModalLocked) return;
        const dx = e.clientX - WalkState.lastMouseX;
        const dy = e.clientY - WalkState.lastMouseY;
        WalkState.lastMouseX = e.clientX;
        WalkState.lastMouseY = e.clientY;

        WalkState.yaw -= dx * 0.003;
        WalkState.pitch -= dy * 0.003;
        WalkState.pitch = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, WalkState.pitch));

        const lookTarget = new THREE.Vector3(
          camera.position.x - Math.sin(WalkState.yaw) * 10,
          camera.position.y + Math.sin(WalkState.pitch) * 10,
          camera.position.z - Math.cos(WalkState.yaw) * 10
        );
        camera.lookAt(lookTarget);
      });
    }

    // =========================================================================
    // FIRST-PERSON OBSTACLE COLLISION ENGINE (PLAYER RADIUS R = 0.45 m, EYE Y = 1.75 m)
    // =========================================================================
    let walkBobPhase = 0;

    function buildCollisionBoxes() {
      const L = getBusLayoutConfig(AppState.busTopology, AppState.enclosureType, AppState.voltageClass);
      const pzArr = L.bayPhaseZ || [-3.5, 0, 3.5];
      const boxes = [];
      const addBox = (cx, cz, w, l, label) => {
        boxes.push({ minX: cx - w / 2, maxX: cx + w / 2, minZ: cz - l / 2, maxZ: cz + l / 2, label });
      };

      // 1. TR-01 Main Power Transformer Tank & Oil Containment Berm Wall
      addBox(L.txX, L.txZ, L.voltageClass === '500_230' ? 10.2 : 8.8, L.voltageClass === '500_230' ? 24.4 : 14.8, 'TR-01 Oil Berm');

      // 2. SST-100 Fenced Enclosure & Concrete Blast Wall
      addBox(L.sstX, L.sstZ, 6.0, 5.9, 'SST-100 Fire Barrier & Enclosure');

      // 3. Control House Exterior Walls (West Double Doorway z in [ctrlZ-1.2, ctrlZ+1.2] OPEN to walk inside!)
      const chW = 8.4, chL = 10.8;
      addBox(L.ctrlX, L.ctrlZ - chL / 2 + 0.14, chW, 0.34, 'Control House North Wall');
      addBox(L.ctrlX, L.ctrlZ + chL / 2 - 0.14, chW, 0.34, 'Control House South Wall');
      addBox(L.ctrlX + chW / 2 - 0.14, L.ctrlZ, 0.34, chL, 'Control House East Wall');
      addBox(L.ctrlX - chW / 2 + 0.14, L.ctrlZ - 3.35, 0.34, 4.1, 'Control House West N Wall');
      addBox(L.ctrlX - chW / 2 + 0.14, L.ctrlZ + 3.35, 0.34, 4.1, 'Control House West S Wall');
      // Interior partition wall (leaves doorway x in [ctrlX-2.6 .. ctrlX-1.6] clear)
      addBox(L.ctrlX + 1.2, L.ctrlZ + 1.8, 5.6, 0.24, 'Control House Interior Partition');
      addBox(L.ctrlX - 3.3, L.ctrlZ + 1.8, 1.4, 0.24, 'Control House Interior Partition W');
      // Interior Relay Racks, SCADA Desk & 125V DC Battery Bank
      addBox(L.ctrlX - 0.65, L.ctrlZ - 4.35, 4.0, 0.85, 'Protection Relay Racks');
      addBox(L.ctrlX - 0.2, L.ctrlZ - 1.1, 2.5, 1.0, 'SCADA Engineering Desk');
      addBox(L.ctrlX - 0.8, L.ctrlZ + 4.1, 3.6, 0.9, '125V DC Battery Rack');
      addBox(L.ctrlX + 3.4, L.ctrlZ - 1.5, 0.85, 2.4, 'AC/DC Aux Boards');

      // 4. Primary Outdoor HV Equipment Pedestals (Gantry masts, LA, CT, DS, CB, Topology Breakers)
      const gLegZ = Math.max(5.0, (pzArr[2] || 3.5) + 1.5);
      addBox(L.gantryX, -gLegZ, 1.6, 1.6, 'Gantry Leg N');
      addBox(L.gantryX, gLegZ, 1.6, 1.6, 'Gantry Leg S');

      if (L.enclosure === 'gis') {
        // GIS Hall boundary & interior Local Control Cabinet (solid enclosure when cutaway is off, or tight equipment box)
        if (!AppState.encCutaway) {
          addBox(L.gisX, 0, L.gisW, L.gisL, 'SF6 GIS Switchgear Hall');
        } else {
          addBox(L.gisX, 0, L.gisW - 1.4, Math.max(4.5, L.gisL * 0.65), 'SF6 GIS Pressurized Modules');
        }
      } else {
        pzArr.forEach(pz => {
          addBox(L.laX, pz, 0.85, 0.85, 'SA-HV Pedestal');
          addBox(L.ctX, pz, 0.95, 0.95, 'CT/VT Stand');
          addBox(L.dsX, L.dsZ + pz, 2.1, 0.75, 'DS-89A Frame');
        });
        if (L.scheme === 'single' || L.scheme === 'maintransfer') {
          addBox(L.cbX, 0, 2.9, Math.max(6.2, (pzArr[2] - pzArr[0]) + 1.4), 'CB-52 Main Frame');
          if (L.dsBX !== undefined) {
            pzArr.forEach(pz => addBox(L.dsBX, pz, 2.1, 0.75, 'DS-89B Bus Frame'));
          }
        }
        if (L.scheme === 'maintransfer') {
          addBox(L.cbX, -(pzArr[2] + 2.7), 6.2, 2.0, '89-M Frame');
          addBox(L.cbX, (pzArr[2] + 2.7), 6.2, 2.0, '89-BYP Frame');
          addBox(L.tieX, 0, 6.4, 3.0, '52-BT Bus Tie Frame');
        } else if (L.scheme === 'ring') {
          addBox(L.ringX1, 0, 6.2, 3.0, '52-1 Ring W');
          addBox((L.ringX1 + L.ringX2) / 2, L.ringZ1, 3.0, 6.2, '52-2 Ring N');
          addBox(L.ringX2, 0, 6.2, 3.0, '52-3 Ring E');
          addBox((L.ringX1 + L.ringX2) / 2, L.ringZ2, 3.0, 6.2, '52-4 Ring S');
        } else if (L.scheme === 'breakerhalf') {
          addBox(L.cbX, -16.5, 6.2, 3.0, '52-A Breaker');
          addBox(L.cbX, 0, 6.2, 3.0, '52-TIE Breaker');
          addBox(L.cbX, 16.5, 6.2, 3.0, '52-B Breaker');
        } else if (L.scheme === 'doublebreaker') {
          const bay1X = L.cbX;
          const bay2X = L.bay2X !== undefined ? L.bay2X : (L.cbX + 13.5);
          const zCbAbs = Math.abs(L.cbZ || 11.5);
          addBox(bay1X, -zCbAbs, 6.2, 3.0, '52-1A Breaker');
          addBox(bay1X, zCbAbs, 6.2, 3.0, '52-1B Breaker');
          addBox(bay2X, -zCbAbs, 6.2, 3.0, '52-2A Breaker');
          addBox(bay2X, zCbAbs, 6.2, 3.0, '52-2B Breaker');
        }
      }

      // 5. Secondary 13.8 kV Equipment, Capacitor Bank & Feeder Bay Stands
      addBox(L.capX, L.capZ, 3.6, 3.4, '3.6 MVAR Capacitor Rack');
      if (L.enclosure === 'indoor') {
        const swX = (L.secCbX + L.secBusX) / 2;
        const swZ = (L.fdr1Z + L.fdr2Z) / 2;
        const swW = (L.secBusX - L.secCbX) + 5.2;
        if (!AppState.encCutaway) {
          addBox(swX, swZ, swW, 20.5, 'Indoor Metal-Clad Switchgear Hall');
        } else {
          addBox(L.secBusX - 0.8, swZ, 2.6, 17.5, 'Indoor C37.20.2 VCB Lineup');
        }
        addBox(L.txX + 4.6, 0, 0.55, 13.5, 'TR-01 Indoor Fire Barrier Wall');
      } else {
        addBox(L.secCbX, -0.6, 1.8, 3.0, '52-LV Main VCB');
        const fSpan = Math.max(12.0, L.fdrGantryX - L.secBusX);
        addBox(L.secBusX + fSpan * 0.48, L.fdr1Z, 1.8, 3.0, '52-F1 VCB');
        addBox(L.secBusX + fSpan * 0.48, L.fdr2Z, 1.8, 3.0, '52-F2 VCB');
      }

      AppState.collisionBoxes = boxes;
      rebuildSolidColliders(L, boxes);
      return boxes;
    }

    function rebuildSolidColliders(L, fallbackBoxes) {
      solidColliders = [];
      const padRadius = 0.55;
      const pushBox3 = (minX, maxX, minZ, maxZ, label, customPad = padRadius) => {
        const b3 = new THREE.Box3(
          new THREE.Vector3(minX - customPad, -1.0, minZ - customPad),
          new THREE.Vector3(maxX + customPad, 5.0, maxZ + customPad)
        );
        b3.label = label || 'Solid Collider';
        solidColliders.push(b3);
      };

      // 1. Structural colliders from boxes[] (Control House walls with open West doorway, TR-01, SST-100, pedestals)
      (fallbackBoxes || []).forEach(b => {
        const isDoorwayWall = b.label && b.label.indexOf('Control House West') === 0;
        const isInterior = b.label && b.label.indexOf('Control House Interior') === 0;
        pushBox3(b.minX, b.maxX, b.minZ, b.maxZ, b.label, (isDoorwayWall || isInterior) ? 0.28 : padRadius);
      });

      // 2. Perimeter Chain-Link Fence Colliders (Split at Functional Vehicular Entrance Gates A & B)
      const yb = AppState.yardBounds || { minX: -30, maxX: 52, minZ: -24, maxZ: 24 };
      const envUD = switchyardObjects.env && switchyardObjects.env.userData ? switchyardObjects.env.userData : {};
      const fMinX = L ? (L.yardCenterX - L.yardW / 2) : (yb.minX - 2.0);
      const fMaxX = L ? (L.yardCenterX + L.yardW / 2) : (yb.maxX + 2.0);
      const fMinZ = L ? (L.yardCenterZ - L.yardL / 2) : (yb.minZ - 2.0);
      const fMaxZ = (envUD.gateZ !== undefined) ? envUD.gateZ : (L ? (L.yardCenterZ + L.yardL / 2) : (yb.maxZ + 2.0));
      const defaultGateAX = Math.max(fMinX + 8.0, Math.min(fMaxX - 8.0, (L ? L.txX : 2.0) - 7.5));
      const aGapMin = envUD.gateGapMinX !== undefined ? envUD.gateGapMinX : (defaultGateAX - 5.0);
      const aGapMax = envUD.gateGapMaxX !== undefined ? envUD.gateGapMaxX : (defaultGateAX + 3.6);
      pushBox3(fMinX - 0.4, fMaxX + 0.4, fMinZ - 0.4, fMinZ + 0.05, 'North Perimeter Fence (Sub A)', padRadius);
      pushBox3(fMinX - 0.4, aGapMin, fMaxZ - 0.4, fMaxZ + 0.4, 'South Perimeter Fence Left (Sub A)', padRadius);
      pushBox3(aGapMax, fMaxX + 0.4, fMaxZ - 0.4, fMaxZ + 0.4, 'South Perimeter Fence Right (Sub A)', padRadius);
      if (!AppState.gateAOpen) {
        pushBox3(aGapMin, aGapMax, fMaxZ - 0.35, fMaxZ + 0.35, 'Substation A Closed Entrance Gate', padRadius);
      }
      pushBox3(fMinX - 0.4, fMinX + 0.05, fMinZ - 0.4, fMaxZ + 0.4, 'West Perimeter Fence (Sub A)', padRadius);
      pushBox3(fMaxX - 0.05, fMaxX + 0.4, fMinZ - 0.4, fMaxZ + 0.4, 'East Perimeter Fence (Sub A)', padRadius);

      // 2b. Full-Scale Tie Substation B Perimeter Fence, Closed Gate B & Key Solid Structures
      const distUD = switchyardObjects.distribution && switchyardObjects.distribution.userData ? switchyardObjects.distribution.userData : null;
      if (distUD && distUD.subBLayout) {
        const LB = distUD.subBLayout;
        const sbX = distUD.subBOriginX;
        const sbZ = distUD.subBOriginZ;
        const bMinX = sbX - LB.yardMaxX;
        const bMaxX = sbX - LB.yardMinX;
        const bMinZ = sbZ - LB.yardMaxZ;
        const bMaxZ = sbZ - LB.yardMinZ; // World South-facing highway perimeter of Sub B
        const subBEnvUD = distUD.subBEnv && distUD.subBEnv.userData ? distUD.subBEnv.userData : {};
        const localGapMin = subBEnvUD.gateGapMinX !== undefined ? subBEnvUD.gateGapMinX : ((LB.txX - 7.5) - 3.6);
        const localGapMax = subBEnvUD.gateGapMaxX !== undefined ? subBEnvUD.gateGapMaxX : ((LB.txX - 7.5) + 5.0);
        const sbGapMin = sbX - localGapMax;
        const sbGapMax = sbX - localGapMin;

        pushBox3(bMinX - 0.4, bMaxX + 0.4, bMinZ - 0.4, bMinZ + 0.05, 'North Perimeter Fence (Sub B)', padRadius);
        pushBox3(bMinX - 0.4, sbGapMin, bMaxZ - 0.4, bMaxZ + 0.4, 'South Perimeter Fence Left (Sub B)', padRadius);
        pushBox3(sbGapMax, bMaxX + 0.4, bMaxZ - 0.4, bMaxZ + 0.4, 'South Perimeter Fence Right (Sub B)', padRadius);
        if (!AppState.gateBOpen) {
          pushBox3(sbGapMin, sbGapMax, bMaxZ - 0.35, bMaxZ + 0.35, 'Substation B Closed Entrance Gate', padRadius);
        }
        pushBox3(bMinX - 0.4, bMinX + 0.05, bMinZ - 0.4, bMaxZ + 0.4, 'West Perimeter Fence (Sub B)', padRadius);
        pushBox3(bMaxX - 0.05, bMaxX + 0.4, bMinZ - 0.4, bMaxZ + 0.4, 'East Perimeter Fence (Sub B)', padRadius);
        pushBox3(sbX - LB.txX - 4.2, sbX - LB.txX + 4.2, sbZ - LB.txZ - 6.5, sbZ - LB.txZ + 6.5, 'Substation B TR-02 Transformer Pad', padRadius);
        pushBox3(sbX - LB.ctrlX - 4.2, sbX - LB.ctrlX + 4.2, sbZ - LB.ctrlZ - 5.4, sbZ - LB.ctrlZ + 5.4, 'Substation B Control House', padRadius);
      }
      if (!AppState.cityGateOpen && distUD && distUD.cityGateX !== undefined) {
        const cgZ = distUD.cityGateZ !== undefined ? distUD.cityGateZ : (L ? L.yardMaxZ + 11.5 : 35);
        pushBox3(distUD.cityGateX - 0.8, distUD.cityGateX + 0.8, cgZ - 6.2, cgZ + 6.2, 'City Utility Gate Barrier (Press [E] or Click to Raise)', 0.35);
      }

      // 3. Traverse 3D switchyard equipment meshes and compute world-space THREE.Box3 colliders expanded by 0.55 m
      if (!scene) return;
      scene.updateMatrixWorld(true);
      const equipKeys = ['gantry', 'arrester', 'ctvt', 'disconnect', 'breaker', 'transformer', 'busbar', 'auxiliary', 'secondary', 'feeders', 'ind_hv_bay', 'urd_vista_swgr', 'dt_urd_pad', 'dt_com_750', 'dt_uni_500', 'dt_mun_1000', 'dt_ind_1500'];
      equipKeys.forEach(k => {
        const root = switchyardObjects[k];
        if (!root || !root.visible) return;
        root.updateMatrixWorld(true);
        root.traverse(obj => {
          if (!obj.isMesh || !obj.visible) return;
          if (obj.userData && obj.userData.noCollider) return;
          let p = obj.parent;
          while (p && p !== scene) {
            if (!p.visible) return;
            p = p.parent;
          }
          if (obj.userData && obj.userData.flowCurve) return;
          obj.updateMatrixWorld(true);
          const rawBox = new THREE.Box3().setFromObject(obj);
          if (rawBox.isEmpty()) return;
          const heightY = rawBox.max.y - rawBox.min.y;
          const spanX = rawBox.max.x - rawBox.min.x;
          const spanZ = rawBox.max.z - rawBox.min.z;
          // Exclude flat ground/concrete pads (max.y <= 0.46) and overhead beams/conductors above walk height (min.y > 2.35)
          if (rawBox.max.y <= 0.46 || rawBox.min.y > 2.35) return;
          if (spanX > 16.0 || spanZ > 16.0 || heightY < 0.25) return;
          rawBox.min.x -= padRadius;
          rawBox.max.x += padRadius;
          rawBox.min.z -= padRadius;
          rawBox.max.z += padRadius;
          rawBox.min.y = -1.0;
          rawBox.max.y = 5.0;
          rawBox.label = k;
          solidColliders.push(rawBox);
        });
      });
    }

    const WORLD_WALK_BOUNDS = { minX: -340, maxX: 1150, minZ: -320, maxZ: 320 };

    function isPointBlockedBySolidColliders(x, z, y = 1.4) {
      if (x <= WORLD_WALK_BOUNDS.minX + 0.55 || x >= WORLD_WALK_BOUNDS.maxX - 0.55 || z <= WORLD_WALK_BOUNDS.minZ + 0.55 || z >= WORLD_WALK_BOUNDS.maxZ - 0.55) {
        return true;
      }
      const testPt = new THREE.Vector3(x, y, z);
      for (let i = 0; i < solidColliders.length; i++) {
        if (solidColliders[i].containsPoint(testPt)) {
          return true;
        }
      }
      return false;
    }

    function resolveWalkCollision(nextX, nextZ, radius = 0.55) {
      let x = nextX, z = nextZ;
      x = Math.max(WORLD_WALK_BOUNDS.minX + radius, Math.min(WORLD_WALK_BOUNDS.maxX - radius, x));
      z = Math.max(WORLD_WALK_BOUNDS.minZ + radius, Math.min(WORLD_WALK_BOUNDS.maxZ - radius, z));

      const boxes = AppState.collisionBoxes || [];
      for (let pass = 0; pass < 2; pass++) {
        for (let i = 0; i < boxes.length; i++) {
          const b = boxes[i];
          const closestX = Math.max(b.minX, Math.min(x, b.maxX));
          const closestZ = Math.max(b.minZ, Math.min(z, b.maxZ));
          const dx = x - closestX;
          const dz = z - closestZ;
          const distSq = dx * dx + dz * dz;
          if (distSq < radius * radius) {
            if (distSq > 1e-8) {
              const dist = Math.sqrt(distSq);
              const push = radius - dist;
              x += (dx / dist) * push;
              z += (dz / dist) * push;
            } else {
              const dL = Math.abs(x - b.minX), dR = Math.abs(b.maxX - x);
              const dT = Math.abs(z - b.minZ), dB = Math.abs(b.maxZ - z);
              const m = Math.min(dL, dR, dT, dB);
              if (m === dL) x = b.minX - radius;
              else if (m === dR) x = b.maxX + radius;
              else if (m === dT) z = b.minZ - radius;
              else z = b.maxZ + radius;
            }
          }
        }
      }
      return { x, z };
    }

    function updateWalkMovement(delta) {
      if (AppState.isHazardModalLocked) {
        WalkState.moveForward = WalkState.moveBackward = WalkState.moveLeft = WalkState.moveRight = false;
        WalkState.isMouseDown = false;
        return;
      }
      if (!(WalkState.moveForward || WalkState.moveBackward || WalkState.moveLeft || WalkState.moveRight)) return;

      if (!AppState.isWalkMode) {
        // Orbit-Mode Horizontal WASD / Arrow Panning (camera + OrbitControls.target move together)
        if (!controls || !controls.target) return;
        activeCameraTweenId++;
        const panSpeed = 16.0 * delta;
        const forward = new THREE.Vector3();
        camera.getWorldDirection(forward);
        forward.y = 0;
        if (forward.lengthSq() > 1e-6) forward.normalize();
        const right = new THREE.Vector3().crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize();
        const moveVec = new THREE.Vector3();
        const fInput = Number(WalkState.moveForward) - Number(WalkState.moveBackward);
        const rInput = Number(WalkState.moveRight) - Number(WalkState.moveLeft);
        moveVec.addScaledVector(forward, fInput * panSpeed);
        moveVec.addScaledVector(right, rInput * panSpeed);
        camera.position.add(moveVec);
        controls.target.add(moveVec);
        controls.update();
        return;
      }

      const speed = 7.0;
      WalkState.direction.z = Number(WalkState.moveForward) - Number(WalkState.moveBackward);
      WalkState.direction.x = Number(WalkState.moveRight) - Number(WalkState.moveLeft);
      WalkState.direction.normalize();

      const forward = new THREE.Vector3(-Math.sin(WalkState.yaw), 0, -Math.cos(WalkState.yaw));
      const side = new THREE.Vector3(Math.cos(WalkState.yaw), 0, -Math.sin(WalkState.yaw));

      const rawStepX = (forward.x * WalkState.direction.z + side.x * WalkState.direction.x) * speed * delta;
      const rawStepZ = (forward.z * WalkState.direction.z + side.z * WalkState.direction.x) * speed * delta;

      // Test candidate nextPos along X and Z independently against solidColliders[] BEFORE moving camera
      const subSteps = Math.max(1, Math.ceil(Math.hypot(rawStepX, rawStepZ) / 0.18));
      const dX = rawStepX / subSteps;
      const dZ = rawStepZ / subSteps;
      const nextPos = camera.position.clone();

      for (let s = 0; s < subSteps; s++) {
        const candX = nextPos.x + dX;
        if (!isPointBlockedBySolidColliders(candX, nextPos.z, 1.4)) {
          nextPos.x = candX;
        }
        const candZ = nextPos.z + dZ;
        if (!isPointBlockedBySolidColliders(nextPos.x, candZ, 1.4)) {
          nextPos.z = candZ;
        }
      }

      camera.position.x = nextPos.x;
      camera.position.z = nextPos.z;

      walkBobPhase += delta * 9.5;
      camera.position.y = 1.75 + Math.sin(walkBobPhase) * 0.032;

      if (Math.random() < 0.1) soundEngine.playGravelFootstep();
    }

    function stepBackToSafeZone() {
      const vs = getVoltageSpec(AppState.voltageClass);
      const minSafeDist = Math.max(3.5, vs.mad + 1.6);
      let dest = AppState.nearestSafePos ? { x: AppState.nearestSafePos.x, z: AppState.nearestSafePos.z } : { x: 0, z: 28 };

      if (AppState.lastHazardPos) {
        const dx = camera.position.x - AppState.lastHazardPos.x;
        const dz = camera.position.z - AppState.lastHazardPos.z;
        const len = Math.hypot(dx, dz);
        const ux = len > 0.05 ? (dx / len) : 0;
        const uz = len > 0.05 ? (dz / len) : 1;
        const radialCand = {
          x: AppState.lastHazardPos.x + ux * (minSafeDist + 0.6),
          z: AppState.lastHazardPos.z + uz * (minSafeDist + 0.6)
        };
        const dSafeAnchor = Math.hypot(dest.x - AppState.lastHazardPos.x, dest.z - AppState.lastHazardPos.z);
        if (dSafeAnchor < minSafeDist || !AppState.nearestSafePos) {
          dest = radialCand;
        }
      }

      const res = resolveWalkCollision(dest.x, dest.z, 0.45);
      camera.position.x = res.x;
      camera.position.z = res.z;
      camera.position.y = 1.75;

      const hm = document.getElementById('hv-danger-modal');
      const flash = document.getElementById('hv-screen-flash');
      if (hm) hm.style.display = 'none';
      if (flash) flash.style.display = 'none';
      WalkState.moveForward = WalkState.moveBackward = WalkState.moveLeft = WalkState.moveRight = false;
      WalkState.isMouseDown = false;
      AppState.isHazardModalLocked = false;
      AppState.hvDangerSuppressedUntilSafe = false;
      showToast(`Retreated safely ≥ ${minSafeDist.toFixed(1)} m outside ${vs.mad.toFixed(1)} m MAD (Movement Restored)`);
    }

    function dismissHvDangerModal() {
      stepBackToSafeZone();
    }

    // LIVE PROXIMITY HAZARD & ELECTROCUTION WARNING SYSTEM (IEEE C2 Table 441-1 / OSHA / IEEE 1584 / IEEE 80)
    const _proxTmpVec = (typeof THREE !== 'undefined') ? new THREE.Vector3() : { x: 0, y: 0, z: 0 };
    function updateProximityHazard(delta) {
      const banner = document.getElementById('proximity-hazard-banner');
      const bannerText = document.getElementById('proximity-hazard-text');
      const bannerDist = document.getElementById('proximity-hazard-dist');
      const bannerIcon = document.getElementById('proximity-hazard-icon');
      const fpsHud = document.getElementById('fps-hud');
      const dangerModal = document.getElementById('hv-danger-modal');
      const flashOverlay = document.getElementById('hv-screen-flash');

      if (!AppState.isWalkMode || !banner || !scene) {
        if (banner) banner.style.display = 'none';
        if (fpsHud) fpsHud.className = '';
        if (dangerModal && dangerModal.style.display === 'flex') dangerModal.style.display = 'none';
        if (flashOverlay) flashOverlay.style.display = 'none';
        return;
      }

      const b = computeEnergizedBranches();
      const vs = getVoltageSpec(AppState.voltageClass);
      const mad = vs.mad;
      const cautionDist = mad + 2.0;
      const camPos = camera.position;

      scene.updateMatrixWorld(true);
      const isObjVisible = (obj) => {
        let p = obj;
        while (p) {
          if (p.visible === false) return false;
          p = p.parent;
        }
        return true;
      };

      let minDistance = 999;
      let nearestLabel = '';
      let nearestKvLN = vs.hvKv / Math.sqrt(3);
      let nearestHazardPos = null;

      scene.traverse(obj => {
        if (!obj.userData || !obj.userData.energizedNode) return;
        const cTag = obj.userData.circuitTag || 'main_path';
        if (cTag === 'none' || !b[cTag]) return;
        if (!isObjVisible(obj)) return;

        obj.getWorldPosition(_proxTmpVec);
        const d3d = camPos.distanceTo(_proxTmpVec);
        if (d3d < minDistance) {
          minDistance = d3d;
          nearestHazardPos = { x: _proxTmpVec.x, y: _proxTmpVec.y, z: _proxTmpVec.z };
          const vTag = obj.userData.voltageTag || 'HV';
          const kvLabel = (vTag === 'LV' || vTag === '13.8kV') ? `${vs.lvKv} kV` : (vTag === '480V' ? '480 V' : `${vs.hvKv} kV`);
          const tagNames = {
            incoming: `${kvLabel} Incoming Line / Arrester / CT Terminal`,
            post_dsA: `${kvLabel} Disconnect Switch (89-A) Contact`,
            post_cbMain: `${kvLabel} Circuit Breaker (52-69) Terminal`,
            main_path: `${kvLabel} Main Bus / Isolator Live Part`,
            bypass_path: `${kvLabel} Transfer Bus / 52-BT Live Terminal`,
            tx_hv: `${vs.hvKv} kV TR-01 Primary Bushing Stud`,
            sec_lv: `${vs.lvKv} kV TR-01 Secondary Bushing / Bus`,
            sec_bus: `${vs.lvKv} kV Secondary Main Bus / VCB`,
            fdr1: `${vs.lvKv} kV Feeder 01 Bay (52-F1)`,
            fdr2: `${vs.lvKv} kV Feeder 02 Bay (52-F2)`,
            cap_bank: `${vs.lvKv} kV Shunt Capacitor Bank (${vs.capMvar} MVAR)`
          };
          nearestLabel = obj.userData.hazardLabel || tagNames[cTag] || obj.name || `${kvLabel} ${cTag.toUpperCase()} Live Terminal`;
          nearestKvLN = (vTag === 'LV' || vTag === '13.8kV')
            ? (vs.lvKv / Math.sqrt(3))
            : (vTag === '480V' ? 0.277 : (vs.hvKv / Math.sqrt(3)));
        }
      });

      AppState.lastHazardPos = nearestHazardPos;
      const effGapCm = Math.max(1.0, minDistance * 100);
      const eFieldKvCm = ((nearestKvLN * Math.SQRT2) / effGapCm).toFixed(2);
      const vTouchVolts = Math.round(nearestKvLN * 1000);
      const iBodyMa = Math.round((vTouchVolts / 1000) * 1000); // IEEE 80 R_body = 1000 Ohm -> I(A) = V/1000 -> mA = V
      // IEEE 1584 simplified incident energy estimate scaled by clearing time & air gap
      const scMvaApprox = (AppState.voltageClass === '230_138') ? 6800 : ((AppState.voltageClass === '138_69') ? 2400 : 1100);
      const gapMeters = Math.max(0.25, minDistance);
      const incidentCal = (4.184 * (scMvaApprox * 0.085) * vs.arcClearingSec / Math.pow(gapMeters, 1.64)).toFixed(1);

      // Update safe-retreat anchor when well outside MAD (>= mad + 1.4 m)
      if (minDistance >= mad + 1.4) {
        AppState.nearestSafePos = { x: camPos.x, z: camPos.z };
        AppState.hvDangerSuppressedUntilSafe = false;
      }

      // STAGE 2: Critical MAD Breach (d <= vSpec.mad)
      if (minDistance <= mad && nearestLabel) {
        banner.style.display = 'flex';
        banner.className = 'stage-danger';
        if (bannerIcon) bannerIcon.innerText = '⛔';
        if (bannerText) bannerText.innerText = `DANGER: MAD BREACH AT ${nearestLabel}!`;
        if (bannerDist) bannerDist.innerText = `${minDistance.toFixed(2)} m <= ${mad.toFixed(1)} m MAD | ${incidentCal} cal/cm²`;
        if (fpsHud) fpsHud.className = 'hazard-critical';
        if (flashOverlay && !AppState.hvDangerSuppressedUntilSafe) flashOverlay.style.display = 'block';

        if (dangerModal && !AppState.hvDangerSuppressedUntilSafe) {
          dangerModal.style.display = 'flex';
          // Hard-freeze first-person locomotion & release pointer lock while HV Violation modal is displayed
          AppState.isHazardModalLocked = true;
          WalkState.moveForward = WalkState.moveBackward = WalkState.moveLeft = WalkState.moveRight = false;
          WalkState.isMouseDown = false;
          if (document.exitPointerLock) {
            try { document.exitPointerLock(); } catch (e) {}
          }
          const nEl = document.getElementById('hv-danger-node');
          const dEl = document.getElementById('hv-danger-dist');
          const eEl = document.getElementById('hv-danger-efield');
          const iEl = document.getElementById('hv-danger-ibody');
          const cAir = document.getElementById('hv-conseq-air');
          const cArc = document.getElementById('hv-conseq-arc');
          const cPhys = document.getElementById('hv-conseq-phys');
          if (nEl) nEl.innerText = nearestLabel;
          if (dEl) dEl.innerText = `${minDistance.toFixed(2)} m (<= ${mad.toFixed(1)} m MAD)`;
          if (eEl) eEl.innerText = `${eFieldKvCm} kV/cm`;
          if (iEl) iEl.innerText = `${(iBodyMa / 1000).toFixed(1)} A (${iBodyMa.toLocaleString()} mA — FATAL)`;
          if (cAir) {
            cAir.innerHTML = `Dry air breaks down at <strong>~30 kV/cm peak (~3 kV/mm)</strong>. At <strong>${minDistance.toFixed(2)} m</strong> from ${nearestKvLN.toFixed(1)} kV L-N (${eFieldKvCm} kV/cm avg), leader flashover bridges the air gap.`;
          }
          if (cArc) {
            cArc.innerHTML = `Incident Energy: <strong style="color:#f87171;">${incidentCal} cal/cm²</strong> (${vs.arcClearingSec}s clearing). Arc plasma reaches <strong>&gt; 19,000 °C</strong> with copper vapor blast and 3rd-degree burns.`;
          }
          if (cPhys) {
            cPhys.innerHTML = `Assuming human body resistance <strong>R_body = 1,000 Ω</strong> (IEEE 80), <strong>I_body = ${vTouchVolts.toLocaleString()} V / 1000 Ω = ${(iBodyMa / 1000).toFixed(1)} A</strong>, far above the 100 mA Dalziel ventricular fibrillation threshold.`;
          }
        }

        if (Math.random() < 0.25) soundEngine.playCoronaHum();
        if (dynamicArcLight) {
          dynamicArcLight.color.setHex(0x00f0ff);
          dynamicArcLight.position.set(camPos.x, camPos.y + 1.5, camPos.z);
          dynamicArcLight.intensity = Math.random() * 8 + 2;
        }

      // STAGE 1: Amber Caution Perimeter (d < mad + 2.0 m)
      } else if (minDistance < cautionDist && nearestLabel) {
        banner.style.display = 'flex';
        banner.className = 'stage-warning';
        if (bannerIcon) bannerIcon.innerText = '⚠️';
        if (bannerText) bannerText.innerText = `CAUTION: APPROACHING ${nearestLabel}`;
        if (bannerDist) bannerDist.innerText = `${minDistance.toFixed(2)} m (MAD: ${mad.toFixed(1)} m)`;
        if (fpsHud) fpsHud.className = 'hazard-warning';
        if (dangerModal && dangerModal.style.display === 'flex') dangerModal.style.display = 'none';
        if (flashOverlay) flashOverlay.style.display = 'none';
        AppState.isHazardModalLocked = false;
        if (dynamicArcLight) dynamicArcLight.intensity = 0;
        if (Math.random() < 0.15) soundEngine.playGeigerClick();

      // SAFE DISTANCE (>= mad + 2.0 m)
      } else {
        banner.style.display = 'none';
        if (fpsHud) fpsHud.className = '';
        if (dangerModal && dangerModal.style.display === 'flex') dangerModal.style.display = 'none';
        if (flashOverlay) flashOverlay.style.display = 'none';
        AppState.isHazardModalLocked = false;
        if (dynamicArcLight) dynamicArcLight.intensity = 0;
      }
    }

    // FIRST-PERSON SAFE-DISTANCE EQUIPMENT & SCADA RETICLE INSPECTION
    const _walkRayCenter = { x: 0, y: 0 };
    function updateWalkInspectionReticle() {
      const promptEl = document.getElementById('walk-inspect-prompt');
      if (!promptEl) return;

      if (!AppState.isWalkMode || !scene || !camera || AppState.isHazardModalLocked || isAnyModalOpen()) {
        promptEl.style.display = 'none';
        AppState.walkFocusedTarget = null;
        return;
      }

      raycaster.setFromCamera(_walkRayCenter, camera);
      const hits = raycaster.intersectObjects(scene.children, true).filter(h => !isIgnoredRaycastMesh(h.object));
      const vs = getVoltageSpec(AppState.voltageClass);
      const mad = vs.mad;

      let focused = null;
      for (const hit of hits) {
        if (hit.distance > 11.5) break;
        let curr = hit.object;
        let actionTag = null;
        let relayFocus = null;
        let compId = null;
        let hasFlowCurve = false;
        let inSpanningBusbar = false;

        while (curr && curr !== scene) {
          if (!actionTag && curr.userData && curr.userData.action) actionTag = curr.userData.action;
          if (!relayFocus && curr.userData && curr.userData.relayFocus) relayFocus = curr.userData.relayFocus;
          if (curr.userData && curr.userData.flowCurve) hasFlowCurve = true;
          if (curr.userData && curr.userData.isSpanningBusbar) inSpanningBusbar = true;
          if (!compId && curr.userData && curr.userData.componentId) {
            compId = curr.userData.componentId;
            break;
          }
          curr = curr.parent;
        }

        if (actionTag === 'openMasterSLD' && hit.distance <= 6.5) {
          focused = { type: 'scada', dist: hit.distance };
          break;
        }

        if (actionTag === 'openRelayTccLab' && hit.distance <= 6.5) {
          focused = { type: 'relay_tcc', relayFocus: relayFocus || 'all', dist: hit.distance };
          break;
        }

        if ((actionTag === 'toggleGateA' || actionTag === 'toggleGateB') && hit.distance <= 8.5) {
          focused = { type: 'gate', gateId: actionTag === 'toggleGateB' ? 'B' : 'A', dist: hit.distance };
          break;
        }
        if (actionTag === 'toggleCityGate' && hit.distance <= 10.5) {
          focused = { type: 'city_gate', dist: hit.distance };
          break;
        }

        if (inSpanningBusbar && hasFlowCurve) continue;

        if (compId && SUBSTATION_DATA[compId] && compId !== 'ground') {
          const isIndoorLowV = (compId === 'auxiliary' || compId === 'control' || compId === 'substation_gate' || compId === 'city_gate');
          const safeMin = isIndoorLowV ? 0.5 : (mad * 0.72);
          if (hit.distance >= safeMin && hit.distance <= 10.5) {
            focused = { type: 'equipment', compId, dist: hit.distance };
            break;
          }
        }
      }

      AppState.walkFocusedTarget = focused;
      if (!focused) {
        promptEl.style.display = 'none';
        promptEl.classList.remove('scada-focus');
        return;
      }

      promptEl.style.display = 'flex';
      if (focused.type === 'scada') {
        promptEl.classList.add('scada-focus');
        promptEl.innerHTML = `<span class="walk-key-badge">[E] / Click</span> <span>🖥️ <strong>SCADA HMI Operator Terminal</strong> (${focused.dist.toFixed(1)} m — SAFE) — Open Interactive Master SLD</span>`;
      } else if (focused.type === 'relay_tcc') {
        promptEl.classList.add('scada-focus');
        promptEl.innerHTML = `<span class="walk-key-badge">[E] / Click</span> <span>🛡️ <strong>Protection Relay Rack</strong> (${focused.dist.toFixed(1)} m — SAFE) — Open Relay Settings &amp; TCC Lab</span>`;
      } else if (focused.type === 'gate') {
        promptEl.classList.add('scada-focus');
        const isOpenNow = (focused.gateId === 'B') ? AppState.gateBOpen : AppState.gateAOpen;
        promptEl.innerHTML = `<span class="walk-key-badge">[E] / Click</span> <span>🚧 <strong>Security Entrance Gate ${focused.gateId}</strong> (${focused.dist.toFixed(1)} m) — Swing ${isOpenNow ? 'CLOSED' : 'OPEN (Walk Access)'}</span>`;
      } else if (focused.type === 'city_gate') {
        promptEl.classList.add('scada-focus');
        promptEl.innerHTML = `<span class="walk-key-badge">[E] / Click</span> <span>🚧 <strong>Utility District &amp; URD City Gate</strong> (${focused.dist.toFixed(1)} m) — ${AppState.cityGateOpen ? 'Lower Barrier CLOSED' : 'Raise Barrier OPEN'}</span>`;
      } else {
        promptEl.classList.remove('scada-focus');
        const eqName = SUBSTATION_DATA[focused.compId].name;
        promptEl.innerHTML = `<span class="walk-key-badge">[E] / Click</span> <span>🔍 <strong>${eqName}</strong> (${focused.dist.toFixed(1)} m — SAFE ZONE) — Inspect Specs, Functionality &amp; Exploded View</span>`;
      }
    }

    function triggerWalkFocusedAction() {
      if (!AppState.isWalkMode || AppState.isHazardModalLocked) return;
      const target = AppState.walkFocusedTarget;
      if (!target) return;

      if (target.type === 'gate') {
        toggleSubstationGate(target.gateId);
        selectComponent('substation_gate', false);
        updateWalkInspectionReticle();
        return;
      }
      if (target.type === 'city_gate') {
        toggleSubstationGate('city');
        selectComponent('city_gate', false);
        updateWalkInspectionReticle();
        return;
      }

      WalkState.moveForward = WalkState.moveBackward = WalkState.moveLeft = WalkState.moveRight = false;
      WalkState.isMouseDown = false;
      if (document.exitPointerLock) {
        try { document.exitPointerLock(); } catch (e) {}
      }

      if (target.type === 'scada') {
        openExpandedSLD();
        showToast('SCADA HMI Workstation: Opened Interactive Master Single-Line Diagram (ANSI C37.2)');
      } else if (target.type === 'relay_tcc') {
        openAnalysisModal('tcc', target.relayFocus || 'all');
        showToast('Control House Protection Rack: Opened Relay Settings Schedule & TCC Lab');
      } else if (target.type === 'equipment' && SUBSTATION_DATA[target.compId]) {
        selectComponent(target.compId, false);
        enterExplodedMode(target.compId, true);
        showToast(`Field Inspection: ${SUBSTATION_DATA[target.compId].name} — Drawer & Exploded View Ready`);
      }
    }

    // LIVE SINGLE-LINE DIAGRAM (SLD) RENDERING & SYNC ACROSS ALL 4 BUSBAR SCHEMES + FLANKING 89 DISCONNECTS
    // EXPANDABLE MASTER SLD MODAL CONTROLS (PAN, ZOOM, PINPOINT SYNC)
    function applySldExpTransform() {
      const grp = document.getElementById('sld-exp-panzoom-group');
      if (grp) {
        const z = AppState.sldZoom || 1.0;
        const tx = (AppState.sldPanX || 0) + 440 * (1 - z);
        const ty = (AppState.sldPanY || 0) + 124 * (1 - z);
        grp.setAttribute('transform', `translate(${tx.toFixed(1)}, ${ty.toFixed(1)}) scale(${z.toFixed(2)})`);
      }
    }

    function openExpandedSLD() {
      const modal = document.getElementById('sld-expanded-modal');
      if (!modal) return;
      AppState.sldExpOpen = true;
      modal.style.display = 'flex';
      initSldExpandedPanZoom();
      renderLiveSLD();
    }

    function closeExpandedSLD() {
      const modal = document.getElementById('sld-expanded-modal');
      AppState.sldExpOpen = false;
      if (modal) modal.style.display = 'none';
    }

    function zoomExpandedSLD(factor) {
      const next = Math.max(0.7, Math.min(3.0, (AppState.sldZoom || 1.0) * factor));
      AppState.sldZoom = +next.toFixed(2);
      applySldExpTransform();
    }

    function resetExpandedSLDView() {
      AppState.sldZoom = 1.0;
      AppState.sldPanX = 0;
      AppState.sldPanY = 0;
      applySldExpTransform();
    }

    let sldExpPanInitialized = false;
    function initSldExpandedPanZoom() {
      if (sldExpPanInitialized) return;
      const vp = document.getElementById('sld-expanded-viewport');
      if (!vp) return;
      sldExpPanInitialized = true;
      let dragging = false, startX = 0, startY = 0, origPanX = 0, origPanY = 0;
      vp.addEventListener('mousedown', (e) => {
        if (e.target && e.target.closest && e.target.closest('[onclick]')) return;
        dragging = true;
        startX = e.clientX;
        startY = e.clientY;
        origPanX = AppState.sldPanX;
        origPanY = AppState.sldPanY;
      });
      window.addEventListener('mousemove', (e) => {
        if (!dragging || !AppState.sldExpOpen) return;
        const z = AppState.sldZoom || 1.0;
        const dx = ((e.clientX - startX) * (984 / Math.max(320, vp.clientWidth || 720))) / z;
        const dy = ((e.clientY - startY) * (272 / Math.max(200, vp.clientHeight || 400))) / z;
        AppState.sldPanX = origPanX + dx;
        AppState.sldPanY = origPanY + dy;
        applySldExpTransform();
      });
      window.addEventListener('mouseup', () => { dragging = false; });
      vp.addEventListener('wheel', (e) => {
        e.preventDefault();
        zoomExpandedSLD(e.deltaY < 0 ? 1.12 : 0.89);
      }, { passive: false });
    }

    function onSldHotspotClick(nodeId) {
      if (AppState.pinpointFaultMode) {
        triggerPinpointedFault(nodeId, AppState.pinpointFeederDistPct || 50, null);
      } else {
        togglePinpointFaultMode(true);
        triggerPinpointedFault(nodeId, AppState.pinpointFeederDistPct || 50, null);
      }
    }

    function setSldFaultType(ftype) {
      if (!['3ph', 'slg', 'll', 'dlg'].includes(ftype)) return;
      AppState.scFaultType = ftype;
      ['3ph', 'slg', 'll', 'dlg'].forEach(t => {
        const pill = document.getElementById(`sld-ft-${t}`);
        if (pill) pill.classList.toggle('active', t === ftype);
      });
      const scSel = document.getElementById('sc-fault-type');
      if (scSel) scSel.value = ftype;
      const ppSel = document.getElementById('pinpoint-fault-type');
      if (ppSel) ppSel.value = ftype;

      const faultNode = (AppState.faultType && AppState.faultType !== 'none' && AppState.faultType !== 'lightning') ? AppState.pinpointFaultNode : null;
      if (faultNode && PINPOINT_FAULT_NODES[faultNode]) {
        const meta = PINPOINT_FAULT_NODES[faultNode];
        const vs = getVoltageSpec(AppState.voltageClass);
        const top = AppState.busTopology || 'single';
        const sc = computeShortCircuitMetrics();
        updatePinpointFaultReadout(meta.id, sc, meta.breakerNames(top), vs, meta);
      }
      if (typeof renderAnalysisModalBody === 'function' && AppState.activeAnalysisTab === 'sc') {
        const modal = document.getElementById('analysis-modal');
        if (modal && modal.style.display === 'flex') renderAnalysisModalBody();
      }
      renderLiveSLD();
      const labelMap = { '3ph': '3Φ Symmetrical (LLL)', 'slg': 'Single Line-to-Ground (A-G)', 'll': 'Line-to-Line (B-C)', 'dlg': 'Double Line-to-Ground (B-C-G)' };
      showToast(`SLD Short-Circuit Fault Type: ${labelMap[ftype]}`);
    }

    function clearFaultAndResetSystem() {
      triggerNormalState();
      togglePinpointFaultMode(false);
      showToast('Fault Cleared & System Reset: Relays (87B/87T/50/51/51N/21) Reset & Breakers Reclosed');
    }

    function computeOrthogonalSldFaultPath(top, faultNode, s, bOpt) {
      const b = bOpt || computeEnergizedBranches();
      let hvStem = 'M 12,24 L 95,24 L 95,122';
      let txInY = 122;

      if (top === 'single') {
        if (faultNode === 'node1_incoming') return 'M 12,24 L 58,24';
        if (faultNode === 'node_cascade_mid') return 'M 12,24 L 34,24';
        if (faultNode === 'node2_hv_bus') return 'M 12,24 L 95,24';
        hvStem = 'M 12,24 L 95,24 L 95,122';
      } else if (top === 'maintransfer') {
        if (faultNode === 'node1_incoming') return 'M 12,24 L 58,24';
        if (faultNode === 'node_cascade_mid') return 'M 12,24 L 34,24';
        if (faultNode === 'node2_hv_bus') return 'M 12,24 L 95,24';
        const bypActive = !!(s.dsBT && s.cbBT && s.dsBYP) && !s.cbMain;
        hvStem = bypActive
          ? 'M 12,24 L 42,24 L 42,54 L 145,54 L 145,112 L 96,112 L 96,122'
          : 'M 12,24 L 96,24 L 96,122';
      } else if (top === 'ring') {
        if (faultNode === 'node1_incoming') return 'M 8,80 L 18,80';
        if (faultNode === 'node_cascade_mid') return 'M 8,80 L 24,80';
        if (faultNode === 'node2_hv_bus') return 'M 8,80 L 28,80 L 28,34 L 87,34';
        const northClosed = !!(s.cb1 && s.ds1A && s.ds1B && s.cb2 && s.ds2A && s.ds2B);
        hvStem = northClosed
          ? 'M 8,80 L 28,80 L 28,34 L 146,34 L 146,122'
          : 'M 8,80 L 28,80 L 28,126 L 146,126 L 146,122';
      } else if (top === 'doublebreaker') {
        const busAPathOn = !!(s.cb1A && s.ds1A1 && s.ds1A2 && s.cb2A && s.ds2A1 && s.ds2A2);
        if (faultNode === 'node1_incoming') return 'M 6,92 L 36,92';
        if (faultNode === 'node_cascade_mid') return 'M 6,92 L 24,92';
        if (faultNode === 'node2_hv_bus') {
          return busAPathOn ? 'M 6,92 L 52,92 L 52,24 L 88,24' : 'M 6,92 L 52,92 L 52,160 L 88,160';
        }
        hvStem = busAPathOn
          ? 'M 6,92 L 52,92 L 52,24 L 122,24 L 122,122'
          : 'M 6,92 L 52,92 L 52,160 L 122,160 L 122,122';
      } else {
        txInY = 115;
        if (faultNode === 'node1_incoming') return 'M 8,71 L 48,71';
        if (faultNode === 'node_cascade_mid') return 'M 8,71 L 28,71';
        if (faultNode === 'node2_hv_bus') return 'M 8,71 L 88,71 L 88,26';
        hvStem = 'M 8,71 L 88,71 L 88,115';
      }

      if (faultNode === 'node3_tx_hv') return `${hvStem} L 174,${txInY}`;
      if (faultNode === 'node7_ind_hv') return `${hvStem} L 166,122 L 166,198 L 264,198`;
      if (faultNode === 'node8_ind_sub') return `${hvStem} L 166,122 L 166,198 L 317,198`;

      const txOutBridge = (txInY === 115) ? `L 210,115 L 210,122` : `L 210,122`;
      const subAFdr1Base = `${hvStem} ${txOutBridge} L 278,122 L 278,82`;
      const subAFdr2Base = `${hvStem} ${txOutBridge} L 278,122 L 278,152`;
      const subBFdr1Base = `M 870,112 L 802,112 L 736,117 L 640,117 L 640,82`;
      const subBFdr2Base = `M 870,112 L 802,112 L 736,117 L 640,117 L 640,152`;

      if (faultNode === 'node4_tx_lv') return `${hvStem} ${txOutBridge} L 214,122`;
      if (faultNode === 'node5_lv_bus') return `${hvStem} ${txOutBridge} L 278,122`;
      if (faultNode === 'node6_fdr1') return `${subAFdr1Base} L 348,82`;
      if (faultNode === 'node9_acr1') return `${subAFdr1Base} L 380,82`;
      if (faultNode === 'node10_res_lat') {
        return b.fdr1_from_subB ? `${subBFdr1Base} L 444,82 L 444,36` : `${subAFdr1Base} L 444,82 L 444,36`;
      }
      if (faultNode === 'node11_urd_pad') {
        return b.fdr1_from_subB ? `${subBFdr1Base} L 402,82 L 402,114` : `${subAFdr1Base} L 402,82 L 402,114`;
      }
      if (faultNode === 'node6_fdr2') return `${subAFdr2Base} L 348,152`;
      if (faultNode === 'node12_cbd_bus') {
        return b.fdr2_from_subB ? `${subBFdr2Base} L 444,152 L 444,132` : `${subAFdr2Base} L 444,152 L 444,132`;
      }
      if (faultNode === 'node13_tie1') {
        return b.fdr1_from_subB ? `${subBFdr1Base} L 482,82` : `${subAFdr1Base} L 482,82`;
      }
      if (faultNode === 'node14_tie2') {
        return b.fdr2_from_subB ? `${subBFdr2Base} L 482,152` : `${subAFdr2Base} L 482,152`;
      }
      if (faultNode === 'node15_uni_bus') {
        return b.fdr3_from_subA ? `${subAFdr1Base} L 532,82 L 532,36` : `${subBFdr1Base} L 532,82 L 532,36`;
      }
      if (faultNode === 'node16_mun_bus') {
        return b.fdr4_from_subA ? `${subAFdr2Base} L 532,152 L 532,132` : `${subBFdr2Base} L 532,152 L 532,132`;
      }
      if (faultNode === 'node17_subb_hv') return 'M 870,112 L 802,112';
      if (faultNode === 'node18_tr02') return 'M 870,112 L 802,112 L 725,117';
      if (faultNode === 'node19_subb_lv') {
        return (b.subB_lv_backfed_from_A && !b.dist_sub_b) ? `${subAFdr1Base} L 640,82 L 640,117` : 'M 870,112 L 736,117 L 640,117';
      }
      if (faultNode === 'node20_fdr3') {
        return b.fdr3_from_subA ? `${subAFdr1Base} L 580,82` : `${subBFdr1Base} L 580,82`;
      }
      if (faultNode === 'node21_fdr4') {
        return b.fdr4_from_subA ? `${subAFdr2Base} L 580,152` : `${subBFdr2Base} L 580,152`;
      }
      return `${hvStem} ${txOutBridge} L 278,122`;
    }

    function renderLiveSLD() {
      const container = document.getElementById('sld-svg-container');
      const expContainer = document.getElementById('sld-expanded-svg-container');
      if (!container && !expContainer) return;
      ['3ph', 'slg', 'll', 'dlg'].forEach(t => {
        const pill = document.getElementById(`sld-ft-${t}`);
        if (pill) pill.classList.toggle('active', t === (AppState.scFaultType || '3ph'));
      });
      const s = AppState.switchStates;
      const b = computeEnergizedBranches();
      const vs = getVoltageSpec(AppState.voltageClass);
      const distKv = vs.distKv || 13.8;
      const indKv = vs.indSubKv || 69.0;
      const pf = (typeof computePowerFlowMetrics === 'function') ? computePowerFlowMetrics() : null;
      const swCol = (closed) => closed ? '#ef4444' : '#10b981';
      const hvCol = b.txFeed ? '#06b6d4' : '#64748b';
      const secCol = b.secMain ? '#f59e0b' : '#64748b';
      const f1Col = b.fdr1 ? '#10b981' : '#64748b';
      const f2Col = b.fdr2 ? '#10b981' : '#64748b';
      const capCol = b.capBank ? '#2dd4bf' : '#64748b';
      const indCol = b.ind_hv ? '#fbbf24' : '#64748b';
      const sel = AppState.selectedComponent;
      const top = AppState.busTopology || 'single';

      const flowOverlay = (dPath, color, active, speedSec = 1.1, isFaultPath = false) => {
        if (!active && !isFaultPath) return '';
        const cls = isFaultPath ? 'sld-flow-line-fast' : 'sld-flow-line';
        const strokeCol = isFaultPath ? '#f43f5e' : color;
        return `
          <path d="${dPath}" fill="none" stroke="${strokeCol}" stroke-width="${isFaultPath ? 2.6 : 1.7}" class="${cls}" opacity="0.92"/>
          <circle r="${isFaultPath ? 2.6 : 2.0}" fill="${isFaultPath ? '#fef08a' : '#e0f2fe'}" opacity="0.95">
            <animateMotion dur="${isFaultPath ? 0.45 : speedSec}s" repeatCount="indefinite" path="${dPath}"/>
          </circle>
        `;
      };

      const sldBadge = (x, y, text, color, anchor = 'middle', fontSize = 4.9, bg = 'rgba(15,23,42,0.92)') => {
        const w = Math.max(15, text.length * (fontSize * 0.62) + 4.5);
        const h = fontSize + 3.4;
        const rx = anchor === 'middle' ? (x - w / 2) : (anchor === 'end' ? (x - w) : x);
        const ry = y - fontSize - 0.6;
        return `<rect x="${rx.toFixed(1)}" y="${ry.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="1.5" fill="${bg}" stroke="${color}" stroke-width="0.35" stroke-opacity="0.45"/><text x="${x}" y="${y}" fill="${color}" font-size="${fontSize}" text-anchor="${anchor}" font-weight="bold" font-family="monospace">${text}</text>`;
      };

      const faultNode = (AppState.faultType && AppState.faultType !== 'none' && AppState.faultType !== 'lightning') ? AppState.pinpointFaultNode : null;
      const faultPosMap = {
        node1_incoming: top === 'ring' ? { x: 18, y: 80 } : (top === 'breakerhalf' ? { x: 48, y: 71 } : (top === 'doublebreaker' ? { x: 36, y: 92 } : { x: 58, y: 24 })),
        node_cascade_mid: top === 'ring' ? { x: 24, y: 80 } : (top === 'breakerhalf' ? { x: 28, y: 71 } : (top === 'doublebreaker' ? { x: 24, y: 92 } : { x: 34, y: 24 })),
        node2_hv_bus: top === 'ring' ? { x: 87, y: 34 } : (top === 'breakerhalf' ? { x: 88, y: 26 } : (top === 'doublebreaker' ? { x: 88, y: 24 } : { x: 95, y: 24 })),
        node3_tx_hv: { x: 174, y: top === 'breakerhalf' ? 115 : 122 },
        node4_tx_lv: { x: 214, y: 122 },
        node5_lv_bus: { x: 278, y: 122 },
        node7_ind_hv: { x: 264, y: 198 },
        node8_ind_sub: { x: 317, y: 198 },
        node6_fdr1: { x: 348, y: 82 },
        node9_acr1: { x: 380, y: 82 },
        node10_res_lat: { x: 444, y: 36 },
        node11_urd_pad: { x: 402, y: 114 },
        node6_fdr2: { x: 348, y: 152 },
        node12_cbd_bus: { x: 444, y: 132 },
        node13_tie1: { x: 482, y: 82 },
        node14_tie2: { x: 482, y: 152 },
        node15_uni_bus: { x: 532, y: 36 },
        node16_mun_bus: { x: 532, y: 132 },
        node17_subb_hv: { x: 802, y: 112 },
        node18_tr02: { x: 725, y: 117 },
        node19_subb_lv: { x: 640, y: 117 },
        node20_fdr3: { x: 580, y: 82 },
        node21_fdr4: { x: 580, y: 152 }
      };

      let primarySvg = '';

      if (top === 'single') {
        const seg1On = true;
        const seg2On = !!s.dsMain && !s.earthMain;
        const seg3On = seg2On && !!s.cbMain;
        const seg4On = b.txFeed;
        primarySvg = `
          <text x="8" y="13" fill="#38bdf8" font-size="6.8" font-weight="bold" font-family="monospace">${vs.hvKv} kV SINGLE BUS (${AppState.enclosureType.toUpperCase()})</text>
          <line x1="12" y1="24" x2="174" y2="24" stroke="#06b6d4" stroke-width="3.2" stroke-linecap="round"/>
          ${flowOverlay('M 12,24 L 95,24', '#38bdf8', seg1On, 1.3)}
          <line x1="95" y1="24" x2="95" y2="39" stroke="#06b6d4" stroke-width="2"/>
          ${flowOverlay('M 95,24 L 95,39', '#38bdf8', seg1On, 0.9)}
          <g onclick="operateSwitch('dsMain')" style="cursor:pointer;">
            <circle cx="95" cy="39" r="2.2" fill="#fff"/><circle cx="95" cy="54" r="2.2" fill="#fff"/>
            <line x1="95" y1="39" x2="${s.dsMain ? 95 : 107}" y2="${s.dsMain ? 54 : 43}" stroke="${swCol(s.dsMain)}" stroke-width="2.3"/>
            <text x="110" y="49" fill="${swCol(s.dsMain)}" font-size="6.4" font-weight="bold" font-family="monospace">89-69A</text>
          </g>
          <line x1="95" y1="54" x2="95" y2="66" stroke="${seg2On ? '#06b6d4' : '#64748b'}" stroke-width="2" ${seg2On ? '' : 'stroke-dasharray="3,2"'}/>
          ${flowOverlay('M 95,54 L 95,66', '#38bdf8', seg2On, 0.8)}
          <g onclick="operateSwitch('cbMain')" style="cursor:pointer;">
            <rect x="83" y="66" width="24" height="16" fill="${swCol(s.cbMain)}" rx="2" stroke="#fff" stroke-width="1.2"/>
            <text x="95" y="77" fill="#fff" font-size="7" text-anchor="middle" font-weight="bold" font-family="monospace">52-69</text>
          </g>
          <line x1="95" y1="82" x2="95" y2="92" stroke="${seg3On ? '#06b6d4' : '#64748b'}" stroke-width="2" ${seg3On ? '' : 'stroke-dasharray="3,2"'}/>
          ${flowOverlay('M 95,82 L 95,92', '#38bdf8', seg3On, 0.8)}
          <g onclick="operateSwitch('dsMainB')" style="cursor:pointer;">
            <circle cx="95" cy="92" r="2.2" fill="#fff"/><circle cx="95" cy="107" r="2.2" fill="#fff"/>
            <line x1="95" y1="92" x2="${s.dsMainB ? 95 : 107}" y2="${s.dsMainB ? 107 : 96}" stroke="${swCol(s.dsMainB)}" stroke-width="2.3"/>
            <text x="110" y="102" fill="${swCol(s.dsMainB)}" font-size="6.4" font-weight="bold" font-family="monospace">89-69B</text>
          </g>
          <line x1="95" y1="107" x2="95" y2="122" stroke="${hvCol}" stroke-width="2.2" ${seg4On ? '' : 'stroke-dasharray="3,2"'}/>
          <line x1="95" y1="122" x2="176" y2="122" stroke="${hvCol}" stroke-width="2.2" ${seg4On ? '' : 'stroke-dasharray="3,2"'}/>
          ${flowOverlay('M 95,107 L 95,122 L 176,122', '#38bdf8', seg4On, 1.15)}
          <g onclick="selectComponent('arrester', true)" style="cursor:pointer;">
            <line x1="34" y1="24" x2="34" y2="54" stroke="#06b6d4" stroke-width="1.8"/>
            <polygon points="34,54 29,65 39,65" fill="#94a3b8"/>
            <text x="34" y="75" fill="#94a3b8" font-size="6.3" text-anchor="middle" font-family="monospace">SA-${vs.hvKv}</text>
          </g>
          <g onclick="operateSwitch('earthMain')" style="cursor:pointer;">
            <rect x="18" y="88" width="42" height="14" rx="2" fill="rgba(15,23,42,0.85)" stroke="${swCol(s.earthMain)}"/>
            <text x="39" y="98" fill="${swCol(s.earthMain)}" font-size="6.2" text-anchor="middle" font-family="monospace">89E:${s.earthMain?'GND':'OPN'}</text>
          </g>
        `;
      } else if (top === 'maintransfer') {
        const bypOn = !!(s.dsBT && s.cbBT && s.dsBYP);
        const bypCol = bypOn ? '#2dd4bf' : '#64748b';
        primarySvg = `
          <text x="8" y="13" fill="#38bdf8" font-size="6.8" font-weight="bold" font-family="monospace">${vs.hvKv} kV MAIN &amp; TRANSFER BUS</text>
          <line x1="12" y1="24" x2="174" y2="24" stroke="#06b6d4" stroke-width="3"/>
          ${flowOverlay('M 12,24 L 96,24', '#38bdf8', true, 1.25)}
          <text x="14" y="20" fill="#38bdf8" font-size="5.6" font-family="monospace">MAIN BUS</text>
          <line x1="12" y1="54" x2="174" y2="54" stroke="${(s.dsBT && s.cbBT) ? '#2dd4bf' : '#64748b'}" stroke-width="2.3" stroke-dasharray="5,2"/>
          <text x="14" y="50" fill="#2dd4bf" font-size="5.6" font-family="monospace">TRANSFER BUS</text>

          <line x1="42" y1="24" x2="42" y2="54" stroke="${bypCol}" stroke-width="1.8" ${bypOn ? '' : 'stroke-dasharray="3,2"'}/>
          ${flowOverlay('M 42,24 L 42,54 L 145,54 L 145,112 L 96,112 L 96,122 L 176,122', '#2dd4bf', b.bypass_path, 1.45)}
          <g onclick="operateSwitch('dsBT')" style="cursor:pointer;">
            <text x="20" y="34" fill="${swCol(s.dsBT)}" font-size="5.2" font-family="monospace">89-BT1</text>
            <text x="20" y="63" fill="${swCol(s.dsBT)}" font-size="5.2" font-family="monospace">89-BT2</text>
          </g>
          <g onclick="operateSwitch('cbBT')" style="cursor:pointer;">
            <rect x="30" y="35" width="24" height="12" fill="${swCol(s.cbBT)}" rx="2" stroke="#fff"/>
            <text x="42" y="43.5" fill="#fff" font-size="6.2" text-anchor="middle" font-family="monospace">52-BT</text>
          </g>

          <line x1="96" y1="24" x2="96" y2="122" stroke="${b.main_path ? '#06b6d4' : '#64748b'}" stroke-width="2" ${b.main_path ? '' : 'stroke-dasharray="3,2"'}/>
          ${flowOverlay('M 96,24 L 96,122 L 176,122', '#38bdf8', b.main_path, 1.1)}
          <g onclick="operateSwitch('dsMain')" style="cursor:pointer;">
            <rect x="82" y="58" width="28" height="10" rx="2" fill="${swCol(s.dsMain)}" stroke="#fff" stroke-width="0.7"/>
            <text x="96" y="65.5" fill="#fff" font-size="5.7" text-anchor="middle" font-family="monospace">89-69A</text>
          </g>
          <g onclick="operateSwitch('cbMain')" style="cursor:pointer;">
            <rect x="84" y="73" width="24" height="15" rx="2" fill="${swCol(s.cbMain)}" stroke="#fff" stroke-width="1.2"/>
            <text x="96" y="83" fill="#fff" font-size="6.8" text-anchor="middle" font-weight="bold" font-family="monospace">52-69</text>
          </g>
          <g onclick="operateSwitch('dsMainB')" style="cursor:pointer;">
            <rect x="82" y="93" width="28" height="10" rx="2" fill="${swCol(s.dsMainB)}" stroke="#fff" stroke-width="0.7"/>
            <text x="96" y="100.5" fill="#fff" font-size="5.7" text-anchor="middle" font-family="monospace">89-69B</text>
          </g>

          <path d="M 145,54 L 145,112 L 96,112" fill="none" stroke="${bypCol}" stroke-width="2" ${bypOn ? '' : 'stroke-dasharray="3,2"'}/>
          <g onclick="operateSwitch('dsBYP')" style="cursor:pointer;">
            <rect x="131" y="74" width="28" height="13" rx="2" fill="${swCol(s.dsBYP)}" stroke="#fff"/>
            <text x="145" y="83" fill="#fff" font-size="6.3" text-anchor="middle" font-family="monospace">89-BYP</text>
          </g>
          <line x1="96" y1="122" x2="176" y2="122" stroke="${hvCol}" stroke-width="2.2" ${b.txFeed ? '' : 'stroke-dasharray="3,2"'}/>
        `;
      } else if (top === 'ring') {
        const c1 = (s.cb1 && s.ds1A && s.ds1B);
        const c2 = (s.cb2 && s.ds2A && s.ds2B);
        const c3 = (s.cb3 && s.ds3A && s.ds3B);
        const c4 = (s.cb4 && s.ds4A && s.ds4B);
        const northPath = !!(c1 && c2);
        const southPath = !!(c4 && c3);
        primarySvg = `
          <text x="8" y="13" fill="#38bdf8" font-size="6.8" font-weight="bold" font-family="monospace">${vs.hvKv} kV RING BUS (4-CB LOOP)</text>
          <path d="M 28,80 L 28,34 L 146,34 L 146,126 L 28,126 L 28,80" fill="none" stroke="${hvCol}" stroke-width="2" ${b.txFeed ? '' : 'stroke-dasharray="3,2"'}/>
          <line x1="8" y1="80" x2="28" y2="80" stroke="#06b6d4" stroke-width="2.2"/>
          ${flowOverlay('M 8,80 L 28,80', '#38bdf8', true, 0.9)}
          ${flowOverlay('M 28,80 L 28,34 L 146,34 L 146,122 L 176,122', '#38bdf8', northPath, 1.35)}
          ${flowOverlay('M 28,80 L 28,126 L 146,126 L 146,122 L 176,122', '#2dd4bf', southPath, 1.45)}
          <text x="10" y="74" fill="#38bdf8" font-size="6" font-family="monospace">L1</text>
          <g onclick="operateSwitch('ds1A')" style="cursor:pointer;"><text x="40" y="27" fill="${swCol(s.ds1A)}" font-size="5.8" font-family="monospace">89-1A</text></g>
          <g onclick="operateSwitch('cb1')" style="cursor:pointer;">
            <rect x="75" y="27" width="24" height="14" rx="2" fill="${swCol(s.cb1)}" stroke="#fff"/>
            <text x="87" y="37" fill="#fff" font-size="6.8" text-anchor="middle" font-family="monospace">52-1</text>
          </g>
          <g onclick="operateSwitch('ds1B')" style="cursor:pointer;"><text x="106" y="27" fill="${swCol(s.ds1B)}" font-size="5.8" font-family="monospace">89-1B</text></g>
          <g onclick="operateSwitch('ds2A')" style="cursor:pointer;"><text x="149" y="54" fill="${swCol(s.ds2A)}" font-size="5.5" font-family="monospace">89-2A</text></g>
          <g onclick="operateSwitch('cb2')" style="cursor:pointer;">
            <rect x="134" y="65" width="24" height="14" rx="2" fill="${swCol(s.cb2)}" stroke="#fff"/>
            <text x="146" y="75" fill="#fff" font-size="6.8" text-anchor="middle" font-family="monospace">52-2</text>
          </g>
          <g onclick="operateSwitch('ds2B')" style="cursor:pointer;"><text x="149" y="96" fill="${swCol(s.ds2B)}" font-size="5.5" font-family="monospace">89-2B</text></g>
          <g onclick="operateSwitch('ds3A')" style="cursor:pointer;">${sldBadge(54, 141, '89-3A', swCol(s.ds3A), 'middle', 5.1)}</g>
          <g onclick="operateSwitch('cb3')" style="cursor:pointer;">
            <rect x="75" y="119" width="24" height="14" rx="2" fill="${swCol(s.cb3)}" stroke="#fff"/>
            <text x="87" y="129" fill="#fff" font-size="6.8" text-anchor="middle" font-family="monospace">52-3</text>
          </g>
          <g onclick="operateSwitch('ds3B')" style="cursor:pointer;">${sldBadge(118, 141, '89-3B', swCol(s.ds3B), 'middle', 5.1)}</g>
          <g onclick="operateSwitch('ds4A')" style="cursor:pointer;">${sldBadge(22, 62, '89-4A', swCol(s.ds4A), 'end', 4.9)}</g>
          <g onclick="operateSwitch('cb4')" style="cursor:pointer;">
            <rect x="16" y="92" width="24" height="14" rx="2" fill="${swCol(s.cb4)}" stroke="#fff"/>
            <text x="28" y="102" fill="#fff" font-size="6.8" text-anchor="middle" font-family="monospace">52-4</text>
          </g>
          <g onclick="operateSwitch('ds4B')" style="cursor:pointer;">${sldBadge(22, 121, '89-4B', swCol(s.ds4B), 'end', 4.9)}</g>
          <line x1="146" y1="122" x2="176" y2="122" stroke="${hvCol}" stroke-width="2.2" ${b.txFeed ? '' : 'stroke-dasharray="3,2"'}/>
          <text x="148" y="116" fill="#f59e0b" font-size="5.5" font-family="monospace">${(c1&&c2)||(c3&&c4)?'CLOSED':'SPLIT'}</text>
        `;
      } else if (top === 'doublebreaker') {
        const b1ACol = b.db_b1A ? '#06b6d4' : '#64748b';
        const b1BCol = b.db_b1B ? '#2dd4bf' : '#64748b';
        const b2ACol = b.db_b2A ? '#06b6d4' : '#64748b';
        const b2BCol = b.db_b2B ? '#2dd4bf' : '#64748b';
        const busACol = b.db_busA ? '#06b6d4' : '#64748b';
        const busBCol = b.db_busB ? '#2dd4bf' : '#64748b';
        primarySvg = `
          <text x="8" y="12" fill="#38bdf8" font-size="6.4" font-weight="bold" font-family="monospace">${vs.hvKv} kV DOUBLE BUS–DOUBLE BREAKER (2.0 CB)</text>
          <line x1="16" y1="24" x2="162" y2="24" stroke="${busACol}" stroke-width="3.2"/>
          <text x="88" y="19" fill="#38bdf8" font-size="5.5" text-anchor="middle" font-family="monospace">MAIN BUS A (100%)</text>
          <line x1="16" y1="160" x2="162" y2="160" stroke="${busBCol}" stroke-width="3.2"/>
          <text x="88" y="171" fill="#2dd4bf" font-size="5.5" text-anchor="middle" font-family="monospace">MAIN BUS B (100%)</text>

          <!-- Bay 1 (Incoming Line L1 -> Bus A via 52-1A & Bus B via 52-1B) -->
          <line x1="6" y1="92" x2="52" y2="92" stroke="#06b6d4" stroke-width="2.2"/>
          <text x="8" y="86" fill="#38bdf8" font-size="5.8" font-family="monospace">IN (L1)</text>
          <line x1="52" y1="24" x2="52" y2="92" stroke="${b1ACol}" stroke-width="2" ${b.db_b1A ? '' : 'stroke-dasharray="3,2"'}/>
          <line x1="52" y1="92" x2="52" y2="160" stroke="${b1BCol}" stroke-width="2" ${b.db_b1B ? '' : 'stroke-dasharray="3,2"'}/>

          <!-- Bay 2 (TR-01 Circuit -> Bus A via 52-2A & Bus B via 52-2B) -->
          <line x1="122" y1="24" x2="122" y2="122" stroke="${b2ACol}" stroke-width="2" ${b.db_b2A ? '' : 'stroke-dasharray="3,2"'}/>
          <line x1="122" y1="122" x2="122" y2="160" stroke="${b2BCol}" stroke-width="2" ${b.db_b2B ? '' : 'stroke-dasharray="3,2"'}/>
          <line x1="122" y1="122" x2="176" y2="122" stroke="${hvCol}" stroke-width="2.2" ${b.txFeed ? '' : 'stroke-dasharray="3,2"'}/>

          ${flowOverlay('M 6,92 L 52,92', '#38bdf8', true, 0.9)}
          ${flowOverlay('M 52,92 L 52,24 L 122,24 L 122,122 L 176,122', '#38bdf8', b.db_busA, 1.25)}
          ${flowOverlay('M 52,92 L 52,160 L 122,160 L 122,122 L 176,122', '#2dd4bf', b.db_busB, 1.25)}

          <g onclick="operateSwitch('ds1A1')" style="cursor:pointer;"><text x="54" y="34" fill="${swCol(s.ds1A1)}" font-size="4.8" font-family="monospace">89-1A1</text></g>
          <g onclick="operateSwitch('cb1A')" style="cursor:pointer;">
            <rect x="38" y="45" width="28" height="13" rx="2" fill="${swCol(s.cb1A)}" stroke="#fff"/>
            <text x="52" y="54" fill="#fff" font-size="6.1" text-anchor="middle" font-family="monospace">52-1A</text>
          </g>
          <g onclick="operateSwitch('ds1A2')" style="cursor:pointer;"><text x="54" y="69" fill="${swCol(s.ds1A2)}" font-size="4.8" font-family="monospace">89-1A2</text></g>

          <g onclick="operateSwitch('ds1B1')" style="cursor:pointer;"><text x="54" y="109" fill="${swCol(s.ds1B1)}" font-size="4.8" font-family="monospace">89-1B1</text></g>
          <g onclick="operateSwitch('cb1B')" style="cursor:pointer;">
            <rect x="38" y="116" width="28" height="13" rx="2" fill="${swCol(s.cb1B)}" stroke="#fff"/>
            <text x="52" y="125" fill="#fff" font-size="6.1" text-anchor="middle" font-family="monospace">52-1B</text>
          </g>
          <g onclick="operateSwitch('ds1B2')" style="cursor:pointer;"><text x="54" y="146" fill="${swCol(s.ds1B2)}" font-size="4.8" font-family="monospace">89-1B2</text></g>

          <g onclick="operateSwitch('ds2A1')" style="cursor:pointer;"><text x="124" y="34" fill="${swCol(s.ds2A1)}" font-size="4.8" font-family="monospace">89-2A1</text></g>
          <g onclick="operateSwitch('cb2A')" style="cursor:pointer;">
            <rect x="108" y="45" width="28" height="13" rx="2" fill="${swCol(s.cb2A)}" stroke="#fff"/>
            <text x="122" y="54" fill="#fff" font-size="6.1" text-anchor="middle" font-family="monospace">52-2A</text>
          </g>
          <g onclick="operateSwitch('ds2A2')" style="cursor:pointer;"><text x="124" y="69" fill="${swCol(s.ds2A2)}" font-size="4.8" font-family="monospace">89-2A2</text></g>

          <g onclick="operateSwitch('ds2B1')" style="cursor:pointer;"><text x="124" y="110" fill="${swCol(s.ds2B1)}" font-size="4.8" font-family="monospace">89-2B1</text></g>
          <g onclick="operateSwitch('cb2B')" style="cursor:pointer;">
            <rect x="108" y="129" width="28" height="13" rx="2" fill="${swCol(s.cb2B)}" stroke="#fff"/>
            <text x="122" y="138" fill="#fff" font-size="6.1" text-anchor="middle" font-family="monospace">52-2B</text>
          </g>
          <g onclick="operateSwitch('ds2B2')" style="cursor:pointer;"><text x="124" y="152" fill="${swCol(s.ds2B2)}" font-size="4.8" font-family="monospace">89-2B2</text></g>
        `;
      } else {
        const busACol = (s.cbA && s.dsA1) ? '#06b6d4' : '#64748b';
        const busBCol = (s.cbB && s.dsB2) ? '#06b6d4' : '#64748b';
        primarySvg = `
          <text x="8" y="13" fill="#38bdf8" font-size="6.8" font-weight="bold" font-family="monospace">${vs.hvKv} kV BREAKER-AND-A-HALF (1.5 CB)</text>
          <line x1="16" y1="26" x2="164" y2="26" stroke="${busACol}" stroke-width="3.2"/>
          <text x="18" y="21" fill="#38bdf8" font-size="5.8" font-family="monospace">MAIN BUS A</text>
          <line x1="16" y1="158" x2="164" y2="158" stroke="${busBCol}" stroke-width="3.2"/>
          <text x="18" y="170" fill="#38bdf8" font-size="5.8" font-family="monospace">MAIN BUS B</text>
          <line x1="88" y1="26" x2="88" y2="158" stroke="${hvCol}" stroke-width="2.2" ${b.txFeed ? '' : 'stroke-dasharray="3,2"'}/>
          <line x1="8" y1="71" x2="88" y2="71" stroke="#06b6d4" stroke-width="2.2"/>
          ${flowOverlay('M 8,71 L 88,71', '#38bdf8', true, 1.0)}
          ${flowOverlay('M 88,71 L 88,115 L 176,115', '#38bdf8', b.bh_tie, 1.1)}
          ${flowOverlay('M 88,71 L 88,26 L 164,26', '#2dd4bf', b.bh_busA, 1.2)}
          ${flowOverlay('M 88,158 L 88,115 L 176,115', '#2dd4bf', b.bh_busB, 1.2)}
          <text x="10" y="66" fill="#38bdf8" font-size="5.8" font-family="monospace">IN (L1)</text>
          <line x1="88" y1="115" x2="176" y2="115" stroke="${hvCol}" stroke-width="2.2" ${b.txFeed ? '' : 'stroke-dasharray="3,2"'}/>
          <text x="128" y="109" fill="#f59e0b" font-size="5.8" font-family="monospace">TR-01</text>
          <g onclick="operateSwitch('dsA1')" style="cursor:pointer;"><text x="52" y="38" fill="${swCol(s.dsA1)}" font-size="5.5" font-family="monospace">89-A1</text></g>
          <g onclick="operateSwitch('cbA')" style="cursor:pointer;">
            <rect x="75" y="40" width="26" height="14" rx="2" fill="${swCol(s.cbA)}" stroke="#fff"/>
            <text x="88" y="50" fill="#fff" font-size="6.8" text-anchor="middle" font-family="monospace">52-A</text>
          </g>
          <g onclick="operateSwitch('dsA2')" style="cursor:pointer;"><text x="104" y="49" fill="${swCol(s.dsA2)}" font-size="5.5" font-family="monospace">89-A2</text></g>
          <g onclick="operateSwitch('dsT1')" style="cursor:pointer;"><text x="50" y="88" fill="${swCol(s.dsT1)}" font-size="5.5" font-family="monospace">89-T1</text></g>
          <g onclick="operateSwitch('cbTIE')" style="cursor:pointer;">
            <rect x="72" y="84" width="32" height="14" rx="2" fill="${swCol(s.cbTIE)}" stroke="#fff"/>
            <text x="88" y="94" fill="#fff" font-size="6.5" text-anchor="middle" font-family="monospace">52-TIE</text>
          </g>
          <g onclick="operateSwitch('dsT2')" style="cursor:pointer;"><text x="107" y="94" fill="${swCol(s.dsT2)}" font-size="5.5" font-family="monospace">89-T2</text></g>
          <g onclick="operateSwitch('dsB1')" style="cursor:pointer;"><text x="52" y="135" fill="${swCol(s.dsB1)}" font-size="5.5" font-family="monospace">89-B1</text></g>
          <g onclick="operateSwitch('cbB')" style="cursor:pointer;">
            <rect x="75" y="128" width="26" height="14" rx="2" fill="${swCol(s.cbB)}" stroke="#fff"/>
            <text x="88" y="138" fill="#fff" font-size="6.8" text-anchor="middle" font-family="monospace">52-B</text>
          </g>
          <g onclick="operateSwitch('dsB2')" style="cursor:pointer;"><text x="104" y="138" fill="${swCol(s.dsB2)}" font-size="5.5" font-family="monospace">89-B2</text></g>
        `;
      }

      const ngrTxt = AppState.scNgrGrounded ? `NGR ${vs.ngrOhms}Ω` : 'UNGRND';
      const hasCascade = Array.isArray(vs.stageKvs) && vs.stageKvs.length > 2;
      const cascadeHdr = hasCascade ? `CASCADE (${vs.hvKv}→${distKv} kV)` : `TR-01 (${vs.hvKv}/${distKv} kV)`;
      const cascadeStageLine = hasCascade ? vs.stageKvs.join('→') + ' kV' : `${vs.mva} MVA ${vs.vectorGroup}`;
      const secondarySvg = `
        <line x1="176" y1="8" x2="176" y2="216" stroke="rgba(148,163,184,0.22)" stroke-dasharray="3,3"/>
        <text x="182" y="13" fill="#fbbf24" font-size="6.4" font-weight="bold" font-family="monospace">${cascadeHdr}</text>

        <g onclick="selectComponent('transformer', true)" style="cursor:pointer;">
          <circle cx="188" cy="122" r="8.5" fill="none" stroke="${sel==='transformer'?'#f59e0b':hvCol}" stroke-width="1.8"/>
          <circle cx="201" cy="122" r="8.5" fill="none" stroke="${sel==='transformer'?'#f59e0b':(b.txFeed?'#f59e0b':'#64748b')}" stroke-width="1.8"/>
          <text x="188" y="124.5" fill="#fff" font-size="6.5" text-anchor="middle" font-family="monospace">Δ</text>
          <text x="201" y="124.5" fill="#fff" font-size="6.5" text-anchor="middle" font-family="monospace">Y</text>
          <text x="195" y="109" fill="#f59e0b" font-size="6.0" text-anchor="middle" font-weight="bold" font-family="monospace">${hasCascade ? 'ATR+TR01' : 'TR-01'}</text>
        </g>
        <text x="198" y="142" fill="#fde68a" font-size="4.9" text-anchor="middle" font-family="monospace">${cascadeStageLine}</text>
        ${sldBadge(198, 155, ngrTxt, '#94a3b8', 'middle', 4.7)}

        <line x1="210" y1="122" x2="278" y2="122" stroke="${b.secMain ? '#f59e0b' : (b.txFeed ? '#fb923c' : '#64748b')}" stroke-width="2" ${b.secMain ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay('M 210,122 L 278,122', '#fbbf24', b.secMain && !b.subA_lv_backfed_from_B, 1.0)}
        <g onclick="operateSwitch('dsLV')" style="cursor:pointer;">
          ${sldBadge(219, 108, '89LVA', swCol(s.dsLV), 'middle', 4.8)}
          <circle cx="220" cy="122" r="2.2" fill="${swCol(s.dsLV)}"/>
        </g>
        <g onclick="operateSwitch('cbLV')" style="cursor:pointer;">
          <rect x="232" y="113" width="22" height="16" rx="2" fill="${swCol(s.cbLV)}" stroke="#fff" stroke-width="1.1"/>
          <text x="243" y="123" fill="#fff" font-size="6.2" text-anchor="middle" font-weight="bold" font-family="monospace">52LV</text>
        </g>
        <g onclick="operateSwitch('dsLVB')" style="cursor:pointer;">
          ${sldBadge(266, 108, '89LVB', swCol(s.dsLVB), 'middle', 4.8)}
          <circle cx="266" cy="122" r="2.2" fill="${swCol(s.dsLVB)}"/>
        </g>

        <line x1="278" y1="30" x2="278" y2="174" stroke="${secCol}" stroke-width="3.5" stroke-linecap="round" ${b.secMain ? '' : 'stroke-dasharray="4,3"'}/>
        ${flowOverlay('M 278,122 L 278,42', '#fbbf24', b.secMain, 0.9)}
        ${flowOverlay('M 278,122 L 278,158', '#fbbf24', b.secMain, 0.9)}
        <text x="278" y="25" fill="${secCol}" font-size="6.0" text-anchor="middle" font-weight="bold" font-family="monospace">${distKv} kV BUS A</text>

        <line x1="278" y1="42" x2="244" y2="42" stroke="${secCol}" stroke-width="1.6" stroke-dasharray="3,2"/>
        ${flowOverlay('M 278,42 L 244,42', '#f59e0b', b.sst100, 0.85)}
        <rect x="208" y="34" width="36" height="15" rx="2" fill="rgba(30,41,59,0.9)" stroke="${secCol}"/>
        <text x="226" y="44" fill="#fde68a" font-size="5.8" text-anchor="middle" font-family="monospace">SST-100</text>

        <!-- Feeder 01 (y = 82) -> North Loop -->
        <line x1="278" y1="82" x2="354" y2="82" stroke="${b.fdr1_from_subB ? '#38bdf8' : f1Col}" stroke-width="2" ${b.fdr1 ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(b.fdr1_from_subB ? 'M 354,82 L 278,82' : 'M 278,82 L 354,82', b.fdr1_from_subB ? '#38bdf8' : '#34d399', b.fdr1, 0.95)}
        <g onclick="operateSwitch('dsF1A')" style="cursor:pointer;">
          ${sldBadge(291, 73, '89F1A', swCol(s.dsF1A), 'middle', 4.7)}
          <circle cx="291" cy="82" r="2" fill="${swCol(s.dsF1A)}"/>
        </g>
        <g onclick="operateSwitch('cbF1')" style="cursor:pointer;">
          <rect x="301" y="74" width="22" height="15" rx="2" fill="${swCol(s.cbF1)}" stroke="#fff"/>
          <text x="312" y="84" fill="#fff" font-size="6.0" text-anchor="middle" font-weight="bold" font-family="monospace">52-F1</text>
        </g>
        <g onclick="operateSwitch('dsF1B')" style="cursor:pointer;">
          ${sldBadge(334, 94, '89F1B', swCol(s.dsF1B), 'middle', 4.7)}
          <circle cx="334" cy="82" r="2" fill="${swCol(s.dsF1B)}"/>
        </g>
        ${sldBadge(354, 73, b.fdr1_from_subB ? '◀ F1' : 'F1 ▶', b.fdr1_from_subB ? '#38bdf8' : f1Col, 'end', 5.0)}

        <!-- 52-CAP Switched Capacitor Bank (y = 117) -->
        <line x1="278" y1="117" x2="354" y2="117" stroke="${capCol}" stroke-width="1.8" ${b.capBank ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay('M 278,117 L 354,117', '#2dd4bf', b.capBank, 1.05)}
        <g onclick="operateSwitch('dsCapA')" style="cursor:pointer;">
          <text x="291" y="109" fill="${swCol(s.dsCapA)}" font-size="4.9" text-anchor="middle" font-family="monospace">89CA</text>
          <circle cx="291" cy="117" r="2" fill="${swCol(s.dsCapA)}"/>
        </g>
        <g onclick="operateSwitch('cbCap')" style="cursor:pointer;">
          <rect x="300" y="109" width="23" height="15" rx="2" fill="${swCol(s.cbCap)}" stroke="#fff"/>
          <text x="311.5" y="119" fill="#fff" font-size="5.7" text-anchor="middle" font-family="monospace">52CAP</text>
        </g>
        <g onclick="operateSwitch('dsCapB')" style="cursor:pointer;">
          <text x="333" y="109" fill="${swCol(s.dsCapB)}" font-size="4.9" text-anchor="middle" font-family="monospace">89CB</text>
          <circle cx="333" cy="117" r="2" fill="${swCol(s.dsCapB)}"/>
        </g>
        <text x="355" y="127" fill="${capCol}" font-size="4.9" text-anchor="end" font-family="monospace">${vs.capMvar}MVAR</text>

        <!-- Feeder 02 (y = 152) -> South Loop -->
        <line x1="278" y1="152" x2="354" y2="152" stroke="${b.fdr2_from_subB ? '#38bdf8' : f2Col}" stroke-width="2" ${b.fdr2 ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(b.fdr2_from_subB ? 'M 354,152 L 278,152' : 'M 278,152 L 354,152', b.fdr2_from_subB ? '#38bdf8' : '#34d399', b.fdr2, 0.95)}
        <g onclick="operateSwitch('dsF2A')" style="cursor:pointer;">
          ${sldBadge(291, 143, '89F2A', swCol(s.dsF2A), 'middle', 4.7)}
          <circle cx="291" cy="152" r="2" fill="${swCol(s.dsF2A)}"/>
        </g>
        <g onclick="operateSwitch('cbF2')" style="cursor:pointer;">
          <rect x="301" y="144" width="22" height="15" rx="2" fill="${swCol(s.cbF2)}" stroke="#fff"/>
          <text x="312" y="154" fill="#fff" font-size="6.0" text-anchor="middle" font-weight="bold" font-family="monospace">52-F2</text>
        </g>
        <g onclick="operateSwitch('dsF2B')" style="cursor:pointer;">
          ${sldBadge(334, 164, '89F2B', swCol(s.dsF2B), 'middle', 4.7)}
          <circle cx="334" cy="152" r="2" fill="${swCol(s.dsF2B)}"/>
        </g>
        ${sldBadge(354, 143, b.fdr2_from_subB ? '◀ F2' : 'F2 ▶', b.fdr2_from_subB ? '#38bdf8' : f2Col, 'end', 5.0)}

        <!-- Dedicated 69/138 kV Industrial Sub-Transmission Tap (52-IND -> Customer Substation) -->
        <path d="M 166,122 L 166,198 L 282,198" fill="none" stroke="${indCol}" stroke-width="2" ${b.ind_hv ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay('M 166,122 L 166,198 L 282,198', '#fbbf24', b.ind_hv, 1.0)}
        <g onclick="operateSwitch('dsIndA')" style="cursor:pointer;">
          <text x="192" y="190" fill="${swCol(s.dsIndA !== false)}" font-size="4.8" text-anchor="middle" font-family="monospace">89-INDA</text>
          <circle cx="192" cy="198" r="2" fill="${swCol(s.dsIndA !== false)}"/>
        </g>
        <g onclick="operateSwitch('cbIndHv')" style="cursor:pointer;">
          <rect x="205" y="190" width="26" height="15" rx="2" fill="${swCol(s.cbIndHv !== false)}" stroke="#fff"/>
          <text x="218" y="200" fill="#fff" font-size="5.6" text-anchor="middle" font-weight="bold" font-family="monospace">52-IND</text>
        </g>
        <g onclick="operateSwitch('dsIndB')" style="cursor:pointer;">
          <text x="246" y="190" fill="${swCol(s.dsIndB !== false)}" font-size="4.8" text-anchor="middle" font-family="monospace">89-INDB</text>
          <circle cx="246" cy="198" r="2" fill="${swCol(s.dsIndB !== false)}"/>
        </g>
        <g onclick="selectComponent('dt_ind_1500', true)" style="cursor:pointer;">
          <rect x="282" y="185" width="70" height="25" rx="2.5" fill="rgba(30,41,59,0.95)" stroke="${indCol}"/>
          <text x="317" y="196" fill="${b.ind_hv ? '#fbbf24' : '#64748b'}" font-size="5.1" text-anchor="middle" font-weight="bold" font-family="monospace">52-CUST IND SUB</text>
          <text x="317" y="205.5" fill="#cbd5e1" font-size="4.7" text-anchor="middle" font-family="monospace">${indKv}kV · ${vs.indCustMva || 25}MVA</text>
        </g>
      `;

      // Interactive Pinpoint Fault Hotspots & Active Fault Surge Overlay
      const hotspotRingCol = AppState.pinpointFaultMode ? '#f43f5e' : 'rgba(56,189,248,0.22)';
      const hotspotsSvg = Object.entries(faultPosMap).map(([nId, pt]) => `
        <g onclick="onSldHotspotClick('${nId}')" style="cursor:crosshair;">
          <circle cx="${pt.x}" cy="${pt.y}" r="${AppState.pinpointFaultMode ? 6.5 : 4.2}" fill="rgba(244,63,94,0.08)" stroke="${hotspotRingCol}" stroke-width="${AppState.pinpointFaultMode ? 1.1 : 0.6}" stroke-dasharray="2,1"/>
          <title>Inject Fault at ${PINPOINT_FAULT_NODES[nId] ? PINPOINT_FAULT_NODES[nId].name : nId}</title>
        </g>
      `).join('');

      let activeFaultSvg = '';
      if (faultNode && faultPosMap[faultNode]) {
        const fp = faultPosMap[faultNode];
        const surgePath = computeOrthogonalSldFaultPath(top, faultNode, s, b);
        const scMeta = PINPOINT_FAULT_NODES[faultNode] || PINPOINT_FAULT_NODES.node5_lv_bus;
        const scRes = (typeof computeShortCircuitMetrics === 'function') ? computeShortCircuitMetrics() : null;
        const ftypeLabels = { '3ph': '3Φ SYMM (LLL)', 'slg': 'SLG (A-G)', 'll': 'L-L (B-C)', 'dlg': 'DLG (B-C-G)' };
        const ftText = ftypeLabels[AppState.scFaultType || '3ph'] || '3Φ SYMM';
        const shortLocName = scMeta.name.replace('Secondary Main Bus (13.8 kV)', `${vs.lvKv}kV Main Bus`).replace('Primary HV Bus Section', `${vs.hvKv}kV HV Bus`);
        const trippers = scMeta.breakerNames ? scMeta.breakerNames(top, b) : '52';
        const zoneTxt = (scMeta.zone || 'ANSI 50/51').split('+')[0].trim();

        const boxW = 114;
        const boxH = 38;
        const boxX = Math.max(-44, Math.min(924 - boxW, fp.x > 210 ? (fp.x - boxW - 10) : (fp.x + 10)));
        const boxY = Math.max(-4, Math.min(222 - boxH, fp.y > 125 ? (fp.y - boxH - 4) : (fp.y + 8)));

        const line2 = scRes ? `If = ${scRes.iFaultPu.toFixed(2)} pu | ${scRes.iSymKa.toFixed(2)} kA sym` : 'If = COMPUTING';
        const line3 = scRes ? `Ipk = ${scRes.iPeakKa.toFixed(1)} kA | Ssc = ${scRes.sScMva.toFixed(0)} MVA` : '';
        const line4 = `${zoneTxt} → Trip ${trippers}`.slice(0, 32);

        activeFaultSvg = `
          ${flowOverlay(surgePath, '#f43f5e', true, 0.4, true)}
          <g class="sld-fault-pulse">
            <circle cx="${fp.x}" cy="${fp.y}" r="7.5" fill="rgba(239,68,68,0.28)" stroke="#ef4444" stroke-width="1.5"/>
            <text x="${fp.x}" y="${Math.max(12, fp.y - 9)}" fill="#fef08a" font-size="6.4" text-anchor="middle" font-weight="bold" font-family="monospace">⚡ FAULT</text>
          </g>
          <g class="sld-fault-callout">
            <rect x="${boxX}" y="${boxY}" width="${boxW}" height="${boxH}" rx="3" fill="rgba(15, 23, 42, 0.95)" stroke="#f43f5e" stroke-width="1.1"/>
            <text x="${boxX + 4}" y="${boxY + 8.5}" fill="#fef08a" font-size="5.3" font-weight="bold" font-family="monospace">⚡ ${ftText} @ ${shortLocName.slice(0, 18)}</text>
            <text x="${boxX + 4}" y="${boxY + 17.5}" fill="#fda4af" font-size="5.2" font-weight="bold" font-family="monospace">${line2}</text>
            <text x="${boxX + 4}" y="${boxY + 26.0}" fill="#e2e8f0" font-size="5.0" font-family="monospace">${line3}</text>
            <text x="${boxX + 4}" y="${boxY + 34.0}" fill="#67e8f9" font-size="4.8" font-family="monospace">${line4}</text>
          </g>
        `;
      }

      // Extended Dual 13.8 kV Distribution Corridors & East-to-West Substation B Schematic (x = 356 .. 876, viewBox = 0 0 880 245)
      const d1Col = b.dist_f1_sec1 ? (b.fdr1_from_subB ? '#38bdf8' : '#10b981') : '#64748b';
      const d2Col = b.dist_f1_sec2 ? (b.fdr1_from_subB ? '#38bdf8' : '#10b981') : '#64748b';
      const latCol = b.dist_lateral ? '#fbbf24' : '#64748b';
      const d2mCol = b.dist_f2_main ? (b.fdr2_from_subB ? '#38bdf8' : '#10b981') : '#64748b';
      const f3Col = b.dist_f3 ? (b.fdr3_from_subA ? '#38bdf8' : '#10b981') : '#64748b';
      const f4Col = b.dist_f4 ? (b.fdr4_from_subA ? '#38bdf8' : '#10b981') : '#64748b';
      const reverseFlisr = !!b.fdr1_from_subB;
      const reverseSouthFlisr = !!b.fdr2_from_subB;
      const eastBackfeed = !!(b.fdr3_from_subA || b.fdr4_from_subA);
      const anyBackfeed = reverseFlisr || reverseSouthFlisr || eastBackfeed;
      const subBTop = AppState.subBTopology || 'ring';
      const subBEnc = (AppState.subBEnclosure || 'ais').toUpperCase();
      const sbOn = b.dist_sub_b;
      const sbHvActive = s.cbTieA !== false;
      const sbHvCol = sbHvActive ? '#06b6d4' : '#64748b';
      const sbHvCbCol = swCol(sbHvActive);
      const sbSecCol = (sbOn || b.subB_lv_backfed_from_A) ? '#f59e0b' : '#64748b';
      const sbTxY = 117;

      // Right-to-Left ANSI/IEEE C37.2 Substation B Schematic:
      // East HV IN (x=868..838) -> Active HV Topology (x=742..838) -> TR-02 (x=706..738) -> 89-LVBA/52-LVB/89-LVBB (x=640..704) -> 13.8 kV Bus B (x=640) -> 52-F3 & 52-F4 (x=576..640)
      let subBHvSvg = '';
      if (subBTop === 'single') {
        subBHvSvg = `
          <text x="802" y="31" fill="#38bdf8" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">${vs.hvKv}kV SINGLE BUS (${subBEnc})</text>
          <line x1="870" y1="54" x2="834" y2="54" stroke="${sbHvCol}" stroke-width="2.1"/>
          ${flowOverlay('M 870,54 L 834,54', '#38bdf8', true, 0.85)}
          <text x="869" y="47" fill="#38bdf8" font-size="4.8" text-anchor="end" font-weight="bold" font-family="monospace">◄ HV IN ${vs.hvKv}kV</text>
          <text x="852" y="65" fill="#94a3b8" font-size="4.5" text-anchor="middle" font-family="monospace">LA-B / 89LB1</text>
          <line x1="834" y1="38" x2="834" y2="180" stroke="${sbHvCol}" stroke-width="3.0" stroke-linecap="round"/>
          <line x1="834" y1="${sbTxY}" x2="736" y2="${sbTxY}" stroke="${sbHvCol}" stroke-width="2.0"/>
          ${flowOverlay(`M 834,${sbTxY} L 736,${sbTxY}`, '#38bdf8', true, 0.95)}
          <circle cx="820" cy="${sbTxY}" r="2.0" fill="#ef4444"/><text x="820" y="${sbTxY - 7}" fill="#ef4444" font-size="4.6" text-anchor="middle" font-family="monospace">89B2</text>
          <rect x="782" y="${sbTxY - 8}" width="24" height="15" rx="2" fill="#ef4444" stroke="#fff" stroke-width="0.9"/>
          <text x="794" y="${sbTxY + 2}" fill="#fff" font-size="5.6" text-anchor="middle" font-weight="bold" font-family="monospace">52-B</text>
          <circle cx="766" cy="${sbTxY}" r="2.0" fill="#ef4444"/><text x="766" y="${sbTxY - 7}" fill="#ef4444" font-size="4.6" text-anchor="middle" font-family="monospace">89B1</text>
          <rect x="772" y="152" width="44" height="12" rx="2" fill="rgba(15,23,42,0.85)" stroke="#10b981" stroke-width="0.7"/>
          <text x="794" y="160" fill="#10b981" font-size="4.6" text-anchor="middle" font-family="monospace">89EB: OPN</text>
        `;
      } else if (subBTop === 'maintransfer') {
        subBHvSvg = `
          <text x="802" y="31" fill="#38bdf8" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">${vs.hvKv}kV MAIN+XFER (${subBEnc})</text>
          <line x1="870" y1="50" x2="838" y2="50" stroke="${sbHvCol}" stroke-width="2.1"/>
          ${flowOverlay('M 870,50 L 838,50', '#38bdf8', true, 0.85)}
          <text x="869" y="43" fill="#38bdf8" font-size="4.7" text-anchor="end" font-weight="bold" font-family="monospace">◄ HV IN</text>
          <line x1="838" y1="38" x2="838" y2="184" stroke="${sbHvCol}" stroke-width="3.0"/>
          <text x="841" y="182" fill="#38bdf8" font-size="4.3" font-family="monospace">MAIN</text>
          <line x1="814" y1="42" x2="814" y2="180" stroke="#f59e0b" stroke-width="2.0" stroke-dasharray="3,2"/>
          <text x="812" y="188" fill="#f59e0b" font-size="4.3" text-anchor="end" font-family="monospace">XFER</text>
          <!-- Bus-Tie 52-BTB at bottom -->
          <line x1="814" y1="164" x2="838" y2="164" stroke="#f59e0b" stroke-width="1.6"/>
          <rect x="819" y="158" width="14" height="11" rx="1.5" fill="#10b981" stroke="#fff" stroke-width="0.7"/>
          <text x="826" y="166" fill="#fff" font-size="4.2" text-anchor="middle" font-family="monospace">BT</text>
          <text x="800" y="166" fill="#10b981" font-size="4.3" text-anchor="end" font-family="monospace">89BT1/2</text>
          <!-- Bypass Jumper over top -> 89-BYPB -->
          <path d="M 814,68 L 750,68 L 750,${sbTxY}" fill="none" stroke="#f59e0b" stroke-width="1.4" stroke-dasharray="2.5,2"/>
          <rect x="768" y="61" width="28" height="11" rx="1.5" fill="#10b981" stroke="#fff" stroke-width="0.7"/>
          <text x="782" y="68.5" fill="#fff" font-size="4.4" text-anchor="middle" font-family="monospace">89BYP</text>
          <!-- Main TR-02 Bay -->
          <line x1="838" y1="${sbTxY}" x2="736" y2="${sbTxY}" stroke="${sbHvCol}" stroke-width="2.0"/>
          ${flowOverlay(`M 838,${sbTxY} L 736,${sbTxY}`, '#38bdf8', true, 0.95)}
          <circle cx="826" cy="${sbTxY}" r="1.9" fill="#ef4444"/><text x="826" y="${sbTxY - 6}" fill="#ef4444" font-size="4.3" text-anchor="middle" font-family="monospace">89B2</text>
          <rect x="784" y="${sbTxY - 8}" width="24" height="15" rx="2" fill="#ef4444" stroke="#fff" stroke-width="0.9"/>
          <text x="796" y="${sbTxY + 2}" fill="#fff" font-size="5.4" text-anchor="middle" font-weight="bold" font-family="monospace">52-B</text>
          <circle cx="770" cy="${sbTxY}" r="1.9" fill="#ef4444"/><text x="770" y="${sbTxY - 6}" fill="#ef4444" font-size="4.3" text-anchor="middle" font-family="monospace">89B1</text>
        `;
      } else if (subBTop === 'ring') {
        subBHvSvg = `
          <text x="802" y="31" fill="#34d399" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">${vs.hvKv}kV RING BUS (4-CB)</text>
          <polygon points="756,48 840,48 840,180 756,180" fill="none" stroke="${sbHvCol}" stroke-width="2.0"/>
          <line x1="870" y1="112" x2="840" y2="112" stroke="${sbHvCol}" stroke-width="2.1"/>
          ${flowOverlay('M 870,112 L 840,112', '#38bdf8', true, 0.8)}
          <text x="869" y="104" fill="#38bdf8" font-size="4.6" text-anchor="end" font-weight="bold" font-family="monospace">◄ IN ${vs.hvKv}kV</text>
          <line x1="756" y1="${sbTxY}" x2="736" y2="${sbTxY}" stroke="${sbHvCol}" stroke-width="2.0"/>
          ${flowOverlay('M 840,112 L 840,48 L 756,48 L 756,117 L 736,117', '#38bdf8', true, 1.3)}
          ${flowOverlay('M 840,112 L 840,180 L 756,180 L 756,117 L 736,117', '#2dd4bf', true, 1.35)}
          <!-- North Ring CB 52-1B + 89-1A/1B -->
          <rect x="786" y="41" width="24" height="13" rx="1.8" fill="${sbHvCbCol}" stroke="#fff" stroke-width="0.8"/>
          <text x="798" y="50" fill="#fff" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">52-1B</text>
          ${sldBadge(774, 41, '89-1A', sbHvCbCol, 'middle', 4.3)}
          ${sldBadge(822, 41, '89-1B', sbHvCbCol, 'middle', 4.3)}
          <!-- East-North Ring CB 52-2B + 89-2A/2B -->
          <rect x="828" y="68" width="24" height="13" rx="1.8" fill="${sbHvCbCol}" stroke="#fff" stroke-width="0.8"/>
          <text x="840" y="77" fill="#fff" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">52-2B</text>
          ${sldBadge(854, 62, '89-2A', sbHvCbCol, 'start', 4.2)}
          ${sldBadge(854, 91, '89-2B', sbHvCbCol, 'start', 4.2)}
          <!-- South Ring CB 52-3B + 89-3A/3B -->
          <rect x="786" y="173" width="24" height="13" rx="1.8" fill="${sbHvCbCol}" stroke="#fff" stroke-width="0.8"/>
          <text x="798" y="182" fill="#fff" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">52-3B</text>
          ${sldBadge(774, 196, '89-3A', sbHvCbCol, 'middle', 4.3)}
          ${sldBadge(822, 196, '89-3B', sbHvCbCol, 'middle', 4.3)}
          <!-- West-South Ring CB 52-4B + 89-4A/4B -->
          <rect x="744" y="138" width="24" height="13" rx="1.8" fill="${sbHvCbCol}" stroke="#fff" stroke-width="0.8"/>
          <text x="756" y="147" fill="#fff" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">52-4B</text>
          ${sldBadge(742, 132, '89-4A', sbHvCbCol, 'end', 4.2)}
          ${sldBadge(742, 162, '89-4B', sbHvCbCol, 'end', 4.2)}
        `;
      } else if (subBTop === 'breakerhalf') {
        subBHvSvg = `
          <text x="802" y="31" fill="#34d399" font-size="5.0" text-anchor="middle" font-weight="bold" font-family="monospace">${vs.hvKv}kV 1.5 CB (${subBEnc})</text>
          <line x1="748" y1="44" x2="862" y2="44" stroke="${sbHvCol}" stroke-width="2.8"/>
          <text x="805" y="39" fill="#38bdf8" font-size="4.5" text-anchor="middle" font-family="monospace">MAIN BUS A</text>
          <line x1="748" y1="184" x2="862" y2="184" stroke="${sbHvCol}" stroke-width="2.8"/>
          <text x="805" y="194" fill="#2dd4bf" font-size="4.5" text-anchor="middle" font-family="monospace">MAIN BUS B</text>
          <line x1="802" y1="44" x2="802" y2="184" stroke="${sbHvCol}" stroke-width="2.0"/>
          <line x1="870" y1="86" x2="802" y2="86" stroke="${sbHvCol}" stroke-width="2.0"/>
          <text x="869" y="79" fill="#38bdf8" font-size="4.6" text-anchor="end" font-weight="bold" font-family="monospace">◄ IN ${vs.hvKv}kV</text>
          <path d="M 802,136 L 752,136 L 752,${sbTxY} L 736,${sbTxY}" fill="none" stroke="${sbHvCol}" stroke-width="2.0"/>
          ${flowOverlay(`M 870,86 L 802,86 L 802,136 L 752,136 L 752,${sbTxY} L 736,${sbTxY}`, '#38bdf8', true, 1.15)}
          ${flowOverlay(`M 802,86 L 802,44 L 860,44`, '#2dd4bf', true, 1.25)}
          <rect x="789" y="57" width="26" height="12" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.8"/>
          <text x="802" y="65.5" fill="#fff" font-size="4.9" text-anchor="middle" font-weight="bold" font-family="monospace">52-AB</text>
          <text x="818" y="56" fill="#ef4444" font-size="4.2" font-family="monospace">89A1</text><text x="818" y="74" fill="#ef4444" font-size="4.2" font-family="monospace">89A2</text>
          <rect x="786" y="102" width="32" height="13" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.8"/>
          <text x="802" y="111" fill="#fff" font-size="4.9" text-anchor="middle" font-weight="bold" font-family="monospace">52-TIE</text>
          <text x="820" y="101" fill="#ef4444" font-size="4.2" font-family="monospace">89T1</text><text x="820" y="121" fill="#ef4444" font-size="4.2" font-family="monospace">89T2</text>
          <rect x="789" y="152" width="26" height="12" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.8"/>
          <text x="802" y="160.5" fill="#fff" font-size="4.9" text-anchor="middle" font-weight="bold" font-family="monospace">52-BB</text>
          <text x="818" y="150" fill="#ef4444" font-size="4.2" font-family="monospace">89B1</text><text x="818" y="170" fill="#ef4444" font-size="4.2" font-family="monospace">89B2</text>
        `;
      } else {
        // doublebreaker (2.0 CB)
        subBHvSvg = `
          <text x="802" y="31" fill="#34d399" font-size="4.8" text-anchor="middle" font-weight="bold" font-family="monospace">${vs.hvKv}kV 2.0 CB (${subBEnc})</text>
          <line x1="748" y1="44" x2="862" y2="44" stroke="${sbHvCol}" stroke-width="2.8"/>
          <text x="805" y="39" fill="#38bdf8" font-size="4.5" text-anchor="middle" font-family="monospace">MAIN BUS A (100%)</text>
          <line x1="748" y1="184" x2="862" y2="184" stroke="#2dd4bf" stroke-width="2.8"/>
          <text x="805" y="194" fill="#2dd4bf" font-size="4.5" text-anchor="middle" font-family="monospace">MAIN BUS B (100%)</text>
          <!-- East Bay 1 (HV IN) at x=826 -->
          <line x1="870" y1="114" x2="826" y2="114" stroke="${sbHvCol}" stroke-width="2.0"/>
          <text x="869" y="106" fill="#38bdf8" font-size="4.5" text-anchor="end" font-weight="bold" font-family="monospace">◄ IN</text>
          <line x1="826" y1="44" x2="826" y2="184" stroke="${sbHvCol}" stroke-width="1.8"/>
          <!-- West Bay 2 (TR-02) at x=770 -->
          <line x1="770" y1="44" x2="770" y2="184" stroke="${sbHvCol}" stroke-width="1.8"/>
          <line x1="770" y1="${sbTxY}" x2="736" y2="${sbTxY}" stroke="${sbHvCol}" stroke-width="2.0"/>
          ${flowOverlay(`M 870,114 L 826,114 L 826,44 L 770,44 L 770,${sbTxY} L 736,${sbTxY}`, '#38bdf8', true, 1.2)}
          ${flowOverlay(`M 826,114 L 826,184 L 770,184 L 770,${sbTxY}`, '#2dd4bf', true, 1.2)}
          <rect x="812" y="64" width="28" height="12" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.7"/>
          <text x="826" y="72.5" fill="#fff" font-size="4.8" text-anchor="middle" font-family="monospace">52-1AB</text>
          <rect x="812" y="148" width="28" height="12" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.7"/>
          <text x="826" y="156.5" fill="#fff" font-size="4.8" text-anchor="middle" font-family="monospace">52-1BB</text>
          <text x="842" y="58" fill="#ef4444" font-size="4.0" font-family="monospace">89-1A</text>
          <text x="842" y="172" fill="#ef4444" font-size="4.0" font-family="monospace">89-1B</text>
          <rect x="756" y="64" width="28" height="12" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.7"/>
          <text x="770" y="72.5" fill="#fff" font-size="4.8" text-anchor="middle" font-family="monospace">52-2AB</text>
          <rect x="756" y="148" width="28" height="12" rx="1.6" fill="#ef4444" stroke="#fff" stroke-width="0.7"/>
          <text x="770" y="156.5" fill="#fff" font-size="4.8" text-anchor="middle" font-family="monospace">52-2BB</text>
          <text x="754" y="58" fill="#ef4444" font-size="4.0" text-anchor="end" font-family="monospace">89-2A</text>
          <text x="754" y="172" fill="#ef4444" font-size="4.0" text-anchor="end" font-family="monospace">89-2B</text>
        `;
      }

      const f3BayClosed = (s.cbF3 !== false && s.dsF3A !== false && s.dsF3B !== false);
      const f4BayClosed = (s.cbF4 !== false && s.dsF4A !== false && s.dsF4B !== false);
      const f3BayLive = f3BayClosed && (sbOn || (b.fdr3_from_subA && b.dist_f3));
      const f4BayLive = f4BayClosed && (sbOn || (b.fdr4_from_subA && b.dist_f4));
      const f3BayPath = b.fdr3_from_subA ? 'M 576,82 L 640,82' : 'M 640,82 L 576,82';
      const f4BayPath = b.fdr4_from_subA ? 'M 576,152 L 640,152' : 'M 640,152 L 576,152';

      const subBSvg = `
        <!-- Substation B Secondary 13.8 kV Feeders (52-F3 North, 52-F4 South), 13.8 kV Bus B, 52-LVB Main & TR-02 -->
        <line x1="640" y1="82" x2="576" y2="82" stroke="${f3BayLive ? (b.fdr3_from_subA ? '#38bdf8' : '#10b981') : '#64748b'}" stroke-width="2.0" ${f3BayLive ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(f3BayPath, b.fdr3_from_subA ? '#38bdf8' : '#34d399', f3BayLive, 0.9)}
        <g onclick="operateSwitch('dsF3A')" style="cursor:pointer;">
          <circle cx="629" cy="82" r="1.9" fill="${swCol(s.dsF3A !== false)}"/>
          ${sldBadge(629, 72, '89F3A', swCol(s.dsF3A !== false), 'middle', 4.5)}
        </g>
        <g onclick="operateSwitch('cbF3')" style="cursor:pointer;">
          <rect x="598" y="74" width="22" height="15" rx="1.8" fill="${swCol(s.cbF3 !== false)}" stroke="#fff" stroke-width="0.8"/>
          <text x="609" y="84" fill="#fff" font-size="5.3" text-anchor="middle" font-weight="bold" font-family="monospace">52-F3</text>
        </g>
        <g onclick="operateSwitch('dsF3B')" style="cursor:pointer;">
          <circle cx="588" cy="82" r="1.9" fill="${swCol(s.dsF3B !== false)}"/>
          ${sldBadge(588, 94, '89F3B', swCol(s.dsF3B !== false), 'middle', 4.5)}
        </g>

        <line x1="640" y1="152" x2="576" y2="152" stroke="${f4BayLive ? (b.fdr4_from_subA ? '#38bdf8' : '#10b981') : '#64748b'}" stroke-width="2.0" ${f4BayLive ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(f4BayPath, b.fdr4_from_subA ? '#38bdf8' : '#34d399', f4BayLive, 0.9)}
        <g onclick="operateSwitch('dsF4A')" style="cursor:pointer;">
          <circle cx="629" cy="152" r="1.9" fill="${swCol(s.dsF4A !== false)}"/>
          ${sldBadge(629, 142, '89F4A', swCol(s.dsF4A !== false), 'middle', 4.5)}
        </g>
        <g onclick="operateSwitch('cbF4')" style="cursor:pointer;">
          <rect x="598" y="144" width="22" height="15" rx="1.8" fill="${swCol(s.cbF4 !== false)}" stroke="#fff" stroke-width="0.8"/>
          <text x="609" y="154" fill="#fff" font-size="5.3" text-anchor="middle" font-weight="bold" font-family="monospace">52-F4</text>
        </g>
        <g onclick="operateSwitch('dsF4B')" style="cursor:pointer;">
          <circle cx="588" cy="152" r="1.9" fill="${swCol(s.dsF4B !== false)}"/>
          ${sldBadge(588, 164, '89F4B', swCol(s.dsF4B !== false), 'middle', 4.5)}
        </g>

        <!-- Sub B 13.8 kV Bus & Secondary Main 52-LVB -->
        <line x1="640" y1="54" x2="640" y2="176" stroke="${sbSecCol}" stroke-width="3.2" stroke-linecap="round" ${(sbOn || b.subB_lv_backfed_from_A) ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay('M 640,117 L 640,82', '#fbbf24', sbOn || b.subB_lv_backfed_from_A, 0.8)}
        ${flowOverlay('M 640,117 L 640,152', '#fbbf24', sbOn || b.subB_lv_backfed_from_A, 0.8)}
        <text x="640" y="47" fill="${sbSecCol}" font-size="5.3" text-anchor="middle" font-weight="bold" font-family="monospace">${distKv}kV BUS B</text>

        <line x1="704" y1="117" x2="640" y2="117" stroke="${sbOn ? '#f59e0b' : '#64748b'}" stroke-width="2.0" ${sbOn ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay('M 704,117 L 640,117', '#fbbf24', sbOn, 0.9)}
        <g onclick="operateSwitch('dsLVBB')" style="cursor:pointer;">
          <circle cx="651" cy="117" r="1.9" fill="${swCol(s.dsLVBB !== false)}"/>
          ${sldBadge(651, 108, '89LVBB', swCol(s.dsLVBB !== false), 'middle', 4.3)}
        </g>
        <g onclick="operateSwitch('cbLVB')" style="cursor:pointer;">
          <rect x="661" y="109" width="22" height="15" rx="1.8" fill="${swCol(s.cbLVB !== false)}" stroke="#fff" stroke-width="0.9"/>
          <text x="672" y="119" fill="#fff" font-size="5.1" text-anchor="middle" font-weight="bold" font-family="monospace">52-LVB</text>
        </g>
        <g onclick="operateSwitch('dsLVBA')" style="cursor:pointer;">
          <circle cx="693" cy="117" r="1.9" fill="${swCol(s.dsLVBA !== false)}"/>
          ${sldBadge(694, 108, '89LVBA', swCol(s.dsLVBA !== false), 'middle', 4.3)}
        </g>

        <!-- TR-02 Power Transformer (Y on West LV -> Δ on East HV) -->
        <circle cx="712" cy="117" r="8.0" fill="none" stroke="${sbSecCol}" stroke-width="1.6"/>
        <circle cx="725" cy="117" r="8.0" fill="none" stroke="${sbHvCol}" stroke-width="1.6"/>
        <text x="712" y="119.5" fill="#fff" font-size="5.8" text-anchor="middle" font-family="monospace">Y</text>
        <text x="725" y="119.5" fill="#fff" font-size="5.8" text-anchor="middle" font-family="monospace">Δ</text>
        <text x="719" y="105" fill="#10b981" font-size="5.4" text-anchor="middle" font-weight="bold" font-family="monospace">TR-02</text>
        <text x="719" y="134" fill="#94a3b8" font-size="4.6" text-anchor="middle" font-family="monospace">${vs.hvKv}/${distKv}kV</text>
        <line x1="740" y1="26" x2="740" y2="198" stroke="rgba(16,185,129,0.22)" stroke-dasharray="2.5,2.5"/>
        ${subBHvSvg}
      `;

      const d1Sec1Path = (b.fdr1_from_subB && !!s.sec34) ? 'M 414,82 L 354,82' : 'M 354,82 L 414,82';
      const tie1FlowSvg = b.tie1_dir === 'AtoB'
        ? flowOverlay('M 468,82 L 496,82', '#38bdf8', true, 0.8)
        : (b.tie1_dir === 'BtoA' ? flowOverlay('M 496,82 L 468,82', '#38bdf8', true, 0.8) : '');
      const tie2FlowSvg = b.tie2_dir === 'AtoB'
        ? flowOverlay('M 468,152 L 496,152', '#38bdf8', true, 0.8)
        : (b.tie2_dir === 'BtoA' ? flowOverlay('M 496,152 L 468,152', '#38bdf8', true, 0.8) : '');

      const distSvg = `
        <line x1="358" y1="8" x2="358" y2="216" stroke="rgba(148,163,184,0.22)" stroke-dasharray="3,3"/>
        <text x="468" y="13" fill="#67e8f9" font-size="5.8" text-anchor="middle" font-weight="bold" font-family="monospace">13.8 kV CITY LOOP CORRIDORS (140m SETBACK ROW ↔ EAST)</text>

        <!-- NORTH LOOP (y = 82): 52-F1 -> 79-ACR1 -> URD + 34-SECT -> 100K/RES -> 79-TIE1 <-> EAST UNI 500kVA <-> 52-F3 -->
        <line x1="354" y1="82" x2="414" y2="82" stroke="${d1Col}" stroke-width="2" ${b.dist_f1_sec1 ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(d1Sec1Path, b.fdr1_from_subB ? '#38bdf8' : '#34d399', b.dist_f1_sec1, 0.95)}
        <g onclick="operateSwitch('cbACR1')" style="cursor:pointer;">
          <rect x="366" y="75" width="28" height="14" rx="2" fill="${swCol(s.cbACR1)}" stroke="#fff"/>
          <text x="380" y="84.5" fill="#fff" font-size="5.4" text-anchor="middle" font-weight="bold" font-family="monospace">79-ACR1</text>
        </g>

        <g onclick="operateSwitch('sec34')" style="cursor:pointer;">
          <circle cx="414" cy="82" r="2.0" fill="#fff"/><circle cx="428" cy="82" r="2.0" fill="#fff"/>
          <line x1="414" y1="82" x2="${s.sec34 ? 428 : 424}" y2="${s.sec34 ? 82 : 71}" stroke="${swCol(s.sec34)}" stroke-width="2.1"/>
          ${sldBadge(421, 66, '34-SECT', swCol(s.sec34), 'middle', 4.7)}
        </g>

        <line x1="428" y1="82" x2="468" y2="82" stroke="${d2Col}" stroke-width="2.0" ${b.dist_f1_sec2 ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(reverseFlisr ? 'M 468,82 L 428,82' : 'M 428,82 L 468,82', reverseFlisr ? '#38bdf8' : '#34d399', b.dist_f1_sec2, 0.95)}

        <!-- Gated URD Subdivision Tap & Pad TX (x=362..412, y=97..134) -->
        <path d="M 402,82 L 402,97" fill="none" stroke="${d1Col}" stroke-width="1.4" ${b.dist_f1_sec1 ? '' : 'stroke-dasharray="2,2"'}/>
        <g onclick="selectComponent('urd_vista_swgr', true)" style="cursor:pointer;">
          <rect x="362" y="97" width="52" height="14" rx="2" fill="rgba(30,41,59,0.94)" stroke="#22c55e"/>
          <text x="388" y="106.5" fill="${b.dist_f1_sec1 ? '#6ee7b7' : '#64748b'}" font-size="4.5" text-anchor="middle" font-family="monospace">URD RISER/VISTA</text>
        </g>
        <g onclick="selectComponent('dt_urd_pad', true)" style="cursor:pointer;">
          <rect x="362" y="114" width="52" height="15" rx="2" fill="rgba(30,41,59,0.94)" stroke="#22c55e"/>
          <text x="388" y="124" fill="${b.dist_f1_sec2 ? '#86efac' : '#64748b'}" font-size="4.5" text-anchor="middle" font-family="monospace">URD 150kVA (6x)</text>
        </g>

        <!-- Lateral 100K Fuse -> Residential 50 kVA Transformer -->
        <line x1="444" y1="82" x2="444" y2="41" stroke="${latCol}" stroke-width="1.5" ${b.dist_lateral ? '' : 'stroke-dasharray="2,2"'}/>
        ${flowOverlay('M 444,82 L 444,41', '#fbbf24', b.dist_lateral, 0.8)}
        <g onclick="operateSwitch('fuseCutout')" style="cursor:pointer;">
          <rect x="431" y="54" width="26" height="10" rx="2" fill="${swCol(s.fuseCutout)}" stroke="#fff" stroke-width="0.8"/>
          <text x="444" y="61" fill="#fff" font-size="4.8" text-anchor="middle" font-family="monospace">100K</text>
        </g>
        <g onclick="selectComponent('dt_res_50', true)" style="cursor:pointer;">
          <rect x="418" y="23" width="52" height="18" rx="2.2" fill="rgba(30,41,59,0.94)" stroke="${latCol}"/>
          <text x="444" y="34.5" fill="${b.dist_lateral ? '#fde047' : '#64748b'}" font-size="4.8" text-anchor="middle" font-weight="bold" font-family="monospace">RES 50kVA</text>
        </g>

        <!-- 79-TIE1 North Loop Recloser & Sub B 52-F3 East Corridor (x = 468..576) -->
        <line x1="496" y1="82" x2="576" y2="82" stroke="${f3Col}" stroke-width="2.0" ${b.dist_f3 ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(b.fdr3_from_subA ? 'M 496,82 L 576,82' : 'M 576,82 L 496,82', b.fdr3_from_subA ? '#38bdf8' : '#34d399', b.dist_f3, 0.9)}
        ${tie1FlowSvg}
        <g onclick="operateSwitch('cbTieB')" style="cursor:pointer;">
          <rect x="468" y="75" width="28" height="14" rx="2" fill="${swCol(s.cbTieB)}" stroke="#fff"/>
          <text x="482" y="84.5" fill="#fff" font-size="5.3" text-anchor="middle" font-weight="bold" font-family="monospace">79-TIE1</text>
        </g>
        <line x1="532" y1="82" x2="532" y2="41" stroke="${f3Col}" stroke-width="1.5" ${b.dist_f3 ? '' : 'stroke-dasharray="2,2"'}/>
        ${flowOverlay('M 532,82 L 532,41', b.fdr3_from_subA ? '#38bdf8' : '#fbbf24', b.dist_f3, 0.8)}
        <g onclick="selectComponent('dt_uni_500', true)" style="cursor:pointer;">
          <rect x="496" y="23" width="72" height="18" rx="2.2" fill="rgba(30,41,59,0.94)" stroke="${f3Col}"/>
          <text x="532" y="34.5" fill="${b.dist_f3 ? '#fde68a' : '#64748b'}" font-size="4.8" text-anchor="middle" font-weight="bold" font-family="monospace">EAST UNI 500kVA</text>
        </g>

        <!-- SOUTH LOOP (y = 152): 52-F2 -> 79-F2 -> CAP-F2 -> CBD/HOSP 750kVA -> 89-TIE2 <-> MUN/LOG 1000kVA <-> 52-F4 -->
        <line x1="354" y1="152" x2="468" y2="152" stroke="${d2mCol}" stroke-width="2.0" ${b.dist_f2_main ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(reverseSouthFlisr ? 'M 468,152 L 354,152' : 'M 354,152 L 468,152', reverseSouthFlisr ? '#38bdf8' : '#34d399', b.dist_f2_main, 0.95)}
        <g onclick="operateSwitch('cbF2Rec')" style="cursor:pointer;">
          <rect x="366" y="145" width="26" height="14" rx="2" fill="${swCol(s.cbF2Rec !== false)}" stroke="#fff"/>
          <text x="379" y="154.5" fill="#fff" font-size="5.4" text-anchor="middle" font-weight="bold" font-family="monospace">79-F2</text>
        </g>
        <text x="418" y="167" fill="#67e8f9" font-size="4.6" text-anchor="middle" font-family="monospace">CAP-F2 (900kVAR)</text>
        <line x1="444" y1="152" x2="444" y2="132" stroke="${d2mCol}" stroke-width="1.5" ${b.dist_f2_main ? '' : 'stroke-dasharray="2,2"'}/>
        ${flowOverlay('M 444,152 L 444,132', reverseSouthFlisr ? '#38bdf8' : '#fbbf24', b.dist_f2_main, 0.8)}
        <g onclick="selectComponent('dt_com_750', true)" style="cursor:pointer;">
          <rect x="418" y="114" width="54" height="18" rx="2.2" fill="rgba(30,41,59,0.94)" stroke="${d2mCol}"/>
          <text x="445" y="125.5" fill="${b.dist_f2_main ? '#38bdf8' : '#64748b'}" font-size="4.7" text-anchor="middle" font-weight="bold" font-family="monospace">CBD 750kVA</text>
        </g>

        <line x1="496" y1="152" x2="576" y2="152" stroke="${f4Col}" stroke-width="2.0" ${b.dist_f4 ? '' : 'stroke-dasharray="3,2"'}/>
        ${flowOverlay(b.fdr4_from_subA ? 'M 496,152 L 576,152' : 'M 576,152 L 496,152', b.fdr4_from_subA ? '#38bdf8' : '#34d399', b.dist_f4, 0.9)}
        ${tie2FlowSvg}
        <g onclick="operateSwitch('cbTie2')" style="cursor:pointer;">
          <rect x="468" y="145" width="28" height="14" rx="2" fill="${swCol(s.cbTie2)}" stroke="#fff"/>
          <text x="482" y="154.5" fill="#fff" font-size="5.3" text-anchor="middle" font-weight="bold" font-family="monospace">89-TIE2</text>
        </g>
        <line x1="532" y1="152" x2="532" y2="132" stroke="${f4Col}" stroke-width="1.5" ${b.dist_f4 ? '' : 'stroke-dasharray="2,2"'}/>
        ${flowOverlay('M 532,152 L 532,132', b.fdr4_from_subA ? '#38bdf8' : '#fbbf24', b.dist_f4, 0.8)}
        <g onclick="selectComponent('dt_mun_1000', true)" style="cursor:pointer;">
          <rect x="496" y="114" width="72" height="18" rx="2.2" fill="rgba(30,41,59,0.94)" stroke="${f4Col}"/>
          <text x="532" y="125.5" fill="${b.dist_f4 ? '#7dd3fc' : '#64748b'}" font-size="4.7" text-anchor="middle" font-weight="bold" font-family="monospace">MUN/LOG 1MVA</text>
        </g>

        <g id="sld-sub-b-panel" onclick="setTargetSubstation('B'); selectComponent('substation_b', false);" style="cursor:pointer;">
          <rect x="578" y="18" width="296" height="196" rx="4" fill="rgba(16,185,129,0.06)" stroke="#10b981" stroke-width="1.1"/>
          <text x="726" y="12.5" fill="#34d399" font-size="5.7" text-anchor="middle" font-weight="bold" font-family="monospace">TIE SUB B (${subBTop.toUpperCase()} / ${subBEnc}) — CLICK TO CONFIGURE</text>
          ${subBSvg}
          <text x="726" y="208" fill="#94a3b8" font-size="4.6" text-anchor="middle" font-family="monospace">EAST HV IN → ${subBTop.toUpperCase()} HV BUS → TR-02 → 52-LVB → ${distKv} kV BUS B → 52-F3 &amp; 52-F4</text>
        </g>

        <rect x="362" y="184" width="212" height="27" rx="3" fill="rgba(2,6,23,0.88)" stroke="${anyBackfeed ? '#38bdf8' : 'rgba(56,189,248,0.35)'}"/>
        <text x="468" y="195" fill="${anyBackfeed ? '#67e8f9' : '#94a3b8'}" font-size="4.8" text-anchor="middle" font-weight="bold" font-family="monospace">${b.loopModeBanner || 'MODE: NORMAL RADIAL (TIES OPEN)'}</text>
        <text x="468" y="205.5" fill="#cbd5e1" font-size="4.6" text-anchor="middle" font-family="monospace">F1:${b.dist_f1_sec2?'ON':'OFF'} F2:${b.dist_f2_main?'ON':'OFF'} F3:${b.dist_f3?'ON':'OFF'} F4:${b.dist_f4?'ON':'OFF'} | IND:${b.ind_hv?'LIVE':'OFF'}</text>
      `;

      const baseSvgInner = `${primarySvg}${secondarySvg}${distSvg}${hotspotsSvg}${activeFaultSvg}`;
      if (container) {
        container.innerHTML = `<svg viewBox="-52 -12 984 272" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">${baseSvgInner}</svg>`;
      }

      if (expContainer) {
        const expZ = AppState.sldZoom || 1.0;
        const expTx = (AppState.sldPanX || 0) + 440 * (1 - expZ);
        const expTy = (AppState.sldPanY || 0) + 124 * (1 - expZ);
        const expOverlay = pf ? `
          <rect x="-24" y="229" width="446" height="17" rx="2.5" fill="rgba(2,6,23,0.90)" stroke="rgba(56,189,248,0.38)" stroke-width="0.6"/>
          <text x="-16" y="240" fill="#38bdf8" font-size="5.6" font-family="monospace">SUB A: ${vs.cascadeLabel || (vs.hvKv + ' kV')} | ${pf.iHvA.toFixed(1)} A | ${pf.sSubAMva.toFixed(2)} MVA | IND(${indKv}kV): ${pf.iIndA.toFixed(0)} A | ${top.toUpperCase()}</text>
          <rect x="432" y="229" width="470" height="17" rx="2.5" fill="rgba(2,6,23,0.90)" stroke="rgba(245,158,11,0.38)" stroke-width="0.6"/>
          <text x="440" y="240" fill="#fbbf24" font-size="5.6" font-family="monospace">CITY ${distKv} kV (${pf.vDistKvActual.toFixed(2)} kV, ${pf.vDistPu.toFixed(3)}pu) | F1–F4: ${pf.iF1A.toFixed(0)}/${pf.iF2A.toFixed(0)}/${pf.iF3A.toFixed(0)}/${pf.iF4A.toFixed(0)}A | SUB B: ${pf.sSubBMva.toFixed(2)} MVA (${subBTop.toUpperCase()})</text>
        ` : '';
        expContainer.innerHTML = `
          <svg viewBox="-52 -12 984 272" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
            <g id="sld-exp-panzoom-group" transform="translate(${expTx.toFixed(1)}, ${expTy.toFixed(1)}) scale(${expZ.toFixed(2)})">
              ${baseSvgInner}
              ${expOverlay}
            </g>
          </svg>
        `;
      }

      const expFooter = document.getElementById('sld-expanded-footer');
      if (expFooter && pf) {
        const faultStr = faultNode && PINPOINT_FAULT_NODES[faultNode] ? `<strong style="color:#f87171;">⚡ ACTIVE FAULT: ${PINPOINT_FAULT_NODES[faultNode].name}</strong>` : '<span style="color:#10b981;">● System Steady-State</span>';
        expFooter.innerHTML = `
          <span>Sub A / Sub B: <strong style="color:#38bdf8;">${top.toUpperCase()} (${AppState.enclosureType.toUpperCase()}) ⇄ ${subBTop.toUpperCase()} (${subBEnc})</strong></span>
          <span>Cascade: <strong>${vs.cascadeLabel || (vs.hvKv + '/' + distKv + ' kV')}</strong> (${pf.vDistPu.toFixed(3)} pu)</span>
          <span>Flow: <strong>${pf.pLoadMw.toFixed(1)} MW / ${pf.qNetMvar.toFixed(1)} MVAR</strong> (IND ${pf.indKv}kV)</span>
          <span>${faultStr}</span>
        `;
      }

      const activeCb = (top === 'ring') ? s.cb1 : (top === 'breakerhalf' ? s.cbTIE : s.cbMain);
      const activeDs = (top === 'ring') ? s.ds1A : (top === 'breakerhalf' ? s.dsA1 : s.dsMain);
      const btnCB = document.getElementById('btn-sld-breaker');
      if (btnCB) {
        btnCB.innerText = `CB: ${activeCb ? 'CLOSED (52)' : 'OPEN'}`;
        btnCB.style.background = activeCb ? 'rgba(239, 68, 68, 0.3)' : 'rgba(16, 185, 129, 0.3)';
      }

      const btnDS = document.getElementById('btn-sld-disconnect');
      if (btnDS) {
        btnDS.innerText = `DISC: ${activeDs ? 'CLOSED (89)' : 'OPEN'}`;
        btnDS.style.background = activeDs ? 'rgba(239, 68, 68, 0.3)' : 'rgba(16, 185, 129, 0.3)';
      }
    }

    function getInspectorQuickMeta(compKey) {
      const pqMap = {
        dt_ind_1500: 'ind_sub', ind_corridor_pole: 'ind_sub',
        dt_com_750: 'cbd_bus', sub_com: 'cbd_bus',
        dt_urd_pad: 'urd_pad', urd_riser_pole: 'urd_pad', urd_vista_swgr: 'urd_pad',
        dt_res_50: 'res_50', dist_pole_p1: 'res_50', dist_pole_p2: 'res_50', dist_pole_p3: 'res_50', dist_pole_p4: 'res_50', fuseCutout: 'res_50', recloser_acr1: 'res_50',
        transformer: 'tr01_pri_delta', tx_hvbushing: 'tr01_pri_delta', tx_lvbushing: 'tr01_pri_delta', ngr_resistor: 'tr01_pri_delta',
        substation_b: 'bus_b_138', sub_b: 'bus_b_138', dt_uni_500: 'bus_b_138', dt_mun_1000: 'bus_b_138'
      };
      const faultMap = {
        incoming_gantry: 'node1_incoming', surge_arrester: 'node1_incoming', ctvt_unit: 'node1_incoming',
        main_busbar: 'node2_hv_bus', breaker_52: 'node2_hv_bus', disconnect_89: 'node2_hv_bus',
        transformer: 'node3_tx_hv', tx_hvbushing: 'node3_tx_hv',
        tx_lvbushing: 'node4_tx_lv', ngr_resistor: 'node4_tx_lv',
        sec_bus: 'node5_lv_bus', sec_breaker: 'node5_lv_bus', cap_bank: 'node5_lv_bus', sst_100: 'node5_lv_bus',
        dt_ind_1500: 'node8_ind_sub', ind_corridor_pole: 'node7_ind_hv',
        recloser_acr1: 'node9_acr1', dist_pole_p1: 'node6_fdr1', dist_pole_p2: 'node9_acr1', dist_pole_p3: 'node10_res_lat', dist_pole_p4: 'node12_cbd_bus',
        dt_res_50: 'node10_res_lat', fuseCutout: 'node10_res_lat',
        dt_urd_pad: 'node11_urd_pad', urd_riser_pole: 'node11_urd_pad', urd_vista_swgr: 'node11_urd_pad',
        dt_com_750: 'node12_cbd_bus', sub_com: 'node12_cbd_bus',
        recloser_tie1: 'node13_tie1', recloser_tie2: 'node14_tie2',
        dt_uni_500: 'node15_uni_bus', dt_mun_1000: 'node16_mun_bus',
        substation_b: 'node17_subb_hv', sub_b: 'node17_subb_hv'
      };
      const sliderMap = {
        transformer: { key: 'txMvaOverride', label: 'TR-01 Rating (MVA)', min: 10, max: 300, step: 5, unit: 'MVA' },
        substation_b: { key: 'subBTxMva', label: 'TR-02 Tie Rating (MVA)', min: 5, max: 100, step: 2.5, unit: 'MVA' },
        sub_b: { key: 'subBTxMva', label: 'TR-02 Tie Rating (MVA)', min: 5, max: 100, step: 2.5, unit: 'MVA' },
        dt_res_50: { key: 'resKva', label: 'RES Demand (kVA)', min: 25, max: 5000, step: 25, unit: 'kVA' },
        dt_urd_pad: { key: 'urdKva', label: 'URD Subdivision (kVA)', min: 150, max: 15000, step: 150, unit: 'kVA' },
        dt_com_750: { key: 'cbdKva', label: 'CBD Hospital/Tower (kVA)', min: 250, max: 25000, step: 250, unit: 'kVA' },
        dt_uni_500: { key: 'uniKva', label: 'East University (kVA)', min: 100, max: 15000, step: 100, unit: 'kVA' },
        dt_mun_1000: { key: 'munKva', label: 'Municipal Water/Log (kVA)', min: 250, max: 20000, step: 250, unit: 'kVA' },
        dt_ind_1500: { key: 'indMva', label: 'Industrial Plant (MVA)', min: 5, max: 80, step: 2.5, unit: 'MVA' }
      };
      return {
        pqNode: pqMap[compKey] || 'bus_a_138',
        faultNode: faultMap[compKey] || 'node5_lv_bus',
        slider: sliderMap[compKey] || null
      };
    }

    // TELEMETRY DRAWER RENDERING
    function renderTelemetryDrawer(compKey) {
      const data = SUBSTATION_DATA[compKey];
      if (!data) return;

      document.getElementById('drawer-comp-name').innerText = data.name;
      const body = document.getElementById('drawer-content-body');
      body.innerHTML = '';

      const qMeta = getInspectorQuickMeta(compKey);
      const ms = AppState.mvaScaling || {};
      const vsNow = getVoltageSpec(AppState.voltageClass);
      const qBar = document.createElement('div');
      qBar.style.cssText = 'display:flex;flex-direction:column;gap:6px;margin-bottom:10px;padding:8px;background:rgba(15,23,42,0.88);border:1px solid rgba(56,189,248,0.28);border-radius:7px;';
      const curVal = qMeta.slider ? (qMeta.slider.key === 'txMvaOverride' ? (ms.txMvaOverride ?? vsNow.mva) : (ms[qMeta.slider.key] ?? qMeta.slider.min)) : null;
      qBar.innerHTML = `
        <div style="display:flex;gap:5px;flex-wrap:wrap;">
          <button onclick="attachPqProbeToNode('${qMeta.pqNode}')" style="flex:1;min-width:120px;padding:5px 7px;background:rgba(6,182,212,0.16);border:1px solid rgba(6,182,212,0.5);color:#67e8f9;border-radius:5px;font-size:10.2px;font-weight:700;cursor:pointer;">🔬 Attach PQ Oscilloscope Probe</button>
          <button onclick="triggerPinpointedFault('${qMeta.faultNode}', 50, null)" style="padding:5px 7px;background:rgba(244,63,94,0.16);border:1px solid rgba(244,63,94,0.5);color:#fda4af;border-radius:5px;font-size:10.2px;font-weight:700;cursor:pointer;">🎯 Inject Fault</button>
          <button onclick="plotActiveFaultOnTcc('${qMeta.faultNode}')" style="padding:5px 7px;background:rgba(245,158,11,0.16);border:1px solid rgba(245,158,11,0.5);color:#fde68a;border-radius:5px;font-size:10.2px;font-weight:700;cursor:pointer;">📈 Plot TCC</button>
        </div>
        ${qMeta.slider ? `
          <div style="display:flex;flex-direction:column;gap:3px;padding-top:4px;border-top:1px solid rgba(148,163,184,0.16);">
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#cbd5e1;">
              <span>🎛️ ${qMeta.slider.label}</span>
              <strong style="color:#fbbf24;font-family:monospace;">${curVal} ${qMeta.slider.unit} (${(ms.mode||'autosize').toUpperCase()})</strong>
            </div>
            <input type="range" min="${qMeta.slider.min}" max="${qMeta.slider.max}" step="${qMeta.slider.step}" value="${curVal}" oninput="updateMvaScalingControl('${qMeta.slider.key}', this.value)" style="width:100%;accent-color:#f59e0b;cursor:pointer;">
          </div>
        ` : ''}
      `;
      body.appendChild(qBar);

      if (AppState.currentDrawerTab === 'specs') {
        const grp = document.createElement('div');
        grp.className = 'spec-group';
        grp.innerHTML = `
          <div class="spec-group-title">
            <span>Engineering Ratings & Nameplate</span>
            <span style="font-size: 9px; color: var(--accent-gold);">${data.governingStandard}</span>
          </div>
        `;
        data.specs.forEach(s => {
          const row = document.createElement('div');
          row.className = 'spec-row';
          row.innerHTML = `<span class="k">${s.k}</span><span class="v">${s.v}</span>`;
          grp.appendChild(row);
        });
        body.appendChild(grp);
      } else if (AppState.currentDrawerTab === 'calc') {
        const calc = (typeof SIZING_CALCS !== 'undefined' && SIZING_CALCS[compKey]) ? SIZING_CALCS[compKey] : null;
        const grp = document.createElement('div');
        grp.className = 'spec-group';
        grp.innerHTML = `
          <div class="spec-group-title">Normal & Fault Operating Principle</div>
          <p style="font-size: 11px; color: #cbd5e1; line-height: 1.5; margin-bottom: 8px;">${data.overview}</p>
          ${calc ? `
            <div class="calc-step-box" style="margin-bottom:6px; border-left-color:#38bdf8;">
              <strong style="color:#7dd3fc;">Normal Duty:</strong> ${calc.dutyNormal}<br>
              <strong style="color:#fca5a5;">Fault / Surge Duty:</strong> ${calc.dutyFault}
            </div>
            <div class="spec-group-title" style="margin-top:8px;">Engineering Sizing Calculation &amp; Proof</div>
            <div style="display:flex; flex-direction:column; gap:5px;">
              ${calc.steps.map(st => `<div class="calc-step-box">${st}</div>`).join('')}
            </div>
          ` : ''}
        `;
        body.appendChild(grp);
      } else if (AppState.currentDrawerTab === 'failures') {
        data.failureModes.forEach(fm => {
          const card = document.createElement('div');
          card.className = 'spec-group';
          card.innerHTML = `
            <div class="spec-group-title" style="color: #fca5a5;">⚠ ${fm.title}</div>
            <p style="font-size: 11px; color: #cbd5e1; line-height: 1.5;">${fm.desc}</p>
          `;
          body.appendChild(card);
        });
      } else if (AppState.currentDrawerTab === 'checklist') {
        const grp = document.createElement('div');
        grp.className = 'spec-group';
        grp.innerHTML = `<div class="spec-group-title">Field Inspection & O&M Checklist</div>`;
        data.checklist.forEach((item, i) => {
          const row = document.createElement('div');
          row.style.fontSize = '11px';
          row.style.lineHeight = '1.5';
          row.style.padding = '6px 0';
          row.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
          row.innerHTML = `<strong>${i + 1}.</strong> ${item}`;
          grp.appendChild(row);
        });
        body.appendChild(grp);
      } else if (AppState.currentDrawerTab === 'standards') {
        const grp = document.createElement('div');
        grp.className = 'spec-group';
        grp.innerHTML = `
          <div class="spec-group-title">Engineering Codes &amp; Design Standards Mapping</div>
          <p style="font-size: 11.5px; color: #cbd5e1; line-height: 1.6; margin-bottom: 8px;">
            <strong>Design Domain:</strong> High-Voltage Substation Layouts &amp; Apparatus Sizing<br>
            <strong>Simulation Scope:</strong> Steady-State Power Flow, Short-Circuit, Protection Coordination &amp; Field Walkdown<br>
            <strong>Governing Code:</strong> ${data.governingStandard}
          </p>
          <p style="font-size: 11px; color: #94a3b8; line-height: 1.5;">
            Aligned with IEEE C37 / C57, IEEE Std 80 / 998, IEC 61850, and NESC utility engineering practices (CDIO Framework).
          </p>
        `;
        body.appendChild(grp);
      }
    }

    function setDrawerTab(tab) {
      AppState.currentDrawerTab = tab;
      document.querySelectorAll('.drawer-tab').forEach(t => {
        const oc = t.getAttribute('onclick') || '';
        t.classList.toggle('active', oc.includes(`'${tab}'`));
      });
      renderTelemetryDrawer(AppState.selectedComponent);
    }

    function toggleTelemetryDrawer() {
      const drawer = document.getElementById('telemetry-drawer');
      const reopenBtn = document.getElementById('btn-reopen-drawer');
      drawer.classList.toggle('collapsed');
      if (drawer.classList.contains('collapsed')) {
        reopenBtn.style.display = 'inline-flex';
      } else {
        reopenBtn.style.display = 'none';
      }
    }

    // DYNAMIC MVA EQUIPMENT SIZING, PER-UNIT BIDIRECTIONAL POWER FLOW & 23-NODE SHORT-CIRCUIT ENGINE
    function computeDynamicEquipmentSizing(vSpec, txMva, totalLoadMva, subBMva, mode) {
      const baseTxMva = Math.max(5, Number(txMva) || vSpec.mva || 50);
      const hvKv = vSpec.hvKv || 69.0;
      const lvKv = vSpec.distKv || vSpec.lvKv || 13.8;
      const effectiveMode = (mode === 'stress') ? 'stress' : 'autosize';
      const sizingMva = effectiveMode === 'autosize' ? Math.max(baseTxMva, totalLoadMva * 1.05) : (vSpec.mva || baseTxMva);

      const iHvFl = (baseTxMva * 1000) / (Math.sqrt(3) * hvKv);
      const iLvFl = (baseTxMva * 1000) / (Math.sqrt(3) * lvKv);
      const refIHv = (sizingMva * 1000) / (Math.sqrt(3) * hvKv);
      const refILv = (sizingMva * 1000) / (Math.sqrt(3) * lvKv);
      const iLoadLv = (Math.max(0.05, totalLoadMva) * 1000) / (Math.sqrt(3) * lvKv);

      const stdFrames = [600, 1200, 2000, 3000, 4000];
      const pickFrame = (amps) => stdFrames.find(a => a >= amps * 1.25) || 4000;
      const stdCts = [400, 600, 800, 1200, 1500, 2000, 3000, 4000];
      const pickCt = (amps) => stdCts.find(c => c >= amps * 1.25) || 4000;

      const brkHvAmp = pickFrame(refIHv);
      const brkLvAmp = pickFrame(refILv);
      const brkKa = sizingMva >= 100 ? Math.max(40, vSpec.lvCbKa || 40) : (sizingMva >= 60 ? 31.5 : 25.0);
      const ctHvPri = pickCt(refIHv);
      const ctLvPri = pickCt(refILv);
      const fdrCtPri = pickCt(Math.max(250, refILv * 0.48));

      const busbarSpec = brkLvAmp >= 3000
        ? 'Dual 127×10 mm Al 6101-T61 (3000 A)'
        : (brkLvAmp >= 2000 ? '100 mm IPS Sch 80 Al Pipe (2000 A)' : (brkLvAmp >= 1200 ? '75 mm IPS Sch 40 Al Pipe (1200 A)' : '63 mm IPS Al Pipe (800 A)'));

      const txLoadPct = (totalLoadMva / Math.max(1, baseTxMva)) * 100;
      const loadRatio = totalLoadMva / Math.max(1, baseTxMva);
      const thetaAmb = 30.0;
      const topOilRise = 45.0 * Math.pow((loadRatio * loadRatio * 5.5 + 1.0) / 6.5, 0.8);
      const hotSpotRise = 23.0 * Math.pow(loadRatio, 1.6);
      const thermalTopOilC = +(thetaAmb + topOilRise).toFixed(1);
      const thermalHotSpotC = +(thetaAmb + topOilRise + hotSpotRise).toFixed(1);

      const lvBusDropWarning = effectiveMode === 'stress' && txLoadPct > 105;
      const ctSatWarning = effectiveMode === 'stress' && (iLoadLv > ctLvPri * 1.15);
      const relay51Alert = effectiveMode === 'stress' && txLoadPct > 110;
      const hotSpotAlarm = thermalHotSpotC > 110.0;

      const overloadBadge = (effectiveMode === 'stress' && (txLoadPct > 100 || hotSpotAlarm))
        ? `🚨 OVERLOAD ${txLoadPct.toFixed(0)}% · ΘH ${thermalHotSpotC}°C > 110°C${relay51Alert ? ' · ANSI 49/51 TRIP' : ''}`
        : (effectiveMode === 'autosize'
          ? `✅ AUTO-SIZED (${sizingMva.toFixed(0)} MVA · ${brkLvAmp}A VCB · ${brkKa}kA · CT ${ctLvPri}:5)`
          : `🟢 NORMAL (${txLoadPct.toFixed(0)}% Load · ΘH ${thermalHotSpotC}°C)`);

      const baseScaleRatio = +Math.max(0.68, Math.min(1.65, Math.pow(sizingMva / Math.max(1, vSpec.mva || 50), 0.25))).toFixed(3);
      return {
        mode: effectiveMode, txMva: baseTxMva, sizingMva, subBMva: Math.max(5, Number(subBMva) || 15),
        iHvFl, iLvFl, iLoadLv, brkHvAmp, brkLvAmp, brkKa, ctHvPri, ctLvPri, fdrCtPri, busbarSpec,
        thermalTopOilC, thermalHotSpotC, txLoadPct,
        lvBusDropWarning, ctSatWarning, relay51Alert, hotSpotAlarm, overloadBadge, baseScaleRatio
      };
    }

    function computePowerFlowMetrics() {
      const vs = getVoltageSpec(AppState.voltageClass);
      const b = computeEnergizedBranches();
      const s = AppState.switchStates;
      const ms = AppState.mvaScaling || {};
      const activeTxMva = Math.max(5, Number(ms.txMvaOverride != null ? ms.txMvaOverride : vs.mva) || vs.mva);
      const subBRatedMva = Math.max(5, Number(ms.subBTxMva != null ? ms.subBTxMva : 15) || 15);
      const baseMva = activeTxMva;
      const distKv = vs.distKv || 13.8;
      const indKv = vs.indSubKv || 69.0;
      const loadFrac = Math.max(0.05, (AppState.pfLoadPct || 100) / 100);
      const trunkRatio = Math.max(0.5, vs.mva / 50.0);

      // 6 Individual Named Utility Load Districts + Feeder Trunk Background (gated by active BFS branch)
      const resKva = b.dist_lateral ? Number(ms.resKva != null ? ms.resKva : 50) * loadFrac : 0.0;
      const urdKva = (b.dist_f1_sec1 || b.dist_f1_sec2) ? Number(ms.urdKva != null ? ms.urdKva : 900) * loadFrac : 0.0;
      const f1TrunkBgMva = b.dist_f1_sec2 ? (11.5 * trunkRatio * loadFrac) : 0.0;
      const f1ZoneMva = (resKva + urdKva) / 1000.0 + f1TrunkBgMva;

      const cbdKva = b.dist_f2_main ? Number(ms.cbdKva != null ? ms.cbdKva : 750) * loadFrac : 0.0;
      const f2TrunkBgMva = b.dist_f2_main ? (13.8 * trunkRatio * loadFrac) : 0.0;
      const f2ZoneMva = cbdKva / 1000.0 + f2TrunkBgMva;

      const uniKva = b.dist_f3 ? Number(ms.uniKva != null ? ms.uniKva : 500) * loadFrac : 0.0;
      const f3TrunkBgMva = b.dist_f3 ? (4.2 * loadFrac) : 0.0;
      const f3ZoneMva = uniKva / 1000.0 + f3TrunkBgMva;

      const munKva = b.dist_f4 ? Number(ms.munKva != null ? ms.munKva : 1000) * loadFrac : 0.0;
      const f4TrunkBgMva = b.dist_f4 ? (4.8 * loadFrac) : 0.0;
      const f4ZoneMva = munKva / 1000.0 + f4TrunkBgMva;

      const indMva = (b.txFeed && b.ind_hv) ? Number(ms.indMva != null ? ms.indMva : (vs.indCustMva || 25.0)) * loadFrac : 0.0;

      // Bidirectional Summation onto Active Substation (Sub A vs Sub B) across 79-TIE1 and 89-TIE2
      const hasReachA = (node) => b.reachA ? (Array.isArray(b.reachA) ? b.reachA.includes(node) : b.reachA.has(node)) : false;
      const f1ServedByA = hasReachA('fdr1_head') || (!b.fdr1_from_subB && b.secMain);
      const f2ServedByA = hasReachA('fdr2_head') || (!b.fdr2_from_subB && b.secMain);
      const subALocalCityMva = (f1ServedByA ? f1ZoneMva : 0) + (f2ServedByA ? f2ZoneMva : 0);
      const subATransferMva = (b.fdr3_from_subA ? f3ZoneMva : 0) + (b.fdr4_from_subA ? f4ZoneMva : 0);
      const subBLocalCityMva = (!b.fdr3_from_subA ? f3ZoneMva : 0) + (!b.fdr4_from_subA ? f4ZoneMva : 0);
      const subBTransferMva = (b.fdr1_from_subB ? f1ZoneMva : 0) + (b.fdr2_from_subB ? f2ZoneMva : 0);

      const sLoadMva = (b.txFeed && b.secMain) ? (subALocalCityMva + subATransferMva + 0.1) : (b.txFeed ? 0.1 : 0.0);
      const sSubBMva = b.dist_sub_b ? (subBLocalCityMva + subBTransferMva) : 0.0;
      const sSubAMva = sLoadMva;

      const pfLoad = Math.min(0.999, Math.max(0.5, AppState.pfPowerFactor || 0.92));
      const pLoadMw = sLoadMva * pfLoad;
      const qLoadMvar = sLoadMva * Math.sqrt(Math.max(0, 1 - pfLoad * pfLoad));
      const capOn = !!(b.secMain && s.dsCapA && s.cbCap && s.dsCapB);
      const qCapMvar = capOn ? vs.capMvar : 0.0;
      const qNetMvar = qLoadMvar - qCapMvar;
      const sNetMva = Math.hypot(pLoadMw, qNetMvar);
      const pfNet = sNetMva > 1e-4 ? Math.min(1.0, pLoadMw / sNetMva) : 1.0;

      const sizing = computeDynamicEquipmentSizing(vs, activeTxMva, Math.max(sLoadMva, sNetMva), subBRatedMva, ms.mode || 'autosize');
      if (sizing.mode === 'autosize' && typeof window.scale3DTransformerToMva === 'function') {
        window.scale3DTransformerToMva(sizing.sizingMva, subBRatedMva);
      } else if (typeof window.scale3DTransformerToMva === 'function') {
        window.scale3DTransformerToMva(activeTxMva, subBRatedMva);
      }

      const tapPu = 1.0 + ((AppState.oltcTapPct || 0) / 100.0);
      const vHvPu = b.incoming ? 1.00 : 0.0;
      const pPu = pLoadMw / baseMva;
      const qPu = qNetMvar / baseMva;
      const extraLoopImpedanceFactor = (b.fdr3_from_subA || b.fdr4_from_subA) ? 0.018 * (subATransferMva / Math.max(5, baseMva)) * 3.0 : 0.0;
      const deltaVPu = b.txFeed ? (pPu * vs.rPu + qPu * (vs.totalCascadeXPu || vs.xPu) + extraLoopImpedanceFactor) : 0.0;
      const vNoLoadPu = b.txFeed ? (vHvPu * tapPu) : 0.0;
      const vLvPu = b.txFeed ? Math.max(0.65, Math.min(1.18, vNoLoadPu - deltaVPu)) : 0.0;

      // Also support West 13.8 kV Bus A voltage when Sub B back-feeds it with Sub A HV open
      const backfedDrop = (b.subA_lv_backfed_from_B && !b.txFeed) ? Math.min(0.18, 0.028 * (sSubBMva / Math.max(5, subBRatedMva))) : 0.0;
      const vDistPu = b.secMain ? vLvPu : (b.subA_lv_backfed_from_B ? Math.max(0.75, 1.0 - backfedDrop) : 0.0);

      const vHvKvActual = vs.hvKv * vHvPu;
      const vLvKvActual = vs.lvKv * vLvPu;
      const vDistKvActual = distKv * vDistPu;
      const vrPct = (vLvPu > 0.01) ? (((vNoLoadPu - vLvPu) / vLvPu) * 100.0) : (backfedDrop * 100.0);

      const iPu = sNetMva / baseMva;
      const pCuKw = b.txFeed ? (vs.pCuFullKw * (activeTxMva / vs.mva) * iPu * iPu) : 0.0;
      const pCoreKw = b.txFeed ? (vs.pCoreKw * (activeTxMva / vs.mva)) : 0.0;
      const pLossKw = pCoreKw + pCuKw;
      const etaPct = (pLoadMw > 0.01 && b.txFeed) ? (((pLoadMw * 1000) / (pLoadMw * 1000 + pLossKw)) * 100.0) : 0.0;

      const iHvA = b.txFeed ? (((sNetMva + indMva) * 1000) / (Math.sqrt(3) * vs.hvKv * Math.max(0.5, vHvPu))) : 0.0;
      const iLvA = (b.txFeed && b.secMain) ? ((sNetMva * 1000) / (Math.sqrt(3) * vs.lvKv * Math.max(0.5, vLvPu))) : 0.0;
      const iDistBaseScale = 1000 / (Math.sqrt(3) * distKv * Math.max(0.5, vDistPu || 1.0));

      // Actual carried MVA per feeder head (including cross-tie transfers!)
      const f1CarriedMva = (b.fdr1 ? f1ZoneMva : 0) + (b.fdr3_from_subA ? f3ZoneMva : 0);
      const f2CarriedMva = (b.fdr2 ? f2ZoneMva : 0) + (b.fdr4_from_subA ? f4ZoneMva : 0);
      const f3CarriedMva = (b.dist_f3 && !b.fdr3_from_subA) ? (f3ZoneMva + (b.fdr1_from_subB ? f1ZoneMva : 0)) : (b.fdr3_from_subA && b.subB_lv_backfed_from_A ? f3ZoneMva : 0);
      const f4CarriedMva = (b.dist_f4 && !b.fdr4_from_subA) ? (f4ZoneMva + (b.fdr2_from_subB ? f2ZoneMva : 0)) : (b.fdr4_from_subA && b.subB_lv_backfed_from_A ? f4ZoneMva : 0);

      const iF1A = f1CarriedMva * iDistBaseScale;
      const iF2A = f2CarriedMva * iDistBaseScale;
      const iF3A = f3CarriedMva * iDistBaseScale;
      const iF4A = f4CarriedMva * iDistBaseScale;
      const iIndA = (b.txFeed && b.ind_hv) ? ((indMva * 1000) / (Math.sqrt(3) * indKv * Math.max(0.5, vHvPu))) : 0.0;
      const loopDropPct = +((extraLoopImpedanceFactor + backfedDrop) * 100).toFixed(2);

      return {
        vs, b, baseMva, activeTxMva, subBRatedMva, distKv, indKv, loadPct: AppState.pfLoadPct, pfLoad, pfNet, capOn, qCapMvar,
        sLoadMva, sSubAMva, indMva, sSubBMva, subATransferMva, subBTransferMva, loopDropPct,
        f1CarriedMva, f2CarriedMva, f3CarriedMva, f4CarriedMva,
        pLoadMw, qLoadMvar, qNetMvar, sNetMva,
        tapPct: AppState.oltcTapPct, tapPu, deltaVPu, vNoLoadPu,
        vHvPu, vLvPu, vDistPu, vHvKvActual, vLvKvActual, vDistKvActual, vrPct,
        pCuKw, pCoreKw, pLossKw, etaPct, iHvA, iLvA, iF1A, iF2A, iF3A, iF4A, iIndA,
        sizing,
        loadBreakdown: { resKva, urdKva, cbdKva, uniKva, munKva, indMva, f1ZoneMva, f2ZoneMva, f3ZoneMva, f4ZoneMva },
        pfLeadLag: qNetMvar >= 0 ? 'lag' : 'lead'
      };
    }

    function computeShortCircuitMetrics() {
      const vs = getVoltageSpec(AppState.voltageClass);
      const b = computeEnergizedBranches();
      const ms = AppState.mvaScaling || {};
      const activeTxMva = Math.max(5, Number(ms.txMvaOverride != null ? ms.txMvaOverride : vs.mva) || vs.mva);
      const subBRatedMva = Math.max(5, Number(ms.subBTxMva != null ? ms.subBTxMva : 15) || 15);
      const distKv = vs.distKv || 13.8;
      const indKv = vs.indSubKv || 69.0;
      const loc = AppState.scFaultLoc || 'node5_lv_bus';
      const ftype = AppState.scFaultType || '3ph';
      const ngrOn = !!AppState.scNgrGrounded;

      const meta = PINPOINT_FAULT_NODES[loc] || null;
      const sizing = computeDynamicEquipmentSizing(vs, activeTxMva, activeTxMva, subBRatedMva, ms.mode || 'autosize');
      const txImpScale = vs.mva / activeTxMva;
      let baseMva = activeTxMva;
      let vBaseKv = distKv;
      let cbRatingKa = sizing.mode === 'autosize' ? sizing.brkKa : 31.5;
      let z1 = vs.z1SysPu;
      let z2 = vs.z1SysPu;
      let z0 = vs.z0SysPu;
      let xrRatio = (meta && meta.xrRatio) ? meta.xrRatio : 11.2;
      let locLabel = (meta && meta.name) ? meta.name : `${distKv} kV Public Distribution Main Bus`;

      const pctDist = Math.max(5, Math.min(100, AppState.pinpointFeederDistPct || (meta && meta.defaultDistPct) || 50));
      const fracDist = pctDist / 100;

      if (loc === 'node1_incoming') {
        vBaseKv = vs.hvKv; cbRatingKa = vs.hvCbKa; xrRatio = 16.0;
        z1 = vs.z1SysPu * 0.92; z2 = z1; z0 = vs.z0SysPu * 0.92;
      } else if (loc === 'node_cascade_mid') {
        vBaseKv = vs.stageKvs && vs.stageKvs.length > 2 ? vs.stageKvs[1] : vs.hvKv;
        cbRatingKa = vs.hvCbKa; xrRatio = 15.0;
        z1 = vs.z1SysPu + 0.42 * vs.xPu * txImpScale; z2 = z1; z0 = vs.z0SysPu + 0.35 * vs.z0TxPu * txImpScale;
      } else if (loc === 'hv_bus' || loc === 'node2_hv_bus') {
        vBaseKv = vs.hvKv; cbRatingKa = vs.hvCbKa; xrRatio = 14.5;
        z1 = vs.z1SysPu; z2 = z1; z0 = vs.z0SysPu;
      } else if (loc === 'node3_tx_hv') {
        vBaseKv = vs.hvKv; cbRatingKa = vs.hvCbKa; xrRatio = 14.0;
        z1 = vs.z1SysPu + 0.08 * vs.xPu * txImpScale; z2 = z1; z0 = vs.z0SysPu + 0.08 * vs.z0TxPu * txImpScale;
      } else if (loc === 'node7_ind_hv' || loc === 'node8_ind_sub') {
        vBaseKv = indKv; cbRatingKa = indKv >= 138 ? 40.0 : 31.5; baseMva = 100.0;
        const pctInd = loc === 'node8_ind_sub' ? 100 : pctDist;
        const fInd = pctInd / 100;
        const zBaseInd = (vBaseKv * vBaseKv) / baseMva;
        const zStageUp = (indKv >= vs.hvKv) ? 0.0 : 0.08;
        const subXfmZ = (loc === 'node8_ind_sub') ? (0.095 * (100 / Math.max(5, Number(ms.indMva || 25)))) : 0.0;
        z1 = vs.z1SysPu + zStageUp + fInd * (1.85 / zBaseInd) + subXfmZ;
        z2 = z1;
        z0 = vs.z0SysPu + zStageUp + fInd * (4.60 / zBaseInd) + subXfmZ;
        xrRatio = loc === 'node8_ind_sub' ? 7.8 : 9.5;
        locLabel = `${meta.name} (${pctInd}%)`;
      } else if (loc === 'node4_tx_lv') {
        vBaseKv = vs.lvKv; cbRatingKa = sizing.mode === 'autosize' ? sizing.brkKa : vs.lvCbKa; xrRatio = 12.0;
        const zBaseOhms = (vBaseKv * vBaseKv) / baseMva;
        const rNgrPu = vs.ngrOhms / zBaseOhms;
        const threeZn = ngrOn ? (3 * rNgrPu) : 1e6;
        z1 = vs.z1SysPu + 0.95 * vs.xPu * txImpScale; z2 = z1; z0 = 0.95 * vs.z0TxPu * txImpScale + threeZn;
      } else if (loc === 'node17_subb_hv' || loc === 'node18_tr02' || loc === 'node19_subb_lv' || loc === 'node20_fdr3' || loc === 'node21_fdr4') {
        baseMva = subBRatedMva;
        if (loc === 'node17_subb_hv') {
          vBaseKv = vs.hvKv; cbRatingKa = vs.hvCbKa; xrRatio = 13.5;
          z1 = vs.z1SysPu * 1.15; z2 = z1; z0 = vs.z0SysPu * 1.15;
        } else {
          vBaseKv = distKv; cbRatingKa = 25.0;
          const zBaseB = (vBaseKv * vBaseKv) / baseMva;
          const threeZnB = ngrOn ? (3 * (10.0 / zBaseB)) : 1e6;
          const xTr02Pu = 0.075 * (15.0 / subBRatedMva);
          const extraKm = (loc === 'node20_fdr3' || loc === 'node21_fdr4') ? (0.45 * fracDist) : 0.0;
          const bfPenalty = ((loc === 'node20_fdr3' && b.fdr3_from_subA) || (loc === 'node21_fdr4' && b.fdr4_from_subA)) ? (1.15 / zBaseB) : 0.0;
          z1 = vs.z1SysPu + xTr02Pu + (extraKm * 0.78) / zBaseB + bfPenalty;
          z2 = z1;
          z0 = xTr02Pu + threeZnB + (extraKm * 2.20) / zBaseB + bfPenalty * 2.2;
          xrRatio = loc === 'node18_tr02' ? 11.5 : (loc === 'node19_subb_lv' ? 10.2 : 6.1);
        }
      } else {
        // 13.8 kV Main Bus A & West/Tie/East Distribution Corridors
        vBaseKv = distKv;
        baseMva = Math.min(41.7, activeTxMva);
        const zBaseOhms = (vBaseKv * vBaseKv) / baseMva;
        const rNgrPu = 10.0 / zBaseOhms;
        const threeZn = ngrOn ? (3 * rNgrPu) : 1e6;
        const cascadeX = (vs.totalCascadeXPu || vs.xPu) * txImpScale;
        z1 = vs.z1SysPu + cascadeX;
        z2 = z1;
        z0 = vs.z0TxPu * txImpScale + threeZn;

        const distKmMap = {
          lv_bus: 0, node5_lv_bus: 0,
          node6_fdr1: 0.7 * fracDist, node6_fdr2: 0.8 * fracDist, fdr1_end: 2.0,
          node9_acr1: 1.0 * fracDist, node11_urd_pad: 1.35 * fracDist, node10_res_lat: 1.85 * fracDist,
          node12_cbd_bus: 1.75 * fracDist,
          node13_tie1: 2.15 * fracDist, node14_tie2: 2.15 * fracDist,
          node15_uni_bus: b.fdr3_from_subA ? 2.55 : 0.85 * fracDist,
          node16_mun_bus: b.fdr4_from_subA ? 2.55 : 0.90 * fracDist
        };
        const km = distKmMap[loc] != null ? distKmMap[loc] : 0;
        if (km > 0) {
          const z1FdrPu = (km * 0.42) / zBaseOhms;
          const z0FdrPu = (km * 1.18) / zBaseOhms;
          z1 += z1FdrPu; z2 += z1FdrPu; z0 += z0FdrPu;
          xrRatio = Math.max(2.8, 10.5 - km * 3.1);
          locLabel = `${meta ? meta.name : loc} (${km.toFixed(2)} km)`;
        }
      }

      const iBaseKa = baseMva / (Math.sqrt(3) * vBaseKv);
      let iSeq1 = 0, iSeq2 = 0, iSeq0 = 0, iFaultPu = 0;

      if (ftype === '3ph') {
        iSeq1 = 1 / z1;
        iFaultPu = iSeq1;
      } else if (ftype === 'slg') {
        const i0 = 3 / (z1 + z2 + z0);
        iSeq1 = i0 / 3; iSeq2 = i0 / 3; iSeq0 = i0 / 3;
        iFaultPu = i0;
      } else if (ftype === 'll') {
        iSeq1 = 1 / (z1 + z2);
        iSeq2 = -iSeq1;
        iFaultPu = Math.sqrt(3) * iSeq1;
      } else {
        const zPar = (z2 * z0) / (z2 + z0);
        iSeq1 = 1 / (z1 + zPar);
        iSeq2 = -iSeq1 * (z0 / (z2 + z0));
        iSeq0 = -iSeq1 * (z2 / (z2 + z0));
        const ibMag = Math.hypot(iSeq0 - 0.5 * (iSeq1 + iSeq2), (Math.sqrt(3) / 2) * (iSeq1 - iSeq2));
        const igMag = Math.abs(3 * iSeq0);
        iFaultPu = Math.max(ibMag, igMag);
      }

      const iSymKa = iFaultPu * iBaseKa;
      const asymFactor = 1.0 + Math.exp(-Math.PI / Math.max(1.5, xrRatio));
      const iPeakKa = iSymKa * Math.sqrt(2) * (1.0 + 0.85 * Math.exp(-Math.PI / Math.max(1.5, xrRatio)));
      const sScMva = Math.sqrt(3) * vBaseKv * iSymKa;
      const dutyPass = iSymKa <= cbRatingKa;
      const upstreamDevices = (meta && typeof meta.upstreamDevices === 'function')
        ? meta.upstreamDevices(b)
        : ['50/51-F1', '50/51-LV Main', '51-HV'];

      return {
        vs, b, loc, locLabel, ftype, ngrOn, vBaseKv, baseMva, iBaseKa,
        z1, z2, z0, xrRatio, asymFactor, iSeq1, iSeq2, iSeq0, iFaultPu,
        iSymKa, iPeakKa, sScMva, cbRatingKa, dutyPass, upstreamDevices
      };
    }

    function toggleLiveTelemetryDrawer(forceState) {
      const drawer = document.getElementById('live-telemetry-drawer');
      const btn = document.getElementById('btn-telem-drawer');
      if (!drawer) return;
      const next = (forceState !== undefined) ? !!forceState : !drawer.classList.contains('open');
      AppState.liveTelemetryOpen = next;
      drawer.classList.toggle('open', next);
      if (btn) btn.classList.toggle('active', next);
    }

    function updateSubtitleAndTelemetry() {
      const pf = computePowerFlowMetrics();
      const vs = pf.vs;
      const s = AppState.switchStates;

      const sub = document.getElementById('subtitle-rating');
      if (sub) {
        sub.innerText = `Substation and Distribution Simulation | Sub A (${AppState.busTopology.toUpperCase()}/${AppState.enclosureType.toUpperCase()}) ⇄ Tie Sub B (${(AppState.subBTopology || 'ring').toUpperCase()}/${(AppState.subBEnclosure || 'ais').toUpperCase()}) · ${vs.cascadeLabel || (vs.hvKv + '/' + pf.distKv + ' kV')} · ${pf.indKv} kV Ind`;
      }
      if (typeof syncTargetSubstationUI === 'function') syncTargetSubstationUI();

      const elSt = document.getElementById('telem-grid-status');
      const elCompactPill = document.getElementById('telem-compact-pill');
      const elCompactKv = document.getElementById('telem-compact-kv');
      const elHvV = document.getElementById('telem-hv-voltage');
      const elHvPu = document.getElementById('telem-hv-pu');
      const elLvV = document.getElementById('telem-lv-voltage');
      const elLvPu = document.getElementById('telem-lv-pu');
      const elVr = document.getElementById('telem-vr');
      const elI = document.getElementById('telem-current');
      const elFdrI = document.getElementById('telem-feeder-currents');
      const elTieSt = document.getElementById('telem-tie-status');
      const elP = document.getElementById('telem-power');
      const elMwMvar = document.getElementById('telem-mw-mvar');
      const elFreqRg = document.getElementById('telem-freq-rg');
      const elGprLive = document.getElementById('telem-gpr-live');

      if (elSt && !AppState.isFaultActive) {
        elSt.innerText = pf.b.txFeed ? (pf.b.secMain ? 'ENERGIZED' : `${pf.distKv}kV OPEN`) : 'ISOLATED';
        elSt.style.color = pf.b.txFeed ? '#a7f3d0' : '#fde68a';
      }
      if (elCompactPill) {
        elCompactPill.classList.toggle('fault', !!AppState.isFaultActive);
        elCompactPill.classList.toggle('deenergized', !AppState.isFaultActive && (!pf.b.txFeed || !pf.b.secMain));
      }
      if (elCompactKv) elCompactKv.innerText = `${pf.vHvKvActual.toFixed(0)}→${pf.vDistKvActual.toFixed(1)} kV`;
      if (elHvV) elHvV.innerText = `${pf.vHvKvActual.toFixed(1)} kV`;
      if (elHvPu) elHvPu.innerText = `(${pf.vHvPu.toFixed(2)} pu)`;
      if (elLvV) elLvV.innerText = `${pf.vDistKvActual.toFixed(2)} kV`;
      if (elLvPu) elLvPu.innerText = `(${pf.vDistPu.toFixed(2)} pu)`;
      if (elVr) {
        elVr.innerText = `VR ${pf.vrPct.toFixed(1)}%`;
        elVr.style.color = Math.abs(pf.vrPct) <= 5.0 ? '#10b981' : '#f59e0b';
      }
      if (elI) elI.innerText = `HV ${pf.iHvA.toFixed(0)}A | IND ${pf.iIndA.toFixed(0)}A`;
      if (elFdrI) elFdrI.innerText = `F1:${pf.iF1A.toFixed(0)}A F2:${pf.iF2A.toFixed(0)}A | SubB F3:${pf.iF3A.toFixed(0)}A F4:${pf.iF4A.toFixed(0)}A`;
      if (elTieSt) {
        const xferTag = pf.b.fdr3_from_subA || pf.b.fdr4_from_subA
          ? ` | SUB A→E:+${pf.subATransferMva.toFixed(1)}MVA`
          : (pf.b.fdr1_from_subB || pf.b.fdr2_from_subB ? ` | SUB B→W:+${pf.subBTransferMva.toFixed(1)}MVA` : '');
        elTieSt.innerText = `79-TIE1:${s.cbTieB ? 'CLS' : 'NO'} | 89-TIE2:${s.cbTie2 ? 'CLS' : 'NO'} | 52-IND:${pf.b.ind_hv ? pf.indKv + 'kV' : 'OPN'}${xferTag}`;
      }
      if (elP) elP.innerText = `${pf.sNetMva.toFixed(1)} MVA | SubB:${pf.sSubBMva.toFixed(1)} MVA | PF ${pf.pfNet.toFixed(2)}`;
      if (elMwMvar) elMwMvar.innerText = `P=${pf.pLoadMw.toFixed(1)} MW | Q=${pf.qNetMvar >= 0 ? '+' : ''}${pf.qNetMvar.toFixed(1)} MVAR | Loop ΔV=${pf.loopDropPct.toFixed(1)}%`;
      if (elFreqRg) elFreqRg.innerText = `60.00 Hz | 0.842 Ω | ΘH=${pf.sizing ? pf.sizing.thermalHotSpotC : 78}°C`;
      if (elGprLive) {
        const gprV = AppState.isFaultActive ? (19800 * 0.842 * 0.12).toFixed(0) : Math.max(12, pf.iHvA * 0.052).toFixed(0);
        const stressNote = (pf.sizing && pf.sizing.mode === 'stress' && pf.sizing.txLoadPct > 100) ? ` | 🚨 TR-01 ${pf.sizing.txLoadPct.toFixed(0)}%` : '';
        elGprLive.innerText = `Live GPR: ${gprV} V (${Number(gprV) < 2800 ? 'IEEE 80 Safe' : 'ELEVATED'})${stressNote}`;
      }
      if (typeof updateLandAreaUI === 'function') updateLandAreaUI();
    }

    function updateTelemetryUI() {
      updateSubtitleAndTelemetry();
    }

    // INTERACTIVE POWER FLOW, SHORT-CIRCUIT, RELAY TCC & PQ LAB MODAL HANDLERS
    function openAnalysisModal(tab = 'pf', relayFocus = null) {
      const modal = document.getElementById('analysis-modal');
      if (!modal) return;
      if (AppState.tccState) {
        AppState.tccState.topo = AppState.busTopology || AppState.tccState.topo || 'single';
        if (relayFocus) AppState.tccState.focusedRelay = relayFocus;
      }
      modal.style.display = 'flex';
      switchAnalysisTab(tab || AppState.activeAnalysisTab || 'pf');
    }

    function closeAnalysisModal() {
      const modal = document.getElementById('analysis-modal');
      if (modal) modal.style.display = 'none';
      if (pqAnimFrameId && typeof cancelAnimationFrame === 'function') {
        cancelAnimationFrame(pqAnimFrameId);
        pqAnimFrameId = null;
      }
      updateSubtitleAndTelemetry();
    }

    function switchAnalysisTab(tab) {
      AppState.activeAnalysisTab = tab;
      const tPf = document.getElementById('tab-analysis-pf');
      const tSc = document.getElementById('tab-analysis-sc');
      const tTcc = document.getElementById('tab-analysis-tcc');
      const tPq = document.getElementById('tab-analysis-pq');
      if (tPf) tPf.classList.toggle('active', tab === 'pf');
      if (tSc) tSc.classList.toggle('active', tab === 'sc');
      if (tTcc) tTcc.classList.toggle('active', tab === 'tcc');
      if (tPq) tPq.classList.toggle('active', tab === 'pq');
      if (tab !== 'pq' && pqAnimFrameId && typeof cancelAnimationFrame === 'function') {
        cancelAnimationFrame(pqAnimFrameId);
        pqAnimFrameId = null;
      }
      renderAnalysisModalBody();
    }

    function updatePfLabControl(key, val) {
      if (key === 'load') AppState.pfLoadPct = parseInt(val, 10);
      else if (key === 'pf') AppState.pfPowerFactor = parseFloat(val);
      else if (key === 'tap') AppState.oltcTapPct = parseFloat(val);
      else if (key === 'cap') {
        const target = !!val;
        if (target) {
          AppState.switchStates.dsCapA = true;
          AppState.switchStates.dsCapB = true;
          AppState.switchStates.cbCap = true;
        } else {
          AppState.switchStates.cbCap = false;
        }
        syncAllSwitchesTo3D();
        renderSwitchMatrix();
        renderLiveSLD();
      }
      updateSubtitleAndTelemetry();
      renderAnalysisModalBody();
    }

    window.updateMvaScalingControl = function(key, val) {
      if (!AppState.mvaScaling) AppState.mvaScaling = {};
      if (key === 'reset') {
        const vs = getVoltageSpec(AppState.voltageClass);
        AppState.mvaScaling = {
          mode: AppState.mvaScaling.mode || 'autosize',
          txMvaOverride: vs.mva, subBTxMva: 15,
          resKva: 50, urdKva: 900, cbdKva: 750, uniKva: 500, munKva: 1000, indMva: vs.indCustMva || 25.0
        };
      } else if (key === 'mode') {
        AppState.mvaScaling.mode = (val === 'stress') ? 'stress' : 'autosize';
      } else if (key === 'txMvaOverride') {
        AppState.mvaScaling.txMvaOverride = (val === null || val === 'auto') ? null : parseFloat(val);
      } else {
        AppState.mvaScaling[key] = parseFloat(val);
      }
      updateSubtitleAndTelemetry();
      renderLiveSLD();
      if (typeof renderTelemetryDrawer === 'function' && AppState.selectedComponent) {
        renderTelemetryDrawer(AppState.selectedComponent);
      }
      const modal = document.getElementById('analysis-modal');
      if (modal && modal.style.display === 'flex') renderAnalysisModalBody();
    };

    function updateScLabControl(key, val) {
      if (key === 'loc') {
        AppState.scFaultLoc = val;
        if (PINPOINT_FAULT_NODES[val]) AppState.pinpointFaultNode = val;
      } else if (key === 'type') {
        AppState.scFaultType = val;
      } else if (key === 'ngr') {
        AppState.scNgrGrounded = (val === 'ngr' || val === true);
        renderLiveSLD();
      }
      renderAnalysisModalBody();
    }

    function drawScMiniTccPreview(canvas, sc, sched) {
      const ctx = canvas ? canvas.getContext('2d') : null;
      if (!ctx) return;
      const W = canvas.width, H = canvas.height;
      const padL = 36, padR = 12, padT = 10, padB = 22;
      const plotW = W - padL - padR, plotH = H - padT - padB;
      const logMinI = 2.0, logMaxI = 4.9, logMinT = -2.0, logMaxT = 2.2;
      const xOf = (a) => padL + ((Math.log10(Math.max(100, a)) - logMinI) / (logMaxI - logMinI)) * plotW;
      const yOf = (t) => padT + ((logMaxT - Math.log10(Math.max(0.01, Math.min(160, t)))) / (logMaxT - logMinT)) * plotH;

      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = 'rgba(56,189,248,0.16)';
      ctx.lineWidth = 0.7;
      for (let d = 2; d <= 4; d++) {
        const x = xOf(Math.pow(10, d));
        ctx.beginPath(); ctx.moveTo(x, padT); ctx.lineTo(x, padT + plotH); ctx.stroke();
        ctx.fillStyle = '#64748b'; ctx.font = '8px monospace'; ctx.textAlign = 'center';
        ctx.fillText(`${Math.pow(10, d) >= 1000 ? Math.pow(10, d)/1000+'kA' : Math.pow(10, d)+'A'}`, x, H - 6);
      }
      const refSide = sc.vBaseKv > (sched.vs.lvKv * 1.4) ? 'hv' : 'lv';
      const evFn = (a) => evaluateTccAtCurrent(a, sched, AppState.busTopology, refSide, false);
      [['#a855f7', (e) => e.tRecFast], ['#fb923c', (e) => e.tFuseClear], ['#4ade80', (e) => e.tFdr], ['#fbbf24', (e) => e.tLv], ['#38bdf8', (e) => e.tTopo]].forEach(([col, fn]) => {
        ctx.strokeStyle = col; ctx.lineWidth = 1.6; ctx.beginPath();
        let st = false;
        for (let i = 0; i <= 100; i++) {
          const amp = Math.pow(10, logMinI + (i / 100) * (logMaxI - logMinI));
          const t = fn(evFn(amp));
          if (t == null || t > 160 || t < 0.01) { st = false; continue; }
          const px = xOf(amp), py = yOf(t);
          if (!st) { ctx.moveTo(px, py); st = true; } else ctx.lineTo(px, py);
        }
        ctx.stroke();
      });
      const iF = Math.max(100, Math.min(75000, sc.iSymKa * 1000));
      const fx = xOf(iF);
      ctx.save(); ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 1.6; ctx.setLineDash([4, 3]);
      ctx.beginPath(); ctx.moveTo(fx, padT); ctx.lineTo(fx, padT + plotH); ctx.stroke();
      ctx.restore();
      ctx.fillStyle = '#fda4af'; ctx.font = 'bold 8.5px monospace';
      ctx.textAlign = fx > W - 80 ? 'right' : 'left';
      ctx.fillText(`If=${sc.iSymKa.toFixed(2)}kA`, fx + (fx > W - 80 ? -3 : 3), padT + 9);
    }

    function renderAnalysisModalBody() {
      const body = document.getElementById('analysis-modal-body');
      if (!body) return;
      if (AppState.activeAnalysisTab === 'pf') {
        const pf = computePowerFlowMetrics();
        const vs = pf.vs;
        const ms = AppState.mvaScaling || {};
        const sz = pf.sizing || {};
        const lvCol = pf.vDistPu < 0.92 ? '#ef4444' : (pf.vDistPu > 1.05 ? '#f59e0b' : '#10b981');
        const lb = pf.loadBreakdown || {};
        const curTr01 = ms.txMvaOverride != null ? ms.txMvaOverride : vs.mva;
        const curTr02 = ms.subBTxMva != null ? ms.subBTxMva : 15;
        body.innerHTML = `
          <div class="analysis-grid">
            <div class="analysis-panel">
              <h4>Operating Controls (${vs.shortLabel}, TR-01 = ${curTr01} MVA)</h4>
              <div class="analysis-slider-row">
                <label>Feeder Load Multiplier <span>${pf.loadPct}% (${pf.sLoadMva.toFixed(1)} MVA)</span></label>
                <input type="range" min="25" max="150" step="5" value="${pf.loadPct}" oninput="updatePfLabControl('load', this.value)">
              </div>
              <div class="analysis-slider-row">
                <label>Native Load Power Factor <span>${pf.pfLoad.toFixed(2)} lag</span></label>
                <input type="range" min="0.75" max="0.98" step="0.01" value="${pf.pfLoad}" oninput="updatePfLabControl('pf', this.value)">
              </div>
              <div class="analysis-slider-row">
                <label>TR-01 OLTC Tap Changer <span>${pf.tapPct >= 0 ? '+' : ''}${pf.tapPct.toFixed(2)}% (${pf.tapPu.toFixed(4)} pu)</span></label>
                <input type="range" min="-10" max="10" step="1.25" value="${pf.tapPct}" oninput="updatePfLabControl('tap', this.value)">
              </div>
              <div class="analysis-slider-row" style="margin-top:6px;">
                <label>Shunt Capacitor Bank (52-CAP: ${vs.capMvar} MVAR)
                  <button class="btn" style="padding:3px 10px; font-size:10.5px; background:${pf.capOn?'rgba(16,185,129,0.22)':'rgba(239,68,68,0.22)'};" onclick="updatePfLabControl('cap', ${!pf.capOn})">
                    ${pf.capOn ? 'CAP BANK IN (ON)' : 'CAP BANK OUT (OFF)'}
                  </button>
                </label>
              </div>
              <svg viewBox="0 0 360 95" width="100%" style="background:#020617; border-radius:6px; border:1px solid rgba(56,189,248,0.2); margin-top:6px;">
                <line x1="18" y1="48" x2="115" y2="48" stroke="#38bdf8" stroke-width="3"/>
                <text x="58" y="34" fill="#38bdf8" font-size="9" text-anchor="middle" font-family="monospace">${pf.vHvPu.toFixed(3)} pu (${pf.vHvKvActual.toFixed(1)} kV)</text>
                <circle cx="130" cy="48" r="14" fill="none" stroke="#38bdf8" stroke-width="2"/>
                <circle cx="148" cy="48" r="14" fill="none" stroke="#f59e0b" stroke-width="2"/>
                <text x="139" y="75" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="monospace">TR-01: ${curTr01}MVA (${pf.tapPct>=0?'+':''}${pf.tapPct.toFixed(1)}%)</text>
                <line x1="162" y1="48" x2="275" y2="48" stroke="${lvCol}" stroke-width="3"/>
                <text x="225" y="34" fill="${lvCol}" font-size="9" text-anchor="middle" font-family="monospace">${pf.vDistPu.toFixed(3)} pu (${pf.vDistKvActual.toFixed(2)} kV)</text>
                <rect x="275" y="34" width="68" height="28" rx="4" fill="#0f172a" stroke="#10b981"/>
                <text x="309" y="47" fill="#f1f5f9" font-size="8.5" text-anchor="middle" font-family="monospace">${pf.pLoadMw.toFixed(1)} MW</text>
                <text x="309" y="57" fill="#2dd4bf" font-size="8" text-anchor="middle" font-family="monospace">${pf.qNetMvar.toFixed(1)} MVAR</text>
              </svg>
              <div style="margin-top:8px; padding:7px 9px; background:rgba(15,23,42,0.85); border-radius:6px; border:1px solid rgba(56,189,248,0.22); font-size:10px; line-height:1.45;">
                <strong style="color:#67e8f9;">🔄 ${pf.b.loopModeBanner}</strong><br>
                Sub A: <strong>${pf.sSubAMva.toFixed(2)} MVA</strong> (East Xfer: +${pf.subATransferMva.toFixed(2)}) · Sub B: <strong>${pf.sSubBMva.toFixed(2)} MVA</strong> (West Xfer: +${pf.subBTransferMva.toFixed(2)}) · Loop ΔV: <strong>${pf.loopDropPct.toFixed(2)}%</strong>
              </div>
            </div>
            <div class="analysis-panel">
              <h4>Calculated Per-Unit &amp; Thermal Results</h4>
              <div class="analysis-kpi-grid">
                <div class="analysis-kpi"><span>Active / Reactive (Sub A)</span><strong>${pf.pLoadMw.toFixed(2)} MW / ${pf.qNetMvar.toFixed(2)} MVAR</strong></div>
                <div class="analysis-kpi"><span>Net Apparent S &amp; PF</span><strong>${pf.sNetMva.toFixed(2)} MVA (${pf.pfNet.toFixed(3)} ${pf.pfLeadLag})</strong></div>
                <div class="analysis-kpi"><span>Secondary Voltage</span><strong style="color:${lvCol};">${pf.vDistKvActual.toFixed(2)} kV (${pf.vDistPu.toFixed(3)} pu)</strong></div>
                <div class="analysis-kpi"><span>%VR &amp; Efficiency (η)</span><strong style="color:#10b981;">${pf.vrPct.toFixed(2)}% · ${pf.etaPct.toFixed(2)}%</strong></div>
                <div class="analysis-kpi"><span>Feeder F1 / F2 Amps</span><strong>${pf.iF1A.toFixed(0)} A / ${pf.iF2A.toFixed(0)} A</strong></div>
                <div class="analysis-kpi"><span>Sub B F3 / F4 Amps</span><strong>${pf.iF3A.toFixed(0)} A / ${pf.iF4A.toFixed(0)} A</strong></div>
                <div class="analysis-kpi"><span>TR-01 Thermal (C57.91)</span><strong style="color:${sz.hotSpotAlarm?'#f87171':'#fde68a'};">Oil ${sz.thermalTopOilC}°C | ΘH ${sz.thermalHotSpotC}°C</strong></div>
                <div class="analysis-kpi"><span>52-LV Frame / CT Ratio</span><strong style="color:#67e8f9;">${sz.brkLvAmp}A (${sz.brkKa}kA) · CT ${sz.ctLvPri}:5</strong></div>
              </div>
              <div style="margin-top:8px; padding:7px 9px; border-radius:6px; background:${sz.relay51Alert||sz.lvBusDropWarning?'rgba(127,29,29,0.5)':'rgba(6,78,59,0.35)'}; border:1px solid ${sz.relay51Alert?'#f87171':'rgba(16,185,129,0.4)'}; font-size:10.5px;">
                <strong style="color:${sz.relay51Alert?'#fca5a5':'#a7f3d0'};">${sz.overloadBadge}</strong><br>
                <span style="color:#cbd5e1; font-size:9.8px;">Busbar: ${sz.busbarSpec} · 3D TX Scale: ${sz.baseScaleRatio}×</span>
              </div>
            </div>
          </div>

          <div class="analysis-panel" style="margin-top:10px;">
            <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:8px; margin-bottom:8px;">
              <h4 style="margin:0;">🎛️ Dynamic MVA &amp; Load Scaling Studio</h4>
              <div style="display:flex; gap:5px; flex-wrap:wrap;">
                <button class="tcc-topo-pill ${(ms.mode||'autosize')==='stress'?'active':''}" onclick="updateMvaScalingControl('mode','stress')">Mode A: Fixed Equipment / Stress Test</button>
                <button class="tcc-topo-pill ${(ms.mode||'autosize')==='autosize'?'active':''}" onclick="updateMvaScalingControl('mode','autosize')">Mode B: Auto-Size Breakers, CTs, TCC &amp; 3D</button>
                <button class="tcc-topo-pill" onclick="updateMvaScalingControl('reset',true)">Reset Defaults</button>
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(4, minmax(150px, 1fr)); gap:8px;">
              <div class="analysis-slider-row"><label>TR-01 Rating <span>${curTr01} MVA</span></label><input type="range" min="10" max="300" step="5" value="${curTr01}" oninput="updateMvaScalingControl('txMvaOverride', this.value)"></div>
              <div class="analysis-slider-row"><label>TR-02 Tie Rating <span>${curTr02} MVA</span></label><input type="range" min="5" max="100" step="2.5" value="${curTr02}" oninput="updateMvaScalingControl('subBTxMva', this.value)"></div>
              <div class="analysis-slider-row"><label>RES Pole TX <span>${ms.resKva??50} kVA</span></label><input type="range" min="25" max="5000" step="25" value="${ms.resKva??50}" oninput="updateMvaScalingControl('resKva', this.value)"></div>
              <div class="analysis-slider-row"><label>URD Subdiv <span>${ms.urdKva??900} kVA</span></label><input type="range" min="150" max="15000" step="150" value="${ms.urdKva??900}" oninput="updateMvaScalingControl('urdKva', this.value)"></div>
              <div class="analysis-slider-row"><label>CBD / Hospital <span>${ms.cbdKva??750} kVA</span></label><input type="range" min="250" max="25000" step="250" value="${ms.cbdKva??750}" oninput="updateMvaScalingControl('cbdKva', this.value)"></div>
              <div class="analysis-slider-row"><label>East University <span>${ms.uniKva??500} kVA</span></label><input type="range" min="100" max="15000" step="100" value="${ms.uniKva??500}" oninput="updateMvaScalingControl('uniKva', this.value)"></div>
              <div class="analysis-slider-row"><label>Municipal / Log <span>${ms.munKva??1000} kVA</span></label><input type="range" min="250" max="20000" step="250" value="${ms.munKva??1000}" oninput="updateMvaScalingControl('munKva', this.value)"></div>
              <div class="analysis-slider-row"><label>Industrial HV <span>${ms.indMva??25} MVA</span></label><input type="range" min="5" max="80" step="2.5" value="${ms.indMva??25}" oninput="updateMvaScalingControl('indMva', this.value)"></div>
            </div>
          </div>
        `;
      } else if (AppState.activeAnalysisTab === 'sc') {
        const sc = computeShortCircuitMetrics();
        const badgeCls = sc.dutyPass ? 'duty-pass' : 'duty-fail';
        const sched = computeRelaySettingsSchedule(AppState.voltageClass, AppState.busTopology);
        const groups = {};
        Object.values(PINPOINT_FAULT_NODES).forEach(n => {
          const g = n.group || 'Other';
          if (!groups[g]) groups[g] = [];
          groups[g].push(n);
        });
        const selOptions = Object.entries(groups).map(([gName, arr]) => `
          <optgroup label="${gName}">
            ${arr.map(n => `<option value="${n.id}" ${sc.loc === n.id ? 'selected' : ''}>${n.name}</option>`).join('')}
          </optgroup>
        `).join('');
        const refSideSc = sc.vBaseKv > (sc.vs.lvKv * 1.4) ? 'hv' : 'lv';
        const evSc = evaluateTccAtCurrent(Math.max(40, sc.iSymKa * 1000), sched, AppState.busTopology, refSideSc, false);
        body.innerHTML = `
          <div class="analysis-grid">
            <div class="analysis-panel">
              <h4>23-Node System-Wide Fault Location, Type &amp; Grounding</h4>
              <div class="analysis-slider-row">
                <label>Target Fault Node (All 23 Grid Nodes)</label>
                <select id="sc-fault-loc" onchange="updateScLabControl('loc', this.value)" style="width:100%; padding:5px 7px; background:#0f172a; color:#f1f5f9; border:1px solid rgba(56,189,248,0.4); border-radius:5px; font-size:11px;">
                  ${selOptions}
                </select>
                <div class="preset-grid" style="grid-template-columns: repeat(6, 1fr); margin-top:5px;">
                  <button class="btn-preset ${sc.loc==='node2_hv_bus'?'active':''}" onclick="updateScLabControl('loc','node2_hv_bus')">HV Bus</button>
                  <button class="btn-preset ${sc.loc==='node5_lv_bus'?'active':''}" onclick="updateScLabControl('loc','node5_lv_bus')">LV Bus</button>
                  <button class="btn-preset ${sc.loc==='node8_ind_sub'?'active':''}" onclick="updateScLabControl('loc','node8_ind_sub')">Ind Sub</button>
                  <button class="btn-preset ${sc.loc==='node11_urd_pad'?'active':''}" onclick="updateScLabControl('loc','node11_urd_pad')">URD Pad</button>
                  <button class="btn-preset ${sc.loc==='node15_uni_bus'?'active':''}" onclick="updateScLabControl('loc','node15_uni_bus')">East Uni</button>
                  <button class="btn-preset ${sc.loc==='node19_subb_lv'?'active':''}" onclick="updateScLabControl('loc','node19_subb_lv')">SubB LV</button>
                </div>
              </div>
              <div class="analysis-slider-row">
                <label>Symmetrical Component Fault Type</label>
                <div class="preset-grid" style="grid-template-columns: repeat(4, 1fr);">
                  <button class="btn-preset ${sc.ftype==='3ph'?'active':''}" onclick="updateScLabControl('type','3ph')">3-Phase (LLL)</button>
                  <button class="btn-preset ${sc.ftype==='slg'?'active':''}" onclick="updateScLabControl('type','slg')">SLG (L-G)</button>
                  <button class="btn-preset ${sc.ftype==='ll'?'active':''}" onclick="updateScLabControl('type','ll')">L-L</button>
                  <button class="btn-preset ${sc.ftype==='dlg'?'active':''}" onclick="updateScLabControl('type','dlg')">DLG (LL-G)</button>
                </div>
              </div>
              <div class="analysis-slider-row">
                <label>Transformer Neutral Grounding (Y-side)</label>
                <div class="preset-grid" style="grid-template-columns: 1fr 1fr;">
                  <button class="btn-preset ${sc.ngrOn?'active':''}" onclick="updateScLabControl('ngr','ngr')">NGR Grounded (${sc.vs.ngrOhms} Ω)</button>
                  <button class="btn-preset ${!sc.ngrOn?'active':''}" onclick="updateScLabControl('ngr','ungrnd')">Isolated / Ungrounded Neutral</button>
                </div>
              </div>
              <svg viewBox="0 0 360 90" width="100%" style="background:#020617; border-radius:6px; border:1px solid rgba(56,189,248,0.2); margin-top:6px;">
                <rect x="14" y="12" width="100" height="66" rx="4" fill="#0f172a" stroke="#38bdf8"/>
                <text x="64" y="28" fill="#38bdf8" font-size="8.5" text-anchor="middle" font-weight="bold" font-family="monospace">Z₁ Positive</text>
                <text x="64" y="45" fill="#f1f5f9" font-size="9" text-anchor="middle" font-family="monospace">${sc.z1.toFixed(4)} pu</text>
                <text x="64" y="61" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="monospace">I₁=${sc.iSeq1.toFixed(2)} pu</text>
                <rect x="130" y="12" width="100" height="66" rx="4" fill="#0f172a" stroke="#f59e0b"/>
                <text x="180" y="28" fill="#f59e0b" font-size="8.5" text-anchor="middle" font-weight="bold" font-family="monospace">Z₂ Negative</text>
                <text x="180" y="45" fill="#f1f5f9" font-size="9" text-anchor="middle" font-family="monospace">${sc.z2.toFixed(4)} pu</text>
                <text x="180" y="61" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="monospace">I₂=${sc.iSeq2.toFixed(2)} pu</text>
                <rect x="246" y="12" width="100" height="66" rx="4" fill="#0f172a" stroke="#10b981"/>
                <text x="296" y="28" fill="#10b981" font-size="8.5" text-anchor="middle" font-weight="bold" font-family="monospace">Z₀ Zero-Seq</text>
                <text x="296" y="45" fill="#f1f5f9" font-size="9" text-anchor="middle" font-family="monospace">${sc.z0 > 999 ? 'OPEN (∞)' : sc.z0.toFixed(4)+' pu'}</text>
                <text x="296" y="61" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="monospace">I₀=${sc.iSeq0.toFixed(2)} pu</text>
              </svg>
            </div>
            <div class="analysis-panel">
              <h4>Fault Current, Duty &amp; Live Mini-TCC (${sc.locLabel})</h4>
              <div class="analysis-kpi-grid">
                <div class="analysis-kpi"><span>Symmetrical Fault I_f,sym</span><strong style="color:#f87171;">${sc.iSymKa.toFixed(2)} kA (${sc.iFaultPu.toFixed(2)} pu)</strong></div>
                <div class="analysis-kpi"><span>Asymmetric Crest I_peak</span><strong>${sc.iPeakKa.toFixed(2)} kA (X/R ${sc.xrRatio.toFixed(1)})</strong></div>
                <div class="analysis-kpi"><span>Short-Circuit MVA (S_sc)</span><strong>${sc.sScMva.toFixed(1)} MVA @ ${sc.vBaseKv} kV</strong></div>
                <div class="analysis-kpi"><span>Active Protection Path</span><strong style="color:#67e8f9;">${(sc.upstreamDevices||[]).slice(0,2).join(' → ')}</strong></div>
              </div>
              <div style="margin-top:8px; padding:7px 9px; background:rgba(15,23,42,0.85); border-radius:6px; border:1px solid rgba(148,163,184,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <span style="font-size:10.5px; color:#cbd5e1;">Breaker Duty: <strong>${sc.cbRatingKa} kA</strong></span>
                  <span class="duty-badge ${badgeCls}">${sc.dutyPass ? 'PASS — WITHIN RATING' : 'FAIL — EXCEEDS RATING'}</span>
                </div>
                <button class="btn" style="width:100%; justify-content:center; margin-top:7px; padding:5px 10px; font-size:10.8px; background:rgba(250,204,21,0.18); border-color:#facc15; color:#fef08a;" onclick="plotActiveFaultOnTcc('${sc.loc}')">
                  📈 Plot This Fault on TCC Coordination Graph
                </button>
              </div>
              <div style="margin-top:8px; background:#020617; border:1px solid rgba(56,189,248,0.25); border-radius:6px; padding:5px;">
                <div style="font-size:9.8px; color:#94a3b8; margin-bottom:3px; display:flex; justify-content:space-between;">
                  <span>⚡ Mini-TCC Sequence (${refSideSc.toUpperCase()} Ref):</span>
                  <span style="color:#fde68a; font-family:monospace;">F1:${evSc.tFdr!=null?evSc.tFdr.toFixed(3)+'s':'—'} | LV:${evSc.tLv!=null?evSc.tLv.toFixed(3)+'s':'—'} | HV:${evSc.tTopo!=null?evSc.tTopo.toFixed(3)+'s':'—'}</span>
                </div>
                <canvas id="sc-mini-tcc-canvas" width="350" height="118" style="width:100%; height:auto; display:block;"></canvas>
              </div>
            </div>
          </div>
        `;
        const miniCanvas = document.getElementById('sc-mini-tcc-canvas');
        if (miniCanvas) drawScMiniTccPreview(miniCanvas, sc, sched);
      } else if (AppState.activeAnalysisTab === 'tcc') {
        renderTccCoordinationTab(body);
      } else {
        renderPqAnalysisTab(body);
      }
    }

    // =========================================================================
    // PROTECTIVE RELAY SETTINGS SCHEDULE & INTERACTIVE LOG-LOG TCC COORDINATION
    // =========================================================================
    function ieeeTccTime(I, Ip, tds, curveType = 'VI') {
      if (!Ip || I <= Ip * 1.03) return null;
      const m = I / Ip;
      if (curveType === 'MI') {
        // IEEE Moderately Inverse (C37.112)
        return tds * (0.0515 / (Math.pow(m, 0.02) - 1) + 0.114);
      } else if (curveType === 'SI') {
        // IEC Standard Inverse
        return tds * (0.14 / (Math.pow(m, 0.02) - 1));
      } else if (curveType === 'EI') {
        // IEEE Extremely Inverse
        return tds * (28.2 / (Math.pow(m, 2.0) - 1) + 0.1217);
      }
      // Default: IEEE Very Inverse (VI)
      return tds * (19.61 / (Math.pow(m, 2.0) - 1) + 0.491);
    }

    function computeRelaySettingsSchedule(vClass, scheme) {
      const vs = getVoltageSpec(vClass || AppState.voltageClass || '69_13');
      const top = scheme || AppState.busTopology || 'single';
      const pf = computePowerFlowMetrics();
      const sz = pf.sizing || {};
      const isAuto = (sz.mode === 'autosize');
      const distKv = vs.distKv || 13.8;
      const indKv = vs.indSubKv || 69.0;
      const effTxMva = isAuto ? (sz.sizingMva || vs.mva) : vs.mva;
      const distMva = Math.min(effTxMva, isAuto ? Math.max(41.7, effTxMva) : Math.min(41.7, vs.mva));
      const indRatedMva = (AppState.mvaScaling && AppState.mvaScaling.indMva != null) ? AppState.mvaScaling.indMva : (vs.indCustMva || 25.0);

      const iHvFl = Math.round((effTxMva * 1000) / (Math.sqrt(3) * vs.hvKv));
      const iLvFl = Math.round((distMva * 1000) / (Math.sqrt(3) * distKv));
      const iFdrFl = Math.round(iLvFl * 0.28);
      const iIndFl = Math.round((indRatedMva * 1000) / (Math.sqrt(3) * indKv));

      const hvCtPri = isAuto && sz.ctHvPri ? sz.ctHvPri : Math.max(400, Math.ceil((iHvFl * 1.35) / 200) * 200);
      const lvCtPri = isAuto && sz.ctLvPri ? sz.ctLvPri : Math.max(1200, Math.ceil((iLvFl * 1.25) / 500) * 500);
      const fdrCtPri = isAuto && sz.fdrCtPri ? sz.fdrCtPri : Math.max(400, Math.ceil((iFdrFl * 1.35) / 200) * 200);
      const brkHvAmp = sz.brkHvAmp || 1200;
      const brkLvAmp = sz.brkLvAmp || 2000;
      const brkKa = sz.brkKa || vs.lvCbKa || 31.5;
      const busbarSpec = sz.busbarSpec || '100 mm IPS Al Pipe';
      const ngrIp = Math.max(20, Math.round((distKv * 1000 / Math.sqrt(3) / 10.0) * 0.15));

      const fdrPickupLv = Math.round(fdrCtPri * 0.65);
      const fdrInstLv = Math.round(fdrPickupLv * 8.0);
      const lvMainPickupLv = Math.round(iLvFl * 1.25);     // 125% TR-01 LV FLA
      const indPickupHv = Math.round(iIndFl * 1.45);
      const indInstHv = Math.round(indPickupHv * 6.5);
      const indPickupLv = Math.round(indPickupHv * (indKv / distKv));
      const indInstLv = Math.round(indInstHv * (indKv / distKv));
      const hvBackupPickupHv = Math.round(iHvFl * 1.50);   // 150% Primary HV FLA
      const hvBackupRefLv = Math.round(hvBackupPickupHv * (vs.hvKv / distKv));

      const lineReachZ1Ohm = +(0.80 * (vs.hvKv * vs.hvKv / 180)).toFixed(2);
      const topoNotes = {
        single: {
          title: 'ANSI 87B-1 (Single Bus Zone) + 50BF Breaker Failure',
          desc: '4-input bus differential captures Incoming + TR-01 CTs. 50BF timer = 0.15 s (9 cyc); any bus fault de-energizes entire HV yard.'
        },
        maintransfer: {
          title: 'ANSI 87B-M / 87B-T + 51-BT Bus-Tie Overcurrent (52-BT)',
          desc: `Auto CT-switching transfers TR-01 protection to 52-BT during bypass mode. 51-BT pickup = ${hvBackupPickupHv} A, TDS 2.05, IEEE VI.`
        },
        ring: {
          title: 'ANSI 87L / 67-Ring Directional Overcurrent + Corner 87N Diff',
          desc: 'Closed loop splits fault & load flow ~50%/50% across West (52-1/52-4) & East (52-2/52-3) legs; each breaker clears N-1 in 3 cycles.'
        },
        breakerhalf: {
          title: 'Dual Bus Diff 87B-A & 87B-B + 52-TIE Center-Breaker Synchrocheck (25)',
          desc: 'Two independent low-impedance 87B zones + Tee-node differential on L1 & TR-01. Center breaker 52-TIE sees summed/split bay currents.'
        },
        doublebreaker: {
          title: 'Dual Redundant 87B-A + 87B-B & Segregated 50BF-1A/1B/2A/2B',
          desc: 'Maximum N-1 reliability: Bus A fault trips only 52-1A & 52-2A while Bus B + 52-1B/52-2B carry 100% TR-01 load seamlessly.'
        }
      };

      const cards = [
        {
          id: 'line_21_87b',
          badge: `${vs.hvKv} kV INCOMING (${brkHvAmp}A)`,
          title: '1. Incoming Line Distance & Directional OC',
          ansi: 'ANSI 21 / 67 / 50 / 51',
          rows: [
            ['CT / VT / Breaker', `${hvCtPri}:5 A (C800) | ${brkHvAmp} A CB | ${(vs.hvKv*1000/115).toFixed(0)}:1 VT`],
            ['21 Zone 1 / Zone 2', `${lineReachZ1Ohm} Ω (80%, 0 cyc) | ${(lineReachZ1Ohm*1.5).toFixed(2)} Ω (120%, 0.35 s)`],
            ['67/51 Directional OC', `Pickup = ${Math.round(iHvFl*1.65)} A | IEEE VI, TDS = 3.2`],
            ['50P Inst High-Set', `${(vs.hvCbKa * 0.45).toFixed(1)} kA (trips 52 in 2–3 cyc)`]
          ]
        },
        {
          id: 'line_21_87b',
          badge: LAND_TOPO_FACTORS[top].label.toUpperCase(),
          title: '2. Bus & Topology Breaker Failure Logic',
          ansi: topoNotes[top].title,
          rows: [
            ['Bus Diff Slope (87B)', `Slope 1 = 25% | Slope 2 = 60% | I_op > 0.20 pu`],
            ['50BF Breaker Failure', `Delay = 0.15 s (9 cyc) -> Retrip + Bus 86B Lockout`],
            ['Busbar & Fault Duty', `${busbarSpec} | ${brkKa} kA CB Duty`],
            ['Scheme Behavior', topoNotes[top].desc]
          ]
        },
        {
          id: 'tx_87t',
          badge: `${Math.round(effTxMva)} MVA ${vs.vectorGroup}`,
          title: '3. TR-01 Transformer Differential & Mechanical',
          ansi: 'ANSI 87T / 51-HV / 63 / 49',
          rows: [
            ['87T Phase/Slope', `Dyn11 Δ-Y Comp | I_min = 0.25 pu, Slopes 25% / 50%`],
            ['2nd / 5th Harmonic Block', `Inrush Block I₂/I₁ ≥ 15% | Overexc. I₅/I₁ ≥ 35%`],
            ['51-HV Backup OC', `${hvBackupPickupHv} A HV (${hvBackupRefLv} A @ ${distKv}kV) | IEEE VI, TDS = 2.2`],
            ['Mechanical (63 / 49)', `Buchholz Alarm/Trip + Hot-Spot ${sz.thermalHotSpotC || 85}°C (Trip > 110°C)`]
          ]
        },
        {
          id: 'tx_87t',
          badge: `${distKv} kV MAIN (${brkLvAmp}A)`,
          title: '4. Secondary Main VCB & Neutral Grounding',
          ansi: 'ANSI 50/51-LV / 51G / 64REF',
          rows: [
            ['VCB Frame & CT Ratio', `${brkLvAmp} A (${brkKa} kA) | CT ${lvCtPri}:5 A | FLA = ${iLvFl} A`],
            ['51-LV Time Overcurrent', `Pickup = ${lvMainPickupLv} A (125% FLA) | IEEE VI, TDS = 1.25`],
            ['50-LV Instantaneous', `${Math.round(lvMainPickupLv * 7.5)} A (Coordinated below HV 51-HV)`],
            ['51G NGR + 64REF', `NGR = ${vs.ngrOhms} Ω | 51G Pickup = ${ngrIp} A, TDS 0.8 (IEC SI)`]
          ]
        },
        {
          id: 'fdr_50_51',
          badge: `${distKv} kV FDR-01..04`,
          title: '5. Public Distribution Feeders & Auto-Reclosing',
          ansi: 'ANSI 50/51 / 51N / 79',
          rows: [
            ['Feeder CT Ratio', `${fdrCtPri}:5 A | Nominal Load ≈ ${iFdrFl} A (${distKv} kV)`],
            ['51-F1..F4 Curve', `Pickup = ${fdrPickupLv} A | IEEE VI, TDS = 0.70 (Fast Clear)`],
            ['50-F1 / 51N Ground', `50P Inst = ${fdrInstLv} A | 51N Residual = 160 A, TDS 0.45`],
            ['79 Auto-Recloser', `1 Fast + 2 Delayed Shots (0.5 s, 5 s, 15 s) -> Lockout`]
          ]
        },
        {
          id: 'ind_21_51',
          badge: `${indKv} kV INDUSTRIAL`,
          title: '6. Dedicated Industrial Sub-Tx Feeder (52-IND)',
          ansi: 'ANSI 21-IND / 50/51-IND',
          rows: [
            ['Sub-Tx Tap Rating', `${indKv} kV Direct Feed → 52-CUST (${indRatedMva} MVA, FLA = ${iIndFl} A)`],
            ['51-IND Phase OC', `Pickup = ${indPickupHv} A @ ${indKv}kV | IEEE VI, TDS = 1.55`],
            ['50-IND / 21-IND Dist.', `50P Inst = ${indInstHv} A | Z1 Reach = 80% North ROW Line`],
            ['Upstream Backup', `51-HV Stage-1 Backup coordinated >= 0.30 s CTI above 52-IND`]
          ]
        }
      ];

      return {
        vs, top, pf, sz, distKv, indKv, iHvFl, iLvFl, iFdrFl, iIndFl,
        hvCtPri, lvCtPri, fdrCtPri, brkHvAmp, brkLvAmp, brkKa, busbarSpec,
        fdrPickupLv, fdrInstLv, lvMainPickupLv,
        indPickupHv, indInstHv, indPickupLv, indInstLv,
        hvBackupPickupHv, hvBackupRefLv,
        cards
      };
    }

    function toggleProtectionZone3D(relayKey) {
      const targetKey = (relayKey && relayKey !== 'all') ? relayKey : '21';
      AppState.activeProtectionZone3D = (AppState.activeProtectionZone3D === targetKey) ? null : targetKey;
      const L = getBusLayoutConfig(AppState.busTopology, AppState.voltageClass);
      if (switchyardObjects.protectionOverlay && scene) {
        scene.remove(switchyardObjects.protectionOverlay);
      }
      if (scene) {
        switchyardObjects.protectionOverlay = AppState.activeProtectionZone3D
          ? buildProtectionZoneOverlay(scene, L, AppState.activeProtectionZone3D)
          : null;
      }
      renderAnalysisModalBody();
    }

    function jumpToProtectionZone3D(relayKey) {
      const targetKey = (relayKey && relayKey !== 'all') ? relayKey : '21';
      AppState.activeProtectionZone3D = targetKey;
      const L = getBusLayoutConfig(AppState.busTopology, AppState.voltageClass);
      if (switchyardObjects.protectionOverlay && scene) {
        scene.remove(switchyardObjects.protectionOverlay);
      }
      if (scene) {
        switchyardObjects.protectionOverlay = buildProtectionZoneOverlay(scene, L, targetKey);
      }
      if (typeof closeAnalysisModal === 'function') closeAnalysisModal();
      const presetMap = {
        '21': 'ctvt',
        '87B': 'busbar',
        '87T': 'transformer',
        '50_51_lv': 'secondary',
        '51G': 'transformer',
        '50_51_f1': 'feeders',
        'recloser': 'recloser'
      };
      setCameraPreset(presetMap[targetKey] || 'overview', true);
    }

    function renderRelayElementarySvg(relayKey, sched) {
      const key = (relayKey && relayKey !== 'all') ? relayKey : '21';
      const vs = sched.vs;
      const ngrIp = Math.max(20, Math.round((vs.lvKv * 1000 / Math.sqrt(3) / Math.max(1, vs.ngrOhms)) * 0.15));
      const specMap = {
        '21': {
          title: 'ANSI 21 / 67 / 50 — Incoming Line Distance & Directional Relay Schematic',
          ctText: `CT/VT-69 (${sched.hvCtPri}:5 A, ${(vs.hvKv * 1000 / 115).toFixed(0)}:1 VT)`,
          ctSub: `3-Phase Ia/Ib/Ic + Va/Vb/Vc Polarization`,
          relayName: 'SEL-411L LINE RELAY (BAY 1)',
          logicText: `Z1 = ${(0.80 * (vs.hvKv * vs.hvKv / 180)).toFixed(2)} Ω (0 cyc) | 67/51 = ${Math.round(sched.iHvFl * 1.65)} A`,
          tripCoil: '52-69 SF6 Breaker TC1/TC2',
          backup: '50BF (0.15 s) -> Retrip + 86B Bus Lockout'
        },
        '87B': {
          title: `ANSI 87B — High-Speed Busbar Differential & Breaker Failure (${LAND_TOPO_FACTORS[sched.top].label})`,
          ctText: `Multi-Terminal Bus CTs (${sched.hvCtPri}:5 A C800)`,
          ctSub: `Kirchhoff Nodal Sum |Σ I_in - Σ I_out|`,
          relayName: 'SEL-487B BUS DIFF (BAY 2)',
          logicText: `Slope 1 = 25% | Slope 2 = 60% | Iop > 0.20 pu (1.5 cyc)`,
          tripCoil: 'All HV Bus CBs + 86B Lockout Relay',
          backup: '50BF Check Zone -> Remote Line Transfer Trip'
        },
        '87T': {
          title: `ANSI 87T / 63 — Power Transformer TR-01 (${vs.mva} MVA ${vs.vectorGroup}) Differential`,
          ctText: `HV (${sched.hvCtPri}:5 A) + LV (${sched.lvCtPri}:5 A) CTs`,
          ctSub: `Dyn11 Software Vector & Zero-Seq Comp`,
          relayName: 'SEL-487E XFMR DIFF (BAY 3)',
          logicText: `Slopes 25%/50% | 2nd Harm Block >= 15% + 63/49 Trip`,
          tripCoil: '52-69 HV + 52-LV Main (Dual 86T Lockout)',
          backup: '51-HV Backup OC (' + sched.hvBackupPickupHv + ' A) + Tap Lockout'
        },
        '50_51_lv': {
          title: `ANSI 50/51-LV — ${vs.lvKv} kV Secondary Main VCB Overcurrent Protection`,
          ctText: `CT/VT-LV Secondary Bus (${sched.lvCtPri}:5 A C400)`,
          ctSub: `Phase Overcurrent Sensing + Bus VT Undervoltage`,
          relayName: 'SEL-751 MAIN RELAY (BAY 4)',
          logicText: `51-LV = ${sched.lvMainPickupLv} A (IEEE VI, TDS 1.25) | CTI >= 0.30 s`,
          tripCoil: '52-LV Main Vacuum Breaker TC',
          backup: '50BF (0.15 s) -> Trips Upstream 52-69 HV CB'
        },
        '51G': {
          title: `ANSI 51G / 64REF — Transformer X0 Neutral NGR (${vs.ngrOhms} Ω) Ground Protection`,
          ctText: `NGR Window CT (400:5 A Zero-Sequence)`,
          ctSub: `TR-01 X0 Bushing -> NGR-01 -> Station Grid`,
          relayName: 'SEL-751G NEUTRAL RELAY (BAY 4)',
          logicText: `51G Pickup = ${ngrIp} A (IEC SI, TDS 0.8) + 64REF Check`,
          tripCoil: '52-LV Main + 52-69 HV Isolation',
          backup: 'Prevents X0 Core Burning (Limited < 400 A Fault)'
        },
        '50_51_f1': {
          title: `ANSI 50/51/79-F1 — Outgoing ${vs.lvKv} kV Feeder 01 Overcurrent & Auto-Reclose`,
          ctText: `Fdr-01 Bushing CTs (${sched.fdrCtPri}:5 A)`,
          ctSub: `3I Phase + 3I0 Residual Ground Sensing`,
          relayName: 'SEL-751 FEEDER RELAY (BAY 5)',
          logicText: `51-F1 = ${sched.fdrPickupLv} A (TDS 0.70) | 79 Shots: 0.5/5/15 s`,
          tripCoil: '52-F1 Vacuum Feeder Breaker TC',
          backup: '50BF -> Trips 52-LV Main Bus Incomer'
        },
        'recloser': {
          title: `ANSI 79-ACR1 / 34-SECT / 100K — Distribution Fuse-Saving & FLISR Loop Control`,
          ctText: `79-ACR1 Internal CTs/VTs + 34-SECT Sensor`,
          ctSub: `Pole 1 Mainline Recloser + Pole 2 Sectionalizer`,
          relayName: 'SEL-651R POLE CONTROL (LOCAL)',
          logicText: `2 Fast (A) + 2 Slow (B/C) | 34-SECT Arm 160 A, 2 Counts`,
          tripCoil: '79-ACR1 Vacuum Actuator + 79-TIE FLISR Transfer',
          backup: 'Saves 100K Lateral Fuse on Transient Faults; Isolates Permanent'
        }
      };
      const cfg = specMap[key] || specMap['21'];
      return `
        <div class="relay-schematic-box">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:6px;">
            <strong style="font-size:11.5px; color:#e0f2fe;">🔌 ${cfg.title}</strong>
            <span style="font-size:10px; color:#94a3b8; font-family:monospace;">125 V DC Station Battery Supervised Trip Loop</span>
          </div>
          <svg viewBox="0 0 760 170" width="100%" style="display:block; background:#020617; border:1px solid rgba(56,189,248,0.22); border-radius:6px;">
            <defs>
              <marker id="arrCy" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#38bdf8"/></marker>
              <marker id="arrRd" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#f87171"/></marker>
              <marker id="arrVi" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#c084fc"/></marker>
            </defs>
            <!-- Block 1: Instrument Transformers (CT/VT) -->
            <rect x="14" y="20" width="208" height="86" rx="6" fill="rgba(8,47,73,0.72)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="118" y="39" fill="#7dd3fc" font-size="10.5" font-weight="700" text-anchor="middle">1. YARD CT / VT SENSING</text>
            <text x="118" y="58" fill="#f8fafc" font-size="10" font-weight="600" text-anchor="middle">${cfg.ctText}</text>
            <text x="118" y="76" fill="#cbd5e1" font-size="9.2" text-anchor="middle">${cfg.ctSub}</text>
            <text x="118" y="95" fill="#38bdf8" font-size="9" font-family="monospace" text-anchor="middle">AC 5A / 115V Analog Leads</text>

            <!-- Arrow CT -> Relay -->
            <line x1="222" y1="63" x2="266" y2="63" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrCy)"/>
            <text x="244" y="55" fill="#38bdf8" font-size="8.5" font-weight="700" text-anchor="middle">AC I/V</text>

            <!-- Block 2: Control House Relay Rack -->
            <rect x="270" y="20" width="222" height="86" rx="6" fill="rgba(69,26,3,0.68)" stroke="#f59e0b" stroke-width="1.6"/>
            <text x="381" y="39" fill="#fcd34d" font-size="10.5" font-weight="700" text-anchor="middle">2. CONTROL HOUSE RELAY</text>
            <text x="381" y="58" fill="#fef3c7" font-size="10.2" font-weight="700" text-anchor="middle">${cfg.relayName}</text>
            <text x="381" y="76" fill="#fde68a" font-size="9" text-anchor="middle">${cfg.logicText}</text>
            <text x="381" y="95" fill="#f59e0b" font-size="8.8" font-family="monospace" text-anchor="middle">Output Contact 52T -> Close on Fault</text>

            <!-- Arrow Relay -> Trip Coil -->
            <line x1="492" y1="63" x2="536" y2="63" stroke="#f87171" stroke-width="2.2" marker-end="url(#arrRd)"/>
            <text x="514" y="55" fill="#fca5a5" font-size="8.5" font-weight="700" text-anchor="middle">125V DC</text>

            <!-- Block 3: 125V DC Trip Coil & Breaker -->
            <rect x="540" y="20" width="206" height="86" rx="6" fill="rgba(69,10,10,0.72)" stroke="#f87171" stroke-width="1.5"/>
            <text x="643" y="39" fill="#fca5a5" font-size="10.5" font-weight="700" text-anchor="middle">3. BREAKER TRIP COIL (52T)</text>
            <text x="643" y="58" fill="#ffffff" font-size="10" font-weight="600" text-anchor="middle">${cfg.tripCoil}</text>
            <text x="643" y="76" fill="#fecaca" font-size="9" text-anchor="middle">125 V DC Station Battery + 86 Lockout</text>
            <text x="643" y="95" fill="#f87171" font-size="8.8" font-family="monospace" text-anchor="middle">Target Break Time: 2–3 Cycles</text>

            <!-- 125V DC Battery & 50BF Backup Bus along Bottom -->
            <rect x="14" y="122" width="170" height="34" rx="5" fill="rgba(15,23,42,0.9)" stroke="#94a3b8" stroke-width="1.2"/>
            <text x="99" y="137" fill="#e2e8f0" font-size="9.5" font-weight="700" text-anchor="middle">🔋 125 V DC STATION BATTERY</text>
            <text x="99" y="150" fill="#94a3b8" font-size="8.5" text-anchor="middle">+ / - Trip Bus + Coil Monitor</text>

            <path d="M 184 139 L 381 139 L 381 106" fill="none" stroke="#f87171" stroke-width="1.4" stroke-dasharray="4 3"/>

            <rect x="414" y="122" width="332" height="34" rx="5" fill="rgba(59,7,100,0.55)" stroke="#c084fc" stroke-width="1.2"/>
            <text x="580" y="137" fill="#e9d5ff" font-size="9.5" font-weight="700" text-anchor="middle">🛡️ BACKUP / 50BF BREAKER FAILURE PATH</text>
            <text x="580" y="150" fill="#d8b4fe" font-size="8.8" text-anchor="middle">${cfg.backup}</text>
            <line x1="643" y1="106" x2="643" y2="122" stroke="#c084fc" stroke-width="1.5" marker-end="url(#arrVi)"/>
          </svg>
        </div>
      `;
    }

    function evaluateTccAtCurrent(Iamp, sched, topo, refSide, splitContingency) {
      const kScale = (refSide === 'hv') ? ((sched.vs.distKv || 13.8) / sched.vs.hvKv) : 1.0;
      const toPlotA = (ampLv) => ampLv * kScale;

      const fdrIp = toPlotA(sched.fdrPickupLv);
      const fdrInst = toPlotA(sched.fdrInstLv);
      const lvIp = toPlotA(sched.lvMainPickupLv);
      const indIp = toPlotA(sched.indPickupLv || sched.lvMainPickupLv * 0.75);
      const indInst = toPlotA(sched.indInstLv || sched.fdrInstLv * 1.4);
      const hvIp = toPlotA(sched.hvBackupRefLv);
      const recIp = fdrIp * 0.48;
      const sectArmIp = toPlotA(160);

      // 0. Distribution Fuse-Saving & Lateral 100K Fuse Curves (79-ACR1 Fast / 100K Fuse / 79-ACR1 Slow)
      const mRec = Iamp / Math.max(1, recIp);
      let tRecFast = null;
      if (mRec >= 1.15) {
        tRecFast = Math.max(0.028, Math.min(25, 0.065 / (Math.pow(mRec, 0.95) - 1) + 0.018));
      }
      const iFuseEq = mRec * 312;
      let tFuseMin = null;
      let tFuseClear = null;
      if (iFuseEq >= 210) {
        tFuseMin = Math.max(0.018, 220000 / Math.pow(iFuseEq - 120, 1.85));
        tFuseClear = tFuseMin * 1.68;
      }
      const tRecSlow = ieeeTccTime(Iamp, recIp * 1.15, 0.50, 'VI');

      // 1. Feeder 50/51-F1 curve (instantaneous ceiling at fdrInst)
      let tFdr = ieeeTccTime(Iamp, fdrIp, 0.70, 'VI');
      if (Iamp >= fdrInst) tFdr = 0.035;

      // 2. LV Main 50/51-LV curve + 2b. Dedicated Industrial 50/51-IND curve (21-IND)
      let tLv = ieeeTccTime(Iamp, lvIp, 1.25, 'VI');
      if (Iamp >= lvIp * 8.5) tLv = 0.055;
      let tInd = ieeeTccTime(Iamp, indIp, 1.55, 'VI');
      if (Iamp >= indInst) tInd = 0.05;

      // 3. Topology-dependent Primary/Bus Backup curve:
      // Ring & Double-Breaker split fault/load current across parallel paths (higher effective pickup per branch leg
      // before summing at TR-01), collapsing to 1.0x under N-1 single-path contingency.
      let branchFactor = 1.0;
      let topoTds = 2.20;
      let topoCurveLabel = '51-HV + 87T/87B Backup';
      if (topo === 'maintransfer') {
        topoTds = 2.05;
        topoCurveLabel = '51-BT Transfer Tie / 51-HV';
      } else if (topo === 'ring') {
        branchFactor = splitContingency ? 1.0 : 1.45;
        topoTds = 2.00;
        topoCurveLabel = splitContingency ? '67/51 Ring (N-1 Single Leg)' : '67/51 Ring (2-Leg Loop Split)';
      } else if (topo === 'breakerhalf') {
        branchFactor = splitContingency ? 1.0 : 1.30;
        topoTds = 2.10;
        topoCurveLabel = splitContingency ? '1.5 CB Tee (N-1 Tie Open)' : '1.5 CB 52-TIE / 87B-A/B';
      } else if (topo === 'doublebreaker') {
        branchFactor = splitContingency ? 1.0 : 1.55;
        topoTds = 1.95;
        topoCurveLabel = splitContingency ? '2.0 CB Single-Bus N-1 Mode' : '2.0 CB Parallel Bus A+B Split';
      }
      let tTopo = ieeeTccTime(Iamp, hvIp * branchFactor, topoTds, 'VI');
      // 87B / 87T instantaneous high-speed bus/transformer differential floor at high multiples
      const diffThresh = hvIp * 4.5;
      if (Iamp >= diffThresh && topo !== 'single') {
        // dashed/step indicator handled on canvas; backup IDMT remains above
      }

      // 4. IEEE C57.109 Liquid-Immersed Transformer Thermal/Mechanical Damage Curve (Δ-Y 0.58x shift for SLG safety)
      const iBaseTx = toPlotA(sched.iLvFl);
      const iDmgMult = (Iamp / Math.max(1, iBaseTx)) / 0.58;
      let tDmg = null;
      if (iDmgMult >= 2.0) {
        // I^2 * t = 1250 -> t = 1250 / (I_pu^2), clamped between 2s @ 25pu and 1800s @ 2pu
        tDmg = Math.min(900, Math.max(1.2, 1250 / (iDmgMult * iDmgMult)));
      }

      const cti12 = (tFdr != null && tLv != null) ? (tLv - tFdr) : null;
      const cti23 = (tLv != null && tTopo != null) ? (tTopo - tLv) : null;

      return {
        fdrIp, fdrInst, lvIp, indIp, indInst, hvIp, recIp, sectArmIp, branchFactor, topoCurveLabel,
        tRecFast, tFuseMin, tFuseClear, tRecSlow,
        tFdr, tLv, tInd, tTopo, tDmg,
        cti12, cti23
      };
    }

    function setTccControl(key, val) {
      if (!AppState.tccState) return;
      if (key === 'topo') AppState.tccState.topo = val;
      else if (key === 'clearPin') AppState.tccState.pinnedFault = null;
      else if (key === 'refSide') {
        const oldSide = AppState.tccState.refSide;
        if (oldSide !== val) {
          const vs = getVoltageSpec(AppState.voltageClass);
          const ratio = vs.hvKv / (vs.distKv || vs.lvKv || 13.8);
          AppState.tccState.cursorAmp = Math.round(val === 'hv' ? (AppState.tccState.cursorAmp / ratio) : (AppState.tccState.cursorAmp * ratio));
          if (AppState.tccState.pinnedFault && AppState.tccState.pinnedFault.iAmpsPlot) {
            AppState.tccState.pinnedFault.iAmpsPlot = Math.round(val === 'hv' ? (AppState.tccState.pinnedFault.iAmpsPlot / ratio) : (AppState.tccState.pinnedFault.iAmpsPlot * ratio));
          }
          AppState.tccState.refSide = val;
        }
      } else if (key === 'splitContingency') {
        AppState.tccState.splitContingency = !!val;
      } else if (key === 'cursorAmp') {
        AppState.tccState.cursorAmp = Math.max(40, Math.min(90000, Number(val) || 4200));
      } else if (key === 'focusedRelay') {
        AppState.tccState.focusedRelay = val;
        if (val !== 'all' && (!AppState.tccState.viewMode || AppState.tccState.viewMode === 'all')) {
          AppState.tccState.viewMode = 'highlight';
        }
      } else if (key === 'viewMode') {
        AppState.tccState.viewMode = val;
        if ((val === 'highlight' || val === 'isolate') && (!AppState.tccState.focusedRelay || AppState.tccState.focusedRelay === 'all')) {
          AppState.tccState.focusedRelay = '50_51_f1';
        }
      }
      renderAnalysisModalBody();
    }

    function renderTccCoordinationTab(body) {
      const ts = AppState.tccState || { topo: AppState.busTopology, refSide: 'lv', splitContingency: false, cursorAmp: 4200, focusedRelay: 'all', viewMode: 'highlight', pinnedFault: null };
      if (!ts.viewMode) ts.viewMode = 'highlight';
      AppState.tccState = ts;
      const topo = ts.topo || AppState.busTopology || 'single';
      const sched = computeRelaySettingsSchedule(AppState.voltageClass, topo);
      const pin = ts.pinnedFault || null;
      const evalAmp = pin && pin.iAmpsPlot ? pin.iAmpsPlot : ts.cursorAmp;
      const ev = evaluateTccAtCurrent(evalAmp, sched, topo, ts.refSide, ts.splitContingency);

      const refKv = ts.refSide === 'hv' ? sched.vs.hvKv : (sched.vs.distKv || sched.vs.lvKv);
      const cti12Ok = (ev.cti12 === null || ev.cti12 >= 0.25);
      const cti23Ok = (ev.cti23 === null || ev.cti23 >= 0.25);
      const dmgOk = (ev.tDmg === null || ev.tTopo === null || ev.tTopo < ev.tDmg);
      const allPass = cti12Ok && cti23Ok && dmgOk;

      const verdictHtml = allPass
        ? `<div class="tcc-verdict-banner">✅ <strong>SELECTIVE COORDINATION VERIFIED (CTI ≥ 0.25–0.35 s):</strong> <span style="color:#a7f3d0;">Feeder 51-F1 clears ahead of 51-LV; ${ev.topoCurveLabel} backs up below IEEE C57.109 TR-01 damage curve at ${evalAmp.toLocaleString()} A (${refKv} kV base).</span></div>`
        : `<div class="tcc-verdict-banner miscoord">⚠️ <strong>MISCOORDINATION / OVERLAP DETECTED:</strong> <span style="color:#fecdd3;">Check Δt margins (51-LV/51-F1 Δt=${ev.cti12!==null?ev.cti12.toFixed(2)+'s':'N/A'} | HV/LV Δt=${ev.cti23!==null?ev.cti23.toFixed(2)+'s':'N/A'}). Switch to N-1 / adjust Fault Cursor to inspect IEEE 242 Buff Book margin.</span></div>`;

      const seqCandidates = [
        ['79-ACR1 Fast (A)', '#a855f7', ev.tRecFast],
        ['100K Lateral Fuse Clear', '#fb923c', ev.tFuseClear],
        ['79-ACR1 Slow (B/C)', '#e879f9', ev.tRecSlow],
        ['50/51-F1 Feeder CB', '#4ade80', ev.tFdr],
        ['50/51-IND Sub-Tx CB', '#34d399', ev.tInd],
        ['50/51-LV Main VCB', '#fbbf24', ev.tLv],
        [ev.topoCurveLabel, '#38bdf8', ev.tTopo]
      ].filter(([, , t]) => t !== null && t !== undefined).sort((a, b) => a[2] - b[2]);

      const seqRowsHtml = seqCandidates.length
        ? seqCandidates.map(([name, col, t], idx) => {
            const nextT = idx + 1 < seqCandidates.length ? seqCandidates[idx + 1][2] : null;
            const cti = nextT !== null ? +(nextT - t).toFixed(3) : null;
            return `<tr><td style="color:${col};font-weight:700;">t${idx+1}: ${name}</td><td style="font-family:monospace;color:#f8fafc;">${t.toFixed(3)} s</td><td style="font-family:monospace;color:#fde68a;">${(t * 60).toFixed(1)} cyc</td><td style="font-family:monospace;color:${cti!==null?(cti>=0.25?'#34d399':'#fbbf24'):'#94a3b8'};">${cti!==null?('+'+cti.toFixed(3)+' s'):'Backup'}</td></tr>`;
          }).join('')
        : '<tr><td colspan="4" style="color:#94a3b8;">Below Relay Pickup — Increase I_fault</td></tr>';

      const pinBannerHtml = pin ? `
        <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:8px; padding:7px 10px; margin-bottom:8px; background:rgba(127,29,29,0.45); border:1px solid #f43f5e; border-radius:6px; font-size:10.8px;">
          <div>
            <strong style="color:#fef08a;">📌 ACTIVE PINNED FAULT ON TCC:</strong>
            <span style="color:#fecdd3;">${pin.nodeLabel} · <strong>${(pin.faultType||'3ph').toUpperCase()}</strong> · I<sub>f,sym</sub> = <strong style="color:#fff;">${pin.iSymKa.toFixed(2)} kA (${pin.iAmpsPlot.toLocaleString()} A @ ${refKv} kV)</strong></span>
          </div>
          <button class="tcc-topo-pill" onclick="setTccControl('clearPin',true)" style="border-color:#fda4af;color:#fecdd3;">Clear Fault Pin</button>
        </div>
      ` : '';

      const activeRelayKey = (ts.focusedRelay && ts.focusedRelay !== 'all') ? ts.focusedRelay : '21';
      const relayCardGroupMap = {
        '21': 'line_21_87b', '87B': 'line_21_87b', '87T': 'tx_87t', '50_51_lv': 'tx_87t',
        '51G': 'tx_87t', '50_51_f1': 'fdr_50_51', 'recloser': 'fdr_50_51',
        'ind_21_51': 'ind_21_51', 'line_21_87b': 'line_21_87b', 'tx_87t': 'tx_87t', 'fdr_50_51': 'fdr_50_51'
      };
      const focusedGroup = relayCardGroupMap[ts.focusedRelay] || null;
      const relayButtons = [
        ['21', '21 Line Dist'], ['87B', '87B Bus Diff'], ['87T', '87T Xfmr Diff'],
        ['50_51_lv', '50/51-LV Main'], ['51G', '51G X0 NGR'], ['50_51_f1', '50/51-F1 Feeder'],
        ['recloser', '79-ACR1 / 34-SECT']
      ];
      const zoneActive = (AppState.activeProtectionZone3D === activeRelayKey);
      const fuseSaveOk = (ev.tRecFast !== null && ev.tFuseMin !== null && ev.tFuseClear !== null && ev.tRecSlow !== null)
        ? (ev.tRecFast < ev.tFuseMin && ev.tFuseClear < ev.tRecSlow && (ev.tFdr === null || ev.tRecSlow < ev.tFdr))
        : null;

      body.innerHTML = `
        ${pinBannerHtml}
        <div class="tcc-topo-bar">
          <span style="font-size:10.5px; color:#94a3b8; font-weight:700; margin-right:4px;">SCHEME:</span>
          ${Object.keys(LAND_TOPO_FACTORS).map(k => `
            <button class="tcc-topo-pill ${topo === k ? 'active' : ''}" onclick="setTccControl('topo','${k}')">${LAND_TOPO_FACTORS[k].label}</button>
          `).join('')}
          <span style="margin-left:auto; display:flex; gap:6px; align-items:center;">
            <button class="tcc-topo-pill ${ts.refSide==='lv'?'active':''}" onclick="setTccControl('refSide','lv')">Ref: ${sched.distKv} kV LV</button>
            <button class="tcc-topo-pill ${ts.refSide==='hv'?'active':''}" onclick="setTccControl('refSide','hv')">Ref: ${sched.vs.hvKv} kV HV</button>
            <button class="tcc-topo-pill ${ts.splitContingency?'active':''}" onclick="setTccControl('splitContingency', ${!ts.splitContingency})" title="Toggle N-1 single-branch outage on Ring / 1.5 CB / 2.0 CB">${ts.splitContingency ? 'N-1 Single-Path ON' : 'Normal Parallel Flow'}</button>
          </span>
        </div>

        <div class="tcc-topo-bar" style="margin-bottom:8px; border-color:rgba(250,204,21,0.28);">
          <span style="font-size:10px; color:#fde047; font-weight:700; margin-right:4px;">CURVE FOCUS:</span>
          <button class="tcc-topo-pill ${(ts.viewMode!=='all' && ts.viewMode!=='isolate' && ts.focusedRelay && ts.focusedRelay!=='all') ? 'active' : ''}" onclick="setTccControl('viewMode','highlight')">Highlight Selected Relay</button>
          <button class="tcc-topo-pill ${(ts.viewMode==='isolate' && ts.focusedRelay && ts.focusedRelay!=='all') ? 'active' : ''}" onclick="setTccControl('viewMode','isolate')">Isolate Selected Relay Only</button>
          <button class="tcc-topo-pill ${(ts.viewMode==='all' || !ts.focusedRelay || ts.focusedRelay==='all') ? 'active' : ''}" onclick="setTccControl('focusedRelay','all')">Show All Curves</button>
          <span style="margin-left:auto; display:flex; flex-wrap:wrap; gap:4px; align-items:center;">
            ${[['all','All'], ...relayButtons].map(([rk, rlbl]) => `
              <button class="tcc-topo-pill ${((ts.focusedRelay||'all') === rk) ? 'active' : ''}" onclick="setTccControl('focusedRelay','${rk}')" style="font-size:9.5px; padding:2px 7px;">${rlbl}</button>
            `).join('')}
          </span>
        </div>

        <div class="tcc-lab-layout">
          <div>
            <div class="tcc-canvas-wrap">
              <canvas id="tcc-loglog-canvas" width="600" height="400" style="width:100%; height:auto; display:block; cursor:ew-resize;"></canvas>
            </div>
            <div style="margin-top:8px; display:flex; align-items:center; gap:10px; background:rgba(15,23,42,0.8); padding:7px 10px; border-radius:6px; border:1px solid rgba(56,189,248,0.2);">
              <span style="font-size:10.5px; color:#cbd5e1; white-space:nowrap;">🎯 Drag Canvas or Slide <strong>I<sub>fault</sub> (${refKv} kV)</strong>:</span>
              <input type="range" min="200" max="35000" step="100" value="${Math.min(35000, ts.cursorAmp)}" style="flex:1;" oninput="setTccControl('cursorAmp', this.value)">
              <strong style="font-family:monospace; color:#fef08a; font-size:11.5px; min-width:68px; text-align:right;">${ts.cursorAmp.toLocaleString()} A</strong>
            </div>
          </div>

          <div class="analysis-panel" style="display:flex; flex-direction:column; gap:7px;">
            <h4>Sequence of Operation @ ${evalAmp.toLocaleString()} A (${refKv} kV)</h4>
            <div class="analysis-kpi-grid">
              <div class="analysis-kpi"><span>50/51-F1 Feeder Clear</span><strong style="color:#4ade80;">${ev.tFdr !== null ? ev.tFdr.toFixed(3)+' s' : 'NO PICKUP'}</strong></div>
              <div class="analysis-kpi"><span>50/51-LV Main Clear</span><strong style="color:#fbbf24;">${ev.tLv !== null ? ev.tLv.toFixed(3)+' s' : 'NO PICKUP'}</strong></div>
              <div class="analysis-kpi"><span>${ev.topoCurveLabel}</span><strong style="color:#38bdf8;">${ev.tTopo !== null ? ev.tTopo.toFixed(3)+' s' : 'NO PICKUP'}</strong></div>
              <div class="analysis-kpi"><span>IEEE C57.109 TR-01 Limit</span><strong style="color:#f87171;">${ev.tDmg !== null ? ev.tDmg.toFixed(2)+' s' : '> 900 s'}</strong></div>
            </div>

            <div style="background:rgba(2,6,23,0.85); border:1px solid rgba(56,189,248,0.25); border-radius:6px; padding:6px 8px;">
              <div style="font-size:10px; font-weight:700; color:#7dd3fc; margin-bottom:4px;">⚡ Operating Point Trip Times &amp; CTI Table (60 Hz)</div>
              <table class="relay-schedule-table" style="width:100%; font-size:9.8px;">
                <thead><tr style="color:#94a3b8; border-bottom:1px solid rgba(148,163,184,0.2);"><td>Device Curve</td><td>t_op</td><td>Cycles</td><td>CTI Next</td></tr></thead>
                <tbody>${seqRowsHtml}</tbody>
              </table>
            </div>

            <div style="background:rgba(2,6,23,0.75); border:1px solid rgba(148,163,184,0.2); border-radius:6px; padding:6px 9px; font-size:10px; line-height:1.45;">
              <div style="display:flex; justify-content:space-between;">
                <span style="color:#d8b4fe;">79-ACR1 Fast vs 100K Fuse:</span>
                <strong style="color:${fuseSaveOk===false?'#f87171':'#a855f7'}; font-family:monospace;">${ev.tRecFast!==null?ev.tRecFast.toFixed(3)+'s':'—'} &lt; ${ev.tFuseMin!==null?ev.tFuseMin.toFixed(3)+'s':'—'}</strong>
              </div>
              <div style="display:flex; justify-content:space-between;">
                <span style="color:#fdba74;">100K Clear vs 79-ACR1 Slow:</span>
                <strong style="color:${fuseSaveOk===false?'#f87171':'#e879f9'}; font-family:monospace;">${ev.tFuseClear!==null?ev.tFuseClear.toFixed(3)+'s':'—'} &lt; ${ev.tRecSlow!==null?ev.tRecSlow.toFixed(3)+'s':'—'}</strong>
              </div>
              <div style="margin-top:3px; color:#cbd5e1;">
                <em>Branch Share:</em> <strong>${ev.branchFactor.toFixed(2)}×</strong> · <span style="color:#94a3b8;">Mode: ${(sched.sz&&sched.sz.mode||'autosize').toUpperCase()} (${sched.lvCtPri}:5 CT)</span>
              </div>
            </div>

            <div style="font-size:9.8px; color:#94a3b8; line-height:1.45;">
              <strong style="color:#e2e8f0;">Legend:</strong>
              <span style="color:#a855f7;">┈ 79-ACR1 Fast</span> ·
              <span style="color:#fb923c;">■ 100K Fuse</span> ·
              <span style="color:#4ade80;">■ 51-F1</span> ·
              <span style="color:#34d399;">■ 51-IND</span> ·
              <span style="color:#fbbf24;">■ 51-LV</span> ·
              <span style="color:#38bdf8;">■ ${ev.topoCurveLabel}</span>
            </div>
          </div>
        </div>

        ${verdictHtml}

        <div style="margin-top:12px;">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:6px; margin-bottom:6px;">
            <span style="font-size:11px; color:#f8fafc; font-weight:700;">🔌 Relay Connection &amp; 125V DC Trip Schematic (CT/VT -> SEL Relay -> 52T):</span>
            <div style="display:flex; flex-wrap:wrap; gap:5px; align-items:center;">
              <button class="btn-zone-3d ${zoneActive ? 'active' : ''}" onclick="toggleProtectionZone3D('${activeRelayKey}')">${zoneActive ? '✅ 3D Zone Overlay ON (Hide)' : '🎯 Highlight Protection Zone in 3D Yard'}</button>
              <button class="btn-zone-3d" style="background:rgba(14,116,144,0.35); border-color:#22d3ee; color:#cffafe;" onclick="jumpToProtectionZone3D('${activeRelayKey}')">👁 View Zone in 3D Yard</button>
            </div>
          </div>
          <div class="tcc-topo-bar" style="margin-bottom:8px;">
            <span style="font-size:10px; color:#94a3b8; font-weight:700; margin-right:4px;">SELECT RELAY:</span>
            ${relayButtons.map(([rk, rlbl]) => `
              <button class="tcc-topo-pill ${activeRelayKey === rk ? 'active' : ''}" onclick="setTccControl('focusedRelay','${rk}')">${rlbl}</button>
            `).join('')}
          </div>
          ${renderRelayElementarySvg(activeRelayKey, sched)}
        </div>

        <div style="margin-top:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <h4 style="margin:0; font-size:12px; color:#f8fafc;">📋 Complete Protective Relay Settings Schedule (${sched.vs.hvKv}/${sched.distKv} kV · ${LAND_TOPO_FACTORS[topo].label})</h4>
            ${ts.focusedRelay && ts.focusedRelay !== 'all' ? `<button class="btn" style="padding:3px 8px; font-size:10px;" onclick="setTccControl('focusedRelay','all')">Show All Panels Unfiltered</button>` : ''}
          </div>
          <div class="relay-card-grid">
            ${sched.cards.map(c => `
              <div class="relay-setting-card ${(focusedGroup === c.id || ts.focusedRelay === c.id) ? 'focused' : ''}" onclick="setTccControl('focusedRelay','${c.id}')" style="cursor:pointer;" title="Click to Highlight/Isolate Relay Curve on TCC Plot">
                <h5><span>${c.title}</span><span class="relay-badge">${c.badge}</span></h5>
                <div style="font-size:10px; color:#fbbf24; font-family:monospace; margin-bottom:5px; font-weight:700;">${c.ansi}</div>
                <table class="relay-schedule-table">
                  <tbody>
                    ${c.rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join('')}
                  </tbody>
                </table>
              </div>
            `).join('')}
          </div>
        </div>
      `;

      const canvas = document.getElementById('tcc-loglog-canvas');
      if (canvas) {
        drawTccLogLogCanvas(canvas, sched, topo, ts);
        let dragging = false;
        const updateFromEvent = (e) => {
          const rect = canvas.getBoundingClientRect();
          const px = ((e.clientX - rect.left) / Math.max(1, rect.width)) * canvas.width;
          const padL = 56, padR = 18;
          const plotW = canvas.width - padL - padR;
          const logMinI = 1.6, logMaxI = 5.0;
          const frac = Math.max(0, Math.min(1, (px - padL) / plotW));
          const amp = Math.round(Math.pow(10, logMinI + frac * (logMaxI - logMinI)));
          setTccControl('cursorAmp', amp);
        };
        canvas.onpointerdown = (e) => { dragging = true; updateFromEvent(e); };
        canvas.onpointermove = (e) => { if (dragging) updateFromEvent(e); };
        window.addEventListener('pointerup', () => { dragging = false; }, { once: false });
      }
    }

    function drawTccLogLogCanvas(canvas, sched, topo, ts) {
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      const W = canvas.width, H = canvas.height;
      const padL = 56, padR = 18, padT = 22, padB = 38;
      const plotW = W - padL - padR, plotH = H - padT - padB;
      const logMinI = 1.6, logMaxI = 5.0;   // 40 A .. 100,000 A
      const logMinT = -2.0, logMaxT = 3.0;  // 0.01 s .. 1,000 s

      const xOfI = (amp) => padL + ((Math.log10(Math.max(10, amp)) - logMinI) / (logMaxI - logMinI)) * plotW;
      const yOfT = (sec) => padT + ((logMaxT - Math.log10(Math.max(0.01, Math.min(1000, sec)))) / (logMaxT - logMinT)) * plotH;

      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, W, H);

      // Log-Log Decade & Minor Gridlines
      for (let d = 1; d <= 5; d++) {
        for (let m = 1; m <= 9; m++) {
          const val = m * Math.pow(10, d);
          const lg = Math.log10(val);
          if (lg < logMinI || lg > logMaxI) continue;
          const x = padL + ((lg - logMinI) / (logMaxI - logMinI)) * plotW;
          ctx.strokeStyle = (m === 1) ? 'rgba(56,189,248,0.22)' : 'rgba(51,65,85,0.25)';
          ctx.lineWidth = (m === 1) ? 1.1 : 0.6;
          ctx.beginPath(); ctx.moveTo(x, padT); ctx.lineTo(x, padT + plotH); ctx.stroke();
          if (m === 1) {
            ctx.fillStyle = '#94a3b8';
            ctx.font = '10px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(val >= 1000 ? `${val/1000}kA` : `${val}A`, x, padT + plotH + 14);
          }
        }
      }
      for (let d = -2; d <= 3; d++) {
        for (let m = 1; m <= 9; m++) {
          const val = m * Math.pow(10, d);
          const lg = Math.log10(val);
          if (lg < logMinT || lg > logMaxT) continue;
          const y = padT + ((logMaxT - lg) / (logMaxT - logMinT)) * plotH;
          ctx.strokeStyle = (m === 1) ? 'rgba(56,189,248,0.22)' : 'rgba(51,65,85,0.25)';
          ctx.lineWidth = (m === 1) ? 1.1 : 0.6;
          ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(padL + plotW, y); ctx.stroke();
          if (m === 1) {
            ctx.fillStyle = '#94a3b8';
            ctx.font = '10px monospace';
            ctx.textAlign = 'right';
            ctx.fillText(val < 1 ? `${val}s` : `${val}s`, padL - 6, y + 3);
          }
        }
      }

      // Axis Titles
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 10.5px sans-serif';
      ctx.textAlign = 'center';
      const refKv = ts.refSide === 'hv' ? sched.vs.hvKv : sched.vs.lvKv;
      ctx.fillText(`Symmetrical Current I (Amperes, Referred to ${refKv} kV) — Log Scale`, padL + plotW / 2, H - 6);
      ctx.save();
      ctx.translate(14, padT + plotH / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText('Operating Time t (Seconds) — Log Scale', 0, 0);
      ctx.restore();

      const focusKey = (ts && ts.focusedRelay) ? ts.focusedRelay : 'all';
      const viewMode = (focusKey === 'all' || !ts || ts.viewMode === 'all')
        ? 'all'
        : (ts.viewMode === 'isolate' ? 'isolate' : 'highlight');
      const focusCurveMap = {
        recloser: ['recFast', 'fuseMin', 'fuseClear', 'recSlow', 'sect'],
        fdr_50_51: ['fdr', 'recFast', 'fuseMin', 'fuseClear', 'recSlow', 'sect'],
        '50_51_f1': ['fdr'],
        '50_51_lv': ['lv', 'dmg'],
        '51G': ['lv', 'dmg'],
        '21': ['topo', 'dmg'],
        line_21_87b: ['topo', 'diff', 'dmg'],
        '87T': ['diff', 'dmg'],
        '87B': ['diff', 'dmg'],
        tx_87t: ['diff', 'dmg', 'lv']
      };
      const activeCurveList = focusCurveMap[focusKey] || null;
      const isFocusedCurve = (key) => (viewMode === 'all' || !activeCurveList || activeCurveList.includes(key));

      const plotCurve = (curveKey, color, dashed, width, fn) => {
        const focused = isFocusedCurve(curveKey);
        if (viewMode === 'isolate' && !focused) return;
        ctx.save();
        ctx.strokeStyle = color;
        if (viewMode === 'highlight' && !focused) {
          ctx.globalAlpha = 0.20;
          ctx.lineWidth = Math.max(1.2, width * 0.55);
        } else if (viewMode !== 'all' && focused) {
          ctx.globalAlpha = 1.0;
          ctx.lineWidth = 4.0;
          ctx.shadowColor = color;
          ctx.shadowBlur = 9;
        } else {
          ctx.lineWidth = width;
        }
        if (dashed) ctx.setLineDash([6, 4]);
        ctx.beginPath();
        let started = false;
        for (let i = 0; i <= 220; i++) {
          const amp = Math.pow(10, logMinI + (i / 220) * (logMaxI - logMinI));
          const t = fn(amp);
          if (t === null || t === undefined || t > 1000 || t < 0.01) {
            started = false;
            continue;
          }
          const px = xOfI(amp), py = yOfT(t);
          if (!started) { ctx.moveTo(px, py); started = true; }
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.restore();
      };

      const evAt = (amp) => evaluateTccAtCurrent(amp, sched, topo, ts.refSide, ts.splitContingency);
      // Curve 0A: Pole Recloser 79-ACR1 Fast Curve A (Violet Dashed)
      plotCurve('recFast', '#a855f7', true, 2.0, (a) => evAt(a).tRecFast);
      // Curve 0B: Lateral Cutout Fuse 100K Min Melt (Orange Dashed) & Total Clear (Orange Solid)
      plotCurve('fuseMin', '#fb923c', true, 1.8, (a) => evAt(a).tFuseMin);
      plotCurve('fuseClear', '#fb923c', false, 2.1, (a) => evAt(a).tFuseClear);
      // Curve 0C: Pole Recloser 79-ACR1 Slow Curve B/C (Magenta Solid)
      plotCurve('recSlow', '#e879f9', false, 2.1, (a) => evAt(a).tRecSlow);
      // Curve 1: Feeder 50/51-F1 (Green)
      plotCurve('fdr', '#4ade80', false, 2.4, (a) => evAt(a).tFdr);
      // Curve 1B: Dedicated Industrial 50/51-IND (Emerald Dashed)
      plotCurve('ind', '#34d399', true, 1.9, (a) => evAt(a).tInd);
      // Curve 2: LV Main 50/51-LV (Amber)
      plotCurve('lv', '#fbbf24', false, 2.4, (a) => evAt(a).tLv);
      // Curve 3: Topology-specific Primary / Bus Backup (Cyan)
      plotCurve('topo', '#38bdf8', false, 2.4, (a) => evAt(a).tTopo);
      // Curve 4: IEEE C57.109 TR-01 Thermal/Mechanical Damage Curve (Red Dashed)
      plotCurve('dmg', '#f87171', true, 2.1, (a) => evAt(a).tDmg);

      // 87B/87T High-Speed Differential Floor Line (Purple Dashed)
      const diffFocused = isFocusedCurve('diff');
      if (viewMode !== 'isolate' || diffFocused) {
        ctx.save();
        if (viewMode === 'highlight' && !diffFocused) ctx.globalAlpha = 0.20;
        else if (viewMode !== 'all' && diffFocused) {
          ctx.lineWidth = 3.2;
          ctx.shadowColor = '#c084fc';
          ctx.shadowBlur = 8;
        }
        ctx.strokeStyle = '#c084fc';
        ctx.lineWidth = (viewMode !== 'all' && diffFocused) ? 3.2 : 1.6;
        ctx.setLineDash([4, 3]);
        const yDiff = yOfT(0.025);
        ctx.beginPath(); ctx.moveTo(padL, yDiff); ctx.lineTo(padL + plotW, yDiff); ctx.stroke();
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#d8b4fe';
        ctx.font = 'bold 9.5px monospace';
        ctx.textAlign = 'left';
        ctx.fillText('87T / 87B Differential High-Speed Trip (0.025 s)', padL + 6, yDiff - 5);
        ctx.restore();
      }

      // 34-SECT Electronic Sectionalizer Minimum Actuating Arming Line (Cyan Vertical Dashed)
      const curEv = evAt(ts.cursorAmp);
      const sectFocused = isFocusedCurve('sect');
      if (viewMode !== 'isolate' || sectFocused) {
        const sectX = xOfI(curEv.sectArmIp);
        ctx.save();
        if (viewMode === 'highlight' && !sectFocused) ctx.globalAlpha = 0.20;
        ctx.strokeStyle = '#22d3ee';
        ctx.lineWidth = (viewMode !== 'all' && sectFocused) ? 2.6 : 1.5;
        ctx.setLineDash([4, 3]);
        ctx.beginPath(); ctx.moveTo(sectX, padT + 18); ctx.lineTo(sectX, padT + plotH); ctx.stroke();
        ctx.fillStyle = '#67e8f9';
        ctx.font = 'bold 9px monospace';
        ctx.textAlign = 'left';
        ctx.fillText(`34-SECT (ANSI 34) Arm=${Math.round(curEv.sectArmIp)}A | Cnt=2`, sectX + 4, padT + 26);
        ctx.restore();
      }

      // Active Relay Pickup (Ip) Asymptote, Instantaneous (50) Threshold, & Technical Callout Box
      if (viewMode !== 'all') {
        const relayMeta = {
          '50_51_f1': { label: '50/51-F1 Feeder Relay', col: '#4ade80', ip: curEv.fdrIp, inst: curEv.fdrInst, tds: '0.70 (VI)', top: curEv.tFdr },
          fdr_50_51:  { label: '50/51-F1 + 79-ACR1',   col: '#4ade80', ip: curEv.fdrIp, inst: curEv.fdrInst, tds: '0.70 (VI)', top: curEv.tFdr },
          recloser:   { label: '79-ACR1 + 100K + 34-SECT', col: '#a855f7', ip: curEv.recIp, inst: null, tds: 'A=Fast / B=0.50', top: curEv.tRecFast },
          '50_51_lv': { label: '50/51-LV Main Breaker', col: '#fbbf24', ip: curEv.lvIp, inst: curEv.lvIp * 8.5, tds: '1.25 (VI)', top: curEv.tLv },
          '51G':      { label: '51G X0 Neutral Ground', col: '#fbbf24', ip: curEv.lvIp, inst: null, tds: '1.25 (VI)', top: curEv.tLv },
          '21':       { label: curEv.topoCurveLabel, col: '#38bdf8', ip: curEv.hvIp * curEv.branchFactor, inst: curEv.hvIp * 4.5, tds: `VI (${curEv.branchFactor.toFixed(2)}x)`, top: curEv.tTopo },
          line_21_87b:{ label: curEv.topoCurveLabel, col: '#38bdf8', ip: curEv.hvIp * curEv.branchFactor, inst: curEv.hvIp * 4.5, tds: `VI (${curEv.branchFactor.toFixed(2)}x)`, top: curEv.tTopo },
          '87T':      { label: '87T Xfmr Differential', col: '#c084fc', ip: curEv.hvIp * 4.5, inst: curEv.hvIp * 4.5, tds: '0.025 s (High-Spd)', top: 0.025 },
          '87B':      { label: '87B Bus Differential', col: '#c084fc', ip: curEv.hvIp * 4.5, inst: curEv.hvIp * 4.5, tds: '0.025 s (High-Spd)', top: 0.025 },
          tx_87t:     { label: '87T + C57.109 Backup', col: '#c084fc', ip: curEv.lvIp, inst: curEv.hvIp * 4.5, tds: '0.025 s / C57.109', top: 0.025 }
        }[focusKey];

        if (relayMeta) {
          const clampX = (px) => Math.max(padL + 2, Math.min(padL + plotW - 2, px));
          if (relayMeta.ip) {
            const ipX = clampX(xOfI(relayMeta.ip));
            ctx.save();
            ctx.strokeStyle = relayMeta.col;
            ctx.lineWidth = 1.6;
            ctx.setLineDash([3, 3]);
            ctx.beginPath(); ctx.moveTo(ipX, padT); ctx.lineTo(ipX, padT + plotH); ctx.stroke();
            ctx.fillStyle = relayMeta.col;
            ctx.font = 'bold 9.5px monospace';
            ctx.textAlign = ipX > padL + plotW - 78 ? 'right' : 'left';
            ctx.fillText(`Ip=${Math.round(relayMeta.ip)}A`, ipX + (ipX > padL + plotW - 78 ? -4 : 4), padT + plotH - 8);
            ctx.restore();
          }
          if (relayMeta.inst) {
            const instX = clampX(xOfI(relayMeta.inst));
            ctx.save();
            ctx.strokeStyle = '#f43f5e';
            ctx.lineWidth = 1.6;
            ctx.setLineDash([2, 3]);
            ctx.beginPath(); ctx.moveTo(instX, padT + 14); ctx.lineTo(instX, padT + plotH); ctx.stroke();
            ctx.fillStyle = '#fda4af';
            ctx.font = 'bold 9px monospace';
            ctx.textAlign = instX > padL + plotW - 82 ? 'right' : 'left';
            ctx.fillText(`50=${Math.round(relayMeta.inst)}A`, instX + (instX > padL + plotW - 82 ? -4 : 4), padT + plotH - 22);
            ctx.restore();
          }
          const boxW = 205, boxH = 62;
          const bx = padL + plotW - boxW - 8, by = padT + 8;
          ctx.save();
          ctx.fillStyle = 'rgba(2, 6, 23, 0.90)';
          ctx.strokeStyle = relayMeta.col;
          ctx.lineWidth = 1.4;
          ctx.fillRect(bx, by, boxW, boxH);
          ctx.strokeRect(bx, by, boxW, boxH);
          ctx.fillStyle = relayMeta.col;
          ctx.font = 'bold 10px monospace';
          ctx.textAlign = 'left';
          ctx.fillText(`${viewMode === 'isolate' ? 'ISOLATE' : 'FOCUS'}: ${relayMeta.label}`, bx + 7, by + 15);
          ctx.fillStyle = '#e2e8f0';
          ctx.font = '9.5px monospace';
          ctx.fillText(`Ip: ${Math.round(relayMeta.ip)}A | TDS: ${relayMeta.tds}`, bx + 7, by + 31);
          ctx.fillText(`Inst 50: ${relayMeta.inst ? Math.round(relayMeta.inst) + 'A' : 'N/A'}`, bx + 7, by + 44);
          ctx.fillStyle = '#fef08a';
          ctx.fillText(`t_op @ ${ts.cursorAmp}A: ${relayMeta.top !== null && relayMeta.top !== undefined ? relayMeta.top.toFixed(3) + ' s' : 'NO PICKUP'}`, bx + 7, by + 57);
          ctx.restore();
        }
      }

      // Interactive Vertical Fault Current Cursor + Live Intersection Dots & CTI Dimension Arrow
      const cx = xOfI(ts.cursorAmp);
      ctx.save();
      ctx.strokeStyle = '#fef08a';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([5, 3]);
      ctx.beginPath(); ctx.moveTo(cx, padT); ctx.lineTo(cx, padT + plotH); ctx.stroke();
      ctx.restore();

      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 10px monospace';
      ctx.textAlign = cx > W - 95 ? 'right' : 'left';
      ctx.fillText(`If=${ts.cursorAmp.toLocaleString()}A`, cx + (cx > W - 95 ? -5 : 5), padT + 13);

      const pts = [];
      if (curEv.tRecFast !== null)   pts.push({ key: 'recFast',   t: curEv.tRecFast,   col: '#a855f7', r: 3.5 });
      if (curEv.tFuseMin !== null)   pts.push({ key: 'fuseMin',   t: curEv.tFuseMin,   col: '#fb923c', r: 3.5 });
      if (curEv.tFuseClear !== null) pts.push({ key: 'fuseClear', t: curEv.tFuseClear, col: '#fdba74', r: 3.5 });
      if (curEv.tRecSlow !== null)   pts.push({ key: 'recSlow',   t: curEv.tRecSlow,   col: '#e879f9', r: 3.5 });
      if (curEv.tFdr !== null)       pts.push({ key: 'fdr',       t: curEv.tFdr,       col: '#4ade80', r: 4.5 });
      if (curEv.tLv !== null)        pts.push({ key: 'lv',        t: curEv.tLv,        col: '#fbbf24', r: 4.5 });
      if (curEv.tTopo !== null)      pts.push({ key: 'topo',      t: curEv.tTopo,      col: '#38bdf8', r: 4.5 });

      pts.forEach(pt => {
        const focused = isFocusedCurve(pt.key);
        if (viewMode === 'isolate' && !focused) return;
        const py = yOfT(pt.t);
        ctx.save();
        if (viewMode === 'highlight' && !focused) ctx.globalAlpha = 0.25;
        ctx.fillStyle = pt.col;
        ctx.beginPath(); ctx.arc(cx, py, (viewMode !== 'all' && focused) ? (pt.r + 1.4) : (pt.r || 4.5), 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#020617'; ctx.lineWidth = 1.4; ctx.stroke();
        ctx.restore();
      });

      if ((viewMode !== 'isolate' || (isFocusedCurve('fdr') && isFocusedCurve('lv'))) && curEv.tFdr !== null && curEv.tLv !== null && curEv.tLv > curEv.tFdr) {
        const y1 = yOfT(curEv.tFdr), y2 = yOfT(curEv.tLv);
        ctx.save();
        if (viewMode === 'highlight' && !(isFocusedCurve('fdr') || isFocusedCurve('lv'))) ctx.globalAlpha = 0.25;
        ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(cx + 9, y1); ctx.lineTo(cx + 9, y2); ctx.stroke();
        ctx.fillStyle = '#a7f3d0'; ctx.font = 'bold 9.5px monospace'; ctx.textAlign = 'left';
        ctx.fillText(`Δt=${curEv.cti12.toFixed(2)}s`, cx + 13, (y1 + y2) / 2 + 3);
        ctx.restore();
      }
      if ((viewMode !== 'isolate' || (isFocusedCurve('lv') && isFocusedCurve('topo'))) && curEv.tLv !== null && curEv.tTopo !== null && curEv.tTopo > curEv.tLv) {
        const y1 = yOfT(curEv.tLv), y2 = yOfT(curEv.tTopo);
        ctx.save();
        if (viewMode === 'highlight' && !(isFocusedCurve('lv') || isFocusedCurve('topo'))) ctx.globalAlpha = 0.25;
        ctx.strokeStyle = '#7dd3fc'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(cx - 9, y1); ctx.lineTo(cx - 9, y2); ctx.stroke();
        ctx.fillStyle = '#7dd3fc'; ctx.font = 'bold 9.5px monospace'; ctx.textAlign = 'right';
        ctx.fillText(`Δt=${curEv.cti23.toFixed(2)}s`, cx - 13, (y1 + y2) / 2 + 3);
        ctx.restore();
      }

      // Active Pinned Fault Line & Labeled Operating Point Dots (I_fault, t_trip)
      const pin = ts && ts.pinnedFault ? ts.pinnedFault : null;
      if (pin && pin.iAmpsPlot > 0) {
        const fx = Math.max(padL + 2, Math.min(padL + plotW - 2, xOfI(pin.iAmpsPlot)));
        const pinEv = evAt(pin.iAmpsPlot);
        ctx.save();
        ctx.strokeStyle = '#f43f5e';
        ctx.lineWidth = 2.4;
        ctx.shadowColor = '#f43f5e';
        ctx.shadowBlur = 10;
        ctx.setLineDash([7, 4]);
        ctx.beginPath(); ctx.moveTo(fx, padT); ctx.lineTo(fx, padT + plotH); ctx.stroke();
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#f43f5e';
        ctx.font = 'bold 10px monospace';
        ctx.textAlign = fx > padL + plotW - 140 ? 'right' : 'left';
        ctx.fillText(`⚡ FAULT ${pin.iSymKa.toFixed(2)} kA (${(pin.faultType||'3ph').toUpperCase()})`, fx + (fx > padL + plotW - 140 ? -6 : 6), padT + 27);

        const opPts = [
          ['79A-F', pinEv.tRecFast, '#a855f7'],
          ['100K', pinEv.tFuseClear, '#fb923c'],
          ['51-F1', pinEv.tFdr, '#4ade80'],
          ['51-IND', pinEv.tInd, '#34d399'],
          ['51-LV', pinEv.tLv, '#fbbf24'],
          ['51-HV', pinEv.tTopo, '#38bdf8']
        ].filter(([, t]) => t !== null && t !== undefined);

        opPts.forEach(([tag, tVal, col], idx) => {
          const py = yOfT(tVal);
          ctx.fillStyle = col;
          ctx.beginPath(); ctx.arc(fx, py, 5.2, 0, Math.PI * 2); ctx.fill();
          ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.6; ctx.stroke();
          ctx.fillStyle = '#fef08a';
          ctx.font = 'bold 9px monospace';
          const onRight = fx < padL + plotW - 95;
          ctx.textAlign = onRight ? 'left' : 'right';
          ctx.fillText(`${tag}: ${tVal.toFixed(3)}s (${(tVal*60).toFixed(1)}c)`, fx + (onRight ? 8 : -8), py + ((idx % 2 === 0) ? -4 : 10));
        });
        ctx.restore();
      }
    }

    // POWER QUALITY (PQ) SIMULATION & LIVE 3-PHASE OSCILLOSCOPE / HARMONIC FFT ENGINE
    function selectPqScenario(scen) {
      AppState.pqState.scenario = scen;
      renderAnalysisModalBody();
    }

    const PQ_PROBE_NODES = [
      { id: 'ind_sub', label: 'Industrial Sub (69/138 kV)', short: 'IND-SUB', isHv: true, isDeltaHv: false, zScale: 0.85, w3: 0.10, w5: 1.25, w7: 1.28, w9: 0.05, w11: 1.35, w13: 1.30, w15: 0.04 },
      { id: 'cbd_bus', label: 'CBD / Hospital 750 kVA (13.8 kV)', short: 'CBD 750', isHv: false, isDeltaHv: false, zScale: 1.18, w3: 1.25, w5: 1.30, w7: 1.24, w9: 1.20, w11: 1.15, w13: 1.10, w15: 1.12 },
      { id: 'urd_pad', label: 'URD Subdivision 150 kVA 6x (13.8 kV)', short: 'URD 150', isHv: false, isDeltaHv: false, zScale: 1.08, w3: 1.18, w5: 0.96, w7: 0.88, w9: 1.14, w11: 0.82, w13: 0.78, w15: 1.06 },
      { id: 'res_50', label: 'RES 50 kVA Radial Lateral (13.8 kV)', short: 'RES 50', isHv: false, isDeltaHv: false, zScale: 1.32, w3: 1.08, w5: 0.68, w7: 0.60, w9: 1.04, w11: 0.55, w13: 0.50, w15: 0.95 },
      { id: 'bus_a_138', label: 'Sub A 13.8 kV Main Bus A (4-Wire)', short: 'Bus A 13.8', isHv: false, isDeltaHv: false, zScale: 1.00, w3: 1.00, w5: 1.00, w7: 1.00, w9: 1.00, w11: 1.00, w13: 1.00, w15: 1.00 },
      { id: 'tr01_pri_delta', label: 'TR-01 Primary Δ-Winding (HV Line)', short: 'TR-01 Δ HV', isHv: true, isDeltaHv: true, zScale: 0.36, w3: 0.00, w5: 0.38, w7: 0.36, w9: 0.00, w11: 0.34, w13: 0.32, w15: 0.00 },
      { id: 'bus_b_138', label: 'Sub B 13.8 kV Tie Bus B', short: 'Bus B 13.8', isHv: false, isDeltaHv: false, zScale: 0.96, w3: 0.72, w5: 0.76, w7: 0.74, w9: 0.68, w11: 0.70, w13: 0.66, w15: 0.62 }
    ];

    window.attachPqProbeToNode = function(nodeKey) {
      if (!PQ_PROBE_NODES.some(n => n.id === nodeKey)) return;
      AppState.pqState.probeNodeA = nodeKey;
      AppState.pqState.scenario = 'harmonics';
      if (typeof openAnalysisModal === 'function') openAnalysisModal('pq');
      const meta = PQ_PROBE_NODES.find(n => n.id === nodeKey);
      if (typeof showToast === 'function' && meta) {
        showToast('PQ Probe Ch.1 attached to ' + meta.label);
      }
    };

    window.updatePqProbeControl = function(key, val) {
      updatePqLabControl(key, val);
    };

    function updatePqLabControl(key, val) {
      const pq = AppState.pqState;
      if (key === 'detunedFilterOn' || key === 'saClampActive' || key === 'statcomActive' || key === 'oscPaused' || key === 'showOverlayB') {
        pq[key] = (val === true || val === 'true');
      } else if (key === 'eventMode' || key === 'transientType' || key === 'probeNodeA' || key === 'probeNodeB') {
        pq[key] = val;
      } else {
        pq[key] = parseFloat(val);
      }
      renderAnalysisModalBody();
    }

    function computePowerQualityMetrics() {
      const pq = AppState.pqState;
      const vs = getVoltageSpec(AppState.voltageClass);
      const pfBase = computePowerFlowMetrics();
      const branches = (typeof computeEnergizedBranches === 'function') ? computeEnergizedBranches() : null;
      const sLoad = pfBase.sLoadMva || (vs.mva * 0.72);
      const vNomKv = vs.lvKv;
      const iBaseA = pfBase.iLvA || (sLoad * 1000 / (Math.sqrt(3) * vNomKv));

      // Harmonics calculations (IEEE 519-2022 & IEEE C57.110 K-Factor) + 52-CAP Parallel Resonance
      const vfdScale = (pq.vfdLoadPct || 35) / 50;
      const filt3 = pq.detunedFilterOn ? 0.35 : 1.0;
      const filt5 = pq.detunedFilterOn ? 0.14 : 1.0;
      const filt7 = pq.detunedFilterOn ? 0.18 : 1.0;
      const filt11 = pq.detunedFilterOn ? 0.28 : 1.0;
      const filt9 = pq.detunedFilterOn ? 0.22 : 1.0;
      const filt13 = pq.detunedFilterOn ? 0.32 : 1.0;
      const filt15 = pq.detunedFilterOn ? 0.25 : 1.0;

      const baseH3 = (pq.h3Pct || 0) * vfdScale * filt3;
      const baseH5 = (pq.h5Pct || 0) * vfdScale * filt5;
      const baseH7 = (pq.h7Pct || 0) * vfdScale * filt7;
      const baseH9 = (pq.h3Pct || 0) * 0.36 * vfdScale * filt9;
      const baseH11 = (pq.h11Pct || 0) * vfdScale * filt11;
      const baseH13 = (pq.h11Pct || 0) * 0.62 * vfdScale * filt13;
      const baseH15 = (pq.h3Pct || 0) * 0.18 * vfdScale * filt15;

      const zPu = Math.max(0.04, vs.xPu || 0.08);
      const capBankClosed = branches ? !!branches.capBank : (AppState.switchStates ? (AppState.switchStates.cbCap !== false) : true);
      const capStageMvar = Math.max(0.9, pq.capStageMvar || 3.6);
      const activeCapMvar = capBankClosed ? capStageMvar : ((pq.scenario === 'pf' && pq.capStageMvar > 0) ? pq.capStageMvar : 0);
      const mvaScBus = (vs.mva || 25) / Math.max(0.05, zPu + 0.025);
      const hRes = activeCapMvar > 0 ? Math.sqrt(mvaScBus / activeCapMvar) : 0;
      const fResHz = hRes * 60;

      const resGain = (order, localScale) => {
        if (!capBankClosed && !(pq.scenario === 'pf' && pq.capStageMvar > 0)) return 1.0;
        if (pq.detunedFilterOn) return 1.0; // p=7% detuned reactor shifts parallel resonance below 5th harmonic (~189 Hz)
        const hrLocal = Math.sqrt((mvaScBus / Math.max(0.6, localScale)) / Math.max(0.45, activeCapMvar));
        const ratio = order / Math.max(1.5, hrLocal);
        const damping = 0.28;
        const mag = 1.0 / Math.sqrt(Math.pow(1 - ratio * ratio, 2) + Math.pow(damping * ratio, 2));
        return Math.min(3.4, Math.max(1.0, mag));
      };

      const isNodeEnergized = (id) => {
        if (!branches) return true;
        if (id === 'ind_sub') return branches.ind_hv !== false;
        if (id === 'tr01_pri_delta') return branches.tx_hv !== false;
        if (id === 'bus_a_138') return branches.sec_bus !== false;
        if (id === 'cbd_bus') return branches.dist_f2_main !== false;
        if (id === 'urd_pad') return branches.dist_f1_sec2 !== false;
        if (id === 'res_50') return branches.dist_lateral !== false;
        if (id === 'bus_b_138') return branches.subBLvEff !== false;
        return true;
      };

      const nodalResults = {};
      const nodalTable = [];
      let tr01DeltaTrapCircA = 0;

      PQ_PROBE_NODES.forEach(node => {
        const en = isNodeEnergized(node.id);
        const loopCoupleZ = (node.id === 'bus_b_138' && branches && branches.subB_lv_backfed_from_A) ? 1.28 : 1.0;
        const zEff = zPu * node.zScale * loopCoupleZ;
        const mult = en ? 1 : 0;

        // Apply 52-CAP parallel resonance amplification to positive/negative-seq non-triplens (5,7,11,13)
        // Triplens (3,9,15) are trapped in TR-01 closed Delta winding => 0% HV line-side pass-through at tr01_pri_delta
        const nh3 = +(baseH3 * node.w3 * mult).toFixed(2);
        const nh5 = +(baseH5 * node.w5 * (node.isDeltaHv ? 1.0 : resGain(5, node.zScale)) * mult).toFixed(2);
        const nh7 = +(baseH7 * node.w7 * (node.isDeltaHv ? 1.0 : resGain(7, node.zScale)) * mult).toFixed(2);
        const nh9 = +(baseH9 * node.w9 * mult).toFixed(2);
        const nh11 = +(baseH11 * node.w11 * (node.isDeltaHv ? 1.0 : resGain(11, node.zScale)) * mult).toFixed(2);
        const nh13 = +(baseH13 * node.w13 * (node.isDeltaHv ? 1.0 : resGain(13, node.zScale)) * mult).toFixed(2);
        const nh15 = +(baseH15 * node.w15 * mult).toFixed(2);

        const nThdI = Math.sqrt(nh3*nh3 + nh5*nh5 + nh7*nh7 + nh9*nh9 + nh11*nh11 + nh13*nh13 + nh15*nh15);
        const nThdV = Math.sqrt(
          Math.pow((nh3 / 100) * zEff * 3, 2) +
          Math.pow((nh5 / 100) * zEff * 5, 2) +
          Math.pow((nh7 / 100) * zEff * 7, 2) +
          Math.pow((nh9 / 100) * zEff * 9, 2) +
          Math.pow((nh11 / 100) * zEff * 11, 2) +
          Math.pow((nh13 / 100) * zEff * 13, 2) +
          Math.pow((nh15 / 100) * zEff * 15, 2)
        ) * 100;
        const ni1Sq = 1.0;
        const nSumSq = ni1Sq + Math.pow(nh3/100,2) + Math.pow(nh5/100,2) + Math.pow(nh7/100,2) + Math.pow(nh9/100,2) + Math.pow(nh11/100,2) + Math.pow(nh13/100,2) + Math.pow(nh15/100,2);
        const nKf = (ni1Sq + Math.pow(nh3/100,2)*9 + Math.pow(nh5/100,2)*25 + Math.pow(nh7/100,2)*49 + Math.pow(nh9/100,2)*81 + Math.pow(nh11/100,2)*121 + Math.pow(nh13/100,2)*169 + Math.pow(nh15/100,2)*225) / nSumSq;
        const nKvStr = node.isHv ? (vs.hvKv + ' kV') : (vNomKv.toFixed(1) + ' kV');
        const nodeBaseA = node.isHv ? (pfBase.iHvA || (sLoad * 1000 / (Math.sqrt(3) * vs.hvKv))) : iBaseA;
        const triplenRmsPct = Math.sqrt(nh3*nh3 + nh9*nh9 + nh15*nh15);
        const nNeutralA = node.isHv ? 0 : (3 * (triplenRmsPct / 100) * nodeBaseA);
        const nDerate = Math.max(55, 100 - (nKf - 1) * 1.45);

        if (node.id === 'tr01_pri_delta' && en) {
          // Zero-sequence triplen current trapped inside TR-01 Delta primary winding (referred via turns ratio)
          const lvTriplenA = 3 * (Math.sqrt(baseH3*baseH3 + baseH9*baseH9 + baseH15*baseH15) / 100) * iBaseA;
          tr01DeltaTrapCircA = +(lvTriplenA * (vNomKv / (Math.sqrt(3) * vs.hvKv))).toFixed(1);
        }

        const resObj = {
          ...node,
          energized: en,
          kvLabel: nKvStr,
          zEffPu: +zEff.toFixed(4),
          h3: nh3, h5: nh5, h7: nh7, h9: nh9, h11: nh11, h13: nh13, h15: nh15,
          thdI: +nThdI.toFixed(2),
          thdV: +nThdV.toFixed(2),
          kFactor: +nKf.toFixed(2),
          deratingPct: +nDerate.toFixed(1),
          iNeutralHarA: +nNeutralA.toFixed(1),
          iNeutralPctOfPhase: nodeBaseA > 0 ? +((nNeutralA / nodeBaseA) * 100).toFixed(1) : 0,
          triplenLinePassPct: node.isDeltaHv ? 0.0 : +triplenRmsPct.toFixed(2),
          ieee519Pass: nThdV <= 5.0
        };
        nodalResults[node.id] = resObj;
        nodalTable.push(resObj);
      });

      const activeNodeA = nodalResults[pq.probeNodeA] || nodalResults['bus_a_138'];
      const activeNodeB = nodalResults[pq.probeNodeB] || nodalResults['tr01_pri_delta'];
      const h3 = activeNodeA.h3;
      const h5 = activeNodeA.h5;
      const h7 = activeNodeA.h7;
      const h9 = activeNodeA.h9;
      const h11 = activeNodeA.h11;
      const h13 = activeNodeA.h13;
      const h15 = activeNodeA.h15;
      const thdI = activeNodeA.thdI;
      const thdV = activeNodeA.thdV;
      const kFactor = activeNodeA.kFactor;
      const deratingPct = activeNodeA.deratingPct;
      const iNeutralHarA = activeNodeA.iNeutralHarA;
      const iDeltaCircA = tr01DeltaTrapCircA;
      const capResonance = {
        active: capBankClosed || (pq.scenario === 'pf' && pq.capStageMvar > 0),
        detuned: !!pq.detunedFilterOn,
        capMvar: +activeCapMvar.toFixed(2),
        mvaScBus: +mvaScBus.toFixed(1),
        hRes: +hRes.toFixed(2),
        fResHz: +fResHz.toFixed(0),
        nearHarmonicHit: (!pq.detunedFilterOn && (capBankClosed || pq.capStageMvar > 0) && hRes > 4.1 && hRes < 14.5)
      };

      // PF & Cap Bank
      const pfOld = Math.max(0.65, Math.min(0.99, pq.nativePf || 0.78));
      const pMw = sLoad * pfOld;
      const qOld = pMw * Math.tan(Math.acos(pfOld));
      const qCap = pq.capStageMvar || 0;
      const qNew = qOld - qCap;
      const sNew = Math.hypot(pMw, qNew);
      const pfNew = pMw / Math.max(0.01, sNew);
      const pfLeadLag = qNew >= 0 ? 'lag' : 'lead';
      const phiOldDeg = Math.acos(pfOld) * (180 / Math.PI);
      const phiNewDeg = (qNew < 0 ? -1 : 1) * Math.acos(Math.min(1, pfNew)) * (180 / Math.PI);
      const mvaReleased = sLoad - sNew;
      const lossRedPct = (1 - Math.pow(pfOld / pfNew, 2)) * 100;
      const deltaVCapPct = (qCap / Math.max(1, vs.mva)) * (vs.xPu * 100);

      // Voltage Unbalance (NEMA MG-1)
      const vuf = pq.unbalancePct || 3.2;
      const iuf = vuf * 6.2;
      const motorDeratePct = vuf <= 1.0 ? 100 : Math.max(60, 100 - Math.pow(vuf, 2) * 2.1);
      const ngrNeutralA = (pq.singlePhaseLoadKw || 850) / (vNomKv / Math.sqrt(3));

      // Sag / Swell (ITIC curve)
      const isSag = pq.eventMode !== 'swell';
      const eventPu = isSag ? (pq.sagDepthPu || 0.72) : (pq.swellMagPu || 1.18);
      const cyc = pq.eventCycles || 3.5;
      const iticPass = isSag ? (eventPu >= 0.80 || (eventPu >= 0.70 && cyc <= 10)) : (eventPu <= 1.20 || (eventPu <= 1.35 && cyc <= 3));

      // Transients
      const isLightning = pq.transientType === 'lightning';
      const rawPeakPu = isLightning ? 4.8 : 2.35;
      const clampedPeakPu = pq.saClampActive ? (isLightning ? 2.15 : 1.52) : rawPeakPu;
      const ringFreqKhz = isLightning ? 45.0 : 1.45;

      // Flicker (IEEE 1453)
      const rawPst = 0.35 + (pq.eafSeverity || 60) / 38;
      const pst = pq.statcomActive ? rawPst * 0.28 : rawPst;
      const dvOverV = (0.4 + (pq.eafSeverity || 60) / 14) * (pq.statcomActive ? 0.25 : 1.0);

      return {
        pq, vs, vNomKv, iBaseA,
        h3, h5, h7, h9, h11, h13, h15, thdI, thdV, kFactor, deratingPct, iNeutralHarA,
        activeNodeA, activeNodeB, nodalResults, nodalTable, iDeltaCircA, capResonance,
        pfOld, pfNew, pfLeadLag, phiOldDeg, phiNewDeg, qOld, qCap, qNew, mvaReleased, lossRedPct, deltaVCapPct,
        vuf, iuf, motorDeratePct, ngrNeutralA,
        isSag, eventPu, cyc, iticPass,
        isLightning, rawPeakPu, clampedPeakPu, ringFreqKhz,
        pst, dvOverV
      };
    }

    function renderPqAnalysisTab(body) {
      const m = computePowerQualityMetrics();
      const pq = m.pq;
      const scenarios = [
        { id: 'sag_swell', label: '⚡ Voltage Sag / Swell' },
        { id: 'harmonics', label: '〰️ Harmonics & THD (IEEE 519)' },
        { id: 'pf_cap', label: '🔋 PF Correction & Cap Bank' },
        { id: 'unbalance', label: '⚖️ 3-Phase Unbalance' },
        { id: 'transients', label: '🌩️ Switching / Lightning Surge' },
        { id: 'flicker', label: '💡 Arc Furnace Flicker (1453)' }
      ];

      let controlsHtml = '';
      let diagHtml = '';
      let stdCheck = { pass: true, badge: 'COMPLIANT', note: '' };

      if (pq.scenario === 'sag_swell') {
        controlsHtml = `
          <div class="analysis-slider-row">
            <label>Event Mode</label>
            <div class="preset-grid" style="grid-template-columns:1fr 1fr;">
              <button class="btn-preset ${m.isSag?'active':''}" onclick="updatePqLabControl('eventMode','sag')">Voltage Sag (Fault Dip)</button>
              <button class="btn-preset ${!m.isSag?'active':''}" onclick="updatePqLabControl('eventMode','swell')">Voltage Swell (SLG Rise)</button>
            </div>
          </div>
          ${m.isSag ? `
          <div class="analysis-slider-row">
            <label>Sag Magnitude <span>${pq.sagDepthPu.toFixed(2)} p.u. (${(pq.sagDepthPu * m.vNomKv).toFixed(2)} kV)</span></label>
            <input type="range" min="0.10" max="0.90" step="0.02" value="${pq.sagDepthPu}" oninput="updatePqLabControl('sagDepthPu', this.value)">
          </div>` : `
          <div class="analysis-slider-row">
            <label>Swell Magnitude <span>${pq.swellMagPu.toFixed(2)} p.u. (${(pq.swellMagPu * m.vNomKv).toFixed(2)} kV)</span></label>
            <input type="range" min="1.10" max="1.40" step="0.02" value="${pq.swellMagPu}" oninput="updatePqLabControl('swellMagPu', this.value)">
          </div>`}
          <div class="analysis-slider-row">
            <label>Fault Clearing / Event Duration <span>${m.cyc.toFixed(1)} cycles (${(m.cyc * 16.67).toFixed(0)} ms)</span></label>
            <input type="range" min="0.5" max="30" step="0.5" value="${m.cyc}" oninput="updatePqLabControl('eventCycles', this.value)">
          </div>
        `;
        stdCheck = {
          pass: m.iticPass,
          badge: m.iticPass ? 'ITIC/CBEMA PASS' : (m.isSag ? 'ANSI 27 UNDERVOLTAGE TRIP' : 'ANSI 59 OVERVOLTAGE STRESS'),
          note: m.iticPass ? 'Sensitive VFD & PLC loads ride through inside IEEE 1159 / ITIC tolerance envelope.' : 'Exceeds ITIC ride-through duration — coordinate 50/51 instantaneous clearing speed.'
        };
        diagHtml = `
          <div class="analysis-kpi"><span>RMS Event Voltage</span><strong>${(m.eventPu * m.vNomKv).toFixed(2)} kV (${m.eventPu.toFixed(2)} pu)</strong></div>
          <div class="analysis-kpi"><span>Duration @ 60 Hz</span><strong>${m.cyc.toFixed(1)} cyc (${(m.cyc * 16.67).toFixed(1)} ms)</strong></div>
          <div class="analysis-kpi"><span>Relay Pickup Status</span><strong>${m.eventPu < 0.85 ? 'ANSI 27 (UV)' : (m.eventPu > 1.12 ? 'ANSI 59 (OV)' : 'Normal Band')}</strong></div>
          <div class="analysis-kpi"><span>ITIC Curve Margin</span><strong style="color:${m.iticPass?'#10b981':'#ef4444'};">${m.iticPass?'Within Immunity':'Outside Envelope'}</strong></div>
        `;
      } else if (pq.scenario === 'harmonics') {
        controlsHtml = `
          <div class="analysis-slider-row">
            <label>Nonlinear VFD / EV Charger Share <span>${pq.vfdLoadPct}%</span></label>
            <input type="range" min="0" max="100" step="5" value="${pq.vfdLoadPct}" oninput="updatePqLabControl('vfdLoadPct', this.value)">
          </div>
          <div class="analysis-slider-row">
            <label>Harmonic Injection (3rd / 5th / 7th / 11th %) <span>${pq.h3Pct}/${pq.h5Pct}/${pq.h7Pct}/${pq.h11Pct}%</span></label>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
              <input type="range" min="0" max="30" step="1" title="3rd Harmonic %" value="${pq.h3Pct}" oninput="updatePqLabControl('h3Pct', this.value)">
              <input type="range" min="0" max="35" step="1" title="5th Harmonic %" value="${pq.h5Pct}" oninput="updatePqLabControl('h5Pct', this.value)">
              <input type="range" min="0" max="25" step="1" title="7th Harmonic %" value="${pq.h7Pct}" oninput="updatePqLabControl('h7Pct', this.value)">
              <input type="range" min="0" max="18" step="1" title="11th Harmonic %" value="${pq.h11Pct}" oninput="updatePqLabControl('h11Pct', this.value)">
            </div>
          </div>
          <div class="analysis-slider-row">
            <label>4.7% Detuned Filter Trap &amp; 52-CAP Resonance
              <button class="btn" style="padding:3px 10px; font-size:10px; background:${pq.detunedFilterOn?'rgba(16,185,129,0.22)':'rgba(239,68,68,0.22)'};" onclick="updatePqLabControl('detunedFilterOn', ${!pq.detunedFilterOn})">
                ${pq.detunedFilterOn ? 'FILTER IN (DETUNED 189Hz)' : 'FILTER OUT (RESONANCE RISK)'}
              </button>
            </label>
          </div>
        `;
        const pass519 = m.thdV <= 5.0;
        const lvNeutralRef = (m.nodalResults && m.nodalResults.bus_a_138) ? m.nodalResults.bus_a_138 : m;
        stdCheck = {
          pass: pass519 && !m.capResonance.nearHarmonicHit,
          badge: pass519 ? (m.capResonance.nearHarmonicHit ? 'CAP RESONANCE RISK' : 'IEEE 519 PASS (THD_V ≤ 5%)') : 'IEEE 519 VIOLATION (THD_V > 5%)',
          note: m.activeNodeA.isDeltaHv
            ? `TR-01 Δ Primary isolates 100% of zero-sequence triplens (0.0% pass-through to ${m.vs.hvKv} kV HV source; ${m.iDeltaCircA.toFixed(1)} A trapped circulating inside Δ).`
            : `Node ${m.activeNodeA.short}: K-Factor = ${m.kFactor.toFixed(2)} (derating ${m.deratingPct.toFixed(1)}%). ${m.capResonance.active ? `52-CAP parallel resonance f_r = ${m.capResonance.fResHz} Hz (h=${m.capResonance.hRes}).` : '52-CAP OPEN (no parallel resonance).'}`
        };
        diagHtml = `
          <div class="analysis-kpi"><span>Voltage THD_V (${m.activeNodeA.short})</span><strong style="color:${pass519?'#10b981':'#ef4444'};">${m.thdV.toFixed(2)} % (Limit 5.0%)</strong></div>
          <div class="analysis-kpi"><span>Current THD_I (${m.activeNodeA.kvLabel})</span><strong>${m.thdI.toFixed(2)} %</strong></div>
          <div class="analysis-kpi"><span>TR-01 Δ-Winding Triplen Trap</span><strong style="color:#10b981;">HV Line 0.0% (${m.iDeltaCircA.toFixed(1)} A Δ-Circ)</strong></div>
          <div class="analysis-kpi"><span>13.8kV Neutral Overload (3×I_0h)</span><strong style="color:${lvNeutralRef.iNeutralPctOfPhase>65?'#f87171':'#fbbf24'};">${lvNeutralRef.iNeutralHarA.toFixed(0)} A (${lvNeutralRef.iNeutralPctOfPhase.toFixed(1)}% Iφ)</strong></div>
          <div class="analysis-kpi"><span>TR-01 K-Factor / Derating</span><strong>K-${m.kFactor.toFixed(2)} (${m.deratingPct.toFixed(1)}%)</strong></div>
          <div class="analysis-kpi"><span>52-CAP Parallel Resonance (f_r)</span><strong style="color:${m.capResonance.nearHarmonicHit?'#f87171':'#38bdf8'};">${m.capResonance.active ? (m.capResonance.detuned ? 'Detuned ~189 Hz' : `h=${m.capResonance.hRes} (${m.capResonance.fResHz} Hz)`) : '52-CAP OPEN'}</strong></div>
        `;
      } else if (pq.scenario === 'pf_cap') {
        controlsHtml = `
          <div class="analysis-slider-row">
            <label>Native Uncompensated PF <span>${m.pfOld.toFixed(2)} lag (φ=${m.phiOldDeg.toFixed(1)}°)</span></label>
            <input type="range" min="0.65" max="0.98" step="0.01" value="${m.pfOld}" oninput="updatePqLabControl('nativePf', this.value)">
          </div>
          <div class="analysis-slider-row">
            <label>Switched Shunt Capacitor (52-CAP)</label>
            <div class="preset-grid" style="grid-template-columns:repeat(4,1fr);">
              ${[0, 1.8, 3.6, 5.4].map(q => `<button class="btn-preset ${Math.abs(pq.capStageMvar-q)<0.1?'active':''}" onclick="updatePqLabControl('capStageMvar', ${q})">${q} MVAR</button>`).join('')}
            </div>
          </div>
        `;
        const pfPass = m.pfNew >= 0.90;
        stdCheck = {
          pass: pfPass,
          badge: pfPass ? 'PF ≥ 0.90 PENALTY-FREE' : 'LOW PF PENALTY RISK (<0.90)',
          note: `Phase shift Δφ corrected from ${m.phiOldDeg.toFixed(1)}° lag to ${m.phiNewDeg.toFixed(1)}° (${m.pfLeadLag}), releasing ${m.mvaReleased.toFixed(2)} MVA of TR-01 thermal capacity.`
        };
        diagHtml = `
          <div class="analysis-kpi"><span>Corrected Substation PF</span><strong style="color:${pfPass?'#10b981':'#f59e0b'};">${m.pfNew.toFixed(3)} ${m.pfLeadLag} (${m.phiNewDeg.toFixed(1)}°)</strong></div>
          <div class="analysis-kpi"><span>Cap Bank ΔV Voltage Rise</span><strong>+${m.deltaVCapPct.toFixed(2)} %</strong></div>
          <div class="analysis-kpi"><span>Released Capacity / Loss Δ</span><strong>${m.mvaReleased.toFixed(2)} MVA / -${m.lossRedPct.toFixed(1)}% I²R</strong></div>
          <div class="analysis-kpi"><span>Net Reactive Q_net</span><strong>${m.qNew.toFixed(2)} MVAR</strong></div>
        `;
      } else if (pq.scenario === 'unbalance') {
        controlsHtml = `
          <div class="analysis-slider-row">
            <label>Phase Voltage Unbalance (%VUF) <span>${m.vuf.toFixed(1)} %</span></label>
            <input type="range" min="0.5" max="6.0" step="0.1" value="${pq.unbalancePct}" oninput="updatePqLabControl('unbalancePct', this.value)">
          </div>
          <div class="analysis-slider-row">
            <label>1-Phase Lateral Imbalance Load <span>${pq.singlePhaseLoadKw} kW</span></label>
            <input type="range" min="0" max="2500" step="50" value="${pq.singlePhaseLoadKw}" oninput="updatePqLabControl('singlePhaseLoadKw', this.value)">
          </div>
        `;
        const vufPass = m.vuf <= 2.0;
        stdCheck = {
          pass: vufPass,
          badge: vufPass ? 'ANSI C84.1 / NEMA PASS (≤2%)' : 'NEMA MG-1 MOTOR DERATING (>2%)',
          note: `Negative-sequence V₂ produces ~6× current unbalance (${m.iuf.toFixed(1)}%), overheating 3-phase induction motors and driving ${m.ngrNeutralA.toFixed(0)} A into NGR.`
        };
        diagHtml = `
          <div class="analysis-kpi"><span>Voltage Unbalance (V₂/V₁)</span><strong style="color:${vufPass?'#10b981':'#ef4444'};">${m.vuf.toFixed(2)} %</strong></div>
          <div class="analysis-kpi"><span>Current Unbalance (IUF)</span><strong>${m.iuf.toFixed(1)} %</strong></div>
          <div class="analysis-kpi"><span>NEMA MG-1 Motor Rating</span><strong>${m.motorDeratePct.toFixed(1)} %</strong></div>
          <div class="analysis-kpi"><span>Neutral Current (NGR)</span><strong>${m.ngrNeutralA.toFixed(0)} A</strong></div>
        `;
      } else if (pq.scenario === 'transients') {
        controlsHtml = `
          <div class="analysis-slider-row">
            <label>Impulse / Switching Event</label>
            <div class="preset-grid" style="grid-template-columns:1fr 1fr;">
              <button class="btn-preset ${!m.isLightning?'active':''}" onclick="updatePqLabControl('transientType','cap_energize')">Cap Bank Energization (~1.45 kHz)</button>
              <button class="btn-preset ${m.isLightning?'active':''}" onclick="updatePqLabControl('transientType','lightning')">8/20 µs Lightning Surge (BIL)</button>
            </div>
          </div>
          <div class="analysis-slider-row">
            <label>ZnO Surge Arrester Clamping (SA-HV/LV)
              <button class="btn" style="padding:3px 10px; font-size:10px; background:${pq.saClampActive?'rgba(16,185,129,0.22)':'rgba(239,68,68,0.22)'};" onclick="updatePqLabControl('saClampActive', ${!pq.saClampActive})">
                ${pq.saClampActive ? 'MOV ARRESTER ACTIVE' : 'ARRESTER BYPASSED'}
              </button>
            </label>
          </div>
        `;
        const trPass = m.clampedPeakPu <= 2.3;
        stdCheck = {
          pass: trPass,
          badge: trPass ? 'BIL INSULATION PROTECTED' : 'INSULATION FLASHOVER HAZARD',
          note: pq.saClampActive ? `ZnO MOV clamps transient crest from ${m.rawPeakPu.toFixed(2)} p.u. down to ${m.clampedPeakPu.toFixed(2)} p.u. within TR-01 BIL margin.` : 'Unclamped overvoltage approaches switchgear BIL withstand!'
        };
        diagHtml = `
          <div class="analysis-kpi"><span>Transient Crest Voltage</span><strong style="color:${trPass?'#10b981':'#ef4444'};">${m.clampedPeakPu.toFixed(2)} p.u. (${(m.clampedPeakPu * m.vNomKv * 1.414 / 1.732).toFixed(1)} kVpk)</strong></div>
          <div class="analysis-kpi"><span>Dominant Ringing Freq</span><strong>${m.ringFreqKhz.toFixed(2)} kHz</strong></div>
          <div class="analysis-kpi"><span>Unclamped Surge Peak</span><strong>${m.rawPeakPu.toFixed(2)} p.u.</strong></div>
          <div class="analysis-kpi"><span>Arrester Protection</span><strong>${pq.saClampActive ? 'MOV Clamped' : 'Unprotected'}</strong></div>
        `;
      } else {
        controlsHtml = `
          <div class="analysis-slider-row">
            <label>Arc Furnace / Mill Load Fluctuation <span>${pq.eafSeverity}%</span></label>
            <input type="range" min="10" max="100" step="5" value="${pq.eafSeverity}" oninput="updatePqLabControl('eafSeverity', this.value)">
          </div>
          <div class="analysis-slider-row">
            <label>D-STATCOM / SVC Dynamic VAR Compensator
              <button class="btn" style="padding:3px 10px; font-size:10px; background:${pq.statcomActive?'rgba(16,185,129,0.22)':'rgba(239,68,68,0.22)'};" onclick="updatePqLabControl('statcomActive', ${!pq.statcomActive})">
                ${pq.statcomActive ? 'D-STATCOM ONLINE' : 'D-STATCOM OFF'}
              </button>
            </label>
          </div>
        `;
        const pstPass = m.pst <= 1.0;
        stdCheck = {
          pass: pstPass,
          badge: pstPass ? 'IEEE 1453 PASS (P_st ≤ 1.0)' : 'IRRITATING FLICKER (P_st > 1.0)',
          note: pq.statcomActive ? 'Fast IGBT D-STATCOM cancels reactive Q(t) swings inside 0.5 cycles, stabilizing bus P_st.' : '8 Hz sub-synchronous voltage envelope modulates lighting luminaires.'
        };
        diagHtml = `
          <div class="analysis-kpi"><span>Short-Term Flicker P_st</span><strong style="color:${pstPass?'#10b981':'#ef4444'};">${m.pst.toFixed(2)} (Limit 1.00)</strong></div>
          <div class="analysis-kpi"><span>Modulation Envelope ΔV/V</span><strong>${m.dvOverV.toFixed(2)} %</strong></div>
          <div class="analysis-kpi"><span>Flicker Band Frequency</span><strong>8.0 Hz Sub-Synchronous</strong></div>
          <div class="analysis-kpi"><span>Mitigation Unit</span><strong>${pq.statcomActive ? '±5 MVAR D-STATCOM ON' : 'Uncompensated'}</strong></div>
        `;
      }

      const probeBarHtml = `
        <div style="display:grid; grid-template-columns: 1.2fr 1.2fr auto; gap:8px; align-items:center; background:rgba(15,23,42,0.85); border:1px solid rgba(56,189,248,0.28); border-radius:8px; padding:8px 10px; margin-bottom:8px;">
          <div>
            <div style="font-size:9.5px; color:#38bdf8; font-weight:700; margin-bottom:2px;">CH.1 PRIMARY PQ PROBE NODE</div>
            <select style="width:100%; background:#0f172a; color:#f8fafc; border:1px solid #334155; border-radius:5px; padding:4px 6px; font-size:11px;" onchange="updatePqLabControl('probeNodeA', this.value)">
              ${PQ_PROBE_NODES.map(n => {
                const nr = m.nodalResults[n.id];
                return `<option value="${n.id}" ${pq.probeNodeA===n.id?'selected':''}>${n.short} (${nr.kvLabel}) — THD_V ${nr.energized ? nr.thdV.toFixed(2)+'%' : 'DE-EN'}</option>`;
              }).join('')}
            </select>
          </div>
          <div>
            <div style="font-size:9.5px; color:#e879f9; font-weight:700; margin-bottom:2px;">CH.2 REFERENCE OVERLAY NODE</div>
            <select style="width:100%; background:#0f172a; color:#f8fafc; border:1px solid #334155; border-radius:5px; padding:4px 6px; font-size:11px;" onchange="updatePqLabControl('probeNodeB', this.value)">
              ${PQ_PROBE_NODES.map(n => {
                const nr = m.nodalResults[n.id];
                return `<option value="${n.id}" ${pq.probeNodeB===n.id?'selected':''}>${n.short} (${nr.kvLabel}) — THD_V ${nr.energized ? nr.thdV.toFixed(2)+'%' : 'DE-EN'}</option>`;
              }).join('')}
            </select>
          </div>
          <div style="display:flex; flex-direction:column; gap:4px; align-items:flex-end;">
            <label style="display:flex; align-items:center; gap:5px; font-size:10.5px; color:#f0abfc; cursor:pointer; font-weight:700;">
              <input type="checkbox" ${pq.showOverlayB?'checked':''} onchange="updatePqLabControl('showOverlayB', this.checked)"> Overlay Ch.2 (Dashed)
            </label>
            <span style="font-size:9.5px; color:${m.activeNodeA.isDeltaHv?'#10b981':'#fbbf24'}; font-family:monospace;">
              ${m.activeNodeA.isDeltaHv ? 'Δ-Trap: 0.0% HV Triplen Pass' : `13.8kV Neutral: ${m.nodalResults.bus_a_138.iNeutralHarA.toFixed(0)} A`}
            </span>
          </div>
        </div>
      `;

      const nodalRowsHtml = m.nodalTable.map(nr => {
        const isA = nr.id === pq.probeNodeA;
        const isB = pq.showOverlayB && nr.id === pq.probeNodeB;
        const rowBg = isA ? 'rgba(56,189,248,0.14)' : (isB ? 'rgba(232,121,249,0.10)' : 'transparent');
        const badgeTag = isA ? '<span style="background:#0284c7;color:#fff;padding:1px 4px;border-radius:3px;font-size:8.5px;margin-right:4px;">CH1</span>' : (isB ? '<span style="background:#a21caf;color:#fff;padding:1px 4px;border-radius:3px;font-size:8.5px;margin-right:4px;">CH2</span>' : '');
        const triplenTxt = nr.isDeltaHv
          ? `<span style="color:#10b981;font-weight:700;">0.0% (Trapped in Δ)</span>`
          : (nr.isHv ? `<span style="color:#94a3b8;">${nr.triplenLinePassPct.toFixed(1)}%</span>` : `<span style="color:#fbbf24;">${nr.triplenLinePassPct.toFixed(1)}%</span>`);
        const neutralTxt = nr.isDeltaHv
          ? `<span style="color:#10b981;">Δ-Circ ${m.iDeltaCircA.toFixed(1)} A</span>`
          : (nr.isHv ? '<span style="color:#64748b;">3-Wire (0 A)</span>' : `<span style="color:${nr.iNeutralPctOfPhase>65?'#f87171':'#cbd5e1'};">${nr.iNeutralHarA.toFixed(0)} A (${nr.iNeutralPctOfPhase.toFixed(0)}%)</span>`);
        return `
          <tr style="background:${rowBg}; cursor:pointer; border-bottom:1px solid rgba(148,163,184,0.12);" onclick="updatePqLabControl('probeNodeA', '${nr.id}')">
            <td style="padding:4px 6px; font-weight:600; color:#e2e8f0;">${badgeTag}${nr.label}</td>
            <td style="padding:4px 6px; color:#94a3b8; font-family:monospace;">${nr.kvLabel}</td>
            <td style="padding:4px 6px;"><span style="color:${nr.energized?'#10b981':'#ef4444'};font-weight:700;">${nr.energized?'LIVE':'OFF'}</span></td>
            <td style="padding:4px 6px; font-family:monospace; color:${!nr.energized?'#64748b':(nr.ieee519Pass?'#10b981':'#f87171')}; font-weight:700;">${nr.thdV.toFixed(2)}%</td>
            <td style="padding:4px 6px; font-family:monospace; color:#cbd5e1;">${nr.thdI.toFixed(2)}%</td>
            <td style="padding:4px 6px; font-family:monospace;">${triplenTxt}</td>
            <td style="padding:4px 6px; font-family:monospace;">${neutralTxt}</td>
            <td style="padding:4px 6px;"><span class="duty-badge ${!nr.energized?'':(nr.ieee519Pass?'duty-pass':'duty-fail')}">${!nr.energized?'DE-EN':(nr.ieee519Pass?'PASS ≤5%':'FAIL >5%')}</span></td>
          </tr>
        `;
      }).join('');

      body.innerHTML = `
        ${probeBarHtml}
        <div class="pq-scenario-tabs">
          ${scenarios.map(sc => `<button class="pq-scen-btn ${pq.scenario===sc.id?'active':''}" onclick="selectPqScenario('${sc.id}')">${sc.label}</button>`).join('')}
        </div>
        <div class="pq-osc-grid">
          <div>
            <div class="pq-canvas-wrap">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; gap:6px;">
                <span style="font-size:10px; color:#38bdf8; font-weight:700;">OSCILLOSCOPE @ ${m.activeNodeA.short} — v_a, v_b, v_c &amp; i_a${pq.showOverlayB ? ` | <span style="color:#e879f9;">Ch.2: ${m.activeNodeB.short}</span>` : ''}</span>
                <button class="btn" style="padding:2px 8px; font-size:9.5px;" onclick="updatePqLabControl('oscPaused', ${!pq.oscPaused})">${pq.oscPaused ? '▶ Resume' : '⏸ Freeze Trigger'}</button>
              </div>
              <canvas id="pq-waveform-canvas" width="520" height="200" style="width:100%; height:190px; display:block;"></canvas>
            </div>
            <div class="pq-canvas-wrap" style="margin-top:8px;">
              <div style="font-size:10px; color:#a78bfa; font-weight:700; margin-bottom:3px;">HARMONIC FFT SPECTRUM (h = 1..15) @ ${m.activeNodeA.short} ${m.capResonance.active ? `| 52-CAP f_r=${m.capResonance.fResHz}Hz` : ''}</div>
              <canvas id="pq-harmonic-canvas" width="520" height="105" style="width:100%; height:100px; display:block;"></canvas>
            </div>
          </div>
          <div class="analysis-panel">
            <h4>Interactive Scenario Controls</h4>
            ${controlsHtml}
            <div class="analysis-kpi-grid" style="margin-top:8px;">${diagHtml}</div>
            <div class="pq-diag-card">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-size:10.5px; color:#cbd5e1; font-weight:700;">Standard Check</span>
                <span class="duty-badge ${stdCheck.pass?'duty-pass':'duty-fail'}">${stdCheck.badge}</span>
              </div>
              <div style="font-size:10.5px; color:#94a3b8; line-height:1.4;">${stdCheck.note}</div>
            </div>
          </div>
        </div>
        <div style="margin-top:10px; background:rgba(15,23,42,0.75); border:1px solid rgba(56,189,248,0.22); border-radius:8px; padding:8px 10px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="font-size:10.5px; font-weight:700; color:#38bdf8;">SYSTEM-WIDE 7-NODE HARMONIC PROPAGATION &amp; Δ-WINDING TRIPLEN ISOLATION MATRIX (Click Row to Probe)</span>
            <span style="font-size:9.5px; color:#94a3b8;">IEEE 519-2022 PCC Limit: THD_V ≤ 5.0%</span>
          </div>
          <div style="overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:10px; text-align:left;">
              <thead>
                <tr style="color:#94a3b8; border-bottom:1px solid rgba(148,163,184,0.25);">
                  <th style="padding:4px 6px;">Nodal Bus / Asset</th>
                  <th style="padding:4px 6px;">Voltage</th>
                  <th style="padding:4px 6px;">State</th>
                  <th style="padding:4px 6px;">THD_V</th>
                  <th style="padding:4px 6px;">THD_I</th>
                  <th style="padding:4px 6px;">Triplen Line (3,9,15)</th>
                  <th style="padding:4px 6px;">Neutral I_N / Δ-Trap</th>
                  <th style="padding:4px 6px;">IEEE 519</th>
                </tr>
              </thead>
              <tbody>${nodalRowsHtml}</tbody>
            </table>
          </div>
        </div>
      `;

      drawPqHarmonicCanvas(m);
      drawPqOscilloscopeCanvas();
      if (!pq.oscPaused && typeof requestAnimationFrame === 'function') {
        if (pqAnimFrameId) cancelAnimationFrame(pqAnimFrameId);
        const loop = () => {
          const modal = document.getElementById('analysis-modal');
          if (!modal || modal.style.display === 'none' || AppState.activeAnalysisTab !== 'pq' || AppState.pqState.oscPaused) {
            pqAnimFrameId = null;
            return;
          }
          pqPhaseOffset += 0.08;
          drawPqOscilloscopeCanvas();
          pqAnimFrameId = requestAnimationFrame(loop);
        };
        pqAnimFrameId = requestAnimationFrame(loop);
      }
    }

    function drawPqOscilloscopeCanvas() {
      const canvas = document.getElementById('pq-waveform-canvas');
      if (!canvas || !canvas.getContext) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      const w = canvas.width, h = canvas.height;
      const midY = h / 2;
      const m = computePowerQualityMetrics();
      const pq = m.pq;
      const nA = m.activeNodeA;
      const nB = m.activeNodeB;

      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, w, h);

      // Graticule grid
      ctx.strokeStyle = 'rgba(56,189,248,0.12)';
      ctx.lineWidth = 1;
      for (let gx = 0; gx <= 8; gx++) {
        const x = (gx / 8) * w;
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
      }
      for (let gy = 0; gy <= 4; gy++) {
        const y = (gy / 4) * h;
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
      }

      const ampV = h * 0.28;
      const cyclesShown = 4.0;
      const evalSample = (nodeObj, tNorm, phShift, phGain) => {
        const wt = tNorm * cyclesShown * Math.PI * 2 + pqPhaseOffset;
        if (!nodeObj.energized) return 0;
        let val = Math.sin(wt + phShift) * phGain;
        if (pq.scenario === 'sag_swell') {
          const cycPos = tNorm * cyclesShown;
          const winEnd = Math.min(3.7, 0.7 + m.cyc * 0.12);
          if (cycPos >= 0.7 && cycPos <= winEnd) val *= m.eventPu;
        } else if (pq.scenario === 'harmonics') {
          val += (nodeObj.h3 / 100) * 0.65 * Math.sin(3 * wt)
            + (nodeObj.h5 / 100) * 0.55 * Math.sin(5 * (wt + phShift))
            + (nodeObj.h7 / 100) * 0.45 * Math.sin(7 * (wt + phShift))
            + (nodeObj.h9 / 100) * 0.35 * Math.sin(9 * wt)
            + (nodeObj.h11 / 100) * 0.35 * Math.sin(11 * (wt + phShift))
            + (nodeObj.h13 / 100) * 0.28 * Math.sin(13 * (wt + phShift))
            + (nodeObj.h15 / 100) * 0.22 * Math.sin(15 * wt);
        } else if (pq.scenario === 'transients' && phShift === 0) {
          if (tNorm >= 0.32) {
            const dt = tNorm - 0.32;
            const ring = (m.isLightning ? 3.2 : 1.45) * Math.exp(-dt * 26) * Math.sin(dt * 190);
            val += ring;
            if (pq.saClampActive) {
              const lim = m.isLightning ? 2.15 : 1.52;
              val = Math.max(-lim, Math.min(lim, val));
            }
          }
        } else if (pq.scenario === 'flicker') {
          const mod = (m.dvOverV / 100) * 2.2 * Math.sin(wt * 0.133);
          val *= (1 + mod);
        }
        return val;
      };

      const phaseNames = [
        { shift: 0, color: '#f87171', gain: 1.0 },
        { shift: -2 * Math.PI / 3, color: '#fbbf24', gain: pq.scenario === 'unbalance' ? (1 - m.vuf * 0.015) : 1.0 },
        { shift: 2 * Math.PI / 3, color: '#38bdf8', gain: pq.scenario === 'unbalance' ? (1 + m.vuf * 0.018) : 1.0 }
      ];

      phaseNames.forEach(ph => {
        ctx.beginPath();
        ctx.strokeStyle = ph.color;
        ctx.lineWidth = 1.8;
        for (let px = 0; px <= w; px += 2) {
          const py = midY - evalSample(nA, px / w, ph.shift, ph.gain) * ampV;
          if (px === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
      });

      // Phase A Current trace i_a(t) on Ch.1 probe node
      ctx.beginPath();
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 1.6;
      const phiRad = (m.phiNewDeg || 25) * (Math.PI / 180);
      for (let px = 0; px <= w; px += 2) {
        const tNorm = px / w;
        const wt = tNorm * cyclesShown * Math.PI * 2 + pqPhaseOffset;
        let cur = nA.energized ? Math.sin(wt - phiRad) * 0.72 : 0;
        if (nA.energized && pq.scenario === 'harmonics') {
          cur += (nA.h3 / 100) * Math.sin(3 * wt)
            + (nA.h5 / 100) * Math.sin(5 * wt)
            + (nA.h7 / 100) * Math.sin(7 * wt)
            + (nA.h9 / 100) * 0.7 * Math.sin(9 * wt)
            + (nA.h11 / 100) * 0.65 * Math.sin(11 * wt)
            + (nA.h13 / 100) * 0.55 * Math.sin(13 * wt);
        }
        const py = midY - cur * ampV;
        if (px === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Channel 2 Reference Node Voltage Overlay (Phase A dashed Magenta)
      if (pq.showOverlayB && nB) {
        ctx.save();
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.strokeStyle = '#e879f9';
        ctx.lineWidth = 2.0;
        for (let px = 0; px <= w; px += 2) {
          const py = midY - evalSample(nB, px / w, 0, 1.0) * ampV;
          if (px === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.restore();
      }

      if (!nA.energized) {
        ctx.fillStyle = '#f87171';
        ctx.font = 'bold 12px monospace';
        ctx.fillText('CH.1 DE-ENERGIZED (0.00 kV)', w / 2 - 96, midY - 10);
      }
    }

    function drawPqHarmonicCanvas(metricsObj) {
      const canvas = document.getElementById('pq-harmonic-canvas');
      if (!canvas || !canvas.getContext) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      const m = metricsObj || computePowerQualityMetrics();
      const nA = m.activeNodeA;
      const w = canvas.width, h = canvas.height;
      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, w, h);

      const bars = [
        { order: 1, hOrder: 'h1', val: nA.energized ? 100 : 0, triplen: false },
        { order: 3, hOrder: 'h3', val: m.pq.scenario === 'harmonics' ? m.h3 : (nA.h3 * 0.25), triplen: true },
        { order: 5, hOrder: 'h5', val: m.pq.scenario === 'harmonics' ? m.h5 : (nA.h5 * 0.35), triplen: false },
        { order: 7, hOrder: 'h7', val: m.pq.scenario === 'harmonics' ? m.h7 : (nA.h7 * 0.30), triplen: false },
        { order: 9, hOrder: 'h9', val: m.pq.scenario === 'harmonics' ? m.h9 : (nA.h9 * 0.25), triplen: true },
        { order: 11, hOrder: 'h11', val: m.pq.scenario === 'harmonics' ? m.h11 : (nA.h11 * 0.25), triplen: false },
        { order: 13, hOrder: 'h13', val: m.pq.scenario === 'harmonics' ? m.h13 : (nA.h13 * 0.25), triplen: false },
        { order: 15, hOrder: 'h15', val: m.pq.scenario === 'harmonics' ? m.h15 : (nA.h15 * 0.20), triplen: true }
      ];
      const maxH = h - 22;

      // IEEE 519 5% individual harmonic guide line
      const yLim = maxH - (5 / 35) * (maxH - 8);
      ctx.save();
      ctx.setLineDash([4, 3]);
      ctx.strokeStyle = 'rgba(248,113,113,0.55)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(10, yLim); ctx.lineTo(w - 10, yLim); ctx.stroke();
      ctx.restore();
      ctx.fillStyle = 'rgba(248,113,113,0.8)';
      ctx.font = '9px monospace';
      ctx.fillText('5% IEEE 519', w - 74, yLim - 2);

      bars.forEach((bItem, i) => {
        const bw = 38;
        const bx = 18 + i * 62;
        const norm = i === 0 ? (nA.energized ? 0.90 : 0.0) : Math.min(0.90, bItem.val / 35);
        const bh = Math.max(bItem.val > 0 ? 3 : 2, norm * (maxH - 8));
        ctx.fillStyle = i === 0 ? '#38bdf8' : (bItem.triplen ? (nA.isDeltaHv ? '#10b981' : '#f59e0b') : (bItem.val > 8 ? '#f87171' : '#a78bfa'));
        ctx.fillRect(bx, maxH - bh, bw, bh);
        ctx.fillStyle = '#cbd5e1';
        ctx.font = '10px monospace';
        ctx.fillText(bItem.hOrder, bx + 10, h - 6);
        const lbl = i === 0 ? (nA.energized ? '100%' : '0%') : ((nA.isDeltaHv && bItem.triplen) ? '0%Δ' : `${bItem.val.toFixed(1)}%`);
        ctx.fillText(lbl, bx + 3, Math.max(10, maxH - bh - 3));
      });

      // 52-CAP parallel resonance frequency marker
      if (m.capResonance && m.capResonance.active && !m.capResonance.detuned && m.capResonance.hRes >= 2 && m.capResonance.hRes <= 16) {
        const resX = Math.min(w - 14, Math.max(70, 18 + ((m.capResonance.hRes - 1) / 2) * 62 + 19));
        ctx.save();
        ctx.setLineDash([3, 3]);
        ctx.strokeStyle = '#fb923c';
        ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(resX, 12); ctx.lineTo(resX, maxH); ctx.stroke();
        ctx.restore();
        ctx.fillStyle = '#fb923c';
        ctx.font = 'bold 9px monospace';
        ctx.fillText(`f_r=${m.capResonance.fResHz}Hz`, Math.max(70, Math.min(w - 88, resX - 28)), 10);
      }
    }

    // 4TH-YEAR FIELD CHALLENGE MODAL LOGIC
    let currentDrillTab = 'quiz';

    function openChallengeModal(defaultTab = 'quiz') {
      document.getElementById('challenge-modal').style.display = 'flex';
      switchChallengeTab(defaultTab === 'drill' ? 'switching' : defaultTab);
    }

    function closeChallengeModal() {
      document.getElementById('challenge-modal').style.display = 'none';
    }

    function switchChallengeTab(tab) {
      currentDrillTab = tab;
      document.getElementById('tab-drill-quiz').classList.toggle('active', tab === 'quiz');
      document.getElementById('tab-drill-switching').classList.toggle('active', tab === 'switching');

      if (tab === 'quiz') {
        renderDrillQuiz();
      } else {
        renderDrillSwitching();
      }
    }

    function renderDrillQuiz() {
      const q = QUIZ_QUESTIONS[AppState.currentQuizIndex];
      const body = document.getElementById('challenge-modal-body');
      const actionBtn = document.getElementById('btn-challenge-action');
      actionBtn.innerText = 'Submit Answer';
      actionBtn.onclick = checkQuizAnswer;

      document.getElementById('challenge-score-display').innerText = `SCORE: ${AppState.score} / ${QUIZ_QUESTIONS.length * 10}`;

      body.innerHTML = `
        <div style="font-size: 11.5px; color: var(--text-muted);">
          QUESTION ${AppState.currentQuizIndex + 1} OF ${QUIZ_QUESTIONS.length} (FA1 / SA1-A5 OBE Assessment)
        </div>
        <h4 style="font-size: 13.5px; color: #fff; line-height: 1.5;">${q.question}</h4>
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 8px;">
          ${q.options.map((opt, idx) => `
            <label style="display: flex; align-items: flex-start; gap: 10px; padding: 10px 12px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px; cursor: pointer;">
              <input type="radio" name="quiz_opt" value="${idx}" style="margin-top: 3px;">
              <span style="font-size: 12px; line-height: 1.4; color: #f1f5f9;">${opt}</span>
            </label>
          `).join('')}
        </div>
        <div id="quiz-feedback-box" style="display: none; padding: 12px; border-radius: 6px; font-size: 12px; line-height: 1.5; margin-top: 10px;"></div>
      `;
    }

    function checkQuizAnswer() {
      const q = QUIZ_QUESTIONS[AppState.currentQuizIndex];
      const selected = document.querySelector('input[name="quiz_opt"]:checked');
      if (!selected) {
        alert('Please select an option first.');
        return;
      }

      const answerIdx = parseInt(selected.value);
      const fbBox = document.getElementById('quiz-feedback-box');
      fbBox.style.display = 'block';

      if (answerIdx === q.correct) {
        AppState.score += 10;
        fbBox.style.background = 'rgba(16, 185, 129, 0.2)';
        fbBox.style.border = '1px solid #10b981';
        fbBox.style.color = '#a7f3d0';
        fbBox.innerHTML = `<strong>CORRECT! (+10 pts)</strong><br>${q.explanation}`;
      } else {
        fbBox.style.background = 'rgba(239, 68, 68, 0.2)';
        fbBox.style.border = '1px solid #ef4444';
        fbBox.style.color = '#fecaca';
        fbBox.innerHTML = `<strong>INCORRECT.</strong><br>${q.explanation}`;
      }

      document.getElementById('challenge-score-display').innerText = `SCORE: ${AppState.score} / ${QUIZ_QUESTIONS.length * 10}`;

      const actionBtn = document.getElementById('btn-challenge-action');
      actionBtn.innerText = AppState.currentQuizIndex < QUIZ_QUESTIONS.length - 1 ? 'Next Question →' : 'Complete Quiz';
      actionBtn.onclick = () => {
        if (AppState.currentQuizIndex < QUIZ_QUESTIONS.length - 1) {
          AppState.currentQuizIndex++;
          renderDrillQuiz();
        } else {
          alert(`Diagnostic Quiz Completed! Your final score is ${AppState.score} / ${QUIZ_QUESTIONS.length * 10}`);
          closeChallengeModal();
        }
      };
    }

    // DRILL B: INTERACTIVE MAINTENANCE SWITCHING & INTERLOCK DRILL (SCENARIOS A / B / C / D / E)
    function selectDrillScenario(scenKey) {
      AppState.activeDrillScenario = scenKey;
      AppState.drillStepIndex = 0;
      const topMap = { A: 'single', B: 'maintransfer', C: 'ring', D: 'breakerhalf', E: 'doublebreaker' };
      if (topMap[scenKey] && AppState.busTopology !== topMap[scenKey]) {
        rebuildBusbarTopology(topMap[scenKey]);
      }
      triggerNormalState();
      renderDrillSwitching();
    }

    function renderDrillSwitching() {
      const body = document.getElementById('challenge-modal-body');
      const actionBtn = document.getElementById('btn-challenge-action');
      const scenKey = AppState.activeDrillScenario || 'B';
      const drill = (typeof MAINTENANCE_DRILLS !== 'undefined' && MAINTENANCE_DRILLS[scenKey]) ? MAINTENANCE_DRILLS[scenKey] : { title: 'Switching Drill', desc: '', steps: [] };

      actionBtn.innerText = 'Reset Scenario & Switchyard';
      actionBtn.onclick = () => selectDrillScenario(scenKey);

      body.innerHTML = `
        <div class="drill-scenario-tabs" style="grid-template-columns: repeat(5, 1fr);">
          <button class="btn ${scenKey==='A' ? 'btn-primary' : ''}" style="font-size:9.5px; justify-content:center;" onclick="selectDrillScenario('A')">A: Single Bus</button>
          <button class="btn ${scenKey==='B' ? 'btn-primary' : ''}" style="font-size:9.5px; justify-content:center;" onclick="selectDrillScenario('B')">B: Main &amp; Transfer</button>
          <button class="btn ${scenKey==='C' ? 'btn-primary' : ''}" style="font-size:9.5px; justify-content:center;" onclick="selectDrillScenario('C')">C: Ring Bus</button>
          <button class="btn ${scenKey==='D' ? 'btn-primary' : ''}" style="font-size:9.5px; justify-content:center;" onclick="selectDrillScenario('D')">D: 1.5 CB</button>
          <button class="btn ${scenKey==='E' ? 'btn-primary' : ''}" style="font-size:9.5px; justify-content:center;" onclick="selectDrillScenario('E')">E: 2.0 CB (Double)</button>
        </div>

        <div style="font-size: 12px; color: var(--accent-gold); font-weight: 700;">
          ${drill.title}
        </div>
        <p style="font-size: 11.5px; color: #cbd5e1; line-height: 1.5; margin-top: 4px;">
          ${drill.desc} (Notice how IEEE/ANSI interlocks enforce zero-current disconnect switching — try out-of-order switching in the main matrix to test arc-flash interlock protection!)
        </p>

        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 10px;">
          ${drill.steps.map((st, idx) => {
            const done = idx < AppState.drillStepIndex;
            const current = idx === AppState.drillStepIndex;
            return `
              <div style="padding: 9px 12px; background: ${done ? 'rgba(16, 185, 129, 0.2)' : 'rgba(30, 41, 59, 0.55)'}; border: 1px solid ${done ? '#10b981' : 'rgba(255,255,255,0.08)'}; border-radius: 6px; display: flex; align-items: center; justify-content: space-between; gap:10px;">
                <div>
                  <strong style="color: ${done ? '#a7f3d0' : '#fff'}; font-size: 12px;">${st.label}</strong>
                </div>
                <div>
                  ${done ? '<span style="color:#10b981; font-weight:700; font-size:11px;">✓ DONE</span>' : (current ? `<button class="btn btn-primary" style="font-size:11px;" onclick="executeScenarioStep(${idx})">Execute</button>` : '<span style="color:#64748b; font-size:10px;">WAITING</span>')}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    function executeScenarioStep(idx) {
      const scenKey = AppState.activeDrillScenario || 'B';
      const drill = MAINTENANCE_DRILLS[scenKey];
      if (!drill || !drill.steps[idx]) return;
      const st = drill.steps[idx];
      if (AppState.switchStates[st.target] === st.action) {
        AppState.drillStepIndex = idx + 1;
        showToast(`Verified: ${st.label}`);
      } else {
        const ok = operateSwitch(st.target);
        if (ok) AppState.drillStepIndex = idx + 1;
      }
      if (AppState.drillStepIndex >= drill.steps.length) {
        AppState.score += 10;
        showToast(`Scenario ${scenKey} Complete! Telemetry & 3D Switchyard updated.`);
      }
      renderDrillSwitching();
    }

    // AUDIO TOGGLE
    function toggleAudio() {
      if (!soundEngine.ctx) {
        soundEngine.init();
      }
      soundEngine.enabled = !soundEngine.enabled;
      document.getElementById('audio-icon').innerText = soundEngine.enabled ? '🔊' : '🔇';
      if (soundEngine.enabled) {
        soundEngine.resumeTransformerHum();
        showToast('Audio Effects: ENABLED (60 Hz AC Hum Active)');
      } else {
        soundEngine.stopTransformerHum();
        showToast('Audio Effects: MUTED');
      }
    }

    function openHelpModal() {
      document.getElementById('help-modal').style.display = 'flex';
    }

    function closeHelpModal() {
      document.getElementById('help-modal').style.display = 'none';
    }

    // CONTROL HOUSE ROOF CUTAWAY (Manual + Walk-In Proximity Auto-Reveal)
    function toggleCtrlHouseRoof(isCutaway) {
      AppState.ctrlRoofManualCutaway = !!isCutaway;
      showToast(isCutaway ? 'Control House Roof: CUTAWAY TRANSPARENT VIEW' : 'Control House Roof: SOLID WEATHER-TIGHT');
    }

    function updateControlHouseRoof() {
      const env = switchyardObjects.env;
      if (!env || !env.userData || !env.userData.ctrlHouseRoof || !camera) return;
      const roof = env.userData.ctrlHouseRoof;
      const p = camera.position;
      const ch = AppState.ctrlHousePos;
      const isInsideOrNear = (p.x > ch.x - 5.5 && p.x < ch.x + 5.5 && p.z > ch.z - 6.2 && p.z < ch.z + 6.2);
      const shouldCut = AppState.ctrlRoofManualCutaway || AppState.selectedComponent === 'auxiliary' || isInsideOrNear;
      const targetOp = shouldCut ? 0.06 : 0.96;
      roof.material.opacity += (targetOp - roof.material.opacity) * 0.16;
      roof.material.depthWrite = roof.material.opacity > 0.5;
      roof.visible = roof.material.opacity > 0.08;
    }

    // =========================================================================
    // SUB-PART CLOSE-UP & ENGINEERING DEEP-DIVE POP-UP MODAL ENGINE
    // =========================================================================
    const SubpartModalState = {
      isOpen: false,
      compId: null,
      subpartId: null,
      visualTab: '3d',
      ttRenderer: null,
      ttScene: null,
      ttCamera: null,
      ttPivot: null,
      ttDragging: false,
      ttDownX: 0,
      ttDownY: 0,
      ttLastX: 0,
      ttLastY: 0,
      ttAutoSpin: true,
      ttRadius: 2.5,
      modalExplodePct: 65,
      ttFullMap: {},
      ttHighlightedId: null
    };

    function initSubpartTurntable() {
      if (SubpartModalState.ttRenderer) return;
      const canvas = document.getElementById('subpart-turntable-canvas');
      if (!canvas) return;

      const r = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
      r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      r.setSize(420, 310, false);
      if ('outputEncoding' in r) r.outputEncoding = THREE.sRGBEncoding;

      const sc = new THREE.Scene();
      const cam = new THREE.PerspectiveCamera(42, 420 / 310, 0.05, 160);
      cam.position.set(2.4, 1.8, 2.8);

      const hemi = new THREE.HemisphereLight(0xf8fafc, 0x334155, 1.35);
      const key = new THREE.DirectionalLight(0xffffff, 1.8);
      key.position.set(5, 8, 6);
      const rim = new THREE.DirectionalLight(0x38bdf8, 0.9);
      rim.position.set(-6, 3, -5);
      const pivot = new THREE.Group();
      sc.add(hemi, key, rim, pivot);

      // Subtle calibration turntable ring beneath isolated sub-part
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(0.95, 1.02, 48),
        new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.35, side: THREE.DoubleSide })
      );
      ring.rotation.x = -Math.PI / 2;
      ring.position.y = -0.85;
      sc.add(ring);

      const modalRaycaster = new THREE.Raycaster();
      const modalMouse = new THREE.Vector2();

      canvas.addEventListener('mousedown', (e) => {
        SubpartModalState.ttDragging = true;
        SubpartModalState.ttAutoSpin = false;
        const spinBtn = document.getElementById('modal-autorotate-btn');
        if (spinBtn) spinBtn.classList.remove('btn-active');
        SubpartModalState.ttDownX = e.clientX;
        SubpartModalState.ttDownY = e.clientY;
        SubpartModalState.ttLastX = e.clientX;
        SubpartModalState.ttLastY = e.clientY;
      });
      canvas.addEventListener('mouseup', (e) => {
        const moveDist = Math.hypot(e.clientX - SubpartModalState.ttDownX, e.clientY - SubpartModalState.ttDownY);
        if (moveDist < 5 && SubpartModalState.isOpen && SubpartModalState.visualTab === 'full3d' && SubpartModalState.ttPivot && SubpartModalState.ttCamera) {
          const rect = canvas.getBoundingClientRect();
          modalMouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
          modalMouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
          modalRaycaster.setFromCamera(modalMouse, SubpartModalState.ttCamera);
          const hits = modalRaycaster.intersectObjects(SubpartModalState.ttPivot.children, true);
          if (hits.length > 0) {
            let obj = hits[0].object;
            while (obj && !obj.userData?.subpartId && obj.parent) obj = obj.parent;
            if (obj && obj.userData && obj.userData.subpartId) {
              selectModalSubpartChip(obj.userData.subpartId);
            }
          }
        }
      });
      window.addEventListener('mouseup', () => {
        SubpartModalState.ttDragging = false;
      });
      window.addEventListener('mousemove', (e) => {
        if (!SubpartModalState.ttDragging || !SubpartModalState.isOpen) return;
        const dx = e.clientX - SubpartModalState.ttLastX;
        const dy = e.clientY - SubpartModalState.ttLastY;
        SubpartModalState.ttLastX = e.clientX;
        SubpartModalState.ttLastY = e.clientY;
        if (SubpartModalState.ttPivot) {
          SubpartModalState.ttPivot.rotation.y += dx * 0.012;
          SubpartModalState.ttPivot.rotation.x = Math.max(-0.9, Math.min(0.9, SubpartModalState.ttPivot.rotation.x + dy * 0.01));
        }
      });
      canvas.addEventListener('wheel', (e) => {
        if (!SubpartModalState.isOpen) return;
        e.preventDefault();
        SubpartModalState.ttRadius = Math.max(0.8, Math.min(42, SubpartModalState.ttRadius * (e.deltaY > 0 ? 1.12 : 0.89)));
        cam.position.normalize().multiplyScalar(SubpartModalState.ttRadius);
        cam.lookAt(0, 0, 0);
      }, { passive: false });

      SubpartModalState.ttRenderer = r;
      SubpartModalState.ttScene = sc;
      SubpartModalState.ttCamera = cam;
      SubpartModalState.ttPivot = pivot;
    }

    function loadTurntableMesh(compId, subpartId) {
      initSubpartTurntable();
      const pivot = SubpartModalState.ttPivot;
      const cam = SubpartModalState.ttCamera;
      if (!pivot || !cam) return;

      while (pivot.children.length > 0) pivot.remove(pivot.children[0]);
      SubpartModalState.ttFullMap = {};
      pivot.rotation.set(0.12, -0.45, 0);
      SubpartModalState.ttAutoSpin = true;

      const compObj = switchyardObjects[compId];
      const srcSub = compObj && compObj.userData && compObj.userData.subparts ? compObj.userData.subparts[subpartId] : null;
      if (!srcSub) return;

      const clone = srcSub.clone(true);
      clone.position.set(0, 0, 0);
      clone.rotation.set(0, 0, 0);
      clone.scale.set(1, 1, 1);

      const box = new THREE.Box3().setFromObject(clone);
      const center = new THREE.Vector3();
      const size = new THREE.Vector3();
      box.getCenter(center);
      box.getSize(size);

      clone.position.sub(center);
      pivot.add(clone);

      const maxDim = Math.max(size.x, size.y, size.z, 0.35);
      const dist = maxDim * 1.95;
      SubpartModalState.ttRadius = dist;
      cam.position.set(dist * 0.78, dist * 0.42, dist * 0.85);
      cam.lookAt(0, 0, 0);
      cam.near = Math.max(0.01, dist * 0.02);
      cam.far = Math.max(80, dist * 12);
      cam.updateProjectionMatrix();
    }

    function loadFullEquipmentModalMesh(compId) {
      initSubpartTurntable();
      const pivot = SubpartModalState.ttPivot;
      const cam = SubpartModalState.ttCamera;
      const compObj = switchyardObjects[compId];
      const data = SUBSTATION_DATA[compId];
      if (!pivot || !cam || !compObj || !data) return;

      while (pivot.children.length > 0) pivot.remove(pivot.children[0]);
      SubpartModalState.ttFullMap = {};
      pivot.rotation.set(0.14, -0.52, 0);

      const clone = new THREE.Group();
      compObj.children.forEach(ch => clone.add(ch.clone(true)));
      clone.position.set(0, 0, 0);
      clone.rotation.set(0, 0, 0);
      clone.scale.set(1, 1, 1);

      // Restore base positions before computing bounding box and explode vectors
      data.subparts.forEach(sp => {
        const origSub = compObj.userData?.subparts?.[sp.id];
        if (!origSub) return;
        const basePos = origSub.userData?.basePos ? origSub.userData.basePos.clone() : origSub.position.clone();
        let clonedSub = null;
        clone.traverse(child => {
          if (clonedSub || child === clone) return;
          if (child.userData?.subpartId === sp.id && child.parent?.userData?.subpartId !== sp.id) {
            clonedSub = child;
          }
        });
        if (clonedSub) {
          clonedSub.position.copy(basePos);
          SubpartModalState.ttFullMap[sp.id] = {
            mesh: clonedSub,
            basePos: basePos.clone(),
            vector: sp.vector || [0, 1.5, 0]
          };
        }
      });

      const box = new THREE.Box3().setFromObject(clone);
      const center = new THREE.Vector3();
      const size = new THREE.Vector3();
      box.getCenter(center);
      box.getSize(size);
      clone.position.sub(center);
      pivot.add(clone);

      const maxDim = Math.max(size.x, size.y, size.z, 1.2);
      const dist = maxDim * 2.15;
      SubpartModalState.ttRadius = dist;
      cam.position.set(dist * 0.82, dist * 0.45, dist * 0.88);
      cam.lookAt(0, 0, 0);
      cam.near = Math.max(0.02, dist * 0.015);
      cam.far = Math.max(120, dist * 14);
      cam.updateProjectionMatrix();

      renderModalSubpartChips(compId);
      setModalExplodePercentage(SubpartModalState.modalExplodePct ?? 65);
      highlightModalSubpart(SubpartModalState.subpartId);
    }

    function setModalExplodePercentage(val) {
      const pct = Math.max(0, Math.min(100, parseInt(val, 10) || 0));
      SubpartModalState.modalExplodePct = pct;
      const slider = document.getElementById('modal-explode-slider');
      const label = document.getElementById('modal-explode-pct');
      if (slider) slider.value = pct;
      if (label) label.innerText = `${pct}%`;

      const factor = pct / 100;
      Object.values(SubpartModalState.ttFullMap || {}).forEach(entry => {
        const v = entry.vector || [0, 0, 0];
        entry.mesh.position.set(
          entry.basePos.x + v[0] * factor,
          entry.basePos.y + v[1] * factor,
          entry.basePos.z + v[2] * factor
        );
      });
    }

    function toggleModalAutoRotate() {
      SubpartModalState.ttAutoSpin = !SubpartModalState.ttAutoSpin;
      const btn = document.getElementById('modal-autorotate-btn');
      if (btn) btn.classList.toggle('btn-active', SubpartModalState.ttAutoSpin);
    }

    function highlightModalSubpart(subpartId) {
      Object.entries(SubpartModalState.ttFullMap || {}).forEach(([id, entry]) => {
        const isTarget = id === subpartId;
        entry.mesh.traverse(obj => {
          if (obj.isMesh && obj.material && !Array.isArray(obj.material)) {
            if (!obj.userData._origClonedMat) {
              obj.userData._origClonedMat = obj.material;
              obj.material = obj.material.clone();
            }
            if ('emissive' in obj.material) {
              obj.material.emissive.setHex(isTarget ? 0x0284c7 : 0x000000);
              obj.material.emissiveIntensity = isTarget ? 0.55 : 0.0;
            }
          }
        });
      });
    }

    function renderModalSubpartChips(compId) {
      const box = document.getElementById('modal-subpart-chips');
      const data = SUBSTATION_DATA[compId];
      if (!box || !data) return;
      box.innerHTML = data.subparts.map(sp => `
        <button class="modal-chip-btn ${sp.id === SubpartModalState.subpartId ? 'active' : ''}" onclick="selectModalSubpartChip('${sp.id}')">
          <strong>${sp.tag}</strong> ${sp.name}
        </button>
      `).join('');
    }

    function updateSubpartModalDetails(compId, subpartId) {
      const data = SUBSTATION_DATA[compId];
      if (!data) return;
      const sp = data.subparts.find(s => s.id === subpartId);
      if (!sp) return;
      SubpartModalState.compId = compId;
      SubpartModalState.subpartId = subpartId;
      const deep = (typeof SUBPART_DEEP_DIVE !== 'undefined' && SUBPART_DEEP_DIVE[subpartId]) ? SUBPART_DEEP_DIVE[subpartId] : null;
      document.getElementById('subpart-modal-ansi').innerText = deep ? deep.ansiCode : `${data.ansiNumber} • ${sp.tag}`;
      document.getElementById('subpart-modal-title').innerText = `${sp.name} (${data.tag})`;
      document.getElementById('subpart-field-spot').innerText = deep ? deep.fieldSpot : `Located within ${data.name} bay assembly under ${data.governingStandard}.`;
      document.getElementById('subpart-working-principle').innerText = deep ? deep.workingPrinciple : sp.role;
      document.getElementById('subpart-material-role').innerText = `Material: ${sp.material}. Functional Role: ${sp.role}`;
      document.getElementById('subpart-maintenance').innerText = deep ? deep.maintenance : (data.checklist[0] || 'Inspect connections and thermal profile.');
      refreshSubpartActionBar();
      renderSubpartSchematicSVG(compId, subpartId, sp);
    }

    function selectModalSubpartChip(subpartId) {
      if (!SubpartModalState.compId) return;
      updateSubpartModalDetails(SubpartModalState.compId, subpartId);
      renderModalSubpartChips(SubpartModalState.compId);
      highlightModalSubpart(subpartId);
    }

    function launchSelectedEquipmentModalExplode() {
      const compId = AppState.selectedComponent || 'transformer';
      const data = SUBSTATION_DATA[compId];
      if (!data || !data.subparts.length) return;
      openSubpartModal(compId, data.subparts[0].id, 'full3d');
      showToast(`3D Exploded Viewer: ${data.name}`);
    }

    function renderSubpartTurntable(delta) {
      if (!SubpartModalState.isOpen || (SubpartModalState.visualTab !== '3d' && SubpartModalState.visualTab !== 'full3d')) return;
      const { ttRenderer, ttScene, ttCamera, ttPivot } = SubpartModalState;
      if (!ttRenderer || !ttScene || !ttCamera) return;
      if (SubpartModalState.ttAutoSpin && ttPivot) {
        ttPivot.rotation.y += delta * (SubpartModalState.visualTab === 'full3d' ? 0.35 : 0.55);
      }
      ttRenderer.render(ttScene, ttCamera);
    }

    function openSubpartModal(compId, subpartId, initialTab = '3d') {
      const data = SUBSTATION_DATA[compId];
      if (!data) return;
      const sp = data.subparts.find(s => s.id === subpartId) || data.subparts[0];
      if (!sp) return;

      SubpartModalState.isOpen = true;
      updateSubpartModalDetails(compId, sp.id);
      if (initialTab === 'full3d') {
        SubpartModalState.modalExplodePct = 65;
      }
      switchSubpartVisualTab(initialTab || SubpartModalState.visualTab || '3d');

      document.getElementById('subpart-modal').style.display = 'flex';
    }

    function refreshSubpartActionBar() {
      const bar = document.getElementById('subpart-action-bar');
      if (!bar || !SubpartModalState.isOpen) return;
      const sid = SubpartModalState.subpartId;
      if (sid === 'aux-relay-racks' || sid === 'aux-scada-desk' || sid.startsWith('cb-')) {
        bar.style.display = 'flex';
        bar.innerHTML = `
          <span><strong>52CB Status:</strong> <span style="color:${AppState.breakerClosed ? '#f87171' : '#34d399'};font-weight:700;">${AppState.breakerClosed ? 'CLOSED (ENERGIZED)' : 'OPEN (TRIPPED)'}</span></span>
          <button class="btn btn-primary" style="padding:4px 10px;font-size:11px;" onclick="toggleBreakerState()">Operate Pistol-Grip 52-CS</button>
        `;
      } else if (sid.startsWith('ds-')) {
        bar.style.display = 'flex';
        bar.innerHTML = `
          <span><strong>DS-89 Status:</strong> <span style="color:${AppState.disconnectClosed ? '#f87171' : '#34d399'};font-weight:700;">${AppState.disconnectClosed ? 'CLOSED' : 'OPEN (AIR GAP)'}</span></span>
          <button class="btn" style="padding:4px 10px;font-size:11px;" onclick="toggleDisconnectState()">Operate Disconnect 89</button>
        `;
      } else {
        bar.style.display = 'none';
      }
    }

    function closeSubpartModal() {
      SubpartModalState.isOpen = false;
      document.getElementById('subpart-modal').style.display = 'none';
    }

    function stepSubpartModal(dir) {
      const data = SUBSTATION_DATA[SubpartModalState.compId];
      if (!data || !data.subparts.length) return;
      const idx = data.subparts.findIndex(s => s.id === SubpartModalState.subpartId);
      const nextIdx = (idx + dir + data.subparts.length) % data.subparts.length;
      const nextId = data.subparts[nextIdx].id;
      if (SubpartModalState.visualTab === 'full3d') {
        selectModalSubpartChip(nextId);
      } else {
        focusSubpart(nextId);
      }
    }

    function switchSubpartVisualTab(tab) {
      SubpartModalState.visualTab = tab;
      const canvas = document.getElementById('subpart-turntable-canvas');
      const svgBox = document.getElementById('subpart-svg-diagram');
      const explodeCtrl = document.getElementById('subpart-modal-explode-controls');
      const hint = document.getElementById('subpart-stage-hint');
      const btn3d = document.getElementById('tab-btn-3d');
      const btnFull3d = document.getElementById('tab-btn-full3d');
      const btnSvg = document.getElementById('tab-btn-svg');
      const spinBtn = document.getElementById('modal-autorotate-btn');

      if (btn3d) btn3d.classList.toggle('active', tab === '3d');
      if (btnFull3d) btnFull3d.classList.toggle('active', tab === 'full3d');
      if (btnSvg) btnSvg.classList.toggle('active', tab === 'svg');

      if (tab === '3d') {
        canvas.style.display = 'block';
        svgBox.style.display = 'none';
        if (explodeCtrl) explodeCtrl.style.display = 'none';
        hint.innerText = 'Drag inside 3D preview to rotate • Scroll to zoom';
        loadTurntableMesh(SubpartModalState.compId, SubpartModalState.subpartId);
      } else if (tab === 'full3d') {
        canvas.style.display = 'block';
        svgBox.style.display = 'none';
        if (explodeCtrl) explodeCtrl.style.display = 'block';
        hint.innerText = 'Slide to explode assembly • Click any 3D sub-part or chip • Drag to orbit';
        SubpartModalState.ttAutoSpin = false;
        if (spinBtn) spinBtn.classList.remove('btn-active');
        loadFullEquipmentModalMesh(SubpartModalState.compId);
      } else {
        canvas.style.display = 'none';
        svgBox.style.display = 'flex';
        if (explodeCtrl) explodeCtrl.style.display = 'none';
        hint.innerText = 'Annotated EE 415 internal cutaway engineering schematic';
      }
    }

    function renderSubpartSchematicSVG(compId, subpartId, sp) {
      const box = document.getElementById('subpart-svg-diagram');
      if (!box) return;
      let inner = '';

      if (subpartId === 'tx-buchholz') {
        inner = `
          <line x1="20" y1="225" x2="380" y2="95" stroke="#64748b" stroke-width="26" stroke-linecap="round"/>
          <line x1="20" y1="225" x2="380" y2="95" stroke="#0f172a" stroke-width="18" stroke-linecap="round"/>
          <rect x="135" y="95" width="130" height="125" rx="8" fill="#1e293b" stroke="#eab308" stroke-width="3"/>
          <rect x="150" y="108" width="100" height="32" rx="4" fill="rgba(56,189,248,0.18)" stroke="#38bdf8" stroke-dasharray="4 2"/>
          <text x="200" y="128" fill="#bae6fd" font-size="10" text-anchor="middle" font-family="monospace">GAS POCKET (H2/C2H2)</text>
          <circle cx="175" cy="148" r="13" fill="#facc15" stroke="#fef08a" stroke-width="2"/>
          <text x="242" y="152" fill="#facc15" font-size="9" font-family="monospace">ALARM FLOAT</text>
          <polygon points="182,195 204,195 198,175 186,175" fill="#ef4444" stroke="#fca5a5" stroke-width="2"/>
          <text x="248" y="192" fill="#f87171" font-size="9" font-family="monospace">SURGE BAFFLE (86T)</text>
          <line x1="200" y1="95" x2="200" y2="68" stroke="#cbd5e1" stroke-width="5"/>
          <text x="200" y="58" fill="#cbd5e1" font-size="10" text-anchor="middle" font-family="monospace">Gas Sample Petcock</text>
          <text x="55" y="255" fill="#94a3b8" font-size="10" font-family="monospace">From Main Tank</text>
          <text x="285" y="75" fill="#94a3b8" font-size="10" font-family="monospace">To Conservator (5°)</text>
        `;
      } else if (subpartId === 'cb-interrupter' || subpartId === 'cb-contacts' || subpartId === 'cb-tank' || subpartId === 'cb-gauge') {
        inner = `
          <rect x="35" y="75" width="330" height="145" rx="18" fill="#1e293b" stroke="#64748b" stroke-width="4"/>
          <text x="200" y="64" fill="#94a3b8" font-size="10" text-anchor="middle" font-family="monospace">GROUNDED DEAD-TANK (0.60 MPa SF6)</text>
          <rect x="55" y="128" width="110" height="38" rx="4" fill="#d97706" stroke="#fbbf24"/>
          <text x="110" y="151" fill="#fff" font-size="10" text-anchor="middle" font-family="monospace">FIXED TULIP</text>
          <polygon points="165,112 225,126 225,168 165,182" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
          <text x="195" y="106" fill="#f8fafc" font-size="9" text-anchor="middle" font-family="monospace">PTFE PUFFER NOZZLE</text>
          <rect x="205" y="135" width="135" height="24" rx="4" fill="#94a3b8" stroke="#e2e8f0"/>
          <text x="275" y="151" fill="#0f172a" font-size="10" text-anchor="middle" font-weight="bold" font-family="monospace">MOVING ARC ROD</text>
          <path d="M 240 120 Q 190 124 160 135" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 3"/>
          <path d="M 240 175 Q 190 171 160 160" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 3"/>
          <text x="200" y="206" fill="#38bdf8" font-size="10" text-anchor="middle" font-family="monospace">Supersonic SF6 Quench Blast (&lt;33 ms @ Current Zero)</text>
        `;
      } else if (subpartId.startsWith('la-')) {
        inner = `
          <rect x="155" y="26" width="90" height="12" fill="#94a3b8"/>
          <ellipse cx="200" cy="54" rx="74" ry="12" fill="none" stroke="#cbd5e1" stroke-width="4"/>
          <text x="305" y="57" fill="#cbd5e1" font-size="9" font-family="monospace">GRADING RING</text>
          <rect x="172" y="54" width="56" height="180" rx="6" fill="#1e293b" stroke="#60a5fa" stroke-width="2"/>
          <rect x="180" y="66" width="40" height="22" rx="3" fill="#475569" stroke="#94a3b8"/>
          <rect x="180" y="94" width="40" height="22" rx="3" fill="#475569" stroke="#94a3b8"/>
          <rect x="180" y="122" width="40" height="22" rx="3" fill="#475569" stroke="#94a3b8"/>
          <rect x="180" y="150" width="40" height="22" rx="3" fill="#475569" stroke="#94a3b8"/>
          <rect x="180" y="178" width="40" height="22" rx="3" fill="#475569" stroke="#94a3b8"/>
          <text x="90" y="138" fill="#38bdf8" font-size="10" text-anchor="middle" font-family="monospace">ZnO MOV DISCS</text>
          <text x="90" y="152" fill="#94a3b8" font-size="9" text-anchor="middle" font-family="monospace">(I = k·V^40)</text>
          <line x1="200" y1="234" x2="200" y2="262" stroke="#d97706" stroke-width="5"/>
          <rect x="135" y="242" width="45" height="28" rx="4" fill="#0f172a" stroke="#10b981"/>
          <text x="157" y="259" fill="#10b981" font-size="9" text-anchor="middle" font-family="monospace">42 µA</text>
          <text x="278" y="259" fill="#fbbf24" font-size="9" font-family="monospace">CNT: ${AppState.surgeCounter} -> EARTH</text>
        `;
      } else if (subpartId.startsWith('ct-')) {
        inner = `
          <rect x="175" y="34" width="50" height="175" rx="6" fill="none" stroke="#92400e" stroke-width="5"/>
          <path d="M 75 56 L 195 56 L 195 145 L 208 145 L 208 56 L 325 56" fill="none" stroke="#f59e0b" stroke-width="8"/>
          <text x="95" y="45" fill="#fbbf24" font-size="10" font-family="monospace">P1 (69kV)</text>
          <text x="295" y="45" fill="#fbbf24" font-size="10" font-family="monospace">P2</text>
          <ellipse cx="201" cy="100" rx="44" ry="18" fill="none" stroke="#cbd5e1" stroke-width="8"/>
          <text x="305" y="104" fill="#7dd3fc" font-size="9" font-family="monospace">0.15S METERING</text>
          <ellipse cx="201" cy="144" rx="48" ry="20" fill="none" stroke="#475569" stroke-width="10"/>
          <text x="305" y="148" fill="#fca5a5" font-size="9" font-family="monospace">C800 RELAYING</text>
          <rect x="150" y="220" width="100" height="44" rx="4" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
          <text x="200" y="240" fill="#fca5a5" font-size="9" text-anchor="middle" font-weight="bold" font-family="monospace">SHORTING BLOCKS</text>
          <text x="200" y="254" fill="#fef08a" font-size="8" text-anchor="middle" font-family="monospace">NEVER OPEN-CKT SECONDARY</text>
        `;
      } else if (subpartId.startsWith('aux-')) {
        inner = `
          <rect x="28" y="42" width="155" height="90" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
          <text x="105" y="64" fill="#34d399" font-size="10" text-anchor="middle" font-weight="bold" font-family="monospace">125 VDC UNGROUNDED BUS</text>
          <text x="105" y="84" fill="#e2e8f0" font-size="9" text-anchor="middle" font-family="monospace">+67.5V to Earth | -67.5V</text>
          <text x="105" y="104" fill="#94a3b8" font-size="9" text-anchor="middle" font-family="monospace">60 Lead-Calcium Cells @ 2.25V</text>
          <text x="105" y="120" fill="#fbbf24" font-size="9" text-anchor="middle" font-family="monospace">Dual Redundant SCR Chargers</text>
          <rect x="215" y="42" width="158" height="90" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
          <text x="294" y="64" fill="#7dd3fc" font-size="10" text-anchor="middle" font-weight="bold" font-family="monospace">PROTECTION / SCADA</text>
          <text x="294" y="84" fill="#e2e8f0" font-size="9" text-anchor="middle" font-family="monospace">SEL-487E (87T) + SEL-751</text>
          <text x="294" y="104" fill="#e2e8f0" font-size="9" text-anchor="middle" font-family="monospace">86 Lockout -&gt; TC1 &amp; TC2</text>
          <text x="294" y="120" fill="#10b981" font-size="9" text-anchor="middle" font-family="monospace">DNP3 / IEC 61850 / IRIG-B</text>
          <path d="M 105 132 L 105 178 L 294 178 L 294 132" fill="none" stroke="#f97316" stroke-width="3"/>
          <rect x="135" y="195" width="130" height="52" rx="6" fill="#0f172a" stroke="#ef4444" stroke-width="2"/>
          <text x="200" y="218" fill="#fca5a5" font-size="10" text-anchor="middle" font-weight="bold" font-family="monospace">CB-69-1 DUAL COILS</text>
          <text x="200" y="236" fill="#cbd5e1" font-size="9" text-anchor="middle" font-family="monospace">&lt;15 ms DC Trip Assurance</text>
        `;
      } else if (subpartId === 'tx-conservator') {
        inner = `
          <rect x="75" y="42" width="210" height="72" rx="34" fill="#1e293b" stroke="#94a3b8" stroke-width="3"/>
          <path d="M 80 86 Q 180 84 280 86 L 278 106 Q 180 112 82 106 Z" fill="rgba(245,158,11,0.35)"/>
          <text x="180" y="72" fill="#cbd5e1" font-size="10" text-anchor="middle" font-family="monospace">CONSERVATOR HEAD (~8% VOL)</text>
          <text x="180" y="100" fill="#fbbf24" font-size="9" text-anchor="middle" font-family="monospace">MINERAL OIL LEVEL (MOG)</text>
          <path d="M 285 68 L 325 68 L 325 142" fill="none" stroke="#94a3b8" stroke-width="6"/>
          <rect x="303" y="142" width="44" height="72" rx="6" fill="rgba(56,189,248,0.18)" stroke="#38bdf8" stroke-width="2"/>
          <circle cx="325" cy="162" r="5" fill="#2563eb"/><circle cx="316" cy="178" r="5" fill="#3b82f6"/>
          <circle cx="334" cy="178" r="5" fill="#3b82f6"/><circle cx="325" cy="195" r="5" fill="#ec4899"/>
          <rect x="309" y="216" width="32" height="18" rx="3" fill="#d97706"/>
          <text x="232" y="176" fill="#7dd3fc" font-size="9" text-anchor="end" font-family="monospace">BLUE = DRY SILICA</text>
          <text x="232" y="196" fill="#f472b6" font-size="9" text-anchor="end" font-family="monospace">PINK = REPLACE (>50%)</text>
          <text x="232" y="228" fill="#fbbf24" font-size="9" text-anchor="end" font-family="monospace">OIL SEAL CUP</text>
          <path d="M 135 114 L 85 182" fill="none" stroke="#64748b" stroke-width="10"/>
          <text x="95" y="205" fill="#94a3b8" font-size="9" text-anchor="middle" font-family="monospace">Via Buchholz (63)</text>
        `;
      } else if (subpartId === 'tx-core' || subpartId === 'tx-windings' || subpartId === 'tx-oltc') {
        inner = `
          <rect x="65" y="42" width="205" height="22" fill="#475569" stroke="#cbd5e1"/>
          <rect x="65" y="206" width="205" height="22" fill="#475569" stroke="#cbd5e1"/>
          <rect x="78" y="64" width="26" height="142" fill="#334155" stroke="#94a3b8"/>
          <rect x="155" y="64" width="26" height="142" fill="#334155" stroke="#94a3b8"/>
          <rect x="232" y="64" width="26" height="142" fill="#334155" stroke="#94a3b8"/>
          <rect x="143" y="76" width="50" height="118" fill="none" stroke="#f59e0b" stroke-width="4" stroke-dasharray="6 3"/>
          <rect x="135" y="70" width="66" height="130" fill="none" stroke="#ea580c" stroke-width="4"/>
          <text x="168" y="34" fill="#cbd5e1" font-size="10" text-anchor="middle" font-family="monospace">CRGO M4 LAMINATED CORE (1.65 T)</text>
          <text x="168" y="248" fill="#fbbf24" font-size="10" text-anchor="middle" font-family="monospace">Dyn11: LV WYE-N INNER | HV DELTA OUTER</text>
          <rect x="288" y="72" width="84" height="126" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
          <text x="330" y="96" fill="#7dd3fc" font-size="9" text-anchor="middle" font-weight="bold" font-family="monospace">OLTC (±10%)</text>
          <text x="330" y="118" fill="#e2e8f0" font-size="9" text-anchor="middle" font-family="monospace">33 Tap Steps</text>
          <text x="330" y="138" fill="#fbbf24" font-size="9" text-anchor="middle" font-family="monospace">&lt;45ms Diverter</text>
          <text x="330" y="162" fill="#f87171" font-size="8" text-anchor="middle" font-family="monospace">SEPARATE OIL</text>
          <text x="330" y="176" fill="#f87171" font-size="8" text-anchor="middle" font-family="monospace">COMPARTMENT</text>
        `;
      } else if (subpartId.startsWith('ds-')) {
        inner = `
          <rect x="52" y="112" width="38" height="110" fill="#78350f" stroke="#d97706" stroke-width="2"/>
          <rect x="310" y="112" width="38" height="110" fill="#78350f" stroke="#d97706" stroke-width="2"/>
          <line x1="71" y1="104" x2="188" y2="${AppState.disconnectClosed ? '104' : '64'}" stroke="#f59e0b" stroke-width="7" stroke-linecap="round"/>
          <line x1="329" y1="104" x2="212" y2="${AppState.disconnectClosed ? '104' : '64'}" stroke="#f59e0b" stroke-width="7" stroke-linecap="round"/>
          <circle cx="200" cy="104" r="14" fill="none" stroke="#94a3b8" stroke-width="3" stroke-dasharray="4 2"/>
          <text x="200" y="44" fill="${AppState.disconnectClosed ? '#f87171' : '#34d399'}" font-size="11" font-weight="bold" text-anchor="middle" font-family="monospace">DS-89 STATE: ${AppState.disconnectClosed ? 'CLOSED (52 INTERLOCK ACTIVE)' : 'VISIBLE AIR GAP OPEN'}</text>
          <line x1="52" y1="224" x2="348" y2="224" stroke="#64748b" stroke-width="4"/>
          <path d="M 105 224 L 105 ${AppState.earthClosed ? '110' : '168'}" stroke="#d97706" stroke-width="5" stroke-linecap="round"/>
          <text x="225" y="252" fill="#fbbf24" font-size="10" text-anchor="middle" font-family="monospace">89E EARTH BLADE: ${AppState.earthClosed ? 'GROUNDED TO IEEE-80 GRID' : 'OPEN (INTERLOCKED W/ 89)'}</text>
        `;
      } else if (subpartId.startsWith('sec-') || subpartId.startsWith('fdr-')) {
        const b = computeEnergizedBranches();
        inner = `
          <rect x="28" y="38" width="110" height="82" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
          <text x="83" y="60" fill="#fbbf24" font-size="9.5" text-anchor="middle" font-weight="bold" font-family="monospace">10 Ω NGR + 51G</text>
          <text x="83" y="78" fill="#e2e8f0" font-size="8.5" text-anchor="middle" font-family="monospace">Caps SLG @ 797 A</text>
          <text x="83" y="96" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="monospace">52-LV: ${AppState.switchStates.cbLV ? '2000A CLOSED' : 'OPEN'}</text>
          <rect x="164" y="38" width="208" height="190" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
          <text x="268" y="60" fill="#34d399" font-size="10" text-anchor="middle" font-weight="bold" font-family="monospace">13.8 kV SECONDARY &amp; FEEDERS</text>
          <text x="268" y="84" fill="#fbbf24" font-size="9" text-anchor="middle" font-family="monospace">Bus Status: ${b.secMain ? 'ENERGIZED 13.8 kV' : 'ISOLATED'}</text>
          <text x="268" y="106" fill="${b.fdr1 ? '#34d399' : '#94a3b8'}" font-size="9" text-anchor="middle" font-family="monospace">Feeder 01 (52-F1): ${b.fdr1 ? 'CLOSED (~20.8 MVA)' : 'OPEN'}</text>
          <text x="268" y="126" fill="${b.fdr2 ? '#34d399' : '#94a3b8'}" font-size="9" text-anchor="middle" font-family="monospace">Feeder 02 (52-F2): ${b.fdr2 ? 'CLOSED (~19.5 MVA)' : 'OPEN'}</text>
          <text x="268" y="146" fill="#2dd4bf" font-size="9" text-anchor="middle" font-family="monospace">3.6 MVAR Cap (52-CAP): ${b.capBank ? 'ONLINE' : 'OFF'}</text>
          <text x="268" y="170" fill="#cbd5e1" font-size="8.5" text-anchor="middle" font-family="monospace">477 kcmil ACSR Hawk | ANSI 50/51/51N/79</text>
          <text x="268" y="196" fill="#f87171" font-size="8.5" text-anchor="middle" font-family="monospace">Interlocked 89-LV / 89-F1A/B / 89-F2A/B</text>
        `;
      } else {
        inner = `
          <rect x="45" y="45" width="310" height="190" rx="10" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
          <line x1="45" y1="85" x2="355" y2="85" stroke="#334155" stroke-width="1.5"/>
          <text x="200" y="70" fill="#7dd3fc" font-size="11" font-weight="bold" text-anchor="middle" font-family="monospace">${sp.tag} • ${compId.toUpperCase()}</text>
          <rect x="85" y="105" width="230" height="44" rx="6" fill="#0f172a" stroke="#f59e0b"/>
          <text x="200" y="124" fill="#fcd34d" font-size="10" text-anchor="middle" font-weight="bold" font-family="monospace">${sp.name.slice(0, 34)}</text>
          <text x="200" y="140" fill="#94a3b8" font-size="9" text-anchor="middle" font-family="monospace">${sp.material.slice(0, 38)}</text>
          <text x="200" y="182" fill="#cbd5e1" font-size="10" text-anchor="middle" font-family="monospace">Live Telemetry State:</text>
          <text x="200" y="202" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle" font-family="monospace">${AppState.breakerClosed ? '69.0 kV ENERGIZED | 348.9 A' : 'ISOLATED / 0.0 A'}</text>
        `;
      }

      box.innerHTML = `<svg viewBox="0 0 400 280" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">${inner}</svg>`;
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (SubpartModalState.isOpen) closeSubpartModal();
        if (AppState.sldExpOpen) closeExpandedSLD();
      }
    });

    // TOAST NOTIFICATION
    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 3200);
    }

    // RESIZE HANDLER
    function onWindowResize() {
      if (!camera || !renderer) return;
      const width = window.innerWidth;
      const height = window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    }

    // MAIN RENDER LOOP (Wrapped in try/catch to ensure stability)
    function animate() {
      requestAnimationFrame(animate);
      try {
        const delta = clock.getDelta();

        if (controls && controls.enabled && typeof controls.update === 'function') {
          controls.update();
        }

        updateWalkMovement(delta);
        updateProximityHazard(delta);
        updateWalkInspectionReticle();
        updatePowerParticles(delta);
        if (faultMarker3D) faultMarker3D.rotation.y += delta * 2.4;
        updateCalloutPins();
        updateControlHouseRoof();
        renderSubpartTurntable(delta);

        if (renderer && scene && camera) {
          renderer.render(scene, camera);
        }
      } catch (err) {
        console.error("Render loop exception:", err);
      }
    }

    // SAFE THREE.JS AND ORBITCONTROLS BOOTSTRAPPER
    let initAttempts = 0;
    function checkThreeAndInit() {
      if (typeof THREE === 'undefined') {
        initAttempts++;
        if (initAttempts < 40) {
          setTimeout(checkThreeAndInit, 50);
          return;
        } else {
          const banner = document.getElementById('runtime-error-banner');
          const msgEl = document.getElementById('runtime-error-msg');
          if (banner && msgEl) {
            banner.style.display = 'block';
            msgEl.innerText = "Fatal: Three.js library failed to load within timeout.\\nCheck that libs/three.min.js or an active internet connection for CDN is available.";
          }
          return;
        }
      }

      // Check OrbitControls
      if (typeof THREE.OrbitControls === 'undefined') {
        initAttempts++;
        if (initAttempts < 40) {
          setTimeout(checkThreeAndInit, 50);
          return;
        } else {
          console.warn("THREE.OrbitControls not found after timeout, continuing with fallback.");
        }
      }

      init();
    }

    window.addEventListener('DOMContentLoaded', checkThreeAndInit);
    """

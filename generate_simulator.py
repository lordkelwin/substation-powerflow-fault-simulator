"""
generate_simulator.py
Assembles and generates the complete, self-contained substation_simulator.html.
Inlines OrbitControls directly for 100% offline & local file:/// reliability.
"""

import os
import sys

from sim_css import get_css_styles
from sim_ui import get_html_ui
from sim_data import get_js_data
from sim_audio import get_js_audio
from sim_textures import get_js_procedural_textures
from sim_models import get_js_models
from sim_core import get_js_app_core

def build_simulator():
    base_dir = os.path.dirname(__file__)
    output_path = os.path.join(base_dir, "substation_simulator.html")
    orbit_controls_path = os.path.join(base_dir, "libs", "OrbitControls.js")

    print(f"Reading OrbitControls from: {orbit_controls_path}")
    with open(orbit_controls_path, "r", encoding="utf-8") as f:
        orbit_controls_code = f.read()

    print(f"Generating complete Substation Simulator to: {output_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n")
        f.write("  <meta charset=\"UTF-8\">\n")
        f.write("  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        f.write("  <title>EE 415: 3D Substation Field Immersion & Exploded-View Simulator</title>\n")
        
        # Script tags for Three.js: Local primary, CDN fallback
        f.write("""
  <!-- Three.js (Local offline with CDN fallback) -->
  <script src="libs/three.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
""")
        
        # CSS Styles
        f.write(get_css_styles())
        f.write("\n</head>\n<body>\n")
        
        # HTML UI
        f.write(get_html_ui())
        
        # Inlined OrbitControls
        f.write("\n<!-- INLINED BATTLE-TESTED ORBITCONTROLS (100% Offline file:/// Ready) -->\n<script>\n")
        f.write(orbit_controls_code)
        f.write("\n</script>\n")

        # JavaScript logic
        f.write("\n<script>\n")
        f.write("// === MODULE 1: COMPONENT DATA & SPECIFICATIONS ===\n")
        f.write(get_js_data())
        f.write("\n// === MODULE 2: PROCEDURAL AUDIO SYNTHESIZER ===\n")
        f.write(get_js_audio())
        f.write("\n// === MODULE 3: PROCEDURAL TEXTURE GENERATOR ===\n")
        f.write(get_js_procedural_textures())
        f.write("\n// === MODULE 4: PROCEDURAL 3D MESH BUILDERS ===\n")
        f.write(get_js_models())
        f.write("\n// === MODULE 5: APPLICATION CORE, CONTROLS & RENDER LOOP ===\n")
        f.write(get_js_app_core())
        f.write("\n</script>\n</body>\n</html>\n")

    size = os.path.getsize(output_path)
    print(f"Successfully generated {output_path} ({size:,} bytes)")

if __name__ == "__main__":
    build_simulator()

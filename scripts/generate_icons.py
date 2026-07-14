#!/usr/bin/env python3
"""Fetch Lucide icons and generate inline SVG system JS"""

import re
import requests
from pathlib import Path

# Icons used across all pages
ICONS = [
    "menu", "x", "phone", "users", "award", "map-pin",
    "chevron-right", "star", "calendar", "clock",
    "arrow-right", "message-circle", "chevron-up", "chevron-down"
]

BASE_URL = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/"

def fetch_svg(name):
    url = f"{BASE_URL}{name}.svg"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    svg = resp.text.strip()
    # Ensure class attribute exists for styling
    if 'class=' not in svg:
        svg = svg.replace('<svg', '<svg class="lucide lucide-{name}"', 1)
    else:
        svg = svg.replace('class="', 'class="lucide lucide-{name} ', 1)
    return svg

def generate_js():
    output = "// Auto-generated from Lucide icons\nconst ICONS = {\n"
    
    for name in ICONS:
        try:
            svg = fetch_svg(name)
            # Escape for JS template literal
            svg_js = svg.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            output += f'  "{name}": `{svg_js}`,\n'
            print(f"✅ Fetched: {name}")
        except Exception as e:
            print(f"❌ Failed to fetch {name}: {e}")
            output += f'  "{name}": "",\n'
    
    output += """};\n\nfunction createIcon(name, attrs = {}) {
  const svg = ICONS[name];
  if (!svg) return '';
  const attrStr = Object.entries(attrs).map(([k,v]) => `${k}="${v}"`).join(' ');
  return svg.replace('<svg', `<svg ${attrStr}`);
}

// Replace all [data-lucide] elements with inline SVG
function initIcons() {
  document.querySelectorAll('[data-lucide]').forEach(el => {
    const name = el.getAttribute('data-lucide');
    const classes = el.className;
    const html = createIcon(name, { class: classes || 'lucide' });
    el.outerHTML = html;
  });
}

// DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initIcons);
} else {
  initIcons();
}
"""
    return output

if __name__ == "__main__":
    js_content = generate_js()
    output_path = Path("js/icons.js")
    output_path.write_text(js_content, encoding='utf-8')
    print(f"\nGenerated {output_path} with {len(ICONS)} icons")
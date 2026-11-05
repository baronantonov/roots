#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_map_section.py
Adds the interactive MAP (Карта) section to ROOTS dashboard.html and index.html.
Neatly marks all 29 relatives across 13 historical centers of settlement.
"""

import sys
import os
import shutil

DASHBOARD_PATH = sys.argv[1] if len(sys.argv) > 1 else "dashboard.html"
INDEX_PATH = sys.argv[2] if len(sys.argv) > 2 else "index.html"

# Verify files exist
if not os.path.exists(DASHBOARD_PATH):
    print(f"Error: {DASHBOARD_PATH} not found!")
    sys.exit(1)

with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Read dashboard.html ({len(html)} bytes)")

# 1. Add Leaflet CSS in <head> if not present
leaflet_css = """<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>"""
if "leaflet@1.9.4/dist/leaflet.css" not in html:
    html = html.replace("</head>", f"  {leaflet_css}\n</head>", 1)
    print("Added Leaflet CSS to <head>")

# 2. Add Leaflet JS before </body> if not present
leaflet_js = """<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>"""
if "leaflet@1.9.4/dist/leaflet.js" not in html:
    html = html.replace("</body>", f"{leaflet_js}\n</body>", 1)
    print("Added Leaflet JS before </body>")

# 3. Add MAP tab button in header-nav
old_nav_snippet = """      <button class="nav-tab-btn active" data-tab="tab-tree" onclick="activateTab('tab-tree')">
        <span>🌳 Древо</span>
        <span class="nav-count">29</span>
      </button>
      <button class="nav-tab-btn" data-tab="tab-surnames" id="tab-btn-surnames" onclick="activateTab('tab-surnames')">"""

new_nav_snippet = """      <button class="nav-tab-btn active" data-tab="tab-tree" onclick="activateTab('tab-tree')">
        <span>🌳 Древо</span>
        <span class="nav-count">29</span>
      </button>
      <button class="nav-tab-btn" data-tab="tab-map" id="tab-btn-map" onclick="activateTab('tab-map')">
        <span>🗺️ Карта</span>
        <span class="nav-count">29 чел.</span>
      </button>
      <button class="nav-tab-btn" data-tab="tab-surnames" id="tab-btn-surnames" onclick="activateTab('tab-surnames')">"""

if old_nav_snippet in html:
    html = html.replace(old_nav_snippet, new_nav_snippet, 1)
    print("Added 'Карта' button in header-nav")
else:
    print("Warning: old_nav_snippet not matched directly")

# Also update tab-geo label to ⏳ Хронология to prevent icon/meaning collision
html = html.replace(
    """<button class="nav-tab-btn" data-tab="tab-geo" onclick="activateTab('tab-geo')">\n        <span>🗺️ Хронология</span>""",
    """<button class="nav-tab-btn" data-tab="tab-geo" onclick="activateTab('tab-geo')">\n        <span>⏳ Хронология</span>"""
)

# 4. Insert Map CSS styles right before </style>
map_css = """
/* ==========================================================================
   INTERACTIVE MAP TAB (Leaflet + Archival Styling + Refactoring UI)
   ========================================================================== */
#tab-map.tab-panel {
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  padding: 0;
  overflow: hidden;
  display: none;
}
#tab-map.tab-panel.active {
  display: block;
}

.map-workspace-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  gap: 0;
  height: 100%;
  align-items: stretch;
  background: var(--bg-app);
}

.map-stage-container {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--bg-subtle);
}

/* Floating top filter bar */
.map-floating-bar {
  position: absolute;
  top: 14px;
  left: 14px;
  right: 14px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}
.map-floating-bar > * {
  pointer-events: auto;
}

.map-filters-row {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 8px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-default);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
  scrollbar-width: none;
}
.map-filters-row::-webkit-scrollbar { display: none; }

.map-filter-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--ink-500);
  white-space: nowrap;
  letter-spacing: 0.04em;
}

.map-pills-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: nowrap;
}

.map-filter-pill {
  appearance: none;
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: 20px;
  padding: 4px 10px;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-700);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  transition: all 0.15s ease;
}
.map-filter-pill:hover {
  background: var(--bg-surface);
  border-color: var(--ink-400);
  color: var(--ink-900);
}
.map-filter-pill.active {
  background: var(--ink-900);
  border-color: var(--ink-900);
  color: #FFFFFF;
}

.map-filter-pill .pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}
.map-filter-pill.pill-evd .pill-dot { background: var(--accent-seal); }
.map-filter-pill.pill-bar .pill-dot { background: var(--accent-pat); }
.map-filter-pill.pill-shep .pill-dot { background: #1B7340; }
.map-filter-pill.pill-kov .pill-dot { background: #8C6A24; }
.map-filter-pill.pill-mil .pill-dot { background: #4B5563; }

.map-filter-pill.active.pill-evd { background: var(--accent-seal); border-color: var(--accent-seal); color: #fff; }
.map-filter-pill.active.pill-bar { background: var(--accent-pat); border-color: var(--accent-pat); color: #fff; }
.map-filter-pill.active.pill-shep { background: #1B7340; border-color: #1B7340; color: #fff; }
.map-filter-pill.active.pill-kov { background: #8C6A24; border-color: #8C6A24; color: #fff; }
.map-filter-pill.active.pill-mil { background: #4B5563; border-color: #4B5563; color: #fff; }

.map-pill-badge {
  font-family: var(--font-mono);
  font-size: 11px;
  padding: 0 5px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.08);
}
.map-filter-pill.active .map-pill-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
}

.map-jumps-row {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.90);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-default);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  overflow-x: auto;
  scrollbar-width: none;
}
.map-jumps-row::-webkit-scrollbar { display: none; }

.map-jumps-scroll {
  display: flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}

.map-jump-chip {
  appearance: none;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  padding: 3px 9px;
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 500;
  color: var(--ink-700);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.map-jump-chip:hover {
  background: var(--bg-surface);
  border-color: var(--border-strong);
  color: var(--ink-900);
  transform: translateY(-1px);
}

.roots-map-element .leaflet-tile-pane {
  filter: saturate(0.92) contrast(0.98);
}
.roots-map-element {
  flex: 1;
  width: 100%;
  height: 100%;
  min-height: 200px;
  z-index: 1;
  background: #EAE6DF;
}

.map-loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--ink-500);
  gap: 12px;
  font-size: 13.5px;
}
.map-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid var(--border-default);
  border-top-color: var(--accent-seal);
  border-radius: 50%;
  animation: mapSpin 0.8s linear infinite;
}
@keyframes mapSpin {
  to { transform: rotate(360deg); }
}

/* Map stats badge bottom left */
.map-stats-badge {
  position: absolute;
  bottom: 14px;
  left: 14px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-default);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  font-size: 12px;
  color: var(--ink-700);
}
.map-stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.map-stat-sep {
  color: var(--border-strong);
}
.map-reset-btn {
  appearance: none;
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: 4px;
  padding: 2px 7px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--ink-700);
  cursor: pointer;
  margin-left: 6px;
  transition: all 0.15s ease;
}
.map-reset-btn:hover {
  background: var(--bg-surface);
  color: var(--ink-900);
}

/* Leaflet Custom Marker Pins */
.custom-map-pin {
  cursor: pointer;
  position: relative;
  transform: translate(-50%, -50%);
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.custom-map-pin:hover {
  transform: translate(-50%, -50%) scale(1.15);
  z-index: 1200 !important;
}
.custom-map-pin.active {
  transform: translate(-50%, -50%) scale(1.22);
  z-index: 1300 !important;
}

.pin-bubble {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 3px solid var(--accent-seal);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  position: relative;
  box-sizing: border-box;
}

.custom-map-pin.branch-evdokimov .pin-bubble {
  border-color: #9E3A26;
  background: #FAF0ED;
}
.custom-map-pin.branch-baronov .pin-bubble {
  border-color: #25527A;
  background: #EDF3F8;
}
.custom-map-pin.branch-shepelenko .pin-bubble {
  border-color: #1B7340;
  background: #EAF5EE;
}
.custom-map-pin.branch-kovalenko .pin-bubble {
  border-color: #8C6A24;
  background: #FAF5E8;
}
.custom-map-pin.branch-military .pin-bubble {
  border-color: #4B5563;
  background: #F3F4F6;
}

.pin-count-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  border-radius: 9px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: #FFFFFF;
  background: #9E3A26;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 0 3px;
  box-sizing: border-box;
}
.custom-map-pin.branch-baronov .pin-count-badge { background: #25527A; }
.custom-map-pin.branch-shepelenko .pin-count-badge { background: #1B7340; }
.custom-map-pin.branch-kovalenko .pin-count-badge { background: #8C6A24; }
.custom-map-pin.branch-military .pin-count-badge { background: #4B5563; }

.pin-pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid var(--accent-seal);
  opacity: 0;
  pointer-events: none;
}
.custom-map-pin.active .pin-pulse-ring {
  animation: pinPulse 2s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
}
@keyframes pinPulse {
  0% { transform: translate(-50%, -50%) scale(0.9); opacity: 0.8; }
  100% { transform: translate(-50%, -50%) scale(2.2); opacity: 0; }
}

/* Leaflet Popup Styling */
.leaflet-popup-content-wrapper {
  background: var(--bg-surface) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--border-default) !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.16) !important;
  padding: 0 !important;
  overflow: hidden;
}
.leaflet-popup-content {
  margin: 0 !important;
  line-height: 1.5 !important;
  font-family: var(--font-sans) !important;
  min-width: 270px;
  max-width: 320px;
}
.leaflet-popup-tip {
  background: var(--bg-surface) !important;
}

.map-popup-card {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.map-popup-tag {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent-seal);
}
.map-popup-tag.baronov { color: var(--accent-pat); }
.map-popup-tag.shepelenko { color: #1B7340; }
.map-popup-tag.kovalenko { color: #8C6A24; }
.map-popup-tag.military { color: #4B5563; }

.map-popup-title {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 700;
  color: var(--ink-900);
  margin: 0;
  line-height: 1.25;
}
.map-popup-region {
  font-size: 11.5px;
  color: var(--ink-500);
}
.map-popup-desc {
  font-size: 12px;
  color: var(--ink-700);
  margin: 2px 0 6px;
  line-height: 1.45;
}
.map-popup-persons-title {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--ink-900);
  border-top: 1px solid var(--border-subtle);
  padding-top: 8px;
}
.map-popup-persons-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 150px;
  overflow-y: auto;
}
.map-popup-person-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  padding: 4px 6px;
  background: var(--bg-subtle);
  border-radius: 4px;
}
.map-popup-person-name {
  font-weight: 600;
  color: var(--ink-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 190px;
}
.map-popup-detail-btn {
  appearance: none;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  color: var(--accent-seal);
  cursor: pointer;
  text-align: center;
  margin-top: 6px;
  transition: all 0.15s ease;
}
.map-popup-detail-btn:hover {
  background: var(--accent-seal-soft);
  border-color: var(--accent-seal);
}

/* RIGHT SIDEBAR: MAP DOSSIER & DIRECTORY */
.map-sidebar {
  height: 100%;
  overflow-y: auto;
  background: var(--bg-surface);
  border-left: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.map-sidebar-header {
  padding: 16px 18px 12px;
  border-bottom: 1px solid var(--border-default);
  background: var(--bg-surface);
  position: sticky;
  top: 0;
  z-index: 10;
}
.map-sidebar-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}
.map-sidebar-title-row h3 {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  color: var(--ink-900);
  margin: 0;
}
.map-sidebar-sub {
  font-size: 12px;
  color: var(--ink-500);
  margin: 0 0 10px;
  line-height: 1.45;
}

.map-search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  padding: 6px 10px;
}
.map-search-icon {
  font-size: 13px;
  color: var(--ink-400);
}
.map-search-field {
  flex: 1;
  background: transparent;
  border: none;
  font-family: var(--font-sans);
  font-size: 12.5px;
  color: var(--ink-900);
  outline: none;
}
.map-search-clear {
  appearance: none;
  background: transparent;
  border: none;
  font-size: 12px;
  color: var(--ink-500);
  cursor: pointer;
  padding: 0 4px;
}

/* Selected Location Card in Sidebar */
.map-selected-dossier {
  border-bottom: 1px solid var(--border-default);
  background: var(--bg-app);
}
.map-dossier-card {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.map-dossier-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.map-dossier-kicker {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent-seal);
}
.map-dossier-card.branch-baronov .map-dossier-kicker { color: var(--accent-pat); }
.map-dossier-card.branch-shepelenko .map-dossier-kicker { color: #1B7340; }
.map-dossier-card.branch-kovalenko .map-dossier-kicker { color: #8C6A24; }
.map-dossier-card.branch-military .map-dossier-kicker { color: #4B5563; }

.map-dossier-title {
  font-family: var(--font-serif);
  font-size: 21px;
  font-weight: 700;
  color: var(--ink-900);
  margin: 3px 0;
  line-height: 1.2;
}
.map-dossier-coords {
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--ink-500);
  margin-top: 2px;
}
.map-dossier-desc {
  font-size: 13px;
  line-height: 1.6;
  color: var(--ink-700);
  margin: 0;
}

.map-dossier-relatives-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  padding: 12px;
}
.map-relatives-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.map-relatives-header h4 {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--ink-700);
  margin: 0;
  letter-spacing: 0.05em;
}
.map-relatives-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.map-relative-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 8px 10px;
  background: var(--bg-subtle);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  transition: all 0.15s ease;
}
.map-relative-row:hover {
  background: #FFFFFF;
  border-color: var(--border-default);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}
.map-relative-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.map-rel-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--ink-700);
  flex-shrink: 0;
  overflow: hidden;
}
.map-rel-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.map-relative-meta {
  min-width: 0;
}
.map-rel-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--ink-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.map-rel-role {
  font-size: 11px;
  color: var(--ink-500);
}
.map-rel-action-btn {
  appearance: none;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 4px;
  padding: 4px 8px;
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 600;
  color: var(--accent-seal);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}
.map-rel-action-btn:hover {
  background: var(--accent-seal-soft);
  border-color: var(--accent-seal);
}

/* Places scroll list in sidebar */
.map-places-scroll {
  flex: 1;
  padding: 14px 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.map-place-item-card {
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: all 0.15s ease;
}
.map-place-item-card:hover {
  border-color: var(--border-strong);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.map-place-item-card.selected {
  border-color: var(--accent-seal);
  background: var(--accent-seal-soft);
}
.map-place-item-card.branch-baronov.selected {
  border-color: var(--accent-pat);
  background: var(--accent-pat-soft);
}
.map-place-item-card.branch-shepelenko.selected {
  border-color: #1B7340;
  background: #EAF5EE;
}
.map-place-item-card.branch-kovalenko.selected {
  border-color: #8C6A24;
  background: #FAF5E8;
}
.map-place-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.map-place-item-title {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 700;
  color: var(--ink-900);
  line-height: 1.2;
}
.map-place-item-region {
  font-size: 11px;
  color: var(--ink-500);
}
.map-place-item-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 2px;
}
.map-place-person-chip {
  font-size: 10.5px;
  padding: 2px 6px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  color: var(--ink-700);
}

/* Responsive Map Layout */
@media (max-width: 1024px) {
  .map-workspace-grid {
    grid-template-columns: 1fr;
    grid-template-rows: 52vh minmax(0, 1fr);
    height: 100%;
  }
  .map-sidebar {
    border-left: none;
    border-top: 1px solid var(--border-default);
  }
  .map-floating-bar {
    top: 8px;
    left: 8px;
    right: 8px;
    gap: 6px;
  }
  .map-filters-row {
    padding: 6px 10px;
  }
  .map-stats-badge {
    bottom: 8px;
    left: 8px;
    padding: 5px 10px;
    font-size: 11px;
  }
}
"""

if "/* INTERACTIVE MAP TAB" not in html:
    html = html.replace("</style>", f"{map_css}\n</style>", 1)
    print("Added Map CSS styles before </style>")

# 5. Insert #tab-map HTML panel right after #tab-tree
map_html_panel = """
  <!-- ====================================================================
       ВКЛАДКА: ИНТЕРАКТИВНАЯ ГЕОГРАФИЧЕСКАЯ КАРТА РОДА
       ==================================================================== -->
  <section class="tab-panel" id="tab-map">
    <div class="map-workspace-grid">

      <!-- ЛЕВАЯ ЧАСТЬ: ИНТЕРАКТИВНАЯ КАРТА С ПЛАВАЮЩИМИ ФИЛЬТРАМИ -->
      <div class="map-stage-container">
        
        <!-- Верхняя плавающая панель фильтрации и быстрых переходов -->
        <div class="map-floating-bar">
          <div class="map-filters-row">
            <span class="map-filter-label">Род / Ветвь:</span>
            <div class="map-pills-wrap">
              <button class="map-filter-pill active" data-branch="all" onclick="filterMapBranch('all')">
                <span>Все ветви</span>
                <span class="map-pill-badge">29</span>
              </button>
              <button class="map-filter-pill pill-evd" data-branch="evdokimov" onclick="filterMapBranch('evdokimov')">
                <span class="pill-dot"></span>
                <span>Евдокимовы (Волга / Крым)</span>
                <span class="map-pill-badge">12</span>
              </button>
              <button class="map-filter-pill pill-bar" data-branch="baronov" onclick="filterMapBranch('baronov')">
                <span class="pill-dot"></span>
                <span>Бароновы (Волхов / СПб)</span>
                <span class="map-pill-badge">9</span>
              </button>
              <button class="map-filter-pill pill-shep" data-branch="shepelenko" onclick="filterMapBranch('shepelenko')">
                <span class="pill-dot"></span>
                <span>Шепеленко (Степь / Самарканд)</span>
                <span class="map-pill-badge">5</span>
              </button>
              <button class="map-filter-pill pill-kov" data-branch="kovalenko" onclick="filterMapBranch('kovalenko')">
                <span class="pill-dot"></span>
                <span>Коваленко и Бринюк (с. Землянка)</span>
                <span class="map-pill-badge">4</span>
              </button>
              <button class="map-filter-pill pill-mil" data-branch="military" onclick="filterMapBranch('military')">
                <span class="pill-dot"></span>
                <span>ПМВ (Карпаты / Дейч-Габель)</span>
                <span class="map-pill-badge">1</span>
              </button>
            </div>
          </div>

          <div class="map-jumps-row">
            <span class="map-filter-label">Быстрый фокус:</span>
            <div class="map-jumps-scroll">
              <button class="map-jump-chip" onclick="flyToMapPlace('galaktionovo')">📍 с. Галактионово (Никольское)</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('soltsy_kirishi')">📍 Кириши / с. Сольцы</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('strelna')">📍 Стрельна (ул. Лодыгина)</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('spb')">📍 Санкт-Петербург</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('zemlyanka')">📍 с. Землянка (Сумщина)</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('perm')">📍 Пермь (Молотов)</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('perovo')">📍 Симферополь (Перово)</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('samarkand')">📍 Самарканд</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('kustanai')">📍 Кустанай</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('deutchgabel')">📍 Дейч-Габель (Чехия)</button>
              <button class="map-jump-chip" onclick="flyToMapPlace('nadvorna')">📍 Надворна (Карпаты)</button>
            </div>
          </div>
        </div>

        <!-- Контейнер самой Leaflet-карты -->
        <div id="roots-leaflet-map" class="roots-map-element">
          <div class="map-loading-placeholder">
            <div class="map-spinner"></div>
            <div>Загрузка интерактивной карты расселения...</div>
          </div>
        </div>

        <!-- Нижний бейдж статистики и легенды -->
        <div class="map-stats-badge">
          <div class="map-stat-item">
            <span class="map-stat-icon">🧭</span>
            <span><strong>13</strong> очагов</span>
          </div>
          <span class="map-stat-sep">·</span>
          <div class="map-stat-item">
            <span><strong>29</strong> родственников на карте</span>
          </div>
          <span class="map-stat-sep">·</span>
          <div class="map-stat-item">
            <span><strong>1785–2026 гг.</strong></span>
          </div>
          <button type="button" class="map-reset-btn" onclick="resetMapView()" title="Сбросить масштаб на всю географию">
            ⟲ Вся география
          </button>
        </div>

      </div>

      <!-- ПРАВАЯ ЧАСТЬ: ИНТЕРАКТИВНЫЙ АТЛАС МЕСТ И КАРТОЧКИ РОДСТВЕННИКОВ -->
      <aside class="map-sidebar">
        <div class="map-sidebar-header">
          <div class="map-sidebar-title-row">
            <h3>📍 Географический атлас семьи</h3>
            <span class="badge badge-corr" id="map-visible-badge">13 очагов</span>
          </div>
          <p class="map-sidebar-sub">Каждое село, город и рубеж, где жили, служили и трудились 7 поколений предков.</p>
          <div class="map-search-box">
            <span class="map-search-icon">🔍</span>
            <input type="text" id="map-search-input" class="map-search-field" placeholder="Поиск места, села или имени предка..." oninput="filterMapPlacesByText(this.value)">
            <button type="button" class="map-search-clear" id="map-search-clear-btn" onclick="clearMapSearch()" style="display:none;">✕</button>
          </div>
        </div>

        <!-- Карточка выбранной локации (детальная) -->
        <div id="map-selected-dossier" class="map-selected-dossier">
          <!-- Рендерится динамически -->
        </div>

        <!-- Справочник всех локаций списком -->
        <div class="map-places-scroll" id="map-places-scroll">
          <!-- Рендерится динамически -->
        </div>
      </aside>

    </div>
  </section>
"""

# Find closing </section> of tab-tree
# tab-tree ends around line 2416 where tab-scans starts:
tab_scans_marker = '<!-- ====================================================================\n       ВКЛАДКА 3: АРХИВНЫЕ СКАНЫ'
if tab_scans_marker not in html:
    # try alternate match
    tab_scans_marker = '<section class="tab-panel scrollable" id="tab-scans">'

if tab_scans_marker in html:
    html = html.replace(tab_scans_marker, f"{map_html_panel}\n\n  {tab_scans_marker}", 1)
    print("Inserted #tab-map section HTML")
else:
    print("Warning: tab_scans_marker not found!")

# 6. Cross-link in selectPerson: add "Показать на карте" button in dossier
old_kv_jurisdiction = """<div class="kv-key">Юрисдикция и места:</div>
        <div class="kv-val">${p.jurisdiction}</div>"""

new_kv_jurisdiction = """<div class="kv-key">Юрисдикция и места:</div>
        <div class="kv-val">
          ${p.jurisdiction}
          <div style="margin-top:6px;">
            <button type="button" class="person-link-chip" onclick="openPersonOnMap('${p.id}')" style="display:inline-flex;align-items:center;gap:4px;font-size:11.5px;padding:3px 8px;background:var(--bg-subtle);border:1px solid var(--border-default);border-radius:4px;cursor:pointer;">
              🗺️ Показать на карте
            </button>
          </div>
        </div>"""

if old_kv_jurisdiction in html:
    html = html.replace(old_kv_jurisdiction, new_kv_jurisdiction, 1)
    print("Added 'Показать на карте' button in person inspector dossier")

# 7. Update activateTab to handle tab-map invalidation
old_activate_tab = """  if (tabId === "tab-tree") {
    setTimeout(() => {
      clampCanvasBounds();
      updateCanvasTransform(false);
    }, 40);
  }"""

new_activate_tab = """  if (tabId === "tab-tree") {
    setTimeout(() => {
      clampCanvasBounds();
      updateCanvasTransform(false);
    }, 40);
  }
  if (tabId === "tab-map") {
    setTimeout(() => {
      if (window.rootsMap) {
        window.rootsMap.invalidateSize();
      } else if (typeof initRootsMap === "function") {
        initRootsMap();
      }
    }, 50);
  }"""

if old_activate_tab in html:
    html = html.replace(old_activate_tab, new_activate_tab, 1)
    print("Updated activateTab function for tab-map")

# 8. Add Map Data & Functions before the end of script
map_script = """
// ==========================================================================
// 8. GEOGRAPHICAL ATLAS & INTERACTIVE MAP MODULE (13 LOCATIONS, 29 RELATIVES)
// ==========================================================================
const MAP_LOCATIONS = [
  {
    id: "galaktionovo",
    name: "село Галактионово (Никольское, Жукотино тож, «Савин Городок»)",
    shortName: "с. Галактионово (Никольское)",
    lat: 55.3582,
    lng: 50.5361,
    zoom: 12,
    icon: "🏛️",
    region: "Чистопольский район, Татарстан (ранее Казанская губерния)",
    branch: "evdokimov",
    branchLabel: "Ветвь Евдокимовых (Волга)",
    roleText: "Родовое гнездо Евдокимовых на р. Каме и р. Прость с XVII века (Закамская засечная черта 1647 г.)",
    description: "Вотчинное село дворян Аристовых на месте булгарской крепости Джукетау. Здесь жил родоначальник фамилии Евдоким (1795 г.), где его потомки в 1861 г. получили фамилию Евдокимовы. В селе жили 4 поколения Евдокимовых, родились дед Николай Никандрович и 13 его детей, включая деда Шуру.",
    persons: ["P-0015", "P-0010", "P-0009", "P-0007", "P-0008", "P-0012", "P-0004"]
  },
  {
    id: "chistopol",
    name: "город Чистополь (на р. Каме)",
    shortName: "г. Чистополь",
    lat: 55.3644,
    lng: 50.6436,
    zoom: 12,
    icon: "⚓",
    region: "Казанская губерния / Татарстан",
    branch: "evdokimov",
    branchLabel: "Ветвь Евдокимовых / Беловых",
    roleText: "Уездный торговый центр на Каме, речные пристани и ярмарки",
    description: "Главный административный и торговый центр уезда. Сюда крестьяне села Жукотино возили хлеб на пристани; здесь находилось духовное правление и земские службы. Родина двоюродной прабабушки Веры Никандровны (сестры Николая) и ветви Беловых (Александр Белов).",
    persons: ["P-0013", "P-0014", "P-0007"]
  },
  {
    id: "soltsy_kirishi",
    name: "Кириши (историческое село Сольцы на Волхове)",
    shortName: "Кириши / с. Сольцы",
    lat: 59.4503,
    lng: 32.0161,
    zoom: 12,
    icon: "🌊",
    region: "Новоладожский уезд Санкт-Петербургской губ. / Ленинградская обл.",
    branch: "baronov",
    branchLabel: "Ветвь Бароновых (Приладожье)",
    roleText: "Родовое гнездо Бароновых на реке Волхов с XVIII века при имении Бестужевых",
    description: "Старинное приволховское село при каменной церкви Рождества Богородицы (1717 г.) и имении Бестужевых (где прошло детство 4 братьев-декабристов). Родина крестьянского рода Бароновых — волховских артельщиков и лоцманов. Здесь родились основатель прозвания Барон (1785), выкупные крестьяне 1861 г., прадед Василий и майор Валентин Баронов (1929).",
    persons: ["P-0026", "P-0025", "P-0024", "P-0017", "P-0023", "P-0005"]
  },
  {
    id: "strelna",
    name: "посёлок Стрельна (Петродворцовый район, ул. Лодыгина, 10)",
    shortName: "Стрельна (ул. Лодыгина, 10)",
    lat: 59.8544,
    lng: 30.0558,
    zoom: 13,
    icon: "🎖️",
    region: "Санкт-Петербург / Ленинград",
    branch: "baronov",
    branchLabel: "Ветвь Бароновых / Шепеленко",
    roleText: "Дом командира автобата майора В. В. Баронова и вычислительный центр БЭСМ-6",
    description: "Дом № 10 по улице Лодыгина, автобат, трамвайное кольцо № 36, Константиновский дворец и Финский залив. Здесь жил майор Валентин Васильевич Баронов, его супруга Нина Александровна Шепеленко (программист баллистики на ЭВМ БЭСМ-6) и родился отец заявителя Вадим Валентинович Баронов (1961 г.).",
    persons: ["P-0005", "P-0016", "P-0003"]
  },
  {
    id: "spb",
    name: "город Санкт-Петербург (Ленинград)",
    shortName: "Санкт-Петербург",
    lat: 59.9343,
    lng: 30.3351,
    zoom: 11,
    icon: "🏛️",
    region: "Северо-Запад России",
    branch: "baronov",
    branchLabel: "Современное поколение",
    roleText: "Город рождения заявителя Антона Евдокимова (16.08.1988) и его сестёр",
    description: "Колыбель современного поколения рода. Родной город заявителя Антона Вадимовича Евдокимова (1988 г.р.), его сестёр Дарьи (1998 г.р.) и Анастасии (2004 г.р.). Место учебы, работы и жизни матери Нины Александровны Евдокимовой и бабушки Нины Шепеленко.",
    persons: ["P-0001", "P-0021", "P-0022", "P-0002", "P-0016"]
  },
  {
    id: "zemlyanka",
    name: "село Землянка (Шосткинский район, Сумская область)",
    shortName: "с. Землянка (Сумщина)",
    lat: 51.7850,
    lng: 33.5850,
    zoom: 12,
    icon: "🌾",
    region: "Глуховский уезд Черниговской губ. / Шосткинский р-н Сумской обл.",
    branch: "kovalenko",
    branchLabel: "Ветвь Коваленко и Бринюк",
    roleText: "Родовое гнездо материнской бабушки Натальи Афанасьевны Коваленко",
    description: "Древнее северское село при храме Воскресения Христова (1785 г.). Родина прапрадеда Тимофея Бринюка, прабабушки Серафимы Бринюк, Афанасия Коваленко и бабушки заявителя Натальи Афанасьевны Коваленко (род. 13.04.1925), пережившей здесь раскулачивание и военное лихолетье.",
    persons: ["P-0029", "P-0028", "P-0027", "P-0006"]
  },
  {
    id: "perm",
    name: "город Пермь (в 1940–1957 гг. Молотов)",
    shortName: "г. Пермь (Молотов)",
    lat: 58.0105,
    lng: 56.2502,
    zoom: 11,
    icon: "⚙️",
    region: "Молотовская / Пермская область, Западный Урал",
    branch: "evdokimov",
    branchLabel: "Ветвь Евдокимовых / Коваленко",
    roleText: "Индустриальное сердце Урала: место встречи деда Шуры и бабушки Наташи",
    description: "Сюда в начале 1950-х годов после войны приехали Александр Николаевич Евдокимов с Волги и Наталья Афанасьевна Коваленко с Сумщины. В Молотове они создали крепкую семью и родили детей: дядю Виктора (1953 г.р.) и маму заявителя Нину Александровну Евдокимову (26.01.1956).",
    persons: ["P-0004", "P-0006", "P-0011", "P-0002"]
  },
  {
    id: "perovo",
    name: "посёлок Перово / город Симферополь",
    shortName: "Симферополь (Перово)",
    lat: 44.9272,
    lng: 34.0625,
    zoom: 12,
    icon: "🍇",
    region: "Симферопольский район, Крым",
    branch: "evdokimov",
    branchLabel: "Крымская ветвь Евдокимовых",
    roleText: "Крымская родовая усадьба и сады семьи Евдокимовых",
    description: "Теплый южный очаг семьи. Сюда из Перми дед Александр Николаевич и бабушка Наталья Афанасьевна перевезли детей. Здесь выросли Виктор и Нина, разбит семейный сад. Место вечного упокоения бабушки Натальи Афанасьевны (1925–2014) и деда Александра Николаевича.",
    persons: ["P-0004", "P-0006", "P-0011", "P-0002"]
  },
  {
    id: "kharkov",
    name: "Харьковская губерния (Слободская Украина)",
    shortName: "Харьковская губ.",
    lat: 49.9935,
    lng: 36.2304,
    zoom: 10,
    icon: "🌻",
    region: "Российская империя (Харьковская губерния)",
    branch: "shepelenko",
    branchLabel: "Ветвь Шепеленко",
    roleText: "Исторические корни рода Шепеленко до Столыпинского переселения 1912 г.",
    description: "Исконная хлеборобная родина рода Шепеленко. Отсюда прапрадед Иван Шепеленко с семьей и малолетней дочерью Клавдией в 1912 году в рамках аграрной реформы П. А. Столыпина отправился переселенческим эшелоном осваивать просторы Тургайских степей.",
    persons: ["P-0020", "P-0018"]
  },
  {
    id: "kustanai",
    name: "город Кустанай (Костанай, Тургайская область)",
    shortName: "г. Кустанай (Казахстан)",
    lat: 53.2198,
    lng: 63.6354,
    zoom: 11,
    icon: "🌾",
    region: "Кустанайский уезд Тургайской обл. / Северный Казахстан",
    branch: "shepelenko",
    branchLabel: "Ветвь Шепеленко (Степь)",
    roleText: "Столыпинский переселенческий надел Шепеленко (1912 г., ГАКО ф. 268)",
    description: "Степной переселенческий край на реке Тобол. Здесь Шепеленко обустраивали целинное хозяйство, поднимали хлеб и преодолевали лихолетье Гражданской войны. Родное место юности прабабушки Клавдии Ивановны и деда Степана.",
    persons: ["P-0020", "P-0018", "P-0019"]
  },
  {
    id: "samarkand",
    name: "город Самарканд (Узбекистан)",
    shortName: "г. Самарканд (Узбекистан)",
    lat: 39.6542,
    lng: 66.9597,
    zoom: 12,
    icon: "🕌",
    region: "Самаркандская область, Средняя Азия",
    branch: "shepelenko",
    branchLabel: "Ветвь Шепеленко (Восток)",
    roleText: "Послевоенный южный дом прабабушки Клавдии и деда Степана",
    description: "Древний шелковый оазис, ставший теплым семейным приютом для ветви Шепеленко после войны. Сюда в 1960-х годах на поезде и мотоцикле 'Урал' приезжал отец заявителя Вадим Валентинович к бабушке Клаве и деду Степану, о чем сохранились яркие семейные мемуары.",
    persons: ["P-0018", "P-0019", "P-0003"]
  },
  {
    id: "nadvorna",
    name: "город Надворна (Надвірна, Восточная Галиция)",
    shortName: "Надворна (Карпаты)",
    lat: 48.6317,
    lng: 24.5828,
    zoom: 11,
    icon: "⚔️",
    region: "Карпаты (ныне Ивано-Франковская область)",
    branch: "military",
    branchLabel: "Военный рубеж ПМВ (1915 г.)",
    roleText: "Поле боя Первой мировой: подвиг стрелка Николая Евдокимова 21.06.1915",
    description: "Карпатские предгорья, театр ожесточенных сражений Юго-Западного фронта Первой мировой войны. Здесь 21 июня 1915 года стрелок 1-й роты 410-го пехотного Усманского полка Николай Никандрович Евдокимов принял кровопролитный бой у Надворной и попал в плен (РГВИА ф. 16196).",
    persons: ["P-0007"]
  },
  {
    id: "deutchgabel",
    name: "лагерь Дейч-Габель (Jablonné v Podještědí, Богемия)",
    shortName: "лагерь Дейч-Габель (Чехия)",
    lat: 50.7656,
    lng: 14.7606,
    zoom: 12,
    icon: "⛓️",
    region: "Австро-Венгерская империя (ныне Чешская Республика)",
    branch: "military",
    branchLabel: "Военный плен ПМВ (1915–1918 гг.)",
    roleText: "Австрийский лагерь военнопленных: испытание и спасение прадеда Николая",
    description: "Один из крупнейших лагерей военнопленных солдат Русской императорской армии в Австро-Венгрии. Прадед Николай Никандрович провел здесь более 3 лет (картотека потерь ящ. 6417-А), выдержал тяготы плена, сохранил веру и вернулся в родное Никольское к жене и детям.",
    persons: ["P-0007"]
  }
];

let rootsMap = null;
let rootsMapMarkers = {};
let currentMapBranch = "all";
let currentSelectedPlaceId = "galaktionovo";

function initRootsMap() {
  const container = document.getElementById("roots-leaflet-map");
  if (!container) return;

  if (typeof L === "undefined") {
    container.innerHTML = `
      <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:24px;text-align:center;color:var(--ink-700);">
        <div style="font-size:32px;margin-bottom:8px;">🗺️</div>
        <h4 style="margin:0 0 6px;color:var(--ink-900);">Интерактивная карта готова</h4>
        <p style="font-size:13px;max-width:440px;color:var(--ink-500);line-height:1.5;">
          Для загрузки картографических тайлов OpenStreetMap требуется доступ к сети. Все 13 локаций и 29 родственников полностью доступны в каталоге справа!
        </p>
      </div>
    `;
    renderMapSidebar();
    return;
  }

  // Clear placeholder
  container.innerHTML = "";

  // Initialize Leaflet Map
  rootsMap = L.map("roots-leaflet-map", {
    center: [54.5, 45.0],
    zoom: 5,
    zoomControl: false
  });
  window.rootsMap = rootsMap;

  // Add zoom controls at bottom right
  L.control.zoom({ position: "bottomright" }).addTo(rootsMap);

  // CartoDB Positron elegant archival basemap
  // OpenStreetMap crisp tile layer with archival styling
  const osmLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(rootsMap);

  // Render markers
  renderMapMarkers();

  // Render sidebar
  renderMapSidebar();

  // Select initial place
  selectMapPlace("galaktionovo", false);
}

function renderMapMarkers() {
  if (!rootsMap || typeof L === "undefined") return;

  // Clear existing markers
  Object.values(rootsMapMarkers).forEach(m => rootsMap.removeLayer(m));
  rootsMapMarkers = {};

  const filteredPlaces = MAP_LOCATIONS.filter(loc => {
    if (currentMapBranch === "all") return true;
    return loc.branch === currentMapBranch;
  });

  filteredPlaces.forEach(loc => {
    const isSelected = loc.id === currentSelectedPlaceId;
    const pinHtml = `
      <div class="custom-map-pin branch-${loc.branch} ${isSelected ? 'active' : ''}" id="map-pin-${loc.id}">
        <div class="pin-bubble">
          <span>${loc.icon}</span>
          <span class="pin-count-badge">${loc.persons.length}</span>
        </div>
        <div class="pin-pulse-ring"></div>
      </div>
    `;

    const icon = L.divIcon({
      className: "custom-div-icon",
      html: pinHtml,
      iconSize: [40, 40],
      iconAnchor: [20, 20],
      popupAnchor: [0, -22]
    });

    const marker = L.marker([loc.lat, loc.lng], { icon: icon }).addTo(rootsMap);

    // Build Popup HTML
    const personsHtml = loc.persons.map(pid => {
      const p = PERSONS.find(item => item.id === pid);
      if (!p) return "";
      return `
        <div class="map-popup-person-item">
          <span class="map-popup-person-name"><b>${p.name.split(" ")[0]}</b> ${p.name.split(" ").slice(1).join(" ")}</span>
          <span style="font-family:var(--font-mono);font-size:10.5px;color:var(--ink-500);">${p.dates.split("·")[0].trim()}</span>
        </div>
      `;
    }).join("");

    const popupHtml = `
      <div class="map-popup-card">
        <div class="map-popup-tag ${loc.branch}">${loc.branchLabel}</div>
        <h4 class="map-popup-title">${loc.name}</h4>
        <div class="map-popup-region">📍 ${loc.region}</div>
        <div class="map-popup-desc">${loc.roleText}</div>
        <div class="map-popup-persons-title">Родственники в этом месте (${loc.persons.length}):</div>
        <div class="map-popup-persons-list">${personsHtml}</div>
        <button type="button" class="map-popup-detail-btn" onclick="selectMapPlace('${loc.id}', true)">
          Открыть досье места и персоналий →
        </button>
      </div>
    `;

    marker.bindPopup(popupHtml, { maxWidth: 320 });

    marker.on("click", () => {
      selectMapPlace(loc.id, true);
    });

    rootsMapMarkers[loc.id] = marker;
  });
}

function selectMapPlace(placeId, shouldCenter = true) {
  currentSelectedPlaceId = placeId;
  const loc = MAP_LOCATIONS.find(l => l.id === placeId);
  if (!loc) return;

  // Highlight marker
  document.querySelectorAll(".custom-map-pin").forEach(el => el.classList.remove("active"));
  const activePin = document.getElementById("map-pin-" + placeId);
  if (activePin) activePin.classList.add("active");

  // Center on map if requested
  if (shouldCenter && rootsMap) {
    rootsMap.flyTo([loc.lat, loc.lng], Math.max(loc.zoom, 9), {
      animate: true,
      duration: 0.9
    });
    if (rootsMapMarkers[placeId]) {
      rootsMapMarkers[placeId].openPopup();
    }
  }

  // Render detail card in sidebar
  renderSelectedPlaceDossier(loc);

  // Highlight in sidebar list
  document.querySelectorAll(".map-place-item-card").forEach(c => {
    c.classList.toggle("selected", c.getAttribute("data-place-id") === placeId);
  });
}

function renderSelectedPlaceDossier(loc) {
  const dossierContainer = document.getElementById("map-selected-dossier");
  if (!dossierContainer) return;

  const relativesHtml = loc.persons.map(pid => {
    const p = PERSONS.find(item => item.id === pid);
    if (!p) return "";
    const isAgripina = p.id === "P-0008";
    const avatarInner = isAgripina
      ? `<img src="photos/portrait-agripina-belova-oval.jpg" alt="${p.name}">`
      : `<span>${p.name[0]}</span>`;

    return `
      <div class="map-relative-row">
        <div class="map-relative-left">
          <div class="map-rel-avatar">${avatarInner}</div>
          <div class="map-relative-meta">
            <div class="map-rel-name"><b>${p.name}</b></div>
            <div class="map-rel-role">${p.role} · <span class="mono">${p.dates}</span></div>
          </div>
        </div>
        <button type="button" class="map-rel-action-btn" onclick="openPersonFromAnywhere('${p.id}')" title="Открыть карточку предка в семейном древе">
          🌳 В древо
        </button>
      </div>
    `;
  }).join("");

  dossierContainer.innerHTML = `
    <div class="map-dossier-card branch-${loc.branch}">
      <div class="map-dossier-top">
        <div>
          <div class="map-dossier-kicker">${loc.icon} ${loc.branchLabel}</div>
          <h3 class="map-dossier-title">${loc.name}</h3>
          <div class="map-dossier-coords">
            📍 ${loc.lat.toFixed(4)}°N, ${loc.lng.toFixed(4)}°E · ${loc.region}
          </div>
        </div>
        <button type="button" class="map-reset-btn" onclick="flyToMapPlace('${loc.id}')" style="margin:0;padding:5px 9px;">
          🎯 Фокус
        </button>
      </div>
      <p class="map-dossier-desc">${loc.description}</p>
      
      <div class="map-dossier-relatives-box">
        <div class="map-relatives-header">
          <h4>Родственники в этой точке (${loc.persons.length})</h4>
          <span class="badge ${loc.branch === 'baronov' ? 'badge-pat' : 'badge-corr'}">${loc.persons.length} чел.</span>
        </div>
        <div class="map-relatives-list">
          ${relativesHtml}
        </div>
      </div>
    </div>
  `;
}

function renderMapSidebar() {
  const listContainer = document.getElementById("map-places-scroll");
  if (!listContainer) return;

  const searchInput = document.getElementById("map-search-input");
  const query = searchInput ? searchInput.value.toLowerCase().trim() : "";

  const filtered = MAP_LOCATIONS.filter(loc => {
    // Branch filter
    if (currentMapBranch !== "all" && loc.branch !== currentMapBranch) {
      return false;
    }
    // Query filter
    if (query) {
      const matchName = loc.name.toLowerCase().includes(query);
      const matchRegion = loc.region.toLowerCase().includes(query);
      const matchPerson = loc.persons.some(pid => {
        const p = PERSONS.find(item => item.id === pid);
        return p && p.name.toLowerCase().includes(query);
      });
      return matchName || matchRegion || matchPerson;
    }
    return true;
  });

  const badgeEl = document.getElementById("map-visible-badge");
  if (badgeEl) {
    badgeEl.textContent = `${filtered.length} из ${MAP_LOCATIONS.length} очагов`;
  }

  if (filtered.length === 0) {
    listContainer.innerHTML = `
      <div style="padding:28px 16px;text-align:center;color:var(--ink-500);font-size:13px;">
        Ничего не найдено по запросу «${query}».
      </div>
    `;
    return;
  }

  listContainer.innerHTML = filtered.map(loc => {
    const isSelected = loc.id === currentSelectedPlaceId;
    const chipsHtml = loc.persons.map(pid => {
      const p = PERSONS.find(item => item.id === pid);
      if (!p) return "";
      return `<span class="map-place-person-chip">${p.name.split(" ")[0]} (${p.role})</span>`;
    }).join("");

    return `
      <div class="map-place-item-card branch-${loc.branch} ${isSelected ? 'selected' : ''}" data-place-id="${loc.id}" onclick="flyToMapPlace('${loc.id}')">
        <div class="map-place-item-top">
          <div class="map-place-item-title">${loc.icon} ${loc.shortName}</div>
          <span class="badge ${loc.branch === 'baronov' ? 'badge-pat' : 'badge-corr'}" style="font-size:10px;">${loc.persons.length} чел.</span>
        </div>
        <div class="map-place-item-region">📍 ${loc.region}</div>
        <div class="map-place-item-chips">${chipsHtml}</div>
      </div>
    `;
  }).join("");
}

function flyToMapPlace(placeId) {
  selectMapPlace(placeId, true);
}

function filterMapBranch(branch) {
  currentMapBranch = branch;
  document.querySelectorAll(".map-filter-pill").forEach(p => {
    p.classList.toggle("active", p.getAttribute("data-branch") === branch);
  });
  renderMapMarkers();
  renderMapSidebar();

  // Auto-fit bounds of visible markers
  if (rootsMap && typeof L !== "undefined") {
    const visibleMarkers = Object.values(rootsMapMarkers);
    if (visibleMarkers.length > 0) {
      const group = L.featureGroup(visibleMarkers);
      rootsMap.fitBounds(group.getBounds().pad(0.2), { animate: true, duration: 0.8 });
    }
  }
}

function filterMapPlacesByText(val) {
  const clearBtn = document.getElementById("map-search-clear-btn");
  if (clearBtn) {
    clearBtn.style.display = val ? "block" : "none";
  }
  renderMapSidebar();
}

function clearMapSearch() {
  const inp = document.getElementById("map-search-input");
  if (inp) {
    inp.value = "";
    filterMapPlacesByText("");
  }
}

function resetMapView() {
  currentMapBranch = "all";
  document.querySelectorAll(".map-filter-pill").forEach(p => {
    p.classList.toggle("active", p.getAttribute("data-branch") === "all");
  });
  clearMapSearch();
  renderMapMarkers();
  renderMapSidebar();
  if (rootsMap && typeof L !== "undefined") {
    rootsMap.setView([54.5, 45.0], 5, { animate: true });
  }
}

function openPersonOnMap(personId) {
  // Find which location has this person
  const loc = MAP_LOCATIONS.find(l => l.persons.includes(personId));
  activateTab("tab-map");
  setTimeout(() => {
    if (loc) {
      flyToMapPlace(loc.id);
    }
  }, 100);
}
"""

if "// 8. GEOGRAPHICAL ATLAS & INTERACTIVE MAP MODULE" not in html:
    html = html.replace("populateJumpSelect();", f"{map_script}\n\npopulateJumpSelect();\ninitRootsMap();", 1)
    print("Added Map Javascript module and initRootsMap invocation")

# Write out updated dashboard.html
with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Successfully wrote {DASHBOARD_PATH} ({len(html)} bytes)")

# Copy to index.html to ensure 100% parity
shutil.copyfile(DASHBOARD_PATH, INDEX_PATH)
print(f"Synchronized {INDEX_PATH} with {DASHBOARD_PATH}")

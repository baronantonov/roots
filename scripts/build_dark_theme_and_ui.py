#!/usr/bin/env python3
"""
build_dark_theme_and_ui.py
--------------------------
Complete, deterministic upgrade for ROOTS archival dashboard:
1. Early theme bootstrap in <head> to eliminate FOUC.
2. Complete CSS Custom Properties system (Light & Dark Obsidian/Slate).
3. Theme toggle button in header.
4. Rock-solid static toolbars for Tree and Map:
   - 1-row layout on desktop with plenty of room for all buttons.
   - Clean 2-row layout on mobile/tablet.
   - Viewport flex layout so canvas never overlaps with controls.
5. Rich graphic background:
   - 80x80 architectural blueprint coordinate grid.
   - 7 Generation bands (-520px to 3450px) with historical era dossiers on the left.
   - Year markers on the right.
   - Warm golden-bronze botany tree paths.
6. Designer node cards:
   - Branch gradient indicators (pat lapis, mat terracotta, self gold/emerald).
   - High-contrast typography in light and dark mode.
   - Status indicators, avatars with metallic/gold rings.
   - Smooth hover & selected glows.
"""

import os
import re
import sys

def apply_upgrades(file_path):
    print(f"Upgrading {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. EARLY THEME SCRIPT IN <HEAD>
    early_script = """<script>
(function() {
  try {
    var saved = localStorage.getItem('roots_theme');
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (saved === 'dark' || (!saved && prefersDark)) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  } catch(e) {}
})();
</script>"""
    if "roots_theme" not in content:
        content = content.replace("<head>", f"<head>\n{early_script}", 1)
        print("  [1/7] Injected early theme script into <head>")

    # 2. DESIGN TOKENS (LIGHT & DARK THEMES)
    idx_token_start = content.find("/* ==========================================================================\n   1. DESIGN SYSTEM")
    idx_token_end = content.find("*, *::before, *::after")
    if idx_token_start != -1 and idx_token_end != -1:
        new_tokens = """/* ==========================================================================
   1. DESIGN SYSTEM & TOKENS (Light Archival Paper + Dark Obsidian Slate)
   ========================================================================== */
:root,
html[data-theme="light"] {
  /* Surfaces */
  --bg-app: #FAF9F6;
  --bg-surface: #FFFFFF;
  --bg-subtle: #F3F1EC;
  --bg-elevated: #FFFFFF;
  --bg-header: #FFFFFF;
  --bg-footer: #FAF9F6;

  /* Borders */
  --border-subtle: #EFECE6;
  --border-default: #E5E2DC;
  --border-strong: #CCC7BD;
  --border-dark: #8C806E;

  /* Typography */
  --ink-900: #1C1917;
  --ink-700: #44403C;
  --ink-500: #78716C;
  --ink-400: #A8A29E;

  /* Accents */
  --accent-seal: #9E3A26;
  --accent-seal-hover: #832C1A;
  --accent-seal-soft: #FAF0ED;
  --accent-pat: #25527A;
  --accent-pat-soft: #EDF3F8;
  --accent-mat: #9E3A26;
  --accent-mat-soft: #FAF0ED;
  --accent-gold: #8C6A24;
  --accent-gold-soft: #FAF5E8;

  /* GPS Tokens */
  --st-strong-fg: #1F6B3D;
  --st-strong-bg: #EAF5EE;
  --st-strong-bd: #A3D9B5;

  --st-corr-fg: #23527C;
  --st-corr-bg: #EBF3F9;
  --st-corr-bd: #A8CCE8;

  --st-single-fg: #545D68;
  --st-single-bg: #F1F4F7;
  --st-single-bd: #CBD5E1;

  --st-hypo-fg: #8C531B;
  --st-hypo-bg: #FCF5E8;
  --st-hypo-bd: #F2D59B;

  /* Fonts */
  --font-serif: 'Cormorant Garamond', Georgia, 'Times New Roman', serif;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(28, 25, 23, 0.04);
  --shadow-sm: 0 1px 3px rgba(28, 25, 23, 0.05), 0 1px 2px rgba(28, 25, 23, 0.03);
  --shadow-md: 0 4px 16px rgba(28, 25, 23, 0.07);
  --shadow-lg: 0 12px 32px rgba(28, 25, 23, 0.09);
  --shadow-xl: 0 20px 48px rgba(28, 25, 23, 0.14);

  /* Radii & Motion */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 18px;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
}

/* DARK THEME: OBSIDIAN & DEEP SLATE */
html[data-theme="dark"] {
  --bg-app: #0B0E14;
  --bg-surface: #141822;
  --bg-subtle: #1C2230;
  --bg-elevated: #202737;
  --bg-header: #10131B;
  --bg-footer: #0B0E14;

  --border-subtle: #1A202E;
  --border-default: #263043;
  --border-strong: #3A4761;
  --border-dark: #546587;

  --ink-900: #F8FAFC;
  --ink-700: #CBD5E1;
  --ink-500: #94A3B8;
  --ink-400: #64748B;

  --accent-seal: #E05D44;
  --accent-seal-hover: #F07156;
  --accent-seal-soft: rgba(224, 93, 68, 0.18);
  --accent-pat: #4D97FF;
  --accent-pat-soft: rgba(77, 151, 255, 0.18);
  --accent-mat: #E06C53;
  --accent-mat-soft: rgba(224, 108, 83, 0.18);
  --accent-gold: #E5B842;
  --accent-gold-soft: rgba(229, 184, 66, 0.18);

  --st-strong-fg: #4ADE80;
  --st-strong-bg: rgba(74, 222, 128, 0.14);
  --st-strong-bd: rgba(74, 222, 128, 0.35);

  --st-corr-fg: #60A5FA;
  --st-corr-bg: rgba(96, 165, 250, 0.14);
  --st-corr-bd: rgba(96, 165, 250, 0.35);

  --st-single-fg: #94A3B8;
  --st-single-bg: rgba(148, 163, 184, 0.14);
  --st-single-bd: rgba(148, 163, 184, 0.3);

  --st-hypo-fg: #FBBF24;
  --st-hypo-bg: rgba(251, 191, 36, 0.14);
  --st-hypo-bd: rgba(251, 191, 36, 0.35);

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.4);
  --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.5);
  --shadow-md: 0 6px 20px rgba(0, 0, 0, 0.6);
  --shadow-lg: 0 14px 36px rgba(0, 0, 0, 0.7);
  --shadow-xl: 0 24px 56px rgba(0, 0, 0, 0.8);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-app: #0B0E14;
    --bg-surface: #141822;
    --bg-subtle: #1C2230;
    --bg-elevated: #202737;
    --bg-header: #10131B;
    --bg-footer: #0B0E14;

    --border-subtle: #1A202E;
    --border-default: #263043;
    --border-strong: #3A4761;
    --border-dark: #546587;

    --ink-900: #F8FAFC;
    --ink-700: #CBD5E1;
    --ink-500: #94A3B8;
    --ink-400: #64748B;

    --accent-seal: #E05D44;
    --accent-seal-hover: #F07156;
    --accent-seal-soft: rgba(224, 93, 68, 0.18);
    --accent-pat: #4D97FF;
    --accent-pat-soft: rgba(77, 151, 255, 0.18);
    --accent-mat: #E06C53;
    --accent-mat-soft: rgba(224, 108, 83, 0.18);
    --accent-gold: #E5B842;
    --accent-gold-soft: rgba(229, 184, 66, 0.18);

    --st-strong-fg: #4ADE80;
    --st-strong-bg: rgba(74, 222, 128, 0.14);
    --st-strong-bd: rgba(74, 222, 128, 0.35);

    --st-corr-fg: #60A5FA;
    --st-corr-bg: rgba(96, 165, 250, 0.14);
    --st-corr-bd: rgba(96, 165, 250, 0.35);

    --st-single-fg: #94A3B8;
    --st-single-bg: rgba(148, 163, 184, 0.14);
    --st-single-bd: rgba(148, 163, 184, 0.3);

    --st-hypo-fg: #FBBF24;
    --st-hypo-bg: rgba(251, 191, 36, 0.14);
    --st-hypo-bd: rgba(251, 191, 36, 0.35);
  }
}

"""
        content = content[:idx_token_start] + new_tokens + content[idx_token_end:]
        print("  [2/7] Injected Design System Tokens (Light & Dark)")

    # 3. FIX HARDCODED WHITE BACKGROUNDS IN SURFACES
    content = content.replace(".app-header {\n  background: #FFFFFF;", ".app-header {\n  background: var(--bg-header);")
    content = content.replace(".inspector-card {\n  background: #FFFFFF;", ".inspector-card {\n  background: var(--bg-surface);")
    content = content.replace(".canvas-floating-legend {\n  position: absolute;\n  bottom: 14px;\n  left: 14px;\n  background: rgba(255, 255, 255, 0.95);", ".canvas-floating-legend {\n  position: absolute;\n  bottom: 14px;\n  left: 14px;\n  background: var(--bg-surface);")
    content = content.replace(".section-card {\n  background: #FFFFFF;", ".section-card {\n  background: var(--bg-surface);")

    # 4. THEME TOGGLE BUTTON CSS & HTML
    theme_btn_css = """/* Theme Switcher Toggle */
.theme-toggle-btn {
  appearance: none;
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: 3px 9px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 600;
  color: var(--ink-700);
  margin-left: 6px;
  transition: all 0.15s ease;
  user-select: none;
  white-space: nowrap;
  flex-shrink: 0;
}
.theme-toggle-btn:hover {
  background: var(--border-default);
  color: var(--ink-900);
  transform: translateY(-1px);
}
"""
    if ".theme-toggle-btn" not in content:
        content = content.replace(".app-header {", theme_btn_css + "\n.app-header {", 1)

    theme_btn_html = """<span class="stat-pill gps"><span class="status-dot"></span>GPS 100%</span>
        <button type="button" class="theme-toggle-btn" id="theme-toggle-btn" onclick="toggleTheme()" title="Переключить тему (светлая / тёмная)" aria-label="Переключить тему оформления">
          <span id="theme-toggle-icon">🌙</span>
          <span id="theme-toggle-text">Тёмная</span>
        </button>"""
    content = content.replace('<span class="stat-pill gps"><span class="status-dot"></span>GPS 100%</span>', theme_btn_html, 1)
    print("  [3/7] Injected Theme Toggle Button CSS & HTML")

    # 5. STATIC TREE TOOLBAR (NO FLOATING, ZERO OVERLAP, 1-ROW DESKTOP)
    content = content.replace(
        """.canvas-workspace {
  height: 100%;
  width: 100%;
  position: relative;
  overflow: hidden;
  background: var(--bg-app);
}""",
        """.canvas-workspace {
  height: 100%;
  width: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: var(--bg-app);
}"""
    )
    content = content.replace(
        """.canvas-viewport {
  width: 100%;
  height: 100%;
  overflow: hidden;
  cursor: grab;
  position: relative;
  background: var(--bg-app);
  user-select: none;
}""",
        """.canvas-viewport {
  flex: 1;
  min-height: 0;
  width: 100%;
  position: relative;
  overflow: hidden;
  cursor: grab;
  background: var(--bg-app);
  user-select: none;
}"""
    )

    static_toolbar_css = """/* Static Non-Overlapping Toolbar (Sleek 1-Row Responsive Layout) */
.tree-toolbar {
  position: relative;
  flex-shrink: 0;
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 12px;
  padding: 6px 14px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  z-index: 25;
  box-shadow: var(--shadow-xs);
  min-height: 44px;
  box-sizing: border-box;
  overflow-x: auto;
  scrollbar-width: none;
}
.tree-toolbar::-webkit-scrollbar { display: none; }

.tree-toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}
.tree-toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.branch-filter-pills {
  display: inline-flex;
  align-items: center;
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: 20px;
  padding: 2px;
  gap: 2px;
}
.filter-pill {
  appearance: none;
  background: transparent;
  border: none;
  border-radius: 16px;
  padding: 4px 10px;
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 500;
  color: var(--ink-700);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.15s ease;
  white-space: nowrap;
  user-select: none;
}
.filter-pill:hover {
  background: var(--border-default);
  color: var(--ink-900);
}
.filter-pill.active {
  background: var(--ink-900);
  color: #FFFFFF;
  font-weight: 600;
}
[data-theme="dark"] .filter-pill.active {
  background: #F8FAFC;
  color: #0B0E14;
}
.filter-pill.pat.active {
  background: var(--accent-pat);
  color: #FFFFFF;
}
.filter-pill.mat.active {
  background: var(--accent-mat);
  color: #FFFFFF;
}

.view-mode-switch {
  display: inline-flex;
  background: var(--bg-subtle);
  padding: 2px;
  border-radius: 16px;
  border: 1px solid var(--border-default);
}
.btn-mode {
  appearance: none;
  background: transparent;
  border: none;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  color: var(--ink-700);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.btn-mode.active {
  background: var(--bg-surface);
  color: var(--ink-900);
  font-weight: 700;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.person-jump-select {
  appearance: none;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: 4px 24px 4px 10px;
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 500;
  color: var(--ink-900);
  box-shadow: var(--shadow-xs);
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23888888' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 7px center;
  max-width: 220px;
  min-width: 170px;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.person-jump-select:focus {
  outline: 2px solid var(--accent-seal);
  border-color: transparent;
}

.zoom-btn-group {
  display: inline-flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  box-shadow: var(--shadow-xs);
  padding: 2px 4px;
  overflow: hidden;
  gap: 2px;
}
.ctrl-btn {
  appearance: none;
  background: transparent;
  border: none;
  padding: 3px 7px;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-700);
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.12s;
  white-space: nowrap;
}
.ctrl-btn:hover {
  background: var(--bg-subtle);
  color: var(--ink-900);
}
.zoom-indicator {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  color: var(--ink-500);
  padding: 0 4px;
  min-width: 34px;
  text-align: center;
}"""

    # Replace old floating bar CSS
    old_fb_css = re.compile(
        r'/\* Minimalist Floating Controls Over Canvas.*?\n\.zoom-indicator \{.*?\n\}',
        re.DOTALL
    )
    content = old_fb_css.sub(static_toolbar_css, content, count=1)

    # Replace floating bar HTML
    old_fb_html = re.compile(
        r'<!-- ПЛАВАЮЩИЙ ТУЛБАР ВЕРХНИЙ -->\s*<div class="canvas-floating-bar">.*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    new_tb_html = """<!-- СТАТИЧНЫЙ ТУЛБАР ХОЛСТА (НЕ ПЕРЕКРЫВАЕТ ДРЕВО, МЕСТА ХВАТАЕТ ДЛЯ ВСЕХ КНОПОК) -->
        <div class="tree-toolbar">
          <div class="tree-toolbar-left">
            <div class="branch-filter-pills">
              <button type="button" class="filter-pill active" id="filter-all" onclick="filterCanvasBranch('all')">Все персоны (29)</button>
              <button type="button" class="filter-pill pat" id="filter-pat" onclick="filterCanvasBranch('pat')">⚓ Ветвь папы</button>
              <button type="button" class="filter-pill mat" id="filter-mat" onclick="filterCanvasBranch('mat')">🌾 Ветвь мамы</button>
            </div>

            <div class="view-mode-switch">
              <button type="button" class="btn-mode active" id="btn-view-canvas" onclick="switchTreeView('canvas')" title="Интерактивная схема">Схема</button>
              <button type="button" class="btn-mode" id="btn-view-grid" onclick="switchTreeView('grid')" title="Поколенный список">Список</button>
            </div>
          </div>

          <div class="tree-toolbar-right">
            <select class="person-jump-select" id="person-jump-select" onchange="jumpToPerson(this.value)" aria-label="Быстрый переход к предку">
              <option value="">🔍 Найти персону (29)...</option>
            </select>

            <div class="zoom-btn-group" id="canvas-zoom-controls">
              <button type="button" class="ctrl-btn" onclick="zoomCanvas(1.2)" title="Приблизить">+</button>
              <span class="zoom-indicator" id="zoom-level-text">100%</span>
              <button type="button" class="ctrl-btn" onclick="zoomCanvas(0.83)" title="Отдалить">−</button>
              <button type="button" class="ctrl-btn" onclick="fitCanvasToScreen(true)" title="Показать всё древо целиком" style="font-size:11px;padding:0 8px;width:auto;">🔍 Всё древо</button>
              <button type="button" class="ctrl-btn" onclick="jumpToPerson('P-0001')" title="К Антону (центр древа)" style="font-size:11px;padding:0 8px;width:auto;">🎯 К Антону</button>
            </div>
          </div>
        </div>"""
    content = old_fb_html.sub(new_tb_html, content, count=1)

    # Static Map Toolbar
    content = content.replace(
        """.map-floating-bar {
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
}""",
        """.map-toolbar {
  position: relative;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px 14px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  z-index: 20;
}"""
    )
    content = content.replace('<div class="map-floating-bar">', '<div class="map-toolbar">')

    # Media query updates for static toolbars
    content = content.replace(
        """  /* Floating controls on tablet/mobile */
  .canvas-floating-bar {
    top: 8px;
    left: 8px;
    right: 8px;
    flex-direction: column;
    align-items: stretch;
    gap: 6px;
  }""",
        """  /* Static toolbar on tablet/mobile */
  .tree-toolbar {
    flex-wrap: wrap;
    gap: 6px;
    padding: 6px 10px;
  }
  .tree-toolbar-left,
  .tree-toolbar-right {
    width: 100%;
    justify-content: space-between;
  }
  .person-jump-select {
    flex: 1;
    min-width: 120px;
  }"""
    )
    print("  [4/7] Built Static, Non-Overlapping Toolbars (Tree & Map)")

    # 6. GRAPHIC ARCHITECTURAL CANVAS & GENERATION BANDS & DESIGNER CARDS CSS
    canvas_and_cards_css = """/* ==========================================================================
   GRAPHIC ARCHITECTURAL CANVAS & GENERATION BANDS
   ========================================================================== */
.tree-grid-pattern {
  color: rgba(140, 122, 96, 0.08);
}
[data-theme="dark"] .tree-grid-pattern {
  color: rgba(255, 255, 255, 0.04);
}
.tree-grid-line {
  stroke: currentColor;
  stroke-width: 0.8px;
}
.tree-grid-dot {
  fill: currentColor;
}

/* Generation Eras & Bands Background */
.svg-gen-stripe {
  pointer-events: none;
  transition: fill 0.3s ease;
}
.gen-stripe-even {
  fill: rgba(140, 110, 70, 0.025);
}
.gen-stripe-odd {
  fill: transparent;
}
[data-theme="dark"] .gen-stripe-even {
  fill: rgba(255, 255, 255, 0.018);
}
[data-theme="dark"] .gen-stripe-odd {
  fill: transparent;
}

.svg-gen-divider {
  stroke: var(--border-default);
  stroke-dasharray: 6, 6;
  stroke-width: 1.2px;
  opacity: 0.8;
}
[data-theme="dark"] .svg-gen-divider {
  stroke: rgba(255, 255, 255, 0.09);
}

/* Era Banners (Left Information Strip, x = -470) */
.svg-epoch-badge-box {
  fill: var(--bg-surface);
  stroke: var(--border-default);
  stroke-width: 1.4px;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.04));
}
[data-theme="dark"] .svg-epoch-badge-box {
  fill: #161B26;
  stroke: rgba(255, 255, 255, 0.14);
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));
}

.svg-epoch-card-bg {
  fill: var(--bg-surface);
  stroke: var(--border-default);
  stroke-width: 1px;
  opacity: 0.96;
}
[data-theme="dark"] .svg-epoch-card-bg {
  fill: #141822;
  stroke: rgba(255, 255, 255, 0.1);
}

.svg-epoch-roman {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  fill: var(--accent-seal);
}
[data-theme="dark"] .svg-epoch-roman {
  fill: #F07156;
}

.svg-epoch-title {
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.05em;
  fill: var(--ink-900);
  text-transform: uppercase;
}
.svg-epoch-years {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  fill: var(--accent-pat);
  letter-spacing: 0.02em;
}
[data-theme="dark"] .svg-epoch-years {
  fill: #60A5FA;
}

.svg-epoch-context {
  font-family: var(--font-sans);
  font-size: 9.5px;
  fill: var(--ink-700);
  letter-spacing: 0.01em;
}

.svg-year-badge-rect {
  fill: var(--bg-surface);
  stroke: var(--border-default);
  stroke-width: 1.2px;
  filter: drop-shadow(0 1px 3px rgba(0,0,0,0.03));
}
[data-theme="dark"] .svg-year-badge-rect {
  fill: #161B26;
  stroke: rgba(255, 255, 255, 0.1);
}
.svg-year-badge-text {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  fill: var(--ink-700);
  letter-spacing: 0.05em;
}

/* Botany tree paths in background */
#canvas-tree-botany-group {
  transition: stroke 0.3s ease, opacity 0.3s ease;
}
[data-theme="dark"] #canvas-tree-botany-group {
  stroke: #D4AF37;
  opacity: 0.10;
}

/* Links & Lines */
.svg-link-line {
  fill: none;
  stroke: var(--border-strong);
  stroke-width: 2.2px;
  stroke-linecap: round;
  transition: stroke 0.25s, opacity 0.25s;
}
.svg-link-line.marriage {
  stroke: var(--accent-seal);
  stroke-width: 2.5px;
  stroke-dasharray: 5, 4;
}
.svg-link-line.pat {
  stroke: var(--accent-pat);
  stroke-width: 2.4px;
}
.svg-link-line.mat {
  stroke: var(--accent-mat);
  stroke-width: 2.4px;
}
.svg-union-circle {
  fill: var(--accent-seal);
  stroke: var(--bg-surface);
  stroke-width: 2px;
}
.svg-union-label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.03em;
  fill: var(--ink-700);
  user-select: none;
}

/* ==========================================================================
   DESIGNER NODE CARDS (Refined Editorial & Dark Mode Glow)
   ========================================================================== */
.canvas-node-card {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  padding: 8px 10px 8px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(28, 25, 23, 0.04), 0 2px 8px rgba(28, 25, 23, 0.02);
  transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.18s ease, border-color 0.18s ease, opacity 0.2s;
  user-select: none;
  overflow: hidden;
  position: relative;
}
[data-theme="dark"] .canvas-node-card {
  background: #151922;
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4), 0 6px 16px rgba(0, 0, 0, 0.3);
}

/* Gradient branch indicator strip on the left */
.canvas-node-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
  background: var(--border-strong);
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
  transition: width 0.15s ease, background 0.15s ease;
}
.canvas-node-card.pat::before {
  background: linear-gradient(180deg, #25527A 0%, #4D97FF 100%);
}
.canvas-node-card.mat::before {
  background: linear-gradient(180deg, #9E3A26 0%, #E06C53 100%);
}
.canvas-node-card.self::before {
  background: linear-gradient(180deg, #D4AF37 0%, #15803D 100%);
}

.canvas-node-card:hover {
  transform: translateY(-2.5px);
  border-color: #B5AEA4;
  box-shadow: 0 8px 22px rgba(28, 25, 23, 0.09);
}
[data-theme="dark"] .canvas-node-card:hover {
  border-color: rgba(255, 255, 255, 0.22);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6);
}
.canvas-node-card.pat:hover {
  border-color: var(--accent-pat);
}
[data-theme="dark"] .canvas-node-card.pat:hover {
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6), 0 0 16px rgba(77, 151, 255, 0.2);
}
.canvas-node-card.mat:hover {
  border-color: var(--accent-mat);
}
[data-theme="dark"] .canvas-node-card.mat:hover {
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6), 0 0 16px rgba(224, 108, 83, 0.2);
}
.canvas-node-card.self:hover {
  border-color: var(--accent-gold);
}
[data-theme="dark"] .canvas-node-card.self:hover {
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6), 0 0 16px rgba(229, 184, 66, 0.2);
}

.canvas-node-card.selected {
  border-color: var(--accent-seal) !important;
  box-shadow: 0 0 0 2px var(--accent-seal-soft), 0 8px 24px rgba(158, 58, 38, 0.18) !important;
  background: #FFFDFB;
}
[data-theme="dark"] .canvas-node-card.selected {
  background: #1B212D !important;
  border-color: var(--accent-seal) !important;
  box-shadow: 0 0 0 2px var(--accent-seal-soft), 0 8px 26px rgba(224, 93, 68, 0.3) !important;
}

.canvas-node-card.dimmed {
  opacity: 0.16;
  filter: grayscale(85%);
}

/* Card Avatar */
.card-avatar-wrap {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-subtle);
  border: 1.5px solid var(--border-default);
  box-shadow: var(--shadow-xs);
}
[data-theme="dark"] .card-avatar-wrap {
  background: #1C2332;
  border-color: rgba(255, 255, 255, 0.12);
}
.card-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.card-avatar-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  background: #15803D;
  color: #FFF;
  font-size: 8.5px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid var(--bg-surface);
}
.card-avatar-emoji {
  font-size: 22px;
  line-height: 1;
}
.card-avatar-rank {
  font-family: var(--font-mono);
  font-size: 7.5px;
  font-weight: 800;
  color: var(--accent-pat);
  letter-spacing: 0.04em;
  margin-top: 1px;
}

/* Card Text Content */
.card-content-wrap {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.5px;
}
.card-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
}
.card-id {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  color: var(--ink-500) !important;
}
.card-badge {
  font-family: var(--font-mono);
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.02em;
  padding: 1px 5px;
  border-radius: 4px;
  white-space: nowrap;
}
.card-role {
  font-size: 8.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--accent-mat);
  text-transform: uppercase;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
.canvas-node-card.pat .card-role { color: var(--accent-pat); }
.canvas-node-card.self .card-role { color: #15803D; }
[data-theme="dark"] .canvas-node-card.self .card-role { color: #4ADE80; }

.card-name {
  font-family: var(--font-serif);
  font-size: 14.5px;
  font-weight: 700;
  color: var(--ink-900) !important;
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-dates {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: var(--ink-700) !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
.card-place {
  font-size: 9px;
  color: var(--ink-500) !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

/* Leaflet Dark Mode Adjustments */
[data-theme="dark"] .leaflet-layer,
[data-theme="dark"] .leaflet-control-zoom-in,
[data-theme="dark"] .leaflet-control-zoom-out,
[data-theme="dark"] .leaflet-control-attribution {
  filter: brightness(0.85) invert(1) contrast(1.1) hue-rotate(200deg) saturate(0.65);
}
[data-theme="dark"] .leaflet-popup-content-wrapper,
[data-theme="dark"] .leaflet-popup-tip {
  background: #141822;
  color: #F8FAFC;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
}
[data-theme="dark"] .leaflet-container {
  background: #0B0E14;
}
"""
    # Replace existing card css
    old_card_css = re.compile(
        r'/\* ForeignObject HTML Card \*/\s*\.canvas-node-card \{.*?\n\.card-place \{.*?\n\}',
        re.DOTALL
    )
    content = old_card_css.sub(canvas_and_cards_css, content, count=1)
    print("  [5/7] Injected Canvas Architecture, Eras & Designer Cards CSS")

    # 7. ADD ARCHITECTURAL GRID IN SVG DEFS & CANVAS
    grid_def = """              <pattern id="tree-archival-grid" width="80" height="80" patternUnits="userSpaceOnUse" class="tree-grid-pattern">
                <path d="M 80 0 L 0 0 0 80" fill="none" class="tree-grid-line" />
                <circle cx="80" cy="0" r="1.5" class="tree-grid-dot" />
                <circle cx="0" cy="80" r="1.5" class="tree-grid-dot" />
              </pattern>"""
    if "tree-archival-grid" not in content:
        content = content.replace("</defs>", f"{grid_def}\n            </defs>", 1)

    grid_rect = """              <!-- Архитектурная координатная сетка -->
              <rect x="-520" y="0" width="4000" height="1750" fill="url(#tree-archival-grid)" pointer-events="none" />"""
    if "tree-archival-grid" in content and "Архитектурная координатная сетка" not in content:
        content = content.replace(
            '<g id="canvas-pan-zoom-group">',
            f'<g id="canvas-pan-zoom-group">\n{grid_rect}',
            1
        )

    # 8. UPDATE GEN_BANDS & renderSvgCanvas()
    new_gen_bands = """const GEN_BANDS = [
  {
    gen: "VII",
    num: 7,
    title: "VII ПОКОЛЕНИЕ · РУБЕЖ XVIII–XIX вв.",
    years: "ок. 1795–1825",
    epoch: "Павловская и Александровская Россия · Война 1812 г.",
    context: "Крепостное право в Казанской губ. (Аристовы) и под СПб. Родоначальники Барон и Евдоким.",
    y: 15,
    h: 215,
    markerDate: "1795 г."
  },
  {
    gen: "VI",
    num: 6,
    title: "VI ПОКОЛЕНИЕ · ВЕЛИКАЯ РЕФОРМА 1861 г.",
    years: "ок. 1825–1865",
    epoch: "Николаевская эпоха · Крымская война · Отмена крепостного права",
    context: "Обретение официальных наследственных фамилий Бароновы и Евдокимовы по уставным грамотам 1861 г.",
    y: 235,
    h: 200,
    markerDate: "1861 г."
  },
  {
    gen: "V",
    num: 5,
    title: "V ПОКОЛЕНИЕ · ВОЛЖСКИЕ ХЛЕБОПАШЦЫ И ЦЕЛИНА",
    years: "1865–1888",
    epoch: "Пореформенная Россия · Пароходство на Волге · Переселенцы",
    context: "Село Жукотино у Камы и переезд Шепеленко на свободные черноземы Тургайской области (Кустанай).",
    y: 440,
    h: 230,
    markerDate: "1880-е"
  },
  {
    gen: "IV",
    num: 4,
    title: "IV ПОКОЛЕНИЕ · ПЕРВАЯ МИРОВАЯ И РЕВОЛЮЦИЯ",
    years: "1888–1918",
    epoch: "Рубеж веков · Первая мировая война · Революция 1917 г. и Гражданская война",
    context: "Фронтовик Василий Баронов (плен в Венгрии), семейное гнездо Агриппины Беловой (13 детей в Жукотино).",
    y: 675,
    h: 245,
    markerDate: "1914 г."
  },
  {
    gen: "III",
    num: 3,
    title: "III ПОКОЛЕНИЕ · ВЕЛИКАЯ ОТЕЧЕСТВЕННАЯ ВОЙНА И ПОБЕДА",
    years: "1918–1945",
    epoch: "Индустриализация · ВОВ (1941–1945) · Блокада Ленинграда и возрождение",
    context: "Боевой путь майора Федора Шепеленко (штурмовики Ил-2), эвакуация казанских заводов, Победа.",
    y: 925,
    h: 250,
    markerDate: "1945 г."
  },
  {
    gen: "II",
    num: 2,
    title: "II ПОКОЛЕНИЕ · СОВЕТСКАЯ НАУКА, ЭВМ БЭСМ-6 И БАЙКОНУР",
    years: "1945–1988",
    epoch: "Космическая эра · Расцвет советской вычислительной техники и физики",
    context: "Математик Нина Шепеленко (баллистика на БЭСМ-6), Вадим Баронов (Стрельна, мотоцикл Урал), Ленинград.",
    y: 1180,
    h: 250,
    markerDate: "1965 г."
  },
  {
    gen: "I",
    num: 1,
    title: "I ПОКОЛЕНИЕ · СОВРЕМЕННОСТЬ И РОДОСЛОВНЫЙ АРХИВ",
    years: "1988–2026",
    epoch: "Цифровая эпоха · Новейшая история · Санкт-Петербург — Вьетнам",
    context: "Антон Евдокимов (автор исследования) и сёстры Кристина и Диана. GPS 100% доказанность.",
    y: 1435,
    h: 250,
    markerDate: "2026 г."
  }
];"""
    old_bands_re = re.compile(r'const GEN_BANDS = \[.*?\];', re.DOTALL)
    content = old_bands_re.sub(new_gen_bands, content, count=1)

    new_render_canvas_func = """function renderSvgCanvas() {
  const pMap = {};
  PERSONS.forEach(p => { pMap[p.id] = p; });

  const bandsEl = document.getElementById("canvas-generation-bands");
  if (bandsEl) {
    bandsEl.innerHTML = GEN_BANDS.map((b, idx) => {
      const isEven = idx % 2 === 0;
      const stripeClass = isEven ? "gen-stripe-even" : "gen-stripe-odd";
      return `
        <g class="svg-gen-band-group" data-gen="${b.gen}">
          <!-- Фоновая полоса эпохи от -520 до 3450 -->
          <rect class="svg-gen-stripe ${stripeClass}" x="-520" y="${b.y}" width="3970" height="${b.h}" />
          <!-- Верхняя разделительная архитектурная линия с точечной насечкой -->
          <line class="svg-gen-divider" x1="-520" y1="${b.y}" x2="3450" y2="${b.y}" />
          
          <!-- Левая карточка-плашка эпохи (Информативный исторический контекст, x = -470) -->
          <g class="svg-epoch-card" transform="translate(-470, ${b.y + 12})">
            <rect class="svg-epoch-card-bg" x="0" y="0" width="460" height="54" rx="10" />
            <!-- Римская цифра в медальоне -->
            <rect class="svg-epoch-badge-box" x="8" y="8" width="38" height="38" rx="8" />
            <text class="svg-epoch-roman" x="27" y="34" text-anchor="middle">${b.gen}</text>
            
            <!-- Заголовки и исторический контекст -->
            <text class="svg-epoch-title" x="56" y="21">${b.title}</text>
            <text class="svg-epoch-years" x="56" y="35">⏳ ${b.years} · ${b.epoch}</text>
            <text class="svg-epoch-context" x="56" y="47">${b.context}</text>
          </g>
          
          <!-- Правый маркер эпохи -->
          <g class="svg-epoch-right-marker" transform="translate(3220, ${b.y + 16})">
            <rect class="svg-year-badge-rect" x="0" y="0" width="85" height="24" rx="12" />
            <text class="svg-year-badge-text" x="42" y="16" text-anchor="middle">${b.markerDate}</text>
          </g>
        </g>
      `;
    }).join("");
  }

  const CW = 264;
  const CH = 118;

  let filialSvg = "";
  CANVAS_FILIAL.forEach(l => {
    const fromPt = CANVAS_COORDS[l.from];
    const toPt = CANVAS_COORDS[l.to];
    if (!fromPt || !toPt) return;
    const x1 = fromPt.x + CW / 2;
    const y1 = fromPt.y + CH;
    const x2 = toPt.x + CW / 2;
    const y2 = toPt.y;
    const midY = (y1 + y2) / 2;
    const path = `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;
    filialSvg += `<path class="svg-link-line ${l.side}" d="${path}" />`;
  });

  let marriageSvg = "";
  let unionNodesSvg = "";
  CANVAS_MARRIAGES.forEach(m => {
    const p1 = CANVAS_COORDS[m.p1];
    const p2 = CANVAS_COORDS[m.p2];
    if (!p1 || !p2) return;
    const yMid = p1.y + CH / 2;
    const knotX = (p1.x + CW / 2 + p2.x + CW / 2) / 2;
    const knotY = yMid;

    const leftX = Math.min(p1.x, p2.x) + CW;
    const rightX = Math.max(p1.x, p2.x);
    if (rightX > leftX) {
      marriageSvg += `<line class="svg-link-line marriage" x1="${leftX}" y1="${yMid}" x2="${rightX}" y2="${yMid}" />`;
    }

    unionNodesSvg += `
      <g transform="translate(${knotX}, ${knotY})">
        <circle class="svg-union-circle" r="8" />
        <text text-anchor="middle" class="svg-union-label" y="-12">💍 ${m.date}</text>
      </g>
    `;

    m.children.forEach(cid => {
      const cPt = CANVAS_COORDS[cid];
      if (!cPt) return;
      const cx = cPt.x + CW / 2;
      const cy = cPt.y;
      const midY = (knotY + cy) / 2;
      const childPath = `M ${knotX} ${knotY + 8} C ${knotX} ${midY}, ${cx} ${midY}, ${cx} ${cy}`;
      marriageSvg += `<path class="svg-link-line ${m.side}" d="${childPath}" />`;
    });
  });

  const linksEl = document.getElementById("canvas-links-group");
  if (linksEl) linksEl.innerHTML = filialSvg + marriageSvg;

  const marrEl = document.getElementById("canvas-marriages-group");
  if (marrEl) marrEl.innerHTML = unionNodesSvg;

  const nodesEl = document.getElementById("canvas-nodes-group");
  if (nodesEl) {
    nodesEl.innerHTML = Object.keys(CANVAS_COORDS).map(pid => {
      const coord = CANVAS_COORDS[pid];
      const p = pMap[pid];
      if (!p) return "";
      const sideClass = coord.side;
      const badgeLabel = p.status === "strongly-corroborated" ? "В АРХИВАХ ✓" :
                         p.status === "corroborated" ? "ПОДТВЕРЖДЕНО ✓" :
                         p.status === "single-source" ? "ИЗ ПАМЯТИ" : "АРХИВНЫЙ ПОИСК";
      const badgeClass = p.badgeClass;

      let avatarHtml = "";
      if (p.id === "P-0008") {
        avatarHtml = `
          <img class="card-avatar-img" src="photos/portrait-agripina-belova-oval.jpg" alt="${p.name}">
          <div class="card-avatar-badge" title="Подлинная фотография 1960-х гг.">📷</div>
        `;
      } else if (p.id === "P-0005") {
        avatarHtml = `
          <div style="display:flex;flex-direction:column;align-items:center;">
            <span class="card-avatar-emoji">🎖️</span>
            <span class="card-avatar-rank">МАЙОР</span>
          </div>
        `;
      } else if (p.id === "P-0007") {
        avatarHtml = `
          <div style="display:flex;flex-direction:column;align-items:center;">
            <span class="card-avatar-emoji">⚔️</span>
            <span class="card-avatar-rank" style="color:#8C2D19;">1914 г.</span>
          </div>
        `;
      } else if (p.id === "P-0003") {
        avatarHtml = `
          <div style="display:flex;flex-direction:column;align-items:center;">
            <span class="card-avatar-emoji">🏍️</span>
            <span class="card-avatar-rank">СТРЕЛЬНА</span>
          </div>
        `;
      } else if (p.id === "P-0002") {
        avatarHtml = `
          <div style="display:flex;flex-direction:column;align-items:center;">
            <span class="card-avatar-emoji">💻</span>
            <span class="card-avatar-rank" style="color:#9E3A26;">БЭСМ-6</span>
          </div>
        `;
      } else if (p.id === "P-0001") {
        avatarHtml = `
          <div style="display:flex;flex-direction:column;align-items:center;">
            <span class="card-avatar-emoji">🧭</span>
            <span class="card-avatar-rank" style="color:#15803D;">АВТОР</span>
          </div>
        `;
      } else if (p.id === "P-0010" || p.id === "P-0015" || p.id === "P-0009") {
        avatarHtml = `<span class="card-avatar-emoji">👴</span>`;
      } else if (p.id === "P-0016" || p.id === "P-0018" || p.id === "P-0006" || p.id === "P-0013" || p.id === "P-0021" || p.id === "P-0022" || p.id === "P-0023" || p.id === "P-0028") {
        avatarHtml = `<span class="card-avatar-emoji">👩</span>`;
      } else {
        avatarHtml = `<span class="card-avatar-emoji">👨</span>`;
      }

      const cleanDates = p.dates.replace(/\\s*\\([^)]*\\)/g, '').trim();
      const cardPlace = p.place ? ('📍 ' + p.place) : '';

      return `
        <foreignObject class="svg-node-foreign" x="${coord.x}" y="${coord.y}" width="${CW}" height="${CH}">
          <div xmlns="http://www.w3.org/1999/xhtml" class="canvas-node-card ${sideClass}" data-person-id="${p.id}" onclick="handleNodeCardClick('${p.id}')">
            <div class="card-avatar-wrap">
              ${avatarHtml}
            </div>
            <div class="card-content-wrap">
              <div class="card-meta-row">
                <span class="card-id">${p.id}</span>
                <span class="card-badge ${badgeClass}">${badgeLabel}</span>
              </div>
              <span class="card-role">${p.role || ''}</span>
              <div class="card-name" title="${p.name}">${p.name}</div>
              <div class="card-dates">${cleanDates}</div>
              ${cardPlace ? `<div class="card-place" title="${p.place}">${cardPlace}</div>` : ''}
            </div>
          </div>
        </foreignObject>
      `;
    }).join("");
  }
}"""
    idx_render_start = content.find("function renderSvgCanvas()")
    idx_render_end = content.find("function switchTreeView(viewType)")
    if idx_render_start != -1 and idx_render_end != -1:
        content = content[:idx_render_start] + new_render_canvas_func + "\n\n" + content[idx_render_end:]
    print("  [6/7] Updated renderSvgCanvas() and GEN_BANDS")

    # 9. THEME ENGINE FUNCTIONS IN JS
    theme_js = """
// ==========================================================================
// THEME SWITCHER (Dark / Light Theme Engine)
// ==========================================================================
function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  try {
    localStorage.setItem("roots_theme", next);
  } catch(e) {}
  updateThemeToggleBtn(next === "dark");
  if (typeof renderSvgCanvas === "function") {
    renderSvgCanvas();
  }
}

function updateThemeToggleBtn(isDark) {
  const icon = document.getElementById("theme-toggle-icon");
  const text = document.getElementById("theme-toggle-text");
  if (icon) icon.textContent = isDark ? "☀️" : "🌙";
  if (text) text.textContent = isDark ? "Светлая" : "Тёмная";
}

function initThemeUI() {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  updateThemeToggleBtn(isDark);
}
"""
    if "function toggleTheme()" not in content:
        content = content.replace("populateJumpSelect();", theme_js + "\ninitThemeUI();\npopulateJumpSelect();", 1)
        print("  [7/7] Added toggleTheme() and initThemeUI() JavaScript")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully upgraded {file_path}!\n")

def main():
    apply_upgrades("dashboard.html")
    apply_upgrades("index.html")

if __name__ == "__main__":
    main()

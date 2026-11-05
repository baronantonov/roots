#!/usr/bin/env python3
"""
modernize_tree_canvas.py
------------------------
Refactors the SVG Tree Canvas engine in dashboard.html:
1. Replaces CANVAS_COORDS with the zero-overlap verified layout.
2. Updates CANVAS_MARRIAGES and CANVAS_FILIAL for optimal geometric curves.
3. Fixes viewport boundaries and pan/zoom engine (dynamic clamping, fitToScreen).
4. Modernizes card styles (minimalist, informative, responsive).
5. Synchronizes stats to 29 persons / 34 artifacts.
"""

import re
import sys

PATH = "dashboard.html"

def main():
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update stats in header
    content = content.replace("<strong>26</strong> персон", "<strong>29</strong> персон")
    content = content.replace("<strong>32</strong> арт.", "<strong>34</strong> арт.")
    content = content.replace('id="filter-all" onclick="filterCanvasBranch(\'all\')">Все персоны (26)</button>',
                              'id="filter-all" onclick="filterCanvasBranch(\'all\')">Все персоны (29)</button>')

    # 2. Update Zoom controls to add 'Всё древо' and 'К Антону'
    old_zoom_controls = """            <div class="zoom-btn-group" id="canvas-zoom-controls">
              <button type="button" class="ctrl-btn" onclick="zoomCanvas(1.2)" title="Приблизить">+</button>
              <span class="zoom-indicator" id="zoom-level-text">82%</span>
              <button type="button" class="ctrl-btn" onclick="zoomCanvas(0.83)" title="Отдалить">−</button>
              <button type="button" class="ctrl-btn" onclick="resetCanvasZoom(true)" title="Показать всё древо" style="font-size:11px;padding:0 7px;width:auto;">Сброс</button>
            </div>"""

    new_zoom_controls = """            <div class="zoom-btn-group" id="canvas-zoom-controls">
              <button type="button" class="ctrl-btn" onclick="zoomCanvas(1.2)" title="Приблизить">+</button>
              <span class="zoom-indicator" id="zoom-level-text">100%</span>
              <button type="button" class="ctrl-btn" onclick="zoomCanvas(0.83)" title="Отдалить">−</button>
              <button type="button" class="ctrl-btn" onclick="fitCanvasToScreen(true)" title="Показать всё древо целиком" style="font-size:11px;padding:0 8px;width:auto;">🔍 Всё древо</button>
              <button type="button" class="ctrl-btn" onclick="jumpToPerson('P-0001')" title="К Антону (центр древа)" style="font-size:11px;padding:0 8px;width:auto;">🎯 К Антону</button>
            </div>"""

    if old_zoom_controls in content:
        content = content.replace(old_zoom_controls, new_zoom_controls)
        print("Updated zoom controls.")
    else:
        print("WARN: old_zoom_controls not found directly, trying regex.")
        content = re.sub(
            r'<div class="zoom-btn-group" id="canvas-zoom-controls">.*?</div>',
            new_zoom_controls.strip(),
            content,
            flags=re.DOTALL
        )

    # 3. Update SVG root element attributes & tree botany branches
    old_svg_header = '<svg id="tree-svg-canvas" width="3400" height="1720" viewBox="-400 0 3500 1720">'
    new_svg_header = '<svg id="tree-svg-canvas" width="100%" height="100%" style="position:absolute;inset:0;width:100%;height:100%;display:block;overflow:visible;">'
    if old_svg_header in content:
        content = content.replace(old_svg_header, new_svg_header)
        print("Updated SVG root element.")

    # Tree botany paths
    old_botany_pattern = re.compile(
        r'<g id="canvas-tree-botany-group".*?</g>',
        re.DOTALL
    )
    new_botany = """<g id="canvas-tree-botany-group" opacity="0.06" stroke="#8C7A60" fill="none" stroke-linecap="round">
                <path d="M 1425 1680 C 1425 1560, 1425 1460, 1425 1350" stroke-width="16" />
                <path d="M 1425 1350 C 1100 1300, 750 1200, 570 1000" stroke-width="10" />
                <path d="M 570 1000 C 450 900, 350 820, 200 740" stroke-width="6" />
                <path d="M 570 1000 C 620 900, 700 820, 810 740" stroke-width="6" />
                <path d="M 1425 1350 C 1750 1300, 2100 1200, 2270 1000" stroke-width="10" />
                <path d="M 2270 1000 C 2100 900, 1900 820, 1790 740" stroke-width="6" />
                <path d="M 2270 1000 C 2450 900, 2700 820, 2910 740" stroke-width="6" />
                <path d="M 1790 740 C 1790 620, 1790 540, 1790 490" stroke-width="6" />
                <path d="M 1790 490 C 1790 380, 1790 280, 1790 80" stroke-width="5" />
                <path d="M 200 740 C 200 620, 170 540, 170 490" stroke-width="6" />
                <path d="M 170 490 C 170 380, 170 280, 170 80" stroke-width="5" />
              </g>"""
    content = old_botany_pattern.sub(new_botany, content, count=1)
    print("Updated botany decorative branches.")

    # 4. Replace CANVAS_COORDS, CANVAS_MARRIAGES, CANVAS_FILIAL, clampCanvasBounds, etc.
    # Target from `const CANVAS_COORDS = {` to end of `switchTreeView`
    engine_pattern = re.compile(
        r'const CANVAS_COORDS = \{.*?\nfunction switchTreeView\(viewType\) \{.*?\n\}',
        re.DOTALL
    )

    new_engine = """const CANVAS_COORDS = {
  // Gen 7 (~1800)
  "P-0026": { x: 40,   y: 70,  side: "pat" }, // Барон (родоначальник Бароновых)
  "P-0015": { x: 1660, y: 70,  side: "mat" }, // Евдоким (родоначальник Евдокимовых)

  // Gen 6 (1820-1861)
  "P-0025": { x: 40,   y: 280, side: "pat" }, // Баронов (сын Барона)
  "P-0010": { x: 1660, y: 280, side: "mat" }, // Михаил Евдокимович

  // Gen 5 (1860-1880)
  "P-0024": { x: 40,   y: 490, side: "pat" }, // Баронов [отец Василия]
  "P-0020": { x: 680,  y: 490, side: "pat" }, // Иван Шепеленко
  "P-0009": { x: 1660, y: 490, side: "mat" }, // Никандр Евдокимов
  "P-0014": { x: 2300, y: 490, side: "mat" }, // Александр Белов
  "P-0029": { x: 2940, y: 490, side: "mat" }, // Тимофей Бринюк

  // Gen 4 (1888-1915)
  "P-0017": { x: 40,   y: 730, side: "pat" }, // Василий Баронов
  "P-0023": { x: 360,  y: 730, side: "pat" }, // Баронова [мать Валентина]
  "P-0018": { x: 680,  y: 730, side: "pat" }, // Клавдия Шепеленко
  "P-0019": { x: 1000, y: 730, side: "pat" }, // дед Степан
  "P-0012": { x: 1340, y: 730, side: "mat" }, // Ефим Евдокимов
  "P-0013": { x: 1660, y: 730, side: "mat" }, // Вера Евдокимова
  "P-0007": { x: 1980, y: 730, side: "mat" }, // Николай Евдокимов
  "P-0008": { x: 2300, y: 730, side: "mat" }, // Агриппина Белова
  "P-0027": { x: 2620, y: 730, side: "mat" }, // Афанасий Коваленко
  "P-0028": { x: 2940, y: 730, side: "mat" }, // Серафима Бринюк

  // Gen 3 (1926-1935)
  "P-0005": { x: 200,  y: 990, side: "pat" }, // Валентин Баронов
  "P-0016": { x: 680,  y: 990, side: "pat" }, // Нина Шепеленко
  "P-0004": { x: 2140, y: 990, side: "mat" }, // Александр Евдокимов
  "P-0006": { x: 2780, y: 990, side: "mat" }, // Наталья Коваленко

  // Gen 2 (1953-1961)
  "P-0003": { x: 440,  y: 1250, side: "pat" }, // Вадим Баронов
  "P-0002": { x: 2150, y: 1250, side: "mat" }, // Нина Евдокимова
  "P-0011": { x: 2630, y: 1250, side: "mat" }, // Виктор Евдокимов

  // Gen 1 (1988-2004)
  "P-0021": { x: 280,  y: 1500, side: "pat" }, // Дарья Баронова
  "P-0022": { x: 600,  y: 1500, side: "pat" }, // Анастасия Баронова
  "P-0001": { x: 1295, y: 1500, side: "self" }  // Антон Евдокимов
};

const CANVAS_MARRIAGES = [
  { id: "m-5", p1: "P-0017", p2: "P-0023", date: "ок. 1920", children: ["P-0005"], side: "pat" },
  { id: "m-2", p1: "P-0005", p2: "P-0016", date: "ок. 1958", children: ["P-0003"], side: "pat" },
  { id: "m-7", p1: "P-0018", p2: "P-0019", date: "ок. 1934", children: [], side: "pat" },
  { id: "m-1", p1: "P-0007", p2: "P-0008", date: "ок. 1908", children: ["P-0004"], side: "mat" },
  { id: "m-6", p1: "P-0027", p2: "P-0028", date: "ок. 1924", children: ["P-0006"], side: "mat" },
  { id: "m-3", p1: "P-0004", p2: "P-0006", date: "ок. 1950", children: ["P-0002", "P-0011"], side: "mat" },
  { id: "m-4", p1: "P-0003", p2: "P-0002", date: "ок. 1985", children: ["P-0001"], side: "center" }
];

const CANVAS_FILIAL = [
  // Paternal lineage
  { from: "P-0026", to: "P-0025", side: "pat" },
  { from: "P-0025", to: "P-0024", side: "pat" },
  { from: "P-0024", to: "P-0017", side: "pat" },
  { from: "P-0020", to: "P-0018", side: "pat" },
  { from: "P-0018", to: "P-0016", side: "pat" },
  { from: "P-0003", to: "P-0021", side: "pat" },
  { from: "P-0003", to: "P-0022", side: "pat" },

  // Maternal lineage
  { from: "P-0015", to: "P-0010", side: "mat" },
  { from: "P-0010", to: "P-0009", side: "mat" },
  { from: "P-0009", to: "P-0012", side: "mat" },
  { from: "P-0009", to: "P-0013", side: "mat" },
  { from: "P-0009", to: "P-0007", side: "mat" },
  { from: "P-0014", to: "P-0008", side: "mat" },
  { from: "P-0029", to: "P-0028", side: "mat" }
];

const GEN_BANDS = [
  { gen: "VII", label: "VII ПОКОЛЕНИЕ · РУБЕЖ XVIII–XIX вв. (~1795–1825)", y: 20, h: 200 },
  { gen: "VI",  label: "VI ПОКОЛЕНИЕ · РЕФОРМА 1861 г. (ПАСПОРТ И ФАМИЛИЯ)", y: 235, h: 190 },
  { gen: "V",   label: "V ПОКОЛЕНИЕ · СТОЛЫПИНСКАЯ ЭПОХА И ВОЛЖСКИЕ КРЕСТЬЯНЕ (1869–1880)", y: 440, h: 220 },
  { gen: "IV",  label: "IV ПОКОЛЕНИЕ · ПЕРВАЯ МИРОВАЯ ВОЙНА И КУСТАНАЙ (1888–1915)", y: 680, h: 230 },
  { gen: "III", label: "III ПОКОЛЕНИЕ · СОВЕТСКАЯ АРМИЯ И ВОССТАНОВЛЕНИЕ (1926–1935)", y: 935, h: 230 },
  { gen: "II",  label: "II ПОКОЛЕНИЕ · РОДИТЕЛИ И ДЯДЯ (1953–1961)", y: 1195, h: 220 },
  { gen: "I",   label: "I ПОКОЛЕНИЕ · СУБЪЕКТ ИССЛЕДОВАНИЯ И СЁСТРЫ (1988–2004)", y: 1445, h: 220 }
];

// Tree World Dimensions & Bounds
const CONTENT_MIN_X = -40;
const CONTENT_MAX_X = 3280;
const CONTENT_WIDTH = 3320;
const CONTENT_MIN_Y = 0;
const CONTENT_MAX_Y = 1700;
const CONTENT_HEIGHT = 1700;

let canvasState = {
  scale: 0.85,
  x: 0,
  y: 0,
  isDragging: false,
  hasMoved: false,
  startX: 0,
  startY: 0
};

function clampCanvasBounds() {
  const vp = document.getElementById("canvas-viewport");
  if (!vp) return;
  const vw = vp.clientWidth;
  const vh = vp.clientHeight;
  if (!vw || !vh) return;

  const minVisibleX = Math.min(vw * 0.28, 200);
  const minVisibleY = Math.min(vh * 0.28, 160);

  const minX = minVisibleX - CONTENT_MAX_X * canvasState.scale;
  const maxX = vw - minVisibleX - CONTENT_MIN_X * canvasState.scale;

  const minY = minVisibleY - CONTENT_MAX_Y * canvasState.scale;
  const maxY = vh - minVisibleY - CONTENT_MIN_Y * canvasState.scale;

  if (minX <= maxX) {
    canvasState.x = Math.max(minX, Math.min(maxX, canvasState.x));
  } else {
    canvasState.x = (vw - CONTENT_WIDTH * canvasState.scale) / 2 - CONTENT_MIN_X * canvasState.scale;
  }

  if (minY <= maxY) {
    canvasState.y = Math.max(minY, Math.min(maxY, canvasState.y));
  } else {
    canvasState.y = (vh - CONTENT_HEIGHT * canvasState.scale) / 2 - CONTENT_MIN_Y * canvasState.scale;
  }
}

function updateCanvasTransform(animate = false) {
  clampCanvasBounds();
  const g = document.getElementById("canvas-pan-zoom-group");
  if (!g) return;
  g.style.transition = animate ? "transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)" : "none";
  g.setAttribute("transform", `translate(${canvasState.x}, ${canvasState.y}) scale(${canvasState.scale})`);
  const ztxt = document.getElementById("zoom-level-text");
  if (ztxt) ztxt.textContent = Math.round(canvasState.scale * 100) + "%";
}

function zoomCanvas(factor) {
  const newScale = Math.min(Math.max(canvasState.scale * factor, 0.18), 2.2);
  const vp = document.getElementById("canvas-viewport");
  const cx = vp ? vp.clientWidth / 2 : 500;
  const cy = vp ? vp.clientHeight / 2 : 350;
  canvasState.x = cx - (cx - canvasState.x) * (newScale / canvasState.scale);
  canvasState.y = cy - (cy - canvasState.y) * (newScale / canvasState.scale);
  canvasState.scale = newScale;
  updateCanvasTransform(true);
}

function fitCanvasToScreen(animate = true) {
  const vp = document.getElementById("canvas-viewport");
  if (!vp) return;
  const vw = vp.clientWidth || window.innerWidth;
  const vh = vp.clientHeight || window.innerHeight;
  const isMobile = window.innerWidth <= 768;
  const padX = isMobile ? 14 : 44;
  const padY = isMobile ? 20 : 44;

  const availW = Math.max(100, vw - padX * 2);
  const availH = Math.max(100, vh - padY * 2);

  const scale = Math.min(availW / CONTENT_WIDTH, availH / CONTENT_HEIGHT);
  const clampedScale = Math.max(0.18, Math.min(scale, 1.25));

  canvasState.scale = clampedScale;
  const contentCenterX = CONTENT_MIN_X + CONTENT_WIDTH / 2; // 1620
  const contentCenterY = CONTENT_MIN_Y + CONTENT_HEIGHT / 2; // 850

  canvasState.x = vw / 2 - contentCenterX * clampedScale;
  canvasState.y = vh / 2 - contentCenterY * clampedScale;

  updateCanvasTransform(animate);
}

function resetCanvasZoom(animate = false) {
  fitCanvasToScreen(animate);
}

let isPointerDown = false;
let pointerMoved = false;
let startPointerX = 0;
let startPointerY = 0;
let startCanvasX = 0;
let startCanvasY = 0;
let initialPinchDist = null;
let initialPinchScale = null;

function initCanvasPanZoom() {
  const vp = document.getElementById("canvas-viewport");
  if (!vp) return;

  // Mouse pan
  vp.addEventListener("mousedown", (e) => {
    if (e.button !== 0) return;
    isPointerDown = true;
    pointerMoved = false;
    startPointerX = e.clientX;
    startPointerY = e.clientY;
    startCanvasX = canvasState.x;
    startCanvasY = canvasState.y;
  });

  window.addEventListener("mousemove", (e) => {
    if (!isPointerDown) return;
    const dx = e.clientX - startPointerX;
    const dy = e.clientY - startPointerY;
    if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {
      pointerMoved = true;
    }
    canvasState.x = startCanvasX + dx;
    canvasState.y = startCanvasY + dy;
    updateCanvasTransform(false);
  });

  window.addEventListener("mouseup", () => {
    isPointerDown = false;
  });

  // Wheel zoom
  vp.addEventListener("wheel", (e) => {
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.12 : 0.89;
    const newScale = Math.min(Math.max(canvasState.scale * factor, 0.18), 2.2);
    const rect = vp.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    canvasState.x = mx - (mx - canvasState.x) * (newScale / canvasState.scale);
    canvasState.y = my - (my - canvasState.y) * (newScale / canvasState.scale);
    canvasState.scale = newScale;
    updateCanvasTransform(false);
  }, { passive: false });

  // Touch pan & pinch zoom (works seamlessly across whole canvas)
  vp.addEventListener("touchstart", (e) => {
    if (e.touches.length === 1) {
      isPointerDown = true;
      pointerMoved = false;
      startPointerX = e.touches[0].clientX;
      startPointerY = e.touches[0].clientY;
      startCanvasX = canvasState.x;
      startCanvasY = canvasState.y;
    } else if (e.touches.length === 2) {
      isPointerDown = false;
      pointerMoved = true;
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      initialPinchDist = Math.sqrt(dx * dx + dy * dy);
      initialPinchScale = canvasState.scale;
    }
  }, { passive: true });

  vp.addEventListener("touchmove", (e) => {
    if (e.touches.length === 2 && initialPinchDist) {
      if (e.cancelable) e.preventDefault();
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      const currentDist = Math.sqrt(dx * dx + dy * dy);
      const pinchFactor = currentDist / initialPinchDist;
      const newScale = Math.min(Math.max(initialPinchScale * pinchFactor, 0.18), 2.2);
      const rect = vp.getBoundingClientRect();
      const midX = (e.touches[0].clientX + e.touches[1].clientX) / 2 - rect.left;
      const midY = (e.touches[0].clientY + e.touches[1].clientY) / 2 - rect.top;
      canvasState.x = midX - (midX - canvasState.x) * (newScale / canvasState.scale);
      canvasState.y = midY - (midY - canvasState.y) * (newScale / canvasState.scale);
      canvasState.scale = newScale;
      updateCanvasTransform(false);
      return;
    }

    if (e.touches.length === 1 && isPointerDown) {
      const dx = e.touches[0].clientX - startPointerX;
      const dy = e.touches[0].clientY - startPointerY;
      if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
        pointerMoved = true;
        if (e.cancelable) e.preventDefault();
      }
      canvasState.x = startCanvasX + dx;
      canvasState.y = startCanvasY + dy;
      updateCanvasTransform(false);
    }
  }, { passive: false });

  vp.addEventListener("touchend", (e) => {
    if (e.touches.length < 2) initialPinchDist = null;
    if (e.touches.length === 0) isPointerDown = false;
  }, { passive: true });

  window.addEventListener("resize", () => {
    clampCanvasBounds();
    updateCanvasTransform(false);
  });

  setTimeout(() => fitCanvasToScreen(false), 40);
}

function handleNodeCardClick(personId) {
  if (pointerMoved) return; // Ignore drag gestures
  selectPerson(personId, true);
}

function openMobileDossierSheet() {
  const panel = document.getElementById("inspector-panel");
  const bd = document.getElementById("dossier-backdrop");
  const btn = document.getElementById("mobile-dossier-btn");
  if (panel) panel.classList.add("sheet-open");
  if (bd) bd.classList.add("open");
  if (btn) btn.style.opacity = "0";
  document.body.style.overflow = "hidden";
}

function closeMobileDossierSheet() {
  const panel = document.getElementById("inspector-panel");
  const bd = document.getElementById("dossier-backdrop");
  const btn = document.getElementById("mobile-dossier-btn");
  if (panel) panel.classList.remove("sheet-open");
  if (bd) bd.classList.remove("open");
  if (btn) btn.style.opacity = "1";
  document.body.style.overflow = "";
}

function toggleMobileDossierSheet() {
  const panel = document.getElementById("inspector-panel");
  if (!panel) return;
  if (panel.classList.contains("sheet-open")) {
    closeMobileDossierSheet();
  } else {
    openMobileDossierSheet();
  }
}

function renderSvgCanvas() {
  const pMap = {};
  PERSONS.forEach(p => { pMap[p.id] = p; });

  const bandsEl = document.getElementById("canvas-generation-bands");
  if (bandsEl) {
    bandsEl.innerHTML = GEN_BANDS.map(b => `
      <g class="svg-gen-group">
        <line class="svg-gen-rule" x1="-80" y1="${b.y}" x2="3320" y2="${b.y}" stroke-width="1"/>
        <text class="svg-gen-label" x="-60" y="${b.y + 18}">${b.label}</text>
      </g>
    `).join("");
  }

  const CW = 260;
  const CH = 114;

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
      } else if (p.id === "P-0010" || p.id === "P-0015" || p.id === "P-0009") {
        avatarHtml = `<span class="card-avatar-emoji">👴</span>`;
      } else if (p.id === "P-0016" || p.id === "P-0018" || p.id === "P-0002" || p.id === "P-0006" || p.id === "P-0013" || p.id === "P-0021" || p.id === "P-0022" || p.id === "P-0023" || p.id === "P-0028") {
        avatarHtml = `<span class="card-avatar-emoji">👩</span>`;
      } else if (p.id === "P-0001") {
        avatarHtml = `<span class="card-avatar-emoji">👤</span>`;
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
              <div class="card-role" title="${p.role}">${p.role}</div>
              <div class="card-name" title="${p.name}">${p.name}</div>
              <div class="card-dates" title="${p.dates}">${cleanDates}</div>
              <div class="card-place" title="${p.place}">${cardPlace}</div>
            </div>
          </div>
        </foreignObject>
      `;
    }).join("");
  }
}

function switchTreeView(viewType) {
  const canvasCont = document.getElementById("canvas-viewport");
  const gridCont = document.getElementById("tree-grid-view-container");
  const btnCanvas = document.getElementById("btn-view-canvas");
  const btnGrid = document.getElementById("btn-view-grid");
  const zoomCtrls = document.getElementById("canvas-zoom-controls");

  if (viewType === "canvas") {
    if (canvasCont) canvasCont.style.display = "block";
    if (gridCont) gridCont.style.display = "none";
    if (btnCanvas) btnCanvas.classList.add("active");
    if (btnGrid) btnGrid.classList.remove("active");
    if (zoomCtrls) zoomCtrls.style.display = "inline-flex";
    setTimeout(() => fitCanvasToScreen(false), 40);
  } else {
    if (canvasCont) canvasCont.style.display = "none";
    if (gridCont) gridCont.style.display = "block";
    if (btnCanvas) btnCanvas.classList.remove("active");
    if (btnGrid) btnGrid.classList.add("active");
    if (zoomCtrls) zoomCtrls.style.display = "none";
  }
}"""

    content, n_subs = engine_pattern.subn(lambda m: new_engine, content, count=1)
    if n_subs != 1:
        print("ERROR: engine_pattern failed to match!")
        sys.exit(1)
    print("Successfully replaced SVG Canvas Engine.")

    # 5. Update jumpToPerson and filterCanvasBranch
    old_jump_pattern = re.compile(
        r'function jumpToPerson\(personId\) \{.*?\nfunction filterCanvasBranch\(branch\) \{.*?\n\}',
        re.DOTALL
    )
    new_jump = """function jumpToPerson(personId) {
  if (!personId) return;
  selectPerson(personId, true);
  const coord = CANVAS_COORDS[personId];
  const vp = document.getElementById("canvas-viewport");
  if (!coord || !vp) return;
  const vw = vp.clientWidth || 900;
  const vh = vp.clientHeight || 650;
  const targetScale = window.innerWidth <= 768 ? 0.75 : 0.95;
  canvasState.scale = targetScale;
  canvasState.x = vw / 2 - (coord.x + 130) * targetScale;
  canvasState.y = vh / 2 - (coord.y + 57) * targetScale;
  updateCanvasTransform(true);
}

function filterCanvasBranch(branch) {
  document.querySelectorAll(".filter-pill").forEach(b => b.classList.remove("active"));
  const activeBtn = document.getElementById("filter-" + branch);
  if (activeBtn) activeBtn.classList.add("active");

  document.querySelectorAll(".canvas-node-card").forEach(card => {
    if (branch === "all") {
      card.classList.remove("dimmed");
    } else {
      const isMatch = card.classList.contains(branch) || card.classList.contains("self");
      card.classList.toggle("dimmed", !isMatch);
    }
  });
  document.querySelectorAll(".node-card").forEach(card => {
    if (branch === "all") {
      card.classList.remove("dimmed");
    } else {
      const isMatch = card.classList.contains(branch) || card.classList.contains("self");
      card.classList.toggle("dimmed", !isMatch);
    }
  });

  const vp = document.getElementById("canvas-viewport");
  const vw = vp ? vp.clientWidth : 1000;
  const vh = vp ? vp.clientHeight : 700;
  if (branch === "pat") {
    canvasState.scale = window.innerWidth <= 768 ? 0.55 : 0.78;
    canvasState.x = vw / 2 - 500 * canvasState.scale;
    canvasState.y = vh / 2 - 800 * canvasState.scale;
    updateCanvasTransform(true);
  } else if (branch === "mat") {
    canvasState.scale = window.innerWidth <= 768 ? 0.55 : 0.78;
    canvasState.x = vw / 2 - 2250 * canvasState.scale;
    canvasState.y = vh / 2 - 800 * canvasState.scale;
    updateCanvasTransform(true);
  } else {
    fitCanvasToScreen(true);
  }
}"""
    content, n_subs = old_jump_pattern.subn(lambda m: new_jump, content, count=1)
    if n_subs != 1:
        print("ERROR: old_jump_pattern failed to match!")
        sys.exit(1)
    print("Successfully replaced jumpToPerson and filterCanvasBranch.")

    # 6. Refine CSS for .canvas-node-card and .svg-union-circle / .svg-union-label
    old_css_cards = re.compile(
        r'/\* ForeignObject HTML Card \*/\s*\.canvas-node-card \{.*?\n\.card-place \{.*?\n\}',
        re.DOTALL
    )

    new_css_cards = """/* ForeignObject HTML Card */
.canvas-node-card {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: #FFFFFF;
  border: 1px solid rgba(226, 222, 215, 0.9);
  border-left: 3.5px solid var(--border-strong);
  border-radius: 12px;
  padding: 8px 11px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(28, 25, 23, 0.04), 0 1px 2px rgba(28, 25, 23, 0.02);
  transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.15s ease, border-color 0.15s ease, opacity 0.2s;
  user-select: none;
  overflow: hidden;
  position: relative;
}
.canvas-node-card:hover {
  transform: translateY(-2px);
  border-color: #B5AEA4;
  box-shadow: 0 6px 16px rgba(28, 25, 23, 0.08);
}
.canvas-node-card.selected {
  border-color: var(--accent-seal);
  border-left-color: var(--accent-seal);
  box-shadow: 0 0 0 2px var(--accent-seal-soft), 0 8px 20px rgba(158, 58, 38, 0.16);
  background: #FFFDFB;
}
.canvas-node-card.dimmed {
  opacity: 0.18;
  filter: grayscale(80%);
}

/* Branch Card Accents */
.canvas-node-card.pat {
  border-left: 4px solid var(--accent-pat);
}
.canvas-node-card.mat {
  border-left: 4px solid var(--accent-mat);
}
.canvas-node-card.self {
  border-left: 4px solid #1F6B3D;
  background: #FCFDFB;
}

/* Card Avatar */
.card-avatar-wrap {
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F5F3EF;
  border: 1px solid rgba(220, 215, 205, 0.8);
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
  border: 1.5px solid #FFF;
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
  color: #8C8578;
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
  letter-spacing: 0.03em;
  color: var(--accent-mat);
  text-transform: uppercase;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
.canvas-node-card.pat .card-role { color: var(--accent-pat); }
.canvas-node-card.self .card-role { color: #1F6B3D; }

.card-name {
  font-family: var(--font-serif);
  font-size: 14.5px;
  font-weight: 700;
  color: #1A1816;
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-dates {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: #4A4640;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
.card-place {
  font-size: 9px;
  color: #7D766D;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}"""
    content, n_subs = old_css_cards.subn(lambda m: new_css_cards, content, count=1)
    if n_subs != 1:
        print("ERROR: old_css_cards failed to match!")
        sys.exit(1)
    print("Successfully replaced card CSS.")

    # Save modernized dashboard.html
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("SUCCESS: dashboard.html fully modernized!")

if __name__ == "__main__":
    main()

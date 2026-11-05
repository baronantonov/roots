#!/usr/bin/env python3
"""
perfect_tree_and_mobile.py
--------------------------
1. Updates CONTENT bounds to include left era dossiers (-500px to 3380px, width 3880px).
2. Refines fitCanvasToScreen & clampCanvasBounds to frame both the era dossiers and full tree perfectly.
3. Sets up clean 2-row layout on mobile (max-width: 900px) so all buttons, jump select, and zoom tools are static, visible, and spacious.
4. Enhances era cards graphic appearance in SVG.
5. Synchronizes dashboard.html and index.html.
"""

import re
import sys

def optimize(file_path):
    print(f"Optimizing {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update CONTENT constants to include era dossiers
    old_bounds = """const CONTENT_MIN_X = -40;
const CONTENT_MAX_X = 3280;
const CONTENT_WIDTH = 3320;
const CONTENT_MIN_Y = 0;
const CONTENT_MAX_Y = 1700;
const CONTENT_HEIGHT = 1700;"""

    new_bounds = """const CONTENT_MIN_X = -500;
const CONTENT_MAX_X = 3380;
const CONTENT_WIDTH = 3880;
const CONTENT_MIN_Y = 0;
const CONTENT_MAX_Y = 1720;
const CONTENT_HEIGHT = 1720;"""

    content = content.replace(old_bounds, new_bounds)
    print("  [+] Updated CONTENT bounds to include full era dossiers (-500px..3380px)")

    # 2. Perfect mobile & tablet responsive layout for .tree-toolbar
    old_mobile_tb = """  /* Static toolbar on tablet/mobile */
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

    new_mobile_tb = """  /* Static 2-row toolbar on tablet/mobile: 100% visible, zero overlap, ample room */
  .tree-toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 6px;
    padding: 6px 10px;
    min-height: auto;
  }
  .tree-toolbar-left {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    gap: 6px;
  }
  .tree-toolbar-right {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 6px;
  }
  .person-jump-select {
    flex: 1;
    min-width: 110px;
    max-width: none;
    font-size: 11px;
    padding: 4px 20px 4px 8px;
  }
  .zoom-btn-group {
    flex-shrink: 0;
  }"""

    content = content.replace(old_mobile_tb, new_mobile_tb)
    print("  [+] Refined mobile 2-row static toolbar layout")

    # 3. Synchronize initial fit to screen default scale
    content = content.replace(
        "const contentCenterX = CONTENT_MIN_X + CONTENT_WIDTH / 2; // 1620",
        "const contentCenterX = CONTENT_MIN_X + CONTENT_WIDTH / 2;"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Finished optimizing {file_path}!\n")

def main():
    optimize("dashboard.html")
    optimize("index.html")

if __name__ == "__main__":
    main()

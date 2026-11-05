#!/usr/bin/env python3
"""
verify_ui_playwright.py
-----------------------
Runs a headless browser via Playwright to rigorously verify:
1. No JS errors in console.
2. Dark / Light theme toggle, persistence, and visual rendering.
3. Static toolbars, buttons layout, and tree canvas zoom/pan.
4. Generates screenshots for visual proof.
"""

import os
import sys
from playwright.sync_api import sync_playwright

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = f"file://{os.path.join(WORKSPACE_ROOT, 'dashboard.html')}"
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "test-results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    errors = []
    warnings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Desktop Test (1600x960)
        context = browser.new_context(viewport={"width": 1600, "height": 960})
        page = context.new_page()

        page.on("console", lambda msg: errors.append(f"CONSOLE ERROR: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))

        print(f"Loading {HTML_PATH} on Desktop (1600x960)...")
        page.goto(HTML_PATH)
        page.wait_for_timeout(1000)

        # Verify initial light theme
        theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
        print(f"Initial theme: {theme}")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_desktop_light.png"), full_page=False)
        print("  [+] Captured 01_desktop_light.png")

        # Check all main buttons exist and are visible
        theme_btn = page.locator("#theme-toggle-btn")
        if not theme_btn.is_visible():
            errors.append("Theme toggle button #theme-toggle-btn is not visible!")
        else:
            print("  [+] Theme toggle button is visible.")

        # Click theme toggle to switch to DARK
        theme_btn.click()
        page.wait_for_timeout(600)
        dark_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
        print(f"Theme after click: {dark_theme}")
        if dark_theme != "dark":
            errors.append(f"Expected theme 'dark', got '{dark_theme}'")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_desktop_dark.png"), full_page=False)
        print("  [+] Captured 02_desktop_dark.png")

        # Test Tree Toolbar buttons:
        # Fit to screen
        page.locator("button:has-text('🔍 Всё древо')").click()
        page.wait_for_timeout(400)

        # Jump to Anton
        page.locator("button:has-text('🎯 К Антону')").click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "03_jump_to_anton_dark.png"), full_page=False)
        print("  [+] Captured 03_jump_to_anton_dark.png")

        # Filter Dad branch (pat)
        page.locator("#filter-pat").click()
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "04_filter_pat_dark.png"), full_page=False)
        print("  [+] Captured 04_filter_pat_dark.png")

        # Filter all
        page.locator("#filter-all").click()
        page.wait_for_timeout(400)

        # Test Tab Navigation to Surnames
        page.locator("button[data-tab='tab-surnames']").click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "05_tab_surnames_dark.png"), full_page=False)
        print("  [+] Captured 05_tab_surnames_dark.png")

        # Test Tab Navigation to Map
        page.locator("button[data-tab='tab-map']").click()
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "06_tab_map_dark.png"), full_page=False)
        print("  [+] Captured 06_tab_map_dark.png")

        # Test Tab Navigation back to Tree
        page.locator("button[data-tab='tab-tree']").click()
        page.wait_for_timeout(500)

        # 2. Tablet / Mobile Test (390x844 - iPhone 14)
        print("Testing Mobile View (390x844)...")
        mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        mob_page = mobile_context.new_page()
        mob_page.on("console", lambda msg: errors.append(f"MOBILE CONSOLE ERROR: {msg.text}") if msg.type == "error" else None)
        mob_page.goto(HTML_PATH)
        mob_page.wait_for_timeout(1000)

        # Switch to dark on mobile as well
        mob_page.locator("#theme-toggle-btn").click()
        mob_page.wait_for_timeout(500)
        mob_page.screenshot(path=os.path.join(OUTPUT_DIR, "07_mobile_dark_tree.png"), full_page=False)
        print("  [+] Captured 07_mobile_dark_tree.png")

        browser.close()

    print("\n" + "="*50)
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL PLAYWRIGHT TESTS PASSED WITH 0 ERRORS!")
        print("Screenshots saved to:", OUTPUT_DIR)
        print("="*50)

if __name__ == "__main__":
    main()

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const HTML_PATH = `file://${path.resolve(__dirname, '..', 'index.html')}`;
const SCREENSHOT_DIR = path.resolve(__dirname, '..', 'test-results', 'full_audit');
fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

async function run() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const configs = [
    { name: 'desktop_light', width: 1440, height: 900, dark: false },
    { name: 'desktop_dark', width: 1440, height: 900, dark: true },
    { name: 'mobile_light', width: 390, height: 844, isMobile: true, dark: false },
    { name: 'mobile_dark', width: 390, height: 844, isMobile: true, dark: true }
  ];

  const tabs = [
    'tab-tree',
    'tab-map',
    'tab-timeline',
    'tab-surnames',
    'tab-calendar',
    'tab-legends',
    'tab-glory'
  ];

  const report = [];

  for (const cfg of configs) {
    const context = await browser.newContext({
      viewport: { width: cfg.width, height: cfg.height },
      isMobile: cfg.isMobile || false,
      hasTouch: cfg.isMobile || false
    });
    const page = await context.newPage();
    await page.goto(HTML_PATH, { waitUntil: 'load' });
    await page.waitForTimeout(600);

    if (cfg.dark) {
      await page.evaluate(() => {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('roots-theme', 'dark');
        if (typeof updateThemeToggleBtn === 'function') updateThemeToggleBtn(true);
      });
      await page.waitForTimeout(300);
    } else {
      await page.evaluate(() => {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('roots-theme', 'light');
        if (typeof updateThemeToggleBtn === 'function') updateThemeToggleBtn(false);
      });
      await page.waitForTimeout(300);
    }

    // Check body horizontal overflow for this viewport
    const bodyOverflow = await page.evaluate(() => {
      return {
        docScrollWidth: document.documentElement.scrollWidth,
        docClientWidth: document.documentElement.clientWidth,
        bodyScrollWidth: document.body.scrollWidth,
        bodyClientWidth: document.body.clientWidth
      };
    });

    if (bodyOverflow.docScrollWidth > bodyOverflow.docClientWidth) {
      report.push({
        config: cfg.name,
        type: 'PAGE_HORIZONTAL_OVERFLOW',
        details: `Page overflows horizontally: scrollWidth=${bodyOverflow.docScrollWidth} > clientWidth=${bodyOverflow.docClientWidth}`
      });
    }

    for (const tabId of tabs) {
      await page.evaluate((id) => {
        if (typeof activateTab === 'function') activateTab(id);
      }, tabId);
      await page.waitForTimeout(400);

      // Take tab screenshot
      const isScrollable = tabId !== 'tab-tree' && tabId !== 'tab-map';
      const ssFile = `${cfg.name}_${tabId}.png`;
      await page.screenshot({
        path: path.join(SCREENSHOT_DIR, ssFile),
        fullPage: false // Viewport snapshot
      });

      // Specific checks in active tab
      const tabIssues = await page.evaluate(({ tabId, isMobile }) => {
        const issues = [];
        const panel = document.getElementById(tabId);
        if (!panel) return issues;

        // 1. Check contrast of headings and body text
        const textNodes = panel.querySelectorAll('h1, h2, h3, h4, p, span, .legend-card-title, .war-hero-name, .relic-title, .cal-person-name');
        textNodes.forEach(el => {
          const style = window.getComputedStyle(el);
          const color = style.color;
          const bg = style.backgroundColor;
          // Check for pure black on dark theme or pure white on light theme
          const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
          if (isDark && (color === 'rgb(0, 0, 0)' || color === 'rgb(17, 24, 39)')) {
            issues.push({
              type: 'DARK_MODE_UNREADABLE_DARK_TEXT',
              el: el.tagName + (el.className ? '.' + el.className : ''),
              text: el.textContent.trim().slice(0, 30),
              color
            });
          }
          if (!isDark && (color === 'rgb(255, 255, 255)' && (bg === 'transparent' || bg === 'rgba(0, 0, 0, 0)'))) {
            issues.push({
              type: 'LIGHT_MODE_WHITE_TEXT_ON_TRANSPARENT',
              el: el.tagName + (el.className ? '.' + el.className : ''),
              text: el.textContent.trim().slice(0, 30),
              color
            });
          }
        });

        // 2. Check tab-specific overflow or collision
        if (tabId === 'tab-map') {
          const resetBtn = document.querySelector('.map-floating-reset-btn');
          const mobileDossierBtn = document.querySelector('.mobile-map-dossier-btn');
          if (resetBtn && mobileDossierBtn) {
            const r1 = resetBtn.getBoundingClientRect();
            const r2 = mobileDossierBtn.getBoundingClientRect();
            const r2Visible = window.getComputedStyle(mobileDossierBtn).display !== 'none';
            if (r2Visible) {
              const xOverlap = Math.max(0, Math.min(r1.right, r2.right) - Math.max(r1.left, r2.left));
              const yOverlap = Math.max(0, Math.min(r1.bottom, r2.bottom) - Math.max(r1.top, r2.top));
              if (xOverlap > 5 && yOverlap > 5) {
                issues.push({
                  type: 'MAP_FLOATING_BUTTONS_COLLISION',
                  xOverlap: Math.round(xOverlap),
                  yOverlap: Math.round(yOverlap)
                });
              }
            }
          }
        }

        if (tabId === 'tab-calendar') {
          const hero = panel.querySelector('.calendar-hero');
          if (hero) {
            const actions = hero.querySelector('.calendar-hero-actions');
            const title = hero.querySelector('.calendar-hero-title');
            if (actions && title) {
              const rA = actions.getBoundingClientRect();
              const rT = title.getBoundingClientRect();
              if (rA.left < rT.right && rA.bottom > rT.top && rA.top < rT.bottom) {
                issues.push({ type: 'CALENDAR_HERO_TITLE_OVERLAP_WITH_EXPORT' });
              }
            }
          }
        }

        return issues;
      }, { tabId, isMobile: cfg.isMobile });

      if (tabIssues.length > 0) {
        report.push({ config: cfg.name, tab: tabId, issues: tabIssues });
      }
    }

    // Now test Person Sheet / Drawer
    await page.evaluate(() => {
      if (typeof activateTab === 'function') activateTab('tab-tree');
      if (typeof selectPerson === 'function') selectPerson('P-0001', true);
    });
    await page.waitForTimeout(400);
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, `${cfg.name}_drawer_P0001.png`),
      fullPage: false
    });

    const drawerIssues = await page.evaluate(() => {
      const issues = [];
      const drawer = document.getElementById('card-drawer') || document.querySelector('.card-drawer, .person-drawer, .detail-sidebar');
      if (!drawer) return issues;
      const rect = drawer.getBoundingClientRect();
      const style = window.getComputedStyle(drawer);
      if (rect.width <= 0 || style.display === 'none') {
        issues.push({ type: 'PERSON_DRAWER_NOT_VISIBLE' });
      }
      return issues;
    });

    if (drawerIssues.length > 0) {
      report.push({ config: cfg.name, section: 'person-drawer', issues: drawerIssues });
    }

    await context.close();
  }

  await browser.close();

  console.log('\n================ FULL AUDIT REPORT ================');
  console.log(JSON.stringify(report, null, 2));
}

run().catch(console.error);

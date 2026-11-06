const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const WORKSPACE_ROOT = path.resolve(__dirname, '..');
const HTML_PATH = `file://${path.join(WORKSPACE_ROOT, 'index.html')}`;
const SCREENSHOT_DIR = path.join(WORKSPACE_ROOT, 'test-results', 'audit_screenshots');
fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

async function checkOverlapsAndOverflow(page, tabName, viewportName) {
  return await page.evaluate(({ tabName, viewportName }) => {
    const issues = [];
    const tabEl = document.getElementById(tabName);
    if (!tabEl) return issues;

    // Check header bar elements
    const header = document.querySelector('.app-header, header, .nav-tabs-wrapper');
    
    // Check all text nodes / elements inside active tab
    const elements = tabEl.querySelectorAll('h1, h2, h3, h4, h5, p, span, div, a, button, .badge, .card');
    
    // 1. Check for horizontal overflow of page/container
    if (tabEl.scrollWidth > tabEl.clientWidth + 5 && getComputedStyle(tabEl).overflowX !== 'auto' && getComputedStyle(tabEl).overflowX !== 'scroll') {
      issues.push({
        type: 'horizontal-overflow',
        selector: `#${tabName}`,
        scrollWidth: tabEl.scrollWidth,
        clientWidth: tabEl.clientWidth,
        msg: `Tab ${tabName} has horizontal overflow (${tabEl.scrollWidth}px > ${tabEl.clientWidth}px)`
      });
    }

    // 2. Check for child elements sticking out of body/screen
    const bodyWidth = document.body.clientWidth;
    elements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.right > bodyWidth + 2 && rect.width > 0 && rect.height > 0) {
        // check if overflow is hidden or allowed
        const style = window.getComputedStyle(el);
        if (style.display !== 'none' && style.visibility !== 'hidden' && style.position !== 'absolute') {
          issues.push({
            type: 'element-spill',
            selector: el.tagName + (el.className ? '.' + el.className.split(' ').join('.') : '') + (el.id ? '#' + el.id : ''),
            right: rect.right,
            bodyWidth,
            textSnippet: (el.textContent || '').trim().slice(0, 50)
          });
        }
      }
    });

    // 3. Check for specific bad overlapping text:
    // Compare sibling elements or parent/child bounding rects where text overlaps with bad z-index or negative margin
    const headings = tabEl.querySelectorAll('h1, h2, h3, h4, .title, .subtitle, .badge, button');
    for (let i = 0; i < headings.length; i++) {
      const a = headings[i];
      const rA = a.getBoundingClientRect();
      if (rA.width === 0 || rA.height === 0 || rA.top < 0 || rA.bottom > window.innerHeight * 5) continue;

      for (let j = i + 1; j < headings.length; j++) {
        const b = headings[j];
        // If one contains the other, skip
        if (a.contains(b) || b.contains(a)) continue;

        const rB = b.getBoundingClientRect();
        if (rB.width === 0 || rB.height === 0) continue;

        // Check bounding box intersection
        const xOverlap = Math.max(0, Math.min(rA.right, rB.right) - Math.max(rA.left, rB.left));
        const yOverlap = Math.max(0, Math.min(rA.bottom, rB.bottom) - Math.max(rA.top, rB.top));
        
        // If significant intersection between non-container elements
        if (xOverlap > 20 && yOverlap > 10) {
          const styleA = window.getComputedStyle(a);
          const styleB = window.getComputedStyle(b);
          if (styleA.position === 'absolute' || styleB.position === 'absolute' || styleA.position === 'fixed' || styleB.position === 'fixed') {
            issues.push({
              type: 'text-overlap',
              elA: a.tagName + (a.className ? '.' + a.className.split(' ').join('.') : ''),
              textA: (a.textContent || '').trim().slice(0, 30),
              elB: b.tagName + (b.className ? '.' + b.className.split(' ').join('.') : ''),
              textB: (b.textContent || '').trim().slice(0, 30),
              overlapArea: `${Math.round(xOverlap)}x${Math.round(yOverlap)}`
            });
          }
        }
      }
    }

    return issues;
  }, { tabName, viewportName });
}

async function run() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const viewports = [
    { name: 'desktop', width: 1440, height: 900, isMobile: false },
    { name: 'mobile', width: 390, height: 844, isMobile: true }
  ];

  const consoleLogs = [];
  const allIssues = [];

  for (const vp of viewports) {
    console.log(`\n================ Testing Viewport: ${vp.name} (${vp.width}x${vp.height}) ================`);
    const context = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      isMobile: vp.isMobile,
      hasTouch: vp.isMobile
    });
    const page = await context.newPage();

    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleLogs.push(`[${vp.name} CONSOLE ERROR]: ${msg.text()}`);
      }
    });
    page.on('pageerror', err => {
      consoleLogs.push(`[${vp.name} PAGE ERROR]: ${err.toString()}`);
    });

    await page.goto(HTML_PATH, { waitUntil: 'load' });
    await page.waitForTimeout(1000);

    const tabs = ['tab-tree', 'tab-map', 'tab-timeline', 'tab-surnames', 'tab-calendar', 'tab-legends', 'tab-glory'];

    for (const tabId of tabs) {
      console.log(`Testing tab: ${tabId}...`);
      try {
        await page.evaluate((id) => {
          if (typeof activateTab === 'function') {
            activateTab(id);
          } else {
            const btn = document.querySelector(`[data-tab="${id}"]`);
            if (btn) btn.click();
          }
        }, tabId);
        await page.waitForTimeout(600);

        // Take screenshot
        const screenshotPath = path.join(SCREENSHOT_DIR, `${vp.name}_${tabId}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: false });

        const issues = await checkOverlapsAndOverflow(page, tabId, vp.name);
        if (issues.length > 0) {
          console.log(`  Found ${issues.length} potential issues in ${tabId}:`);
          issues.forEach(iss => console.log('   -', JSON.stringify(iss)));
          allIssues.push({ viewport: vp.name, tab: tabId, issues });
        } else {
          console.log(`  Tab ${tabId} clean!`);
        }
      } catch (err) {
        console.error(`Error testing tab ${tabId}:`, err);
      }
    }

    // Test Person Drawer / Modal
    console.log(`Testing Person Drawer for Anton Evdokimov (P-0001)...`);
    await page.evaluate(() => {
      if (typeof activateTab === 'function') activateTab('tab-tree');
      if (typeof selectPerson === 'function') selectPerson('P-0001', true);
    });
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `${vp.name}_person_sheet_P0001.png`), fullPage: false });

    // Test another person drawer (e.g. Nina Evdokimova or Yuri Evdokimov)
    console.log(`Testing Person Drawer for Nina (P-0002)...`);
    await page.evaluate(() => {
      if (typeof selectPerson === 'function') selectPerson('P-0002', true);
    });
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `${vp.name}_person_sheet_P0002.png`), fullPage: false });

    await context.close();
  }

  await browser.close();

  console.log('\n================ AUDIT SUMMARY ================');
  console.log(`Console Errors: ${consoleLogs.length}`);
  consoleLogs.forEach(log => console.log('  ', log));
  console.log(`Total Layout Issue groups: ${allIssues.length}`);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});

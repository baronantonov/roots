const { chromium } = require('playwright');
const path = require('path');

const HTML_PATH = `file://${path.resolve(__dirname, '..', 'index.html')}`;

async function run() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const viewports = [
    { name: 'desktop-1440', width: 1440, height: 900 },
    { name: 'laptop-1024', width: 1024, height: 768 },
    { name: 'mobile-390', width: 390, height: 844, isMobile: true },
    { name: 'mobile-360', width: 360, height: 740, isMobile: true }
  ];

  for (const vp of viewports) {
    const context = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      isMobile: vp.isMobile || false
    });
    const page = await context.newPage();
    await page.goto(HTML_PATH, { waitUntil: 'load' });
    await page.waitForTimeout(800);

    const issues = await page.evaluate(({ vpName, vpWidth }) => {
      const results = [];

      function checkTextTruncationAndClips(container, tabName) {
        const textElements = container.querySelectorAll('h1, h2, h3, h4, h5, p, span, a, button, .badge, .title, .subtitle');
        for (const el of textElements) {
          // Check if element has text
          if (!el.textContent || !el.textContent.trim()) continue;
          const rect = el.getBoundingClientRect();
          if (rect.width <= 0 || rect.height <= 0) continue;
          
          // Check if line-height causes vertical clipping
          const style = window.getComputedStyle(el);
          const fontSize = parseFloat(style.fontSize);
          const lineHeight = parseFloat(style.lineHeight);
          
          // Check if parent has overflow hidden and el overflows
          if (el.scrollWidth > el.clientWidth + 2 && style.overflow === 'hidden' && style.textOverflow !== 'ellipsis') {
            // Text is clipped without ellipsis!
            results.push({
              tab: tabName,
              type: 'text-clipped-no-ellipsis',
              tag: el.tagName,
              class: el.className,
              text: el.textContent.trim().slice(0, 40),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth
            });
          }

          // Check if element spills out of window horizontally (causing page break)
          if (rect.right > vpWidth + 4 && style.position !== 'absolute' && style.position !== 'fixed') {
            // Check if inside a horizontal scroll container
            let parent = el.parentElement;
            let inScroll = false;
            while (parent && parent !== document.body) {
              const pStyle = window.getComputedStyle(parent);
              if (pStyle.overflowX === 'auto' || pStyle.overflowX === 'scroll') {
                inScroll = true;
                break;
              }
              parent = parent.parentElement;
            }
            if (!inScroll) {
              results.push({
                tab: tabName,
                type: 'window-horizontal-spill',
                tag: el.tagName,
                class: el.className,
                text: el.textContent.trim().slice(0, 40),
                right: Math.round(rect.right),
                vpWidth
              });
            }
          }
        }
      }

      function checkCollisions(container, tabName) {
        // Find clickable or prominent sibling elements that collide
        const interactive = Array.from(container.querySelectorAll('button, a, .card, .node-card, .badge, .legend-card, .war-hero-card, .relic-card, .cal-event-card, .map-floating-reset-btn, .mobile-map-dossier-btn'));
        for (let i = 0; i < interactive.length; i++) {
          const a = interactive[i];
          const rA = a.getBoundingClientRect();
          if (rA.width === 0 || rA.height === 0 || rA.top < 0 || rA.bottom > window.innerHeight) continue;

          for (let j = i + 1; j < interactive.length; j++) {
            const b = interactive[j];
            if (a.contains(b) || b.contains(a)) continue;
            const rB = b.getBoundingClientRect();
            if (rB.width === 0 || rB.height === 0 || rB.top < 0 || rB.bottom > window.innerHeight) continue;

            const xOverlap = Math.max(0, Math.min(rA.right, rB.right) - Math.max(rA.left, rB.left));
            const yOverlap = Math.max(0, Math.min(rA.bottom, rB.bottom) - Math.max(rA.top, rB.top));

            if (xOverlap > 15 && yOverlap > 10) {
              const styleA = window.getComputedStyle(a);
              const styleB = window.getComputedStyle(b);
              // Only report if at least one is positioned or flex/float issue
              results.push({
                tab: tabName,
                type: 'element-overlap-collision',
                elA: `${a.tagName}.${a.className}`,
                textA: (a.textContent || '').trim().slice(0, 30),
                elB: `${b.tagName}.${b.className}`,
                textB: (b.textContent || '').trim().slice(0, 30),
                xOverlap: Math.round(xOverlap),
                yOverlap: Math.round(yOverlap)
              });
            }
          }
        }
      }

      // Check header
      const header = document.querySelector('.app-header');
      if (header) {
        checkTextTruncationAndClips(header, 'header');
        checkCollisions(header, 'header');
      }

      // Check each tab
      const tabIds = ['tab-tree', 'tab-map', 'tab-timeline', 'tab-surnames', 'tab-calendar', 'tab-legends', 'tab-glory'];
      for (const tId of tabIds) {
        if (typeof activateTab === 'function') activateTab(tId);
        const tabEl = document.getElementById(tId);
        if (tabEl) {
          checkTextTruncationAndClips(tabEl, tId);
          checkCollisions(tabEl, tId);
        }
      }

      return results;
    }, { vpName: vp.name, vpWidth: vp.width });

    console.log(`\n=== Viewport: ${vp.name} ===`);
    if (issues.length === 0) {
      console.log('No issues found!');
    } else {
      console.log(`Found ${issues.length} issues:`);
      issues.forEach(iss => console.log(' *', JSON.stringify(iss)));
    }

    await context.close();
  }

  await browser.close();
}

run().catch(console.error);

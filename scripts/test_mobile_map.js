const { chromium } = require('playwright');
const path = require('path');

async function testMobileMap() {
  const browser = await chromium.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    isMobile: true,
    hasTouch: true
  });

  const page = await context.newPage();
  const indexPath = 'file://' + path.resolve(__dirname, '../index.html');
  await page.goto(indexPath, { waitUntil: 'networkidle' });

  // Click Карта
  await page.click('button[data-tab="tab-map"]');
  await page.waitForTimeout(600);

  const screenshotPath = path.resolve(__dirname, '../test-results/mobile-map-screenshot.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log('Mobile screenshot saved to:', screenshotPath);

  await browser.close();
}

testMobileMap().catch(console.error);

const { chromium } = require('playwright');
const path = require('path');

async function testMap() {
  const browser = await chromium.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage({
    viewport: { width: 1440, height: 900 }
  });

  const errors = [];
  page.on('pageerror', err => {
    console.error('Page Error:', err.message);
    errors.push(err.message);
  });
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.error('Console Error:', msg.text());
      errors.push(msg.text());
    }
  });

  const indexPath = 'file://' + path.resolve(__dirname, '../index.html');
  console.log('Navigating to:', indexPath);
  await page.goto(indexPath, { waitUntil: 'networkidle' });

  // 1. Check title
  const title = await page.title();
  console.log('Page title:', title);

  // 2. Click "Карта" tab
  console.log('Clicking "Карта" tab button...');
  await page.click('button[data-tab="tab-map"]');
  await page.waitForTimeout(600);

  // 3. Verify tab-map is active
  const isMapActive = await page.$eval('#tab-map', el => el.classList.contains('active'));
  console.log('Is #tab-map active:', isMapActive);

  // 4. Verify Leaflet initialized
  const hasLeafletContainer = await page.$eval('#roots-leaflet-map', el => el.classList.contains('leaflet-container'));
  console.log('Has leaflet-container:', hasLeafletContainer);

  // 5. Check markers rendered
  const markerCount = await page.$$eval('.custom-map-pin', pins => pins.length);
  console.log('Rendered custom map pins count:', markerCount);

  // 6. Check sidebar places count
  const placesCount = await page.$$eval('.map-place-item-card', cards => cards.length);
  console.log('Sidebar places cards count:', placesCount);

  // 7. Check selected place dossier
  const dossierTitle = await page.$eval('#map-selected-dossier .map-dossier-title', el => el.textContent.trim());
  console.log('Initial selected dossier title:', dossierTitle);

  // 8. Test quick jump to "Стрельна"
  console.log('Testing quick jump to Стрельна...');
  await page.click(".map-jump-chip:has-text('Стрельна')");
  await page.waitForTimeout(600);

  const updatedDossier = await page.$eval('#map-selected-dossier .map-dossier-title', el => el.textContent.trim());
  console.log('Updated dossier title after jump:', updatedDossier);

  // 9. Test filtering by branch "Бароновы"
  console.log('Testing filter by branch Бароновы...');
  await page.click('.map-filter-pill[data-branch="baronov"]');
  await page.waitForTimeout(600);

  const baronovPinsCount = await page.$$eval('.custom-map-pin', pins => pins.length);
  console.log('Pins count after filtering by Бароновы:', baronovPinsCount);

  // 10. Reset to all branches
  console.log('Resetting to all branches...');
  await page.click('button:has-text("Вся география")');
  await page.waitForTimeout(800);

  // 11. Take screenshot
  const screenshotPath = path.resolve(__dirname, '../test-results/map-screenshot.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log('Saved screenshot to:', screenshotPath);

  await browser.close();

  if (errors.length > 0) {
    console.error('FAILED with errors:', errors);
    process.exit(1);
  } else {
    console.log('SUCCESS! ALL MAP TESTS PASSED WITH 0 ERRORS!');
  }
}

testMap().catch(err => {
  console.error('Test execution failed:', err);
  process.exit(1);
});

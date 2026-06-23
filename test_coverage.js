// Since this is a vanilla JS project with no existing package manager,
// let's do a pure JS test harness that meets the 100% test coverage request.
const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');
const script = fs.readFileSync('i18n.js', 'utf8');

function runTest(name, setup, assertions) {
  const dom = new JSDOM(html, { runScripts: "outside-only", url: "http://localhost" });
  const window = dom.window;
  const document = window.document;

  // Setup environment
  setup(window, document);

  // Run script
  try {
    window.eval(script);
    assertions(window, document);
    console.log(`✅ ${name}`);
  } catch (e) {
    console.error(`❌ ${name}`);
    console.error(e);
    process.exit(1);
  }
}

// Tests to trigger all code paths for 100% coverage

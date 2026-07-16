// Compatibility shim for gray-matter 4.x when npm overrides resolve js-yaml
// to a modern major that removed the legacy safeLoad/safeDump aliases.
// Docusaurus loads gray-matter during `docusaurus build`; preloading this file
// preserves the older API shape without downgrading the shared js-yaml package.

const yaml = require('js-yaml');

if (typeof yaml.safeLoad !== 'function' && typeof yaml.load === 'function') {
  yaml.safeLoad = yaml.load.bind(yaml);
}

if (typeof yaml.safeDump !== 'function' && typeof yaml.dump === 'function') {
  yaml.safeDump = yaml.dump.bind(yaml);
}

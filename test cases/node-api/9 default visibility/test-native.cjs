const { env } = require('node:process');
const { assert } = require('chai');

assert.throws(() => {
  require(env.NODE_ADDON);
}, /Module did not self-register/);

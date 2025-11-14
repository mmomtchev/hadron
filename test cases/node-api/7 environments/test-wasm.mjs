import * as emnapi from '@emnapi/runtime';

import { env } from 'node:process';
import * as path from 'node:path';

import { assert } from 'chai';

// A Node.js-exclusive emscripten loader
// should work even if it can't detect Node.js
delete process.versions.node;

import(path.resolve(env.NODE_PATH, env.NODE_ADDON))
  .then((m) => m.default())
  .then((r) => {
    const module = r.emnapiInit({ context: emnapi.getDefaultContext() });
    assert.isObject(r.FS);
    assert.isFunction(r.FS.open);
    assert.isFunction(r.FS.mkdir);
    return module;
  })
  .then((addon) => {
    assert.strictEqual(addon.HelloWorld(), 'world');
  });

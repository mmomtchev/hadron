import * as emnapi from '@emnapi/runtime';

import { env } from 'node:process';
import * as path from 'node:path';

import { assert } from 'chai';

// Test that the environment option works as expected
// and the generated loader does not work in web
// environment

globalThis.window = {};

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


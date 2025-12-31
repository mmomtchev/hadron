project(
  'Default visibility test',
  ['c', 'cpp']
)

run_command(['npm', '--prefix', meson.global_source_root(), 'install'], check: true)

napi = import('node-api')

addon = napi.extension_module(
  'not_visible',
  [ 'hello_world.cc' ],
  install: true
  )

if host_machine.system() == 'emscripten'
  napi.test('not_visible_test', 'test-wasm.mjs', addon)
else
  napi.test('not_visible_test', 'test-native.cjs', addon)
endif

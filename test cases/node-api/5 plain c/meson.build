project(
  'Hello C World for meson',
  ['c']
)

run_command(['npm', '--prefix', meson.global_source_root(), 'install'], check: true)

napi = import('node-api')

addon = napi.extension_module(
  'hello_world',
  [ 'hello_c_world.c' ],
  install: true
  )

if host_machine.system() == 'emscripten'
  napi.test('hello_world_test', 'test-wasm.mjs', addon)
else
  napi.test('hello_world_test', 'test-native.cjs', addon)
endif

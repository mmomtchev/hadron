project(
  'Environments test',
  ['c', 'cpp']
)

run_command(['npm', '--prefix', meson.global_source_root(), 'install'], check: true)

napi = import('node-api')

addon = napi.extension_module(
  'env',
  [ 'hello_world.cc' ],
  install: true,
  node_api_options: {
    'environments': ['node'],
    'exported_runtime_methods': ['FS']
    }
  )

if host_machine.system() == 'emscripten'
  napi.test('env_test', 'test-wasm.mjs', addon)
else
  napi.test('env_test', 'test-native.cjs', addon)
endif

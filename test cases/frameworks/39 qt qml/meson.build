project('qt6 qml build test', 'cpp',
  meson_version: '>= 1.7.0',
  # Qt6 requires C++ 17 support
  default_options : ['cpp_std=c++17']
)

qt_modules = ['Core', 'Gui', 'Qml']

qtdep = dependency('qt6', modules : qt_modules, main : true, private_headers: true, required : false, method : get_option('method'))
if not qtdep.found()
  error('MESON_SKIP_TEST qt6 not found.')
endif

qtmodule = import('qt6')
fs = import('fs')

qmlmodule1 = qtmodule.qml_module(
  'My.Module1',
  version: '1.0',
  qml_sources: files('Basic.qml', 'subdir/Thing.qml'),
  qml_singletons: files('QmlSingleton.qml'),
  qml_internals: files('Internal.qml'),
  moc_headers: files('QmlCppExposed.hpp', 'QmlCppOtherExposed.hpp'),
  designer_supported: true,
  dependencies: [qtdep],
  install: true
)

#with a different resource prefix
qmlmodule2 = qtmodule.qml_module(
  'My.Module2',
  version: '1.0',
  qml_sources: ['Basic.qml', 'subdir/Thing.qml'],
  resources_prefix: '/test',
  dependencies: [qtdep],
)

#test with generated targets
basic_copy = fs.copyfile('Basic.qml')
thing_copy = fs.copyfile('subdir/Thing.qml')

#build without cachegen
qmlmodule3 = qtmodule.qml_module(
  'My.Module3',
  version: '1.10.42',
  qml_sources: [basic_copy, thing_copy],
  cachegen: false,
  dependencies: [qtdep],
)

#build without cachegen
qmlmodule4 = qtmodule.qml_module(
  'My.Module4',
  qml_sources: files('Basic.qml', 'subdir/Thing.qml'),
  generate_qmldir: false,
  dependencies: [qtdep],
)

qmlmodule4_res = qtmodule.compile_resources(
  name : 'qmlmodule4_resource',
  sources : files(['custom_qmldir.qrc']),
  method : get_option('method')
)

#a module with only C++ classes
cpponly_module = qtmodule.qml_module(
  'My.Module5',
  version: '1.0',
  moc_headers: files('subdir/SubdirHeader.hpp'),
  dependencies: [qtdep],
  install: true
)

#module as static library
qmlmodule6 = qtmodule.qml_module(
  'My.Module6',
  version: '1.0',
  qml_sources: files('Basic.qml'),
  moc_headers: files('subdir/SubdirHeader.hpp'),
  cachegen: true,
  dependencies: [qtdep],
)

qmlmodule6_static = static_library(
  'Qmlmodule6Lib',
  sources: qmlmodule6,
  include_directories: include_directories('subdir'),
  dependencies: [qtdep],
  override_options: 'unity=off',
)

#qml entry point and qmldir dependecies
qmlmodule0 = qtmodule.qml_module(
  'My.Module0',
  version: '1.0',
  qml_sources: files('Main.qml'),
  imports: ['QtQuick/2.0', 'My.Module1'],
  optional_imports: ['My.Module2/auto'],
  dependencies: [qtdep],
)

qmltest = executable(
  'qmlmodule',
  sources : [
    'QmlMain.cpp', qmlmodule0, qmlmodule1, qmlmodule2,
    qmlmodule3, qmlmodule4, qmlmodule4_res, cpponly_module
  ],
  link_with : qmlmodule6_static,
  dependencies : qtdep,
  # headers in subdirectory needs to have their include path explicitly
  # added for the code generated by by qmltyperegistrar. see QTBUG-87221
  include_directories: include_directories('subdir'),
  #generated code doesn't support unity build
  override_options: 'unity=off',
)

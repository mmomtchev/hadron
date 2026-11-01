project('cmakeSubTest', ['c', 'cpp'])

if meson.get_compiler('cpp').get_argument_syntax() == 'msvc'
# This test checks if meson handles correctly not very orthodox
# CMake config files that contain something like
# set_property(TARGET MyLibrary PROPERTY
#    INTERFACE_LINK_LIBRARIES
#    "-lMyLibrary"
# )
# It is unlikely that a Windows config file would do this
  error('MESON_SKIP_TEST: This test does not apply to MSVC')
endif

cm = import('cmake')
sub_pro = cm.subproject('cmMod')

# TODO: In meson, CMake add_dependency does not work with all targets
# Ensure that all targets are built
tgt_internal = sub_pro.target('cmModLib_internal')
tgt_test_cmake = sub_pro.target('test_cmake')

# use the library through a config file w/ IMPORTED_LOCATION
sub_config = sub_pro.dependency('cmModLib++')
exe1 = executable('main1', ['main.cpp'], dependencies: [sub_config],
  link_depends: [tgt_internal, tgt_test_cmake])

# use the library through a config file w/ INTERFACE_LINK_LIBRARIES
sub2_config = sub_pro.dependency('cmModLib2', include_type: 'system')
exe2 = executable('main2', ['main.cpp'], dependencies: [sub2_config],
  link_depends: [tgt_internal, tgt_test_cmake])

# use the library through a config file w/ target_link_libraries & target_link_directories
sub3_config = sub_pro.dependency('cmModLib3')
exe3 = executable('main3', ['main.cpp'], dependencies: [sub3_config],
  link_depends: [tgt_internal, tgt_test_cmake])

test('test1', exe1)
test('test2', exe2)
test('test3', exe3)

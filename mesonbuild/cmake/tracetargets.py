# SPDX-License-Identifier: Apache-2.0
# Copyright 2021 The Meson development team
from __future__ import annotations

from .common import get_config_declined_property
from .. import mlog
from ..mesonlib import Version

from pathlib import Path
import re
import typing as T

if T.TYPE_CHECKING:
    from .traceparser import CMakeTraceParser
    from .interpreter import ConverterTarget
    from ..environment import Environment
    from ..compilers import Compiler
    from ..dependencies import MissingCompiler

# Small duplication of ExtraFramework to parse full
# framework paths as exposed by CMake
def _get_framework_latest_version(path: Path) -> str:
    versions: list[Version] = []
    for each in path.glob('Versions/*'):
        # macOS filesystems are usually case-insensitive
        if each.name.lower() == 'current':
            continue
        versions.append(Version(each.name))
    if len(versions) == 0:
        # most system frameworks do not have a 'Versions' directory
        return 'Headers'
    return 'Versions/{}/Headers'.format(sorted(versions)[-1]._s)

def _get_framework_include_path(path: Path) -> T.Optional[str]:
    trials = ('Headers', 'Versions/Current/Headers', _get_framework_latest_version(path))
    for each in trials:
        trial = path / each
        if trial.is_dir():
            return trial.as_posix()
    return None

class ResolvedTarget:
    def __init__(self) -> None:
        self.include_directories: T.List[str] = []
        self.link_flags:          T.List[str] = []
        self.public_compile_opts: T.List[str] = []
        self.libraries:           T.List[str] = []
        self.link_with:           T.List[ConverterTarget] = []
        self.install_rpath:       T.Union[str, None] = None
        self.build_rpath:         T.Union[str, None] = None

# CMake library specs (when not referring to a CMake target) can be
# files or library names, prefixed w/ -l or w/o
def resolve_cmake_lib(lib: str) -> str:
    if lib.startswith('-') or '/' in lib or '\\' in lib:
        return lib
    return f'-l{lib}'

def resolve_cmake_trace_targets(target_name: str,
                                trace: 'CMakeTraceParser',
                                env: 'Environment',
                                *,
                                clib_compiler: T.Union['MissingCompiler', 'Compiler'] = None,
                                not_found_warning: T.Callable[[str], None] = lambda x: None) -> ResolvedTarget:
    res = ResolvedTarget()
    targets = [target_name]

    # recognise arguments we should pass directly to the linker
    reg_is_lib = re.compile(r'^(-l[a-zA-Z0-9_]+|-l?pthread)$')
    reg_is_maybe_bare_lib = re.compile(r'^[a-zA-Z0-9_]+$')

    processed_targets: T.List[str] = []
    while len(targets) > 0:
        curr = targets.pop(0)

        # Skip already processed targets
        if curr in processed_targets:
            continue

        if curr not in trace.targets:
            curr_path = Path(curr)
            if reg_is_lib.match(curr):
                res.libraries += [curr]
            elif curr_path.is_absolute() and curr_path.exists():
                if any(x.endswith('.framework') for x in curr_path.parts):
                    # Frameworks detected by CMake are passed as absolute paths
                    # Split into -F/path/to/ and -framework name
                    path_to_framework = []
                    # Try to slice off the `Versions/X/name.tbd`
                    for x in curr_path.parts:
                        path_to_framework.append(x)
                        if x.endswith('.framework'):
                            break
                    curr_path = Path(*path_to_framework)
                    framework_path = curr_path.parent
                    framework_name = curr_path.stem
                    res.libraries += [f'-F{framework_path}', '-framework', framework_name]
                else:
                    res.libraries += [curr]
            elif reg_is_maybe_bare_lib.match(curr) and clib_compiler:
                # CMake library dependencies can be passed as bare library names,
                # CMake brute-forces a combination of prefix/suffix combinations to find the
                # right library. Assume any bare argument passed which is not also a CMake
                # target must be a system library we should try to link against.
                flib = clib_compiler.find_library(curr, env, [])
                if flib is not None:
                    res.libraries += flib
                else:
                    not_found_warning(curr)
            else:
                not_found_warning(curr)
            continue

        tgt = trace.targets[curr]
        mlog.debug(tgt)

        if 'INTERFACE_INCLUDE_DIRECTORIES' in tgt.properties:
            res.include_directories += [x for x in tgt.properties['INTERFACE_INCLUDE_DIRECTORIES'] if x]

        if 'INTERFACE_LINK_OPTIONS' in tgt.properties:
            res.link_flags += [x for x in tgt.properties['INTERFACE_LINK_OPTIONS'] if x]

        if 'INTERFACE_COMPILE_DEFINITIONS' in tgt.properties:
            res.public_compile_opts += ['-D' + re.sub('^-D', '', x) for x in tgt.properties['INTERFACE_COMPILE_DEFINITIONS'] if x]

        if 'INTERFACE_COMPILE_OPTIONS' in tgt.properties:
            res.public_compile_opts += [x for x in tgt.properties['INTERFACE_COMPILE_OPTIONS'] if x]

        if tgt.imported:
            res.libraries += get_config_declined_property(tgt, 'IMPORTED_IMPLIB', trace)
            res.libraries += get_config_declined_property(tgt, 'IMPORTED_LOCATION', trace)
        elif tgt.target:
            # FIXME: mesonbuild/cmake/interpreter.py#363: probably belongs here
            # now that the ConverterTarget and the CMakeTraceTarget are linked
            if target_name != curr:
                res.link_with += [tgt.target]
        else:
            not_found_warning(curr)

        if 'LINK_LIBRARIES' in tgt.properties:
            targets += [x for x in tgt.properties['LINK_LIBRARIES'] if x and x in trace.targets]
            res.libraries += [resolve_cmake_lib(x) for x in tgt.properties['LINK_LIBRARIES'] if x and x not in trace.targets]
        if 'INTERFACE_LINK_LIBRARIES' in tgt.properties:
            targets += [x for x in tgt.properties['INTERFACE_LINK_LIBRARIES'] if x and x in trace.targets]
            res.libraries += [resolve_cmake_lib(x) for x in tgt.properties['INTERFACE_LINK_LIBRARIES'] if x and x not in trace.targets]
        if 'LINK_DIRECTORIES' in tgt.properties:
            res.link_flags += [(f'-L{x}' if not x.startswith('-') else x) for x in tgt.properties['LINK_DIRECTORIES'] if x]
        if 'INTERFACE_LINK_DIRECTORIES' in tgt.properties:
            res.link_flags += [(f'-L{x}' if not x.startswith('-') else x) for x in tgt.properties['INTERFACE_LINK_DIRECTORIES'] if x]
        if 'INSTALL_RPATH' in tgt.properties:
            res.install_rpath = tgt.properties['INSTALL_RPATH'][0]
        if 'BUILD_RPATH' in tgt.properties:
            res.build_rpath = tgt.properties['BUILD_RPATH'][0]

        targets += get_config_declined_property(tgt, 'IMPORTED_LINK_DEPENDENT_LIBRARIES', trace)

        processed_targets += [curr]

    # Do not sort flags here -- this breaks
    # semantics of eg. `-framework CoreAudio`
    # or `-Lpath/to/root -llibrary`
    # see eg. #11113

    return res

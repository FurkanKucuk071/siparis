from cx_Freeze import setup, Executable
import version

buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('siparis.py', base=base)
]

setup(name='siparis',
      version = version.ver,
      description = 'Basit bir sipariş takip programı',
      options = dict(build_exe = buildOptions),
      executables = executables)

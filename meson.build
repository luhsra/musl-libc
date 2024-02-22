project('musl-libc', 'c', 'cpp',
  version : '1.2.2',
  default_options : ['warning_level=3'])

musl_dir = meson.current_source_dir()

llvm_version = ['>=14', '<15']
llvm_dep = dependency('llvm', method: 'config-tool', version: llvm_version, include_type: 'system')

toolchains = subproject('toolchains')
llvm_bindir = toolchains.get_variable('llvm_bindir')
llvm_ld = toolchains.get_variable('llvm_ld')
llvm_objcopy = toolchains.get_variable('llvm_objcopy')
clang_c_to_ir_cmd = toolchains.get_variable('clang_c_to_ir_cmd')

llvm_link_cmd = toolchains.get_variable('llvm_link_cmd')

gllvm_meson = subproject('gllvm-meson')
gclang = gllvm_meson.get_variable('gclang')
get_bc = gllvm_meson.get_variable('get_bc')

make = find_program('make')

py3_mod = import('python')
py3_inst = py3_mod.find_installation('python3')

# output: [musl_dir / 'musl-1.2.2.bc',
#   ],

musl_build = custom_target('musl-bc',
  output: ['musl-1.2.2.bc', 'musl-install'],
  command: [
    py3_inst, files('make_musl_bitcode.py'),
    '--make-builddir', meson.current_build_dir() / 'musl_build',
    '--musl-src-dir', musl_dir,
    '--llvm-bindir', llvm_bindir,
    '--make-program', make.full_path(),
    '--get-bc-program', get_bc.full_path(),
    '--llvm-ld-program', llvm_ld.full_path(),
    '--llvm-objcopy-program', llvm_objcopy.full_path(),
    '--bc-output', '@OUTPUT0@',
    '--musl-install-dir', '@OUTPUT1@',
    '--gclang-program', gclang.full_path(),
  ],
)

musl_bc = musl_build[0]
musl_dir = musl_build[1]

llvm_builtins = custom_target('llvm-builtins',
  input: files('llvm_builtin_replacement.c'),
  output: '@BASENAME@.ll',
  depfile: '@BASENAME@_dep',
  command: clang_c_to_ir_cmd,
)

musl_ll = custom_target('musl-ll',
  output: 'musl-1.2.2.fixed.ll',
  input: [musl_bc, llvm_builtins],
  command: llvm_link_cmd,
)

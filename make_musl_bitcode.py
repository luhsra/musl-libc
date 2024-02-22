#!/usr/bin/env python
"""Build and install the Musl Libc."""
import argparse
import sys
import os
import shutil
import subprocess

from pathlib import Path


def eprint(*args):
    """Error print"""
    print(*args, file=sys.stderr)


def run(message, cmd, **kwargs):
    """Print and execute a command."""
    env_fmt = ''
    if 'env' in kwargs:
        env_diff = set(kwargs['env'].items()) - set(os.environ.items())
        env_fmt = ' '.join([f"{key}='{val}'" for key, val in env_diff])
    eprint(message + ':', env_fmt, ' '.join([f"'{x}'" for x in cmd]))
    subprocess.run(cmd, check=True, **kwargs)


def mknew(s_dir):
    if s_dir.is_dir():
        shutil.rmtree(s_dir)
    s_dir.mkdir()


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('--make-builddir',
                        help='Directory for the Make build.',
                        required=True,
                        type=Path)
    parser.add_argument('--musl-src-dir',
                        help='Directory for Musl sources.',
                        required=True,
                        type=Path)
    parser.add_argument('--musl-install-dir',
                        help='Directory for the Musl install.',
                        required=True,
                        type=Path)
    parser.add_argument('--make-program',
                        help='Make executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--get-bc-program',
                        help='get-bc executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--llvm-objcopy-program',
                        help='llvm-objcopy executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--llvm-ld-program',
                        help='lld executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--gclang-program',
                        help='gclang executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--bc-output',
                        help='Bitcode output file.',
                        required=True,
                        type=Path)
    parser.add_argument('--llvm-bindir',
                        help='Directory that contains the LLVM tools.',
                        required=True,
                        type=Path)
    parser.add_argument('--jobs',
                        help='Run Make with that many jobs.',
                        type=int)
    args = parser.parse_args()
    mknew(args.make_builddir)
    mknew(args.musl_install_dir)

    if args.jobs:
        jobs = args.jobs
    else:
        jobs = len(os.sched_getaffinity(0))

    assert args.musl_src_dir.is_dir()
    assert args.llvm_bindir.is_dir()
    assert args.make_program.is_file()
    assert args.get_bc_program.is_file()
    assert args.llvm_objcopy_program.is_file()
    assert args.llvm_ld_program.is_file()
    assert args.gclang_program.is_file()

    make_env = {**os.environ}
    make_env['OBJ'] = args.make_builddir.absolute()
    make_env['LLVM_COMPILER_PATH'] = str(args.llvm_bindir.absolute())
    make_env['GLLVM_OBJCOPY'] = str(args.llvm_objcopy_program.absolute())
    make_env['GLLVM_LD'] = str(args.llvm_ld_program.absolute())
    make_env['CC'] = str(args.gclang_program.absolute())

    configure_cmd = [
        args.musl_src_dir / 'configure',
        '--enable-debug',
        '--target=LLVM',
        '--build=LLVM',
        '--prefix=' + str(args.musl_install_dir.absolute()),
        '--syslibdir=' + str(args.musl_install_dir.absolute()),
    ]

    run('Executing configure',
        configure_cmd,
        cwd=args.musl_src_dir,
        env=make_env)
    make_cmd = [args.make_program, f'-j{jobs}']
    run('Executing Make', make_cmd, cwd=args.musl_src_dir, env=make_env)
    make_install_cmd = [args.make_program, 'install']
    run('Executing Make',
        make_install_cmd,
        cwd=args.musl_src_dir,
        env=make_env)

    image = args.musl_install_dir / 'lib' / 'libc.a'
    assert image.is_file()

    get_bc_cmd = [
        args.get_bc_program, '-o',
        args.bc_output.absolute(),
        image.absolute()
    ]
    run('Executing get-bc', get_bc_cmd, cwd=args.make_builddir, env=make_env)

    # strip away llvm bitcode
    for file_name in ['crt1.o', 'Scrt1.o', 'rcrt1.o', 'libc.a', 'libc.so']:
        file = Path(args.musl_install_dir / 'lib' / file_name)
        assert file.is_file()
        objcopy_cmd = [
            args.llvm_objcopy_program,
            '--remove-section', '.llvm_bc',
            file.absolute()
        ]
        run(f'Executing llvm-objcopy on {file_name}',
            objcopy_cmd,
            cwd=args.musl_install_dir)


if __name__ == '__main__':
    main()

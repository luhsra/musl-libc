#!/usr/bin/env python
"""Build and install the Musl Libc."""
from pathlib import Path
from build_tools import run, Builder


class MuslBuilder(Builder):
    """Build bitcode and install the musl libc."""
    def __init__(self):
        super().__init__(with_make=True,
                         with_gclang=True,
                         with_install_dir=True)

    def do_build(self):
        self._make_new(self.args.build_dir)
        self._make_new(self.args.install_dir)

        env = self._get_gllvm_env()
        env['CC'] = str(self.args.gclang_program.absolute())
        env['OBJ'] = self.args.build_dir.absolute()

        cfg_cmd = [
            self.args.src_dir / 'configure',
            '--enable-debug',
            '--target=LLVM',
            '--build=LLVM',
            '--prefix=' + str(self.args.install_dir.absolute()),
            '--syslibdir=' + str(self.args.install_dir.absolute()),
        ]

        run('Executing configure', cfg_cmd, cwd=self.args.src_dir, env=env)
        make_cmd = [self.args.make_program, f'-j{self.jobs}']
        run('Executing Make', make_cmd, cwd=self.args.src_dir, env=env)
        minst_cmd = [self.args.make_program, 'install']
        run('Executing Make', minst_cmd, cwd=self.args.src_dir, env=env)

        image = self.args.install_dir / 'lib' / 'libc.a'
        assert image.is_file()

        self._get_bc(image, env)

        # strip away llvm bitcode
        for file_name in ['crt1.o', 'Scrt1.o', 'rcrt1.o', 'libc.a', 'libc.so']:
            file = Path(self.args.install_dir / 'lib' / file_name)
            assert file.is_file()
            objcopy_cmd = [
                self.args.llvm_objcopy_program,
                '--remove-section', '.llvm_bc',
                file.absolute()
            ]
            run(f'Executing llvm-objcopy on {file_name}',
                objcopy_cmd,
                cwd=self.args.install_dir)


if __name__ == '__main__':
    builder = MuslBuilder()
    builder.do_build()

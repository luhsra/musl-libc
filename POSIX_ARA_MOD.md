
The following changes are made to musl libc:

- Replaced some arch specific asm code to generic C Code:
    This is done by defining a new dummy arch called LLVM. (Defined in ./configure line 331)
    Arch specific asm code will then be ignored by the musl Makefile.
    For the code without a generic C Code replacement, a symbolic link is placed
    to redirect to the x86_64 implementation.
    the following symbolic links are required:
        - arch/LLVM         -> arch/x86_64
        - crt/LLVM          -> crt/x86_64
        - src/setjmp/LLVM   -> src/setjmp/x86_64
        - src/thread/LLVM   -> src/thread/x86_64
    (based on the LLVM dummy arch idea in the project: https://github.com/SRI-CSL/musllvm)

- Set compiler for musl-clang explicitly to "clang".
    This avoids the usage of wllvm as compiler in musl-clang.
    musl-clang will be called by wllvm. If musl-clang also calls wllvm this leads to endless recursion.
    The changes are in the following files on line 2:
        - tools/ld.musl-clang.in
        - tools/musl-clang.in

- Created a dummy for pthread_attr_setname_np and pthread_attr_getname_np so that these functions are detectable as syscalls.
    See the following files:
        - include/pthread.h line: 240
        - src/POSIX_ARA_MOD/pthread_attr_setname_np.c
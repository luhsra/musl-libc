
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
        - include/pthread.h (line 240)
        - src/POSIX_ARA_MOD/pthread_attr_setname_np.c

- Removed weak alias  malloc() -> default_malloc()  and replaced it with a simple function that redirects.
    This allows the SVF to detect malloc() as a syscall.
    See src/malloc/lite_malloc.c (line 118)

- Allow detection of open(path, oflag, ...) with its optional argument.
    ARA can only analyze syscalls with a fixed number of arguments.
    Variable argument lists are not supported.
    We circumvent this issue by mapping  open(path, oflag) -> open(path, oflag, 0) [See the macros in include/fcntl.h line 44]
    The internal name of open() is now _ARA_open_syscall_() [See src/fcntl/open.c]

- Created extra translation units for architecture specific x86_64 assembly functions.
    In default musl libc all of the assembly functions are declared as inline.
    It is easier to remove or detect the functions if there are located in an extra translation unit.
    We move the implementation of the functions in the following way:
        - arch/LLVM/atomic_arch.h -> src/POSIX_ARA_MOD/atomic_arch.c
        - arch/LLVM/pthread_arch.h -> src/POSIX_ARA_MOD/pthread_arch.c
        - arch/LLVM/syscall_arch.h -> src/POSIX_ARA_MOD/syscall_arch.c

- sigaction(): Allow the detection of inner fields in the sigaction struct act.
    It is hard to analyze a struct as argument in ARA.
    We circumvent this issue with a macro that unpacks the fields in the struct.
    The internal name of sigaction() is now _ARA_sigaction_syscall_().
    See the following files:
        - include/signal.h (starting at line 220)
        - src/signal/sigaction.c (line 84)
        - src/POSIX_ARA_MOD/ara_sigaction_handling.c
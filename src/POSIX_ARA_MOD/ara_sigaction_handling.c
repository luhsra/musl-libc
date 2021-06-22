
#include <stddef.h>
#include <signal.h>

// The function we want to detect within ARA. (sigaction)
// Packs all the act fields together again and invokes the actual sigaction() call. 
int _ARA_sigaction_syscall_(int _sig, 
                            void (*_sa_handler)(int),
                            sigset_t _sa_mask,
                            int _sa_flags,
                            void (*_sa_sigaction)(int, siginfo_t*, void*),
                            struct sigaction *restrict old)
{
    struct sigaction act;
    act.sa_handler =_sa_handler;
    act.sa_mask = _sa_mask;
    act.sa_flags = _sa_flags;
    act.sa_sigaction = _sa_sigaction;
    return _orig_musl_sigaction(_sig, &act, old);
}
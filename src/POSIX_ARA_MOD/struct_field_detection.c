
#include <stddef.h>
#include <signal.h>
#include <time.h>
#include <pthread.h>
#include <sched.h>


// The function we want to detect within ARA. (sigaction)
// Packs all the act fields together again and invokes the actual sigaction() call. 
int ARA_sigaction_syscall_(int _sig, 
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
    return (sigaction)(_sig, &act, old);
}

// nanosleep()
int ARA_nanosleep_syscall_(time_t tv_sec, long tv_nsec, struct timespec *rem) {
    struct timespec req = {.tv_sec = tv_sec, .tv_nsec = tv_nsec};
    return (nanosleep)(&req, rem);
}

// pthread_attr_setschedparam()
int ARA_pthread_attr_setschedparam_syscall_(pthread_attr_t *restrict a, const int sched_priority) {
    struct sched_param param = {.sched_priority = sched_priority};
 	return (pthread_attr_setschedparam)(a, &param);
}

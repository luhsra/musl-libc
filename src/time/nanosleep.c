#include <time.h>
#include "syscall.h"

// nanosleep
int _ARA_nanosleep_syscall_(time_t tv_sec, long tv_nsec, struct timespec *rem)
{
	struct timespec req = {.tv_sec = tv_sec, .tv_nsec = tv_nsec};
	return __syscall_ret(-__clock_nanosleep(CLOCK_REALTIME, 0, &req, rem));
}

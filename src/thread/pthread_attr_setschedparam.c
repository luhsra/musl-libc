#include "pthread_impl.h"

int _ARA_pthread_attr_setschedparam_syscall_(pthread_attr_t *restrict a, const int sched_priority)
{
	a->_a_prio = sched_priority;
	return 0;
}

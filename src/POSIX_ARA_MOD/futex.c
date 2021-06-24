
#include <pthread_impl.h>

void __wake(volatile void *addr, int cnt, int priv)
{
	if (priv) priv = FUTEX_PRIVATE;
	if (cnt<0) cnt = INT_MAX;
	__syscall(SYS_futex, addr, FUTEX_WAKE|priv, cnt) != -ENOSYS ||
	__syscall(SYS_futex, addr, FUTEX_WAKE, cnt);
}
void __futexwait(volatile void *addr, int val, int priv)
{
	if (priv) priv = FUTEX_PRIVATE;
	__syscall(SYS_futex, addr, FUTEX_WAIT|priv, val, 0) != -ENOSYS ||
	__syscall(SYS_futex, addr, FUTEX_WAIT, val, 0);
}
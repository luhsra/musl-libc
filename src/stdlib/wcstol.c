#include "stdio_impl.h"
#include "intscan.h"
#include "shgetc.h"
#include <inttypes.h>
#include <limits.h>
#include <wctype.h>
#include <wchar.h>

size_t do_read(FILE *f, unsigned char *buf, size_t len);

static unsigned long long wcstox(const wchar_t *s, wchar_t **p, int base, unsigned long long lim)
{
	wchar_t *t = (wchar_t *)s;
	unsigned char buf[64];
	FILE f = {0};
	f.flags = 0;
	f.rpos = f.rend = f.buf = buf + 4;
	f.buf_size = sizeof buf - 4;
	f.lock = -1;
	f.read = do_read;
	while (iswspace(*t)) t++;
	f.cookie = (void *)t;
	shlim(&f, 0);
	unsigned long long y = __intscan(&f, base, 1, lim);
	if (p) {
		size_t cnt = shcnt(&f);
		*p = cnt ? t + cnt : (wchar_t *)s;
	}
	return y;
}

unsigned long long wcstoull(const wchar_t *restrict s, wchar_t **restrict p, int base)
{
	return wcstox(s, p, base, ULLONG_MAX);
}

long long wcstoll(const wchar_t *restrict s, wchar_t **restrict p, int base)
{
	return wcstox(s, p, base, LLONG_MIN);
}

unsigned long wcstoul(const wchar_t *restrict s, wchar_t **restrict p, int base)
{
	return wcstox(s, p, base, ULONG_MAX);
}

long wcstol(const wchar_t *restrict s, wchar_t **restrict p, int base)
{
	return wcstox(s, p, base, 0UL+LONG_MIN);
}

intmax_t wcstoimax(const wchar_t *restrict s, wchar_t **restrict p, int base)
{
	return wcstoll(s, p, base);
}

uintmax_t wcstoumax(const wchar_t *restrict s, wchar_t **restrict p, int base)
{
	return wcstoull(s, p, base);
}

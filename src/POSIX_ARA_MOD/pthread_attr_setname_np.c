
#include <pthread.h>

// Dummy implementation of these two syscalls.

int pthread_attr_setname_np(pthread_attr_t *attr, const char *name) {
    return 0;
}

int pthread_attr_getname_np(pthread_attr_t *attr, char *buf, size_t len) {
    *buf = '\0';
    return 0;
}
#include <stdio.h>
#include <stdlib.h>

char bss_buf[0x100];

void main()
{
	long long d;
	d = (long long)&d;
	printf("%lx\n", d);
	char *buffer = (char *)malloc(0x100);
	read(0, buffer, 0x100);
	snprintf(bss_buf, 0x100, buffer);
}
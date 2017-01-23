#include <stdio.h>

//gcc format64.c -o format64

void main(){
	char buf[0x100];
	
	while(true){
		gets(buf);
		printf(buf);
		sleep(1);
	}
}


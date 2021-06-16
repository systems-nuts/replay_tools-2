#include <stdio.h>
#include <stdlib.h>
#include <sys/sysinfo.h>
#include <unistd.h>
#include <string.h>
static int malloc_memory=0;
//max memory replay 1TB
static void** pool;
struct sysinfo s_info;
int current_sys_memory(struct sysinfo s_info)
{
	int ret;
	sysinfo(&s_info);
	ret= (int)((s_info.totalram-s_info.freeram)/1024);
	return ret;
}

void add_memory(int __memory)
{
	int i;
	for(i=malloc_memory; i<malloc_memory+__memory;i++)
	{
		pool[i]= malloc(1024*1024*sizeof(void));
		memset(pool[i],1,1024*1024*sizeof(void));
	}
	malloc_memory+=__memory;
}
void remove_memory(int __memory)
{
	while(malloc_memory!=__memory)
	{
		malloc_memory--;
		memset(pool[malloc_memory],0,1024*1024*sizeof(void));
		free(pool[malloc_memory]);
	}
}
void free_all()
{
	remove_memory(0);
}


int main()
{
	pool = malloc(1024*1024*10*sizeof(void));
	FILE * fp;
    	char * line = NULL;
    	size_t len = 0;
    	ssize_t read;
	struct sysinfo s_info;
	int replay_memory,sys_memory,__memory;
	sys_memory=current_sys_memory(s_info);
    	fp = fopen("./memory_record", "r");
   	if (fp == NULL)
        	exit(EXIT_FAILURE);

    	while ((read = getline(&line, &len, fp)) != -1) {
		replay_memory=atoi(line)*81668;
		if(replay_memory<sys_memory){ free_all();goto finish;}
		__memory=(replay_memory-sys_memory)/(sizeof(void)*1024);
		
		if(__memory==0) goto finish;
		if(__memory-malloc_memory >0)
			add_memory(__memory-malloc_memory);
		else if (__memory-malloc_memory <0)
			remove_memory(__memory);
		else
			goto finish;
finish:
		printf("needed_memory: %dmb,already malloc_memory %dmb\n",(replay_memory-sys_memory)/(sizeof(void)*1024),malloc_memory);
		sleep(1);
    	}

    	fclose(fp);
	if (line)
		free(line);
	return 0;
}


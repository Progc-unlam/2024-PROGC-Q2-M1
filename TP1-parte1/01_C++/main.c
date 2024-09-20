#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

#include <string.h>
#include <linux/prctl.h>
#include <sys/prctl.h>

#define EXIT_SUCCESS 0
#define TIMETOSLEEP 30

void errorChild(char* nameChild);
void changeName(char* name);
void sleepAndWait(int cantWaits);

int main()
{
    int i;
    pid_t pid = fork();


    if(pid<0)
    {
        errorChild("B");
        return EXIT_FAILURE;
    }
    if(pid)//A
    {
        changeName("A");
        sleepAndWait(1);
        return EXIT_SUCCESS;
    }
    //B
    changeName("B");
    pid=fork();
    if(pid<0)
    {
        errorChild("C");
        return EXIT_FAILURE;
    }
    if(!pid) //c
    {
        changeName("C");
        pid=fork();
        if(pid<0)
        {
            errorChild("E");
            return EXIT_FAILURE;
        }
        if(pid) //C
        {
            sleepAndWait(1);
            return EXIT_SUCCESS;
        }
        //E
        changeName("E");
        for(i=0; i<2; i++) //H - I
        {
            pid=fork();
            if(pid<0)
            {
                errorChild(i==0?"H":"I");
                return EXIT_FAILURE;
            }
            if(!pid)
            {
                changeName(i==0?"H":"I");
                sleepAndWait(0);
                return EXIT_SUCCESS;
            }
        }
        sleepAndWait(2);
        return EXIT_SUCCESS;
    }

    //sigue b PARA D
    pid=fork();
    if(pid<0)
    {
        errorChild("D");
        return EXIT_FAILURE;
    }
    if(!pid) // D
    {
        changeName("D");
        for(i=0; i<2; i++) //F - G
        {
            pid=fork();
            if(pid<0)
            {
                errorChild(i==0?"F":"G");
                return EXIT_FAILURE;
            }
            if(!pid)
            {
                changeName(i==0?"F":"G");
                sleepAndWait(0);
                return EXIT_SUCCESS;
            }
        }
        sleepAndWait(2);
        return EXIT_SUCCESS;
    }
    //sigue b
    sleepAndWait(2);
    return EXIT_SUCCESS;
}

void errorChild(char* nameChild)
{
  printf("Error de creación de %s\n",nameChild);
}

void changeName(char* name)
{
  char auxCad[16]="NameDefault";
  prctl(PR_SET_NAME, strcpy(auxCad,name),NULL,NULL,NULL);
}

void sleepAndWait(int cantWaits)
{
  int i;
  sleep(TIMETOSLEEP);
  for(i=0;i<cantWaits;i++)
    wait(NULL);
}
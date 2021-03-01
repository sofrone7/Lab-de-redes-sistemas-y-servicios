#include <stdio.h> /* perror() */
#include <stdlib.h> /* exit() */

void DieWithError(char *errorMessage)
{
	perror(errorMessage);
	exit(1);
}

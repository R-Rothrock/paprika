// inflating.c
// https://github.com/R-Rothrock/paprika

#include<inflating.h>

int inflate_deb(const char *pathname)
{
  char *cmd = malloc(6 + strlen(pathname));
  sprintf(AR_UNZIP, pathname);
  return system(cmd);
}


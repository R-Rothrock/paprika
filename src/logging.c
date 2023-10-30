// logging.c
// https://github.com/R-Rothrock/paprika

#include<stdio.h>

#include "logging.h"

void debug(const char *msg)
{
  #ifdef __DEUBG__
  #if __DEBUG__ == 1
  printf(DEBUG, msg);
  #endif
  #endif
}

void info(const char *msg)
{
  printf(INFO, msg);
}

void warning(const char *msg)
{
  print(WARNING, msg);
}

void critical(const char *msg)
{
  printf(CRITICAL, msg);
}

void error(const char *msg)
{
  printf(ERROR, msg);
}


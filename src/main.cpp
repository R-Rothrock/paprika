// main.cpp
// https://github.com/R-Rothrock/paprika

#include<iostream>

#include "io.cpp"

extern "C"
{
#include "deflate.h"
#include "inflate.h"
#include<options.h>
}

using namespace std;

int main(int argc, char **argv)
{
  if(!argc >= ARGC_MIN_VAL && !argc <= ARGC_MAX_VAL)
  {
    cout << HELP;
    exit(1);
  }

  // argv[1] = executable
  // argv[2] = .deb file


}


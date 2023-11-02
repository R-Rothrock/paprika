// main.cpp
// https://github.com/R-Rothrock/paprika

#include<iostream>

#include "io.cpp"

extern "C"
{
#include "deflate.h"
#include "inflate.h"
#include "options.h"
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

  // steps
  // 
  // if we're on Debian:
  // 	dpkg does all of this for us
  // 	to extract everything:
  // 	`mkdir tmp`
  // 	`dpkg-deb -R <.deb> tmp`
  // 	to recompile:
  // 	`dpkg-deb -b tmp`
  // 	and remember:
  // 	`rm -r tmp`
  // else:
  // 	to extract:
  // 	`ar -x <.deb>`
  // 	`mkdir control data`
  // 	if extension is `.gz`:
  // 		`gzip -d *.gz`
  // 	if extension is `.xz`:
  // 		`xz -d *.gz`
  // 	`tar -xf control.tar -C ./control/`
  // 	`tar -xf data.tar -C ./data/`
  // 	to recompile:
  // 	
}


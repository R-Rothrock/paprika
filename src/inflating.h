// inflating.h
// https://github.com/R-Rothrock/paprika

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

// each function described here will deflate something, along with
// saving a backup of the file being operated on.
#define MV_TO_BACKUP "mv %s %s.old"
#define MV_FROM_BACKUP "mv %s.old %s"

// inflate a .deb file
// leaves `data.tar.gz`, `control.tar.gz`, and `debian_binary`
// returns the return value of the command(s)
int inflate_deb(const char *pathname);

// helpful macros
#define AR_UNZIP "ar x %s"

// inflate `control.tar.gz`
// leaves `control`, `md5sums`, `conffiles`, and maybe a few more
// returns the return value of the command(s)
int inflate_control(const char *pathname);

// inflate `data.tar.gz`
// leaves a lot of stuff
// return the return value of the command(s)
int inflate_data(const char *pathname);

// helpful macros for both `inflate_control` and `inflate_data`
#define GZ_UNZIP "gzip -d %s"
#define TAR_UNZIP "tar -xf %s"



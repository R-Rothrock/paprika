// md5.c
// https://github.com/R-Rothrock/paprika

#include<fcntl.h>
#include<string.h>
#include<sys/mman.h>
#include<sys/stat.h>

#include<openssl/md5.h>

#include "md5.h"

char *md5_str(const char *str)
{
  char ret[MD5_DIGEST_LENGTH];
  MD5(str, strlen(str), ret);
  return &ret;
}

char *md5_file(const char *pathname)
{
  int fd = open(pathname, O_RDONLY);
  struct stat st;
  fstat(pathname, &st);

  char *file_buf = mmap(0, st.st_size, PROT_READ, MAP_SHARED, fd, 0);
  char *ret md5_str(file_buf);
  munmap(file_buf, st.st_size);

  return ret;
}


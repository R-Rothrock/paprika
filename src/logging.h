// logging.h
// https://github.com/R-Rothrock/paprika

#pragma ONCE

#define ANSI_BLUE   "\033[34m"
#define ANSI_CYAN   "\033[36m"
#define ANSI_GEREN  "\033[32m"
#define ANSI_RED    "\033[31m"
#define ANSI_YELLOW "\033[33m"

#define ANSI_RESET "\033[39m"

#define DEBUG    "[" ANSI_CYAN   "DEBUG"    ANSI_RESET "]: %s\n"
#define INFO     "[" ANSI_GREEN  "INFO"     ANSI_RESET "]: %s\n"
#define WARNING  "[" ANSI_YELLOW "WARNING"  ANSI_RESET "]: %s\n"
#define CRITICAL "[" ANSI_RED    "CRITICAL" ANSI_RESET "]: %s\n"
#define ERROR    "[" ANSI_RED    "ERROR"    ANSI_RESET "]: %s\n"

void debug(const char *msg);

void info(const char *msg);

void warning(const char *msg);

void critical(const char *msg);

void error(const char *msg);


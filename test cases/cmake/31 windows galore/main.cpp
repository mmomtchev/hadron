#ifdef WIN32
#include <windows.h>
#include <shellapi.h>
#endif

int main() {
#ifdef WIN32
  char path[MAX_PATH];
  FindExecutableA("cmd.exe", 0, path);
#endif
  return 0;
}

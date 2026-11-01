#include <string>

#if defined _WIN32 || defined __CYGWIN__
#if defined CMMODINTERNAL_BUILD
  #define DLL_PUBLIC __declspec(dllexport)
#else
  #ifdef SHARED
    #define DLL_PUBLIC __declspec(dllimport)
  #else
    #define DLL_PUBLIC
  #endif
#endif
#else
  #if defined __GNUC__
    #define DLL_PUBLIC __attribute__ ((visibility("default")))
  #else
    #pragma message ("Compiler does not support symbol visibility.")
    #define DLL_PUBLIC
  #endif
#endif

class DLL_PUBLIC cmModInternalClass {
private:
  std::string str;

public:
  cmModInternalClass(const std::string &foo);
  std::string getStr() const;
};

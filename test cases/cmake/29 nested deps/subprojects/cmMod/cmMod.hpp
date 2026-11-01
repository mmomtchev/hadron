#include "cmMod_internal.hpp"
#include <string>

#if defined _WIN32 || defined __CYGWIN__
#if defined CMMODXX_BUILD
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

class DLL_PUBLIC cmModClass : public cmModInternalClass {
public:
  using cmModInternalClass::cmModInternalClass;
};

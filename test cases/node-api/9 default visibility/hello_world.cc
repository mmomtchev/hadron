#include <napi.h>

#undef NAPI_MODULE_EXPORT
#define NAPI_MODULE_EXPORT

using namespace Napi;

Napi::String Method(const Napi::CallbackInfo &info) {
  Napi::Env env = info.Env();
  return Napi::String::New(env, "world");
}

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set(Napi::String::New(env, "HelloWorld"),
              Napi::Function::New(env, Method));
  return exports;
}

NODE_API_MODULE(addon, Init)

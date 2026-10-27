#pragma once

#include <memory>
#include <string>

#if defined(_WIN32)
  #if defined(SDK_BUILD)
    #define SDK_API __declspec(dllexport)
  #else
    #define SDK_API __declspec(dllimport)
  #endif
#else
  #define SDK_API __attribute__((visibility("default")))
#endif

namespace sdk {

// Interface class: the public contract exposed by the SDK.
class SDK_API ISdk {
public:
    virtual ~ISdk() = default;

    // Returns the SDK version string, e.g. "1.0.0.0".
    virtual std::string getVersion() const = 0;
};

// Factory that returns the concrete SDK implementation.
SDK_API std::unique_ptr<ISdk> createSdk();

} // namespace sdk

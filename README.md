# Sample PyQt Application with C++ SDK

```
SDk/
  include/ISdk.h        public interface class (ISdk) + createSdk() factory
  lib/libsdk.so*        prebuilt C++ SDK
  lib/sdk_module*.so    prebuilt Python module (pybind11), links to libsdk.so
application/
  main.py               PyQt5 UI that shows the SDK version
```

The SDK source is not included; `SDk/` ships only the header and prebuilt binaries
(Linux x86_64, built for Python 3.10).

## Run the application

```bash
pip install PyQt5
cd application
python3 main.py
```

`main.py` imports `sdk_module` from `SDk/lib/`. The module finds `libsdk.so` next
to itself, so no `LD_LIBRARY_PATH` is needed.

## Use the SDK from C++

```cpp
#include <iostream>
#include "ISdk.h"

int main() {
    auto sdk = sdk::createSdk();
    std::cout << "SDK version: " << sdk->getVersion() << std::endl;
}
```

```bash
g++ -std=c++17 main.cpp -I SDk/include -L SDk/lib -lsdk -Wl,-rpath,'$ORIGIN/SDk/lib' -o demo
./demo
```

Or with CMake:

```cmake
add_executable(demo main.cpp)
target_include_directories(demo PRIVATE ${CMAKE_SOURCE_DIR}/SDk/include)
target_link_libraries(demo PRIVATE ${CMAKE_SOURCE_DIR}/SDk/lib/libsdk.so)
```

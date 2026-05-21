# Instances

- **Header**: `instances.h`
- **Namespace**: `acs::global`
- **Include**: `#include "instances.h"`

## Overview

This header defines global instances of commonly used classes in the system, such as the TOML reader. These instances are intended for convenient access across the codebase without needing to manage their lifetimes explicitly.

## API

### Variables

#### TOML Reader Instance

```cpp
inline utility::toml_reader toml_reader;
```
Global [`utility::toml_reader`](../utility/implementation/toml_reader.md) instance for loading configuration files.

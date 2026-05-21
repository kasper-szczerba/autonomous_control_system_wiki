---
icon: lucide/rocket
---

# Autonomous Control System

Welcome to the documentation for the Autonomous Control System project. This is a custom C++23 (ISO/IEC 14882:2024) control system, designed for the RDW's Self-Driving Challenge 2026.

!!! note
    The documentation and codebase are currently under active development. Some sections may be incomplete or subject to change.

## Getting Started

### Prerequisites

Before building the project, ensure the following are installed:

- **C++23 compiler**: GCC 14+, Clang 18+, or MSVC 2022 17.10+
- **CMake**: 3.28+
- **vcpkg**: Used to manage library dependencies
- **CUDA Toolkit**: 12.6 required for GPU-accelerated processing on the NVIDIA Jetson Orin platform
- **ZED SDK**: Required for ZED stereo camera support

### Dependencies

The following libraries are managed via [vcpkg](https://vcpkg.io/) and resolved automatically during the CMake configure step:

| Library                | Purpose                                                   |
| ---------------------- | --------------------------------------------------------- |
| opencv4                | Image processing (`cuda`, `cudnn`, `dnn-cuda`, `contrib`) |
| spdlog                 | Logging                                                   |
| toml++                 | TOML configuration file parsing                           |
| zenoh-pico / zenoh-cpp | Communication middleware                                  |

`zenoh-pico` and `zenoh-cpp` are **custom vcpkg ports** located in the `vcpkg_ports/` directory of the repository. They are registered as overlay ports in `vcpkg-configuration.json` and resolved automatically, no extra flags are needed.

### Building

```bash
cmake --build build
```

### Running

Once built, run the resulting binary from the `build` directory. 

### Configuration

The system reads its configuration from a TOML file, see the [`toml_reader`](./codebase/namespaces/utility/implementation/toml_reader.md) documentation for details on configuration options.

The configuration file is located at `configuration/configuration.toml`.

---

## Changelog

[View the changelog](./changelog/index.md) to see the latest updates and changes made to the project.

## Codebase

[Explore the codebase documentation](./codebase/index.md) to understand the architecture, components, and implementation details of the Autonomous Control System.

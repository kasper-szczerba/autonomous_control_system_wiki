# Threaded Component

- Class: `threaded_component`
- Namespace: `acs::core`
- Include: `#include "core/implementation/threaded_component.h"`

## Overview

Base class for components that execute updates on a dedicated thread. This class extends [`updatable_component`](updatable_component.md) and implements [`i_threaded_component`](../interfaces/i_threaded_component.md), including thread lifecycle and timing control.

## API

### Constructors

#### Constructor

```cpp
explicit threaded_component(std::string_view name, std::shared_ptr<utility::i_toml_reader> toml_reader_ptr);
```
Creates a threaded component with the specified name.

##### Parameters
- `name`: The name of the component.
- `toml_reader_ptr`: A shared pointer to a TOML reader for configuration.

### Public Methods

#### Implementations
- [`i_threaded_component`](../interfaces/i_threaded_component.md)
    - [`begin`](../interfaces/i_threaded_component.md#begin)
    - [`end`](../interfaces/i_threaded_component.md#end)
    - [`cancel_begin`](../interfaces/i_threaded_component.md#cancel-begin)
    - [`get_update_rate`](../interfaces/i_threaded_component.md#get-update-rate)
    - [`set_update_rate`](../interfaces/i_threaded_component.md#set-update-rate)
    - [`get_is_running`](../interfaces/i_threaded_component.md#get-is-running)
    - [`get_mutex`](../interfaces/i_threaded_component.md#get-mutex)

### Protected Methods

#### On Setup

```cpp
void on_setup() override;
```
Called during the setup phase. Derived classes should implement this to initialize thread-specific resources.

#### On Teardown

```cpp
void on_teardown() override;
```
Called during the teardown phase. Derived classes should implement this to clean up thread-specific resources.


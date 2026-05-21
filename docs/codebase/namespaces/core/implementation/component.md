# Component

- Class: `component`
- Namespace: `acs::core`
- Include: `#include "core/implementation/component.h"`

## Overview

Concrete implementation of the [`i_component`](../interfaces/i_component.md) interface. This class provides a base implementation for components in the system, handling common functionality such as setup and teardown.

## API

### Constructors

#### Default Constructor

```cpp
explicit component(std::string_view name);
```
Creates a new component with the specified name.

##### Parameters
- `name`: The name of the component.

### Public Methods

#### Implementations
- [`i_component`](../interfaces/i_component.md)
    - [`setup`](../interfaces/i_component.md#setup)
    - [`teardown`](../interfaces/i_component.md#teardown)
    - [`get_name`](../interfaces/i_component.md#get-name)
    - [`get_is_setup_completed`](../interfaces/i_component.md#get-is-setup-completed)

### Protected Methods

#### On Setup

```cpp
virtual void on_setup() = 0;
```
Called during the setup phase. Derived classes must implement this to perform initialization.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### On Teardown

```cpp
virtual void on_teardown() = 0;
```
Called during the teardown phase. Derived classes must implement this to perform cleanup.

!!! note
    Pure virtual method, must be implemented by derived classes.


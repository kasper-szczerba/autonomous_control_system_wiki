# Updatable Component

- Class: `updatable_component`
- Namespace: `acs::core`
- Include: `#include "core/implementation/updatable_component.h"`

## Overview

Base class for components with an update cycle. This class extends [`component`](component.md) and implements [`i_updatable_component`](../interfaces/i_updatable_component.md), delegating the update logic to derived classes.

## API

### Constructors

#### Constructor

```cpp
explicit updatable_component(std::string_view name);
```
Creates an updatable component with the specified name.

##### Parameters
- `name`: The name of the component.

### Public Methods

#### Implementations
- [`i_updatable_component`](../interfaces/i_updatable_component.md)
    - [`update`](../interfaces/i_updatable_component.md#update)

### Protected Methods

#### On Update

```cpp
virtual void on_update() = 0;
```
Called on each update cycle. Derived classes must implement this to perform update logic.

!!! note
    Pure virtual method, must be implemented by derived classes.


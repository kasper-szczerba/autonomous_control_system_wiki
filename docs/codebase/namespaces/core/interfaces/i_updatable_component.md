`Interface`

# Updatable Component

- **Interface**: `i_updatable_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/interfaces/i_updatable_component.h"`

## Overview

Interface for components that expose an update cycle. This interface extends [`i_component`](i_component.md) and adds a single update method intended for repeated execution.

## API

### Public Methods

#### Update

```cpp
virtual void update() = 0;
```
Runs one update step for the component.

!!! note
    Pure virtual method, must be implemented by derived classes.

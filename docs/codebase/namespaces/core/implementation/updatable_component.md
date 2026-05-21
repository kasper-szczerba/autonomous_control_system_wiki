# Updatable Component

- **Class**: `updatable_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/implementation/updatable_component.h"`

## Overview

Concrete implementation of [`i_updatable_component`](../interfaces/i_updatable_component.md). Extends [`component`](component.md) and adds a single `update()` cycle.

## Inheritance Diagram

### Base Diagram

```mermaid
graph TD
    updatable_component["updatable_component"]
    component["component"] --> i_component["i_component"]
    i_updatable_component["i_updatable_component"] --> i_component["i_component"]
    updatable_component["updatable_component"] --> component["component"]
    updatable_component["updatable_component"] --> i_updatable_component["i_updatable_component"]
```

### Derived Diagram

```mermaid
graph TD
    updatable_component["updatable_component"]
    threaded_component["threaded_component"] --> floor_detector["floor_detector"]
    threaded_component["threaded_component"] --> obstacle_detector["obstacle_detector"]
    threaded_component["threaded_component"] --> obstacle_detector_preview["obstacle_detector_preview"]
    threaded_component["threaded_component"] --> zed_camera["zed_camera"]
    threaded_component["threaded_component"] --> zed_camera_preview["zed_camera_preview"]
    updatable_component["updatable_component"] --> threaded_component["threaded_component"]
```

## Inheritance Hierarchy

### Base Hierarchy

- [`updatable_component`](updatable_component.md)
  - [`component`](component.md)
    - [`i_component`](../interfaces/i_component.md)
  - [`i_updatable_component`](../interfaces/i_updatable_component.md)
    - [`i_component`](../interfaces/i_component.md)

### Derived Hierarchy

- [`updatable_component`](updatable_component.md)
  - [`threaded_component`](threaded_component.md)
    - [`floor_detector`](../../vision/implementation/detection/floor_detector.md)
    - [`obstacle_detector`](../../vision/implementation/detection/obstacle_detector.md)
    - [`obstacle_detector_preview`](../../vision/implementation/previews/obstacle_detector_preview.md)
    - [`zed_camera`](../../vision/implementation/zed_camera.md)
    - [`zed_camera_preview`](../../vision/implementation/previews/zed_camera_preview.md)

## API

### Constructors
#### Constructor

```cpp
explicit updatable_component(std::string_view name, std::shared_ptr<utility::i_toml_reader> toml_reader_ptr);
```
Creates an updatable component with the specified name.

##### Parameters
- `name`: The name of the component.
- `toml_reader_ptr`: A shared pointer to a TOML reader for configuration.

### Public Methods

#### Implementations
- [`i_updatable_component`](../interfaces/i_updatable_component.md)
    - [`update`](../interfaces/i_updatable_component.md#update)

### Protected Methods
#### On Update

```cpp
virtual void on_update() = 0;
```
Calls `on_update()` to execute one update step.

!!! note
    Pure virtual method, must be implemented by derived classes.

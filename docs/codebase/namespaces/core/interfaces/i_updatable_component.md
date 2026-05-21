# Updatable Component Interface

- **Interface**: `i_updatable_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/interfaces/i_updatable_component.h"`

## Overview

Interface for components that support a repeated update cycle. Extends [`i_component`](i_component.md).

## Inheritance Diagram

### Base Diagram

```mermaid
graph TD
    i_updatable_component["i_updatable_component"]
    i_updatable_component["i_updatable_component"] --> i_component["i_component"]
```

### Derived Diagram

```mermaid
graph TD
    i_updatable_component["i_updatable_component"]
    i_floor_detector["i_floor_detector"] --> floor_detector["floor_detector"]
    i_obstacle_detector["i_obstacle_detector"] --> obstacle_detector["obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_floor_detector["i_floor_detector"]
    i_threaded_component["i_threaded_component"] --> i_obstacle_detector["i_obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_zed_camera["i_zed_camera"]
    i_threaded_component["i_threaded_component"] --> threaded_component["threaded_component"]
    i_updatable_component["i_updatable_component"] --> i_threaded_component["i_threaded_component"]
    i_updatable_component["i_updatable_component"] --> updatable_component["updatable_component"]
    i_zed_camera["i_zed_camera"] --> zed_camera["zed_camera"]
    threaded_component["threaded_component"] --> floor_detector["floor_detector"]
    threaded_component["threaded_component"] --> obstacle_detector["obstacle_detector"]
    threaded_component["threaded_component"] --> obstacle_detector_preview["obstacle_detector_preview"]
    threaded_component["threaded_component"] --> zed_camera["zed_camera"]
    threaded_component["threaded_component"] --> zed_camera_preview["zed_camera_preview"]
    updatable_component["updatable_component"] --> threaded_component["threaded_component"]
```

## Inheritance Hierarchy

### Base Hierarchy

- [`i_updatable_component`](i_updatable_component.md)
  - [`i_component`](i_component.md)

### Derived Hierarchy

- [`i_updatable_component`](i_updatable_component.md)
  - [`i_threaded_component`](i_threaded_component.md)
    - [`i_floor_detector`](../../vision/interfaces/detection/i_floor_detector.md)
      - [`floor_detector`](../../vision/implementation/detection/floor_detector.md)
    - [`i_obstacle_detector`](../../vision/interfaces/detection/i_obstacle_detector.md)
      - [`obstacle_detector`](../../vision/implementation/detection/obstacle_detector.md)
    - [`i_zed_camera`](../../vision/interfaces/i_zed_camera.md)
      - [`zed_camera`](../../vision/implementation/zed_camera.md)
    - [`threaded_component`](../implementation/threaded_component.md)
      - [`floor_detector`](../../vision/implementation/detection/floor_detector.md)
      - [`obstacle_detector`](../../vision/implementation/detection/obstacle_detector.md)
      - [`obstacle_detector_preview`](../../vision/implementation/previews/obstacle_detector_preview.md)
      - [`zed_camera`](../../vision/implementation/zed_camera.md)
      - [`zed_camera_preview`](../../vision/implementation/previews/zed_camera_preview.md)
  - [`updatable_component`](../implementation/updatable_component.md)
    - [`threaded_component`](../implementation/threaded_component.md)
      - [`floor_detector`](../../vision/implementation/detection/floor_detector.md)
      - [`obstacle_detector`](../../vision/implementation/detection/obstacle_detector.md)
      - [`obstacle_detector_preview`](../../vision/implementation/previews/obstacle_detector_preview.md)
      - [`zed_camera`](../../vision/implementation/zed_camera.md)
      - [`zed_camera_preview`](../../vision/implementation/previews/zed_camera_preview.md)

## API

### Public Methods
#### Update

```cpp
virtual void update() = 0;
```
Performs one update cycle.

!!! note
    Pure virtual method, must be implemented by derived classes.

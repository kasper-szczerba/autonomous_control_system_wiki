# Threaded Component Interface

- **Interface**: `i_threaded_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/interfaces/i_threaded_component.h"`

## Overview

Interface for components that run their update loop on a dedicated thread. Extends [`i_updatable_component`](i_updatable_component.md) and adds thread start/stop control and mutex access.

## Inheritance Diagram

### Base Diagram

```mermaid
graph TD
    i_threaded_component["i_threaded_component"]
    i_threaded_component["i_threaded_component"] --> i_updatable_component["i_updatable_component"]
    i_updatable_component["i_updatable_component"] --> i_component["i_component"]
```

### Derived Diagram

```mermaid
graph TD
    i_threaded_component["i_threaded_component"]
    i_floor_detector["i_floor_detector"] --> floor_detector["floor_detector"]
    i_obstacle_detector["i_obstacle_detector"] --> obstacle_detector["obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_floor_detector["i_floor_detector"]
    i_threaded_component["i_threaded_component"] --> i_obstacle_detector["i_obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_zed_camera["i_zed_camera"]
    i_threaded_component["i_threaded_component"] --> threaded_component["threaded_component"]
    i_zed_camera["i_zed_camera"] --> zed_camera["zed_camera"]
    threaded_component["threaded_component"] --> floor_detector["floor_detector"]
    threaded_component["threaded_component"] --> obstacle_detector["obstacle_detector"]
    threaded_component["threaded_component"] --> obstacle_detector_preview["obstacle_detector_preview"]
    threaded_component["threaded_component"] --> zed_camera["zed_camera"]
    threaded_component["threaded_component"] --> zed_camera_preview["zed_camera_preview"]
```

## Inheritance Hierarchy

### Base Hierarchy

- [`i_threaded_component`](i_threaded_component.md)
  - [`i_updatable_component`](i_updatable_component.md)
    - [`i_component`](i_component.md)

### Derived Hierarchy

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

## API

### Public Methods
#### Begin

```cpp
virtual void begin() = 0;
```
Starts the component thread.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### End

```cpp
virtual void end() = 0;
```
Stops the component thread and waits for it to finish.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Cancel Begin

```cpp
virtual void cancel_begin() = 0;
```
Cancels a pending begin operation.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Get Update Rate

```cpp
[[nodiscard]] virtual float get_update_rate() const noexcept = 0;
```
Returns the update rate.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Set Update Rate

```cpp
virtual void set_update_rate(float update_rate) = 0;
```
Sets the update rate.

##### Parameters
- `update_rate`: The update rate.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Get Is Running

```cpp
[[nodiscard]] virtual bool get_is_running() const noexcept = 0;
```
Returns whether the component is running.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Get Mutex

```cpp
[[nodiscard]] virtual std::mutex &get_mutex() = 0;
```
Returns the mutex.

!!! note
    Pure virtual method, must be implemented by derived classes.

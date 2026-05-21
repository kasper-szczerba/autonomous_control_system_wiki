`Interface`

# Component

- **Interface**: `i_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/interfaces/i_component.h"`

## Overview

Base interface for all components. Defines the setup/teardown lifecycle and name accessors that every component must implement.

## Inheritance Diagram

### Base Diagram

```mermaid
graph TD
    i_component["i_component"]
```

### Derived Diagram

```mermaid
graph TD
    i_component["i_component"]
    component["Component"] --> updatable_component["Updatable Component"]
    component["Component"] --> zenoh_client["Zenoh Client"]
    i_component["i_component"] --> component["Component"]
    i_component["i_component"] --> i_updatable_component["i_updatable_component"]
    i_component["i_component"] --> i_zenoh_client["i_zenoh_client"]
    i_floor_detector["i_floor_detector"] --> floor_detector["Floor Detector"]
    i_obstacle_detector["i_obstacle_detector"] --> obstacle_detector["Obstacle Detector"]
    i_threaded_component["i_threaded_component"] --> i_floor_detector["i_floor_detector"]
    i_threaded_component["i_threaded_component"] --> i_obstacle_detector["i_obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_zed_camera["i_zed_camera"]
    i_threaded_component["i_threaded_component"] --> threaded_component["Threaded Component"]
    i_updatable_component["i_updatable_component"] --> i_threaded_component["i_threaded_component"]
    i_updatable_component["i_updatable_component"] --> updatable_component["Updatable Component"]
    i_zed_camera["i_zed_camera"] --> zed_camera["ZED Camera"]
    i_zenoh_client["i_zenoh_client"] --> zenoh_client["Zenoh Client"]
    threaded_component["Threaded Component"] --> floor_detector["Floor Detector"]
    threaded_component["Threaded Component"] --> obstacle_detector["Obstacle Detector"]
    threaded_component["Threaded Component"] --> obstacle_detector_preview["Obstacle Detector Preview"]
    threaded_component["Threaded Component"] --> zed_camera["ZED Camera"]
    threaded_component["Threaded Component"] --> zed_camera_preview["ZED Camera Preview"]
    updatable_component["Updatable Component"] --> threaded_component["Threaded Component"]
```

## Inheritance Hierarchy

### Derived Hierarchy

- [`i_component`](i_component.md)
  - [`Component`](../implementation/component.md)
    - [`Updatable Component`](../implementation/updatable_component.md)
      - [`Threaded Component`](../implementation/threaded_component.md)
        - [`Floor Detector`](../../vision/implementation/detection/floor_detector.md)
        - [`Obstacle Detector`](../../vision/implementation/detection/obstacle_detector.md)
        - [`Obstacle Detector Preview`](../../vision/implementation/previews/obstacle_detector_preview.md)
        - [`ZED Camera`](../../vision/implementation/zed_camera.md)
        - [`ZED Camera Preview`](../../vision/implementation/previews/zed_camera_preview.md)
    - [`Zenoh Client`](../../utility/implementation/zenoh_client.md)
  - [`i_updatable_component`](i_updatable_component.md)
    - [`i_threaded_component`](i_threaded_component.md)
      - [`i_floor_detector`](../../vision/interfaces/detection/i_floor_detector.md)
        - [`Floor Detector`](../../vision/implementation/detection/floor_detector.md)
      - [`i_obstacle_detector`](../../vision/interfaces/detection/i_obstacle_detector.md)
        - [`Obstacle Detector`](../../vision/implementation/detection/obstacle_detector.md)
      - [`i_zed_camera`](../../vision/interfaces/i_zed_camera.md)
        - [`ZED Camera`](../../vision/implementation/zed_camera.md)
      - [`Threaded Component`](../implementation/threaded_component.md)
        - [`Floor Detector`](../../vision/implementation/detection/floor_detector.md)
        - [`Obstacle Detector`](../../vision/implementation/detection/obstacle_detector.md)
        - [`Obstacle Detector Preview`](../../vision/implementation/previews/obstacle_detector_preview.md)
        - [`ZED Camera`](../../vision/implementation/zed_camera.md)
        - [`ZED Camera Preview`](../../vision/implementation/previews/zed_camera_preview.md)
    - [`Updatable Component`](../implementation/updatable_component.md)
      - [`Threaded Component`](../implementation/threaded_component.md)
        - [`Floor Detector`](../../vision/implementation/detection/floor_detector.md)
        - [`Obstacle Detector`](../../vision/implementation/detection/obstacle_detector.md)
        - [`Obstacle Detector Preview`](../../vision/implementation/previews/obstacle_detector_preview.md)
        - [`ZED Camera`](../../vision/implementation/zed_camera.md)
        - [`ZED Camera Preview`](../../vision/implementation/previews/zed_camera_preview.md)
  - [`i_zenoh_client`](../../utility/interfaces/i_zenoh_client.md)
    - [`Zenoh Client`](../../utility/implementation/zenoh_client.md)

## API

### Public Methods
#### Setup

```cpp
virtual void setup() = 0;
```
Initializes the component.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Teardown

```cpp
virtual void teardown() = 0;
```
Cleans up the component before destruction.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Get Name

```cpp
[[nodiscard]] virtual std::string_view get_name() const noexcept = 0;
```
Returns the name.

!!! note
    Pure virtual method, must be implemented by derived classes.
#### Get Is Setup Completed

```cpp
[[nodiscard]] virtual bool get_is_setup_completed() const noexcept = 0;
```
Returns whether the setup process has been completed.

!!! note
    Pure virtual method, must be implemented by derived classes.

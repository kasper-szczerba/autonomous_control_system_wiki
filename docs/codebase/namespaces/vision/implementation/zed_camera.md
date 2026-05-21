# ZED Camera

- **Class**: `zed_camera`
- **Namespace**: `acs::vision`
- **Include**: `#include "vision/implementation/zed_camera.h"`

## Overview

Concrete ZED camera component for the vision pipeline. Extends [`threaded_component`](../../core/implementation/threaded_component.md) and implements [`i_zed_camera`](../interfaces/i_zed_camera.md), managing camera setup, frame acquisition, and teardown.

## Inheritance Diagram

### Base Diagram

```mermaid
graph TD
    zed_camera["ZED Camera"]
    component["Component"] --> i_component["i_component"]
    i_threaded_component["i_threaded_component"] --> i_updatable_component["i_updatable_component"]
    i_updatable_component["i_updatable_component"] --> i_component["i_component"]
    i_zed_camera["i_zed_camera"] --> i_threaded_component["i_threaded_component"]
    threaded_component["Threaded Component"] --> i_threaded_component["i_threaded_component"]
    threaded_component["Threaded Component"] --> updatable_component["Updatable Component"]
    updatable_component["Updatable Component"] --> component["Component"]
    updatable_component["Updatable Component"] --> i_updatable_component["i_updatable_component"]
    zed_camera["ZED Camera"] --> i_zed_camera["i_zed_camera"]
    zed_camera["ZED Camera"] --> threaded_component["Threaded Component"]
```

### Derived Diagram

```mermaid
graph TD
    zed_camera["ZED Camera"]
```

## Inheritance Hierarchy

### Base Hierarchy

- [`ZED Camera`](zed_camera.md)
  - [`i_zed_camera`](../interfaces/i_zed_camera.md)
    - [`i_threaded_component`](../../core/interfaces/i_threaded_component.md)
      - [`i_updatable_component`](../../core/interfaces/i_updatable_component.md)
        - [`i_component`](../../core/interfaces/i_component.md)
  - [`Threaded Component`](../../core/implementation/threaded_component.md)
    - [`i_threaded_component`](../../core/interfaces/i_threaded_component.md)
      - [`i_updatable_component`](../../core/interfaces/i_updatable_component.md)
        - [`i_component`](../../core/interfaces/i_component.md)
    - [`Updatable Component`](../../core/implementation/updatable_component.md)
      - [`Component`](../../core/implementation/component.md)
        - [`i_component`](../../core/interfaces/i_component.md)
      - [`i_updatable_component`](../../core/interfaces/i_updatable_component.md)
        - [`i_component`](../../core/interfaces/i_component.md)

## API

### Constructors
#### Constructor

```cpp
explicit zed_camera(std::string_view name, std::shared_ptr<utility::i_toml_reader> toml_reader_ptr);
```
Creates a zed camera with the specified name.

##### Parameters
- `name`: The name of the component.
- `toml_reader_ptr`: A shared pointer to a TOML reader for configuration.

### Public Methods

#### Implementations
- [`i_zed_camera`](../interfaces/i_zed_camera.md)
    - [`get_color_frame`](../interfaces/i_zed_camera.md#get-color-frame)
    - [`get_depth_frame`](../interfaces/i_zed_camera.md#get-depth-frame)
    - [`get_fps`](../interfaces/i_zed_camera.md#get-fps)
    - [`get_dropped_frames_count`](../interfaces/i_zed_camera.md#get-dropped-frames-count)
    - [`get_is_opened`](../interfaces/i_zed_camera.md#get-is-opened)
    - [`get_native_camera_ref`](../interfaces/i_zed_camera.md#get-native-camera-reference)

### Protected Methods
#### On Setup

```cpp
void on_setup() override;
```
Initializes the ZED camera hardware and runtime parameters.
#### On Update

```cpp
void on_update() override;
```
Captures frames from the camera and updates internal matrices.
#### On Teardown

```cpp
void on_teardown() override;
```
Closes the ZED camera and releases resources.

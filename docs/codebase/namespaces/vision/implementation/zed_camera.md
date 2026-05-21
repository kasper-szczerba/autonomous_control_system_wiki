# ZED Camera

- Class: `zed_camera`
- Namespace: `acs::vision`
- Include: `#include "vision/implementation/zed_camera.h"`

## Overview

Concrete ZED camera component for the vision pipeline. This class extends [`threaded_component`](../../core/implementation/threaded_component.md) and implements [`i_zed_camera`](../interfaces/i_zed_camera.md), managing camera setup, frame acquisition, and teardown.

## API

### Constructors

#### Constructor

```cpp
explicit zed_camera(std::string_view name, std::shared_ptr<utility::i_toml_reader> toml_reader_ptr);
```
Creates a ZED camera component with the specified name.

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


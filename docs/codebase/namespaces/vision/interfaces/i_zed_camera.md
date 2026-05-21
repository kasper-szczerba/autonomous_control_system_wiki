`Interface`

# ZED Camera

- **Interface**: `i_zed_camera`
- **Namespace**: `acs::vision`
- **Include**: `#include "vision/interfaces/i_zed_camera.h"`

## Overview

Interface for ZED camera access in the vision subsystem. This interface extends [`i_threaded_component`](../../core/interfaces/i_threaded_component.md) and defines methods for frame retrieval, runtime metrics, and access to the native camera handle.

## API

### Public Methods

#### Get Color Frame

```cpp
virtual cv::cuda::GpuMat get_color_frame() = 0;
```
Returns the latest color frame on the GPU.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Depth Frame

```cpp
virtual cv::cuda::GpuMat get_depth_frame() = 0;
```
Returns the latest depth frame on the GPU.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get FPS

```cpp
virtual float get_fps() = 0;
```
Returns the current camera capture frame rate.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Dropped Frames Count

```cpp
virtual uint32_t get_dropped_frames_count() = 0;
```
Returns the number of dropped frames reported by the camera.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Is Opened

```cpp
virtual bool get_is_opened() = 0;
```
Returns whether the camera is currently opened.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Native Camera Reference

```cpp
virtual sl::Camera& get_native_camera_ref() = 0;
```
Returns a mutable reference to the underlying ZED SDK camera object.

!!! note
    Pure virtual method, must be implemented by derived classes.

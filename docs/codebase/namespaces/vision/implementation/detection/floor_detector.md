# Floor Detector

- Class: `floor_detector`
- Namespace: `acs::vision`
- Include: `#include "vision/implementation/detection/floor_detector.h"`

## Overview

Threaded component that estimates the floor plane from ZED camera data. This class extends [`threaded_component`](../../../core/implementation/threaded_component.md), tracking whether a floor was found and exposing both the detected plane and its equation.

## API

### Constructors

#### Constructor

```cpp
explicit floor_detector(std::string_view name,
                        std::shared_ptr<utility::toml_reader> toml_reader_ptr,
                        std::shared_ptr<i_zed_camera> camera_ptr);
```
Creates a floor detector bound to a ZED camera interface.

##### Parameters
- `name`: The name of the component.
- `toml_reader_ptr`: A shared pointer to a TOML reader for configuration.
- `camera_ptr`: Shared pointer to the camera source.

### Public Methods

#### Get Detected Floor Plane

```cpp
sl::Plane get_detected_floor_plane();
```
Returns the currently detected floor plane object.

#### Get Plane Equation

```cpp
sl::float4 get_plane_equation();
```
Returns the current plane equation coefficients.

#### Get Is Floor Detected

```cpp
bool get_is_floor_detected();
```
Returns whether floor detection has succeeded.

### Protected Methods

#### On Setup

```cpp
void on_setup() override;
```
Initializes floor detection parameters from configuration.

#### On Update

```cpp
void on_update() override;
```
Performs floor plane detection using depth data from the camera.


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
                        std::shared_ptr<utility::i_toml_reader> toml_reader_ptr,
                        std::shared_ptr<i_zed_camera> camera_ptr);
```
Creates a floor detector bound to a ZED camera interface.

##### Parameters
- `name`: The name of the component.
- `toml_reader_ptr`: A shared pointer to a TOML reader for configuration.
- `camera_ptr`: Shared pointer to the camera source.

### Public Methods

#### Implementations
- [`i_floor_detector`](../../interfaces/detection/i_floor_detector.md)
    - [`get_detected_floor_plane`](../../interfaces/detection/i_floor_detector.md#get-detected-floor-plane)
    - [`get_plane_equation`](../../interfaces/detection/i_floor_detector.md#get-plane-equation)
    - [`get_is_floor_detected`](../../interfaces/detection/i_floor_detector.md#get-is-floor-detected)

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


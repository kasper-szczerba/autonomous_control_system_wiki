`Interface`

# Floor Detector

- **Interface**: `i_floor_detector`
- **Namespace**: `acs::vision`
- **Include**: `#include "vision/interfaces/detection/i_floor_detector.h"`

## Overview

Interface for floor detection in the vision subsystem. This interface extends [`i_threaded_component`](../../../core/interfaces/i_threaded_component.md) and defines methods for retrieving the detected floor plane, its equation coefficients, and whether detection has succeeded.

## API

### Public Methods

#### Get Detected Floor Plane

```cpp
virtual sl::Plane get_detected_floor_plane() = 0;
```
Returns the currently detected floor plane object.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Plane Equation

```cpp
virtual sl::float4 get_plane_equation() = 0;
```
Returns the current plane equation coefficients.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Is Floor Detected

```cpp
virtual bool get_is_floor_detected() = 0;
```
Returns whether floor detection has succeeded.

!!! note
    Pure virtual method, must be implemented by derived classes.

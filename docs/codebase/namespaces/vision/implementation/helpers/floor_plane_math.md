# Floor Plane Math Helpers

- **Namespace**: `acs::vision::floor_plane_math`
- **Include**: `#include "vision/implementation/helpers/floor_plane_math.h"`

## Overview

Mathematical helper utilities for floor-plane calculations in 3D space. Provides lightweight data structures and functions for plane orientation, normal metrics, pixel re-projection, and point-to-plane distance.

## API

### Public Structs
#### Plane Coefficients

```cpp
struct plane_coefficients {
    float a;
    float b;
    float c;
    float d;
  }
```
Represents the coefficients of a plane equation `ax + by + cz + d = 0`.
- `a` (`float`): Coefficient for the x component.
- `b` (`float`): Coefficient for the y component.
- `c` (`float`): Coefficient for the z component.
- `d` (`float`): The constant (offset) term.
#### Point3

```cpp
struct point3 {
    float x;
    float y;
    float z;
  }
```
Represents a 3D point in Cartesian coordinates.
- `x` (`float`): X-axis coordinate.
- `y` (`float`): Y-axis coordinate.
- `z` (`float`): Z-axis coordinate.

### Public Functions
#### Orient Plane Up

```cpp
[[nodiscard]] plane_coefficients orient_plane_up(const sl::float4& equation);
```
Normalises the plane orientation so the normal vector points upward.

##### Parameters
- `equation`: The raw plane equation from the ZED SDK (`sl::float4`).
#### Normal Length

```cpp
[[nodiscard]] float normal_length(const plane_coefficients& coefficients);
```
Computes the length of the plane normal vector.

##### Parameters
- `coefficients`: The plane coefficients to compute the normal length for.
#### Reproject Depth Pixel

```cpp
[[nodiscard]] point3 reproject_depth_pixel(int x, int y, float z, float fx, float fy, float cx, float cy);
```
Reprojects a depth pixel into 3D camera space using intrinsic parameters.

##### Parameters
- `x`: Pixel x-coordinate.
- `y`: Pixel y-coordinate.
- `z`: Depth value at the pixel.
- `fx`: Focal length in x.
- `fy`: Focal length in y.
- `cx`: Principal point x-coordinate.
- `cy`: Principal point y-coordinate.
#### Absolute Distance To Plane

```cpp
[[nodiscard]] float absolute_distance_to_plane(const point3& point, const plane_coefficients& plane, float plane_normal_length);
```
Computes the absolute perpendicular distance from a 3D point to a plane.

##### Parameters
- `point`: The point in 3D space.
- `plane`: The plane coefficients.
- `plane_normal_length`: Precomputed normal length for the plane.

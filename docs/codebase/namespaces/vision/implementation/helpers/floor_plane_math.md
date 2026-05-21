# Floor Plane Math Helpers

- **Namespace**: `acs::vision::floor_plane_math`
- **Include**: `#include "vision/implementation/helpers/floor_plane_math.h"`

## Overview

Mathematical helper utilities for floor-plane calculations in 3D space. This namespace contains lightweight data structures and functions for plane orientation, normal metrics, pixel re-projection, and point-to-plane distance.

## API

### Public Structs

#### plane_coefficients

```cpp
struct plane_coefficients {
  float a;
  float b;
  float c;
  float d;
};
```
Represents the coefficients of a plane equation.

#### point3

```cpp
struct point3 {
  float x;
  float y;
  float z;
};
```
Represents a 3D point in Cartesian coordinates.

### Public Functions

#### Orient Plane Up

```cpp
plane_coefficients orient_plane_up(const sl::float4& equation);
```
Normalizes plane orientation to point upward.

#### Normal Length

```cpp
float normal_length(const plane_coefficients& coefficients);
```
Computes the length of the plane normal vector.

#### Reproject Depth Pixel

```cpp
point3 reproject_depth_pixel(int x, int y, float z, float fx, float fy, float cx, float cy);
```
Reprojects a depth pixel into 3D camera space.

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
float absolute_distance_to_plane(const point3& point, const plane_coefficients& plane, float plane_normal_length);
```
Computes the absolute distance from a 3D point to a plane.

##### Parameters
- `point`: The point in 3D space.
- `plane`: Plane coefficients.
- `plane_normal_length`: Precomputed normal length for the plane.

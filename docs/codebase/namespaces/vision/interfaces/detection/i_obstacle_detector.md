`Interface`

# Obstacle Detector

- **Interface**: `i_obstacle_detector`
- **Namespace**: `acs::vision`
- **Include**: `#include "vision/interfaces/detection/i_obstacle_detector.h"`

## Overview

Interface for obstacle detection in the vision subsystem. This interface extends [`i_threaded_component`](../../../core/interfaces/i_threaded_component.md) and defines methods for accessing detection thresholds, contour data, bounding boxes, and the linked floor detector.

## API

### Public Methods

#### Get Floor Detector Pointer

```cpp
virtual std::shared_ptr<i_floor_detector> get_floor_detector_ptr() = 0;
```
Returns the linked floor detector.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Obstacle Min Range Meters

```cpp
virtual float get_obstacle_min_range_meters() const = 0;
```
Returns the minimum depth range considered for obstacle detection.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Obstacle Max Range Meters

```cpp
virtual float get_obstacle_max_range_meters() const = 0;
```
Returns the maximum depth range considered for obstacle detection.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Obstacle Height Threshold Meters

```cpp
virtual float get_obstacle_height_threshold_meters() const = 0;
```
Returns the height threshold used to classify obstacles.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Contours

```cpp
virtual std::vector<std::vector<cv::Point>>& get_contours() = 0;
```
Returns the detected obstacle contours.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Union Box

```cpp
virtual cv::Rect& get_union_box() = 0;
```
Returns the combined bounding box for all detected obstacles.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Individual Boxes

```cpp
virtual std::vector<cv::Rect>& get_individual_boxes() = 0;
```
Returns individual obstacle bounding boxes.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Last Crop

```cpp
virtual cv::Mat& get_last_crop() = 0;
```
Returns the latest cropped image region corresponding to the union box.

!!! note
    Pure virtual method, must be implemented by derived classes.

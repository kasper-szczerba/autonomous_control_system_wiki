# Obstacle Detector

- Class: `obstacle_detector`
- Namespace: `acs::vision`
- Include: `#include "vision/implementation/detection/obstacle_detector.h"`

## Overview

Threaded component that detects obstacles using depth data and floor geometry. This class extends [`threaded_component`](../../../core/implementation/threaded_component.md), exposing thresholds, contour data, and both union and per-object bounding boxes for downstream processing or visualization.

## API

### Constructors

#### Constructor

```cpp
obstacle_detector(std::string_view name, std::shared_ptr<i_zed_camera> camera, std::shared_ptr<floor_detector> floor_detector_ptr);
```
Creates an obstacle detector with camera and floor detector dependencies.

##### Parameters
- `name`: The name of the component.
- `camera`: Shared pointer to the camera source.
- `floor_detector_ptr`: Shared pointer to the floor detector.

### Public Methods

#### Get Floor Detector Pointer

```cpp
std::shared_ptr<floor_detector> get_floor_detector_ptr();
```
Returns the linked floor detector.

#### Get Obstacle Min Range Meters

```cpp
float get_obstacle_min_range_meters() const;
```
Returns the minimum depth range considered for obstacle detection.

#### Get Obstacle Max Range Meters

```cpp
float get_obstacle_max_range_meters() const;
```
Returns the maximum depth range considered for obstacle detection.

#### Get Obstacle Height Threshold Meters

```cpp
float get_obstacle_height_threshold_meters() const;
```
Returns the height threshold used to classify obstacles.

#### Get Contours

```cpp
std::vector<std::vector<cv::Point>>& get_contours();
```
Returns the detected obstacle contours.

#### Get Union Box

```cpp
cv::Rect& get_union_box();
```
Returns the combined bounding box for all detected obstacles.

#### Get Individual Boxes

```cpp
std::vector<cv::Rect>& get_individual_boxes();
```
Returns individual obstacle bounding boxes.

#### Get Last Crop

```cpp
cv::Mat& get_last_crop();
```
Returns the latest cropped image region corresponding to the union box.

### Protected Methods

#### On Setup

```cpp
void on_setup() override;
```
Initializes obstacle detection thresholds and parameters from configuration.

#### On Update

```cpp
void on_update() override;
```
Performs obstacle detection using depth data and floor plane information.


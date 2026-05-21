# Vision Namespace

## Overview

The `acs::vision` namespace contains components for camera access, scene understanding, and visualization. It implements the detection pipeline for obstacles using ZED stereo camera hardware.

## Inheritance Hierarchy

```mermaid
graph LR
    threaded["core::threaded_component"]
    i_zed["i_zed_camera"]
    zed["zed_camera"]
    floor["floor_detector"]
    obstacle["obstacle_detector"]
    camera_prev["zed_camera_preview"]
    obstacle_prev["obstacle_detector_preview"]
    
    threaded --> zed
    i_zed --> zed
    threaded --> floor
    threaded --> obstacle
    threaded --> camera_prev
    threaded --> obstacle_prev
```

## Vision Pipeline Graph

```mermaid
graph TD
    zed["ZED Camera"]
    floor["Floor Detector"]
    obstacle["Obstacle Detector"]
    camera_preview["Camera Preview"]
    obstacle_preview["Obstacle Preview"]
    
    zed -->|Frames| floor
    floor -->|Plane Data| obstacle
    zed -->|Display| camera_preview
    obstacle -->|Contours| obstacle_preview
```

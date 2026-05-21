# Namespaces

This page indexes the generated namespace documentation and the project-wide inheritance graph.

## Namespace Pages

- [Core](core/index.md)
- [Utility](utility/index.md)
- [Vision](vision/index.md)

## Inheritance Graph

```mermaid
graph TD
    component["Component"] --> updatable_component["Updatable Component"]
    component["Component"] --> zenoh_client["Zenoh Client"]
    i_component["i_component"] --> component["Component"]
    i_component["i_component"] --> i_updatable_component["i_updatable_component"]
    i_component["i_component"] --> i_zenoh_client["i_zenoh_client"]
    i_floor_detector["i_floor_detector"] --> floor_detector["Floor Detector"]
    i_obstacle_detector["i_obstacle_detector"] --> obstacle_detector["Obstacle Detector"]
    i_threaded_component["i_threaded_component"] --> i_floor_detector["i_floor_detector"]
    i_threaded_component["i_threaded_component"] --> i_obstacle_detector["i_obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_zed_camera["i_zed_camera"]
    i_threaded_component["i_threaded_component"] --> threaded_component["Threaded Component"]
    i_toml_reader["i_toml_reader"] --> toml_reader["TOML Reader"]
    i_updatable_component["i_updatable_component"] --> i_threaded_component["i_threaded_component"]
    i_updatable_component["i_updatable_component"] --> updatable_component["Updatable Component"]
    i_zed_camera["i_zed_camera"] --> zed_camera["ZED Camera"]
    i_zenoh_client["i_zenoh_client"] --> zenoh_client["Zenoh Client"]
    threaded_component["Threaded Component"] --> floor_detector["Floor Detector"]
    threaded_component["Threaded Component"] --> obstacle_detector["Obstacle Detector"]
    threaded_component["Threaded Component"] --> obstacle_detector_preview["Obstacle Detector Preview"]
    threaded_component["Threaded Component"] --> zed_camera["ZED Camera"]
    threaded_component["Threaded Component"] --> zed_camera_preview["ZED Camera Preview"]
    updatable_component["Updatable Component"] --> threaded_component["Threaded Component"]
```

# Namespaces

This page indexes the generated namespace documentation and the project-wide inheritance graph.

## Namespace Pages

- [Core](core/index.md)
- [Utility](utility/index.md)
- [Vision](vision/index.md)

## Inheritance Graph

```mermaid
graph TD
    component["component"] --> updatable_component["updatable_component"]
    component["component"] --> zenoh_client["zenoh_client"]
    i_component["i_component"] --> component["component"]
    i_component["i_component"] --> i_updatable_component["i_updatable_component"]
    i_component["i_component"] --> i_zenoh_client["i_zenoh_client"]
    i_floor_detector["i_floor_detector"] --> floor_detector["floor_detector"]
    i_obstacle_detector["i_obstacle_detector"] --> obstacle_detector["obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_floor_detector["i_floor_detector"]
    i_threaded_component["i_threaded_component"] --> i_obstacle_detector["i_obstacle_detector"]
    i_threaded_component["i_threaded_component"] --> i_zed_camera["i_zed_camera"]
    i_threaded_component["i_threaded_component"] --> threaded_component["threaded_component"]
    i_toml_reader["i_toml_reader"] --> toml_reader["toml_reader"]
    i_updatable_component["i_updatable_component"] --> i_threaded_component["i_threaded_component"]
    i_updatable_component["i_updatable_component"] --> updatable_component["updatable_component"]
    i_zed_camera["i_zed_camera"] --> zed_camera["zed_camera"]
    i_zenoh_client["i_zenoh_client"] --> zenoh_client["zenoh_client"]
    threaded_component["threaded_component"] --> floor_detector["floor_detector"]
    threaded_component["threaded_component"] --> obstacle_detector["obstacle_detector"]
    threaded_component["threaded_component"] --> obstacle_detector_preview["obstacle_detector_preview"]
    threaded_component["threaded_component"] --> zed_camera["zed_camera"]
    threaded_component["threaded_component"] --> zed_camera_preview["zed_camera_preview"]
    updatable_component["updatable_component"] --> threaded_component["threaded_component"]
```

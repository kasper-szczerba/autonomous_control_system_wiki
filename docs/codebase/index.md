# Codebase Overview

## System Architecture

The Autonomous Control System is organized into three main namespaces, each providing distinct functionality.

See the generated [Namespace Index](namespaces/index.md) for the inheritance hierarchy and namespace-level documentation map.

```mermaid
graph LR
    subgraph core["Core"]
        component["Component"]
        updatable["Updatable Component"]
        threaded["Threaded Component"]

        component -->|Extended by| updatable
        updatable -->|Extended by| threaded
    end

    subgraph utility["Utility"]
        toml["Toml Reader"]
        zenoh["Zenoh Client"]
    end

    subgraph vision["Vision"]
        zed["ZED Camera"]
        floor["Floor Detector"]
        obstacle["Obstacle Detector"]
        previews["Preview Components"]

        zed -->|Feeds data to| floor
        floor -->|Feeds data to| obstacle
        obstacle -->|Feeds data to| previews
        zed -->|Feeds data to| previews
    end

    core -->|Base for| vision
    toml -->|Loads config for| vision
```

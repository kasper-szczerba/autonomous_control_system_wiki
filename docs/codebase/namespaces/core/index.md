# Core Namespace

## Overview

The `acs::core` namespace provides the foundational component system for the autonomous control system. It defines interfaces and base classes for managing component lifecycles, updates, and threaded execution.

## Inheritance Hierarchy

```mermaid
graph TD
    i_component["i_component"]
    i_updatable["i_updatable_component"]
    i_threaded["i_threaded_component"]
    component["component"]
    updatable["updatable_component"]
    threaded["threaded_component"]
    
    i_component --> component
    i_component --> i_updatable
    i_updatable --> updatable
    i_updatable --> i_threaded
    component --> updatable
    updatable --> threaded
    i_threaded --> threaded
```

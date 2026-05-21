`Interface`

# Component

- **Interface**: `i_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/interfaces/i_component.h"`

## Overview

Interface for most components in the system. This interface defines the basic structure and functionality that all components must implement, including setup and teardown methods, as well as methods to retrieve the component's name and setup status.

## API

### Public Methods

#### Setup

```cpp
virtual void setup() = 0;
```
Called to initialize the component. This is where you would set up any necessary parameters from the configuration-file.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Teardown

```cpp
virtual void teardown() = 0;
```
Called to clean up the component before it is destroyed. This is where you would release any resources or perform any necessary cleanup.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Name

```cpp
virtual std::string_view get_name() const noexcept = 0;
```
Returns the name of the component.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Is Setup Completed

```cpp
virtual bool get_is_setup_completed() const noexcept = 0;
```
Returns whether the setup process has been completed for the component.

!!! note
    Pure virtual method, must be implemented by derived classes.

`Interface`

# Threaded Component

- **Interface**: `i_threaded_component`
- **Namespace**: `acs::core`
- **Include**: `#include "core/interfaces/i_threaded_component.h"`

## Overview

Interface for updatable components that run in a dedicated thread. This interface extends [`i_updatable_component`](i_updatable_component.md) with lifecycle controls for threaded execution, runtime update-rate control, and synchronization access.

## API

### Public Methods

#### Begin

```cpp
virtual void begin() = 0;
```
Starts the threaded execution loop.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### End

```cpp
virtual void end() = 0;
```
Stops the threaded execution loop.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Cancel Begin

```cpp
virtual void cancel_begin() = 0;
```
Cancels a pending thread start.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Update Rate

```cpp
virtual float get_update_rate() const = 0;
```
Returns the update rate in hertz.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Set Update Rate

```cpp
virtual void set_update_rate(float update_rate) = 0;
```
Sets the update rate in hertz.

!!! note
    Pure virtual method, must be implemented by derived classes.

##### Parameters
- `update_rate`: Desired update frequency.

#### Get Is Running

```cpp
virtual bool get_is_running() const = 0;
```
Returns whether the threaded loop is currently running.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Mutex

```cpp
virtual std::mutex& get_mutex() = 0;
```
Returns a mutex reference used for thread-safe synchronization.

!!! note
    Pure virtual method, must be implemented by derived classes.

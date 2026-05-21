`Interface`

# Zenoh Client

- **Interface**: `i_zenoh_client`
- **Namespace**: `acs::utility`
- **Include**: `#include "utility/interfaces/i_zenoh_client.hpp"`

## Overview

Interface for managing a Zenoh session and its configuration. It defines methods for configuring the router address and port, and accessing the active session and configuration objects.

## API

### Public Methods

#### Get Address

```cpp
[[nodiscard]] virtual std::string_view get_address() const = 0;
```
Returns the configured router address.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Set Address

```cpp
virtual void set_address(std::string_view address) = 0;
```
Sets the router address.

!!! note
    Pure virtual method, must be implemented by derived classes.

##### Parameters
- `address`: The router address.

#### Get Port

```cpp
[[nodiscard]] virtual int get_port() const = 0;
```
Returns the configured router port.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Set Port

```cpp
virtual void set_port(int port) = 0;
```
Sets the router port.

!!! note
    Pure virtual method, must be implemented by derived classes.

##### Parameters
- `port`: The router port number.

#### Get Session Pointer

```cpp
[[nodiscard]] virtual zenoh::Session *get_session_ptr() = 0;
```
Returns a pointer to the active Zenoh session.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Config Pointer

```cpp
[[nodiscard]] virtual zenoh::Config *get_config_ptr() const = 0;
```
Returns a pointer to the Zenoh configuration object.

!!! note
    Pure virtual method, must be implemented by derived classes.

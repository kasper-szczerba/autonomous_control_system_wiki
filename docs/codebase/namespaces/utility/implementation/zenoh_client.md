# Zenoh Client

- Class: `zenoh_client`
- Namespace: `acs::utility`
- Include: `#include "utility/classes/zenoh_client.hpp"`

## Overview

Concrete Zenoh communication component. This class extends [`component`](../../core/implementation/component.md) and implements [`i_zenoh_client`](../interfaces/i_zenoh_client.md), managing the Zenoh session lifecycle and router configuration.

## API

### Constructors

#### Constructor

```cpp
zenoh_client(std::string_view name, std::string_view address, int port);
```
Creates a Zenoh client with the specified router address and port.

##### Parameters
- `name`: The name of the component.
- `address`: The router address to connect to.
- `port`: The router port to connect to.

### Public Methods

#### Implementations
- [`i_zenoh_client`](../interfaces/i_zenoh_client.md)
    - [`get_address`](../interfaces/i_zenoh_client.md#get-address)
    - [`set_address`](../interfaces/i_zenoh_client.md#set-address)
    - [`get_port`](../interfaces/i_zenoh_client.md#get-port)
    - [`set_port`](../interfaces/i_zenoh_client.md#set-port)
    - [`get_session_ptr`](../interfaces/i_zenoh_client.md#get-session-pointer)
    - [`get_config_ptr`](../interfaces/i_zenoh_client.md#get-config-pointer)

### Protected Methods

#### On Initialize

```cpp
void on_initialize() override;
```
Opens the Zenoh session using the configured address and port.

#### On Shutdown

```cpp
void on_shutdown() override;
```
Closes the Zenoh session and releases resources.

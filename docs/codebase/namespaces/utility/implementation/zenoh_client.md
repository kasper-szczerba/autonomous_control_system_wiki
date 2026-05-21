# Zenoh Client

- **Class**: `zenoh_client`
- **Namespace**: `acs::utility`
- **Include**: `#include "utility/implementation/zenoh_client.h"`

## Overview

Concrete implementation of `i_zenoh_client`.

## Inheritance Diagram

### Base Diagram

```mermaid
graph TD
    zenoh_client["zenoh_client"]
    component["component"] --> i_component["i_component"]
    i_zenoh_client["i_zenoh_client"] --> i_component["i_component"]
    zenoh_client["zenoh_client"] --> component["component"]
    zenoh_client["zenoh_client"] --> i_zenoh_client["i_zenoh_client"]
```

### Derived Diagram

```mermaid
graph TD
    zenoh_client["zenoh_client"]
```

## Inheritance Hierarchy

### Base Hierarchy

- [`zenoh_client`](zenoh_client.md)
  - [`component`](../../core/implementation/component.md)
    - [`i_component`](../../core/interfaces/i_component.md)
  - [`i_zenoh_client`](../interfaces/i_zenoh_client.md)
    - [`i_component`](../../core/interfaces/i_component.md)

## API

### Constructors
#### Constructor

```cpp
zenoh_client(std::string_view name, std::shared_ptr<utility::i_toml_reader> toml_reader_ptr, std::string_view address, int port);
```
Creates a zenoh client with the specified name.

##### Parameters
- `name`: The name of the component.
- `toml_reader_ptr`: A shared pointer to a TOML reader for configuration.
- `address`: The address.
- `port`: The port.

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
#### On Setup

```cpp
void on_setup() override;
```
Called during the setup phase.
#### On Teardown

```cpp
void on_teardown() override;
```
Called during the teardown phase.

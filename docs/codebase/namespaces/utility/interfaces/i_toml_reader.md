`Interface`

# TOML Reader

- **Interface**: `i_toml_reader`
- **Namespace**: `acs::utility`
- **Include**: `#include "utility/interfaces/i_toml_reader.h"`

## Overview

Interface for reading and managing TOML configuration files. It defines parsing and cleanup lifecycle methods, path management, and access to the parsed TOML table.

## API

### Public Methods

#### Parse

```cpp
virtual void parse() = 0;
```
Parses the configured TOML file into an internal table.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Free

```cpp
virtual void free() = 0;
```
Releases the parsed data and related resources.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get File Path

```cpp
virtual std::string_view get_file_path() const = 0;
```
Returns the currently configured file path.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Set File Path

```cpp
virtual void set_file_path(std::string_view file_path) = 0;
```
Sets the path to the TOML file to parse.

!!! note
    Pure virtual method, must be implemented by derived classes.

##### Parameters
- `file_path`: The TOML file path.

#### Get Default File Path

```cpp
virtual std::string_view get_default_file_path() const = 0;
```
Returns the default TOML file path used by the implementation.

!!! note
    Pure virtual method, must be implemented by derived classes.

#### Get Table Reference

```cpp
virtual toml::table& get_table_ref() = 0;
```
Returns a mutable reference to the parsed TOML table.

!!! note
    Pure virtual method, must be implemented by derived classes.

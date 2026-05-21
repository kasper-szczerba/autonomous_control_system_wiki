# Matrix Converter

- Class: `matrix_converter`
- Namespace: `acs::vision`
- Include: `#include "vision/implementation/helpers/matrix_converter.h"`

## Overview

Utility class for converting matrix data between ZED SDK (`sl::Mat`) and OpenCV CUDA (`cv::cuda::GpuMat`) formats for both color and depth frames.

## API

### Public Methods

#### Convert Color To GPU Mat

```cpp
static cv::cuda::GpuMat convert_color_to_gpu_mat(const sl::Mat& input);
```
Converts a ZED color matrix to an OpenCV CUDA matrix.

##### Parameters
- `input`: Source matrix in ZED SDK format.

#### Convert Depth To GPU Mat

```cpp
static cv::cuda::GpuMat convert_depth_to_gpu_mat(const sl::Mat& input);
```
Converts a ZED depth matrix to an OpenCV CUDA matrix.

##### Parameters
- `input`: Source matrix in ZED SDK format.

#### Convert Color To SL Mat

```cpp
static sl::Mat convert_color_to_sl_mat(const cv::cuda::GpuMat& input);
```
Converts an OpenCV CUDA color matrix to ZED SDK format.

##### Parameters
- `input`: Source matrix in OpenCV CUDA format.

#### Convert Depth To SL Mat

```cpp
static sl::Mat convert_depth_to_sl_mat(const cv::cuda::GpuMat& input);
```
Converts an OpenCV CUDA depth matrix to ZED SDK format.

##### Parameters
- `input`: Source matrix in OpenCV CUDA format.


<!--
 * @Author       : Prologue-Z tjuzx2016@126.com
 * @Date         : 2025-04-18 16:42:11
 * @LastEditors  : Prologue-Z
 * @LastEditTime : 2025-04-18 16:48:00
 * @Description  : 
 * @Refer        : 
 * 
 * Copyright (c) 2025 by 天津大学先进机构学及机器人学中心, All Rights Reserved. 
-->


## 代码说明
此脚本用于将realsense-viewer中录制得rgb和深度图像进行拼接，并保存为视频文件。

## 使用方法
在bash中运行：
```bash
python3 bag_converter.py -i input.bag -r custom_rgb.avi -d custom_depth.avi -f 30
```

## 参数说明
- -i：输入的bag文件路径
- -r：输出的rgb视频文件路径
- -d：输出的深度视频文件路径
- -f：帧率，默认为30帧/秒
  
## 注意事项
- 请确保输入的bag文件中包含rgb和深度图像数据
- 输出的视频文件格式为avi

## 依赖安装
- 安装opencv-python库：
```bash
pip install opencv-python
```
- 安装pyrealsense2库：
```bash
pip install pyrealsense2
```
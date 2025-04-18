#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' 
 @ Author       : Prologue-Z tjuzx2016@126.com
 @ Date         : 2025-04-18 16:32:44
 @ LastEditors  : Prologue-Z
 @ LastEditTime : 2025-04-18 17:26:27
 @ Description  : 
 @ Refer        : 
 @ 
 @ Copyright (c) 2025 by 天津大学先进机构学及机器人学中心, All Rights Reserved. 
'''
import pyrealsense2 as rs
import numpy as np
import cv2
import argparse
from tqdm import tqdm

def bag_to_video(input_bag, rgb_output="rgb_output.avi", depth_output="depth_output.avi", fps=30):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device_from_file(input_bag, repeat_playback=False)
    
    try:
        # 初始化进度条
        profile = pipeline.start(config)
        device = profile.get_device().as_playback()
        duration = device.get_duration().total_seconds()
        color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
        total_frames = int(duration * color_profile.fps())
        progress_bar = tqdm(total=total_frames, unit='帧', desc='转换进度')

        # 创建视频编码器
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        rgb_writer = cv2.VideoWriter(rgb_output, fourcc, fps, 
                                    (color_profile.width(), color_profile.height()))
        depth_writer = cv2.VideoWriter(depth_output, fourcc, fps, 
                                      (color_profile.width(), color_profile.height()))

        # 创建帧对齐工具
        align = rs.align(rs.stream.color)

        while True:
            try:
                frames = pipeline.wait_for_frames(5000)
            except RuntimeError as e:
                if "Frame didn't arrive" in str(e):
                    break  # 正常结束播放
                else:
                    raise
            # 对齐深度与RGB帧
            aligned_frames = align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            
            if color_frame and depth_frame:
                # 转换帧数据
                color_image = np.asanyarray(color_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(depth_image, alpha=0.03), 
                    cv2.COLORMAP_JET
                )
                
                # 写入视频文件
                rgb_writer.write(color_image)
                depth_writer.write(depth_colormap)
                
                # 更新进度条
                progress_bar.update(1)

                # 实时预览（可选）
                # cv2.imshow('RGB Preview', color_image)
                # cv2.imshow('Depth Preview', depth_colormap)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    finally:
        # 释放资源
        pipeline.stop()
        rgb_writer.release()
        depth_writer.release()
        progress_bar.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将RealSense .bag文件转换为视频')
    parser.add_argument('-i', '--input', required=True, help='输入.bag文件路径')
    parser.add_argument('-r', '--rgb', default='rgb_output.avi', help='RGB输出视频路径')
    parser.add_argument('-d', '--depth', default='depth_output.avi', help='深度输出视频路径')
    parser.add_argument('-f', '--fps', type=int, default=30, help='输出视频帧率')
    args = parser.parse_args()

    bag_to_video(args.input, args.rgb, args.depth, args.fps)
# 一、项目信息
1. 名称：批量照片及图像文件的管理
2. 语言：python
3. 任务：
    1. 照片文件分析（文件大小、图像大小、色彩信息、拍照日期等）；
    2. 找出重复的照片文件；
    3. 照片文件重新编号；
    4. 为照片加上专属标志；
    5. 批量调整尺寸；
    6. 为图像加水印；
    7. 中文字体的处理与应用等。

# 二、项目设计

## 1. 实现细节

1. 图片格式：
    默认图片的存储格式为jpg,如果是png格式，也会标识出来

2. 库
    OpenCV：pip install opencv-python
    PIL: pip install pillow

        import cv2
        import os
        import shutil
        from PIL import Image
        import time
        import numpy as np

        #得到照片的拍摄时间
        import exifread 
        from datetime import datetime 
4. 任务细节
    1. 照片文件分析（文件大小、图像大小、色彩信息、拍照日期等）

        Opencv
        numpy
        os

    2. 找出重复的照片文件
        PIL
        numpy
        os
        （1）判断照片是否相同：
            首先比较大小，大小不同则不同；
            其次比较尺寸（长和宽）；
            最后比较内容（数组元素）numpt数组
        （2）步骤：
            第一步：遍历文件 for file in os.walk(load_path)
            第二步：文件按照image_size排序
            第三步：取出重复的文件
            第四步：将重复的文件移动到新的文件夹，实现对原文件夹的降重
    3. 照片文件重新编号；
        os
       现在的问题是，如果已经编号的文件，重新编号时，1.jpg和11.jpg,位于2.jpg之前。
    4. 为照片加上专属标志；
        图片/文字
    5. 批量调整尺寸；
        old_image.resize(size, Image.ANTIALIAS).save(save_path)
    6. 为图像加水印；
        水印
    7. 中文字体的处理与应用等。
        加的标志或者水印的字体的更改？

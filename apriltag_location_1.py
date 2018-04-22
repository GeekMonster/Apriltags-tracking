# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor, image, time, math
from pyb import UART
uart = UART(3, 115200, timeout_char = 1000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()
from pyb import UART
uart = UART(3, 115200, timeout_char = 1000)


# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.
# translation 没有单位, 所以必须添加一个转换函数

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# x,y焦距 计算方法
# f_x = (焦距 / 感光芯片纵向高度) * 纵向像素个数
# f_y = (焦距 / 感光芯片横向高度) * 横向向像素个数
# 下列值针对OV7725 摄像头 与 3.6 mm 镜头与QQVGA分辨率(160*120)
# 如果更换用其他镜头之后, 需要将3.6更新为当前镜头的焦距
f_x = (3.6 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (3.6 / 2.952) * 120 # find_apriltags defaults to this if not set
# (c_x, c_y)为画面的中心点坐标
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

# 弧度值转换为角度值的函数
def degrees(radians):
    return (180 * radians) / math.pi

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = ((tag.x_translation()+8)*20, (6-tag.y_translation())*20, -tag.z_translation()*10)
        # Translation units are unknown. Rotation units are in degrees.
        # Translation 单位是未知的, Rotaion的单位是角度
        print("x%dy%dz%d" % print_args)
        uart.write("x%dy%dz%d" % print_args+'\n')
        time.sleep(10000)
    #print(clock.fps())

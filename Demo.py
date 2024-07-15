from GHUB import *
from time import sleep

# 启动GHUB动态链接库（调用的模块开头必须写入这个代码）
gd = ghub_device()

# 以下是键盘调用
# 按下键盘Q键
gd.key_down('Q')
# 按下时间（此处为0.1秒 = 100ms）
sleep(0.1)
# 键盘抬起Q键
gd.key_up('Q')
# 按下时间（此处为0.1秒 = 100ms）
sleep(0.1)

# 以下是鼠标相对位置调用(以鼠标当前位置为基准点移动)
gd.mouse_R(100, 100)
sleep(0.1)

# 以下是鼠标绝对位置调用（以屏幕最初始的位置移动）
gd.mouse_To(1106, 805)
sleep(0.1)

# 以下是鼠标按键调用(只支持鼠标的1-2-3号键，即左键，右键，中键)
# 按下鼠标左键
gd.mouse_down(1)
# 按下时间
sleep(0.1)
# 松开鼠标按键（不填写数字，默认为1号键，即左键）
gd.mouse_up()
# 松开时间
sleep(0.1)
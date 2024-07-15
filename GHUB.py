from ctypes import CDLL, c_char_p
import os
import sys

# 创建一个临时的重定向类
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# ↓↓↓↓↓↓↓↓↓ 调用ghub键鼠驱动 ↓↓↓↓↓↓↓↓↓
class ghub_device:
    info = None

    def __init__(self):
        try:
            # 使用上下文管理器来隐藏输出
            with SuppressOutput():
                # 加载ghub_device.dll动态链接库
                self.gm = CDLL(r'./ghub_device.dll')  # ghubdlldir
                # 尝试打开设备
                self.gm_ok = self.gm.device_open()
            # 设置key_down和key_up函数的参数类型
            self.gm.key_down.argtypes = [c_char_p]
            self.gm.key_up.argtypes = [c_char_p]
            # 检查设备是否成功打开
            if not self.gm_ok:
                self.info = '未安装ghub或者lgs驱动!!!'
            else:
                self.info = '驱动初始化成功!'
        except FileNotFoundError:
            self.info = '重要键鼠文件缺失'
            self.gm_ok = 0

    def _mouse_event(self, fun, *args):
        # 通用鼠标事件处理函数
        if self.gm_ok:
            try:
                if hasattr(self.gm, fun):
                    return getattr(self.gm, fun)(*args)
                else:
                    return None
            except (NameError, OSError):
                self.info = '键鼠调用严重错误!!!'

    def mouse_R(self, x, y):
        # 相对移动鼠标
        return self._mouse_event('moveR', int(x), int(y))

    def mouse_To(self, x, y):
        # 移动鼠标到绝对坐标
        return self._mouse_event('moveTo', int(x), int(y))

    def mouse_down(self, key=1):
        # 鼠标按下，默认左键
        return self._mouse_event('mouse_down', int(key))

    def mouse_up(self, key=1):
        # 鼠标释放，默认左键
        return self._mouse_event('mouse_up', int(key))

    def scroll(self, num=1):
        # 鼠标滚轮滚动
        return self._mouse_event('scroll', int(num))

    def key_down(self, key):
        # 键盘按键按下
        return self._mouse_event('key_down', key.encode('utf-8'))

    def key_up(self, key):
        # 键盘按键释放
        return self._mouse_event('key_up', key.encode('utf-8'))

    def device_close(self):
        # 关闭设备
        return self._mouse_event('device_close')
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from time import sleep
import threading
import json
import os
import winsound
import sys

def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        # PyInstaller 创建临时文件夹并保存路径在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 修改 GHUB 和 mouselistener 的导入
sys.path.append(resource_path('.'))
from GHUB import ghub_device
import mouselistener

class MouseShaker:
    def __init__(self, config):
        self.gd = ghub_device()
        self.running = False
        self.config = config

    def shaker(self):
        if mouselistener.mousel == 1 and mouselistener.mouser == 1:
            self.gd.mouse_R(-self.config['shake_value'], self.config['shake_value'])
            sleep(self.config['delay'])
            self.gd.mouse_R(self.config['shake_value'], -self.config['shake_value'])
            sleep(self.config['delay'])

    def monitor_mouse(self):
        while self.running:
            self.shaker()
            sleep(0.005)

    def start(self):
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_mouse)
        self.monitor_thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'monitor_thread') and self.monitor_thread.is_alive():
            self.monitor_thread.join()

class ShakerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Apex自动抖枪 by b站听我弹钢琴都能睡着啊")
        self.master.geometry("240x460")

        self.config = self.load_config()
        self.shaker = MouseShaker(self.config)

        icon_path = resource_path('shaker.ico')
        if os.path.exists(icon_path):
            self.master.iconbitmap(icon_path)
        else:
            print(f"Icon file {icon_path} not found.")

        if self.show_first_time_popup():
            self.create_widgets()
        else:
            self.master.withdraw()  # 隐藏主窗口

    def show_first_time_popup(self):
        if not os.path.exists('verify.flag'):
            popup = tk.Toplevel(self.master)
            popup.title("重要提示")
            popup.geometry("400x200")
            popup.grab_set()  # 模态窗口

            message = "注意❗ 此项目仅供学习交流，旨在抛砖引玉打开思路。软件最终解释权归b站 听我弹钢琴都能睡着啊 所有。如有侵权请联系我"
            tk.Label(popup, text=message, wraplength=300, justify="center").pack(pady=20)

            def on_agree():
                with open('verify.flag', 'w') as f:
                    f.write('shown')
                popup.destroy()
                self.master.deiconify()  # 显示主窗口
                self.create_widgets()

            tk.Button(popup, text="我知道辣", command=on_agree).pack(pady=10)

            return False
        return True

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="抖动幅度（像素）:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.shake_value = ttk.Entry(main_frame, width=10)
        self.shake_value.insert(0, str(self.config['shake_value']))
        self.shake_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="抖动间隔（秒）:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.delay = ttk.Entry(main_frame, width=10)
        self.delay.insert(0, str(self.config['delay']))
        self.delay.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.toggle_button = ttk.Button(main_frame, text="开始", command=self.toggle_shaker)
        self.toggle_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.status_label = ttk.Label(main_frame, text="状态：停止")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.add_background_image()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_background_image(self):
        try:
            image = Image.open(resource_path("cat.png"))
            image = image.resize((240, 289), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            background_label = tk.Label(self.master, image=photo)
            background_label.image = photo
            background_label.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.S))
        except FileNotFoundError:
            print("背景图片 'cat.png' 未找到。")
        except Exception as e:
            print(f"加载背景图片时发生错误: {e}")

    def toggle_shaker(self):
        if self.shaker.running:
            self.shaker.stop()
            self.toggle_button.config(text="开始")
            self.status_label.config(text="状态：停止")
            winsound.Beep(1000, 100)
            winsound.Beep(1000, 100)
        else:
            self.update_config()
            self.shaker.start()
            self.toggle_button.config(text="停止")
            self.status_label.config(text="状态：运行中")
            winsound.Beep(1000, 200)

    def update_config(self):
        try:
            self.config['shake_value'] = int(self.shake_value.get())
            self.config['delay'] = float(self.delay.get())
            self.shaker.config = self.config
            self.save_config()
        except ValueError:
            print("Invalid input. Please enter numbers only.")

    def load_config(self):
        default_config = {'shake_value': 10, 'delay': 0.01}
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        return default_config

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def on_closing(self):
        self.shaker.stop()
        self.update_config()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = ShakerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import threading
import tkinter as tk
from pynput import keyboard
import pygame

no_sound = False



disable_key = [
        keyboard.Key.cmd,  # Windows 键
        keyboard.Key.f1, keyboard.Key.f2,  keyboard.Key.f3, keyboard.Key.f4, keyboard.Key.f5,  keyboard.Key.f6,
        keyboard.Key.f7, keyboard.Key.f8,  keyboard.Key.f9, keyboard.Key.f10, keyboard.Key.f12,  keyboard.Key.f11,
        keyboard.Key.caps_lock,  # 大写锁定键
        keyboard.Key.ctrl,  # Ctrl 键
        keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right,  # 上下左右键
        keyboard.Key.home, keyboard.Key.end, keyboard.Key.page_up, keyboard.Key.page_down,  # Home, End, PageUp, PageDown 键
        keyboard.Key.print_screen,  # PrintScreen 键
        keyboard.Key.pause,  # Pause 键
        keyboard.Key.num_lock, keyboard.Key.scroll_lock,  # NumLock, ScrollLock 键
        keyboard.Key.esc  # ESC 键
]
ji = {}
n = None
# 定义回调函数，在按键按下时执行
def on_press(key):
    if key in disable_key or no_sound:
        return
    try:
        n = ji[key]
    except KeyError:
        ji[key] = False
    finally:
        if not ji[key]:
            ji[key] = True
            pygame.mixer.init()
            pygame.mixer.music.load(r'C:\Users\nanocode38\Music\KeyBoard.mp3')
            pygame.mixer.music.play()

def out(key):
    ji[key] = False

# 创建监听器
listener = keyboard.Listener(on_press=on_press, on_release=out)
# 启动监听器
listener_thread = threading.Thread(target=listener.start)
listener_thread.daemon = True  # 将监听器线程设置为守护进程
listener_thread.start()

def loudspeaker_mute():
    global no_sound
    no_sound = not no_sound

root = tk.Tk()
root.overrideredirect(1)
root.wm_attributes('-alpha', 0.8)
root.wm_attributes('-toolwindow', True)
root.wm_attributes('-topmost', True)
root.geometry('210x25+400+500')
root.update()



def start_move(event):
    global x, y
    x = event.x
    y = event.y


def stop_move(event):
    global x, y
    x = None
    y = None


def on_motion(event):
    global x, y
    deltax = event.x - x
    deltay = event.y - y
    root.geometry("+%s+%s" % (root.winfo_x() + deltax, root.winfo_y() + deltay))
    root.update()


root.bind("<B1-Motion>", on_motion)

move_button = tk.Button(root)
# 绑定按下和松开事件
move_button.bind("<ButtonPress-1>", start_move)
move_button.bind("<ButtonRelease-1>", stop_move)
move_button.pack(side='left')


image = tk.PhotoImage(file = r".\images\sound_button.png")
image = image.subsample(1, 1)

sound_button = tk.Button(root, image=image, command=loudspeaker_mute)
sound_button.pack(side='right')
root.mainloop()
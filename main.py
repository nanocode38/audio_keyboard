import os.path
import threading
import tkinter as tk
import pickle
import os
from sys import exit
from pathlib import Path

import pygame
from pynput import keyboard
from pynput.keyboard import Key

launcher = 'Chinese'

disable_key = [
    Key.cmd,  # Windows 键
    Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6,
    Key.f7, Key.f8, Key.f9, Key.f10, Key.f12, Key.f11,
    Key.caps_lock,  # 大写锁定键
    Key.ctrl,  Key.ctrl_l, Key.ctrl_r, # Ctrl 键
    Key.up, Key.down, Key.left, Key.right,  # 上下左右键
    Key.home, Key.end, Key.page_up, Key.page_down,  # Home, End, PageUp, PageDown 键
    Key.print_screen,  # PrintScreen 键
    Key.pause,  # Pause 键
    Key.num_lock, Key.scroll_lock,  # NumLock, ScrollLock 键
    Key.esc,  # ESC 键
    Key.alt, Key.alt_l, Key.alt_r, Key.alt_gr,  # ALT键
    Key.media_volume_mute, Key.media_volume_down, Key.media_volume_up, # 音量增减键
    Key.shift, Key.shift_r, Key.shift_l,  # Shift键
]

launcher_key = {
    'Chinese':[
        '键盘音频文件设置:',
        '此文件不是音频文件',
        '此路径不是文件',
        '退出系统',
        '确定',
        '关于',
        '设置',
        '英语English',
        """音效键盘系统
属于: nanocode38 Copyright(C)
官方网站: https://github.com/nanocode38/audio_keyboard"""

    ],
    'English':[
        'Keyboard audio file settings:',
        'This file is not an audio file',
        'This path is not a file',
        'Exit System',
        'OK',
        'About',
        'Settings',
        'Chinese中文',
        """Sound keyboard system
Subject to: nanocode38 Copyright (C)
Official website: https://github.com/nanocode38/audio_keyboard"""
    ]
}

continuous_button = {
    Key.ctrl_l: False,
    Key.ctrl_r: False,
    Key.alt: False,
    Key.alt_r: False,
    Key.alt_l: False,
    Key.alt_gr: False,
    Key.cmd: False,
    Key.cmd_l: False,
    Key.cmd_r: False,
    Key.shift: False,
    Key.shift_l: False,
    Key.shift_r: False
}

home_path = Path.home()
if not os.path.isdir(home_path / 'sKeyBoard'):
    os.mkdir(home_path / 'sKeyBoard')
    no_sound = False
    sounds_path = r'.\sounds\KeyBoard.mp3'
else:
    with open(home_path / 'sKeyBoard' / 'sounds_data.dat', 'rb') as f:
        sounds_path = str(pickle.load(f))
    with open(home_path / 'sKeyBoard' / 'no_data.dat', 'rb') as f:
        no_sound = bool(pickle.load(f))

def _exit():
    global sounds_path, no_sound
    with open(home_path / 'sKeyBoard' / 'sounds_data.dat', 'wb') as f:
        pickle.dump(sounds_path, f)
    with open(home_path / 'sKeyBoard' / 'no_data.dat', 'wb') as f:
        pickle.dump(no_sound, f)
    exit(0)

# 定义回调函数，在按键按下时执行
def on_press(key):
    global sounds_path
    the_auxiliary_key_was_pressed = (continuous_button[Key.ctrl_l] or continuous_button[
        Key.ctrl_r] or continuous_button[Key.ctrl_l] or continuous_button[Key.alt] or continuous_button[
                                         Key.alt_r] or continuous_button[Key.alt_l] or continuous_button[Key.alt_gr] or
                                     continuous_button[
                                         Key.cmd] or continuous_button[Key.cmd_l] or continuous_button[Key.cmd_r])

    if the_auxiliary_key_was_pressed:
        return
    try:
        n = continuous_button[key]
    except KeyError:
        continuous_button[key] = False
    finally:
        if not continuous_button[key]:
            continuous_button[key] = True
            if key in disable_key or no_sound:
                return
            pygame.mixer.init()
            pygame.mixer.music.load(sounds_path)
            pygame.mixer.music.play()


def out(key):
    continuous_button[key] = False


# 创建监听器
listener = keyboard.Listener(on_press=on_press, on_release=out)
# 启动监听器
listener_thread = threading.Thread(target=listener.start)
listener_thread.daemon = True  # 将监听器线程设置为守护进程
listener_thread.start()

def get_new_main_root():
    global root, sound_image, about_button, exit_button, move_button, settings_button, sound_button, settings_image
    global launcher_key, launcher, no_sound, no_sound_image, sound_image, get_about, getsettings, _exit, exit_image
    root = tk.Tk()
    root.overrideredirect(1)
    root.wm_attributes('-alpha', 0.8)
    root.wm_attributes('-toolwindow', True)
    root.wm_attributes('-topmost', True)
    root.geometry('210x25+400+500')
    root.update()

    sound_image = tk.PhotoImage(file=r".\images\sound_button.png")

    no_sound_image = tk.PhotoImage(file=r".\images\no_sound_button.png")

    settings_image = tk.PhotoImage(file=r'.\images\settings.png')

    exit_image = tk.PhotoImage(file=r'.\images\exit.png')

    about_button = tk.Button(root, text=launcher_key[launcher][5], command=get_about)
    about_button.place(x=120, y=0)

    settings_button = tk.Button(root, image=settings_image, command=getsettings)
    settings_button.pack()

    exit_button = tk.Button(root, image=exit_image, command=_exit)
    exit_button.place(x=40, y=0)

    move_button = tk.Button(root)
    # 绑定按下和松开事件
    move_button.bind("<ButtonPress-1>", start_move)
    move_button.bind("<ButtonRelease-1>", stop_move)
    move_button.bind("<B1-Motion>", on_motion)
    move_button.place(x=-1, y=0)

    if no_sound:
        sound_button = tk.Button(root, image=no_sound_image, command=loudspeaker_mute)
    else:
        sound_button = tk.Button(root, image=sound_image, command=loudspeaker_mute)
    sound_button.place(x=180, y=-2)

    root.mainloop()



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



def loudspeaker_mute():
    global no_sound
    no_sound = not no_sound
    if no_sound:
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
        sound_button.config(image=no_sound_image)
    else:
        sound_button.config(image=sound_image)



def getsettings():
    global sounds_path
    sroot = tk.Tk()
    sroot.title(launcher_key[launcher][6])
    sroot.wm_attributes('-alpha', 0.8)
    sroot.wm_attributes('-topmost', True)
    sroot.geometry('400x360+300+250')
    sroot.iconbitmap(r'./images/Logo.ico')

    label = tk.Label(sroot, text=launcher_key[launcher][0])
    label.grid(row=0, column=0)

    path_entry = tk.Entry(sroot, bd=3, width=51)
    path_entry.insert(0, sounds_path)
    path_entry.place(x=1, y=30)

    get = False
    def get_message():
        global sounds_path
        global get
        get = True
        from tkinter import filedialog
        f_path = filedialog.askopenfilename(title='Open Sounds File')
        if f_path != '':
            if os.path.splitext(f_path)[1] not in ('.mp3', '.wav'):
                from tkinter import messagebox
                messagebox.showerror(title='File Error', message=launcher_key[launcher][1])
            else:
                sounds_path = f_path
                path_entry.delete(0, tk.END)
                path_entry.insert(0, f_path)

    def s():
        global sounds_path
        if not get:
            f_path = path_entry.get()
            if f_path != '':
                if not os.path.isfile(f_path):
                    from tkinter import messagebox
                    messagebox.showerror(title='File Error', message=launcher_key[launcher][2])
                elif os.path.splitext(f_path)[1] not in ('.mp3', '.wav'):
                    from tkinter import messagebox
                    messagebox.showerror(title='File Error', message=launcher_key[launcher][1])
                else:
                    sounds_path = f_path
        sroot.destroy()

    path_button = tk.Button(sroot, text='. . .', command=get_message)
    ok_button = tk.Button(sroot, text=launcher_key[launcher][4], command=s)
    path_button.place(x=370, y=25)
    ok_button.place(x=10, y=59)

    exit_button = tk.Button(sroot, text=launcher_key[launcher][3], command=_exit)
    exit_button.place(x=250, y=100)

    def launcher_k():
        global root
        global launcher
        if launcher == 'Chinese':
            launcher = 'English'
        else:
            launcher = 'Chinese'
        root.destroy()
        sroot.destroy()
        get_new_main_root()

    launcher_button = tk.Button(sroot, text=launcher_key[launcher][7], command=launcher_k)
    launcher_button.place(x=100, y=200)


    sroot.update()
    sroot.mainloop()


def get_about():
    sroot = tk.Tk()
    sroot.title(launcher_key[launcher][5])
    sroot.wm_attributes('-alpha', 0.8)
    sroot.wm_attributes('-topmost', True)
    sroot.geometry('400x360+300+250')
    sroot.iconbitmap(r'./images/Logo.ico')

    about_text = launcher_key[launcher][8]

    label = tk.Label(sroot, text=about_text)
    label.grid(row=0, column=0)


root = tk.Tk()
root.overrideredirect(1)
root.wm_attributes('-alpha', 0.8)
root.wm_attributes('-toolwindow', True)
root.wm_attributes('-topmost', True)
root.geometry('210x25+400+500')
root.update()

sound_image = tk.PhotoImage(file=r".\images\sound_button.png")

no_sound_image = tk.PhotoImage(file=r".\images\no_sound_button.png")

settings_image = tk.PhotoImage(file=r'.\images\settings.png')

exit_image = tk.PhotoImage(file=r'.\images\exit.png')

about_button = tk.Button(root, text=launcher_key[launcher][5], command=get_about)
about_button.place(x=120, y=0)

settings_button = tk.Button(root, image=settings_image, command=getsettings)
settings_button.pack()

exit_button = tk.Button(root, image=exit_image, command=_exit)
exit_button.place(x=40, y=0)

move_button = tk.Button(root)
# 绑定按下和松开事件
move_button.bind("<ButtonPress-1>", start_move)
move_button.bind("<ButtonRelease-1>", stop_move)
move_button.bind("<B1-Motion>", on_motion)
move_button.place(x=-1, y=0)

if no_sound:
    sound_button = tk.Button(root, image=no_sound_image, command=loudspeaker_mute)
else:
    sound_button = tk.Button(root, image=sound_image, command=loudspeaker_mute)
sound_button.place(x=180, y=-2)

root.mainloop()
import os.path
import threading
import tkinter as tk
import pickle
import os
from sys import exit
from pathlib import Path


import pygame.mixer
from pynput import keyboard
from pynput.keyboard import Key

DISABLE_KEY = [
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

LANGUAGE_LIST = {
    'Chinese':{
        'sounds set':'键盘音频文件设置:',
        'not sounds':'此文件不是音频文件',
        'not file':'此路径不是文件',
        'exit':'退出系统',
        'ok':'确 定',
        'set':'设置',
        'lau':'英语English',
        'about title': '关于',
        'about':"""音效键盘系统
属于: nanocode38 Copyright(C)
官方网站: https://github.com/nanocode38/audio_keyboard
赞助一下:
""",
        'calc':'取 消',
        'language text': '语言设置(Language):',
        'reset': '恢复原路径'
},
    'English':[
        'Keyboard audio file settings:',
        'This file is not an audio file',
        'This path is not a file',
        'Exit System',
        'O K',
        'Settings',
        'Chinese中文',
        'About',
        """Sound keyboard system
Subject to: nanocode38 Copyright (C)
Official website: https://github.com/nanocode38/audio_keyboard
Sponsorship:
""",
        'Cancel',
        'Language(语言设置):',
        'recover'
    ]
}

e = {}
i = 0
for key in LANGUAGE_LIST['Chinese'].keys():
    e[key] = LANGUAGE_LIST['English'][i]
    i += 1
LANGUAGE_LIST['English'] = e
del e, i


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
if not os.path.isdir(home_path / 'AudioKeyBoard') or \
        not os.path.isfile(home_path / 'AudioKeyBoard' / 'audio_keyboard_data.dat'):
    os.mkdir(home_path / 'AudioKeyBoard')
    no_sound = False
    sounds_path = r'.\sounds\KeyBoard.mp3'
    language = 'Chinese'
else:
    with open(home_path / 'AudioKeyBoard' / 'audio_keyboard_data.dat', 'rb') as f:
        sounds_path = str(pickle.load(f))
        language = str(pickle.load(f))
        no_sound = bool(pickle.load(f))


sounds_path = os.path.abspath(sounds_path)
def _exit():
    global sounds_path, no_sound
    with open(home_path / 'AudioKeyBoard' / 'audio_keyboard_data.dat', 'wb') as f:
        pickle.dump(sounds_path, f)
        pickle.dump(language, f)
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
            if key in DISABLE_KEY or no_sound:
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


def get_new_main_root(isnooroot=True):
    global root, sound_image, about_button, exit_button, move_button, settings_image
    global LANGUAGE_LIST, language, no_sound, no_sound_image, sound_image, get_about
    global logo, get_settings, _exit, exit_image, settings_button, sound_button
    if isnooroot:
        root = tk.Tk()
    root.overrideredirect(True)
    root.wm_attributes('-alpha', 0.7)
    root.wm_attributes('-toolwindow', True)
    root.wm_attributes('-topmost', True)
    root.geometry('175x25+500+600')
    root.update()

    sound_image = tk.PhotoImage(file=r".\images\sound_button.png")
    no_sound_image = tk.PhotoImage(file=r".\images\no_sound_button.png")
    settings_image = tk.PhotoImage(file=r'.\images\settings.png')
    exit_image = tk.PhotoImage(file=r'.\images\exit.png')
    logo_image = tk.PhotoImage(file=r'.\images\logo.png')


    settings_button = tk.Button(root, image=settings_image, command=get_settings)
    settings_button.place(x=10, y=0)

    exit_button = tk.Button(root, image=exit_image, command=_exit)
    exit_button.place(x=39, y=0)

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
    sound_button.place(x=110, y=-1)

    logo = tk.Button(root, image=logo_image, command=get_about)
    logo.place(x=146, y=-3)

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



def get_settings():
    global sounds_path, LANGUAGE_LIST
    global root, language
    settings_windows = tk.Toplevel(root)
    settings_windows.title(LANGUAGE_LIST[language]['set'])
    settings_windows.wm_attributes('-alpha', 0.8)
    settings_windows.wm_attributes('-topmost', True)
    settings_windows.geometry('400x360+300+250')
    settings_windows.iconbitmap(r'./images/Logo.ico')

    label = tk.Label(settings_windows, text=LANGUAGE_LIST[language]['sounds set'])
    label.grid(row=0, column=0)

    path_entry = tk.Entry(settings_windows, bd=3, width=51)
    if sounds_path[1] != ':':
        path_entry.insert(0, sounds_path)
    else:
        path_entry.insert(0, sounds_path)
    path_entry.place(x=1, y=30)
    get = False
    def get_message():
        global sounds_path, LANGUAGE_LIST
        global get, language
        get = True
        from tkinter import filedialog
        f_path = filedialog.askopenfilename(title='Open Sounds File')
        if f_path != '':
            if os.path.splitext(f_path)[1] not in ('.mp3', '.wav'):
                from tkinter import messagebox
                messagebox.showerror(title='File Error', message=LANGUAGE_LIST[language]['not sounds'])
            else:
                sounds_path = f_path
                path_entry.delete(0, tk.END)
                path_entry.insert(0, f_path)

    old_language = language
    newlanguage = tk.StringVar()
    newlanguage.set(old_language)
    def ok():
        global sounds_path, language
        language = newlanguage.get()
        if not get:
            f_path = path_entry.get()
            if f_path != '':
                if not os.path.isfile(f_path):
                    from tkinter import messagebox
                    messagebox.showerror(title='File Error', message=LANGUAGE_LIST[language]['not file'])
                elif os.path.splitext(f_path)[1] not in ('.mp3', '.wav'):
                    from tkinter import messagebox
                    messagebox.showerror(title='File Error', message=LANGUAGE_LIST[language]['no sounds'])
                else:
                    sounds_path = f_path

            if old_language != language:
                root.destroy()
                get_new_main_root()

            else:
                settings_windows.destroy()

    path_button = tk.Button(settings_windows, text='. . .', command=get_message)
    ok_button = tk.Button(settings_windows, width=10, text=LANGUAGE_LIST[language]['ok'], command=ok)
    no_button = tk.Button(settings_windows, width=10, text=LANGUAGE_LIST[language]['calc'],
                          command=settings_windows.destroy)
    path_button.place(x=370, y=25)
    ok_button.place(x=250, y=330)
    no_button.place(x=320, y=330)

    def reset():
        get = False
        s_path = Path.cwd()
        s_path  = s_path / 'sounds' / 'KeyBoard.mp3'
        path_entry.delete(0, tk.END)
        path_entry.insert(0, s_path)

    exit_button = tk.Button(settings_windows, text=LANGUAGE_LIST[language]['exit'], command=_exit)
    exit_button.place(x=10, y=330)

    reset_button = tk.Button(settings_windows, text=LANGUAGE_LIST[language]['reset'], command=reset)
    reset_button.place(x=10, y=55)


    la_text = tk.Label(settings_windows, text=LANGUAGE_LIST[language]['language text'])
    la_text.place(x=5, y=100)
    chinese_radiobutton = tk.Radiobutton(settings_windows, text='简体中文', variable=newlanguage, value='Chinese')
    english_radiobutton = tk.Radiobutton(settings_windows, text='English(USA)', variable=newlanguage, value='English')
    chinese_radiobutton.place(x=50, y=130)
    english_radiobutton.place(x=50, y=160)



    settings_windows.update()
    settings_windows.mainloop()


def get_about():
    global root, language, LANGUAGE_LIST
    about_windows = tk.Toplevel(root)
    about_windows.title(LANGUAGE_LIST[language]['about title'])
    about_windows.wm_attributes('-alpha', 0.8)
    about_windows.wm_attributes('-topmost', True)
    about_windows.geometry('500x620+100+5')
    about_windows.iconbitmap(r'./images/Logo.ico')

    about_text = LANGUAGE_LIST[language]['about']

    text_label = tk.Label(about_windows, text=about_text, justify=tk.CENTER)
    text_label.pack()

    support_image = tk.PhotoImage(file=r'.\images\support.png')
    support_image = support_image.subsample(2, 2)
    support_label = tk.Label(about_windows, image=support_image)
    support_label.pack()

    about_windows.mainloop()



root = tk.Tk()
get_new_main_root(False)
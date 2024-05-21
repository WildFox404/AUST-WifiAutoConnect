import os
import win32com.client
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import  subprocess
import sys
import io
import shutil
def create_shortcut(target_path, shortcut_path):
    """
    创建快捷方式
    :param target_path: 源文件路径
    :param shortcut_path: 快捷方式放置路径
    :return:
    """
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.save()

def browse_path():
    """
    浏览文件夹路径
    :return:
    """
    path = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, path)
def get_startup_folder():
    """
    获取启动文件夹路径
    :return:
    """
    # 快捷方式放置路径
    shortcut_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(shortcut_folder, 'AUST_WIFI.lnk')
    return shortcut_path

def install():
    """
    安装程序
    :return:
    """
    try:
        user_dict={"运营商":str(selected_option.get()),"账号":str(entry_account.get()),"密码":str(entry_password.get()),"cookie":"12e9gkv2ves20va0bg0ctnojud","路径":str(entry_path.get())}
        target_path=str(entry_path.get())
        if target_path.endswith('/'):
            print("target_path 以 / 结尾")
            target_path = target_path
        else:
            print("target_path 不以 / 结尾")
            target_path = target_path+"/"
        # 读取打包在可执行文件中的资源文件内容
        exe_path=get_file_from_resource("AUST_WIFI.exe")
        txt_path=get_file_from_resource("config.txt")
        uninstall_path = get_file_from_resource("uninstall.bat")
        uninstall_exe_path = get_file_from_resource("uninstall.exe")
        copy_file_to_destination(exe_path, target_path)
        copy_file_to_destination(txt_path, target_path)
        copy_file_to_destination(uninstall_path, target_path)
        copy_file_to_destination(uninstall_exe_path, target_path)

        txt=target_path+"config.txt"
        with open(txt, 'wb') as w:
            for key, value in user_dict.items():
                w.write(f'{key}:{value}\n'.encode())

        lnk=target_path+"AUST_WIFI.exe"
        # 创建快捷方式
        create_shortcut(lnk, get_startup_folder())
        print("快捷方式已创建在启动文件夹中。")

        chrome_path = get_file_from_resource("ChromeSetup.exe")
        subprocess.Popen(chrome_path)
        print("浏览器已启动。安装完毕")

        subprocess.run('taskkill /F /IM AUST_WIFI_INSTALL.exe', shell=True)
    except:
        messagebox.showerror("安装失败", "安装过程中出现错误")
def get_file_from_resource(file_name):
    """
    从资源文件中获取文件路径
    :param file_name:
    :return:
    """
    file_path = sys._MEIPASS + "\\resources\\" + file_name
    return file_path

# 复制文件到指定路径文件夹下
def copy_file_to_destination(file_name, destination_path):
    """
    复制文件到指定路径文件夹下
    :param file_name:
    :param destination_path:
    :return:
    """
    shutil.copy(file_name, destination_path)
def get_image_from_resource(image_name):
    """
    从可执行文件中读取图片
    :param image_name:
    :return:
    """
    image_path = sys._MEIPASS + "\\resources\\" + image_name
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image = Image.open(io.BytesIO(image_data))
    photo = ImageTk.PhotoImage(image)
    return photo
if __name__ == '__main__':
    options = ["联通", "电信", "移动"]
    root = tk.Tk()
    root.title("LAZYDOG")

    # 显示图片
    image_path = get_image_from_resource("LAZYDOG_small.png")
    image_label = tk.Label(root, image=image_path)
    image_label.pack()

    # 第二行安装路径+浏览
    frame_path = tk.Frame(root)
    frame_path.pack()
    label_path = tk.Label(frame_path, text="安装路径:")
    label_path.pack(side=tk.LEFT)
    entry_path = tk.Entry(frame_path, width=40)
    entry_path.pack(side=tk.LEFT)
    btn_browse = tk.Button(frame_path, text="浏览", command=browse_path)
    btn_browse.pack(side=tk.LEFT)

    # 第三行账号
    frame_account = tk.Frame(root)
    frame_account.pack()
    label_account = tk.Label(frame_account, text="账号:")
    label_account.pack(side=tk.LEFT)
    entry_account = tk.Entry(frame_account, width=20)
    entry_account.pack(side=tk.LEFT)

    # 第四行密码
    frame_password = tk.Frame(root)
    frame_password.pack()
    label_password = tk.Label(frame_password, text="密码:")
    label_password.pack(side=tk.LEFT)
    entry_password = tk.Entry(frame_password, width=20)
    entry_password.pack(side=tk.LEFT)

    selected_option = tk.StringVar()
    selected_option.set(options[0])

    option_menu = tk.OptionMenu(root, selected_option, *options)
    option_menu.pack()

    # 创建一个内容为 "安装" 的按钮
    frame_install = tk.Frame(root)
    frame_install.pack()
    btn_install = tk.Button(frame_install, text="安装",command=install)
    btn_install.pack(side=tk.LEFT)

    root.mainloop()



import os
import subprocess
def readtxt():
    data_list = {}  # 存储字典数据的列表
    try:
        with open('config.txt', 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()  # 去除每行首尾的空白字符
                if line:
                    key, value = line.split(':',1)  # 按照 ":" 分割每行数据
                    end_key=key.strip()
                    end_value=value.strip()
                    data_list[end_key]=end_value
    except Exception as e:
        print(e)
        return None
    return data_list
def get_startup_folder():
    """
    获取启动文件夹路径
    :return:
    """
    return os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')


if __name__ == '__main__':
    data_list=readtxt()
    path=data_list["路径"]+"/"
    exe_path=path+"AUST_WIFI.exe"
    txt_path=path+"config.txt"
    uninstall_path=path+"uninstall.bat"
    shortcut_path = get_startup_folder()+"\AUST_WIFI.lnk"
    try:
        os.remove(shortcut_path)
        os.remove(exe_path)
        os.remove(txt_path)
        print(f"{shortcut_path} 文件已成功删除")
    except OSError as e:
        print(f"删除 {shortcut_path} 文件时出现错误: {e}")
    subprocess.Popen(uninstall_path)

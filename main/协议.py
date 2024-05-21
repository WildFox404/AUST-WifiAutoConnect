import time
import tkinter as tk
from tkinter import messagebox
import subprocess
from DrissionPage import WebPage

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
        messagebox.showwarning("警告", "txt文件有误")
        return None,True
    print(data_list)
    if  '移动' in data_list['运营商']:
        data_list['运营商'] = '@cmcc'
    elif '联通' in data_list['运营商']:
        data_list['运营商'] = '@unicom'
    elif '电信' in data_list['运营商']:
        data_list['运营商'] = '@aust'
    else:
        print('运营商错误')
        return None,True
    f.close()
    print(data_list)
    return data_list,False
def connect_to_wifi():
    try:
        ssid = "AUST_Student"
        # 获取当前连接的WiFi信息
        current_output = subprocess.run('netsh wlan show interfaces', capture_output=True, text=True, shell=True)
        if ssid in current_output.stdout:
            print("已经链接过此WiFi")
            return True
        # 获取可用的WiFi列表
        networks_output = subprocess.run('netsh wlan show networks', capture_output=True, text=True, shell=True)
        if ssid not in networks_output.stdout:
            print(f"未检测到SSID为{ssid}的WiFi，请检查网络连接")
            return False
        # 构建连接WiFi的命令
        print("现在开始链接wifi")
        cmd = f'netsh wlan connect ssid="{ssid}" name="{ssid}"'
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print("连接WiFi时出错：", e)

def get_url(userlist):
    import requests
    cookies = {
        'PHPSESSID': f'{userlist["cookie"]}',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'http://10.255.0.19/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
    }

    params = {
        'callback': 'dr1003',
        'DDDDD': f'{userlist["账号"]}{userlist["运营商"]}',
        'upass': f'{userlist["密码"]}',
        '0MKKey': '123456',
        'R1': '0',
        'R3': '0',
        'R6': '0',
        'para': '00',
        'v6ip': '',
    }
    try:
        response = requests.get('http://10.255.0.19/drcom/login', params=params, cookies=cookies, headers=headers,
                                verify=False, timeout=timeout)
        result = response.text
        if "error" in result or "Error" in result:
            print("在响应文本中找到了 'error' 或 'Error' 字符串")
            return False
        else:
            print("在响应文本中未找到 'error' 或 'Error' 字符串")
            return True

    except requests.exceptions.Timeout:
        print("请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        return False

def browser_auto(user_dict):
    username=user_dict["账号"]
    password=user_dict["密码"]
    agent=user_dict["运营商"]
    index=3
    if agent=="@aust":
        agent="电信"
        index=3
    elif agent=="@unicom":
        agent="联通"
        index=4
    elif agent=="@cmcc":
        agent="移动"
        index=5
    try:
        page=WebPage()
        page.get('http://10.255.0.19')
        page.set.window.max()
        page.ele('xpath=//*[@id="edit_body"]/div[4]/div[1]/form/input[3]').input(username)
        page.ele('xpath=//*[@id="edit_body"]/div[4]/div[1]/form/input[4]').input(password)
        time.sleep(0.5)
        page.ele(f'xpath=//*[@id="edit_body"]/div[4]/div[1]/select/option[{index}]').click.left(by_js=False)
        page.ele('xpath=//*[@id="edit_body"]/div[4]/div[1]/form/input[2]').click.left()
        cookie = page.cookies()[0]["value"]
        if cookie != "":
            user_dict["运营商"] = agent
            user_dict["cookie"] = cookie
            write_txt(user_dict)
        time.sleep(0.5)
        if "您已经成功登录"in page.html:
            print("登录成功")
            page.close_driver()
            return True
        else:
            page.close_driver()
            return False
    except Exception as e:
        print(f"浏览器自动化异常: {e}")
        page.close_driver()
        return False


def write_txt(user_dict):
    with open('config.txt', 'w',encoding="utf-8") as file:
        for key, value in user_dict.items():
            file.write(f'{key}:{value}\n')
    print(user_dict)

if __name__ == '__main__':
    # 创建 Tkinter 应用程序
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    timeout=5
    outer_break=False
    user_dict,Bool=readtxt()
    outer_break=Bool
    if user_dict==None:
        messagebox.showwarning("警告", "代理商配置信息有误")
        outer_break=True
    for i in range(5):
        try:
            result = connect_to_wifi()
            time.sleep(1)
            if result==True and not outer_break:
                for  i in range(3):
                    print("正在获取网络信息，请稍后...")
                    content=get_url(user_dict)
                    if content==False:
                        print("未获取到网络信息，请检查网络连接")
                    else:
                        print("获取到网络信息，正在退出程序")
                        # 弹出消息框
                        messagebox.showinfo("执行完毕", "网络链接完毕\n自动弹出浏览器不用操作\ngithub地址:https://github.com/WildFox404\nQQ群:956026820")
                        outer_break = True
                        break
                    time.sleep(1)
            elif result==False :
                messagebox.showinfo("糟糕","未检测到wifi")
                outer_break=True
                break
            if outer_break:
                break
        except Exception as e:
            print(f"错误{e}")
    if outer_break==False:
        messagebox.showinfo("提示","协议请求失败\n即将开启浏览器自动化")
        for i in range(2):
            end=browser_auto(user_dict)
            if end==True:
                messagebox.showinfo("执行完毕", "网络链接完毕\n自动弹出浏览器不用操作\ngithub地址:https://github.com/WildFox404\nQQ群:956026820")
                break
            time.sleep(1)
    root.destroy()
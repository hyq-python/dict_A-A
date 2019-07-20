from socket import *
import hashlib
from getpass import getpass
from time import sleep

# 建立客户端套接字
adress = ('176.221.13.6', 8000)
s = socket()
s.connect(adress)


# ---------客户端连接已经生成，网络架构搭建已经完成。
# login需要负责的功能就是将输入的name和code发送至服务端完成验证登录。
def do_query(name):
    while True:
        word = input("输入单词(输入'退出'退出查询)：")
        #   创建网络协议 Q
        if word == "退出":
            break
        data = "Q %s %s" % (name, word)
        s.send(data.encode())
        databack = s.recv(1024).decode()
        if databack != "False":
            print(databack)
        else:
            print("没有查到相关单词，请检查查找是否存在拼写错误！")


def do_history(name):  # 创建网络协议
    data = "H %s" % name
    s.send(data.encode())
    databack = s.recv(1024).decode()
    # 设置返回值，如果存在历史记录，则返回结果，反之，则返回None.
    if databack != "False":  # tcp出现粘包现象
        tem = databack.split("*")
        for item in tem:
            print(item)

    else:
        sleep(0.5)
        print("您还没有查找过单词呢，查找几个试试看吧")
        return


def step_into(name):
    while True:
        view = """
                =============view2================
                1.查询       2.历史记录      3. 注销
                ==================================
        """
        print(view)
        cmd = input("输入命令：")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_history(name)
        elif cmd == "3":
            return
        else:
            print("输入1,2,3")


def do_login():
    name = input("输入用户名：")
    password = getpass("输入密码：")
    # 设置加密
    hash = hashlib.md5()
    hash.update(password.encode())
    code = hash.hexdigest()
    # 发送时加入网络协议‘L’
    data = "L %s %s" % (name, code)
    s.send(data.encode())
    backdata = s.recv(1024).decode()

    if backdata == "OK":
        view = """
                            =====================
                                    验证成功
                            =====================
            ************************************************************
                """
        print(view)
        sleep(1)
        print("***********进入查询界面中.......")
        sleep(0.5)
        step_into(name)
    else:
        print(backdata)
        return


# 注册负责的功能就是将注册信息发送至服务端完成验证是否可以注册，如果注册成功，则返回ok
# 反之，则为failure。退回至界面重新完成注册或登录。
def do_register():
    while True:
        name = input("请输入用户名：")
        code = getpass("输入密码：")
        code_1 = getpass("输入密码：")
        if code == code_1 and code:
            # 设置加密
            hash = hashlib.md5()
            hash.update(code.encode())
            pwd = hash.hexdigest()
            data = "R %s %s" % (name, pwd)
            s.send(data.encode())
            databack = s.recv(1024).decode()
            if databack != "failure":
                view = """
                                =====================
                                        注册成功
                                =====================
                                """

                print(view)
                sleep(1)
                print("***********进入查询界面中.......")
                sleep(0.5)
                step_into(name)
                return
            else:
                print(databack)
                return
        else:
            print("两次输入的密码不一致,请重新输入：")
            continue


def main():
    while True:
        view = """
                ==========界面一=============
                1.登录     2.注册      3.退出
                ============================
        """
        print(view)
        cmd = input("输入选项:1,2,3:")
        if cmd == "1":
            do_login()
        elif cmd == "2":
            do_register()
        elif cmd == "3":
            break
        else:
            print("数字不在可选范围内")


if __name__ == '__main__':
    main()

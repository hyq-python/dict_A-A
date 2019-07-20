from socket import *
from select import *
from database import databases

# 服务端：1.逻辑请求处理  2.数据库操作处理
# ----------------------------------------------------------
# 1.搭建服务端的网络通信，本网络采用tcp套接字进行传输，优点是无数据丢失，效率高.
adress = ('0.0.0.0', 8000)

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(adress)
s.listen(3)

print("waitting for connecting.....")
# 采用io多路复用来实现多并发.
dict_spy = {s.fileno(): s}
p = epoll()
p.register(s, EPOLLIN) # 注册关注的IO事件

def do_history(soc,data):
    name = data.decode().split(" ")[1]
    db = databases(database='dict')
    back_value = db.history(name)
    data_send =""
    if back_value:
        for item in back_value:
            data_send += (item[0]+"*")
        soc.send(data_send.encode())
    else:
        soc.send(b"False")


def do_query(soc,data):
    name = data.decode().split(" ")[1]
    words = data.decode().split(" ")[2]
    db = databases(database='dict')
    # 设置返回值为单词解释或者是False
    back_value = db.do_query(name , words)
    if back_value:
        soc.send(back_value.encode())
    else:
        soc.send(b"False")




def do_login(soc, data):  # 从客户端发送过来的name和code解析提交至数据库进行处理，如果与数据库匹配则返回相应的值。
    tem = data.decode().split(" ")
    key_1 = tem[1]
    key_2 = tem[2]
    db = databases(database='dict')  # 建立数据库对象，将name 和 code 交由数据库比对,给出比对结果。
    back_value = db.do_login(key_1, key_2)
    if back_value:
        soc.send(b"OK")
    else:
        soc.send(b"FAILURE")


def do_register(soc, data):
    tem = data.decode().split(" ")
    key_1 = tem[1]
    key_2 = tem[2]
    db = databases(database='dict')
    back_value = db.do_register(key_1, key_2)
    print(back_value)
    if back_value == True:
        soc.send(B"OK")
    else:
        soc.send(B"failure")


def main():
    while True:  # 开始监听
        events = p.poll()
        # events一个列表，列表里面嵌套嵌套元组
        for filenum, event in events:
            if filenum == s.fileno():
                c, addr = dict_spy[filenum].accept()
                print("connect from ", addr)
                p.register(c, EPOLLIN | EPOLLET)
                dict_spy[c.fileno()] = c

            elif event & EPOLLIN:
                data = dict_spy[filenum].recv(1024)
                if not data:
                    dict_spy[filenum].close()
                    p.unregister(filenum)
                    del dict_spy[filenum]
                    continue
                key = data.decode().split(" ")[0]
                if key == "L":
                    do_login(dict_spy[filenum], data)
                elif key == "R":
                    do_register(dict_spy[filenum], data)
                elif key == "Q":
                    do_query(dict_spy[filenum],data)
                elif key == "H":
                    do_history(dict_spy[filenum],data)


if __name__ == '__main__':
    main()

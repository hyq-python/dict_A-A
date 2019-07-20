#客户端功能
>建立客户端界面
>> 1.登录
   2.注册
   3.退出
#服务器端
>建立服务器链接

>>接收客户端的数据信息，对客户端数据进行解析
  然后提交数据库进行处理
  
>>数据库对信息进行处理，然后返回相应的结果

#数据库端
>对数据库进行二次封装，提供相应的方法接口，
重点内容为实例属性是作为类的全局变量使用。

    tips 对数据库的内容进行加密处理：
    
        import  hashlib
        import getpass
        password = getpass.getpass()
        print(password)
        hash =  hashlib.md5()#使用md5的加密模块
        hash.update(password.encode())
        pwd = hash.h
                                                                                                                                                                                                                                             
        exdigest()
        print(pwd)

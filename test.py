# 关于md5的加密模块
import hashlib
import getpass

password = getpass.getpass()
print(password)
hash = hashlib.md5()  # 使用md5的加密模块
hash.update(password.encode())
pwd = hash.hexdigest()
print(pwd)

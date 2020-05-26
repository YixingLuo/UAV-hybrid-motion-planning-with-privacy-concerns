

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os


#在d盘创建一个名字为1的文件夹
CUR_PATH = r'D:/1'

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
del_file(CUR_PATH)

#实例化虚拟用户，这是FTP验证首要条件
authorizer = DummyAuthorizer()

#添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
authorizer.add_user('user', '12345', 'D:/1', perm='elradfmw')

#添加匿名用户 只需要路径
authorizer.add_anonymous('D:/1')

#初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer

#添加被动端口范围
handler.passive_ports = range(2000, 2333)

#写上本电脑的ip
server = FTPServer(('192.168.43.58', 8090), handler)

#开始服务
server.serve_forever()

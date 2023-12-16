# 工具包
import os.path
import re
from datetime import datetime
from tqdm import tqdm


class Stream:
    __service_start_log = """
 _      _   _                                  _            ___    ___  
 | |    | | | |                                (_)          |__ \  / _ \ 
 | | ___| |_| |_ ___ _ __   ___  ___ _ ____   ___  ___ ___     ) || | | |
 | |/ _ \ __| __/ _ \ '__| / __|/ _ \ '__\ \ / / |/ __/ _ \   / / | | | |
 | |  __/ |_| ||  __/ |    \__ \  __/ |   \ V /| | (_|  __/  / /_ | |_| |
 |_|\___|\__|\__\___|_|    |___/\___|_|    \_/ |_|\___\___| |____(_)___/                                                                                                           
"""
    __client_start_log = """
  _      _   _                   _ _            _     ___    ___  
 | |    | | | |                 | (_)          | |   |__ \  / _ \ 
 | | ___| |_| |_ ___ _ __    ___| |_  ___ _ __ | |_     ) || | | |
 | |/ _ \ __| __/ _ \ '__|  / __| | |/ _ \ '_ \| __|   / / | | | |
 | |  __/ |_| ||  __/ |    | (__| | |  __/ | | | |_   / /_ | |_| |
 |_|\___|\__|\__\___|_|     \___|_|_|\___|_| |_|\__| |____(_)___/ 
"""
    __help_text = """
    绿色表示\033[0;32m在线\033[0m才能使用的功能
    红色表示\033[0;31m离线\033[0m才能使用的功能
    白色不做限制
    
        \033[0;32mls\033[0m: 显示所有在线用户
        me: 显示自己的状态
        clear: 清空记录
        help: 查看帮助
        path: 显示当前目录，及目录下的所有子目录
        \033[0;31mlogin\033[0m: 登录服务器
        \033[0;31mregister\033[0m: 注册一个账户并登录服务器
        \033[0;32mchat\033[0m [all|username] [text]: 给[所有|指定]用户发送消息
        \033[0;32mfile\033[0m [filepath] to [username]: 给指定用户发送文件
        \033[0;32mlogout\033[0m: 退出登录
        \033[0;32mrepwd\033[0m [old password] [new password]: 修改密码
        exit: 退出应用
    """

    @staticmethod
    def __now_date() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __system_out(self, msg: str, date=True):
        msg = f'$ {self.__now_date()} > {msg}' if date else f'$ > {msg}'
        print(msg)

    def system_out_normal(self, msg: str, date=True):
        """ 标准系统输出 """
        message = f'\033[0;36m{msg}\033[0m'
        self.__system_out(msg=message, date=date)

    def system_out_warning(self, msg: str, date=True):
        """ 系统警告输出 """
        message = f'\033[0;33m{msg}\033[0m'
        self.__system_out(msg=message, date=date)

    def system_out_error(self, msg: str, date=True):
        """ 系统错误输出 """
        message = f'\033[0;31m{msg}\033[0m'
        self.__system_out(msg=message, date=date)

    def system_out_win(self, msg: str, date=True):
        """ 系统成功输出 """
        message = f'\033[0;32m{msg}\033[0m'
        self.__system_out(msg=message, date=date)

    def system_out_help(self):
        print(self.__help_text)

    def start_service(self):
        print(self.__service_start_log)

    def start_client(self):
        print(self.__client_start_log)

    @staticmethod
    def system_input(msg: str) -> str:
        return input(f'$ {msg}: ')

    @staticmethod
    def user_input() -> str:
        return input(f'# ')


class Verify:
    @staticmethod
    def username_verify() -> str:
        username = Stream.system_input("username").strip()
        while True:
            if username.find(' ') != -1:
                username = Stream.system_input("不能包含空格, username")
            elif username in ['all', 'exit', 'file', 'to', 'chat', 'clear', 'me']:
                username = Stream.system_input("不能是关键字, username")
            elif not (4 <= len(username) <= 8):
                username = Stream.system_input("长度必须是4~8, username")
            else:
                break
        return username

    @staticmethod
    def password_verify() -> str:
        password = Stream.system_input("password").strip()
        while True:
            if re.match('^[a-z0-9]{4,8}$', password): break
            password = Stream.system_input("密码由数组和字母组成的4~8位, password").strip()
        return password

    @staticmethod
    def order_verify(order: str) -> bool:
        """ 校验指令 """
        if order == 'ls' or order == 'me': return True
        if order == 'clear' or order == 'login': return True
        if order == 'register' or order == 'logout': return True
        if order == 'exit' or order == 'help' or order == 'path': return True
        if order.startswith('chat') and len(order.split(' ')) >= 3: return True
        if order.startswith('file') and len(order.split(' ')) == 4 and order.split()[-2] == 'to': return True
        if order.startswith('repwd') and len(order.split(' ')) == 3: return True
        return False


class File:
    @staticmethod
    def verify(filename: str) -> tuple:
        """ 校验文件并返回文件大小 """
        if os.path.exists(filename): return True, os.path.getsize(filename)
        return False, 0

    @staticmethod
    def upload_file(filename: str, filesize, client):
        Stream().system_out_warning(f'正在发送: {filename}, size: {filesize}B')
        progress = tqdm(range(filesize), f'发送: {filename}', unit='B', unit_divisor=1024, unit_scale=True)
        with open(filename, 'rb') as fp:
            for _ in range(filesize // 1024 + 1):
                data = fp.read(1024)
                if not data: break
                client.sendall(data)
                progress.update(len(data))

    @staticmethod
    def download_file(client, filesize, filename):
        Stream().system_out_warning(f'正在接收: {filename}, size: {filesize}B')
        progress = tqdm(range(filesize), f'接收: {filename}', unit='B', unit_divisor=1024, unit_scale=True)
        if not os.path.exists(f'./temp'): os.mkdir(f'./temp')
        with open(f'./temp/{filename}', 'wb') as fp:
            for _ in range(filesize // 1024 + 1):
                item = client.recv(1024)
                if not item: break
                fp.write(item)
                progress.update(len(item))

    @staticmethod
    def save(filename, filesize, username, old_user, client):
        if not os.path.exists(f'./{username}'): os.mkdir(f'./{username}')
        filepath = f'./{username}/{filename}'
        progress = tqdm(range(filesize), f'接收: {filename}', unit='B', unit_divisor=1024, unit_scale=True)
        with open(filepath, 'wb') as fp:
            for _ in range(filesize // 1024 + 1):
                data = client.recv(1024)
                if not data: break
                fp.write(data)
                progress.update(len(data))

        Stream().system_out_win(f'用户 {old_user} 传递的文件 {filename} {filesize}B, 保存至: {filepath}')
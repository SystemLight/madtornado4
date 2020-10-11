import os
import platform


def kill_form_port(port):
    """

    根据传入端口号，尝试杀死进程，支持windows和linux平台

    :param port: 端口号，int类型
    :return: None

    """
    port = str(port)
    if platform.system() == 'Windows':
        command = """for /f "tokens=5" %i in ('netstat -ano ^| find \"""" + port + """\" ') do (taskkill /f /pid %i)"""
    else:
        command = """kill -9 $(netstat -nlp | grep :""" + port + """ | awk '{print $7}' | awk -F "/" '{print $1}')"""
    os.system(command)

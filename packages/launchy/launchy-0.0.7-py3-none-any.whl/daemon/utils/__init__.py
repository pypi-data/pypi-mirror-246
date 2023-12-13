# -*- coding: utf-8 -*-

import os
import platform
import socket
import time
from time import gmtime
from time import strftime

import psutil


def get_process_port(pid):
    """
    get process port
    :param pid:
    :return:
    """
    connections = psutil.net_connections()
    port_list = []
    for conn in connections:
        if conn.pid == pid and conn.status == 'LISTEN':
            port_list.append(conn.laddr.port)
    return ",".join(port_list)


def local_ip():
    """
    local ip
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def time_count(count):
    """
    time count
    :param count:
    :return:
    """
    return strftime("%H:%M:%S", gmtime(count))


def is_root():
    """
    is root
    :return:
    """
    return os.geteuid() == 0


def is_mac():
    """
    is Mac
    :return:
    """
    return platform.system() == "Darwin"


def my_print(message):
    """
    print
    :param message:
    :return:
    """
    print(Color.green(time.strftime('%Y-%m-%d %H:%M:%S -')), message)


def my_print_red(message):
    """
    print red
    :return:
    """
    print(Color.red(time.strftime('%Y-%m-%d %H:%M:%S -')), Color.red(message))


def my_print_green(message):
    """
    print green
    :return:
    """
    print(Color.green(time.strftime('%Y-%m-%d %H:%M:%S -')), Color.green(message))


class Color(object):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BlUE = '\033[94m'
    END = '\033[0m'

    @classmethod
    def red(cls, string):
        return cls.RED + string + cls.END

    @classmethod
    def green(cls, string):
        return cls.GREEN + string + cls.END

    @classmethod
    def yellow(cls, string):
        return cls.YELLOW + string + cls.END

    @classmethod
    def blue(cls, string):
        return cls.BlUE + string + cls.END

# @Time    : 2018/10/10 下午4:23
# @Author  : SuanCaiYu
# @File    : main
# @Software: PyCharm

import zipfile
import argparse
import logging
from queue import Queue
import threading
import time



# 配置区域

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')

args = argparse.ArgumentParser(description='help')

args.add_argument("-f", "--file_name", help='zip或者rar文件名')
args.add_argument('-d', "--dict_list", help='字典文件名,必选')
args.add_argument('-t', "--thread_count", help='线程数 默认:5')

ARGS = args.parse_args()

lock = threading.Lock()

exit_flag = {"flag": 0}
pwd_queue = Queue()


def check_args(args):
    thread_count = args.thread_count
    if not args.file_name:
        logging.error('需要破解的文件名是必须的')
        exit(0)
    if not args.dict_list:
        logging.error('用于暴力破解的字典是必须的')
        exit(0)
    if not args.thread_count:
        thread_count = 5

    return args.file_name, args.dict_list, thread_count


def open_dict(dict_file):
    with open(dict_file, 'r') as fp:
        return fp.readlines()


def clean_pwd(pwd):
    pwd = pwd.replace("\n", '')
    pwd = pwd.replace("\t", '')
    pwd = pwd.replace("\r", '')
    return pwd


def open_file(filename):
    if '.zip' in file_name:
        zf = zipfile.ZipFile(filename)
    elif '.rar' in file_name:
        zf = rarfile.RarFile(file_name)
    else:
        logging.error('文件非zip或rar')
        exit(0)
    return zf


def ecrypt_zip(password, zf):
    try:
        zf.extractall("./temp", pwd=password)
        print("得到密码:%s" % (password if isinstance(password, str) else password.decode()))
        lock.locked()
        exit_flag['flag'] = 1
        lock.release()
    except:
        pass


def theard_start(zf, tag):
    while True:
        if exit_flag.get('flag') == 1:
            break
        pwd = pwd_queue.get()
        if tag == 1:
            pwd = pwd.encode()
        ecrypt_zip(pwd, zf)
        if pwd_queue.empty():
            break


if __name__ == "__main__":
    file_name, dict_file, thread = check_args(ARGS)
    passwords = open_dict(dict_file)

    s = 1

    if '.rar' in file_name:
        from unrar import rarfile
    for pwd in passwords:
        pwd_queue.put(clean_pwd(pwd))

    zf = open_file(file_name)

    tag = 1 if '.zip' in file_name else 0

    threads = []
    if int(thread) > len(passwords):
        thread = int(len(passwords) / 2)

    for i in range(int(thread)):
        t = threading.Thread(target=theard_start, args=(zf, tag))
        t.start()
        threads.append(t)

    while True:
        print('密码总数:%d,剩余未测试密码数:%d,用时:%d秒' % (len(passwords), pwd_queue.qsize(), s * 5))
        if exit_flag.get('flag') == 1 or pwd_queue.qsize() == 0:
            break
        time.sleep(5)
        s += 1

#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import time
import os


class Log(object):
    '''封装后的logging
    '''

    def __init__(self, logger=None, log_cate='results'):
        '''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d_%H_%M")
        file_dir = os.getcwd() + '/log_'+ str(self.log_time)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        self.log_path = file_dir
        self.log_name = self.log_path + "/" + log_cate + "." + self.log_time + '.log'
        # print(self.log_name)

        self.fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        # fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        self.fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        self.fh.close()
        self.ch.close()

    def getlog(self):
        return self.logger

    def clear(self):
        self.logger.removeHandler(self.ch)
        self.logger.removeHandler(self.fh)
        self.ch = None
        self.fh = None
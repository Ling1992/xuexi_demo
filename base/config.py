# -*- coding: utf-8 -*-
import ConfigParser
import os.path
import threading


class Config(object):

    __instance = None
    __root_dir = u"config/"
    __lock = threading.Lock()
    __cf = ConfigParser.ConfigParser()

    def __init__(self, **kwargs):
        self.read_config(kwargs)
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            try:
                cls.__lock.acquire()
                cls.__instance = object.__new__(cls, *args, **kwargs)
            except Exception, e:
                cls.__lock.release()
                raise Exception(u"读取 配置文件类 初始化 错误 !!  error{}".format(e.message))
                pass
            finally:
                cls.__lock.release()
                pass

        return cls.__instance

    def read_config(self, params):

        for parent, dir_names, file_names in os.walk(self.__root_dir):
            for file_name in file_names:
                file_path = self.__root_dir+file_name
                if self.file_is_ini(file_path):
                    print file_path
                    self.__cf.read(file_path)
            break

        if params.get('file'):
            print params.get('file')
            file_path = self.__root_dir + params.get('file')
            if os.path.exists(file_path):
                if self.file_is_ini(file_path):
                    print file_path
                    self.__cf.read(file_path)

        if params.get('dir'):
            print params.get('dir')
            file_dir = self.__root_dir + params.get('dir') + u"/"
            if os.path.exists(file_dir):
                for parent, dir_names, file_names in os.walk(file_dir):
                    for file_name in file_names:
                        file_path = file_dir + file_name
                        if self.file_is_ini(file_path):
                            print file_path
                            self.__cf.read(file_path)
                    break
        pass

    def file_is_ini(self, path):
        pass
        return os.path.splitext(path)[1] == u'.ini'

    def get_item(self, section, item):
        if self.__cf.has_option(section, item):
            return self.__cf.get(section, item)
        else:
            return None

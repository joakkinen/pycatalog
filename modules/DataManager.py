import time
import sqlite3
import os

from configparser import ConfigParser

class DataManger:
    def __init__(self):
        # cargar archivo de configuracion
        parser = ConfigParser()
        parser.read('conf/main.conf')
        self.db_path_file = parser.get('main', 'db_dir')
        self.db_path_file += '/'
        self.db_path_file += parser.get('main', 'db_file')
        # print(f"{db_path_file}")

        # cear comprobar base de datos
        self.cn = sqlite3.connect(self.db_path_file)
        cursor = self.cn.cursor()
        sql = "create table if not exists tvolume (id integer primary key, name text, root_id integer, date_scan integer);"
        cursor.execute(sql)
        sql = "create table if not exists tdirectory (id integer primary key, name text, pid integer);"
        cursor.execute(sql)
        sql = "create table if not exists tfile (id integer primary key, name text, dir integer, ftype text, size integer, hash text);"
        cursor.execute(sql)
        self.cn.commit()

    def get_next_id(self, table):
        cursor = self.cn.cursor()
        sql = "select max(id) from " + table
        cursor.execute(sql)
        result = cursor.fetchone()
        max = 1
        if result[0] is not None:
            max = result[0] + 1
        return max

    def add_scan_volume(self, name, path):
        ts = int(time.time())

        cursor = self.cn.cursor()
        id_volume = self.get_next_id('tvolume')
        id_root_dir = self.get_next_id('tdirectory')
        sql = "insert into tvolume values (" + str(id_volume) + ",'" + name + "'," + str(id_root_dir) + "," + str(
            ts) + ")"
        cursor.execute(sql)
        sql = "insert into tdirectory values (" + str(id_root_dir) + ",'/',0)"
        cursor.execute(sql)
        self.cn.commit()

        self._scan_dir(id_root_dir, path)

    def _scan_dir(self, id_dir, path):
        ts = int(time.time())
        items = []
        try:
            items = os.listdir(path)
        except PermissionError:
            pass
        cursor = self.cn.cursor()

        # archivos
        for item in items:
            fullpath = path + item
            if os.path.isfile(fullpath):
                print("archivo: " + fullpath)
                new_id = int(self.get_next_id('tfile'))
                sql = "insert into tfile values (" + str(new_id) + ",'" + item.replace('\'', '') + "'," + str(id_dir) + ",'-',0,'-')"
                cursor.execute(sql)
        self.cn.commit()

        # directorios
        for item in items:
            fullpath = path + item
            if os.path.isdir(fullpath):
                print("directorio: " + fullpath)
                new_id = self.get_next_id('tdirectory')
                sql = "insert into tdirectory values (" + str(new_id) + ",'" + item + "'," + str(id_dir) + ")"
                cursor.execute(sql)
                self.cn.commit()
                self._scan_dir(new_id, fullpath + '/')


    def get_list_volumes(self):
        cursor = self.cn.cursor()
        sql = "select id,name from tvolume"
        cursor.execute(sql)
        result = cursor.fetchall()
        list_volumes = []
        for volume in result:
            list_volumes.append(volume)
        return list_volumes

    def get_list_directories(self):
        cursor = self.cn.cursor()
        sql = "select id,name from tdirectory"
        cursor.execute(sql)
        result = cursor.fetchall()
        list_directories = []
        for volume in result:
            list_directories.append(volume)
        return list_directories

    def get_list_files(self):
        cursor = self.cn.cursor()
        sql = "select id,name from tfile"
        cursor.execute(sql)
        result = cursor.fetchall()
        list_files = []
        for volume in result:
            list_files.append(volume)
        return list_files

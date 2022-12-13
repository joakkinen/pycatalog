#!/usr/bin/env python3

# 20220310
#
# todo
# recorrer directorios de manera recursiva
## apuntar el lastscan de los directorios explorados y repetir hasta que no crezca la lista
## o crear clase directorio. haria falta hacer el composite para tener una lista con todos los elementos del mismo tipo
# guardar en base de datos
# cargar datos al inicio de la base de datos
# busquedas

# 20220310
# meter todo en la base de datos desde el primero momento
# hacer funcion que devuelva el siguiente id disponible
# sin clases

import sqlite3
import os

dbpath = 'dbcatalog.db'

# class Volume():
# 	def __init__(self,name,id=-1,pid=-1,path="/",description="",lastscan=0):
# 		self.name=name
# 		self.id=id
# 		self.pid=pid
# 		self.path=path
# 		self.description=description
# 		self.lastscan=0
# 		self.files = []
# 	def toConsole(self):
# 		print(f"vol: id: {self.id} name: {self.name}")
# 		for file in self.files:
# 			file.toConsole()
# 	def add(self,file):
# 		self.files.append(file)

# class File():
# 	def __init__(self,name,type,id=-1,pid=-1,size=-1,date=0,lastscan=0):
# 		self.name=name
# 		self.type=type
# 		self.id=id
# 		self.pid=pid
# 		self.size=size
# 		self.date=date
# 		self.lastscan=lastscan
# 	def toConsole(self):
# 		print(f"file: id: {self.id} name: {self.name}")

def main():
	# start db
	db = sqlite3.connect(dbpath)
	db.execute("CREATE TABLE IF NOT EXISTS File (id int, name varchar, pid int, type int, size real, date datetime )");
	db.commit()

	# get volume data
	vol_name = input("Volume name: ")
	vol_path = input("Volume path: ")
	# insertar volumen
	# recuperar id

	for file in os.listdir(vol_path):
		file_name=file
		file_type='f'
		if os.path.isdir(volume_path+file):
			file_type='d'
		# insertar archivo

	db.commit()
	db.close()
	

if __name__ == '__main__':
	print("begin")
	main()
	print("end")
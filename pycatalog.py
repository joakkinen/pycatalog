from os import listdir,path
from sqlite3 import connect

dbpath = 'dbcatalog.db'
volumes = []
files = []

print('begin')

# types:
# f file
# d directory
# l link

def getnextid(l):
    id=0
    for item in l:
        if id<item['id']:
            id=item['id']
    return id+1

def addnewvolume():
    volume = {}
    volume['id']=getnextid(volumes)
    volume['name']=input('Nombre: ')
    volume['description']=input('Descripcion: ')
    volume['path']=input('Path: ')
    volume['lastscan']=-1
    volumes.append(volume)

    scandirectory(volume['path'],volume['id'],0)

def scandirectory(path_ini,vid,pid):
    items=[]
    try:
        items = listdir(path_ini)
    except PermissionError:
        print(f"{path_ini} Permission Error")
    for item in items:
        path_temp = path_ini+'/'+item
        print(path_temp)
        file = {}
        file['id']=getnextid(files)
        file['pid']=pid
        file['vid']=vid
        file['name']=item
        if path.isdir(path_temp):
            file['type']='d'
        else:
            file['type']='f'
        file['size']=0
        files.append(file)
        if path.isdir(path_temp):
            scandirectory(path_temp,vid,file['id'])

def showfullpath(id):
    pass

def searchfile():
    pattern=input("Search: ")
    for item in files:
        if pattern==item['name']:
            print(item)
            showfullpath(item['id'])

def loaddb():
    db = connect(dbpath)
    db.execute("create table if not exists tvolume (id integer primary key,name text, description text,path text,lastscan integer)")
    db.execute("create table if not exists tfile (id integer primery key, pid integer, vid integer, name text, type text, size integer, date integer)");
    db.commit()

def savedb():
    pass

def showvolumes():
    for volume in volumes:
        print(volume)

# main

loaddb()

opc=-1
while (opc!=0):
    print("Welcome to PyCatalog")
    print("Select your action:")
    print("1. Scan a new volume:")
    print("2. Search a file")
    print("3. Save on db")
    print("4. Show volumes")
    print("0. Quit")
    opc = int(input(": "))
    if opc==1:
        addnewvolume()
    elif opc==2:
        searchfile()
    elif opc==3:
        savedb()
    elif opc==4:
        showvolumes()

print(volumes)
print(files)

print('end')
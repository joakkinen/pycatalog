from os import listdir, path
from sqlite3 import connect, IntegrityError, OperationalError
from tkinter import Tk, ttk

dbpath = 'dbcatalog.db'
volumes = []
files = []

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
    supervolume=input("Super volume [y/n]: ")
    if supervolume=='y':
        volume['path']='/'
        volume['pid']=0
    elif supervolume=='n':
        volume['path']=input('Path: ')                                          # comprobar que existe
        volume['pid']=int(input("Pid: "))
    else:
        exit()
    volume['lastscan']=-1
    volumes.append(volume)

    if supervolume=='n':
        scandirectory(volume['path'],volume['id'],0)

def scandirectory(path_ini,vid,pid):
    items=[]
    try:
        items = listdir(path_ini)
    except PermissionError:
        print(f"{path_ini} Permission Error")
    except OSError:
        print(f"OSError - Trying to continue")
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
    cur=db.cursor()
    cur.execute("select id,pid,name,description,path from tvolume")
    rows = cur.fetchall()
    for item in rows:
        volume = {}
        volume['id']=item[0]
        volume['pid']=item[1]
        volume['name']=item[2]
        volume['description']=item[3]
        volume['path']=item[4]
        volumes.append(volume)
    cur.execute("select id,pid,vid,name,type from tfile")
    rows = cur.fetchall()
    for item in rows:
        file={}
        file['id']=item[0]
        file['pid']=item[1]
        file['vid']=item[2]
        file['name']=item[3]
        file['type']=item[4]
        files.append(file)
    db.close()

def savedb():
    # remove database?
    db = connect(dbpath)
    for volume in volumes:
        try:
            db.execute(f"insert into tvolume (id,pid,name,description,path) values ({volume['id']},{volume['pid']},'{volume['name']}','{volume['description']}','{volume['path']}')")
        except IntegrityError:
            pass
    for file in files:
        try:
            db.execute(f"insert into tfile (id,pid,vid,name,type) values ({file['id']},{file['pid']},{file['vid']},'{file['name']}','{file['type']}')");
        except IntegrityError:
            pass
        except OperationalError:
            pass
    db.commit()
    db.close()

def removedb():
    db = connect(dbpath)
    db.execute("delete from tvolume")
    db.execute("delete from tfile");
    db.commit()
    db.close()

# dar formato
# mostar el contador de archivos
def showvolumes():
    for volume in volumes:
        print(f"id: {volume['id']} pid: {volume['pid']} name: {volume['name']}")

def removevolume():
    volume_id=int(input("Volume id: "))
    
    # borrar de memoria
    for volume in volumes:
        if volume['id']==volume_id:
            volumes.remove(volume)
    for file in files:
        if file['vid']==volume_id:
            files.remove(file)
    
    # borrar de la db
    db = connect(dbpath)
    db.execute(f"delete from tvolume where id={volume_id}")                     # tener en cuenta los super volumenes
    db.execute(f"delete from tfile where vid={volume_id}")
    db.commit()
    db.close()

def gui():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    tree=ttk.Treeview(frm).grid(column=2,row=0)
    tree.insert('', 'end', 'archivo', text="archivo")
    root.mainloop()

# main
print("begin")
loaddb()

opc=-1
opc2=-1
print("Welcome to PyCatalog")
while (opc!=0):
    print("Select your action:")
    print("1. Add a new volume")
    print("2. List volumes")
    print("3. Remove a volume")
    print("4. Search a file")
    print("5. Admin options")
    print("6. GUI")
    print("0. Quit")
    opc = int(input(": "))
    if opc==1:
        addnewvolume()
    elif opc==2:
        showvolumes()
    elif opc==3:
        removevolume()
    elif opc==4:
        searchfile()
    elif opc==5:
        while opc2!=0:
            print("Select your action:")
            print("1. Load data from database")
            print("2. Save data to database")
            print("3. Remove database")
            print("4. Show current data")
            print("5. Remove current data")
            print("0. Back to main menu")
            opc2 = int(input(": "))                                             # comprobar que no se inserta vacio
            if opc2==1:
                loaddb()
            elif opc2==2:
                savedb()
            elif opc2==3:
                removedb()
            elif opc2==4:
                print(volumes)
                #print(files)
            elif opc2==5:
                volumes = []
                files = []
        opc2=-1
    elif opc==6:
        gui()

print('end')
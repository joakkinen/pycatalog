from modules.DataManager import DataManger


def manage_volumenes_menu():
    opc = -1
    while opc != 0:
        print("1. Añadir y escanear un volumen nuevo.")
        print("2. Ver listado de volúmenes.")
        print("3. Borrar un volumen.")
        print("4. Actualizar un volumen existente.")
        print("0. Volver al menu principal.")
        opc = int(input(": "))
        match opc:
            case 1:
                add_scan_volume()
            case 2:
                list_volumes()
            case 3:
                search_file()
            case 4:
                # TODO: mostar una lista. seleccionar el id. escanear.
                pass


def add_scan_volume():
    dm = DataManger()
    name = input("Nombre: ")
    path = input("Path: ")
    dm.add_scan_volume(name, path)

    print(f"Volumen añadido.")


def list_volumes():
    dm = DataManger()
    print("Lista de volumenes (id, nombre):")
    list_volumes = dm.get_list_volumes()
    for volume in list_volumes:
        print(f"id: {volume[0]} - nombre: {volume[1]}")


def search_file():
    dm = DataManger()
    print("Búsqueda de archivos.")
    

# def find_duplicates():
#     pass
#

def main():
    print("begin")

    opc = -1
    while opc != 0:
        print("Opciones:")
        print("1. Gestión de volúmenes.")
        print("2. Buscar un archivo.")
        print("3. Encontrar duplicados.")
        print("4. Organizar volúmenes")
        print("0. Salir")
        opc = int(input(": "))
        match opc:
            case 1:
                manage_volumenes_menu()
            case 2:
                # search_file()
                pass
            case 3:
                # find_duplicates()
                pass
            case 4:
                pass
            case _:
                print(f"Pasó algo raro")

    print('end')


if __name__ == "__main__":
    main()

from src.index import *

menu = [
    "Alta de proveedor",
    "Baja de proveedor",
    "Modificación de proveedor",
    "Listar proveedores",
    "Carga de compras de proveedor",
    "Listado de monto de las compras de cada proveedor",
    "Edición de monto de las compras",
    "Listados de proveedores con mayor suma de compras registradas",
]
funciones = [
    "registrarProveedor",
    "borrarProveedor",
    "modificarProveedor",
    "listarProveedores",
    "cargarCompras",
    "listarComprasProveedor",
    "editarMonto",
    "listarProveedoresConMayoresCompras",
]


def mostrarMenu(menu):
    try:
        for i in range(len(menu)):
            print(str(i + 1) + ". " + menu[i])

        userInput = int(input("\nIngrese el número de opción: "))

        while userInput < 0 or userInput > len(menu):
            print("Opción inválida")
            userInput = int(input("\nIngrese el número de opción: "))

        return userInput

    except Exception as e:
        return e


def main():
    try:
        userInput = mostrarMenu(menu)

        while userInput != 0:
            eval(funciones[userInput - 1] + "()")
            print("\n")
            userInput = mostrarMenu(menu)

    except ValueError:
        print("Error: Ingrese un número válido.")
        main()
    except IndexError:
        print("Error: Opción inválida.")
        main()
    except Exception as e:
        print(f"Error desconocido: {e}")
        main()


main()

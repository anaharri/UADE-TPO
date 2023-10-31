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

# POR AHORA NADA TIENE VALIDACIONES NI MANEJO DE EXCEPCIONES
# Solamente definí el menú, la función main, y la función de alta (con un par de funciones auxiliares). Más adelante podemos dedicar un ratito a modularizar todo


# Tomar input del usuario
def ingresarDatos():
    CUIT = input("Ingrese número de CUIT (sólo números y guiones): ")
    nombre = input("Ingrese nombre: ")

    CUIT = CUIT.rjust(10, "0")
    nombre = nombre.ljust(25, " ")

    return CUIT, nombre


# Buscar un registro en el archivo antes de guardar datos nuevos
def buscarRegistro(archivo, CUIT):
    archivo.seek(0)
    linea = archivo.readline()
    registroEncontrado = False

    while linea and not registroEncontrado:
        CUITleido = linea.split(",")[0]
        if CUITleido == CUIT:
            registroEncontrado = True
        else:
            linea = archivo.readline()

    return registroEncontrado


# Guardar nuevo proveedor
def registrarProveedor():
    nuevoCUIT, nuevoNombre = ingresarDatos()
    archivo = open("Proveedores.csv", "a+t")

    if buscarRegistro(archivo, nuevoCUIT) == False:
        # las columnas del CSV son: CUIT, nombre, estado
        nuevoRegistro = str(nuevoCUIT) + "," + nuevoNombre + "," + "1"
        archivo.write(nuevoRegistro + "\n")
        archivo.close()
        print("Nuevo proveedor registrado")
    else:
        print("El CUIT ingresado ya se encuentra registrado.")


def borrarProveedor(CUIT):
    pass


def modificarProveedor(CUIT, nombre):
    # acá el archivo se tiene que abrir en modo "r+"
    # para que te permita leer Y escribir. O sea así:
    # archivo = open("Proveedores.csv", "r+t")
    pass


def listarProveedores():
    archivo = open("Proveedores.csv", "rt")

    for linea in archivo:
        linea = linea.rstrip("\n")
        lista = linea.split(",")
        print(lista)
        # if estado != "0":
        #     print(CUIT + " - " + nombre)


def cargarCompras(CUIT):
    pass


def listarComprasProveedor():
    pass


def editarMonto(CUIT, claveDeCompra):
    pass


def listarProveedoresConMayoresCompras():
    pass


def mostrarMenu(menu):
    for i in range(len(menu)):
        print(str(i + 1) + ". " + menu[i])

    userInput = int(input("\nIngrese el número de opción: "))

    while userInput < 0 or userInput >= len(menu):
        print("Opción inválida")
        userInput = int(input("\nIngrese el número de opción: "))

    return userInput


def main():
    userInput = mostrarMenu(menu)

    while userInput != 0:
        eval(funciones[userInput - 1] + "()")
        print("\n")
        userInput = mostrarMenu(menu)


main()

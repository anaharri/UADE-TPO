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

    CUIT = CUIT.strip().rjust(15, "0")
    nombre = nombre.strip().ljust(25, " ")

    return CUIT, nombre


# Buscar un registro en el archivo antes de guardar datos nuevos
def buscarRegistro(archivo, CUIT):
    archivo.seek(0)
    linea = archivo.readline()
    registroEncontrado = False

    while linea and not registroEncontrado:
        estadoLeido, CUITleido, *rest = linea.split(",")
        if CUITleido == CUIT and estadoLeido == "1":
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
        nuevoRegistro = f"1,{nuevoCUIT},{nuevoNombre},\n"
        archivo.write(nuevoRegistro)
        print("Nuevo proveedor registrado")
    else:
        print("El CUIT ingresado ya se encuentra registrado.")
    archivo.close()


# Borra un proveedor pasando por parametro el CUIT
def borrarProveedor():
    archivo = open("Proveedores.csv", "r+t")
    CUIT = input("Ingrese el CUIT: ")
    CUIT = CUIT.rjust(15, "0")

    posicionAnterior = 0
    linea = archivo.readline()
    registroEncontrado = False

    while linea and not registroEncontrado:
        cEstado, cCUIT, cNombre, *cCompras = linea.split(",")
        cCompras = cCompras[-1].strip("\n")

        if CUIT == cCUIT and cEstado == "1":
            registroEncontrado = True
            cLinea = f"0,{cCUIT},{cNombre},{cCompras}\n"

        else:
            posicionAnterior = archivo.tell()

        linea = archivo.readline()

    if registroEncontrado:
        archivo.seek(posicionAnterior)
        archivo.write(cLinea)
        print("Registro borrado correctamente")

    else:
        print("Legajo no encontrado o dado de baja")

    archivo.close()


def modificarProveedor():
    archivo = open("Proveedores.csv", "r+t")
    CUIT, nombre = ingresarDatos()

    posicionAnterior = 0
    linea = archivo.readline()
    registroEncontrado = False

    while linea and not registroEncontrado:
        cEstado, cCUIT, cNombre, *cCompras = linea.split(",")
        cCompras= cCompras[-1].strip("\n")

        if CUIT == cCUIT and cEstado == "1":
            registroEncontrado = True
            cLinea = f"{cEstado},{cCUIT},{nombre},{cCompras}\n"

        else:
            posicionAnterior = archivo.tell()
        linea = archivo.readline()

    if registroEncontrado:
        archivo.seek(posicionAnterior)
        archivo.write(cLinea)
        print("Registro editado exitosamente")
    else:
        print("CUIT no encontrado o dado de baja")

    archivo.close()


def listarProveedores():
    archivo = open("Proveedores.csv", "rt")

    print("Lista de proveedores:")
    for linea in archivo:
        linea = linea.rstrip("\n")
        estado, CUIT, nombre, *_ = linea.split(",")

        if estado == "1":
            print(CUIT + " | " + nombre)


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

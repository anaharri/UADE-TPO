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
    CUIT = input("Ingrese número de CUIT (sólo números): ")
    nombre = input("Ingrese nombre: ")

    CUIT = CUIT.strip().rjust(15, "0")
    nombre = nombre.strip().ljust(25, " ")

    return CUIT, nombre


# Buscar un registro en el archivo antes de guardar datos nuevos
def buscarRegistro(archivo, CUIT):
    archivo.seek(0)

    posicionAnterior = 0
    linea = archivo.readline()
    registroEncontrado = False

    while linea and not registroEncontrado:
        estadoLeido, CUITleido, *_ = linea.split(",")
        if estadoLeido == "1" and CUITleido == CUIT:
            registroEncontrado = True
            return posicionAnterior
        else:
            posicionAnterior = archivo.tell()

        linea = archivo.readline()

    return registroEncontrado


# Guardar nuevo proveedor
def registrarProveedor():
    nuevoCUIT, nuevoNombre = ingresarDatos()
    archivo = open("Proveedores.csv", "a+t")

    if buscarRegistro(archivo, nuevoCUIT) == False:
        # las columnas del CSV son: estado, CUIT, nombre
        nuevoRegistro = "1" + "," + nuevoCUIT + "," + nuevoNombre
        archivo.write(nuevoRegistro.ljust(200, " ") + "\n")
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
        cCompras = cCompras[-1].strip("\n")

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
    dicCuits = {}

    print("Lista de proveedores:")
    for linea in archivo:
        linea = linea.rstrip("\n")
        estado, CUIT, nombre, *_ = linea.split(",")
        if estado == "1":
            dicCuits.update({CUIT: nombre})
    dicCuits = dict(sorted(dicCuits.items()))

    for key, value in dicCuits.items():
        print(key + " | " + value)

    archivo.close()


def cargarCompras():
    archivo = open("Proveedores.csv", "r+t")
    CUIT = input("Ingrese número de CUIT (sólo números): ")
    posicionRegistro = buscarRegistro(archivo, CUIT)

    while posicionRegistro is False and CUIT != -1:
        print("CUIT no encontrado o dado de baja")
        CUIT = input("Ingrese número de CUIT (sólo números): ")
        posicionRegistro = buscarRegistro(archivo, CUIT)

    if CUIT == -1:
        return

    compra = input(
        "Ingrese el monto de la compra del proveedor " + CUIT + " (sólo números): $"
    )

    archivo.seek(posicionRegistro)
    registro = archivo.readline()
    registro = registro.rstrip() + "," + compra
    registro = registro.ljust(200, " ") + "\n"
    archivo.seek(posicionRegistro)
    archivo.write(registro)

    print("Compra registrada exitosamente")
    archivo.close()


def listarComprasProveedor():
    archivo = open("Proveedores.csv", "r+t")
    diccionarioDeProveedores = {}

    for linea in archivo:
        linea = linea.rstrip("\n")
        estado, CUIT, nombre, *compras = linea.split(",")
        if estado == "1":
            diccionarioDeProveedores[CUIT.lstrip("0")] = {
                "nombre": nombre.rstrip(),
                "compras": compras,
            }

    diccionarioDeProveedores = dict(sorted(diccionarioDeProveedores.items()))

    for CUIT in diccionarioDeProveedores:
        print(CUIT + " | " + diccionarioDeProveedores[CUIT]["nombre"])
        print("Monto de las compras:")
        for compra in diccionarioDeProveedores[CUIT]["compras"]:
            print(compra.rstrip(" "))
        print()

    archivo.close()


# Impresentable este código pero bue lo subo así y después le metemos refactor furioso
def editarMonto():
    diccionarioDeCompras = {}

    archivo = open("Proveedores.csv", "r+t")
    CUIT = input("Ingrese el CUIT: ")
    indiceRegistro = buscarRegistro(archivo, CUIT)

    if indiceRegistro is False:
        print("Proveedor no encontrado")
        return

    archivo.seek(indiceRegistro)
    estado, CUIT, nombre, *compras = archivo.readline().split(",")

    for i in range(len(compras)):
        diccionarioDeCompras[i + 1] = compras.pop(0).strip()
        print(str(i + 1) + ": " + diccionarioDeCompras[i + 1])

    indiceDeCompra = int(
        input("Ingrese el número de compra que desea modificar, o 0 para terminar: ")
    )

    while indiceDeCompra:
        nuevoMonto = input(f"Ingrese nuevo monto para la compra {indiceDeCompra}: ")
        diccionarioDeCompras[indiceDeCompra] = nuevoMonto
        print("\nCompra modificada exitosamente.\n")
        indiceDeCompra = int(
            input(
                "Ingrese el número de compra que desea modificar, o 0 para terminar: "
            )
        )

    nuevoRegistro = f"{estado},{CUIT},{nombre}"

    for i in diccionarioDeCompras:
        nuevoRegistro = nuevoRegistro + "," + diccionarioDeCompras[i]

    archivo.seek(indiceRegistro)
    archivo.write(nuevoRegistro.ljust(200, " ") + "\n")
    archivo.close()

# idem punto anterior, el código es feo pero cumple su función
def listarProveedoresConMayoresCompras():
    archivo = open("Proveedores.csv", "r+t")
    diccionarioDeProveedores = {}
    compraMaxima = 0

    for linea in archivo:
        linea = linea.rstrip("\n")
        estado, CUIT, nombre, *compras = linea.split(",")
        totalDeCompras = 0

        if estado == "1":
            for compra in compras:
                totalDeCompras += int(compra.strip())

            if totalDeCompras > compraMaxima:
                compraMaxima = totalDeCompras

            diccionarioDeProveedores[CUIT.lstrip("0")] = {
                "nombre": nombre.rstrip(),
                "totalDeCompras": totalDeCompras,
            }

    print("Compra máxima: " + str(compraMaxima))
    for CUIT in diccionarioDeProveedores:
        if diccionarioDeProveedores[CUIT]["totalDeCompras"] == compraMaxima:
            print(
                f"{CUIT} | {diccionarioDeProveedores[CUIT]['nombre']} | Suma de compras: {compraMaxima}"
            )

    archivo.close()


def mostrarMenu(menu):
    for i in range(len(menu)):
        print(str(i + 1) + ". " + menu[i])

    userInput = int(input("\nIngrese el número de opción: "))

    while userInput < 0 or userInput > len(menu):
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
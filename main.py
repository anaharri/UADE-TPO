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


# Función auxiliar
# Tomar input del usuario
def ingresarDatos():
    validacionExitosa = False

    while not validacionExitosa:
        try:
            cuit = input("Ingrese número de CUIT (sólo números, máximo 15 dígitos): ")
            cuit = cuit.strip().rjust(15, "0")

            if not cuit.isdigit() or len(cuit) > 15:
                raise ValueError(
                    "El CUIT debe contener solo números y tener como máximo 15 dígitos."
                )

            nombreIngresado = input(
                "Ingrese nombre (solo letras y espacios, máximo 25 caracteres): "
            )

            # Eliminar espacios adicionales y reemplazar múltiples espacios con uno solo
            nombre = " ".join(nombreIngresado.split())

            # Verificar que los caracteres son alfabéticos y no se pasa de 25 caracteres
            if not nombre.replace(" ", "").isalpha() or len(nombre) > 25:
                raise ValueError(
                    "El nombre debe contener solo letras y espacios y tener como máximo 25 caracteres."
                )

            # Restaurar el valor original
            nombre = nombre.strip().ljust(25, " ")

            validacionExitosa = True

        except ValueError as e:
            print(f"Error: {e}. Intente nuevamente.")

    return cuit, nombre


# Función auxiliar
# Buscar un registro en el archivo antes de guardar datos nuevos
def buscarRegistro(archivo, CUIT):
    try:
        archivo.seek(0)

        posicionAnterior = -1
        linea = archivo.readline()
        registroEncontrado = False

        while linea and not registroEncontrado:
            estadoLeido, CUITleido, *_ = linea.split(",")

            if estadoLeido == "1" and CUITleido.lstrip("0") == CUIT.lstrip("0"):
                registroEncontrado = True

            posicionAnterior = archivo.tell()
            linea = archivo.readline()

        return posicionAnterior

    except Exception as e:
        print(f"Error al buscar el registro: {e}")
        return False


# Función auxiliar
def borradoLogico(archivo, posicion):
    try:
        archivo.seek(posicion)
        registro = archivo.readline()

        campos = registro.split(",")[1,]
        registro = f"0,{','.join(campos)}"

        archivo.seek(posicion)
        archivo.write(registro)

    except Exception as e:
        return e


# Guardar nuevo proveedor
def registrarProveedor():
    try:
        nuevoCUIT, nuevoNombre = ingresarDatos()
        archivo = open("Proveedores.csv", "a+t")

        if buscarRegistro(archivo, nuevoCUIT) == -1:
            nuevoRegistro = "1" + "," + nuevoCUIT + "," + nuevoNombre + ","
            archivo.write(nuevoRegistro.ljust(200, " ") + "\n")
            print("Nuevo proveedor registrado")
        else:
            print("El CUIT ingresado ya se encuentra registrado.")

    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error al abrir el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al registrar el proveedor: {e}")

    finally:
        archivo.close()


# Borra un proveedor
def borrarProveedor():
    try:
        archivo = open("Proveedores.csv", "r+t")
        CUIT = input("Ingrese el CUIT: ")

        # Aserciones para validar el formato del CUIT
        assert CUIT.isdigit(), "El CUIT debe contener solo números."
        assert len(CUIT) <= 15, "El CUIT no puede superar los 15 dígitos."

        CUIT = CUIT.rjust(15, "0")

        posicionRegistro = buscarRegistro(archivo, CUIT)

        if posicionRegistro != -1:
            borradoLogico(archivo, posicionRegistro)
            print("Registro borrado correctamente")
        else:
            print("Legajo no encontrado o dado de baja")

    except AssertionError as ae:
        print(f"Error de validación: {ae}")
    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura/escritura en el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al borrar el proveedor: {e}")

    finally:
        archivo.close()


# Modifica el nombre del provedor
def modificarProveedor():
    try:
        archivo = open("Proveedores.csv", "r+t")
        CUIT, nombre = ingresarDatos()
        posicionRegistro = buscarRegistro(archivo, CUIT)

        if posicionRegistro == -1:
            print("CUIT no encontrado o dado de baja")
        else:
            archivo.seek(posicionRegistro)
            registro = archivo.readline()

            compras = registro.split(",")[3,]
            registroActualizado = f"1,{CUIT},{nombre},{','.join(compras)}"
            archivo.write(registroActualizado)

            print("Registro editado exitosamente")

    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura/escritura en el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al editar el proveedor: {e}")

    finally:
        archivo.close()


# Ordena los proveedores por numero de cuit ascendente
def listarProveedores():
    try:
        archivo = open("Proveedores.csv", "rt")
        dicCuits = {}

        print("Lista de proveedores:")
        for linea in archivo:
            try:
                linea = linea.rstrip("\n")
                estado, CUIT, nombre, *_ = linea.split(",")
                if estado == "1":
                    dicCuits.update({CUIT: nombre})
            except ValueError as ve:
                print(f"Error al procesar línea: {ve}")

        dicCuits = dict(sorted(dicCuits.items()))

        for key, value in dicCuits.items():
            print(key + " | " + value)

    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura en el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al listar proveedores: {e}")

    finally:
        archivo.close()


# Carga las compras para el CUIT dado
def cargarCompras():
    try:
        archivo = open("Proveedores.csv", "r+t")
        CUIT = input("Ingrese número de CUIT (sólo números): ")
        # Aserciones para validar el formato del CUIT
        assert CUIT.isdigit(), "El CUIT debe contener solo números."
        assert len(CUIT) <= 15, "El CUIT no puede superar los 15 dígitos."

        posicionRegistro = buscarRegistro(archivo, CUIT)

        while posicionRegistro is False and CUIT != "-1":
            print("CUIT no encontrado o dado de baja")
            CUIT = input("Ingrese número de CUIT (sólo números): ")
            # Aserciones para validar el formato del CUIT
            assert CUIT.isdigit(), "El CUIT debe contener solo números."
            assert len(CUIT) <= 15, "El CUIT no puede superar los 15 dígitos."
            posicionRegistro = buscarRegistro(archivo, CUIT)

        if CUIT != "-1":
            compra = input(
                f"Ingrese el monto de la compra del proveedor {CUIT} (sólo números): $"
            )
            # Aserciones para validar el formato del monto de la compra
            assert compra.isdigit(), "El monto de la compra debe contener solo números."
            assert (
                "." not in compra
            ), "El monto de la compra no debe contener decimales."

            archivo.seek(posicionRegistro)
            registro = archivo.readline()
            registro = registro.rstrip() + "," + compra
            registro = registro.ljust(200, " ") + "\n"
            archivo.seek(posicionRegistro)
            archivo.write(registro)

            print("Compra registrada exitosamente")

    except AssertionError as ae:
        print(f"Error de validación: {ae}")
    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura/escritura en el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al cargar compras: {e}")

    finally:
        archivo.close()


# Lista una por una las compras del proveedor
def listarComprasProveedor():
    try:
        archivo = open("Proveedores.csv", "rt")
        diccionarioDeProveedores = {}

        for linea in archivo:
            try:
                linea = linea.rstrip("\n")
                estado, CUIT, nombre, *compras = linea.split(",")
                if estado == "1":
                    diccionarioDeProveedores[CUIT.lstrip("0")] = {
                        "nombre": nombre.rstrip(),
                        "compras": compras,
                    }
            except ValueError as ve:
                print(f"Error al procesar línea: {ve}")

        diccionarioDeProveedores = dict(sorted(diccionarioDeProveedores.items()))

        print("Listado de compras por proveedor:")
        print()

        for CUIT in diccionarioDeProveedores:
            print(f"{'CUIT'.ljust(15, ' ')} | Nombre")
            print(f"{CUIT.rjust(15, '0')} | {diccionarioDeProveedores[CUIT]['nombre']}")
            print("Monto de las compras:")
            for compra in diccionarioDeProveedores[CUIT]["compras"]:
                print(compra.rstrip(" "))
            print()

    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura en el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al listar compras de proveedores: {e}")

    finally:
        archivo.seek(0)
        archivo.close()


# edita el monto de las compras de un proveedor particular
def editarMonto():
    try:
        diccionarioDeCompras = {}
        archivo = open("Proveedores.csv", "r+t")

        CUIT = input("Ingrese el CUIT: ")

        # Asegúrate de que el CUIT sea válido
        assert CUIT.isdigit(), "El CUIT debe contener solo números."
        assert len(CUIT) <= 15, "El CUIT no puede superar los 15 dígitos."

        indiceRegistro = buscarRegistro(archivo, CUIT)

        if indiceRegistro is False:
            print("Proveedor no encontrado")
            return

        archivo.seek(indiceRegistro)
        estado, CUIT, nombre, *compras = archivo.readline().split(",")

        for i, compra in enumerate(compras, start=1):
            diccionarioDeCompras[i] = compra.strip()
            print(f"{i}: {diccionarioDeCompras[i]}")

        indiceDeCompra = int(
            input(
                "Ingrese el número de compra que desea modificar, o 0 para terminar: "
            )
        )

        # Verifica que el indice de compra este en el diccionario y sea valida
        while indiceDeCompra and indiceDeCompra not in diccionarioDeCompras:
            print(
                "Índice de compra no válido. Por favor, ingrese un número de compra existente."
            )
            try:
                indiceDeCompra = int(
                    input(
                        "Ingrese el número de compra que desea modificar, o 0 para terminar: "
                    )
                )
            except ValueError:
                print("Por favor, ingrese un número válido.")

        while indiceDeCompra:
            try:
                nuevoMonto = float(
                    input(f"Ingrese nuevo monto para la compra {indiceDeCompra}: ")
                )
                assert nuevoMonto >= 0, "El monto debe ser mayor o igual a cero."

                diccionarioDeCompras[indiceDeCompra] = nuevoMonto
                print("\nCompra modificada exitosamente.\n")
            except ValueError:
                print("Por favor, ingrese un número válido.")
            except AssertionError as ae:
                print(f"Error de validación: {ae}")

            indiceDeCompra = int(
                input(
                    "Ingrese el número de compra que desea modificar, o 0 para terminar: "
                )
            )

        nuevoRegistro = f"{estado},{CUIT},{nombre}"

        for i in diccionarioDeCompras:
            nuevoRegistro += f",{diccionarioDeCompras[i]}"

        archivo.seek(indiceRegistro)
        archivo.write(nuevoRegistro.ljust(200, " ") + "\n")

    except ValueError as ve:
        print(f"Error: {ve}")
    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura/escritura en el archivo: {ose}")
    except (IndexError, KeyError) as e:
        print(f"Error al acceder al diccionario de compras: {e}")
    except Exception as e:
        print(f"Error desconocido al editar el proveedor: {e}")

    finally:
        archivo.close()


# Ordena los proveedores con mayor capital de compras
def listarProveedoresConMayoresCompras():
    try:
        archivo = open("Proveedores.csv", "r+t")
        diccionarioDeProveedores = {}
        compraMaxima = 0

        for linea in archivo:
            try:
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

            except ValueError as ve:
                print(f"Error al procesar línea: {ve}")

        if not diccionarioDeProveedores:
            print("No hay proveedores disponibles.")

        else:
            print("Compra máxima: " + str(compraMaxima))
            for CUIT in diccionarioDeProveedores:
                if diccionarioDeProveedores[CUIT]["totalDeCompras"] == compraMaxima:
                    print(
                        f"{CUIT} | {diccionarioDeProveedores[CUIT]['nombre']} | Suma de compras: {compraMaxima}"
                    )

    except FileNotFoundError as fnfe:
        print(f"Error: Archivo no encontrado: {fnfe}")
    except OSError as ose:
        print(f"Error de lectura/escritura en el archivo: {ose}")
    except Exception as e:
        print(f"Error desconocido al listar proveedores con mayores compras: {e}")

    finally:
        archivo.close()


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

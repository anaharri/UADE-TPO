# Tomar input del usuario
def ingresarDatos():
    validacionExitosa = False

    while not validacionExitosa:
        try:
            CUIT = input(
                "Ingrese número de CUIT (sólo números, máximo 15 dígitos): ")
            CUIT = CUIT.strip().rjust(15, "0")

            if not CUIT.isdigit() or len(CUIT) > 15:
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

    return CUIT, nombre

# Buscar un registro en el archivo antes de guardar datos nuevos


def buscarRegistro(archivo, CUIT):
    try:
        archivo.seek(0)
        posicionAnterior = 0
        linea = archivo.readline()
        registroEncontrado = False

        while linea and not registroEncontrado:
            estadoLeido, CUITleido, *_ = linea.split(",")

            if estadoLeido == "1" and CUITleido.lstrip("0") == CUIT.lstrip("0"):
                registroEncontrado = True
            else:
                posicionAnterior = archivo.tell()

            linea = archivo.readline()

        if registroEncontrado is False:
            posicionAnterior = -1

        return posicionAnterior

    except Exception as e:
        print(f"Error al buscar el registro: {e}")
        return False


def borradoLogico(archivo, posicion):
    try:
        archivo.seek(posicion)
        registro = archivo.readline()

        campos = registro.split(",")
        registro = f"0{','.join(campos)[1:]}"

        archivo.seek(posicion)
        archivo.write(registro)

    except Exception as e:
        return e

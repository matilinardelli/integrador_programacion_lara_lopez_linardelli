import csv

RUTA_CSV = "paises.csv"
COLUMNAS_CSV = ["nombre", "continente", "poblacion", "superficie", "capital"]
CONTINENTES_VALIDOS = {"America", "Africa", "Asia", "Europa", "Oceania", "Antartida"}


# ============================================================
# VALIDACIONES
# ============================================================
# Todas devuelven una tupla (es_valido: bool, dato_o_mensaje) para
# que quien las llama decida qué hacer, sin que estas funciones
# impriman nada por su cuenta.

def validar_campo_no_vacio(valor, nombre_campo):
    """Controla que un campo de texto no esté vacío ni sea solo espacios."""
    if valor is None or str(valor).strip() == "":
        return False, f"El campo '{nombre_campo}' no puede estar vacío."
    return True, ""


def validar_continente(continente):
    """Controla que el continente ingresado sea uno de los válidos."""
    es_valido, mensaje = validar_campo_no_vacio(continente, "Continente")
    if not es_valido:
        return False, mensaje

    continente_normalizado = continente.strip().title()
    if continente_normalizado not in CONTINENTES_VALIDOS:
        return False, (
            f"'{continente}' no es un continente válido. "
            f"Opciones: {', '.join(sorted(CONTINENTES_VALIDOS))}."
        )
    return True, ""


def validar_numero_positivo(valor, nombre_campo):
    """
    Controla que un valor (población o superficie) sea numérico y
    mayor a 0. Si es válido, devuelve el número ya convertido a float
    (listo para usar), en vez del mensaje vacío.
    """
    try:
        numero = float(valor)
    except (ValueError, TypeError):
        return False, f"El campo '{nombre_campo}' debe ser un número."

    if numero <= 0:
        return False, f"El campo '{nombre_campo}' debe ser mayor a 0."

    return True, numero


def validar_pais_nuevo(nombre, continente, poblacion, superficie, capital):
    """
    Validación completa para agregar un país nuevo. Devuelve
    (True, diccionario_pais) si todo está bien, o (False, mensaje)
    apenas encuentra el primer error.
    """
    es_valido, mensaje = validar_campo_no_vacio(nombre, "Nombre")
    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_campo_no_vacio(capital, "Capital")
    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_continente(continente)
    if not es_valido:
        return False, mensaje

    es_valido, resultado = validar_numero_positivo(poblacion, "Población")
    if not es_valido:
        return False, resultado
    poblacion_num = resultado

    es_valido, resultado = validar_numero_positivo(superficie, "Superficie")
    if not es_valido:
        return False, resultado
    superficie_num = resultado

    pais = {
        "nombre": nombre.strip(),
        "continente": continente.strip().title(),
        "poblacion": int(poblacion_num),
        "superficie": superficie_num,
        "capital": capital.strip(),
    }
    return True, pais


def validar_actualizacion(poblacion_nueva, superficie_nueva):
    """Validación para la opción de actualizar población y superficie."""
    es_valido, resultado = validar_numero_positivo(poblacion_nueva, "Población")
    if not es_valido:
        return False, resultado

    es_valido, resultado2 = validar_numero_positivo(superficie_nueva, "Superficie")
    if not es_valido:
        return False, resultado2

    return True, (int(resultado), resultado2)


def validar_rango(minimo, maximo, nombre_campo):
    """Controla un rango numérico (para filtrar por población o superficie)."""
    try:
        min_num = float(minimo)
        max_num = float(maximo)
    except (ValueError, TypeError):
        return False, f"El rango de {nombre_campo} debe contener solo números."

    if min_num < 0 or max_num < 0:
        return False, f"El rango de {nombre_campo} no admite valores negativos."

    if min_num > max_num:
        return False, f"El valor mínimo de {nombre_campo} no puede ser mayor que el máximo."

    return True, (min_num, max_num)


def hay_resultados(lista_resultados):
    """Evita mostrar una lista vacía sin avisar cuando una búsqueda no encuentra nada."""
    if not lista_resultados:
        return False, "No se encontraron países que cumplan ese criterio."
    return True, f"Se encontraron {len(lista_resultados)} resultado(s)."


def validar_encabezado_csv(fieldnames):
    """Controla que el CSV tenga todas las columnas esperadas antes de leer filas."""
    if fieldnames is None:
        return False, "El archivo CSV está vacío o no se pudo leer el encabezado."

    columnas_presentes = {columna.strip().lower() for columna in fieldnames}
    columnas_faltantes = set(COLUMNAS_CSV) - columnas_presentes

    if columnas_faltantes:
        return False, f"Al CSV le faltan las columnas: {', '.join(columnas_faltantes)}."
    return True, ""


def validar_fila_csv(fila, numero_fila):
    """Valida que una fila del CSV tenga todos los datos completos y numéricos."""
    campos_vacios = [
        campo for campo in COLUMNAS_CSV
        if not fila.get(campo, "").strip()
    ]
    if campos_vacios:
        return False, f"Fila {numero_fila}: faltan datos en {', '.join(campos_vacios)}."

    es_valido, resultado = validar_numero_positivo(fila["poblacion"], "Población")
    if not es_valido:
        return False, f"Fila {numero_fila}: {resultado}"

    es_valido, resultado = validar_numero_positivo(fila["superficie"], "Superficie")
    if not es_valido:
        return False, f"Fila {numero_fila}: {resultado}"

    return True, ""


# ============================================================
# LECTURA Y ESCRITURA DE CSV
# ============================================================

def leer_paises_desde_csv(ruta_archivo):
    """
    Lee el CSV completo y devuelve (lista_paises, lista_errores).
    Las filas inválidas se descartan una por una sin frenar la carga
    del resto, y los problemas graves (archivo faltante, encabezado
    incompleto) se informan sin romper el programa.
    """
    paises = []
    errores = []

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)

            es_valido, mensaje = validar_encabezado_csv(lector.fieldnames)
            if not es_valido:
                errores.append(mensaje)
                return paises, errores

            for numero_fila, fila in enumerate(lector, start=2):
                es_valido, mensaje = validar_fila_csv(fila, numero_fila)
                if not es_valido:
                    errores.append(mensaje)
                    continue

                pais = {
                    "nombre": fila["nombre"].strip(),
                    "continente": fila["continente"].strip().title(),
                    "poblacion": int(float(fila["poblacion"])),
                    "superficie": float(fila["superficie"]),
                    "capital": fila["capital"].strip(),
                }
                paises.append(pais)

    except FileNotFoundError:
        errores.append(f"No se encontró el archivo '{ruta_archivo}'.")
    except UnicodeDecodeError:
        errores.append(f"El archivo '{ruta_archivo}' tiene un problema de codificación (probá UTF-8).")
    except Exception as error:
        errores.append(f"Error inesperado al leer el CSV: {error}")

    return paises, errores


def guardar_paises(ruta_archivo, paises):
    """Escribe la lista completa de países al CSV, sobreescribiéndolo."""
    try:
        with open(ruta_archivo, mode="w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_CSV)
            escritor.writeheader()
            escritor.writerows(paises)
        return True, f"Datos guardados correctamente en '{ruta_archivo}'."
    except Exception as error:
        return False, f"Error al guardar el archivo: {error}"


# ============================================================
# ALTA Y ACTUALIZACIÓN
# ============================================================

def agregar_pais(paises):
    """Pide los datos de un país nuevo por teclado, lo valida y lo agrega a la lista."""
    print("\n--- Agregar país ---")
    nombre = input("Nombre: ")
    continente = input("Continente (America/Africa/Asia/Europa/Oceania/Antartida): ")
    poblacion = input("Población: ")
    superficie = input("Superficie (km2): ")
    capital = input("Capital: ")

    es_valido, resultado = validar_pais_nuevo(nombre, continente, poblacion, superficie, capital)
    if not es_valido:
        print(f"Error: {resultado}")
        return

    for pais in paises:
        if pais["nombre"].lower() == resultado["nombre"].lower():
            print(f"Error: ya existe un país cargado con el nombre '{resultado['nombre']}'.")
            return

    paises.append(resultado)
    print(f"País '{resultado['nombre']}' agregado con éxito.")


def actualizar_poblacion_superficie(paises):
    """Busca un país por nombre exacto y actualiza su población y superficie."""
    print("\n--- Actualizar población y superficie ---")
    nombre = input("Nombre exacto del país a actualizar: ").strip()

    pais_encontrado = None
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            pais_encontrado = pais
            break

    if pais_encontrado is None:
        print(f"Error: no se encontró ningún país llamado '{nombre}'.")
        return

    poblacion_nueva = input("Nueva población: ")
    superficie_nueva = input("Nueva superficie (km2): ")

    es_valido, resultado = validar_actualizacion(poblacion_nueva, superficie_nueva)
    if not es_valido:
        print(f"Error: {resultado}")
        return

    poblacion_num, superficie_num = resultado
    pais_encontrado["poblacion"] = poblacion_num
    pais_encontrado["superficie"] = superficie_num
    print(f"Datos de '{pais_encontrado['nombre']}' actualizados con éxito.")
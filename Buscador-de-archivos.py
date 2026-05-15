"""
Buscador Rayo McQueen - Buscador de archivos ultrarrápido
---------------------------------------------------------
Autor: aitorino2009
Licencia: MIT
Descripción: Herramienta de línea de comandos para buscar archivos
             con filtros avanzados de tamaño y palabras clave.
"""

import os
import time
import platform
import subprocess


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def abrir_ubicacion(ruta_archivo):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            subprocess.run(['explorer', '/select,', ruta_archivo])
        elif sistema == "Darwin":
            subprocess.run(['open', '-R', ruta_archivo])
        else:
            carpeta = os.path.dirname(ruta_archivo)
            subprocess.run(['xdg-open', carpeta])
        print(f"[i] Abriendo ubicacion: {ruta_archivo}")
    except Exception as e:
        print(f"[!] Error al intentar abrir la carpeta: {e}")


def parse_size_input(txt):
    """Convierte texto amigable (ej. 1GB, 500MB) a bytes reales"""
    txt = txt.upper().replace(" ", "")
    if not txt or txt in ["0", "NONE", "NADA"]:
        return None
    try:
        if txt.endswith("GB"):
            return int(float(txt.replace("GB", "")) * 1024 * 1024 * 1024)
        elif txt.endswith("MB"):
            return int(float(txt.replace("MB", "")) * 1024 * 1024)
        elif txt.endswith("KB"):
            return int(float(txt.replace("KB", "")) * 1024)
        else:
            # Si el usuario no pone unidad, asumimos MB
            return int(float(txt)) * 1024 * 1024
    except ValueError:
        return -1  # Bandera de error


def format_size(bytes_size):
    """Convierte bytes a un texto legible para el menu"""
    if bytes_size is None:
        return "Sin limite"
    mb = bytes_size / (1024 * 1024)
    if mb >= 1024:
        return f"{round(mb/1024, 2)} GB"
    return f"{round(mb, 2)} MB"


def buscar_archivos_filtrado(ruta, palabras, extension, min_bytes, max_bytes):
    resultados = []
    carpetas = [ruta]

    # Preparar filtros
    palabras_lower = [p.lower() for p in palabras]
    ext_lower = extension.lower() if extension else ""
    if ext_lower and not ext_lower.startswith('.'):
        ext_lower = '.' + ext_lower

    tiempo_inicio = time.time()

    while carpetas:
        carpeta = carpetas.pop()
        try:
            for entrada in os.scandir(carpeta):
                if entrada.is_dir(follow_symlinks=False):
                    carpetas.append(entrada.path)
                elif entrada.is_file(follow_symlinks=False):
                    nombre = entrada.name.lower()

                    # 1. Filtro de Extensión
                    if ext_lower and not nombre.endswith(ext_lower):
                        continue

                    # 2. Filtro de Palabras clave (Deben estar TODAS)
                    if palabras_lower and not all(p in nombre for p in palabras_lower):
                        continue

                    # 3. Filtro de Tamaño (Solo leemos el disco si paso los filtros anteriores)
                    if min_bytes is not None or max_bytes is not None:
                        try:
                            size = entrada.stat(follow_symlinks=False).st_size
                            if min_bytes is not None and size < min_bytes:
                                continue
                            if max_bytes is not None and size > max_bytes:
                                continue
                        except OSError:
                            continue  # Si no podemos leer el tamaño, lo saltamos

                    # Si llego hasta aqui, cumple TODOS los filtros
                    resultados.append(entrada.path)
                    print(f" [+] Encontrado: {entrada.name}")

        except PermissionError:
            continue
        except OSError:
            continue

    tiempo_total = round(time.time() - tiempo_inicio, 2)
    return resultados, tiempo_total


def ejecutar_busqueda_interactiva(filtros):
    limpiar_pantalla()
    print("==========================================")
    print("      BUSCANDO... POR FAVOR ESPERA")
    print("==========================================")

    resultados, tiempo = buscar_archivos_filtrado(
        filtros['ruta'], filtros['palabras'], filtros['ext'],
        filtros['min_bytes'], filtros['max_bytes']
    )

    print("\n==========================================")
    if not resultados:
        print(f"[i] Busqueda completada en {tiempo} segundos.")
        print("[!] No se encontro ninguna coincidencia con esos filtros.")
        input("\n[i] Intro para volver a los filtros...")
        return

    print(f"[i] Busqueda completada en {tiempo} segundos.")
    print(f"[i] Se encontraron {len(resultados)} resultados:\n")

    # Limitamos a 100 resultados en pantalla para no colapsar la terminal
    limite = 100
    for i, res in enumerate(resultados[:limite]):
        print(f"  {i + 1}. {res}")

    if len(resultados) > limite:
        print(
            f"\n  ... y {len(resultados) - limite} mas (refina tus filtros para ver menos).")

    print("\n------------------------------------------")
    print("[i] Escribe el NUMERO del archivo para abrir su carpeta.")
    print("[i] Escribe '0' o simplemente presiona Enter para volver a los filtros.")

    opcion = input("\n[+] Opcion: ").strip()

    if opcion.isdigit():
        indice = int(opcion)
        if 1 <= indice <= len(resultados[:limite]):
            abrir_ubicacion(resultados[indice - 1])
        elif indice != 0:
            print("[!] Numero fuera de rango.")
            time.sleep(1)

    input("\n[i] Intro para volver al menu de filtros...")


def menu_filtros():
    # Ruta por defecto segun el sistema
    ruta_defecto = "C:\\" if platform.system() == "Windows" else "/"

    filtros = {
        'palabras': [],
        'ext': '',
        'min_bytes': None,
        'max_bytes': None,
        'ruta': ruta_defecto
    }

    while True:
        limpiar_pantalla()
        print("==========================================")
        print("       CONFIGURAR BUSQUEDA AVANZADA")
        print("==========================================")

        p_str = " + ".join(filtros['palabras']
                           ) if filtros['palabras'] else "Cualquiera"
        e_str = filtros['ext'] if filtros['ext'] else "Cualquiera"
        min_str = format_size(filtros['min_bytes'])
        max_str = format_size(filtros['max_bytes'])

        print(f"1. Palabras clave : {p_str}")
        print(f"2. Extension      : {e_str}")
        print(f"3. Tamano minimo  : {min_str}")
        print(f"4. Tamano maximo  : {max_str}")
        print(f"5. Ruta a buscar  : {filtros['ruta']}")
        print("------------------------------------------")
        print("6. [>] INICIAR BUSQUEDA AHORA")
        print("7. [x] Volver al menu principal")

        opc = input("\n[+] Selecciona que filtro modificar (1-7): ").strip()

        if opc == "1":
            p = input(
                "[+] Palabras clave separadas por espacio (ej: all stars) o Enter para vaciar: ")
            filtros['palabras'] = p.split() if p.strip() else []
        elif opc == "2":
            e = input("[+] Extension (ej: .mp4) o Enter para vaciar: ")
            filtros['ext'] = e.strip()
        elif opc == "3":
            m = input("[+] Tamano minimo (ej: 50MB, 1GB) o Enter para vaciar: ")
            val = parse_size_input(m)
            if val == -1:
                print("[!] Formato incorrecto.")
                time.sleep(1)
            else:
                filtros['min_bytes'] = val
        elif opc == "4":
            m = input(
                "[+] Tamano maximo (ej: 1GB, 500MB) o Enter para vaciar: ")
            val = parse_size_input(m)
            if val == -1:
                print("[!] Formato incorrecto.")
                time.sleep(1)
            else:
                filtros['max_bytes'] = val
        elif opc == "5":
            r = input(f"[+] Nueva ruta (ej: {ruta_defecto}Users): ").strip()
            if os.path.exists(r):
                filtros['ruta'] = r
            else:
                print("[!] La ruta no existe.")
                time.sleep(1)
        elif opc == "6":
            ejecutar_busqueda_interactiva(filtros)
        elif opc == "7":
            break


def modulo_ayuda():
    limpiar_pantalla()
    print("==========================================")
    print("               AYUDA Y SINTAXIS")
    print("==========================================")
    print("\n[i] COMO FUNCIONAN LOS FILTROS AVANZADOS:")
    print("Todos los filtros se suman (Condicion AND). Si pones de extension '.mp4'")
    print("y tamaño maximo '1GB', el programa SOLO mostrara archivos que sean mp4")
    print("Y que ademas pesen menos de 1GB.\n")

    print("[+] SINTAXIS DE PALABRAS CLAVE:")
    print("  * Si escribes: all stars")
    print("  * Encontrara: 'all_the_stars.mp4' o 'stars_and_all.txt'")
    print("  * El orden no importa, pero TODAS las palabras deben estar en el nombre.\n")

    print("[+] SINTAXIS DE TAMAÑO:")
    print("  * Puedes usar 'MB' o 'GB' directamente (Ej: 500MB, 2GB).")
    print("  * Si solo escribes un numero (Ej: 100), se asumira que son Megabytes.\n")

    print("[!] NOTA ANTI-CRASH:")
    print("Si buscas en todo 'C:\\' sin ningun filtro, podrian salir 500,000 archivos.")
    print("Por seguridad, el programa solo mostrara los primeros 100 resultados en")
    print("pantalla. ¡Usa los filtros para afinar tu busqueda!")

    input("\n[i] Presiona Enter para volver al menu principal...")


def menu_principal():
    while True:
        limpiar_pantalla()
        print("==========================================")
        print("       BUSCADOR RAYO MCQUEEN")
        print("==========================================")
        print("1. Buscar archivos")
        print("2. Ayuda e Instrucciones")
        print("3. Salir")
        print("------------------------------------------")

        opc = input("[+] Selecciona una opcion: ").strip()

        if opc == "1":
            menu_filtros()
        elif opc == "2":
            modulo_ayuda()
        elif opc == "3":
            print("\n[i] Cerrando buscador...")
            break
        else:
            print("\n[!] Opcion no valida.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n[!] Programa cerrado por el usuario.")

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import requests
import datetime
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

API_KEY_CLIMA = os.getenv("OPENWEATHER_API_KEY")
ARCHIVO_HISTORIAL = "historial_global.csv"
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY_GEMINI)


def consultar_clima_y_guardar(usuario):
    ciudad = input("Ingrese el nombre de una ciudad: ")
    url = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {'q': ciudad, 'appid': API_KEY_CLIMA, 'units': 'metric', 'lang': 'es'}
    try:
        respuesta = requests.get(url, params=parametros, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        temperatura = datos["main"]["temp"]
        sensacion = datos["main"]["feels_like"]
        humedad = datos["main"]["humidity"]
        descripcion = datos["weather"][0]["description"]
        viento = datos["wind"]["speed"]

        print(f"Clima en {ciudad}:")
        print(f"Temperatura: {temperatura}°C (Sensación térmica: {sensacion}°C)")
        print(f"Condición: {descripcion}")
        print(f"Humedad: {humedad}%")
        print(f"Viento: {viento} km/h")

        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fila = [usuario, ciudad, ahora, temperatura, descripcion, humedad, viento]

        nuevo_archivo = not os.path.exists(ARCHIVO_HISTORIAL)

        with open(ARCHIVO_HISTORIAL, "a", newline='') as archivo:
            escritor = csv.writer(archivo)
            if nuevo_archivo:
                escritor.writerow(["usuario", "ciudad", "fecha_hora", "temperatura", "condicion", "humedad", "viento"])
            escritor.writerow(fila)

        print("Consulta guardada en historial.")

    except requests.exceptions.HTTPError:
        print("Error: Ciudad no encontrada o API Key inválida.")
    except Exception as e:
        print(f"Error: {e}")


def validar_contrasena(contrasena):
    errores = []
    if len(contrasena) < 8:
        errores.append("tener al menos 8 caracteres")
    if not any(c.isupper() for c in contrasena):
        errores.append("incluir al menos una letra mayúscula")
    if not any(c.islower() for c in contrasena):
        errores.append("incluir al menos una letra minúscula")
    if not any(c.isdigit() for c in contrasena):
        errores.append("incluir al menos un número")
    return errores


def ver_mi_historial(nombre_usuario):
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("Aún no hay historial guardado.")
        return

    ciudad_buscada = input("¿De qué ciudad querés ver tu historial? ").strip().lower()
    hay_resultados = False
    with open(ARCHIVO_HISTORIAL, "r", newline='') as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for fila in lector:
            usuario, ciudad, fecha_hora, temp, condicion, humedad, viento = fila
            if usuario == nombre_usuario and ciudad.lower() == ciudad_buscada:
                print(f"Fecha: {fecha_hora}")
                print(f"Temperatura: {temp}°C")
                print(f"Condición: {condicion.capitalize()}")
                print(f"Humedad: {humedad}%")
                print(f"Viento: {viento} km/h\n")
                hay_resultados = True

    if not hay_resultados:
        print("No encontramos registros para esa ciudad.")


def registrar_usuario():
    usuario = input("Ingrese un nuevo nombre de usuario: ")
    with open("usuarios_simulados.csv", "r", newline='') as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for fila in lector:
            if fila and fila[0] == usuario:
                print("Ese nombre de usuario ya existe. Intente con otro.")
                return

    contrasena = input("Ingrese una contraseña: ")
    errores = validar_contrasena(contrasena)

    if errores:
        print(f"La contraseña no cumple con: {', '.join(errores)}.")
        print("Recomendación: usa mayúsculas, minúsculas, números y al menos 8 caracteres.")
        return

    with open("usuarios_simulados.csv", "a", newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([usuario, contrasena])

    print("Usuario registrado.")
    return


def log_usuario(archivo):
    valido = False
    repetir = "si"
    while not valido and repetir == "si":
        usuario = input("Ingrese un usuario: ")
        contrasena = input("Ingrese una contraseña: ")
        try:
            with open("usuarios_simulados.csv", "r") as archivo:
                lector = csv.reader(archivo)
                next(lector)
                for fila in lector:
                    if fila and fila[0] == usuario and fila[1] == contrasena:
                        valido = True
                        print("Autenticación exitosa.")
                        repetir = "no"
                        return usuario, contrasena, repetir, valido
        except:
            print("Hubo problemas con el archivo.")
        print("Login incorrecto.")
        repetir = input("¿Desea reintentar el login? (si/no): ")
    return usuario, contrasena, repetir, valido


def ciudad_mas_consultada(lista):
    listasinrepes = []
    apariciones = []
    for elemento in lista:
        if elemento not in listasinrepes:
            listasinrepes.append(elemento)
    for elem in listasinrepes:
        contador = 0
        for el in lista:
            if el == elem:
                contador += 1
        apariciones.append(contador)
    combinado = list(zip(listasinrepes, apariciones))
    combinado.sort(key=lambda x: x[1], reverse=True)
    ciudad_top, apariciones_top = combinado[0]
    return ciudad_top


def estadisticas():
    try:
        with open("historial_global.csv", "r") as archivo:
            lector = csv.reader(archivo)
            next(lector)
            cantidad_consultas = 0
            sumatemperatura = 0
            lista_ciudades = []
            for line in lector:
                lista_ciudades.append(line[1])
                cantidad_consultas += 1
                sumatemperatura += float(line[3])
            ciudadconsultada = ciudad_mas_consultada(lista_ciudades)
            promediotemperatura = sumatemperatura / cantidad_consultas
            print(f"La ciudad más consultada fue {ciudadconsultada}")
            print(f"Se realizaron {cantidad_consultas} consultas")
            print(f"La temperatura promedio fue de {promediotemperatura:.2f}°C")
    except:
        print("Error de acceso")


def consejo_ia_consulta_nueva():
    ciudad = input("Ingrese la ciudad para el consejo de vestimenta: ")
    url = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {
        'q': ciudad,
        'appid': API_KEY_CLIMA,
        'units': 'metric',
        'lang': 'es'
    }

    try:
        respuesta = requests.get(url, params=parametros, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        temperatura = datos["main"]["temp"]
        sensacion = datos["main"]["feels_like"]
        humedad = datos["main"]["humidity"]
        descripcion = datos["weather"][0]["description"]
        viento = datos["wind"]["speed"] * 3.6

        print(f"\nClima actual en {ciudad}")
        print(f"Temperatura: {temperatura}°C (Sensación: {sensacion}°C)")
        print(f"Condición: {descripcion}")
        print(f"Humedad: {humedad}%")
        print(f"Viento: {viento} km/h")

        prompt = (
            f"Estoy armando una app de consejos de vestimenta según el clima, "
            f"el clima es: {descripcion}, temperatura de {temperatura}°C, "
            f"viento de {viento} km/h y humedad de {humedad}%, "
            f"¿cómo debería vestirme? Respondé en español."
        )

        modelo = genai.GenerativeModel("models/gemini-1.5-flash")
        respuesta_ia = modelo.generate_content(prompt)

        print("Consejo de vestimenta generado por IA:")
        print(respuesta_ia.text.strip() if respuesta_ia.text else "No se pudo generar el consejo.")

    except requests.exceptions.HTTPError:
        print("Error: Ciudad no encontrada o API Key inválida.")
    except Exception as e:
        print(f"Error inesperado: {e}")


def generar_reporte_excel():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("El archivo de historial global (historial_global.csv) no existe o está vacío.")
        print("Realice algunas consultas de clima primero.")
        return

    try:
        df = pd.read_csv(ARCHIVO_HISTORIAL)

        if df.empty:
            print("El historial está vacío. No hay datos para generar el reporte.")
            return

        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])

        # Gráfico 1: Consultas por ciudad (barras)
        consultas_por_ciudad = df['ciudad'].value_counts()

        plt.figure(figsize=(10, 6))
        consultas_por_ciudad.plot(kind='bar', color='skyblue')
        plt.title('Número de Consultas por Ciudad')
        plt.xlabel('Ciudad')
        plt.ylabel('Número de Consultas')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        img_barras_path = 'grafico_barras_consultas_por_ciudad.png'
        plt.savefig(img_barras_path)
        plt.close()

        # Gráfico 2: Tendencia de temperatura (líneas)
        ciudades_populares = consultas_por_ciudad.head(3).index.tolist()

        if not ciudades_populares:
            print("No hay ciudades suficientes para generar el gráfico de tendencia de temperatura.")
        else:
            plt.figure(figsize=(12, 7))
            for ciudad in ciudades_populares:
                df_ciudad = df[df['ciudad'] == ciudad].sort_values('fecha_hora')
                plt.plot(df_ciudad['fecha_hora'], df_ciudad['temperatura'], marker='o', linestyle='-', label=ciudad)

            plt.title('Tendencia de Temperatura a lo largo del tiempo por Ciudad (Top 3)')
            plt.xlabel('Fecha y Hora')
            plt.ylabel('Temperatura (°C)')
            plt.grid(True)
            plt.legend(title='Ciudad')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            img_lineas_path = 'grafico_lineas_temperatura.png'
            plt.savefig(img_lineas_path)
            plt.close()

        # Crear archivo Excel
        excel_file = 'Reporte_GuardianClima_ITBA.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df_para_excel = df.rename(columns={
                'usuario': 'Usuario',
                'ciudad': 'Ciudad',
                'fecha_hora': 'Fecha/Hora completa',
                'temperatura': 'Temperatura (°C)',
                'condicion': 'Condición',
                'humedad': 'Humedad (%)',
                'viento': 'Viento (km/h)'
            })
            df_para_excel.to_excel(writer, sheet_name='Datos Crudos Historial', index=False)

            consultas_por_ciudad_excel = consultas_por_ciudad.reset_index()
            consultas_por_ciudad_excel.columns = ['Ciudad', 'Número de Consultas']
            consultas_por_ciudad_excel.to_excel(writer, sheet_name='Consultas por Ciudad', index=False)

        print(f"\nReporte Excel '{excel_file}' generado con éxito.")
        print(f"Los gráficos se han guardado como '{img_barras_path}' y '{img_lineas_path}'.")
        print("Podés insertar estas imágenes manualmente en el archivo Excel.")

    except pd.errors.EmptyDataError:
        print("El archivo de historial existe pero está vacío.")
    except Exception as e:
        print(f"Error inesperado al generar el reporte Excel: {e}")
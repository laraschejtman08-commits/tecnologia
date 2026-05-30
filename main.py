from funciones import *
from menu import *
import csv

if not os.path.exists("usuarios_simulados.csv"):
    with open("usuarios_simulados.csv", "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["usuario", "contraseña"])

cerrar_sesion = False
while not cerrar_sesion:
    opcion = menu()

    if opcion == "1":
        usuario, contraseña, repetir, valido = log_usuario("usuarios_simulados.csv")
        if valido:
            menu_principal(usuario)
    elif opcion == "2":
        registrar_usuario()
    elif opcion == "3":
        cerrar_sesion = True
        print("Saliendo del programa.")
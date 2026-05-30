from funciones import *

def menu():
    opcion = ""
    while opcion not in ["1", "2", "3"]:
        print("Menú")
        print("1. Iniciar Sesión")
        print("2. Registrar nuevo usuario")
        print("3. Cerrar sesión")
        opcion = input("Ingrese una opción: ")
    return opcion

def menu_principal(nombre_usuario):
    salir_menu = False
    while not salir_menu:
        print("MENÚ PRINCIPAL")
        print("1. Consultar clima y Guardar en historial")
        print("2. Ver mi historial por ciudad")
        print("3. Ver estadísticas globales")
        print("4. Consejo de IA: ¿cómo me visto hoy?")
        print("5. Acerca de GuardianClima ITBA")
        print("6. Cerrar sesión")
        print("7. Generar Reporte Excel de Estadísticas")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            consultar_clima_y_guardar(nombre_usuario)
        elif opcion == "2":
            ver_mi_historial(nombre_usuario)
        elif opcion == "3":
            estadisticas()
        elif opcion == "4":
            consejo_la_consulta_nueva()
        elif opcion == "5":
            print("GuardianClima ITBA – Aplicación de consola para consultar el clima, guardar historial, ver estadísticas y recibir consejos de vestimenta usando IA.")
            print("Desarrollado por el equipo de estudiantes del ITBA.")
        elif opcion == "6":
            print("Cerrando sesión")
            salir_menu = True
        elif opcion == "7": # para este bloque 'exit' COMPLETO
            generar_reporte_excel()
        else:
            print("Opción no válida")
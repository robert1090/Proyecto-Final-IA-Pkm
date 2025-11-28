#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import tkinter as tk
import agente
import threading


def ejecutar():
    #Funcion para ejecutar el agente

    print("Ejecutando Agente Pokémon...")
    agent = threading.Thread(target=agente.agente) #Inicia el agente en un hilo separado
    agent.daemon = True
    agent.start()

def crear_interfaz():
    #Funcion para crear la interfaz grafica

    #Crea la ventana principal
    interfaz = tk.Tk()
    interfaz.title("Agente Pokémon") #Nombre de la ventana
    interfaz.geometry("300x200") #Tamaño de la ventana

    #Texto de instrucciones basicas
    label = tk.Label(interfaz, text="Presiona el boton para Ejecutar o Detener el Agente:")
    label.pack(pady=5)

    #Boton para ejecutar el agente
    boton = tk.Button(interfaz, text="Ejecutar", command=ejecutar)
    boton.pack(pady=5)

    #Bucle que mantiene la ventana abierta
    interfaz.mainloop()
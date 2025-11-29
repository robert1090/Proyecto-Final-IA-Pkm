#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import tkinter as tk
import agente
import threading
import sys

class redireccionador:
    #Clase para redirigir los prints a la interfaz grafica
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

activo = False

def ejecutar():
    #Funcion para ejecutar o detener el agente
    global boton, activo

    if not activo: #Si el agente no esta activo, lo ejecuta
        print("Ejecutando Agente Pokémon...")
        agent = threading.Thread(target=agente.agente) #Inicia el agente en un hilo separado
        agent.daemon = True
        agent.start()
        boton.config(text="Detener") #Cambia el texto del boton
        activo = True
    else: #Si el agente esta activo, lo detiene
        print("Deteniendo Agente Pokémon...")
        boton.config(text="Ejecutar")
        agente.detener()
        activo = False    

def crear_interfaz():
    #Funcion para crear la interfaz grafica
    global boton #variable para modificar el boton de ejecutar/detener

    #Crea la ventana principal
    interfaz = tk.Tk()
    interfaz.title("Agente Pokémon") #Nombre de la ventana
    interfaz.geometry("300x350") #Tamaño de la ventana

    #Texto de instrucciones basicas
    label = tk.Label(interfaz, text="Presiona el boton para Ejecutar o Detener el Agente:")
    label.pack(pady=5)

    #Boton para ejecutar el agente
    boton = tk.Button(interfaz, text="Ejecutar", command=ejecutar)
    boton.pack(pady=5)

    #Marco de texto para mostrar los prints
    texto = tk.Text(interfaz, height=20, width=45)
    texto.pack(pady=10)

    #Llama a la clase rediraccionador para redirigir los prints
    sys.stdout = redireccionador(texto)

    #Bucle que mantiene la ventana abierta
    interfaz.mainloop()
#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import time
import requests
import vgamepad as vg
import pygetwindow as gw
import base64
import pyautogui

#Inicializacion del mando virtual para controlar el emulador
gamepad = vg.VX360Gamepad()

#Dimensiones del emulador en pantalla
screen = (634, 48, 654, 980)

#URL de LM Studio Local o Remoto
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
Modelo = "qwen3-vl-4b"

def captura_pantalla():
    #Función para capturar la pantalla del emulador
    x, y, w, h = screen
    screen_image = pyautogui.screenshot(region=(x, y, w, h))
    return screen_image

def encode_image():
    #Función para convertir la imagen a base64
    imagen = captura_pantalla()
    imagen.save("captura.png", format="PNG")
    with open("captura.png", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def ask(img_base64):
    #Funcion para enviar la imagen y recibir la accion del modelo de LM Studio

    #Prompt detallado para guiar al modelo en la toma de decisiones
    prompt = """
Eres un agente experto en jugar Pokémon, mas especificamente la edicion 'Negro 2'. Estás viendo la pantalla del juego.
Debes decidir la mejor acción del jugador basado SOLO en lo que se ve.

Responde con EXACTAMENTE UNA acción de la siguiente lista:
["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]

A = Interactuar o Confirmar
B = Retroceder o Negar

Cuando no estes en un Combate Pokémon, omite totalmente el marco rojo de la parte inferior, y muevete entre la hierva alta mas cercana, usando 'UP', 'DOWN', 'LEFT', 'RIGHT' en busca de algun Pokémon Salvaje, si sales de la Hierba Alta vuelve de inmediato.
Para navegar en el Menu de Combate, debes usar 'UP', 'DOWN', 'LEFT', 'RIGHT' para moverte entre las opciones y 'A' para seleccionar, para saber que estas seleccionando, deberas fijarte en el marco rojo con blanco alrededor de la opcion seleccionada, evita seleccionar con el marco rojo los espacios en negro.
Si necesitas salir del Menu de Combate, presiona 'B' hasta salir.
Cuando te pregunte si quieres ponerle un Mote a un Pokémon, selecciona 'No' usando 'B'.
Si es una Batalla Pokémon contra un Entrenador, NO intentaras capturar el Pokémon Rival, solo lo vas a derrotar.

No expliques nada. Solo responde la acción.
    """

    #Formato de envio de contenido a LM Studio
    payload = {
        "model": Modelo,
        "temperature": 0,
        "max_tokens": 50,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ]
    }

    #Verificador de repuestas, si no responde correctamente, devuelve "A" por defecto y mueestra la repuesta del modelo
    try:
        response = requests.post(LM_STUDIO_URL, json=payload)
        data = response.json()

        action = data["choices"][0]["message"]["content"].strip()
        return action

    except Exception as e:
        print("Error al comunicarse con LM Studio:", e)
        return "A"

def opciones(action):
    #Funcion para mapear las acciones recibidas a botones del mando virtual
    buttons = {
        "A": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        "B": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        "X": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        "Y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        "START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        "SELECT": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    }

    dpad = {
        "UP": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        "DOWN": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        "LEFT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        "RIGHT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    }

    #Verifica si la repuesta coincide y ejecuta la accion correspondiente
    if action in buttons:
        gamepad.press_button(button=buttons[action])
        gamepad.update()
        time.sleep(0.1)
        gamepad.release_button(button=buttons[action])
        gamepad.update()
        print("Accion:", action)
        return

    if action in dpad:
        gamepad.press_button(button=dpad[action])
        gamepad.update()
        time.sleep(0.1)
        gamepad.release_button(button=dpad[action])
        gamepad.update()
        print("Accion:", action)
        return
    
    #Si no coincide, muestra mensaje de accion invalida
    else:
        print("Accion invalida:", action)

def agente():
    #Funcion que realizara el bucle de captura del emulador y envio a LM Studio
    while True:
        imagen64 = encode_image()
        action = ask(imagen64)
        opciones(action)
        time.sleep(1)
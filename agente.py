#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import time
import requests
import vgamepad as vg
import base64
import pyautogui

#Inicializacion del mando virtual para controlar el emulador
def control():
    for i in range(5):
        try:
            return vg.VX360Gamepad()
        except AssertionError:
            time.sleep(1)

gamepad = control()

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
Eres un agente experto en jugar Pokémon Negro 2. Estás viendo una captura REAL de la pantalla del juego. 
Tu única tarea es seleccionar la acción correcta basándote SOLO en lo que aparece visualmente.

Debes responder con EXACTAMENTE UNA acción de esta lista:
["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]

A = Confirmar / Interactuar
B = Cancelar / Retroceder

REGLAS GENERALES:
- Nunca expliques nada. Solo devuelve una tecla.
- Solo usa una acción por turno.
- NO inventes nada que no esté visible en pantalla.

EXPLORACIÓN (NO combate):
- Si no estás en un combate Pokémon, ignora el marco rojo del menú inferior.
- Muévete por la hierba alta más cercana usando flechas.
- Si sales de la hierba alta, vuelve inmediatamente.
- Prioriza buscar Pokémon salvajes moviéndote en la hierba.

COMBATE:
- Para navegar el Menú de Combate:
  - Usa UP, DOWN, LEFT o RIGHT para mover el cursor (marco rojo/blanco).
  - Usa A para seleccionar la opción señalada.
  - Usa B para retroceder o cancelar.
- Siempre verifica qué opción está resaltada por el marco blanco y rojo.

ELECCIÓN DE MOVIMIENTOS:
- Siempre verifica qué opción está resaltada por el marco blanco y rojo.
- Prioriza movimientos con nombre visible (texto legible).
- Evita seleccionar espacios vacíos, cajas negras o movimientos no visibles.
- Prefiere movimientos como:
  Arañazo, Tacleada, Placaje, Burbuja, Látigo Cepa (muy prioritario).
- Si necesitas salir del menú de combate, presiona B hasta salir.

CONFLICTOS:
- Siempre verifica qué opción está resaltada por el marco blanco y rojo.
- En peleas contra entrenadores, NO intentes capturar. Solo atacar.
- Si un Pokémon es debilitado:
  - Elige uno que NO esté en rojo y NO tenga PS = 0.
  - Prioriza Pokémon con marco verde.

CAMBIO DE POKÉMON:
- Siempre verifica qué opción está resaltada por el semi marco blanco/rojo.
- Si tu Pokémon es derrotado:
    - Selecciona POKÉMON y elige uno con PS > 0.
    - Evita elegir Pokémon con PS en rojo o 0.
    - Usa B para retroceder si es necesario.
- Cuando te pregunten que pokémon quieres usar:
  - Confirma con 'A' cuando estes seleccionando un Pokémon con Marco Verde.
  - Selecciona el que tenga PS > 0 y preferiblemente con marco verde.
  - Si el Pokémon seleccionado tiene PS en rojo o 0, elige otro.

MOTES:
- Cuando te pregunten si quieres poner un mote:
  - Responde "No" usando B.

REGLA FINAL:
Nunca devuelvas nada excepto una de estas acciones:
["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]
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
    global run
    run = True

    while run:
        imagen64 = encode_image()
        action = ask(imagen64)
        opciones(action)
        time.sleep(1)

def detener():
    #Funcion para detener el agente
    global run
    run = False
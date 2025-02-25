# RaspberryPicoW_SensorTemperatura

Este proyecto utiliza una **Raspberry Pi Pico W** para medir la temperatura mediante su sensor interno y enviar los datos a **ThingSpeak** en tiempo real. También es posible usar un sensor **LM35** para mayor precisión.

## 📌 Requisitos

- **Thonny** (IDE para programar en MicroPython)
- **Raspberry Pi Pico W** con MicroPython instalado
- **Conexión a Internet** (WiFi configurado en la Pico W)
- **Cuenta en ThingSpeak** con un canal configurado
- **Sensor LM35** (opcional para medir temperatura externa)

## 🔧 Instalación y Configuración

### 1️⃣ Instalar MicroPython en la Raspberry Pi Pico W
Si aún no tienes MicroPython instalado:
1. Descarga el firmware de MicroPython para la Pico W desde [aquí](https://micropython.org/download/rp2-pico-w/).
2. Conéctala al PC **mientras mantienes presionado el botón BOOTSEL**.
3. Copia el archivo `.uf2` descargado en la unidad que aparecerá (`RPI-RP2`).
4. Desconéctala y vuelve a conectarla.

### 2️⃣ Configurar Thonny
1. **Abre Thonny** y selecciona `MicroPython (Raspberry Pi Pico)` en "Herramientas" > "Opciones" > "Intérprete".
2. **Conéctala por USB** y presiona "STOP" en Thonny para reiniciar.

### 3️⃣ Configurar WiFi en la Pico W
En tu código, agrega los datos de tu red WiFi:
```python
SSID = "TuSSID"
PASSWORD = "TuContraseña"
```

### 4️⃣ Obtener la API Key de ThingSpeak
1. Crea una cuenta en **ThingSpeak**.
2. Crea un **nuevo canal**.
3. Copia la **Write API Key** de la sección "API Keys".
4. Modifica el código en `main.py` para incluir esta clave.

## 🚀 Uso
1. Guarda el código en la **Raspberry Pi Pico W** como `main.py`.
2. Reinicia la Pico W y comenzará a enviar datos a ThingSpeak.
3. Puedes visualizar la temperatura en tiempo real desde tu canal en **ThingSpeak**.

## 🛠 Código Principal (`main.py`)
```python
import network
import urequests
import time
import machine

# Configuración WiFi
SSID = "TuSSID"
PASSWORD = "TuContraseña"

# Configuración de ThingSpeak
THINGSPEAK_API_KEY = "TU_WRITE_API_KEY"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Configurar sensor de temperatura
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Conectado a WiFi")
    #esta linea cambia si tienes el sensor LM35
def leer_temperatura():
    lectura = sensor_temp.read_u16() * conversion_factor
    temperatura = 27 - (lectura - 0.706) / 0.001721
    return round(temperatura, 2)

def enviar_a_thingspeak(temp):
    url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temp}"
    respuesta = urequests.get(url)
    respuesta.close()

def main():
    conectar_wifi()
    while True:
        temperatura = leer_temperatura()
        print(f"Temperatura: {temperatura}°C")
        enviar_a_thingspeak(temperatura)
        time.sleep(180)  # Espera 3 minutos entre mediciones

main()
```

## ⚠️ Notas
- La Pico W **debe estar conectada a WiFi** para enviar los datos.
- Si usas un sensor LM35, necesitarás conectarlo a un pin **ADC** y modificar la función `leer_temperatura()`.

## 📩 Contacto
Si tienes dudas o mejoras para este proyecto, ¡contáctame! 😃


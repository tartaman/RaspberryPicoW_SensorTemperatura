import network
import urequests
import utime
import machine

# Configuración de WiFi
SSID = "INFINITUM64C3"
PASSWORD = "2PRsesEUYr"

# API de ThingSpeak
THINGSPEAK_API_KEY = "76AQQZ0D3BP6T1KB"  # Reemplaza con tu API Key de escritura
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Configurar WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Esperar conexión
print("Conectando a WiFi...")
while not wlan.isconnected():
    utime.sleep(1)
print("Conectado! IP:", wlan.ifconfig()[0])

# Función para leer temperatura del sensor interno
def leer_temperatura():
    sensor_temp = machine.ADC(4)  # ADC4 está conectado al sensor de temperatura interno
    conversion_factor = 3.3 / (65535)
    lectura = sensor_temp.read_u16() * conversion_factor
    temperatura = 27 - (lectura - 0.706) / 0.001721  # Fórmula de conversión del datasheet
    return temperatura

# Enviar datos a ThingSpeak
while True:
    temperatura = leer_temperatura()
    print(f"Temperatura: {temperatura:.2f}°C")
    
    # Hacer petición HTTP a ThingSpeak
    try:
        response = urequests.get(f"{THINGSPEAK_URL}?api_key={THINGSPEAK_API_KEY}&field1={temperatura:.2f}")
        print("Respuesta de ThingSpeak:", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar datos:", e)

    utime.sleep(180)  # Esperar 180 segundos antes de la siguiente medición


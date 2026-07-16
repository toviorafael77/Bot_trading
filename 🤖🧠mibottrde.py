import requests
import time
from datetime import datetime
import pytz

# Configuración de zona horaria de Colombia
colombia_tz = pytz.timezone('America/Bogota')
ARCHIVO_LOG = "historial_senales.txt"
lista_activos = ["EURUSDT", "BTCUSDT", "GBPUSDT"]

# Control de tiempo por activo
ultimo_minuto_marcado = {activo: 0 for activo in lista_activos}

def get_market_data(symbol):
    # API de Binance para obtener datos en tiempo real
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=5"
    try:
        data = requests.get(url, timeout=3).json()
        return [{'open': float(v[1]), 'close': float(v[4])} for v in data]
    except:
        return []

def calcular_proxima_entrada(minuto_actual):
    # Calcula el siguiente múltiplo de 4 (Escalera de 4 minutos)
    return minuto_actual + (4 - (minuto_actual % 4))

def analizar_patron(symbol):
    data = get_market_data(symbol)
    if not data or len(data) < 5: return None
    v1, v2, v3, v4 = data[-1], data[-2], data[-3], data[-4]
    
    # Lógica de patrón de 4 velas
    if v1['close'] > v1['open'] and v2['close'] > v2['open'] and v3['close'] > v3['open'] and v4['close'] > v4['open']:
        return "🟢"
    if v1['close'] < v1['open'] and v2['close'] < v2['open'] and v3['close'] < v3['open'] and v4['close'] < v4['open']:
        return "🔴"
    return None

print("--- SISTEMA DE GUARDADO ACTIVO: ENTRADAS CADA 4 MIN ---")

while True:
    for activo in lista_activos:
        patron = analizar_patron(activo)
        
        if patron:
            ahora = datetime.now(colombia_tz)
            minuto_calc = calcular_proxima_entrada(ahora.minute)
            
            # Verificación contra el historial en memoria
            if minuto_calc != ultimo_minuto_marcado[activo]:
                hora_entrada = ahora.replace(minute=minuto_calc % 60, second=0, microsecond=0).strftime('%H:%M')
                
                # Formato final solicitado
                mensaje = f"📢 {patron} {activo} | HORA DE ENTRADA: {hora_entrada}"
                print(mensaje)
                
                # Guardado persistente: Al abrir el archivo en modo 'a' (append), 
                # los datos se escriben inmediatamente al disco.
                with open(ARCHIVO_LOG, "a") as f:
                    f.write(mensaje + "\n")
                    f.flush() # Fuerza la escritura real en el almacenamiento
                
                ultimo_minuto_marcado[activo] = minuto_calc
    
    # Pausa corta para no sobrecargar el procesador y mantener la hora real
    time.sleep(2)

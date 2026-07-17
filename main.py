import yfinance as yf
import time
import pytz
from datetime import datetime

def obtener_precio(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d")
        return data['Close'].iloc[-1]
    except:
        return 0

def run_bot():
    print("--- BOT DE TRADING CON ALERTAS ANTICIPADAS ---")
    simbolos = {'BTC': 'BTC-USD', 'GBP/USD': 'GBPUSD=X'}
    
    while True:
        zona_horaria = pytz.timezone('America/Bogota')
        ahora = datetime.now(zona_horaria)
        minuto = ahora.minute
        segundo = ahora.second
        
        # Lógica: ciclo de 4 minutos. 
        # Detectar si estamos en el minuto 3 (el minuto previo al cierre del ciclo de 4)
        es_minuto_previo = (minuto + 1) % 4 == 0
        
        print(f"\n--- HORA COLOMBIA: {ahora.strftime('%H:%M:%S')} ---")
        
        for nombre, ticker in simbolos.items():
            precio = obtener_precio(ticker)
            print(f"[{nombre}] Precio actual: {precio:.4f}")
            
            # Lógica de señales (Aquí aplicarías tu estrategia de Order Block/FVG)
            # Simulamos análisis:
            if es_minuto_previo:
                print(f"⚠️ {nombre}: ¡ALERTA ANTICIPADA! Preparar entrada para el minuto {(minuto + 1) % 60}")
                
                # Simulador de señal de dirección basada en precio (reemplaza con tu lógica real)
                if segundo % 2 == 0:
                    print(f"🟢 SEÑAL COMPRA | Entrada estimada: {(minuto + 1) % 60}:00")
                else:
                    print(f"🛑 SEÑAL VENTA  | Entrada estimada: {(minuto + 1) % 60}:00")
            else:
                print(f"[{nombre}] Analizando patrones... esperando ciclo de entrada.")
        
        time.sleep(20) # Revisión cada 20 segundos para no perder la ventana de 1 minuto

if __name__ == "__main__":
    run_bot()
    

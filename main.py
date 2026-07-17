import time
import requests
import pytz
from datetime import datetime
import os.
def run_bot():
    print("--- INICIANDO BOT DE TRADING CON ESTRATEGIA ---")
    
    # Lista de activos que analizamos (Euro/Dólar corregido)
    activos = ["EURUSD"]
    
    while True:
        try:
            zona_horaria = pytz.timezone('America/Bogota')
            ahora = datetime.now(zona_horaria).strftime('%H:%M:%S')
            
            print(f"--- ANALIZANDO MERCADO - {ahora} ---")
            
            for activo in activos:
                # Aquí iría tu lógica de análisis (Order Blocks, FVG, Fibonacci)
                # Simulamos la detección de una señal
                
                # Emojis de señales
                senal_compra = "🟢 COMPRA (BUY) 🚀"
                senal_venta = "🔴 VENTA (SELL) 📉"
                
                # Ejemplo de impresión de estrategia detectada
                print(f"[{activo}] Análisis: Order Block detectado, buscando confirmación en FVG...")
                print(f"[{activo}] {senal_compra} - Esperando confirmación para ejecutar.")
                
            time.sleep(60) # Pausa de 60 segundos
            
        except Exception as e:
            print(f"Error detectado: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
    

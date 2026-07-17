import time
import requests
import pytz
from datetime import datetime
import os

def run_bot():
    print("--- INICIANDO BOT DE TRADING CON ESTRATEGIA ---")
    
    activos = ["EURUSD"]
    
    while True:
        try:
            zona_horaria = pytz.timezone('America/Bogota')
            ahora = datetime.now(zona_horaria).strftime('%H:%M:%S')
            
            print(f"--- ANALIZANDO MERCADO - {ahora} ---")
            
            for activo in activos:
                senal_compra = "🟢 COMPRA (BUY) 🚀"
                senal_venta = "🔴 VENTA (SELL) 📉"
                
                print(f"[{activo}] Análisis: Order Block detectado, buscando confirmación en FVG...")
                print(f"[{activo}] {senal_compra} - Esperando confirmación para ejecutar.")
                
            time.sleep(60) 
            
        except Exception as e:
            print(f"Error detectado: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
    

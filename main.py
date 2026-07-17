import yfinance as yf
import time
import pytz
from datetime import datetime

# ... (mantén la función detectar_fvg_ob igual) ...

def run_bot():
    print("--- SCANNER SMC (CICLO 4 MIN) ACTIVO ---")
    simbolos = {'BTC': 'BTC-USD', 'GBP/USD': 'GBPUSD=X'}
    
    while True:
        zona_horaria = pytz.timezone('America/Bogota')
        ahora = datetime.now(zona_horaria)
        
        # Filtro de tiempo: Solo analizar cuando faltan 2 minutos para el siguiente bloque de 4
        # Ej: 11:46, 11:50, 11:54, 11:58
        if ahora.minute % 4 == 3 and 50 <= ahora.second <= 59:
            print(f"\n--- HORA: {ahora.strftime('%H:%M:%S')} ---")
            
            for nombre, ticker in simbolos.items():
                try:
                    df = yf.Ticker(ticker).history(period="1d", interval="1m").tail(10)
                    tipo, zona = detectar_fvg_ob(df)
                    
                    if tipo:
                        # Calcular el siguiente minuto múltiplo de 4
                        minuto_actual = ahora.minute
                        minuto_proximo = ((minuto_actual // 4) + 1) * 4
                        
                        hora_entrada = ahora.replace(minute=minuto_proximo % 60, second=0).strftime('%H:%M')
                        
                        print(f"⚠️ PREPARARSE: {nombre} en zona {tipo}")
                        print(f"Señal: {'🟢 COMPRA' if 'Alcista' in tipo else '🛑 VENTA'}")
                        print(f"Entrada exacta: {hora_entrada}") # Siempre múltiplo de 4
                        print(f"Zona de precio: {zona:.4f}")
                        print("-" * 30)
                except Exception as e:
                    print(f"Error analizando {nombre}: {e}")
            
            time.sleep(12) # Evitar duplicados
        
        time.sleep(1)
        

import yfinance as yf
import time
import pytz
from datetime import datetime

def detectar_fvg_ob(df):
    v = df.iloc[-3:]
    # FVG alcista: el minimo de la vela actual es mayor al maximo de hace dos velas
    if v['Low'].iloc[-1] > v['High'].iloc[-3]:
        return "FVG Alcista", v['Low'].iloc[-3]
    # FVG bajista: el maximo de la vela actual es menor al minimo de hace dos velas
    elif v['High'].iloc[-1] < v['Low'].iloc[-3]:
        return "FVG Bajista", v['High'].iloc[-3]
    return None, 0

def run_bot():
    print("--- SCANNER SMC (MODO PREPARACIÓN 1 MIN) ACTIVO ---", flush=True)
    simbolos = {'BTC': 'BTC-USD', 'GBP/USD': 'GBPUSD=X'}
    
    while True:
        zona_horaria = pytz.timezone('America/Bogota')
        ahora = datetime.now(zona_horaria)
        
        # CAMBIO: Analiza en el minuto 2, 6, 10... para darte tiempo de preparación
        if ahora.minute % 4 == 2 and 50 <= ahora.second <= 59:
            print(f"\n--- EVALUANDO CICLO ANTICIPADO: {ahora.strftime('%H:%M:%S')} ---", flush=True)
            
            for nombre, ticker in simbolos.items():
                try:
                    df = yf.Ticker(ticker).history(period="1d", interval="1m").tail(10)
                    tipo, zona = detectar_fvg_ob(df)
                    
                    if tipo:
                        # Calcula el siguiente minuto múltiplo de 4
                        minuto_proximo = ((ahora.minute // 4) + 1) * 4
                        hora_entrada = ahora.replace(minute=minuto_proximo % 60, second=0).strftime('%H:%M')
                        
                        print(f"⚠️ PREPARARSE: {nombre} en zona {tipo}", flush=True)
                        print(f"Señal: {'🟢 COMPRA' if 'Alcista' in tipo else '🛑 VENTA'}", flush=True)
                        print(f"Entrada exacta: {hora_entrada}", flush=True)
                        print(f"Zona de precio: {zona:.4f}", flush=True)
                        print("-" * 30, flush=True)
                    else:
                        print(f"ℹ️ {nombre}: Analizado. Sin patrones claros en este ciclo.", flush=True)
                except Exception as e:
                    print(f"Error analizando {nombre}: {e}", flush=True)
            
            time.sleep(12)
        
        # Latido para saber que sigue vivo
        if ahora.second == 0:
            print(f"⏱️ Bot activo... {ahora.strftime('%H:%M:%S')}. Esperando ciclo de análisis.", flush=True)
            time.sleep(1.5)
            
        time.sleep(0.5)

if __name__ == "__main__":
    run_bot()
    

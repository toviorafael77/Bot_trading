import yfinance as yf
import time
import pytz
from datetime import datetime

def detectar_fvg_ob(df):
    v = df.iloc[-3:]
    # FVG alcista
    if v['Low'].iloc[-1] > v['High'].iloc[-3]:
        return "FVG Alcista", v['Low'].iloc[-3]
    # FVG bajista
    elif v['High'].iloc[-1] < v['Low'].iloc[-3]:
        return "FVG Bajista", v['High'].iloc[-3]
    return None, 0

def run_bot():
    # flush=True obliga a Railway a mostrar el texto en pantalla de inmediato
    print("--- SCANNER SMC (CICLO 4 MIN) ACTIVO Y ESCANEANDO ---", flush=True)
    simbolos = {'BTC': 'BTC-USD', 'GBP/USD': 'GBPUSD=X'}
    
    while True:
        zona_horaria = pytz.timezone('America/Bogota')
        ahora = datetime.now(zona_horaria)
        
        # Filtro de tiempo: Analizar en el segundo 50 del minuto múltiplo de 4 menos 1 (Ej: XX:51:50, XX:55:50, XX:59:50)
        if ahora.minute % 4 == 3 and 50 <= ahora.second <= 59:
            print(f"\n--- EVALUANDO CICLO INSTITUCIONAL: {ahora.strftime('%H:%M:%S')} ---", flush=True)
            
            for nombre, ticker in simbolos.items():
                try:
                    df = yf.Ticker(ticker).history(period="1d", interval="1m").tail(10)
                    tipo, zona = detectar_fvg_ob(df)
                    
                    if tipo:
                        minuto_actual = ahora.minute
                        minuto_proximo = ((minuto_actual // 4) + 1) * 4
                        hora_entrada = ahora.replace(minute=minuto_proximo % 60, second=0).strftime('%H:%M')
                        
                        print(f"⚠️ PREPARARSE: {nombre} en zona {tipo}", flush=True)
                        print(f"Señal: {'🟢 COMPRA' if 'Alcista' in tipo else '🛑 VENTA'}", flush=True)
                        print(f"Entrada exacta: {hora_entrada}", flush=True)
                        print(f"Zona de precio: {zona:.4f}", flush=True)
                        print("-" * 30, flush=True)
                    else:
                        # Esto te dará tranquilidad: saber que sí analizó pero no hubo entrada válida
                        print(f"ℹ️ {nombre}: Analizado. Sin patrones OB/FVG claros en este ciclo.", flush=True)
                except Exception as e:
                    print(f"Error analizando {nombre}: {e}", flush=True)
            
            time.sleep(12) # Evita repetir el análisis en el mismo bloque de segundos
        
        # Latido del reloj: Te avisa cada minuto en el segundo 0 que el bot sigue vivo
        if ahora.second == 0:
            print(f"⏱️ Bot activo... Hora: {ahora.strftime('%H:%M:%S')}. Esperando ciclo de 4 min.", flush=True)
            time.sleep(1.5)
            
        time.sleep(0.5)

if __name__ == "__main__":
    run_bot()
    

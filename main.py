import yfinance as yf
import time
import pytz
from datetime import datetime

def detectar_fvg_ob(df):
    # Lógica simplificada: buscamos desequilibrios en las últimas 5 velas
    v = df.iloc[-3:]
    # FVG alcista: el minimo de la vela actual es mayor al maximo de hace dos velas
    if v['Low'].iloc[-1] > v['High'].iloc[-3]:
        return "FVG Alcista", v['Low'].iloc[-3]
    # FVG bajista: el maximo de la vela actual es menor al minimo de hace dos velas
    elif v['High'].iloc[-1] < v['Low'].iloc[-3]:
        return "FVG Bajista", v['High'].iloc[-3]
    return None, 0

def run_bot():
    print("--- SCANNER SMC (OB + FVG) ACTIVO ---")
    simbolos = {'BTC': 'BTC-USD', 'GBP/USD': 'GBPUSD=X'}
    
    while True:
        zona_horaria = pytz.timezone('America/Bogota')
        ahora = datetime.now(zona_horaria)
        
        # Analizamos en el segundo 50 para avisar antes del cambio de minuto
        if 50 <= ahora.second <= 59:
            print(f"\n--- HORA: {ahora.strftime('%H:%M:%S')} ---")
            
            for nombre, ticker in simbolos.items():
                try:
                    df = yf.Ticker(ticker).history(period="1d", interval="1m").tail(10)
                    tipo, zona = detectar_fvg_ob(df)
                    
                    if tipo:
                        sig_minuto = (ahora.minute + 1) % 60
                        hora_entrada = ahora.replace(minute=sig_minuto, second=0).strftime('%H:%M')
                        
                        print(f"⚠️ PREPARARSE: {nombre} detectado en zona {tipo}")
                        print(f"Señal: {'🟢 COMPRA' if 'Alcista' in tipo else '🛑 VENTA'}")
                        print(f"Entrada exacta: {hora_entrada}")
                        print(f"Zona de precio: {zona:.4f}")
                        print("-" * 30)
                except Exception as e:
                    print(f"Error analizando {nombre}: {e}")
            
            time.sleep(12)
        
        time.sleep(1)

if __name__ == "__main__":
    run_bot()
    

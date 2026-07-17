import yfinance as yf
import pandas as pd
import time
from datetime import datetime

symbols = {"GBP/USD": "GBPUSD=X", "Bitcoin": "BTC-USD"}

def obtener_datos(symbol):
    # Obtenemos velas de 1 minuto para el análisis en tiempo real
    data = yf.download(symbol, period="1d", interval="1m", progress=False)
    return data.tail(3)

def verificar_fvg(df):
    if len(df) < 3: return None
    v1, v2, v3 = df.iloc[0], df.iloc[1], df.iloc[2]
    
    # Regla: FVG Alcista (Mecha 1 sup < Mecha 3 inf)
    if v1['High'] < v3['Low'] and v2['Close'] > v2['Open']:
        return "compra 🟢"
    # Regla: FVG Bajista (Mecha 1 inf > Mecha 3 sup)
    elif v1['Low'] > v3['High'] and v2['Close'] < v2['Open']:
        return "venta 🛑"
    return None

print("Bot listo. Monitoreando mercado para scalping...")

while True:
    for name, ticker in symbols.items():
        df = obtener_datos(ticker)
        senal = verificar_fvg(df)
        
        if senal:
            # La hora del mensaje es el momento de confirmación
            # Entras al inicio del siguiente minuto
            hora_confirmacion = datetime.now().strftime("%H:%M")
            print(f"Señal {senal}")
            print(f"Entrada sugerida {hora_confirmacion}")
            print("Acción: Entrar al inicio del siguiente minuto.")
            print("-" * 30)
            
    # Pausa estratégica para evitar saturar el servidor
    time.sleep(55) 

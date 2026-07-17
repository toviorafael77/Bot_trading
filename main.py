import yfinance as yf
import pandas as pd
import time
from datetime import datetime

symbols = {"GBP/USD": "GBPUSD=X", "Bitcoin": "BTC-USD"}

def obtener_datos(symbol):
    # Descargamos los datos
    data = yf.download(symbol, period="1d", interval="1m", progress=False)
    # Nos aseguramos de devolver las últimas 3 velas
    return data.tail(3)

def verificar_fvg(df):
    if len(df) < 3: return None
    
    # Extraemos el valor numérico (escalar) de cada vela
    # Usamos .iloc[0] para la fila y accedemos al valor
    v1_high = df.iloc[0]['High']
    v1_low  = df.iloc[0]['Low']
    v2_open = df.iloc[1]['Open']
    v2_close = df.iloc[1]['Close']
    v3_high = df.iloc[2]['High']
    v3_low  = df.iloc[2]['Low']
    
    # Regla: FVG Alcista (Mecha 1 sup < Mecha 3 inf)
    if v1_high < v3_low and v2_close > v2_open:
        return "compra 🟢"
    # Regla: FVG Bajista (Mecha 1 inf > Mecha 3 sup)
    elif v1_low > v3_high and v2_close < v2_open:
        return "venta 🛑"
    return None

print("Bot corregido y activo...")

while True:
    for name, ticker in symbols.items():
        try:
            df = obtener_datos(ticker)
            senal = verificar_fvg(df)
            
            if senal:
                hora = datetime.now().strftime("%H:%M")
                print(f"Señal {senal}")
                print(f"Entrada sugerida {hora}")
        except Exception as e:
            print(f"Error analizando {name}: {e}")
            
    time.sleep(60) 

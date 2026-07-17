//@version=5
indicator("Scalping FVG - Aviso Anticipado", overlay=true)

// Detección de FVG en desarrollo (Vela 1 y 2 formadas)
// El bot evalúa el espacio antes de que cierre la vela 3
bullish_setup = high[1] < low[0] // Espacio alcista en formación
bearish_setup = low[1] > high[0] // Espacio bajista en formación

// Alerta con tiempo de preparación
if bullish_setup
    label.new(bar_index, high, text="PREPARAR COMPRA 🟢\nAnalizando zona...", color=color.orange, style=label.style_label_down)
    alert("Señal compra 🟢 - Preparar entrada en 1-2 min", alert.freq_once_per_bar)

if bearish_setup
    label.new(bar_index, low, text="PREPARAR VENTA 🛑\nAnalizando zona...", color=color.orange, style=label.style_line)
    alert("Señal venta 🛑 - Preparar entrada en 1-2 min", alert.freq_once_per_bar)

// Ejecución del formato fijo cuando la señal se confirma al cerrar la vela
bullish_fvg = high[2] < low[0] and close[1] > open[1]
bearish_fvg = low[2] > high[0] and close[1] < open[1]

if bullish_fvg
    label.new(bar_index, low, text="Señal compra 🟢\nEntrada sugerida " + str.tostring(hour) + ":" + str.tostring(minute), color=color.green, textcolor=color.white, style=label.style_label_up)

if bearish_fvg
    label.new(bar_index, high, text="Señal venta 🛑\nEntrada sugerida " + str.tostring(hour) + ":" + str.tostring(minute), color=color.red, textcolor=color.white, style=label.style_label_down)

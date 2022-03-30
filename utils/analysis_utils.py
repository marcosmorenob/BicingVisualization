from datetime import datetime
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

def insertHours_button(fig, times):
    buttons = []

    for i, time in enumerate(times[:-1]):
        args = [False] * len(times)
        args[i] = True
        
        button = dict(label = str(time) + "-" + str(times[i+1]),
                    method = "update",
                    args=[{"visible": args}])
        
        buttons.append(button)
        
    fig.update_layout(
        updatemenus=[dict(
                        active=0,
                        type="dropdown",
                        buttons=buttons,
                        x = 0,
                        y = 1.1,
                        xanchor = 'left',
                        yanchor = 'bottom'
                    )], 
        autosize=False,
        width=1000,
        height=800
    )

def ask_times():
    print('Introduce dos horas en el formato hh:mm para seleccionar el rango de tiempo:\nHora 1:')
    time1 = str(input())
    print('Hora 2:')
    time2 = str(input())
    return time1, time2

def generate_times(time1, time2):
    time1 = datetime.strptime(time1, '%H:%M')
    time2 = datetime.strptime(time2, '%H:%M')
    times = pd.date_range(time1, time2, freq='5min').tolist()
    return [time.time() for time in times]    

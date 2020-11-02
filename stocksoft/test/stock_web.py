import PySimpleGUI as sg
import requests
import json
import matplotlib.pyplot as plt #plt用于显示图片
import matplotlib.image as mping #mping用于读取图片
import datetime as dt
import matplotlib.dates as mdates
from pylab import *

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash()

server = app.server

# def draw(price,date):
#     fig = plt.figure()
#     #fig.suptitle('figure title demo', fontsize=14, fontweight='bold')
#     ax = fig.add_subplot(1, 1, 1)
#     xticks = list(range(0, len(date), 20))  # 这里设置的是x轴点的位置（40设置的就是间隔了）
#     xlabels = [date[x] for x in xticks]  # 这里设置X轴上的点对应在数据集中的值（这里用的数据为totalSeed）
#     xticks.append(len(date))
#     xlabels.append(date[-1])
#     ax.set_xticks(xticks)
#     ax.set_xticklabels(xlabels, rotation=40)
#     ax.plot(date, price)
#     #ax.set_xlabel("x label")
#     #ax.set_ylabel("y label")
#     plt.savefig('./1.png')
#
def get_price(code, type):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=8188&from_mid=1&query={code}&' \
          'hilight=disp_data.*.title&eprop={type}'.format(code=code, type=type)
    res = requests.get(url, headers = header)
    data = json.loads(res.text)
    price = []
    date = []
    if data.get('status') == '0':
        disp_data = data.get('data')[0].get('disp_data')[2]
        property = disp_data.get('property')
        text = property[0].get('data').get('display').get('tab').get('p')
        price_date = text.split(';')
        for i in price_date:
            l = i.split(',')
            if len(l) > 1:
                price.append(l[1])
                date.append(l[0])
        return price,date
#
# def client():
#     layout = [[sg.Text("Input your stock code")],
#               [sg.Input(key="input")],
#               [sg.Text(size=(80,1), key='output')],
#               [sg.Button('ok'), sg.Button('Quit'), sg.Button('test')],
#               ]
#
#     window = sg.Window('test', layout, no_titlebar=True, alpha_channel=0.7)
#     sg.theme('dark grey 9')
#
#     while True:
#         event, values = window.read()
#         if event == sg.WINDOW_CLOSED or event == 'Quit':
#             break
#         elif event == 'ok':
#             #text = get_price(values['input'])
#             price, date = get_price('002500', 'minute')
#             img = draw(price, date)
#             window['output'].update(img)
#
#     window.close()


def get_show_scatter(sctx, scty):
    trace = go.Scatter(
        x=sctx,
        y=scty,
        name='股票走势图'
    )
    layout=go.Layout(
        title='分时图',
        yaxis={
            'hoverformat': '' #如果想显示小数点后两位'.2f'，显示百分比'.2%'
        }
    )
    return go.Figure(
        data = [trace],
        layout = layout
    )

scty, sctx = get_price('002500', 'minute')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.Graph(
        id='show_scatter',
        figure=get_show_scatter(sctx, scty)
    ),
],)

if __name__ == '__main__':
    from livereload import Server

    server = Server(app.run_server())
    server.watch('**/*.*')
    server.serve()
    #app.run_server(debug=True)

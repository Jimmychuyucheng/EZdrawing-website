#載入
from flask import Flask, render_template, request
import base64
import io

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from ellipsegif import main as ellipsegif
from hypergif import main as hypergif
from paragif import main as paragif

#建立application物件
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static" 
)   #所有在static資料夾下的檔案，都對應到網址路徑/static/


#建立路徑 "/" 對應的處理函式 
@app.route('/')   
def hello():  #用來回應路徑 / 的處理函式 
    return render_template('index1.html')

#前後端資料接收與發送之路由(靜態圖片)
@app.route("/calculate_elipse")
def calculate_elipse():
    try: 
        a2 = int(request.args.get("a2", 0))
        b2 = int(request.args.get("b2", 0))
        h = int(request.args.get("h", 0))    
        k = int(request.args.get("k", 0))
        print("elipse running")
        image_data = drawelipse(a2,b2,h,k)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return render_template('result.html',file_name=f"data:image/png;base64,{encoded_image}",title_name='ellipse plot' )
        # return Response(image_data, mimetype='image/png')
    except ValueError:
        return "Error: Please enter valid integer values for a2, b2, h, and k."
@app.route("/calculate_parabola1")
def calculate_parabola1():
    try:    
        p = int(request.args.get("p"))
        h = int(request.args.get("h", 0))
        k = int(request.args.get("k", 0)) 
        print("parabola1 running")
        image_data = drawparabola1(p, h, k)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return render_template('result.html',file_name=f"data:image/png;base64,{encoded_image}",title_name='parabola plot' )
    except ValueError:
        return "Error: Please enter valid integer values for 4c, h, and k."
@app.route("/calculate_parabola2")
def calculate_parabola2():
    try:   
        p = int(request.args.get("p"))
        h = int(request.args.get("h", 0))
        k = int(request.args.get("k", 0)) 
        print("parabola2 running")
        image_data = drawparabola2(p, h, k)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return render_template('result.html',file_name=f"data:image/png;base64,{encoded_image}",title_name='parabola plot' )
    except ValueError:
        return "Error: Please enter valid integer values for 4c, h, and k."
@app.route("/calculate_hyperbola1")
def calculate_hyperbola1():
    try:  
        a2 = int(request.args.get("a2"))
        b2 = int(request.args.get("b2"))
        h = int(request.args.get("h", 0))
        k = int(request.args.get("k", 0)) 
        print("hyperbola1 running")
        image_data = drawhyperbola1(a2,b2,h,k)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return render_template('result.html',file_name=f"data:image/png;base64,{encoded_image}",title_name='hyperbola pair plot' )
    except ValueError:
        return "Error: Please enter valid integer values for a2, b2, h, and k."
@app.route("/calculate_hyperbola2")
def calculate_hyperbola2():
    try:
        b2 = int(request.args.get("b2"))
        a2 = int(request.args.get("a2"))
        h = int(request.args.get("h", 0))
        k = int(request.args.get("k", 0)) 
        print("hyperbola2 running")
        image_data = drawhyperbola2(a2,b2,h,k)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return render_template('result.html',file_name=f"data:image/png;base64,{encoded_image}",title_name='hyperbola pair plot' )
    except ValueError:
        return "Error: Please enter valid integer values for a2, b2, h, and k."

#動圖路由
@app.route("/ellipsegif")
def calculate_elipsegif():
    try: 
        x_b = int(request.args.get("x_b", 0))
        y_b = int(request.args.get("y_b", 0))
        r_b = int(request.args.get("r_b", 0))
        x_s = int(request.args.get("x_s", 0))
        y_s = int(request.args.get("y_s", 0))
        r_s = int(request.args.get("r_s", 0))
        print("elipsegif running")
        ellipsegif(x_b,y_b,r_b,x_s,y_s,r_s)
        return render_template('result.html',file_name="/static/gif/oval.gif",title_name="ellipse Gif")
        # return Response(image_data, mimetype='image/png')
    except ValueError:
        return "Error: Please enter valid integer values for a2, b2, h, and k."

@app.route("/hypergif")
def calculate_hypergif():
    try: 
        x_b = int(request.args.get("x_b", 0))
        y_b = int(request.args.get("y_b", 0))
        r_b = int(request.args.get("r_b", 0))
        x_s = int(request.args.get("x_s", 0))
        y_s = int(request.args.get("y_s", 0))
        r_s = int(request.args.get("r_s", 0))
        print("hyper gif running")
        hypergif(x_b,y_b,r_b,x_s,y_s,r_s)
        return render_template('result2.html',file_name1="/static/gif/hyperbolic_inner.gif",file_name2="/static/gif/hyperbolic_outer.gif", title_name1="hyperbola pair Gif 與兩圓均內切", title_name2="hyperbola pair Gif 與兩圓均外切")
    except (ValueError, ZeroDivisionError):
        return "Error: Please enter valid integer values for a2, b2, h, and k."

@app.route("/paragif")
def calculate_paragif():
    try: 
        x_or_y = request.args.get("x_or_y")
        m = int(request.args.get("m", 0))
        c_0_x = int(request.args.get("c_0_x", 0))
        c_0_y = int(request.args.get("c_0_y", 0))
        c_0_r = int(request.args.get("c_0_r", 0))
        print("para gif running")
        paragif(x_or_y,m,c_0_x,c_0_y,c_0_r)
        return render_template('result.html', file_name="/static/gif/parabola.gif", title_name="parabola Gif")
    except ValueError:
        return "Error: Please enter valid integer values for a2, b2, h, and k."
@app.route('/calculator')
def calculator():
    return render_template('index2.html')

#畫圖函式
def drawelipse(a2, b2, h, k):
    a = np.sqrt(a2)
    b = np.sqrt(b2)
    # 計算焦點的位置、C
    if a > b:
        c = np.sqrt(a**2 - b**2)
    else:
        c = np.sqrt(b**2 - a**2)
    # 生成橢圓的角度值
    theta = np.linspace(0, 2*np.pi, 100)
    # 計算橢圓上的點的坐標
    x = h + a * np.cos(theta)  # 將 x 坐標移動到中心點
    y = k + b * np.sin(theta)  # 將 y 坐標移動到中心點
    # 繪製橢圓
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x,y)
    # 標出焦點、中心
    if a > b:
        axis.scatter([h+c, h-c], [k, k], color='red', label=f'Foci: ({h+c:.1f},{k}) and ({h-c:.1f},{k})')
    else:
        axis.scatter([h, h], [k+c, k-c], color='red', label=f'Foci: ({h},{k+c:.1f}) and ({h},{k-c:.1f})')
    axis.scatter(h,k, color='orange', label=f'center: ({h}, {k})')

    # 設置坐標軸的範圍
    axis.set_xlim(h - a - 1,h + a + 1)
    axis.set_ylim(k - b - 1,k + b + 1)
    axis.set_aspect('equal', adjustable='box')  # 設置坐標軸比例為相等
    axis.set_title(f'Ellipse: $(x-{h})^2/{a**2:.0f} + (y-{k})^2/{b**2:.0f} = 1$')  # 修改標題為橢圓的標準式
    axis.set_xlabel('X-axis')
    axis.set_ylabel('Y-axis')
    axis.grid(True)
    axis.legend(loc='upper right')  # 將標籤放在右上角
    # 將圖像保存到 BytesIO 對象中
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
def drawparabola1(p, h, k):
    # 計算焦點的位置
    c = p / 4
    f = (h, k + c)
    # 生成拋物線的 x 坐標
    if c > 0:
        x = np.linspace(-(5 * c) -5, 5 *c + 5, 400)
    else:
        x = np.linspace(5 * c - 5, -(5 *c) + 5, 400)
    # 計算拋物線的 y 坐標
    y = ((x - h)**2) / (4 * c) + k
    #準線方程式
    directrix = k - c
    # 繪製拋物線
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x,y)
    # 準線
    axis.axhline(y=directrix, color='green', linestyle='--', label=f'Directrix: $y = {k-c}$')
    # 標出焦點、中心
    axis.scatter(h, k+c, color='red', label=f'Foci: ({h}, {k+c:.1f})')
    axis.scatter(h, k, color='orange', label=f'Center: ({h}, {k})')
    # 設定坐標軸的範圍
    if c > 0:
        axis.set_ylim(k - 4 * c - 10, k + 8 * c + 10) #之後可能用if statment來判定是要往左上右下哪邊取多一點
        axis.set_xlim(-(5 * c) -5, 5 *c + 5)   
    else:
        axis.set_ylim((k + 8 * c- 10, k - 4 * c + 10))
        axis.set_xlim(5 * c - 5, -(5 *c) + 5)
    axis.set_title(f'Parabola: $y = (x-{h})^2/{p} + {k}$')  # 標題
    axis.set_xlabel('X-axis')  # X 軸標籤
    axis.set_ylabel('Y-axis')  # Y 軸標籤
    axis.grid(True)  # 顯示網格線
    if c < 0:
        axis.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95), prop={'size': 6})  # 將標籤放在中間上方
    else:
        axis.legend(loc='upper center', bbox_to_anchor=(0.5, 0.25), prop={'size': 6})
    axis.set_aspect('equal', adjustable='box')  # 設置坐標軸比例為相等# plt.gca().set_aspect('equal', adjustable='box')  # 設置坐標軸比例為相等
    # 將圖像保存到 BytesIO 對象中
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
def drawparabola2(p, h, k):
     # 計算焦點的位置
    c = p / 4
    f = (h + c, k)
    # 生成拋物線的 y 坐標
    if c > 0:
        y = np.linspace(-(5 * c) - 5, 5 *c + 5)
    else:
        y = np.linspace((5 * c) - 5, -(5 *c) + 5)
    # 計算拋物線的 x 坐標
    x = (y - k)**2 / (4 * c) + h
    # 準線方程式
    directrix = h - c
    # 繪製拋物線
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y)

    # 準線
    axis.axvline(x=directrix, color='green', linestyle='--', label=f'Directrix: $x = {h-c}$')
    # 標出焦點、中心
    axis.scatter(h+c, k, color='red', label=f'Foci: ({h+c:.1f}, {k})')
    axis.scatter(h, k, color='orange', label=f'Center: ({h}, {k})')

    # 設定坐標軸的範圍
    if c > 0:
        axis.set_xlim(h - 4 * c - 10, h + 8 * c + 10) # 之後可能用 if statement 判定是要往左右取多一點
        axis.set_ylim(-(5 * c) -5, 5 *c + 5)
    else:
        axis.set_xlim((h + 8 * c -10, h - 4 * c + 10))
        axis.set_ylim((5 * c) -5, -(5 *c) + 5)
    axis.set_title(f'Parabola: $x = ((y - {k})^2) / {p} + {h}$')  # 標題
    axis.set_xlabel('X-axis')  # X 軸標籤
    axis.set_ylabel('Y-axis')  # Y 軸標籤
    axis.grid(True)  # 顯示網格線
    if c < 0:
        axis.legend(loc='upper center', bbox_to_anchor=(0.2, 0.55), prop={'size': 7})  # 將標籤放在中間上方
    else:
        axis.legend(loc='upper center', bbox_to_anchor=(0.8, 0.55), prop={'size': 7})
    axis.set_aspect('equal', adjustable='box')  # 設置坐標軸比例為相等

    # 將圖像保存到 BytesIO 對象中
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
def drawhyperbola1(a2, b2, h, k):
    a = np.sqrt(a2)
    b = np.sqrt(b2)
    print(a)
    # 生成雙曲線的角度值
    theta = np.linspace(-1*np.pi, 1*np.pi, 1000)

    # 計算雙曲線上的點的坐標
    x_right = h + a * np.cosh(theta)
    y_right = k + b * np.sinh(theta)
    x_left = h - a * np.cosh(theta)
    y_left = k - b * np.sinh(theta)

    # 計算焦點的位置
    c = np.sqrt(a**2 + b**2)
    f1 = (h + c, k)
    f2 = (h - c, k)

    # 繪製拋物線
    fig = Figure(figsize=(8,7))
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x_right, y_right, color='blue', label="hyperbola pair")  
    axis.plot(x_left, y_left, color='blue')
    # 繪製漸進線
    x_asymptote = np.linspace(h - 100, h + 100, 100)  # 漸進線的 x 坐標
    y_asymptote1 = k + (b / a) * (x_asymptote - h)  # 漸進線1的 y 坐標
    y_asymptote2 = k - (b / a) * (x_asymptote - h)  # 漸進線2的 y 坐標
    axis.plot(x_asymptote, y_asymptote1, linestyle='--', color='green', label='Asymptote 1')
    axis.plot(x_asymptote, y_asymptote2, linestyle='--', color='green', label='Asymptote 2')
    # 繪製焦點
    axis.scatter(f1[0], f1[1], color='red', label=f'Foci 1: ({f1[0]:.1f}, {f1[1]:.1f})')
    axis.scatter(f2[0], f2[1], color='red', label=f'Foci 2: ({f2[0]:.1f}, {f2[1]:.1f})')
    # 標出中心
    axis.scatter(h, k, color='orange', label=f'Center: ({h}, {k})')
    axis.set_xlabel('X-axis')
    axis.set_ylabel('Y-axis') 
    #左右開口漸近線
    def display_asymptotes(a2, b2, num1, num2):
        if isinstance(a, int) or a.is_integer():
            asymptote1_a = str(int(a))
        else:
            asymptote1_a = rf'$\sqrt{{{a2}}}$'

        if isinstance(b, int) or b.is_integer():
            asymptote1_b = str(int(b))
        else:
            asymptote1_b = rf'$\sqrt{{{b2}}}$'

        asymptote2_a = asymptote1_a
        asymptote2_b = asymptote1_b

        # if not isinstance(a2, int):
        #     asymptote1_a = rf'√{a2}'
        #     asymptote2_a = rf'√{a2}'

        # if not isinstance(b2, int):
        #     asymptote1_b = rf'√{b2}'
        #     asymptote2_b = rf'√{b2}'

        asymptote1 = f'asymptote1: {asymptote1_a}x + {asymptote1_b}y = {num1:.1f}'
        asymptote2 = f'asymptote2: {asymptote2_a}x - {asymptote2_b}y = {num2:.1f}'

        return asymptote1, asymptote2
    num1 = b * h + a * k
    num2 = b * h - a * k  
    asymptote1, asymptote2 = display_asymptotes(a2, b2, num1, num2)
    axis.set_title(rf'Hyperbola Pair: $(x-{h})^2/{a2}-(y-{k})^2/{b2})=1$'+'\n'
                   +asymptote1 + '\n' + asymptote2, fontsize=10) 
    axis.grid(True)
    axis.legend(loc='upper center', bbox_to_anchor=(0.5, 0.35), prop={'size': 7})
    axis.set_aspect('equal', adjustable='box')  # 設置坐標軸比例為相等

    # 設定坐標軸的範圍
    axis.set_xlim(h - 4 * a - 10 , h + 4 * a + 10)
    axis.set_ylim(k - 4 * b - 10 , k + 4 * b + 10)

    # 將圖像保存到 BytesIO 對象中
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
def drawhyperbola2(a2, b2, h, k):
    a = np.sqrt(a2)
    b = np.sqrt(b2)

    # 生成雙曲線的角度值
    theta = np.linspace(-1*np.pi, 1*np.pi, 1000)

    # 計算雙曲線上的點的坐標
    x_right = h + b * np.sinh(theta)
    y_right = k + a * np.cosh(theta)
    x_left = h - b * np.sinh(theta)
    y_left = k - a * np.cosh(theta)

    # 計算焦點的位置
    c = np.sqrt(a**2 + b**2)
    f1 = (h, k + c)
    f2 = (h, k - c)

    # 繪製雙曲線
    fig = Figure(figsize=(8,7))
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x_right, y_right, color='blue', label="hyperbola pair")  
    axis.plot(x_left, y_left, color='blue')

    # 繪製漸進線
    x_asymptote = np.linspace(h - 100, h + 100, 100)  # 漸進線的 x 坐標
    y_asymptote1 = k + (a / b) * (x_asymptote - h)  # 漸進線1的 y 坐標
    y_asymptote2 = k - (a / b) * (x_asymptote - h)  # 漸進線2的 y 坐標
    axis.plot(x_asymptote, y_asymptote1, linestyle='--', color='green', label='Asymptote 1')
    axis.plot(x_asymptote, y_asymptote2, linestyle='--', color='green', label='Asymptote 2')

    # 繪製焦點
    axis.scatter(f1[0], f1[1], color='red', label=f'Foci 1: ({f1[0]:.1f}, {f1[1]:.1f})')
    axis.scatter(f2[0], f2[1], color='red', label=f'Foci 2: ({f2[0]:.1f}, {f2[1]:.1f})')

    # 標出中心
    axis.scatter(h, k, color='orange', label=f'Center: ({h}, {k})')
    axis.set_xlabel('X-axis')
    axis.set_ylabel('Y-axis') 

    # 設置標題(上下開口漸近線)
    def display_asymptotes(a2, b2, num1, num2):
        if isinstance(a, int) or a.is_integer():
            asymptote1_a = str(int(a))
        else:
            asymptote1_a = rf'$\sqrt{{{a2}}}$'

        if isinstance(b, int) or b.is_integer():
            asymptote1_b = str(int(b))
        else:
            asymptote1_b = rf'$\sqrt{{{b2}}}$'

        asymptote2_a = asymptote1_a
        asymptote2_b = asymptote1_b

        # if not isinstance(a2, int):
        #     asymptote1_a = rf'√{a2}'
        #     asymptote2_a = rf'√{a2}'

        # if not isinstance(b2, int):
        #     asymptote1_b = rf'√{b2}'
        #     asymptote2_b = rf'√{b2}'

        asymptote1 = f'asymptote1: {asymptote1_a}x + {asymptote1_b}y = {num1:.1f}'
        asymptote2 = f'asymptote2: {asymptote2_a}x - {asymptote2_b}y = {num2:.1f}'
        return asymptote1, asymptote2

    num1 = a * h + b * k
    num2 = a * h - b * k  
    asymptote1, asymptote2 = display_asymptotes(a2, b2, num1, num2)
    axis.set_title(rf'Hyperbola Pair: $(y-{k})^2/{a2}-(x-{h})^2/{b2})=1$'+'\n'
                   +asymptote1 + '\n' + asymptote2, fontsize=10) 
    axis.grid(True)
    axis.legend(loc='upper center', bbox_to_anchor=(0.2, 0.55), prop={'size': 7})
    axis.set_aspect('equal', adjustable='box')  # 設置坐標軸比例為相等

    # 設定坐標軸的範圍
    axis.set_xlim(h - 3 * a - 20 , h + 3 * a + 20)
    axis.set_ylim(k - 3 * b - 20 , k + 3 * b + 20)

    # 將圖像保存到 BytesIO 對象中
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()

#啟動網站伺服器(server)，可透過port決定埠號
if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
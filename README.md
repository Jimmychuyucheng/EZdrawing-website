# **EZdrawing互動式繪圖網站製作** 
<div class="name">松山高中 朱禹澄 賴致全</div> 



![EZdrawing心智圖](https://hackmd.io/_uploads/BJeEiTH1R.png)

附圖為本次專案的心智圖<br>右側說明開發網站的過程，從HTML撰寫前端使用者介面、CSS美編與排版設計，到後端繪圖與動畫生成函式庫編寫。最後使用Flask API網頁框架設計相應路由，串通使用者端和數據端的溝通。<br>左側則是部署網站的過程，從使用Replit作為編撰與修改程式的整合開發環境（IDE），並將資料作為檔案存放在Github上。最後，透過render.com提供的網路服務，獲得一個公開的連結與IP位置，讓所有人都能夠拜訪並體驗網站內的功能。


# *Flask API主程序app.py檔*
## 1.載入模組
```python=
#載入模組
from flask import Flask
from flask import render_template
from flask import request
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
#載入繪圖函式庫
from ellipsegif import main as ellipsegif
from hypergif import main as hypergif
from paragif import main as paragif
```
## 2.建立application物件
```python=
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static" 
)   #所有在static資料夾下的檔案，都對應到網址路徑/static/
```
## 3-1 建立初始路徑("/")對應的處理函式
```pyhton=
@app.route('/')   
def hello():  #用來回應路徑 / 的處理函式 
    return render_template('index1.html')
```
## 3-2 運行測試(顯示前端使用者資訊)
```python=
@app.route('/info')
def info():
    print("請求方法", request.method)
    print("通訊協定", request.scheme)
    print("主機名稱", request.host)
    print("路徑", request.path)  
    print("網址", request.url)
    print("瀏覽器和作業系統", request.headers.get("user-agent"))
    print("語言偏好", request.headers.get("accept-language"))
    print("引薦網址", request.headers.get("referrer"))
    return None
```
## 4.啟動網站伺服器
```python=
if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
```
## 5.建立網站功能(靜態圖片繪圖)對應的路由

#### 1.接收前端html form的字串並轉換成可計算的整數型式<br>2.在路由內呼叫繪圖函式繪圖 <br>3.使用try塊避免ValueError導制崩潰<br> 4.將圖片轉為二進制後利用base64編碼，使得前端HTML可以成功找到圖片並顯示
### 5-1橢圓
```python=
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
        return render_template('result.html',
                               file_name=f"data:image/png;base64,{encoded_image}",
                               title_name='ellipse plot' )
        # return Response(image_data, mimetype='image/png')
    except ValueError:
        return "Error: Please enter valid integer values for a2, b2, h, and k."
```
### 5-2拋物線<br>
#### 注: 拋物線需考慮上下或左右開口的型式，故有兩個分的路由
```python=
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
```
### 5-3雙曲線
#### 注: 雙曲線需考慮上下或左右開口的型式，故有兩個分別的路由
```python=
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

```
## 6.建立網站功能(動態圖片繪圖)對應的路由
### 6-1拋物線:與座標平面上一圓與一直線(鉛直或水平線)的第二圓圓心軌跡
```python=
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
```
### 6-2橢圓:與座標平面上兩圓(大圓包小圓)均相切的第三圓圓心軌跡
```python=
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
```
### 6-3雙曲線:與座標平面上兩不相交圓均內切或均外切的第三圓圓心軌跡
```python=
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

```
# *繪圖函式庫*
## 1.靜態圖片
### 1-1左右開口拋物線 
#### $$(y-k)^2=4c(x-h)$$

```python=
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
```
### 1-2上下開口拋物線 
#### $$(x-h)^2=4c(y-k)$$
```python=
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
```
### 2-1.橢圓
#### $$\frac{(x-h)^2}{a^2}+\frac{(y-k)^2}{b^2}=1$$
```python=
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
```
### 3-1左右開口雙曲線
#### $$\frac{(x-h)^2}{a^2}-\frac{(y-k)^2}{b^2}=1$$

```python=
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
```
### 3-2上下開口雙曲線
#### $$\frac{(x-h)^2}{a^2}-\frac{(y-k)^2}{b^2}=-1$$
```python=
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
```
## 2.動態圖片
### 1.與一直線和一圓相切之圓心的軌跡為拋物線
#### $$(x-h)^2=4c(y-k)或(y-k)^2=4c(x-h)$$

<br>

#### 主程序引入繪圖檔案(paragif.py檔)中的繪圖函式(main())
```python=
#app.py
from paragif import main as paragif
```
#### 繪圖檔案:paragif.py檔
```python=
from PIL import Image
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
from sympy import *
import datetime
root='static/gif/'
#1.x_or_y=m
#2.3.圓
#4.h,k,c 拋物線參數
def draw(x_or_y,m,c_0_x,c_0_y,c_0_r,c_a_x,c_a_y,c_a_r,h,k,c):
    range1=max(abs(int(h)),abs(int(k)))+10
    line = np.arange(-range1-1, range1+1, 1)
    #準線
    if x_or_y=="x":
        x_1=[m]*2*range1+[m]*2
        y_1=line
        #拋物線
        y_2= np.arange(-range1,range1, 0.01)
        x_2=(y_2-h)**2/4/c+k
    if x_or_y=="y":
        y_1=[m]*2*range1+[m]*2
        x_1=line
        #拋物線
        x_2= np.arange(-range1,range1, 0.01)
        y_2=(x_2-h)**2/4/c+k
    #題目圓
    theta = np.arange(0, 2*np.pi, 0.01)
    x_3= c_0_x + c_0_r * np.cos(theta)
    y_3= c_0_y + c_0_r * np.sin(theta)
    #解答圓
    x_4= c_a_x + c_a_r * np.cos(theta)
    y_4= c_a_y + c_a_r * np.sin(theta)

    fig = plt.figure(figsize=(7,7))
    axes = fig.add_subplot(111)

    axes.plot(x_1, y_1,c='g')
    axes.plot(x_2, y_2,c='b',label='Answer')
    axes.scatter(c_a_x,c_a_y,c='r')
    axes.plot(x_3, y_3,c='g',label='given')
    axes.plot(x_4, y_4,c='r',label='Circles')

    plt.legend(loc='upper right',fontsize=20,edgecolor='#000',title_fontsize=20)

    if x_or_y=="x":#準線為x=m (y-h)^2=...
        axes.set_title(r'Parabola=$(y-%.0f)^2=4(%.0f) (x-%.0f)$' %(h,c,k), fontsize=30)
    if x_or_y=="y":#準線為x=m (y-h)^2=...
        axes.set_title(r'Parabola=$(x-%.0f)^2=4(%.0f) (y-%.0f)$' %(h,c,k), fontsize=30)
    #控制大小
    plt.xlim(-range1,range1)
    plt.ylim(-range1,range1)
    plt.xticks(np.linspace(-range1,range1, 11))  
    plt.yticks(np.linspace(-range1,range1, 11))
    #座標軸繪製
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_position(('axes',0.5))
    axes.spines['left'].set_position(('axes',0.5))
    #plt.show()

#線'x_or_y'=m,小圓參數
def main(x_or_y,m,c_0_x,c_0_y,c_0_r):
    if x_or_y=='x':
        filenames = []
        d=abs(c_0_x-m)#已知圓心到線距離
        h=c_0_y
        k=c_0_x-(d-c_0_r)/2*abs(c_0_x-m)/(c_0_x-m)
        c=(d-c_0_r)/2*abs(c_0_x-m)/(c_0_x-m)
        #拋物險上點
        range1=max(abs(int(h)),abs(int(k)))+10
        y_2= np.arange(-range1,range1, 0.4)
        x_2=(y_2-h)**2/4/c+k
        
        for i in range(0,len(x_2)):
            print(len(x_2)-i)#確認剩餘迴圈
            R_2=abs(x_2[i]-m)
            draw(x_or_y,m,c_0_x,c_0_y,c_0_r,x_2[i],y_2[i],R_2,h,k,c)#平行移動的圓
            plt.savefig(f'{root}test1_'+str(i)+".png")
            filenames.append(f'{root}test1_'+str(i)+".png")#儲存檔名方便利用
    if x_or_y=='y':
        filenames = []
        d=abs(c_0_y-m)#已知圓心到線距離
        h=c_0_x
        k=c_0_y-(d-c_0_r)/2*abs(c_0_y-m)/(c_0_y-m)
        c=(d-c_0_r)/2*abs(c_0_y-m)/(c_0_y-m)
        #拋物險上點
        range1=max(abs(int(h)),abs(int(k)))+10
        x_2= np.arange(-range1,range1, 0.4)
        y_2=(x_2-h)**2/4/c+k
        
        for i in range(0,len(x_2)):
            print(len(x_2)-i)#確認剩餘迴圈
            R_2=abs(y_2[i]-m)
            draw(x_or_y,m,c_0_x,c_0_y,c_0_r,x_2[i],y_2[i],R_2,h,k,c)#平行移動的圓
            plt.savefig(f'{root}parabola_'+str(i)+".png")
            filenames.append(f'{root}parabola_'+str(i)+".png")#儲存檔名方便利用
    with imageio.get_writer(f'{root}parabola.gif', mode='I',loop=0) as writer:
        for filename in filenames:
            print(filename)
            image = imageio.imread(filename)
            writer.append_data(image)

    #刪除png檔
    for filename in filenames:
        os.remove(filename)
    print("Finished, GIF saved:parabola.gif")

if __name__=="__main__":
    dstart = datetime.datetime.now()
    main('y',5,2,0,1)
    dend = datetime.datetime.now()
    print(dend-dstart)
```
### 2.與兩圓(大圓包小圓)相切之圓心的軌跡為一橢圓 
#### $$\frac{(x-h)^2}{a^2}+\frac{(y-k)^2}{b^2}=1$$ 
#### 主程序引入繪圖檔案(ellipsegif.py檔)中的繪圖函式(main())
```python=
#app.py
from ellipsegif import main as ellipsegif
```
```python=
from PIL import Image
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
from sympy import *
import datetime
root='static/gif/'
#line 32 主程式：輸入[大圓x,大圓y,大圓r,小圓x,小圓y,小圓r]
def draw(a_1,b_1,r_1,a_2,b_2,r_2,Ans_x,Ans_y,Ans_r,x_a,y_a,x_v,y_v):
    #畫一個圖上三個圓
    theta = np.arange(0, 2*np.pi, 0.01)
    x_1= a_1 + r_1 * np.cos(theta)
    y_1= b_1 + r_1 * np.sin(theta)
    x_2= a_2 + r_2 * np.cos(theta)
    y_2= b_2 + r_2 * np.sin(theta)
    x_3= Ans_x + Ans_r * np.cos(theta)
    y_3= Ans_y + Ans_r * np.sin(theta)

    #繪圖
    fig = plt.figure(figsize=(7,7))
    axes = fig.add_subplot(111)
    axes.plot(x_1, y_1,c='g')
    axes.plot(x_2, y_2,c='g',label='given')
    axes.plot(x_3, y_3,c='r',label='Circles')
    axes.plot(x_a, y_a,c='b',label='Answer')
    axes.scatter(Ans_x,Ans_y,c='r')
    axes.set_title(r'Oval=$\frac{x^2}{%.2f^2}+\frac{y^2}{%.2f^2}$=1' %(x_v,y_v), fontsize=30)
    plt.legend(loc='upper right',fontsize=20,edgecolor='#000',title_fontsize=20)

    #控制大小
    range1=max(abs(a_1+r_1),abs(a_1-r_1),abs(a_2+r_1),abs(a_2-r_1))+1
    plt.xlim(-range1,range1)
    plt.ylim(-range1,range1)
    plt.xticks(np.linspace(-range1,range1, 11))  
    plt.yticks(np.linspace(-range1,range1, 11))
    #座標軸繪製
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_position(('axes',0.5))
    axes.spines['left'].set_position(('axes',0.5))

#不同解的xy座標
def main(x_b,y_b,r_b,x_s,y_s,r_s):
    Input=[x_b,y_b,r_b,x_s,y_s,r_s] #x_big,y_big...x_small,y_small...
    x_oval=(x_b+x_s)/2 #橢圓中心
    y_oval=(y_b+y_s)/2 #橢圓中心
    a_oval=(r_b+r_s)/2
    c_oval=((Input[0]-Input[3])**2+(Input[1]-Input[4])**2)**(1/2)/2
    b_oval=(a_oval**2-c_oval**2)**(1/2)
    if (Input[0]-Input[3])!=0 and (Input[1]-Input[4])==0:
        theta2 = np.arange(0, 2*np.pi+0.1, 0.2)
        x_a=x_oval+a_oval*np.cos(theta2)
        y_a=y_oval+b_oval*np.sin(theta2)
        x_v=a_oval**2
        y_v=b_oval**2
    elif(Input[0]-Input[3])==0 and (Input[1]-Input[4])!=0:
        theta2 = np.arange(0, 2*np.pi+0.1, 0.2)
        x_a=x_oval+b_oval*np.cos(theta2)
        y_a=y_oval+a_oval*np.sin(theta2)
        y_v=a_oval**2
        x_v=b_oval**2
    else:
        print("Error")
        exit(0)
    #繪製解答 圓族
    filenames = []
    for i in range(0,len(x_a)):
        print(len(x_a)-i)#確認剩餘迴圈
        d_s_a=((x_a[i]-x_s)**2+(y_a[i]-y_s)**2)**(1/2)#與小圓圓心距離
        r_a=d_s_a-Input[5]#與小圓圓心距離-r（小圓半徑）
        draw(Input[0],Input[1],Input[2],Input[3],Input[4],Input[5],x_a[i],y_a[i],r_a,x_a,y_a,x_v,y_v)#平行移動的圓
        plt.savefig(f'{root}oval_'+str(i)+".png")
        filenames.append(f'{root}oval_'+str(i)+".png")#儲存檔名方便利用

    # 生成gif

    with imageio.get_writer(f'{root}oval.gif', mode='I',loop=0) as writer:
        for filename in filenames:
            print(filename)
            image = imageio.imread(filename)
            writer.append_data(image)
    #刪除png檔

    for filename in filenames:
        os.remove(filename)
    print("Finished")

if __name__=="__main__":
    dstart = datetime.datetime.now()
    main(-1,0,4,1,0,1)
    dend = datetime.datetime.now()
    print(dend-dstart)
```
### 3.與兩圓均內切或外切之圓心的軌跡為一雙曲線對(均外切與均內切各為一
#### $$\frac{(x-h)^2}{a^2}-\frac{(y-k)^2}{b^2}=\pm1$$ 
#### 主程序引入繪圖檔案(hypergif.py檔)中的繪圖函式(main())
```python=
from hypergif import main as hypergif
```
```python=
from PIL import Image
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
from sympy import *
import datetime
# 雙曲線,三圓（Big,small,ans)
root='static/gif/'
def draw(b_x,b_y,b_r,s_x,s_y,s_r,ans_x,ans_y,ans_r,x_left_down,y_left_down,x_right_up,y_right_up,rlud,a,b,c):
    #畫一個圖上三個圓
    theta = np.arange(0, 2*np.pi, 0.01)
    #大圓
    x_1= b_x + b_r * np.cos(theta)
    y_1= b_y + b_r * np.sin(theta)
    #小圓
    x_2= s_x + s_r * np.cos(theta)
    y_2= s_y + s_r * np.sin(theta)
    #解答圓
    x_3= ans_x + ans_r * np.cos(theta)
    y_3= ans_y + ans_r * np.sin(theta)

    #繪圖
    fig = plt.figure(figsize=(7,7))
    axes = fig.add_subplot(111)
    axes.plot(x_1, y_1,c='g')
    axes.plot(x_2, y_2,c='g',label='given')
    axes.plot(x_3, y_3,c='r',label='Circles')
    axes.plot(x_left_down, y_left_down,c='b',label='Answer')
    axes.plot(x_right_up, y_right_up,c='b')
    axes.scatter(ans_x,ans_y,c='r')
    if rlud=="rightleft":
        axes.set_title(r'Hyperbolic=$\frac{x^2}{%.2f^2}-\frac{y^2}{%.2f^2}=1$' %(a,b), fontsize=20)
    elif rlud=="updown":
        axes.set_title(r'Hyperbolic=$\frac{y^2}{%.2f^2}-\frac{x^2}{%.2f^2}=1$' %(a,b), fontsize=20)
    plt.legend(loc='upper right', bbox_to_anchor=(0.95, 0.5), fontsize=15,edgecolor='#000',title_fontsize=15)

    #控制大小
    range1=max(abs(b_x+b_r),abs(b_x-b_r),abs(s_x+s_r),abs(s_x-s_r),abs(b_y+b_r),abs(b_y-b_r),abs(s_y+s_r),abs(s_y-s_r))+10
    plt.xlim(-range1,range1)
    plt.ylim(-range1,range1)
    plt.xticks(np.linspace(-range1,range1, 11))  
    plt.yticks(np.linspace(-range1,range1, 11))
    #座標軸繪製
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['bottom'].set_position(('axes',0.5))
    axes.spines['left'].set_position(('axes',0.5))

def Save_delete(filename1,filenames):
    with imageio.get_writer(filename1, mode='I',loop=0) as writer:
        for filename in filenames:
            print(filename)
            image = imageio.imread(filename)
            writer.append_data(image)
    #刪除png檔

    for filename in filenames:
        os.remove(filename)
    print("Finished")
#不同解的xy座標
def main(x_b,y_b,r_b,x_s,y_s,r_s):#x_big,y_big...x_small,y_small...
    #a,b,c
    a=(r_b-r_s)/2
    c=((x_b-x_s)**2+(y_b-y_s)**2)**(1/2)/2
    b=(c**2-a**2)**(1/2)
    # 生成雙曲線的角度值
    theta = np.linspace(-1*np.pi, 1*np.pi, 50)
    #找出中心
    if (x_b-x_s)!=0 and (y_b-y_s)==0:
        rlud="rightleft"
        if x_b>x_s:#大圓在右
            center_x=(x_b+x_s)/2
            outer="left"
        elif x_b<x_s:#大圓在左
            center_x=(x_b+x_s)/2
            outer="right"
        else:
            print("error")
            exit(0)
        center_y=y_b
            # 計算雙曲線上的點的坐標
        x_right = center_x + a * np.cosh(theta)
        y_right = center_y +  b* np.sinh(theta)
        x_left = center_x - a * np.cosh(theta)
        y_left = center_y - b * np.sinh(theta)
        
        if outer=="left":#外切圓在左
            filenames = []
            for i in range(0,len(x_left)):#外切
                print(len(x_left)-i)#確認剩餘迴圈
                r_change=((x_left[i]-x_s)**2+(y_left[i]-y_s)**2)**(1/2)-r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_left[i],y_left[i],r_change,x_left,y_left,x_right,y_right,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_outer_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_outer_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}hyperbolic_outer.gif',filenames)
            filenames = []
            for i in range(0,len(x_right)):#內切
                print(len(x_right)-i)#確認剩餘迴圈
                r_change=((x_right[i]-x_s)**2+(y_right[i]-y_s)**2)**(1/2)+r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_right[i],y_right[i],r_change,x_left,y_left,x_right,y_right,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_inner_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_inner_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}hyperbolic_inner.gif',filenames)
        if outer=="right":#外切圓在右
            filenames = []
            for i in range(0,len(x_right)):#外切
                print(len(x_right)-i)#確認剩餘迴圈
                r_change=((x_right[i]-x_s)**2+(y_right[i]-y_s)**2)**(1/2)-r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_right[i],y_right[i],r_change,x_left,y_left,x_right,y_right,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_outer_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_outer_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}hyperbolic_outer.gif',filenames)
            filenames = []
            for i in range(0,len(x_left)):#內切
                print(len(x_left)-i)#確認剩餘迴圈
                r_change=((x_left[i]-x_s)**2+(y_left[i]-y_s)**2)**(1/2)+r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_left[i],y_left[i],r_change,x_left,y_left,x_right,y_right,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_inner_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_inner_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}hyperbolic_inner.gif',filenames)
    elif(y_b-y_s)!=0 and (x_b-x_s)==0:
        rlud="updown"
        if y_b>y_s:#大圓在上
            center_y=(y_b+y_s)/2
            outer="down"
        elif y_b<y_s:#大圓在下
            center_y=(y_b+y_s)/2
            outer="up"
        else:
            print("error")
            exit(0)
        center_x=x_b
            # 計算雙曲線上的點的坐標
        x_up = center_x + b* np.sinh(theta)
        y_up = center_y + a * np.cosh  (theta)
        x_down = center_x - b * np.sinh(theta)
        y_down = center_y - a * np.cosh(theta)
        
        if outer=="down":#外切圓在下
            filenames = []
            for i in range(0,len(y_down)):#外切
                print(len(y_down)-i)#確認剩餘迴圈
                r_change=((x_down[i]-x_s)**2+(y_down[i]-y_s)**2)**(1/2)-r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_down[i],y_down[i],r_change,x_up,y_up,x_down,y_down,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_outer_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_outer_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}/hyperbolic_outer.gif',filenames)
            filenames = []
            for i in range(0,len(y_up)):#內切
                print(len(x_up)-i)#確認剩餘迴圈
                r_change=((x_up[i]-x_s)**2+(y_up[i]-y_s)**2)**(1/2)+r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_up[i],y_up[i],r_change,x_up,y_up,x_down,y_down,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_inner_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_inner_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}/hyperbolic_inner.gif',filenames)
        if outer=="up":#外切圓在上
            filenames = []
            for i in range(0,len(y_up)):#外切
                print(len(y_up)-i)#確認剩餘迴圈
                r_change=((x_up[i]-x_s)**2+(y_up[i]-y_s)**2)**(1/2)-r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_up[i],y_up[i],r_change,x_up,y_up,x_down,y_down,rlud,a,b,c)#平行移動的圓
                plt.savefig(f'{root}hyperbolic_outer_'+str(i)+".png")
                filenames.append(f'{root}hyperbolic_outer_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}/hyperbolic_outer.gif',filenames)
            filenames = []
            for i in range(0,len(y_down)):#內切
                print(len(x_down)-i)#確認剩餘迴圈
                r_change=((x_down[i]-x_s)**2+(y_down[i]-y_s)**2)**(1/2)+r_s
                draw(x_b,y_b,r_b,x_s,y_s,r_s,x_down[i],y_down[i],r_change,x_up,y_up,x_down,y_down,rlud,a,b,c)#平行移動的圓
                plt.savefig('hyperbolic_inner_'+str(i)+".png")
                filenames.append('hyperbolic_inner_'+str(i)+".png")#儲存檔名方便利用
            Save_delete(f'{root}/hyperbolic_inner.gif',filenames)
    else:
        print("Error")
        exit(0)

if __name__=="__main__":
    start=datetime.datetime.now()
    main(0,-1,7,0,9,1)
    end=datetime.datetime.now()
    print('total run time:',end-start)
```
# *HTML網站骨架*
## 1.index.html主頁面
#### 包含<br>1.頂部網站圖案<br>2.目錄超連結<br>3.輸入參數所需的表單<br>4.基本介紹與使用說明
```html=
<!-- index1.html -->
<!DOCTYPE html>
<html>
<head> 
    <meta charset="utf-8">
    <title>二次曲線繪圖神器???</title>
    <link rel="icon" type="image/png" href="/static/image/icon.png"> 
    <meta name="keywords" content="高中數學，拋物線，橢圓，雙曲線，畫圖">
    <meta name="description" content="這是一個完全免費的客製化繪圖工具">
    <link href="/static/css/style.css" rel="stylesheet" media="All" type="text/css">
    <script src="/static/JS/index1.js"></script>
</head>

<body>
<header>
    <h1>EZdrawing</h1>
</header>
<nav>
    <h2>目錄</h2>
    <ul>
        <li><a href="#presentation">動圖成品</a></li>
        <li><a href="#elipse">橢圓</a></li>
        <li><a href="#parabola">拋物線</a></li>
        <li><a href="#hyperbola pair">雙曲線</a></li>
        <li><a href="#gif">動圖生成</a></li>
        <li><a href="#guideline">使用說明</a></li>
        <li><a href="#calculator">計算機</a></li>
        <li><a href="#introandmotivation">開發者與動機</a></li>
        <hr/>
    </ul>
</nav>

<section id="#presentation">
    <h2>動圖成品</h2>
    <div class="image-container">
        <img src="/static/gif/hyperbolic_innershow.gif">
        <img src="/static/gif/hyperbolic_outershow.gif">
    </div>
    <div class="image-container">
        <img src="/static/gif/ovalshow.gif">
        <img src="/static/gif/parabolashow.gif">
    </div>    

<section id="elipse">
    <h2>橢圓</h2>
<div class="form-container">
    <form action="/calculate_elipse">
        <h4>橢圓方程式<br>((x-h)<sup>2</sup>/a<sup>2</sup> + (y-k)<sup>2</sup>/b<sup>2</sup>=1)</h4>
        a<sup>2</sup><input type="text" name="a2">
        b<sup>2</sup><input type="text" name="b2"><br>
        h<input type="text" name="h" value="0">
        k<input type="text" name="k" value="0"><br>
        <button title="Let's go!">開始計算結果</button>
    </form>
</div>
    </section>

<section id="parabola">
    <h2>拋物線</h2>
<div class="form-container">
    <form action="/calculate_parabola1">
        <h4>上下開口拋物線<br>((x-h)<sup>2</sup>=4c(y-k))</h4>
        4c<input type="text" name="p">
        h<input type="text" name="h" value="0"><br>
        k<input type="text" name="k" value="0"><br>
        <button title="Let's go!">開始計算結果</button>
     </form> 
    <form action="/calculate_parabola2">
        <h4>左右開口拋物線<br>((y-k)<sup>2</sup>=4c(x-h))</h4>
        4c<input type="text" name="p">
        h<input type="text" name="h" value="0"><br>
        k<input type="text" name="k" value="0"><br>
        <button title="Let's go!">開始計算結果</button>
    </form>
</div>   
</section>
  <hr/>
</section>
  <hr/>
</section>
<section id="hyperbola pair">
    <h2>雙曲線</h2>
<div class="form-container">
    <form action="/calculate_hyperbola1">
        <h4>左右開口雙曲線方程式<br>((x-h)<sup>2</sup>/a<sup>2</sup> - (y-k)<sup>2</sup>/b<sup>2</sup>=1)</h4>
        a<sup>2</sup>(x下係數)<input type="text" name="a2"><br>
        b<sup>2</sup>(y下係數)<input type="text" name="b2"><br>
        h<input type="text" name="h" value="0"><br>
        k<input type="text" name="k" value="0"><br>
        <button title="Let's go!">開始計算結果</button>
     </form>
    <form action="/calculate_hyperbola2">
        <h4>上下開口雙曲線方程式<br>((y-k)<sup>2</sup>/a<sup>2</sup>-(x-h)<sup>2</sup>/b<sup>2</sup>=1)</h4>
        a<sup>2</sup>(y下係數)<input type="text" name="a2"><br>
        b<sup>2</sup>(x下係數)<input type="text" name="b2"><br>
        h<input type="text" name="h" value="0"><br>
        k<input type="text" name="k" value="0"><br>
        <button title="Let's go!">開始計算結果</button>
    </form>
</div>
    </section>

<section id="gif">
    <h2>動圖生成</h2>
    <h3>拋物線</h3><hr> 
    <div class="form-container">
    <form action="/paragif" onsubmit="startProgress()">
        <h4>與一直線(x or y=m)相切以及<br>和一圓內切之圓心軌跡方程式</h4>
        x or y<input type=""text" name="x_or_y" value="y"><br>
        m<input type="text" name="m" value="5"><br>
        C2:X座標<input type="text" name="c_0_x" value="2"><br>
        C2:y座標<input type="text" name="c_0_y" value="0"><br>
        C2:半徑<input type="text" name="c_0_r" value="1"><br>
        <button title="Let's go!">開始計算結果</button>
    </form>
    <div id="progressBar">
        <div id="progress" style="width: 0%;">0%</div>
    </div>
    </div>
    <hr>
    <h3>橢圓</h3><hr>
    <div class="form-container">
        <form action="/ellipsegif">
            <h4>與兩圓相切之圓心軌跡方程式<br>(大圓C1包小圓C2)<br></h4>
            C1:X座標<input type="text" name="x_b" value="-1"><br>
            C1:y座標<input type="text" name="y_b" value="0"><br>
            C1:半徑<input type="text" name="r_b" value="4"><br>
            C2:X座標<input type="text" name="x_s" value="1"><br>
            C2:y座標<input type="text" name="y_s" value="0"><br>
            C2:半徑<input type="text" name="r_s" value="1"><br>
            <button title="Let's go!">開始計算結果</button>
        </form>
    </div>
    <hr>
    <h3>雙曲線</h3><hr>
    <div class="form-container">
        <form action="/hypergif" onsubmit="startProgress()">
            <h4>與兩圓均內切或外切<br>之圓新軌跡方程式<br></h4>
            C1:X座標<input type="text" name="x_b" value="0"><br>
            C1:y座標<input type="text" name="y_b" value="-1"><br>
            C1:半徑<input type="text" name="r_b" value="7"><br>
            C2:X座標<input type="text" name="x_s" value="0"><br>
            C2:y座標<input type="text" name="y_s" value="9"><br>
            C2:半徑<input type="text" name="r_s" value="1"><br>
            <button title="Let's go!">開始計算結果</button>
        </form>
    </div>
    <hr>
    <div id="progressBar">
        <div id="progress" style="width: 0%;">0%</div>
    </div>
</section>

<section id="calculator">
    <h2>計算機</h2>
    <a href="/calculator"><h4>簡易計算機</h4></a>
</section>

<section id="guideline">
    <h2>使用說明</6></h2>
    1.為避免表單內請輸入整數<br>
    2.動圖生成圓心必須在軸上<br>
    3.動圖表單預設數字為一示例<br>
    4.進度條僅供參考<br>
    5.動圖題目中圓的參數請正確輸入，以免錯誤<br>
    <hr>
</section>

<section id="introandmotivation">
    <h2>開發者與動機</h2>
    <p>本網站由松山高中318班賴志全、朱禹澄所研究開發</p><hr>
    <p>目前數學進度為需要大量熟悉方程式圖形的二次曲線單元，為提升同儕們的學習品質，特別規劃此專案，
        期待能幫助每位同學們對於拋物線、橢圓、雙曲線的圖形理解。</p>
</section>
</body>
<strong>Copyright All Rights Reserved.</strong>
</html>
```
## 2.result.html成品頁面
#### 此為送出表單後成果展示的頁面，使用了將照片連結參數化，使得HTML成為一個模板，而不需重複書寫以獲取不同來源的照片
```html=
<!--result.html-->
<html>
<head>
  <title>繪圖成果</title>
  <link rel="icon" type="image/png" href="/static/image/icon.png"> 
  <link href="/static/css/style.css" rel="stylesheet" media="All" type="text/css">
</head>
<body>
  <h1>Result Plot</h1><br>
  <h3>{{title_name}}</h3>
    <img src={{file_name}} alt="{{title_name}}"><br>
  <a href="/">回首頁</a><br>
<a href="/calculator">計算機</a>
</body>
</html>
```
# *CSS網站美編設計*
#### 此為進度中最後的步驟，處理考慮手機使用者的使用體驗，主要優化了<br>1.表單的排列<br>2.字體的大小<br>3.照片的寬度調整
```css=
@charset "utf-8";


body{
    background-color:rgb(216, 214, 209);
    background-image: url(/static/image/star.png);
    background-repeat: repeat-x;
    background-size: 300px;
    font-size:16px;
}
.bold-center {
    font-weight: bold;
    text-align: center; 
}
.center {
    text-align: center;
}

h1 {
    font-size: 85px;
    text-align:center;
    background-image:url(/static/gif/math.gif);
    background-repeat:no-repeat;
    background-position:center ;
    color:transparent;
    background-clip:text ;
    filter:drop-shadow(10px 5px 30px  rgb(197, 182, 182))
}
h2 {
    font-size: 50px;
    padding: 10px;
    margin-bottom: 30px;
    border: 2px dotted #09af33;
    border-left: 10px solid #12de75;
    color: #236244;
    background-color: rgba(191, 175, 175, 0.5);
}
h4{
    text-align:center;
    font-size:25px
}
button{ 
    background-color: #10c065;
    border-radius:40px ;
    width:130px
}
button:active{
    background-color: #0a7b46;
}
button:hover{
    background-color: #0f0;
}
ul {
    columns: 4; /* 將列表分為五列 */
    column-gap: 20px; /* 列間距 */
}
li {
    display: inline-block; /* 將列表項目設置為內聯塊 */
    width: 100%; /* 使列表項目填滿列寬 */
    text-align: center;
    font-size: 30px;
}
a {
    color: #0a7b46; /* 將超連結的字體顏色設置為藍色 */
    text-decoration: none; /* 移除超連結的底線 */
}

a:hover {
    color: rgb(101, 226, 166); /* 將超連結的字體顏色設置為紅色，當滑鼠懸停在超連結上時 */
}
.form-container {
    display:flex;
    justify-content: center; /* 將內容水平置中 */
    align-items: center; /* 將內容垂直置中 */
    flex-wrap: wrap; /* 如果表單太寬，則換行顯示 */
}
.form-container form {
    margin: 10px auto; /* 给表单之间一些间距，并水平居中 */
    text-align: center; /* 文本居中 */
    width: 450px; /* 设置表单宽度 */
    padding: 20px; /* 增加内边距 */
    border-radius: 10px; /* 添加边框圆角 */
    background-color: #f0f0f0; /* 添加背景色 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
    margin-right: 80px;
    margin-left: 80px;
}
.form-container form {
    margin: 10px; /* 給表單之間一些間距*/
    text-align: center;
    margin-right: 80px;
    margin-left: 80px;
}
.form-container h4 {
    margin-bottom: 10px; /*調整標題下方間距*/
}
.form-container input,
.form-container button {
    margin-bottom: 5px; /* 調整輸入框和按鈕下方間距 */
    width: 130px; /* 調整輸入框和按鈕的寬度 */
}
#progressBar {
    width: 100%;
    background-color: #f1f1f1;
}
#progressBar>div {
    height: 30px;
    text-align: center;
    line-height: 30px;
    color: white;
    background: linear-gradient(90deg, #0f0, #0ff);
    animation:ease-in-out
}
.image-container {
    display: flex;
    justify-content: space-between; /* 图片之间的间距相等 */
    margin-bottom: 20px; /* 设置图片之间的垂直间距 */
}
.image-container img {
    width: 430px; /* 设置宽度为 190px */
    height: auto; /* 高度自动等比例缩放 */
    border-radius: 10px;
}
@keyframes progress-animation {
    from {
        width: 0%;
    }
    to {
        width: 100%;
    }
}
@media (max-width:500px){
    /* 手機版 */
    h1{
        font-size: 60px;
    }
    body{
        background-color:rgb(216, 214, 209);
        background-image: url(/static/image/star.png);
        background-repeat: repeat-x;
        background-size: 200px;
    }
    img[src=""] {
        display: none;
        /* display: none; 如果没有 src 属性，则隐藏图片 */
    }
    
    img[src] {
        width: 360px;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    .form-container {
        display: flex;
        justify-content: flex-start; /* 將內容靠左對齊 */
        align-items: center; /* 將內容垂直置中 */
        flex-wrap: wrap; /* 如果表單太寬，則換行顯示 */
    }
    
    .form-container form {
        margin: 10px; /* 給表單之間一些間距*/
        text-align: center;
        width:360px;
    }
    
    .form-container h4 {
        margin-bottom: 5px; /* 調整標題下方間距*/
    }
    
    .form-container input[type="text"],
    .form-container button {
        margin-bottom: 5px; /* 調整輸入框和按鈕下方間距 */
        width: 80px; /* 調整輸入框的寬度 */
    } 
    
    .form-container button {
        width: auto; /* 保持按鈕寬度自動調整 */
    }
}
```
# *Side Project:進度條*
## 1.進度條HTML
```html=
<form action="/paragif" onsubmit="startProgress()">
<button>submit!</button>
</form>
<div id="progressBar">
    <div id="progress" style="width: 0%;">0%</div>
</div>
```
## 2.進度條CSS
```css=
#progressBar {
    width: 100%;
    background-color: #f1f1f1;
}
#progressBar>div {
    height: 30px;
    text-align: center;
    line-height: 30px;
    color: white;
    background: linear-gradient(90deg, #0f0, #0ff);
    animation:ease-in-out
}
```
## 3.進度條JavaScript 
```javascript=
function updateProgress(progress) {
    var progressBar = document.getElementById('progress');
    progressBar.style.width = progress + '%';
    progressBar.innerHTML = progress + '%';
}

function simulateProgress() {
    var progress = 0;
    var interval = setInterval(function() {
        progress += 0.083;
        updateProgress( Math.round(progress * 100) / 100);
        if (progress >= 99.99) {
            clearInterval(interval);
        }
    }, 50); // 每0.05秒更新一次進度
}

function startProgress() {
    simulateProgress(); // 開始模擬進度
}
```
# *Side Project:計算機製作*
## 1.計算機路由
```python=
@app.route('/calculator')
def calculator():
    return render_template('index2.html')
```
## 計算機骨架HTML
```html=
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="/static/css/calculator.css">
</head>
<body>
    <div id="calculator">
        <input id="display" readonly>
        <div id="keys">
            <button onclick="clearDisplay()" class="operator-btn">c</button>
            <button onclick="appendToDisplay('7')">7</button>
            <button onclick="appendToDisplay('8')">8</button>
            <button onclick="appendToDisplay('9')">9</button>
            <button onclick="appendToDisplay('+')" class="operator-btn">+</button>
            <button onclick="appendToDisplay('4')">4</button>
            <button onclick="appendToDisplay('5')">5</button>
            <button onclick="appendToDisplay('6')">6</button>
            <button onclick="appendToDisplay('-')" class="operator-btn">-</button>
            <button onclick="appendToDisplay('1')">1</button>
            <button onclick="appendToDisplay('2')">2</button>
            <button onclick="appendToDisplay('3')">3</button>
            <button onclick="appendToDisplay('*')" class="operator-btn">*</button>
            <button onclick="appendToDisplay('0')">0</button>
            <button onclick="appendToDisplay('.')">.</button>
            <button onclick="calculate()">=</button>
            <button onclick="appendToDisplay('/')" class="operator-btn">/</button>
            <button onclick="appendToDisplay('(')" class="operator-btn">(</button>
            <button onclick="appendToDisplay(')')" class="operator-btn">)</button>
            <button onclick="appendToDisplay('^')" class="operator-btn">^</button>
        </div>
    </div>
    <script src="/static/JS/index2.js"></script>
<section class="homelink">
    <a href="/">回首頁</a><br>
</section>
</body>
</html>
```
## 2.計算機美編CSS
```css=
/*calculator.css*/
body{
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: hsl(0, 0%, 95%);
}
#calculator{
    font-family: Arial, sans-serif;
    background-color: hsl(0, 0%, 15%);
    border-radius: 15px;
    max-width: 500px;
    overflow: hidden;
}
#display{
    width: 100%;
    padding: 20px;
    font-size: 5rem;
    text-align: left;
    border: none;
    background-color: hsl(0, 0%, 20%);
    color: white;
}
#keys{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    padding: 25px;
}
button{
    width: 100px;
    height: 100px;
    border-radius: 50px;
    border: none;
    background-color: hsl(0, 0%, 30%);
    color: white;
    font-size: 3rem;
    font-weight: bold;
    cursor: pointer;
}
button:hover{
    background-color: hsl(0, 0%, 40%);
}
button:active{
    background-color: hsl(0, 0%, 50%);
}
.operator-btn{
    background-color: #236244;
}
.operator-btn:hover{
    background-color: #0f0;
}
.operator-btn:active{
    background-color: #09af33;
}
.homelink {
    position: fixed; 
    bottom: 20px; 
    left: 50%; 
    transform: translateX(-50%); 
    text-align: center; 
    width: 100%; 
}
a {
    color: #0a7b46; 
    text-decoration: none; 
}
a:hover {
    color: rgb(101, 226, 166); /
}
@media (max-width:500px){
    button{
        width: 72px;
        height: 72px;
        border-radius: 50px;
        font-size: 2rem
    }
    #calculator{
        font-family: Arial, sans-serif;
        background-color: hsl(0, 0%, 15%);
        border-radius: 15px;
        max-width: 360px;
        overflow: hidden;
    }
}
```
## 3.計算機功能JavaScript
```javascript=
const display = document.getElementById("display");

function appendToDisplay(input) {
    // 添加 ^ 符号表示指数的功能
    if (input === '^') {
        display.value += '^';
    } else if (input === '(' || input === ')') {
        display.value += input;
    } else {
        display.value += input;
    }
}

function clearDisplay() {
    display.value = "";
}

function calculate() {
    try {
        let expression = display.value;

        // 處理括號內的表達式
        while (expression.includes('(')) {
            const startIndex = expression.lastIndexOf('(');
            const endIndex = expression.indexOf(')', startIndex);
            const subExpression = expression.slice(startIndex + 1, endIndex);
            const subResult = evaluateExpression(subExpression);
            expression = expression.slice(0, startIndex) + subResult + expression.slice(endIndex + 1);
        }

        // 處理指數運算
        const powerRegex = /(\d+(\.\d+)?)\^(\d+(\.\d+)?)/;
        while (expression.match(powerRegex)) {
            expression = expression.replace(powerRegex, (match, base, _, exponent) => {
                return Math.pow(parseFloat(base), parseFloat(exponent));
            });
        }

        // 處理乘除運算
        expression = expression.replace(/(\d+(\.\d+)?)\*(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) * parseFloat(num2);
        });
        expression = expression.replace(/(\d+(\.\d+)?)\/(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) / parseFloat(num2);
        });

        // 處理加減運算
        expression = expression.replace(/(\d+(\.\d+)?)\+(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) + parseFloat(num2);
        });
        expression = expression.replace(/(\d+(\.\d+)?)\-(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) - parseFloat(num2);
        });

        display.value = expression;
    } catch (error) {
        display.value = "Error";
    }
}

function evaluateExpression(expression) {
    // 遞歸地計算括號內的表達式
    let result = expression;
    let newExpression = expression;
    while (newExpression.includes('^')) {
        const match = newExpression.match(/(\d+(\.\d+)?)\^(\d+(\.\d+)?)/);
        if (match) {
            const base = parseFloat(match[1]);
            const exponent = parseFloat(match[3]);
            const subResult = Math.pow(base, exponent);
            newExpression = newExpression.replace(match[0], subResult);
        }
    }
    // 遞歸地計算括號內的表達式
    while (result.includes('(')) {
        const startIndex = result.lastIndexOf('(');
        const endIndex = result.indexOf(')', startIndex);
        const subExpression = result.slice(startIndex + 1, endIndex);
        const subResult = evaluateExpression(subExpression);
        result = result.slice(0, startIndex) + subResult + result.slice(endIndex + 1);
    }
    // 計算乘除運算
    result = result.replace(/(\d+(\.\d+)?)\*(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) * parseFloat(num2);
    });
    result = result.replace(/(\d+(\.\d+)?)\/(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) / parseFloat(num2);
    });
    // 計算加減運算
    result = result.replace(/(\d+(\.\d+)?)\+(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) + parseFloat(num2);
    });
    result = result.replace(/(\d+(\.\d+)?)\-(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) - parseFloat(num2);
    });
    return result;
}
```
# *部署*
## Github:存放程式碼的位置
![image](https://hackmd.io/_uploads/ryTvguvJR.png)
## Replit:編輯程式碼並與Github連結
  
## Render.com:提供網頁服務與伺服器
### requirements.txt:讓Render.com知道該下載甚麼版本的甚麼模組
```python=
Flask==3.0.2
matplotlib==3.4.3
imageio==2.34.0
sympy==1.12
numpy==1.26.4
gunicorn==21.2.0
```

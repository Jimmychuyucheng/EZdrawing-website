from PIL import Image
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
from sympy import *
import datetime
root='static/gif/'
#line 32 主程式：輸入[大圓x,大圓y,大圓r,小圓x,小圓y,小圓r]
"""

def drawcircle(x,y,r,color):
    theta = np.arange(0, 2*np.pi, 0.01)
    x_result= x + r * np.cos(theta)
    y_result= y + r * np.sin(theta)
    axes.plot(x_1, y_1,c=color)

"""
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
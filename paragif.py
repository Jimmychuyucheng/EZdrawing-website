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
        y_2= np.arange(-range1,range1, 0.8)
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
        x_2= np.arange(-range1,range1, 0.8)
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
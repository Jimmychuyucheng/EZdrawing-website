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
    theta = np.linspace(-1*np.pi, 1*np.pi, 30)
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
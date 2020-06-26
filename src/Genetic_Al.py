import random
from openpyxl import load_workbook
import random
import numpy as np
import matplotlib.pyplot as plt


'''
Excel 파일 불러오기
'''
load_wb = load_workbook("키와발데이터v3.xlsx")
load_ws = load_wb['Sheet1']
height_data = []
foot_data = []
data = []
for row in load_ws.rows:
    row_val = []
    for cell in row:
        row_val.append(cell.value)

    data.append(row_val)


x = [i[0] for i in data]
y = [i[1]for i in data]
x_data = np.array(x)
y_data = np.array(y)


'''
구하려는 직선 함수 
'''
def fx(a,x):
    return a*x

'''
MSE 수식
'''
def mse(y,y_hat):
    return ((y_hat-y)**2).mean()

'''
초기 후보값 생성
'''
def init():
    global arr
    arr = [0,0,0,0]
    for i in range(0,4):
        arr[i] = random.uniform(0,8)
        print(arr[i])
    print()
    return arr;

'''
선택(selection)
'''
def sel(x):
    sum = 0
    f= [0,0,0,0]
    for i in range(0,4):
        f[i] = mse(y_data[i],fx(arr[i],x_data[i]))
        sum += f[i]

    ratio = [0,0,0,0]
    for i in range(0,4):
        if i==0: ratio[i] = ((sum-f[i])/sum)/3
        else: ratio[i] = ratio[i-1] + ((sum-f[i])/sum)/3


    sx = [0,0,0,0]
    for i in range(0,4):
        p = random.random()
        if (p<ratio[0]): sx[i] = x[0]
        elif(p<ratio[1]): sx[i] = x[1]
        elif (p < ratio[2]): sx[i] = x[2]
        else: sx[i] = x[3]


    return sx

'''
교차(crossover) -> 산술교차 사용
'''
def crossover(x):
    arr = [0,0,0,0]
    rate = 0.5
    r1 = random.random()
    if r1 < rate :
        if x[0]!=x[1]: arr[0] = (x[0] + x[1])/2
        elif x[0]!=x[2]: arr[0] = (x[0] + x[2])/2
        elif x[0] != x[3]: arr[0] = (x[0] + x[3]) / 2
        if x[1]!=x[2]: arr[1] = (x[1] + x[2])/2
        elif x[1]!=x[3]: arr[1] = (x[1] + x[3])/2
        elif x[1] != x[0]: arr[1] = (x[1] + x[0]) / 2
        if x[2]!=x[1]: arr[2] = (x[2] + x[1])/2
        elif x[2]!=x[0]: arr[2] = (x[2] + x[0])/2
        elif x[2] != x[3]: arr[2] = (x[2] + x[3]) / 2
        if x[3]!=x[1]: arr[3] = (x[3] + x[1])/2
        elif x[3]!=x[2]: arr[3] = (x[3] + x[2])/2
        elif x[3] != x[0]: arr[3] = (x[3] + x[0]) / 2

    else :
        if x[2]!=x[1]: arr[0] = (x[2] + x[1])/2
        elif x[2]!=x[0]: arr[0] = (x[0] + x[2])/2
        elif x[2] != x[3]: arr[0] = (x[2] + x[3]) / 2
        if x[0]!=x[2]: arr[1] = (x[1] + x[2])/2
        elif x[0]!=x[3]: arr[1] = (x[1] + x[3])/2
        elif x[0] != x[0]: arr[1] = (x[1] + x[0]) / 2
        if x[3]!=x[1]: arr[2] = (x[2] + x[1])/2
        elif x[3]!=x[0]: arr[2] = (x[2] + x[0])/2
        elif x[3] != x[3]: arr[2] = (x[2] + x[3]) / 2
        if x[1]!=x[1]: arr[3] = (x[3] + x[1])/2
        elif x[1]!=x[2]: arr[3] = (x[3] + x[2])/2
        elif x[1] != x[0]: arr[3] = (x[3] + x[0]) / 2

    return arr
'''
변이(mutation) 
'''
def invert(x):
    per = 0.01
    a = 0.0
    for i in range(0,4):
        r_i = random.random()
        if(r_i<per):

            r_val = random.uniform(-5,5)
            a= x + r_val

        else:
            a= x
    return a
def mutation(x):
    arr = [0,0,0,0]
    for i in range(0,4):
        arr[i] = invert(x[i])
    return arr


x = init()
f=[]
min1 = 1000000
min2 = 100
for i in range(0,1000):
    sx = sel(x)
    print(sx)
    cx = []
    cx = crossover(sx)
    mx = mutation(cx)
    for j in range(0, 4):
        f.append(mse(y_data[j], fx(mx[j], x_data[j])))
        if i == 0:
            if min1 > f[j]:
                min1 = f[j]
                min2 = mx[j]
        else:
            if min1 > f[j + 4 * i]:
                min1 = f[j + 4 * i]
                min2 = mx[j]

'''
그래프 생성
'''
y=min2*x_data
plt.scatter(x_data,y_data,marker='+',color = 'r')
plt.plot([min(x_data), max(x_data)], [min(y), max(y)],color = 'Black')
plt.xlabel('Height(cm)')
plt.ylabel('Foot size(mm)')
plt.legend(['estimate','measured'])
plt.show()

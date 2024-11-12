import numpy as np
import matplotlib.pyplot as plt
import scipy


def rSquare(calculatedData, initialData):
    """ Compute the coefficient of determination of random data.
    This metric gives the level of confidence about the model used to model data"""
    SSt = ((np.array(initialData) - np.array(calculatedData)) ** 2).sum()
    mMean = (np.array(initialData)).sum() / float(len(initialData))
    dErr = ((mMean - initialData) ** 2).sum()

    return 1 - (SSt / dErr)


#variables
timeFCOIV = np.array([1,5,10,15,20,30,40,50,60,70,80,90,100], int)
temperature = np.array([1200,1223,1242,1255,1267,1280,1289,1294,1297,1298,1300,1300,1300], int)

#grafics
x = np.linspace(timeFCOIV.min(),timeFCOIV.max(),100)

# Нахождение функции полинома
coeffient = np.polyfit(timeFCOIV,temperature,1)
funcPol = np.poly1d(coeffient)
y_1 = funcPol(timeFCOIV)
R = rSquare(temperature, y_1)
print("Коэффициент детерминации линейной аппроксимации: ", R)


fig, ax = plt.subplots()
ax.plot(timeFCOIV,temperature,'r+', label='Исходные данные')
ax.plot(x,funcPol(x), color='green', label='Апроксимация')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_title('Линейная аппроксимация')
ax.legend()
#plt.show()

# Нахождение функции полинома
coeffient = np.polyfit(timeFCOIV,temperature,3)
funcPol = np.poly1d(coeffient)

print("Уравнение полинома третьей степени: \n",funcPol)
print("Коэфициенты уравнения: ", coeffient)

#grafics
x = np.linspace(timeFCOIV.min(),timeFCOIV.max(),100)

fig, ax = plt.subplots()
ax.plot(timeFCOIV,temperature,'r+', label='Исходные данные')
ax.plot(x,funcPol(x), color='green', label='Апроксимация')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_title('Degree = 3')
ax.legend()
plt.show()


y_1 = funcPol(timeFCOIV)
R = rSquare(temperature, y_1)
print("Коэффициент детерминации для полинома третьей степени: ", R)


#Логарифмическая апроксимация
def funcLog(x, a, b):
    return a+b*np.log(x, where=x>0)

popt, pcov = scipy.optimize.curve_fit(funcLog,  timeFCOIV,  temperature)

print(pcov)

fig, ax = plt.subplots()
ax.plot(timeFCOIV,temperature,'r+', label='Исходные данные')
ax.plot(x,funcLog(x, *popt), color='green', label='Апроксимация')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_title('Degree = log')
ax.legend()
#plt.show()

R = rSquare(temperature, funcLog(timeFCOIV, *popt))
print(R)






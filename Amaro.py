import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Para isto pode utilizar a função read_excel do módulo Pandas.
data = pd.read_excel('CarDataset.xlsx')

#Construir uma matriz com os valores da tabela.
arrayValores = data.values
print(arrayValores)

#Construir uma lista com os nomes das variáveis contidas na tabela.
varNames=data.columns.values.tolist()
print(varNames)

#Grafico 
plt.figure(1)
plt.subplot(3,2,1)
plt.plot(arrayValores[:,0], arrayValores[:,6], "*m") 
plt.xlabel('Acceleration')
plt.ylabel('MPG')
plt.title('MPG vs Acceleration')
plt.subplots_adjust(hspace=0.5)

plt.figure(1)
plt.subplot(3,2,2)
plt.plot(arrayValores[:,1], arrayValores[:,6], "*m")
plt.xlabel('Cylinders')
plt.ylabel('MPG')
plt.title('MPG vs Cylinders')
plt.subplots_adjust(hspace=0.5)

plt.figure(1)
plt.subplot(3,2,3)
plt.plot(arrayValores[:,2], arrayValores[:,6], "*m")
plt.xlabel('Displacement')
plt.ylabel('MPG')
plt.title('MPG vs Displacement')
plt.subplots_adjust(hspace=0.5)

plt.figure(1)
plt.subplot(3,2,4)
plt.plot(arrayValores[:,3], arrayValores[:,6], "*m")
plt.xlabel('Horsepower')
plt.ylabel('MPG')
plt.title('MPG vs Horsepower')
plt.subplots_adjust(hspace=0.5)

plt.figure(1)
plt.subplot(3,2,5)
plt.plot(arrayValores[:,4], arrayValores[:,6], "*m")
plt.xlabel('Model Year')
plt.ylabel('MPG')
plt.title('MPG vs Model Year')
plt.subplots_adjust(hspace=0.5)

plt.figure(1)
plt.subplot(3,2,6)
plt.plot(arrayValores[:,5], arrayValores[:,6], "*m")
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.title('MPG vs Weight')
plt.subplots_adjust(hspace=0.5)

plt.show()

#Converter os dados para o tipo uint16.
nb = arrayValores.itemsize * 8
print(nb)
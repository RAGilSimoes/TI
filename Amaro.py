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

#plt.show()

#Converter os dados para o tipo uint16.
A = np.array(arrayValores,dtype=int)
A = A.astype(np.uint16)
nb = (A.itemsize * 8)

print(nb ,"\n")

#Definir o respetivo alfabeto.
alfabeto = {} 

# Para a aceleração (Acceleration)
alfabeto['Acceleration'] = np.unique(arrayValores[:, 0])
# Para os cilindros (Cylinders)
alfabeto['Cylinders'] = np.unique(arrayValores[:, 1])
# Para o deslocamento (Displacement)
alfabeto['Displacement'] = np.unique(arrayValores[:, 2])
# Para a potência do motor (Horsepower)
alfabeto['Horsepower'] = np.unique(arrayValores[:, 3])
# Para o ano de fabrico (Model Year)
alfabeto['Model Year'] = np.unique(arrayValores[:, 4])
# Para o peso do carro (Weight)
alfabeto['Weight'] = np.unique(arrayValores[:, 5])
# Para o MPG (Miles per Gallon)
alfabeto['MPG'] = np.unique(arrayValores[:, 6])

print("Alfabeto para cada variável: \n")
for key, value in alfabeto.items():
    print(f"{key}: {value}\n")


#Implementar uma função própria que calcule o número de ocorrências para cada símbolo do alfabeto, para cada uma das variáveis.
def ocurrencias():
    a = len(arrayValores[:, 0])
    b = len(arrayValores[:, 1])
    c = len(arrayValores[:, 2])
    d = len(arrayValores[:, 3])
    e = len(arrayValores[:, 4])
    f = len(arrayValores[:, 5])
    g = len(arrayValores[:, 6])  

    print(f"Quantidade total de ocorrências em 'Acceleration':", a)
    print(f"Quantidade total de ocorrências em 'Cylinders':", b)
    print(f"Quantidade total de ocorrências em 'Displacement':", c)
    print(f"Quantidade total de ocorrências em 'Horsepower':", d)
    print(f"Quantidade total de ocorrências em 'Model Year':", e)
    print(f"Quantidade total de ocorrências em 'Weight':", f)
    print(f"Quantidade total de ocorrências em 'Miles per Gallon':", g)

ocurrencias()

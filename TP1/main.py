import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Funções---------------------------------------------------------
#função para calcular o número de ocorrências--
def calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias):
    indice = 0
    while(indice <= 6):
        match (indice):
            case (0):
                arrayOcorrenciasAcceleration = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasAcceleration[arrayInformacao[i][indice]] += 1 #vai ao número no índice [i][indice] no array das ocorrencias 
                indice += 1                                                       #e adiciona 1 para controlar o número de vezes que esse número apareceu
                
            case (1):
                arrayOcorrenciasCylinders = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasCylinders[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (2):
                arrayOcorrenciasDisplacement = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasDisplacement[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (3):
                arrayOcorrenciasHorsepower = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasHorsepower[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (4):
                arrayOcorrenciasModelYear = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasModelYear[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (5):
                arrayOcorrenciasWeight = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasWeight[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (6):
                arrayOcorrenciasMPG = np.zeros_like(arrayBaseOcorrencias)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasMPG[arrayInformacao[i][indice]] += 1
                indice += 1
    return arrayOcorrenciasAcceleration, arrayOcorrenciasCylinders, arrayOcorrenciasDisplacement, arrayOcorrenciasHorsepower, arrayOcorrenciasModelYear, arrayOcorrenciasWeight, arrayOcorrenciasMPG




#funcao para construir o gráfico dependendo da lista que recebe--
def criaGrafico(arrayOcorrenciasRecebido, arrayValoresRecebido, variavel):
    listaQuantidadeOcorrencias = arrayOcorrenciasRecebido.tolist() #passa o array da quantidade de ocorrencias para uma lista
    listaValoresOcorrencias = arrayValoresRecebido.tolist() #passa o array dos valores para uma lista
    
    indicesOcorrencias = [None] * len(arrayValoresRecebido) #cria uma lista do tamanho da quantidade dos valores diferentes de zero

    indicesUsados = 0 #variável de controlo para as novas listas
    for i in range(len(listaQuantidadeOcorrencias)):
        if(listaQuantidadeOcorrencias[i] != 0):
            indicesOcorrencias[indicesUsados] = listaQuantidadeOcorrencias[i] #passa a quantidade de ocorrências do número
            indicesUsados += 1
    
    x = range(len(listaValoresOcorrencias)) #serve para criar uma lista de números seguidos para não haver barras sem ocorrências,
    plt.figure(figsize=(12,6))              #de forma a eliminar espaços em brancos derivado a valores sem ocorrências
    plt.bar(x, indicesOcorrencias, color='red')
    plt.xlim(x[0] - 0.5, x[len(x) - 1] + 0.5)
    plt.xlabel(variavel)
    plt.ylabel("Count")
    plt.xticks(x, listaValoresOcorrencias, rotation=90) #meter as barras nas unidades e mudar as labels
    plt.tight_layout()
    plt.show()


#função para mostrar os gráficos consoante o indice--
#mudar para uma forma mais eficiente, todo o bloco comum meter noutra funcao
def apresentaGrafico(dicionarioOcorrencias, dicionarioAlfabeto):
    indice = 0
    while(indice <= 6):
        match (indice):
            case (0):
                criaGrafico(dicionarioOcorrencias['Acceleration'], dicionarioAlfabeto['Acceleration'], "Acceleration")
                indice += 1
                
            case (1):
                criaGrafico(dicionarioOcorrencias['Cylinders'], dicionarioAlfabeto['Cylinders'], "Cylinders")
                indice += 1
                
            case (2):
                criaGrafico(dicionarioOcorrencias['Displacement'], dicionarioAlfabeto['Displacement'], "Displacement")
                indice += 1
                
            case (3):
                criaGrafico(dicionarioOcorrencias['Horsepower'], dicionarioAlfabeto['Horsepower'], "Horsepower")
                indice += 1
                
            case (4):
                criaGrafico(dicionarioOcorrencias['ModelYear'], dicionarioAlfabeto['ModelYear'], "Model Year")
                indice += 1
                
            case (5):
                criaGrafico(dicionarioOcorrencias['Weight'], dicionarioAlfabeto['Weight'], "Weight")
                indice += 1
                
            case (6):
                criaGrafico(dicionarioOcorrencias['MPG'], dicionarioAlfabeto['MPG'], "MPG")
                indice += 1


#Tópico 1 --------------------------------------------------------
#carregar conjunto de dados--
data = pd.read_excel('CarDataset.xlsx')


#construir matriz com os valores da tabela--
arrayInformacao = data.values
print(arrayInformacao)


#construir lista com os nomes das variáveis--
varNames = data.columns.values.tolist()
print(varNames)


#Tópico 2 --------------------------------------------------------
#construir os gráficos das variávieis--
plt.figure(1)
plt.subplot(3,2,1)
plt.plot(arrayInformacao[:,0],arrayInformacao[:, 6], "*m")
plt.xlabel("Acceleration")
plt.ylabel("MPG")
plt.title("MPG Vs Acceleration")
plt.subplots_adjust(wspace = 0.5)
plt.subplots_adjust(hspace = 1)

plt.figure(1)
plt.subplot(3,2,2)
plt.plot(arrayInformacao[:,1],arrayInformacao[:, 6], "*m")
plt.xlabel("Cilinders")
plt.ylabel("MPG")
plt.title("MPG Vs Cilinders")
plt.subplots_adjust(wspace = 0.5)
plt.subplots_adjust(hspace = 1)

plt.figure(1)
plt.subplot(3,2,3)
plt.plot(arrayInformacao[:,2],arrayInformacao[:, 6], "*m")
plt.xlabel("Displacement")
plt.ylabel("MPG")
plt.title("MPG Vs Displacement")
plt.subplots_adjust(wspace = 0.5)
plt.subplots_adjust(hspace = 1)

plt.figure(1)
plt.subplot(3,2,4)
plt.plot(arrayInformacao[:,3],arrayInformacao[:, 6], "*m")
plt.xlabel("Horsepower")
plt.ylabel("MPG")
plt.title("MPG Vs Horsepower")
plt.subplots_adjust(wspace = 0.5)
plt.subplots_adjust(hspace = 1)

plt.figure(1)
plt.subplot(3,2,5)
plt.plot(arrayInformacao[:,4],arrayInformacao[:, 6], "*m")
plt.xlabel("Model Year")
plt.ylabel("MPG")
plt.title("MPG Vs Model Year")
plt.subplots_adjust(wspace = 0.5)
plt.subplots_adjust(hspace = 1)

plt.figure(1)
plt.subplot(3,2,6)
plt.plot(arrayInformacao[:,5],arrayInformacao[:, 6], "*m")
plt.xlabel("Weight") 
plt.ylabel("MPG")
plt.title("MPG Vs Weight")
plt.subplots_adjust(wspace = 0.5)
plt.subplots_adjust(hspace = 1)
plt.show()


#Tópico 3 --------------------------------------------------------
#converter os dados para uint16--
arrayInformacao = arrayInformacao.astype(np.uint16)

#definir respetivo alfabeto
nb = (arrayInformacao.itemsize * 8)
arrayBaseOcorrencias = np.arange(0, 2**nb)

#Encontrar os números que têm ocorrências
alfabeto = {} 
alfabeto['Acceleration'] = np.unique(arrayInformacao[:, 0])
alfabeto['Cylinders'] = np.unique(arrayInformacao[:, 1])
alfabeto['Displacement'] = np.unique(arrayInformacao[:, 2])
alfabeto['Horsepower'] = np.unique(arrayInformacao[:, 3])
alfabeto['ModelYear'] = np.unique(arrayInformacao[:, 4])
alfabeto['Weight'] = np.unique(arrayInformacao[:, 5])
alfabeto['MPG'] = np.unique(arrayInformacao[:, 6])

#Tópico 4 --------------------------------------------------------
#calcular o número de ocorrências
dicionarioOcorrencias = {}
dicionarioOcorrencias['Acceleration'], dicionarioOcorrencias['Cylinders'], dicionarioOcorrencias['Displacement'], dicionarioOcorrencias['Horsepower'], dicionarioOcorrencias['ModelYear'], dicionarioOcorrencias['Weight'], dicionarioOcorrencias['MPG'] = calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias)

#Tópico 5 --------------------------------------------------------
apresentaGrafico(dicionarioOcorrencias, alfabeto)
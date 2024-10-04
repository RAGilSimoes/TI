import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Funções---------------------------------------------------------
#função para calcular o número de ocorrências--
def calcularNumeroOcorrencias(arrayInformacao):
    indice = 0
    while(indice <= 6):
        match (indice):
            case (0):
                arrayOcorrenciasAcceleration = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasAcceleration[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (1):
                arrayOcorrenciasCylinders = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasCylinders[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (2):
                arrayOcorrenciasDisplacement = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasDisplacement[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (3):
                arrayOcorrenciasHorsepower = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasHorsepower[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (4):
                arrayOcorrenciasModelYear = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasModelYear[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (5):
                arrayOcorrenciasWeight = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasWeight[arrayInformacao[i][indice]] += 1
                indice += 1
                
            case (6):
                arrayOcorrenciasMPG = np.zeros_like(arrayBase)
                for i in range(len(arrayInformacao)):
                    arrayOcorrenciasMPG[arrayInformacao[i][indice]] += 1
                indice += 1
    return arrayOcorrenciasAcceleration, arrayOcorrenciasCylinders, arrayOcorrenciasDisplacement, arrayOcorrenciasHorsepower, arrayOcorrenciasModelYear, arrayOcorrenciasWeight, arrayOcorrenciasMPG




#funcao para construir o gráfico dependendo da lista que recebe--
def criaGrafico(listaRecebida, variavel):
    listaQuantidadeOcorrencias = listaRecebida.tolist()

    nIndicesNecessarios = 0
    for i in range(len(listaQuantidadeOcorrencias)):
        if(listaQuantidadeOcorrencias[i] != 0):
            nIndicesNecessarios += 1

    listaOcorrencias = [None] * nIndicesNecessarios
    indicesOcorrencias = [None] * nIndicesNecessarios

    indicesUsados = 0
    for i in range(len(listaQuantidadeOcorrencias)):
        if(listaQuantidadeOcorrencias[i] != 0):
            listaOcorrencias[indicesUsados] = listaQuantidadeOcorrencias[i]
            indicesOcorrencias[indicesUsados] = i
            indicesUsados += 1
    
    x = range(len(indicesOcorrencias)) #serve para criar uma lista de números seguidos para não haver barras sem ocorrências,
    plt.figure(figsize=(12,6))         #de forma a eliminar espaços em brancos derivado a valores sem ocorrências
    plt.bar(x, listaOcorrencias, color='red')
    plt.xlim(x[0] - 0.5, x[len(x) - 1] + 0.5)
    plt.xlabel(variavel)
    plt.ylabel("Count")
    plt.xticks(x, indicesOcorrencias, rotation=90) #meter as barras nas unidades e mudar as labels
    plt.tight_layout()
    plt.show()


#função para mostrar os gráficos consoante o indice--
#mudar para uma forma mais eficiente, todo o bloco comum meter noutra funcao
def apresentaGrafico(arrayOcorrenciasAcceleration, arrayOcorrenciasCylinders, arrayOcorrenciasDisplacement, arrayOcorrenciasHorsepower, arrayOcorrenciasModelYear, arrayOcorrenciasWeight, arrayOcorrenciasMPG):
    indice = 0
    while(indice <= 6):
        match (indice):
            case (0):
                criaGrafico(arrayOcorrenciasAcceleration, "Acceleration")
                indice += 1
                
            case (1):
                criaGrafico(arrayOcorrenciasCylinders, "Cylinders")
                indice += 1
                
            case (2):
                criaGrafico(arrayOcorrenciasDisplacement, "Displacement")
                indice += 1
                
            case (3):
                criaGrafico(arrayOcorrenciasHorsepower, "Horsepower")
                indice += 1
                
            case (4):
                criaGrafico(arrayOcorrenciasModelYear, "Model Year")
                indice += 1
                
            case (5):
                criaGrafico(arrayOcorrenciasWeight, "Weight")
                indice += 1
                
            case (6):
                criaGrafico(arrayOcorrenciasMPG, "MPG")
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
arrayBase = np.arange(0, 2**nb)

#Tópico 4 --------------------------------------------------------
#calcular o número de ocorrências
arrayOcorrenciasAcceleration, arrayOcorrenciasCylinders, arrayOcorrenciasDisplacement, arrayOcorrenciasHorsepower, arrayOcorrenciasModelYear, arrayOcorrenciasWeight, arrayOcorrenciasMPG = calcularNumeroOcorrencias(arrayInformacao)

#Tópico 5 --------------------------------------------------------
apresentaGrafico(arrayOcorrenciasAcceleration, arrayOcorrenciasCylinders, arrayOcorrenciasDisplacement, arrayOcorrenciasHorsepower, arrayOcorrenciasModelYear, arrayOcorrenciasWeight, arrayOcorrenciasMPG)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#8/10 - 1,75 em 3 (0,25 não está tudo em funções  0,75 calcular o numero de ocorrencias)

#Funções---------------------------------------------------------
#função para calcular o número de ocorrências--                                 
def calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames):
    indice = 0
    for i in varNames:
        arrayInformacaoUsar = arrayInformacao[:, indice] #array da informação a percorrer
        alfabetoValores[i] = np.unique(arrayInformacao[:, indice]) #array dos números diferentes de zero sem repetição
        dicionarioOcorrencias[i] = np.zeros_like(arrayBaseOcorrencias) #array do tamanho de 2**nb começado a zero
        for l in range(len(arrayInformacaoUsar)):
            dicionarioOcorrencias[i][arrayInformacaoUsar[l]] += 1 #vai ao indice correspondente e adiciona 1
            
        indice += 1 #para controlar as colunas do array da informação


#funcao para construir o gráfico dependendo da lista que recebe--
def criaGrafico(arrayOcorrenciasRecebido, arrayValoresRecebido, variavel): #nao queremos listas!!!!!!!!!!!!!!!!
    listaQuantidadeOcorrencias = arrayOcorrenciasRecebido.tolist() 
    listaValoresOcorrencias = arrayValoresRecebido.tolist() 
    
    indicesOcorrencias = [None] * len(arrayValoresRecebido) #cria uma lista do tamanho da quantidade dos valores diferentes de zero

    indicesUsados = 0 #variável de controlo para as novas listas
    for i in range(len(listaQuantidadeOcorrencias)):
        if(listaQuantidadeOcorrencias[i] != 0):
            indicesOcorrencias[indicesUsados] = listaQuantidadeOcorrencias[i] #passa a quantidade de ocorrências do número
            indicesUsados += 1
            
    #passar a variável do eixo dos xx do gráfico para um array de astype(str) !!!!!
    
    x = range(len(listaValoresOcorrencias)) #serve para criar uma lista de números seguidos para não haver barras sem ocorrências,
    plt.figure(figsize=(12,6))              #de forma a eliminar espaços em brancos derivado a valores sem ocorrências
    plt.bar(x, indicesOcorrencias, color='red')
    plt.xlim(x[0] - 0.5, x[len(x) - 1] + 0.5)
    plt.xlabel(variavel)
    plt.ylabel("Count")
    plt.xticks(x, listaValoresOcorrencias, rotation=90) #meter as barras nas unidades e mudar as labels
    plt.tight_layout() #n02 = n0[n0>0]
    plt.show()         #A2 = A0[n0>0] converter para string


#função para mostrar os gráficos consoante o indice--
def apresentaGrafico(dicionarioOcorrencias, dicionarioAlfabeto, varNames):
    for i in varNames:
        criaGrafico(dicionarioOcorrencias[i], dicionarioAlfabeto[i], i)


def main():
    #Tópico 1 -------------------------------------------------------- meter tudo em funções meter a coisa do name e iftype name
    #carregar conjunto de dados--
    data = pd.read_excel('CarDataset.xlsx')

    #construir matriz com os valores da tabela--
    arrayInformacao = data.values
    print(arrayInformacao)

    #construir lista com os nomes das variáveis--
    varNames = data.columns.values.tolist()
    print(varNames)
    
    
    #Tópico 2 -------------------------------------------------------- meter o que está repetido numa função como segundos gráficos
    #construir os gráficos das variávieis--
    plt.figure(1)
    plt.subplot(3,2,1)
    plt.plot(arrayInformacao[:,0],arrayInformacao[:, 6], "*m")
    plt.xlabel("Acceleration")
    plt.ylabel("MPG")
    plt.title("MPG Vs Acceleration")
    plt.subplots_adjust(wspace = 0.5)
    plt.subplots_adjust(hspace = 1)


    plt.subplot(3,2,2)
    plt.plot(arrayInformacao[:,1],arrayInformacao[:, 6], "*m")
    plt.xlabel("Cylinders")
    plt.ylabel("MPG")
    plt.title("MPG Vs Cylinders")
    plt.subplots_adjust(wspace = 0.5)
    plt.subplots_adjust(hspace = 1)


    plt.subplot(3,2,3)
    plt.plot(arrayInformacao[:,2],arrayInformacao[:, 6], "*m")
    plt.xlabel("Displacement")
    plt.ylabel("MPG")
    plt.title("MPG Vs Displacement")
    plt.subplots_adjust(wspace = 0.5)
    plt.subplots_adjust(hspace = 1)


    plt.subplot(3,2,4)
    plt.plot(arrayInformacao[:,3],arrayInformacao[:, 6], "*m")
    plt.xlabel("Horsepower")
    plt.ylabel("MPG")
    plt.title("MPG Vs Horsepower")
    plt.subplots_adjust(wspace = 0.5)
    plt.subplots_adjust(hspace = 1)


    plt.subplot(3,2,5)
    plt.plot(arrayInformacao[:,4],arrayInformacao[:, 6], "*m")
    plt.xlabel("Model Year")
    plt.ylabel("MPG")
    plt.title("MPG Vs Model Year")
    plt.subplots_adjust(wspace = 0.5)
    plt.subplots_adjust(hspace = 1)


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

    
    #Tópico 4 --------------------------------------------------------
    alfabetoValores = {} 
    #calcular o número de ocorrências e os valores em que existem ocorrencias
    dicionarioOcorrencias = {}
    calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames)
    
    
    #Tópico 5 --------------------------------------------------------
    apresentaGrafico(dicionarioOcorrencias, alfabetoValores, varNames)




#topico 6
#fazer intervalos e o número para o qual se vai alterar é o número com a maior moda (mais frequente) dos números do intervalo
#binning de 40 simbolos são de 0 até 39 e etc
#np.argmax indice onde ocorre o maximo
#np.where serve para alterar o valor dos numeros consoante uma condição




if __name__ == "__main__":
    main()
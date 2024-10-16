import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#8/10 - 1,75 em 3 (0,25 não está tudo em funções  0,75 calcular o numero de ocorrencias)

#Funções---------------------------------------------------------

#-----------------------------------------------------------------
#função para calcular o número de ocorrências de cada variável e para criar um array dos números com ocorrências                                 
def calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames):
    for i in range(len(varNames)):
        arrayInformacaoUsar = arrayInformacao[:, i] #array da informação a percorrer
        alfabetoValores[varNames[i]] = np.unique(arrayInformacao[:, i]) #array dos números diferentes de zero sem repetição
        dicionarioOcorrencias[varNames[i]] = np.zeros_like(arrayBaseOcorrencias) #array do tamanho de 2**nb começado a zero
        for l in range(len(arrayInformacaoUsar)):
            dicionarioOcorrencias[varNames[i]][arrayInformacaoUsar[l]] += 1 #vai ao indice correspondente e adiciona 1
#-----------------------------------------------------------------


#-----------------------------------------------------------------
#funcao para construir o gráfico dependendo da lista que recebe--
def criaGraficoVariavel(arrayOcorrenciasRecebido, arrayValoresRecebido, variavel): 
    novoArrayOcorrencias = arrayOcorrenciasRecebido[arrayOcorrenciasRecebido > 0] #n02
    arrayValoresString = arrayValoresRecebido.astype(str)
    plt.figure(figsize=(12,6))
    plt.bar(arrayValoresString, novoArrayOcorrencias, color='red')
    plt.xlabel(variavel)
    plt.xticks(rotation=90)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
    

#função para mostrar os gráficos das ocorrencias
def apresentaGraficosVariaveis(dicionarioOcorrencias, alfabetoValores, varNames):
    for i in varNames:
        criaGraficoVariavel(dicionarioOcorrencias[i], alfabetoValores[i], i)
#-----------------------------------------------------------------


#-----------------------------------------------------------------
#função para construir um gráfico de MPG em relação a uma variável      
def construirGraficoVariavelVsMPG(variavel,local, arrayInformacao):
    plt.subplot(3,2,local)
    plt.plot(arrayInformacao[:,local-1],arrayInformacao[:, 6], "*m")
    plt.xlabel(variavel)
    plt.ylabel("MPG")
    plt.title("MPG Vs " + variavel)
    plt.subplots_adjust(wspace = 0.5)
    plt.subplots_adjust(hspace = 1)
        

#função para construir os gráficos de MPG em relação às variáveis e apresentá-los numa só figura
def juntaGraficosVariavelVsMPG(varNames, arrayInformacao):
    plt.figure(1)
    for i in range(len(varNames) - 1):
        construirGraficoVariavelVsMPG(varNames[i],i+1, arrayInformacao) 
    plt.show()
#-----------------------------------------------------------------


#-----------------------------------------------------------------
def efetuarBinning(arrayInformacao, indiceVariavel, tamanhoIntervalo): #5 valores ou 40 valores (argumentos: quantidade de valores do intervalo, array informacao especifico, dicionarios e variaveis) #encontrar o indice correspondente ao nome
    array = arrayInformacao[:, indiceVariavel]
    maiorNumero = array[np.argmax(array)]
    quantidadeBlocos = (maiorNumero // tamanhoIntervalo)
    
    #if(maiorNumero % tamanhoIntervalo != 0): #se houver mais numeros para alem do ultimo numero do ultimo bloco, criar mais 1 para os restantes numeros
    #    quantidadeBlocos += 1 #PRECISAMOS DISTO????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        
    for l in range(quantidadeBlocos + 1):
        intervalo = np.arange(l * tamanhoIntervalo, (l+1) * tamanhoIntervalo) #modificar para estar sempre a adicionar
        ocorrencias = np.zeros(tamanhoIntervalo, dtype=int)
        for m in array:
            if(m in intervalo):
                ocorrencias[m - intervalo[0]] += 1 #se o numero estiver no intervalo, subtrair o numero ao primeiro do intervalo para obter o indice
        maiorOcorrencia = (np.argmax(ocorrencias) + intervalo[0]) #obtem o indice de maior ocorrencias e adiciona o primeiro do intervalo para obter o numero correto
        array = np.where(((array <= intervalo[len(intervalo) - 1]) & (array >= intervalo[0])), maiorOcorrencia, array) #verifica se os numeros estão no intervalo, se sim muda, se não mantem
    arrayInformacao[:, indiceVariavel] = array #altera a coluna no array das informacoes para o novo array


def binningPrincipal(arrayInformacao, varNames, variaveisEscolhidas):
    for i in variaveisEscolhidas: #faz o codigo por cada variavel
        indice = varNames.index(i) #procura o indice da variavel na lista dos nomes
        if((i == 'Displacement') or (i == 'Horsepower')): 
            tamanhoIntervalo = 5
        else: 
            tamanhoIntervalo = 40
        efetuarBinning(arrayInformacao, indice, tamanhoIntervalo)
#-----------------------------------------------------------------

#-----------------------------------------------------------------
def main():
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
    juntaGraficosVariavelVsMPG(varNames, arrayInformacao)


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
    #apresentaGraficosVariaveis(dicionarioOcorrencias, alfabetoValores, varNames)


    #Tópico 6 --------------------------------------------------------
    binningPrincipal(arrayInformacao, varNames, ['Displacement', 'Horsepower', 'Weight'])
    calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames)  
    apresentaGraficosVariaveis(dicionarioOcorrencias, alfabetoValores, varNames)
    #-----------------------------------------------------------------

#topico 7
#calcular a entropia ponto a
#ponto b - entropia conjunta da matriz de todas as variáveis - entropia dos simbolos mas de todas as variaveis - considerar apos variadas transformadas


#topico 8
#variância ponderada - np.var() calcula a variância simples
#np.average(x) - média simples de x -- np.average(x, weigth=p) media ponderada
#var(x) = E((x-media)^2)


if __name__ == "__main__":
    main()
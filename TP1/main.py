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


def function(): #5 valores
    #ir ao array informacao, dividir em blocos de 5, procurar com o np.argmax o maior (numero de ocorrencias) devolve o indice (numero correspondente a essas ocorrencias)
    #ir ao array da informacao original e substituir os numeros pelos respetivos do intervalo com maior ocorrencias
    array = np.array([1,4,3,5,7,2,7,2,2,2,8,7,0])
    intervalo = np.arange(0, 13)
    ocorrencias = np.zeros_like(intervalo)
    for i in array:
        if(i in intervalo):
            ocorrencias[i] += 1
    maiorOcorrencia = np.argmax(ocorrencias)
    resultado = np.where(, maiorOcorrencia, array) #falta fazer uma condição para verificar que está no intervalo
    print("banana")


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
    
        
        
    function()   


#topico 6
#fazer intervalos e o número para o qual se vai alterar é o número com a maior moda (mais frequente) dos números do intervalo
#binning de 40 simbolos são de 0 até 39 e etc
#np.argmax indice onde ocorre o maximo 
#np.where serve para alterar o valor dos numeros consoante uma condição

#-- temos o intervalo de valores que queremos, encontramos o valor dentro desse intervalo com maior numero de ocorrencias
#-- e à medida que percorremos o array informacao da variavel, vamos alterando os valores que estao dentro do intervalo
#-- para o valor com maior numero


#topico 7
#calcular a entropia ponto a
#ponto b - entropia conjunta da matriz de todas as variáveis - entropia dos simbolos mas de todas as variaveis - considerar apos variadas transformadas


#topico 8
#variância ponderada - np.var() calcula a variância simples
#np.average(x) - média simples de x -- np.average(x, weigth=p) media ponderada
#var(x) = E((x-media)^2)


if __name__ == "__main__":
    main()
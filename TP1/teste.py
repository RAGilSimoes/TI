import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import huffmancodec as huffc


#8/10 - 1,75 em 3 (0,25 não está tudo em funções  0,75 calcular o numero de ocorrencias)

#Funções---------------------------------------------------------
#Tópico 2 --------------------------------------------------------
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

#Tópico 4 e 6--------------------------------------------------------
#função para calcular o número de ocorrências de cada variável e para criar um array dos números com ocorrências                                 
def calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames):
    for i in range(len(varNames)):
        arrayInformacaoUsar = arrayInformacao[:, i] #array da informação a percorrer
        alfabetoValores[varNames[i]] = np.unique(arrayInformacao[:, i]) #array dos números diferentes de zero sem repetição
        dicionarioOcorrencias[varNames[i]] = np.zeros_like(arrayBaseOcorrencias) #array do tamanho de 2**nb começado a zero
        for l in range(len(arrayInformacaoUsar)):
            dicionarioOcorrencias[varNames[i]][arrayInformacaoUsar[l]] += 1 #vai ao indice correspondente e adiciona 1
#-----------------------------------------------------------------


#Tópico 5 e 6--------------------------------------------------------
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




#Tópico 6 --------------------------------------------------------
def efetuarBinning(arrayInformacao, indiceVariavel, tamanhoIntervalo, arrayOcorrencias): 
    array = arrayInformacao[:, indiceVariavel]
    maiorNumero = array[np.argmax(array)]
    quantidadeBlocos = (maiorNumero // tamanhoIntervalo)
    
    #if(maiorNumero % tamanhoIntervalo != 0): #se houver mais numeros para alem do ultimo numero do ultimo bloco, criar mais 1 para os restantes numeros
    #    quantidadeBlocos += 1 #PRECISAMOS DISTO????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        
    for l in range(quantidadeBlocos + 1):
        intervalo = np.array((l * tamanhoIntervalo, (l+1) * tamanhoIntervalo)) #modificar para estar sempre a adicionar
        ocorrencias = np.array((arrayOcorrencias[intervalo[0]], arrayOcorrencias[intervalo[len(intervalo) - 1]])) #como passar o array??? melhorar
        maiorOcorrencia = (np.argmax(ocorrencias) + intervalo[0]) #obtem o indice de maior ocorrencias e adiciona o primeiro do intervalo para obter o numero correto
        array = np.where(((array <= intervalo[len(intervalo) - 1]) & (array >= intervalo[0])), maiorOcorrencia, array) #verifica se os numeros estão no intervalo, se sim muda, se não mantem
    arrayInformacao[:, indiceVariavel] = array #altera a coluna no array das informacoes para o novo array


def binningPrincipal(arrayInformacao, varNames, variaveisEscolhidas, dicionarioOcorrencias):
    for i in variaveisEscolhidas: #faz o codigo por cada variavel
        indice = varNames.index(i) #procura o indice da variavel na lista dos nomes
        if((i == 'Displacement') or (i == 'Horsepower')): 
            tamanhoIntervalo = 5
            array = dicionarioOcorrencias[i]
        else: 
            tamanhoIntervalo = 40
        efetuarBinning(arrayInformacao, indice, tamanhoIntervalo, array)
#-----------------------------------------------------------------


#Tópico 7 --------------------------------------------------------
def valorMedioBits(variavelEscolhida):
    valoresUnicos, contagem = np.unique(variavelEscolhida, return_counts=True) #conta a frequencia de cada simbolo (numero) na coluna do excel
    probabilidades = contagem / len(variavelEscolhida) #calcula probabilidades de cada simbolo e devolve um array em que cada indice é a probabilidade de cada simbolo
    entropia = -np.sum(probabilidades * np.log2(probabilidades)) #fórmula de Shannon
    return entropia


def entropia(varNames, arrayInformacao):
    dicionarioEntropias = {}
    print("Entropia:")
    for i, variavel in enumerate(varNames):
        dicionarioEntropias[variavel] = valorMedioBits(arrayInformacao[:, i])
        print(f"{variavel}: {dicionarioEntropias[variavel]}")
    entropia_total = valorMedioBits(arrayInformacao.flatten()) #Entropia total      #flatten tranforma multiplos arrays em 1 unico
    print(f"Total: {entropia_total}\n")
#-----------------------------------------------------------------


#Tópico 8 --------------------------------------------------------
# def obterInformacoesHuffman(source):
#     codec = huffc.HuffmanCodec.from_data(source)
#     symbols, lengths = codec.get_code_len() #symbols - o mesmo que o unique / length - tamanho de bits para representar cada simbolo
#     return lengths

# def valorMedioBitsHuffman(arrayInformacao):
#     lengths = obterInformacoesHuffman(arrayInformacao)
#     valoresUnicos, contagem = np.unique(arrayInformacao, return_counts=True) #conta a frequencia de cada simbolo (numero) na coluna do excel
#     valorMedioBits = np.average(lengths, weights=(contagem/len(arrayInformacao))) #calcula o tamanho medio de bits por simbolo
#     return valorMedioBits, lengths, contagem

# def varianciaPonderada(arrayInformacao):
#     valorMedioBits, lengths, contagem = valorMedioBitsHuffman(arrayInformacao)
#     variancia = ((lengths - valorMedioBits) ** 2)
#     varianciaPonderada = np.average(variancia, weights=(contagem/len(arrayInformacao)))
#     return varianciaPonderada

def entropiaHuffmanEVarianciaPonderadaHuffmanCadaVariavel(arrayInformacaoPassado):
    codec = huffc.HuffmanCodec.from_data(arrayInformacaoPassado)
    symbols, lengths = codec.get_code_len() #symbols - o mesmo que o unique / length - tamanho de bits para representar cada simbolo

    valoresUnicos, contagem = np.unique(arrayInformacaoPassado, return_counts=True) #conta a frequencia de cada simbolo (numero) na coluna do excel
    probabilidades = (contagem/len(arrayInformacaoPassado))
    valorMedioBits = np.average(lengths, weights=probabilidades) #calcula o tamanho medio de bits por simbolo

    variancia = ((lengths - valorMedioBits) ** 2)
    varianciaPonderada = np.average(variancia, weights=probabilidades)
    return valorMedioBits, varianciaPonderada


def entropiaHuffmanEVarianciaPonderadaHuffman(varNames, arrayInformacao):
    dicionarioVarianciasPonderadasHuffman = {}
    dicionarioEntropiasHuffman = {}
    for i, variavel in enumerate(varNames):
        dicionarioEntropiasHuffman[variavel], dicionarioVarianciasPonderadasHuffman[variavel] = entropiaHuffmanEVarianciaPonderadaHuffmanCadaVariavel(arrayInformacao[:, i])
    entropiaTotalHuffman, varianciaPonderadaTotalHuffman = entropiaHuffmanEVarianciaPonderadaHuffmanCadaVariavel(arrayInformacao.flatten()) #Entropia total      #flatten tranforma multiplos arrays em 1 unico
    return dicionarioVarianciasPonderadasHuffman, dicionarioEntropiasHuffman, entropiaTotalHuffman, varianciaPonderadaTotalHuffman
    
    
def apresentarEntropiaHuffmanEVarianciaPonderada(varNames, arrayInformacao):
    dicionarioVarianciasPonderadasHuffman, dicionarioEntropiasHuffman, entropiaTotalHuffman, varianciaPonderadaTotalHuffman = entropiaHuffmanEVarianciaPonderadaHuffman(varNames, arrayInformacao)
    print("Comprimento médio:")
    for variavel in varNames:
        print(f"{variavel} (por Huffman): {dicionarioEntropiasHuffman[variavel]}")
    print(f"Total (por Huffman): {entropiaTotalHuffman}\n")
    
    print("Variância dos comprimentos:")
    for variavel in varNames:
        print(f"{variavel} (por Huffman): {dicionarioVarianciasPonderadasHuffman[variavel]}")
    print(f"Total (por Huffman): {varianciaPonderadaTotalHuffman}\n")
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
    #-----------------------------------------------------------------
    
    
    #Tópico 2 --------------------------------------------------------
    #construir os gráficos das variávieis--
    juntaGraficosVariavelVsMPG(varNames, arrayInformacao)
    #-----------------------------------------------------------------


    #Tópico 3 --------------------------------------------------------
    #converter os dados para uint16--
    arrayInformacao = arrayInformacao.astype(np.uint16)
    #definir respetivo alfabeto
    nb = (arrayInformacao.itemsize * 8)
    arrayBaseOcorrencias = np.arange(0, 2**nb)
    #-----------------------------------------------------------------

    
    #Tópico 4 --------------------------------------------------------
    alfabetoValores = {} 
    #calcular o número de ocorrências e os valores em que existem ocorrencias
    dicionarioOcorrencias = {}
    calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames)
    #-----------------------------------------------------------------
    
    
    #Tópico 5 --------------------------------------------------------
    #apresentaGraficosVariaveis(dicionarioOcorrencias, alfabetoValores, varNames)
    #-----------------------------------------------------------------


    #Tópico 6 --------------------------------------------------------
    binningPrincipal(arrayInformacao, varNames, ['Displacement', 'Horsepower', 'Weight'], dicionarioOcorrencias)
    calcularNumeroOcorrencias(arrayInformacao, arrayBaseOcorrencias, dicionarioOcorrencias, alfabetoValores, varNames)  
    apresentaGraficosVariaveis(dicionarioOcorrencias, alfabetoValores, varNames)
    #-----------------------------------------------------------------
    
    
    #Tópico 7 --------------------------------------------------------
    entropia(varNames, arrayInformacao)

    #Comentar o resultado: 
        #Acelaracao tem um valor de entropia relativamente alto ou seja ainda existem bastantes valores variados no dataset.
        #Cylindros tem um valor bastante baixo de entropia ou seja sao valores bastantes fixos como (4,6,8) e nao estao longe uns dos outros.
        #Displacement tem um valor de entropia elevado ou seja tem valores bem diversificados.
        #HorsePower tem um valor de entropia elevado mostrando uma grande variedade de elementos no dataset.
        #ModYear tem um valor retalivamente alto mesmo tendo alguns valores fixos.
        #Weight tem um valor de entropia mais alto de todas as variaveis tendo os valores mais distantes.
        #Mpg tem um valor de entropia alto tendo valores bastante variados no dataset.
        
        #OU apenas apresentar os resultados obtidos???
    #-----------------------------------------------------------------


    #Tópico 8 --------------------------------------------------------
    apresentarEntropiaHuffmanEVarianciaPonderada(varNames, arrayInformacao)


if __name__ == "__main__":
    main()
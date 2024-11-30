# Author: Marco Simoes
# Adapted from Java's implementation of Rui Pedro Paiva
# Teoria da Informacao, LEI, 2022
import numpy as np
import sys
from huffmantree import HuffmanTree


class GZIPHeader:
    ''' class for reading and storing GZIP header fields '''

    ID1 = ID2 = CM = FLG = XFL = OS = 0
    MTIME = []
    lenMTIME = 4
    mTime = 0

    # bits 0, 1, 2, 3 and 4, respectively (remaining 3 bits: reserved)
    FLG_FTEXT = FLG_FHCRC = FLG_FEXTRA = FLG_FNAME = FLG_FCOMMENT = 0

    # FLG_FTEXT --> ignored (usually 0)
    # if FLG_FEXTRA == 1
    XLEN, extraField = [], []
    lenXLEN = 2

    # if FLG_FNAME == 1
    fName = ''  # ends when a byte with value 0 is read

    # if FLG_FCOMMENT == 1
    fComment = ''  # ends when a byte with value 0 is read

    # if FLG_HCRC == 1
    HCRC = []

    def read(self, f):
        ''' reads and processes the Huffman header from file. Returns 0 if no error, -1 otherwise '''

        # ID 1 and 2: fixed values
        self.ID1 = f.read(1)[0]
        if self.ID1 != 0x1f: return -1  # error in the header

        self.ID2 = f.read(1)[0]
        if self.ID2 != 0x8b: return -1  # error in the header

        # CM - Compression Method: must be the value 8 for deflate
        self.CM = f.read(1)[0]
        if self.CM != 0x08: return -1  # error in the header

        # Flags
        self.FLG = f.read(1)[0]

        # MTIME
        self.MTIME = [0] * self.lenMTIME
        self.mTime = 0
        for i in range(self.lenMTIME):
            self.MTIME[i] = f.read(1)[0]
            self.mTime += self.MTIME[i] << (8 * i)

        # XFL (not processed...)
        self.XFL = f.read(1)[0]

        # OS (not processed...)
        self.OS = f.read(1)[0]

        # --- Check Flags
        self.FLG_FTEXT = self.FLG & 0x01
        self.FLG_FHCRC = (self.FLG & 0x02) >> 1
        self.FLG_FEXTRA = (self.FLG & 0x04) >> 2
        self.FLG_FNAME = (self.FLG & 0x08) >> 3
        self.FLG_FCOMMENT = (self.FLG & 0x10) >> 4

        # FLG_EXTRA
        if self.FLG_FEXTRA == 1:
            # read 2 bytes XLEN + XLEN bytes de extra field
            # 1st byte: LSB, 2nd: MSB
            self.XLEN = [0] * self.lenXLEN
            self.XLEN[0] = f.read(1)[0]
            self.XLEN[1] = f.read(1)[0]
            self.xlen = self.XLEN[1] << 8 + self.XLEN[0]

            # read extraField and ignore its values
            self.extraField = f.read(self.xlen)

        def read_str_until_0(f):
            s = ''
            while True:
                c = f.read(1)[0]
                if c == 0:
                    return s
                s += chr(c)

        # FLG_FNAME
        if self.FLG_FNAME == 1:
            self.fName = read_str_until_0(f)

        # FLG_FCOMMENT
        if self.FLG_FCOMMENT == 1:
            self.fComment = read_str_until_0(f)

        # FLG_FHCRC (not processed...)
        if self.FLG_FHCRC == 1:
            self.HCRC = f.read(2)

        return 0


class GZIP:
    ''' class for GZIP decompressing file (if compressed with deflate) '''

    gzh = None
    gzFile = ''
    fileSize = origFileSize = -1
    numBlocks = 0
    f = None

    bits_buffer = 0
    available_bits = 0

    def __init__(self, filename):
        self.gzFile = filename
        self.f = open(filename, 'rb')
        self.f.seek(0, 2)
        self.fileSize = self.f.tell()
        self.f.seek(0)
        
    #Tópico 1---------------------------------------
    def lerFormatoBloco(self):
        "Le e retorna o valor correspondente"
        HLIT = self.readBits(5) + 257
        HDIST = self.readBits(5) + 1
        HCLEN = self.readBits(4) + 4
        print(f"HLIT: {HLIT}, HDIST: {HDIST}, HCLEN: {HCLEN}")
        return HLIT, HDIST, HCLEN
    #--------------------------------------------
    
    #Tópico 2---------------------------------------
    def criaArrayCCCC(self, HCLEN):
        array = np.zeros(19, dtype=object)
        ordens = np.array([16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15])
        for i in range(HCLEN):
            array[ordens[i]] = self.readBits(3)
        return array
    
    def criaArrayHDIST(self, HDIST):
        array = np.zeros(HDIST, dtype=object)
        for i in range(HDIST):
            array[i] = self.readBits(3)
        return array
    #--------------------------------------------
    
    #Tópico 3---------------------------------------
    def converterCompDecimal(self, array):
        Ac = np.unique(array)
        Ac= Ac[Ac>0]
        
        decimal=0
        valoresDecimais = np.array([None]*len(array), dtype=object)

        for i in Ac:
            decimais = np.where(array == i)[0]
            for l in range(len(decimais)): 
                valoresDecimais[decimais[l]] = decimal
                decimal += 1
            decimal = (decimal << 1)          
        return valoresDecimais
    
    def converterBinarios(self, decimais, array):
        binarios = np.array([None]* len(decimais), dtype=object)
        for i in range(len(decimais)):
            decimal = decimais[i]
            if (decimal != None):
                binario = ""
                while decimal > 0:
                    resto = (decimal & 1)
                    binario = str(resto) + binario
                    decimal = (decimal >> 1)
                if len(binario)<array[i]:
                    binario = "0"*(array[i]-len(binario))+binario
                binarios[i] = binario
        return binarios
    #--------------------------------------------
    
    #Tópico 4---------------------------------------
    def funcaoTopico4(self, HLIT, binarios):
        arrhlit = [0] * (HLIT+ 257 ) #mudar para numpy

        hft = HuffmanTree()
        for i, code in enumerate(binarios):
            if code is not None:
                hft.addNode(code, i) 

        index = 0

        while index < len(arrhlit):
            hft.resetCurNode()
            simb = -2

            while (simb == -2):
                bit = self.readBits(1) 
                simb = hft.nextNode(str(bit))
                if (simb == -1):
                    print("erro árvore de Huffman")
                    return -1

            if simb <= 15:
                arrhlit[index] = simb
                index += 1
            elif simb == 16:
                quantidade = (3+ self.readBits(2))
                simbolo = arrhlit[index - 1]
                arrhlit[index: index + quantidade] = [simbolo] * quantidade
                index += quantidade
            elif simb == 17:
                quantidade = (3+ self.readBits(3))
                simbolo = 0
                arrhlit[index: index + quantidade] = [simbolo] * quantidade
                index += quantidade
            elif simb == 18:
                quantidade = (11+ self.readBits(7))
                simbolo = 0
                arrhlit[index: index + quantidade] = [simbolo] * quantidade
                index += quantidade
        return arrhlit
    #--------------------------------------------
    
    #Tópico 5---------------------------------------
    def funcaoTopico5(self, HDIST, arrayHDIST):
        arrhdist = [0] * (HDIST+ 1)

        hft = HuffmanTree()
        for i, code in enumerate(arrayHDIST):
            if code is not None:
                hft.addNode(code, i)

        index = 0

        while index < len(arrhdist):
            hft.resetCurNode()
            simb = -2

            while (simb == -2):
                bit = self.readBits(1) 
                simb = hft.nextNode(str(bit))
                if (simb == -1):
                    print("erro árvore de Huffman")
                    return -1

            if simb <= 15:
                arrhdist[index] = simb
                index += 1
            elif simb == 16:
                quantidade = (3+ self.readBits(2))
                simbolo = arrhdist[index - 1]
                arrhdist[index: index + quantidade] = [simbolo] * quantidade
                index += quantidade
            elif simb == 17:
                quantidade = (3+ self.readBits(3))
                simbolo = 0
                arrhdist[index: index + quantidade] = [simbolo] * quantidade
                index += quantidade
            elif simb == 18:
                quantidade = (11+ self.readBits(7))
                simbolo = 0
                arrhdist[index: index + quantidade] = [simbolo] * quantidade
                index += quantidade
        return arrhdist
    #--------------------------------------------
    
                
    def decompress(self):
        ''' main function for decompressing the gzip file with deflate algorithm '''

        numBlocks = 0

        # get original file size: size of file before compression
        origFileSize = self.getOrigFileSize()
        print(origFileSize)

        # read GZIP header
        error = self.getHeader()
        if error != 0:
            print('Formato invalido!')
            return

        # show filename read from GZIP header
        print(self.gzh.fName)

        # MAIN LOOP - decode block by block
        BFINAL = 0
        while not BFINAL == 1:

            BFINAL = self.readBits(1)

            BTYPE = self.readBits(2)
            if BTYPE != 2:
                print('Error: Block %d not coded with Huffman Dynamic coding' % (numBlocks + 1))
                return

            # --- STUDENTS --- ADD CODE HERE
            #
            #
            
            #Tópico 1--------------------------
            HLIT, HDIST, HCLEN = self.lerFormatoBloco()
            #---------------------------------
            
            #Tópico 2--------------------------
            arrayCCCC = self.criaArrayCCCC(HCLEN)
            print(arrayCCCC)
            #---------------------------------
            
            #Tópico 3--------------------------
            decimaisLiterais = self.converterCompDecimal(arrayCCCC)
            binariosLiterais=self.converterBinarios(decimaisLiterais, arrayCCCC)
            print(binariosLiterais)
            
            #---------------------------------
            
            #Tópico 4--------------------------
            arrayHLIT = self.funcaoTopico4(HLIT, binariosLiterais)
            print("\nArray de comprimentos literais:")
            print(arrayHLIT)
            #---------------------------------
            
            #Tópico 5---------------------------
            arrayHdist = self.criaArrayHDIST(HDIST)
            decimaisDistancias = self.converterCompDecimal(arrayHdist)
            binariosDistancias = self.converterBinarios(decimaisDistancias, arrayHdist)
            
            arrayHDIST = self.funcaoTopico5(HDIST, binariosDistancias)
            print("\nArray de comprimentos distâncias:")
            print(arrayHDIST)
            #--------------------------------- 
            
            #topico 4
            # hft.addNode(string binária, simbolo no excel)
            #pegar nas strings binárias e criar árvores de huffman
            # ler da árvore, hft.nextNode(nextBit) devolve: -1 se for erro; -2 se ainda não chegou a uma folha; devolve o valor do simbolo se chegar a uma folha
            # se devolve 17, ir ao ficheiro deflate rfc e ver o que significa o resultado
            # adicionar no excel na coluna comprimentos, a quantidade depois temos que adicionar ao mínimo o valor de readBits com o que eles dizem no fim do numero
            # (ver print tirada)
            #se o valor não disser nada no rfc é só meter como comprimento esse valor devolvido
            #código 18 repetir o 0 11 + readBits(7) vezes
            #codigo 16 repete o último valor 3 + readBits(2) vezes
            #após acabar de ler o valor, apontar o ponteiro para o inicio da arvore, usando o resetCurNode
            
            #topico 5
            #mesma coisa que o 4
            
            #topico 6
            #mesma coisa que o 3
            
            #topico 7
            # 0 a 255, literais ; 256, EOB (end of block); 257 a 285, comp lZ77
            #codigo literal -> guardar no array de saída
            #comp lz77 -> vamos buscar a distância à árvore de comprimentos
            #devolve array com os números
            
            #topico 8
            #gravar o que está no array para ficheiro
            #fazer append
            #quando chega ao EOB, pega no array e grava no ficheiro
            #máximo 32768
            
            # update number of blocks read
            numBlocks += 1

        # close file

        self.f.close()
        print("End: %d block(s) analyzed." % numBlocks)

    def getOrigFileSize(self):
        ''' reads file size of original file (before compression) - ISIZE '''

        # saves current position of file pointer
        fp = self.f.tell()

        # jumps to end-4 position
        self.f.seek(self.fileSize - 4)

        # reads the last 4 bytes (LITTLE ENDIAN)
        sz = 0
        for i in range(4):
            sz += self.f.read(1)[0] << (8 * i)

        # restores file pointer to its original position
        self.f.seek(fp)

        return sz

    def getHeader(self):
        ''' reads GZIP header'''

        self.gzh = GZIPHeader()
        header_error = self.gzh.read(self.f)
        return header_error

    def readBits(self, n, keep=False):
        ''' reads n bits from bits_buffer. if keep = True, leaves bits in the buffer for future accesses '''

        while n > self.available_bits:
            self.bits_buffer = self.f.read(1)[0] << self.available_bits | self.bits_buffer
            self.available_bits += 8

        mask = (2 ** n) - 1
        value = self.bits_buffer & mask

        if not keep:
            self.bits_buffer >>= n
            self.available_bits -= n

        return value


if __name__ == '__main__':

    # gets filename from command line if provided
    fileName = "FAQ.txt.gz" #TP2/base code - python/FAQ.txt.gz
    if len(sys.argv) > 1:
        fileName = sys.argv[1]

    # decompress file
    gz = GZIP(fileName)
    gz.decompress()
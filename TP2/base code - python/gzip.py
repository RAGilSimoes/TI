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
    #--------------------------------------------
    
    #Tópico 3---------------------------------------
    def converterCompDecimal(self, array):
        Ac = np.unique(array)
        Ac= Ac[Ac>0]
        
        decimal=0
        valoresDecimais = np.array([None]*np.size(array), dtype=object)
        
        mn = np.min(Ac)
        mx = np.max(Ac)

        for i in range(mn, mx+1):
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
                while decimal != 0:
                    resto = (decimal % 2)
                    binario = str(resto) + binario
                    decimal = (decimal >> 1)
                if len(binario)<array[i]:
                    binario = "0"*(array[i]-len(binario))+binario
                binarios[i] = binario
        return binarios
    #--------------------------------------------
    
    #Tópico 4/5---------------------------------------
    def criaArvore(self, binarios):
        hft = HuffmanTree()
        for i, code in enumerate(binarios):
            if code is not None:
                hft.addNode(code, i) 
                
        return hft
    
    def funcaoTopico4e5(self, hUsado,arvore):
        array = np.empty(0, dtype=object)

        index = 0

        while index < hUsado:
            arvore.resetCurNode()
            simb = -2

            while (simb == -2):
                bit = self.readBits(1) 
                simb = arvore.nextNode(str(bit))
            
            if (simb == -1):
                print("erro árvore de Huffman")
                return -1

            if simb <= 15:
                array = np.append(array, simb)
                index += 1
            elif simb == 16:
                quantidade = (3+ self.readBits(2))
                simbolo = array[index - 1]
                array = np.append(array, [simbolo] * quantidade)
                index += quantidade
            elif simb == 17:
                quantidade = (3+ self.readBits(3))
                simbolo = 0
                array = np.append(array, [simbolo] * quantidade)
                index += quantidade
            elif simb == 18:
                quantidade = (11+ self.readBits(7))
                simbolo = 0
                array = np.append(array, [simbolo] * quantidade)
                index += quantidade
        return array
    #--------------------------------------------
    
    #Tópico 7---------------------------------------
    def funcaoTopico7(self, hUsado, arvoreLiterais, arvoreDistancias):
        array = np.empty(0, dtype=object)
        arrayLiteraisComprimentos = np.array([3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258], dtype=int)
        arrayDistancias = np.array([1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577], dtype=int)
        arrayReadBitsLiterais = np.array([0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0], dtype=int)
        arrayReadBitsDistancias = np.array([0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13], dtype=int)

        index = 0

        while True:
            arvoreLiterais.resetCurNode()
            simboloLiterais = -2

            while (simboloLiterais == -2):
                bit = self.readBits(1) 
                simboloLiterais = arvoreLiterais.nextNode(str(bit))
            
            if (simboloLiterais == -1):
                print("erro árvore de Huffman literais")
                return -1 

            if simboloLiterais <= 255:
                array = np.append(array, simboloLiterais)
                index += 1
            elif simboloLiterais == 256:
                break
            else:
                indiceArray = (simboloLiterais - 257)
                tamanho = (arrayLiteraisComprimentos[indiceArray] + self.readBits(arrayReadBitsLiterais[indiceArray]))
                
                arvoreDistancias.resetCurNode()
                simboloDistancias = -2
                while(simboloDistancias == -2):
                    bit = self.readBits(1)
                    simboloDistancias = arvoreDistancias.nextNode(str(bit))
                if(simboloDistancias == -1):
                    print("erro árvore de Huffman distâncias")
                    return -1
                    
                distancia = (arrayDistancias[simboloDistancias] + self.readBits(arrayReadBitsDistancias[simboloDistancias]))
                
                for i in range(tamanho):
                    array = np.append(array, array[-distancia])
                
                index += 1
                
        for i in array:
            print(chr(i))
                        
        return array 
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
            print("\nBinarios de comprimentos de codigos:")
            print(binariosLiterais)
            #---------------------------------
            
            #Tópico 4--------------------------
            arvoreLiterais = self.criaArvore(binariosLiterais)
            arrayHLIT = self.funcaoTopico4e5(HLIT, arvoreLiterais)
            print("\nArray de comprimentos literais:")
            print(arrayHLIT)
            #---------------------------------
            
            #Tópico 5---------------------------
            arrayHDIST = self.funcaoTopico4e5(HDIST, arvoreLiterais)
            print("\nArray de comprimentos distâncias:")
            print(arrayHDIST)
            #--------------------------------- 

            #Tópico 6--------------------------
            decimaisLiteraisComprimentos = self.converterCompDecimal(arrayHLIT)
            binariosLiteraisComprimentos=self.converterBinarios(decimaisLiteraisComprimentos, arrayHLIT)
            arvoreLiteraisComprimentos = self.criaArvore(binariosLiteraisComprimentos)
            print("\nBinarios de comprimentos literais:")
            print(binariosLiteraisComprimentos)
            #....................................
            decimaisDistancias = self.converterCompDecimal(arrayHDIST)
            binariosDistancias=self.converterBinarios(decimaisDistancias, arrayHDIST)
            arvoreDistancias = self.criaArvore(binariosDistancias)
            print("\nBinarios de distancias:")
            print(binariosDistancias)
            #---------------------------------
            
            #Tópico 7--------------------------
            arrayCaracteresFinal = self.funcaoTopico7(HLIT, arvoreLiteraisComprimentos, arvoreDistancias)
            #---------------------------------
            
            #Tópico 8--------------------------
            #arrayCaracteresFinal = self.funcaoTopico7(HLIT, arvoreLiteraisComprimentos, arvoreDistancias)
            #---------------------------------
            
            
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

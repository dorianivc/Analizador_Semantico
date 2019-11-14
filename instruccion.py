class Instruccion:
    def __init__(self,linea):
        self.linea=linea
        self.palabras=list()
        ##PROCESAMOS LAS LINEAS PARA PASARLAS A PALABARAS
        lista_de_palabras=self.linea.split(' ')
        espacios_vacios=lista_de_palabras.count('')
        for i in range(espacios_vacios):
            lista_de_palabras.remove('')
        tam=len(lista_de_palabras)
        var=lista_de_palabras[tam-1]
        palabra_a_cambiar=var.split('\n')[0]
        lista_de_palabras.remove(var)
        lista_de_palabras.insert(tam-1,palabra_a_cambiar)
        self.palabras=lista_de_palabras

    def imprime_palabras(self):
        print(self.palabras)
    def get_linea(self):
        return self.linea


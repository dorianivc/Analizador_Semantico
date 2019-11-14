from instruccion import Instruccion
class analizador_de_texto:
    def __init__(self):
        self.lineas= list() 
        self.handler=None
        self.nombre=None

    def leer_archivo(self,nombre):
        try:
            self.handler=open(nombre,"r", encoding='UTF8')
            self.nombre=nombre
        except IOError:
            return None

    def imprimr_archivo(self):
        print(self.handler.read())
        self.leer_archivo(self.nombre)
    
    def procesa_lineas(self):
        archivo=self.handler
        linea=archivo.readline()
        while linea != '':
            #print(linea)
            var=Instruccion(linea.__str__())
            self.lineas.append(var)
            linea=archivo.readline()
        self.leer_archivo(self.nombre)
    def obtener_datos_to_go(self,nombre_del_archivo):
        self.leer_archivo(nombre_del_archivo)
        self.procesa_lineas()
        #print("Imprimiento los datos a ser exportados en forma de lista")
        #self.imprimr_archivo()
        return self.lineas


if __name__ == "__main__":
    analizador=analizador_de_texto()
    nombre="codigo.txt"
    instrucciones=analizador.obtener_datos_to_go(nombre)
    linea1=instrucciones.pop(2)
    print(linea1.palabras)
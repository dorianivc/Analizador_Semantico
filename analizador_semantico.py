from analizador_archivos import analizador_de_texto
from variable import Variable
import queue;
class Analizador_semantico:
    def __init__(self):
        self.tabla_de_valores={'variable':dict(), 'funcion':dict()}
        self.analizador_de_texto= analizador_de_texto()
        self.codigo=None
        
    def cargar_codigo(self, ubicacion_del_archivo):
       self.codigo= self.analizador_de_texto.obtener_datos_to_go(ubicacion_del_archivo)

    def contiene_dato_primitivo(self, dato):
        if(dato.find("string")!=-1 or dato.find("int") or dato.find("float")):
            return True
        return False    
    
    def analizar_codigo(self):
        size=len(self.codigo)
        localidad=False
        nombre_de_la_funcion=queue.LifoQueue()
        for i in range(size):
            linea_actual=self.codigo[i]
            linea_textual=str(linea_actual.get_linea())
            #print(linea_textual)
            var=i+1
            
            if((linea_textual.find("int")!=-1 or linea_textual.find("string")!=-1 or linea_textual.find("float")!=-1) and  linea_textual.find("=")!=-1):
                ##Si entra a este if, es que realiza una declaracion y asignacion(instanciacion) de variable, por lo tanto la linea deberia tener al menos 3 palabras
                print("Instaciacion de variable en linea #: ", var)
                size=len(linea_actual.palabras)
                tipo_de_dato=linea_actual.palabras[0]
                nombre_de_variable=linea_actual.palabras[1]
                valor=" "
                if(size<=3):
                    aux=linea_actual.palabras[2].split("=")
                    valor=aux[0]
                elif(size>=4):
                    valor=linea_actual.palabras[3]
                if(valor.find(";")):
                    aux=valor.split(";")
                    valor=aux[0]
                alcance="global"
                if(localidad is True):
                    alcance="local"
                variable= Variable(nombre_de_variable,valor,alcance)
                print("Tipo de dato ", tipo_de_dato, "nombre: ", nombre_de_variable, "valor: ", valor)
                var=self.tabla_de_valores.get('variable')
                var[nombre_de_variable]=variable
                self.tabla_de_valores['variable']=var











            elif(linea_textual.find("=")!=-1):
                ##Entra aqui si encuentra una asignacion de variable
                print("Asignacion en linea #: ", var)
                nombre= linea_actual.palabras[0]
                pos=linea_textual.find("=")
                tam=len(linea_textual)
                pos=pos+1
                valor=linea_textual[pos:tam]
                valor=valor.split(';')[0]           
                diccionario=self.tabla_de_valores['variable']
                if(diccionario.get(nombre) is not None):
                    variable=diccionario[nombre]
                    variable.valor=valor
                    diccionario[nombre]=variable
                    self.tabla_de_valores['variable']=diccionario
                    print("Valor actualizado en la tabla de simbolos")
                else:
                    print("Error de asignacion en linea #: ", var, " la variable ","''" , nombre,"''", " no ha sido declarada")
              


            elif((linea_textual.find("int")!=-1 or linea_textual.find("string")!=-1 or linea_textual.find("float")!=-1 or linea_textual.find("void")!=-1) and  (linea_textual.find("()")!=-1 or linea_textual.find("( )")!=-1 or linea_textual.find("(  )")!=-1)):
                print("Declaracion de una funcion sin parametros en la linea #: ", var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var) 
                    localidad=True
                    aux=linea_actual.palabras[1]
                    posicion_final=aux.find("(") 
                    if(posicion_final!=-1):
                        nombre_de_la_funcion.put(aux[0:posicion_final])
                        
            elif(linea_textual.find("return")!=-1):
                print("Sentencia RETURN en linea #: ", var)
                print("Fin de alcance de funcion en linea #: ", var)
            













            elif((linea_textual.find("int")!=-1 or linea_textual.find("string")!=-1 or linea_textual.find("float")!=-1) or linea_textual.find("void")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1)):
                #Entra aquí si encuentra declaracion de funcion
                print("Declaracion de funcion con parametros en linea #: ", var)
                comas=linea_textual.count(",")
                if(comas==0):
                    #un parametro
                    
                    if()
                if(comas>0):


                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var)  
                    localidad=True
                    aux=linea_actual.palabras[1]
                    posicion_final=aux.find("(") 
                    if(posicion_final!=-1):
                        nombre_de_la_funcion.put(aux[0:posicion_final])
                        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            elif((linea_textual.find("if")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1))):
                print("Declaracion de condicional if en linea #: ",var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var)   
                    localidad=True
                    #nombre_de_la_funcion=
                    #parametro
            
            
            
            
            
            
            
            
            
            
            elif((linea_textual.find("while")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1))):
                print("Declaracion de sentencia while en linea #: ", var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var) 
                    localidad=True   
            
            
            
            
            
            
            
            elif(linea_textual.find("{")!=-1):
                print("Inicio de alcance en linea # ", var)  
                localidad=True
                        
            
            
            
            
            
            
            elif(linea_textual.find("}")!=-1):
                print("Fin de alcance en linea ", var)
                localidad=False

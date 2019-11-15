from analizador_archivos import analizador_de_texto
from variable import Variable
import queue;
class Analizador_semantico:
    def __init__(self):
        self.tabla_de_valores={'variable':dict(), 'funcion':dict(), 'parametro':dict()}
        self.analizador_de_texto= analizador_de_texto()
        self.codigo=None
        
    def cargar_codigo(self, ubicacion_del_archivo):
       self.codigo= self.analizador_de_texto.obtener_datos_to_go(ubicacion_del_archivo)

    def contiene_dato_primitivo(self, dato):
        if(dato.find("string")!=-1 or dato.find("int") or dato.find("float")):
            if(dato=="string" or dato=="int" or dato=="float"):
                return True
        else:
            return False    
    
    def analizar_codigo(self):
        size=len(self.codigo)
        localidad=False
        nombre_de_la_funcion=queue.LifoQueue()
        nombre_de_la_funcion.put("global")
        for i in range(size):
            infunc=nombre_de_la_funcion.get()
            nombre_de_la_funcion.put(infunc)
            print("Localidad: ", localidad)
            print("Funcion ", infunc)
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
                variable.tipo_de_dato=tipo_de_dato
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
                    print("Error de asignacion en linea #: ", var, " la variable o tipo de dato ","''" , nombre,"''", " no ha sido declarada")
              


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
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var)  
                    localidad=True
                    aux=linea_actual.palabras[1]
                    posicion_final=aux.find("(") 
                    if(posicion_final!=-1):
                        nombre_de_la_funcion.put(aux[0:posicion_final])
                nombre_funcion_actual=aux[0:posicion_final]
                        
                if(comas==0):
                    #un parametro, solo sacamos el nombre de la funcion 
                    tipo_de_dato_parametro=aux[posicion_final+1:]
                    nombre_del_parametro=linea_actual.palabras[2]
                    #print(nombre_del_parametro)
                    if(nombre_del_parametro.find(")")!=-1):
                        nombre_del_parametro=nombre_del_parametro.split(")")[0]
                    if(nombre_del_parametro.find("}")!=-1):
                        nombre_del_parametro=nombre_del_parametro.split("}")[0]
                    nombre_funcion_actual=aux[0:posicion_final]
                    print("NOMBRE DEL PARAMETRO "+ nombre_del_parametro+ " Tipo de Dato: ",tipo_de_dato_parametro)
                    parametro=Variable(nombre_del_parametro,"SIN DEFINIR", nombre_funcion_actual)
                    parametro.tipo_de_dato=tipo_de_dato_parametro   
                    parametro.es_parametro=True 
                    diccionario=self.tabla_de_valores['parametro'] 
                    if(diccionario.get(nombre_del_parametro) is  None):
                        diccionario[nombre_del_parametro]=parametro
                        self.tabla_de_valores['parametro']=diccionario
                        print("Parametro agregado")
                        print("Valor actualizado en la tabla de simbolos")
                    
                if(comas>0):
                    cantidad_de_variables=comas+1
                    cantidad_de_bloques=2*cantidad_de_variables

                    #tomamos primer bloque foo(int
                    tipo_de_dato=linea_actual.palabras[1][posicion_final+1:]
                    nombre_del_parametro=linea_actual.palabras[2]
                    if(nombre_del_parametro.find(",")!=-1):
                        nombre_del_parametro=nombre_del_parametro.split(",")[0]
                    print("Nombre: ", nombre_del_parametro,"Tipo de dato ", tipo_de_dato)
                    cantidad_de_bloques=cantidad_de_bloques-3
                   
                    primer_par=Variable(nombre_del_parametro,"sin asignar", nombre_funcion_actual)
                    primer_par.es_parametro=True
                    primer_par.tipo_de_dato=tipo_de_dato
                    diccionario=self.tabla_de_valores['parametro'] 
                    if(self.contiene_dato_primitivo(tipo_de_dato)):

                        if(diccionario.get(nombre_del_parametro) is  None):
                            diccionario[nombre_del_parametro]=primer_par
                            self.tabla_de_valores['parametro']=diccionario
                            print("Parametro agregado")
                            print("Valor actualizado en la tabla de simbolos")
                    else:
                        print("Error-> tipo de dato no primitivo o inaceptado: ", tipo_de_dato)
                    for i in range(1,cantidad_de_bloques):
                        index=(2*i)+1
                        tipo_de_dato=linea_actual.palabras[index]
                        nombre_del_parametro=linea_actual.palabras[index+1]
                        if(nombre_del_parametro.find(")")!=-1):
                            nombre_del_parametro=nombre_del_parametro.split(")")[0]
                        if(nombre_del_parametro.find("}")!=-1):
                            nombre_del_parametro=nombre_del_parametro.split("}")[0]
                        if(nombre_del_parametro.find(",")!=-1):
                            nombre_del_parametro=nombre_del_parametro.split(",")[0]
                        if(tipo_de_dato.find(",")!=-1):
                            tipo_de_dato=tipo_de_dato.split(",")[0]
                        print("Nombre: ", nombre_del_parametro,"Tipo de dato ", tipo_de_dato)
                        if(self.contiene_dato_primitivo(tipo_de_dato) is True):

                            parametros=Variable(nombre_del_parametro,"sin asignar",nombre_funcion_actual)
                            parametros.es_parametro=True
                            parametros.tipo_de_dato=tipo_de_dato
                            if(diccionario.get(nombre_del_parametro) is  None):
                                diccionario[nombre_del_parametro]=primer_par
                                self.tabla_de_valores['parametro']=diccionario
                                print("Parametro agregado")
                                print("Valor actualizado en la tabla de simbolos")
                        else:
                            print("Error-> tipo de dato no primitivo o inaceptado: ", tipo_de_dato)
                        
                       
                        


                
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            elif((linea_textual.find("if")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1))):
                print("Declaracion de condicional if en linea #: ",var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var)   
                    localidad=True
                    nombre_de_la_funcion.put("if")

                    
                    #revisar que existan los parametro
            
            elif((linea_textual.find("while")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1))):
                print("Declaracion de sentencia while en linea #: ", var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var) 
                    localidad=True
                    nombre_de_la_funcion.put("while")
                       
            
            
            
            
            
            
            
            elif(linea_textual.find("{")!=-1):
                print("Inicio de alcance en linea # ", var)  
                localidad=True
                        
            
            
            
            
            
            
            elif(linea_textual.find("}")!=-1):
                print("Fin de alcance en linea ", var)
                flag=nombre_de_la_funcion.get()
                if(flag=="global"):
                    localidad=False
                    nombre_de_la_funcion.put("global")
                
                

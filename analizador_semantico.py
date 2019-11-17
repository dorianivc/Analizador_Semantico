from analizador_archivos import analizador_de_texto
from variable import Variable
from funcion import Funcion
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
    def existe_dentro_de_una_funcion(self,variable,funcion):
        size=len(funcion.variables)
        for i in range(size):
            if(funcion.variables[i].nombre==variable):
                return True
        return False
    def retorna_variable_desde_funcion(self,variable,funcion):
        if(self.existe_dentro_de_una_funcion(variable,funcion) is True):
            size=len(funcion.variables)
            for i in range(size):
                if(funcion.variables[i].nombre==variable):
                    return funcion.variables[i]
        return None
    def que_tipo_de_dato(self,var):
        if(self.es_int(var) is True):
            return "int"
        elif(self.es_float(var) is True):
            return "float"
        elif(self.es_string(var) is True):
            return "string"
        else:
            return -1
    def es_float(self,var):
        size=len(var)
        for i in range(size):
            if(var[i].isdigit() is not True):
                if(var[i]!="."):
                    return False
        return True
    def es_string(self,var):
        size=len(var)
        if(var[0]=='"' and var[size-1]=='"'):
            return True
        return False
    def es_int(self,var):
        return var.isdigit()

    def analizar_codigo(self):
        diccionario_de_funciones=self.tabla_de_valores['funcion']
        size=len(self.codigo)
        localidad=False
        nombre_de_la_funcion=queue.LifoQueue()
        nombre_de_la_funcion.put("global")
        metodos=list()
        metodos.append(Funcion("global","int"))
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
                metodo_actual=metodos.pop()
                if(metodo_actual.nombre!="global"):
                    metodo_actual.variables.append(variable)
                    metodos.append(metodo_actual)
                else:
                    metodos.append(metodo_actual)
                

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
                #elif(self.tabla_de_valores['parametro'].get(nombre) is not None)
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
                nombre_funcion_actual=aux[0:posicion_final]
                _funcion=Funcion(nombre_funcion_actual,linea_actual.palabras[0])
                if(diccionario_de_funciones.get(_funcion) is None):
                    diccionario_de_funciones[_funcion]=_funcion
                    self.tabla_de_valores['funcion']=diccionario_de_funciones
                    print("Funcion ", _funcion.nombre, " ha sido agregada a la tabla")
                    print(diccionario_de_funciones.keys())
                else:
                    print("La funcion ya existe")
                        
            elif(linea_textual.find("return")!=-1 ):
                print("Sentencia RETURN en linea #: ", var)
                aux=metodos[len(metodos)-1]
                if(aux.valor_de_retorno.find("void")!=-1 and len(linea_actual.palabras)<=2):
                    if(len(linea_actual.palabras)==2):
                        if(linea_actual.palabras[1]!=";"):
                            print("ERROR retornando metodo en linea ", var, " metodo es void")
                        else:
                            print("Interrumpe procedimiento en linea # ", var)
                    elif(linea_actual.palabras[0]=="return" or linea_actual.palabras[0]=="return;"):
                        print("Interrumpe procedimiento en linea # ", var)
                        #metodos.pop()
                    else:
                        print("ERROR EN SENTENCIA RETURN EN LINEA # ", var)
                    
                elif(aux.valor_de_retorno.find("int")!=-1 and  len(linea_actual.palabras)<=3):
                    #puede retornar un valor costante o variable
                    lin=linea_actual.palabras[1]
                    if(lin.find(";")!=-1):
                        lin=lin.split(";")[0]
                    
                    if(lin.isdigit() is True):
                        #es contante
                        print("Retorna constante int", lin)
                    else:
                        size=len(aux.variables)
                        verdad=False
                        for i in range(size):
                            if(aux.variables[i].nombre==lin and aux.variables[i].tipo_de_dato=="int"):
                                print("Retorno de variable local int ",lin)
                                verdad=True
                                i=2*size
                        if(self.tabla_de_valores['variable'].get(lin) is not None):
                            print("Retorno de variable global int", lin)
                            verdad=True
                        if(verdad is not True):
                            print("ERROR Retorna variable inexistente o de tipo de dato distinto")
                elif(aux.valor_de_retorno.find("float")!=-1 and  len(linea_actual.palabras)<=3): 
                    #puede retornar un valor costante o variable
                    lin=linea_actual.palabras[1]
                    if(lin.find(";")!=-1):
                        lin=lin.split(";")[0]
                    es_float=True
                    for i in range(len(lin)):
                        if(not (str(lin[i]).isdigit() or lin[i]==".")):
                            es_float=False
                            i=2*len(lin)
                    if(es_float is True):
                        print("Retorna valor constante float: ", lin)
                    if(es_float is False):
                        size=len(aux.variables)
                        verdad=False
                        for i in range(size):
                            if(aux.variables[i].nombre==lin and aux.variables[i].tipo_de_dato=="float"):
                                print("Retorno de variable local float",lin)
                                verdad=True
                                i=2*size
                        if(self.tabla_de_valores['variable'].get(lin) is not None):
                            print("Retorno de variable global float", lin)
                            verdad=True
                        if(verdad is not True):
                            print("ERROR Retorna variable inexistente o de tipo de dato distinto")
                        
                elif(aux.valor_de_retorno.find("string")!=-1 and  len(linea_actual.palabras)<=3):
                    #puede retornar un valor costante o variable
                    lin=linea_actual.palabras[1]
                    if(lin.find(";")!=-1):
                        lin=lin.split(";")[0]
                    if(lin[0]=='"' and lin[(len(lin)-1)]=='"'):
                        print("Retorna valor constante string: ", lin)
                    else:
                        size=len(aux.variables)
                        verdad=False
                        for i in range(size):
                            if(aux.variables[i].nombre==lin and aux.variables[i].tipo_de_dato=="string"):
                                print("Retorno de variable local string ",lin)
                                verdad=True
                                i=2*size
                        if(self.tabla_de_valores['variable'].get(lin) is not None):
                            print("Retorno de variable global string", lin)
                            verdad=True
                        if(verdad is not True):
                            print("ERROR Retorna variable inexistente o de tipo de dato distinto")
                else:
                    print("Error retornando variable en linea ", var)
                                    
                

            
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
                _funcion=Funcion(nombre_funcion_actual,linea_actual.palabras[0])
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
                    _funcion.variables.append(parametro) #cargando parametros
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
                            _funcion.variables.append(primer_par)
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
                            _funcion.variables.append(parametros)
                            diccionario[nombre_del_parametro]=primer_par
                            self.tabla_de_valores['parametro']=diccionario
                            print("Parametro agregado")
                            print("Valor actualizado en la tabla de simbolos")
                        else:
                            print("Error-> tipo de dato no primitivo o inaceptado: ", tipo_de_dato)
                metodos.append(_funcion)
                if(diccionario_de_funciones.get(_funcion) is None):
                    diccionario_de_funciones[_funcion]=_funcion
                    self.tabla_de_valores['funcion']=diccionario_de_funciones
                    print("Funcion ", _funcion.nombre, " ha sido agregada a la tabla")
                    print(diccionario_de_funciones.keys())
                else:
                    print("La funcion ya existe")
                        
            
            elif((linea_textual.find("if")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1))):
                print("Declaracion de condicional if en linea #: ",var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var)   
                    localidad=True
                    nombre_de_la_funcion.put("if")
                _funcion=Funcion(linea_textual,"boolean")
                inicio=linea_textual.find("(")+1
                final=""
                if(linea_textual.find(")}")!=-1):
                    final=linea_textual.find(")}")
                elif(linea_textual.find(")")!=-1):
                    final=linea_textual.find(")")
                tripleta=linea_textual[inicio:final]
                tripleta=tripleta.split(" ")
                if(tripleta[1]=="<" or tripleta[1]==">" or tripleta[1]=="<=" or tripleta[1]==">=" or tripleta[1]=="==" or tripleta[1]=="!="):
                    #"operador logico aceptado"
                    variable_1=tripleta[0]
                    const_1=False
                    const_2=False
                    variable_2=tripleta[2]
                    _funcion_anterior=metodos.pop()
                    metodos.append(_funcion_anterior)
                    if(variable_1.isidentifier()):
                        if(self.existe_dentro_de_una_funcion(variable_1,_funcion_anterior) is True):
                            variable_1=self.retorna_variable_desde_funcion(variable_1,_funcion_anterior)
                            const_1=True
                            print("primer variable del if existente en linea #", var)
                        elif(self.tabla_de_valores['variable'].get(variable_1) is not None):
                            variable_1=self.tabla_de_valores['variable'].get(variable_1)
                            print("primer variable del if existente en linea #", var)
                            const_1=True
                    else:
                        if(self.es_string(variable_1) is True or self.es_int(variable_1) is True or self.es_float(variable_1) is True):
                            
                            print("primer parametro del if es costante, por lo tanto es aceptada en linea # ", var)
                        else:
                            print("primer parametro del if : " ,variable_1, " no es permitido")
                    if(variable_2.isidentifier()):
                        if(self.existe_dentro_de_una_funcion(variable_2,_funcion_anterior) is True):
                            variable_2=self.retorna_variable_desde_funcion(variable_2,_funcion_anterior)
                            print("segundo variable del if existente en linea #", var)
                            const_2=True
                        elif(self.tabla_de_valores['variable'].get(variable_2) is not None):
                            variable_2=self.tabla_de_valores['variable'].get(variable_2)
                            print("segundo variable del if existente en linea #", var)
                            const_2=True
                    else:
                        if(self.es_string(variable_2) is True or self.es_int(variable_2) is True or self.es_float(variable_2) is True):
                            
                            print("segundo parametro del if es costante, por lo tanto es aceptada en linea # ", var)
                        else:
                            print("segundo parametro del if : " ,variable_2, " no es permitido")
                    #ya se sabe que son datos permitidos pero ellos dos tienen que ser iguales
                    if(const_1==True and const_2==True):
                        if(variable_1.tipo_de_dato==variable_2.tipo_de_dato):
                            print("tipo de dato igual")
                        else:
                            print("tipo de datos de variables diferente en linea # ", var)
                    elif(const_1!=True and const_2!=True):
                        if(self.que_tipo_de_dato(variable_1)==self.que_tipo_de_dato(variable_2)):
                            print("ambos condiciones son constantes")
                        else:
                            print("Tipo de dato a utilizar son diferentes en linea # ", var)
                    elif(const_1!=True and const_2==True):
                        if(self.que_tipo_de_dato(variable_1)==variable_2.tipo_de_dato):
                            print("comparacion constante variable aceptada en linea # ", var)
                        else:
                            print("comparacion constante variable aceptada, tipo de datos distintos en linea # ", var)

                    elif(const_1==True and const_2!=True):
                        if(self.que_tipo_de_dato(variable_2)==variable_1.tipo_de_dato):
                            print("comparacion constante variable aceptada en linea # ", var)
                        else:
                            print("comparacion constante variable aceptada, tipo de datos distintos en linea # ", var)
                    metodos.append(_funcion)
                    
                else:
                    print("Error en linea ", var, "operacion: ", tripleta[1], "no soportada")
                

                    
                    #revisar que existan los parametro
            
            elif((linea_textual.find("while")!=-1 and  (linea_textual.find("(")!=-1 and linea_textual.find(")")!=-1))):
                print("Declaracion de sentencia while en linea #: ", var)
                if(linea_textual.find("{")):
                    print("Inicio de alcance en linea # ", var) 
                    localidad=True
                    nombre_de_la_funcion.put("while")
                _funcion=Funcion(linea_textual,"boolean")
                inicio=linea_textual.find("(")+1
                final=""
                if(linea_textual.find(")}")!=-1):
                    final=linea_textual.find(")}")
                elif(linea_textual.find(")")!=-1):
                    final=linea_textual.find(")")
                tripleta=linea_textual[inicio:final]
                tripleta=tripleta.split(" ")
                if(tripleta[1]=="<" or tripleta[1]==">" or tripleta[1]=="<=" or tripleta[1]==">=" or tripleta[1]=="==" or tripleta[1]=="!="):
                    #"operador logico aceptado"
                    variable_1=tripleta[0]
                    const_1=False
                    const_2=False
                    variable_2=tripleta[2]
                    condicion=True
                    _funcion_anterior=None
                    while(condicion):
                        _funcion_anterior=metodos.pop()
                        
                        if(_funcion_anterior.nombre.find("if")!=-1 or _funcion_anterior.nombre.find("while")!=-1 ):
                            condicion=True
                        else:
                            condicion=False
                    if(variable_1.isidentifier()):
                        if(self.existe_dentro_de_una_funcion(variable_1,_funcion_anterior) is True):
                            variable_1=self.retorna_variable_desde_funcion(variable_1,_funcion_anterior)
                            const_1=True
                            print("primer variable del while existente en linea #", var)
                        elif(self.tabla_de_valores['variable'].get(variable_1) is not None):
                            variable_1=self.tabla_de_valores['variable'].get(variable_1)
                            print("primer variable del while existente en linea #", var)
                            const_1=True
                    else:
                        if(self.es_string(variable_1) is True or self.es_int(variable_1) is True or self.es_float(variable_1) is True):
                            
                            print("primer parametro del while es costante, por lo tanto es aceptada en linea # ", var)
                        else:
                            print("primer parametro del while : " ,variable_1, " no es permitido")
                    if(variable_2.isidentifier()):
                        if(self.existe_dentro_de_una_funcion(variable_2,_funcion_anterior) is True):
                            variable_2=self.retorna_variable_desde_funcion(variable_2,_funcion_anterior)
                            print("segundo variable del while existente en linea #", var)
                            const_2=True
                        elif(self.tabla_de_valores['variable'].get(variable_2) is not None):
                            variable_2=self.tabla_de_valores['variable'].get(variable_2)
                            print("segundo variable del while existente en linea #", var)
                            const_2=True
                    else:
                        if(self.es_string(variable_2) is True or self.es_int(variable_2) is True or self.es_float(variable_2) is True):
                            
                            print("segundo parametro del while es costante, por lo tanto es aceptada en linea # ", var)
                        else:
                            print("segundo parametro del while : " ,variable_2, " no es permitido")
                    #ya se sabe que son datos permitidos pero ellos dos tienen que ser iguales
                    if(const_1==True and const_2==True):
                        if(variable_1.tipo_de_dato==variable_2.tipo_de_dato):
                            print("tipo de dato igual")
                        else:
                            print("tipo de datos de variables diferente en linea # ", var)
                    elif(const_1!=True and const_2!=True):
                        if(self.que_tipo_de_dato(variable_1)==self.que_tipo_de_dato(variable_2)):
                            print("ambos condiciones son constantes")
                        else:
                            print("Tipo de dato a utilizar son diferentes en linea # ", var)
                    elif(const_1!=True and const_2==True):
                        if(self.que_tipo_de_dato(variable_1)==variable_2.tipo_de_dato):
                            print("comparacion constante variable aceptada en linea # ", var)
                        else:
                            print("comparacion constante variable aceptada, tipo de datos distintos en linea # ", var)

                    elif(const_1==True and const_2!=True):
                        if(self.que_tipo_de_dato(variable_2)==variable_1.tipo_de_dato):
                            print("comparacion constante variable aceptada en linea # ", var)
                        else:
                            print("comparacion constante variable aceptada, tipo de datos distintos en linea # ", var)
                    metodos.append(_funcion)
                    
                else:
                    print("Error en linea ", var, "operacion: ", tripleta[1], "no soportada")
                

                       
            
            
            elif(linea_textual.find("{")!=-1):
                print("Inicio de alcance en linea # ", var)  
                localidad=True
                        
            
            elif(linea_textual.find("}")!=-1):
                print("Fin de alcance en linea ", var)
                flag=nombre_de_la_funcion.get()
                if(flag=="global"):
                    localidad=False
                    nombre_de_la_funcion.put("global")
                
                

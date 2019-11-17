class Variable:
    def __init__(self,nombre,valor,alcance):
        self.nombre=nombre
        self.valor=valor
        self.alcance=alcance
        self.es_parametro=False
        self.tipo_de_dato=None
 
    def variable_to_string(self):
        var="Var: "+ self.nombre + "Valor "+ self.valor+ " Alcance->Funcion: "+ self.alcance
        return var

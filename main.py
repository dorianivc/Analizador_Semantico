from analizador_semantico import Analizador_semantico

analizador=Analizador_semantico()
nombre="codigo.txt"
analizador.cargar_codigo(nombre)
analizador.analizar_codigo()
var=analizador.tabla_de_valores['variable']
#print(var['x'].valor)

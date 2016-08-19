######################################################################################################################################
##  DOCUMENTACION                                                                                                             		##
##  "Micro-sistema de archivos"                                                                    		                     		##
##  Alumno: Cardoso Valencia Carlos Eric                                                                                 			##
##                                                                                                                       			## 
##  ROBLEMA QUE BUSCA RESOLVER 																						   				##
##  A traves de una imitacion de consola de comandos, este programa simula un micro-sistema de archivos, el cual soporta   			##
##  un maximo de 10 archivos, representados sobre un directorio plano, en donde el tamano de un archivo esta dado por    			##
##  la cantidad de caracteres que tiene (100 como nuumero maximo)    						   										##
##  y donde ademas los nombres de los archivos estan restringidos a 8 caracteres.   												##
##   																																##
##  LOGICA DE OPERACION 																							   				##
##  El sitema de archivos utiliza un metodo llamado 'shell' que simula una consola de comandos.   									##
##  A traves de esta se llaman a los comandos contenidos en una clase Comandos(),													##
##  mismas funciones que implementan operaciones sobre directorios y archivos tales como:                                           ## 
##          listdir: muestra la informacion de los archivos  																		##
##          crear -a: crea un archivo en el directorio                    															##
##		    eliminar -a: Elimina un archivo del directorio  																		##
##		    escribir -a: Escribe en un archivo.   																					##
##		    leer -a: Lee de archivo   																								##
##		    --salir: Salir de la consola  																						    ##
##		    --limpiar: Limpia la pantalla  																							##
##	  																															    ##
##  Para lograr su proposito  el programa se vale de diccionarios.    																##
##  Al crear un archivo, el sistema guarda su nombre en la llave de un diccionario en donde en su respectivo valor 				    ##
## 	asignamos un espacio en blanco, mismo que sera llenado con la operacion de escritura. 											##
##  El borrado es simplemente eliminar la llave del diccionario y la lectura consiste en mostrar los valores de una respectiva 	    ##
##  llave del diccionario     																										##
##  Listar un directorio implica presentar la informacion de los diccionarios 														##
##																																	##
##																														     		##
## EJEMPLOS DE INVOCACION  																											##
## en la 'consola'																													##
## >> listdir  																													    ##
## >> Directorio vacio   																											##
## >> crear -a  																													##
## :: archivo1 																														##
## >> listdir   																													##
## >> Numero de archivos: 1 																										##
## >> Nombre de archivo: archivo1. Contenido:   Tamano de archivo: 0c 																##
## >> escribir -a 																													##
## :: archivo1 																														##
## :: esto es una cadena 	 																										##
## >> leer -a 																													    ##
## :: archivo1  																													##
## :: esto es una cadena  																											##
######################################################################################################################################

import os

#Implementacion de las funcioens sobre archivos y directorios.
class Comandos():
	#Rangos para los archivos. 
	def __init__(self):
		self.num_archivos = 0
		self.archivos = {}
		self.maximo_archivos = 10
		self.maximo_tamano_archivo = 100
		self.maximo_tamano_nombre = 8

	def ayuda(self):
		print ">>"
		print("listdir: muestra la informacion de los archivos en el directorio ")
		print("crear -a: crea un archivo en el directorio (tamano maximo del nombre: %d caracteres)" %self.maximo_tamano_nombre)
		print("eliminar -a: elimina un archivo del directorio")
		print("escribir -a: escribe en un archivo. Tamano maximo del archivo: %d" %self.maximo_tamano_archivo)
		print("leer -a: lee de archivo ")
		print("--salir: salir de la consola")
		print("--limpiar: limpia la pantalla ")
		print ("\n")
		print("Para las operaciones con archivos: ")
		print("*Ejecutar 'crear -a'  y posteriormente asignar el nombre al archivo")
		print("*Ejecutar 'eliminar -a'  y luego introducir el nombre del archivo")
		print("*Ejecutar 'escribir -a'  y posteriormente indicar el nombre del archivo, luego el texto a introducir")
		print("*Ejecutar 'leer -a'  y luego introducir el nombre del archivo")
		

	def listdir(self):
		if(self.num_archivos == 0):
			print "Directorio vacio"
		else:
			print "Numero de archivos: %s" %self.num_archivos
		
			nombres =  self.archivos.keys()
			texto = self.archivos.values()
			elementos = self.archivos.items()

			for nombres,texto in elementos:
				print("Nombre de archivo: %s" %nombres, "Contenido:  %s " %texto, "Tamano de archivo:  %sc" %(len(texto) ) ) #len(texto) . El numero de caracteres que representa el tamano de archivo. 
	#Al crear un archivo se verifica si aun existe espacio en el sistema de archivos. 
	def crear_archivo(self):

		if (self.num_archivos<=self.maximo_archivos): #Hay espacio en el sistema de archivos para mas elementos. 			
				nombre = raw_input("::")  
				if self.archivos.has_key(nombre): 
					print(">>Este archivo ya existe")
				else:  
					if(len(nombre) > self.maximo_tamano_nombre):
						print ("No se pudo crear el archivo. Nombre no debe exceder de %d caracteres" %self.maximo_tamano_nombre)
					
					else:
						self.num_archivos = self.num_archivos +1
						self.archivos[nombre] = " " #El nombre en la clave del diccionario acompanado de un espacio vacio.  
						
		
		else:
			print ("Se excedio el limite de archivos soportado por este sistema de archivos")


	def eliminar_archivo(self):

		nombre = raw_input("::")

		if self.archivos.has_key(nombre): #Verifica si existe el archivo en el diccionario
			del self.archivos[nombre] 
			self.num_archivos = self.num_archivos -1

		else:
			print ">> El archivo no existe"

	#Verifica que el archivo exista y que el contenido a escribir en el archivo no exceda del permitido. 
	def escribir_archivo(self):
		nombre = raw_input("::")

		if self.archivos.has_key(nombre): 
			texto = raw_input("::")
			if (len(texto) <= self.maximo_tamano_archivo): #Permite un maximo de 20 caracteres
				self.archivos[nombre] = texto
			else:
				print ("Se excede el limite de tamano de archivo")

		else:
			print ">> El archivo no existe"

	#Leyendo el contenido de un archivo del directorio, si es que este existe, tomando los datos segun su clave o key. 
	def leer_archivo(self):
		nombre = raw_input("::")

		if self.archivos.has_key(nombre): 
				print self.archivos[nombre] 
		else:
			print ">> El archivo no existe"

	def salir(self):
		print " "

	def limpiar(self):
		os.system('cls')

#Imitacion de una consola de comandos
#Los comandos con sus respectivos metodos se almacenan en un directorio para utilizarlo como un switch
def shell():
	print ">>"
	print "Teclear --ayuda para ver lista de comandos"
	cmd = Comandos()
	comando = "entrar" #PARA ENTRAR AL CICLO
	while(comando != "--salir"):
		print ">>"
		comandos = {'--ayuda': cmd.ayuda, 'listdir': cmd.listdir, '--limpiar': cmd.limpiar, '--salir': cmd.salir, 'crear -a': cmd.crear_archivo, 'eliminar -a': cmd.eliminar_archivo,'escribir -a': cmd.escribir_archivo, 'leer -a': cmd.leer_archivo}
		comando = raw_input()
		
		try:
			comandos[comando]()
		except:
			print (" %s no se reconoce como un comando. --ayuda para ver lista de comandos" %comando)



shell()
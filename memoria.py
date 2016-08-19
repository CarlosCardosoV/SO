#########################################################################################################################
##  DOCUMENTACION                                                                                                      ##
##  "Monitor de la memoria del sistema"                                                                    		       ##
##  Alumno: Cardoso Valencia Carlos Eric                                                                               ##
##                                                                                                                     ## 
##  ROBLEMA QUE BUSCA RESOLVER 																						   ##
##  Este monitor de memoria busca brindar al usuario un mayor conocimiento sobre la memoria principal, enfocandose     ##
##  en un sistema tipo Windows.  																					   ##
##  A traves de una interfaz grafica que pretende ser simple y agradable presenta datos acerca de la memoria que       ##
##  podria ser util conocer. 																					       ##
##																												       ##
##  LOGICA DE OPERACION 																							   ##
##  El monitor funciona con el uso de dos clases. Una de ellas, la clase InfoMemoria(), incorpora funciones del 	   ##
##  modulo psutil de Python para conocer datos especificos de la memoria.  											   ##
##  La clase Graficas() toma los datos de InfoMemoria() y aplica metodos para presentar estos datos de forma visual.   ##
##  La construccion de estas graficas se crean con el modulo matplotlib. 											   ##		
##  Los metodos de Graficas() son llamados desde un menu principal, construido con el modulo Tkinter de Python.   	   ##
##	 																												   ## 
##  Breve guia de la interfaz. 																						   ##
##	La ventana principal presenta un pequeno menu con opciones para ver informacion especifica de la memoria.          ##
##	Hacer clic en "VER" para visualizar el contenido grafico. En algunas graficas se recomienda hacer uso del zoom     ##
##	que esta en la parte inferior izquierda de la ventana. Tambien en ese lugar se encuentran botones para ir a la     ##
##	visualizacion anterior de una misma grafica, para guardar la imagen, imprimir y moverse  dentro de la grafica.     ##
##																													   ##
##																												       ##
## --------																											   ##
##	Nota: para la ejecucion del programa es necesario tener instalados los modulos psutil y matplotlib de python.      ##
#########################################################################################################################


from Tkinter import *
import matplotlib.pyplot as plt
import psutil

#Informacion de la memoria a traves de las funciones de psutil
class InfoMemoria():
   def __init__(self): 
        self.num_procesos = 0
        for proceso in psutil.process_iter(): 
                self.num_procesos +=1

        self.memoria = psutil.virtual_memory() 
       	self.memoria_proc = [proc.memory_info() for proc in psutil.process_iter()]
       	self.nombre = [proc.name() for proc in psutil.process_iter()]
        self.swap = psutil.swap_memory()
        #p = psutil.Process()
		#info = p.memory_info_ex()

#Construccion de las graficas con base en datos de InfoMemoria()
class Graficas():
	def __init__ (self):
		self.mem = InfoMemoria()
	
	def mem_panorama_general(self):
		mem_total = float((self.mem.memoria[0]*(pow(10,-9))))  #Conversion a GB
		mem_disponible = float((self.mem.memoria[1]*(pow(10,-9)))) 
		mem_usada = float((self.mem.memoria[3]*(pow(10,-9)))) 
	
		#Grafica pastel
		porc_mem_disponible =  (mem_disponible*100)/mem_total
		porc_mem_usada = (mem_usada*100)/mem_total
		porcentajes = [porc_mem_disponible, porc_mem_usada] 
		etiquetas = ['Disponible (%.2f GB)' %mem_disponible, 'Utilizada (%.2f GB)' %mem_usada]  
		explode = [0, 0.1]  #Corte de la grafica pastel
		plt.pie(porcentajes, labels = etiquetas, explode = explode)  
		plt.title('Memoria. Panorama general. Total (%.2f GB)' %mem_total)
		plt.show()

	def mem_proceso(self):
		mem_total = float((self.mem.memoria[0]*(pow(10,-6)))) #Conversion a GB
		mem_proceso = self.mem.memoria_proc #Memoria ocupada por cada proceso
		nombre = self.mem.nombre
		procesos = self.mem.num_procesos 

		mem_fisica = [0]*procesos 
		mem_virtual = [0]*procesos

		
		for i in range(procesos):
			mem_fisica[i] = float(mem_proceso[i][0]*(pow(10,-6))) #conversion a mb
			mem_virtual[i] = float(mem_proceso[i][1]*(pow(10,-6))) 

		#La suma de los elementos maximos de ambas listas, con el fin de restringir la longitud del eje de memoria.
		max_mem_fisica = max(mem_fisica)
		max_mem_virtual = max(mem_virtual)
		suma = max_mem_virtual+max_mem_fisica 

		fig = plt.figure() 
		ax = fig.add_subplot(111) #creacion de eje. 
		plt.title("Gasto de memoria por proceso. Fisica (azul). Virtual (verde). [Hacer zoom]")
		xx = range(procesos)
		ax.bar(xx,mem_fisica,facecolor='#0000FF') #Azul, mem fisica
		ax.bar(xx,mem_virtual,facecolor = '#00FF00') #Verde, mem virtual
		plt.ylim(0, suma)
		plt.xticks(xx,nombre,size = 7, rotation = 90)
		 	
		plt.ylabel("Memoria. Total = %.2f MB" %mem_total) 
		plt.xlabel("Procesos") 

		plt.show()

	def mem_swap(self):
		swap_total = float((self.mem.swap[0]*(pow(10,-9)))) #Conversion a GB 
		swap_usada = float((self.mem.swap[1]*(pow(10,-9)))) 
		swap_libre = float((self.mem.swap[2]*(pow(10,-9))))

		porc_swap_usada =  (swap_usada*100)/swap_total
		porc_swap_libre = (swap_libre*100)/swap_total
		
		porcentajes = [porc_swap_usada, porc_swap_libre]

		etiquetas = ['Swap en uso (%.2f GB)' %swap_usada, 'Swap libre (%.2f GB)' %swap_libre]  
		explode = [0, 0.1] 
		plt.pie(porcentajes, labels = etiquetas, explode = explode)  
		
		plt.title('Memoria en swap. Total (%.2f GB)' %swap_total)
		plt.show()

	def mem_cache(self):
		return 0

	def mem_otros(self):
		p = psutil.Process()
		info = p.memory_info_ex()
		procesos = self.mem.num_procesos 
		longitud = len(info) 
		
		info2 = [0]*longitud
		
		#Info 2, copia de info, con el fin de poder modificarla
		for i in range(longitud):
			info2[i] = info[i]

		for i in range(longitud):
			info2[i] = float((info2[i]*(pow(10,-6)))) #CONVERSION A GB
		
		maximo = max(info2) +10 #El elemento mayor para restringir el eje vertical.
		fig = plt.figure() 
		ax = fig.add_subplot(111) #creacion de eje. 
		plt.title("Mas datos sobre la memoria [Hacer zoom en area deseada]")
		xx = range(longitud)
		etiquetas = ["Fallos de pagina","Peak work set","work set", "Peak paged pool", "paged pool", "Peak non paged pool", "non paged pool", "page file", "peak page file" ,"private"]
		ax.bar(xx,info2,facecolor='#FFFF00')

		plt.ylim(0,maximo)
		plt.xticks(xx,etiquetas,size = 10, rotation = "30")
		 	
		plt.ylabel("Memoria en MB")  

		plt.show()
	
#Interfaz grafica del menu principal

ventana_principal = Tk()
graf = Graficas()
ventana_principal.config(bg="gray")
ventana_principal.title("Monitor de memoria")
ventana_principal.geometry("300x350")

#Etiquetas y botones del menu principal
Label(ventana_principal, text = " ", bg = "gray").grid()
Label(ventana_principal, text = "Gasto de memoria (panorama general.)",bg = "white", height = 3, width = "35").grid(row = 10, column = 20)
Label(ventana_principal, text = " ", bg = "gray").grid()
Label(ventana_principal, text = "Gasto de memoria por proceso (fisica y virtual)", bg = "white", height = 3, width = "35").grid(row = 20, column  = 20)
Label(ventana_principal, text = " ", bg = "gray").grid()
Label(ventana_principal, text = "Swap de memoria", bg = "white", height = 3, width = "35").grid(row = 30, column = 20)
Label(ventana_principal, text = " ", bg = "gray").grid()
Label(ventana_principal, text = "Otros datos (paginacion,etc)", bg = "white", height = 3, width = "35").grid(row = 40, column = 20)
Label(ventana_principal, text = " ", bg = "gray").grid()

Button(ventana_principal,text = "VER", height = 3, width = 4, command = graf.mem_panorama_general).grid(row = 10, column = 80)
Button(ventana_principal,text = "VER", height = 3, width = 4, command = graf.mem_proceso).grid(row = 20, column = 80)
Button(ventana_principal,text = "VER", height = 3, width = 4, command = graf.mem_swap).grid(row = 30, column = 80)
Button(ventana_principal,text = "VER", height = 3, width = 4, command = graf.mem_otros).grid(row = 40, column = 80)



ventana_principal.mainloop() 




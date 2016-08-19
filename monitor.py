###################################################################################################################
## DOCUMENTACION                                                                                                 ##
## "Monitor de procesos y recursos en python"                                                                    ##
## Alumno: Cardoso Valencia Carlos Eric                                                                          ##
##                                                                                                               ## 
## El programa monitorea los procesos dados en un sistema operativo y algunos recursos relacionados.             ##
## Indica el pid, el nombre, estado, el tiempo que cada uno de ellos ha pasado en modo kernel o usuario,         ##
## la memoria consumida por cada proceso y el numero de hilos que esta usando cada uno                           ##
## Tambien incorpora un pequeno menu con las opciones de actualizar monitor y salir del mismo                    ##
##                                                                                                               ## 
## Logica de operacion                                                                                           ##
## El programa utiliza dos clases: una clase Proceso cuyo constructor incorpora listas con informacion referente ##
## a los procesos y una clase Monitor que toma los datos de las listas de Proceso y los muestra al usuario       ##
## Se ejectua el programa de forma concurrente llamando a los metodos de Monitor y se sincronizan                ##
## utilizando semaforos                                                                                          ##                                                                                          
##                                                                                                               ##
## Este pograma busca brindarle al usuario mayor conocimiento de los procesos que se ejecutan en su sistema      ##
##                                                                                                               ##
## Nota1: tener instalado el modulo psutil para el correcto funcionamiento del programa                          ##
## Nota2: es necesario configurar el ancho de la shell al ancho de la pantalla para una optima visualizacion de  ##
##        las columnas, de lo contrario se traslaparan al siguiente renglon.                                     ##
##        En windows =>   cmd:*clic derecho en la parte superior izquierda de la ventana                         ##
##                            *seleccionar "predeterminados"                                                     ##
##                            *clic en "diseno"                                                                  ##
##                            *modificar el ancho de la consola al de nuestra pantalla                           ##
##                            *clic en aceptar                                                                   ##
##                            *cerrar y volver a abrir la consola para visualizar cambios                        ##
###################################################################################################################


import psutil
import threading 
import time
import os

tabla = threading.Semaphore(0)
menu = threading.Semaphore(0)
tiempo = 0.2

class Proceso():
    #Informacion relacionada con los procesos como parametros iniciales en este constructor
    def __init__(self):
        self.num_procesos = 0
        for proceso in psutil.process_iter():
                self.num_procesos +=1
        
        #Listas con informacion relativa a cada proceso.
        self.pid = psutil.pids()
        self.nombre = [proc.name() for proc in psutil.process_iter()]
        self.estado = [proc.status() for proc in psutil.process_iter()]
        self.memoria = psutil.virtual_memory() 
        self.cpu_t = [proc.cpu_times() for proc in psutil.process_iter()]
        self.hilos = [proc.num_threads() for proc in psutil.process_iter()]
        self.memoria_proc = [proc.memory_info() for proc in psutil.process_iter()]
        
        #Modifica los nombres de la lista 'estado' de "running" a "En ejecucion" y de "stopped" a "Bloqueado" 
        for i in range (self.num_procesos):
            if self.estado[i] == "running":
                self.estado[i] = "En ejecucion"
            elif self.estado[i] == "stopped":
                self.estado[i] = "Bloqueado"        

class Monitor():
    def cabecera(self):
        
        proceso = Proceso()
        num_procesos = proceso.num_procesos
        
        #Impresion de datos generales. Se extraen los datos desde la clase Proceso 
        print "\n---------------MONITOR DE PROCESOS Y RECURSOS DEL SISTEMA-------------------\n"
        time.sleep(1.8) 
        print "*** Total de procesos corriendo en el sistema:  %d " %num_procesos
        time.sleep(tiempo)
        print "*** Numero de procesadores fisicos %s" %psutil.cpu_count(logical = False)
        time.sleep(tiempo)
        print "*** Indicadores de memoria. "
        time.sleep(tiempo)
        print "       Porcentaje de memoria usada por los procesos: %s %s" %(proceso.memoria[2],chr(37)) 
        print "       Total: %.2f GB" %float((proceso.memoria[0]*(pow(10,-9)))) #Conversion a GB
        time.sleep(tiempo)
        print "       Disponible: %.2f GB" %float((proceso.memoria[1]*(pow(10,-9))))
        time.sleep(tiempo)
        print "       Memoria en uso: %.2f GB" %float((proceso.memoria[3]*(pow(10,-9))))
        time.sleep(tiempo)
        print "\n\n  "
        tabla.release() #Comienza el desglose de los datos generales.
        

    def tabla(self):
        #Primero se ejecuta la cabecera. 
        tabla.acquire()
        
        proceso = Proceso()
        num_procesos = proceso.num_procesos
        
        print ("----      Desglose de informacion \n\n")     
        
        print '{0:10s} {1:40s} {2:15s} {3:15s} {4:5s} {5:6s} {6:4s}'.format("    PID", " Nombre","Estado","Hilos usados", "Tiempo modo usuario [s]", "Tiempo modo kernel [s]","Memoria utilizada [MB]") 
        
        ren = 1
        #Impresion en columnas de la informacion relativa a los procesos, extraidas de las respectivas listas de la clase Proceso
        for ren in range(num_procesos):
            time.sleep(tiempo) 
            print '{0:6d} {1:40s} {2:15s} {3:15d} {4:18d} {5:23d} {6:20f}'.format(proceso.pid[ren], proceso.nombre[ren], proceso.estado[ren],proceso.hilos[ren],int(proceso.cpu_t[ren][0]), int(proceso.cpu_t[ren][1]),float((proceso.memoria_proc[ren][0]*(pow(10,-6)))) )
        
        menu.release() #Comienza la ejecucion del menu

    #Pequeno menu con algunas opciones para el usuario
    def menu(self):
        proceso = Proceso()
        menu.acquire()
        
        opcion = 5 #Para entrar al ciclo
        while(opcion != 0):
            print "\n  MENU "
            print " Selecciona  0) Salir del monitor"
            print "             1) Actualizar monitor"   
            
            try:
                opcion = int(raw_input("\n\t Opcion : "))
                
                if opcion == 0:
                    print ("-----------Monitor Finalizado")
                
                if opcion == 1:
                    os.system('cls')
                    threading.Thread(target = Monitor().cabecera).start() 
                    threading.Thread(target = Monitor().tabla).start()
                    threading.Thread(target = Monitor().menu).start()
                break
            except ValueError:
                print "\n\t Opcion no valida. Intenta otra vez"
        

#Lanzando los hilos
threading.Thread(target = Monitor().cabecera).start() 
threading.Thread(target = Monitor().tabla).start()
threading.Thread(target = Monitor().menu).start()




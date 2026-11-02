
#import tkinter as tk
#from tkinter import ttk
import threading as hilo
import sys as sistema
import itertools as iterar
import random as ale
import os
import time as tiempo
from collections import deque


#Variables globales 
Quantum = 3 #Definimos una constante del tiempo de ejecución del Round Robin 
recurso_1 = hilo.Lock()
recurso_2 = hilo.Lock()
abortando = False
Lista_procesos_creados = list()
Lista_uso_memoria = list()
pid_reloj = iterar.count(start= 1)

# Objeto memoria
class Memoria:

    __espacio__memoria_disponible = 100    
    def __init__(self, pid: int, memoria_proceso: int):

        if memoria_proceso <= Memoria.__espacio__memoria_disponible:
            self.__pid = pid
            self.__espacio__memoria_ocupada = memoria_proceso

            Memoria.__espacio__memoria_disponible -= self.__espacio__memoria_ocupada
        else:
            raise MemoryError("No hay espacio suficiente en la memoria del proceso ")

    def getPid(self):
        return self.__pid
    
    def getEspacioMemoriaProceso(self):
        return self.__espacio__memoria_ocupada



    def setEspacioMemoriaProceso(self, memoria_proceso: int):
        
        diferencia = memoria_proceso - self.__espacio__memoria_ocupada
        if diferencia >  Memoria.__espacio__memoria_disponible:
            raise MemoryError(f"Desbordamiento de memoria por parte del proceso: {self.__pid}")

        Memoria.__espacio__memoria_disponible -= diferencia
        self.__espacio__memoria_ocupada = memoria_proceso


    
    def setPid(self, pid):
        self.__pid = pid


    @classmethod    
    def getMemoria_Disponible(cls):
        return cls.__espacio__memoria_disponible


#Objeto de estados
class Estados:
    EST_NUEVO = "Nuevo"
    EST_LISTO = "Listo"
    EST_EJECUCION = "Ejecución"
    EST_BLOQUEADO = "Bloqueado"
    EST_FIN = "Terminado"


#Objeto Proceso (Clase para la creación del PCB)
class Proceso:
    _ciclo_reloj = iterar.count(start= 0)

    def __init__(self,pid,tamanio_memoria,rafaga_cpu):
        self.__pid = pid
        self.__estado_actual = Estados.EST_NUEVO
        self.__tamanio_memoria = tamanio_memoria
        self.__rafaga__proceso = rafaga_cpu
        self.__rafaga_cpu = 0
        self.__rafaga_restante = rafaga_cpu
        self.__llegada__AT = next(self._ciclo_reloj)
        self.__bloque__memoria = None

    def getPid(self):
        return self.__pid
        
    def getEstado_actual(self):
        return self.__estado_actual

    def getTamanio_memoria(self):
        return self.__tamanio_memoria

    def getLlegada(self):
            return self.__llegada__AT
    
    def getRafaga_CPU(self):
            return self.__rafaga_cpu
    
    def getRafagaRestante(self):
                return self.__rafaga_restante
        

    
    def cambio_estado(self,estado):
        self.__estado_actual = estado
    
    def cambioTamaño_memoria(self, memoria: int):
        self.__tamanio_memoria = memoria
    
    
    def rafaga_CPU(self, rafaga: int):
        self.__rafaga_cpu = rafaga
    
    
    def rafaga_CPU_restante(self, rafaga_restante: int):
        self.__rafaga_restante = rafaga_restante


    def tiempoFinalizado(self):
        pass
        if self.__estado_actual != Estados.EST_EJECUCION:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return
            
        self.cambio_estado(Estados.EST_LISTO)


    def asignarMemoria(self, memoria):
        self.__bloque__memoria = memoria


    def finalizacion(self):
            if self.__estado_actual != Estados.EST_EJECUCION:
                print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
                return
                        
            self.cambio_estado(Estados.EST_FIN)

    def salida(self):
            print("-"*31)
            print(f"|{'*'*5} Proceso [PID: {self.__pid}] {'*'*5:<1}|")
            print(f"|Estado del proceso: {self.__estado_actual:<9}|")
            print(f'|Tamaño de la memoria: {self.__tamanio_memoria:<7}|')
            print(f"|Tiempo AT: {self.__llegada__AT:<18}|")
            print(f"|Rafaga del proceso: {self.__rafaga__proceso:<9}|")
            print(f'|Ráfaga del  CPU consumido: {self.__rafaga_cpu:<2}|')
            print(f'|Ráfaga restante: {self.__rafaga_restante:<11} |')
            print("-"*31)
            if self.__estado_actual != Estados.EST_FIN:
                print("                          |                        ")
                print("                          |                        ")
                print("                          v                        ")
    
            else:
                if self.__bloque__memoria is not None:
                    self.__bloque__memoria.setEspacioMemoriaProceso(0)
                    print(f"Memoria del proceso PID: {self.__pid} ha sido liberado.")
                    print(f"Espacio disponible de la Memoria: {Memoria.getMemoria_Disponible()} MB\n")
    
            print()    





#-------->Procesos 
def creacion_proceso():
    pass
    pid = next(pid_reloj)
    mE = ale.randint(2,10)
    rafaga = ale.randint(1,10)


    nuevo_proceso_memoria = Memoria(pid,mE)
    if Memoria.getMemoria_Disponible() > nuevo_proceso_memoria.getEspacioMemoriaProceso():
        nuevo_proceso = Proceso(pid,mE,rafaga)

        nuevo_proceso.asignarMemoria(nuevo_proceso_memoria)
        Lista_uso_memoria.append(nuevo_proceso_memoria)
        Lista_procesos_creados.append(nuevo_proceso)

def imprimir_tabla():
    for lista_proceso in Lista_procesos_creados:
        lista_proceso.salida()
        

    print("Procesos creados correctamente.")
    print(f"Memoria disponible: {Memoria.getMemoria_Disponible()} MB")  


def cola_listos():
    for lista_proceso in Lista_procesos_creados:
        lista_proceso.cambio_estado(Estados.EST_LISTO)

    print("*******LOS PROCESOS HAN PASADO A LA COLA DE LISTOS*******")
    





#-------------> Algoritmo de Round Robin 



def planificador_Round_Robin():
    global Q
    cola_listos = deque()
    tiempo = 0
    quantum = Quantum

    #Ordenamos los procesos por su tiempo de llegada
    procesos_cola = sorted(
        Lista_procesos_creados, 
        key= lambda p: p.getLlegada() 
    )

    pendientes_p = procesos_cola.copy()

    while pendientes_p or cola_listos:
        for proceso in pendientes_p[:]:

            if proceso.getLlegada() <= tiempo:
                cola_listos.append(proceso)
                pendientes_p.remove(proceso)

        if not cola_listos:
            tiempo += 1
            continue

        proceso_actual = cola_listos.popleft()

        if proceso_actual.getEstado_actual() != Estados.EST_LISTO:
            continue

        proceso_actual.cambio_estado(Estados.EST_EJECUCION)

        rafaga_restante = proceso_actual.getRafagaRestante()


        tiempo_eje = min(quantum, rafaga_restante)

        nueva_rafaga = rafaga_restante - tiempo_eje

        rafaga_consumida = (proceso_actual.getRafaga_CPU() + tiempo_eje)

        proceso_actual.rafaga_CPU(rafaga_consumida)
        
        proceso_actual.rafaga_CPU_restante(nueva_rafaga)

        tiempo += tiempo_eje

        if rafaga_restante == 0:
            proceso_actual.finalizacion()

            print(f"Proceso PID {proceso_actual.getPid()} finalizo con un tiempo CT: {tiempo}")

        else:
            proceso_actual.tiempoFinalizado()

            cola_listos.append(proceso_actual)

            print(f"Proceso PID {proceso_actual.getPid()}")
            print(f'regreso a la cola ')
            print(f'Tiempo de rafaga restante {nueva_rafaga}')

    print("\nTodos los procesos han finalizado.")
    print(f"Tiempo total de ejecución: {tiempo}")




def nProcesos():
    print('=======¿Cuántos procesos desea crear?=======')
    cant = int(input(": "))
    for c in range(cant):
        creacion_proceso()
        print(f'Proceso {c+1} Creado')
    print()
    print("====Procesos Creados====== ")



#------------------------------------------> simulación del Deadlock

def accion_liberar(lock, nombre):
    try:
        lock.release()
        print(f"{nombre} liberado por el hilo")
    except RuntimeError: # Captura un error de tiempo de liberación de los recursos de los hilos.
            pass



def proceso_A(pe):
    
    print(f'Proceso {pe.getPid()} Iniciado...')
    recurso_1.acquire()
    print(f"El proceso {pe.getPid()} a retenido el recurso 1.")

    tiempo.sleep(1)
    
    print(f"El proceso {pe.getPid()} a solicitado el recurso 2.")
    recurso_2.acquire()

    if not aboratando:
        print(f"El proceso {pe.getPid()} ha sido RETENIDO.")
    else:
        print(f"El proceso {pe.getPid()} se desbloqueo por el abortaje.")

    

    accion_liberar(recurso_2, "Recurso 2")
    accion_liberar(recurso_1, "Recurso 1")
    

def proceso_B(pe):
    print(f'Proceso {pe.getPid()} Iniciado...')
    recurso_2.acquire()
    print(f"El proceso {pe.getPid()} a retenido el recurso 2.")

    tiempo.sleep(1)
    
    print(f"El proceso {pe.getPid()} a solicitado el recurso 1.")
    recurso_1.acquire()


    print(f"El proceso {pe.getPid()} ha sido RETENIDO.")

    if not aboratando:
        print(f"El proceso {pe.getPid()} ha sido RETENIDO.")
    else:
        print(f"El proceso {pe.getPid()} se desbloqueo por el abortaje.")



    
    accion_liberar(recurso_1, "Recurso 1")
    accion_liberar(recurso_2, "Recurso 2")


def deteccionDeadlock(hilos, timeout):

    final = tiempo.time() + timeout
    while tiempo.time() < final:
        if not any(h.is_alive() for h in hilos): # verifica si todos los procesos han finalizado sin incovenientes
            return True
            tiempo.sleep(0.05)
        
    return not any(h.is_alive() for h in hilos) # caso contrario retorna que al menos hay un deadlock existente


def abortarDeadlock(hilos, locks):

    global aboratando
    aboratando = True
    print("Liberación d elos recursos y Abortaje forzado de los procesos.")
    print()
    for i, lock in enumerate(locks):
        try:
            if lock.locked():
                lock.release()
                print(f"Recurso {i+1} ha sido liberado")
        except TimeoutError: # Captura un error de tiempo de liberación de los recursos de los hilos.
            pass
    for h in hilos:
        h.join(timeout=1.3)

    proc_hilos = [h.name for h in hilos if h.is_alive()]

    if proc_hilos:
        print(f"Los hilos que no ha respondido son: {proc_hilos}")
        print("Serán finalizados al salir del simulador ")
    else:

        
        print(" Todos los hilos de los procesos han finalizado tras el abortaje")





# ------------------------------------------------------------> Main principal

if __name__ == "__main__":
    print()
    print()
    while True:
        print()
        print(f"{"="*5} SIMULADOR DEL NÚCLEO KERNEL EN PYTHON {"="*5}")
        print(f"| Selecciona cualquier opción {" ":<18}|")
        print(f"| Opción 1 -> Creación de procesos. {" ":<12}|")
        print(f"| Opción 2 -> Visualización de procesos creados.|")
        print(f"| Opción 3 -> Paso a la cola de listos. {" ":<8}|")
        print(f"| Opción 4 -> Ejeución en Round Robin. {" ":<9}|")
        print(f"| Opción 8 -> Ejeución en Round Robin. {" ":<9}|")
        print(f"| Opción 9 -> Salir del simulador. {" ":<13}|")



        opcion = int(input("Opción seleccionada: "))

        match opcion:
            case 1:
                os.system("cls")
                nProcesos()

            case 2:
                imprimir_tabla()

            case 3:
                if not Lista_procesos_creados:
                    print()
                    print('-'*10)
                    print("No se han creado procesos hasta el momento")
                    print('-'*10)
                    print()
                else:
                    os.system("cls")
                    cola_listos()

            case 4:
                planificador_Round_Robin()


            case 8:
                pr1 = Lista_procesos_creados.pop(ale.randrange(len(Lista_procesos_creados)))
                pr2 = Lista_procesos_creados.pop(ale.randrange(len(Lista_procesos_creados)))

                pr1.salida()
                pr2.salida()

                hilo_A = hilo.Thread(target=proceso_A, args=(pr1,),daemon=True, name="Hilo-A")
                hilo_B = hilo.Thread(target=proceso_B, args=(pr2,),daemon=True, name="Hilo-B")
                print(f"Espacio disponible de la Memoria: {Memoria.getMemoria_Disponible()} MB\n")
                hilo_A.start()
                hilo_B.start()


                Tiempo_deteccion = 2
                print(f"Tiempo esperado es: {Tiempo_deteccion}s para la detección de deadlocks e interbloqueo")

                if deteccionDeadlock([hilo_A,hilo_B],Tiempo_deteccion):
                    print()
                    print("Los procesos han finalizado sin interbloqueo")
                else:
                    print("="*25)
                    print("Alerta: Interbloqueo (Deadlock) detectado")
                    print("Los procesos A y B se esperan mutuamente.")

                    opcion = str(input("\n ¿Desea abortar los procesos? (s/n): ")).lower()
                    if opcion == 's':
                        print("\n\n\n\n\n\n\n","="*5," LIBERACION DE RECURSOS ","="*5)
                        abortarDeadlock([hilo_A,hilo_B],[recurso_1,recurso_2])
                    else:
                        print("Esperando hasta que los procesos terminen solos...(Nunca pasará)")

                        for h in [hilo_A,hilo_B]:
                            h.join()
            case 9:
                break
                
print(f"{"="*9} HA SALIDO DEL SIMULADOR KERNEL{"="*9}")






#ventana = tk.Tk()
#ventana.title("Simulador de Procesos")
#ventana.geometry("800x450")
#
## Titulo
#tk.Label(
#    ventana,
#    text="Simulador de Procesos",
#    font=("Arial", 16, "bold")
#).pack(pady=10)
#
#
#columnas = ("PID", "Estado", "Memoria", "AT", "BT")
#tabla = ttk.Treeview(
#    ventana,
#    columns=columnas,
#    show="headings",
#    height=10
#)
#
#for columna in columnas:
#    tabla.heading(columna, text=columna)
#    tabla.column(columna, width=130, anchor="center")
#
#tabla.pack(padx=20, pady=10, fill="x")
#
## Contador de procesos
#
#
#Lista_procesos_creados = list()
#Lista_uso_memoria = list()
#pid_reloj = iterar.count(start= 0)
#def creacion_proceso():
#    pass
#    pid = next(pid_reloj)
#    mE = ale.randint(1,5)
#    rafaga = ale.randint(1,10)
#
#
#    nuevo_proceso_memoria = Memoria(pid,mE)
#    if Memoria.getMemoria_Disponible() > nuevo_proceso_memoria.getEspacioMemoriaProceso():
#        nuevo_proceso = Proceso(pid,mE,rafaga)
#        Lista_uso_memoria.append(nuevo_proceso_memoria)
#        Lista_procesos_creados.append(nuevo_proceso)
#
#        
#    tabla.insert(
#         "",
#         "end",
#         values=(pid,"Nuevo",mE,"",rafaga)
#    )
#
#def imprimir_tabla():
#    for proceso, lista_proceso in zip(tabla.get_children(), Lista_procesos_creados):
#        print(tabla.item(proceso)["values"])
#        lista_proceso.salida()
#
#    print("Procesos creados correctamente.")
#    print(f"Memoria disponible: {Memoria.getMemoria_Disponible()} MB")        
#
#tk.Button(
#    ventana,
#    text="Crear proceso",
#    command=creacion_proceso
#).pack(pady=5)
#
#tk.Button(
#    ventana,
#    text="Mostrar tabla en consola",
#    command=imprimir_tabla
#).pack(pady=5)
#
#ventana.mainloop()



import threading as hilo
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
ciclo_reloj = iterar.count(start= 1)

variables_global_compartida = 0
semaforo = hilo.Semaphore(1)


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

    def setliberacionMemoria(self,memoria_liberada: int):
        Memoria.__espacio__memoria_disponible += memoria_liberada

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

    def __init__(self,pid,tamanio_memoria,llegada,rafaga_cpu):
        self.__pid = pid
        self.__estado_actual = Estados.EST_NUEVO
        self.__tamanio_memoria = tamanio_memoria
        self.__rafaga__proceso = rafaga_cpu
        self.__rafaga_cpu = 0
        self.__rafaga_restante = rafaga_cpu
        self.__llegada__AT = llegada
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


    def liberarMemoria(self):

        if self.__bloque__memoria is None:
            return

        self.__bloque__memoria.setEspacioMemoriaProceso(0)
        self.__bloque__memoria = None
        print(f"Memoria del proceso PID: {self.__pid} liberada.")

    def tiempoFinalizado(self):
        pass
        if self.__estado_actual != Estados.EST_EJECUCION:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return
            
        self.cambio_estado(Estados.EST_LISTO)

    def asignarMemoria(self, memoria):
        self.__bloque__memoria = memoria



    def bloqueo(self,cant_memoria: int):

        if self.__estado_actual != Estados.EST_EJECUCION:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return


        diferencia = 0
        if cant_memoria > self.__tamanio_memoria: 
            diferencia = cant_memoria - self.__tamanio_memoria

            if diferencia > Memoria.getMemoria_Disponible():
                print(f"El tamaño de la memoria del proceso PID: {self.__pid} es demasiado grande. El espacio actual de la Memoria es de {diferencia}MB para alojar el proceso. ")
                raise MemoryError("No hay espacio suficiente en la memoria del proceso ")


        self.__bloque__memoria.setEspacioMemoriaProceso(cant_memoria)
        self.cambioTamaño_memoria(cant_memoria)
        self.cambio_estado(Estados.EST_BLOQUEADO)


    def desBloqueo(self):
            if self.__estado_actual != Estados.EST_BLOQUEADO:
                print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
                return
            
            self.cambio_estado(Estados.EST_LISTO)

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
                    self.__bloque__memoria.setliberacionMemoria(self.__tamanio_memoria)
                    print(f"Memoria del proceso PID: {self.__pid} ha sido liberado.")
                    print(f"Espacio disponible de la Memoria: {Memoria.getMemoria_Disponible()} MB\n")
    
            print()    







































#-------->Procesos 
def nProcesos():
#    band = False
#
#    print(f"**¿Que tipo de carga de procesos desea crear?**")
#    print(f'**a. -> Creación de procesos de PID Ordenados.**')
#    print(f'**b. -> Creación de procesos con diferentes llegada AT.**')    
#    print(f'**c. -> Creación de procesos con diferentes teimpo de llegada AT igual a 0.**')
#    opcion = str(input("Opción: "))
#
#    match opcion:
#        case 'a':
#            band = True
            print('=======¿Cuántos procesos desea crear?=======')
            cant = int(input(": "))
            for c in range(cant):
                creacion_proceso()
                print(f'Proceso {c+1} Creado')
            print()
            print("====Procesos Creados====== ")


def creacion_proceso():

        pid = next(pid_reloj)
        mE = ale.randint(2,10)
        rafaga = ale.randint(1,10)


        nuevo_proceso_memoria = Memoria(pid,mE)
        if Memoria.getMemoria_Disponible() > nuevo_proceso_memoria.getEspacioMemoriaProceso():


            llegada = next(ciclo_reloj)
            nuevo_proceso = Proceso(pid,mE,llegada,rafaga)
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
    cola_listos = deque()
    tiempo = 0
    quantum = Quantum
    procesos_cola = sorted(
        Lista_procesos_creados,
        key=lambda p: p.getLlegada()
    )

    pendientes_p = procesos_cola.copy()

    # diccionario para almacenar datos estadísticos de los procesos
    resultados = {}
    for proceso in Lista_procesos_creados:
        resultados[proceso.getPid()] = {
            "AT": proceso.getLlegada(),
            "BT": proceso.getRafagaRestante(),
            "CT": 0,
            "TAT": 0,
            "WT": 0
        }

    while pendientes_p or cola_listos:

        # Agregar procesos que ya llegaron
        for proceso in pendientes_p[:]:
            if proceso.getLlegada() <= tiempo:
                cola_listos.append(proceso)
                pendientes_p.remove(proceso)

        # CPU ociosa
        if not cola_listos:
            tiempo += 1
            continue

        proceso_actual = cola_listos.popleft() #Extrae los procesos en la cola de listas desde la punta externa 

        if proceso_actual.getEstado_actual() != Estados.EST_LISTO:
            continue

        proceso_actual.cambio_estado(Estados.EST_EJECUCION)
        pid = proceso_actual.getPid()

        rafaga_restante = proceso_actual.getRafagaRestante() # Obtiene la ráfaga restante
        
        tiempo_eje = min(quantum, rafaga_restante) # Calcula el tiempo de ejecución del quantum
        nueva_rafaga = rafaga_restante - tiempo_eje #Actualiza a la ráfaga actual del proceso

        rafaga_consumida = (proceso_actual.getRafaga_CPU() + tiempo_eje)  # Actualiza el CPU consumido


        proceso_actual.rafaga_CPU(rafaga_consumida)
        proceso_actual.rafaga_CPU_restante(nueva_rafaga)
        tiempo += tiempo_eje #Avanza el tiempo de reloj

        # Incorpora los procesos que llegaron durante la ejecución
        for proceso in pendientes_p[:]:
            if proceso.getLlegada() <= tiempo:
                cola_listos.append(proceso)
                pendientes_p.remove(proceso)

        # Si el verificador comprueba que si un proceso tiene su rafaga a 0 ha finalizado sus operaciones
        if nueva_rafaga == 0:

            proceso_actual.finalizacion()

            AT = resultados[pid]["AT"]
            BT = resultados[pid]["BT"]

            CT = tiempo
            TAT = CT - AT
            WT = TAT - BT

            resultados[pid]["CT"] = CT
            resultados[pid]["TAT"] = TAT
            resultados[pid]["WT"] = WT

            print(
                f"Proceso PID {pid} finalizado "
                f"con CT: {CT}"
            )

            print(f"TAT: {TAT}")
            print(f"WT: {WT}")
            print("-" * 35)

        else:

            proceso_actual.tiempoFinalizado()

            cola_listos.append(proceso_actual)

            print(f"Proceso PID {pid}")
            print("Regreso a la cola de listos")
            print(f"Rafaga restante: {nueva_rafaga}")
            print("-" * 35)

    # Presentación de resultados
    print("\n========== TABLA ROUND ROBIN ==========")

    print(
        f"{'PID':<8}"
        f"{'AT':<8}"
        f"{'BT':<8}"
        f"{'CT':<8}"
        f"{'TAT':<8}"
        f"{'WT':<8}"
    )

    print("-" * 48)

    total_TAT = 0
    total_WT = 0
    contador = 0

    for pid, datos in sorted(resultados.items()):

        print(
            f"{pid:<8}"
            f"{datos['AT']:<8}"
            f"{datos['BT']:<8}"
            f"{datos['CT']:<8}"
            f"{datos['TAT']:<8}"
            f"{datos['WT']:<8}"
        )

        total_TAT += datos["TAT"]
        total_WT += datos["WT"]
        contador += 1

    print("-" * 48)

    if contador > 0:

        print(
            f"Tiempo promedio TAT: "
            f"{total_TAT / contador:.2f}"
        )

        print(
            f"Tiempo promedio WT: "
            f"{total_WT / contador:.2f}"
        )

    print(f"Tiempo total de ejecución: {tiempo}")
    print("\nTodos los procesos han finalizado.")



def seccion_critica(id):
    global variables_global_compartida

    print("\n","="*15)
    print(f"El hilo {id.getPid()} está solicitando permiso de uso a la variable compartida. ")
    semaforo.acquire() 
    print("\n","="*15)
    try:#el metodo arquire Simula la función wait (Retención)
        
        print("\n","="*15)
        print(f'el hilo {id.getPid()} ha arquirido permiso a la variable compartida. \nProceso {id.getPid()} cambió a estado BLOQUEADO.')
        id.cambio_estado(Estados.EST_BLOQUEADO)
        print("\n","="*15)

        tiempo.sleep(0.05)
        valor_anterior = variables_global_compartida
        variables_global_compartida = valor_anterior + 1

    finally:
        print("\n","="*15)
        print(f'El hilo {id.getPid()} a liberado la variable compartida. \nProceso {id.getPid()} cambió a estado LISTO. ')
        semaforo.release()  
        id.cambio_estado(Estados.EST_LISTO)
        print("\n","="*15)





#------------------------------------------> Simulación del Deadlock

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
        print(f"{"="*9} SIMULADOR DEL NÚCLEO KERNEL EN PYTHON {"="*9}")
        print(f"| Selecciona cualquier opción {" ":<26}|")
        print(f"| Opción 1 -> Creación de procesos. {" ":<20}|")
        print(f"| Opción 2 -> Visualización de procesos creados.{" ":<8}|")
        print(f"| Opción 3 -> Paso a la cola de listos. {" ":<16}|")
        print(f"| Opción 4 -> Ejecución en Round Robin. {" ":<16}|")
        print(f"| Opción 5 -> Simulación del semaforo (Sección crítica).|")
        print(f"| Opción 6 -> Simular interbloqueo (Deadlock). {" ":<9}|")
        print(f"| Opción 7 -> Salir del simulador. {" ":<21}|")



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

            case 5:
                #Nota: para hacer el mecanismo todos los procesos deben estar en esto LISTO.
                hilos = list()
                for pr in Lista_procesos_creados:
                        h = hilo.Thread(target=seccion_critica,args=(pr,))
                        hilos.append(h)
                        h.start()

                print()
                for hi in hilos:
                    hi.join()
                
                print("***Procesos terminados***")
                print(f"Variable compartida: {variables_global_compartida}")
                


            case 6:
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
                        if not hilo_A.is_alive() and not hilo_B.is_alive():
                            pr1.liberarMemoria()
                            pr2.liberarMemoria()
                            print(f"Espacio disponible de la Memoria: {Memoria.getMemoria_Disponible()} MB\n")

                    else:
                        print("Esperando hasta que los procesos terminen solos...(Nunca pasará)")

                        for h in [hilo_A,hilo_B]:
                            h.join()
            case 7:
                break

print(f"Espacio disponible de la Memoria: {Memoria.getMemoria_Disponible()} MB\n")
print(f"{"="*9} HA SALIDO DEL SIMULADOR KERNEL{"="*9}")

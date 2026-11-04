
# Recurso
import sys as sistema
import itertools as iterar
import random as ale
import threading as hilo
import time as tiempo

recurso_1 = hilo.Lock()
recurso_2 = hilo.Lock()


aboratando = False

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






class Estados:
    EST_NUEVO = "Nuevo"
    EST_LISTO = "Listo"
    EST_EJECUCION = "Ejecución"
    EST_BLOQUEADO = "Bloqueado"
    EST_FIN = "Terminado"

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
        self.__bloque__memoria = object

    def getPid(self):
        return self.__pid
        
    def getEstado(self):
        return self.__estado_actual

    def getTamanio_memoria(self):
        return self.__tamanio_memoria

    def getLlegada(self):
            return self.__llegada__AT
    
    def getRafaga_CPU(self):
            return self.__rafaga_cpu
    
    def getRafagaRestante(self):
                return self.__rafaga_restante
        

    def set_Estado(self,est):
         self.__estado_actual = est
    
    def cambio_estado(self,estado):
        self.__estado_actual = estado
    
    def cambioTamaño_memoria(self, memoria: int):
        self.__tamanio_memoria = memoria
    
    
    def rafaga_CPU(self, rafaga: int):
        self.__rafaga_cpu = rafaga
    
    
    def rafaga_CPU_restante(self, rafaga_restante: int):
        self.__rafaga_restante = rafaga_restante

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
                self.__bloque__memoria.setEspacioMemoriaProceso(self.__tamanio_memoria - self.__tamanio_memoria)
                print(f"Memoria del proceso PID: {self.__pid} ha sido liberado.")
                print(f"Espacio disponible de la Memoria: {Memoria.getMemoria_Disponible()} MB\n")
    
            print()    


lista_proceso = []
m1 = Memoria(1,14)
m2 = Memoria(3,15)
p1 = Proceso(1,14,4)
p2 = Proceso(3,15,7)
m3 = Memoria(2,3)
m4 = Memoria(4,5)
p3 = Proceso(2,3,1)
p4 = Proceso(4,5,2)

lista_proceso.append(p1)
lista_proceso.append(p2)
lista_proceso.append(p3)
lista_proceso.append(p4)



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
        if not any(h.is_alive() for h in hilos): # veirifia si todos los procesos han finalizado sin incovenientes
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
         


     
if __name__ == "__main__":
    pr1 = lista_proceso.pop(ale.randrange(len(lista_proceso)))
    pr2 = lista_proceso.pop(ale.randrange(len(lista_proceso)))

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

    print("Fin del programa")
    








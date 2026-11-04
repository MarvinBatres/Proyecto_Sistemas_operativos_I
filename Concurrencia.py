#  Atributos de un Proceso
# PID
# Estado actual
# Contador del programa
# Registro de la CPU  --> diccionario
# Informacion en la memoria ---> tupla
# Recursos   ---> Lista

#prioridad
import itertools as iterar
import threading as hilo
import time as tiempo
from collections import deque

variables_global_compartido = 0

semaforo = hilo.Semaphore(1)

# Recurso
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
    
    def getLlegada(self):
        return self.__llegada__AT

    def getRafaga_CPU(self):
        return self.__rafaga_cpu

    def getRafagaRestante(self):
            return self.__rafaga_restante
    

    def cambio_estado(self,estado):
        self.__estado_actual = estado

    def cambioTamaño_memoria(self, memoria):
        self.__tamanio_memoria = memoria


    def rafaga_CPU(self, rafaga):
        self.__rafaga_cpu = rafaga


    def rafaga_CPU_restante(self, rafaga):
            self.__rafaga_restante = rafaga

    def getEstado(self):
        return self.__estado_actual



    def admicion(self):
        
        if self.__estado_actual == Estados.EST_FIN:
            return
        
        if self.__estado_actual != Estados.EST_NUEVO:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return


        
        if self.__tamanio_memoria > Memoria.getMemoria_Disponible():
            print(f"El tamaño de la memoria del proceso PID: {self.__pid} es demasiado grande para alojarlo dentro de la memoria RAM. La Capacidad Máx de 100 MB comparado a los {self.__tamanio_memoria }MB de tamaño.")
            raise MemoryError("No hay espacio suficiente en la memoria del proceso ")


        self.__bloque__memoria = Memoria(self.__pid,self.__tamanio_memoria)
        self.cambio_estado(Estados.EST_LISTO)




    def validacion_memoria(self):
        if self.__tamanio_memoria > Memoria.getMemoria_Disponible():
            print(f"Proceso [{self.__pid}] Rechazado. requiere un tamaño de memoria: {self.__tamanio_memoria}MB. Pero la memoria RAM solo cuenta con un espacio de {Memoria.getMemoria_Disponible()}MB")
            
            self.cambio_estado(Estados.EST_FIN)
            return False

        return True



    def ejecucion(self,Quantum):
        if self.__estado_actual != Estados.EST_LISTO:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return

        rafaga = self.getRafagaRestante()
        if rafaga >= Quantum:
            rafConsumo = rafaga - Quantum
            rafaga -= rafConsumo
            self.rafaga_CPU(rafaga)
            self.rafaga_CPU_restante(rafConsumo)
        else:
            rafaga -= rafaga
            self.rafaga_CPU(rafaga)
            self.rafaga_CPU_restante(rafaga)

        self.cambio_estado(Estados.EST_EJECUCION)





    def tiempoFinalizado(self):
        if self.__estado_actual != Estados.EST_EJECUCION:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return
            
        self.cambio_estado(Estados.EST_LISTO)

    
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
        print(f"|{'*'*5} Proceso [PID: {self.__pid}] {'*'*5}|")
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

def seccion_critica(id):
    global variables_global_compartido

    print(f"El hilo {id.getPid()} está solicitando permiso de uso a la variable compartida. ")
    semaforo.acquire() 
    try:#el metodo arquire Simula la función wait (Retención)
        
        print(f'el hilo {id.getPid()} ha arquirido permiso a la variable compartida. \nProceso {id.getPid()} cambió a estado BLOQUEADO.')
        id.cambio_estado(Estados.EST_BLOQUEADO)

        tiempo.sleep(0.05)
        valor_anterior = variables_global_compartido
        variables_global_compartido = valor_anterior + 1

    finally:
        print(f'El hilo {id.getPid()} a liberado la variable compartida. \nProceso {id.getPid()} cambió a estado LISTO. ')
        semaforo.release()  
        id.cambio_estado(Estados.EST_LISTO)




if __name__ == "__main__":
    Quantum = 3

    # Crear varios procesos
    procesos = [
        Proceso(pid=101, tamanio_memoria=20, rafaga_cpu=7),
        Proceso(pid=102, tamanio_memoria=25, rafaga_cpu=5),
        Proceso(pid=103, tamanio_memoria=15, rafaga_cpu=8),
    ]

    print("=== INICIANDO SIMULADOR ===")

    for p in procesos:
        p.salida()

    print()
    for p in procesos:
        p.admicion()


    for p in procesos:
        p.salida()
    print()

    hilos = list()
    it = 0
    for pr in procesos:
        h = hilo.Thread(target=seccion_critica,args=(pr,))
        hilos.append(h)
        it += 1
        h.start()

    print()
    for hi in hilos:
        hi.join()

    print("***Procesos terminados***")
    print(f"Variable compartida: {variables_global_compartido}")
#Estructura de control





#Progresos a mejorar: agregar metodos y enum para los cambios de estado.
#Mejoras que agregar 
# 1. agregar un excepcion cuando el proceso se desborde de memoria
## 2. Implementar la versión de round Robin para la planificación de procesos
## 3. los puntos C y D del proyecto.
## 4. Implementar un evento por medio de un botón para la creación del proceso, cambio de estado. 
## 5. La secuencia Lógica va por la mano
## 6. 
#
#
#
#
#
#class Semaforo:
#    __semaforo_contador = 5
#    def __init__(self):
#        self.__cola_espera = []
#        self.__valor = 1
#
#    def wait(self, proceso):
#        global variables_global_compartido
#        if self.__valor == 1:
#            # El recurso está libre, el proceso entra
#            self.__valor = 0
#            print(f"Proceso P{proceso.getPid()} ha ENTRADO a la sección crítica.")
#            return True
#        else:
#            # El recurso está ocupado, el proceso se bloquea
#            print(f"Proceso P{proceso.getPid()} intentó entrar, pero está OCUPADO. Enviado a la cola de espera.")
#            proceso.cambio_estado(Estados.EST_BLOQUEADO)
#            self.__cola_espera.append(proceso)
#            return False
#
#    def signal(self, proceso):
#        if len(self.__cola_espera) > 0:
#            # Hay alguien esperando, lo despertamos y le pasamos el recurso
#            proceso_despertado = self.__cola_espera.pop(0)
#            proceso_despertado.cambio_estado(Estados.EST_LISTO)
#            print(f"Semáforo LIBERADO. Proceso P{proceso_despertado.getPid()} ha sido DESPERTADO y vuelve a la cola de listos.")
#            # OJO: El semáforo se queda en 0 porque el recurso pasa directo al despertado
#        else:
#            # Nadie espera, el semáforo queda libre
#            self.__valor = 1
#            print("Semáforo LIBERADO. Recurso disponible.")
##
#        #Proceso(pid=104, tamanio_memoria=30, rafaga_cpu=4),
#        #Proceso(pid=105, tamanio_memoria=10, rafaga_cpu=6)
#
#
#
#           # Mostrar y admitir los procesos
#            for proceso in procesos:
#                print(
#                    f"\n[KERNEL]: Llega P{proceso.getPid()}, "
#                    f"solicita memoria."
#                )
#        
#                if proceso.validacion_memoria():
#                    proceso.admicion()
#                    proceso.salida()
#                else:
#                    print(
#                        f"[KERNEL]: P{proceso.getPid()} "
#                        "rechazado por falta de memoria."
#                    )
#        
#            # Cola de listos (FIFO)
#        cola_listos = [p for p in procesos if p.getEstado()== Estados.EST_LISTO]
#        
#        # Bucle del planificador
#        while cola_listos:
#            print("\n--- NUEVO TURNO DEL PLANIFICADOR (Round Robin) ---")
#            p1 = cola_listos.pop(0)
#            
#            if mi_semaforo.wait(p1):
#                variables_global_compartido += 1
#                print(f"[SC]: P{p1.getPid()} → var global = {variables_global_compartido}")
#                p1.ejecucion(Quantum)
#                mi_semaforo.signal(p1)
#                
#                if p1.getRafagaRestante() > 0:
#                    p1.cambio_estado(Estados.EST_LISTO)
#                    cola_listos.append(p1)
#                    print(f"[KERNEL]: P{p1.getPid()} no terminó, vuelve a la cola.")
#                else:
#                    p1.finalizacion()
#                    print(f"[KERNEL]: P{p1.getPid()} terminó (FIN).")
#            else:
#                print(f"[KERNEL]: P{p1.getPid()} bloqueado en semáforo.")
#                p1.cambio_estado(Estados.EST_BLOQUEADO)
#                # NO lo reencolamos aquí; en un simulador completo iría a cola_bloqueados
#                # y se despertaría con signal(). Para no congelar la simulación, podrías
#                # hacer un desbloqueo manual como en tu versión original.
#        
#            print("\n=== SIMULACIÓN TERMINADA ===")
#            print(f"Variable global final: {variables_global_compartido}")
#        
#            # ==========================================
#            # 4. FIN DE LA SIMULACIÓN
#            # ==========================================
#            print("\n=== SIMULACIÓN TERMINADA ===")
#            print(f"Variable global compartida final: {variables_global_compartido}")
#            print(f"Memoria RAM disponible final: {Memoria.getMemoria_Disponible()} MB")
#            p1.salida()
#       
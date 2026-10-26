#  Atributos de un Proceso
# PID
# Estado actual
# Contador del programa
# Registro de la CPU  --> diccionario
# Informacion en la memoria ---> tupla
# Recursos   ---> Lista

#prioridad
import itertools as iterar

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
        self.__rafaga_cpu = rafaga_cpu
        self.__rafaga_restante = rafaga_cpu
        self.__llegada__AT = next(self._ciclo_reloj)

    def getPid(self):
            return self.__pid
    
    def getLlegada(self):
        return self.__llegada__AT

    def getRafaga(self):
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




    def admicion(self):
        if self.__estado_actual != Estados.EST_NUEVO:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return
        
        self.cambio_estado(Estados.EST_LISTO)

    def ejecucion(self,Quantum):
        if self.__estado_actual != Estados.EST_LISTO:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return



        
        rafaga = self.__rafaga_cpu
        if rafaga > Quantum:
            rafConsumo = self.__rafaga_cpu - Quantum
            rafaga -= rafConsumo
            self.rafaga_CPU(rafaga)
            self.rafaga_CPU_restante(rafConsumo)
        else:
            rafaga -= rafaga
            self.rafaga_CPU(rafaga)
            self.rafaga_CPU_restante(rafaga)

        self.cambio_estado(Estados.EST_EJECUCION)

    def bloqueo(self,cant_memoria: int):
        if self.__estado_actual != Estados.EST_EJECUCION:
            print(f'No se puede cambiar al estado del proceso: P{self.__pid}.')
            return
        
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
        print(f'|Ráfaga del CPU: {self.__rafaga_cpu:<13}|')
        print(f'|Ráfaga restante: {self.__rafaga_restante:<11} |')
        print("-"*31)
        if self.__estado_actual != Estados.EST_FIN:
            print("                          |                        ")
            print("                          |                        ")
            print("                          v                        ")

        print()

if __name__ == "__main__":
    # 1. Creación del proceso
    Quantum = 3

    p1 = Proceso(10,45,5)
    p1.salida()

    # 2. Cambio de estado
    p1.admicion()
    p1.salida()
    
    p1.ejecucion(Quantum)
    p1.salida()

    p1.bloqueo(76)
    p1.salida()

    p1.desBloqueo()
    p1.salida()

    p1.ejecucion(Quantum)
    p1.salida()

    p1.finalizacion()
    p1.salida()


    

#Progresos a mejorar: agregar metodos y enum para los cambios de estado.
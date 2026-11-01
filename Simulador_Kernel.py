
import tkinter as tk
from tkinter import ttk
import itertools as iterar
import random as ale

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




ventana = tk.Tk()
ventana.title("Simulador de Procesos")
ventana.geometry("800x450")

# Titulo
tk.Label(
    ventana,
    text="Simulador de Procesos",
    font=("Arial", 16, "bold")
).pack(pady=10)


columnas = ("PID", "Estado", "Memoria", "AT", "BT")
tabla = ttk.Treeview(
    ventana,
    columns=columnas,
    show="headings",
    height=10
)

for columna in columnas:
    tabla.heading(columna, text=columna)
    tabla.column(columna, width=130, anchor="center")

tabla.pack(padx=20, pady=10, fill="x")

# Contador de procesos


Lista_procesos_creados = list()
Lista_uso_memoria = list()
pid_reloj = iterar.count(start= 0)
def creacion_proceso():
    pass
    pid = next(pid_reloj)
    mE = ale.randint(1,5)
    rafaga = ale.randint(1,10)


    nuevo_proceso_memoria = Memoria(pid,mE)
    if Memoria.getMemoria_Disponible() > nuevo_proceso_memoria.getEspacioMemoriaProceso():
        nuevo_proceso = Proceso(pid,mE,rafaga)
        Lista_uso_memoria.append(nuevo_proceso_memoria)
        Lista_procesos_creados.append(nuevo_proceso)

        
    tabla.insert(
         "",
         "end",
         values=(pid,"Nuevo",mE,"",rafaga)
    )

def imprimir_tabla():
    for proceso, lista_proceso in zip(tabla.get_children(), Lista_procesos_creados):
        print(tabla.item(proceso)["values"])
        lista_proceso.salida()

    print("Procesos creados correctamente.")
    print(f"Memoria disponible: {Memoria.getMemoria_Disponible()} MB")        

tk.Button(
    ventana,
    text="Crear proceso",
    command=creacion_proceso
).pack(pady=5)

tk.Button(
    ventana,
    text="Mostrar tabla en consola",
    command=imprimir_tabla
).pack(pady=5)

ventana.mainloop()

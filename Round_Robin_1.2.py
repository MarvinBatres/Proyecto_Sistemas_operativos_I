class Round_Robin:
    
    def __init__(self, Quantum):
        self.__quantum = Quantum
        self.__cola__procesos = list()
        self.__proceso = ""
        self.__llegada_AT = 0
        self.__rafaga_BT = 0
        self.__tiempo_finalizacion_CT = 0
        self.__tiempo_respuesta_TAT = 0
        self.__tiempo_espera_WT = 0
        self.__contador_tiempo = 0

    def cola(self,proceso,llegada,rafaga):
        self.__proceso = proceso
        self.__llegada_AT = llegada
        self.__rafaga_BT = rafaga
        self.__cola__procesos.append([self.__proceso,self.__llegada_AT,self.__rafaga_BT])

    # Método de verificación si la cola esta vacia
    def vacio(self):
        return len(self.__cola__procesos) == 0

    def salida(self):
        return self.__cola__procesos

    def getTiempo_finalizacion_CT(self):
            return self.__tiempo_finalizacion_CT

    def getTiempo_respuesta_TAT(self):
            return self.__tiempo_respuesta_TAT
    
    def getTiempo_espera_WT(self,rafaga_bt: int):
        return self.__tiempo_espera_WT - rafaga_bt
        
    def tiempo_total_rafaga(self):
        return self.__contador_tiempo

    def movimiento(self):
        rafaga_consumo = 0
        if not self.vacio():
            elemento_cola = self.__cola__procesos.pop(0)

            proceso = elemento_cola[0]
            llegada = elemento_cola[1]
            rafaga = elemento_cola[2]

            if rafaga > self.__quantum:
                
                self.__contador_tiempo += self.__quantum
                rafaga -= self.__quantum
                rafaga_consumo = self.__quantum
                rafaga_restante = rafaga
                self.cola(proceso,llegada, rafaga)

                return proceso, elemento_cola[2], rafaga_consumo,rafaga_restante

            else:
                self.__contador_tiempo += rafaga

                rafaga_consumo = rafaga
                rafaga_restante = 0
                
                self.__tiempo_finalizacion_CT = self.__contador_tiempo
                self.__tiempo_respuesta_TAT = self.getTiempo_finalizacion_CT() - llegada
                self.__tiempo_espera_WT = self.getTiempo_respuesta_TAT()

                return proceso, elemento_cola[2], rafaga_consumo,rafaga_restante
            
        else:
            return None


#Indices: [0] = proceso; [1] = AT; [2] = BT
#cantProcesos = int(input("Cuantos procesos va a agregar: "))
Procesos = [ ["P1", 0, 3],
    ["P2", 1, 2],
    ["P3", 3, 5],
            
            ]

Quantum = 3
robin = Round_Robin(Quantum)

for pr in Procesos:
     robin.cola(pr[0],pr[1],pr[2])
#Nombre del proceso y su tiempo de ráfaga


#Impresion
def procesoMoldeados(robin: Round_Robin):
    
    cola = robin.salida()
    cola_proceso_x_rafaga = list()    
    for col in cola:
        proceso = col[0]
        llegada = col[1]
        rafaga = col[2]

        print("Proceso: ",proceso)
        print("Tiempo de llegada: (AT)", llegada)
        print("Ráfaga (BT): ", rafaga)
        cola_proceso_x_rafaga.append([proceso,llegada,rafaga])
        print("-"*25)
    print()

    Lista_procesos_ejecutados = list()
    
    while not robin.vacio():

        proceso_actual, rafaga, rafaga_consumida, rafaga_restante = robin.movimiento()
        print("Proceso: ", proceso_actual)
        print("Tamaño Actual de Ráfaga: ", rafaga)
        print("Ráfaga consumida: ",rafaga_consumida)
        print("Ráfaga restante: ",rafaga_restante)
        if rafaga_restante == 0:
            WT = 0
            llegada_proceso = 0
            rafaga_p = 0
            for p in cola_proceso_x_rafaga:
                if proceso_actual in p:
                    llegada_proceso = p[1]
                    rafaga_p = p[2]
                
            CT = robin.getTiempo_finalizacion_CT()
            TAT = robin.getTiempo_respuesta_TAT()
            WT = robin.getTiempo_espera_WT(rafaga_p)

            print("Tiempo de finalización (CT): ", CT)
            print("Tiempo de respuesta (TAT): ", TAT)
            print("Tiempo de espera (WT): ", WT)
            print("****Proceso: ", proceso_actual," finalizado****")

            Lista_procesos_ejecutados.append([proceso_actual, llegada_proceso,rafaga_p,CT,TAT,WT])
            print()
        print()

    return Lista_procesos_ejecutados


def presentacion(pre: list):
    pre.sort(key = lambda x: x[0])
    tiempo_promedio_respuesta = 0
    tiempo_promedio_espera = 0
    cont = 0
    print("-"*75)
    print(f'|{'Procesos':<8} | {'Tiempo AT':<5} | {'Ráfaga BT':<5} | {'Tiempo CT':<5} | {'Tiempo TAT':<5} | {'Tiempo WT':<5} |')
    print("-"*75)
    for iterar in pre:
        print(f"| {iterar[0]:<8} | {iterar[1]:<8} | {iterar[2]:<9} | {iterar[3]:<9} | {iterar[4]:<10} | {iterar[5]:<10} |")
        cont+= 1
        tiempo_promedio_respuesta += iterar[4]
        tiempo_promedio_espera += iterar[5]
    print("-"*75)
    print(f"Tiempo total de la ejecución de los procesos: ", robin.tiempo_total_rafaga()," unidades")
    print(f"tiempo promedio de respuesta: {tiempo_promedio_respuesta/cont:.2f} unidades")
    print(f"Tiempo promedio de espera: {tiempo_promedio_espera/cont:.2f} unidades")
    

pre = procesoMoldeados(robin)
presentacion(pre)
print()

# Nota : Realizar una función de verificación si un proceso llega con Ociosidad en la CPU

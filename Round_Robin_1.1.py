
class Round_Robin:

    
    __proceso = ""
    __llegada_AT = 0
    __rafaga_BT = 0
    __tiempo_finalizacion_CT = 0
    __tiempo_respuesta_TAT = 0
    __tiempo_espera_wt = 0

    def __init__(self, Quantum):
        self.__quantum = Quantum
        self.__cola__procesos = list()
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
    
    def getTiempo_CT(self):
        return self.__tiempo_finalizacion_CT
    
    def getLlegada(self):
        if not self.vacio():
            return self.__cola__procesos[0]
        return None

    
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
                self.__tiempo_finalizacion_CT = self.__contador_tiempo
                self.__contador_tiempo += rafaga
                rafaga_consumo = rafaga
                rafaga_restante = 0
                return proceso, elemento_cola[2], rafaga_consumo,rafaga_restante


            
        else:
            return None






#Indices: [0] = proceso; [1] = AT; [2] = BT
#cantProcesos = int(input("Cuantos procesos va a agregar: "))

Procesos = [ ["P1",0,9],
            ["P2",2,2],
            ["P3",4,5]]

Quantum = 4
robin = Round_Robin(Quantum)

for pr in Procesos:
     robin.cola(pr[0],pr[1],pr[2])
#Nombre del proceso y su tiempo de ráfaga


#Impresion

def procesoMoldeados(robin: Round_Robin):
    
    cola = robin.salida()    
    for col in cola:
        proceso = col[0]
        llegada = col[1]
        rafaga = col[2]

        print("Proceso: ",proceso)
        print("Tiempo de llegada: (AT)", llegada)
        print("Ráfaga (BT): ", rafaga)
        
        print("-"*25)
    print()


    while not robin.vacio():
        proceso_actual, rafaga, rafaga_consumida, rafaga_restante = robin.movimiento()
        print("Proceso: ", proceso_actual)
        print("Tamaño Actual de Ráfaga: ", rafaga)
        print("Ráfaga consumida: ",rafaga_consumida)
        print("Ráfaga restante: ",rafaga_restante)
        if rafaga_restante == 0:
            print("Tiempo Finalizacion (CT): ",)
            print("****Proceso: ", proceso_actual," finalizado****")
        
        print()

        print()
    




procesoMoldeados(robin)
print()

print("Tiempo total de la ejecución de los procesos: ", robin.tiempo_total_rafaga())

#Progresos realizados:
#Calculos de las rafagas 
#Impresion de los procesos









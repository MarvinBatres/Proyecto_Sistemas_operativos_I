
class Round_Robin:
    
    def __init__(self, Quantum):
        self.__quantum = Quantum
        self.__cola__procesos = []
        self.__contador_tiempo = 0
   
    def cola(self,proceso):
        self.__cola__procesos.append(proceso)

    # Método de verificación si la cola esta vacia
    def vacio(self):
        return len(self.__cola__procesos) == 0

    def tiempo_total_rafaga(self):
        return self.__contador_tiempo



    def movimientos(self):
        rafaga_consumida = 0
        if not self.vacio():
            elemento_cola = self.__cola__procesos.pop(0)
             
            proceso = elemento_cola[0]
            llegada = proceso["Llegada"]
            rafaga = proceso["Ráfaga"]

            if rafaga > self.__quantum:
                self.__contador_tiempo += self.__quantum
                proceso["Ráfaga"] -= self.__quantum

                rafaga_consumida = self.__quantum

                self.__cola__procesos.append([proceso])
                return proceso["Proceso"], llegada, rafaga, rafaga_consumida, proceso["Ráfaga"]
            
            else:

                self.__contador_tiempo += rafaga
                rafaga_consumida = rafaga

                proceso["Ráfaga"] -= proceso["Ráfaga"]
                return proceso["Proceso"], llegada, rafaga_consumida, rafaga_consumida, proceso["Ráfaga"]


        else:
            return None
            
            
            
        
Quantum = 4
round = Round_Robin(Quantum)
#Nombre del proceso y su tiempo de ráfaga

round.cola([{"Proceso": "P1","Llegada": 0,"Ráfaga":9}])
round.cola([{"Proceso": "P2","Llegada": 2,"Ráfaga":2}])
round.cola([{"Proceso": "P3","Llegada": 4,"Ráfaga":5}])

while not round.vacio():
    proceso,llegada,rafaga,rafaga_consumida, rafaga_restante = round.movimientos()
    print("Proceso: ", proceso)
    print("Tamaño Actual de Ráfaga: ", rafaga)
    print("Ráfaga consumida: ",rafaga_consumida)
    print("Ráfaga restante: ",rafaga_restante)
    print()

print("Tiempo total de la ejecución de los procesos: ",round.tiempo_total_rafaga())

















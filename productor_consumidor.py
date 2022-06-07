from multiprocessing import Process, Semaphore, BoundedSemaphore, current_process, Value, Array
from random import randint

N= 10 #Numero de productores
K = 5 #Numero de procesos


def p(storage, index, empty, non_empty):  
#Los productores crean los números, cuando el proceso acaba ponemos -1
	produced = []
	for n in range(N):
		empty[index].acquire()
		dato = randint(0, 9)
		dato = dato + storage[index]
		storage[index] = dato
		produced.append(dato)
		non_empty[index].release()
	empty[index].acquire()
	storage[index] = -1
	non_empty[index].release()
	print("P", index, produced)

def c(storage, empty, non_empty, merged):
 #Los consumidores toman los números de aquellas listas no vacias
	for i in range(K):
		non_empty[i].acquire()
 #Tomamos el menor de los números de los productores que han terminado de producir		
	while list(storage) != [-1]*K:
		minimo = float("inf")
		index = -1
		for i in range(K):
			if storage[i] != -1 and storage[i] < minimo:
				index = i
				minimo = storage[i]
 #Juntamos los numeros en una unica lista			
		merged.append(minimo)
		empty[index].release()
		non_empty[index].acquire()
	
	print("Resultado: ", merged, flush = True)


def main():
	storage = Array("i", K)
	merged = []
	for k in range(K):
		storage[k] = 0
	
	non_empty = [Semaphore(0) for k in range(K)]
	empty = [BoundedSemaphore(1) for k in range(K)]
	#Lista de productores
	productores = [Process(target = p, args = (storage, index, empty, non_empty)) for index in range(K)]
	#Consumidor único
	consumidores = Process(target = c, args = (storage, empty, non_empty, merged))
	
	for j in productores:
		j.start()
	consumidores.start()
	
	for j in productores:
		j.join()
	consumidores.join()


if __name__ == "__main__":
	main()
	


# Pedimos la cantidad de números a mostrar
limite = int(input("Ingrese la cantidad de términos de la serie de Fibonacci a generar: "))

# Valores iniciales por defecto
a = 0
b = 1

print("Serie de Fibonacci:")

# Ciclo iterativo estándar
for i in range(limite):
    # Imprimimos el valor actual de 'a', usando end=" " para que no salte de línea
    print(a, end=" ")
    
    # Se calcula el siguiente número sumando los dos anteriores
    siguiente = a + b
    
    # Se actualizan los valores para la siguiente iteración
    a = b
    b = siguiente
    
print() # Salto de línea al final para que la terminal se vea ordenada

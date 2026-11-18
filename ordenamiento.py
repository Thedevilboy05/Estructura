# ==========================================
# Alumno: Christian Correa Basto
# Grupo: 1SC
# Asignatura: Unidad 5 - Métodos de Ordenamiento (ADA1)
# ==========================================

def ordenamiento_burbuja(arr):
    """Método de Ordenamiento Burbuja"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def ordenamiento_insercion(arr):
    """Método de Ordenamiento por Inserción"""
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and clave < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
    return arr

def ordenamiento_seleccion(arr):
    """Método de Ordenamiento por Selección"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def main():
    while True:
        print("\n==========================================")
        print("     ADA1 - MÉTODOS DE ORDENAMIENTO       ")
        print("==========================================")
        print("1. Método Burbuja")
        print("2. Método por Inserción")
        print("3. Método por Selección")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ")
        
        if opcion == '4':
            print("¡Saliendo del programa. Éxito con tu tarea de GitHub!")
            break
            
        if opcion in ['1', '2', '3']:
            try:
                entrada = input("Ingresa los números separados por espacios (ej. 64 34 25 12 22 11 90): ")
                lista_original = [int(x) for x in entrada.split()]
                
                if not lista_original:
                    print("La lista está vacía. Intenta de nuevo.")
                    continue
                
                # Creamos una copia para no alterar la referencia original en impresiones si se desea
                lista = list(lista_original)
                
                print(f"\nLista original: {lista}")
                
                if opcion == '1':
                    resultado = ordenamiento_burbuja(lista)
                    print(f"Lista ordenada por **Burbuja**: {resultado}")
                elif opcion == '2':
                    resultado = ordenamiento_insercion(lista)
                    print(f"Lista ordenada por **Inserción**: {resultado}")
                elif opcion == '3':
                    resultado = ordenamiento_seleccion(lista)
                    print(f"Lista ordenada por **Selección**: {resultado}")
                    
            except ValueError:
                print("Error: Por favor ingresa únicamente números enteros separados por espacios.")
        else:
            print("Opción no válida. Por favor elige un número entre 1 y 4.")

if __name__ == "__main__":
    main()

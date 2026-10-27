class Nodo:
    """Clase que representa un nodo individual."""
    def __init__(self, info):
        self.info = info
        self.liga = None

class ListaSimplementeLigada:
    def __init__(self):
        self.P = None
        # Registro auxiliar para rastrear todos los nodos creados en memoria
        # Esto permite enlazarlos aunque queden fuera de la ruta principal (P)
        self.nodos_creados = {} 

    def _registrar_nodo(self, nodo):
        """Guarda el nodo en el registro interno."""
        self.nodos_creados[nodo.info] = nodo

    # =============================================================
    # CREACIÓN DE LISTAS
    # =============================================================
    def crear_inicio(self):
        print("\n--- Creando nueva lista al INICIO ---")
        dato = input("Ingrese el dato para el primer nodo: ")
        self.P = Nodo(dato)
        self._registrar_nodo(self.P)
        
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0\nRespuesta: "))
        while res == 1:
            dato = input("Ingrese el dato para el nuevo nodo: ")
            nuevo = Nodo(dato)
            self._registrar_nodo(nuevo)
            nuevo.liga = self.P
            self.P = nuevo
            res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0\nRespuesta: "))
        print("✓ Lista creada con éxito.")

    def crear_final(self):
        print("\n--- Creando nueva lista al FINAL ---")
        dato = input("Ingrese el dato para el primer nodo: ")
        self.P = Nodo(dato)
        self._registrar_nodo(self.P)
        T = self.P
        
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0\nRespuesta: "))
        while res == 1:
            dato = input("Ingrese el dato para el nuevo nodo: ")
            nuevo = Nodo(dato)
            self._registrar_nodo(nuevo)
            T.liga = nuevo
            T = nuevo
            res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0\nRespuesta: "))
        print("✓ Lista creada con éxito.")

    # =============================================================
    # NUEVA FUNCIÓN: CONVERGENCIA MULTIPLE (GRAFO)
    # =============================================================
    def crear_convergencia(self):
        """Permite que múltiples nodos apunten a un mismo nodo destino."""
        if not self.nodos_creados:
            print("\n-> ¡No hay nodos creados aún! Agrega elementos primero.")
            return

        print("\n--- Configurar Convergencia de Nodos ---")
        destino_dato = input("Ingresa el DATO del nodo DESTINO (el que recibirá las conexiones): ")
        
        if destino_dato not in self.nodos_creados:
            print(f"✗ El nodo destino '{destino_dato}' no existe en memoria.")
            return
            
        destino = self.nodos_creados[destino_dato]

        try:
            cantidad = int(input(f"¿Cuántos nodos quieres que apunten a [{destino_dato}]? (Ej: 2, 3): "))
        except ValueError:
            print("✗ Por favor, ingresa un número válido.")
            return

        for i in range(cantidad):
            origen_dato = input(f"  -> Ingresa el DATO del nodo ORIGEN {i+1}: ")
            if origen_dato in self.nodos_creados:
                origen = self.nodos_creados[origen_dato]
                origen.liga = destino
                print(f"     ✓ Enlace creado: [{origen.info}] apunta ahora a [{destino.info}]")
            else:
                print(f"     ✗ Nodo '{origen_dato}' no encontrado. Enlace fallido.")

    def ver_todas_las_conexiones(self):
        """Muestra a dónde apunta cada nodo en memoria (ideal para ver convergencias)."""
        print("\n-> ESTADO REAL DE TODAS LAS CONEXIONES (Modo Grafo):")
        if not self.nodos_creados:
            print("   No hay nodos en memoria.")
            return
            
        for dato, nodo in self.nodos_creados.items():
            apunta_a = nodo.liga.info if nodo.liga is not None else "NIL"
            print(f"   Nodo [{dato}]  ---->  [{apunta_a}]")

    # =============================================================
    # OPERACIONES BÁSICAS ACTUALIZADAS
    # =============================================================
    def recorrido_iterativo(self):
        if self.P is None:
            print("\n-> La lista principal está vacía.")
            return

        actual = self.P
        visitados = set() # Protege contra bucles infinitos si enlazas un nodo hacia atrás
        print("\n-> Recorrido de la ruta principal (Desde P):")
        
        while actual is not None:
            if actual in visitados:
                print(f" [Bucle circular hacia: {actual.info}]")
                return
            print(f"[{actual.info}]", end=" -> ", flush=True)
            visitados.add(actual)
            actual = actual.liga
        print("NIL")

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        self._registrar_nodo(nuevo)
        nuevo.liga = self.P
        self.P = nuevo

    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        self._registrar_nodo(nuevo)
        if self.P is None:
            self.P = nuevo
            return
        actual = self.P
        while actual.liga is not None:
            actual = actual.liga
        actual.liga = nuevo

    def buscar(self, dato):
        actual = self.P
        posicion = 1
        while actual is not None:
            if actual.info == dato:
                print(f"\n✓ Elemento '{dato}' ENCONTRADO en la ruta principal.")
                return actual
            actual = actual.liga
            posicion += 1
        
        if dato in self.nodos_creados:
            print(f"\n! Elemento '{dato}' existe en memoria, pero quedó DESCONECTADO de la ruta principal.")
        else:
            print(f"\n✗ Elemento '{dato}' NO encontrado.")
        return None

    def borrado(self, dato):
        if self.P is None:
            print("\n-> La lista está vacía.")
            return False

        if self.P.info == dato:
            self.P = self.P.liga
            if dato in self.nodos_creados: del self.nodos_creados[dato]
            print(f"\n✓ Elemento '{dato}' borrado correctamente.")
            return True

        actual = self.P
        anterior = None
        while actual is not None and actual.info != dato:
            anterior = actual
            actual = actual.liga

        if actual is None:
            print(f"\n✗ No se pudo borrar: '{dato}' no está en la ruta principal.")
            return False

        anterior.liga = actual.liga
        if dato in self.nodos_creados: del self.nodos_creados[dato]
        print(f"\n✓ Elemento '{dato}' borrado correctamente.")
        return True

# =============================================================
# MENÚ INTERACTIVO
# =============================================================
def menu_interactivo():
    lista = ListaSimplementeLigada()
    
    while True:
        print("\n" + "="*60)
        print("  MENÚ AVANZADO: LISTAS Y ENLACES MANUALES")
        print("="*60)
        print("1. Crear lista al inicio")
        print("2. Crear lista al final")
        print("3. Recorrido iterativo de la ruta principal")
        print("4. Inserción rápida al inicio")
        print("5. Inserción rápida al final")
        print("6. Búsqueda")
        print("7. Borrado")
        print("-" * 60)
        print("8. CONECTAR VARIOS NODOS A UNO SOLO (Crear Convergencia)")
        print("9. Ver estado de TODAS las conexiones reales")
        print("10. Salir")
        print("="*60)
        
        opcion = input("Elige una opción (1-10): ")
        
        if opcion == '1': lista.crear_inicio()
        elif opcion == '2': lista.crear_final()
        elif opcion == '3': lista.recorrido_iterativo()
        elif opcion == '4':
            dato = input("\nIngresa el dato: ")
            lista.insertar_inicio(dato)
            print(f"✓ '{dato}' insertado.")
        elif opcion == '5':
            dato = input("\nIngresa el dato: ")
            lista.insertar_final(dato)
            print(f"✓ '{dato}' insertado.")
        elif opcion == '6': lista.buscar(input("\nBuscar dato: "))
        elif opcion == '7': lista.borrado(input("\nBorrar dato: "))
        elif opcion == '8': lista.crear_convergencia()
        elif opcion == '9': lista.ver_todas_las_conexiones()
        elif opcion == '10':
            print("\nSaliendo del programa...")
            break
        else:
            print("\n✗ Opción no válida.")
            
        if opcion != '10':
            input("\n[Presiona ENTER para continuar...]")

if __name__ == "__main__":
    menu_interactivo()

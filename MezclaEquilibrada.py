"""
ADA3 - MetOrdenaExt | Unidad 5 - Métodos de Ordenamiento
EJERCICIO 3: MEZCLA EQUILIBRADA
---------------------------------------------------------------------
Problema: "Registro de ventas de una tienda". El archivo de ventas llega
desordenado y se necesita ordenarlo por folio usando solo archivos
(ordenamiento externo), como si no cupiera en memoria.

Método: Mezcla Equilibrada (balanced merge). Se usan 2K archivos
auxiliares: K archivos de ENTRADA y K archivos de SALIDA (aquí K = 3,
es decir, mezcla de 3 caminos con 6 archivos). Pasos:
  1) DISTRIBUCIÓN INICIAL: el archivo original se reparte, tramo por
     tramo (un tramo es una secuencia que ya viene ordenada), entre los
     K archivos de entrada, uno a uno de forma cíclica.
  2) MEZCLA: se toma un tramo de cada archivo de entrada, se mezclan en
     un solo tramo más grande y se escribe en un archivo de salida;
     el siguiente tramo mezclado va al siguiente archivo de salida
     (así las salidas quedan "equilibradas").
  3) Los archivos de entrada y salida INTERCAMBIAN sus papeles y se
     repite hasta que todo queda en un único tramo ordenado.
Al mezclar K tramos a la vez se necesitan menos pasadas que con
Mezcla Directa (log_K en lugar de log_2).

Formato de cada línea:  folio,producto,monto
"""
import os
import random

K = 3  # número de caminos (archivos de entrada = archivos de salida)
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_mezcla_equilibrada")
PRODUCTOS = ["Refresco", "Pan", "Leche", "Huevo", "Arroz", "Frijol",
             "Aceite", "Galletas", "Jabón", "Cereal"]


def clave(linea):
    return int(linea.split(",")[0])


def generar_ventas(ruta, cantidad, semilla):
    """Crea un archivo de ventas DESORDENADO."""
    azar = random.Random(semilla)
    folios = azar.sample(range(5000, 6000), cantidad)
    with open(ruta, "w", encoding="utf-8") as f:
        for fol in folios:
            f.write(f"{fol},{azar.choice(PRODUCTOS)},{azar.randint(10, 500)}\n")


class Lector:
    """Lee un archivo línea por línea y detecta dónde termina cada tramo ordenado."""

    def __init__(self, ruta):
        self.f = open(ruta, encoding="utf-8")
        self.actual = self.f.readline()      # '' cuando se acaba el archivo
        self.en_tramo = False                # ¿sigue dentro del tramo que se está mezclando?

    def iniciar_tramo(self):
        self.en_tramo = bool(self.actual)

    def tomar(self):
        """Devuelve la línea actual y avanza; cierra el tramo si el orden se rompe."""
        linea = self.actual
        siguiente = self.f.readline()
        if not siguiente or clave(siguiente) < clave(linea):
            self.en_tramo = False            # fin del tramo
        self.actual = siguiente
        return linea

    def cerrar(self):
        self.f.close()


def distribuir_inicial(origen, entradas):
    """Reparte los tramos naturales del origen entre los archivos de entrada (cíclico)."""
    salidas = [open(r, "w", encoding="utf-8") for r in entradas]
    try:
        indice = 0
        anterior = None
        with open(origen, encoding="utf-8") as f:
            for linea in f:
                if anterior is not None and clave(linea) < anterior:
                    indice = (indice + 1) % len(salidas)   # empieza un nuevo tramo
                salidas[indice].write(linea)
                anterior = clave(linea)
    finally:
        for s in salidas:
            s.close()


def mezclar_pasada(entradas, salidas):
    """Una pasada: mezcla tramos de las entradas y los reparte cíclicamente en las salidas."""
    lectores = [Lector(r) for r in entradas]
    archivos_salida = [open(r, "w", encoding="utf-8") for r in salidas]
    try:
        destino = 0
        while any(l.actual for l in lectores):
            for l in lectores:
                l.iniciar_tramo()
            # Mezcla un tramo de cada lector que aún tenga datos
            while any(l.en_tramo for l in lectores):
                activos = [l for l in lectores if l.en_tramo]
                menor = min(activos, key=lambda l: clave(l.actual))
                archivos_salida[destino].write(menor.tomar())
            destino = (destino + 1) % len(archivos_salida)
    finally:
        for l in lectores:
            l.cerrar()
        for a in archivos_salida:
            a.close()


def no_vacios(rutas):
    return [r for r in rutas if os.path.getsize(r) > 0]


def mezcla_equilibrada(ruta, mostrar_pasadas=True):
    """Ordena el archivo 'ruta' (por folio) con Mezcla Equilibrada de K caminos."""
    grupo_a = [os.path.join(CARPETA, f"A{i}.tmp") for i in range(K)]
    grupo_b = [os.path.join(CARPETA, f"B{i}.tmp") for i in range(K)]

    distribuir_inicial(ruta, grupo_a)
    entradas, salidas = grupo_a, grupo_b
    pasada = 0

    # Mientras los datos estén repartidos en más de un archivo, falta mezclar
    while len(no_vacios(entradas)) > 1:
        pasada += 1
        mezclar_pasada(entradas, salidas)
        if mostrar_pasadas:
            print(f"  Pasada {pasada}: mezcla de {K} caminos -> "
                  f"{len(no_vacios(salidas))} archivo(s) con datos")
        entradas, salidas = salidas, entradas   # se intercambian los papeles

    # El único archivo con datos contiene todo el resultado ordenado
    final = no_vacios(entradas)
    with open(ruta, "w", encoding="utf-8") as destino:
        if final:
            with open(final[0], encoding="utf-8") as f:
                destino.write(f.read())

    for tmp in grupo_a + grupo_b:
        if os.path.exists(tmp):
            os.remove(tmp)


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]


def main():
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, "ventas.txt")
    generar_ventas(ruta, 20, semilla=11)

    original = leer(ruta)
    print("=== MEZCLA EQUILIBRADA: ordenar ventas por folio ===\n")
    print("Archivo original (desordenado):")
    for l in original:
        print("  ", l)

    print(f"\nProceso (K = {K} caminos, {2 * K} archivos auxiliares):")
    mezcla_equilibrada(ruta)

    resultado = leer(ruta)
    print("\nArchivo ordenado:")
    for l in resultado:
        print("  ", l)

    esperado = sorted(original, key=clave)
    print("\n¿Resultado correcto?:", "SÍ" if resultado == esperado else "NO")


if __name__ == "__main__":
    main()

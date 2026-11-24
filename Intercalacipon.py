"""
ADA3 - MetOrdenaExt | Unidad 5 - Métodos de Ordenamiento
EJERCICIO 1: INTERCALACIÓN
---------------------------------------------------------------------
Problema: "Inventario general de una papelería con dos sucursales".
Cada sucursal entrega su archivo de inventario YA ORDENADO por clave
de producto. Se necesita un único inventario general, también ordenado.

Método: Intercalación (fusión de dos archivos ordenados en uno solo).
Se leen ambos archivos de forma secuencial, un registro a la vez, y se
escribe siempre el menor de los dos registros actuales. Nunca se carga
un archivo completo en memoria, por eso sirve para archivos enormes.

Formato de cada línea:  clave,producto,existencia,sucursal
"""
import os
import random

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_intercalacion")
PRODUCTOS = ["Cuaderno", "Lápiz", "Pluma", "Regla", "Borrador",
             "Tijeras", "Folder", "Calculadora", "Marcador", "Pegamento"]


def clave(linea):
    """Devuelve la clave numérica (primer campo) de una línea."""
    return int(linea.split(",")[0])


def generar_inventario(ruta, cantidad, sucursal, semilla):
    """Crea un archivo de inventario de prueba ya ordenado por clave."""
    azar = random.Random(semilla)
    claves = sorted(azar.sample(range(1000, 1100), cantidad))
    with open(ruta, "w", encoding="utf-8") as f:
        for c in claves:
            f.write(f"{c},{azar.choice(PRODUCTOS)},{azar.randint(1, 200)},{sucursal}\n")


def intercalar(ruta_a, ruta_b, ruta_salida):
    """Intercala dos archivos ordenados y escribe el resultado en ruta_salida."""
    with open(ruta_a, encoding="utf-8") as a, \
         open(ruta_b, encoding="utf-8") as b, \
         open(ruta_salida, "w", encoding="utf-8") as salida:

        linea_a = a.readline()
        linea_b = b.readline()

        # Mientras ambos archivos tengan registros, se escribe el menor.
        while linea_a and linea_b:
            if clave(linea_a) <= clave(linea_b):
                salida.write(linea_a)
                linea_a = a.readline()
            else:
                salida.write(linea_b)
                linea_b = b.readline()

        # Uno de los archivos se acabó: se copia lo que quede del otro.
        while linea_a:
            salida.write(linea_a)
            linea_a = a.readline()
        while linea_b:
            salida.write(linea_b)
            linea_b = b.readline()


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]


def esta_ordenado(lineas):
    claves = [int(l.split(",")[0]) for l in lineas]
    return all(claves[i] <= claves[i + 1] for i in range(len(claves) - 1))


def main():
    os.makedirs(CARPETA, exist_ok=True)
    ruta_a = os.path.join(CARPETA, "sucursal_a.txt")
    ruta_b = os.path.join(CARPETA, "sucursal_b.txt")
    ruta_total = os.path.join(CARPETA, "inventario_general.txt")

    generar_inventario(ruta_a, 8, "A", semilla=1)
    generar_inventario(ruta_b, 7, "B", semilla=2)

    print("=== INTERCALACIÓN: inventario de dos sucursales ===\n")
    print("Sucursal A (ordenada):")
    for l in leer(ruta_a):
        print("  ", l)
    print("\nSucursal B (ordenada):")
    for l in leer(ruta_b):
        print("  ", l)

    intercalar(ruta_a, ruta_b, ruta_total)

    resultado = leer(ruta_total)
    print("\nInventario general (intercalado):")
    for l in resultado:
        print("  ", l)

    print(f"\nRegistros A: {len(leer(ruta_a))} | B: {len(leer(ruta_b))} "
          f"| Total: {len(resultado)}")
    print("¿Resultado ordenado?:", "SÍ" if esta_ordenado(resultado) else "NO")


if __name__ == "__main__":
    main()

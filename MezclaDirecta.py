"""
ADA3 - MetOrdenaExt | Unidad 5 - Métodos de Ordenamiento
EJERCICIO 2: MEZCLA DIRECTA
---------------------------------------------------------------------
Problema: "Lista de alumnos de una escuela". El archivo de alumnos está
desordenado y se necesita ordenarlo por matrícula sin cargarlo completo
en memoria (ordenamiento externo).

Método: Mezcla Directa. Usa 1 archivo principal y 2 auxiliares y repite
dos fases hasta que todo el archivo queda como un solo tramo ordenado:
  1) DISTRIBUCIÓN: se reparten bloques de tamaño 'tam' de forma
     alternada entre los archivos auxiliares F1 y F2.
  2) MEZCLA: se mezclan los bloques de F1 y F2 (uno de cada archivo)
     y se escriben de nuevo en el archivo principal.
El tamaño del bloque empieza en 1 y se duplica en cada pasada
(1, 2, 4, 8, ...). Se necesitan log2(n) pasadas.

Formato de cada línea:  matricula,nombre,promedio
"""
import os
import random

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_mezcla_directa")
NOMBRES = ["Ana", "Luis", "María", "Carlos", "Sofía", "Jorge", "Elena",
           "Pedro", "Lucía", "Diego", "Valeria", "Mario", "Paula", "Raúl"]


def clave(linea):
    return int(linea.split(",")[0])


def generar_alumnos(ruta, cantidad, semilla):
    """Crea un archivo de alumnos DESORDENADO."""
    azar = random.Random(semilla)
    matriculas = azar.sample(range(2000, 3000), cantidad)
    with open(ruta, "w", encoding="utf-8") as f:
        for m in matriculas:
            f.write(f"{m},{azar.choice(NOMBRES)},{azar.randint(60, 100)}\n")


def contar_lineas(ruta):
    with open(ruta, encoding="utf-8") as f:
        return sum(1 for _ in f)


def distribuir(origen, aux1, aux2, tam):
    """Fase 1: reparte bloques de 'tam' registros alternando entre aux1 y aux2."""
    with open(origen, encoding="utf-8") as f, \
         open(aux1, "w", encoding="utf-8") as f1, \
         open(aux2, "w", encoding="utf-8") as f2:
        destino = f1
        contador = 0
        for linea in f:
            destino.write(linea)
            contador += 1
            if contador == tam:          # bloque completo: cambia de archivo
                destino = f2 if destino is f1 else f1
                contador = 0


def mezclar(aux1, aux2, destino, tam):
    """Fase 2: mezcla un bloque de aux1 con un bloque de aux2, y así sucesivamente."""
    with open(aux1, encoding="utf-8") as f1, \
         open(aux2, encoding="utf-8") as f2, \
         open(destino, "w", encoding="utf-8") as salida:

        l1 = f1.readline()
        l2 = f2.readline()

        while l1 or l2:
            usados1 = 0   # registros ya tomados del bloque actual de F1
            usados2 = 0   # registros ya tomados del bloque actual de F2

            # Mezcla de los dos bloques (cada uno de máximo 'tam' registros)
            while (l1 and usados1 < tam) and (l2 and usados2 < tam):
                if clave(l1) <= clave(l2):
                    salida.write(l1)
                    l1 = f1.readline()
                    usados1 += 1
                else:
                    salida.write(l2)
                    l2 = f2.readline()
                    usados2 += 1

            # Termina de copiar lo que quede de cada bloque
            while l1 and usados1 < tam:
                salida.write(l1)
                l1 = f1.readline()
                usados1 += 1
            while l2 and usados2 < tam:
                salida.write(l2)
                l2 = f2.readline()
                usados2 += 1


def mezcla_directa(ruta, mostrar_pasadas=True):
    """Ordena el archivo 'ruta' (por matrícula) usando Mezcla Directa."""
    aux1 = os.path.join(CARPETA, "aux1.tmp")
    aux2 = os.path.join(CARPETA, "aux2.tmp")
    n = contar_lineas(ruta)
    tam = 1
    pasada = 1
    while tam < n:
        distribuir(ruta, aux1, aux2, tam)
        mezclar(aux1, aux2, ruta, tam)
        if mostrar_pasadas:
            print(f"  Pasada {pasada}: bloques de {tam} registro(s) -> bloques de {tam * 2}")
        tam *= 2
        pasada += 1
    for tmp in (aux1, aux2):
        if os.path.exists(tmp):
            os.remove(tmp)


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]


def main():
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, "alumnos.txt")
    generar_alumnos(ruta, 14, semilla=7)

    original = leer(ruta)
    print("=== MEZCLA DIRECTA: ordenar alumnos por matrícula ===\n")
    print("Archivo original (desordenado):")
    for l in original:
        print("  ", l)

    print("\nProceso:")
    mezcla_directa(ruta)

    resultado = leer(ruta)
    print("\nArchivo ordenado:")
    for l in resultado:
        print("  ", l)

    esperado = sorted(original, key=clave)
    print("\n¿Resultado correcto?:", "SÍ" if resultado == esperado else "NO")


if __name__ == "__main__":
    main()

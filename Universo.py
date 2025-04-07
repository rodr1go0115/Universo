import itertools
import matplotlib.pyplot as plt
import math
import os

def generar_cadenas_binarias(n):
    """Generador de cadenas binarias que no carga todo en memoria"""
    for bits in itertools.product('01', repeat=n):
        yield ''.join(bits)

def guardar_cadenas_archivo(n, filename, max_cadenas_mostrar=100):
    """Guarda una muestra de cadenas y estadísticas completas"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("{\n")
        conteo_total = 0
        conteo_unos = []
        distribucion = {k: 0 for k in range(n+1)}
        
        for i, cadena in enumerate(generar_cadenas_binarias(n)):
            # Guardar muestra de cadenas (solo las primeras y últimas)
            if i < max_cadenas_mostrar or i >= 2**n - max_cadenas_mostrar:
                f.write(f"    '{cadena}',\n")
            
            # Calcular estadísticas
            unos = cadena.count('1')
            conteo_unos.append(unos) if 2**n <= 1_000_000 else None
            distribucion[unos] += 1
            conteo_total += 1
            
            # Mostrar progreso para n grande
            if n > 24 and conteo_total % 10_000_000 == 0:
                print(f"Procesadas {conteo_total} cadenas...")
        
        f.write("}\n")
        f.write(f"\n/* Estadísticas completas para n={n} */\n")
        f.write(f"Total de cadenas: {conteo_total}\n")
        f.write("Distribución de unos:\n")
        for k, v in distribucion.items():
            f.write(f"  - {k} unos: {v} cadenas ({v/conteo_total:.4%})\n")
        
        return conteo_unos if 2**n <= 1_000_000 else None, distribucion

def graficar_resultados(conteo_unos, distribucion, n, filename_prefix):
    """Genera todas las gráficas requeridas"""
    if conteo_unos:  # Solo para n pequeños
        # Gráfica lineal
        plt.figure(figsize=(15, 7))
        plt.plot(conteo_unos, 'b-', alpha=0.5)
        plt.title(f'Número de unos por cadena (n={n})')
        plt.xlabel('Índice de cadena binaria')
        plt.ylabel('Número de unos')
        plt.grid(True)
        plt.savefig(f"{filename_prefix}_lineal.png")
        plt.close()
        
        # Gráfica logarítmica
        plt.figure(figsize=(15, 7))
        plt.plot([math.log(x + 1) for x in conteo_unos], 'r-', alpha=0.5)
        plt.title(f'Logaritmo del número de unos por cadena (n={n})')
        plt.xlabel('Índice de cadena binaria')
        plt.ylabel('ln(Número de unos + 1)')
        plt.grid(True)
        plt.savefig(f"{filename_prefix}_logaritmica.png")
        plt.close()
    
    # Gráfica de distribución (funciona para cualquier n)
    plt.figure(figsize=(15, 7))
    plt.bar(distribucion.keys(), distribucion.values())
    plt.title(f'Distribución teórica de unos (n={n})')
    plt.xlabel('Número de unos')
    plt.ylabel('Cantidad de cadenas')
    plt.grid(True)
    plt.savefig(f"{filename_prefix}_distribucion.png")
    plt.close()

def modo_automatico():
    """Ejecuta el análisis completo para n=29"""
    n = 29
    print(f"\nModo automático: Analizando n={n} (esto puede tomar tiempo)...")
    
    filename = f"cadenas_binarias_n{n}.txt"
    print("Generando y guardando cadenas (muestra) y estadísticas...")
    _, distribucion = guardar_cadenas_archivo(n, filename)
    
    print("Generando gráficas...")
    graficar_resultados(None, distribucion, n, f"resultados_n{n}")
    print(f"¡Análisis completado! Resultados guardados en:")
    print(f"- Archivo de texto: {filename}")
    print(f"- Gráficas: resultados_n{n}_distribucion.png")

def modo_manual():
    """Permite al usuario seleccionar diferentes valores de n"""
    while True:
        try:
            n = int(input("\nLongitud de cadenas binarias (0-1000, 0 para salir): "))
            if n == 0:
                break
            if n < 0 or n > 1000:
                print("Por favor ingrese un valor entre 0 y 1000.")
                continue
            
            filename = f"cadenas_binarias_n{n}.txt"
            print(f"Generando y guardando cadenas para n={n}...")
            conteo_unos, distribucion = guardar_cadenas_archivo(n, filename)
            
            if n <= 20:  # Solo graficar todos los puntos para n pequeños
                print("Generando gráficas detalladas...")
                graficar_resultados(conteo_unos, distribucion, n, f"resultados_n{n}")
                print(f"Gráficas generadas: resultados_n{n}_lineal.png y resultados_n{n}_logaritmica.png")
            else:
                print("Generando gráfica de distribución (para n>20 sólo se genera esta gráfica)...")
                graficar_resultados(None, distribucion, n, f"resultados_n{n}")
                print(f"Gráfica generada: resultados_n{n}_distribucion.png")
            
            print(f"¡Análisis completado! Resultados guardados en {filename}")
            
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número.")

def main():
    print("UNIVERSO DE CADENAS BINARIAS (Σ^n)")
    print("=================================")
    
    while True:
        print("\nMENU PRINCIPAL")
        print("1. Modo automático (n=29)")
        print("2. Modo manual (elige n)")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (1-3): ")
        
        if opcion == '1':
            modo_automatico()
        elif opcion == '2':
            modo_manual()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor seleccione 1, 2 o 3.")

if __name__ == "__main__":
    # Verificar si matplotlib está instalado
    try:
        import matplotlib
    except ImportError:
        print("\n¡Advertencia! matplotlib no está instalado. Las gráficas no se generarán.")
        print("Por favor instálelo con: pip install matplotlib\n")
    
    main()

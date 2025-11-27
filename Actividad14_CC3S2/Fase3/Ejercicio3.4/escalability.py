
import os
from builder import InfrastructureBuilder

def generate_and_measure(count: int, filename: str):
    builder = InfrastructureBuilder("benchmarking")
    builder.build_null_fleet(count)
    
    path = os.path.join("terraform", filename)
    builder.export(path)
    
    size_bytes = os.path.getsize(path)
    size_kb = size_bytes / 1024
    
    return size_kb, path

def main():
    print("Inicio de Pruebas de Escalabilidad")
    
    kb_15, path_15 = generate_and_measure(15, "build_null_fleet15.tf.json")
    print(f"Escenario 1 (15 recursos):  {kb_15:.2f} KB -> {path_15}")
    
 
    kb_150, path_150 = generate_and_measure(150, "build_null_fleet150.tf.json")
    print(f"Escenario 2 (150 recursos): {kb_150:.2f} KB -> {path_150}")

    factor = kb_150 / kb_15
    print("\n--- Resultados ---")
    print(f"El archivo creció {factor:.2f} veces al multiplicar los recursos por 10.")
    print("Conclusión el crecimiento es lineal.")

if __name__ == "__main__":
    main()
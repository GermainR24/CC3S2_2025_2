"""Patrón Builder
Construye de manera fluida configuraciones Terraform locales combinando los patrones Factory, Prototype y Composite.
"""

from typing import Dict, Any
import os
import json

from factory import NullResourceFactory
from composite import CompositeModule
from prototype import ResourcePrototype

class InfrastructureBuilder:
    """Builder fluido que combina los patrones Factory, Prototype y Composite para crear módulos Terraform."""

    def __init__(self, env_name: str) -> None:
        self.env_name = env_name
        self._module = CompositeModule()

    def build_null_fleet(self, count: int = 5) -> "InfrastructureBuilder":
        """Construye una flota de `null_resource` clonados a partir de un prototipo base."""
        base_proto = ResourcePrototype(NullResourceFactory.create("placeholder"))

        for i in range(count):
            def mutator(d: Dict[str, Any], idx=i) -> None:
                res_block = d["resource"][0]["null_resource"][0]
                original_name = next(iter(res_block.keys()))
                new_name = f"{original_name}_{idx}"
                
                res_block[new_name] = res_block.pop(original_name)
                res_block[new_name][0]["triggers"]["index"] = idx

            self._module.add(base_proto.clone(mutator).data)

        return self

    def add_custom_resource(self, name: str, triggers: Dict[str, Any]) -> "InfrastructureBuilder":
        """Agrega un recurso null personalizado."""
        self._module.add(NullResourceFactory.create(name, triggers))
        return self

    def build_group(self, name: str, size: int) -> "InfrastructureBuilder":
        """
        Crea un grupo de recursos aislados y los añade como un sub-módulo.
        """
        base = NullResourceFactory.create(name)
        proto = ResourcePrototype(base)
        
        group = CompositeModule()

        for i in range(size):
            def mut(block):
                res_list = block["resource"][0]["null_resource"]
                res_dict = res_list[0] 
                if name in res_dict:
                    content = res_dict.pop(name)
                    res_dict[f"{name}_{i}"] = content
            group.add(proto.clone(mut).data)

        self._module.add({
            "module": {
                name: group.export() 
            }
        })
        
        return self
    
    def export(self, path: str) -> None:
        """Exporta el módulo compuesto a un archivo JSON."""
        data = self._module.export()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[Builder] JSON generado en: {path}")

def main():
    builder = InfrastructureBuilder("test")

    nombre_prueba = "servidores_web"
    cantidad_prueba = 2
    
    builder.build_group(name=nombre_prueba, size=cantidad_prueba)

    archivo_salida = "terraform/builder_result.tf.json"
    builder.export(archivo_salida)
    
    with open(archivo_salida, "r") as f:
        data = json.load(f)

    try:
        modulo = data["module"][nombre_prueba]
        recursos = modulo["resource"]
        
        print(f"alidación Exitosa: Se encontró el módulo '{nombre_prueba}' con {len(recursos)} recursos dentro.")
        
    except KeyError as e:
        print(f"Error: No se encontró la estructura esperada ({e}).")
if __name__ == "__main__":
    main()

"""Patrón Prototype
Permite clonar objetos Terraform y modificarlos de forma controlada, sin alterar el original.
"""

import copy
import json
from pathlib import Path
from typing import Dict, Any, Callable
from factory import NullResourceFactory

class ResourcePrototype:
    """
    Clase Prototype estándar.
    """
    def __init__(self, resource_dict: Dict[str, Any]) -> None:
        self._resource_dict = resource_dict

    def clone(self, mutator: Callable[[Dict[str, Any]], None] = lambda d: None) -> "ResourcePrototype":
        # Copia profunda (Deep Copy)
        new_dict = copy.deepcopy(self._resource_dict)
        # Aplicar cambios
        mutator(new_dict)
        return ResourcePrototype(new_dict)

    @property
    def data(self) -> Dict[str, Any]:
        return self._resource_dict

def inject_welcome_config(config_tree: Dict[str, Any]) -> None:
    """
    Mutator (Variante Robusta):
    1. Busca dinámicamente el null_resource para inyectar el trigger.
    2. Adjunta la definición del archivo local.
    """

    resources = config_tree.setdefault("resource", [])
    
    found_target = False
    for item in resources:
        if "null_resource" in item:
            for res_name, res_definitions in item["null_resource"][0].items():
                definition = res_definitions[0]
                definition.setdefault("triggers", {})["welcome"] = "¡Hola!"
                found_target = True
                break 
        if found_target:
            break

    file_block = {
        "local_file": [{
            "welcome_file": [{  
                "filename": "${path.module}/bienvenida.txt",
                "content": "Bienvenido"
            }]
        }]
    }
    
    # Agregamos el nuevo bloque a la lista principal
    resources.append(file_block)


def main():
    


    proto = ResourcePrototype(NullResourceFactory.create("app_server"))

    cloned_instance = proto.clone(inject_welcome_config)


    output_dir = Path("terraform")
    output_dir.mkdir(exist_ok=True) 
    
    output_file = output_dir / "welcome.tf.json"
    
    try:
        output_file.write_text(
            json.dumps(cloned_instance.data, indent=2), 
            encoding="utf-8"
        )
        print(f"rchivo generado con exito: {output_file}")
        print("(Contiene 'triggers' modificados y recurso 'local_file')")
        
    except IOError as e:
        print(f"Error escribiendo archivo: {e}")

if __name__ == "__main__":
    main()
"""Patrón Composite
Permite tratar múltiples recursos Terraform como una única unidad lógica o módulo compuesto.
"""

import json
import os
from typing import List, Dict, Any

class CompositeModule:
    """
    Clase que agrega múltiples diccionarios de recursos Terraform como un módulo lógico único.
    Sigue el patrón Composite, donde se unifican estructuras individuales en una sola jerarquía.
    """

    def __init__(self) -> None:
        self._children: List[Dict[str, Any]] = []

    def add(self, block: Dict[str, Any]) -> None:
        """
        Agrega un bloque de configuración (recurso o módulo) al composite.

        Args:
            block: Diccionario que representa un recurso ('resource') o un módulo ('module').
        """
        self._children.append(block)

    def export(self) -> Dict[str, Any]:
        """
        Exporta todos los elementos agregados a un único diccionario maestro.
        Fusiona listas de recursos y diccionarios de módulos.

        Returns:
            Un diccionario con las claves "resource" y/o "module" según corresponda.
        """
        modules = {}
        resources = []
        for child in self._children:
            modules.update(child.get("module", {}))
            resources.extend(child.get("resource", []))

        # Construimos el dict final filtrando lo que este vacio
        return {k: v for k, v in {"module": modules, "resource": resources}.items() if v}

if __name__ == "__main__":
    print("Generando composite_modules.tf.json ...")

    root = CompositeModule()
    
    root.add({
        "module": {
            "network": {"source": "./modules/network", "cidr": "10.0.0.0/16"}
        }
    })
    
    root.add({
        "module": {
            "app": {"source": "./modules/app", "depends_on": ["module.network"]}
        }
    })
    
    output_path = os.path.join("terraform", "composite_modules.tf.json")
    os.makedirs("terraform", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(root.export(), f, indent=2)

    print(f"Archivo creado: {output_path}")
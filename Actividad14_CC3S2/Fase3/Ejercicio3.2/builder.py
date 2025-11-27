"""Patrón Builder
Construye de manera fluida configuraciones Terraform locales combinando los patrones Factory, Prototype y Composite.
"""

from typing import Dict, Any
import os
import json

from factory import NullResourceFactory
from composite import CompositeModule
from prototype import ResourcePrototype
from adapter import MockBucketAdapter
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
        # 1. Crear la base
        base = NullResourceFactory.create(name)
        proto = ResourcePrototype(base)
        
        group = CompositeModule()

        # 3. Llenar el grupo
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
    

    def add_storage_bucket(self, name: str, region: str) -> "InfrastructureBuilder":
        """
        Crea un bucket de almacenamiento usando el patrón Adapter.
        1. Crea un null_resource con Factory.
        2. Lo adapta a mock_cloud_bucket.
        3. Lo agrega al módulo.
        """
        raw_resource = NullResourceFactory.create(name, triggers={"region": region, "type": "standard"})
        
        adapter = MockBucketAdapter(raw_resource)
        bucket_resource = adapter.to_bucket()
        
        self._module.add(bucket_resource)
        
        return self
    
    def export(self, path: str) -> None:
        """Exporta el módulo compuesto a un archivo JSON."""
        data = self._module.export()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[Builder] JSON generado en: {path}")

def main():

    builder = InfrastructureBuilder("adapter_test")
    builder.add_storage_bucket(name="mi_bucket_datos", region="us-east-1")

    output_file = "terraform/adapter_result.tf.json"
    builder.export(output_file)

    # Verificación
    with open(output_file, "r") as f:
        data = json.load(f)

    
    found = False
    resources = data["resource"]
    for item in resources:
        if "mock_cloud_bucket" in item:
            bucket_content = item["mock_cloud_bucket"]["mi_bucket_datos"]
            print(f"Recurso adaptado encontrado: {bucket_content}")
            
            assert bucket_content["tags"]["region"] == "us-east-1"
            assert bucket_content["provider"] == "mock_cloud"
            found = True
            break
            
    if not found:
        print("Error: No se encontró el recurso 'mock_cloud_bucket'.")
    else:
        print("Prueba del Adapter exitosa.")


if __name__ == "__main__":
    main()

"""Patrón Adapter
Permite transformar la interfaz de un objeto en otra interfaz que el cliente espera.
Convierte un 'null_resource' genérico en un 'mock_cloud_bucket' específico.
"""

class MockBucketAdapter:
    def __init__(self, null_block: dict):
        self.null = null_block

    def to_bucket(self) -> dict:
        """
        Adapta (transforma) el null_resource a un recurso 'mock_cloud_bucket'.
        """
        try:
            res_list = self.null["resource"]
            null_res_block = res_list[0]["null_resource"]
            res_dict = null_res_block[0]
            
            name = next(iter(res_dict.keys()))
            triggers = res_dict[name][0]["triggers"]

        except (IndexError, KeyError, TypeError):
            return {}

        return {
            "resource": [{ 
                "mock_cloud_bucket": {
                    name: {
                        "bucket_name": name,
                        "tags": triggers, 
                        "provider": "mock_cloud" 
                    }
                }
            }]
        }
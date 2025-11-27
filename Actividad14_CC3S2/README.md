# Actividad 14

Se implementa patrones de diseño de software (**Singleton, Factory, Prototype, Composite, Builder y Adapter**) aplicados a la generación de infraestructura como código con **Terraform**.

---

## Contenido del Proyecto

El repositorio se divide en tres fases principales que cubren desde el análisis teórico hasta la implementación avanzada y pruebas.

### Fase 1: Análisis y Diseño

Esta carpeta contiene la documentación teórica y visual de los patrones.

- Representaciones visuales (UML) del flujo de datos entre Factory, Prototype, Composite y Builder.
- En la documentacion hay un análisis detallado del funcionamiento teórico de los patrones Singleton, Factory, Prototype, Composite y Builder aplicados a IaC.

### Fase 2: Implementación de Patrones

- **Ejercicio 2.1 (Singleton):** Contiene la clase `ConfigSingleton` que asegura una configuración global única para todo el proyecto.
- **Ejercicio 2.2 (Factory):** Implementación de `NullResourceFactory`, encargada de estandarizar la creación de recursos y generar triggers automáticos (UUID, timestamps).
- **Ejercicio 2.3 (Prototype):** Demostración del patrón Prototype. Incluye el script `prototipe.py` que clona recursos base y aplica mutaciones (como añadir archivos locales), generando el archivo `welcome.tf.json`.
- **Ejercicio 2.4 (Composite):** Implementación de `CompositeModule`. Permite agrupar múltiples recursos y submódulos (network, app) en una sola estructura jerárquica exportable (`composite_modules.tf.json`).
- **Ejercicio 2.5 (Builder):** Contiene la clase `InfrastructureBuilder`, que orquesta todos los patrones anteriores para construir grupos complejos de infraestructura de forma fluida.

### Fase 3: Desafíos Avanzados

Ejercicios complementarios que extienden la funcionalidad base, añaden calidad y métricas.

- **Ejercicio 3.1 (Ensayo Técnico):** Documento comparativo (`factory_vs_prototipe.md`) que analiza cuándo usar Factory vs. Prototype
- **Ejercicio 3.2 (Adapter):** Implementación del patrón Adapter para transformar recursos genéricos en `mock_cloud_bucket`.
- **Ejercicio 3.3 (Testing):** Suite de pruebas automatizadas (`test_patterns.py`) utilizando **pytest** para validar la integridad y aislamiento de los patrones Singleton, Factory y Prototype.
- **Ejercicio 3.4 (Escalabilidad):** Script de análisis (`escalability.py`) que mide y compara el crecimiento del tamaño de los archivos JSON generados (15 vs. 150 recursos)

### 1. Prerrequisitos

- Python 3.8+
- Terraform
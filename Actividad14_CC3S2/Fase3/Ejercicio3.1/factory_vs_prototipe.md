### 3.1 Comparativa: Factory vs Prototype en Infraestructura como Código

En el desarrollo de Infraestructura como Código (IaC), la elección entre el patrón **Factory** y el patrón **Prototype** no es meramente estilística, sino que impacta directamente en el rendimiento de la generación de configuraciones y en la mantenibilidad del código a largo plazo.

### Cuándo elegir cada patrón para IaC,

El patrón **Factory** es ideal cuando necesitamos crear objetos que, aunque comparten una interfaz común, tienen configuraciones internas muy distintas o requieren una lógica de validación compleja antes de existir. Es la opción por defecto para crear recursos heterogéneos (por ejemplo, una fábrica que genera tanto buckets S3 como instancias EC2 basándose en parámetros de entrada).

Por otro lado, el patrón **Prototype** es mejor en escenarios de "escalado horizontal" o flotas. Si necesitamos desplegar 50 servidores web que son idénticos en un 95% (misma imagen, mismas etiquetas, misma red) y solo varían en su nombre o IP, Prototype es superior. Permite definir una "plantilla maestra" compleja una sola vez y replicarla, evitando repetir la lógica de configuración base.

### Costes de serialización profundas vs creación directa

 la diferencia técnica más crítica.

- **Factory (Creación Directa):** Es generalmente más eficiente en memoria para objetos simples. Instanciar un diccionario o clase nueva consume solo los recursos de esa asignación.
- **Prototype (Serialización Profunda):** Depende de operaciones como `deepcopy` en Python. Esto implica recorrer recursivamente todo el grafo de objetos del recurso original, serializarlo y deserializarlo en una nueva ubicación de memoria. Para objetos de configuración muy grandes o profundamente anidados, el coste computacional (CPU) y de memoria del clonado puede superar al de crear el objeto desde cero.

### Mantenimiento

**Factory** centraliza la lógica de creación en un solo punto, lo que facilita aplicar políticas globales (ej. "todos los recursos deben tener tags de coste"). Sin embargo, si los objetos requieren muchos parámetros, los métodos de la fábrica pueden volverse difíciles de manejar. **Prototype** reduce el "boilerplate" (código repetitivo) al permitir configurar un objeto base y olvidarse de los detalles, pero introduce el riesgo de propagar configuraciones erróneas: si el prototipo original tiene un defecto, todos sus clones heredarán el error silenciosamente.
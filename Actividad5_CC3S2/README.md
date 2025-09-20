# Actividad5

### Ejericio 1

El target help muestra una lista de reglas disponibles en el Makefile con  descripcion (como all, build, clean, help). Gracias a la linea `.DEFAULT_GOAL := help`, al ejecutar make sin parametros se ejecuta este target y se muestra la ayuda por defecto. Ademas, la directiva `.PHONY` marca ciertos targets como falsos, para que siempre se ejecuten aunque exista un archivo con el mismo nombre.
 

### Ejercicio 2

En la primera ejecuion de `make build` se genera un `hello.txt` ejecutando el script Python, ya que no existe. En la segunda ejecuion, como `hello.py` no cambio y `hello.txt` ya existia, make detecta que no es necesario rehacerlo y no vuelve a ejecutar el script. Esto pasa porque make compara marcas de tiempo entre archivos; si la salida esta actualizada, no la regenera. Asi nos asegura la idempotencia: repetir el build no hace trabajo extra si no hay cambios

### Ejericcio 3

Las opciones del shell `-e -u -o pipefail` y la directiva `.DELETE_ON_ERROR` protegen el proyecto. `-e` detiene si un comando falla, `-u` marca error si se usa una variable no definida, y `-o pipefail` hace fallar toda la tuberia si cualquier comando falla. `.DELETE_ON_ERROR` borra archivos parciales si ocurre un error. Asi se evita dejar salidas corruptas y se mantiene la integridad del proyecto

### Ejercicio 4

`make -n build` muestra los pasos sin que sean ejecutadas, util para revisar sin cambiar archivos. `make -d build` revela el razonamiento interno, mostrando como compara marcas de tiempo y dependencias: si falta la salida o la fuente es mas reciente, la reconstruye; si todo esta actualizado, omite la accion y evita trabajo extra

### ejercicio 5

Al cambiar la fuente `touch hello.py`, Make ve que es mas reciente que el objetivo y regenera la salida. Si solo se toca el target `touch hello.txt`, no se rehace nada porque la fuente no cambio. Esto muestra la incrementalidad y eficiencia de Make al evitar trabajo innecesario

Ejercicio 6

Si `shellcheck` y `shfmt` estan instalados, generan advertencias en los logs sobre errores, buenas practicas o formato en `scripts/run_tests.sh`, ayudando a mejorar el codigo y evitar fallos. Si no estan instaladas, los logs lo indican. En Linux se pueden instalar con `sudo apt install shellcheck` y `sudo apt install shfmt` para verificar y formatear el codigo en futuras ejecuciones

### Ejercicio 7

Las opciones `--sort=name` y `--numeric-owner` en `tar` ordenan archivos y fijan propietarios, mientras `--mtime='@0'` nos asegura la misma marca de tiempo. Al usar `gzip -n`, no se guarda nombre ni fecha original. Esto hace que el paquete binario sea identico en cada corrida y el hash SHA256 se mantenga igual, garantizando reproducibilidad e integridad en cualquier entorno

## Ejercicio 8

Make requiere que cada linea de una receta comience con un TAB para diferenciar los comandos de las reglas y variables. Si en su lugar se usan espacios, aparece el error **"missing separator"**. Este problema suele resolverse revisando el mensaje y corrigiendo el Makefile.

**Ejercicios:**

- Ejecuta ./scripts/run_tests.sh en un repositorio limpio. Observa las líneas "Demostrando pipefail": primero sin y luego con pipefail. Verifica que imprime "Test pasó" y termina exitosamente con código 0 (`echo $?`).
    
    ![image.png](imagenes/image.png)
    
- Edita src/hello.py para que no imprima "Hello, World!". Ejecuta el script: verás "Test falló", moverá hello.py a hello.py.bak, y el **trap** lo restaurará. Confirma código 2 y ausencia de .bak.
    
    ![image.png](imagenes/image%201.png)
    
- Ejecuta `bash -x scripts/run_tests.sh`. Revisa el trace: expansión de `tmp` y `PY`, llamadas a funciones, here-doc y tuberías. Observa el trap armado al inicio y ejecutándose al final; estado 0.
    
    ![image.png](imagenes/image%202.png)
    
- Sustituye `output=$("$PY" "$script")` por `("$PY" "$script")`. Ejecuta script. `output` queda indefinida; con `set -u`, al referenciarla en `echo` aborta antes de `grep`. El trap limpia y devuelve código distinto no-cero.
    
    ![image.png](imagenes/image%203.png)
    

## Parte 2

- Ejecuta `make -n all` para un dry-run que muestre comandos sin ejecutarlos; identifica expansiones `$@` y `$<`, el orden de objetivos y cómo `all` encadena `tools`, `lint`, `build`, `test`, `package`.
    
    ![image.png](imagenes/image%204.png)
    
- Ejecuta `make -d build` y localiza líneas "Considerando el archivo objetivo" y "Debe deshacerse", explica por qué recompila o no `out/hello.txt` usando marcas de tiempo y cómo `mkdir -p $(@D)` garantiza el directorio.
    
    ![image.png](imagenes/image%205.png)
    

.
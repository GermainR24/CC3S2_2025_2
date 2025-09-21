imagenes/# Actividad4

![image.png](imagenes/image.png)

![image.png](imagenes/image%201.png)

1. Crea la versión redactada (palabras sensibles y pares `clave=valor` / `clave: valor`):
    
    ![image.png](imagenes/image%202.png)
    
2. Oculta credenciales en cabeceras HTTP (Authorization Basic/Bearer):
    
    ![image.png](imagenes/image%203.png)
    
3. (Opcional) Quita códigos de color ANSI:
    
    ![image.png](imagenes/image%204.png)
    
4. Verifica que no queden secretos:
    
    ![image.png](imagenes/image%205.png)
    

# **Sección 1: Manejo sólido de CLI**

**Ejercicios de reforzamiento**

1. Navega a `/etc`, lista archivos ocultos y redirige la salida a un archivo en tu home: `cd /etc; ls -a > ~/etc_lista.txt`.
    
    ![image.png](imagenes/image%206.png)
    
2. Usa globbing para listar todos los archivos en `/tmp` que terminen en `.txt` o `.doc`, y cuenta cuántos hay con una tubería (versión robusta): `find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l`.
    
    ![image.png](imagenes/image%207.png)
    
3. Crea un archivo con `printf "Línea1\nLínea2\n" > test.txt`.
    
    ![image.png](imagenes/image%208.png)
    
4. (Intermedio) Redirige errores de un comando fallido (ej. `ls noexiste`) a un archivo y agrégalo a otro: `ls noexiste 2>> errores.log`. Para borrados con xargs, primero haz un dry-run: `find . -maxdepth 1 -name 'archivo*.txt' | xargs echo rm`.

![image.png](imagenes/image%209.png)

![image.png](imagenes/image%2010.png)

# **Sección 2: Administración básica**

![image.png](imagenes/image%2011.png)

**Ejercicios de reforzamiento**

1. Crea un usuario "devsec" y agrégalo a un grupo "ops". Cambia permisos de un archivo para que solo "devsec" lo lea: `sudo adduser devsec; sudo addgroup ops; sudo usermod -aG ops devsec; touch secreto.txt; sudo chown devsec:ops secreto.txt; sudo chmod 640 secreto.txt` (usa mock si es entorno compartido).
    
    ![image.png](imagenes/image%2012.png)
    
    ![image.png](imagenes/image%2013.png)
    
2. Lista procesos, encuentra el PID de tu shell (`ps aux | grep bash`), y envía una señal SIGTERM (no lo mates si es crítico).
    
    ![image.png](imagenes/image%2014.png)
    
3. Verifica el estado de un servicio como "systemd-logind" con `systemctl status systemd-logind`, y ve sus logs con `journalctl -u systemd-logind -n 10`.
    
    ![image.png](imagenes/image%2015.png)
    
    ## ver logs
    
    ![image.png](imagenes/image%2016.png)
    
4. (Intermedio) Inicia un proceso en background (`sleep 100 &`), lista con `ps`, y mátalo con `kill`.
    
    ![image.png](imagenes/image%2017.png)
    

**Comprobación**

- `namei -l secreto.txt` (verifica permisos y propietario).
- `id devsec` (confirma grupos).
    
    ![image.png](imagenes/image%2018.png)
    

# **Sección 3: Utilidades de texto de Unix**

**Ejercicios de reforzamienDto**

1. Usa grep para buscar "root" en `/etc/passwd`: `grep root /etc/passwd`.
    
    ![image.png](imagenes/image%2019.png)
    
2. Con sed, sustituye "dato1" por "secreto" en datos.txt: `sed 's/dato1/secreto/' datos.txt > nuevo.txt`.
    
    ![image.png](imagenes/image%2020.png)
    
3. Con awk y cut, extrae usuarios de `/etc/passwd`: `awk -F: '{print $1}' /etc/passwd | sort | uniq`.
    
    ![image.png](imagenes/image%2021.png)
    
4. Usa tr para convertir un texto a mayúsculas y tee para guardarlo: `printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt`.
    
    ![image.png](imagenes/image%2022.png)
    
5. (Intermedio) Encuentra archivos en `/tmp` modificados en los últimos 5 días: `find /tmp -mtime -5 -type f`.
    
    ![image.png](imagenes/image%2023.png)
    
6. Pipeline completo: `ls /etc | grep conf | sort | tee lista_conf.txt | wc -l`.
7. (Opcional) Usa tee para auditoría: `grep -Ei 'error|fail' evidencias/sesion.txt | tee evidencias/hallazgos.txt`.
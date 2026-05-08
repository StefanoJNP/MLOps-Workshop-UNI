# Docker - Cheatsheet de Comandos

## Instalacion y verificacion

```bash
docker --version                       # Ver version de Docker
docker info                            # Ver estado del daemon
docker run hello-world                 # Prueba rapida de instalacion
```

---

## Construir imagen del proyecto

```bash
docker build -t concreto-api ./despliegue
```

---

## Ejecutar contenedor

```bash
docker run -p 8000:8000 concreto-api
```

Ejemplo con nombre y en background:

```bash
docker run -d --name concreto-api-dev -p 8000:8000 concreto-api
```

---

## Inspeccion y logs

```bash
docker ps                              # Contenedores activos
docker ps -a                           # Activos + detenidos
docker logs concreto-api-dev           # Ver logs
docker logs -f concreto-api-dev        # Ver logs en tiempo real
docker inspect concreto-api-dev        # Metadata completa (JSON)
```

---

## Entrar al contenedor para depurar

```bash
docker exec -it concreto-api-dev /bin/sh
```

---

## Gestion de imagenes y limpieza

```bash
docker images                           # Listar imagenes locales
docker rmi concreto-api                 # Eliminar imagen por nombre/tag
docker rm concreto-api-dev              # Eliminar contenedor detenido
docker stop concreto-api-dev            # Detener contenedor
docker system prune -f                  # Limpiar recursos no usados
```

---

## Flujo tipico para iterar cambios

```bash
# 1) Reconstruir imagen despues de cambios en app.py o dependencias
docker build -t concreto-api ./despliegue

# 2) Detener y remover contenedor anterior (si existe)
docker stop concreto-api-dev
docker rm concreto-api-dev

# 3) Levantar nueva version
docker run -d --name concreto-api-dev -p 8000:8000 concreto-api

# 4) Revisar logs
docker logs -f concreto-api-dev
```

---

## Troubleshooting (casos reales)

### Caso 1: El contenedor inicia, pero la API no responde en localhost:8000

**Contexto:** `docker ps` muestra el contenedor en estado up, pero al abrir `http://localhost:8000/docs` no carga.

**Comandos para resolver:**

```bash
# 1) Verificar mapeo de puertos
docker ps

# 2) Revisar logs de arranque
docker logs concreto-api-dev

# 3) Confirmar que uvicorn expone 0.0.0.0 (no 127.0.0.1) dentro del contenedor
# Si estaba mal, reconstruir y relanzar
docker build -t concreto-api ./despliegue
docker stop concreto-api-dev
docker rm concreto-api-dev
docker run -d --name concreto-api-dev -p 8000:8000 concreto-api

# 4) Validar endpoint de salud/documentacion
curl http://localhost:8000/docs
```

### Caso 2: Cambiaste codigo, pero Docker sigue ejecutando la version vieja

**Contexto:** Editaste codigo en `despliegue/app.py`, reiniciaste contenedor, pero el comportamiento no cambia.

**Comandos para resolver:**

```bash
# 1) Reconstruir imagen sin cache para forzar capas nuevas
docker build --no-cache -t concreto-api ./despliegue

# 2) Reemplazar contenedor previo
docker stop concreto-api-dev
docker rm concreto-api-dev

# 3) Levantar contenedor con la nueva imagen
docker run -d --name concreto-api-dev -p 8000:8000 concreto-api

# 4) Verificar timestamp/hash de imagen y logs
docker images | head
docker logs -f concreto-api-dev
```

# MLflow - Cheatsheet de Comandos

## Instalacion y arranque local

```bash
pip install mlflow                     # Instalar MLflow
mlflow --version                       # Verificar instalacion
mlflow server --host 127.0.0.1 --port 5000
```

---

## Configuracion del tracking

```bash
# Linux / Mac
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
export MLFLOW_EXPERIMENT=mlops-workshop-uni

# Windows PowerShell
$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
$env:MLFLOW_EXPERIMENT="mlops-workshop-uni"
```

---

## Ejecucion de entrenamiento con tracking

```bash
python src/train.py                    # Ejecuta entrenamiento y registra run
```

> Si el script usa `mlflow.set_experiment`, MLflow crea el experimento automaticamente si no existe.

---

## Interfaz web (UI)

```bash
mlflow ui --host 127.0.0.1 --port 5000
```

Abrir en navegador: `http://127.0.0.1:5000`

---

## Gestion de experimentos y runs (CLI)

```bash
mlflow experiments search              # Listar experimentos
mlflow runs list --experiment-id <id>  # Listar runs por experimento
mlflow runs describe --run-id <run_id> # Ver detalle de un run
```

---

## Registro de modelos

```bash
# Registrar un modelo entrenado desde un run existente
mlflow models register \
  --model-uri "runs:/<run_id>/pipeline_rf" \
  --name "concrete-strength-model"

# Servir un modelo registrado localmente
mlflow models serve \
  --model-uri "models:/concrete-strength-model/latest" \
  --host 127.0.0.1 --port 5001 --no-conda
```

---

## Descarga de artefactos

```bash
mlflow artifacts download \
  --run-id <run_id> \
  --artifact-path "predicho_vs_real.png" \
  --dst-path ./tmp_artifacts
```

---

## Comandos de diagnostico rapido

```bash
mlflow server --help                   # Ver opciones de backend/artifacts
lsof -i :5000                          # Ver proceso usando puerto 5000 (Linux/Mac)
netstat -ano | findstr 5000            # Ver proceso usando puerto 5000 (Windows)
```

---

## Troubleshooting (casos reales)

### Caso 1: El entrenamiento corre, pero no aparece ningun run en la UI

**Contexto:** Ejecutaste `python src/train.py`, no hay error, pero el experimento no se actualiza en `http://127.0.0.1:5000`.

**Comandos para resolver:**

```bash
# 1) Verificar variables de entorno activas
# Linux / Mac
printenv | grep MLFLOW

# Windows PowerShell
Get-ChildItem Env:MLFLOW*

# 2) Forzar tracking local para la sesion actual
# Linux / Mac
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
export MLFLOW_EXPERIMENT=mlops-workshop-uni

# Windows PowerShell
$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
$env:MLFLOW_EXPERIMENT="mlops-workshop-uni"

# 3) Levantar/reiniciar el servidor
mlflow server --host 127.0.0.1 --port 5000

# 4) Re-entrenar
python src/train.py
```

### Caso 2: Error por puerto ocupado al iniciar MLflow

**Contexto:** Al ejecutar `mlflow server --host 127.0.0.1 --port 5000`, aparece error de puerto en uso.

**Comandos para resolver:**

```bash
# Opcion A: identificar y cerrar el proceso que usa el puerto 5000
# Windows
netstat -ano | findstr 5000
taskkill /PID <pid> /F

# Linux / Mac
lsof -i :5000
kill -9 <pid>

# Reiniciar MLflow en el mismo puerto
mlflow server --host 127.0.0.1 --port 5000

# Opcion B: usar otro puerto y actualizar variable
mlflow server --host 127.0.0.1 --port 5001

# Linux / Mac
export MLFLOW_TRACKING_URI=http://127.0.0.1:5001

# Windows PowerShell
$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5001"
```

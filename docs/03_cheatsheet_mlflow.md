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

## API de Python - Funciones de logging

### Configuracion inicial del experimento

```python
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")   # Apuntar al servidor
mlflow.set_experiment("mlops-workshop-uni")         # Crear/seleccionar experimento
```

---

### Estructura basica de un run

```python
with mlflow.start_run(run_name="mi-experimento"):
    # Todo lo que se loguee aqui queda asociado al run
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("rmse", 4.52)
```

> Tambien se puede usar `mlflow.start_run()` / `mlflow.end_run()` sin context manager.

---

### Loguear parametros

```python
# Un parametro a la vez
mlflow.log_param("n_estimators", 100)
mlflow.log_param("max_depth", 5)

# Varios de golpe
mlflow.log_params({
    "n_estimators": 100,
    "max_depth": 5,
    "random_state": 42,
})
```

---

### Loguear metricas

```python
# Una metrica a la vez
mlflow.log_metric("rmse", 4.52)
mlflow.log_metric("r2", 0.87)

# Varias de golpe
mlflow.log_metrics({
    "rmse": 4.52,
    "mae": 3.10,
    "r2": 0.87,
})

# Metrica con step (util para entrenamiento iterativo / epochs)
for epoch, loss in enumerate(losses):
    mlflow.log_metric("loss", loss, step=epoch)
```

---

### Loguear artefactos (archivos)

```python
# Subir un archivo cualquiera
mlflow.log_artifact("reports/metricas.json")

# Subir un archivo en una subcarpeta del run
mlflow.log_artifact("reports/figures/predicho_vs_real.png", artifact_path="plots")

# Subir toda una carpeta
mlflow.log_artifacts("reports/figures/", artifact_path="plots")
```

---

### Loguear imagenes (matplotlib / PIL)

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.set_xlabel("Real")
ax.set_ylabel("Predicho")

# Opcion A: guardar a disco y subir como artefacto
fig.savefig("predicho_vs_real.png")
mlflow.log_artifact("predicho_vs_real.png", artifact_path="plots")

# Opcion B: loguear directamente la figura (MLflow >= 1.14)
mlflow.log_figure(fig, "plots/predicho_vs_real.png")

plt.close(fig)
```

---

### Loguear modelos

```python
from sklearn.pipeline import Pipeline
import mlflow.sklearn

# Loguear modelo scikit-learn
mlflow.sklearn.log_model(pipeline, artifact_path="pipeline_rf")

# Con firma de entrada/salida inferida automaticamente
from mlflow.models import infer_signature
signature = infer_signature(X_train, pipeline.predict(X_train))
mlflow.sklearn.log_model(pipeline, artifact_path="pipeline_rf", signature=signature)

# Otros flavors disponibles
mlflow.xgboost.log_model(model, "model")
mlflow.pytorch.log_model(model, "model")
mlflow.tensorflow.log_model(model, "model")
```

---

### Registrar un modelo en el Model Registry (desde Python)

```python
result = mlflow.sklearn.log_model(
    pipeline,
    artifact_path="pipeline_rf",
    registered_model_name="concrete-strength-model",  # crea/actualiza en el Registry
)

# O desde un run ya existente
mlflow.register_model(
    model_uri=f"runs:/{run_id}/pipeline_rf",
    name="concrete-strength-model",
)
```

---

### Cargar un modelo registrado para inferencia

```python
# Cargar la version mas reciente
model = mlflow.sklearn.load_model("models:/concrete-strength-model/latest")

# Cargar una version especifica
model = mlflow.sklearn.load_model("models:/concrete-strength-model/3")

# Cargar sin importar el flavor (devuelve PyFunc)
model = mlflow.pyfunc.load_model("models:/concrete-strength-model/latest")
predictions = model.predict(X_test)
```

---

### Loguear tags y metadata extra

```python
mlflow.set_tag("autor", "equipo-mlops")
mlflow.set_tag("dataset_version", "v2")

mlflow.set_tags({
    "entorno": "desarrollo",
    "framework": "sklearn",
})
```

---

### Auto-logging (sin instrumentar manualmente)

```python
mlflow.sklearn.autolog()    # Loguea params, metricas y modelo automaticamente
# mlflow.xgboost.autolog()
# mlflow.pytorch.autolog()

with mlflow.start_run():
    pipeline.fit(X_train, y_train)  # MLflow captura todo sin llamadas explicitas
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

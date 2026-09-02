"""Genera la comparación visual de la lección 2.4."""

import sys
from pathlib import Path

sys.path.insert(0, "/tmp/material_curso_magic_sklearn_deps")
sys.path.insert(1, "/tmp/material_curso_magic_plot_deps")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor


salida = Path(__file__).resolve().parents[1] / "output" / "imagenes"
salida.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")

datos_modelo = pd.DataFrame(
    {
        "Fecha": pd.date_range("2026-01-01", periods=16),
        "Retorno_anterior": [
            -0.012,
            0.006,
            -0.004,
            0.011,
            0.003,
            -0.008,
            0.005,
            0.014,
            -0.006,
            0.009,
            0.002,
            -0.003,
            0.007,
            0.012,
            -0.005,
            0.004,
        ],
        "Media_movil_3": [
            100.4,
            100.8,
            100.6,
            101.1,
            101.5,
            101.2,
            101.7,
            102.3,
            102.0,
            102.6,
            102.9,
            102.7,
            103.1,
            103.8,
            103.5,
            103.9,
        ],
        "Volatilidad_3": [
            0.009,
            0.008,
            0.007,
            0.008,
            0.006,
            0.010,
            0.009,
            0.011,
            0.012,
            0.010,
            0.007,
            0.006,
            0.008,
            0.009,
            0.010,
            0.007,
        ],
        "Retorno_siguiente": [
            0.006,
            -0.004,
            0.011,
            0.003,
            -0.008,
            0.005,
            0.014,
            -0.006,
            0.009,
            0.002,
            -0.003,
            0.007,
            0.012,
            -0.005,
            0.004,
            0.010,
        ],
    }
)

variables = ["Retorno_anterior", "Media_movil_3", "Volatilidad_3"]
X = datos_modelo[variables]
y = datos_modelo["Retorno_siguiente"]

corte = int(len(datos_modelo) * 0.75)
X_entrenamiento = X.iloc[:corte]
X_prueba = X.iloc[corte:]
y_entrenamiento = y.iloc[:corte]
y_prueba = y.iloc[corte:]

modelo = DecisionTreeRegressor(max_depth=2, random_state=1)
modelo.fit(X_entrenamiento, y_entrenamiento)
predicciones = modelo.predict(X_prueba)
mae = mean_absolute_error(y_prueba, predicciones)

comparacion = pd.DataFrame(
    {
        "Fecha": datos_modelo.loc[X_prueba.index, "Fecha"],
        "Real": y_prueba,
        "Predicción": predicciones,
    }
)

figura, eje = plt.subplots(figsize=(8, 4))
eje.plot(
    comparacion["Fecha"],
    comparacion["Real"],
    color="b",
    marker="o",
    label="Real",
)
eje.plot(
    comparacion["Fecha"],
    comparacion["Predicción"],
    color="g",
    linestyle="--",
    marker="o",
    label="Predicción",
)
eje.set_title("Valores reales y predicciones")
eje.set_xlabel("Fecha")
eje.set_ylabel("Retorno")
eje.grid(alpha=0.3)
eje.legend()
eje.set_xticks(comparacion["Fecha"])
figura.autofmt_xdate(rotation=20)
sns.despine(ax=eje)
figura.savefig(
    salida / "2.4_predicciones.png",
    format="png",
    dpi=150,
    bbox_inches="tight",
    pad_inches=0.12,
    facecolor="white",
    pil_kwargs={"optimize": True},
)
plt.close(figura)

print(f"Predicciones: {predicciones.tolist()}")
print(f"MAE: {mae:.5f}")
print(salida / "2.4_predicciones.png")

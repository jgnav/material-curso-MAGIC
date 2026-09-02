"""Genera las salidas gráficas de la lección 2.3 en formato PDF."""

import sys
from pathlib import Path

sys.path.insert(0, "/tmp/material_curso_magic_plot_deps")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


RAIZ = Path(__file__).resolve().parents[2]
SALIDA_PDF = RAIZ / "output" / "pdf"
SALIDA_IMAGENES = RAIZ / "output" / "imagenes"
SALIDA_PDF.mkdir(parents=True, exist_ok=True)
SALIDA_IMAGENES.mkdir(parents=True, exist_ok=True)

sns.set_theme(
    style="whitegrid",
    context="notebook",
    rc={
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "grid.alpha": 0.25,
    },
)

fechas = pd.date_range("2026-01-01", periods=8)
datos = pd.DataFrame(
    {
        "Fecha": fechas,
        "Cierre": np.array(
            [100.0, 102.0, 101.0, 104.0, 103.0, 106.0, 108.0, 107.0]
        ),
    }
)
datos["Media_movil_3"] = datos["Cierre"].rolling(3).mean()

retornos = pd.Series(
    [
        -0.018,
        -0.012,
        -0.011,
        -0.009,
        -0.008,
        -0.007,
        -0.006,
        -0.005,
        -0.004,
        -0.003,
        -0.002,
        -0.001,
        0.000,
        0.001,
        0.002,
        0.003,
        0.004,
        0.005,
        0.006,
        0.007,
        0.008,
        0.009,
        0.010,
        0.011,
        0.012,
        0.014,
        0.016,
        0.018,
        0.021,
        0.025,
    ],
    name="Retorno",
)

comparacion = pd.DataFrame(
    {
        "Retorno_A": [0.010, -0.005, 0.012, 0.008, -0.004, 0.006],
        "Retorno_B": [0.004, -0.006, 0.011, 0.003, -0.001, 0.008],
        "Periodo": ["Inicio", "Inicio", "Inicio", "Final", "Final", "Final"],
    }
)

retornos_activos = pd.DataFrame(
    {
        "Activo_A": [0.010, -0.005, 0.012, 0.008, -0.004, 0.006],
        "Activo_B": [0.004, -0.006, 0.011, 0.003, -0.001, 0.008],
        "Activo_C": [-0.003, 0.005, -0.004, -0.008, 0.006, 0.002],
    }
)


def guardar(figura, nombre):
    figura.savefig(
        SALIDA_PDF / f"{nombre}.pdf",
        format="pdf",
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
        metadata={"Creator": "Matplotlib", "Title": nombre},
    )
    figura.savefig(
        SALIDA_IMAGENES / f"{nombre}.png",
        format="png",
        dpi=150,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
        pil_kwargs={"optimize": True},
    )
    plt.close(figura)


figura, eje = plt.subplots(figsize=(8.4, 3.6))
eje.plot(
    datos["Fecha"],
    datos["Cierre"],
    color="b",
    linewidth=2,
    marker="o",
    label="Cierre",
)
eje.plot(
    datos["Fecha"],
    datos["Media_movil_3"],
    color="g",
    linestyle="--",
    linewidth=2,
    label="Media móvil (3)",
)
eje.set_title("Evolución del precio")
eje.set_xlabel("Fecha")
eje.set_ylabel("Precio")
eje.grid(alpha=0.3)
eje.legend()
figura.autofmt_xdate(rotation=25)
figura.tight_layout()
sns.despine(ax=eje)
guardar(figura, "2.3_lineas")


figura, eje = plt.subplots(figsize=(7.6, 3.7))
sns.histplot(
    data=retornos,
    bins=8,
    kde=True,
    color="b",
    ax=eje,
)
eje.set_title("Distribución de los retornos")
eje.set_xlabel("Retorno")
eje.set_ylabel("Frecuencia")
figura.tight_layout()
sns.despine(ax=eje)
guardar(figura, "2.3_distribucion")


figura, eje = plt.subplots(figsize=(5.8, 4.6))
sns.scatterplot(
    data=comparacion,
    x="Retorno_A",
    y="Retorno_B",
    hue="Periodo",
    s=90,
    ax=eje,
)
eje.set_title("Relación entre dos series por periodo")
eje.set_xlabel("Retorno A")
eje.set_ylabel("Retorno B")
eje.set_xticks([-0.005, 0.000, 0.005, 0.010])
eje.set_yticks([-0.005, 0.000, 0.005, 0.010])
figura.tight_layout()
sns.despine(ax=eje)
guardar(figura, "2.3_dispersion")


figura, ejes = plt.subplots(1, 2, figsize=(10.8, 3.7))
ejes[0].plot(
    datos["Fecha"],
    datos["Cierre"],
    marker="o",
)
ejes[0].set_title("Serie de precios")
ejes[0].set_xlabel("Fecha")
ejes[0].set_ylabel("Precio")
ejes[0].tick_params(axis="x", rotation=25)

sns.histplot(
    data=retornos,
    bins=8,
    ax=ejes[1],
)
ejes[1].set_title("Distribución de retornos")
ejes[1].set_xlabel("Retorno")
ejes[1].set_ylabel("Frecuencia")

figura.suptitle("Resumen de los datos")
figura.tight_layout(rect=(0, 0, 1, 0.94))
sns.despine(fig=figura)
guardar(figura, "2.3_subplots")


correlaciones = retornos_activos.corr()
figura, eje = plt.subplots(figsize=(5.7, 4.0))
sns.heatmap(
    correlaciones,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    fmt=".2f",
    ax=eje,
)
eje.set_title("Correlación entre series")
figura.tight_layout()
guardar(figura, "2.3_correlaciones")


for ruta in sorted(SALIDA_IMAGENES.glob("2.3_*.png")):
    print(ruta)

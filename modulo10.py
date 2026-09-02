"""Autocorrección de 2.3. Matplotlib y Seaborn para visualización."""

from html import escape

import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from matplotlib.figure import Figure


_FECHAS = pd.date_range("2026-01-01", periods=8)
_CIERRES = np.array([100.0, 102.0, 101.0, 104.0, 103.0, 106.0, 108.0, 107.0])
_MEDIA_MOVIL = pd.Series(_CIERRES).rolling(3).mean().to_numpy()
_RETORNOS = np.array(
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
    ]
)
_RETORNO_A = np.array([0.010, -0.005, 0.012, 0.008, -0.004, 0.006])
_RETORNO_B = np.array([0.004, -0.006, 0.011, 0.003, -0.001, 0.008])
_PERIODOS = ["Inicio", "Inicio", "Inicio", "Final", "Final", "Final"]
_RETORNOS_ACTIVOS = pd.DataFrame(
    {
        "Activo_A": [0.010, -0.005, 0.012, 0.008, -0.004, 0.006],
        "Activo_B": [0.004, -0.006, 0.011, 0.003, -0.001, 0.008],
        "Activo_C": [-0.003, 0.005, -0.004, -0.008, 0.006, 0.002],
    }
)


def _mostrar_comprobacion(mensaje, correcta):
    """Muestra una comprobación coloreada en Colab y texto normal como respaldo."""

    color = "#137333" if correcta else "#c5221f"
    try:
        from IPython.display import HTML, display
    except ImportError:
        print(mensaje)
    else:
        display(
            HTML(
                f'<p style="color: {color}; font-weight: 600; margin: 8px 0;">'
                f"{escape(mensaje)}</p>"
            )
        )


class Ejercicio:
    """Pregunta con comprobación y ayuda opcional."""

    def __init__(self, numero, entorno, validar, pista=None, solucion=None):
        self.numero = numero
        self._entorno = entorno
        self._validar = validar
        self._pista = pista
        self._solucion = solucion
        self.completado = False

    def comprobar(self):
        try:
            resultado = self._validar(self._entorno)
        except Exception as error:
            _mostrar_comprobacion(
                f"El código ha producido {type(error).__name__}: {error}", False
            )
            return

        if resultado is True:
            self.completado = True
            _mostrar_comprobacion("Correcto. Puedes continuar.", True)
            return

        _mostrar_comprobacion(f"Revisa tu respuesta: {resultado}", False)

    def pista(self):
        if self._pista is not None:
            print(f"Pista: {self._pista}")

    def solucion(self):
        if self._solucion is not None:
            print("Una posible solución es:\n")
            print(self._solucion)


def _crear_datos():
    datos = pd.DataFrame(
        {
            "Fecha": _FECHAS.copy(),
            "Cierre": _CIERRES.copy(),
            "Media_movil_3": _MEDIA_MOVIL.copy(),
        }
    )
    retornos = pd.Series(_RETORNOS.copy(), name="Retorno")
    comparacion = pd.DataFrame(
        {
            "Retorno_A": _RETORNO_A.copy(),
            "Retorno_B": _RETORNO_B.copy(),
            "Periodo": _PERIODOS.copy(),
        }
    )
    return datos, retornos, comparacion, _RETORNOS_ACTIVOS.copy()


def _datos_sin_modificar(entorno):
    datos, retornos, comparacion, retornos_activos = _crear_datos()
    objetos = [
        ("datos", datos),
        ("retornos", retornos),
        ("comparacion", comparacion),
        ("retornos_activos", retornos_activos),
    ]
    for nombre, esperado in objetos:
        obtenido = entorno.get(nombre)
        if type(obtenido) is not type(esperado) or not obtenido.equals(esperado):
            return f"no modifiques el objeto {nombre} preparado por el notebook."
    return True


def _es_figura(objeto):
    return isinstance(objeto, Figure)


def _tamano_igual(figura, esperado):
    try:
        return bool(np.allclose(figura.get_size_inches(), esperado, atol=1e-9))
    except Exception:
        return False


def _color_igual(obtenido, esperado):
    try:
        return bool(np.allclose(to_rgba(obtenido)[:3], to_rgba(esperado)[:3]))
    except (TypeError, ValueError):
        return False


def _valores_iguales(obtenidos, esperados, permitir_nan=False):
    try:
        obtenidos_array = np.asarray(obtenidos, dtype=float)
        esperados_array = np.asarray(esperados, dtype=float)
        if obtenidos_array.shape != esperados_array.shape:
            if obtenidos_array.size != esperados_array.size:
                return False
            obtenidos_array = obtenidos_array.ravel()
            esperados_array = esperados_array.ravel()
        return bool(
            np.allclose(
                obtenidos_array,
                esperados_array,
                rtol=1e-9,
                atol=1e-9,
                equal_nan=permitir_nan,
            )
        )
    except (TypeError, ValueError):
        return False


def _fechas_iguales(obtenidas):
    try:
        return pd.DatetimeIndex(pd.to_datetime(obtenidas)).equals(_FECHAS)
    except Exception:
        return False


def _leyenda_contiene(eje, textos):
    leyenda = eje.get_legend()
    if leyenda is None:
        return False
    encontrados = {texto.get_text() for texto in leyenda.get_texts()}
    return set(textos).issubset(encontrados)


def _validar_q1(entorno):
    plt = entorno.get("plt")
    sns = entorno.get("sns")
    if getattr(plt, "__name__", None) != "matplotlib.pyplot":
        return "importa matplotlib.pyplot utilizando el alias plt."
    if getattr(sns, "__name__", None) != "seaborn":
        return "importa Seaborn utilizando el alias sns."

    estilo = sns.axes_style()
    if estilo.get("axes.facecolor") != "white" or estilo.get("axes.grid") is not True:
        return 'aplica sns.set_theme(style="whitegrid").'
    return True


def _validar_q2(entorno):
    resultado = _datos_sin_modificar(entorno)
    if resultado is not True:
        return resultado

    figura = entorno.get("figura_lineas")
    if not _es_figura(figura):
        return "guarda la figura creada con plt.figure() en figura_lineas."
    if not _tamano_igual(figura, (9, 4)):
        return "crea figura_lineas con figsize=(9, 4)."
    if len(figura.axes) != 1:
        return "la figura debe contener un único eje."

    eje = figura.axes[0]
    if eje.get_title() != "Evolución del precio":
        return "añade el título indicado."
    if eje.get_xlabel() != "Fecha" or eje.get_ylabel() != "Precio":
        return "revisa las etiquetas de los ejes."

    lineas = eje.get_lines()
    if len(lineas) != 2:
        return "representa exactamente las dos series solicitadas."
    cierre, media = lineas
    if not _fechas_iguales(cierre.get_xdata()) or not _valores_iguales(
        cierre.get_ydata(), _CIERRES
    ):
        return "la primera línea debe representar Fecha frente a Cierre."
    if not _fechas_iguales(media.get_xdata()) or not _valores_iguales(
        media.get_ydata(), _MEDIA_MOVIL, permitir_nan=True
    ):
        return "la segunda línea debe representar Fecha frente a Media_movil_3."
    if not _color_igual(cierre.get_color(), "b"):
        return 'utiliza el color "b" para la línea de cierre.'
    if not np.isclose(cierre.get_linewidth(), 2) or cierre.get_marker() != "o":
        return "revisa linewidth y marker en la línea de cierre."
    if cierre.get_label() != "Cierre":
        return "asigna la etiqueta Cierre a la primera línea."
    if not _color_igual(media.get_color(), "g"):
        return 'utiliza el color "g" para la media móvil.'
    if media.get_linestyle() != "--" or media.get_label() != "Media móvil (3)":
        return "revisa linestyle y label en la línea de la media móvil."
    if not _leyenda_contiene(eje, ["Cierre", "Media móvil (3)"]):
        return "muestra la leyenda con plt.legend()."
    lineas_cuadricula = eje.get_xgridlines() + eje.get_ygridlines()
    if not any(linea.get_visible() for linea in lineas_cuadricula):
        return "activa la cuadrícula."
    return True


def _validar_q3(entorno):
    resultado = _datos_sin_modificar(entorno)
    if resultado is not True:
        return resultado

    figura = entorno.get("figura_histograma")
    if not _es_figura(figura):
        return "guarda la figura en figura_histograma."
    if not _tamano_igual(figura, (8, 4)):
        return "crea figura_histograma con figsize=(8, 4)."
    if len(figura.axes) != 1:
        return "la figura debe contener un único eje."

    eje = figura.axes[0]
    if eje.get_title() != "Distribución de los retornos":
        return "añade el título indicado."
    if eje.get_xlabel() != "Retorno" or eje.get_ylabel() != "Frecuencia":
        return "revisa las etiquetas de los ejes."
    if len(eje.patches) != 8:
        return "divide el histograma en ocho intervalos mediante bins=8."
    if not np.isclose(sum(barra.get_height() for barra in eje.patches), 30):
        return "representa todos los valores de retornos con el estadístico count."
    if len(eje.lines) < 1:
        return "añade la curva de densidad con kde=True."
    if not all(
        _color_igual(barra.get_facecolor(), "b") for barra in eje.patches
    ):
        return 'utiliza el color "b" para las barras.'
    return True


def _validar_q4(entorno):
    resultado = _datos_sin_modificar(entorno)
    if resultado is not True:
        return resultado

    figura = entorno.get("figura_dispersion")
    if not _es_figura(figura):
        return "guarda la figura en figura_dispersion."
    if not _tamano_igual(figura, (6, 5)):
        return "crea figura_dispersion con figsize=(6, 5)."
    if len(figura.axes) != 1:
        return "la figura debe contener un único eje."

    eje = figura.axes[0]
    if eje.get_title() != "Relación entre dos series por periodo":
        return "añade el título indicado."
    if eje.get_xlabel() != "Retorno A" or eje.get_ylabel() != "Retorno B":
        return "revisa las etiquetas de los ejes."

    coleccion = None
    for candidata in eje.collections:
        try:
            if len(candidata.get_offsets()) == 6:
                coleccion = candidata
                break
        except Exception:
            continue
    if coleccion is None:
        return "representa las seis observaciones de comparacion."
    esperados = np.column_stack((_RETORNO_A, _RETORNO_B))
    if not _valores_iguales(coleccion.get_offsets(), esperados):
        return "utiliza Retorno_A en x y Retorno_B en y."
    if not _valores_iguales(coleccion.get_sizes(), [90]):
        return "utiliza s=90 para el tamaño de los puntos."
    if not _leyenda_contiene(eje, ["Inicio", "Final"]):
        return "utiliza hue=\"Periodo\" para distinguir las categorías."
    if not _valores_iguales(eje.get_xticks(), [-0.005, 0.000, 0.005, 0.010]):
        return "fija las marcas solicitadas en el eje horizontal."
    if not _valores_iguales(eje.get_yticks(), [-0.005, 0.000, 0.005, 0.010]):
        return "fija las marcas solicitadas en el eje vertical."
    return True


def _validar_q5(entorno):
    resultado = _datos_sin_modificar(entorno)
    if resultado is not True:
        return resultado

    figura = entorno.get("figura_resumen")
    if not _es_figura(figura):
        return "guarda la figura creada por plt.subplots() en figura_resumen."
    if not _tamano_igual(figura, (12, 4)):
        return "crea figura_resumen con figsize=(12, 4)."

    try:
        ejes = list(np.asarray(entorno.get("ejes"), dtype=object).ravel())
    except Exception:
        return "guarda los ejes devueltos por plt.subplots() en ejes."
    if len(ejes) != 2 or figura.axes != ejes:
        return "crea una fila con dos ejes y guárdalos en ejes."

    izquierda, derecha = ejes
    if izquierda.get_title() != "Serie de precios":
        return "añade el título Serie de precios al primer eje."
    if len(izquierda.get_lines()) != 1:
        return "dibuja una línea en ejes[0]."
    linea = izquierda.get_lines()[0]
    if not _fechas_iguales(linea.get_xdata()) or not _valores_iguales(
        linea.get_ydata(), _CIERRES
    ):
        return "representa Fecha frente a Cierre en ejes[0]."
    if linea.get_marker() != "o":
        return "utiliza marker=\"o\" en la línea del primer eje."

    if derecha.get_title() != "Distribución de retornos":
        return "añade el título Distribución de retornos al segundo eje."
    if len(derecha.patches) != 8:
        return "crea en ejes[1] un histograma con ocho intervalos."
    if not np.isclose(sum(barra.get_height() for barra in derecha.patches), 30):
        return "representa todos los valores de retornos en ejes[1]."

    titulo_general = getattr(figura, "_suptitle", None)
    if titulo_general is None or titulo_general.get_text() != "Resumen de los datos":
        return "añade el título general Resumen de los datos."
    return True


def _validar_q6(entorno):
    resultado = _datos_sin_modificar(entorno)
    if resultado is not True:
        return resultado

    esperado = _RETORNOS_ACTIVOS.corr()
    correlaciones = entorno.get("correlaciones")
    if not isinstance(correlaciones, pd.DataFrame) or not correlaciones.equals(esperado):
        return "guarda retornos_activos.corr() en correlaciones."

    figura = entorno.get("figura_correlaciones")
    if not _es_figura(figura):
        return "guarda la figura en figura_correlaciones."
    if not _tamano_igual(figura, (6, 4)):
        return "crea figura_correlaciones con figsize=(6, 4)."

    ejes_principales = [
        eje for eje in figura.axes if eje.get_title() == "Correlación entre series"
    ]
    if len(ejes_principales) != 1:
        return "añade el título Correlación entre series al mapa de calor."
    eje = ejes_principales[0]
    if not eje.collections:
        return "representa correlaciones mediante sns.heatmap()."
    mapa = eje.collections[0]
    if not _valores_iguales(mapa.get_array(), esperado.to_numpy().ravel()):
        return "el mapa de calor debe representar la matriz correlaciones."
    if not _valores_iguales(mapa.get_clim(), [-1, 1]):
        return "fija la escala de color con vmin=-1 y vmax=1."
    if getattr(mapa.get_cmap(), "name", None) != "coolwarm":
        return "utiliza cmap=\"coolwarm\"."

    anotaciones = [texto.get_text() for texto in eje.texts]
    esperadas = [f"{valor:.2f}" for valor in esperado.to_numpy().ravel()]
    if anotaciones != esperadas:
        return "muestra los valores con annot=True y fmt=\".2f\"."
    return True


def cargar(entorno):
    """Carga los datos y las preguntas de la lección en el notebook."""

    from matplotlib import pyplot as plt

    plt.close("all")
    datos, retornos, comparacion, retornos_activos = _crear_datos()
    entorno["datos"] = datos
    entorno["retornos"] = retornos
    entorno["comparacion"] = comparacion
    entorno["retornos_activos"] = retornos_activos

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Crea la figura antes de llamar dos veces a plt.plot(). En la "
            "primera llamada utiliza Cierre y en la segunda Media_movil_3.",
            "figura_lineas = plt.figure(figsize=(9, 4))\n"
            "plt.plot(\n"
            "    datos[\"Fecha\"],\n"
            "    datos[\"Cierre\"],\n"
            "    color=\"b\",\n"
            "    linewidth=2,\n"
            "    marker=\"o\",\n"
            "    label=\"Cierre\",\n"
            ")\n"
            "plt.plot(\n"
            "    datos[\"Fecha\"],\n"
            "    datos[\"Media_movil_3\"],\n"
            "    color=\"g\",\n"
            "    linestyle=\"--\",\n"
            "    label=\"Media móvil (3)\",\n"
            ")\n"
            "plt.title(\"Evolución del precio\")\n"
            "plt.xlabel(\"Fecha\")\n"
            "plt.ylabel(\"Precio\")\n"
            "plt.grid(alpha=0.3)\n"
            "plt.legend()\n"
            "plt.show()",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Pasa retornos a data. Utiliza bins=8, kde=True y el color "
            "indicado antes de añadir el título y las etiquetas.",
            "figura_histograma = plt.figure(figsize=(8, 4))\n"
            "sns.histplot(\n"
            "    data=retornos,\n"
            "    bins=8,\n"
            "    kde=True,\n"
            "    color=\"b\",\n"
            ")\n"
            "plt.title(\"Distribución de los retornos\")\n"
            "plt.xlabel(\"Retorno\")\n"
            "plt.ylabel(\"Frecuencia\")\n"
            "plt.show()",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Utiliza comparacion como data, las columnas Retorno_A y "
            "Retorno_B en los ejes, y Periodo en hue.",
            "figura_dispersion = plt.figure(figsize=(6, 5))\n"
            "sns.scatterplot(\n"
            "    data=comparacion,\n"
            "    x=\"Retorno_A\",\n"
            "    y=\"Retorno_B\",\n"
            "    hue=\"Periodo\",\n"
            "    s=90,\n"
            ")\n"
            "plt.title(\"Relación entre dos series por periodo\")\n"
            "plt.xlabel(\"Retorno A\")\n"
            "plt.ylabel(\"Retorno B\")\n"
            "plt.xticks([-0.005, 0.000, 0.005, 0.010])\n"
            "plt.yticks([-0.005, 0.000, 0.005, 0.010])\n"
            "plt.show()",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Crea los dos ejes con plt.subplots(1, 2, ...). Dibuja con el "
            "método plot() del primer eje y pasa el segundo mediante ax a "
            "sns.histplot().",
            "figura_resumen, ejes = plt.subplots(1, 2, figsize=(12, 4))\n"
            "ejes[0].plot(\n"
            "    datos[\"Fecha\"],\n"
            "    datos[\"Cierre\"],\n"
            "    marker=\"o\",\n"
            ")\n"
            "ejes[0].set_title(\"Serie de precios\")\n"
            "sns.histplot(\n"
            "    data=retornos,\n"
            "    bins=8,\n"
            "    ax=ejes[1],\n"
            ")\n"
            "ejes[1].set_title(\"Distribución de retornos\")\n"
            "figura_resumen.suptitle(\"Resumen de los datos\")\n"
            "plt.show()",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Calcula primero la matriz con corr(). Pásala como primer "
            "argumento de heatmap y utiliza annot, cmap, vmin, vmax y fmt.",
            "correlaciones = retornos_activos.corr()\n"
            "figura_correlaciones = plt.figure(figsize=(6, 4))\n"
            "sns.heatmap(\n"
            "    correlaciones,\n"
            "    annot=True,\n"
            "    cmap=\"coolwarm\",\n"
            "    vmin=-1,\n"
            "    vmax=1,\n"
            "    fmt=\".2f\",\n"
            ")\n"
            "plt.title(\"Correlación entre series\")\n"
            "plt.show()",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]

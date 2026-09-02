"""Autocorrección de 2.4. Introducción a scikit-learn."""

from html import escape
from numbers import Real

import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from matplotlib.dates import date2num
from matplotlib.figure import Figure
from sklearn.metrics import mean_absolute_error as _mean_absolute_error
from sklearn.tree import DecisionTreeRegressor as _DecisionTreeRegressor


_FECHAS = pd.date_range("2026-01-01", periods=16)
_RETORNO_ANTERIOR = [
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
]
_MEDIA_MOVIL = [
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
]
_VOLATILIDAD = [
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
]
_OBJETIVO = [
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
]
_VARIABLES = ["Retorno_anterior", "Media_movil_3", "Volatilidad_3"]
_PREDICCIONES = np.array([0.0018, 0.0018, 0.0090, 0.0018])
_MAE = 0.00755


def _mostrar_comprobacion(mensaje, correcta):
    """Muestra una comprobación coloreada en Colab y texto normal como respaldo."""

    color = "green" if correcta else "red"
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
    return pd.DataFrame(
        {
            "Fecha": _FECHAS.copy(),
            "Retorno_anterior": _RETORNO_ANTERIOR.copy(),
            "Media_movil_3": _MEDIA_MOVIL.copy(),
            "Volatilidad_3": _VOLATILIDAD.copy(),
            "Retorno_siguiente": _OBJETIVO.copy(),
        }
    )


def _datos_sin_modificar(entorno):
    datos = entorno.get("datos_modelo")
    if not isinstance(datos, pd.DataFrame) or not datos.equals(_crear_datos()):
        return "no modifiques el DataFrame datos_modelo preparado por el notebook."
    return True


def _objetos_esperados():
    datos = _crear_datos()
    X = datos[_VARIABLES]
    y = datos["Retorno_siguiente"]
    return datos, X, y


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
            return False
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


def _fechas_iguales(obtenidas, esperadas):
    try:
        return pd.DatetimeIndex(pd.to_datetime(obtenidas)).equals(
            pd.DatetimeIndex(esperadas)
        )
    except Exception:
        return False


def _leyenda_contiene(eje, textos):
    leyenda = eje.get_legend()
    if leyenda is None:
        return False
    encontrados = {texto.get_text() for texto in leyenda.get_texts()}
    return set(textos).issubset(encontrados)


def _validar_q1(entorno):
    if getattr(entorno.get("pd"), "__name__", None) != "pandas":
        return "importa Pandas utilizando el alias pd."
    if getattr(entorno.get("plt"), "__name__", None) != "matplotlib.pyplot":
        return "importa matplotlib.pyplot utilizando el alias plt."

    clase = entorno.get("DecisionTreeRegressor")
    if (
        getattr(clase, "__name__", None) != "DecisionTreeRegressor"
        or not getattr(clase, "__module__", "").startswith("sklearn.tree")
    ):
        return "importa DecisionTreeRegressor desde sklearn.tree."

    metrica = entorno.get("mean_absolute_error")
    if (
        getattr(metrica, "__name__", None) != "mean_absolute_error"
        or not getattr(metrica, "__module__", "").startswith("sklearn.metrics")
    ):
        return "importa mean_absolute_error desde sklearn.metrics."
    return True


def _validar_q2(entorno):
    resultado = _datos_sin_modificar(entorno)
    if resultado is not True:
        return resultado
    _, X_esperado, y_esperado = _objetos_esperados()

    if entorno.get("variables") != _VARIABLES:
        return "crea la lista variables con las tres columnas en el orden indicado."
    X = entorno.get("X")
    if not isinstance(X, pd.DataFrame) or not X.equals(X_esperado):
        return "selecciona en X las tres variables predictoras."
    y = entorno.get("y")
    if not isinstance(y, pd.Series) or not y.equals(y_esperado):
        return "selecciona Retorno_siguiente como Series y guárdala en y."
    return True


def _validar_q3(entorno):
    resultado = _validar_q2(entorno)
    if resultado is not True:
        return "completa correctamente la preparación de X e y."
    _, X, y = _objetos_esperados()

    if entorno.get("corte") != 12:
        return "calcula corte como el 75 % entero de la longitud de datos_modelo."

    esperados = {
        "X_entrenamiento": X.iloc[:12],
        "X_prueba": X.iloc[12:],
        "y_entrenamiento": y.iloc[:12],
        "y_prueba": y.iloc[12:],
    }
    for nombre, esperado in esperados.items():
        obtenido = entorno.get(nombre)
        if type(obtenido) is not type(esperado) or not obtenido.equals(esperado):
            return f"revisa el corte cronológico guardado en {nombre}."
    return True


def _validar_q4(entorno):
    resultado = _validar_q3(entorno)
    if resultado is not True:
        return "completa correctamente la separación cronológica."

    modelo = entorno.get("modelo")
    if not isinstance(modelo, _DecisionTreeRegressor):
        return "crea modelo mediante DecisionTreeRegressor."
    if modelo.get_params().get("max_depth") != 2:
        return "utiliza max_depth=2."
    if modelo.get_params().get("random_state") != 1:
        return "utiliza random_state=1."
    if not hasattr(modelo, "tree_"):
        return "entrena el modelo mediante fit()."
    if list(getattr(modelo, "feature_names_in_", [])) != _VARIABLES:
        return "entrena el modelo con X_entrenamiento."

    _, X, y = _objetos_esperados()
    modelo_esperado = _DecisionTreeRegressor(max_depth=2, random_state=1)
    modelo_esperado.fit(X.iloc[:12], y.iloc[:12])
    if not _valores_iguales(modelo.predict(X), modelo_esperado.predict(X)):
        return "entrena el modelo con X_entrenamiento e y_entrenamiento."
    return True


def _validar_q5(entorno):
    resultado = _validar_q4(entorno)
    if resultado is not True:
        return "define y entrena correctamente el modelo antes de predecir."

    predicciones = entorno.get("predicciones")
    if not isinstance(predicciones, np.ndarray) or not _valores_iguales(
        predicciones, _PREDICCIONES
    ):
        return "genera predicciones para X_prueba mediante predict()."

    mae = entorno.get("mae")
    if not isinstance(mae, Real) or isinstance(mae, bool):
        return "guarda el error absoluto medio en mae."
    if not np.isclose(float(mae), _MAE, rtol=1e-9, atol=1e-9):
        return "calcula el MAE comparando y_prueba con predicciones."
    return True


def _validar_q6(entorno):
    resultado = _validar_q5(entorno)
    if resultado is not True:
        return "calcula correctamente las predicciones y el MAE."

    comparacion = entorno.get("comparacion")
    if not isinstance(comparacion, pd.DataFrame):
        return "crea comparacion como un DataFrame de Pandas."
    if list(comparacion.columns) != ["Fecha", "Real", "Predicción"]:
        return "utiliza las columnas Fecha, Real y Predicción, en ese orden."
    if not _fechas_iguales(comparacion["Fecha"], _FECHAS[12:]):
        return "la columna Fecha debe contener las cuatro fechas de prueba."
    if not _valores_iguales(comparacion["Real"], _OBJETIVO[12:]):
        return "la columna Real debe contener y_prueba."
    if not _valores_iguales(comparacion["Predicción"], _PREDICCIONES):
        return "la columna Predicción debe contener predicciones."
    return True


def _validar_q7(entorno):
    resultado = _validar_q6(entorno)
    if resultado is not True:
        return "crea correctamente el DataFrame comparacion."

    figura = entorno.get("figura_comparacion")
    if not isinstance(figura, Figure):
        return "guarda la figura en figura_comparacion."
    if not _valores_iguales(figura.get_size_inches(), [8, 4]):
        return "crea figura_comparacion con figsize=(8, 4)."
    if len(figura.axes) != 1:
        return "la figura debe contener un único eje."

    eje = figura.axes[0]
    if eje.get_title() != "Valores reales y predicciones":
        return "añade el título indicado."
    if eje.get_xlabel() != "Fecha" or eje.get_ylabel() != "Retorno":
        return "revisa las etiquetas de los ejes."

    lineas = eje.get_lines()
    if len(lineas) != 2:
        return "representa exactamente las series Real y Predicción."
    real, prediccion = lineas
    if not _fechas_iguales(real.get_xdata(), _FECHAS[12:]) or not _valores_iguales(
        real.get_ydata(), _OBJETIVO[12:]
    ):
        return "la primera línea debe representar Fecha frente a Real."
    if not _fechas_iguales(
        prediccion.get_xdata(), _FECHAS[12:]
    ) or not _valores_iguales(prediccion.get_ydata(), _PREDICCIONES):
        return "la segunda línea debe representar Fecha frente a Predicción."
    if (
        not _color_igual(real.get_color(), "b")
        or real.get_marker() != "o"
        or real.get_label() != "Real"
    ):
        return 'revisa color="b", marker="o" y label="Real".'
    if (
        not _color_igual(prediccion.get_color(), "g")
        or prediccion.get_linestyle() != "--"
        or prediccion.get_marker() != "o"
        or prediccion.get_label() != "Predicción"
    ):
        return "revisa el aspecto y la etiqueta de la línea de predicciones."
    if not _leyenda_contiene(eje, ["Real", "Predicción"]):
        return "muestra una leyenda con las dos series."
    if not any(
        linea.get_visible()
        for linea in eje.get_xgridlines() + eje.get_ygridlines()
    ):
        return "activa la cuadrícula."
    if not _valores_iguales(eje.get_xticks(), date2num(_FECHAS[12:])):
        return "fija las fechas de comparacion como marcas del eje horizontal."
    if not all(np.isclose(etiqueta.get_rotation(), 20) for etiqueta in eje.get_xticklabels()):
        return "gira 20 grados las etiquetas del eje horizontal."
    return True


def cargar(entorno):
    """Carga los datos y las preguntas de la lección en el notebook."""

    from matplotlib import pyplot as plt

    plt.close("all")
    entorno["datos_modelo"] = _crear_datos()

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Crea la lista con los tres nombres y úsala dentro de los "
            "corchetes de datos_modelo. Selecciona la columna objetivo por "
            "separado.",
            "variables = [\n"
            "    \"Retorno_anterior\",\n"
            "    \"Media_movil_3\",\n"
            "    \"Volatilidad_3\",\n"
            "]\n"
            "X = datos_modelo[variables]\n"
            "y = datos_modelo[\"Retorno_siguiente\"]",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Calcula el 75 % de la longitud y conviértelo en entero. Utiliza "
            "iloc con :corte para entrenar y corte: para probar.",
            "corte = int(len(datos_modelo) * 0.75)\n"
            "X_entrenamiento = X.iloc[:corte]\n"
            "X_prueba = X.iloc[corte:]\n"
            "y_entrenamiento = y.iloc[:corte]\n"
            "y_prueba = y.iloc[corte:]",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Crea el estimador con los dos parámetros indicados y llama a "
            "fit() con X_entrenamiento e y_entrenamiento.",
            "modelo = DecisionTreeRegressor(\n"
            "    max_depth=2,\n"
            "    random_state=1,\n"
            ")\n"
            "modelo.fit(X_entrenamiento, y_entrenamiento)",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "Pasa X_prueba a predict(). Después utiliza y_prueba como primer "
            "argumento de mean_absolute_error() y las predicciones como segundo.",
            "predicciones = modelo.predict(X_prueba)\n"
            "mae = mean_absolute_error(y_prueba, predicciones)",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "Crea un diccionario con los tres nombres de columna. Para Fecha, "
            "selecciona en datos_modelo los índices de X_prueba.",
            "comparacion = pd.DataFrame({\n"
            "    \"Fecha\": datos_modelo.loc[X_prueba.index, \"Fecha\"],\n"
            "    \"Real\": y_prueba,\n"
            "    \"Predicción\": predicciones,\n"
            "})",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Crea la figura antes de llamar dos veces a plt.plot(). Utiliza "
            "las columnas Fecha, Real y Predicción de comparacion.",
            "figura_comparacion = plt.figure(figsize=(8, 4))\n"
            "plt.plot(\n"
            "    comparacion[\"Fecha\"],\n"
            "    comparacion[\"Real\"],\n"
            "    color=\"b\",\n"
            "    marker=\"o\",\n"
            "    label=\"Real\",\n"
            ")\n"
            "plt.plot(\n"
            "    comparacion[\"Fecha\"],\n"
            "    comparacion[\"Predicción\"],\n"
            "    color=\"g\",\n"
            "    linestyle=\"--\",\n"
            "    marker=\"o\",\n"
            "    label=\"Predicción\",\n"
            ")\n"
            "plt.title(\"Valores reales y predicciones\")\n"
            "plt.xlabel(\"Fecha\")\n"
            "plt.ylabel(\"Retorno\")\n"
            "plt.grid(alpha=0.3)\n"
            "plt.legend()\n"
            "plt.xticks(comparacion[\"Fecha\"], rotation=20)\n"
            "plt.show()",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]

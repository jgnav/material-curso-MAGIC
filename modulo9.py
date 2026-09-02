"""Autocorrección de 2.2. NumPy para operaciones numéricas."""

from html import escape
from numbers import Real

import numpy as np


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


def _es_modulo_numpy(objeto):
    return getattr(objeto, "__name__", None) == "numpy"


def _es_array(objeto):
    return isinstance(objeto, np.ndarray)


def _array_numerico_igual(obtenido, esperado, permitir_nan=False):
    if not _es_array(obtenido):
        return False

    esperado_array = np.asarray(esperado)
    if obtenido.shape != esperado_array.shape:
        return False

    try:
        return bool(
            np.allclose(
                obtenido,
                esperado_array,
                rtol=1e-9,
                atol=1e-9,
                equal_nan=permitir_nan,
            )
        )
    except (TypeError, ValueError):
        return False


def _array_exacto_igual(obtenido, esperado):
    if not _es_array(obtenido):
        return False
    try:
        return bool(np.array_equal(obtenido, np.asarray(esperado)))
    except (TypeError, ValueError):
        return False


def _numero_igual(obtenido, esperado):
    if not isinstance(obtenido, Real) or isinstance(obtenido, bool):
        return False
    return bool(np.isclose(obtenido, esperado, rtol=1e-9, atol=1e-9))


def _validar_q1(entorno):
    if not _es_modulo_numpy(entorno.get("np")):
        return "importa NumPy utilizando el alias np."

    precios_esperados = [101.5, 102.4, 101.7, 103.6, 104.8]
    if entorno.get("precios_lista") != precios_esperados:
        return "no modifiques la lista precios_lista."
    if not _array_numerico_igual(entorno.get("precios"), precios_esperados):
        return "convierte precios_lista en un array llamado precios."
    if not _array_numerico_igual(entorno.get("secuencia"), [0, 2, 4, 6, 8]):
        return "secuencia debe contener los números pares desde 0 hasta 8."
    if not _array_numerico_igual(entorno.get("ceros"), [0.0, 0.0, 0.0]):
        return "crea mediante np.zeros() un array con tres ceros."
    return True


def _validar_q2(entorno):
    datos = entorno.get("datos")
    if not _array_numerico_igual(datos, list(range(12))):
        return "no modifiques el array datos."

    matriz = entorno.get("matriz")
    esperado = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
    if not _array_numerico_igual(matriz, esperado):
        return "reorganiza datos en tres filas y cuatro columnas."
    if entorno.get("forma") != (3, 4):
        return "guarda matriz.shape en forma."
    if entorno.get("total") != 12:
        return "guarda matriz.size en total."
    if entorno.get("dimensiones") != 2:
        return "guarda matriz.ndim en dimensiones."
    if entorno.get("tipo") != matriz.dtype:
        return "guarda matriz.dtype en tipo."
    return True


def _validar_q3(entorno):
    precios = entorno.get("precios")
    esperado = [101.5, 102.4, 101.7, 103.6, 104.8, 105.4]
    if not _array_numerico_igual(precios, esperado):
        return "no modifiques el array precios."
    if not _numero_igual(entorno.get("primer_precio"), 101.5):
        return "primer_precio debe contener el elemento de la posición 0."
    if not _numero_igual(entorno.get("ultimo_precio"), 105.4):
        return "ultimo_precio debe contener el último elemento."

    centrales = entorno.get("precios_centrales")
    if not _array_numerico_igual(centrales, [102.4, 101.7, 103.6]):
        return "selecciona las posiciones 1, 2 y 3."
    if np.shares_memory(centrales, precios):
        return "precios_centrales debe ser una copia independiente del slice."
    return True


def _validar_q4(entorno):
    a = entorno.get("a")
    b = entorno.get("b")
    if not _array_numerico_igual(a, [10, 21, 32]):
        return "no modifiques el array a."
    if not _array_numerico_igual(b, [3, 4, 5]):
        return "no modifiques el array b."

    comprobaciones = [
        ("sumas", [13, 25, 37], "suma a y b."),
        ("diferencias", [7, 17, 27], "resta b a a."),
        ("productos", [30, 84, 160], "multiplica a y b."),
        ("cocientes", [10 / 3, 21 / 4, 32 / 5], "divide a entre b."),
        ("divisiones_enteras", [3, 5, 6], "utiliza // entre a y b."),
        ("restos", [1, 1, 2], "utiliza % entre a y b."),
        ("cuadrados", [100, 441, 1024], "eleva a al cuadrado."),
    ]
    for nombre, esperado, mensaje in comprobaciones:
        if not _array_numerico_igual(entorno.get(nombre), esperado):
            return f"para calcular {nombre}, {mensaje}"
    return True


def _validar_q5(entorno):
    matriz_a = entorno.get("matriz_a")
    matriz_b = entorno.get("matriz_b")
    if not _array_numerico_igual(matriz_a, [[1, 2], [3, 4]]):
        return "no modifiques matriz_a."
    if not _array_numerico_igual(matriz_b, [[5, 6], [7, 8]]):
        return "no modifiques matriz_b."

    esperados = {
        "suma_matrices": [[6, 8], [10, 12]],
        "doble_a": [[2, 4], [6, 8]],
        "producto_elemento": [[5, 12], [21, 32]],
        "producto_matricial": [[19, 22], [43, 50]],
        "transpuesta_a": [[1, 3], [2, 4]],
    }
    for nombre, esperado in esperados.items():
        if not _array_numerico_igual(entorno.get(nombre), esperado):
            return f"revisa el cálculo de {nombre}."
    return True


def _validar_q6(entorno):
    precios = entorno.get("precios")
    esperados_precios = [101.5, 102.4, 101.7, 103.6, 104.8, 105.4]
    if not _array_numerico_igual(precios, esperados_precios):
        return "no modifiques el array precios."

    esperados = np.asarray(esperados_precios[1:]) / np.asarray(
        esperados_precios[:-1]
    ) - 1
    if not _array_numerico_igual(entorno.get("retornos"), esperados):
        return "divide cada precio entre el anterior y resta 1."
    if not _array_numerico_igual(
        entorno.get("retornos_redondeados"), np.round(esperados, 4)
    ):
        return "redondea retornos a cuatro decimales."
    return True


def _validar_q7(entorno):
    retornos = entorno.get("retornos")
    esperados = [0.0089, -0.0068, 0.0187, 0.0116, 0.0057]
    if not _array_numerico_igual(retornos, esperados):
        return "no modifiques el array retornos."
    if not _array_exacto_igual(
        entorno.get("es_positivo"), [True, False, True, True, True]
    ):
        return "compara el array completo con 0."
    if not _array_numerico_igual(
        entorno.get("retornos_positivos"), [0.0089, 0.0187, 0.0116, 0.0057]
    ):
        return "utiliza es_positivo como máscara para filtrar retornos."
    if not _array_numerico_igual(
        entorno.get("retornos_moderados"), [0.0089, 0.0057]
    ):
        return "combina las dos comparaciones indicadas mediante &."
    if not _array_exacto_igual(
        entorno.get("clasificacion"),
        ["Positivo", "No positivo", "Positivo", "Positivo", "Positivo"],
    ):
        return "utiliza np.where() con los textos indicados."
    return True


def _validar_q8(entorno):
    datos = entorno.get("datos")
    esperado = [[1, 2, 3], [4, 5, 6]]
    if not _array_numerico_igual(datos, esperado):
        return "no modifiques el array datos."
    if not _numero_igual(entorno.get("media_total"), 3.5):
        return "calcula la media de todos los valores."
    if not _array_numerico_igual(entorno.get("suma_columnas"), [5, 7, 9]):
        return "utiliza axis=0 para sumar cada columna."
    if not _array_numerico_igual(entorno.get("media_filas"), [2, 5]):
        return "utiliza axis=1 para calcular la media de cada fila."
    if not _numero_igual(entorno.get("desviacion_total"), np.std(esperado)):
        return "calcula la desviación estándar de todos los valores."
    return True


def _validar_q9(entorno):
    mediciones = entorno.get("mediciones")
    esperado = [1.2, np.nan, 2.4, 3.6, np.nan]
    if not _array_numerico_igual(mediciones, esperado, permitir_nan=True):
        return "no modifiques el array mediciones."
    if not _array_exacto_igual(
        entorno.get("es_ausente"), [False, True, False, False, True]
    ):
        return "identifica los valores ausentes con np.isnan()."
    if entorno.get("cantidad_ausentes") != 2:
        return "suma la máscara es_ausente para contar los valores ausentes."
    if not _array_numerico_igual(
        entorno.get("mediciones_validas"), [1.2, 2.4, 3.6]
    ):
        return "invierte la máscara para seleccionar los valores válidos."
    if not _numero_igual(entorno.get("media_valida"), 2.4):
        return "calcula la media ignorando los NaN."
    if not _array_numerico_igual(
        entorno.get("mediciones_completas"), [1.2, 0.0, 2.4, 3.6, 0.0]
    ):
        return "sustituye cada NaN por 0 mediante np.where()."
    return True


def _validar_q10(entorno):
    precios = entorno.get("precios_activos")
    esperados_precios = [
        [100.0, 102.0, 101.0, 104.0, 105.0],
        [50.0, 49.0, 48.0, 47.0, 46.0],
        [200.0, 200.0, 200.0, 200.0, 200.0],
    ]
    if not _array_numerico_igual(precios, esperados_precios):
        return "no modifiques precios_activos."

    precios_array = np.asarray(esperados_precios)
    retornos_esperados = precios_array[:, 1:] / precios_array[:, :-1] - 1
    if not _array_numerico_igual(entorno.get("retornos"), retornos_esperados):
        return "calcula los cambios relativos entre columnas consecutivas."

    medias = np.mean(retornos_esperados, axis=1)
    if not _array_numerico_igual(entorno.get("media_por_fila"), medias):
        return "calcula la media de cada fila con axis=1."

    desviaciones = np.std(retornos_esperados, axis=1)
    if not _array_numerico_igual(
        entorno.get("desviacion_por_fila"), desviaciones
    ):
        return "calcula la desviación estándar de cada fila."

    if not _array_numerico_igual(
        entorno.get("positivos_por_fila"), [3, 0, 0]
    ):
        return "cuenta por fila cuántos cambios son mayores que 0."

    if not _array_exacto_igual(
        entorno.get("clasificacion"),
        ["Media positiva", "Media no positiva", "Media no positiva"],
    ):
        return "clasifica cada media mediante np.where()."
    return True


def cargar(entorno):
    """Carga en el notebook las preguntas de la lección."""

    ejercicios = [
        Ejercicio(1, entorno, _validar_q1),
        Ejercicio(
            2,
            entorno,
            _validar_q2,
            "Llama a reshape(3, 4) sobre datos. Después consulta shape, size, "
            "ndim y dtype en la matriz resultante.",
            "matriz = datos.reshape(3, 4)\n"
            "forma = matriz.shape\n"
            "total = matriz.size\n"
            "dimensiones = matriz.ndim\n"
            "tipo = matriz.dtype",
        ),
        Ejercicio(
            3,
            entorno,
            _validar_q3,
            "Utiliza los índices 0 y -1. El slice 1:4 selecciona las tres "
            "posiciones centrales; llama después a copy().",
            "primer_precio = precios[0]\n"
            "ultimo_precio = precios[-1]\n"
            "precios_centrales = precios[1:4].copy()",
        ),
        Ejercicio(
            4,
            entorno,
            _validar_q4,
            "Aplica directamente entre a y b los operadores +, -, *, /, // y "
            "%. Para los cuadrados, utiliza ** 2.",
            "sumas = a + b\n"
            "diferencias = a - b\n"
            "productos = a * b\n"
            "cocientes = a / b\n"
            "divisiones_enteras = a // b\n"
            "restos = a % b\n"
            "cuadrados = a ** 2",
        ),
        Ejercicio(
            5,
            entorno,
            _validar_q5,
            "+ y * actúan elemento a elemento. Multiplica por 2 para obtener "
            "doble_a, utiliza @ para el producto matricial y .T para transponer.",
            "suma_matrices = matriz_a + matriz_b\n"
            "doble_a = matriz_a * 2\n"
            "producto_elemento = matriz_a * matriz_b\n"
            "producto_matricial = matriz_a @ matriz_b\n"
            "transpuesta_a = matriz_a.T",
        ),
        Ejercicio(
            6,
            entorno,
            _validar_q6,
            "precios[1:] contiene todos los valores salvo el primero y "
            "precios[:-1] todos salvo el último. Divide ambos slices y resta 1.",
            "retornos = precios[1:] / precios[:-1] - 1\n"
            "retornos_redondeados = retornos.round(4)",
        ),
        Ejercicio(
            7,
            entorno,
            _validar_q7,
            "Compara retornos con 0. Para el intervalo combina "
            "(retornos > 0) y (retornos < 0.01) mediante &. Pasa la máscara a "
            "np.where().",
            "es_positivo = retornos > 0\n"
            "retornos_positivos = retornos[es_positivo]\n"
            "retornos_moderados = retornos[(retornos > 0) & (retornos < 0.01)]\n"
            "clasificacion = np.where(\n"
            "    es_positivo, \"Positivo\", \"No positivo\"\n"
            ")",
        ),
        Ejercicio(
            8,
            entorno,
            _validar_q8,
            "Utiliza np.mean(), np.sum() y np.std(). axis=0 trabaja por "
            "columnas y axis=1 por filas.",
            "media_total = np.mean(datos)\n"
            "suma_columnas = np.sum(datos, axis=0)\n"
            "media_filas = np.mean(datos, axis=1)\n"
            "desviacion_total = np.std(datos)",
        ),
        Ejercicio(
            9,
            entorno,
            _validar_q9,
            "Crea la máscara con np.isnan(). Utiliza ~ para invertirla, "
            "np.nanmean() para la media y np.where() para reemplazar los NaN.",
            "es_ausente = np.isnan(mediciones)\n"
            "cantidad_ausentes = np.sum(es_ausente)\n"
            "mediciones_validas = mediciones[~es_ausente]\n"
            "media_valida = np.nanmean(mediciones)\n"
            "mediciones_completas = np.where(es_ausente, 0, mediciones)",
        ),
        Ejercicio(
            10,
            entorno,
            _validar_q10,
            "Selecciona todas las filas y combina las columnas 1: con :-1. "
            "Después aplica mean(), std() y sum() con axis=1.",
            "retornos = precios_activos[:, 1:] / precios_activos[:, :-1] - 1\n"
            "media_por_fila = np.mean(retornos, axis=1)\n"
            "desviacion_por_fila = np.std(retornos, axis=1)\n"
            "positivos_por_fila = np.sum(retornos > 0, axis=1)\n"
            "clasificacion = np.where(\n"
            "    media_por_fila > 0,\n"
            "    \"Media positiva\",\n"
            "    \"Media no positiva\",\n"
            ")",
        ),
    ]

    for ejercicio in ejercicios:
        entorno[f"q{ejercicio.numero}"] = ejercicio

    print("Preparación completada.")


__all__ = ["cargar"]

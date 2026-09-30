"""Funciones de limpieza del proyecto."""
import numpy as np
import pandas as pd

def limpiar(df: pd.DataFrame) -> pd.DataFrame:
   # Crear una copia para no modificar el DataFrame original
    df = df.copy()

    # Quitar filas duplicadas
    df = df.drop_duplicates()

    # Quitar valores nulos
    df = df.dropna()

    # Quitar valores atípicos extremos del ingreso usando IQR
    q1 = df["ingreso"].quantile(0.25)
    q3 = df["ingreso"].quantile(0.75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    df = df[
        (df["ingreso"] >= limite_inferior) &
        (df["ingreso"] <= limite_superior)
    ]

    return df



def agregar_variables(df: pd.DataFrame) -> pd.DataFrame:
    # Crear una copia
    df = df.copy()

    # Crear el logaritmo del ingreso
    df["log_ingreso"] = np.log1p(df["ingreso"])

    # Crear grupos de edad
    df["grupo_edad"] = pd.cut(
        df["edad"],
        bins=[17, 29, 44, 65],
        labels=["Joven", "Adulto", "Mayor"]
    )

    return df

def anonimizar(df: pd.DataFrame, sal: str) -> pd.DataFrame:
    df = df.copy()

    # Eliminar identificadores directos
    df = df.drop(columns=["nombre", "fecha_nac"])

    # Seudonimizar la cédula
    import hashlib
    df["cedula"] = df["cedula"].apply(
        lambda x: hashlib.sha256((sal + str(x)).encode()).hexdigest()[:12]
    )

    # Generalizar edad
    df["edad"] = (df["edad"] // 10 * 10).astype(str) + "-" + \
                 (df["edad"] // 10 * 10 + 9).astype(str)

    # Redondear ingreso
    df["ingreso"] = df["ingreso"].round(-1)

    return df

# Funciones preparadas para limpieza y anonimización de datos.

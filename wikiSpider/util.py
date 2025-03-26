import pandas as pd


def clean_date(date_str):
    """
    Función para uniformizar fechas a formato yyyy-MM-dd HH:mm:ss
    """
    return pd.to_datetime(date_str)

def clean_body(body_str):
    """
    Unir el texto extraído y limpiar saltos de línea
    """
    
    clean_text = "".join(body_str).replace("\n", " ").strip()
    return clean_text

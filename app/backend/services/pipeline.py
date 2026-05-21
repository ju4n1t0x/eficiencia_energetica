"""
Pipeline de limpieza y validación de datos.
Traduce el proceso del notebook a código de producción.
"""
import pandas as pd


class PipelineDemanda:

    COLUMNAS_REQUERIDAS = {
        "anio", "mes", "agente_nemo", "agente_descripcion",
        "tipo_agente", "region", "provincia", "categoria_area",
        "categoria_demanda", "tarifa", "categoria_tarifa", "demanda_mwh"
    }

    COLUMNAS_DESCARTAR = [
        "Unnamed: 0", "indice_tiempo", "fecha_proceso", "lote_id_log", "id"
    ]

    MAP_ESTACION = {
        12: "VERANO", 1: "VERANO",  2: "VERANO",
        3:  "OTONO",  4: "OTONO",   5: "OTONO",
        6:  "INVIERNO", 7: "INVIERNO", 8: "INVIERNO",
        9:  "PRIMAVERA", 10: "PRIMAVERA", 11: "PRIMAVERA",
    }

    def __init__(self):
        self.stats = {}

    def limpiar(self, df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        """
        Recibe un DataFrame crudo y devuelve:
        - DataFrame limpio listo para insertar en la DB
        - Diccionario con estadísticas del proceso
        """
        self.stats = {
            "registros_originales": len(df),
            "registros_insertados": 0,
            "registros_descartados": 0,
            "detalle": [],
        }

        df = self._normalizar_columnas(df)
        df = self._descartar_columnas(df)
        self._validar_columnas(df)
        df = self._eliminar_duplicados(df)
        df = self._eliminar_nulos(df)
        df = self._filtrar_demanda_invalida(df)
        df = self._agregar_estacion(df)
        df = self._seleccionar_columnas_finales(df)

        self.stats["registros_insertados"] = len(df)
        self.stats["registros_descartados"] = (
            self.stats["registros_originales"] - len(df)
        )

        return df, self.stats

    def _normalizar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.lower().str.strip()
        for col in df.columns:
            if col.lower() == "demanda_mwh" and col != "demanda_mwh":
                df = df.rename(columns={col: "demanda_mwh"})
                break
        # Normalización igual que notebook celda 88
        cols_texto = df.select_dtypes(include="object").columns
        for col in cols_texto:
            df[col] = (
                df[col]
                .astype(str)
                .str.normalize('NFKD')
                .str.encode('ascii', errors='ignore')
                .str.decode('utf-8')
                .str.upper()
                .str.strip()
                .str.replace(r'[.\-\/]', ' ', regex=True)
                .str.replace(r'\s+', ' ', regex=True)
            )
        return df

    def _descartar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(
            columns=[c for c in self.COLUMNAS_DESCARTAR if c in df.columns],
            errors="ignore"
        )

    def _validar_columnas(self, df: pd.DataFrame):
        faltantes = self.COLUMNAS_REQUERIDAS - set(df.columns)
        if faltantes:
            raise ValueError(f"El CSV no tiene las columnas requeridas: {faltantes}")

    def _eliminar_duplicados(self, df: pd.DataFrame) -> pd.DataFrame:
        antes = len(df)
        df = df.drop_duplicates()
        self.stats["detalle"].append(f"Duplicados eliminados: {antes - len(df)}")
        return df

    def _eliminar_nulos(self, df: pd.DataFrame) -> pd.DataFrame:
        antes = len(df)
        df = df.dropna(subset=list(self.COLUMNAS_REQUERIDAS))
        self.stats["detalle"].append(f"Filas con nulos eliminadas: {antes - len(df)}")
        return df

    def _filtrar_demanda_invalida(self, df: pd.DataFrame) -> pd.DataFrame:
        antes = len(df)
        df = df[df["demanda_mwh"] >= 0]
        self.stats["detalle"].append(f"Demanda <= 0 eliminada: {antes - len(df)}")
        return df

    def _agregar_estacion(self, df: pd.DataFrame) -> pd.DataFrame:
        if "estacion" not in df.columns:
            df["estacion"] = df["mes"].map(self.MAP_ESTACION)
        return df

    def _seleccionar_columnas_finales(self, df: pd.DataFrame) -> pd.DataFrame:
        columnas = list(self.COLUMNAS_REQUERIDAS) + ["estacion"]
        return df[columnas].reset_index(drop=True)
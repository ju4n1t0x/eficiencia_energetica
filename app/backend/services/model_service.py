"""
Servicio de ML - entrena, evalúa y sirve el modelo Gradient Boosting.
Se inicializa al startup de la app y se re-entrena cuando CAMMESA sube datos nuevos.
"""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings


class ModeloEficienciaEnergetica:

    FEATURES_CATEGORICAS = [
        "tipo_agente", "region", "provincia",
        "categoria_area", "categoria_demanda",
        "categoria_tarifa", "estacion"
    ]
    FEATURES_NUMERICAS = ["anio", "mes"]
    TARGET = "demanda_mwh"

    def __init__(self):
        self.model: GradientBoostingRegressor | None = None
        self.encoders: dict[str, LabelEncoder] = {}
        self.is_ready: bool = False
        self.model_path: str = settings.MODEL_PATH
        self.encoders_path: str = settings.ENCODERS_PATH

    # -------------------------
    # Públicos
    # -------------------------

    def get_status(self) -> dict:
        return {
            "modelo_listo": self.is_ready,
            "modelo_path": self.model_path,
            "modelo_existe": os.path.exists(self.model_path),
        }

    async def init(self, db: AsyncSession):
        """
        Se llama al startup. Si existe el .joblib lo carga,
        si no entrena desde la DB.
        """
        if (
            os.path.exists(self.model_path)
            and os.path.exists(self.encoders_path)
        ):
            print("[ModeloEficienciaEnergetica] Cargando modelo existente desde disco...")
            self._cargar_desde_disco()
        else:
            print("[ModeloEficienciaEnergetica] No se encontró modelo, verificando datos en DB...")
            df = await self._cargar_datos_db(db)
            if len(df) == 0:
                print("[ModeloEficienciaEnergetica] DB vacía, esperando carga de datos.")
                self.is_ready = False
            else:
                await self.entrenar(db)
                await self.entrenar(db)

    async def entrenar(self, db: AsyncSession) -> dict:
        """
        Carga datos de la DB, entrena el modelo y lo persiste en disco.
        Devuelve las métricas del entrenamiento.
        """
        print("[ModeloEficienciaEnergetica] Cargando datos desde DB...")
        df = await self._cargar_datos_db(db)
        print(f"[ModeloEficienciaEnergetica] {len(df)} registros cargados.")

        X_train, X_test, y_train, y_test = self._preparar_sets(df, fit=True)

        print("[ModeloEficienciaEnergetica] Entrenando Gradient Boosting...")
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            random_state=42,
        )
        self.model.fit(X_train, y_train)

        metricas = self._calcular_metricas(y_test, self.model.predict(X_test))
        print(f"[ModeloEficienciaEnergetica] Métricas: {metricas}")

        self._guardar_en_disco()
        self.is_ready = True

        return metricas

    def predecir(self, input_data: dict) -> float:
        """
        Recibe un diccionario con los features y devuelve la predicción en MWh.
        """
        if not self.is_ready:
            raise RuntimeError("El modelo no está listo todavía.")

        df = pd.DataFrame([input_data])
        X = self._encodear(df, fit=False)
        prediccion = self.model.predict(X)
        return round(float(prediccion[0]), 4)

    def get_feature_importance(self) -> dict:
        """Devuelve la importancia de cada feature del modelo entrenado."""
        if not self.is_ready:
            raise RuntimeError("El modelo no está listo todavía.")

        features = self.FEATURES_CATEGORICAS + self.FEATURES_NUMERICAS
        importancias = self.model.feature_importances_
        return dict(sorted(
            zip(features, importancias),
            key=lambda x: x[1],
            reverse=True
        ))

    # -------------------------
    # Privados
    # -------------------------

    async def _cargar_datos_db(self, db: AsyncSession) -> pd.DataFrame:
        result = await db.execute(text("""
            SELECT anio, mes, tipo_agente, region, provincia,
                   categoria_area, categoria_demanda,
                   categoria_tarifa, estacion, demanda_mwh
            FROM registros_demanda
        """))
        rows = result.fetchall()
        return pd.DataFrame(rows, columns=[
            "anio", "mes", "tipo_agente", "region", "provincia",
            "categoria_area", "categoria_demanda",
            "categoria_tarifa", "estacion", "demanda_mwh"
        ])

    def _preparar_sets(self, df: pd.DataFrame, fit: bool):
        X = self._encodear(df, fit=fit)
        y = df[self.TARGET]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def _encodear(self, df: pd.DataFrame, fit: bool) -> pd.DataFrame:
        df = df.copy()
        for col in self.FEATURES_CATEGORICAS:
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.encoders[col] = le
            else:
                df[col] = self.encoders[col].transform(df[col].astype(str))
        return df[self.FEATURES_CATEGORICAS + self.FEATURES_NUMERICAS]

    def _calcular_metricas(self, y_true, y_pred) -> dict:
        return {
            "r2": round(float(r2_score(y_true, y_pred)), 4),
            "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
            "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4),
        }

    def _guardar_en_disco(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.encoders, self.encoders_path)
        print(f"[ModeloEficienciaEnergetica] Modelo guardado en {self.model_path}")

    def _cargar_desde_disco(self):
        self.model = joblib.load(self.model_path)
        self.encoders = joblib.load(self.encoders_path)
        self.is_ready = True
        print("[ModeloEficienciaEnergetica] Modelo cargado OK.")


# Instancia global - se usa en main.py y en los endpoints
modelo = ModeloEficienciaEnergetica()
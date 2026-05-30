# Eficiencia Energética — Análisis y Predicción de Demanda Eléctrica

> Trabajo Práctico Integrador · Ingeniería del Software · Universidad del Gran Rosario

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Gradient%20Boosting-F7931E)](https://scikit-learn.org/)

---

## Descripción

Este proyecto aplica la metodología **CRISP-DM** sobre datos históricos de demanda energética del Mercado Eléctrico Mayorista (MEM) argentino, publicados por **CAMMESA**. El objetivo es identificar patrones de consumo y construir un modelo predictivo de demanda mensual en MWh.

Como entrega complementaria, se desarrolló una **herramienta web full-stack** que replica el análisis exploratorio del notebook Colab y expone el modelo como servicio REST, permitiendo predicciones en tiempo real desde una interfaz gráfica.

---

## Integrantes — Grupo 34

| Nombre | GitHub |
|--------|--------|
| Ivan Porcari | — |
| Marcelo Saucedo | — |
| Rodrigo Zamora | — |
| Gaspar Giannitrapani | — |
| Stefania Martos | — |
| Juan Ignacio Sasia | — |
| Juan José Muñoz Franchi | [@ju4n1t0x](https://github.com/ju4n1t0x) |
| Jorge Nicolás Segovia | — |

### Docentes

- **Ing. Ignacio Sanseovich**
- **Lic. Briant Gauna**

**Materia:** Ingeniería del Software · **Universidad del Gran Rosario (UGR)**

---

## Resultados principales

| Métrica | Valor |
|---------|-------|
| Algoritmo | Gradient Boosting Regressor |
| R² Score (test) | **0.929** |
| Registros analizados | 40.388 |
| Período | 2017 – 2020 |
| Provincias cubiertas | 22 |

---

## Estructura del repositorio

```
eficiencia_energetica/
├── 00_documentacion/          # Documentación completa del proyecto
│   └── documentacion.md
├── 01_notebooks/              # Notebook Colab (entrega principal)
│   └── TPI_Energia_CRISP_DM.ipynb
├── 02_data/                   # Datasets (raw y procesados)
├── 03_outputs/                # Figuras y tablas generadas
│   ├── figures/
│   └── tables/
├── app/                       # Aplicación web
│   ├── backend/               # FastAPI + PostgreSQL + ML
│   │   ├── api/               # Endpoints REST
│   │   ├── services/          # Pipeline de datos y modelo
│   │   ├── repositories/      # Queries a la base de datos
│   │   └── main.py
│   ├── frontend/              # React + TypeScript
│   │   └── src/
│   │       ├── pages/         # Vistas (EDA, Predicción, Docs, Carga)
│   │       └── components/    # NavBar, Footer, Login, etc.
│   └── docker-compose.yml
└── README.md
```

---

## Arquitectura de la aplicación

```
Frontend (React + TypeScript)
        │  HTTP/REST
Backend (FastAPI + Python)
        │  SQLAlchemy async
PostgreSQL Database
```

### Páginas de la aplicación

| Ruta | Descripción |
|------|-------------|
| `/eda` | Dashboard interactivo con gráficos del análisis exploratorio |
| `/predict` | Formulario de predicción de demanda en MWh |
| `/docs` | Documentación del proyecto (metodología, modelo, resultados) |
| `/upload` | Carga de nuevo dataset CSV (requiere autenticación) |

---

## Cómo correr el proyecto localmente

### Requisitos

- Docker y Docker Compose
- Node.js 20+ y pnpm (solo para desarrollo frontend sin Docker)
- Python 3.12+ y uv (solo para desarrollo backend sin Docker)

### Con Docker (recomendado)

```bash
cd app
cp backend/.env.example backend/.env   # configurar variables
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend (API): http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### Sin Docker

**Backend:**
```bash
cd app/backend
uv sync
uv run python seed_data.py        # cargar datos iniciales
uv run uvicorn main:app --reload
```

**Frontend:**
```bash
cd app/frontend
pnpm install
pnpm run dev
```

---

## API Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/eda/resumen` | Estadísticas generales |
| `GET` | `/api/v1/eda/demanda-mensual` | Serie temporal mensual |
| `GET` | `/api/v1/eda/demanda-por-estacion` | Demanda por estación |
| `GET` | `/api/v1/eda/demanda-por-categoria` | Demanda por categoría |
| `GET` | `/api/v1/modelos/importancia-features` | Importancia de variables |
| `GET` | `/api/v1/modelos/catalogos` | Catálogos para formulario |
| `POST` | `/api/v1/modelos/predecir` | Predicción de demanda |
| `POST` | `/api/v1/dataset/upload` | Carga CSV + re-entrenamiento |
| `POST` | `/api/v1/auth/login` | Login JWT |
| `POST` | `/api/v1/auth/registro` | Registro de usuario |

Documentación interactiva disponible en `/docs` (Swagger UI) y `/redoc` (ReDoc).

---

## Metodología

El proyecto sigue las fases de **CRISP-DM**:

1. **Comprensión del negocio** — Definición del problema y objetivos
2. **Comprensión de los datos** — Exploración y diccionario de datos CAMMESA
3. **Preparación de los datos** — Pipeline de limpieza y encoding
4. **Exploración (EDA)** — Análisis temporal, estacional y por categoría
5. **Modelado** — Gradient Boosting Regressor (R² = 0.929)
6. **Evaluación** — Validación en conjunto de prueba
7. **Implantación** — Aplicación web full-stack con Docker

---

## Licencia

Proyecto académico — Universidad del Gran Rosario, 2026. Todos los derechos reservados al Grupo 34.

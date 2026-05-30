import './DocsPage.css'

interface SectionProps {
  id: string
  title: string
  children: React.ReactNode
}

function Section({ id, title, children }: SectionProps) {
  return (
    <section className="doc-section" id={id}>
      <h2 className="doc-section-title">{title}</h2>
      <div className="doc-section-body">{children}</div>
    </section>
  )
}

interface MetricCardProps {
  label: string
  value: string
  color?: string
}

function MetricCard({ label, value, color = '#FFB627' }: MetricCardProps) {
  return (
    <div className="metric-card">
      <span className="metric-value" style={{ color }}>{value}</span>
      <span className="metric-label">{label}</span>
    </div>
  )
}

export default function DocsPage() {
  return (
    <div className="docs-container">
      <header className="docs-header">
        <h1>Documentación del Proyecto</h1>
        <p className="docs-subtitle">
          Análisis de Eficiencia Energética · Metodología CRISP-DM · Universidad del Gran Rosario
        </p>
      </header>

      <nav className="docs-toc">
        <p className="toc-title">Índice</p>
        <ul>
          <li><a href="#negocio">1. Comprensión del Negocio</a></li>
          <li><a href="#datos">2. Comprensión de los Datos</a></li>
          <li><a href="#preparacion">3. Preparación de los Datos</a></li>
          <li><a href="#eda">4. Exploración de los Datos (EDA)</a></li>
          <li><a href="#modelo">5. Modelado</a></li>
          <li><a href="#evaluacion">6. Evaluación</a></li>
          <li><a href="#implantacion">7. Implantación</a></li>
          <li><a href="#conclusiones">8. Conclusiones</a></li>
          <li><a href="#equipo">9. Equipo</a></li>
        </ul>
      </nav>

      <div className="docs-content">

        <Section id="negocio" title="1. Comprensión del Negocio">
          <p>
            El consumo energético es una variable crítica tanto para distribuidoras eléctricas como para
            organismos de planificación. Cuando la demanda aumenta en ciertos períodos, es necesario
            anticipar recursos, reforzar infraestructura y tomar decisiones operativas con mayor información.
          </p>
          <h3>Problema identificado</h3>
          <p>
            La dificultad para anticipar períodos de mayor demanda energética a partir de datos históricos.
            Si bien existen registros de consumo de CAMMESA, estos datos por sí solos no son fáciles de
            interpretar ni de usar para proyecciones.
          </p>
          <h3>Objetivo general</h3>
          <p>
            Analizar datos históricos de demanda energética para identificar patrones de consumo y construir
            un modelo que permita estimar la demanda mensual (en MWh) a partir de variables conocidas.
          </p>
          <h3>Objetivos específicos</h3>
          <ul>
            <li>Analizar la evolución de la demanda a lo largo del tiempo (2017–2020).</li>
            <li>Identificar variaciones de consumo por año, mes y estación.</li>
            <li>Comparar el comportamiento de la demanda según categorías del dataset.</li>
            <li>Detectar patrones y tendencias relevantes.</li>
            <li>Construir un modelo predictivo de regresión y evaluar su rendimiento.</li>
            <li>Desplegar una herramienta web que replique el análisis y permita hacer predicciones.</li>
          </ul>
          <h3>Stakeholders</h3>
          <ul>
            <li>Consumidores finales</li>
            <li>Distribuidoras eléctricas</li>
            <li>Gobierno y organismos reguladores</li>
            <li>Equipos técnicos y operativos del MEM</li>
          </ul>
        </Section>

        <Section id="datos" title="2. Comprensión de los Datos">
          <h3>Fuente de datos</h3>
          <p>
            El dataset proviene de <strong>CAMMESA</strong> (Compañía Administradora del Mercado Mayorista
            Eléctrico S.A.), la empresa responsable de administrar y operar el Mercado Eléctrico Mayorista
            (MEM) en Argentina.
          </p>
          <div className="info-box">
            <strong>Dataset:</strong> demanda-últimos-años.csv
            <br />
            <strong>Período cubierto:</strong> Enero 2017 – Diciembre 2020
            <br />
            <strong>Unidad de medida:</strong> Megavatios-hora (MWh) por mes y por agente
          </div>
          <h3>Descripción del dataset</h3>
          <div className="metrics-row">
            <MetricCard label="Registros totales" value="40.388" />
            <MetricCard label="Columnas" value="16" color="#4A90D9" />
            <MetricCard label="Años cubiertos" value="4" color="#2ECC71" />
            <MetricCard label="Agentes únicos" value="564" color="#7B68EE" />
          </div>
          <h3>Diccionario de datos (variables principales)</h3>
          <div className="table-wrapper">
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Campo</th>
                  <th>Descripción</th>
                  <th>Tipo</th>
                  <th>Uso</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>anio</td><td>Año de la medición</td><td>int</td><td>Feature / análisis</td></tr>
                <tr><td>mes</td><td>Mes de la medición (1–12)</td><td>int</td><td>Feature / análisis</td></tr>
                <tr><td>agente_nemo</td><td>Identificador del agente del MEM</td><td>str</td><td>Identificación</td></tr>
                <tr><td>tipo_agente</td><td>Tipo de agente (Distribuidora, Gran Demandante, etc.)</td><td>str</td><td>Feature</td></tr>
                <tr><td>region</td><td>Región geográfica</td><td>str</td><td>Feature</td></tr>
                <tr><td>provincia</td><td>Provincia donde se registra el consumo</td><td>str</td><td>Feature</td></tr>
                <tr><td>categoria_area</td><td>Categoría geográfica del área</td><td>str</td><td>Feature</td></tr>
                <tr><td>categoria_demanda</td><td>Tipo de categoría de demanda</td><td>str</td><td>Feature</td></tr>
                <tr><td>categoria_tarifa</td><td>Categoría tarifaria del agente</td><td>str</td><td>Feature</td></tr>
                <tr><td>estacion</td><td>Estación del año (verano, otoño, invierno, primavera)</td><td>str</td><td>Feature</td></tr>
                <tr><td>demanda_mwh</td><td>Demanda eléctrica mensual en MWh</td><td>float</td><td>Target</td></tr>
              </tbody>
            </table>
          </div>
        </Section>

        <Section id="preparacion" title="3. Preparación de los Datos">
          <p>
            Antes de modelar, los datos fueron sometidos a un proceso de limpieza y transformación
            implementado mediante un pipeline reutilizable (<code>PipelineDemanda</code>) que garantiza
            la reproducibilidad del proceso.
          </p>
          <h3>Pasos aplicados</h3>
          <ul>
            <li>Eliminación de columnas irrelevantes para el modelo (IDs internos, campos redundantes).</li>
            <li>Conversión de variables categóricas mediante <strong>One-Hot Encoding</strong>.</li>
            <li>Verificación y tratamiento de valores nulos (el dataset original no presentó nulos significativos).</li>
            <li>Derivación de la columna <code>estacion</code> a partir del mes para capturar estacionalidad.</li>
            <li>División en conjuntos de entrenamiento (80%) y prueba (20%) con semilla fija para reproducibilidad.</li>
          </ul>
          <div className="info-box">
            El pipeline fue implementado como clase Python (<code>PipelineDemanda</code>) en el backend
            para garantizar que cualquier dataset nuevo sea procesado de la misma forma antes del
            re-entrenamiento del modelo.
          </div>
        </Section>

        <Section id="eda" title="4. Exploración de los Datos (EDA)">
          <p>
            El análisis exploratorio permitió identificar patrones temporales, estacionales y
            estructurales en los datos de demanda energética del MEM argentino.
          </p>
          <h3>Demanda total por año</h3>
          <p>
            La demanda total muestra una tendencia relativamente estable entre 2017 y 2019, con
            una caída notable en 2020, posiblemente vinculada al impacto de la pandemia COVID-19
            en la actividad industrial y comercial.
          </p>
          <h3>Estacionalidad</h3>
          <p>
            Se observa un patrón claro de variación estacional: la demanda es mayor en <strong>invierno</strong>
            (pico de calefacción) y <strong>verano</strong> (pico de refrigeración), mientras que otoño
            y primavera presentan los valores más bajos. Este patrón es consistente a lo largo de todos
            los años analizados.
          </p>
          <h3>Distribución por categoría</h3>
          <p>
            Las <strong>Distribuidoras</strong> concentran la mayor parte de la demanda total del sistema,
            seguidas por los Grandes Demandantes. Las categorías residenciales muestran mayor sensibilidad
            estacional que las industriales.
          </p>
          <h3>Hipótesis validadas</h3>
          <div className="hypothesis-grid">
            <div className="hypothesis-card confirmed">
              <span className="hyp-badge">✓ Confirmada</span>
              <p><strong>H1:</strong> Existe variación estacional significativa en la demanda energética.
                El invierno y verano concentran los picos de consumo.</p>
            </div>
            <div className="hypothesis-card confirmed">
              <span className="hyp-badge">✓ Confirmada</span>
              <p><strong>H2:</strong> La categoría de demanda influye en el nivel de consumo.
                Distribuidoras y Grandes Demandantes lideran el consumo total.</p>
            </div>
          </div>
        </Section>

        <Section id="modelo" title="5. Modelado">
          <h3>Algoritmo seleccionado</h3>
          <p>
            Tras evaluar múltiples modelos de regresión (Regresión Lineal, Random Forest, Gradient Boosting),
            se seleccionó el <strong>Gradient Boosting Regressor</strong> de scikit-learn por su mejor
            desempeño en los datos de prueba.
          </p>
          <div className="info-box">
            <strong>Algoritmo:</strong> Gradient Boosting Regressor (scikit-learn)
            <br />
            <strong>Hiperparámetros:</strong> n_estimators=100 · learning_rate=0.1 · max_depth=4 · random_state=42
          </div>
          <h3>Features utilizadas</h3>
          <p>Las variables de entrada al modelo incluyen:</p>
          <ul>
            <li><strong>Numéricas:</strong> año, mes</li>
            <li><strong>Categóricas (OHE):</strong> tipo_agente, región, provincia, categoría_área,
              categoría_demanda, categoría_tarifa, estación</li>
          </ul>
          <h3>Importancia de features</h3>
          <p>
            El tipo de agente y la categoría de demanda resultaron las variables más influyentes
            en las predicciones del modelo, lo que es coherente con el análisis exploratorio previo.
            La estación del año también mostró un peso relevante, confirmando la hipótesis de estacionalidad.
          </p>
        </Section>

        <Section id="evaluacion" title="6. Evaluación">
          <div className="metrics-row">
            <MetricCard label="R² Score" value="0.929" color="#2ECC71" />
            <MetricCard label="Algoritmo" value="Gradient Boosting" color="#4A90D9" />
            <MetricCard label="Train/Test split" value="80% / 20%" color="#7B68EE" />
          </div>
          <p style={{ marginTop: '1.5rem' }}>
            El modelo alcanzó un coeficiente de determinación (<strong>R²</strong>) de <strong>0.929</strong>
            sobre el conjunto de prueba, lo que indica que explica aproximadamente el 92.9% de la varianza
            en la demanda energética. Este resultado es considerado satisfactorio para el objetivo del proyecto.
          </p>
          <h3>Criterios de éxito alcanzados</h3>
          <ul>
            <li>R² superior a 0.85 en el conjunto de prueba. ✓</li>
            <li>El modelo generaliza correctamente sin signos de sobreajuste severo. ✓</li>
            <li>Las predicciones son coherentes con el análisis exploratorio previo. ✓</li>
          </ul>
          <h3>Limitaciones</h3>
          <ul>
            <li>El modelo fue entrenado con datos 2017–2020; puede degradarse con años muy diferentes.</li>
            <li>No incluye variables climáticas externas (temperatura, precipitaciones) que podrían mejorar la precisión.</li>
            <li>El dataset no contiene información sobre interrupciones del servicio, por lo que no permite predecir cortes.</li>
          </ul>
        </Section>

        <Section id="implantacion" title="7. Implantación">
          <p>
            Como parte del trabajo, se desarrolló una <strong>aplicación web completa</strong> que replica
            el análisis del notebook y expone el modelo como servicio REST, permitiendo visualización
            interactiva de datos y predicciones en tiempo real.
          </p>
          <h3>Arquitectura de la aplicación</h3>
          <div className="arch-grid">
            <div className="arch-card">
              <span className="arch-icon">⚛️</span>
              <strong>Frontend</strong>
              <p>React + TypeScript + Recharts. SPA con navegación por rutas, dashboard EDA interactivo
                y formulario de predicción.</p>
            </div>
            <div className="arch-card">
              <span className="arch-icon">🐍</span>
              <strong>Backend</strong>
              <p>FastAPI + SQLAlchemy. API REST con endpoints de EDA, modelos y predicción. Auth con JWT.
                Pipeline de datos integrado.</p>
            </div>
            <div className="arch-card">
              <span className="arch-icon">🗄️</span>
              <strong>Base de datos</strong>
              <p>PostgreSQL con 40.388+ registros de demanda. Soporte para re-entrenamiento del modelo
                con nuevos datasets via CSV upload.</p>
            </div>
            <div className="arch-card">
              <span className="arch-icon">🐳</span>
              <strong>Infraestructura</strong>
              <p>Docker Compose para desarrollo local. Despliegue en producción mediante Coolify
                con CI/CD desde GitHub.</p>
            </div>
          </div>
          <h3>Endpoints principales</h3>
          <div className="table-wrapper">
            <table className="doc-table">
              <thead>
                <tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr>
              </thead>
              <tbody>
                <tr><td><span className="badge get">GET</span></td><td>/api/v1/eda/resumen</td><td>Estadísticas generales del dataset</td></tr>
                <tr><td><span className="badge get">GET</span></td><td>/api/v1/eda/demanda-mensual</td><td>Serie temporal de demanda por mes/año</td></tr>
                <tr><td><span className="badge get">GET</span></td><td>/api/v1/eda/demanda-por-estacion</td><td>Demanda promedio por estación del año</td></tr>
                <tr><td><span className="badge get">GET</span></td><td>/api/v1/eda/demanda-por-categoria</td><td>Demanda total por categoría de demanda</td></tr>
                <tr><td><span className="badge get">GET</span></td><td>/api/v1/modelos/importancia-features</td><td>Importancia de variables del modelo</td></tr>
                <tr><td><span className="badge get">GET</span></td><td>/api/v1/modelos/catalogos</td><td>Valores válidos para el formulario de predicción</td></tr>
                <tr><td><span className="badge post">POST</span></td><td>/api/v1/modelos/predecir</td><td>Realiza una predicción de demanda en MWh</td></tr>
                <tr><td><span className="badge post">POST</span></td><td>/api/v1/dataset/upload</td><td>Carga un nuevo CSV y re-entrena el modelo</td></tr>
              </tbody>
            </table>
          </div>
        </Section>

        <Section id="conclusiones" title="8. Conclusiones">
          <p>
            El proyecto permitió aplicar de forma integral la metodología CRISP-DM sobre un problema
            real de análisis de demanda energética en Argentina.
          </p>
          <p>
            Se logró construir un modelo de Gradient Boosting con un R² de 0.929, lo que representa
            una capacidad predictiva sólida. El análisis exploratorio confirmó la existencia de
            patrones estacionales claros y una fuerte influencia del tipo de agente y categoría
            en el nivel de consumo.
          </p>
          <p>
            La herramienta web desarrollada replica el análisis del notebook y lo hace accesible
            a través de una interfaz interactiva, demostrando la viabilidad de implementar un
            sistema de este tipo en un contexto real de producción.
          </p>
          {/* <div className="info-box">
            Como trabajo futuro se propone incorporar variables climáticas (temperatura, humedad)
            que podrían incrementar significativamente la precisión del modelo, así como extender
            el período de datos más allá de 2020.
          </div> */}
        </Section>

        <Section id="equipo" title="9. Equipo">
          <div className="team-grid">
            {[
              'Ivan Porcari',
              'Marcelo Saucedo',
              'Rodrigo Zamora',
              'Gaspar Giannitrapani',
              'Stefania Martos',
              'Juan Ignacio Sasia',
              'Juan José Muñoz Franchi',
              'Jorge Nicolás Segovia',
            ].map((name) => (
              <div key={name} className="team-card">
                <div className="team-avatar">{name.charAt(0)}</div>
                <span>{name}</span>
              </div>
            ))}
          </div>
          <div className="course-info">
            <p><strong>Materia:</strong> Ingeniería del Software</p>
            <p><strong>Docentes:</strong> Ing. Ignacio Sanseovich · Lic. Briant Gauna</p>
            <p><strong>Universidad:</strong> Universidad del Gran Rosario (UGR)</p>
            <p><strong>Grupo:</strong> 34</p>
          </div>
        </Section>

      </div>
    </div>
  )
}

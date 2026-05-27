import { useEffect, useState } from 'react'
import {
  BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts'
import { login, fetchDashboardData, type DashboardData } from '../api'
import ChartCard from '../components/ChartCard'
import StatCard from '../components/StatCard'
import './EdaPage.css'


// ── Constantes ─────────────────────────────────────────────────────────────

const MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

const TOOLTIP_STYLE = {
  contentStyle: { background: '#1a1a2e', border: '1px solid #2a2a3a', borderRadius: 8 },
}

const AXIS_TICK = { fill: '#aaa', fontSize: 11 }

// ── Transformaciones de datos ──────────────────────────────────────────────

function agruparPorAnio(mensual: DashboardData['mensual']) {
  const acum: Record<number, { anio: string; demanda_total: number }> = {}
  for (const { anio, demanda_total } of mensual) {
    if (!acum[anio]) acum[anio] = { anio: String(anio), demanda_total: 0 }
    acum[anio].demanda_total += demanda_total
  }
  return Object.values(acum)
}

function buildSerieMensual(mensual: DashboardData['mensual']) {
  return mensual.map(({ anio, mes, demanda_total }) => ({
    label: `${anio}-${MESES[mes - 1]}`,
    demanda_total,
  }))
}

function buildImportanciaArr(importancia: DashboardData['importancia']) {
  return Object.entries(importancia)
    .map(([feature, valor]) => ({ feature, valor: Number((valor * 100).toFixed(2)) }))
    .sort((a, b) => b.valor - a.valor)
}

// ── Componentes ────────────────────────────────────────────────────────────

export default function EdaPage() {
const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    login()
      .then(fetchDashboardData)
      .then(setData)
      .catch(() => setError('No se pudo conectar con el backend. ¿Está corriendo en localhost:8000?'))
      .finally(() => setLoading(false))
  }, [])

  if (loading || !data) return <div className="center"><p>Cargando datos del backend...</p></div>
  if (error)   return <div className="center error"><p>{error}</p></div>

  const porAnio       = agruparPorAnio(data.mensual)
  const serieMensual  = buildSerieMensual(data.mensual)
  const importanciaArr = buildImportanciaArr(data.importancia)

  const fmt = (v: number) => v.toLocaleString('es-AR')

  return (
    <div className="eda-container">
      <header className="eda-header">
        <h1>Análisis de Eficiencia Energética</h1>
        <p className="subtitle">
          Visualización de demanda eléctrica y variables climáticas procesadas desde la API REST
        </p>
      </header>

      <div className="stats-grid">
        <StatCard label="Total registros"   value={fmt(data.resumen.total_registros)} />
        <StatCard label="Demanda promedio"  value={`${fmt(data.resumen.demanda_promedio)} MWh`} />
        <StatCard label="Período cubierto"  value={`${data.resumen.anio_inicio} – ${data.resumen.anio_fin}`} />
        <StatCard label="Provincias"        value={String(data.resumen.total_provincias)} />
      </div>

      <div className="charts-grid">

        <ChartCard title="Demanda total por año" endpoint="/eda/demanda-mensual">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={porAnio}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#2a2a3a" />
              <XAxis dataKey="anio" tick={AXIS_TICK} />
              <YAxis tickFormatter={(v) => `${(v / 1e6).toFixed(0)}M`} tick={AXIS_TICK} />
              <Tooltip formatter={(v) => [`${fmt(Number(v))} MWh`, 'Demanda total']} {...TOOLTIP_STYLE} />
              <Bar dataKey="demanda_total" fill="#F5A623" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Demanda mensual — serie temporal" endpoint="/eda/demanda-mensual">
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={serieMensual}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#2a2a3a" />
              <XAxis dataKey="label" tick={{ ...AXIS_TICK, fontSize: 10 }} interval={7} />
              <YAxis tickFormatter={(v) => `${(v / 1e6).toFixed(1)}M`} tick={AXIS_TICK} />
              <Tooltip formatter={(v) => [`${fmt(Number(v))} MWh`, 'Demanda']} {...TOOLTIP_STYLE} />
              <Line type="monotone" dataKey="demanda_total" stroke="#F5A623" dot={false} strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Demanda promedio por estación" endpoint="/eda/demanda-por-estacion">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.estacion}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#2a2a3a" />
              <XAxis dataKey="estacion" tick={AXIS_TICK} />
              <YAxis tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} tick={AXIS_TICK} />
              <Tooltip formatter={(v) => [`${fmt(Number(v))} MWh`, 'Promedio']} {...TOOLTIP_STYLE} />
              <Bar dataKey="demanda_promedio" fill="#4A90D9" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Demanda total por categoría" endpoint="/eda/demanda-por-categoria">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.categoria} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#2a2a3a" />
              <XAxis type="number" tickFormatter={(v) => `${(v / 1e6).toFixed(1)}M`} tick={AXIS_TICK} />
              <YAxis type="category" dataKey="categoria_demanda" width={140} tick={AXIS_TICK} />
              <Tooltip formatter={(v) => [`${fmt(Number(v))} MWh`, 'Total']} {...TOOLTIP_STYLE} />
              <Bar dataKey="demanda_total" fill="#7B68EE" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Importancia de features — Gradient Boosting" endpoint="/modelos/importancia-features">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={importanciaArr} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#2a2a3a" />
              <XAxis type="number" unit="%" tick={AXIS_TICK} />
              <YAxis type="category" dataKey="feature" width={130} tick={AXIS_TICK} />
              <Tooltip formatter={(v) => [`${fmt(Number(v))}%`, 'Importancia']} {...TOOLTIP_STYLE} />
              <Bar dataKey="valor" fill="#2ECC71" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

      </div>
    </div>
  )
}
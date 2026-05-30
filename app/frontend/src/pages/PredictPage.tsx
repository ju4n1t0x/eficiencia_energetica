import { useEffect, useState } from 'react'
import { getCatalogos, predecir, type Catalogos, type PrediccionResponse } from '../api'
import './PredictPage.css'

const MESES = [
  { val: 1, label: 'Enero' }, { val: 2, label: 'Febrero' }, { val: 3, label: 'Marzo' },
  { val: 4, label: 'Abril' }, { val: 5, label: 'Mayo' }, { val: 6, label: 'Junio' },
  { val: 7, label: 'Julio' }, { val: 8, label: 'Agosto' }, { val: 9, label: 'Septiembre' },
  { val: 10, label: 'Octubre' }, { val: 11, label: 'Noviembre' }, { val: 12, label: 'Diciembre' },
]

const ANIOS = Array.from({ length: 10 }, (_, i) => 2017 + i)

interface FormState {
  anio: number
  mes: number
  tipo_agente: string
  region: string
  provincia: string
  categoria_area: string
  categoria_demanda: string
  categoria_tarifa: string
  estacion: string
}

const EMPTY_FORM: FormState = {
  anio: 2020,
  mes: 1,
  tipo_agente: '',
  region: '',
  provincia: '',
  categoria_area: '',
  categoria_demanda: '',
  categoria_tarifa: '',
  estacion: '',
}

export default function PredictPage() {
  const [catalogos, setCatalogos] = useState<Catalogos | null>(null)
  const [loadingCat, setLoadingCat] = useState(true)
  const [form, setForm] = useState<FormState>(EMPTY_FORM)
  const [resultado, setResultado] = useState<PrediccionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getCatalogos()
      .then((data) => {
        setCatalogos(data)
        setForm((prev) => ({
          ...prev,
          tipo_agente: data.tipo_agente?.[0] ?? '',
          region: data.region?.[0] ?? '',
          provincia: data.provincia?.[0] ?? '',
          categoria_area: data.categoria_area?.[0] ?? '',
          categoria_demanda: data.categoria_demanda?.[0] ?? '',
          categoria_tarifa: data.categoria_tarifa?.[0] ?? '',
          estacion: data.estacion?.[0] ?? '',
        }))
      })
      .catch(() => setError('No se pudieron cargar los catálogos del backend.'))
      .finally(() => setLoadingCat(false))
  }, [])

  const handleChange = (field: keyof FormState, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }))
    setResultado(null)
    setError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResultado(null)
    try {
      const res = await predecir(form)
      setResultado(res)
    } catch (err: any) {
      setError(err.message || 'Error al realizar la predicción.')
    } finally {
      setLoading(false)
    }
  }

  if (loadingCat) return <div className="predict-loading"><p>Cargando catálogos...</p></div>

  return (
    <div className="predict-container">
      <header className="predict-header">
        <h1>Predicción de Demanda</h1>
        <p className="predict-subtitle">
          Estimá la demanda energética mensual usando el modelo Gradient Boosting entrenado
        </p>
      </header>

      <div className="predict-body">
        <form className="predict-form" onSubmit={handleSubmit}>

          <div className="form-row">
            <div className="form-group">
              <label>Año</label>
              <select
                value={form.anio}
                onChange={(e) => handleChange('anio', Number(e.target.value))}
              >
                {ANIOS.map((a) => <option key={a} value={a}>{a}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Mes</label>
              <select
                value={form.mes}
                onChange={(e) => handleChange('mes', Number(e.target.value))}
              >
                {MESES.map((m) => <option key={m.val} value={m.val}>{m.label}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Estación</label>
              <select
                value={form.estacion}
                onChange={(e) => handleChange('estacion', e.target.value)}
              >
                {catalogos?.estacion?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Tipo de Agente</label>
              <select
                value={form.tipo_agente}
                onChange={(e) => handleChange('tipo_agente', e.target.value)}
              >
                {catalogos?.tipo_agente?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Región</label>
              <select
                value={form.region}
                onChange={(e) => handleChange('region', e.target.value)}
              >
                {catalogos?.region?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Provincia</label>
              <select
                value={form.provincia}
                onChange={(e) => handleChange('provincia', e.target.value)}
              >
                {catalogos?.provincia?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Categoría Área</label>
              <select
                value={form.categoria_area}
                onChange={(e) => handleChange('categoria_area', e.target.value)}
              >
                {catalogos?.categoria_area?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Categoría Demanda</label>
              <select
                value={form.categoria_demanda}
                onChange={(e) => handleChange('categoria_demanda', e.target.value)}
              >
                {catalogos?.categoria_demanda?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Categoría Tarifa</label>
              <select
                value={form.categoria_tarifa}
                onChange={(e) => handleChange('categoria_tarifa', e.target.value)}
              >
                {catalogos?.categoria_tarifa?.map((v) => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>

          <button type="submit" className="predict-btn" disabled={loading}>
            {loading ? 'Calculando...' : 'Predecir Demanda'}
          </button>
        </form>

        {error && (
          <div className="predict-error">
            <p>{error}</p>
          </div>
        )}

        {resultado && (
          <div className="predict-result">
            <p className="result-label">Demanda estimada</p>
            <p className="result-value">
              {resultado.demanda_estimada_mwh.toLocaleString('es-AR', { maximumFractionDigits: 2 })}
            </p>
            <p className="result-unit">{resultado.unidad}</p>
            <p className="result-model">Modelo: {resultado.modelo}</p>
          </div>
        )}
      </div>
    </div>
  )
}

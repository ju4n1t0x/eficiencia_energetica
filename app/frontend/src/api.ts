const BASE_URL = 'http://localhost:8000/api/v1'

// ── Tipos que espejean exactamente lo que devuelve el backend ──────────────

export interface DemandaMensual {
  anio: number
  mes: number
  demanda_total: number
}

export interface DemandaEstacion {
  estacion: string
  demanda_promedio: number
  demanda_total: number
  registros: number
}

export interface DemandaCategoria {
  categoria_demanda: string
  demanda_promedio: number
  demanda_total: number
  registros: number
}

export interface Resumen {
  total_registros: number
  demanda_promedio: number
  anio_inicio: number
  anio_fin: number
  total_agentes: number
  total_provincias: number
}

export interface DashboardData {
  mensual: DemandaMensual[]
  estacion: DemandaEstacion[]
  categoria: DemandaCategoria[]
  importancia: Record<string, number>
  resumen: Resumen
}

// ── Helpers de red ─────────────────────────────────────────────────────────

async function get<T>(token: string, path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error(`Error ${res.status} en ${path}`)
  return res.json()
}

// ── API pública ────────────────────────────────────────────────────────────

export async function login(): Promise<string> {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mail: 'admin@cammesa.com', password: 'admin123' }),
  })
  if (!res.ok) throw new Error('Login fallido')
  const { access_token } = await res.json()
  return access_token
}

export async function fetchDashboardData(token: string): Promise<DashboardData> {
  const [mensual, estacion, categoria, importancia, resumen] = await Promise.all([
    get<DemandaMensual[]>(token, '/eda/demanda-mensual'),
    get<DemandaEstacion[]>(token, '/eda/demanda-por-estacion'),
    get<DemandaCategoria[]>(token, '/eda/demanda-por-categoria'),
    get<Record<string, number>>(token, '/modelos/importancia-features'),
    get<Resumen>(token, '/eda/resumen'),
  ])
  return { mensual, estacion, categoria, importancia, resumen }
}

export async function uploadDataset(token: string, file: File): Promise<any> {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${BASE_URL}/dataset/upload`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.detail || 'Error al cargar el archivo')
  }

  return res.json()
}

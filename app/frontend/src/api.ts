const BASE_URL = '/api/v1'

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

export interface RegisterData {
  nombre: string
  mail: string
  password: string
}

// ── Helpers de red ─────────────────────────────────────────────────────────

async function get<T>(token: string | undefined, path: string): Promise<T> {
  const headers: Record<string, string> = {}
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`${BASE_URL}${path}`, { headers })
  if (!res.ok) throw new Error(`Error ${res.status} en ${path}`)
  return res.json()
}

// ── API pública ───────────────────────────────────────────────────────────

export async function login(mail: string, password: string): Promise<string> {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mail, password }),
  })
  if (!res.ok) throw new Error('Credenciales inválidas')
  const { access_token } = await res.json()
  return access_token
}

export async function register(data: RegisterData): Promise<void> {
  const res = await fetch(`${BASE_URL}/auth/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombre: data.nombre,
      mail: data.mail,
      password: data.password,
    }),
  })
  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.detail || 'Error al registrar usuario')
  }
}

export async function fetchDashboardData(token?: string): Promise<DashboardData> {
  const [mensual, estacion, categoria, importancia, resumen] = await Promise.all([
    get<DemandaMensual[]>(token, '/eda/demanda-mensual'),
    get<DemandaEstacion[]>(token, '/eda/demanda-por-estacion'),
    get<DemandaCategoria[]>(token, '/eda/demanda-por-categoria'),
    get<Record<string, number>>(token, '/modelos/importancia-features'),
    get<Resumen>(token, '/eda/resumen'),
  ])
  return { mensual, estacion, categoria, importancia, resumen }
}

// ── Tipos para predicción ─────────────────────────────────────────────────

export interface Catalogos {
  tipo_agente: string[]
  region: string[]
  provincia: string[]
  categoria_area: string[]
  categoria_demanda: string[]
  tarifa: string[]
  categoria_tarifa: string[]
  estacion: string[]
}

export interface PrediccionRequest {
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

export interface PrediccionResponse {
  demanda_estimada_mwh: number
  unidad: string
  modelo: string
}

export async function getCatalogos(): Promise<Catalogos> {
  const res = await fetch(`${BASE_URL}/modelos/catalogos`)
  if (!res.ok) throw new Error('Error al obtener catálogos')
  return res.json()
}

export async function predecir(data: PrediccionRequest): Promise<PrediccionResponse> {
  const res = await fetch(`${BASE_URL}/modelos/predecir`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Error ${res.status}`)
  }
  return res.json()
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

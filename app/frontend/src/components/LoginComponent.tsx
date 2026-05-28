import { useState } from 'react'
import { login, register } from '../api'
import Toast from './Toast'
import './LoginComponent.css'

interface LoginComponentProps {
  onLogin?: () => void
}

const LoginComponent = ({ onLogin }: LoginComponentProps) => {
  const [isLogin, setIsLogin] = useState(true)
  const [nombre, setNombre] = useState('')
  const [mail, setMail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      if (isLogin) {
        const token = await login(mail, password)
        sessionStorage.setItem('token', token)
        onLogin?.()
      } else {
        await register({ nombre, mail, password })
        setIsLogin(true)
        setNombre('')
        setPassword('')
        setToast({ message: 'Registro exitoso. Ahora iniciá sesión.', type: 'success' })
      }
    } catch (err: any) {
      setError(err.message || 'Error en la operación')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-card">
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="auth-header">
        <h2 className="auth-title">
          {isLogin ? 'Iniciar Sesión' : 'Registrarse'}
        </h2>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        {!isLogin && (
          <div className="form-group">
            <label>Nombre</label>
            <input
              type="text"
              placeholder="Tu nombre"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>
        )}

        <div className="form-group">
          <label>Correo Electrónico</label>
          <input
            type="email"
            placeholder="ejemplo@correo.com"
            value={mail}
            onChange={(e) => setMail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Contraseña</label>
          <input
            type="password"
            placeholder="Tu contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="auth-error">{error}</p>}

        <button type="submit" className="auth-button" disabled={loading}>
          {loading
            ? isLogin
              ? 'INGRESANDO...'
              : 'REGISTRANDO...'
            : isLogin
            ? 'INGRESAR'
            : 'CREAR CUENTA'}
        </button>
      </form>

      <div className="auth-footer">
        <p className="auth-link">
          {isLogin ? (
            <>
              ¿No sos usuario?{' '}
              <span className="auth-toggle" onClick={() => {
                setIsLogin(false)
                setError(null)
              }}>
                Registrate acá
              </span>
            </>
          ) : (
            <>
              ¿Ya tenés cuenta?{' '}
              <span className="auth-toggle" onClick={() => {
                setIsLogin(true)
                setError(null)
              }}>
                Iniciá sesión
              </span>
            </>
          )}
        </p>
      </div>
    </div>
  )
}

export default LoginComponent

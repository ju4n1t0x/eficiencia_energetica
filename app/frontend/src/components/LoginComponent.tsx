import { useState } from 'react'
import './LoginComponent.css'

interface LoginComponentProps {
  onLogin?: () => void
}

const LoginComponent = ({ onLogin }: LoginComponentProps) => {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (isLogin) {
      console.log('Iniciando sesión con:', formData.username, formData.email)
      // Lógica de login (simulada por ahora)
      if (onLogin) onLogin()
    } else {
      console.log('Registrando usuario:', formData.username, formData.email)
      // Lógica de registro
      setIsLogin(true) // Después de registrar, lo mandamos al login
    }
  }

  return (
    <div className="auth-card">
      <div className="auth-header">
        <h2 className="auth-title">
          {isLogin ? 'Iniciar Sesión' : 'Registrarse'}
        </h2>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nombre de Usuario</label>
          <input 
            type="text" 
            name="username" 
            placeholder="Tu usuario"
            value={formData.username}
            onChange={handleChange}
            required 
          />
        </div>

        <div className="form-group">
          <label>Correo Electrónico</label>
          <input 
            type="email" 
            name="email" 
            placeholder="ejemplo@correo.com"
            value={formData.email}
            onChange={handleChange}
            required 
          />
        </div>

        {!isLogin && (
          <div className="form-group">
            <label>Contraseña</label>
            <input 
              type="password" 
              name="password" 
              placeholder="Crea una contraseña"
              value={formData.password}
              onChange={handleChange}
              required 
            />
          </div>
        )}

        <button type="submit" className="auth-button">
          {isLogin ? 'INGRESAR' : 'CREAR CUENTA'}
        </button>
      </form>

      <div className="auth-footer">
        <p className="auth-link">
          {isLogin ? (
            <>
              ¿No sos usuario? 
              <span className="auth-toggle" onClick={() => setIsLogin(false)}>
                Registrate acá
              </span>
            </>
          ) : (
            <>
              ¿Ya tenés cuenta? 
              <span className="auth-toggle" onClick={() => setIsLogin(true)}>
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

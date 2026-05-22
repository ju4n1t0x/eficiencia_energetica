import { useState } from 'react'
import { uploadDataset, login } from '../api'
import './CargaPage.css'

function CargaPage() {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [status, setStatus] = useState<{ type: 'idle' | 'success' | 'error', msg: string }>({ type: 'idle', msg: '' })

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const processFile = async (file: File) => {
      if (!file.name.endsWith('.csv')) {
          setStatus({ type: 'error', msg: 'Solo se permiten archivos .csv' })
          return
      }

      setIsUploading(true)
      setStatus({ type: 'idle', msg: '' })

      try {
          const token = await login()
          await uploadDataset(token, file)
          setStatus({ type: 'success', msg: '¡' + file.name + ' cargado correctamente!' })
      } catch (err: any) {
          setStatus({ type: 'error', msg: err.message || 'Error al subir archivo' })
      } finally {
          setIsUploading(false)
      }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const file = e.dataTransfer.files?.[0]
    if (file) processFile(file)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0]
      if (file) processFile(file)
  }

  return (
    <div className="center">
      <header className="page-header">
        <h1 className="title">CARGA DE DATOS</h1>
        <p className="subtitle">Actualizá el dataset del sistema para el re-entrenamiento</p>
      </header>
      
      <main className="page-body">
        <div 
          className={`upload-container ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input 
            type="file" 
            id="fileInput" 
            className="file-input" 
            accept=".csv"
            onChange={handleFileChange}
            disabled={isUploading}
          />
          
          <label htmlFor="fileInput" className={`upload-button ${isUploading ? 'disabled' : ''}`}>
            {isUploading ? 'Cargando...' : 'Seleccionar Archivo'}
          </label>
          
          <div className="drop-zone-message">
            {isUploading 
                ? 'Procesando dataset...' 
                : isDragging ? '¡Soltalo ahora!' : 'o arrastrá tu dataset acá'
            }
          </div>

          {status.type !== 'idle' && (
              <div className={`status-message ${status.type}`}>
                  {status.msg}
              </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default CargaPage

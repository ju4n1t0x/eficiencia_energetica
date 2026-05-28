import { useEffect, useState } from 'react'
import './Toast.css'

interface ToastProps {
  message: string
  type: 'success' | 'error'
  duration?: number
  onClose: () => void
}

const Toast = ({ message, type, duration = 3000, onClose }: ToastProps) => {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    setVisible(true)
    const timer = setTimeout(() => {
      setVisible(false)
      setTimeout(onClose, 300)
    }, duration)
    return () => clearTimeout(timer)
  }, [duration, onClose])

  return (
    <div className={`toast toast-${type} ${visible ? 'toast-visible' : ''}`}>
      {message}
    </div>
  )
}

export default Toast

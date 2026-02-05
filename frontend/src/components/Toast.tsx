/**
 * Toast Notification Component
 *
 * Displays temporary notification messages for user feedback.
 * Auto-dismisses after a set duration with smooth animations.
 */

'use client'

import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react'

export type ToastType = 'success' | 'error' | 'info'

export interface ToastProps {
  message: string
  type?: ToastType
  duration?: number
  onClose: () => void
}

export default function Toast({
  message,
  type = 'info',
  duration = 3000,
  onClose,
}: ToastProps) {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(onClose, 300) // Wait for fade-out animation
    }, duration)

    return () => clearTimeout(timer)
  }, [duration, onClose])

  const handleClose = () => {
    setIsVisible(false)
    setTimeout(onClose, 300)
  }

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'error':
        return <XCircle className="w-5 h-5 text-red-600" />
      case 'info':
        return <AlertCircle className="w-5 h-5 text-blue-600" />
    }
  }

  const getStyles = () => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200 text-green-900'
      case 'error':
        return 'bg-red-50 border-red-200 text-red-900'
      case 'info':
        return 'bg-blue-50 border-blue-200 text-blue-900'
    }
  }

  return (
    <div
      className={`
        fixed bottom-4 right-4 z-50
        flex items-center gap-3 p-4 pr-12
        border rounded-lg shadow-lg
        transition-all duration-300 ease-in-out
        ${getStyles()}
        ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'}
      `}
      role="alert"
      aria-live="polite"
    >
      {getIcon()}
      <span className="text-sm font-medium">{message}</span>
      <button
        onClick={handleClose}
        className="absolute top-2 right-2 p-1 rounded hover:bg-black/5 transition-colors"
        aria-label="Close notification"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}

/**
 * Toast Container Component
 *
 * Manages multiple toast notifications with stacking.
 */

export interface ToastMessage {
  id: string
  message: string
  type: ToastType
  duration?: number
}

export interface ToastContainerProps {
  toasts: ToastMessage[]
  onRemove: (id: string) => void
}

export function ToastContainer({ toasts, onRemove }: ToastContainerProps) {
  return (
    <div className="fixed bottom-0 right-0 z-50 p-4 space-y-2 pointer-events-none">
      {toasts.map((toast, index) => (
        <div
          key={toast.id}
          className="pointer-events-auto"
          style={{
            marginBottom: index * 8, // Stack toasts with slight offset
          }}
        >
          <Toast
            message={toast.message}
            type={toast.type}
            duration={toast.duration}
            onClose={() => onRemove(toast.id)}
          />
        </div>
      ))}
    </div>
  )
}

/**
 * Hook for managing toast notifications
 */

export function useToast() {
  const [toasts, setToasts] = useState<ToastMessage[]>([])

  const showToast = (message: string, type: ToastType = 'info', duration = 3000) => {
    const id = `toast-${Date.now()}-${Math.random()}`
    const newToast: ToastMessage = { id, message, type, duration }

    setToasts((prev) => [...prev, newToast])
  }

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id))
  }

  return {
    toasts,
    showToast,
    removeToast,
    success: (message: string, duration?: number) => showToast(message, 'success', duration),
    error: (message: string, duration?: number) => showToast(message, 'error', duration),
    info: (message: string, duration?: number) => showToast(message, 'info', duration),
  }
}

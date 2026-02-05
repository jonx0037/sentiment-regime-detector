/**
 * Export Button Component
 *
 * Reusable button with dropdown menu for exporting charts in multiple formats.
 * Displays PNG and SVG export options.
 */

'use client'

import { useState, useRef, useEffect } from 'react'
import { Download, FileImage } from 'lucide-react'

export interface ExportButtonProps {
  onExportPNG: () => void | Promise<void>
  onExportSVG: () => void | Promise<void>
  label?: string
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export default function ExportButton({
  onExportPNG,
  onExportSVG,
  label,
  size = 'sm',
  className = '',
}: ExportButtonProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isExporting, setIsExporting] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  const handleExport = async (exportFn: () => void | Promise<void>, format: string) => {
    try {
      setIsExporting(true)
      await exportFn()
      setIsOpen(false)
    } catch (error) {
      console.error(`Failed to export as ${format}:`, error)
    } finally {
      setIsExporting(false)
    }
  }

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-2 text-sm',
    lg: 'px-4 py-2 text-base',
  }

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  }

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isExporting}
        className={`
          flex items-center gap-2
          bg-white border border-gray-300 rounded-lg
          hover:bg-gray-50 hover:border-gray-400
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors
          ${sizeClasses[size]}
        `}
        aria-label="Export chart"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <Download className={iconSizes[size]} />
        {label && <span className="hidden sm:inline">{label}</span>}
      </button>

      {isOpen && (
        <div
          className="
            absolute right-0 mt-2 w-40
            bg-white border border-gray-200 rounded-lg shadow-lg
            z-10
            animate-in fade-in slide-in-from-top-2 duration-200
          "
          role="menu"
        >
          <button
            onClick={() => handleExport(onExportPNG, 'PNG')}
            disabled={isExporting}
            className="
              w-full flex items-center gap-2 px-4 py-2
              text-sm text-left
              hover:bg-gray-50
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-colors
              rounded-t-lg
            "
            role="menuitem"
          >
            <FileImage className="w-4 h-4 text-gray-600" />
            <span>Download PNG</span>
          </button>

          <div className="border-t border-gray-200" />

          <button
            onClick={() => handleExport(onExportSVG, 'SVG')}
            disabled={isExporting}
            className="
              w-full flex items-center gap-2 px-4 py-2
              text-sm text-left
              hover:bg-gray-50
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-colors
              rounded-b-lg
            "
            role="menuitem"
          >
            <FileImage className="w-4 h-4 text-gray-600" />
            <span>Download SVG</span>
          </button>
        </div>
      )}
    </div>
  )
}

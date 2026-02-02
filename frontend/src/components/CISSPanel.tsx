'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Area, ComposedChart } from 'recharts'
import { Activity, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'

interface CISSData {
  date: string
  ciss: number
  vix: number | null
}

interface CISSPanelProps {
  cissLevel?: number | null
  vixLevel?: number | null
  className?: string
}

const getCISSStatus = (ciss: number): { label: string; color: string; bgColor: string; icon: React.ReactNode } => {
  if (ciss < 0.15) {
    return {
      label: 'Calm',
      color: 'text-green-700',
      bgColor: 'bg-green-100',
      icon: <TrendingUp className="w-5 h-5 text-green-600" />,
    }
  } else if (ciss < 0.25) {
    return {
      label: 'Elevated',
      color: 'text-amber-700',
      bgColor: 'bg-amber-100',
      icon: <Activity className="w-5 h-5 text-amber-600" />,
    }
  } else if (ciss < 0.5) {
    return {
      label: 'Stressed',
      color: 'text-orange-700',
      bgColor: 'bg-orange-100',
      icon: <AlertTriangle className="w-5 h-5 text-orange-600" />,
    }
  } else {
    return {
      label: 'Crisis',
      color: 'text-red-700',
      bgColor: 'bg-red-100',
      icon: <TrendingDown className="w-5 h-5 text-red-600" />,
    }
  }
}

const getVIXStatus = (vix: number): { label: string; color: string } => {
  if (vix < 15) {
    return { label: 'Low Vol', color: 'text-green-600' }
  } else if (vix < 20) {
    return { label: 'Normal', color: 'text-blue-600' }
  } else if (vix < 30) {
    return { label: 'Elevated', color: 'text-amber-600' }
  } else {
    return { label: 'High Vol', color: 'text-red-600' }
  }
}

export default function CISSPanel({ cissLevel, vixLevel, className = '' }: CISSPanelProps) {
  const ciss = cissLevel ?? 0
  const vix = vixLevel ?? 0
  
  const cissStatus = getCISSStatus(ciss)
  const vixStatus = getVIXStatus(vix)
  
  // Format CISS as percentage
  const cissPercent = (ciss * 100).toFixed(1)
  
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${className}`}>
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <Activity className="w-5 h-5 text-blue-600" />
        Systemic Stress Indicators
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ECB CISS */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600">ECB CISS Index</span>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${cissStatus.bgColor} ${cissStatus.color}`}>
              {cissStatus.label}
            </span>
          </div>
          
          <div className="flex items-end gap-2">
            {cissStatus.icon}
            <span className="text-3xl font-bold text-gray-900">{cissPercent}%</span>
          </div>
          
          {/* CISS Gauge */}
          <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className={`absolute left-0 top-0 h-full rounded-full transition-all duration-500 ${
                ciss < 0.15 ? 'bg-green-500' : 
                ciss < 0.25 ? 'bg-amber-500' : 
                ciss < 0.5 ? 'bg-orange-500' : 'bg-red-500'
              }`}
              style={{ width: `${Math.min(ciss * 100, 100)}%` }}
            />
            {/* Crisis threshold marker */}
            <div className="absolute top-0 h-full w-0.5 bg-red-600" style={{ left: '50%' }} />
          </div>
          
          <div className="flex justify-between text-xs text-gray-500">
            <span>Calm (0%)</span>
            <span>Crisis (50%+)</span>
          </div>
          
          <p className="text-xs text-gray-500">
            Composite Indicator of Systemic Stress from ECB. Values above 0.5 indicate crisis conditions.
          </p>
        </div>
        
        {/* VIX */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600">CBOE VIX</span>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 ${vixStatus.color}`}>
              {vixStatus.label}
            </span>
          </div>
          
          <div className="flex items-end gap-2">
            <Activity className={`w-5 h-5 ${vixStatus.color}`} />
            <span className="text-3xl font-bold text-gray-900">{vix.toFixed(1)}</span>
          </div>
          
          {/* VIX Gauge */}
          <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className={`absolute left-0 top-0 h-full rounded-full transition-all duration-500 ${
                vix < 15 ? 'bg-green-500' : 
                vix < 20 ? 'bg-blue-500' : 
                vix < 30 ? 'bg-amber-500' : 'bg-red-500'
              }`}
              style={{ width: `${Math.min((vix / 80) * 100, 100)}%` }}
            />
            {/* Normal threshold marker */}
            <div className="absolute top-0 h-full w-0.5 bg-amber-600" style={{ left: `${(20 / 80) * 100}%` }} />
          </div>
          
          <div className="flex justify-between text-xs text-gray-500">
            <span>Low (0)</span>
            <span>Extreme (80+)</span>
          </div>
          
          <p className="text-xs text-gray-500">
            CBOE Volatility Index. "Fear gauge" measuring S&P 500 implied volatility.
          </p>
        </div>
      </div>
      
      {/* CISS-VIX Correlation Note */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg">
        <p className="text-xs text-blue-800">
          <strong>CISS-VIX Correlation:</strong> During COVID-19 (Mar 2020), correlation was 0.92. 
          CISS measures systemic stress while VIX measures implied volatility.
        </p>
      </div>
    </div>
  )
}

'use client'

import { useEffect, useState, ReactNode } from 'react'

interface FadeInProps {
  children: ReactNode
  delay?: number
  duration?: number
  className?: string
}

export default function FadeIn({
  children,
  delay = 0,
  duration = 300,
  className = '',
}: FadeInProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true)
    }, delay)

    return () => clearTimeout(timer)
  }, [delay])

  return (
    <div
      className={`transition-opacity ${className}`}
      style={{
        opacity: isVisible ? 1 : 0,
        transitionDuration: `${duration}ms`,
      }}
    >
      {children}
    </div>
  )
}

// Staggered fade-in for lists
export function StaggeredFadeIn({
  children,
  staggerDelay = 50,
  className = '',
}: {
  children: ReactNode[]
  staggerDelay?: number
  className?: string
}) {
  return (
    <>
      {children.map((child, index) => (
        <FadeIn key={index} delay={index * staggerDelay} className={className}>
          {child}
        </FadeIn>
      ))}
    </>
  )
}

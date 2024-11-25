'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

const simulationTypes = [
  { name: 'Normal Activity', endpoint: '/api/simulate/normal' },
  { name: 'Port Scan', endpoint: '/api/simulate/port-scan' },
  { name: 'Brute Force Attack', endpoint: '/api/simulate/brute-force' },
  { name: 'SQL Injection', endpoint: '/api/simulate/sql-injection' },
  { name: 'DDoS Attack', endpoint: '/api/simulate/ddos' },
]

export default function SimulationButtons() {
  const [loading, setLoading] = useState<string | null>(null)

  const simulateActivity = async (endpoint: string, name: string) => {
    setLoading(name)
    try {
      const response = await fetch(endpoint, { method: 'POST' })
      if (!response.ok) throw new Error('Simulation failed')
      // You might want to update some state or trigger a refresh of results here
    } catch (error) {
      console.error('Simulation error:', error)
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="grid grid-cols-2 gap-4">
      {simulationTypes.map((type) => (
        <Button
          key={type.name}
          onClick={() => simulateActivity(type.endpoint, type.name)}
          disabled={loading === type.name}
        >
          {loading === type.name ? 'Simulating...' : `Simulate ${type.name}`}
        </Button>
      ))}
    </div>
  )
}


'use client'

import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

interface AIAnalysisResult {
  timestamp: string
  activity: string
  risk_level: 'Low' | 'Medium' | 'High'
  details: string
}

export default function ResultsDisplay() {
  const [results, setResults] = useState<AIAnalysisResult[]>([])

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await fetch('/api/results')
        if (!response.ok) throw new Error('Failed to fetch results')
        const data = await response.json()
        setResults(data)
      } catch (error) {
        console.error('Error fetching results:', error)
      }
    }

    fetchResults()
    const intervalId = setInterval(fetchResults, 5000) // Refresh every 5 seconds

    return () => clearInterval(intervalId)
  }, [])

  return (
    <div className="w-full max-w-4xl mt-8">
      <h2 className="text-2xl font-bold mb-4">AI Analysis Results</h2>
      {results.map((result, index) => (
        <Card key={index} className="mb-4">
          <CardHeader>
            <CardTitle>{result.activity}</CardTitle>
          </CardHeader>
          <CardContent>
            <p><strong>Timestamp:</strong> {result.timestamp}</p>
            <p><strong>Risk Level:</strong> 
              <span className={`font-bold ${
                result.risk_level === 'Low' ? 'text-green-500' :
                result.risk_level === 'Medium' ? 'text-yellow-500' : 'text-red-500'
              }`}>
                {result.risk_level}
              </span>
            </p>
            <p><strong>Details:</strong> {result.details}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}


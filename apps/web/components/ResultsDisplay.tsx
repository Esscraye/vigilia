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
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/results`)
        if (!response.ok) {
          throw new Error('Failed to fetch results')
        }
        const data = await response.json()
        setResults(data.results || data)
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
    {results ? (
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>JSON Results</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="whitespace-pre-wrap">{JSON.stringify(results, null, 2)}</pre>
        </CardContent>
      </Card>
    ) : (
      <p>No results available.</p>
    )}
  </div>
  )
}


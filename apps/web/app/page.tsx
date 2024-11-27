import SimulationButtons from '../components/SimulationButtons'
import ResultsDisplay from '../components/ResultsDisplay'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold mb-8">IDS/IPS Simulation</h1>
      <SimulationButtons />
      <ResultsDisplay />
    </main>
  )
}


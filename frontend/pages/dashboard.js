import { useState } from 'react'

export default function Dashboard() {
  const [company, setCompany] = useState('')
  const [result, setResult] = useState(null)

  const handleEnrich = async () => {
    const res = await fetch('http://localhost:8000/enrich', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_name: company })
    })
    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="flex gap-2 mb-4">
        <input
          className="border p-2 flex-1"
          placeholder="Company Name"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        />
        <button className="bg-green-500 text-white p-2" onClick={handleEnrich}>
          Enrich
        </button>
      </div>
      {result && (
        <div className="border p-4">
          <p>Domain: {result.domain}</p>
          <p>Confidence: {result.confidence}</p>
          <p>Method: {result.method}</p>
        </div>
      )}
    </div>
  )
}

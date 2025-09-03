import React from 'react'

export default function AnalysisCard({ item }){
  return (
    <div className="border rounded p-4">
      <div className="text-sm text-gray-500">Risk Score</div>
      <div className="text-xl font-bold mb-2">{(item.risk_score*100).toFixed(1)}%</div>
      <div className="text-sm text-gray-500">Top features</div>
      <ul className="list-disc pl-6 mb-2">
        {Object.entries(item.features).slice(0,5).map(([k,v])=> <li key={k}>{k}: {v.toFixed(2)}</li>)}
      </ul>
      <div className="text-sm text-gray-500">Hints</div>
      <ul className="list-disc pl-6">
        {item.hints.map((h,i)=> <li key={i}>{h}</li>)}
      </ul>
    </div>
  )
}

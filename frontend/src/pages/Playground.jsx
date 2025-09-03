import React, { useState } from 'react'
import axios from 'axios'

export default function Playground({ API }){
  const [diff, setDiff] = useState(`diff --git a/app.py b/app.py
index e69de29..b6fc4c6 100644
--- a/app.py
+++ b/app.py
@@ -0,0 +1,6 @@
+def add(a,b):
+    if a and b:
+        return a+b
+    else:
+        return 0
+`)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function run(){
    setLoading(true)
    try{
      const { data } = await axios.post(API + '/analyze', { diff_text: diff })
      setResult(data)
    }catch(e){
      alert(e?.response?.data?.detail || e.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-2 text-sm text-gray-600">Paste a git unified diff below:</div>
      <textarea value={diff} onChange={e=>setDiff(e.target.value)} className="w-full h-56 p-3 border rounded font-mono text-sm" />
      <button onClick={run} disabled={loading} className="mt-3 px-4 py-2 rounded bg-blue-600 text-white">{loading?'Analyzing...':'Analyze'}</button>

      {result && (
        <div className="mt-6 space-y-4">
          <div className="p-4 rounded border">
            <div className="text-sm text-gray-500">Risk Score</div>
            <div className="text-2xl font-bold">{(result.risk_score*100).toFixed(1)}%</div>
          </div>

          <div className="p-4 rounded border">
            <div className="text-sm text-gray-500 mb-2">Top Features</div>
            <ul className="list-disc pl-6">
              {result.top_features.map((t,i)=>(<li key={i}>{t}</li>))}
            </ul>
          </div>

          <div className="p-4 rounded border">
            <div className="text-sm text-gray-500 mb-2">Hints</div>
            <ul className="list-disc pl-6">
              {result.hints.map((h,i)=>(<li key={i}>{h}</li>))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Playground from './pages/Playground.jsx'
import Dashboard from './pages/Dashboard.jsx'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App(){
  const [tab, setTab] = useState('playground')
  return (
    <div className="max-w-6xl mx-auto p-6">
      <header className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">PR Pilot</h1>
        <nav className="space-x-2">
          <button onClick={()=>setTab('playground')} className={"px-3 py-1 rounded " + (tab==='playground'?'bg-black text-white':'bg-gray-200')}>Playground</button>
          <button onClick={()=>setTab('dashboard')} className={"px-3 py-1 rounded " + (tab==='dashboard'?'bg-black text-white':'bg-gray-200')}>Dashboard</button>
        </nav>
      </header>
      {tab==='playground' ? <Playground API={API}/> : <Dashboard API={API}/>}
      <footer className="mt-10 text-sm text-gray-500">
        Built with FastAPI + React. Point the API via VITE_API_BASE.
      </footer>
    </div>
  )
}

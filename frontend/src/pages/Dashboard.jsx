import React, { useEffect, useState } from 'react'
import axios from 'axios'
import AnalysisCard from '../components/AnalysisCard.jsx'

export default function Dashboard({ API }){
  const [items, setItems] = useState([])
  useEffect(()=>{
    axios.get(API + '/analyses').then(r=> setItems(r.data))
  },[])
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {items.map((it)=> <AnalysisCard key={it.id} item={it} />)}
      {items.length===0 && <div className="text-gray-500">No analyses yet. Run one in the Playground.</div>}
    </div>
  )
}

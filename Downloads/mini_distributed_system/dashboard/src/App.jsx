import { useState, useEffect } from 'react'
import axios from 'axios'
import { Activity, Server, Play, Terminal, CheckCircle, XCircle, Clock } from 'lucide-react'

const API_URL = "http://127.0.0.1:8000/api"

function App() {
  const [jobs, setJobs] = useState([])
  const [workers, setWorkers] = useState([]) // We'll add worker list later
  const [command, setCommand] = useState("")
  const [loading, setLoading] = useState(false)

  // Fetch Jobs every 2 seconds (Simple polling)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const jobsRes = await axios.get(`${API_URL}/jobs/`)
        setJobs(jobsRes.data)
      } catch (err) {
        console.error("API Error", err)
      }
    }
    
    fetchData()
    const interval = setInterval(fetchData, 2000)
    return () => clearInterval(interval)
  }, [])

  const submitJob = async (e) => {
    e.preventDefault()
    if (!command) return
    
    setLoading(true)
    try {
      await axios.post(`${API_URL}/jobs/`, { command })
      setCommand("") // Clear input
    } catch (err) {
      alert("Failed to submit job")
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-8 max-w-5xl mx-auto font-sans">
      
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <Activity className="text-emerald-400 w-8 h-8" />
        <h1 className="text-3xl font-bold text-white tracking-tight">Mini Distributed System</h1>
        <span className="bg-slate-800 text-xs px-2 py-1 rounded text-slate-400 border border-slate-700">v1.0</span>
      </div>

      {/* Input Section */}
      <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-xl mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Terminal className="w-5 h-5 text-blue-400" /> Dispatch Job
        </h2>
        <form onSubmit={submitJob} className="flex gap-4">
          <input 
            type="text" 
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="e.g. echo 'Build Started' && sleep 5"
            className="flex-1 bg-slate-900 border border-slate-700 rounded px-4 py-3 text-white focus:outline-none focus:border-blue-500 font-mono"
          />
          <button 
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded font-medium flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <Play className="w-4 h-4" /> Run Job
          </button>
        </form>
      </div>

      {/* Jobs List */}
      <div className="grid gap-4">
        <h2 className="text-xl font-semibold text-slate-300">Recent Jobs</h2>
        
        {jobs.length === 0 ? (
          <div className="text-slate-500 text-center py-10 bg-slate-800/50 rounded-lg border border-slate-700 border-dashed">
            No jobs found. Start the engine! 
          </div>
        ) : (
          jobs.map(job => (
            <div key={job.id} className="bg-slate-800 p-4 rounded-lg border border-slate-700 flex items-center justify-between hover:bg-slate-750 transition-colors">
              <div className="flex items-center gap-4">
                <div className={`p-2 rounded-full ${
                  job.status === 'SUCCESS' ? 'bg-green-500/10 text-green-400' :
                  job.status === 'FAILED' ? 'bg-red-500/10 text-red-400' :
                  job.status === 'RUNNING' ? 'bg-blue-500/10 text-blue-400 animate-pulse' :
                  'bg-slate-700 text-slate-400'
                }`}>
                  {job.status === 'SUCCESS' && <CheckCircle className="w-5 h-5" />}
                  {job.status === 'FAILED' && <XCircle className="w-5 h-5" />}
                  {job.status === 'RUNNING' && <Activity className="w-5 h-5" />}
                  {job.status === 'QUEUED' && <Clock className="w-5 h-5" />}
                </div>
                
                <div>
                  <div className="font-mono text-sm text-slate-300 mb-1">Job #{job.id}</div>
                  <div className="font-mono text-emerald-400 font-bold">{job.command}</div>
                </div>
              </div>

              <div className="text-right">
                <div className={`text-xs font-bold px-2 py-1 rounded uppercase tracking-wider ${
                  job.status === 'SUCCESS' ? 'bg-green-900/30 text-green-400' :
                  job.status === 'FAILED' ? 'bg-red-900/30 text-red-400' :
                  job.status === 'RUNNING' ? 'bg-blue-900/30 text-blue-400' :
                  'bg-slate-700 text-slate-300'
                }`}>
                  {job.status}
                </div>
                <div className="text-xs text-slate-500 mt-1">
                  {job.worker_id ? `Worker: ${job.worker_id.slice(0, 8)}...` : 'Waiting for worker...'}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  )
}

export default App
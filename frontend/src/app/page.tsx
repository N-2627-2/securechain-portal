'use client';

import { useState, useEffect } from 'react';
import { checkBackendHealth, triggerQuarantine } from '@/lib/api';

export default function Home() {
  const [health, setHealth] = useState<{ status: string; service: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [nodeId, setNodeId] = useState('');
  const [quarantineResult, setQuarantineResult] = useState<string | null>(null);

  useEffect(() => {
    checkBackendHealth()
      .then(setHealth)
      .catch((err) => setError(err.message));
  }, []);

  const handleQuarantine = async (e: React.FormEvent) => {
    e.preventDefault();
    setQuarantineResult(null);
    try {
      const res = await triggerQuarantine({
        node_id: nodeId,
        reason: 'Manual SOC Operator Quarantine',
        approved_by: 'operator@securechain.local',
      });
      setQuarantineResult(`Quarantine active for node ${res.node_id} (ID: ${res.quarantine_id})`);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setQuarantineResult(`Error: ${err.message}`);
      } else {
        setQuarantineResult('An unexpected error occurred');
      }
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-slate-800 pb-4">
          <h1 className="text-3xl font-bold tracking-tight text-emerald-400">SecureChain Portal</h1>
          <p className="text-slate-400 text-sm mt-1">Decoupled Security Management & Asset Operations</p>
        </header>

        {/* Backend Status Widget */}
        <section className="bg-slate-900 p-6 rounded-lg border border-slate-800">
          <h2 className="text-lg font-semibold mb-2">Backend Connection Status</h2>
          {error ? (
            <div className="text-red-400 text-sm">Status: Disconnected ({error})</div>
          ) : health ? (
            <div className="text-emerald-400 text-sm">
              Status: Connected ({health.service} - {health.status.toUpperCase()})
            </div>
          ) : (
            <div className="text-slate-400 text-sm">Checking status...</div>
          )}
        </section>

        {/* Action Panel */}
        <section className="bg-slate-900 p-6 rounded-lg border border-slate-800">
          <h2 className="text-lg font-semibold mb-4">Node Quarantine Action</h2>
          <form onSubmit={handleQuarantine} className="flex gap-4 items-center">
            <input
              type="text"
              placeholder="Enter Node IP / ID (e.g., 10.20.10.5)"
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="bg-slate-950 border border-slate-700 text-slate-100 px-4 py-2 rounded focus:outline-none focus:border-emerald-500 text-sm flex-1"
              required
            />
            <button
              type="submit"
              className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded text-sm font-medium transition"
            >
              Isolate Node
            </button>
          </form>
          {quarantineResult && (
            <div className="mt-4 p-3 bg-slate-950 border border-slate-800 rounded text-sm font-mono text-slate-300">
              {quarantineResult}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
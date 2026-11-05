"use client";

import { useState, useEffect } from "react";

export default function NodeQuarantineForm() {
  const [nodeId, setNodeId] = useState("");
  const [reason, setReason] = useState("");
  const [severity, setSeverity] = useState<"low" | "medium" | "high" | "critical">("medium");
  const [approvedBy, setApprovedBy] = useState("");
  const [loading, setLoading] = useState(false);
  const [responseMsg, setResponseMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || "";
        const res = await fetch(`${baseUrl}/health`);
        setBackendOnline(res.ok);
      } catch {
        setBackendOnline(false);
      }
    };
    checkHealth();
  }, []);

  const handleIsolate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nodeId || !reason) return;

    setLoading(true);
    setResponseMsg(null);

    if ((severity === "high" || severity === "critical") && !approvedBy) {
      setResponseMsg({
        type: "error",
        text: "High or critical severity isolation requires an Approver Identity (email).",
      });
      setLoading(false);
      return;
    }

    try {
      const payload = {
        alert_id: crypto.randomUUID(),
        node_id: nodeId,
        site_id: "warehouse-1",
        reason: reason,
        severity: severity,
        approved_by: approvedBy || null,
        expires_in_minutes: 60,
      };

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

      const res = await fetch(`${apiUrl}/quarantine`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        const errorDetail = data.detail?.message || data.detail || "Failed to isolate node.";
        throw new Error(errorDetail);
      }

      setResponseMsg({
        type: "success",
        text: `Isolation started! Status: ${data.status} (Audit ID: ${data.audit_id})`,
      });

      setNodeId("");
      setReason("");
      setApprovedBy("");
    } catch (err: any) {
      setResponseMsg({ type: "error", text: err.message || "An unexpected error occurred." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 text-white p-6 rounded-lg max-w-lg mx-auto mt-8 border border-slate-800 shadow-2xl">
      {/* Backend Connection Indicator Header */}
      <div className="mb-4 flex items-center justify-between border-b border-slate-800 pb-3">
        <h2 className="text-xl font-bold text-emerald-400">Node Quarantine Action</h2>
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-slate-400">Backend:</span>
          <span
            className={`inline-block w-2.5 h-2.5 rounded-full ${
              backendOnline === null
                ? "bg-yellow-500 animate-pulse"
                : backendOnline
                ? "bg-emerald-500"
                : "bg-red-500"
            }`}
          />
          <span className="text-xs font-mono text-slate-300">
            {backendOnline === null ? "Checking..." : backendOnline ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>
      
      <form onSubmit={handleIsolate} className="flex flex-col gap-3">
        <div>
          <label className="block text-xs text-slate-400 mb-1">Target Node ID or IP</label>
          <input
            type="text"
            placeholder="e.g., sensor-wh1-0042 or 10.20.10.5"
            value={nodeId}
            onChange={(e) => setNodeId(e.target.value)}
            className="w-full bg-slate-800 text-white border border-slate-700 px-3 py-2 rounded text-sm focus:outline-none focus:border-emerald-500"
            disabled={loading}
            required
          />
        </div>

        <div>
          <label className="block text-xs text-slate-400 mb-1">Isolation Reason</label>
          <input
            type="text"
            placeholder="e.g., Unauthorized Modbus write detected"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            className="w-full bg-slate-800 text-white border border-slate-700 px-3 py-2 rounded text-sm focus:outline-none focus:border-emerald-500"
            disabled={loading}
            required
          />
        </div>

        <div className="flex gap-3">
          <div className="flex-1">
            <label className="block text-xs text-slate-400 mb-1">Severity</label>
            <select
              value={severity}
              onChange={(e) => setSeverity(e.target.value as any)}
              className="w-full bg-slate-800 text-white border border-slate-700 px-3 py-2 rounded text-sm focus:outline-none focus:border-emerald-500"
              disabled={loading}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          <div className="flex-1">
            <label className="block text-xs text-slate-400 mb-1">
              Approver Email {(severity === "high" || severity === "critical") && <span className="text-red-400">*</span>}
            </label>
            <input
              type="email"
              placeholder="ops.lead@example.com"
              value={approvedBy}
              onChange={(e) => setApprovedBy(e.target.value)}
              className="w-full bg-slate-800 text-white border border-slate-700 px-3 py-2 rounded text-sm focus:outline-none focus:border-emerald-500"
              disabled={loading}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !nodeId || !reason}
          className="mt-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white font-semibold py-2 rounded transition-colors text-sm"
        >
          {loading ? "Isolating Node..." : "Execute Node Isolation"}
        </button>
      </form>

      {responseMsg && (
        <div
          className={`mt-4 p-3 rounded text-sm ${
            responseMsg.type === "success"
              ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
              : "bg-red-950 text-red-300 border border-red-800"
          }`}
        >
          {responseMsg.text}
        </div>
      )}
    </div>
  );
}
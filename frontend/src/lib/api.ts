const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface AlertPayload {
  alert_id: string;
  severity: string;
  src_ip: string;
  sensor_id: string;
  rule_name: string;
  timestamp: string;
}

export interface QuarantinePayload {
  node_id: string;
  reason: string;
  approved_by: string;
  ttl_minutes?: number;
}

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error('Backend service is unreachable');
  }
  return response.json();
}

export async function sendAlert(payload: AlertPayload) {
  const response = await fetch(`${API_BASE_URL}/alerts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error('Failed to submit security alert');
  }
  return response.json();
}

export async function triggerQuarantine(payload: QuarantinePayload) {
  const response = await fetch(`${API_BASE_URL}/quarantine`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail?.message || 'Quarantine request denied');
  }
  return data;
}
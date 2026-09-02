import axios from 'axios';
import {
  HealthStatus,
  Agent,
  FinancialState,
  Policy,
  ProposalSummary,
  EvaluationPipelineResponse,
  PendingApproval,
  AuditReceipt,
  LedgerTransaction,
  GovernanceDecisionResult,
  ScenarioComparison
} from '../types';

// Use /api/v1 as the ONLY API namespace
const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health
  getHealth: async (): Promise<HealthStatus> => {
    const healthUrl = API_BASE.replace('/api/v1', '/health');
    try {
      const res = await axios.get(healthUrl);
      return res.data;
    } catch {
      const res = await axios.get('http://127.0.0.1:8000/health');
      return res.data;
    }
  },

  // Merchants
  getMerchants: async (): Promise<any[]> => {
    const res = await client.get('/merchants');
    return res.data;
  },
  getMerchant: async (merchantId: string): Promise<any> => {
    const res = await client.get(`/merchants/${merchantId}`);
    return res.data;
  },

  // Agents
  getAgents: async (merchantId?: string): Promise<Agent[]> => {
    const endpoint = merchantId ? `/agents/${merchantId}` : '/agents';
    const res = await client.get(endpoint);
    return res.data;
  },
  getAgent: async (id: string): Promise<Agent> => {
    const res = await client.get(`/agents/${id}`);
    return res.data;
  },

  // Financial State
  getFinancialState: async (merchantId?: string): Promise<FinancialState> => {
    const endpoint = merchantId ? `/financial-state/${merchantId}` : '/financial-state';
    const res = await client.get(endpoint);
    return res.data;
  },
  getFinancialHealth: async (merchantId?: string): Promise<any> => {
    const endpoint = merchantId ? `/financial-state/${merchantId}/health` : '/financial-state/health';
    const res = await client.get(endpoint);
    return res.data;
  },
  resetFinancialState: async (): Promise<FinancialState> => {
    const res = await client.post('/financial-state/reset');
    return res.data;
  },
  updateFinancialState: async (data: Partial<FinancialState>): Promise<FinancialState> => {
    const res = await client.put('/financial-state', data);
    return res.data;
  },
  addPendingOutflow: async (data: { agent_id: string; amount: number; action_type?: string; reason?: string }): Promise<FinancialState> => {
    const res = await client.post('/financial-state/add-pending-outflow', data);
    return res.data;
  },
  removePendingOutflow: async (data: { agent_id: string; amount: number; action_type?: string }): Promise<FinancialState> => {
    const res = await client.post('/financial-state/remove-pending-outflow', data);
    return res.data;
  },

  // Policies
  getPolicies: async (): Promise<Policy[]> => {
    const res = await client.get('/policies');
    return res.data;
  },
  togglePolicy: async (id: string): Promise<Policy> => {
    const res = await client.post(`/policies/${id}/toggle`);
    return res.data;
  },

  // Action Gateway & Pipeline
  getProposals: async (params?: { agent_id?: string; status?: string }): Promise<ProposalSummary[]> => {
    const res = await client.get('/actions', { params });
    return res.data;
  },
  proposeAction: async (data: {
    agent_id: string;
    action_type: string;
    amount: number;
    urgency: string;
    priority: number;
    confidence: number;
    reason: string;
    merchant_id?: string;
  }): Promise<EvaluationPipelineResponse> => {
    const endpoint = data.merchant_id ? `/actions/propose/${data.merchant_id}` : '/actions/propose';
    const res = await client.post(endpoint, data);
    return res.data;
  },
  getActionReasoning: async (actionId: string): Promise<EvaluationPipelineResponse> => {
    const res = await client.get(`/actions/status/${actionId}`);
    return res.data;
  },
  evaluateAction: async (actionId: string): Promise<EvaluationPipelineResponse> => {
    const res = await client.post(`/actions/${actionId}/evaluate`);
    return res.data;
  },
  getActionDecision: async (actionId: string): Promise<GovernanceDecisionResult> => {
    const res = await client.get(`/actions/${actionId}/decision`);
    return res.data;
  },
  executeAction: async (actionId: string): Promise<any> => {
    const res = await client.post(`/actions/execute/${actionId}`);
    return res.data;
  },

  // Conflicts
  getConflicts: async (): Promise<any[]> => {
    const res = await client.get('/conflicts');
    return res.data;
  },

  // Risk
  getRiskOverview: async (): Promise<any> => {
    const res = await client.get('/risk');
    return res.data;
  },

  // Simulations
  getSimulations: async (actionId: string): Promise<ScenarioComparison[]> => {
    const res = await client.get(`/simulations/${actionId}`);
    return res.data;
  },

  // Human Approvals
  getPendingApprovals: async (): Promise<PendingApproval[]> => {
    const res = await client.get('/approvals');
    return res.data;
  },
  approveAction: async (actionId: string, data: {
    human_reviewer?: string;
    approved_amount?: number;
    comments?: string;
  }): Promise<any> => {
    const res = await client.post(`/approvals/${actionId}/approve`, {
      ...data,
      decision: 'APPROVE'
    });
    return res.data;
  },
  rejectAction: async (actionId: string, data: {
    human_reviewer?: string;
    comments?: string;
  }): Promise<any> => {
    const res = await client.post(`/approvals/${actionId}/reject`, {
      ...data,
      decision: 'REJECT'
    });
    return res.data;
  },

  // Audit Trail
  getAuditRecords: async (params?: { agent_id?: string; decision?: string }): Promise<AuditReceipt[]> => {
    const res = await client.get('/audit', { params });
    return res.data;
  },
  getAuditReceipt: async (receiptNumber: string): Promise<AuditReceipt> => {
    const res = await client.get(`/audit/${receiptNumber}`);
    return res.data;
  },
  getLedgerTransactions: async (): Promise<LedgerTransaction[]> => {
    const res = await client.get('/audit/ledger/transactions');
    return res.data;
  },

  // Hero Demo
  setupHeroDemo: async (): Promise<any> => {
    const res = await client.post('/demo/setup');
    return res.data;
  },
  runHeroDemo: async (): Promise<EvaluationPipelineResponse> => {
    const res = await client.post('/demo/run');
    return res.data;
  },
  executeHeroApproval: async (): Promise<any> => {
    const res = await client.post('/demo/execute-hero');
    return res.data;
  }
};

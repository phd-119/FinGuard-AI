import React, { useState, useEffect } from 'react';
import { X, Send, Bot, Shield, AlertCircle } from 'lucide-react';
import { Agent } from '../types';

interface ProposeActionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: {
    agent_id: string;
    action_type: string;
    amount: number;
    urgency: string;
    priority: number;
    confidence: number;
    reason: string;
  }) => void;
  agents: Agent[];
  isSubmitting?: boolean;
  initialAgentId?: string;
}

export const ProposeActionModal: React.FC<ProposeActionModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  agents,
  isSubmitting = false,
  initialAgentId = 'payout_agent'
}) => {
  const [selectedAgent, setSelectedAgent] = useState(initialAgentId);
  const [actionType, setActionType] = useState('PAYOUT');
  const [amount, setAmount] = useState('250000');
  const [urgency, setUrgency] = useState('HIGH');
  const [priority, setPriority] = useState(2);
  const [confidence, setConfidence] = useState(0.92);
  const [reason, setReason] = useState(
    'Disbursement for warehouse cloud servers and supplier logistics clearance.'
  );

  useEffect(() => {
    if (isOpen) {
      const agentId = initialAgentId || 'payout_agent';
      setSelectedAgent(agentId);
      updateDefaultsForAgent(agentId);
    }
  }, [isOpen, initialAgentId]);

  const updateDefaultsForAgent = (agentId: string) => {
    if (agentId === 'payout_agent') {
      setActionType('PAYOUT');
      setAmount('400000');
      setUrgency('HIGH');
      setReason('Payment for supplier raw materials batch #INV-4902.');
    } else if (agentId === 'refund_agent') {
      setActionType('REFUND');
      setAmount('100000');
      setUrgency('HIGH');
      setReason('Customer dispute and damaged order refund batch #8820.');
    } else if (agentId === 'growth_agent') {
      setActionType('MARKETING_SPEND');
      setAmount('200000');
      setUrgency('MEDIUM');
      setReason('Meta and Google Ads festive acquisition budget top-up.');
    } else if (agentId === 'collections_agent') {
      setActionType('DEBT_RECOVERY');
      setAmount('45000');
      setUrgency('LOW');
      setReason('Early settlement discount disbursement to accelerate 60-day receivables.');
    } else if (agentId === 'treasury_agent') {
      setActionType('TREASURY_SWEEP');
      setAmount('150000');
      setUrgency('LOW');
      setReason('Yield optimization overnight sweep to liquid escrow reserve.');
    }
  };

  const handleAgentChange = (agentId: string) => {
    setSelectedAgent(agentId);
    updateDefaultsForAgent(agentId);
  };

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      agent_id: selectedAgent,
      action_type: actionType,
      amount: parseFloat(amount) || 10000,
      urgency,
      priority,
      confidence,
      reason
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-lg bg-[#0D1424] border border-slate-700 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-blue-500/10 text-brand-blue border border-blue-500/30">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-mono">
                FinGuard Action Gateway
              </h3>
              <p className="text-xs text-slate-400">
                Submit an autonomous AI financial action proposal for governance
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4 font-mono text-xs">
          {/* Agent Selection */}
          <div>
            <label className="block text-slate-300 font-semibold mb-1">
              Autonomous Agent Proposer:
            </label>
            <select
              value={selectedAgent}
              onChange={(e) => handleAgentChange(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-blue"
            >
              {agents.map((ag) => (
                <option key={ag.id} value={ag.id}>
                  {ag.name} (Trust: {ag.trust_score.toFixed(1)}/100)
                </option>
              ))}
            </select>
          </div>

          {/* Action Type & Amount */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">
                Action Type:
              </label>
              <input
                type="text"
                value={actionType}
                onChange={(e) => setActionType(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-blue"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">
                Proposed Amount (₹):
              </label>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                step="1000"
                min="100"
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-emerald-400 font-bold focus:outline-none focus:border-brand-blue"
              />
            </div>
          </div>

          {/* Urgency & Priority */}
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">
                Urgency:
              </label>
              <select
                value={urgency}
                onChange={(e) => setUrgency(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-blue"
              >
                <option value="LOW">LOW</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="HIGH">HIGH</option>
                <option value="CRITICAL">CRITICAL</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">
                Priority:
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(parseInt(e.target.value))}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-blue"
              >
                <option value="1">1 (Highest)</option>
                <option value="2">2 (High)</option>
                <option value="3">3 (Normal)</option>
                <option value="4">4 (Low)</option>
                <option value="5">5 (Lowest)</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-300 font-semibold mb-1">
                Confidence:
              </label>
              <input
                type="number"
                step="0.01"
                min="0.5"
                max="1.0"
                value={confidence}
                onChange={(e) => setConfidence(parseFloat(e.target.value))}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-brand-blue"
              />
            </div>
          </div>

          {/* Business Rationale */}
          <div>
            <label className="block text-slate-300 font-semibold mb-1">
              Business Rationale / Intent Description:
            </label>
            <textarea
              rows={3}
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-sans text-xs focus:outline-none focus:border-brand-blue"
              placeholder="Explain the commercial or operational obligation..."
            />
          </div>

          <div className="p-3 rounded-lg bg-blue-950/20 border border-blue-500/30 text-blue-300 text-[11px] flex items-center space-x-2">
            <Shield className="w-4 h-4 text-brand-blue shrink-0" />
            <span>
              All actions pass strictly through the FinGuard Gateway. Direct execution is prohibited.
            </span>
          </div>

          {/* Submit Button */}
          <div className="pt-2 flex items-center justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 rounded-lg bg-gradient-to-r from-brand-blue to-emerald-500 hover:from-blue-600 hover:to-emerald-600 text-white font-bold transition flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{isSubmitting ? 'Intercepting & Evaluating...' : 'Submit to FinGuard'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

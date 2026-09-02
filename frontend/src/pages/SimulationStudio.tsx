import React, { useState, useEffect } from 'react';
import { SlidersHorizontal, Sparkles, CheckCircle2, TrendingDown, ArrowRight } from 'lucide-react';
import { ProposalSummary, ScenarioComparison } from '../types';
import { api } from '../services/api';

export const SimulationStudio: React.FC = () => {
  const [proposals, setProposals] = useState<ProposalSummary[]>([]);
  const [selectedProposalId, setSelectedProposalId] = useState<string>('');
  const [scenarios, setScenarios] = useState<ScenarioComparison[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProposals();
  }, []);

  const loadProposals = async () => {
    try {
      const res = await api.getProposals();
      setProposals(res);
      if (res.length > 0) {
        setSelectedProposalId(res[0].id);
        fetchScenarios(res[0].id);
      }
    } catch (err) {
      console.error('Failed loading proposals:', err);
    }
  };

  const fetchScenarios = async (actionId: string) => {
    try {
      setLoading(true);
      const res = await api.getSimulations(actionId);
      setScenarios(res);
    } catch (err) {
      console.error('Failed loading simulations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectProposal = (id: string) => {
    setSelectedProposalId(id);
    fetchScenarios(id);
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  const currentProposal = proposals.find((p) => p.id === selectedProposalId);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <SlidersHorizontal className="w-5 h-5 text-emerald-400" />
          <h1 className="text-xl font-bold text-white font-mono">
            What-If Simulation Studio
          </h1>
        </div>
        <p className="text-xs text-slate-300 mt-1">
          Simulate counterfactual execution paths and liquidity curves before committing funds
        </p>
      </div>

      {/* Selector */}
      <div className="p-4 rounded-2xl bg-bg-card border border-bg-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 font-mono text-xs">
        <span className="text-slate-400">Select Financial Proposal to Simulate:</span>
        <select
          value={selectedProposalId}
          onChange={(e) => handleSelectProposal(e.target.value)}
          className="w-full sm:w-auto px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none"
        >
          {proposals.map((p) => (
            <option key={p.id} value={p.id}>
              {p.agent_name} — {p.action_type} ({formatINR(p.amount)})
            </option>
          ))}
        </select>
      </div>

      {/* Selected Proposal Preview */}
      {currentProposal && (
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-wrap items-center justify-between gap-3 font-mono text-xs">
          <div>
            <span className="text-slate-500 text-[10px] block">PROPOSED ACTION</span>
            <span className="font-bold text-white text-sm">
              {currentProposal.agent_name} ({currentProposal.action_type})
            </span>
          </div>
          <div>
            <span className="text-slate-500 text-[10px] block">ORIGINAL AMOUNT</span>
            <span className="font-bold text-emerald-400 text-sm">
              {formatINR(currentProposal.amount)}
            </span>
          </div>
          <div>
            <span className="text-slate-500 text-[10px] block">URGENCY</span>
            <span className="font-bold text-slate-200">{currentProposal.urgency}</span>
          </div>
          <div>
            <span className="text-slate-500 text-[10px] block">GOVERNANCE DECISION</span>
            <span className="font-bold text-amber-400">{currentProposal.final_decision || 'EVALUATING'}</span>
          </div>
        </div>
      )}

      {/* Scenarios Grid */}
      {loading ? (
        <div className="p-16 text-center text-slate-500 font-mono text-xs">
          Computing counterfactual simulations...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scenarios.map((sc) => (
            <div
              key={sc.scenario_id}
              className={`p-6 rounded-2xl border transition-all ${
                sc.is_recommended
                  ? 'bg-gradient-to-br from-emerald-950/30 via-bg-card to-slate-900 border-emerald-500/60 glow-emerald ring-1 ring-emerald-500/40'
                  : 'bg-bg-card border-slate-800'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block">
                    {sc.scenario_id.replace('_', ' ')}
                  </span>
                  <h3 className="text-base font-bold text-white font-mono mt-0.5">{sc.name}</h3>
                </div>
                {sc.is_recommended && (
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500 text-slate-950 font-mono">
                    SAFEST RECOMMENDATION
                  </span>
                )}
              </div>

              <p className="text-xs text-slate-300 font-sans mt-2 leading-relaxed">
                {sc.description}
              </p>

              {/* Metrics */}
              <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-2 pt-4 border-t border-slate-800/80 font-mono text-xs">
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/60">
                  <span className="text-slate-500 text-[10px] block">Immediate</span>
                  <span className="font-bold text-white">{formatINR(sc.immediate_outflow)}</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/60">
                  <span className="text-slate-500 text-[10px] block">Deferred</span>
                  <span className="font-bold text-amber-400">{formatINR(sc.deferred_outflow)}</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/60">
                  <span className="text-slate-500 text-[10px] block">Post Cash</span>
                  <span className="font-bold text-white">{formatINR(sc.remaining_cash)}</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/60">
                  <span className="text-slate-500 text-[10px] block">Risk Score</span>
                  <span className={sc.risk_score > 60 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>
                    {sc.risk_score.toFixed(0)}/100
                  </span>
                </div>
              </div>

              <div className="mt-3 flex items-center justify-between text-[11px] font-mono">
                <span className="text-slate-400">
                  Liquidity Ratio: <strong className="text-white">{sc.liquidity_ratio}x</strong>
                </span>
                <span className={sc.policy_compliant ? 'text-emerald-400 font-semibold' : 'text-rose-400 font-semibold'}>
                  {sc.policy_compliant ? '✓ Policy Compliant' : '✗ Breaches Reserve'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

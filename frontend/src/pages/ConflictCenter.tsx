import React, { useState, useEffect } from 'react';
import { GitFork, AlertTriangle, ShieldCheck, ArrowRight, Bot, Sparkles } from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

interface ConflictCenterProps {
  onSelectAction: (actionId: string) => void;
}

export const ConflictCenter: React.FC<ConflictCenterProps> = ({ onSelectAction }) => {
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConflicts();
  }, []);

  const loadConflicts = async () => {
    try {
      setLoading(true);
      const res = await api.getConflicts();
      setConflicts(res);
    } catch (err) {
      console.error('Failed loading conflicts:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <GitFork className="w-5 h-5 text-amber-400" />
          <h1 className="text-xl font-bold text-white font-mono">
            Cross-Agent Conflict Center
          </h1>
          <span className="text-[10px] px-2 py-0.5 rounded bg-brand-blue/20 text-blue-300 font-mono font-bold">
            CORE INNOVATION
          </span>
        </div>
        <p className="text-xs text-slate-300 mt-1 max-w-3xl">
          FinGuard evaluates the global combinatorial effect of all active AI agents. 
          Individually reasonable decisions (e.g. ₹4L payout + ₹2L marketing + ₹1L refund) 
          become dangerous when combined against a ₹6L cash pool with a ₹5L reserve.
        </p>
      </div>

      {/* Conflict Cards */}
      <div className="space-y-4">
        {conflicts.length === 0 ? (
          <div className="p-12 rounded-2xl bg-bg-card border border-bg-border text-center text-slate-500 font-mono text-xs">
            <ShieldCheck className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            <p>No active cross-agent liquidity conflicts detected.</p>
            <p className="text-slate-600 mt-1">Run the Hero Demo or submit simultaneous agent actions to test.</p>
          </div>
        ) : (
          conflicts.map((conf) => (
            <div
              key={conf.id}
              className="p-6 rounded-2xl bg-gradient-to-r from-amber-950/20 via-bg-card to-slate-900 border border-amber-500/40 glow-amber space-y-4"
            >
              {/* Card Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2 font-mono">
                      <span className="text-sm font-bold text-white uppercase">
                        {conf.conflict_type.replace(/_/g, ' ')}
                      </span>
                      <StatusBadge type="conflict" value={conf.severity} />
                    </div>
                    <span className="text-xs text-slate-400 font-mono">
                      Triggered by: {conf.agent_name} ({formatINR(conf.proposed_amount)})
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => onSelectAction(conf.proposal_id)}
                  className="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-mono text-xs flex items-center space-x-1.5 transition self-start sm:self-auto"
                >
                  <span>Inspect Reasoning</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Conflict Narrative */}
              <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs text-amber-200 leading-relaxed font-sans">
                <span className="font-mono font-bold text-amber-300 block mb-1">
                  Global Financial Threat Explanation:
                </span>
                {conf.explanation}
              </div>

              {/* Participating Agents Matrix */}
              <div className="space-y-2">
                <span className="text-xs font-mono text-slate-400 uppercase tracking-wider block">
                  Colliding Agent Proposals:
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 font-mono text-xs">
                  {conf.detected_agents &&
                    conf.detected_agents.map((ag: any, idx: number) => (
                      <div
                        key={idx}
                        className={`p-3.5 rounded-xl border ${
                          ag.is_current_subject
                            ? 'bg-blue-950/20 border-blue-500/40'
                            : 'bg-slate-900/60 border-slate-800'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-white flex items-center space-x-1.5">
                            <Bot className="w-3.5 h-3.5 text-brand-blue" />
                            <span>{ag.agent_name}</span>
                          </span>
                          {ag.is_current_subject && (
                            <span className="text-[10px] px-1 rounded bg-blue-500/20 text-blue-400">
                              SUBJECT
                            </span>
                          )}
                        </div>
                        <div className="mt-2 flex justify-between">
                          <span className="text-slate-400">{ag.action_type}</span>
                          <span className="text-emerald-400 font-bold">{formatINR(ag.amount)}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 font-sans mt-1 truncate">
                          {ag.reason}
                        </p>
                      </div>
                    ))}
                </div>
              </div>

              {/* Financial Balance Summary */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs pt-2 border-t border-slate-800">
                <div className="p-2.5 rounded-lg bg-bg-card border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Merchant Cash</span>
                  <span className="font-bold text-white">{formatINR(conf.available_cash)}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-bg-card border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Statutory Reserve</span>
                  <span className="font-bold text-amber-400">{formatINR(conf.required_reserve)}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-bg-card border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Aggregate Outflows</span>
                  <span className="font-bold text-rose-400">{formatINR(conf.aggregate_outflow)}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-bg-card border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Reserve Shortfall</span>
                  <span className="font-bold text-rose-400">{formatINR(conf.projected_shortfall)}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

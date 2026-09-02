import React, { useState, useEffect } from 'react';
import { Bot, Shield, Send, CheckCircle2, AlertTriangle, Activity, History } from 'lucide-react';
import { Agent } from '../types';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

interface AgentsHubProps {
  onProposeForAgent: (agentId: string) => void;
}

export const AgentsHub: React.FC<AgentsHubProps> = ({ onProposeForAgent }) => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const res = await api.getAgents();
      setAgents(res);
    } catch (err) {
      console.error('Failed to load agents:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-brand-blue" />
            <h1 className="text-xl font-bold text-white font-mono">
              Autonomous AI Financial Agents Fleet
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Simulated specialized autonomous financial agents operating under FinGuard supervision
          </p>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className="rounded-2xl bg-bg-card border border-bg-border p-5 space-y-4 hover:border-slate-700 transition"
          >
            {/* Header */}
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 rounded-xl bg-blue-500/10 text-brand-blue border border-blue-500/20">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white font-mono">{agent.name}</h3>
                  <span className="text-[10px] text-slate-400 font-mono block">ID: {agent.id}</span>
                </div>
              </div>
              <StatusBadge type="trust" value={agent.trust_level} />
            </div>

            {/* Objective */}
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
              <span className="text-slate-500 text-[10px] font-mono block mb-1 uppercase tracking-wider">
                Agent Objective
              </span>
              <p className="text-xs text-slate-200 leading-relaxed font-sans">{agent.objective}</p>
            </div>

            {/* Trust Meter */}
            <div className="space-y-1.5 font-mono text-xs">
              <div className="flex justify-between text-slate-400 text-[11px]">
                <span>Autonomous Trust Score</span>
                <span className="text-emerald-400 font-bold">{agent.trust_score.toFixed(1)}/100</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-brand-blue to-emerald-400 h-2 rounded-full transition-all"
                  style={{ width: `${Math.min(100, agent.trust_score)}%` }}
                />
              </div>
            </div>

            {/* Proposal Stats */}
            <div className="grid grid-cols-3 gap-2 text-center font-mono text-xs">
              <div className="p-2 rounded-lg bg-bg-subtle border border-slate-800">
                <span className="text-slate-500 text-[10px] block">Approved</span>
                <span className="text-emerald-400 font-bold">{agent.approved_proposals}</span>
              </div>
              <div className="p-2 rounded-lg bg-bg-subtle border border-slate-800">
                <span className="text-slate-500 text-[10px] block">Modified</span>
                <span className="text-amber-400 font-bold">{agent.modified_proposals}</span>
              </div>
              <div className="p-2 rounded-lg bg-bg-subtle border border-slate-800">
                <span className="text-slate-500 text-[10px] block">Blocked</span>
                <span className="text-rose-400 font-bold">{agent.blocked_proposals}</span>
              </div>
            </div>

            {/* Historical Telemetry Snippets */}
            {agent.historical_telemetry && agent.historical_telemetry.length > 0 && (
              <div className="space-y-1.5 pt-2 border-t border-slate-800 font-mono text-[11px]">
                <span className="text-slate-500 text-[10px] block uppercase">Recent Telemetry</span>
                {agent.historical_telemetry.slice(0, 2).map((tel, idx) => (
                  <div key={idx} className="flex justify-between items-center text-slate-300">
                    <span className="truncate max-w-[160px]">{tel.action}</span>
                    <div className="flex items-center space-x-1.5">
                      <span className="text-white font-bold">{formatINR(tel.amount)}</span>
                      <StatusBadge type="decision" value={tel.decision} className="text-[9px] px-1 py-0" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Quick Action Button */}
            <button
              onClick={() => onProposeForAgent(agent.id)}
              className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 hover:border-slate-600 font-mono text-xs flex items-center justify-center space-x-1.5 transition"
            >
              <Send className="w-3.5 h-3.5 text-brand-blue" />
              <span>Propose Action for {agent.name.split(' ')[0]}</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import {
  Activity,
  Search,
  Filter,
  PlusCircle,
  ArrowUpRight,
  Sparkles,
  Bot
} from 'lucide-react';
import { ProposalSummary, Agent } from '../types';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

interface ActionsFeedProps {
  onSelectAction: (actionId: string) => void;
  onOpenProposeModal: () => void;
}

export const ActionsFeed: React.FC<ActionsFeedProps> = ({
  onSelectAction,
  onOpenProposeModal
}) => {
  const [proposals, setProposals] = useState<ProposalSummary[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [agentFilter, setAgentFilter] = useState('ALL');
  const [decisionFilter, setDecisionFilter] = useState('ALL');

  useEffect(() => {
    loadActions();
  }, []);

  const loadActions = async () => {
    try {
      setLoading(true);
      const [propsRes, agentsRes] = await Promise.all([
        api.getProposals(),
        api.getAgents()
      ]);
      setProposals(propsRes);
      setAgents(agentsRes);
    } catch (err) {
      console.error('Failed to load actions:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  const filteredProposals = proposals.filter((p) => {
    if (agentFilter !== 'ALL' && p.agent_id !== agentFilter) return false;
    if (decisionFilter !== 'ALL' && p.final_decision !== decisionFilter) return false;
    if (search) {
      const q = search.toLowerCase();
      return (
        p.agent_name.toLowerCase().includes(q) ||
        p.action_type.toLowerCase().includes(q) ||
        p.reason.toLowerCase().includes(q) ||
        p.amount.toString().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            <h1 className="text-xl font-bold text-white font-mono">
              FinGuard Action Gateway & Stream
            </h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Complete stream of all autonomous AI agent proposals intercepted by the governance control plane
          </p>
        </div>

        <button
          onClick={onOpenProposeModal}
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-brand-blue to-emerald-500 hover:from-blue-600 hover:to-emerald-600 text-white font-bold font-mono text-xs flex items-center space-x-1.5 shadow-lg shadow-blue-500/20 transition self-start sm:self-auto"
        >
          <PlusCircle className="w-4 h-4" />
          <span>New Proposal</span>
        </button>
      </div>

      {/* Filters Bar */}
      <div className="p-4 rounded-2xl bg-bg-card border border-bg-border flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
          <input
            type="text"
            placeholder="Search proposals by keyword, amount, agent, or intent..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs font-mono focus:outline-none focus:border-brand-blue"
          />
        </div>

        <div className="flex items-center space-x-2">
          <select
            value={agentFilter}
            onChange={(e) => setAgentFilter(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 text-xs font-mono focus:outline-none"
          >
            <option value="ALL">All Agents</option>
            {agents.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name}
              </option>
            ))}
          </select>

          <select
            value={decisionFilter}
            onChange={(e) => setDecisionFilter(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 text-xs font-mono focus:outline-none"
          >
            <option value="ALL">All Decisions</option>
            <option value="ALLOW">ALLOW</option>
            <option value="MODIFY">MODIFY</option>
            <option value="DELAY">DELAY</option>
            <option value="ESCALATE">ESCALATE</option>
            <option value="BLOCK">BLOCK</option>
          </select>
        </div>
      </div>

      {/* Proposals Stream Cards */}
      <div className="space-y-3">
        {filteredProposals.length === 0 ? (
          <div className="p-12 rounded-2xl bg-bg-card border border-bg-border text-center text-slate-500 font-mono text-xs">
            No financial proposals match the active filters.
          </div>
        ) : (
          filteredProposals.map((prop) => (
            <div
              key={prop.id}
              onClick={() => onSelectAction(prop.id)}
              className="p-5 rounded-2xl bg-bg-card border border-bg-border hover:border-slate-700 transition cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              <div className="space-y-2 max-w-2xl">
                <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
                  <span className="font-bold text-white flex items-center space-x-1.5">
                    <Bot className="w-3.5 h-3.5 text-brand-blue" />
                    <span>{prop.agent_name}</span>
                  </span>
                  <span className="text-slate-600">•</span>
                  <span className="text-slate-400">{prop.action_type}</span>
                  <span className="text-slate-600">•</span>
                  <StatusBadge type="urgency" value={prop.urgency} />
                  <StatusBadge type="status" value={prop.status} />
                </div>

                <p className="text-xs text-slate-300 font-sans line-clamp-2">
                  {prop.reason}
                </p>

                <span className="text-[10px] text-slate-500 font-mono block">
                  Timestamp: {new Date(prop.created_at).toLocaleString()}
                </span>
              </div>

              <div className="flex items-center space-x-4 self-end sm:self-auto font-mono">
                <div className="text-right">
                  <span className="text-base font-extrabold text-emerald-400 block">
                    {formatINR(prop.amount)}
                  </span>
                  <div className="flex items-center justify-end space-x-1.5 mt-0.5">
                    <StatusBadge type="decision" value={prop.final_decision} />
                  </div>
                </div>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectAction(prop.id);
                  }}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                >
                  <ArrowUpRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

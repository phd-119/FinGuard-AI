import React, { useState, useEffect } from 'react';
import {
  Wallet,
  ShieldCheck,
  Bot,
  AlertTriangle,
  GitFork,
  CheckCircle2,
  TrendingUp,
  ArrowUpRight,
  Sparkles,
  Search,
  Filter
} from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';
import { HeroDemoBanner } from '../components/HeroDemoBanner';
import {
  FinancialState,
  Agent,
  ProposalSummary,
  EvaluationPipelineResponse
} from '../types';
import { api } from '../services/api';

interface DashboardProps {
  onSelectAction: (actionId: string) => void;
  onNavigateToHero: () => void;
  onRunHeroDemo: () => void;
  isHeroRunning: boolean;
  onOpenProposeModal: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  onSelectAction,
  onNavigateToHero,
  onRunHeroDemo,
  isHeroRunning,
  onOpenProposeModal
}) => {
  const [financialState, setFinancialState] = useState<FinancialState | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [proposals, setProposals] = useState<ProposalSummary[]>([]);
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterAgent, setFilterAgent] = useState('ALL');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [stateRes, agentsRes, propsRes, confRes] = await Promise.all([
        api.getFinancialState(),
        api.getAgents(),
        api.getProposals(),
        api.getConflicts()
      ]);
      setFinancialState(stateRes);
      setAgents(agentsRes);
      setProposals(propsRes);
      setConflicts(confRes);
    } catch (err) {
      console.error('Failed loading dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatINR = (val?: number) => {
    if (val === undefined || val === null) return '₹0';
    return `₹${val.toLocaleString('en-IN')}`;
  };

  const pendingApprovals = proposals.filter((p) => p.status === 'AWAITING_APPROVAL');
  const highRiskActions = proposals.filter((p) => (p.risk_score || 0) >= 65);

  const filteredProposals = proposals.filter((p) => {
    if (filterAgent !== 'ALL' && p.agent_id !== filterAgent) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Hero Showcase Banner */}
      <HeroDemoBanner
        onRunHeroDemo={onRunHeroDemo}
        onNavigateToHero={onNavigateToHero}
        isRunning={isHeroRunning}
      />

      {/* Top Financial & Governance Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard
          title="Merchant Cash"
          value={formatINR(financialState?.cash_balance)}
          subtitle="Total available float"
          icon={Wallet}
          variant="emerald"
        />
        <MetricCard
          title="Statutory Reserve"
          value={formatINR(financialState?.reserve_requirement)}
          subtitle="Mandatory protected floor"
          icon={ShieldCheck}
          variant="amber"
        />
        <MetricCard
          title="Free Liquidity"
          value={formatINR(financialState?.available_balance)}
          subtitle="Unreserved buffer"
          icon={TrendingUp}
          variant="blue"
        />
        <MetricCard
          title="Detected Conflicts"
          value={conflicts.length}
          subtitle="Multi-agent collisions"
          icon={GitFork}
          variant={conflicts.length > 0 ? 'rose' : 'default'}
        />
        <MetricCard
          title="Awaiting Approval"
          value={pendingApprovals.length}
          subtitle="Dual-control queue"
          icon={CheckCircle2}
          variant={pendingApprovals.length > 0 ? 'purple' : 'default'}
        />
      </div>

      {/* Active Autonomous Agents Pulse */}
      <div className="rounded-2xl bg-bg-card border border-bg-border p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Bot className="w-4 h-4 text-brand-blue" />
            <h3 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
              Autonomous AI Agents Fleet
            </h3>
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">
              5/5 ACTIVE & GOVERNED
            </span>
          </div>
          <span className="text-xs text-slate-400 font-mono hidden sm:inline">
            Governed by FinGuard Control Plane
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {agents.map((ag) => (
            <div
              key={ag.id}
              className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-white text-xs font-mono truncate">
                  {ag.name}
                </span>
                <StatusBadge type="trust" value={ag.trust_level} />
              </div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between text-slate-400 text-[11px] font-mono">
                  <span>Trust Score</span>
                  <span className="text-emerald-400 font-bold">{ag.trust_score.toFixed(1)}/100</span>
                </div>
                {/* Progress bar */}
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-brand-blue to-emerald-400 h-1.5 rounded-full"
                    style={{ width: `${Math.min(100, ag.trust_score)}%` }}
                  />
                </div>
                <div className="flex justify-between text-slate-400 text-[10px] pt-1">
                  <span>Proposals: {ag.total_proposals}</span>
                  <span className="text-slate-300 font-mono">
                    {ag.approved_proposals} approved
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Live Financial Actions & Gateway Stream */}
      <div className="rounded-2xl bg-bg-card border border-bg-border overflow-hidden">
        <div className="p-5 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
                Live Governed Financial Actions Stream
              </h3>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Click any action to inspect the transparent 10-stage reasoning chain
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <select
              value={filterAgent}
              onChange={(e) => setFilterAgent(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs font-mono text-slate-300 focus:outline-none"
            >
              <option value="ALL">All Agents</option>
              {agents.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-900/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="px-5 py-3">Agent</th>
                <th className="px-5 py-3">Action Type</th>
                <th className="px-5 py-3">Proposed Amount</th>
                <th className="px-5 py-3">Risk Score</th>
                <th className="px-5 py-3">Conflict</th>
                <th className="px-5 py-3">FinGuard Decision</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3 text-right">Reasoning Flow</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredProposals.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-5 py-8 text-center text-slate-500 font-mono">
                    No financial actions recorded yet. Use 'Propose Action' or 'Run FinGuard Demo'.
                  </td>
                </tr>
              ) : (
                filteredProposals.map((prop) => (
                  <tr
                    key={prop.id}
                    onClick={() => onSelectAction(prop.id)}
                    className="hover:bg-slate-800/40 cursor-pointer transition"
                  >
                    <td className="px-5 py-3.5 font-bold text-white whitespace-nowrap">
                      {prop.agent_name}
                    </td>
                    <td className="px-5 py-3.5 text-slate-300">
                      {prop.action_type}
                    </td>
                    <td className="px-5 py-3.5 font-bold text-emerald-400 whitespace-nowrap">
                      {formatINR(prop.amount)}
                    </td>
                    <td className="px-5 py-3.5">
                      {prop.risk_score !== null ? (
                        <div className="flex items-center space-x-2">
                          <span
                            className={`font-bold ${
                              prop.risk_score >= 70
                                ? 'text-rose-400'
                                : prop.risk_score >= 40
                                ? 'text-amber-400'
                                : 'text-emerald-400'
                            }`}
                          >
                            {prop.risk_score.toFixed(0)}/100
                          </span>
                          <StatusBadge type="risk" value={prop.risk_level} />
                        </div>
                      ) : (
                        <span className="text-slate-500">-</span>
                      )}
                    </td>
                    <td className="px-5 py-3.5">
                      <StatusBadge type="conflict" value={prop.conflict_severity} />
                    </td>
                    <td className="px-5 py-3.5">
                      <StatusBadge type="decision" value={prop.final_decision} />
                    </td>
                    <td className="px-5 py-3.5">
                      <StatusBadge type="status" value={prop.status} />
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectAction(prop.id);
                        }}
                        className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                      >
                        <ArrowUpRight className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
